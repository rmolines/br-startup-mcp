---
response: leaf
confidence: high
reasoning: "Override do evaluator (que propôs sub-decomposição epistêmica). Humano concordou que descobrir endpoints CKAN e inspecionar CSVs faz parte do sprint, não é sub-problema separado. Implementar pipeline end-to-end: fetch de CVM/BNDES via CKAN, normalizar CSVs, cachear em DuckDB, e servir via pelo menos 1 tool MCP funcional."
child_predicate:
child_type:
prd_seed: "Implementar pipeline end-to-end: fetch de dados CVM/BNDES via CKAN API, normalizar CSVs, cachear em DuckDB, e servir via MCP tool funcional. Deve incluir setup do projeto Python (pyproject.toml), MCP server básico, e pelo menos 1 tool que retorna dados reais."
leaf_type: cycle
verification: objective
---
