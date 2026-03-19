---
response: leaf
confidence: high
reasoning: "Mesmo padrão do pipeline-gov-aberto — implementar direto. A estratégia de acesso (API gov.br para consultas pontuais ou Base dos Dados/BigQuery para bulk) se resolve implementando. O padrão fetch-normalize-DuckDB-MCP já está validado."
child_predicate:
child_type:
prd_seed: "Implementar data client para Receita Federal/CNPJ: escolher estratégia de acesso (API gov.br para consulta pontual, ou BrasilAPI como proxy aberto), implementar fetch, normalizar para model Startup/Founder, cachear em DuckDB, expor via tool get_startup_by_cnpj e search_startups"
leaf_type: cycle
verification: objective
---
