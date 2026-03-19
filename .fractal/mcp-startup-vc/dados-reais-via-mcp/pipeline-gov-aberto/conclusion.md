---
predicate: "O agente não consegue buscar e normalizar dados reais de uma fonte governamental aberta (CVM ou BNDES) — validar que o pipeline fetch-normalize-cache funciona"
satisfied_date: 2026-03-19
satisfied_by: ship
---

## What was achieved
O pipeline fetch-normalize-cache está funcionando: dados reais chegam da CVM (12.328 registros de ofertas públicas via ZIP download) e do BNDES (100+ registros de financiamentos via CKAN API, de 2.3M disponíveis), são normalizados para modelos Pydantic e cacheados em DuckDB local. O MCP server expõe esses dados via dois tools funcionais (`get_cvm_crowdfunding_offers` e `get_bndes_financing`) com stdio transport — um agente VC já pode consultar dados governamentais reais via Claude.

## Key decisions
CVM usa dataset de ofertas públicas Resolution 160 (não CVM 88 crowdfunding especificamente — dataset separado inexistente no portal). BNDES usa CKAN datastore (CNPJs mascarados em operações indiretas). Todo logging vai para stderr para não corromper o protocolo MCP.

## Deferred
- Dataset CVM 88 equity crowdfunding específico (não encontrado no portal dados.cvm.gov.br)
- BNDES operações não automáticas com CNPJs completos (resource `6f56b78c`)
- Cache TTL / revalidação automática
- Tool get_startup_by_cnpj (próximo nó: Receita Federal)
