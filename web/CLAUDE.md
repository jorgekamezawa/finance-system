# CLAUDE.md — web/ (front React)

O front do Sistema de Finanças: SPA em **React** (básico; "backend-heavy fullstack") que consome a API do `api/`. Este arquivo é carregado **junto** com o CLAUDE.md raiz (regras compartilhadas estão lá).

## Stack

- **TypeScript** — JavaScript com tipos estáticos (a segurança de tipo que você já tem em Kotlin).
- **Vite** — build e dev server. SPA estática (deploy na Vercel). **Não** usamos Next.js: o backend é o FastAPI em `api/`, não um backend embutido no front.
- **npm** — gerenciador de pacotes (`package.json` + `package-lock.json`). Ubíquo no ecossistema JS.
- **Vitest** (+ **React Testing Library**) — testes. API compatível com Jest.
- **ESLint** (lint) + **Prettier** (format) — padrão de mercado em React.

## Comandos

> Os nomes exatos dos scripts são confirmados quando o front do R0 for criado (o scaffold do Vite já cria alguns). Os abaixo são a convenção.

- Instalar dependências: `npm install` — no CI (reproduzível, a partir do lock): `npm ci`
- Adicionar dependência: `npm install <pkg>` — de desenvolvimento: `npm install -D <pkg>`
- Rodar em dev: `npm run dev` (Vite)
- Build de produção: `npm run build`
- Pré-visualizar o build: `npm run preview`
- Testes: `npm run test` — em watch: `npm run test -- --watch`
- Checagem de tipos: `npm run typecheck` (roda `tsc --noEmit`)
- Lint: `npm run lint` (ESLint)
- Formatar: `npm run format` (Prettier)

## Modo professor — paralelos úteis (React/TS ⇄ Kotlin/Java)

- `package.json` + `npm` ≈ `build.gradle` + Gradle; os **scripts** do `package.json` ≈ as **tasks** do Gradle.
- **TypeScript** ≈ a tipagem estática do Kotlin; `interface`/`type` ≈ `interface`/`data class`. O `tsc` ≈ o compilador (`kotlinc`) checando tipos.
- **Vitest** ≈ JUnit (runner); **React Testing Library** testa o **comportamento** da UI (o que o usuário vê), não a implementação.
- **ESLint** ≈ Checkstyle / PMD / detekt (lint); **Prettier** ≈ formatter (spotless / ktlint format).
- ⚠️ **Sem paralelo limpo:** o modelo de **componentes** e **hooks** (`useState`, `useEffect`) do React não tem equivalente direto no backend Java/Spring — é um modelo novo. Explique do zero quando ele aparecer.

## Idiomas do React (siga estes)

> Não impomos Clean Architecture nem DDD tático do back-end aqui — o front segue os idiomas do React; forçar camadas/agregados estilo back-end no React é não-idiomático e atrapalha. (Fonte: react.dev.)

- **Componentes puros.** Um componente é uma função pura das suas entradas: mesmas props/state/context → mesmo JSX, **sem efeito colateral durante o render** (nada de chamada de API, mutação de variável externa ou DOM no corpo do componente). Efeito vai em event handler ou em `Effect`. É regra do próprio React — é ela que permite ao React re-renderizar com segurança.
- **Você provavelmente não precisa de `useEffect`.** `Effect` é uma saída de emergência pra sincronizar com um sistema **externo** (rede, DOM não-React, widget de terceiro). Pra derivar um valor a partir de props/state, **calcule durante o render** (ou `useMemo` se for caro) — não use Effect. Effect desnecessário deixa o código mais difícil de seguir, mais lento e mais propenso a bug. (É o tropeço nº 1 de quem começa.)
- **Composição sobre herança.** Reuso no React é por composição — componentes dentro de componentes, `children`, props —, não por herança de classe.
- **Fluxo de dados unidirecional.** Estado desce por props; mudança sobe por callback. Quando dois componentes precisam do mesmo estado, **suba o estado** (lift state up) pro ancestral comum.
- **Uma responsabilidade por componente.** Componente que faz coisa demais se quebra em menores — é o SRP da raiz aplicado a componente.
- **Custom hooks pra lógica com estado reutilizável.** Lógica que se repete ou que polui o componente sai pra um hook `useAlgo()`; o componente fica focado no que renderiza.
- **Colocation.** Mantenha junto o que muda junto: estado perto de onde é usado, e arquivos organizados por **feature**, não por tipo técnico.

## Notas

- Front é **básico** de propósito. Bibliotecas de **roteamento, estado ou data-fetching** (ex.: React Router, TanStack Query) entram só quando uma feature pedir — não pré-instale.
- O front consome a API do `api/`; em dev local roda à parte (`npm run dev`), fora do `compose.yaml` do `api/`.
- A estrutura de `src/` se define quando o front do R0 nascer; atualize este arquivo conforme estabiliza.