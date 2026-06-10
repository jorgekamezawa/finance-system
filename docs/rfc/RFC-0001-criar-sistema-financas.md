# RFC-0001: Criar o sistema de finanças pessoais

- **Status:** Rascunho
- **Autor:** Jorge Kamezawa
- **Data:** 2026-06-10

## Resumo

Construir um sistema próprio de finanças pessoais que substitui a planilha que uso hoje e serve de veículo de aprendizado de Python, React, DevOps e IA. O formato macro é um monorepo com core em Python/FastAPI sobre Postgres e front em React, single-user e sem auth real no v1; o núcleo é desenhado pra crescer em releases futuros sem ser reescrito. Por que agora: a planilha chegou no teto (digitação manual, análise pobre, sem detalhe por item) e eu quero um artefato que resolva isso enquanto me faz evoluir tecnicamente.

## Motivação

A planilha resolve o básico, mas chegou no limite: lançamento manual, a aba de "Média dos Gastos" quebrada, sem detalhe por item de compra e sem nenhuma camada de IA pra analisar ou perguntar sobre os dados. Beneficiário hoje: eu (single-user).

A motivação tem duas pernas de igual peso: resolver essas dores **e** usar o projeto como veículo de aprendizado dirigido de Python, React, DevOps e IA (sou backend sênior em Kotlin/Java aprendendo essas stacks de propósito). Não fazer = seguir preso à planilha e abrir mão da evolução técnica deliberada.

## Design proposto

O front (React SPA) conversa por HTTP/JSON com o core (FastAPI), que persiste em Postgres. O núcleo é desenhado pra crescer: capacidades novas (ex.: IA, autenticação, integrações externas) entram como módulos/serviços plugados nas bordas, em releases futuros, sem reescrever o core.

```
[ React SPA (web/) ] ──HTTP/JSON──► [ FastAPI core (api/) ] ──► [ Postgres ]

Bordas extensíveis em releases futuros (módulos/serviços plugados ao core).
O formato de cada capacidade futura fica pra sua própria Spec/ADR.
```

Decisões que valem **agora** (cada uma com seu registro):

- Core em **Python/FastAPI** + **Postgres** — ver ADR-0001.
- Front em **React**, básico — ver ADR-0002.
- **Monorepo** `api/` + `web/` — ver ADR-0003.
- **Single-user, sem auth real no v1** (premissa): proteção mínima; auth de verdade quando uma feature exigir, em RFC/ADR própria.
- **Agregados sempre calculados, nunca armazenados** (invariante de modelagem): vira ADR quando o modelo de dados nascer, no R1.

A sequência de releases vive em `docs/roadmaps/roadmap-features-sistema.md` e a evolução de infra/deploy em `docs/roadmaps/roadmap-infra-devops.md` (o v1 nasce no Nível 0). Esta RFC não os duplica.

## Alternativas

### A) Continuar na planilha
- **Prós:** custo zero, já pronta, conhecida.
- **Contras:** é o teto que motiva esta RFC; valor de aprendizado nulo.

### B) Usar um app de mercado (Actual Budget / Firefly III self-hosted, YNAB, Mobills/Organizze)
- **Prós:** maduro, barato ou grátis, mantido por terceiros.
- **Contras:** não cobre o combo que eu quero (IA sobre os meus dados, nível de item por NF, comparação de preço por mercado) e não me ensina nada.

### C) Construir sob medida — **escolhida**
- **Prós:** controle total + as features que não achei prontas em lugar nenhum + veículo de aprendizado + opcionalidade de virar produto no futuro (sem compromisso — ver "Norte de longo prazo" no roadmap de features).
- **Contras:** opção mais cara em esforço e economicamente irracional **se** o objetivo fosse só gerir dinheiro (aí B ganha). A justificativa do build é aprendizado + features diferenciadas, não custo-benefício. Risco de scope creep / abandono típico de projeto solo.

## Riscos e NFRs

Riscos:

- **Sustentabilidade solo / scope creep** (o maior) — mitiga: releases fininhos e no ar, uma Spec por Story.
- **Dado financeiro sensível em deploy público, mesmo single-user** — mitiga: HTTPS, segredos fora do código, auth quando uma feature exigir.
- **Custo de cloud paga** — mitiga: regras anti-susto de custo do `roadmap-infra-devops.md`.

NFRs (macro; o detalhe mora nas Specs e nos roadmaps):

- Config por **12-factor**; segredos fora do código.
- **Observabilidade básica desde o início** (health check, log estruturado).
- **Custo-alvo ~R$0** nos níveis fixos de infra.

## Questões em aberto

Bifurcações reais — graduam para os ADRs abaixo (a resolução fica registrada lá):

- Linguagem/framework do core: Python/FastAPI vs. Kotlin/Spring → **ADR-0001**.
- Framework de front → **ADR-0002**.
- Layout de repositório (monorepo vs. polyrepo) → **ADR-0003**.

Adiados / fora de escopo: autenticação de verdade (linguagem, topologia de repo, sessão) — terá RFC/ADR própria quando uma feature exigir; integração com fontes externas (ex.: Open Finance) — vira RFC própria se avançar.

## ADRs resultantes

- **ADR-0001** — core em Python/FastAPI.
- **ADR-0002** — React no front.
- **ADR-0003** — monorepo (`api/` + `web/`).