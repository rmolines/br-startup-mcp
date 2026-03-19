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
