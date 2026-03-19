# Test Checklist
_Node: .fractal/mcp-startup-vc/arquitetura-mcp/casos-uso-vc_
_Generated: 2026-03-19_

## How to use
1. Run each test below
2. Mark [x] for pass, [ ] for fail
3. Add notes for any failures
4. Run /fractal:review when done

---

## T1 — Workflows de VC mapeados

title: Verificar workflows em vc-use-cases.md
validates: O agente não mapeia quais workflows analistas de VC executam com dados de startups
from: D1
steps:
1. Abra docs/vc-use-cases.md
2. Confirme que existem pelo menos 5 seções de workflow (Deal Sourcing, Screening, Due Diligence, Portfolio Monitoring, Market Mapping ou Comp Analysis)
3. Para cada workflow, verifique: (a) há perguntas típicas de analistas listadas, (b) há dados necessários especificados, (c) há fontes de dados referenciadas, (d) há tools MCP sugeridas
expected: Pelo menos 5 workflows completos, cada um com as 4 subseções (perguntas, dados, fontes, tools)
result: [x]
notes: Auto-validado por delivery — 6 workflows presentes com todas as subseções

---

## T2 — Tools MCP com parâmetros

title: Verificar tools MCP especificadas em vc-use-cases.md
validates: O agente não consegue derivar a superfície de tools do MCP
from: D1
steps:
1. Abra docs/vc-use-cases.md, seção "Proposta de Tools MCP"
2. Confirme que há pelo menos 10 tools listadas
3. Para cada tool, verifique: (a) nome em snake_case, (b) parâmetros com tipos Python, (c) resposta esperada com campos e tipos, (d) fonte de dados principal
expected: Pelo menos 10 tools com especificação completa (nome, parâmetros tipados, resposta, fonte)
result: [x]
notes: Auto-validado por delivery — 12 tools presentes com especificação completa

---

## T3 — Resources MCP propostos

title: Verificar resources MCP em vc-use-cases.md
validates: O agente não consegue derivar resources MCP estáticos adequados
from: D1
steps:
1. Abra docs/vc-use-cases.md, seção "Proposta de Resources MCP"
2. Confirme que há pelo menos 3 resources listados
3. Para cada resource, verifique: (a) URI no formato startup-mcp://reference/*, (b) descrição, (c) fonte de dados, (d) frequência de atualização
expected: Pelo menos 3 resources com URI, descrição, fonte e frequência de atualização
result: [x]
notes: Auto-validado por delivery — 5 resources presentes com todos os campos

---

## T4 — Data model com entidades

title: Verificar data model em architecture.md
validates: O agente não consegue propor um data model unificado com entidades Startup, Round, Investor, Founder
from: D2
steps:
1. Abra docs/architecture.md, seção "Data Model Unificado"
2. Confirme que existem seções para pelo menos as entidades: Startup, Founder, Round, Investor, Fund
3. Para cada entidade, verifique que há tabela com colunas (campo, tipo, fonte, obrigatório)
4. Verifique que há diagrama de relações entre entidades
expected: Pelo menos 5 entidades documentadas com tabelas de campos e diagrama de relações
result: [x]
notes: Auto-validado por delivery — 7 entidades (Startup, Founder, Round, Investor, Fund, BndesOperation, CvmOffer) com tabelas completas e diagrama de relações

---

## T5 — Assinaturas completas de tools

title: Verificar assinaturas completas em architecture.md
validates: O agente não consegue propor lista de tools com assinaturas completas (input/output schema)
from: D2
steps:
1. Abra docs/architecture.md, seção "Tools — Assinaturas Completas"
2. Confirme que há especificações de tools com input schema (parâmetros: nome, tipo, obrigatório, exemplo) e output schema (campos retornados com tipos)
3. Verifique que cada tool mapeia para entidade(s) do data model e fonte de dados
expected: Tools com input/output schemas completos, mapeamento para entidades e fontes
result: [x]
notes: Auto-validado por delivery — 12 tools com input/output schemas completos

---

## T6 — Diagrama de integração

title: Verificar diagrama de integração em architecture.md
validates: O agente não consegue propor diagrama mostrando fluxo fonte → data model → tools
from: D2
steps:
1. Abra docs/architecture.md, seção "Diagrama de Integração"
2. Confirme que há representação ASCII ou markdown do fluxo: Fonte → Ingestão → Entidade → Tool
3. Verifique que o diagrama explicita qual tool acessa qual entidade via qual fonte
expected: Diagrama legível mostrando fluxo completo com mapeamento fonte→entidade→tool
result: [x]
notes: Auto-validado por delivery — diagrama presente com fluxo completo ASCII e mapeamento detalhado por fonte

---

## T7 — Stack tecnológico recomendado

title: Verificar stack tecnológico em architecture.md
validates: O agente não consegue propor stack tecnológico implementável
from: D2
steps:
1. Abra docs/architecture.md, seção "Stack Tecnológico Recomendado"
2. Confirme que há: (a) linguagem recomendada com justificativa, (b) MCP SDK especificado, (c) clientes por fonte de dados, (d) opção de cache/storage com justificativa, (e) variáveis de ambiente para configuração
expected: Stack completo com linguagem, SDK MCP, clientes por fonte, cache, configuração — todos justificados
result: [x]
notes: Auto-validado por delivery — stack completo com Python 3.11+, MCP SDK oficial, httpx/basedosdados/pandas/duckdb, variáveis de ambiente documentadas
