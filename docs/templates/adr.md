# ADR-NNNN: [Título curto da decisão]

- **Status:** Proposto | Aceito | Depreciado | Substituído por ADR-NNNN
- **Data:** AAAA-MM-DD

## Resumo (Y-statement)

No contexto de _\<X\>_, diante de _\<problema/força\>_, decidimos por _\<opção escolhida\>_ e
contra _\<alternativas rejeitadas\>_, para alcançar _\<benefício\>_, aceitando _\<trade-off\>_.

> Simplista, 2–3 linhas. É o resumo pra quem lê bater o olho e já entender a decisão.

## Contexto

As forças em jogo (técnicas, de produto, de prazo). Provavelmente em tensão — explicite.
Descritivo: ainda não defende a escolha.

## Alternativas consideradas

Sempre **pelo menos duas** opções reais. Para cada uma: uma linha do que é + prós/contras.

### A) \<opção\>
\<o que é, em uma linha\>
- **Prós:** ...
- **Contras:** ...

### B) \<opção\>
\<o que é, em uma linha\>
- **Prós:** ...
- **Contras:** ...

## Decisão

A opção escolhida, em voz ativa ("Adotamos..."). Detalhe no nível **arquitetural**: a forma e
os limites da decisão e as definições que dela decorrem — **não** o plano de implementação
(isso é da Spec).

## Consequências

Todas — positivas, negativas e neutras.
- (+) ...
- (−) ...
- (~) ...

---
<!--
Regras operacionais:
- ADR aceito é IMUTÁVEL. Se a decisão mudar, escreva um NOVO ADR que substitui este e
  atualize o Status acima para "Substituído por ADR-NNNN".
- Numeração monotônica (0001, 0002, ...), nunca reutilizada, nem quando um ADR é depreciado.
- Mora em docs/adr/, no mesmo repositório do código.
-->
