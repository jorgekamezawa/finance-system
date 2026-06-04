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

## Notas

- Front é **básico** de propósito. Bibliotecas de **roteamento, estado ou data-fetching** (ex.: React Router, TanStack Query) entram só quando uma feature pedir — não pré-instale.
- O front consome a API do `api/`; em dev local roda à parte (`npm run dev`), fora do `compose.yaml` do `api/`.
- A estrutura de `src/` se define quando o front do R0 nascer; atualize este arquivo conforme estabiliza.
