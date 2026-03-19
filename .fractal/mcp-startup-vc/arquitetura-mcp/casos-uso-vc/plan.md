# Plan — casos-uso-vc

**Predicate:** "O agente não consegue mapear os casos de uso reais de um fundo de VC — quais perguntas analistas fazem, quais workflows executam com dados de startups — para derivar a superfície de tools do MCP"
**Node:** .fractal/mcp-startup-vc/arquitetura-mcp/casos-uso-vc
**Created:** 2026-03-19

---

## Project Context

Tree: mcp-startup-vc
Root: "O agente não consegue construir um MCP abrangente de dados de startups para fundos de VC usarem no Claude"

Satisfied nodes:
- fontes-dados-startups: "O agente não consegue identificar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras para alimentar o MCP"
  achieved: Eleven data sources cataloged in docs/data-sources.md; confirmed programmatically accessible sources exist; recommended 4-layer integration strategy (CNPJ anchor + Crunchbase + CVM + BNDES).
  capabilities: docs/data-sources.md with full source catalog, integrability assessment, and integration strategy
  files: docs/data-sources.md
  deferred: Actual data integrations, API access negotiation with Distrito/ABStartups, data quality evaluation

Active: .fractal/mcp-startup-vc/arquitetura-mcp/casos-uso-vc

---

## Functional Requirements

FR1: docs/vc-use-cases.md existe com pelo menos 5 workflows mapeados
validates: predicado — mapeamento de casos de uso reais de VC
verified_by: D1 acceptance

FR2: Cada workflow tem perguntas típicas de analistas, dados necessários, e fontes que cobrem
validates: predicado — quais perguntas analistas fazem
verified_by: D1 acceptance

FR3: vc-use-cases.md propõe tools MCP derivadas (nome, descrição, parâmetros, fonte)
validates: predicado — derivar superfície de tools do MCP
verified_by: D1 acceptance

FR4: docs/architecture.md existe com data model unificado (entidades: Startup, Round, Investor, Founder)
validates: predicado — arquitetura coerente do MCP
verified_by: D2 acceptance

FR5: architecture.md lista tools com assinatura proposta e diagrama de integração fontes → data model → tools
validates: predicado — superfície de tools derivada do cruzamento com fontes de dados
verified_by: D2 acceptance

FR6: architecture.md inclui stack tecnológico recomendado com justificativas
validates: predicado — arquitetura implementável
verified_by: D2 acceptance

---

## Deliverables

### D1 — Mapear workflows de VC e derivar tools MCP

**Executor:** sonnet
**Isolation:** none
**Depends on:** none
**Predicate:** O agente não mapeia quais workflows analistas de VC executam com dados de startups nem quais tools MCP derivar
**Files touched:**
- `docs/vc-use-cases.md`

**Prompt for subagent:**

> Você está produzindo: `docs/vc-use-cases.md` — mapeamento de workflows de fundos de VC e superfície de tools do MCP derivada.
>
> **Context:**
> - Repo: `br-startup-mcp` em `/Users/rmolines/git/br-startup-mcp/`
> - Nó sibling `fontes-dados-startups` já produziu `docs/data-sources.md` com 11 fontes catalogadas. USE esse arquivo como referência — não re-pesquise fontes.
> - Fontes programaticamente integráveis (sem contrato): Receita Federal CNPJ, Base dos Dados (BigQuery), CVM Dados Abertos, BNDES Dados Abertos, Crunchbase API (Basic), Kaggle/dados.gov.br.
> - Fontes manuais/negociação: ABStartups, Distrito, Sebrae, CNI, LinkedIn (alto risco legal).
> - Estratégia recomendada de integração: CNPJ como âncora + Crunchbase para investimentos + CVM para dados regulatórios + BNDES para financiamento público.
> - No sibling dependencies beyond docs/data-sources.md — use it as the primary reference.
>
> **What to do:**
>
> 1. Leia `/Users/rmolines/git/br-startup-mcp/docs/data-sources.md` na íntegra antes de escrever qualquer coisa.
>
> 2. Crie `/Users/rmolines/git/br-startup-mcp/docs/vc-use-cases.md` com a seguinte estrutura:
>
>    **Seção 1 — Workflows mapeados** (pelo menos 5 dos seguintes):
>    - Deal Sourcing — descoberta de novas startups candidatas a investimento
>    - Screening — triagem inicial de startups (fit tese, estágio, setor)
>    - Due Diligence — investigação aprofundada antes de term sheet
>    - Portfolio Monitoring — acompanhamento de portfólio após investimento
>    - Market Mapping — mapeamento competitivo de um segmento
>    - Comparable Analysis (Comp Analysis) — análise de múltiplos e benchmarks
>
>    Para cada workflow inclua:
>    - Descrição breve (2-3 linhas)
>    - Perguntas típicas que analistas fazem (3-5 perguntas concretas)
>    - Dados necessários (campos e dimensões)
>    - Fontes que cobrem (referenciando data-sources.md pelo nome da fonte)
>    - Tools MCP propostas para este workflow (liste os nomes)
>
>    **Seção 2 — Proposta de Tools MCP** (alvo: 10-20 tools total):
>    Para cada tool:
>    - Nome em snake_case com verbo imperativo em inglês (search_, get_, list_, compare_)
>    - Descrição da tool (1-2 linhas)
>    - Parâmetros de entrada (nome, tipo Python, obrigatório/opcional, descrição)
>    - Resposta esperada (campos principais com tipos)
>    - Fonte de dados principal
>
>    Parâmetros recorrentes padrão onde aplicável: cnpj (str, opcional), sector (str, opcional), stage (enum, opcional), city (str, opcional), limit (int, opcional, default 20).
>
>    **Seção 3 — Proposta de Resources MCP** (pelo menos 3):
>    Resources são dados estáticos ou semi-estáticos expostos pelo MCP sem parâmetros dinâmicos complexos.
>    Exemplos: lista de CNAEs relevantes para startups, lista de fundos FIP registrados na CVM, mapa de cidades com ecossistemas ativos, tabela de rounds por estágio (seed, série A, etc.).
>    Para cada resource: URI, descrição, fonte, frequência de atualização sugerida.
>
> **What NOT to do:**
> - Não invente fontes além das listadas em docs/data-sources.md.
> - Não proponha tools que dependam de scraping ou de fontes sem API programática.
> - Não implemente código — apenas especificação em markdown.
> - Não re-escreva o conteúdo de data-sources.md.
> - Não inclua LinkedIn como fonte primária (alto risco legal, documentado em data-sources.md).
>
> **Validation:** `test -f /Users/rmolines/git/br-startup-mcp/docs/vc-use-cases.md && grep -c "^##" /Users/rmolines/git/br-startup-mcp/docs/vc-use-cases.md`
> Deve retornar >= 3 (Workflows mapeados, Tools MCP, Resources MCP).
>
> **Result format:**
> ```
> ## Result
> task_id: D1
> status: success | partial | failed
> summary: <1-2 sentences>
> errors: <list or empty>
> validation_result: <output do comando de validação>
> files_changed:
> - docs/vc-use-cases.md
> ```

**Acceptance:** `test -f docs/vc-use-cases.md && grep -c "^##" docs/vc-use-cases.md` → retorna >= 3
**Human test:** Abra `docs/vc-use-cases.md` e confirme que existem pelo menos 5 workflows com perguntas de analistas, dados necessários, fontes, e tools MCP propostas com parâmetros e tipos.

---

### D2 — Definir data model e arquitetura do MCP

**Executor:** sonnet
**Isolation:** none
**Depends on:** D1
**Predicate:** O agente não consegue propor um data model unificado e arquitetura de integração fontes → data model → tools
**Files touched:**
- `docs/architecture.md`

**Prompt for subagent:**

> Você está produzindo: `docs/architecture.md` — data model unificado, lista de tools com assinatura completa, diagrama de integração, e stack tecnológico recomendado.
>
> **Context:**
> - Repo: `br-startup-mcp` em `/Users/rmolines/git/br-startup-mcp/`
> - Use docs/data-sources.md (sibling fontes-dados-startups): fontes programáticas disponíveis são Receita Federal CNPJ (API REST + BigQuery via Base dos Dados), CVM (CSV/CKAN API), BNDES (CSV/CKAN API), Crunchbase (REST API, plano Basic gratuito).
> - Use docs/vc-use-cases.md (D1 deste nó): contém os workflows mapeados, tools propostas, e resources — use como insumo direto. Não invente tools novas.
> - Leia AMBOS os arquivos antes de escrever qualquer coisa.
>
> **What to do:**
>
> 1. Leia `/Users/rmolines/git/br-startup-mcp/docs/data-sources.md` e `/Users/rmolines/git/br-startup-mcp/docs/vc-use-cases.md` na íntegra.
>
> 2. Crie `/Users/rmolines/git/br-startup-mcp/docs/architecture.md` com as seguintes seções:
>
>    **## Data Model Unificado**
>    Entidades core obrigatórias: `Startup`, `Round`, `Investor`, `Founder`, `Fund`, `Sector`.
>    Entidades adicionais conforme necessário pelos workflows.
>    Para cada entidade: tabela markdown com colunas (campo, tipo, fonte, obrigatório).
>    Inclua relações entre entidades (ex: "Startup 1—N Round", "Round N—N Investor").
>
>    **## Tools — Assinaturas Completas**
>    Consolide todas as tools de vc-use-cases.md em formato padronizado:
>    - Nome da tool
>    - Descrição
>    - Input schema (parâmetros: nome, tipo, obrigatório/opcional, descrição, exemplo)
>    - Output schema (campos retornados: nome, tipo, descrição)
>    - Entidade(s) do data model que a tool acessa
>    - Fonte de dados principal
>
>    **## Diagrama de Integração**
>    Represente em ASCII art ou markdown aninhado o fluxo completo:
>    Fonte de Dados → Camada de Ingestão (método) → Entidade do Data Model → Tool MCP → Agente VC
>    Mostre explicitamente qual tool acessa qual entidade via qual fonte.
>    Exemplo de formato:
>    ```
>    Receita Federal CNPJ
>      └─ ingestão: API REST / BigQuery
>        └─ entidade: Startup
>          ├─ tool: get_startup_by_cnpj
>          └─ tool: search_startups_by_sector
>    ```
>
>    **## Stack Tecnológico Recomendado**
>    - Runtime e linguagem (justifique com base nas SDKs das fontes)
>    - MCP SDK (qual usar para Python/TypeScript)
>    - Clientes por fonte: HTTP client para CNPJ API, google-cloud-bigquery para Base dos Dados, requests/httpx para CVM/BNDES, crunchbase SDK ou REST direto
>    - Cache/storage local (SQLite, DuckDB, Redis — justifique a escolha)
>    - Formato de configuração (variáveis de ambiente para chaves de API)
>
> **What NOT to do:**
> - Não invente tools que não estejam em vc-use-cases.md (pode consolidar ou renomear, não adicionar workflows novos).
> - Não implemente código — apenas especificação em markdown.
> - Não repita o catálogo completo de fontes — referencie docs/data-sources.md.
> - Não proponha stack com fontes sem API programática.
>
> **Validation:** `test -f /Users/rmolines/git/br-startup-mcp/docs/architecture.md && grep -c "^##" /Users/rmolines/git/br-startup-mcp/docs/architecture.md`
> Deve retornar >= 4 (4 seções principais).
>
> **Result format:**
> ```
> ## Result
> task_id: D2
> status: success | partial | failed
> summary: <1-2 sentences>
> errors: <list or empty>
> validation_result: <output do comando de validação>
> files_changed:
> - docs/architecture.md
> ```

**Acceptance:** `test -f docs/architecture.md && grep -c "^##" docs/architecture.md` → retorna >= 4
**Human test:** Abra `docs/architecture.md` e confirme que há: (1) data model com entidades e campos, (2) lista de tools com parâmetros e tipos, (3) diagrama de integração mostrando fluxo fonte→entidade→tool, (4) stack tecnológico com justificativas.

---

## Dependency Graph

```
D1 ──→ D2
```

## Batch Sequence

```
Batch 1: D1 — Mapear workflows de VC e derivar tools MCP
Batch 2: D2 — Definir data model e arquitetura do MCP (depende de D1)
```

---

## Execution DAG

task: D1
title: Mapear workflows de VC e derivar tools MCP
depends_on:
predicate: O agente não mapeia quais workflows analistas de VC executam com dados de startups nem quais tools MCP derivar
executor: sonnet
isolation: none
batch: 1
files:
- docs/vc-use-cases.md
max_retries: 2
acceptance: test -f docs/vc-use-cases.md && grep -c "^##" docs/vc-use-cases.md | awk '{exit ($1 < 3)}'
human_test: Abra docs/vc-use-cases.md e confirme que há pelo menos 5 workflows com perguntas de analistas, fontes e tools MCP com parâmetros

task: D2
title: Definir data model e arquitetura do MCP
depends_on: D1
predicate: O agente não consegue propor um data model unificado e arquitetura de integração fontes → data model → tools
executor: sonnet
isolation: none
batch: 2
files:
- docs/architecture.md
max_retries: 2
acceptance: test -f docs/architecture.md && grep -c "^##" docs/architecture.md | awk '{exit ($1 < 4)}'
human_test: Abra docs/architecture.md e confirme que há data model com entidades, lista de tools com assinaturas, diagrama de integração e stack tecnológico

---

## Infrastructure

Infrastructure: no changes needed.
