---
predicate: "O agente não consegue mapear os casos de uso reais de um fundo de VC — quais perguntas analistas fazem, quais workflows executam com dados de startups — para derivar a superfície de tools do MCP"
leaf_type: cycle
verification: subjective
created: 2026-03-19
---

# Mapeamento de casos de uso de VC e superfície de tools

## Objetivo

Mapear os workflows típicos de um fundo de VC com dados de startups e derivar a superfície de tools do MCP a partir do cruzamento com as fontes de dados catalogadas em `docs/data-sources.md`.

## Critérios de aceitação

1. Documento `docs/vc-use-cases.md` com:
   - Pelo menos 5 workflows de VC mapeados (deal sourcing, screening, due diligence, portfolio monitoring, market mapping, comp analysis)
   - Para cada workflow: perguntas típicas que analistas fazem, dados necessários, fontes que cobrem
   - Proposta de tools MCP derivadas (nome, descrição, parâmetros, fonte de dados)
   - Proposta de resources MCP (dados estáticos ou semi-estáticos expostos)
2. Documento `docs/architecture.md` com:
   - Data model unificado (entidades: Startup, Round, Investor, Founder, etc.)
   - Lista de tools com assinatura proposta
   - Diagrama de integração de fontes → data model → tools
   - Stack tecnológico recomendado

## Fora de escopo

- Implementação de código
- Validação com VCs reais (isso é responsabilidade do humano)
- Design de UI/UX

## Constraints

- Basear-se em domain knowledge de VC + fontes catalogadas em docs/data-sources.md
- Manter pragmático: tools que podem ser implementadas com as fontes programáticas identificadas
