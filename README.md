# finance-system

Sistema de finanças pessoais — substitui uma planilha e serve de **veículo de aprendizado** (Python, React, DevOps, IA). Monorepo: `api/` (core em Python/FastAPI + Postgres) e `web/` (front em React). Desenvolvido por **Spec-Driven Development (SDD)**; documentação em PT-BR, código em inglês.

## Comece por aqui

**Como o projeto funciona (o mapa do fluxo):** [`docs/process/guia-do-fluxo.md`](docs/process/guia-do-fluxo.md) — em cada fase, o que fazer, qual prompt usar, onde roda e onde salvar.

## Documentação

- **Roadmaps:** [`docs/roadmaps/`](docs/roadmaps/) — features e infra/DevOps.
- **Processo (SDD):** [`docs/process/processo-desenvolvimento-sdd.md`](docs/process/processo-desenvolvimento-sdd.md) · [`docs/process/quando-usar-cada-documento.md`](docs/process/quando-usar-cada-documento.md).
- **Templates e prompts:** [`docs/templates/`](docs/templates/) · [`docs/prompts/`](docs/prompts/).
- **Regras pro Claude Code:** [`CLAUDE.md`](CLAUDE.md) (raiz), `api/CLAUDE.md`, `web/CLAUDE.md`.

## Estrutura

```
api/    # core Python (FastAPI) — tem seu próprio CLAUDE.md
web/    # front React — tem seu próprio CLAUDE.md
docs/   # documentação (PT-BR): roadmaps, process, adr, rfc, specs, epicos, templates, prompts, setup
```