---
name: abrir-pr
description: Analyzes pending changes, creates the branch with the right convention (docs/… exempt from issue ref, or feat//fix/… referencing the subtask), commits with one-line Conventional Commits, pushes, and opens a PR to main with a short description. Use when the user says things like "analise os ajustes e abra o PR", "abra o PR", "commita e abre o PR", "open the PR".
---

# Abrir PR — rotina padrão deste projeto

Leva as alterações locais até um PR na `main`. As **regras** vivem em `docs/process/estrategia-branch-pr.md` (fonte da verdade); esta skill é só a execução. Siga na ordem; pare e pergunte apenas quando algo for genuinamente ambíguo.

## 1. Entender o contexto

- Rode `git status`, `git diff` e `git diff --staged` pra ver tudo que mudou.
- Classifique a natureza das mudanças:
  - **Só docs/processo** (toca apenas `docs/`, `.claude/`, README, prompts) → branch `docs/<slug>`, **isenta** de referenciar issue.
  - **Código** (toca `api/` ou `web/`) → branch `feat/<slug>` ou `fix/<slug>`; o commit/PR **referencia a subtask** com `Closes #NNN`. Se não souber qual issue, pergunte.
- **Nunca** misture prosa (docs) e código de feature no mesmo PR — se as mudanças pendentes forem das duas naturezas, separe em dois PRs.

## 2. Conferir a branch

- Se estou na `main`: crio a branch nova a partir dela.
- Se já estou numa branch de trabalho: confirmo com o usuário antes de seguir (não crio branch sobre branch por engano).

## 3. Criar a branch

Nome em inglês, kebab-case, prefixo conforme a natureza do passo 1 (ex.: `docs/pr-handoff-prompt`, `feat/transaction-create`).

## 4. Commitar

- **Conventional Commits** em inglês, **uma linha só** — sem corpo com bullets (`docs:`, `feat:`, `fix:`, `chore:`, `test:`, `refactor:`…).
- Em branch de código, inclua `Closes #NNN`.
- Se há código, rode os testes antes (CLAUDE.md).
- Trailer `Co-Authored-By` conforme o padrão da sessão.

## 5. Push

`git push -u origin <branch>`.

## 6. Abrir o PR

- `gh pr create --base main`, com título em Conventional Commits e **descrição curta** em inglês (o quê + porquê em 2–4 linhas, mais o footer do padrão da sessão).
- **Nunca** crie issues nem itens no board ao abrir o PR — o board é gerido pelo usuário.

## Regras que não mudam

- Só commito/faço push/abro PR porque esta skill foi invocada (é o pedido explícito).
- O **squash merge** pra `main` é a forma de entrar — mas o merge em si é decisão do usuário, não desta skill.
