# Handover

## pipeline-crunchbase — 2026-03-19

**What was done:** O MCP server agora integra a API Crunchbase Basic (free tier) para dados de rodadas de investimento, valuations e investidores de startups brasileiras. Dois novos tools MCP expostos: `list_recent_rounds` (rodadas recentes via Crunchbase) e `get_investor_portfolio` (portfólio de um fundo pelo nome no cache). Tool `enrich_startup_with_crunchbase` associa dados Crunchbase a uma Startup existente pelo slug. `get_startup_by_cnpj` enriquecido com parâmetro `include_rounds`. Toda a integração degrada graciosamente quando `CRUNCHBASE_API_KEY` não está configurada — retorna JSON com mensagem clara, sem lançar exceção.

**Key decisions:**
- Crunchbase Basic free tier: endpoints `/v4/searches/organizations`, `/v4/searches/funding_rounds`, `/v4/entities/organizations/{permalink}` com auth via `?user_key=`. Sem endpoints pagos.
- Retry + backoff: 429 → sleep 60s, outros erros HTTP → backoff exponencial (1s, 2s, 4s), max 3 retries.
- `list_recent_rounds` usa `fetch_funding_rounds()` (não `fetch_organizations_brazil()`) — rodadas globais, não apenas brasileiras. Filtro por Brasil seria via `funded_organization_location` mas não implementado (aceitável para free tier).
- Matching CNPJ↔Crunchbase UUID é manual via `enrich_startup_with_crunchbase(cnpj, crunchbase_slug)` — sem matching automático (out of scope).
- `investors` no modelo `Round` armazenado como JSON string no DuckDB (coluna VARCHAR) para compatibilidade com schema simples.
- Módulo `_check_api_key()` lê env var em runtime (não em import time) para suporte a testes que mudam `os.environ`.

**Pitfalls discovered:**
- Crunchbase retorna campos monetários como dicts `{"value": 5000000, "currency": "USD", "value_usd": 5000000}` — não floats diretos. Usar `_parse_usd()` que extrai `value_usd` ou `value`.
- Crunchbase datas retornam como dicts `{"value": "2023-01-15", "precision": "day"}` — usar `_parse_date()` que extrai `value`.
- `fetch_organizations_brazil()` não é chamada por nenhum tool (tools de rounds usam `fetch_funding_rounds()`). Está disponível para uso futuro.
- DuckDB `NamedTemporaryFile` cria arquivo vazio — DuckDB rejeita arquivo pré-existente com 0 bytes como "not a valid DuckDB database file". Em testes, criar path em `tempfile.mkdtemp()` sem criar o arquivo antes.

**Next steps:**
- Quando `CRUNCHBASE_API_KEY` for obtida, testar `list_recent_rounds` com dados reais e verificar normalização dos campos
- Popular cache de rounds para investors brasileiros relevantes (Kaszek, Monashees, Softbank, Canary)
- Considerar adicionar filtro de país em `list_recent_rounds` via `funded_organization_location`
- Cache TTL para rounds (dados mudam frequentemente)

**Key files changed:**
- `src/br_startup_mcp/data/crunchbase.py` — Crunchbase API client + normalize + DuckDB cache (novo)
- `src/br_startup_mcp/models/entities.py` — Round, Investor models + Startup enrichment fields
- `src/br_startup_mcp/data/cnpj.py` — startups table extended with Crunchbase columns
- `src/br_startup_mcp/tools/crunchbase.py` — list_recent_rounds, get_investor_portfolio (novo)
- `src/br_startup_mcp/tools/startup.py` — enrich_startup_with_crunchbase, include_rounds param
- `src/br_startup_mcp/server.py` — 3 novos tools registrados (total: 7)

---

## pipeline-gov-aberto — 2026-03-19

**What was done:** Pipeline de ingestão de dados governamentais funcionando end-to-end. O agente agora consegue buscar dados reais da CVM e do BNDES, normalizar para modelos Pydantic, cachear em DuckDB local, e servir via MCP server com stdio transport. Dois tools MCP expostos: `get_cvm_crowdfunding_offers` e `get_bndes_financing`.

**Key decisions:**
- CVM: usou `oferta_distribuicao.zip` (Resolution 160, 12K registros de ofertas públicas gerais) porque o dataset de equity crowdfunding CVM 88 não existe como entidade separada no portal dados.cvm.gov.br. Impacto: os dados CVM não são filtrados por tipo startup/crowdfunding.
- BNDES: usou CKAN datastore API (resource `612faa0b`) com 2.3M registros disponíveis. CNPJs das operações indiretas automáticas estão mascarados (`**.*16.560/0001-**`) — busca por CNPJ de startup não funciona neste dataset.
- Todos os prints/logs vão para `sys.stderr` — o MCP usa `sys.stdout` para o protocolo jsonrpc, qualquer print em stdout corrompe o protocolo.
- Auto-sync no primeiro call de tool quando cache está vazio — pode parecer travado (~5MB download CVM).

**Pitfalls discovered:**
- `server.list_tools()` no MCP SDK retorna o decorator, não uma coroutine — não é possível fazer `asyncio.run(server.list_tools())`. Testar via subprocess com initialize+tools/list.
- DuckDB: `duckdb.connect(db_path, read_only=True)` falha se o arquivo não existe ainda — usar try/except para detectar e disparar sync.

**Next steps:**
- Próximo nó: implementar tool `get_startup_by_cnpj` integrando Receita Federal
- Considerar buscar dataset CVM 88 em fontes alternativas (CVM website direto vs. dados abertos)
- Adicionar configuração de cache TTL para revalidação automática

**Key files changed:**
- `pyproject.toml` — dependências
- `src/br_startup_mcp/models/entities.py` — BndesOperation, CvmOffer
- `src/br_startup_mcp/data/cvm.py` — CVM client
- `src/br_startup_mcp/data/bndes.py` — BNDES client
- `src/br_startup_mcp/server.py` — MCP server
- `src/br_startup_mcp/tools/regulatory.py` — tool implementations

---

## pipeline-cnpj-receita — PR #4 — 2026-03-19

**What was done:**
Implementado o pipeline CNPJ da Receita Federal como fonte âncora do MCP. O MCP server agora consegue buscar dados cadastrais e societários de qualquer empresa brasileira via CNPJ, usando BrasilAPI como proxy gratuito e sem auth da Receita Federal. Modelos Pydantic `Startup` e `Founder` implementados conforme `architecture.md`, com cache DuckDB.

**Key decisions:**
- BrasilAPI escolhida como estratégia de acesso (proxy da Receita Federal, gratuito, sem auth)
- Cache-first: get_startup_by_cnpj tenta DuckDB primeiro, só chama BrasilAPI em cache miss
- `participacao_pct` sempre None — BrasilAPI não retorna percentual de participação societária
- `search_startups` é cache-only (sem busca em batch pela Receita) — popular via calls a get_startup_by_cnpj
- `_STARTUP_COLS` extraído como constante de módulo para evitar duplicação

**Pitfalls discovered:**
- BrasilAPI retorna `cnae_fiscal` como int (ex: `6201500`), não string. Zero-pad para 7 dígitos com `f"{int(cnae):07d}"`.
- `cnaes_secundarios` na BrasilAPI é lista de dicts `{"codigo": int, "descricao": str}` — extrair só `codigo`.
- DuckDB `read_only=True` lança exceção se o arquivo não existe ainda (mesmo comportamento de bndes/cvm) — tratar com try/except.

**Next steps:**
- Próximo nó: integração Crunchbase (enriquecimento de Startup com rodadas, categorias, website)
- Considerar popular cache de `search_startups` com batch de CNPJs de interesse (ex: lista de startups por CNAE)
- Cache TTL para revalidação de dados da Receita (dados mudam com pouca frequência)

**Key files changed:**
- `src/br_startup_mcp/data/cnpj.py` — BrasilAPI client + DuckDB cache
- `src/br_startup_mcp/models/entities.py` — Startup, Founder models
- `src/br_startup_mcp/tools/startup.py` — MCP tools
- `src/br_startup_mcp/server.py` — tool registration
