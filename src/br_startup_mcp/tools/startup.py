"""MCP tools for Receita Federal CNPJ data."""

import json
import os
from typing import Optional

import duckdb

from br_startup_mcp.data.cnpj import (
    _clean_cnpj,
    get_startup_by_cnpj as _fetch_startup,
    load_startup_to_duckdb,
    query_startups,
)


def _db_path() -> str:
    return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")


def _has_crunchbase_key() -> bool:
    return bool(os.environ.get("CRUNCHBASE_API_KEY"))


def get_startup_by_cnpj(
    cnpj: str,
    include_founders: bool = True,
    include_rounds: bool = False,
) -> str:
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

    if include_rounds:
        if not _has_crunchbase_key():
            result["rounds_note"] = (
                "Crunchbase API key não configurada. "
                "Defina CRUNCHBASE_API_KEY para incluir rodadas de investimento."
            )
        elif startup.crunchbase_uuid:
            try:
                from br_startup_mcp.data.crunchbase import query_rounds_by_org
                rounds = query_rounds_by_org(db, startup.crunchbase_uuid)
                result["rounds"] = [r.model_dump(mode="json") for r in rounds]
            except Exception:
                result["rounds"] = []
        else:
            result["rounds_note"] = (
                "Startup não possui crunchbase_uuid associado. "
                "Use enrich_startup_with_crunchbase para associar dados Crunchbase."
            )

    return json.dumps(result, default=str, ensure_ascii=False, indent=2)


def enrich_startup_with_crunchbase(cnpj: str, crunchbase_slug: str) -> str:
    """
    Enriquece dados de uma startup com informações do Crunchbase.

    Busca o perfil da organização pelo slug/permalink do Crunchbase e atualiza
    os campos crunchbase_uuid, total_funding_usd, last_funding_type, etc. na startup.

    Requer CRUNCHBASE_API_KEY configurada.
    """
    if not _has_crunchbase_key():
        return json.dumps(
            {
                "error": (
                    "Crunchbase API key não configurada. "
                    "Defina a variável de ambiente CRUNCHBASE_API_KEY para usar este tool."
                )
            },
            ensure_ascii=False,
        )

    db = _db_path()
    cnpj_clean = _clean_cnpj(cnpj)

    # Fetch startup from cache/API first
    startup = _fetch_startup(cnpj_clean, db_path=db)
    if startup is None:
        return json.dumps(
            {"error": f"CNPJ {cnpj} não encontrado na base de dados"}, ensure_ascii=False
        )

    # Fetch Crunchbase org data
    try:
        from br_startup_mcp.data.crunchbase import (
            fetch_organization_by_permalink,
            _parse_date as _cb_parse_date,
            _parse_usd as _cb_parse_usd,
        )
        props = fetch_organization_by_permalink(crunchbase_slug)
    except Exception as e:
        return json.dumps({"error": f"Erro ao buscar Crunchbase: {e}"}, ensure_ascii=False)

    if not props:
        return json.dumps(
            {"error": f"Organização '{crunchbase_slug}' não encontrada no Crunchbase"},
            ensure_ascii=False,
        )

    # Extract enrichment fields — reuse helpers from data/crunchbase.py
    crunchbase_uuid = props.get("uuid") or props.get("identifier", {}).get("uuid")
    website = props.get("website_url") or (props.get("website") or {}).get("value")
    descricao = props.get("short_description")
    total_funding_usd = _cb_parse_usd(props.get("total_funding_usd"))
    last_funding_type = props.get("last_funding_type")
    if isinstance(last_funding_type, dict):
        last_funding_type = last_funding_type.get("value")
    last_funding_date = _cb_parse_date(props.get("last_funding_at"))
    employee_count = props.get("num_employees_enum")
    if isinstance(employee_count, dict):
        employee_count = employee_count.get("value")
    categories_raw = props.get("categories") or []
    categorias = []
    for cat in categories_raw:
        if isinstance(cat, dict):
            v = cat.get("value") or cat.get("name")
            if v:
                categorias.append(v)
        elif isinstance(cat, str) and cat:
            categorias.append(cat)

    # Update startup object
    startup.crunchbase_uuid = crunchbase_uuid
    startup.crunchbase_slug = crunchbase_slug
    startup.website = website
    startup.descricao = descricao
    startup.total_funding_usd = total_funding_usd
    startup.last_funding_type = last_funding_type
    startup.last_funding_date = last_funding_date
    startup.employee_count = str(employee_count) if employee_count else None
    startup.categorias = categorias

    # Persist updated startup back to DuckDB
    try:
        load_startup_to_duckdb(startup, [], db)
    except Exception as e:
        return json.dumps(
            {"error": f"Erro ao salvar enriquecimento: {e}"}, ensure_ascii=False
        )

    return json.dumps(
        {
            "cnpj": cnpj_clean,
            "crunchbase_slug": crunchbase_slug,
            "crunchbase_uuid": crunchbase_uuid,
            "enriched": startup.model_dump(mode="json"),
        },
        default=str,
        ensure_ascii=False,
        indent=2,
    )


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
