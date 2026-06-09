# Épico <Release>: [Título do release]

> Documento de topo de um release. Funde dois papéis: o do **Épico** (o agrupador — dizer que um conjunto de Stories relacionadas forma este release) e o do **PRD** (a intenção de produto — problema, usuário, resultado, métrica, escopo). No nosso fluxo o agrupamento das Stories no board é feito pelo release + prefixo numérico, então este arquivo **não rastreia nada**: carrega só a intenção, ou seja, o conteúdo de um **PRD enxuto**. Não duplica o roadmap — **expande** a entrada deste release. Ver `docs/process/quando-usar-cada-documento.md`.

- **Status:** Rascunho | Ativo | Entregue
- **Release:** [R0, R1, ...]
- **Data:** AAAA-MM-DD

## Resumo

Um parágrafo: o que este release entrega e por que agora. É o "bate o olho" — quem lê só isto já entende o objetivo do release.

## Problema / Motivação

A dor concreta que este release resolve, e o que acontece se não fizermos (o custo de não fazer). Descritivo, do ponto de vista de quem sente o problema — ainda não é a solução.

## Usuário

Quem se beneficia. Hoje o sistema é single-user (você); explicite mesmo assim, porque o ator muda quando o multiusuário entrar (R8) e o campo já fica pronto pra isso.

## Objetivo / Resultado esperado

O desfecho de produto deste release: o estado do mundo depois que ele estiver no ar. Foco no resultado, não na lista de tarefas (a lista mora no Escopo, em alto nível).

## Objetivo de aprendizado

A skill nova que este release exercita de propósito (Python, React, IA, DevOps...). É parte do "por que agora" neste projeto — o sistema também é veículo de evolução técnica. Uma linha basta.

## Métricas de sucesso

Como você sabe que o release deu certo. Pode ser qualitativo num projeto solo ("paro de usar a planilha", "lanço uma despesa em poucos segundos"). Não invente número de vaidade — uma métrica honesta e verificável vale mais que cinco inventadas.

## Escopo (alto nível)

As capacidades/Stories que entram, em bullets de uma linha — a visão de guarda-chuva do release. **Alto nível**: o detalhe de cada uma mora na Spec da Story, não aqui. Não reescreva o roadmap; expanda-o.

- [capacidade / Story]
- [capacidade / Story]

## Fora de escopo

O que explicitamente NÃO entra neste release, pra cortar ambiguidade. Se algo foi considerado e adiado, diga pra onde foi (release futuro, RFC, "Norte de longo prazo").

## Premissas e restrições

As premissas assumidas e as restrições que pesam (técnicas, de produto, de prazo). ADRs/RFCs que restringem este release entram como **dados já decididos** — referencie, não re-justifique (mesma postura da Spec).

## Referências

- Entrada deste release no roadmap: [`docs/roadmaps/roadmap-features-sistema.md` → seção do release]
- RFCs/ADRs relacionados: [RFC-NNNN, ADR-NNNN]
- Specs que penduram neste Épico: [preenchidas conforme as Stories ganham Spec]

---
<!--
Regras de uso:
- Nome do arquivo: `docs/epicos/<release>-<slug>.md` (ex.: `r1-substituir-planilha.md`). Ver convenção em `docs/process/processo-desenvolvimento-sdd.md`.
- Um Épico por release. Todo release tem.
- NÃO é artefato de board: não lista subtasks nem rastreia status de Story. O agrupamento das Stories é via release + prefixo numérico no board; este doc é só a intenção (PRD enxuto).
- NÃO duplica o roadmap: o roadmap tem a entrada de uma linha; o Épico a expande just-in-time quando o release vira a vez.
- Vive em `docs/epicos/`, no mesmo repo do código. É doc vivo até o release ser entregue (Status: Entregue).
-->
