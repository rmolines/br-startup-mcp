# Fontes de Dados — Startups Brasileiras

> Catálogo de fontes avaliadas para o MCP br-startup-mcp.
> Última atualização: 2026-03-19

---

## Fontes Catalogadas

### 1. Receita Federal — Dados Públicos CNPJ

- **URL:** https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/ e https://www.gov.br/conecta/catalogo/apis/consulta-cnpj
- **Tipo de dado:** Cadastro completo de pessoas jurídicas: razão social, CNAE, endereço, sócios, situação cadastral, data de abertura, capital social, natureza jurídica
- **Cobertura estimada:** ~55 milhões de CNPJs ativos e inativos; toda PJ registrada no Brasil
- **Forma de acesso:** Download (arquivos ZIP mensais) + API REST gov.br (consulta pontual por CNPJ)
- **Custo:** Gratuito
- **Limitações legais/ToS:** Dados públicos por lei (Lei nº 12.527/2011 — LAI). API gov.br requer cadastro e tem limite de requisições por minuto não publicado. Uso comercial permitido com atribuição.
- **Integrabilidade:** Programática
- **Notas:** A base completa em ZIP é atualizada mensalmente (~10 GB compactados). Para consultas pontuais, a API REST é mais prática. Projetos como OpenCNPJ (opencnpj.org), Minha Receita (docs.minhareceita.org) e Base dos Dados (basedosdados.org/dataset/br-me-cnpj) oferecem wrappers já tratados. Não distingue "startup" de outras PJs — requer filtro por CNAE, porte ou data de abertura.

---

### 2. Base dos Dados — CNPJ tratado (BigQuery)

- **URL:** https://basedosdados.org/dataset/br-me-cnpj e https://basedosdados.org/dataset/e43f0d5b-43cf-4bfb-8d90-c38a4e0d7c4f
- **Tipo de dado:** Dados públicos de CNPJ da Receita Federal, já limpos, normalizados e carregados no BigQuery público. Inclui empresas, estabelecimentos, sócios, natureza jurídica, CNAE.
- **Cobertura estimada:** Base completa da Receita Federal (~55M CNPJs)
- **Forma de acesso:** API (BigQuery SQL via Python `basedosdados` ou `google-cloud-bigquery`); download via `bd.read_table()` ou `bd.read_sql()`
- **Custo:** Gratuito (primeiros 1 TB/mês de processamento BigQuery são free; exige projeto Google Cloud)
- **Limitações legais/ToS:** Mesma origem que a Receita Federal — dados públicos. A plataforma Base dos Dados pede atribuição e uso não comercial para os scripts de tratamento (MIT license nos SDKs).
- **Integrabilidade:** Programática
- **Notas:** É a forma mais prática de acessar a base CNPJ completa sem infraestrutura própria. SDK Python maduro (`pip install basedosdados`). Ideal para enriquecer dados de startups com informações societárias.

---

### 3. CVM — Portal de Dados Abertos

- **URL:** https://dados.cvm.gov.br/
- **Tipo de dado:** Dados de companhias abertas (S.A. listadas), fundos de investimento (cadastro, carteiras, informe diário), operações com valores mobiliários, demonstrações financeiras (ITR, DFP), captações de startups via CrowdFunding (instrução CVM 88)
- **Cobertura estimada:** ~700 companhias abertas; ~35.000 fundos registrados; dados desde 2000
- **Forma de acesso:** Download (CSV/ZIP atualizados diariamente) + API REST (CKAN API do portal)
- **Custo:** Gratuito
- **Limitações legais/ToS:** Dados públicos. Portal integrado ao Portal Brasileiro de Dados Abertos (dados.gov.br). Sem restrições de uso comercial.
- **Integrabilidade:** Programática
- **Notas:** Para startups especificamente, o mais relevante é o Registro de Ofertas de Crowdfunding (Resolução CVM 88/2022) — permite identificar startups que captaram via equity crowdfunding. Companhias abertas raramente são startups em estágio inicial. Dados de fundos de VC registrados na CVM são acessíveis (FIP — Fundos de Investimento em Participações).

---

### 4. BNDES — Portal de Dados Abertos

- **URL:** https://dadosabertos.bndes.gov.br/
- **Tipo de dado:** Operações de financiamento contratadas (CNPJ do cliente, valor, setor, porte, produto, data), desembolsos para MPMEs, patrocínios, indicadores financeiros
- **Cobertura estimada:** Operações desde 2002; todo cliente que recebeu financiamento BNDES
- **Forma de acesso:** Download (CSV/XLSX) + API REST (CKAN)
- **Custo:** Gratuito
- **Limitações legais/ToS:** Dados públicos (política de dados abertos do governo federal). Uso livre com atribuição.
- **Integrabilidade:** Programática
- **Notas:** Permite identificar startups que receberam financiamento BNDES (programas BNDES Fintechs, BNDES Garagem, Fundo Criatec). Cobertura limitada ao universo BNDES — não captura captações privadas ou venture capital. Dados de CNPJ permitem cruzamento com base Receita Federal.

---

### 5. ABStartups — StartupBase

- **URL:** https://startupbase.abstartups.com.br/ e https://abstartups.com.br/mapeamento/
- **Tipo de dado:** Cadastro de startups brasileiras autodeclarado: nome, setor, cidade, estágio, modelo de negócio, número de funcionários, fundadores, status. Relatório anual de mapeamento do ecossistema.
- **Cobertura estimada:** >12.800 startups mapeadas (2024); dataset anual cobre ~3.000 startups ativas com dados detalhados
- **Forma de acesso:** Consulta manual via plataforma web (filtros por estado, setor, estágio). Relatório anual em PDF. Não há API pública documentada.
- **Custo:** Gratuito (consulta web e PDF)
- **Limitações legais/ToS:** Dados autodeclarados pelas startups. Uso dos dados de pesquisa requer atribuição à ABStartups. Scraping não autorizado pelos ToS.
- **Integrabilidade:** Manual (web) / Parcialmente programática (PDF estruturado)
- **Notas:** O StartupBase é a base de referência do ecossistema brasileiro. A ausência de API pública é a principal limitação para integração programática. O mapeamento anual (PDF) pode ser parseado para extração de dados agregados. Contato com ABStartups pode viabilizar parceria para acesso estruturado.

---

### 6. Distrito — Plataforma ÍON

- **URL:** https://www.distrito.me/ e https://www.distrito.me/for-startups
- **Tipo de dado:** Inteligência de mercado sobre startups brasileiras e LATAM: perfil, investimentos, rodadas, valuations, segmentos, rankings (unicórnios, aspirantes). Base de >37.000 startups cadastradas.
- **Cobertura estimada:** >37.000 startups cadastradas (Brasil + LATAM); foco em startups de tecnologia
- **Forma de acesso:** Plataforma SaaS (ÍON) — acesso via conta. Cadastro gratuito para startups com acesso limitado. Planos corporativos pagos para acesso completo e analytics.
- **Custo:** Freemium (cadastro gratuito para startups); planos pagos para corporações (preço não publicado, negociação direta)
- **Limitações legais/ToS:** Dados proprietários. Scraping proibido. API não documentada publicamente. Relatórios públicos (ex.: lista de unicórnios) disponíveis no blog sem restrição de leitura.
- **Integrabilidade:** Manual (relatórios públicos) / Parcialmente programática (mediante contrato)
- **Notas:** É a fonte mais abrangente e curada de dados de startups brasileiras. O alto valor dos dados reflete-se no custo de acesso corporativo. Relatórios temáticos publicados no blog (unicórnios, rodadas de investimento, setores) são gratuitos e legíveis.

---

### 7. Crunchbase — API

- **URL:** https://www.crunchbase.com/ e https://data.crunchbase.com/docs
- **Tipo de dado:** Perfis de empresas globais (incluindo Brasil): fundação, fundadores, rodadas de investimento, investidores, valuations, aquisições, IPOs, categorias de negócio
- **Cobertura estimada:** >4 milhões de organizações globais; cobertura de startups brasileiras relevantes (série A em diante) é boa, mas empresas em early-stage têm cobertura irregular
- **Forma de acesso:** API REST (requer chave de API); plano Basic gratuito com acesso limitado; planos pagos para volume e endpoints avançados
- **Custo:** Freemium: Basic gratuito (limitado); Pro ~$49/mês; Business ~$199/mês; Enterprise sob consulta
- **Limitações legais/ToS:** API Terms of Use (última revisão dez/2022). Dados não podem ser revendidos. Scraping do site explicitamente proibido. Redistribuição de dados requer licença Enterprise.
- **Integrabilidade:** Programática
- **Notas:** A cobertura de startups brasileiras de alto perfil (unicórnios, scale-ups com rodadas internacionais) é excelente. Startups early-stage ou sem rodadas internacionais têm cobertura fraca. É a melhor fonte para dados de investimento estruturados. O plano Basic fornece dados de firmografia básica gratuitamente via API.

---

### 8. Observatório Sebrae Startups

- **URL:** https://observatorio.sebraestartups.com.br/
- **Tipo de dado:** Dados agregados do ecossistema brasileiro: startups mapeadas por setor, região, estágio, perfil de fundadores (gênero, formação), investimento, empregos gerados. Relatórios anuais (Sebrae Startups Report).
- **Cobertura estimada:** >18.000 startups mapeadas; dados desde 2022
- **Forma de acesso:** Dashboard web interativo + relatórios em PDF. Sem API pública documentada.
- **Custo:** Gratuito
- **Limitações legais/ToS:** Dados públicos do Sebrae. Uso com atribuição. Sem scraping autorizado.
- **Integrabilidade:** Manual (dashboard e PDF)
- **Notas:** Excelente para dados agregados e análises setoriais/regionais do ecossistema. Não oferece dados individuais de startups de forma estruturada. Complementa ABStartups com cobertura de estágios iniciais e regiões menos representadas (Norte, Nordeste).

---

### 9. Portal da Indústria / CNI — Mapeamento de Startups

- **URL:** https://www.portaldaindustria.com.br/canais/observatorio-nacional-da-industria/produtos/mapeamento-de-startups-brasileiras/
- **Tipo de dado:** Perfis de 1.413 startups industriais brasileiras: nome, setor industrial (11 setores), modelo de negócio, localização (região/estado/cidade), website, área de atuação
- **Cobertura estimada:** 1.413 startups (foco em setores industriais: Fintech, Healthtech, Edtech, Agtech, etc.)
- **Forma de acesso:** Dashboard BI interativo (browser). Metodologia parceira da israelense StartupBlink. Sem API nem download direto.
- **Custo:** Gratuito
- **Limitações legais/ToS:** Dados proprietários do Observatório Nacional da Indústria. Visualização permitida; extração estruturada não autorizada.
- **Integrabilidade:** Manual
- **Notas:** Cobertura restrita a setores industriais. Útil como benchmark e para startups B2B industrial. Base menor que ABStartups e Distrito, mas curada manualmente com qualidade alta.

---

### 10. Kaggle / Dados Públicos — Datasets de Startups BR

- **URL:** https://www.kaggle.com/datasets e https://dados.gov.br/
- **Tipo de dado:** Datasets públicos variados: alguns contêm listas de startups brasileiras exportadas de fontes como ABStartups, Crunchbase-BR ou portais governamentais. Qualidade e atualidade variam muito por dataset.
- **Cobertura estimada:** Variável; datasets existentes cobrem de centenas a alguns milhares de startups
- **Forma de acesso:** Download direto (CSV/JSON/XLSX); API Kaggle disponível via `kaggle` CLI
- **Custo:** Gratuito
- **Limitações legais/ToS:** Cada dataset tem licença própria (CC0, CC-BY, etc.). Verificar antes de usar. Kaggle API requer conta gratuita.
- **Integrabilidade:** Programática
- **Notas:** Não existe um dataset canônico e mantido de startups brasileiras no Kaggle. Os existentes são snapshots históricos de qualidade variável. Útil para prototipagem e testes, não como fonte primária de produção. O Portal Dados Abertos do governo (dados.gov.br) agrega datasets governamentais (CNPJ, CVM, BNDES) em um ponto único de descoberta.

---

### 11. LinkedIn — Dados de Empresas

- **URL:** https://www.linkedin.com/company/ e https://developer.linkedin.com/
- **Tipo de dado:** Perfis de empresas: nome, setor, tamanho, localização, descrição, fundadores, número de seguidores, vagas abertas, produtos
- **Cobertura estimada:** Praticamente todas as startups brasileiras com presença digital têm página no LinkedIn
- **Forma de acesso:** API oficial (Marketing Developer Platform) — acesso extremamente restrito (requer aprovação e casos de uso específicos). Scraping tecnicamente possível mas proibido pelos ToS.
- **Custo:** API oficial: restrita e cara (enterprise); scraping: gratuito mas viola ToS
- **Limitações legais/ToS:** ToS proíbe explicitamente scraping automatizado. A API oficial (Marketing Developer Platform) requer aprovação prévia da LinkedIn e é destinada a parceiros autorizados. Decisão judicial (hiQ vs. LinkedIn) declarou legalidade de scraping de dados públicos nos EUA, mas o risco de bloqueio e ação legal persiste.
- **Integrabilidade:** Parcialmente programática (com alto risco legal/operacional)
- **Notas:** Dados valiosos de enriquecimento (tamanho da equipe, crescimento, vagas), mas acesso confiável e legal é muito difícil sem parceria formal com LinkedIn. Não recomendado como fonte primária.

---

## Avaliação de Viabilidade

| Fonte | Integrabilidade | Motivo |
|---|---|---|
| Receita Federal CNPJ (API/Download) | Programática | API REST oficial + download mensal. Dados abertos por lei. |
| Base dos Dados CNPJ (BigQuery) | Programática | SDK Python maduro, BigQuery SQL, dados pré-tratados. |
| CVM Dados Abertos | Programática | API CKAN + download CSV. Dados abertos governamentais. |
| BNDES Dados Abertos | Programática | API CKAN + download CSV. Dados abertos governamentais. |
| Crunchbase API | Programática | API REST documentada. Plano Basic gratuito disponível. |
| Kaggle / dados.gov.br | Programática | Download direto + API Kaggle. Qualidade variável. |
| ABStartups StartupBase | Manual | Sem API pública. Consulta via web ou PDF anual. |
| Distrito ÍON | Manual / Parcialmente programática | Plataforma SaaS proprietária. API somente via contrato. |
| Observatório Sebrae Startups | Manual | Dashboard e PDF. Sem API. |
| Portal da Indústria / CNI | Manual | Dashboard BI. Sem download estruturado. |
| LinkedIn | Parcialmente programática (alto risco) | API oficial restrita; scraping viola ToS. |

**Fontes programaticamente integráveis (sem contrato/negociação):**
1. Receita Federal CNPJ
2. Base dos Dados (BigQuery)
3. CVM Dados Abertos
4. BNDES Dados Abertos
5. Crunchbase API (plano Basic)
6. Kaggle / dados.gov.br

**Fontes manuais ou que requerem negociação:**
7. ABStartups StartupBase
8. Distrito ÍON
9. Observatório Sebrae Startups
10. Portal da Indústria / CNI
11. LinkedIn (alto risco legal)

---

## Conclusão

**Veredicto: Sim, o conjunto identificado é suficiente para construir um MCP funcional e abrangente sobre startups brasileiras — com importantes ressalvas sobre o que cada fonte cobre e como combiná-las.**

### Cobertura por dimensão

O conjunto de fontes avaliadas cobre bem as principais dimensões de dados relevantes para um fundo de VC. Dados cadastrais e societários são excelentemente cobertos pela Receita Federal / CNPJ (gratuito, programático, completo) e enriquecidos pela Base dos Dados via BigQuery. Dados de investimento e rodadas são cobertos pelo Crunchbase (melhor para startups com rodadas internacionais ou série A+) e parcialmente pelo BNDES (financiamento público). Dados regulatórios e de mercado de capitais são cobertos pela CVM, incluindo o crescente mercado de equity crowdfunding. O perfil do ecossistema (setores, regiões, fundadores) é coberto pelo trio ABStartups, Sebrae Startups e Portal da Indústria.

### Lacunas identificadas

A principal lacuna é a ausência de uma fonte única, programática e atualizada de dados de startups em estágio early-stage com rodadas pré-seed e seed no Brasil. As fontes programáticas (CNPJ, CVM, BNDES, Crunchbase) capturam o extremo — empresas formalizadas ou com rodadas relevantes — mas o "meio" do ecossistema (startups em aceleradoras, rodadas informais, pre-revenue) está disperso em fontes manuais (ABStartups, Sebrae). A cobertura de startups fora do eixo São Paulo–Rio também é mais fraca nas fontes programáticas.

### Estratégia de integração recomendada

A estratégia ótima para o MCP combina camadas: (1) **Base CNPJ como âncora** — toda startup tem CNPJ, portanto usar a Receita Federal como fonte de verdade para dados cadastrais e societários; (2) **Crunchbase como camada de investimento** — enriquecer com dados de rodadas, investidores e valuations via API; (3) **CVM para dados regulatórios** — empresas abertas, FIPs com startups, e captações de crowdfunding; (4) **BNDES para financiamento público** — complementa o quadro de captações; (5) **ABStartups e Sebrae como fontes de descoberta** — ingestão periódica manual ou semi-automática dos relatórios anuais para ampliar o universo de startups. Dado o foco em uso por fundos de VC, as fontes programáticas (1–4) cobrem bem o universo de interesse (startups com tração e captações formais).

### Consideração final

O MCP será tão abrangente quanto a combinação dessas fontes permitir — e essa combinação é viável com esforço de engenharia moderado. As fontes governamentais (CNPJ, CVM, BNDES) são gratuitas e programáticas. O Crunchbase adiciona a camada de mercado privado com custo acessível. O gap real não é de fontes, mas de fragmentação: não existe no Brasil uma fonte única equivalente ao Crunchbase com cobertura nacional completa e API pública gratuita. O MCP precisará ser uma camada de integração que une essas fontes — o que é exatamente o valor que pode agregar para fundos de VC.
