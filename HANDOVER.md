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
