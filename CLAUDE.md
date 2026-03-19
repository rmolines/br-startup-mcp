# br-startup-mcp

MCP server de dados de startups para fundos de VC.

## Fractal tree

This repo uses a fractal predicate tree in `.fractal/` for project management.
Run `bash scripts/fractal-tree.sh` to see current state.
For project context, read `conclusion.md` files from satisfied nodes.
See `references/context-protocol.md` in the fractal plugin for the full navigation protocol.

## Pitfalls

**MCP stdio e stdout:** O MCP protocol usa stdio — `sys.stdout` é canal jsonrpc. Todo logging deve usar `sys.stderr` ou corrompe o protocolo.

**DuckDB read_only abre apenas se arquivo existe:** `duckdb.connect(path, read_only=True)` lança exceção se o arquivo não existe. Use try/except para detectar cache vazio e disparar sync.

**MCP server.list_tools() é decorator:** No SDK Python, `server.list_tools()` registra um handler. Para testar tools, usar subprocess com jsonrpc (initialize + tools/list), não asyncio direto.

**CVM dados abertos:** Não há dataset específico de CVM 88 / equity crowdfunding no portal dados.cvm.gov.br. O disponível é `oferta-distrib` (Resolution 160, todos os tipos de ofertas públicas).

**BNDES CNPJs mascarados:** Operações indiretas automáticas (dataset maior, 2.3M registros) têm CNPJs mascarados. Para busca por CNPJ completo, usar dataset de operações não automáticas.
