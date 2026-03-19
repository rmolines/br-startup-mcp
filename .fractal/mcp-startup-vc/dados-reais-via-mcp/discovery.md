---
response: new_child
confidence: high
reasoning: "Receita Federal/CNPJ é a âncora do data model — toda startup tem CNPJ. Base qualitativamente diferente: ~10 GB em múltiplos ZIPs, tabelas relacionais (empresas, estabelecimentos, sócios). O agente precisa decidir estratégia de acesso (bulk download vs API gov.br vs BigQuery) e implementar. Se falhar, o MCP perde a âncora central."
child_predicate: "O agente não consegue integrar a base CNPJ da Receita Federal como fonte âncora — escolher estratégia de acesso e implementar pipeline para dados cadastrais/societários"
child_type: risk
prd_seed:
leaf_type:
verification:
---
