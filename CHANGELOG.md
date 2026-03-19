# Changelog

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
