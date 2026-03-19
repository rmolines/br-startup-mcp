"""MCP tools for regulatory government data (CVM and BNDES)."""

import json
import os
import sys
from typing import Optional

import duckdb

from br_startup_mcp.data.cvm import query_cvm_offers, sync_cvm
from br_startup_mcp.data.bndes import query_bndes_operations, sync_bndes


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")


def _ensure_data(db_path: str, table: str, sync_fn) -> None:
    """Trigger sync if table is empty or missing."""
    try:
        con = duckdb.connect(db_path, read_only=True)
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        con.close()
        if count == 0:
            raise ValueError("empty")
    except Exception:
        print(f"{table} cache empty — syncing ...", file=sys.stderr)
        sync_fn(db_path=db_path)


def get_cvm_crowdfunding_offers(
    cnpj: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
) -> str:
    """Return CVM public offers from the open data portal as JSON."""
    db = _db_path()
    _ensure_data(db, "cvm_offers", sync_cvm)
    offers = query_cvm_offers(db_path=db, cnpj=cnpj, status=status, limit=limit)
    return json.dumps([o.model_dump(mode="json") for o in offers], default=str, ensure_ascii=False, indent=2)


def get_bndes_financing(
    cnpj: Optional[str] = None,
    produto: Optional[str] = None,
    limit: int = 20,
) -> str:
    """Return BNDES financing operations from the open data portal as JSON."""
    db = _db_path()
    _ensure_data(db, "bndes_operations", lambda db_path: sync_bndes(db_path=db_path, limit=500))
    ops = query_bndes_operations(db_path=db, cnpj=cnpj, produto=produto, limit=limit)
    return json.dumps([o.model_dump(mode="json") for o in ops], default=str, ensure_ascii=False, indent=2)
