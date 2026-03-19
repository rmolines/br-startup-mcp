# Arquitetura do MCP — br-startup-mcp

> Especificação técnica do MCP server para dados de startups brasileiras para uso por fundos de VC.
> Derivada dos workflows mapeados em `docs/vc-use-cases.md` e das fontes catalogadas em `docs/data-sources.md`.
> Última atualização: 2026-03-19

---

## Data Model Unificado

O data model unifica dados heterogêneos de fontes governamentais e de mercado em entidades coerentes. A âncora é o CNPJ — toda empresa brasileira tem um, o que permite cruzamento entre fontes.

### Entidade: Startup

Representa uma empresa do ecossistema de startups, com dados primários da Receita Federal enriquecidos por Crunchbase e outras fontes.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `cnpj` | `str` | Receita Federal | Sim |
| `razao_social` | `str` | Receita Federal | Sim |
| `nome_fantasia` | `str` | Receita Federal | Não |
| `situacao_cadastral` | `str` | Receita Federal | Sim |
| `data_abertura` | `date` | Receita Federal | Sim |
| `capital_social_brl` | `float` | Receita Federal | Sim |
| `cnae_principal` | `str` | Receita Federal | Sim |
| `cnaes_secundarios` | `list[str]` | Receita Federal | Não |
| `natureza_juridica` | `str` | Receita Federal | Sim |
| `porte` | `str` | Receita Federal | Sim |
| `endereco_logradouro` | `str` | Receita Federal | Não |
| `cidade` | `str` | Receita Federal | Sim |
| `estado` | `str` | Receita Federal | Sim |
| `cep` | `str` | Receita Federal | Não |
| `crunchbase_uuid` | `str` | Crunchbase API | Não |
| `crunchbase_slug` | `str` | Crunchbase API | Não |
| `categorias` | `list[str]` | Crunchbase API | Não |
| `descricao` | `str` | Crunchbase API | Não |
| `website` | `str` | Crunchbase API | Não |
| `total_funding_usd` | `float` | Crunchbase API | Não |
| `last_funding_type` | `str` | Crunchbase API | Não |
| `last_funding_date` | `date` | Crunchbase API | Não |
| `employee_count` | `str` | Crunchbase API | Não |
| `updated_at` | `datetime` | Sistema | Sim |

**Relações:**
- `Startup 1—N Founder` (via quadro societário)
- `Startup 1—N Round` (rodadas de investimento)
- `Startup 1—N BndesOperation` (financiamentos BNDES)
- `Startup 1—N CvmOffer` (captações CVM 88)

---

### Entidade: Founder

Representa um sócio/fundador de uma startup. Derivado do quadro societário da Receita Federal.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `id` | `str` | Sistema (gerado) | Sim |
| `cnpj_empresa` | `str` | Receita Federal | Sim |
| `nome` | `str` | Receita Federal | Sim |
| `cpf_cnpj` | `str` | Receita Federal | Não |
| `qualificacao` | `str` | Receita Federal | Sim |
| `participacao_pct` | `float` | Receita Federal | Não |
| `data_entrada` | `date` | Receita Federal | Não |
| `outras_empresas_cnpjs` | `list[str]` | Receita Federal | Não |

**Relações:**
- `Founder N—1 Startup`

---

### Entidade: Round

Representa uma rodada de investimento em uma startup. Fonte primária: Crunchbase.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `id` | `str` | Crunchbase API | Sim |
| `cnpj_empresa` | `str` | Cruzamento CNPJ | Não |
| `crunchbase_org_uuid` | `str` | Crunchbase API | Sim |
| `company_name` | `str` | Crunchbase API | Sim |
| `round_type` | `str` | Crunchbase API | Sim |
| `announced_date` | `date` | Crunchbase API | Não |
| `amount_usd` | `float` | Crunchbase API | Não |
| `pre_money_valuation_usd` | `float` | Crunchbase API | Não |
| `post_money_valuation_usd` | `float` | Crunchbase API | Não |
| `lead_investor_name` | `str` | Crunchbase API | Não |
| `investors` | `list[str]` | Crunchbase API | Não |
| `is_equity` | `bool` | Crunchbase API | Não |

**Relações:**
- `Round N—1 Startup`
- `Round N—N Investor`

---

### Entidade: Investor

Representa um fundo de VC, investidor anjo, CVC ou aceleradora que participou de rodadas.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `id` | `str` | Crunchbase API | Sim |
| `crunchbase_uuid` | `str` | Crunchbase API | Sim |
| `name` | `str` | Crunchbase API | Sim |
| `type` | `str` | Crunchbase API | Sim |
| `country` | `str` | Crunchbase API | Não |
| `city` | `str` | Crunchbase API | Não |
| `cnpj_fundo` | `str` | CVM Dados Abertos | Não |
| `cvm_patrimonio_brl` | `float` | CVM Dados Abertos | Não |
| `cvm_administrador` | `str` | CVM Dados Abertos | Não |
| `website` | `str` | Crunchbase API | Não |
| `description` | `str` | Crunchbase API | Não |

**Relações:**
- `Investor N—N Round`

---

### Entidade: Fund (FIP/CVM)

Representa fundos FIP (Fundos de Investimento em Participações) registrados na CVM — proxy regulatório de fundos de VC/PE brasileiros.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `cnpj_fundo` | `str` | CVM Dados Abertos | Sim |
| `nome` | `str` | CVM Dados Abertos | Sim |
| `tipo` | `str` | CVM Dados Abertos | Sim |
| `administrador` | `str` | CVM Dados Abertos | Sim |
| `gestor` | `str` | CVM Dados Abertos | Não |
| `patrimonio_liquido_brl` | `float` | CVM Dados Abertos | Não |
| `data_constituicao` | `date` | CVM Dados Abertos | Não |
| `data_encerramento` | `date` | CVM Dados Abertos | Não |
| `situacao` | `str` | CVM Dados Abertos | Sim |
| `crunchbase_uuid` | `str` | Crunchbase API | Não |

**Relações:**
- `Fund 1—N CvmPortfolioItem` (participações em empresas, quando disponível)

---

### Entidade: BndesOperation

Representa uma operação de financiamento contratada com o BNDES.

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `id` | `str` | Sistema | Sim |
| `cnpj_cliente` | `str` | BNDES Dados Abertos | Sim |
| `razao_social` | `str` | BNDES Dados Abertos | Sim |
| `produto_bndes` | `str` | BNDES Dados Abertos | Sim |
| `valor_brl` | `float` | BNDES Dados Abertos | Sim |
| `data_contratacao` | `date` | BNDES Dados Abertos | Sim |
| `setor_bndes` | `str` | BNDES Dados Abertos | Não |
| `porte` | `str` | BNDES Dados Abertos | Não |
| `municipio` | `str` | BNDES Dados Abertos | Não |
| `uf` | `str` | BNDES Dados Abertos | Não |

**Relações:**
- `BndesOperation N—1 Startup` (via CNPJ)

---

### Entidade: CvmOffer

Representa uma oferta de captação via equity crowdfunding (Resolução CVM 88/2022).

| Campo | Tipo | Fonte | Obrigatório |
|-------|------|-------|-------------|
| `id` | `str` | Sistema | Sim |
| `cnpj_emissora` | `str` | CVM Dados Abertos | Sim |
| `razao_social` | `str` | CVM Dados Abertos | Sim |
| `plataforma` | `str` | CVM Dados Abertos | Sim |
| `valor_alvo_brl` | `float` | CVM Dados Abertos | Sim |
| `valor_captado_brl` | `float` | CVM Dados Abertos | Não |
| `data_registro` | `date` | CVM Dados Abertos | Sim |
| `data_encerramento` | `date` | CVM Dados Abertos | Não |
| `status` | `str` | CVM Dados Abertos | Sim |
| `tipo_valor_mobiliario` | `str` | CVM Dados Abertos | Não |

**Relações:**
- `CvmOffer N—1 Startup` (via CNPJ)

---

### Diagrama de Relações

```
Startup ──── 1:N ──── Founder
  │
  ├── 1:N ──── Round ──── N:N ──── Investor
  │                                    │
  │                              (cruzamento)
  │                                    │
  ├── 1:N ──── BndesOperation        Fund (FIP/CVM)
  │
  └── 1:N ──── CvmOffer
```

---

## Tools — Assinaturas Completas

As tools listadas em `docs/vc-use-cases.md` são aqui formalizadas com input/output schemas completos e mapeamento para o data model.

---

### `get_startup_by_cnpj`

**Descrição:** Retorna o perfil completo de uma startup via CNPJ, cruzando dados cadastrais da Receita Federal com enriquecimento de Crunchbase, BNDES e CVM.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpj` | `str` | Sim | CNPJ da empresa | `"11.222.333/0001-44"` |
| `include_founders` | `bool` | Não | Incluir quadro societário (default: `true`) | `true` |
| `include_rounds` | `bool` | Não | Incluir rodadas Crunchbase (default: `true`) | `true` |
| `include_bndes` | `bool` | Não | Incluir operações BNDES (default: `false`) | `false` |
| `include_cvm` | `bool` | Não | Incluir captações CVM 88 (default: `false`) | `false` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `startup` | `Startup` | Objeto Startup completo |
| `founders` | `list[Founder]` | Quadro societário (se solicitado) |
| `rounds` | `list[Round]` | Histórico de rodadas (se solicitado) |
| `bndes_ops` | `list[BndesOperation]` | Financiamentos BNDES (se solicitado) |
| `cvm_offers` | `list[CvmOffer]` | Captações CVM 88 (se solicitado) |

**Entidades acessadas:** `Startup`, `Founder`, `Round`, `BndesOperation`, `CvmOffer`
**Fonte primária:** Receita Federal CNPJ / Base dos Dados (BigQuery)

---

### `search_startups_by_sector`

**Descrição:** Busca startups por setor (CNAE ou categoria Crunchbase), com filtros de localização, estágio e período de fundação.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `sector` | `str` | Sim | CNAE (ex: `"6201"`) ou categoria (ex: `"fintech"`) | `"healthtech"` |
| `city` | `str` | Não | Cidade de operação | `"São Paulo"` |
| `state` | `str` | Não | UF (dois caracteres) | `"SP"` |
| `stage` | `str` | Não | Estágio: `pre-seed`, `seed`, `series-a`, `series-b`, `growth` | `"seed"` |
| `founded_after` | `str` | Não | Data mínima de fundação (ISO 8601) | `"2020-01-01"` |
| `founded_before` | `str` | Não | Data máxima de fundação | `"2023-12-31"` |
| `min_capital_brl` | `float` | Não | Capital social mínimo em BRL | `500000.0` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`, max: `100`) | `20` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `results` | `list[Startup]` | Lista de startups (campos básicos) |
| `total_found` | `int` | Total encontrado (pode ser > limit) |
| `query_params` | `dict` | Parâmetros aplicados |

**Entidades acessadas:** `Startup`
**Fonte primária:** Base dos Dados (BigQuery) para CNAE/cadastro; Crunchbase API para estágio/categoria

---

### `search_startups_by_location`

**Descrição:** Busca startups por localização geográfica com filtros opcionais de setor e estágio.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `city` | `str` | Não | Cidade | `"Florianópolis"` |
| `state` | `str` | Não | UF | `"SC"` |
| `region` | `str` | Não | Região: `Norte`, `Nordeste`, `Centro-Oeste`, `Sudeste`, `Sul` | `"Sul"` |
| `sector` | `str` | Não | Setor/CNAE para filtrar | `"agtech"` |
| `stage` | `str` | Não | Estágio de investimento | `"seed"` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`) | `20` |

**Output schema:** Lista de `Startup` com `cnpj`, `razao_social`, `cidade`, `estado`, `cnae_principal`, `data_abertura`, `capital_social_brl`.

**Entidades acessadas:** `Startup`
**Fonte primária:** Base dos Dados (BigQuery)

---

### `get_founders_by_cnpj`

**Descrição:** Retorna o quadro societário completo de uma empresa, com opção de buscar outras empresas dos sócios.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpj` | `str` | Sim | CNPJ da empresa | `"11.222.333/0001-44"` |
| `include_other_companies` | `bool` | Não | Buscar outras empresas dos sócios (default: `false`) | `false` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `cnpj` | `str` | CNPJ consultado |
| `founders` | `list[Founder]` | Quadro societário completo |
| `other_companies` | `dict[str, list[str]]` | Por sócio (CPF/nome): lista de CNPJs de outras empresas (se solicitado) |

**Entidades acessadas:** `Founder`, `Startup`
**Fonte primária:** Receita Federal CNPJ / Base dos Dados (BigQuery)

---

### `get_funding_history`

**Descrição:** Retorna histórico completo de captações de uma startup: rodadas VC, financiamentos BNDES e ofertas CVM 88.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpj` | `str` | Não | CNPJ para cruzar com BNDES/CVM | `"11.222.333/0001-44"` |
| `crunchbase_id` | `str` | Não | UUID ou slug Crunchbase | `"nubank"` |
| `company_name` | `str` | Não | Nome da empresa (fallback de busca) | `"Nubank"` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `rounds` | `list[Round]` | Rodadas de VC do Crunchbase |
| `bndes_ops` | `list[BndesOperation]` | Financiamentos BNDES |
| `cvm_offers` | `list[CvmOffer]` | Captações CVM 88 |
| `total_raised_usd` | `float` | Estimativa total captado em USD |
| `total_raised_brl` | `float` | Estimativa total captado em BRL |

**Entidades acessadas:** `Round`, `BndesOperation`, `CvmOffer`
**Fonte primária:** Crunchbase API, BNDES Dados Abertos, CVM Dados Abertos

---

### `list_recent_rounds`

**Descrição:** Lista rodadas de investimento recentes no Brasil, com filtros por setor, estágio e período.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `sector` | `str` | Não | Setor/categoria | `"fintech"` |
| `stage` | `str` | Não | Tipo de rodada | `"series-a"` |
| `after_date` | `str` | Não | Data mínima (ISO 8601) | `"2024-01-01"` |
| `before_date` | `str` | Não | Data máxima | `"2024-12-31"` |
| `min_amount_usd` | `float` | Não | Valor mínimo USD | `1000000.0` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`) | `20` |

**Output schema:** Lista de `Round` com `company_name`, `cnpj` (se disponível), `round_type`, `amount_usd`, `announced_date`, `lead_investor_name`, `investors`.

**Entidades acessadas:** `Round`
**Fonte primária:** Crunchbase API

---

### `map_sector_rounds`

**Descrição:** Estatísticas agregadas de rodadas de investimento por setor no Brasil.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `sector` | `str` | Sim | Setor/categoria | `"proptech"` |
| `year` | `int` | Não | Ano de referência (default: ano atual - 1) | `2024` |
| `country` | `str` | Não | País (default: `"Brazil"`) | `"Brazil"` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `sector` | `str` | Setor consultado |
| `year` | `int` | Ano de referência |
| `total_rounds` | `int` | Total de rodadas |
| `total_amount_usd` | `float` | Volume total USD |
| `avg_round_size_usd` | `float` | Tamanho médio |
| `median_round_size_usd` | `float` | Mediana |
| `by_stage` | `dict[str, dict]` | Por estágio: `{count, total_usd, avg_usd}` |
| `top_investors` | `list[str]` | Investidores mais ativos no setor |

**Entidades acessadas:** `Round`, `Investor`
**Fonte primária:** Crunchbase API

---

### `compare_startups`

**Descrição:** Compara múltiplas startups em dimensões-chave: financiamento, fundadores, tamanho, setor.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpjs` | `list[str]` | Não | Lista de CNPJs | `["11.222.333/0001-44"]` |
| `crunchbase_ids` | `list[str]` | Não | IDs Crunchbase | `["nubank", "ifood"]` |
| `dimensions` | `list[str]` | Não | Dimensões: `funding`, `founders`, `size`, `sector` (default: todas) | `["funding", "size"]` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `companies` | `list[dict]` | Um dict por empresa com os campos das dimensões solicitadas |
| `summary` | `dict` | Estatísticas comparativas (líder por dimensão, etc.) |

**Entidades acessadas:** `Startup`, `Founder`, `Round`
**Fonte primária:** Receita Federal CNPJ, Crunchbase API

---

### `get_cvm_crowdfunding_offers`

**Descrição:** Retorna captações registradas na CVM via Resolução 88/2022 (equity crowdfunding).

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpj` | `str` | Não | CNPJ da empresa emissora | `"11.222.333/0001-44"` |
| `sector` | `str` | Não | Setor para filtrar | `"energia"` |
| `status` | `str` | Não | `ativa`, `encerrada`, `cancelada` | `"ativa"` |
| `after_date` | `str` | Não | Data mínima de registro | `"2023-01-01"` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`) | `20` |

**Output schema:** Lista de `CvmOffer` com todos os campos da entidade.

**Entidades acessadas:** `CvmOffer`
**Fonte primária:** CVM Dados Abertos

---

### `list_cvm_fip_funds`

**Descrição:** Lista fundos FIP (proxy de VC/PE) registrados na CVM.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `focus_sector` | `str` | Não | Setor de foco (quando disponível) | `"tecnologia"` |
| `min_patrimonio_brl` | `float` | Não | Patrimônio mínimo em BRL | `10000000.0` |
| `status` | `str` | Não | `ativo`, `liquidado` (default: `ativo`) | `"ativo"` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`) | `20` |

**Output schema:** Lista de `Fund` com todos os campos da entidade.

**Entidades acessadas:** `Fund`
**Fonte primária:** CVM Dados Abertos

---

### `get_bndes_financing`

**Descrição:** Retorna operações de financiamento do BNDES para uma empresa ou setor.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpj` | `str` | Não | CNPJ do cliente BNDES | `"11.222.333/0001-44"` |
| `sector` | `str` | Não | Setor BNDES | `"software"` |
| `product` | `str` | Não | Produto BNDES | `"BNDES Fintechs"` |
| `after_date` | `str` | Não | Data mínima da operação | `"2022-01-01"` |
| `limit` | `int` | Não | Máximo de resultados (default: `20`) | `20` |

**Output schema:** Lista de `BndesOperation` com todos os campos da entidade.

**Entidades acessadas:** `BndesOperation`
**Fonte primária:** BNDES Dados Abertos

---

### `monitor_portfolio_changes`

**Descrição:** Verifica alterações recentes em empresas do portfólio: mudanças societárias, situação cadastral, novas rodadas.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cnpjs` | `list[str]` | Sim | CNPJs das empresas do portfólio | `["11.222.333/0001-44"]` |
| `since_date` | `str` | Não | Data de corte (default: 30 dias atrás) | `"2026-02-01"` |
| `check_types` | `list[str]` | Não | Tipos: `socios`, `situacao`, `rounds`, `bndes` (default: todos) | `["socios", "rounds"]` |

**Output schema:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `changes` | `list[dict]` | Por empresa: `{cnpj, type, description, detected_at}` |
| `alerts` | `list[str]` | Alertas críticos (ex: situação mudou para "Inapta") |
| `no_changes` | `list[str]` | CNPJs sem mudanças detectadas |
| `checked_at` | `datetime` | Timestamp da verificação |

**Entidades acessadas:** `Startup`, `Founder`, `Round`
**Fonte primária:** Receita Federal CNPJ, Crunchbase API

---

### `search_investors_by_portfolio`

**Descrição:** Identifica fundos e investidores que investiram em startups de um setor no Brasil.

**Input schema:**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `sector` | `str` | Sim | Setor/categoria | `"cleantech"` |
| `stage` | `str` | Não | Estágio das investidas | `"series-a"` |
| `country` | `str` | Não | País (default: `"Brazil"`) | `"Brazil"` |
| `limit` | `int` | Não | Máximo de investidores (default: `20`) | `20` |

**Output schema:** Lista de `Investor` com `name`, `type`, `portfolio_count_in_sector`, `recent_investments` (últimas 3), `country`, `city`.

**Entidades acessadas:** `Investor`, `Round`
**Fonte primária:** Crunchbase API; complemento: CVM (fundos FIP via `Fund`)

---

## Diagrama de Integração

O fluxo completo vai de Fonte de Dados → Camada de Ingestão → Entidade do Data Model → Tool MCP → Agente VC.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      FONTES DE DADOS                                │
│                                                                     │
│  Receita Federal CNPJ          CVM Dados Abertos                   │
│  Base dos Dados (BigQuery)     BNDES Dados Abertos                  │
│  Crunchbase API (Basic)                                             │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  CAMADA DE INGESTÃO                                 │
│                                                                     │
│  BigQuery SQL (basedosdados SDK)   → CNPJ bulk / consultas SQL      │
│  API REST gov.br                   → consulta pontual por CNPJ      │
│  Crunchbase REST API               → rodadas, investidores          │
│  CVM CKAN API / CSV download       → FIPs, crowdfunding             │
│  BNDES CKAN API / CSV download     → operações de financiamento     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   DATA MODEL UNIFICADO                              │
│                                                                     │
│  Startup ←──── Founder                                             │
│    │                                                                │
│    ├── Round ←──── Investor                                        │
│    │                   │                                            │
│    │               Fund (FIP/CVM)                                  │
│    │                                                                │
│    ├── BndesOperation                                               │
│    └── CvmOffer                                                     │
└─────────────────────┬───────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     TOOLS MCP                                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Mapeamento detalhado Fonte → Entidade → Tool:**

```
Receita Federal CNPJ / Base dos Dados (BigQuery)
  └─ ingestão: BigQuery SQL (bd.read_sql) / API REST pontual
    └─ entidade: Startup (campos cadastrais, CNAE, endereço, porte)
      ├─ tool: get_startup_by_cnpj
      ├─ tool: search_startups_by_sector
      ├─ tool: search_startups_by_location
      ├─ tool: compare_startups
      └─ tool: monitor_portfolio_changes
    └─ entidade: Founder (quadro societário)
      ├─ tool: get_founders_by_cnpj
      ├─ tool: get_startup_by_cnpj (include_founders=true)
      └─ tool: compare_startups

Crunchbase API (Basic REST)
  └─ ingestão: REST API /entities/organizations, /funding_rounds
    └─ entidade: Startup (enriquecimento: categorias, descricao, website, total_funding)
      ├─ tool: get_startup_by_cnpj (include_rounds=true)
      ├─ tool: search_startups_by_sector (filtro por stage/categoria)
      └─ tool: compare_startups
    └─ entidade: Round
      ├─ tool: list_recent_rounds
      ├─ tool: get_funding_history
      ├─ tool: map_sector_rounds
      └─ tool: monitor_portfolio_changes
    └─ entidade: Investor
      ├─ tool: search_investors_by_portfolio
      └─ tool: map_sector_rounds (top_investors)

CVM Dados Abertos
  └─ ingestão: CKAN API / CSV download diário
    └─ entidade: Fund (FIP registrados)
      ├─ tool: list_cvm_fip_funds
      └─ tool: search_investors_by_portfolio (complemento)
    └─ entidade: CvmOffer (captações CVM 88)
      ├─ tool: get_cvm_crowdfunding_offers
      └─ tool: get_funding_history

BNDES Dados Abertos
  └─ ingestão: CKAN API / CSV/XLSX download
    └─ entidade: BndesOperation
      ├─ tool: get_bndes_financing
      ├─ tool: get_funding_history
      └─ tool: get_startup_by_cnpj (include_bndes=true)
```

---

## Stack Tecnológico Recomendado

### Runtime e Linguagem

**Python 3.11+** — recomendado como linguagem principal pelos seguintes motivos:

1. **BigQuery / Base dos Dados:** SDK Python nativo (`basedosdados`, `google-cloud-bigquery`) é o caminho oficial e mais documentado para acessar os dados CNPJ tratados. Não há SDK equivalente maduro em TypeScript/Node para BigQuery em contexto data engineering.
2. **Ecossistema de dados:** pandas, httpx, pydantic — todas as bibliotecas de processamento de dados têm ecossistemas mais ricos em Python.
3. **MCP SDK Python:** O SDK oficial MCP para Python (`mcp` package) é estável e mantido pela Anthropic.

### MCP SDK

**`mcp` (Python SDK oficial da Anthropic)**
- Instalação: `pip install mcp`
- Pattern: async server com `@server.tool()` decorators
- Suporte a tools e resources out-of-the-box

### Clientes por Fonte de Dados

| Fonte | Biblioteca | Instalação | Notas |
|-------|-----------|------------|-------|
| Receita Federal CNPJ (API pontual) | `httpx` (async) | `pip install httpx` | Endpoint: `https://www.gov.br/conecta/catalogo/apis/consulta-cnpj` |
| Base dos Dados / BigQuery | `basedosdados` + `google-cloud-bigquery` | `pip install basedosdados google-cloud-bigquery` | Requer projeto Google Cloud + credenciais |
| CVM Dados Abertos | `httpx` + `pandas` | `pip install httpx pandas` | CSV download ou CKAN API |
| BNDES Dados Abertos | `httpx` + `pandas` | (mesmas acima) | CKAN API + CSV/XLSX |
| Crunchbase API | `httpx` (async) | (mesma acima) | REST API, autenticação por header `X-cb-user-key` |

### Cache / Storage Local

**DuckDB** — recomendado como camada de cache e storage local:

- **Justificativa:** Ideal para queries analíticas em arquivos CSV/Parquet (padrão de saída das fontes governamentais). Sem servidor necessário (embedded). Suporte nativo a Parquet e CSV. Queries SQL completo. Performance excelente para os volumes esperados (~10-100 MB de dados filtrados).
- **Instalação:** `pip install duckdb`
- **Uso:** Cache dos CSVs da CVM/BNDES em tabelas DuckDB locais, atualizadas periodicamente. Evita re-download a cada consulta.
- **Alternativa:** SQLite (mais simples, sem suporte analítico avançado) — aceitável se o servidor for stateless.

**Redis** — não recomendado para este caso: adiciona complexidade operacional desnecessária para um servidor MCP que opera principalmente em modo request-response.

### Configuração e Variáveis de Ambiente

```
# Crunchbase
CRUNCHBASE_API_KEY=<chave do plano Basic>

# Google Cloud / Base dos Dados
GOOGLE_CLOUD_PROJECT=<projeto GCP>
GOOGLE_APPLICATION_CREDENTIALS=<path para service account JSON>

# Receita Federal API gov.br (se necessário)
RECEITA_FEDERAL_API_KEY=<chave da API gov.br>

# Cache local
DUCKDB_PATH=./data/cache.duckdb

# Limites de taxa
CRUNCHBASE_RATE_LIMIT_RPM=200  # requisições por minuto (Basic tier)
```

### Dependências Python (pyproject.toml / requirements)

```
# Core
mcp>=1.0.0
httpx>=0.27.0
pydantic>=2.0.0

# Dados
basedosdados>=2.0.0
google-cloud-bigquery>=3.0.0
pandas>=2.0.0
duckdb>=0.10.0

# Utils
python-dotenv>=1.0.0
```

### Estrutura de Diretórios Sugerida

```
br-startup-mcp/
├── src/
│   ├── server.py              # MCP server entry point
│   ├── tools/
│   │   ├── startup.py         # get_startup_by_cnpj, search_startups_*
│   │   ├── funding.py         # get_funding_history, list_recent_rounds
│   │   ├── portfolio.py       # monitor_portfolio_changes
│   │   ├── market.py          # map_sector_rounds, search_investors_*
│   │   └── regulatory.py      # get_cvm_*, list_cvm_fip_funds, get_bndes_*
│   ├── resources/
│   │   └── references.py      # MCP resources estáticos/semi-estáticos
│   ├── data/
│   │   ├── cnpj.py            # cliente Receita Federal / BigQuery
│   │   ├── crunchbase.py      # cliente Crunchbase API
│   │   ├── cvm.py             # cliente CVM Dados Abertos
│   │   └── bndes.py           # cliente BNDES Dados Abertos
│   └── models/
│       └── entities.py        # Pydantic models: Startup, Founder, Round, etc.
├── data/
│   └── cache.duckdb           # cache local (gitignored)
├── docs/
│   ├── data-sources.md
│   ├── vc-use-cases.md
│   └── architecture.md        # este arquivo
├── pyproject.toml
└── .env.example
```
