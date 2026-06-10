# Guia do fluxo — comece por aqui

> O mapa operacional do projeto: em cada fase, o que fazer, qual prompt usar, onde ele roda, o que gera e onde salvar. **Não duplica conteúdo** — sequencia e aponta pros prompts (`docs/prompts/`), templates (`docs/templates/`) e docs de processo. Pro "porquê/o quê" do processo, ver `docs/process/processo-desenvolvimento-sdd.md`; pra decidir qual artefato criar, `docs/process/quando-usar-cada-documento.md`.

## Regras de ouro

- **Um passo por vez, sob sua aprovação.** Nada de gerar em lote.
- **Autoria roda no Claude.ai** (carrega persona + Knowledge): Épico, RFC, ADR, Spec.
- **Ação roda no Claude Code** (com `@paths` e portão de aprovação): planejar release, decompor Spec, implementar, verificar.
- **Não force documento onde não há decisão:** muitas Specs, alguns ADRs, poucas RFCs.

## Pré-requisito de ambiente (uma vez — já feito)

GitHub configurado: repo + branch protection na `main`, board (GitHub Projects) com colunas/labels/workflows, e o `gh` validado pro Claude Code operar o board. Registro em `docs/setup/setup-github.md` (pasta de experimento, fora do workflow do projeto). A operação do board em si segue `docs/process/operar-board.md`.

## Bootstrap — a primeira vez (fundação do R0)

Acontece **uma vez**. Aqui a RFC fundadora e os ADRs vêm **antes** do Épico (no loop normal é o contrário):

1. **RFC-0001 "criar o sistema"** — Claude.ai, prompt `gerar-rfc`, template `rfc.md` → `docs/rfc/RFC-0001-<slug>.md`. Ao final, aponta os ADRs que vai parir.
2. **ADRs das decisões fundadoras** — Claude.ai, prompt `gerar-adr`, template `adr.md` → `docs/adr/`:
   - ADR-0001 — core em Python/FastAPI (em vez de Kotlin).
   - ADR-0002 — React no front.
   - ADR-0003 — monorepo (`api` + `web`).
3. **Épico do R0** — Claude.ai, prompt `gerar-epico`, template `epico.md` → `docs/epicos/r0-<slug>.md`.
4. Daqui em diante, segue o **loop por release** abaixo, a partir do passo "Planejar release".

> Commit dos docs macro numa branch `docs/...` (isentos de referenciar issue; nunca misturar prosa e código no mesmo PR).

## Loop por release (o que se repete sempre)

| # | Fase | Onde roda | Prompt | Gera / faz | Mora em | Portão |
|---|------|-----------|--------|------------|---------|--------|
| 1 | Épico do release | Claude.ai | `gerar-epico` | Épico (intenção) | `docs/epicos/<release>-<slug>.md` | você revisa |
| 2 | RFC *(só se grande/arriscado)* | Claude.ai | `gerar-rfc` | RFC | `docs/rfc/RFC-NNNN-<slug>.md` | você revisa; aponta ADRs |
| 3 | ADR *(só se bifurcação real)* | Claude.ai | `gerar-adr` | ADR | `docs/adr/ADR-NNNN-<slug>.md` | você revisa |
| 4 | Planejar release | Claude Code | `planejar-release` | propõe Stories e cria as cascas no board (Backlog) | board (ver `operar-board.md`) | aprova a lista antes de criar |
| 5 | Spec *(uma por Story, just-in-time)* | Claude.ai | `gerar-spec` | Spec | `docs/specs/<release>-<slug>.md` | você revisa |
| 6 | Decompor Spec | Claude Code | `decompor-spec` | ajusta a Story e cria as subtasks no board | board (ver `operar-board.md`) | aprova a quebra antes de criar |
| 7 | Implementar *(por subtask)* | Claude Code | — | branch `feat/`/`fix/` referenciando a subtask → código + testes → PR | código + PR | squash merge |
| 8 | Verify | você (+ Claude Code de apoio) | `verificar-contra-spec` | parecer da implementação vs. Spec (não altera código) | — | a decisão é sua |
| 9 | Fechar | — | — | atualizar `docs/`/`CLAUDE.md` se a implementação mudou alguma decisão | `docs/` | "Done" = PR mergeado + testes + docs |

Passos 2 e 3 são **condicionais** (a maioria dos releases não precisa de RFC, e ADR só quando há decisão com trade-off). Os passos 5–8 repetem **por Story** dentro do release.

## Regras transversais (valem em todo o fluxo)

- **Idioma:** `docs/` em PT-BR; código, board, commits e nomes em inglês (`CLAUDE.md`).
- **Commits de doc:** branch `docs/...`, isentos de referenciar issue; **nunca** um PR misturando prosa e código (`docs/process/estrategia-branch-pr.md`).
- **Branch de código:** referencia a subtask (`Closes #NNN`); trunk-based → PR → squash → promoção do mesmo artefato (`docs/process/estrategia-branch-pr.md`).
- **Operar o board:** via `gh` CLI conforme `docs/process/operar-board.md` — os prompts de ação já apontam pra lá.
- **Testes:** derivados da Spec; nunca enfraquecer/apagar teste pra "passar" (`CLAUDE.md`).
