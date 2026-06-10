# ADR-0001: Core em Python/FastAPI

- **Status:** Aceito
- **Data:** 2026-06-10

## Resumo (Y-statement)

No contexto do core do sistema (sendo eu sênior em Kotlin/Java e usando o projeto também para aprender), diante de um roadmap com IA no centro do diferencial, decidimos pelo core em **Python/FastAPI** e contra **Kotlin/Spring** e **Node/TypeScript**, para praticar Python e ficar coeso com o ecossistema de IA, aceitando menor velocidade no curto prazo e tipagem garantida por ferramenta, não pelo compilador.

## Contexto

O core (`api/`) precisa de linguagem e framework. A forma macro do sistema já está na RFC-0001; aqui se decide só a linguagem/framework do core.

Três forças em tensão:

- **Produtividade:** sou sênior em Kotlin/Spring — é onde entrego mais rápido hoje.
- **Aprendizado:** o projeto é, por decisão, veículo para aprender Python (e React).
- **IA:** o roadmap põe features de IA no centro do diferencial, e Python é a língua franca desse ecossistema.

## Alternativas consideradas

### A) Python/FastAPI
Framework web assíncrono de Python, dirigido por type hints, com Pydantic para validação/serialização.
- **Prós:** pratica Python desde o R0; mesma linguagem do ecossistema de IA, então as features de IA ficam coesas com o core, sem fronteira de linguagem; mapeia bem no modelo mental de Spring (type hints + Pydantic ≈ tipos + Bean Validation; injeção por construtor); leve, adequado a um app single-user pequeno.
- **Contras:** menor velocidade no curto prazo; tipagem é opt-in (mypy/pyright a recuperam, mas não é garantida pelo compilador); os modelos sync/async somam curva.

### B) Kotlin/Spring
Meu stack atual: Spring Boot sobre a JVM, onde sou sênior.
- **Prós:** produtividade máxima agora; ecossistema maduro; tipos garantidos pelo compilador.
- **Contras:** aprendizado de linguagem nova ≈ zero (anula metade do propósito do projeto); cria costura de linguagem para o ecossistema de IA (Python); mais pesado para um app single-user minúsculo.

### C) Node/TypeScript (NestJS)
Unificar a linguagem com o front (React/TS): um só idioma no monorepo.
- **Prós:** uma linguagem no front e no back, menos troca de contexto; tipagem razoável.
- **Contras:** não serve à meta de aprender Python; ainda deixa a costura para o ecossistema de IA (Python); seria uma terceira coisa nova para aprender sem esse retorno.

## Decisão

Adotamos **Python com FastAPI sobre Postgres** como o core (`api/`) desde o R0.

FastAPI (e não Django ou Flask) é parte da decisão: queremos async, type hints e Pydantic de primeira classe num framework leve — o Django é peso demais para um app single-user pequeno, e o Flask não traz validação/tipagem/async embutidos.

Esta decisão cobre o **core**. Serviços futuros plugados nas bordas decidem a própria linguagem quando existirem, na sua RFC/ADR.

## Consequências

- (+) Python desde o dia um; as features de IA nascem na mesma linguagem do core, sem costura.
- (+) FastAPI (Pydantic + type hints + injeção por construtor) suaviza a transição Kotlin→Python; core leve, alinhado ao YAGNI.
- (−) Velocidade de entrega menor que em Spring no curto prazo; absorvo a curva de Python, async e do ferramental de tipos.
- (−) Tipagem garantida por ferramenta, não pelo compilador: exige disciplina (mypy como porteira do CI; ver `api/CLAUDE.md`).
- (~) A sub-escolha FastAPI vs Django/Flask fica registrada aqui, sem virar ADR próprio.
