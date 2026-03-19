# Learnings

## pipeline-gov-aberto — 2026-03-19

**CVM dados abertos não tem dataset específico de CVM 88 / equity crowdfunding**
O portal dados.cvm.gov.br tem `crowdfunding-cad` que só contém cadastro de plataformas (não ofertas). As ofertas estão em `oferta-distrib` que cobre todas as ofertas públicas (Resolution 160), não apenas crowdfunding. Para filtrar startups/crowdfunding CVM 88 seria necessário filtrar por campos específicos após o download.

**BNDES CNPJs mascarados em operações indiretas automáticas**
O dataset de operações indiretas automáticas (resource `612faa0b`, o mais completo com 2.3M registros) mascara os CNPJs dos clientes finais (`**.*16.560/0001-**`). Para busca por CNPJ de startup seria necessário usar o dataset de operações não automáticas (`6f56b78c`) que pode ter CNPJs completos.

**MCP server.list_tools() é um decorator, não uma coroutine**
No SDK MCP Python, `@server.list_tools()` registra um handler — `server.list_tools` por si só é o decorator. Para testar se os tools estão registrados, usar subprocess com mensagens jsonrpc (initialize + tools/list), não `asyncio.run(server.list_tools())`.

**stdout vs stderr no MCP server**
O MCP protocol usa stdio — `sys.stdout` é o canal de comunicação jsonrpc. Qualquer print em stdout corrompe o protocolo. Todo logging deve ir para `sys.stderr`.

## pipeline-cnpj-receita — 2026-03-19

**BrasilAPI retorna cnae_fiscal como int, não string**
O campo `cnae_fiscal` da BrasilAPI é um inteiro (ex: `6201500`), não uma string. Para criar um identificador padronizado de 7 dígitos (ex: `"0620150"`), usar `f"{int(cnae):07d}"`. Idem para `cnaes_secundarios[i]["codigo"]`.

**cnaes_secundarios na BrasilAPI é lista de dicts, não lista de strings**
Cada item de `cnaes_secundarios` é um dict com campos `codigo` (int) e `descricao` (str). Para normalizar para `list[str]`, extrair apenas `item["codigo"]` e zero-paddar.

**BrasilAPI não retorna percentual de participação societária**
O endpoint `/api/cnpj/v1/{cnpj}` retorna o quadro societário (campo `qsa`) sem percentual de participação. O campo `participacao_pct` do modelo `Founder` ficará sempre `None` até que outra fonte forneça este dado.

**search_startups retorna vazio sem seed explícito de CNPJs**
`query_startups` consulta apenas o cache DuckDB local. Para que `search_startups` retorne resultados, é necessário popular o cache chamando `get_startup_by_cnpj` com CNPJs específicos antes. Não há mecanismo de busca em batch pela Receita Federal sem BigQuery ou download bulk.
