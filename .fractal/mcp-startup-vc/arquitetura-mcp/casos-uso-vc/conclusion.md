---
predicate: "O agente não consegue mapear os casos de uso reais de um fundo de VC — quais perguntas analistas fazem, quais workflows executam com dados de startups — para derivar a superfície de tools do MCP"
satisfied_date: 2026-03-19
satisfied_by: ship
---

## What was achieved
Os workflows reais de analistas de VC foram mapeados em `docs/vc-use-cases.md` (6 workflows com perguntas concretas, dados necessários e fontes) e a superfície de tools do MCP foi derivada em `docs/architecture.md` (12 tools com assinaturas completas, data model de 7 entidades, diagrama de integração fonte→entidade→tool, e stack Python 3.11+/DuckDB justificado). O conjunto define o que o MCP precisa implementar para ser útil a fundos de VC.

## Key decisions
- Tools propostas derivadas exclusivamente das fontes programáticas identificadas pelo nó sibling (CNPJ, Crunchbase, CVM, BNDES) — sem dependência de fontes manuais ou com alto risco legal
- CNPJ como âncora do data model: toda entidade `Startup` tem CNPJ como chave primária, permitindo cruzamento entre todas as fontes
- DuckDB como cache local recomendado para CSV das fontes governamentais (sem servidor necessário, suporte analítico nativo)

## Deferred
- Implementação do código do MCP server (explicitamente fora de escopo deste nó)
- Validação das assinaturas de tools com VCs reais
- Definição de estratégia de atualização e refresh dos caches locais
