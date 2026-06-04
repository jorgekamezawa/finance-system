# CLAUDE.md — api/ (core Python)

O core do Sistema de Finanças: API em **FastAPI** sobre **Postgres**. Este arquivo é carregado **junto** com o CLAUDE.md raiz (regras compartilhadas estão lá).

## Stack

- **Python 3.13** (pinado em `.python-version`).
- **uv** — gerenciador de pacotes, ambiente virtual e lockfile (`pyproject.toml` + `uv.lock`). Faz o papel do Gradle/Maven no mundo Python.
- **FastAPI** (API) + **Pydantic** (validação/serialização).
- **Postgres** como banco; **Alembic** pra migrations (entra no Nível 1 da infra).
- **pytest** (+ **pytest-cov**) pra testes.
- **ruff** (lint + format), **mypy** (checagem de tipos, porteira do CI), **pyright** (no editor, via extensão Python/Pylance do VSCode).
- Config de ruff / mypy / pytest vive no `pyproject.toml`.

## Comandos

> Os comandos de **execução do app** serão confirmados quando o esqueleto do R0 existir. Os de ferramentas abaixo são estáveis.

- Sincronizar dependências (a partir do lock): `uv sync`
- Adicionar dependência: `uv add <pkg>` — de desenvolvimento: `uv add --dev <pkg>`
- Rodar o app em dev: `uv run fastapi dev app/main.py`
- Testes: `uv run pytest` — com cobertura: `uv run pytest --cov`
- Lint: `uv run ruff check` — corrigindo o que dá: `uv run ruff check --fix`
- Formatar: `uv run ruff format`
- Tipos (porteira do CI): `uv run mypy .`
- Migrations (a partir do Nível 1): `uv run alembic upgrade head` / `uv run alembic revision --autogenerate -m "..."`
- Stack local (app + Postgres): `docker compose up` (lê o `compose.yaml` desta pasta)

## Modo professor — paralelos úteis (Python ⇄ Kotlin/Java)

- `pyproject.toml` + `uv` ≈ `build.gradle` + Gradle (declarar deps, resolver, isolar ambiente, travar versões).
- FastAPI (rotas/handlers) ≈ controllers do Spring Boot; **Pydantic** ≈ seus DTOs + validação (Bean Validation).
- `pytest` ≈ JUnit; `pytest-cov` ≈ JaCoCo.
- `mypy` / `pyright` ≈ a checagem de tipos que o compilador Kotlin/Java te dá de graça (em Python os type hints são opcionais; essas ferramentas é que os fazem valer).
- **Alembic** ≈ Flyway / Liquibase (migrations versionadas e reversíveis).

## Notas

- O `compose.yaml` desta pasta sobe **só** o que é do core (app + Postgres). O front roda à parte, em `web/`.
- O layout de `app/` (rotas, modelos, schemas, etc.) se define no R0; atualize este arquivo conforme a estrutura estabiliza.
