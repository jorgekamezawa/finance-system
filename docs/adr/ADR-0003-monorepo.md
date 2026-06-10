# ADR-0003: Monorepo (`api/` + `web/`)

- **Status:** Aceito
- **Autor:** Jorge Kamezawa
- **Data:** 2026-06-10

## Resumo (Y-statement)

No contexto de organizar o código do sistema (core Python em `api/` e front React em `web/`), desenvolvido por uma pessoa e evoluindo em lockstep, decidimos por **monorepo** (um repo, duas pastas) e contra **polyrepo** (repos separados), para ter commits atômicos atravessando front+back e um só lugar de docs/decisões, aceitando que os dois toolchains (Python e TS) convivem no mesmo repo.

## Contexto

O código tem duas partes — o core Python (`api/`) e o front React (`web/`) — e é preciso decidir se vivem num repo só ou em repos separados. A forma macro já está na RFC-0001; aqui se decide só o layout de repositório.

Três forças em tensão:

- **Coesão de desenvolvimento:** sou um dev só, e front e back evoluem juntos (o `web/` consome contratos do `api/`) — as mudanças costumam atravessar os dois.
- **Isolamento:** os dois têm ecossistemas distintos (Python/uv vs TS/npm) e deployam em lugares diferentes (Render vs Vercel), o que puxa para a separação.
- **Overhead:** projeto solo de aprendizado — quanto menos coordenação e cerimônia, melhor.

## Alternativas consideradas

### A) Monorepo simples por pastas
Um repositório com `api/` e `web/` como pastas; CI separada por filtro de caminho; cada app deploya do seu subdiretório.
- **Prós:** commits atômicos atravessando front+back (mudar um contrato da API e o consumidor num PR só); docs, ADRs e histórico num lugar; menos overhead de coordenação para um dev só; deploy independente continua possível (Vercel do `web/`, Render do `api/`).
- **Contras:** os dois toolchains (Python/uv e TS/npm) convivem no mesmo repo, exigindo disciplina para não misturar; sem o isolamento de ecossistema que o polyrepo dá de graça.

### B) Polyrepo
Um repositório para o `api/` e outro para o `web/`.
- **Prós:** isolamento total — cada repo com seu ecossistema, CI e versionamento 100% independentes; fronteira física clara entre back e front.
- **Contras:** mudança que cruza a fronteira (ex.: um contrato novo) vira dois PRs em dois repos, com coordenação manual; docs e decisões espalhados; overhead alto demais para um projeto solo nesta fase.

## Decisão

Adotamos **monorepo**: um repositório com `api/` e `web/` como pastas, desde o R0.

É um **monorepo simples por pastas, sem ferramental tipo Nx/Turborepo** — essas ferramentas se pagam com muitos pacotes JS/TS, não num split poliglota de dois apps (Python + React); seria over-engineering (YAGNI). A CI é separada por **filtro de caminho** (um workflow por subprojeto), e cada app deploya do seu subdiretório — monorepo **não** impede deploy independente.

Esta decisão cobre o **core** (api + web). Serviços futuros podem viver em repo próprio, na sua própria decisão.

## Consequências

- (+) Commits atômicos atravessando front+back; docs, ADRs e histórico num lugar só; menos coordenação para um dev solo.
- (+) Deploy segue independente (Vercel do `web/`, Render do `api/`) via filtro de caminho na CI — o ganho do monorepo sem perder a separação de deploy.
- (−) Dois toolchains (Python/uv e TS/npm) no mesmo repo; exige disciplina e CI por caminho para não embaralhar.
- (−) Sem o isolamento de ecossistema/versionamento que o polyrepo daria de graça.
- (~) Monorepo simples por pastas, sem Nx/Turborepo (YAGNI); cobre o core, serviços futuros podem ter repo próprio.
