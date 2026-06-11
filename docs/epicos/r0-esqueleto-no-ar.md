# Épico R0: Esqueleto no ar (walking skeleton)

- **Status:** Rascunho
- **Release:** R0
- **Autor:** Jorge Kamezawa
- **Data:** 2026-06-10

## Resumo

O R0 põe o sistema inteiro no ar fazendo o mínimo: criar uma transação e vê-la numa listagem, com o core em FastAPI, o front em React e o banco Postgres, tudo deployado de ponta a ponta. O valor não é de produto — é fundação: provar que o caminho de produção fecha (front ↔ api ↔ banco, no ar, com pipeline) antes de empilhar qualquer feature. Por que agora: é o primeiro degrau do roadmap, e nada sobe depois sem esse trilho pronto.

## Problema / Motivação

Toda feature seguinte nasceria sobre infra não-provada se não houvesse um esqueleto no ar primeiro. O risco de integração — deploy, pipeline de CI/CD, o front conversando com a API e a API com o banco — ficaria represado e estouraria junto, tarde e no pior momento, em vez de ser exercitado e resolvido agora, quando o sistema ainda não faz quase nada. Enquanto não houver um trilho deployado pra receber o que vai substituir a planilha, a planilha segue sendo o sistema real. O custo de não fazer é o clássico: integrar no fim e descobrir que o caminho até produção não está de pé.

## Usuário

Single-user: eu (Jorge). Explicito mesmo sendo óbvio, porque o ator muda quando o multiusuário entrar (R8) e o campo já fica preparado pra isso.

## Objetivo / Resultado esperado

Depois do R0, o sistema está publicamente acessível por uma URL com HTTPS; dá pra criar uma transação pela UI e encontrá-la na listagem, com o dado persistido de verdade no Postgres; e um push mergeado na `main` dispara build e deploy sem nenhum passo manual. Não há valor de uso ainda — o desfecho é o trilho pronto: end-to-end deployado e pipeline funcionando, sobre os quais as features do R1 em diante vão ser construídas.

## Objetivo de aprendizado

O loop de deploy e a autoria de pipeline (CI/CD no GitHub Actions), containerização e 12-factor — casado com o Nível 0 da infra —, mais o primeiro contato prático com FastAPI e React num fluxo real ponta a ponta.

## Métricas de sucesso

Honestas e verificáveis (sem número de vaidade):

- Crio uma transação pela UI em produção e, após recarregar, ela aparece na listagem (prova que persistiu no Postgres).
- Um PR mergeado na `main` builda e faz deploy automaticamente, sem passo manual.
- O sistema está no ar numa URL pública servida por HTTPS.

## Escopo (alto nível)

- Criar uma transação pela UI com os quatro campos básicos (data, descrição, valor, categoria), persistindo no Postgres — a escrita ponta a ponta.
- Listar as transações criadas — a leitura ponta a ponta.
- Os três componentes (React em `web/`, FastAPI em `api/`, Postgres) deployados e conversando em produção.
- CI/CD mínimo no GitHub Actions (PR: lint + testes; merge: build + deploy), alinhado ao Nível 0 da infra.

## Fora de escopo

- CRUD completo (editar/excluir), lançamento de receitas, as ~20 categorias com as duas faixas e meta vs. realizado.
- Dashboards e tendências.
- Import do histórico, foto da NF e as features de IA.
- Autenticação real e multiusuário (o v1 é single-user sem auth por premissa — nada de auth no R0).

## Premissas e restrições

- Core em **Python/FastAPI** sobre **Postgres** (ADR-0001), front em **React/TypeScript** via Vite, SPA e não Next.js (ADR-0002), e **monorepo** `api/` + `web/` (ADR-0003) — restrições já decididas, tratadas como dadas.
- **v1 single-user, sem auth real** (premissa do projeto): não se constrói autenticação no R0.
- Deploy no **Nível 0** da infra (free tier — ver `roadmap-infra-devops.md`); custo-alvo ~R$0.
- **Caixa de tempo de ~1-2 semanas**: o esqueleto prova o trilho e não pode virar um projeto por si só (resolução da tensão PM×TL).
- No R0 existe, na prática, **um ambiente só** (o deploy no ar + os previews por PR da Vercel); o split UAT/PRD começa no Nível 1 da infra — ver `estrategia-branch-pr.md`.

## Referências

- Entrada deste release no roadmap: `docs/roadmaps/roadmap-features-sistema.md` → R0; infra correspondente: `docs/roadmaps/roadmap-infra-devops.md` → Nível 0.
- RFCs/ADRs relacionados: RFC-0001; ADR-0001 (core Python/FastAPI); ADR-0002 (React no front); ADR-0003 (monorepo).
- Specs que penduram neste Épico: preenchidas conforme as Stories ganham Spec.
