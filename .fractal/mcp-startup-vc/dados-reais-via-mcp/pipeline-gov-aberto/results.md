# Results: pipeline-gov-aberto
_Node: .fractal/mcp-startup-vc/dados-reais-via-mcp/pipeline-gov-aberto_
_Generated on: 2026-03-19_

---

task: D1
status: success
summary: pyproject.toml criado com dependências (mcp, httpx, duckdb, pydantic, pandas, python-dotenv). Estrutura src/br_startup_mcp/{models,data,tools}/ criada com __init__.py em cada pacote. Pacote instalado em editable mode via pip.
files_changed:
- pyproject.toml
- src/br_startup_mcp/__init__.py
- src/br_startup_mcp/__main__.py
- src/br_startup_mcp/models/__init__.py
- src/br_startup_mcp/data/__init__.py
- src/br_startup_mcp/tools/__init__.py
- data/.gitkeep
- .env.example
- .gitignore
errors:
validation_result: python -c "import br_startup_mcp; print('ok')" → ok

---

task: D2
status: success
summary: BndesOperation e CvmOffer implementados como Pydantic v2 BaseModel com todos os campos de docs/architecture.md. Helper make_id() adicionado. model_config from_attributes=True em ambos.
files_changed:
- src/br_startup_mcp/models/entities.py
errors:
validation_result: BndesOperation OK: 00.000.000/0001-00 | CvmOffer OK: ativa

---

task: D3
status: success
summary: CVM client implementado em cvm.py. Faz download do ZIP oferta_distribuicao.zip (CVM open data), extrai oferta_resolucao_160.csv (12.401 linhas), normaliza para CvmOffer, persiste em DuckDB. Validado com 12.328 registros reais carregados.
files_changed:
- src/br_startup_mcp/data/cvm.py
errors:
validation_result: Loaded 12328 CVM offers | 3 offers printed com cnpj, razao_social, status

---

task: D4
status: success
summary: BNDES client implementado em bndes.py. Usa CKAN datastore API (2.3M operações disponíveis), busca via paginação, normaliza para BndesOperation, persiste em DuckDB. Validado com 100 registros reais carregados.
files_changed:
- src/br_startup_mcp/data/bndes.py
errors:
validation_result: Loaded 100 BNDES operations | 3 operations printed com cnpj, razao_social, valor

---

task: D5
status: success
summary: MCP server implementado em server.py com stdio transport. 2 tools registradas: get_cvm_crowdfunding_offers e get_bndes_financing. Auto-sync se cache vazio. Smoke test tools/list retorna ambas as tools.
files_changed:
- src/br_startup_mcp/server.py
- src/br_startup_mcp/tools/regulatory.py
- src/br_startup_mcp/__main__.py
errors:
validation_result: Tools found: ['get_cvm_crowdfunding_offers', 'get_bndes_financing'] | D5 smoke test PASSED
