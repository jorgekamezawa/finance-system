# Quando usar cada documento (ADR / RFC / Spec / Y-statement)

Guia rápido pra decidir qual artefato criar. Complementa "A pirâmide de documentos" do processo.
Regra da pirâmide: **muitas Specs, alguns ADRs, poucas RFCs.**

## A regra mental

- **Épico** → vou **planejar um release** e quero fixar a intenção antes de quebrar em Stories. Responde "por que este release existe e como sei que entreguei?". É um documento que **funde dois papéis**: o do **Épico** clássico (o agrupador — dizer que um conjunto de Stories relacionadas forma este release) e o do **PRD** (a intenção de produto — problema, usuário, resultado, métrica, escopo). Fazem sentido juntos porque, no projeto solo, os dois acontecem no mesmo escopo e ao mesmo tempo: um release. E como o agrupamento das Stories no board já é feito pelo release + prefixo numérico, o documento não precisa rastrear nada — carrega **só a intenção**, ou seja, o conteúdo de um **PRD enxuto**. Um por release; todos têm. Mora em `docs/epicos/`. (Poucos, como as RFCs.)
- **RFC** → vou **construir algo grande/arriscado** e quero pensar/alinhar **antes** de codar.
  Responde "devemos fazer isso, e como, no geral?". Ampla e pra frente. (Poucas.)
- **ADR** → tomei **uma decisão com bifurcação real** e quero lembrar o **porquê** depois.
  Responde "por que escolhemos X em vez de Y?". Estreito, registro durável. (Alguns.)
- **Spec** → vou **construir uma feature** e preciso do plano construível + critérios de aceite.
  Responde "o que exatamente vou construir e como sei que terminei?". (Muitas.)
- **Y-statement** → o resumo de uma linha **no topo de um ADR** (o "bate o olho"). Não é um
  documento à parte.

## Relação entre eles

- Uma **RFC** discute uma iniciativa grande e **pare ADRs** (as bifurcações viram registros).
- Uma **Spec** consome ADRs/RFC como restrições já fixadas e detalha a construção da feature.
  Seus critérios de aceite são escritos em **EARS**.
- O fluxo: Épico/roadmap → (RFC, se grande) → ADRs das decisões → Spec → Tasks → Implement → Verify.

Observação importante: o ADR registra o **porquê + a forma arquitetural** de uma decisão; o plano
construível ("o dev só implementa") é responsabilidade da **Spec**, não do ADR.

## Perguntas-pavio (quando bater dúvida)

1. Vou planejar um release e fixar a intenção antes de quebrar em Stories? → **Épico**.
2. É uma escolha com alternativa real que vou querer justificar em 6 meses? → **ADR**.
3. Estou propondo construir algo grande e quero feedback/alinhar antes? → **RFC**.
4. Vou construir uma feature e preciso do plano + critérios de aceite? → **Spec**.
5. É uma escolha pequena de resposta fácil? → não força documento.

## Exemplos (deste projeto)

- Planejar o R0 (a intenção do release: problema, usuário, métrica) → **Épico**.
- Criar o sistema de finanças → **RFC** (RFC-0001).
- Core em Python/FastAPI; React no front; monorepo → **ADR** (0001, 0002, 0003).
- Importar histórico da planilha (R3) → **RFC** → pare ADRs (idempotência, mapeamento).
- Serviço de auth próprio (R8) → **RFC** → pare ADRs (sessão no Redis, formato de token).
- "Agregados sempre calculados, nunca armazenados" → **ADR** (decisão de modelagem).
- CRUD de transações (R1) → **Spec** (feature, sem bifurcação).

## Onde mora a informação de modelo de dados

Três camadas, complementares (não duplicam):

- **Código (migrations + models)** — o schema autoritativo. É a verdade final.
- **Spec → seção Modelo de dados** — o **delta** daquela feature + o mecanismo (índice, upsert por chave natural, etc.).
- **`docs/data-model/`** — o **mapa conceitual** consolidado: entidades, significado dos campos (ex.: "valor negativo = estorno"), relações e invariantes transversais (ex.: "agregados sempre calculados, nunca armazenados").

Regra: o `data-model/` é **conceitual/semântico** — não é cópia coluna-a-coluna do DDL (isso divergiria do código e viraria mentira). É doc vivo, semeado na primeira feature que cria entidades (R0/R1) e atualizado como parte do "docs atualizados" da Definition of Done.

## Docs de estratégia/processo (não são ADR/RFC/Spec)

Como a gente trabalha — branch/PR/deploy, testes de integração, feature flags — mora em docs de processo próprios e duráveis, **não** em ADRs: `estrategia-branch-pr.md`, `estrategia-testes-integracao.md`, `estrategia-feature-flags.md` (em `docs/process/`). Uma decisão pontual com bifurcação dentro de um desses temas ainda pode virar ADR; o doc de estratégia descreve o "como", o ADR registra um "porquê" específico.

## Anti-padrões a evitar

- ADR pra toda feature/entrega (isso é Spec).
- ADR só pro trivial ("lib X vs Y" sem peso) ou só pro cósmico ("seremos cloud-native"),
  pulando as decisões que de fato sustentam peso.
- Guardar fora do repo (Confluence/Notion solto): ADR/RFC moram em `docs/`, no mesmo repo do código.
- Editar ADR aceito: ele é imutável; mude criando um novo que o substitui.