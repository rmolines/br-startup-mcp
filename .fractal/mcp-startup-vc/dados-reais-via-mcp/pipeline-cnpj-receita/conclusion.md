---
predicate: "O agente não consegue integrar a base CNPJ da Receita Federal como fonte âncora — escolher estratégia de acesso e implementar pipeline para dados cadastrais/societários"
satisfied_date: 2026-03-19
satisfied_by: ship
---

## What was achieved
O MCP server agora integra a Receita Federal via BrasilAPI como fonte âncora: qualquer startup brasileira pode ser consultada pelo CNPJ, retornando dados cadastrais completos (CNAE, cidade, capital social, situação) e quadro societário, com cache DuckDB para respostas repetidas. Os modelos `Startup` e `Founder` estão implementados e populados com dados reais, e as tools `get_startup_by_cnpj` e `search_startups` estão registradas no MCP server.

## Key decisions
BrasilAPI escolhida como proxy da Receita Federal (gratuita, sem auth). Cache-first: consulta DuckDB antes de chamar a API. `search_startups` é cache-only — não há busca em batch sem BigQuery.

## Deferred
- Integração BigQuery/Base dos Dados para search em batch (requer GCP credentials)
- `participacao_pct` dos founders (BrasilAPI não fornece)
- Cache TTL / revalidação automática
- Enriquecimento de Startup com dados Crunchbase (próximo nó)
