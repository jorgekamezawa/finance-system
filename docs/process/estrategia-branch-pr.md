# Estratégia de branches, PRs e deploy

> Como o código sai da sua máquina e chega em produção neste projeto. Documento de processo (PT-BR). Irmãos: `estrategia-testes-integracao.md`, `estrategia-feature-flags.md`.

## Modelo: trunk-based

Trabalhamos em **trunk-based development**: a `main` é o tronco único e fica sempre liberável; o trabalho vem em branches curtas (horas a poucos dias) que voltam pra `main` rápido. O oposto é manter branches longas de feature/release que divergem por semanas e geram merges dolorosos.

No BTG você viveu um modelo de **branches por ambiente** (`develop` = UAT, `main` = PRD), o que se chama de GitFlow-lite / environment-branch. A gente **diverge** disso de propósito: ambiente não se define por branch, e sim por **promoção do mesmo artefato** pela pipeline. Branch de ambiente tende a acumular divergência (o que está em `develop` nem sempre é o que vai pra `main`) e a esconder drift entre ambientes; trunk-based + promoção de artefato mantém um só caminho e um só binário subindo de degrau.

## O fluxo

1. Branch curta a partir da `main` (`feat/...`, `fix/...`).
2. Deploy **da branch** no **UAT** pra validar no ar.
3. **Squash merge** pra `main` (histórico limpo: um commit por unidade de trabalho).
4. **Promoção do mesmo artefato** pra **PRD** pela pipeline — não rebuilda; sobe o binário já validado.

Config sempre por **12-factor** (variável de ambiente injetada de fora), **nunca** commitada. O que muda entre UAT e PRD é a config, não o artefato.

## Stacked PRs

PRs empilhados (uma branch em cima da outra, revisados em sequência) entram como **estudo**, não obrigação no solo. Servem quando uma Story se quebra em subtasks dependentes e você quer revisar em fatias pequenas sem esperar a anterior mergear.

## Feature flags no contexto

A maioria dos incrementos é **código inerte** (ainda não cabeado a nenhum caminho que executa) e **dispensa flag** — código morto não faz nada em produção. Flag só entra quando o código novo está **vivo** num caminho que agiria antes de estar pronto. Detalhe em `estrategia-feature-flags.md`.

## Ambientes

Dois ambientes nossos: **UAT** (pré-prod, onde a branch é validada) e **PRD** (produção). "Sandbox" **não** é nome de ambiente nosso — sandbox é o ambiente de teste de um **provedor terceiro** (ver `estrategia-testes-integracao.md`).

Alvo vs. realidade: o fluxo acima é o **alvo**. No **R0** (Nível 0 da infra) existe na prática **um ambiente só** (o deploy no ar) mais os **previews por PR** da Vercel; UAT + PRD separados começam no **Nível 1** da infra. Até lá, "deploy da branch no UAT" colapsa em "preview + prod único".

## Commits

- **Conventional Commits** em inglês (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`…).
- Toda branch **de código** referencia a issue que ela implementa — normalmente uma **subtask (sub-issue)**, já que a Story se decompõe em subtasks. Sub-issue é uma issue do board como qualquer outra (`#NNN`, `Closes #NNN`), então não há problema.
- **Exceção:** commits **só de doc** (Épico, RFC, ADR, Spec) são **isentos** da regra de referenciar issue — são artefatos de planejamento/refinamento, pré-task, e não andam no board como código. Entram via uma branch `docs/...` própria, separados do código da feature (nunca um PR misturando prosa e código).

## Fora de escopo agora

Canary / rollout progressivo (Argo Rollouts) é **Nível 5** da infra — entra como experimento efêmero depois, não no fluxo do dia a dia.