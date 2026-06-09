# Estratégia de testes de integração com terceiros

> Como testamos integrações com sistemas que não controlamos (LLM, visão, Open Finance, pagamento). Documento de processo (PT-BR). Irmãos: `estrategia-branch-pr.md`, `estrategia-feature-flags.md`.

## Princípio: ownership boundary

A escolha entre **mock** e **contrato** sai de quem é dono dos dois lados da fronteira. Se **você controla os dois lados** (ex.: core Python ↔ serviço de auth Kotlin, no R8), dá pra fazer **contract testing** — os dois evoluem juntos e o contrato é verificável ponta a ponta. Se o outro lado é um **terceiro** (você não controla a API dele), contrato bilateral não existe; aí o caminho é **mock**.

## Integrações externas (R0–R7)

Dois mecanismos complementares:

1. **Mock HTTP a partir de captura real** — grava uma resposta real do provedor uma vez e responde com ela nos testes. Roda em **todo PR**: rápido, determinístico, sem rede, sem custo. É o que dá **cobertura** do nosso código que fala com o terceiro.
2. **Cheque fino agendado contra o sandbox do provedor** — um teste pequeno que bate na API de teste **deles** num cron (não em todo PR). É **não-bloqueante**: não derruba o merge; serve pra **pegar drift** no contrato do provedor (eles mudaram a resposta) antes que estoure em produção.

O mock garante que o **nosso** lado está certo e estável; o cheque agendado vigia se o **lado deles** mudou. Um não substitui o outro.

## Contract testing: só no R8

Contract testing de verdade (consumer-driven, estilo Pact) entra **só no R8**, na fronteira **core Python ↔ auth Kotlin** — o primeiro ponto onde você controla os dois lados. Antes disso não há par pra contratar.

## "Seguro o suficiente"

A régua não é cobertura 100% nem testar contra produção. É **CI verde = seguro o suficiente**: CI (mock em todo PR) + safety net (cheque agendado, observabilidade) + **recuperação rápida** (se algo passar batido, você conserta e re-deploya rápido, porque o fluxo é trunk-based e o artefato é promovido).

## Nota sobre "sandbox"

Sandbox é o **ambiente de teste do provedor** (Stripe, Pluggy/Belvo, Open Finance — nome oficial deles), não um ambiente nosso. Nem todo terceiro tem: LLM e visão (R4–R6) em geral **não** oferecem sandbox — aí o cheque fino bate na API real com chave de teste e limite baixo. Daí "sandbox do provedor (quando houver)".

## Onde isto é consumido

O template de Spec (`docs/templates/spec.md`), na seção **Plano de testes**, referencia este doc pra integrações com terceiros.