---
predicate: "O agente não consegue integrar a API do Crunchbase para dados de rodadas de investimento, valuations e investidores de startups brasileiras"
satisfied_date: 2026-03-19
satisfied_by: ship
---

## What was achieved
O MCP server agora integra a API Crunchbase Basic (free tier): um agente VC pode buscar rodadas de investimento recentes (`list_recent_rounds`), consultar o portfólio de um investidor (`get_investor_portfolio`), e enriquecer qualquer startup com dados de funding (`enrich_startup_with_crunchbase`). O `get_startup_by_cnpj` foi estendido com `include_rounds=true` para cruzar dados Crunchbase com o CNPJ. Toda a integração degrada graciosamente quando `CRUNCHBASE_API_KEY` não está configurada — retorna mensagem clara em vez de erro.

## Key decisions
Crunchbase Basic free tier exclusivamente (endpoints `/v4/searches/organizations`, `/v4/searches/funding_rounds`, `/v4/entities/organizations/{permalink}`). Matching CNPJ↔Crunchbase UUID é manual via `enrich_startup_with_crunchbase(cnpj, crunchbase_slug)` — sem matching automático. `_check_api_key()` lê env em runtime para suporte a testes.

## Deferred
- Filtro de país em `list_recent_rounds` (atualmente retorna rodadas globais, não apenas brasileiras)
- Cache TTL para rounds
- Popular cache automaticamente para lista curada de investidores brasileiros
