"""MCP tools for Receita Federal CNPJ data."""

import json
import os
from typing import Optional

import duckdb

from br_startup_mcp.data.cnpj import (
    _clean_cnpj,
    get_startup_by_cnpj as _fetch_startup,
    query_startups,
)


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")


def get_startup_by_cnpj(cnpj: str, include_founders: bool = True) -> str:
    """Busca dados cadastrais e societários de uma startup pelo CNPJ via Receita Federal."""
    db = _db_path()
    cnpj_clean = _clean_cnpj(cnpj)
    startup = _fetch_startup(cnpj_clean, db_path=db)
    if startup is None:
        return json.dumps(
            {"error": f"CNPJ {cnpj} não encontrado"}, ensure_ascii=False
        )
    result = {"startup": startup.model_dump(mode="json")}
    if include_founders:
        try:
            con = duckdb.connect(db, read_only=True)
            rows = con.execute(
                "SELECT * FROM founders WHERE cnpj_empresa = ?", [cnpj_clean]
            ).fetchall()
            cols = [
                "id", "cnpj_empresa", "nome", "cpf_cnpj", "qualificacao",
                "participacao_pct", "data_entrada",
            ]
            result["founders"] = [dict(zip(cols, r)) for r in rows]
            con.close()
        except Exception:
            result["founders"] = []
    return json.dumps(result, default=str, ensure_ascii=False, indent=2)


def search_startups(
    cnae: Optional[str] = None,
    cidade: Optional[str] = None,
    estado: Optional[str] = None,
    data_abertura_min: Optional[str] = None,
    limit: int = 20,
) -> str:
    """Busca startups no cache local por CNAE, cidade, estado ou data de abertura."""
    db = _db_path()
    startups = query_startups(
        db_path=db,
        cnae=cnae,
        cidade=cidade,
        estado=estado,
        data_abertura_min=data_abertura_min,
        limit=limit,
    )
    return json.dumps(
        [s.model_dump(mode="json") for s in startups],
        default=str,
        ensure_ascii=False,
        indent=2,
    )
