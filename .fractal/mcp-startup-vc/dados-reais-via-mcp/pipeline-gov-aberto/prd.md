---
predicate: "O agente não consegue buscar e normalizar dados reais de uma fonte governamental aberta (CVM ou BNDES) — validar que o pipeline fetch-normalize-cache funciona"
leaf_type: cycle
verification: objective
created: 2026-03-19
---

# Pipeline de dados governamentais abertos (CVM + BNDES)

## Objetivo

Implementar pipeline end-to-end: fetch de dados CVM/BNDES, normalizar, cachear em DuckDB, e servir via MCP server funcional com pelo menos 1 tool que retorna dados reais.

## Critérios de aceitação

1. Setup do projeto Python funcional:
   - `pyproject.toml` com dependências (httpx, duckdb, mcp-sdk, pydantic)
   - Estrutura de diretórios seguindo docs/architecture.md
2. Data clients para CVM e BNDES:
   - Fetch via CKAN API ou download direto de CSVs
   - Parsing e normalização para Pydantic models (conforme docs/architecture.md)
   - Cache em DuckDB local
3. MCP server funcional:
   - Pelo menos 1 tool que retorna dados reais (ex: buscar operações BNDES por CNPJ, ou listar ofertas CVM 88)
   - Server roda e responde via stdio
4. Teste de smoke: `echo '{"method":"tools/list"}' | python -m br_startup_mcp` retorna lista de tools

## Fora de escopo

- Integração com Crunchbase (requer API key — será próximo nó)
- Integração com Receita Federal/CNPJ (base grande, tratamento especial)
- UI ou documentação de usuário
- Testes automatizados (MVP)
- Deploy

## Constraints

- Seguir arquitetura documentada em docs/architecture.md
- Python 3.11+, DuckDB, httpx
- CVM e BNDES são fontes abertas sem autenticação
- Dados reais devem fluir do portal governamental até a tool MCP
