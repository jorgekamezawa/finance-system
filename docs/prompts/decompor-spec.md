# Prompt — Decompor Spec (Claude Code)

> Roda no Claude Code. Lê a Spec, propõe a descrição da Story + as subtasks, espera aprovação e então cria no board. Cole o bloco abaixo, trocando `<spec>` e o ID da Story.

```text
Aja como Tech Lead do projeto Sistema de Finanças. Regras em @CLAUDE.md, @docs/process/processo-desenvolvimento-sdd.md e @docs/process/estrategia-branch-pr.md.
Leia a Spec @docs/specs/<spec>.md e a Story [ID/link] no board.
Proponha: (1) a descrição/resumo da Story, com link pra Spec; (2) a quebra em subtasks (sub-issues), normalmente separando back e front, cada uma com objetivo + critério.
NÃO crie nem altere nada ainda — me mostre a proposta e espere minha aprovação.
Depois que eu aprovar: ajuste a descrição da Story e crie as subtasks no board (via gh CLI), cada uma com responsável (assignee). Não comece a implementar.
```
