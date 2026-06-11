# Prompt — Gerar Spec (Claude.ai)

> Roda no Claude.ai. Escreve uma Spec a partir do template. Cole o bloco abaixo, preenchendo os `[campos]`. O bloco de contexto situa a Spec no conjunto de Stories do release; quando o release foi planejado no Claude Code, esse prompt já vem pré-preenchido de lá (com as Stories e seus aceites) — aqui fica o padrão canônico pra preencher à mão.

```text
Contexto — Release [release + nome] (épico: docs/epicos/<release>-<slug>.md).
[Uma linha sobre o release.] Stories (cards no board, prefixo [R?:]):
- [#NN — título. Objetivo: … Aceite: …]
- [#NN — título. Objetivo: … Aceite: …]

---

Pela lente de Tech Lead, escreva uma Spec usando o template docs/templates/spec.md para a Story: [FEATURE/STORY].
Critérios de aceite em EARS, com a tabela de exemplos. Inclua contratos, o toque no modelo de dados (o mecanismo), NFRs e o fora de escopo.
Referencie ADRs/RFCs como restrições já dadas, sem re-justificar.
NÃO inclua quebra em tasks — a Spec não tem essa seção; a decomposição é do Claude Code.
Alinhe comigo o que estiver ambíguo antes de escrever.
Enxuto: corte padding, não substância; não enumerereleases/features específicas.
```
