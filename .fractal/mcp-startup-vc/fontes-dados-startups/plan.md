# Plan — Pesquisa de fontes de dados de startups brasileiras

**Node:** fontes-dados-startups
**Predicate:** "O agente não consegue identificar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras para alimentar o MCP"
**Created:** 2026-03-19

---

## Problem

The agent cannot identify accessible and sufficiently comprehensive data sources about Brazilian startups to feed the MCP. Resolution: produce a structured catalog (`docs/data-sources.md`) evaluating ≥8 sources across coverage, access method, cost, and legal constraints — with a final viability conclusion.

---

## Functional Requirements

FR1: docs/data-sources.md exists with ≥8 sources cataloged
validates: "identificar fontes de dados acessíveis e suficientemente abrangentes"
verified_by: D1 acceptance

FR2: Each source includes: name, URL, data type, coverage, access method, cost, ToS/legal limitations
validates: structured evaluation enabling programmatic vs. manual classification
verified_by: D1 acceptance (grep for required fields)

FR3: Covers all required source categories: governmental (CNPJ/Receita, CVM, BNDES), ecosystem platforms (Distrito, ABStartups), international with BR coverage (Crunchbase), and alternatives (GitHub datasets, accelerators)
validates: "abrangente" — ensures breadth across source types
verified_by: D1 acceptance

FR4: Document includes a conclusion on whether the identified sources are sufficient for a "comprehensive" MCP — with written justification
validates: resolves the predicate's core question
verified_by: D1 human_test (reviewer reads conclusion section)

---

## Deliverables

### D1 — Catalog de fontes de dados de startups brasileiras

**Executor:** sonnet
**Isolation:** none
**Depends on:** none
**Predicate:** Identificar e catalogar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras
**Files touched:**
- `docs/data-sources.md`

**Prompt for subagent:**

> You are producing a research document cataloging data sources for Brazilian startups.
>
> **Context:**
> - Repo: `br-startup-mcp` at `/Users/rmolines/git/br-startup-mcp/`
> - This is an MCP server project for VC funds to query Brazilian startup data via Claude
> - No sibling dependencies for this deliverable — this is the first and only deliverable
> - The output is a markdown document, NOT code
>
> **What to do:**
>
> 1. Use web search to research each of the required source categories listed below. Search for current access methods, API availability, pricing, and terms of service for each.
>
> 2. Create the directory `docs/` at `/Users/rmolines/git/br-startup-mcp/docs/` if it doesn't exist.
>
> 3. Write `/Users/rmolines/git/br-startup-mcp/docs/data-sources.md` with the following structure:
>
> ```markdown
> # Fontes de Dados — Startups Brasileiras
>
> > Catálogo de fontes avaliadas para o MCP br-startup-mcp.
> > Última atualização: <date>
>
> ## Fontes Catalogadas
>
> ### <N>. <Source Name>
> - **URL:** <url>
> - **Tipo de dado:** <what data it contains>
> - **Cobertura estimada:** <number of companies / scope>
> - **Forma de acesso:** API | Scraping | Download | Manual
> - **Custo:** Gratuito | Freemium (limites) | Pago (estimate) | Desconhecido
> - **Limitações legais/ToS:** <summary of relevant ToS clauses, robots.txt, API terms>
> - **Integrabilidade:** Programática | Manual | Parcialmente programática
> - **Notas:** <any relevant details, quirks, or caveats>
>
> ---
> ```
>
> 4. The catalog MUST include at least 8 sources, covering ALL of these categories:
>    - **Governamentais:** CNPJ / Receita Federal (cnpj.ws or Brasil.io), CVM (Comissão de Valores Mobiliários), BNDES (datasets)
>    - **Plataformas de ecossistema:** Distrito (distrito.me), ABStartups (abstartups.com.br)
>    - **Internacionais com cobertura BR:** Crunchbase (API), LinkedIn (company data)
>    - **Alternativas:** GitHub public datasets about Brazilian startups, aceleradoras (e.g., Endeavor, ACE, Plug and Play BR), portais de notícias (StartSe, Startupi)
>
> 5. After cataloging all sources, write a `## Avaliação de Viabilidade` section:
>    - Table: Source | Integrabilidade | Motivo
>    - Separate programmatic sources from manual/scraping ones
>
> 6. Write a `## Conclusão` section (3-5 paragraphs) answering:
>    - Is the identified set of sources sufficient for a "comprehensive" MCP?
>    - What types of data are well-covered vs. gaps?
>    - What is the recommended integration strategy (which sources to prioritize)?
>    - Explicit verdict: "Sim, o conjunto é suficiente" or "Não, o conjunto tem lacunas significativas" — with written justification
>
> **What NOT to do:**
> - Do NOT implement any API integrations or write code
> - Do NOT attempt to scrape or collect actual data
> - Do NOT negotiate API access or create accounts
> - Do NOT write placeholder content — use web search to get real, current information for each source
>
> **Validation:**
> ```bash
> # Check file exists
> test -f /Users/rmolines/git/br-startup-mcp/docs/data-sources.md && echo "FILE EXISTS"
>
> # Count sources (count ### headers after "## Fontes Catalogadas")
> grep -c "^### " /Users/rmolines/git/br-startup-mcp/docs/data-sources.md
> # Must return >= 8
>
> # Check required sections exist
> grep -c "## Avaliação de Viabilidade\|## Conclusão" /Users/rmolines/git/br-startup-mcp/docs/data-sources.md
> # Must return 2
>
> # Check required fields in each entry
> grep -c "Forma de acesso\|Custo\|Integrabilidade\|Limitações" /Users/rmolines/git/br-startup-mcp/docs/data-sources.md
> # Must return >= 8 (at least once per source for each field)
> ```
>
> **Result format:**
> ```
> ## Result
> task_id: D1
> status: success | partial | failed
> summary: <1-2 sentences>
> errors: <list or empty>
> validation_result: <output of validation commands>
> files_changed:
> - docs/data-sources.md
> ```

**Acceptance:** `grep -c "^### " docs/data-sources.md` returns ≥ 8 AND `grep -c "## Avaliação de Viabilidade\|## Conclusão" docs/data-sources.md` returns 2
**Human test:** Open `docs/data-sources.md`, read the Conclusão section, and verify it has a clear verdict ("Sim" or "Não") with at least one paragraph of written justification explaining which source types are sufficient or missing.

---

## Execution DAG

task: D1
title: Catalog de fontes de dados de startups brasileiras
depends_on:
predicate: Identificar e catalogar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras para alimentar o MCP
executor: sonnet
isolation: none
batch: 1
files:
- docs/data-sources.md
max_retries: 2
acceptance: grep -c "^### " /Users/rmolines/git/br-startup-mcp/docs/data-sources.md returns >= 8 AND grep -c "## Avaliação de Viabilidade\|## Conclusão" /Users/rmolines/git/br-startup-mcp/docs/data-sources.md returns 2
human_test: Open docs/data-sources.md and verify the Conclusão section has a clear written verdict with justification

---

## Infrastructure

Infrastructure: no changes needed.
