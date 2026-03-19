---
node: pipeline-cnpj-receita
predicate: "O agente não consegue integrar a base CNPJ da Receita Federal como fonte âncora — escolher estratégia de acesso e implementar pipeline para dados cadastrais/societários"
created: 2026-03-19
status: approved
---

# Plan — Pipeline CNPJ Receita Federal

## Problem

O MCP server `br-startup-mcp` possui pipelines funcionais para CVM e BNDES (entregues por `pipeline-gov-aberto`), mas não tem acesso à Receita Federal — a fonte âncora central. Toda startup tem CNPJ, que é o identificador que permite cruzar todas as outras fontes. Os modelos `Startup` e `Founder` estão especificados em `docs/architecture.md` mas não implementados. Este nó entrega o data client CNPJ (via BrasilAPI) e as tools MCP correspondentes.

## Project Context

Tree: mcp-startup-vc
Root: "O agente não consegue montar um perfil completo de startups brasileiras..."

Satisfied siblings:
- `pipeline-gov-aberto`: pipeline fetch-normalize-cache funcional (cvm.py, bndes.py), padrões estabelecidos
  capabilities: padrão de data client (fetch_raw → normalize → load_to_duckdb → query), _ensure_data, make_id
  files: src/br_startup_mcp/data/cvm.py, src/br_startup_mcp/data/bndes.py, src/br_startup_mcp/tools/regulatory.py, src/br_startup_mcp/models/entities.py
- `arquitetura-mcp`: docs/architecture.md com campos completos de Startup e Founder

Active: .fractal/mcp-startup-vc/dados-reais-via-mcp/pipeline-cnpj-receita

## Functional Requirements

FR1: `cnpj.py` implementa `fetch_cnpj_raw(cnpj)` via BrasilAPI e `normalize_startup()` retorna modelo `Startup` populado com dados reais
validates: critério 1 e 2 do PRD — data client + modelos Pydantic com dados reais
verified_by: D1 acceptance

FR2: Tabelas `startups` e `founders` no DuckDB com upsert funcional via `load_startup_to_duckdb()`
validates: critério 3 do PRD — cache em DuckDB
verified_by: D1 acceptance

FR3: Tool MCP `get_startup_by_cnpj` retorna dados reais de CNPJ conhecido (smoke test)
validates: critério 4a e 5 do PRD — tool funcional + smoke test
verified_by: D2 acceptance

FR4: Tool MCP `search_startups` filtra cache por CNAE, cidade, estado, data de abertura
validates: critério 4b do PRD — search com filtros
verified_by: D2 acceptance

## Deliverables

### D1 — Data client CNPJ + modelos Pydantic + cache DuckDB

**Executor:** sonnet
**Isolation:** none
**Depends on:** none
**Predicate:** `cnpj.py` busca dados reais da BrasilAPI e normaliza para modelos `Startup` + `Founder` com cache DuckDB
**Files touched:**
- `src/br_startup_mcp/data/cnpj.py` (novo)
- `src/br_startup_mcp/models/entities.py` (adição de classes Startup e Founder)

**Prompt for subagent:**

> Você está implementando o data client CNPJ (`cnpj.py`) e os modelos Pydantic `Startup` e `Founder` para o MCP server `br-startup-mcp`.
>
> **Contexto:**
> - Repo: `br-startup-mcp` em `/Users/rmolines/git/br-startup-mcp/`
> - Stack: Python 3.11+, httpx, pydantic v2, duckdb (todos já no pyproject.toml)
> - Padrão estabelecido pelos siblings: siga exatamente o padrão de `src/br_startup_mcp/data/cvm.py` e `src/br_startup_mcp/data/bndes.py` (leia ambos antes de escrever)
> - Architecture spec: `docs/architecture.md` define os campos de `Startup` e `Founder` — use-os literalmente (seções "Entidade: Startup" e "Entidade: Founder")
> - Use `make_id` de `src/br_startup_mcp/models/entities.py` (já implementado pelo sibling `pipeline-gov-aberto`)
>
> **O que fazer:**
>
> 1. Leia `src/br_startup_mcp/data/cvm.py`, `src/br_startup_mcp/data/bndes.py` e `src/br_startup_mcp/models/entities.py` para entender o padrão.
>
> 2. Adicione ao final de `src/br_startup_mcp/models/entities.py` (após imports existentes, adicione `datetime` se necessário):
>
>    ```python
>    from datetime import datetime  # adicionar se não existir
>
>    class Startup(BaseModel):
>        """Dados cadastrais de startup da Receita Federal."""
>        model_config = {"from_attributes": True}
>        cnpj: str
>        razao_social: str
>        nome_fantasia: Optional[str] = None
>        situacao_cadastral: str
>        data_abertura: date
>        capital_social_brl: float
>        cnae_principal: str
>        cnaes_secundarios: list[str] = []
>        natureza_juridica: str
>        porte: str
>        endereco_logradouro: Optional[str] = None
>        cidade: str
>        estado: str
>        cep: Optional[str] = None
>        updated_at: datetime
>
>    class Founder(BaseModel):
>        """Sócio/fundador derivado do quadro societário da Receita Federal."""
>        model_config = {"from_attributes": True}
>        id: str
>        cnpj_empresa: str
>        nome: str
>        cpf_cnpj: Optional[str] = None
>        qualificacao: str
>        participacao_pct: Optional[float] = None
>        data_entrada: Optional[date] = None
>    ```
>
> 3. Crie `src/br_startup_mcp/data/cnpj.py` com:
>
>    - `BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"`
>    - `_clean_cnpj(cnpj: str) -> str`: remove pontos, barras, hífens, espaços — retorna somente dígitos
>    - `fetch_cnpj_raw(cnpj: str) -> dict`: GET na BrasilAPI (cnpj já limpo), timeout=15s, log para stderr, raise RuntimeError em falha HTTP
>    - `normalize_startup(data: dict) -> Optional[Startup]`: mapeia campos BrasilAPI → Startup:
>      - `cnpj` → `cnpj` (via `_clean_cnpj`)
>      - `razao_social` → `razao_social`
>      - `nome_fantasia` → `nome_fantasia`
>      - `descricao_situacao_cadastral` → `situacao_cadastral`
>      - `data_inicio_atividade` (string `YYYY-MM-DD`) → `data_abertura`
>      - `capital_social` (float) → `capital_social_brl`
>      - `cnae_fiscal` (int) → `cnae_principal` (str, zero-pad para 7 dígitos: `f"{cnae:07d}"`)
>      - `cnaes_secundarios` (lista de dicts com campo `codigo`) → `cnaes_secundarios` (lista de str)
>      - `natureza_juridica` → `natureza_juridica`
>      - `porte` → `porte`
>      - `logradouro` → `endereco_logradouro`
>      - `municipio` → `cidade`
>      - `uf` → `estado`
>      - `cep` → `cep`
>      - `updated_at = datetime.utcnow()`
>      - Retorna None em caso de parse error (print para stderr)
>    - `normalize_founder(socio: dict, cnpj_empresa: str) -> Optional[Founder]`: mapeia sócio BrasilAPI:
>      - `nome_socio` → `nome`
>      - `cnpj_cpf_do_socio` → `cpf_cnpj`
>      - `qualificacao_socio` → `qualificacao`
>      - `data_entrada_sociedade` (string `YYYY-MM-DD`) → `data_entrada`
>      - `id = make_id(cnpj_empresa, nome_socio)`
>      - `cnpj_empresa = cnpj_empresa`
>      - `participacao_pct = None` (BrasilAPI não fornece)
>      - Retorna None em erro
>    - SQL DDL em constantes:
>      ```python
>      _CREATE_TABLE_STARTUPS = """
>      CREATE TABLE IF NOT EXISTS startups (
>          cnpj VARCHAR PRIMARY KEY,
>          razao_social VARCHAR,
>          nome_fantasia VARCHAR,
>          situacao_cadastral VARCHAR,
>          data_abertura DATE,
>          capital_social_brl DOUBLE,
>          cnae_principal VARCHAR,
>          cnaes_secundarios VARCHAR,
>          natureza_juridica VARCHAR,
>          porte VARCHAR,
>          endereco_logradouro VARCHAR,
>          cidade VARCHAR,
>          estado VARCHAR,
>          cep VARCHAR,
>          updated_at TIMESTAMP
>      )"""
>
>      _CREATE_TABLE_FOUNDERS = """
>      CREATE TABLE IF NOT EXISTS founders (
>          id VARCHAR PRIMARY KEY,
>          cnpj_empresa VARCHAR,
>          nome VARCHAR,
>          cpf_cnpj VARCHAR,
>          qualificacao VARCHAR,
>          participacao_pct DOUBLE,
>          data_entrada DATE
>      )"""
>      ```
>      Nota: `cnaes_secundarios` é serializado como JSON string (use `json.dumps(list)`)
>    - `load_startup_to_duckdb(startup: Startup, founders: list[Founder], db_path: str) -> None`: cria tabelas + upsert startup + upsert founders (INSERT OR REPLACE)
>    - `get_startup_by_cnpj(cnpj: str, db_path: str) -> Optional[Startup]`:
>      1. Tenta ler do cache DuckDB primeiro
>      2. Se não encontrar (tabela inexistente ou 0 rows), chama `fetch_cnpj_raw`, normaliza, cacheia com `load_startup_to_duckdb`, retorna
>      3. Se BrasilAPI retornar erro 404, retorna None
>    - `query_startups(db_path: str, cnae: Optional[str]=None, cidade: Optional[str]=None, estado: Optional[str]=None, data_abertura_min: Optional[str]=None, limit: int=20) -> list[Startup]`:
>      - Se tabela não existir, retorna lista vazia
>      - Filtros: `cnae_principal ILIKE ?` para cnae, `cidade ILIKE ?` para cidade, `estado = ?` para estado, `data_abertura >= ?` para data_abertura_min
>      - Retorna lista de Startup reconstruídos (cnaes_secundarios via `json.loads`)
>
> **O que NÃO fazer:**
> - Não implementar BigQuery/Base dos Dados (fora de escopo)
> - Não implementar as MCP tools (esse é o D2)
> - Não implementar cache TTL (deferred)
> - Não adicionar campos Crunchbase ao modelo Startup (deferred)
> - Não modificar arquivos existentes além de `entities.py`
>
> **Validação:**
> ```bash
> cd /Users/rmolines/git/br-startup-mcp
> python -c "
> import os; os.environ['DUCKDB_PATH'] = '/tmp/test_cnpj_d1.duckdb'
> from br_startup_mcp.data.cnpj import fetch_cnpj_raw, normalize_startup, normalize_founder, get_startup_by_cnpj
> from br_startup_mcp.models.entities import Startup, Founder
> data = fetch_cnpj_raw('33000167000101')
> s = normalize_startup(data)
> assert s is not None and s.cnpj == '33000167000101', f'Got: {s}'
> founders = [f for f in [normalize_founder(socio, s.cnpj) for socio in data.get('qsa', [])] if f]
> s2 = get_startup_by_cnpj('33000167000101', '/tmp/test_cnpj_d1.duckdb')
> assert s2 is not None
> print('OK:', s.razao_social, '|', len(founders), 'founders | cache works')
> "
> ```
>
> **Result format:**
> ```
> ## Result
> task_id: D1
> status: success | partial | failed
> summary: <1-2 frases>
> errors: <lista ou vazio>
> validation_result: <saída do comando de validação>
> files_changed:
> - src/br_startup_mcp/data/cnpj.py
> - src/br_startup_mcp/models/entities.py
> ```

**Acceptance:** python -c "from br_startup_mcp.data.cnpj import fetch_cnpj_raw, normalize_startup; s = normalize_startup(fetch_cnpj_raw('33000167000101')); assert s and s.cnpj == '33000167000101'" → sem exceção
**Human test:** No manual test needed — covered by automated validation

---

### D2 — MCP tools get_startup_by_cnpj e search_startups

**Executor:** sonnet
**Isolation:** none
**Depends on:** D1
**Predicate:** Tools `get_startup_by_cnpj` e `search_startups` expostas no MCP server, smoke test retorna dados reais
**Files touched:**
- `src/br_startup_mcp/tools/startup.py` (novo)
- `src/br_startup_mcp/server.py` (adição de tools)

**Prompt for subagent:**

> Você está integrando as tools MCP `get_startup_by_cnpj` e `search_startups` ao server `br-startup-mcp`.
>
> **Contexto:**
> - Repo: `br-startup-mcp` em `/Users/rmolines/git/br-startup-mcp/`
> - Padrão das tools: leia `src/br_startup_mcp/tools/regulatory.py` — use o mesmo padrão de `_db_path()`, `_ensure_data()`, e retorno JSON
> - Data client disponível (criado em D1 deste nó): `src/br_startup_mcp/data/cnpj.py`:
>   - `get_startup_by_cnpj(cnpj: str, db_path: str) -> Optional[Startup]`
>   - `query_startups(db_path: str, cnae, cidade, estado, data_abertura_min, limit) -> list[Startup]`
>   - `_clean_cnpj(cnpj: str) -> str`
> - Server: `src/br_startup_mcp/server.py` — adicione as novas tools à lista existente sem remover as anteriores
> - Models: `src/br_startup_mcp/models/entities.py` contém `Startup` e `Founder` (criados em D1)
>
> **O que fazer:**
>
> 1. Leia `src/br_startup_mcp/tools/regulatory.py` e `src/br_startup_mcp/server.py` integralmente.
>
> 2. Crie `src/br_startup_mcp/tools/startup.py`:
>    ```python
>    """MCP tools for Receita Federal CNPJ data."""
>    import json
>    import os
>    from typing import Optional
>
>    import duckdb
>
>    from br_startup_mcp.data.cnpj import _clean_cnpj, get_startup_by_cnpj as _fetch_startup, query_startups
>
>
>    def _db_path() -> str:
>        return os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")
>
>
>    def get_startup_by_cnpj(cnpj: str, include_founders: bool = True) -> str:
>        """Busca dados cadastrais e societários de uma startup pelo CNPJ via Receita Federal."""
>        db = _db_path()
>        cnpj_clean = _clean_cnpj(cnpj)
>        startup = _fetch_startup(cnpj_clean, db_path=db)
>        if startup is None:
>            return json.dumps({"error": f"CNPJ {cnpj} não encontrado"}, ensure_ascii=False)
>        result = {"startup": startup.model_dump(mode="json")}
>        if include_founders:
>            try:
>                con = duckdb.connect(db, read_only=True)
>                rows = con.execute(
>                    "SELECT * FROM founders WHERE cnpj_empresa = ?", [cnpj_clean]
>                ).fetchall()
>                cols = ["id", "cnpj_empresa", "nome", "cpf_cnpj", "qualificacao",
>                        "participacao_pct", "data_entrada"]
>                result["founders"] = [dict(zip(cols, r)) for r in rows]
>                con.close()
>            except Exception:
>                result["founders"] = []
>        return json.dumps(result, default=str, ensure_ascii=False, indent=2)
>
>
>    def search_startups(
>        cnae: Optional[str] = None,
>        cidade: Optional[str] = None,
>        estado: Optional[str] = None,
>        data_abertura_min: Optional[str] = None,
>        limit: int = 20,
>    ) -> str:
>        """Busca startups no cache local por CNAE, cidade, estado ou data de abertura."""
>        db = _db_path()
>        startups = query_startups(
>            db_path=db, cnae=cnae, cidade=cidade, estado=estado,
>            data_abertura_min=data_abertura_min, limit=limit,
>        )
>        return json.dumps(
>            [s.model_dump(mode="json") for s in startups],
>            default=str, ensure_ascii=False, indent=2,
>        )
>    ```
>
> 3. Em `src/br_startup_mcp/server.py`:
>    - Adicione ao `list_tools()` as duas novas tools (mantenha as existentes):
>      ```python
>      types.Tool(
>          name="get_startup_by_cnpj",
>          description=(
>              "Busca dados cadastrais e quadro societário de uma startup pelo CNPJ "
>              "via Receita Federal (BrasilAPI). Retorna razão social, CNAE, cidade, "
>              "estado, capital social, situação cadastral e sócios."
>          ),
>          inputSchema={
>              "type": "object",
>              "properties": {
>                  "cnpj": {"type": "string", "description": "CNPJ da empresa (com ou sem formatação)"},
>                  "include_founders": {"type": "boolean", "description": "Incluir quadro societário (default: true)", "default": True},
>              },
>              "required": ["cnpj"],
>          },
>      ),
>      types.Tool(
>          name="search_startups",
>          description=(
>              "Busca startups no cache local por CNAE, cidade, estado ou data de abertura. "
>              "Requer que CNPJs tenham sido previamente consultados via get_startup_by_cnpj."
>          ),
>          inputSchema={
>              "type": "object",
>              "properties": {
>                  "cnae": {"type": "string", "description": "Código CNAE (parcial, busca por prefixo)"},
>                  "cidade": {"type": "string", "description": "Nome da cidade"},
>                  "estado": {"type": "string", "description": "UF (dois caracteres, ex: SP)"},
>                  "data_abertura_min": {"type": "string", "description": "Data mínima de abertura ISO 8601 (ex: 2020-01-01)"},
>                  "limit": {"type": "integer", "description": "Máximo de resultados (default 20)", "default": 20},
>              },
>              "required": [],
>          },
>      ),
>      ```
>    - Adicione ao `call_tool()` os dois branches:
>      ```python
>      elif name == "get_startup_by_cnpj":
>          from br_startup_mcp.tools.startup import get_startup_by_cnpj
>          result = get_startup_by_cnpj(
>              cnpj=arguments["cnpj"],
>              include_founders=bool(arguments.get("include_founders", True)),
>          )
>      elif name == "search_startups":
>          from br_startup_mcp.tools.startup import search_startups
>          result = search_startups(
>              cnae=arguments.get("cnae"),
>              cidade=arguments.get("cidade"),
>              estado=arguments.get("estado"),
>              data_abertura_min=arguments.get("data_abertura_min"),
>              limit=int(arguments.get("limit", 20)),
>          )
>      ```
>
> **O que NÃO fazer:**
> - Não modificar `regulatory.py` nem as tools existentes
> - Não implementar `include_rounds`, `include_bndes`, `include_cvm` (deferred)
> - Não mudar o transporte stdio do server
>
> **Validação (smoke test):**
> ```bash
> cd /Users/rmolines/git/br-startup-mcp
> python -c "
> import os; os.environ['DUCKDB_PATH'] = '/tmp/test_cnpj_d2.duckdb'
> from br_startup_mcp.tools.startup import get_startup_by_cnpj, search_startups
> result = get_startup_by_cnpj('33.000.167/0001-01')
> import json; data = json.loads(result)
> assert 'startup' in data, f'Missing startup key: {data}'
> assert 'founders' in data, f'Missing founders key: {data}'
> print('get_startup_by_cnpj OK:', data['startup']['razao_social'], '| founders:', len(data['founders']))
> # test search (cache must have been populated by above call)
> r2 = search_startups(estado='RJ', limit=5)
> d2 = json.loads(r2)
> print('search_startups OK:', len(d2), 'results')
> "
> ```
>
> **Result format:**
> ```
> ## Result
> task_id: D2
> status: success | partial | failed
> summary: <1-2 frases>
> errors: <lista ou vazio>
> validation_result: <saída do comando de validação>
> files_changed:
> - src/br_startup_mcp/tools/startup.py
> - src/br_startup_mcp/server.py
> ```

**Acceptance:** python -c "from br_startup_mcp.tools.startup import get_startup_by_cnpj; import json; d=json.loads(get_startup_by_cnpj('33.000.167/0001-01')); assert 'startup' in d and 'founders' in d" → sem exceção
**Human test:** No manual test needed — covered by automated validation

---

## Execution DAG

task: D1
title: Data client CNPJ + modelos Pydantic + cache DuckDB
depends_on:
predicate: cnpj.py busca BrasilAPI, normaliza para Startup/Founder, cacheia em DuckDB
executor: sonnet
isolation: none
batch: 1
files:
- src/br_startup_mcp/data/cnpj.py
- src/br_startup_mcp/models/entities.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.data.cnpj import fetch_cnpj_raw, normalize_startup; s = normalize_startup(fetch_cnpj_raw('33000167000101')); assert s and s.cnpj == '33000167000101'"
human_test: No manual test needed — covered by automated validation

task: D2
title: MCP tools get_startup_by_cnpj e search_startups
depends_on: D1
predicate: tools MCP expostas no server, smoke test retorna dados reais
executor: sonnet
isolation: none
batch: 2
files:
- src/br_startup_mcp/tools/startup.py
- src/br_startup_mcp/server.py
max_retries: 2
acceptance: python -c "from br_startup_mcp.tools.startup import get_startup_by_cnpj; import json; d=json.loads(get_startup_by_cnpj('33.000.167/0001-01')); assert 'startup' in d and 'founders' in d"
human_test: No manual test needed — covered by automated validation

## Infrastructure

- New secrets: none (BrasilAPI é gratuita sem auth)
- CI/CD: no changes
- New dependencies: none (httpx já no pyproject.toml)
- Setup script: none
- Data migration: none
