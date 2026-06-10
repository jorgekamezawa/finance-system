# Prompt — Planejar release (Claude Code)

> Roda no Claude Code. Lê o épico + decisões, propõe as Stories, espera sua aprovação e então cria as cascas no board. Cole o bloco abaixo, trocando `<release>` (ex.: `r0`).

```text
Aja como PM + Tech Lead do projeto Sistema de Finanças. Regras e processo em @CLAUDE.md e @docs/process/processo-desenvolvimento-sdd.md.
Leia o épico docs/epicos/<release>-<slug>.md e os ADRs/RFCs relacionados em @docs/adr/ e @docs/rfc/.
Proponha a quebra do release em Stories (fatias verticais de valor, INVEST), cada uma com objetivo + critério de aceite. Back e front são subtasks sob uma Story, não Stories separadas.
NÃO crie nada ainda — me apresente a lista e espere minha aprovação explícita.
Depois que eu aprovar: crie as cascas de Story no board (GitHub Projects, via gh CLI), em Backlog, com o prefixo numérico que liga ao épico. Pra criar as Stories (comandos gh, labels, assignee), siga @docs/process/operar-board.md. Não escreva Specs — elas vêm uma por vez, depois.
```
