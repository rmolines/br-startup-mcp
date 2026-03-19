"""MCP tools for Crunchbase investment data."""

import json
import os
from typing import Optional

import duckdb

from br_startup_mcp.data.crunchbase import (
    fetch_funding_rounds,
    load_investors_to_duckdb,
    load_rounds_to_duckdb,
    normalize_investor,
    normalize_round,
    query_investor_rounds,
    query_recent_rounds,
)

_NO_KEY_MSG = {
    "error": (
        "Crunchbase API key não configurada. "
        "Defina a variável de ambiente CRUNCHBASE_API_KEY para usar este tool."
    )
}


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")


def _has_key() -> bool:
    return bool(os.environ.get("CRUNCHBASE_API_KEY"))


def list_recent_rounds(
    limit: int = 20,
    category: Optional[str] = None,
    funding_stage: Optional[str] = None,
) -> str:
    """
    Busca rodadas de investimento recentes de startups brasileiras via Crunchbase API.

    Retorna mensagem clara se CRUNCHBASE_API_KEY não estiver configurada.
    """
    if not _has_key():
        return json.dumps(_NO_KEY_MSG, ensure_ascii=False)

    db = _db_path()

    try:
        # Fetch fresh data from Crunchbase and cache it
        entities = fetch_funding_rounds(limit=limit)
        if entities:
            rounds_raw = [normalize_round(e) for e in entities]
            rounds_clean = [r for r in rounds_raw if r is not None]
            if rounds_clean:
                load_rounds_to_duckdb(rounds_clean, db)

            # Also extract and cache investors from this batch
            investors_seen: dict[str, object] = {}
            for entity in entities:
                props = entity.get("properties", {})
                for inv in (props.get("investor_identifiers") or []):
                    inv_obj = normalize_investor(inv)
                    if inv_obj and inv_obj.id not in investors_seen:
                        investors_seen[inv_obj.id] = inv_obj
            if investors_seen:
                load_investors_to_duckdb(list(investors_seen.values()), db)

        # Query from DuckDB for the response (includes any previously cached rounds too)
        rounds = query_recent_rounds(db, limit=limit)
        return json.dumps(
            [r.model_dump(mode="json") for r in rounds],
            default=str,
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def get_investor_portfolio(investor_name: str, limit: int = 20) -> str:
    """
    Retorna portfólio de investimentos de um fundo/investidor pelo nome via dados Crunchbase cacheados.

    Busca no cache DuckDB rounds onde o investidor aparece.
    Retorna mensagem clara se CRUNCHBASE_API_KEY não estiver configurada.
    """
    if not _has_key():
        return json.dumps(_NO_KEY_MSG, ensure_ascii=False)

    db = _db_path()

    try:
        rounds = query_investor_rounds(db, investor_name=investor_name, limit=limit)
        result = {
            "investor_name": investor_name,
            "rounds_found": len(rounds),
            "rounds": [r.model_dump(mode="json") for r in rounds],
        }
        if not rounds:
            result["note"] = (
                "Nenhuma rodada encontrada para este investidor no cache. "
                "Use list_recent_rounds para popular o cache com dados recentes."
            )
        return json.dumps(result, default=str, ensure_ascii=False, indent=2)
    except duckdb.CatalogException:
        # Table doesn't exist yet
        return json.dumps(
            {
                "investor_name": investor_name,
                "rounds_found": 0,
                "rounds": [],
                "note": (
                    "Cache de rodadas ainda não populado. "
                    "Use list_recent_rounds primeiro para buscar dados do Crunchbase."
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
