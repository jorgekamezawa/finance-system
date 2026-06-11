# Spec: Esqueleto local ponta a ponta (web + api + db)

> Fonte da verdade do SDD para esta feature. Detalha o que construir e como saber que terminou. Não re-justifica decisões que já vivem num ADR/RFC — referencia.

## Referências

- Épico / release: R0 — `docs/epicos/r0-esqueleto-no-ar.md` (Story #31).
- ADRs / RFCs: RFC-0001 (criar o sistema), ADR-0001 (core Python/FastAPI), ADR-0002 (React/TS no front), ADR-0003 (monorepo) — restrições já decididas, tratadas como dadas aqui.

## Visão geral

Provar a integração dos três componentes do sistema (front React, core FastAPI, banco Postgres) subindo todos com um único `docker compose up` a partir da raiz do monorepo, antes de qualquer deploy. O front exibe o resultado de um health da API que inclui a readiness do Postgres, fechando o trilho web↔api↔db em ambiente containerizado prod-like. Não há valor de produto: o entregável é o trilho de integração de pé.

## História

Como desenvolvedor do sistema (Jorge, single-user), quero subir os três componentes integrados com um comando local e ver, pela tela do front, que a API e o banco respondem, para provar que a fiação ponta a ponta fecha antes de empilhar deploy (#32) e a primeira feature (#33).

## Critérios de aceite (EARS)

Contrato da API (`/health`):

- QUANDO um cliente chama `GET /health` E o Postgres responde à checagem de readiness, o sistema DEVE retornar `200` com `{status:"ok", checks:{db:"ok"}}`.
- SE o Postgres não responde à checagem de readiness (erro de conexão ou timeout estourado), ENTÃO o sistema DEVE retornar `503` com `{status:"degraded", checks:{db:"down"}}`.

Tela de status (front):

- QUANDO a tela carrega, o front DEVE chamar `GET /health` da API.
- QUANDO a API responde `200`, o front DEVE exibir o estado "ok".
- QUANDO a API responde `503`, o front DEVE exibir o estado "degradado".
- SE a API está inalcançável (falha de rede / sem resposta), ENTÃO o front DEVE exibir "API indisponível".

Esqueleto integrado (compose da raiz):

- QUANDO se roda `docker compose up` na raiz, o sistema DEVE subir os três serviços (web, api, db) e deixá-los se comunicando (web→api por HTTP, api→db).
- O serviço `web` DEVE servir a imagem buildada (estágio final do multi-stage, estático via nginx), não o dev server.

Exemplos concretos (cada linha vira um caso de teste):

| Caso | Pré-condição (estado) | Entrada | Resultado esperado |
|------|-----------------------|---------|--------------------|
| health ok | Postgres no ar e respondendo | `GET /health` | `200` `{status:"ok",checks:{db:"ok"}}` |
| health db parado | Postgres parado (conexão recusada) | `GET /health` | `503` `{status:"degraded",checks:{db:"down"}}` |
| health db lento | Postgres pendurado além do timeout | `GET /health` | `503` `{status:"degraded",checks:{db:"down"}}` |
| front ok | API responde `200` | tela carrega | exibe "ok" |
| front degradado | API responde `503` | tela carrega | exibe "degradado" |
| front sem API | API inalcançável | tela carrega | exibe "API indisponível" |

## Dependências / pré-requisitos

- Sem dependência não óbvia de artefato upstream — #31 é a fundação do R0.
- Restrições já dadas: ADR-0001/0002/0003 (stack e layout) e RFC-0001 (forma macro).
- Pré-requisito externo: Docker + Docker Compose na máquina. A confiabilidade do ambiente WSL2/Win10 é tratada em runbook à parte, **fora** desta Spec.

## Design / abordagem

Três serviços orquestrados pelo `compose.yaml` da raiz do monorepo — este compose é o entregável do #31:

- `db`: Postgres (imagem oficial pinada).
- `api`: core FastAPI, imagem própria via Dockerfile multi-stage; expõe `GET /health`, que faz a readiness do banco com uma query leve (`SELECT 1`) sob um timeout curto. Lê config do ambiente em runtime (12-factor).
- `web`: front React/TS buildado (Vite) e servido como estático por nginx — o estágio final do Dockerfile multi-stage. A tela única chama o `/health` da API e renderiza o status.

O front fala com a API por HTTP **cross-origin**: lê a base da API de env (`VITE_API_URL`) e o FastAPI libera a origem do front por CORS. Em runtime local, `web` e `api` são containers separados em portas distintas — já é cross-origin, então o CORS do esqueleto espelha o de produção (#32).

Dois modos de rodar local (resolve a aparente contradição com `api/CLAUDE.md` e `web/CLAUDE.md`):

- `compose.yaml` da **raiz** = o esqueleto integrado (web+api+db containerizados, imagens prod-like multi-stage) — é o que esta Story entrega.
- `api/compose.yaml` (db+api) + `npm run dev` no front = loop de desenvolvimento do dia a dia (hot reload), já descrito nos CLAUDE.md — **não** é entregável desta Story.

## Contratos

`GET /health` (api → consumido pelo web; contrato web↔api, fronteira de linguagem React/TS ↔ FastAPI):

Resposta `200` (banco ok):

```json
{ "status": "ok", "checks": { "db": "ok" } }
```

Resposta `503` (banco não responde):

```json
{ "status": "degraded", "checks": { "db": "down" } }
```

Configuração injetada (contrato com o ambiente):

- `api` (runtime, 12-factor): URL/credenciais do Postgres (ex.: `DATABASE_URL`) e a(s) origem(ns) permitida(s) no CORS (a origem do front).
- `web` (build-time): `VITE_API_URL` — a base da API, inlinada no bundle em build (ver Decisões de refinamento).

## Modelo de dados

Nenhuma tabela nesta Story. A readiness do Postgres é uma query leve (`SELECT 1`) que não depende de schema — o modelo de transação e as migrations (Alembic) são do #33/R1 e do Nível 1 da infra, respectivamente.

## Decisões de refinamento

- [2026-06-11] Front↔API via **CORS** (cross-origin), com o front lendo a base de `VITE_API_URL`, contra a alternativa "mesma origem via proxy". Escolhido por ser padrão de mercado, genérico, multi-backend e agnóstico de linguagem. Não vira ADR (evita proliferação).
- [2026-06-11] Health: um único `GET /health` de readiness (inclui Postgres), **sem** split liveness/readiness — o split só ganha consumidor com orquestrador fazendo probes (k8s, Nível 3); YAGNI aqui.
- [2026-06-11] Config do **front é build-time** no R0: `VITE_*` é inlinado pelo Vite no build, então o bundle sai com a URL da API "assada" e ela entra como **build arg** do estágio de build. Aceito por simplicidade (YAGNI). Tensão registrada: difere do 12-factor runtime do `api` e da promoção do mesmo artefato (`estrategia-branch-pr.md`); injeção em runtime (env.js gerado no start do container / `envsubst` no nginx) fica como evolução se a promoção do artefato do front passar a doer.

## NFRs

- **Segurança:** containers rodam como usuário **não-root**; segredos por ambiente, nunca no código (12-factor).
- **Confiabilidade:** a checagem de readiness do banco tem **timeout curto** (alvo 1–2s) para que `/health` responda `503` prontamente, em vez de pendurar quando o Postgres não responde.
- **Reprodutibilidade:** versões **pinadas** (imagens base e dependências) para builds determinísticos.
- **Custo:** ambiente local; custo-alvo R$0 (deploy é #32).

Sem log estruturado em JSON nesta Story (cortado do escopo; entra adiante).

## Fora de escopo

- Deploy / CI-CD / HTTPS / ambientes (é #32).
- Qualquer endpoint ou tela de transação e o modelo de dados de transação (é #33/R1).
- Migrations / Alembic (Nível 1 da infra).
- Split liveness/readiness e probes de orquestrador (Nível 3).
- Log estruturado em JSON.
- Autenticação (v1 single-user sem auth real).
- Confiabilidade do ambiente WSL2/Win10 e qualquer workaround de proxy do Vite — é ambiente, mora em runbook à parte; o proxy do Vite, se usado, é config só de dev (`vite.config.ts`) e não muda a arquitetura de prod (que segue CORS).

## Plano de testes

- **api — `/health`:** teste de integração com Postgres no ar (caso ok → `200`/`db:ok`); testes com banco parado (conexão recusada) e com banco que estoura o timeout (ambos → `503`/`db:down`). Sem terceiros nesta Story, então `estrategia-testes-integracao.md` (mock HTTP + cheque agendado) não se aplica.
- **web — tela de status:** testes de comportamento (React Testing Library) cobrindo os três estados renderizados a partir da resposta da API: `200`→ok, `503`→degradado, inalcançável→"API indisponível" (a chamada à API mockada na fronteira do front).
- **esqueleto integrado:** verificação no Verify — `docker compose up` na raiz sobe os três serviços; a tela exibe o status; o `web` serve a imagem buildada (não o dev server). Conferir não-root e pinning como parte do Verify.

## Diagrama de sequência (opcional)

```
Tela (web/nginx) ──GET /health──► API (FastAPI) ──SELECT 1 (c/ timeout)──► Postgres
       ▲                               │
       └────────── status ─────────────┘
   front renderiza: ok (200) | degradado (503) | "API indisponível" (inalcançável)
```
