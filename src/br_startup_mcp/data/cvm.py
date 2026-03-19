"""CVM data client — fetch equity offer data from CVM open data portal and cache in DuckDB."""

import io
import sys
import zipfile
from datetime import datetime
from typing import Optional

import duckdb
import httpx
import pandas as pd

from br_startup_mcp.models.entities import CvmOffer, make_id

# CVM open data URLs — oferta_resolucao_160 contains public offers (the closest to CVM 88 data)
CVM_OFERTA_ZIP_URL = (
    "https://dados.cvm.gov.br/dados/OFERTA/DISTRIB/DADOS/oferta_distribuicao.zip"
)
CVM_TARGET_FILE = "oferta_resolucao_160.csv"

_DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]


def _parse_date(value: str):
    """Try multiple date formats, return date or None."""
    if not value or pd.isna(value):
        return None
    value = str(value).strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(value[:10], fmt).date()
        except ValueError:
            continue
    return None


def _parse_float(value) -> Optional[float]:
    """Parse float from various formats."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return float(str(value).replace(",", ".").strip())
    except (ValueError, TypeError):
        return None


def fetch_cvm_offers_raw() -> list[dict]:
    """
    Download CVM public offers ZIP and return list of dicts.

    Downloads oferta_distribuicao.zip and parses oferta_resolucao_160.csv.
    All progress goes to stderr.
    """
    print(f"Fetching CVM offers from {CVM_OFERTA_ZIP_URL} ...", file=sys.stderr)
    try:
        with httpx.Client(follow_redirects=True, timeout=60.0) as client:
            resp = client.get(CVM_OFERTA_ZIP_URL)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Failed to fetch CVM data: {e}") from e

    print(f"Downloaded {len(resp.content):,} bytes — extracting ...", file=sys.stderr)
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    if CVM_TARGET_FILE not in zf.namelist():
        raise RuntimeError(
            f"Expected '{CVM_TARGET_FILE}' in ZIP, got: {zf.namelist()}"
        )

    with zf.open(CVM_TARGET_FILE) as f:
        raw = f.read().decode("latin-1", errors="replace")

    df = pd.read_csv(io.StringIO(raw), sep=";", dtype=str, low_memory=False)
    print(f"Parsed {len(df)} rows, {len(df.columns)} columns", file=sys.stderr)
    return df.to_dict(orient="records")


def normalize_cvm_offer(row: dict) -> Optional[CvmOffer]:
    """
    Map CVM CSV row to CvmOffer model.

    Columns in oferta_resolucao_160.csv:
    Numero_Requerimento, Rito_Requerimento, Numero_Processo, Data_requerimento,
    Data_Registro, Data_Encerramento, Status_Requerimento, Valor_Mobiliario,
    Tipo_requerimento, CNPJ_Emissor, Nome_Emissor, CNPJ_Lider, Nome_Lider,
    Grupo_Coordenador, Tipo_Oferta, ...
    """
    cnpj = str(row.get("CNPJ_Emissor", "") or "").strip()
    razao = str(row.get("Nome_Emissor", "") or "").strip()
    plataforma = str(row.get("Rito_Requerimento", "") or "Automático").strip()
    status = str(row.get("Status_Requerimento", "") or "").strip()

    if not cnpj or not razao or not status:
        return None

    data_registro = _parse_date(str(row.get("Data_Registro", "") or ""))
    if data_registro is None:
        return None

    # Try multiple value columns
    valor_alvo = _parse_float(
        row.get("Valor_Total_Registra") or row.get("Valor_Total") or 0
    )
    if valor_alvo is None:
        valor_alvo = 0.0

    valor_captado = _parse_float(row.get("Valor_Total_Captado") or None)
    data_enc = _parse_date(str(row.get("Data_Encerramento", "") or ""))
    tipo_vm = str(row.get("Valor_Mobiliario", "") or "").strip() or None

    offer_id = make_id(cnpj, str(data_registro), plataforma)

    try:
        return CvmOffer(
            id=offer_id,
            cnpj_emissora=cnpj,
            razao_social=razao,
            plataforma=plataforma,
            valor_alvo_brl=valor_alvo,
            valor_captado_brl=valor_captado,
            data_registro=data_registro,
            data_encerramento=data_enc,
            status=status,
            tipo_valor_mobiliario=tipo_vm,
        )
    except Exception as e:
        print(f"Skipping row — parse error: {e}", file=sys.stderr)
        return None


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS cvm_offers (
    id VARCHAR PRIMARY KEY,
    cnpj_emissora VARCHAR,
    razao_social VARCHAR,
    plataforma VARCHAR,
    valor_alvo_brl DOUBLE,
    valor_captado_brl DOUBLE,
    data_registro DATE,
    data_encerramento DATE,
    status VARCHAR,
    tipo_valor_mobiliario VARCHAR
)
"""

_UPSERT = """
INSERT OR REPLACE INTO cvm_offers
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def load_to_duckdb(offers: list[CvmOffer], db_path: str) -> int:
    """Upsert CvmOffer records into DuckDB. Returns count inserted."""
    con = duckdb.connect(db_path)
    con.execute(_CREATE_TABLE)
    rows = [
        (
            o.id,
            o.cnpj_emissora,
            o.razao_social,
            o.plataforma,
            o.valor_alvo_brl,
            o.valor_captado_brl,
            o.data_registro,
            o.data_encerramento,
            o.status,
            o.tipo_valor_mobiliario,
        )
        for o in offers
    ]
    con.executemany(_UPSERT, rows)
    con.close()
    return len(rows)


def sync_cvm(db_path: str = "./data/cache.duckdb") -> int:
    """Full pipeline: fetch → normalize → load. Returns record count."""
    raw = fetch_cvm_offers_raw()
    offers = [normalize_cvm_offer(r) for r in raw]
    offers = [o for o in offers if o is not None]
    print(f"Normalized {len(offers)} valid CvmOffer records", file=sys.stderr)
    n = load_to_duckdb(offers, db_path)
    print(f"Loaded {n} records to DuckDB at {db_path}", file=sys.stderr)
    return n


def query_cvm_offers(
    db_path: str,
    cnpj: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
) -> list[CvmOffer]:
    """Query CvmOffer records from DuckDB cache."""
    con = duckdb.connect(db_path, read_only=True)
    sql = "SELECT * FROM cvm_offers WHERE 1=1"
    params = []
    if cnpj:
        sql += " AND cnpj_emissora = ?"
        params.append(cnpj)
    if status:
        sql += " AND status ILIKE ?"
        params.append(f"%{status}%")
    sql += f" LIMIT {int(limit)}"
    try:
        rows = con.execute(sql, params).fetchall()
        cols = [
            "id", "cnpj_emissora", "razao_social", "plataforma",
            "valor_alvo_brl", "valor_captado_brl", "data_registro",
            "data_encerramento", "status", "tipo_valor_mobiliario",
        ]
        result = []
        for row in rows:
            d = dict(zip(cols, row))
            result.append(CvmOffer(**d))
        return result
    finally:
        con.close()
