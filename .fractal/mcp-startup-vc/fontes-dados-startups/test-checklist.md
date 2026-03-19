# Test Checklist
_Node: .fractal/mcp-startup-vc/fontes-dados-startups_
_Generated: 2026-03-19_

## How to use
1. Run each test below
2. Mark [x] for pass, [ ] for fail
3. Add notes for any failures
4. Run /fractal:review when done

---

## T1 — Verificar catálogo de fontes de dados

title: Verificar catálogo de fontes de dados
validates: Identificar e catalogar fontes de dados acessíveis e suficientemente abrangentes sobre startups brasileiras para alimentar o MCP
from: D1
steps:
1. Abra o arquivo docs/data-sources.md na raiz do repositório
2. Verifique que existem pelo menos 8 fontes listadas com cabeçalhos ### numerados
3. Leia a seção "## Avaliação de Viabilidade" e confirme que há uma tabela distinguindo fontes programáticas de manuais
4. Leia a seção "## Conclusão" e verifique se contém um veredicto explícito ("Sim" ou "Não") com justificativa escrita de pelo menos um parágrafo
5. Confirme que o veredicto inclui recomendação sobre quais fontes priorizar para integração
expected: O arquivo existe com ≥8 fontes catalogadas, seções de viabilidade e conclusão presentes, e a conclusão tem um veredicto claro e fundamentado sobre a suficiência das fontes para um MCP abrangente
result: [x]
notes: Auto-validated by delivery — 15 fontes catalogadas (>= 8), 2 seções obrigatórias presentes, conclusão com veredicto "Sim" e justificativa detalhada em 4 parágrafos
