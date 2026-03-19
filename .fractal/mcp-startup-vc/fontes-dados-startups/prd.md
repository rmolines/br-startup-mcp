---
predicate: "O agente não consegue identificar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras para alimentar o MCP"
leaf_type: cycle
verification: objective
created: 2026-03-19
---

# Pesquisa de fontes de dados de startups brasileiras

## Objetivo

Pesquisar e catalogar fontes de dados acessíveis sobre startups brasileiras, avaliando cobertura, forma de acesso e viabilidade para uso no MCP.

## Critérios de aceitação

1. Catálogo estruturado em `docs/data-sources.md` com pelo menos 8 fontes avaliadas
2. Para cada fonte: nome, URL, tipo de dado, cobertura estimada, forma de acesso (API/scraping/download/manual), custo, limitações legais/ToS
3. Avaliação de viabilidade: quais fontes são integráveis programaticamente vs. manuais
4. Conclusão: o conjunto de fontes identificadas é ou não suficiente para um MCP "abrangente" — com justificativa
5. Pesquisa deve incluir fontes governamentais (Receita/CNPJ, CVM, BNDES), plataformas de ecossistema (Distrito, ABStartups), bases internacionais com cobertura BR (Crunchbase), e fontes alternativas (GitHub datasets, aceleradoras)

## Fora de escopo

- Implementação de integrações
- Scraping ou coleta de dados
- Negociação de acesso a APIs pagas

## Constraints

- Pesquisa via web search + análise de documentação pública
- Resultado é um documento markdown, não código
