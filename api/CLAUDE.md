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
- Postgres local: `docker compose up` (lê o `compose.yaml` desta pasta, que sobe só o banco); a api roda no host com `uv run fastapi dev app/main.py`

## Arquitetura & princípios (back-end)

Os princípios gerais (Clean Code, SOLID, YAGNI, comentários) estão na raiz; abaixo, a aplicação no back-end.

### Clean Architecture

- Camadas com a **regra da dependência apontando pra dentro**: o domínio (entidades, regras de negócio) não conhece framework, banco nem HTTP; as camadas de fora (FastAPI, Postgres, integrações) dependem do domínio, nunca o contrário.
- **Framework nas bordas.** FastAPI, driver/ORM e integrações ficam na borda (adapters). O caso de uso não importa `fastapi` nem sabe que existe HTTP.
- **Schemas Pydantic são DTOs de borda** (entrada/saída da API), não as entidades de domínio — mantenha os dois separados.
- Fluxo típico: rota (FastAPI) → caso de uso (aplicação) → domínio; acesso a dados por uma **abstração (repository)** que o domínio define e a borda implementa.
- É a direção, não cerimônia: num app pequeno as camadas podem ser leves — o que não pode é o domínio depender da borda.

### DDD (na medida certa)

- **Linguagem ubíqua:** o código usa os termos do domínio — transação, categoria, meta de gasto, receita, agregado — iguais aos do negócio e dos roadmaps. O nome no código é o nome que você usaria explicando pra alguém.
- **Táticos onde se pagam:** entidades, value objects (ex.: valor/dinheiro) e agregados quando agregam clareza — **sem over-engineering**. É um app single-user pequeno: não monte uma hierarquia DDD cerimoniosa onde uma função simples resolve. Comece simples; promova a value object/aggregate quando a regra justificar.

### SOLID (aplicação no back-end)

- **SRP:** cada módulo/classe/função com uma só razão de mudar.
- **DIP:** dependa de abstração — um `Protocol` (ou ABC) pro repository/serviço externo —, não da implementação concreta. É o que mantém o domínio puro e os testes fáceis (injeta um fake). (Paralelo com Kotlin no fim deste doc.)

### YAGNI, concreto

- Repository: crie **só os métodos que a feature atual chama** (`add`, `get_by_id`…), não um CRUD completo "porque vai precisar". Mesma regra pra serviços, casos de uso e endpoints.

## Modo professor — paralelos úteis (Python ⇄ Kotlin/Java)

- `pyproject.toml` + `uv` ≈ `build.gradle` + Gradle (declarar deps, resolver, isolar ambiente, travar versões).
- FastAPI (rotas/handlers) ≈ controllers do Spring Boot; **Pydantic** ≈ seus DTOs + validação (Bean Validation).
- `pytest` ≈ JUnit; `pytest-cov` ≈ JaCoCo.
- `mypy` / `pyright` ≈ a checagem de tipos que o compilador Kotlin/Java te dá de graça (em Python os type hints são opcionais; essas ferramentas é que os fazem valer).
- **Alembic** ≈ Flyway / Liquibase (migrations versionadas e reversíveis).
- `Protocol`/ABC ≈ `interface` do Kotlin (base do DIP); injeção via construtor ≈ Spring, só que sem o container mágico (você passa a dependência você mesmo).

## Notas

- Dois composes: o **desta pasta** sobe **só o Postgres** — a api roda no host (`uv run fastapi dev app/main.py`) e, com `npm run dev` no `web/`, formam o loop de dev do dia a dia (reload e debug nativos); o `compose.yaml` da **raiz** sobe o **esqueleto integrado** do R0 (web+api+db em imagens prod-like multi-stage) — é prova de integração, não o fluxo diário.
- O layout de `app/` (rotas, modelos, schemas, etc.) se define no R0; atualize este arquivo conforme a estrutura estabiliza.