"""Crunchbase data client — fetch investment data from Crunchbase Basic API and cache in DuckDB.

Uses Crunchbase Basic (free tier) only. Requires CRUNCHBASE_API_KEY env var.
All functions degrade gracefully when the key is absent — return empty list or None.
All progress/errors go to stderr (never stdout — must not corrupt MCP stdio protocol).
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Optional

import duckdb
import httpx

from br_startup_mcp.models.entities import Investor, Round, make_id

CRUNCHBASE_BASE_URL = "https://api.crunchbase.com/api/v4"

# Module-level — re-read at call time via _check_api_key() so env changes in tests work
_CRUNCHBASE_API_KEY_ENV = "CRUNCHBASE_API_KEY"


def _check_api_key() -> Optional[str]:
    """Return CRUNCHBASE_API_KEY from env, or None if not set."""
    return os.environ.get(_CRUNCHBASE_API_KEY_ENV) or None


def _request(method: str, url: str, api_key: str, **kwargs) -> dict:
    """
    Make an HTTP request to Crunchbase API with retry + exponential backoff.

    Retries up to 3 times:
    - 429 (rate limit): sleep 60s then retry
    - Other HTTP errors: backoff 1s, 2s, 4s
    All progress goes to stderr.
    """
    max_retries = 3
    backoff = 1.0

    for attempt in range(max_retries + 1):
        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                if method.upper() == "POST":
                    resp = client.post(url, params={"user_key": api_key}, **kwargs)
                else:
                    params = kwargs.pop("params", {})
                    params["user_key"] = api_key
                    resp = client.get(url, params=params, **kwargs)

            if resp.status_code == 429:
                print(
                    f"Crunchbase rate limit hit (429) — sleeping 60s before retry {attempt + 1}/{max_retries}",
                    file=sys.stderr,
                )
                time.sleep(60)
                continue

            resp.raise_for_status()
            return resp.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {}
            if attempt < max_retries:
                print(
                    f"Crunchbase HTTP {e.response.status_code} — backoff {backoff}s (attempt {attempt + 1})",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError(f"Crunchbase API error after {max_retries} retries: {e}") from e

        except httpx.HTTPError as e:
            if attempt < max_retries:
                print(
                    f"Crunchbase HTTP error — backoff {backoff}s (attempt {attempt + 1}): {e}",
                    file=sys.stderr,
                )
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError(f"Crunchbase request failed after {max_retries} retries: {e}") from e

    return {}


def fetch_organizations_brazil(
    category: Optional[str] = None,
    funding_stage: Optional[str] = None,
    limit: int = 25,
) -> list[dict]:
    """
    Search for Brazilian organizations via Crunchbase API.

    Returns empty list if CRUNCHBASE_API_KEY is not set.
    Uses Crunchbase Basic free tier: POST /v4/searches/organizations
    """
    api_key = _check_api_key()
    if not api_key:
        print("CRUNCHBASE_API_KEY not set — skipping fetch_organizations_brazil", file=sys.stderr)
        return []

    url = f"{CRUNCHBASE_BASE_URL}/searches/organizations"
    query = [
        {
            "type": "predicate",
            "field_id": "location_identifiers",
            "operator_id": "includes",
            "values": ["Brazil"],
        }
    ]

    if category:
        query.append({
            "type": "predicate",
            "field_id": "category_groups",
            "operator_id": "includes",
            "values": [category],
        })

    if funding_stage:
        query.append({
            "type": "predicate",
            "field_id": "last_funding_type",
            "operator_id": "eq",
            "values": [funding_stage],
        })

    body = {
        "field_ids": [
            "uuid",
            "identifier",
            "short_description",
            "website_url",
            "categories",
            "num_employees_enum",
            "total_funding_usd",
            "last_funding_type",
            "last_funding_at",
            "location_identifiers",
        ],
        "query": query,
        "limit": limit,
    }

    print(f"Fetching organizations (Brazil) from Crunchbase (limit={limit}) ...", file=sys.stderr)
    try:
        response = _request("POST", url, api_key, json=body)
        entities = response.get("entities", [])
        print(f"Crunchbase organizations: {len(entities)} results", file=sys.stderr)
        return entities
    except Exception as e:
        print(f"fetch_organizations_brazil error: {e}", file=sys.stderr)
        return []


def fetch_funding_rounds(
    org_uuid: Optional[str] = None,
    limit: int = 25,
) -> list[dict]:
    """
    Search for funding rounds via Crunchbase API.

    Returns empty list if CRUNCHBASE_API_KEY is not set.
    Uses Crunchbase Basic free tier: POST /v4/searches/funding_rounds
    """
    api_key = _check_api_key()
    if not api_key:
        print("CRUNCHBASE_API_KEY not set — skipping fetch_funding_rounds", file=sys.stderr)
        return []

    url = f"{CRUNCHBASE_BASE_URL}/searches/funding_rounds"
    query = []

    if org_uuid:
        query.append({
            "type": "predicate",
            "field_id": "funded_organization_identifier",
            "operator_id": "includes",
            "values": [org_uuid],
        })

    body = {
        "field_ids": [
            "uuid",
            "identifier",
            "short_description",
            "funded_organization_identifier",
            "funded_organization_location",
            "investment_type",
            "announced_on",
            "money_raised",
            "pre_money_valuation",
            "post_money_valuation",
            "lead_investor_identifiers",
            "investor_identifiers",
            "is_equity",
        ],
        "query": query,
        "limit": limit,
    }

    print(
        f"Fetching funding rounds from Crunchbase (org={org_uuid or 'all'}, limit={limit}) ...",
        file=sys.stderr,
    )
    try:
        response = _request("POST", url, api_key, json=body)
        entities = response.get("entities", [])
        print(f"Crunchbase funding rounds: {len(entities)} results", file=sys.stderr)
        return entities
    except Exception as e:
        print(f"fetch_funding_rounds error: {e}", file=sys.stderr)
        return []


def fetch_organization_by_permalink(permalink: str) -> Optional[dict]:
    """
    Fetch a single organization from Crunchbase by permalink/slug.

    Returns None if CRUNCHBASE_API_KEY is not set or org not found.
    Uses Crunchbase Basic free tier: GET /v4/entities/organizations/{permalink}
    """
    api_key = _check_api_key()
    if not api_key:
        print("CRUNCHBASE_API_KEY not set — skipping fetch_organization_by_permalink", file=sys.stderr)
        return None

    url = f"{CRUNCHBASE_BASE_URL}/entities/organizations/{permalink}"
    field_ids = (
        "uuid,identifier,short_description,website_url,categories,"
        "num_employees_enum,total_funding_usd,last_funding_type,last_funding_at"
    )

    print(f"Fetching organization '{permalink}' from Crunchbase ...", file=sys.stderr)
    try:
        response = _request("GET", url, api_key, params={"field_ids": field_ids})
        if not response:
            return None
        props = response.get("properties")
        if props:
            print(f"Crunchbase org found: {props.get('identifier', {}).get('value', permalink)}", file=sys.stderr)
        return props
    except Exception as e:
        print(f"fetch_organization_by_permalink error: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Normalize functions
# ---------------------------------------------------------------------------

def _parse_date(value) -> Optional[object]:
    """Parse date from Crunchbase value dict or string."""
    if not value:
        return None
    # Crunchbase dates can be {"value": "2023-01-15", "precision": "day"} or plain string
    if isinstance(value, dict):
        value = value.get("value", "")
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip()[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _parse_usd(value) -> Optional[float]:
    """Parse USD amount from Crunchbase value dict or number."""
    if value is None:
        return None
    if isinstance(value, dict):
        # {"value": 5000000, "currency": "USD", "value_usd": 5000000}
        v = value.get("value_usd") or value.get("value")
        if v is None:
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def normalize_round(entity: dict, cnpj_empresa: Optional[str] = None) -> Optional[Round]:
    """Map a Crunchbase funding_round entity to the Round model."""
    try:
        props = entity.get("properties", {})

        round_id = entity.get("uuid") or props.get("uuid")
        if not round_id:
            # Fallback: generate from org uuid + announced date
            org_id = (props.get("funded_organization_identifier") or {}).get("uuid", "")
            announced = str(props.get("announced_on", {}).get("value", ""))
            round_id = make_id(org_id, announced)

        org_identifier = props.get("funded_organization_identifier") or {}
        crunchbase_org_uuid = org_identifier.get("uuid", "")
        company_name = org_identifier.get("value", "")

        # Investment type
        investment_type = props.get("investment_type") or {}
        if isinstance(investment_type, dict):
            round_type = investment_type.get("value", "unknown")
        else:
            round_type = str(investment_type) if investment_type else "unknown"

        announced_date = _parse_date(props.get("announced_on"))
        amount_usd = _parse_usd(props.get("money_raised"))
        pre_money = _parse_usd(props.get("pre_money_valuation"))
        post_money = _parse_usd(props.get("post_money_valuation"))

        # Lead investor
        lead_investors = props.get("lead_investor_identifiers") or []
        lead_investor_name = lead_investors[0].get("value") if lead_investors else None

        # All investors
        investor_identifiers = props.get("investor_identifiers") or []
        investors = [inv.get("value", "") for inv in investor_identifiers if inv.get("value")]

        is_equity = props.get("is_equity")
        if isinstance(is_equity, dict):
            is_equity = is_equity.get("value")

        return Round(
            id=round_id,
            cnpj_empresa=cnpj_empresa,
            crunchbase_org_uuid=crunchbase_org_uuid,
            company_name=company_name,
            round_type=round_type,
            announced_date=announced_date,
            amount_usd=amount_usd,
            pre_money_valuation_usd=pre_money,
            post_money_valuation_usd=post_money,
            lead_investor_name=lead_investor_name,
            investors=investors,
            is_equity=bool(is_equity) if is_equity is not None else None,
        )
    except Exception as e:
        print(f"normalize_round error: {e}", file=sys.stderr)
        return None


def normalize_investor(inv_identifier: dict) -> Optional[Investor]:
    """Map a Crunchbase investor identifier dict to the Investor model."""
    try:
        uuid = inv_identifier.get("uuid", "")
        name = inv_identifier.get("value", "")
        entity_def = inv_identifier.get("entity_def_id", "organization")

        if not uuid or not name:
            return None

        return Investor(
            id=uuid,
            crunchbase_uuid=uuid,
            name=name,
            type=entity_def,
        )
    except Exception as e:
        print(f"normalize_investor error: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# DuckDB schema & load functions
# ---------------------------------------------------------------------------

_CREATE_TABLE_ROUNDS = """
CREATE TABLE IF NOT EXISTS rounds (
    id VARCHAR PRIMARY KEY,
    cnpj_empresa VARCHAR,
    crunchbase_org_uuid VARCHAR,
    company_name VARCHAR,
    round_type VARCHAR,
    announced_date DATE,
    amount_usd DOUBLE,
    pre_money_valuation_usd DOUBLE,
    post_money_valuation_usd DOUBLE,
    lead_investor_name VARCHAR,
    investors VARCHAR,
    is_equity BOOLEAN
)
"""

_CREATE_TABLE_INVESTORS = """
CREATE TABLE IF NOT EXISTS investors (
    id VARCHAR PRIMARY KEY,
    crunchbase_uuid VARCHAR,
    name VARCHAR,
    type VARCHAR,
    country VARCHAR,
    city VARCHAR,
    cnpj_fundo VARCHAR,
    cvm_patrimonio_brl DOUBLE,
    cvm_administrador VARCHAR,
    website VARCHAR,
    description VARCHAR
)
"""

_UPSERT_ROUND = """
INSERT OR REPLACE INTO rounds
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_UPSERT_INVESTOR = """
INSERT OR REPLACE INTO investors
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_ROUND_COLS = [
    "id", "cnpj_empresa", "crunchbase_org_uuid", "company_name", "round_type",
    "announced_date", "amount_usd", "pre_money_valuation_usd", "post_money_valuation_usd",
    "lead_investor_name", "investors", "is_equity",
]

_INVESTOR_COLS = [
    "id", "crunchbase_uuid", "name", "type", "country", "city",
    "cnpj_fundo", "cvm_patrimonio_brl", "cvm_administrador", "website", "description",
]


def load_rounds_to_duckdb(rounds: list[Round], db_path: str) -> int:
    """Upsert Round records into DuckDB. Returns count inserted."""
    con = duckdb.connect(db_path)
    con.execute(_CREATE_TABLE_ROUNDS)
    rows = [
        (
            r.id,
            r.cnpj_empresa,
            r.crunchbase_org_uuid,
            r.company_name,
            r.round_type,
            r.announced_date,
            r.amount_usd,
            r.pre_money_valuation_usd,
            r.post_money_valuation_usd,
            r.lead_investor_name,
            json.dumps(r.investors),
            r.is_equity,
        )
        for r in rounds
    ]
    con.executemany(_UPSERT_ROUND, rows)
    con.close()
    return len(rows)


def load_investors_to_duckdb(investors: list[Investor], db_path: str) -> int:
    """Upsert Investor records into DuckDB. Returns count inserted."""
    con = duckdb.connect(db_path)
    con.execute(_CREATE_TABLE_INVESTORS)
    rows = [
        (
            i.id,
            i.crunchbase_uuid,
            i.name,
            i.type,
            i.country,
            i.city,
            i.cnpj_fundo,
            i.cvm_patrimonio_brl,
            i.cvm_administrador,
            i.website,
            i.description,
        )
        for i in investors
    ]
    con.executemany(_UPSERT_INVESTOR, rows)
    con.close()
    return len(rows)


# ---------------------------------------------------------------------------
# Query functions
# ---------------------------------------------------------------------------

def query_recent_rounds(db_path: str, limit: int = 20) -> list[Round]:
    """Query most recent Round records from DuckDB cache, ordered by announced_date desc."""
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception:
        return []
    try:
        sql = f"SELECT * FROM rounds ORDER BY announced_date DESC NULLS LAST LIMIT {int(limit)}"
        rows = con.execute(sql).fetchall()
        result = []
        for row in rows:
            d = dict(zip(_ROUND_COLS, row))
            d["investors"] = json.loads(d.get("investors") or "[]")
            result.append(Round(**d))
        return result
    except Exception:
        return []
    finally:
        con.close()


def query_rounds_by_org(db_path: str, crunchbase_org_uuid: str) -> list[Round]:
    """Query Round records for a specific organization UUID."""
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception:
        return []
    try:
        sql = "SELECT * FROM rounds WHERE crunchbase_org_uuid = ? ORDER BY announced_date DESC NULLS LAST"
        rows = con.execute(sql, [crunchbase_org_uuid]).fetchall()
        result = []
        for row in rows:
            d = dict(zip(_ROUND_COLS, row))
            d["investors"] = json.loads(d.get("investors") or "[]")
            result.append(Round(**d))
        return result
    except Exception:
        return []
    finally:
        con.close()


def query_investor_rounds(db_path: str, investor_name: str, limit: int = 20) -> list[Round]:
    """Query Round records where investor_name appears in the investors JSON field."""
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception:
        return []
    try:
        sql = f"SELECT * FROM rounds WHERE investors ILIKE ? LIMIT {int(limit)}"
        rows = con.execute(sql, [f"%{investor_name}%"]).fetchall()
        result = []
        for row in rows:
            d = dict(zip(_ROUND_COLS, row))
            d["investors"] = json.loads(d.get("investors") or "[]")
            result.append(Round(**d))
        return result
    except Exception:
        return []
    finally:
        con.close()
