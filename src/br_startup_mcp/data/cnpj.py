"""CNPJ data client — fetch company data from BrasilAPI (Receita Federal proxy) and cache in DuckDB."""

import json
import re
import sys
from datetime import datetime
from typing import Optional

import duckdb
import httpx

from br_startup_mcp.models.entities import Founder, Startup, make_id

BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"


def _clean_cnpj(cnpj: str) -> str:
    """Remove formatting from CNPJ — return digits only."""
    return re.sub(r"[.\-/\s]", "", cnpj.strip())


def fetch_cnpj_raw(cnpj: str) -> dict:
    """
    Fetch CNPJ data from BrasilAPI.

    BrasilAPI is a free, no-auth proxy for Receita Federal data.
    All progress/errors go to stderr.
    """
    clean = _clean_cnpj(cnpj)
    url = BRASILAPI_CNPJ_URL.format(cnpj=clean)
    print(f"Fetching CNPJ {clean} from BrasilAPI ...", file=sys.stderr)
    try:
        with httpx.Client(follow_redirects=True, timeout=15.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise RuntimeError(f"CNPJ {clean} não encontrado (404)") from e
        raise RuntimeError(f"BrasilAPI returned {e.response.status_code} for CNPJ {clean}") from e
    except httpx.HTTPError as e:
        raise RuntimeError(f"Failed to fetch CNPJ {clean}: {e}") from e

    data = resp.json()
    print(f"Fetched CNPJ {clean}: {data.get('razao_social', '?')}", file=sys.stderr)
    return data


def _parse_date(value: str):
    """Parse YYYY-MM-DD date string, return date or None."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value).strip()[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def normalize_startup(data: dict) -> Optional[Startup]:
    """Map BrasilAPI CNPJ response dict to Startup model."""
    try:
        cnpj = _clean_cnpj(str(data.get("cnpj", "") or ""))
        razao_social = str(data.get("razao_social", "") or "").strip()
        situacao = str(data.get("descricao_situacao_cadastral", "") or "").strip()
        data_abertura = _parse_date(str(data.get("data_inicio_atividade", "") or ""))
        cidade = str(data.get("municipio", "") or "").strip()
        estado = str(data.get("uf", "") or "").strip()
        natureza_juridica = str(data.get("natureza_juridica", "") or "").strip()
        porte = str(data.get("porte", "") or "").strip()

        if not all([cnpj, razao_social, situacao, data_abertura, cidade, estado, natureza_juridica, porte]):
            print(
                f"normalize_startup: missing required fields for {cnpj} — skipping",
                file=sys.stderr,
            )
            return None

        # Capital social
        try:
            capital_social_brl = float(data.get("capital_social") or 0)
        except (ValueError, TypeError):
            capital_social_brl = 0.0

        # CNAE principal (int from API → zero-padded 7-digit string)
        cnae_raw = data.get("cnae_fiscal")
        try:
            cnae_principal = f"{int(cnae_raw):07d}" if cnae_raw is not None else "0000000"
        except (ValueError, TypeError):
            cnae_principal = "0000000"

        # CNAEs secundários: list of dicts with "codigo" key
        cnaes_raw = data.get("cnaes_secundarios") or []
        cnaes_secundarios = []
        for item in cnaes_raw:
            if isinstance(item, dict) and item.get("codigo"):
                try:
                    cnaes_secundarios.append(f"{int(item['codigo']):07d}")
                except (ValueError, TypeError):
                    cnaes_secundarios.append(str(item["codigo"]))

        return Startup(
            cnpj=cnpj,
            razao_social=razao_social,
            nome_fantasia=str(data.get("nome_fantasia", "") or "").strip() or None,
            situacao_cadastral=situacao,
            data_abertura=data_abertura,
            capital_social_brl=capital_social_brl,
            cnae_principal=cnae_principal,
            cnaes_secundarios=cnaes_secundarios,
            natureza_juridica=natureza_juridica,
            porte=porte,
            endereco_logradouro=str(data.get("logradouro", "") or "").strip() or None,
            cidade=cidade,
            estado=estado,
            cep=str(data.get("cep", "") or "").strip() or None,
            updated_at=datetime.utcnow(),
        )
    except Exception as e:
        print(f"normalize_startup error: {e}", file=sys.stderr)
        return None


def normalize_founder(socio: dict, cnpj_empresa: str) -> Optional[Founder]:
    """Map BrasilAPI QSA (quadro societário) item to Founder model."""
    try:
        nome = str(socio.get("nome_socio", "") or "").strip()
        qualificacao = str(socio.get("qualificacao_socio", "") or "").strip()

        if not nome or not qualificacao:
            return None

        cpf_cnpj = str(socio.get("cnpj_cpf_do_socio", "") or "").strip() or None
        data_entrada = _parse_date(str(socio.get("data_entrada_sociedade", "") or ""))
        founder_id = make_id(cnpj_empresa, nome)

        return Founder(
            id=founder_id,
            cnpj_empresa=cnpj_empresa,
            nome=nome,
            cpf_cnpj=cpf_cnpj,
            qualificacao=qualificacao,
            participacao_pct=None,
            data_entrada=data_entrada,
        )
    except Exception as e:
        print(f"normalize_founder error: {e}", file=sys.stderr)
        return None


_CREATE_TABLE_STARTUPS = """
CREATE TABLE IF NOT EXISTS startups (
    cnpj VARCHAR PRIMARY KEY,
    razao_social VARCHAR,
    nome_fantasia VARCHAR,
    situacao_cadastral VARCHAR,
    data_abertura DATE,
    capital_social_brl DOUBLE,
    cnae_principal VARCHAR,
    cnaes_secundarios VARCHAR,
    natureza_juridica VARCHAR,
    porte VARCHAR,
    endereco_logradouro VARCHAR,
    cidade VARCHAR,
    estado VARCHAR,
    cep VARCHAR,
    updated_at TIMESTAMP
)
"""

_CREATE_TABLE_FOUNDERS = """
CREATE TABLE IF NOT EXISTS founders (
    id VARCHAR PRIMARY KEY,
    cnpj_empresa VARCHAR,
    nome VARCHAR,
    cpf_cnpj VARCHAR,
    qualificacao VARCHAR,
    participacao_pct DOUBLE,
    data_entrada DATE
)
"""

_UPSERT_STARTUP = """
INSERT OR REPLACE INTO startups
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

_UPSERT_FOUNDER = """
INSERT OR REPLACE INTO founders
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

_STARTUP_COLS = [
    "cnpj", "razao_social", "nome_fantasia", "situacao_cadastral",
    "data_abertura", "capital_social_brl", "cnae_principal",
    "cnaes_secundarios", "natureza_juridica", "porte",
    "endereco_logradouro", "cidade", "estado", "cep", "updated_at",
]


def load_startup_to_duckdb(
    startup: Startup, founders: list[Founder], db_path: str
) -> None:
    """Upsert Startup and Founder records into DuckDB."""
    con = duckdb.connect(db_path)
    con.execute(_CREATE_TABLE_STARTUPS)
    con.execute(_CREATE_TABLE_FOUNDERS)

    con.execute(
        _UPSERT_STARTUP,
        [
            startup.cnpj,
            startup.razao_social,
            startup.nome_fantasia,
            startup.situacao_cadastral,
            startup.data_abertura,
            startup.capital_social_brl,
            startup.cnae_principal,
            json.dumps(startup.cnaes_secundarios),
            startup.natureza_juridica,
            startup.porte,
            startup.endereco_logradouro,
            startup.cidade,
            startup.estado,
            startup.cep,
            startup.updated_at,
        ],
    )

    for f in founders:
        con.execute(
            _UPSERT_FOUNDER,
            [
                f.id,
                f.cnpj_empresa,
                f.nome,
                f.cpf_cnpj,
                f.qualificacao,
                f.participacao_pct,
                f.data_entrada,
            ],
        )

    con.close()


def get_startup_by_cnpj(cnpj: str, db_path: str) -> Optional[Startup]:
    """
    Get Startup by CNPJ — cache-first strategy.

    1. Try DuckDB cache first.
    2. On miss, fetch from BrasilAPI, normalize, cache, return.
    3. On BrasilAPI 404, return None.
    """
    clean = _clean_cnpj(cnpj)

    # Try cache first
    try:
        con = duckdb.connect(db_path, read_only=True)
        row = con.execute("SELECT * FROM startups WHERE cnpj = ?", [clean]).fetchone()
        con.close()
        if row:
            d = dict(zip(_STARTUP_COLS, row))
            d["cnaes_secundarios"] = json.loads(d["cnaes_secundarios"] or "[]")
            return Startup(**d)
    except Exception:
        pass  # table doesn't exist yet — fetch from API

    # Fetch from BrasilAPI
    try:
        data = fetch_cnpj_raw(clean)
    except RuntimeError as e:
        if "404" in str(e):
            return None
        raise

    startup = normalize_startup(data)
    if startup is None:
        return None

    founders_raw = data.get("qsa") or []
    founders = [f for f in [normalize_founder(s, clean) for s in founders_raw] if f]

    load_startup_to_duckdb(startup, founders, db_path)
    return startup


def query_startups(
    db_path: str,
    cnae: Optional[str] = None,
    cidade: Optional[str] = None,
    estado: Optional[str] = None,
    data_abertura_min: Optional[str] = None,
    limit: int = 20,
) -> list[Startup]:
    """Query Startup records from DuckDB cache with optional filters."""
    try:
        con = duckdb.connect(db_path, read_only=True)
    except Exception:
        return []

    try:
        sql = "SELECT * FROM startups WHERE 1=1"
        params = []
        if cnae:
            sql += " AND cnae_principal ILIKE ?"
            params.append(f"{cnae}%")
        if cidade:
            sql += " AND cidade ILIKE ?"
            params.append(f"%{cidade}%")
        if estado:
            sql += " AND estado = ?"
            params.append(estado.upper())
        if data_abertura_min:
            sql += " AND data_abertura >= ?"
            params.append(data_abertura_min)
        sql += f" LIMIT {int(limit)}"

        rows = con.execute(sql, params).fetchall()
        result = []
        for row in rows:
            d = dict(zip(_STARTUP_COLS, row))
            d["cnaes_secundarios"] = json.loads(d["cnaes_secundarios"] or "[]")
            result.append(Startup(**d))
        return result
    except Exception:
        return []
    finally:
        con.close()
