# Handover

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
