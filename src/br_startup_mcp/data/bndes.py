"""BNDES data client — fetch financing operations from BNDES open data and cache in DuckDB."""

import sys
from datetime import datetime
from typing import Optional

import duckdb
import httpx

from br_startup_mcp.models.entities import BndesOperation, make_id

# BNDES CKAN API — operações de financiamento (operações indiretas automáticas)
BNDES_RESOURCE_ID = "612faa0b-b6be-4b2c-9317-da5dc2c0b901"
BNDES_DATASTORE_URL = "https://dadosabertos.bndes.gov.br/api/3/action/datastore_search"

_DATE_FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]


def _parse_date(value):
    """Parse date from various formats."""
    if not value:
        return None
    s = str(value).strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s[:19], fmt).date()
        except ValueError:
            continue
    return None


def _parse_float(value) -> Optional[float]:
    """Parse float safely."""
    if value is None:
        return None
    try:
        return float(str(value).replace(",", ".").strip())
    except (ValueError, TypeError):
        return None


def fetch_bndes_operations_raw(limit: int = 500) -> list[dict]:
    """
    Fetch BNDES financing operations via CKAN datastore API.

    Paginates to retrieve up to `limit` records.
    All progress to stderr.
    """
    print(
        f"Fetching BNDES operations (limit={limit}) from CKAN datastore ...",
        file=sys.stderr,
    )
    records: list[dict] = []
    offset = 0
    page_size = min(100, limit)

    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        while len(records) < limit:
            params = {
                "resource_id": BNDES_RESOURCE_ID,
                "limit": page_size,
                "offset": offset,
            }
            try:
                resp = client.get(BNDES_DATASTORE_URL, params=params)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise RuntimeError(f"Failed to fetch BNDES data: {e}") from e

            data = resp.json()
            if not data.get("success"):
                raise RuntimeError(f"CKAN API error: {data.get('error')}")

            page = data["result"]["records"]
            if not page:
                break

            records.extend(page)
            offset += len(page)
            print(
                f"  Fetched {len(records)} records so far ...", file=sys.stderr
            )

            if len(page) < page_size:
                break  # last page

    print(f"Total raw records fetched: {len(records)}", file=sys.stderr)
    return records[:limit]


def normalize_bndes_operation(row: dict) -> Optional[BndesOperation]:
    """
    Map BNDES CKAN row to BndesOperation model.

    BNDES CKAN fields (operações indiretas automáticas):
    - cliente: razao_social
    - cpf_cnpj: CNPJ (may be masked with **)
    - produto: produto_bndes
    - valor_da_operacao_em_reais: valor_brl
    - data_da_contratacao: data_contratacao
    - setor_bndes, porte_do_cliente, municipio, uf
    """
    cnpj = str(row.get("cpf_cnpj", "") or "").strip()
    razao = str(row.get("cliente", "") or "").strip()
    produto = str(row.get("produto", "") or "").strip()
    valor = _parse_float(row.get("valor_da_operacao_em_reais"))
    data_contratacao = _parse_date(row.get("data_da_contratacao"))

    if not cnpj or not razao or not produto or valor is None or data_contratacao is None:
        return None

    setor = str(row.get("setor_bndes", "") or "").strip() or None
    porte = str(row.get("porte_do_cliente", "") or "").strip() or None
    municipio = str(row.get("municipio", "") or "").strip() or None
    uf = str(row.get("uf", "") or "").strip() or None

    op_id = make_id(cnpj, str(data_contratacao), produto)

    try:
        return BndesOperation(
            id=op_id,
            cnpj_cliente=cnpj,
            razao_social=razao,
            produto_bndes=produto,
            valor_brl=valor,
            data_contratacao=data_contratacao,
            setor_bndes=setor,
            porte=porte,
            municipio=municipio,
            uf=uf,
        )
    except Exception as e:
        print(f"Skipping row — parse error: {e}", file=sys.stderr)
        return None


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS bndes_operations (
    id VARCHAR PRIMARY KEY,
    cnpj_cliente VARCHAR,
    razao_social VARCHAR,
    produto_bndes VARCHAR,
    valor_brl DOUBLE,
    data_contratacao DATE,
    setor_bndes VARCHAR,
    porte VARCHAR,
    municipio VARCHAR,
    uf VARCHAR
)
"""

_UPSERT = """
INSERT OR REPLACE INTO bndes_operations
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def load_to_duckdb(ops: list[BndesOperation], db_path: str) -> int:
    """Upsert BndesOperation records into DuckDB. Returns count inserted."""
    con = duckdb.connect(db_path)
    con.execute(_CREATE_TABLE)
    rows = [
        (
            o.id,
            o.cnpj_cliente,
            o.razao_social,
            o.produto_bndes,
            o.valor_brl,
            o.data_contratacao,
            o.setor_bndes,
            o.porte,
            o.municipio,
            o.uf,
        )
        for o in ops
    ]
    con.executemany(_UPSERT, rows)
    con.close()
    return len(rows)


def sync_bndes(db_path: str = "./data/cache.duckdb", limit: int = 500) -> int:
    """Full pipeline: fetch → normalize → load. Returns record count."""
    raw = fetch_bndes_operations_raw(limit=limit)
    ops = [normalize_bndes_operation(r) for r in raw]
    ops = [o for o in ops if o is not None]
    print(f"Normalized {len(ops)} valid BndesOperation records", file=sys.stderr)
    n = load_to_duckdb(ops, db_path)
    print(f"Loaded {n} records to DuckDB at {db_path}", file=sys.stderr)
    return n


def query_bndes_operations(
    db_path: str,
    cnpj: Optional[str] = None,
    produto: Optional[str] = None,
    limit: int = 20,
) -> list[BndesOperation]:
    """Query BndesOperation records from DuckDB cache."""
    con = duckdb.connect(db_path, read_only=True)
    sql = "SELECT * FROM bndes_operations WHERE 1=1"
    params = []
    if cnpj:
        sql += " AND cnpj_cliente = ?"
        params.append(cnpj)
    if produto:
        sql += " AND produto_bndes ILIKE ?"
        params.append(f"%{produto}%")
    sql += f" LIMIT {int(limit)}"
    try:
        rows = con.execute(sql, params).fetchall()
        cols = [
            "id", "cnpj_cliente", "razao_social", "produto_bndes",
            "valor_brl", "data_contratacao", "setor_bndes", "porte",
            "municipio", "uf",
        ]
        return [BndesOperation(**dict(zip(cols, row))) for row in rows]
    finally:
        con.close()
