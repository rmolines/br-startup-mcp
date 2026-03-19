# Plan: pipeline-gov-aberto
_Node: .fractal/mcp-startup-vc/dados-reais-via-mcp/pipeline-gov-aberto_
_Generated on: 2026-03-19_

## Project Context

Tree: mcp-startup-vc
Root: "O agente não consegue construir um MCP abrangente de dados de startups para fundos de VC usarem no Claude"

Satisfied siblings:
- arquitetura-mcp: data model unificado + 12 tool signatures definidas em `docs/architecture.md`. Entidades: Startup, Founder, Round, Investor, BndesOperation, CvmOffer, Fund. Stack: Python 3.11+, DuckDB, httpx. CNPJ como chave âncora.
- casos-uso-vc: 6 workflows VC mapeados em `docs/vc-use-cases.md`
- fontes-dados-startups: catálogo de 11 fontes em `docs/data-sources.md`. CVM e BNDES confirmados como programáticos, gratuitos, sem autenticação.

## Requirements

- R1: Setup Python funcional — `pyproject.toml` com dependências (httpx, duckdb, mcp, pydantic), estrutura de diretórios seguindo `docs/architecture.md`
- R2: Pydantic models para entidades BndesOperation e CvmOffer (conforme `docs/architecture.md`)
- R3: Data client CVM — fetch via CKAN API ou CSV download, normalização para `CvmOffer`, cache DuckDB
- R4: Data client BNDES — fetch via CKAN API ou CSV download, normalização para `BndesOperation`, cache DuckDB
- R5: MCP server com ao menos 1 tool que retorna dados reais de CVM ou BNDES, rodando via stdio
- R6: Smoke test — `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python -m br_startup_mcp` retorna lista de tools com pelo menos 1 tool

## Problem

O predicado falha porque não existe código algum no repositório — só docs. Precisamos construir do zero o pipeline fetch-normalize-cache para CVM e BNDES: setup Python, modelos Pydantic derivados da arquitetura já definida, data clients que consomem os portais governamentais abertos, cache em DuckDB, e um MCP server funcional com stdio transport que exponha ao menos 1 tool retornando dados reais. Os três nós irmãos já entregaram toda a especificação necessária — este nó implementa.

---

## Functional Requirements

FR1: `pyproject.toml` existe em `~/git/br-startup-mcp/` com dependências mcp, httpx, duckdb, pydantic declaradas
validates: R1 — setup do projeto
verified_by: D1 acceptance

FR2: Estrutura de diretórios `src/br_startup_mcp/{models,data,tools}/` existe com `__init__.py` em cada pacote
validates: R1 — estrutura seguindo architecture.md
verified_by: D1 acceptance

FR3: `src/br_startup_mcp/models/entities.py` contém classes `BndesOperation` e `CvmOffer` como Pydantic BaseModel com todos os campos obrigatórios definidos em `docs/architecture.md`
validates: R2 — modelos corretos
verified_by: D2 acceptance

FR4: `src/br_startup_mcp/data/cvm.py` faz fetch real de dados da CVM (CKAN API ou CSV), normaliza para `CvmOffer`, persiste em DuckDB
validates: R3 — pipeline CVM end-to-end
verified_by: D3 acceptance

FR5: `src/br_startup_mcp/data/bndes.py` faz fetch real de dados do BNDES (CKAN API ou CSV), normaliza para `BndesOperation`, persiste em DuckDB
validates: R4 — pipeline BNDES end-to-end
verified_by: D4 acceptance

FR6: `src/br_startup_mcp/server.py` implementa MCP server com stdio transport e ao menos 1 tool que consulta DuckDB e retorna dados reais
validates: R5 — server MCP funcional
verified_by: D5 acceptance

FR7: `echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python -m br_startup_mcp` retorna JSON com `tools` array não vazio
validates: R6 — smoke test
verified_by: D5 acceptance

---

## Deliverables

### D1 — Setup do projeto Python

**Executor:** sonnet
**Isolation:** none
**Depends on:** none
**Predicate:** Setup Python funcional com estrutura de diretórios e dependências declaradas
**Files touched:**
- `~/git/br-startup-mcp/pyproject.toml`
- `~/git/br-startup-mcp/src/br_startup_mcp/__init__.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/__main__.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/models/__init__.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/data/__init__.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/tools/__init__.py`
- `~/git/br-startup-mcp/.env.example`
- `~/git/br-startup-mcp/.gitignore`

**Prompt for subagent:**

> You are implementing: Python project setup for br-startup-mcp — a MCP server for Brazilian startup data.
>
> **Context:**
> - Repo: `br-startup-mcp` at `~/git/br-startup-mcp/`
> - Stack: Python 3.11+, mcp (Anthropic Python SDK), httpx, duckdb, pydantic v2, python-dotenv
> - Architecture already designed in `~/git/br-startup-mcp/docs/architecture.md` — follow the directory structure exactly
> - No existing source code — this is a fresh project setup
> - No sibling dependencies for this deliverable
>
> **What to do:**
>
> 1. Create `~/git/br-startup-mcp/pyproject.toml` with:
>    - `[project]` section: name = "br-startup-mcp", version = "0.1.0", requires-python = ">=3.11"
>    - dependencies: `mcp>=1.0.0`, `httpx>=0.27.0`, `pydantic>=2.0.0`, `duckdb>=0.10.0`, `python-dotenv>=1.0.0`, `pandas>=2.0.0`
>    - `[project.scripts]` entry: `br-startup-mcp = "br_startup_mcp.server:main"`
>    - `[build-system]` using hatchling or setuptools
>
> 2. Create directory structure exactly as in `docs/architecture.md`:
>    ```
>    src/
>      br_startup_mcp/
>        __init__.py         (empty or version string)
>        __main__.py         (calls server.main() for `python -m br_startup_mcp`)
>        server.py           (leave as TODO stub — created in D5)
>        models/
>          __init__.py
>          entities.py       (leave as TODO stub — created in D2)
>        data/
>          __init__.py
>          cvm.py            (leave as TODO stub — created in D3)
>          bndes.py          (leave as TODO stub — created in D4)
>        tools/
>          __init__.py
>          regulatory.py     (leave as TODO stub — created in D5)
>    data/
>      .gitkeep             (DuckDB cache lives here, gitignored)
>    ```
>
> 3. Create `~/git/br-startup-mcp/__main__.py` content:
>    ```python
>    from br_startup_mcp.server import main
>    import asyncio
>    asyncio.run(main())
>    ```
>
> 4. Create `~/git/br-startup-mcp/.env.example`:
>    ```
>    DUCKDB_PATH=./data/cache.duckdb
>    ```
>
> 5. Create/update `~/git/br-startup-mcp/.gitignore` to include:
>    ```
>    data/cache.duckdb
>    data/*.duckdb
>    __pycache__/
>    *.pyc
>    .env
>    .venv/
>    dist/
>    *.egg-info/
>    ```
>
> 6. Install the project in editable mode from the repo root:
>    ```bash
>    cd ~/git/br-startup-mcp && pip install -e ".[dev]" 2>/dev/null || pip install -e .
>    ```
>    (Use `uv pip install -e .` if uv is available — check with `which uv`)
>
> **What NOT to do:**
> - Do not implement server logic, models, or data clients — only stubs with `pass` or `TODO` comments
> - Do not add `basedosdados` or `google-cloud-bigquery` — those are out of scope for this sprint
> - Do not add `crunchbase` integration — explicitly out of scope per PRD
>
> **Validation:** run from repo root:
> ```bash
> cd ~/git/br-startup-mcp && python -c "import br_startup_mcp; print('ok')"
> ```
> Expected: prints `ok` without error.
>
> Also verify structure:
> ```bash
> ls ~/git/br-startup-mcp/src/br_startup_mcp/models/
> ls ~/git/br-startup-mcp/src/br_startup_mcp/data/
> ls ~/git/br-startup-mcp/src/br_startup_mcp/tools/
> ```
>
> **Result format:** when done, output a result block:
> ```
> ## Result
> task_id: D1
> status: success | partial | failed
> summary: <1-2 sentences, what was done>
> errors: <list or empty>
> validation_result: <output of validation command>
> files_changed:
> - <paths>
> ```

**Acceptance:** `cd ~/git/br-startup-mcp && python -c "import br_startup_mcp; print('ok')"` → prints `ok`
**Human test:** No manual test needed — covered by automated validation

---

### D2 — Pydantic models BndesOperation e CvmOffer

**Executor:** sonnet
**Isolation:** none
**Depends on:** D1
**Predicate:** Modelos de dados fiéis à arquitetura definida em docs/architecture.md
**Files touched:**
- `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py`

**Prompt for subagent:**

> You are implementing: Pydantic v2 models for BndesOperation and CvmOffer entities in br-startup-mcp.
>
> **Context:**
> - Repo: `br-startup-mcp` at `~/git/br-startup-mcp/`
> - Stack: Python 3.11+, pydantic v2
> - D1 already created the project structure. File to edit: `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py`
> - Architecture source of truth: `~/git/br-startup-mcp/docs/architecture.md` — read it before writing the models
> - No sibling dependencies for this deliverable beyond D1 structure
>
> **What to do:**
>
> 1. Read `~/git/br-startup-mcp/docs/architecture.md` — sections "Entidade: BndesOperation" and "Entidade: CvmOffer"
>
> 2. Write `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py` with:
>
>    For **BndesOperation** (from architecture.md):
>    ```python
>    from pydantic import BaseModel, Field
>    from datetime import date
>    from typing import Optional
>    import hashlib
>
>    class BndesOperation(BaseModel):
>        id: str                          # generated: hash of cnpj+data_contratacao+produto
>        cnpj_cliente: str
>        razao_social: str
>        produto_bndes: str
>        valor_brl: float
>        data_contratacao: date
>        setor_bndes: Optional[str] = None
>        porte: Optional[str] = None
>        municipio: Optional[str] = None
>        uf: Optional[str] = None
>    ```
>
>    For **CvmOffer** (from architecture.md):
>    ```python
>    class CvmOffer(BaseModel):
>        id: str                          # generated: hash of cnpj+data_registro+plataforma
>        cnpj_emissora: str
>        razao_social: str
>        plataforma: str
>        valor_alvo_brl: float
>        valor_captado_brl: Optional[float] = None
>        data_registro: date
>        data_encerramento: Optional[date] = None
>        status: str
>        tipo_valor_mobiliario: Optional[str] = None
>    ```
>
>    Add a helper function `make_id(*parts: str) -> str` that returns `hashlib.md5("_".join(parts).encode()).hexdigest()[:12]`
>
> 3. Add model_config with `from_attributes=True` to both models (needed for ORM-style construction from DuckDB rows)
>
> **What NOT to do:**
> - Do not add Startup, Founder, Round, Investor entities — those are out of scope for this sprint
> - Do not modify pyproject.toml or any other file — only entities.py
>
> **Validation:**
> ```bash
> cd ~/git/br-startup-mcp && python -c "
> from br_startup_mcp.models.entities import BndesOperation, CvmOffer
> from datetime import date
> op = BndesOperation(id='abc', cnpj_cliente='00.000.000/0001-00', razao_social='Test', produto_bndes='BNDES Fintechs', valor_brl=100000.0, data_contratacao=date(2024,1,1))
> print('BndesOperation OK:', op.cnpj_cliente)
> offer = CvmOffer(id='xyz', cnpj_emissora='00.000.000/0001-00', razao_social='Test', plataforma='TestPlat', valor_alvo_brl=500000.0, data_registro=date(2024,1,1), status='ativa')
> print('CvmOffer OK:', offer.status)
> "
> ```
> Expected: both lines print without error.
>
> **Result format:** when done, output a result block:
> ```
> ## Result
> task_id: D2
> status: success | partial | failed
> summary: <1-2 sentences, what was done>
> errors: <list or empty>
> validation_result: <output of validation command>
> files_changed:
> - <paths>
> ```

**Acceptance:** validation script above exits 0 and prints both OK lines
**Human test:** No manual test needed — covered by automated validation

---

### D3 — CVM data client (fetch + normalize + DuckDB cache)

**Executor:** sonnet
**Isolation:** none
**Depends on:** D2
**Predicate:** Pipeline CVM end-to-end: dados reais chegam do portal CVM, normalizam para CvmOffer, persistem em DuckDB
**Files touched:**
- `~/git/br-startup-mcp/src/br_startup_mcp/data/cvm.py`

**Prompt for subagent:**

> You are implementing: CVM data client that fetches real equity crowdfunding data from CVM's open data portal and caches it in DuckDB.
>
> **Context:**
> - Repo: `br-startup-mcp` at `~/git/br-startup-mcp/`
> - Stack: Python 3.11+, httpx (sync or async), duckdb, pandas, pydantic v2
> - D2 already created `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py` with `CvmOffer` model
> - Use `CvmOffer` from `br_startup_mcp.models.entities` — do NOT redefine it
> - CVM portal: https://dados.cvm.gov.br/ — data is public, no authentication needed
> - Target dataset: equity crowdfunding offers (Resolução CVM 88/2022)
>   - CKAN API endpoint: `https://dados.cvm.gov.br/api/3/action/datastore_search?resource_id=<id>&limit=100`
>   - OR direct CSV: try `https://dados.cvm.gov.br/dados/CFD/DOC/REG_OF/dados/inf_cfd_reg_of.csv` (verify URL is reachable)
>   - Fallback: use CKAN package search to find the crowdfunding dataset: `https://dados.cvm.gov.br/api/3/action/package_search?q=crowdfunding`
>
> **What to do:**
>
> 1. Write `~/git/br-startup-mcp/src/br_startup_mcp/data/cvm.py` with:
>
>    a. A function `fetch_cvm_crowdfunding_raw() -> list[dict]` that:
>       - Tries to download the CSV directly via httpx
>       - If that fails, falls back to CKAN API search to find the correct resource
>       - Returns a list of dicts (one per row)
>       - Prints progress to stderr (not stdout — MCP uses stdio)
>
>    b. A function `normalize_cvm_offer(row: dict) -> Optional[CvmOffer]` that:
>       - Maps CSV column names to CvmOffer fields (column names vary — inspect the actual data)
>       - Parses dates with `datetime.strptime` (try multiple formats)
>       - Generates `id` via `make_id(cnpj_emissora, str(data_registro), plataforma)`
>       - Returns None (and logs to stderr) if required fields are missing/unparseable
>
>    c. A function `load_to_duckdb(offers: list[CvmOffer], db_path: str) -> int` that:
>       - Connects to DuckDB at `db_path`
>       - Creates table `cvm_offers` if not exists (schema matching CvmOffer fields)
>       - Upserts records using `INSERT OR REPLACE` (or DuckDB equivalent)
>       - Returns count of inserted records
>
>    d. A main entry `sync_cvm(db_path: str = "./data/cache.duckdb") -> int` that:
>       - Calls fetch → normalize (filter None) → load_to_duckdb
>       - Returns total records loaded
>
>    e. A query function `query_cvm_offers(db_path: str, cnpj: Optional[str] = None, status: Optional[str] = None, limit: int = 20) -> list[CvmOffer]` that:
>       - Opens DuckDB, runs SELECT with optional WHERE filters
>       - Returns list of CvmOffer
>
> 2. Important: all print/log statements must go to `sys.stderr`, never `sys.stdout`
>
> 3. Handle network errors gracefully — if the URL is unreachable, raise a clear exception with message
>
> **What NOT to do:**
> - Do not implement BNDES client — that's D4
> - Do not implement MCP tools — that's D5
> - Do not modify entities.py — only cvm.py
>
> **Validation:** (requires internet access)
> ```bash
> cd ~/git/br-startup-mcp && python -c "
> from br_startup_mcp.data.cvm import sync_cvm, query_cvm_offers
> import tempfile, os
> db = tempfile.mktemp(suffix='.duckdb')
> n = sync_cvm(db_path=db)
> print(f'Loaded {n} CVM offers')
> results = query_cvm_offers(db_path=db, limit=3)
> for r in results:
>     print(f'  {r.cnpj_emissora} | {r.razao_social[:30]} | {r.status}')
> os.unlink(db)
> "
> ```
> Expected: prints "Loaded N CVM offers" with N > 0, then prints 3 offer lines.
>
> **Result format:** when done, output a result block:
> ```
> ## Result
> task_id: D3
> status: success | partial | failed
> summary: <1-2 sentences, what was done>
> errors: <list or empty>
> validation_result: <output of validation command>
> files_changed:
> - <paths>
> ```

**Acceptance:** validation script prints "Loaded N CVM offers" with N > 0
**Human test:** No manual test needed — covered by automated validation (requires internet to CVM portal)

---

### D4 — BNDES data client (fetch + normalize + DuckDB cache)

**Executor:** sonnet
**Isolation:** none
**Depends on:** D2
**Predicate:** Pipeline BNDES end-to-end: dados reais chegam do portal BNDES, normalizam para BndesOperation, persistem em DuckDB
**Files touched:**
- `~/git/br-startup-mcp/src/br_startup_mcp/data/bndes.py`

**Prompt for subagent:**

> You are implementing: BNDES data client that fetches real financing operations from BNDES open data portal and caches them in DuckDB.
>
> **Context:**
> - Repo: `br-startup-mcp` at `~/git/br-startup-mcp/`
> - Stack: Python 3.11+, httpx (sync), duckdb, pandas, pydantic v2
> - D2 already created `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py` with `BndesOperation` model
> - Use `BndesOperation` from `br_startup_mcp.models.entities` — do NOT redefine it
> - BNDES portal: https://dadosabertos.bndes.gov.br/ — public, no authentication
> - Target dataset: contracted operations (operações contratadas)
>   - CKAN API: `https://dadosabertos.bndes.gov.br/api/3/action/datastore_search?resource_id=<id>&limit=100`
>   - Package list: `https://dadosabertos.bndes.gov.br/api/3/action/package_list`
>   - Search for "operações contratadas": `https://dadosabertos.bndes.gov.br/api/3/action/package_search?q=operacoes+contratadas`
>   - Known CSV URL pattern to try: `https://dadosabertos.bndes.gov.br/dataset/operacoes-contratadas-financiamento/resource/<resource_id>`
>
> **What to do:**
>
> 1. Write `~/git/br-startup-mcp/src/br_startup_mcp/data/bndes.py` with:
>
>    a. A function `fetch_bndes_operations_raw(limit: int = 500) -> list[dict]` that:
>       - Queries CKAN API to discover the "operações contratadas" dataset/resource
>       - Fetches up to `limit` records via CKAN datastore_search (paginate if needed for first batch)
>       - Alternatively tries direct CSV download if CKAN fails
>       - Returns list of dicts
>       - All progress to stderr
>
>    b. A function `normalize_bndes_operation(row: dict) -> Optional[BndesOperation]` that:
>       - Maps actual column names from BNDES data to BndesOperation fields
>       - Required: cnpj_cliente, razao_social, produto_bndes, valor_brl, data_contratacao
>       - Optional: setor_bndes, porte, municipio, uf
>       - Generates `id` via `make_id(cnpj_cliente, str(data_contratacao), produto_bndes)`
>       - Returns None if required fields are missing
>
>    c. A function `load_to_duckdb(ops: list[BndesOperation], db_path: str) -> int` that:
>       - Creates table `bndes_operations` if not exists
>       - Upserts records
>       - Returns count inserted
>
>    d. A main entry `sync_bndes(db_path: str = "./data/cache.duckdb", limit: int = 500) -> int`
>
>    e. A query function `query_bndes_operations(db_path: str, cnpj: Optional[str] = None, produto: Optional[str] = None, limit: int = 20) -> list[BndesOperation]`
>
> 2. All print/log to `sys.stderr` only
>
> 3. Handle network errors gracefully
>
> **What NOT to do:**
> - Do not implement CVM client — that's D3 (already done)
> - Do not implement MCP tools — that's D5
> - Do not modify entities.py — only bndes.py
>
> **Validation:** (requires internet access)
> ```bash
> cd ~/git/br-startup-mcp && python -c "
> from br_startup_mcp.data.bndes import sync_bndes, query_bndes_operations
> import tempfile, os
> db = tempfile.mktemp(suffix='.duckdb')
> n = sync_bndes(db_path=db, limit=100)
> print(f'Loaded {n} BNDES operations')
> results = query_bndes_operations(db_path=db, limit=3)
> for r in results:
>     print(f'  {r.cnpj_cliente} | {r.razao_social[:30]} | {r.valor_brl}')
> os.unlink(db)
> "
> ```
> Expected: prints "Loaded N BNDES operations" with N > 0.
>
> **Result format:** when done, output a result block:
> ```
> ## Result
> task_id: D4
> status: success | partial | failed
> summary: <1-2 sentences, what was done>
> errors: <list or empty>
> validation_result: <output of validation command>
> files_changed:
> - <paths>
> ```

**Acceptance:** validation script prints "Loaded N BNDES operations" with N > 0
**Human test:** No manual test needed — covered by automated validation (requires internet to BNDES portal)

---

### D5 — MCP server com tools CVM e BNDES

**Executor:** sonnet
**Isolation:** none
**Depends on:** D3, D4
**Predicate:** MCP server funcional com stdio transport expondo tools que retornam dados reais de CVM e BNDES
**Files touched:**
- `~/git/br-startup-mcp/src/br_startup_mcp/server.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/tools/regulatory.py`
- `~/git/br-startup-mcp/src/br_startup_mcp/__main__.py`

**Prompt for subagent:**

> You are implementing: MCP server for br-startup-mcp that exposes real government data tools via stdio transport.
>
> **Context:**
> - Repo: `br-startup-mcp` at `~/git/br-startup-mcp/`
> - Stack: Python 3.11+, `mcp` package (Anthropic official Python SDK), pydantic v2
> - D3 created `~/git/br-startup-mcp/src/br_startup_mcp/data/cvm.py` with `query_cvm_offers(db_path, cnpj, status, limit) -> list[CvmOffer]` and `sync_cvm(db_path) -> int`
> - D4 created `~/git/br-startup-mcp/src/br_startup_mcp/data/bndes.py` with `query_bndes_operations(db_path, cnpj, produto, limit) -> list[BndesOperation]` and `sync_bndes(db_path, limit) -> int`
> - D2 created `~/git/br-startup-mcp/src/br_startup_mcp/models/entities.py` with `CvmOffer` and `BndesOperation` pydantic models
> - MCP Python SDK pattern:
>   ```python
>   from mcp.server import Server
>   from mcp.server.stdio import stdio_server
>   from mcp import types
>   import asyncio
>
>   server = Server("br-startup-mcp")
>
>   @server.list_tools()
>   async def list_tools() -> list[types.Tool]:
>       return [types.Tool(name="...", description="...", inputSchema={...})]
>
>   @server.call_tool()
>   async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
>       ...
>
>   async def main():
>       async with stdio_server() as (read_stream, write_stream):
>           await server.run(read_stream, write_stream, server.create_initialization_options())
>   ```
>
> **What to do:**
>
> 1. Create `~/git/br-startup-mcp/src/br_startup_mcp/tools/regulatory.py`:
>    - Tool `get_cvm_crowdfunding_offers`: parameters `cnpj` (optional str), `status` (optional str), `limit` (int, default 20)
>    - Tool `get_bndes_financing`: parameters `cnpj` (optional str), `produto` (optional str), `limit` (int, default 20)
>    - Each tool calls the corresponding query function and returns JSON-serialized results
>    - If DuckDB cache is empty (0 results), trigger sync first (call `sync_cvm` or `sync_bndes`)
>
> 2. Create `~/git/br-startup-mcp/src/br_startup_mcp/server.py`:
>    - Import tools from `regulatory.py`
>    - Declare 2 tools in `list_tools()`: `get_cvm_crowdfunding_offers` and `get_bndes_financing`
>    - inputSchema for each: JSON Schema dict with `type: object`, `properties`, `required: []`
>    - `call_tool()` dispatches to the right function
>    - `db_path` comes from env var `DUCKDB_PATH` with default `./data/cache.duckdb`
>    - Load dotenv at startup: `from dotenv import load_dotenv; load_dotenv()`
>    - `async def main()` with stdio_server as shown in the context pattern
>    - Ensure `data/` directory exists at startup: `os.makedirs(os.path.dirname(db_path), exist_ok=True)`
>
> 3. Update `~/git/br-startup-mcp/src/br_startup_mcp/__main__.py`:
>    ```python
>    import asyncio
>    from br_startup_mcp.server import main
>    asyncio.run(main())
>    ```
>
> 4. Tool return format: each tool returns `[types.TextContent(type="text", text=json.dumps(result, default=str, ensure_ascii=False, indent=2))]`
>
> 5. Error handling: wrap tool execution in try/except, return error as TextContent with error details
>
> **What NOT to do:**
> - Do not implement any other tools (get_startup_by_cnpj, etc.) — those are future nodes
> - Do not add HTTP transport — stdio only
> - Do not modify cvm.py, bndes.py, or entities.py
>
> **Validation — smoke test:**
> First, ensure data dir exists:
> ```bash
> mkdir -p ~/git/br-startup-mcp/data
> ```
> Then run the smoke test:
> ```bash
> cd ~/git/br-startup-mcp && echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}' | timeout 10 python -m br_startup_mcp 2>/dev/null | head -1
> ```
> Expected: a JSON line containing `"result"` with `protocolVersion`.
>
> Also verify tools/list works:
> ```bash
> cd ~/git/br-startup-mcp && python -c "
> import subprocess, json
> msg = json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'test','version':'0.1'}}})
> # Just import-test the server
> from br_startup_mcp.server import server
> import asyncio
> tools = asyncio.run(server.list_tools())
> print('Tools:', [t.name for t in tools])
> "
> ```
> Expected: prints `Tools: ['get_cvm_crowdfunding_offers', 'get_bndes_financing']`
>
> **Result format:** when done, output a result block:
> ```
> ## Result
> task_id: D5
> status: success | partial | failed
> summary: <1-2 sentences, what was done>
> errors: <list or empty>
> validation_result: <output of validation command>
> files_changed:
> - <paths>
> ```

**Acceptance:** `python -c "from br_startup_mcp.server import server; import asyncio; tools = asyncio.run(server.list_tools()); assert len(tools) >= 1"` exits 0
**Human test:** No manual test needed — covered by automated validation

---

## Dependency Graph

```
D1 ──→ D2 ──┬──→ D3 ──┐
             │          ├──→ D5
             └──→ D4 ──┘
```

D3 and D4 are parallel (different files, both depend on D2).
D5 depends on D3 and D4.

---

## Batches

**Batch 1 (sequential):** D1
Gate: verify `python -c "import br_startup_mcp"` succeeds before continuing

**Batch 2 (sequential):** D2
Gate: verify models import correctly before continuing

**Batch 3 (parallel):** D3, D4
_(no gate — can continue to D5 after both complete)_

**Batch 4 (sequential):** D5

---

## Execution DAG

task: D1
title: Setup projeto Python — pyproject.toml e estrutura de diretórios
depends_on:
predicate: Setup Python funcional com estrutura de diretórios e dependências declaradas
executor: sonnet
isolation: none
batch: 1
files: pyproject.toml, src/br_startup_mcp/__init__.py, src/br_startup_mcp/__main__.py, src/br_startup_mcp/models/__init__.py, src/br_startup_mcp/data/__init__.py, src/br_startup_mcp/tools/__init__.py, .env.example, .gitignore
max_retries: 2
acceptance: cd ~/git/br-startup-mcp && python -c "import br_startup_mcp; print('ok')" exits 0
human_test: No manual test needed — covered by automated validation

task: D2
title: Pydantic models BndesOperation e CvmOffer
depends_on: D1
predicate: Modelos de dados fiéis à arquitetura definida em docs/architecture.md
executor: sonnet
isolation: none
batch: 2
files: src/br_startup_mcp/models/entities.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.models.entities import BndesOperation, CvmOffer; print('ok')" exits 0
human_test: No manual test needed — covered by automated validation

task: D3
title: CVM data client — fetch, normalize, DuckDB cache
depends_on: D2
predicate: Pipeline CVM end-to-end com dados reais chegando do portal CVM
executor: sonnet
isolation: none
batch: 3
files: src/br_startup_mcp/data/cvm.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.data.cvm import sync_cvm; import tempfile; n=sync_cvm(db_path=tempfile.mktemp(suffix='.duckdb')); assert n > 0, f'Expected >0 records, got {n}'" exits 0
human_test: No manual test needed — covered by automated validation

task: D4
title: BNDES data client — fetch, normalize, DuckDB cache
depends_on: D2
predicate: Pipeline BNDES end-to-end com dados reais chegando do portal BNDES
executor: sonnet
isolation: none
batch: 3
files: src/br_startup_mcp/data/bndes.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.data.bndes import sync_bndes; import tempfile; n=sync_bndes(db_path=tempfile.mktemp(suffix='.duckdb'), limit=100); assert n > 0, f'Expected >0 records, got {n}'" exits 0
human_test: No manual test needed — covered by automated validation

task: D5
title: MCP server com tools CVM e BNDES via stdio
depends_on: D3, D4
predicate: MCP server funcional com stdio transport expondo tools que retornam dados reais
executor: sonnet
isolation: none
batch: 4
files: src/br_startup_mcp/server.py, src/br_startup_mcp/tools/regulatory.py, src/br_startup_mcp/__main__.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.server import server; import asyncio; tools=asyncio.run(server.list_tools()); assert len(tools)>=1" exits 0
human_test: No manual test needed — covered by automated validation

---

## Infrastructure

- [ ] New secrets: none (CVM e BNDES são públicos sem autenticação)
- [ ] CI/CD: no changes
- [ ] New dependencies: mcp>=1.0.0, httpx>=0.27.0, pydantic>=2.0.0, duckdb>=0.10.0, python-dotenv>=1.0.0, pandas>=2.0.0
- [ ] Setup script: `pip install -e .` or `uv pip install -e .` from repo root after D1
- [ ] Data migration: none (DuckDB cache created fresh on first run)

---

## Rollback

If something goes wrong:

```bash
# Remove generated source files
rm -rf ~/git/br-startup-mcp/src/
rm -f ~/git/br-startup-mcp/pyproject.toml
rm -f ~/git/br-startup-mcp/.env.example

# Remove DuckDB cache
rm -f ~/git/br-startup-mcp/data/cache.duckdb

# Restore from git
git -C ~/git/br-startup-mcp checkout -- .
```
