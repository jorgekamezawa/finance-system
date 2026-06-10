# ADR-0002: React no front

- **Status:** Aceito
- **Autor:** Jorge Kamezawa
- **Data:** 2026-06-10

## Resumo (Y-statement)

No contexto do front do sistema (sendo eu iniciante em front e usando o projeto também como portfólio), diante da escolha do framework de UI, decidimos por **React (com TypeScript)** e contra **Vue** e **Angular**, para ter a skill mais transferível e o maior ecossistema, aceitando uma curva que não é a mais suave e um modelo (componentes/hooks) sem paralelo no backend.

## Contexto

O front (`web/`) precisa de um framework de UI. A forma macro do sistema já está na RFC-0001; aqui se decide só o framework de front.

Três forças em tensão:

- **Aprendizado e mercado:** o front também é skill de portfólio — quero a opção mais transferível e com mais material de estudo.
- **Curva de entrada:** sou iniciante em front; facilidade de aprender conta.
- **Front leve:** por decisão, o front é básico ("backend-heavy fullstack") — peso e cerimônia de framework são custo, não benefício.

## Alternativas consideradas

### A) React
Biblioteca de UI baseada em componentes, a mais usada do mercado.
- **Prós:** maior comunidade, material de estudo e valor de mercado (skill transferível); ecossistema vasto (qualquer necessidade futura tem lib); ampla presença em ferramentas de IA, o que ajuda o aprendizado assistido; com TypeScript, recupero a tipagem estática que já tenho em Kotlin.
- **Contras:** não é a curva mais suave (JSX, hooks, "muitas formas de fazer"); é biblioteca, não framework — roteamento/estado/etc. são escolhas à parte.

### B) Vue
Framework progressivo, conhecido pela curva de entrada mais suave.
- **Prós:** didático, ótima documentação, menos boilerplate que React.
- **Contras:** mercado e ecossistema menores (menor ROI de portfólio); menos presença em material e ferramentas de IA.

### C) Angular
Framework opinativo, TypeScript-first, com injeção de dependência e estrutura de módulos/serviços.
- **Prós:** o mais "familiar" para quem vem de Spring (opinativo, DI, TS nativo, tudo incluso — roteamento, HTTP, forms).
- **Contras:** pesado e cerimonioso — choca com o front leve; curva íngreme; mais do que um app single-user pequeno precisa.

## Decisão

Adotamos **React (com TypeScript, via Vite)** como SPA para o front (`web/`), desde o R0.

TypeScript (não JS puro) é parte da decisão: recupera a tipagem estática que já tenho em Kotlin. E é uma **SPA pura, não Next.js** — o backend é o FastAPI em `api/`; não queremos um meta-framework com backend embutido. Mantemos o front básico: libs de roteamento, estado e data-fetching entram sob demanda, não pré-instaladas.

## Consequências

- (+) Skill de front mais transferível, com mais material e ecossistema — o front também é portfólio.
- (+) Com TypeScript, o modelo mental de tipos do Kotlin transfere quase direto, suavizando a entrada no front.
- (−) A curva de React é real (JSX, hooks); por ser biblioteca, escolho as peças (roteamento/estado) à parte, conforme a necessidade.
- (−) Componentes e hooks não têm paralelo limpo no backend Java/Spring — é modelo novo, aprendido do zero.
- (~) TypeScript, Vite e o "não Next.js" fazem parte desta decisão; não viram ADRs próprios.
