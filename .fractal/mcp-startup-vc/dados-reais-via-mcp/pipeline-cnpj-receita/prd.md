---
predicate: "O agente não consegue integrar a base CNPJ da Receita Federal como fonte âncora"
leaf_type: cycle
verification: objective
created: 2026-03-19
---

# Pipeline CNPJ Receita Federal

## Objetivo

Implementar data client para Receita Federal/CNPJ, a fonte âncora do MCP. Toda startup tem CNPJ — este é o identificador central que conecta todas as outras fontes.

## Critérios de aceitação

1. Data client `cnpj.py` que busca dados de CNPJ:
   - Estratégia recomendada: BrasilAPI (brasilapi.com.br/api/cnpj/v1/{cnpj}) como proxy gratuito e sem auth da Receita Federal, ou API Minha Receita se BrasilAPI estiver instável
   - Fallback: API gov.br (requer cadastro)
   - Para busca em batch/search: considerar Base dos Dados BigQuery se viável sem setup complexo
2. Pydantic models Startup e Founder populados com dados reais da Receita
3. Cache em DuckDB (tabelas startups, founders)
4. Tools MCP funcionais:
   - `get_startup_by_cnpj` — busca dados cadastrais e societários por CNPJ
   - `search_startups` — busca por CNAE, cidade, estado, data de abertura (requer cache local com dados)
5. Smoke test: tool retorna dados reais de um CNPJ conhecido

## Fora de escopo

- Download bulk dos 10GB+ da Receita Federal (inviável para MVP)
- Integração BigQuery completa (requer Google Cloud credentials)
- Crunchbase (próximo nó)

## Constraints

- Seguir padrão existente (cvm.py, bndes.py como referência)
- BrasilAPI é gratuita e sem auth — caminho de menor resistência
- Para search, uma opção é popular o cache consultando CNPJs conhecidos ou usar dataset sample
- Manter compatibilidade com architecture.md
