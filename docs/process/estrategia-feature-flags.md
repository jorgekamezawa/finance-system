# Estratégia de feature flags

> Quando e como ligamos/desligamos comportamento sem novo deploy. Documento de processo (PT-BR). Irmãos: `estrategia-branch-pr.md`, `estrategia-testes-integracao.md`.

## Quando adotar

**Quando precisar** — não por padrão. A maioria dos incrementos é **código inerte**: ainda não cabeado a nenhum caminho que executa, então não faz nada em produção e **dispensa flag**. Flag só entra quando o código novo está **vivo** num caminho que agiria antes de você querer que ele aja.

Exemplo correto do "inerte → vivo": **PR1** adiciona um listener/handler **não cabeado** (ninguém chama; sem flag). **PR2** valida e **persiste** de fato — é aqui que o comportamento fica vivo, e é aqui que entra flag se você quiser ligar gradualmente. (Não confunda com salvar dado não-validado no PR1 — isso estaria errado.)

## Começar leve

- **Tabela no Postgres** com as flags.
- Um **helper** (interface + implementação) que o código de negócio consulta — nunca lê a tabela direto.
- **Cache em memória com TTL** na frente da tabela (não Redis agora; um TTL curto resolve a latência sem nova infra).
- **"Ausente = desligado"**: flag que não existe na tabela conta como `false`. Assim, ligar/desligar **não exige migration** — é dado, não schema.

## O helper é o seam

O helper existe pra ser o **ponto de troca** (seam): hoje ele lê Postgres + cache em memória; amanhã pode ler Redis, um serviço dedicado, ou um SaaS de flags — **sem tocar no código de negócio**, que só conhece a interface. É o padrão **OpenFeature** (interface neutra de avaliação de flag). Na sua praia: é inversão de dependência pura — o negócio depende da abstração (`FeatureFlags`), não da fonte concreta. Quando (ou se) migrar o backend é **decisão futura**; o seam só garante que ela seja barata.

## Relação com branches/PRs

Como a maioria dos PRs é código inerte, a maioria **não** precisa de flag — ver `estrategia-branch-pr.md`. Flag é a exceção, pro caminho vivo.

## Fora de escopo

Deduplicação/idempotência **não** é feature flag — é assunto à parte (idempotência natural por upsert por chave; ver a seção Modelo de dados da Spec). Mensageria, idem, é tardia no projeto (ver `CLAUDE.md`).