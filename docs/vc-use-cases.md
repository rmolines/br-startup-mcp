# VC Use Cases — MCP br-startup-mcp

> Mapeamento de workflows típicos de fundos de VC com dados de startups brasileiras,
> e derivação da superfície de tools e resources do MCP.
> Baseado nas fontes catalogadas em `docs/data-sources.md`.
> Última atualização: 2026-03-19

---

## Workflows Mapeados

### 1. Deal Sourcing

**Descrição:** Processo de descoberta proativa de startups candidatas a investimento. O analista busca empresas que se encaixam na tese do fundo antes de qualquer contato — identificando pelo setor, localização, estágio, data de fundação e sinais de tração.

**Perguntas típicas de analistas:**
1. Quais startups de healthtech foram fundadas nos últimos 3 anos em São Paulo e estão no estágio seed?
2. Existem startups de agtech no Nordeste que ainda não receberam rodadas institucionais?
3. Quais empresas de CNAE 6201 (desenvolvimento de software) têm capital social acima de R$ 500 mil e foram abertas em 2022-2024?
4. Quais startups brasileiras de fintech levantaram rodada seed entre USD 500k e USD 2M no último ano?
5. Há startups de edtech com mais de 10 sócios e sede fora do eixo SP-RJ?

**Dados necessários:**
- CNPJ, razão social, data de abertura, capital social, natureza jurídica
- CNAE (setor/subsetor), porte da empresa
- Localização (cidade, estado)
- Sócios (nomes, participações)
- Rodadas de investimento (valor, data, investidores)
- Estágio declarado (pre-seed, seed, série A...)

**Fontes que cobrem:**
- Receita Federal CNPJ / Base dos Dados (BigQuery): dados cadastrais, societários, CNAE, localização, data de abertura
- Crunchbase API: rodadas de investimento, valuations, investidores, categorias de negócio
- BNDES Dados Abertos: financiamento público recebido (sinal de tração/validação)

**Tools MCP propostas:**
- `search_startups_by_sector`
- `search_startups_by_location`
- `get_startup_by_cnpj`
- `list_recent_rounds`

---

### 2. Screening

**Descrição:** Triagem inicial de um conjunto de startups para avaliar fit com a tese do fundo. O analista cruza dados estruturados para reduzir uma lista longa de candidatos a um shortlist qualificado para análise aprofundada.

**Perguntas típicas de analistas:**
1. Quais das 40 startups da nossa lista têm mais de 5 funcionários e operam em B2B SaaS?
2. Esta startup tem sócios com histórico em outras empresas de tecnologia?
3. Qual o capital social declarado e a natureza jurídica — é uma startup ou uma MEI/ME?
4. A startup recebeu algum financiamento público (BNDES, FINEP) nos últimos 2 anos?
5. Há outras rodadas de investimento registradas no Crunchbase para esta empresa?

**Dados necessários:**
- Dados cadastrais completos (via CNPJ)
- Quadro societário (fundadores, participações)
- Histórico de financiamentos (rodadas VC + público)
- Modelo de negócio (B2B, B2C, marketplace)
- Número de funcionários (proxy: porte declarado na Receita)
- Setor/CNAE principal e secundário

**Fontes que cobrem:**
- Receita Federal CNPJ / Base dos Dados (BigQuery): dados cadastrais, sócios, porte
- Crunchbase API: rodadas, modelo de negócio, categorias
- BNDES Dados Abertos: financiamentos públicos recebidos

**Tools MCP propostas:**
- `get_startup_by_cnpj`
- `get_founders_by_cnpj`
- `get_funding_history`
- `compare_startups`

---

### 3. Due Diligence

**Descrição:** Investigação aprofundada de uma startup específica antes da emissão do term sheet. O analista quer validar a situação legal/regulatória da empresa, estrutura societária completa, histórico financeiro público, e benchmarks do setor.

**Perguntas típicas de analistas:**
1. A empresa está com situação cadastral ativa na Receita Federal? Há alguma irregularidade?
2. Quem são os sócios com mais de 5% de participação e desde quando?
3. A empresa ou seus sócios têm outras empresas abertas? Quais?
4. A startup captou via equity crowdfunding (CVM 88) — quais foram os termos e o histórico de captações?
5. Há financiamentos BNDES ou operações de crédito público registradas?

**Dados necessários:**
- Situação cadastral na Receita (ativa, inapta, baixada)
- Quadro societário detalhado com histórico de alterações
- CNPJ de outras empresas dos fundadores
- Captações via CVM 88 (equity crowdfunding)
- Histórico de financiamentos BNDES
- Rodadas de investimento no Crunchbase (para cross-check)

**Fontes que cobrem:**
- Receita Federal CNPJ / Base dos Dados (BigQuery): situação cadastral, sócios, histórico de alterações
- CVM Dados Abertos: captações de equity crowdfunding (Resolução CVM 88/2022), fundos FIP
- BNDES Dados Abertos: operações de financiamento
- Crunchbase API: rodadas, investidores anteriores

**Tools MCP propostas:**
- `get_startup_by_cnpj`
- `get_founders_by_cnpj`
- `get_cvm_crowdfunding_offers`
- `get_bndes_financing`
- `get_funding_history`

---

### 4. Portfolio Monitoring

**Descrição:** Acompanhamento contínuo das empresas do portfólio após o investimento. O gestor monitora sinais de saúde operacional, alterações societárias, novas captações, e benchmarks do setor para identificar startups que precisam de suporte ou estão prontas para follow-on.

**Perguntas típicas de analistas:**
1. Alguma empresa do portfólio alterou seu quadro societário nos últimos 30 dias?
2. Houve novas rodadas de investimento anunciadas no Crunchbase para empresas do nosso portfólio?
3. Alguma empresa do portfólio recebeu novo financiamento BNDES recentemente?
4. A situação cadastral de todas as empresas do portfólio está ativa?
5. Como estão os múltiplos do setor de healthtech este trimestre — o portfólio está bem posicionado?

**Dados necessários:**
- Situação cadastral atualizada de todas as empresas do portfólio
- Alterações no quadro societário (detecção de mudanças)
- Novas rodadas de investimento (follow-on, bridge rounds)
- Novos financiamentos públicos
- Benchmarks setoriais (valuations médios por estágio/setor)

**Fontes que cobrem:**
- Receita Federal CNPJ / Base dos Dados (BigQuery): situação cadastral, alterações societárias
- Crunchbase API: novas rodadas anunciadas, co-investidores
- BNDES Dados Abertos: novos financiamentos públicos
- CVM Dados Abertos: captações de crowdfunding

**Tools MCP propostas:**
- `get_startup_by_cnpj`
- `monitor_portfolio_changes`
- `list_recent_rounds`
- `get_funding_history`

---

### 5. Market Mapping

**Descrição:** Mapeamento do landscape competitivo de um segmento de mercado específico. O analista quer entender quantas empresas operam num nicho, quem são os players, qual o estágio de maturidade do mercado, e onde estão as oportunidades não capturadas.

**Perguntas típicas de analistas:**
1. Quantas startups de logtech existem no Brasil? Onde estão concentradas?
2. Quais são os maiores rounds de investimento no setor de proptech nos últimos 2 anos?
3. Há concentração de startups de agtech em determinados estados ou biomas?
4. Quais fundos de VC investiram mais em cleantech no Brasil (via registros CVM/FIP)?
5. Qual o volume total de captações via equity crowdfunding no setor de energias renováveis?

**Dados necessários:**
- Lista de empresas por CNAE (setor/subsetor)
- Localização geográfica (cidade, estado, região)
- Distribuição por estágio (seed, série A, etc.)
- Histórico de rodadas por setor
- Fundos FIP registrados na CVM com foco setorial
- Captações de crowdfunding por setor

**Fontes que cobrem:**
- Receita Federal CNPJ / Base dos Dados (BigQuery): universo de empresas por CNAE e localização
- Crunchbase API: rodadas por setor, valuations, mapa de investidores
- CVM Dados Abertos: fundos FIP (fundos VC registrados), captações crowdfunding por setor
- BNDES Dados Abertos: financiamentos por setor

**Tools MCP propostas:**
- `search_startups_by_sector`
- `search_startups_by_location`
- `map_sector_rounds`
- `list_cvm_fip_funds`
- `get_cvm_crowdfunding_offers`

---

### 6. Comparable Analysis (Comp Analysis)

**Descrição:** Análise de comparáveis para estimar valuation de uma startup candidata a investimento. O analista busca empresas de perfil similar (setor, estágio, modelo de negócio) com rodadas recentes para estabelecer múltiplos de referência.

**Perguntas típicas de analistas:**
1. Quais startups de SaaS B2B no Brasil levantaram série A no último ano e a que valuation?
2. Qual o ticket médio de rodadas seed em healthtech no Brasil em 2024?
3. Quais foram os maiores exits (aquisições/IPOs) de startups brasileiras de fintech?
4. Como o valuation desta startup se compara com peers internacionais de perfil similar no Crunchbase?
5. Qual é o múltiplo mediano de receita para investimentos em edtech série A no Brasil?

**Dados necessários:**
- Rodadas de investimento por setor/estágio (valor, data, investidores)
- Valuations declarados (pre/post-money)
- Dados de aquisição e IPO
- Múltiplos implícitos por setor/estágio
- Dados de empresas abertas (S.A.) para benchmarks de mercado público

**Fontes que cobrem:**
- Crunchbase API: rodadas, valuations, aquisições, IPOs — principal fonte para comp analysis
- CVM Dados Abertos: demonstrações financeiras de companhias abertas (benchmarks de mercado público)
- BNDES Dados Abertos: volume de financiamento por setor (proxy de atividade)

**Tools MCP propostas:**
- `compare_startups`
- `map_sector_rounds`
- `list_recent_rounds`
- `get_funding_history`

---

## Proposta de Tools MCP

### `get_startup_by_cnpj`

**Descrição:** Retorna o perfil completo de uma startup a partir do CNPJ, cruzando dados da Receita Federal com Crunchbase e registros governamentais.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpj` | `str` | Sim | CNPJ da empresa (com ou sem formatação) |
| `include_founders` | `bool` | Não | Incluir quadro societário completo (default: True) |
| `include_rounds` | `bool` | Não | Incluir histórico de rodadas do Crunchbase (default: True) |
| `include_bndes` | `bool` | Não | Incluir financiamentos BNDES (default: False) |

**Resposta esperada:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `cnpj` | `str` | CNPJ formatado |
| `razao_social` | `str` | Razão social da empresa |
| `nome_fantasia` | `str` | Nome fantasia (se disponível) |
| `situacao_cadastral` | `str` | Ativa, Inapta, Baixada, Suspensa |
| `data_abertura` | `date` | Data de abertura na Receita Federal |
| `capital_social` | `float` | Capital social declarado em BRL |
| `cnae_principal` | `str` | Código e descrição do CNAE principal |
| `cnae_secundarios` | `list[str]` | CNAEs secundários |
| `endereco` | `dict` | Logradouro, cidade, estado, CEP |
| `porte` | `str` | MEI, ME, EPP, Médio, Grande |
| `socios` | `list[dict]` | Nome, CPF/CNPJ, qualificação, participação % |
| `rounds` | `list[dict]` | Rodadas do Crunchbase (opcional) |
| `bndes_financiamentos` | `list[dict]` | Financiamentos BNDES (opcional) |

**Fonte de dados principal:** Receita Federal CNPJ / Base dos Dados (BigQuery); enriquecimento: Crunchbase API, BNDES

---

### `search_startups_by_sector`

**Descrição:** Busca startups por setor (CNAE ou categoria Crunchbase), com filtros de localização, estágio e data de fundação.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `sector` | `str` | Sim | CNAE (ex: "6201") ou categoria (ex: "fintech", "healthtech") |
| `city` | `str` | Não | Cidade de operação |
| `state` | `str` | Não | Estado (UF, ex: "SP", "RJ") |
| `stage` | `str` | Não | Estágio: "pre-seed", "seed", "series-a", "series-b", "growth" |
| `founded_after` | `str` | Não | Data mínima de fundação (ISO 8601, ex: "2020-01-01") |
| `founded_before` | `str` | Não | Data máxima de fundação (ISO 8601) |
| `min_capital` | `float` | Não | Capital social mínimo em BRL |
| `limit` | `int` | Não | Máximo de resultados (default: 20, max: 100) |

**Resposta esperada:** Lista de objetos com `cnpj`, `razao_social`, `cnae`, `cidade`, `estado`, `data_abertura`, `capital_social`, `stage` (se disponível).

**Fonte de dados principal:** Base dos Dados (BigQuery) para CNAE/cadastro; Crunchbase API para estágio/categoria.

---

### `search_startups_by_location`

**Descrição:** Busca startups por localização geográfica, com filtros opcionais de setor e estágio.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `city` | `str` | Não | Cidade (ex: "Florianópolis") |
| `state` | `str` | Não | Estado UF (ex: "SC") |
| `region` | `str` | Não | Região: "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul" |
| `sector` | `str` | Não | Setor/CNAE para filtrar |
| `stage` | `str` | Não | Estágio de investimento |
| `limit` | `int` | Não | Máximo de resultados (default: 20) |

**Resposta esperada:** Lista de startups com localização, setor, data de abertura e dados cadastrais básicos.

**Fonte de dados principal:** Base dos Dados (BigQuery) — CNPJ com geolocalização.

---

### `get_founders_by_cnpj`

**Descrição:** Retorna o quadro societário detalhado de uma empresa e verifica se os sócios têm outras empresas ativas.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpj` | `str` | Sim | CNPJ da empresa |
| `include_other_companies` | `bool` | Não | Buscar outras empresas dos sócios (default: False) |

**Resposta esperada:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `cnpj` | `str` | CNPJ consultado |
| `socios` | `list[dict]` | Nome, CPF/CNPJ, qualificação, participação %, data de entrada |
| `outras_empresas` | `dict` | Por sócio: lista de CNPJs de outras empresas (opcional) |

**Fonte de dados principal:** Receita Federal CNPJ / Base dos Dados (BigQuery).

---

### `get_funding_history`

**Descrição:** Retorna o histórico completo de captações de uma startup: rodadas de VC (Crunchbase), financiamentos públicos (BNDES) e captações reguladas (CVM 88).

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpj` | `str` | Não | CNPJ da empresa (para cruzar com BNDES/CVM) |
| `crunchbase_id` | `str` | Não | Identificador Crunchbase (para startups sem CNPJ no CB) |
| `company_name` | `str` | Não | Nome da empresa (fallback de busca) |

**Resposta esperada:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `rounds` | `list[dict]` | Rodadas VC: tipo, valor USD, data, investidores, lead |
| `bndes_ops` | `list[dict]` | Operações BNDES: produto, valor BRL, data, setor |
| `cvm_offers` | `list[dict]` | Captações CVM 88: valor alvo, captado, data, status |
| `total_raised_usd` | `float` | Total captado em USD (estimativa) |

**Fonte de dados principal:** Crunchbase API (rounds), BNDES Dados Abertos, CVM Dados Abertos.

---

### `list_recent_rounds`

**Descrição:** Lista rodadas de investimento recentes no Brasil, com filtros por setor, estágio e período.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `sector` | `str` | Não | Setor/categoria para filtrar |
| `stage` | `str` | Não | Estágio: "seed", "series-a", "series-b", etc. |
| `after_date` | `str` | Não | Data mínima da rodada (ISO 8601) |
| `before_date` | `str` | Não | Data máxima da rodada |
| `min_amount_usd` | `float` | Não | Valor mínimo da rodada em USD |
| `limit` | `int` | Não | Máximo de resultados (default: 20) |

**Resposta esperada:** Lista de rodadas com `company_name`, `cnpj` (se disponível), `round_type`, `amount_usd`, `date`, `investors`, `lead_investor`.

**Fonte de dados principal:** Crunchbase API.

---

### `map_sector_rounds`

**Descrição:** Retorna estatísticas agregadas de rodadas de investimento por setor: contagem, valor médio, mediana, distribuição por estágio.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `sector` | `str` | Sim | Setor/categoria |
| `year` | `int` | Não | Ano de referência (default: ano atual - 1) |
| `country` | `str` | Não | País (default: "Brazil") |

**Resposta esperada:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `sector` | `str` | Setor consultado |
| `total_rounds` | `int` | Total de rodadas no período |
| `total_amount_usd` | `float` | Volume total em USD |
| `avg_round_size_usd` | `float` | Tamanho médio de rodada |
| `median_round_size_usd` | `float` | Mediana do tamanho de rodada |
| `by_stage` | `dict` | Breakdown por estágio: seed, series-a, etc. |

**Fonte de dados principal:** Crunchbase API.

---

### `compare_startups`

**Descrição:** Compara um conjunto de startups em dimensões-chave: tamanho, rodadas, valuation, fundadores, crescimento.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpjs` | `list[str]` | Não | Lista de CNPJs para comparar |
| `crunchbase_ids` | `list[str]` | Não | IDs Crunchbase para comparar |
| `dimensions` | `list[str]` | Não | Dimensões: "funding", "founders", "size", "sector" (default: todas) |

**Resposta esperada:** Tabela comparativa com os campos solicitados, uma linha por empresa.

**Fonte de dados principal:** Receita Federal CNPJ, Crunchbase API.

---

### `get_cvm_crowdfunding_offers`

**Descrição:** Retorna captações registradas na CVM via Resolução 88/2022 (equity crowdfunding), com filtros por empresa e status.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpj` | `str` | Não | CNPJ da empresa emissora |
| `sector` | `str` | Não | Setor para filtrar |
| `status` | `str` | Não | "ativa", "encerrada", "cancelada" |
| `after_date` | `str` | Não | Data mínima de registro (ISO 8601) |
| `limit` | `int` | Não | Máximo de resultados (default: 20) |

**Resposta esperada:** Lista de ofertas com `cnpj_emissora`, `razao_social`, `valor_alvo`, `valor_captado`, `data_registro`, `data_encerramento`, `status`, `plataforma`.

**Fonte de dados principal:** CVM Dados Abertos (Resolução CVM 88/2022).

---

### `list_cvm_fip_funds`

**Descrição:** Lista fundos FIP (Fundos de Investimento em Participações) registrados na CVM — proxy de fundos de VC/PE no Brasil.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `focus_sector` | `str` | Não | Setor de foco do fundo (quando disponível) |
| `min_patrimonio` | `float` | Não | Patrimônio líquido mínimo em BRL |
| `status` | `str` | Não | "ativo", "liquidado" (default: "ativo") |
| `limit` | `int` | Não | Máximo de resultados (default: 20) |

**Resposta esperada:** Lista de fundos com `cnpj_fundo`, `nome`, `administrador`, `gestor`, `patrimonio_liquido`, `data_constituicao`, `status`.

**Fonte de dados principal:** CVM Dados Abertos.

---

### `get_bndes_financing`

**Descrição:** Retorna operações de financiamento do BNDES para uma empresa específica ou para um setor.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpj` | `str` | Não | CNPJ do cliente BNDES |
| `sector` | `str` | Não | Setor BNDES para filtrar |
| `product` | `str` | Não | Produto BNDES (ex: "BNDES Fintechs", "Fundo Criatec") |
| `after_date` | `str` | Não | Data mínima da operação |
| `limit` | `int` | Não | Máximo de resultados (default: 20) |

**Resposta esperada:** Lista de operações com `cnpj_cliente`, `razao_social`, `produto_bndes`, `valor_brl`, `data_contratacao`, `setor`, `porte`.

**Fonte de dados principal:** BNDES Dados Abertos.

---

### `monitor_portfolio_changes`

**Descrição:** Verifica alterações recentes em um conjunto de empresas do portfólio: mudanças no quadro societário, situação cadastral, novas rodadas anunciadas.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cnpjs` | `list[str]` | Sim | Lista de CNPJs do portfólio |
| `since_date` | `str` | Não | Data de corte para detectar mudanças (default: 30 dias atrás) |
| `check_types` | `list[str]` | Não | Tipos a checar: "socios", "situacao", "rounds", "bndes" (default: todos) |

**Resposta esperada:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `changes` | `list[dict]` | Por empresa: tipo de mudança, data, detalhes |
| `alerts` | `list[str]` | Alertas críticos (ex: situação mudou para "Inapta") |
| `checked_at` | `datetime` | Timestamp da verificação |

**Fonte de dados principal:** Receita Federal CNPJ (situação/sócios), Crunchbase API (rounds).

---

### `search_investors_by_portfolio`

**Descrição:** Identifica fundos de VC e investidores que investiram em startups de um setor específico no Brasil, para mapeamento de co-investidores e sindicação.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `sector` | `str` | Sim | Setor/categoria de interesse |
| `stage` | `str` | Não | Estágio das investidas |
| `country` | `str` | Não | País das investidas (default: "Brazil") |
| `limit` | `int` | Não | Máximo de investidores retornados (default: 20) |

**Resposta esperada:** Lista de investidores com `name`, `type` (VC, CVC, angel, etc.), `portfolio_count_sector`, `recent_investments`, `location`.

**Fonte de dados principal:** Crunchbase API; complemento: CVM (fundos FIP).

---

## Proposta de Resources MCP

Resources são dados estáticos ou semi-estáticos expostos pelo MCP como contexto de referência, sem parâmetros dinâmicos complexos. Adequados para dados que mudam raramente (mensal ou anualmente).

### Resource 1: Lista de CNAEs Relevantes para Startups

**URI:** `startup-mcp://reference/cnaes-startups`
**Descrição:** Lista curada dos CNAEs mais frequentes em startups tecnológicas brasileiras, com descrição, setor de mercado associado (fintech, healthtech, etc.) e exemplos de empresas.
**Fonte:** Receita Federal (CNAE oficial) + curadoria manual baseada em ABStartups/Sebrae
**Frequência de atualização sugerida:** Anual (CNAE muda raramente)
**Formato:** JSON com campos: `codigo`, `descricao`, `categoria_startup`, `exemplos`

---

### Resource 2: Fundos FIP Ativos na CVM

**URI:** `startup-mcp://reference/fundos-fip-ativos`
**Descrição:** Lista de Fundos de Investimento em Participações (FIPs) registrados e ativos na CVM — proxy do ecossistema de VC/PE brasileiro. Inclui nome, gestor, administrador, patrimônio líquido e data de constituição.
**Fonte:** CVM Dados Abertos (atualizado diariamente)
**Frequência de atualização sugerida:** Mensal
**Formato:** JSON com campos: `cnpj_fundo`, `nome`, `gestor`, `administrador`, `patrimonio_liquido_brl`, `data_constituicao`

---

### Resource 3: Mapa de Ecossistemas Regionais

**URI:** `startup-mcp://reference/ecossistemas-regionais`
**Descrição:** Mapa das principais cidades e regiões com ecossistemas de startups ativos no Brasil, com quantidade estimada de startups, principais setores e hubs de inovação conhecidos.
**Fonte:** Curadoria baseada em ABStartups Mapeamento Anual + Sebrae Startups Report
**Frequência de atualização sugerida:** Anual
**Formato:** JSON com campos: `cidade`, `estado`, `regiao`, `startups_estimadas`, `setores_principais`, `hubs`

---

### Resource 4: Tabela de Estágios de Investimento

**URI:** `startup-mcp://reference/estagios-investimento`
**Descrição:** Referência dos estágios de investimento em startups usados no mercado brasileiro e internacional, com faixas típicas de valuation e ticket, e correspondência com nomenclaturas do Crunchbase.
**Fonte:** Curadoria de mercado (Crunchbase nomenclatura + adaptação ao mercado BR)
**Frequência de atualização sugerida:** Anual
**Formato:** JSON com campos: `estagio`, `nome_br`, `nome_crunchbase`, `ticket_tipico_usd_range`, `valuation_tipico_usd_range`, `descricao`

---

### Resource 5: Calendário de Captações CVM 88 Ativas

**URI:** `startup-mcp://reference/cvm88-ativas`
**Descrição:** Snapshot das ofertas de equity crowdfunding ativas no momento, conforme Resolução CVM 88/2022. Dado semi-estático atualizado diariamente.
**Fonte:** CVM Dados Abertos
**Frequência de atualização sugerida:** Diária
**Formato:** JSON com campos: `cnpj_emissora`, `nome_empresa`, `plataforma`, `valor_alvo_brl`, `valor_captado_brl`, `data_encerramento`, `setor`
