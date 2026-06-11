# Spec: [Nome da feature]

> Fonte da verdade do SDD para esta feature. Detalha o que construir e como saber que terminou. Não re-justifica decisões que já vivem num ADR/RFC — referencia. O código é a verdade final; a Spec dirige.

## Referências

- Épico / release: [link pro doc do épico, ex.: R1]
- ADRs / RFCs relacionados: [ADR-NNNN, RFC-NNNN] — restrições já decididas, tratadas como dadas aqui.

## Visão geral

O que esta feature entrega, em uma ou duas frases.

## História (opcional)

Como [usuário], quero [ação] para [benefício]. O normal é ter história — uma Spec mapeia uma Story (fatia vertical de valor), que tem ator e valor de usuário. Só omita na exceção rara de task puramente técnica, sem ator nem valor de usuário.

## Critérios de aceite (EARS)

Escritos no padrão EARS. Cada critério é uma regra de negócio observável; variação de input vira exemplo/teste, não um critério novo. Um alvo não-funcional testável (ex.: latência) só entra aqui quando é gate de aprovação desta Story; caso contrário, mora em NFRs. Task puramente técnica também tem critérios EARS, desde que haja comportamento observável a verificar.

Padrões EARS:

- Ubíquo: O sistema DEVE [resposta].
- Dirigido a evento: QUANDO [gatilho], o sistema DEVE [resposta].
- Dirigido a estado: ENQUANTO [estado], o sistema DEVE [resposta].
- Comportamento indesejado: SE [condição], ENTÃO o sistema DEVE [resposta].
- Opcional/condicional a feature: ONDE [feature presente], o sistema DEVE [resposta].
- Complexo: os padrões podem ser combinados (ex.: QUANDO [gatilho], SE [condição], ENTÃO o sistema DEVE [resposta]) — sem quebrar a relação em critérios separados.

Exemplos concretos (cada linha vira um caso de teste). Obrigatório sempre que houver variação de input. A coluna Pré-condição é opcional — use quando a mesma entrada produz resultado diferente conforme o estado do sistema (critérios dirigidos a estado/evento); remova-a quando o resultado não depende de estado.

| Caso | Pré-condição (estado) | Entrada | Resultado esperado |
|------|-----------------------|---------|--------------------|
| ...  | ...                   | ...     | ...                |

## Dependências / pré-requisitos

O que precisa estar pronto ou decidido antes de implementar. Liste só dependências concretas e não óbvias — o artefato/contrato upstream de que esta Spec realmente depende, não a sequência cronológica de releases (que a sequência de releases já dá). Se não houver dependência não óbvia, deixe vazio.

- Artefato/contrato upstream específico (ex.: "modelo de transação do R1 estável", "nível de item do R6").
- ADRs/RFCs que restringem esta Spec.
- Pré-requisitos externos (biblioteca, nível de infra, fonte de dados, credencial).

## Design / abordagem

Como será construído, em alto nível: componentes, camadas, estados, fluxo. O que existe e como as peças se encaixam — não pseudo-implementação linha a linha. Pode citar que um endpoint existe, mas a forma exata dele mora em Contratos.

## Contratos

Contratos externos estáveis que esta feature cria ou consome: forma de request/response dos endpoints e, quando houver, nomes de filas/tópicos/buckets (que também são contrato). A régua: se mudar isso quebra um consumidor → é Contrato; se é detalhe interno que você refatora sem avisar ninguém → é Design. Vale o que sobreviveria a trocar a linguagem — inclusive o contrato web ↔ api dentro do monorepo (React/TS consumindo FastAPI já é fronteira de linguagem), não só contratos entre serviços.

## Modelo de dados

Tabelas/campos criados ou alterados, e o mecanismo estrutural com consequência observável/de NFR: índice que sustenta uma consulta específica, validação via query booleana em vez de carregar tudo na memória, upsert por chave natural pra ganhar idempotência. É o como-no-schema; o requisito que ele atende mora em NFRs, e a justificativa da escolha (quando houve alternativa real) mora em Decisões de refinamento.

## Decisões de refinamento

Registro leve das microdecisões tomadas ao detalhar/implementar esta feature: a escolha entre alternativas e o porquê. Curtas, datadas, em lista. Se uma decisão crescer e virar bifurcação real com trade-off, ela gradua pra um ADR — aqui fica só o ponteiro.

- [AAAA-MM-DD] [decisão curta: o que se escolheu, contra o quê, e por quê]

## NFRs

Os requisitos não-funcionais relevantes: performance, segurança, observabilidade, confiabilidade. É o requisito — o que deve valer (ex.: "reexecutar o import NÃO DEVE criar transações duplicadas"); o mecanismo que cumpre isso mora em Modelo de dados. Um alvo não-funcional que seja gate de aprovação desta Story sobe pra Critérios de aceite (EARS) e vira teste; aqui fica a qualidade ampla e o porquê do número, sem duplicar o alvo.

## Fora de escopo

O que explicitamente NÃO entra aqui.

## Plano de testes

Que testes (unitários/integração) cobrem os critérios de aceite, derivados da Spec. Para integração com terceiros (LLM, visão, Open Finance, pagamento), seguir `docs/process/estrategia-testes-integracao.md`: mock HTTP a partir de captura real para cobertura (todo PR) + cheque fino agendado contra o sandbox do provedor (não-bloqueante).

## Diagrama de sequência (opcional)

Quando o fluxo entre componentes/serviços não for óbvio pelo texto.

---
<!--
Regras de uso:
- Nome do arquivo: segue a convenção em `docs/process/processo-desenvolvimento-sdd.md` (padrão: `docs/specs/<release>-<slug>.md`).
- Uma Spec por Story (fatia vertical de valor). Task trivial sem bifurcação é exceção rara.
- A Spec é centralizada e viva (o Claude Code a consome ao implementar). O card da Story no board carrega só resumo + link para esta Spec, sem duplicar contrato/schema. O link é só nessa direção (card -> Spec); a Spec não referencia a issue.
- A partir desta Spec, o Claude Code ajusta a descrição/resumo da Story e cria as subtasks; o humano aprova. A Spec não tem seção "quebra em tasks".
- Régua de roteamento das decisões: requisito -> NFRs; mecanismo de schema -> Modelo de dados; escolha leve entre alternativas -> Decisões de refinamento; bifurcação real com trade-off -> ADR.
- Critérios derivam os testes; nunca enfraquecer nem apagar um teste pra "fazer passar".
-->