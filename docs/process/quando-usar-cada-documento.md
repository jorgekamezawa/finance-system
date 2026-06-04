# Quando usar cada documento (ADR / RFC / Spec / Y-statement)

Guia rápido pra decidir qual artefato criar. Complementa "A pirâmide de documentos" do processo.
Regra da pirâmide: **muitas Specs, alguns ADRs, poucas RFCs.**

## A regra mental

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
- O fluxo: Épico/roadmap → (RFC, se grande) → ADRs das decisões → Spec → Tasks → Implement → Verify.

Observação importante: o ADR registra o **porquê + a forma arquitetural** de uma decisão; o plano
construível ("o dev só implementa") é responsabilidade da **Spec**, não do ADR.

## Perguntas-pavio (quando bater dúvida)

1. É uma escolha com alternativa real que vou querer justificar em 6 meses? → **ADR**.
2. Estou propondo construir algo grande e quero feedback/alinhar antes? → **RFC**.
3. Vou construir uma feature e preciso do plano + critérios de aceite? → **Spec**.
4. É uma escolha pequena de resposta fácil? → não força documento.

## Exemplos (deste projeto)

- Criar o sistema de finanças → **RFC** (RFC-0001).
- Core em Python/FastAPI; React no front; monorepo → **ADR** (0001, 0002, 0003).
- Importar histórico da planilha (R3) → **RFC** → pare ADRs (idempotência, mapeamento).
- Serviço de auth próprio (R8) → **RFC** → pare ADRs (sessão no Redis, formato de token).
- "Agregados sempre calculados, nunca armazenados" → **ADR** (decisão de modelagem).
- CRUD de transações (R1) → **Spec** (feature, sem bifurcação).

## Anti-padrões a evitar

- ADR pra toda feature/entrega (isso é Spec).
- ADR só pro trivial ("lib X vs Y" sem peso) ou só pro cósmico ("seremos cloud-native"),
  pulando as decisões que de fato sustentam peso.
- Guardar fora do repo (Confluence/Notion solto): ADR/RFC moram em `docs/`, no mesmo repo do código.
- Editar ADR aceito: ele é imutável; mude criando um novo que o substitui.
