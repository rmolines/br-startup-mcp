# Changelog

## fontes-early-stage-bulk — PR #6 — 2026-03-19
**Type:** feat
**Node:** fontes-early-stage-bulk
**Commit:** `be19479`
**Decisions:** YC API is fully public (no auth) but `country=Brazil` filter is broken — must scrape all 232 pages and filter by `locations` field (49 BR companies confirmed); ABStartups returned HTTP 503 (site down) with no public API regardless; CVM crowdfunding data tracks platforms (73 active), not individual startup raises under RCVM 88; ACE domain acestartups.com.br was hijacked — correct domain is aceventures.com.br; InovAtiva domain is inovativa.online not inovativa.org.br; total reachable early-stage BR universe: 5,000–8,000 unique startups; see LEARNINGS.md#fontes-early-stage-bulk

## pipeline-crunchbase — PR #5 — 2026-03-19
**Type:** feat
**Node:** pipeline-crunchbase
**Commit:** `c1b42fb`
**Decisions:** Crunchbase Basic free tier only; retry+backoff on 429; manual CNPJ↔UUID matching via enrich tool; investors stored as JSON string in DuckDB; _check_api_key() reads env at runtime for test compatibility; see HANDOVER.md#pipeline-crunchbase

## pipeline-cnpj-receita — PR #4 — 2026-03-19
**Type:** feat
**Node:** pipeline-cnpj-receita
**Commit:** `ea3f86a`
**Decisions:** BrasilAPI chosen as Receita Federal proxy (free, no auth); cache-first strategy in get_startup_by_cnpj; search_startups is cache-only; participacao_pct always None (not provided by BrasilAPI); _STARTUP_COLS extracted to module constant

## pipeline-gov-aberto — PR #3 — 2026-03-19
**Type:** feat
**Node:** pipeline-gov-aberto
**Commit:** `128f30d`
**Decisions:** CVM uses Resolution 160 general offers (not CVM 88 crowdfunding — separate dataset not found); BNDES uses CKAN datastore API (2.3M records, CNPJs masked in indirect ops); auto-sync on empty cache; all logging to stderr only (MCP uses stdout for jsonrpc)

## casos-uso-vc — PR #2 — 2026-03-19
**Type:** feat
**Node:** casos-uso-vc
**Commit:** `fe32a05`
**Decisions:** see docs/vc-use-cases.md (workflows + tools) and docs/architecture.md (data model + stack)

## fontes-dados-startups — PR #1 — 2026-03-19
**Type:** feat
**Node:** fontes-dados-startups
**Commit:** `b9ab2f9`
**Decisions:** see docs/data-sources.md — Conclusão section
