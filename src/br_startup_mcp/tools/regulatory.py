"""MCP tools for regulatory government data (CVM and BNDES)."""

import json
import os
import sys
from typing import Optional

from br_startup_mcp.data.cvm import query_cvm_offers, sync_cvm
from br_startup_mcp.data.bndes import query_bndes_operations, sync_bndes


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")


def _ensure_cvm_data(db_path: str) -> None:
    """Trigger CVM sync if table is empty or missing."""
    import duckdb

    try:
        con = duckdb.connect(db_path, read_only=True)
        count = con.execute(
            "SELECT COUNT(*) FROM cvm_offers"
        ).fetchone()[0]
        con.close()
        if count == 0:
            raise ValueError("empty")
    except Exception:
        print("CVM cache empty — syncing ...", file=sys.stderr)
        sync_cvm(db_path=db_path)


def _ensure_bndes_data(db_path: str) -> None:
    """Trigger BNDES sync if table is empty or missing."""
    import duckdb

    try:
        con = duckdb.connect(db_path, read_only=True)
        count = con.execute(
            "SELECT COUNT(*) FROM bndes_operations"
        ).fetchone()[0]
        con.close()
        if count == 0:
            raise ValueError("empty")
    except Exception:
        print("BNDES cache empty — syncing ...", file=sys.stderr)
        sync_bndes(db_path=db_path, limit=500)


def get_cvm_crowdfunding_offers(
    cnpj: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
) -> str:
    """
    Return CVM public offers from the open data portal.

    Args:
        cnpj: Filter by issuer CNPJ (optional).
        status: Filter by offer status (optional, partial match).
        limit: Maximum number of results (default 20).

    Returns:
        JSON string with list of CvmOffer records.
    """
    db = _db_path()
    _ensure_cvm_data(db)
    offers = query_cvm_offers(db_path=db, cnpj=cnpj, status=status, limit=limit)
    result = [o.model_dump(mode="json") for o in offers]
    return json.dumps(result, default=str, ensure_ascii=False, indent=2)


def get_bndes_financing(
    cnpj: Optional[str] = None,
    produto: Optional[str] = None,
    limit: int = 20,
) -> str:
    """
    Return BNDES financing operations from the open data portal.

    Args:
        cnpj: Filter by client CNPJ (optional).
        produto: Filter by BNDES product name (optional, partial match).
        limit: Maximum number of results (default 20).

    Returns:
        JSON string with list of BndesOperation records.
    """
    db = _db_path()
    _ensure_bndes_data(db)
    ops = query_bndes_operations(db_path=db, cnpj=cnpj, produto=produto, limit=limit)
    result = [o.model_dump(mode="json") for o in ops]
    return json.dumps(result, default=str, ensure_ascii=False, indent=2)
