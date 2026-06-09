# CLAUDE.md — Sistema de Finanças

Projeto pessoal de finanças (substituir uma planilha) que também é veículo de aprendizado de Python, React, DevOps e IA. O autor é backend sênior (Kotlin/Java), aprendendo Python e React.

Este é o CLAUDE.md **raiz** — regras compartilhadas pelo monorepo inteiro. Cada subprojeto tem o seu: `api/CLAUDE.md` (core Python) e `web/CLAUDE.md` (front React). O Claude Code carrega este arquivo **junto** com o da pasta em que você estiver trabalhando.

## Idioma

- **Todo o projeto em inglês:** código, identificadores, comentários, nomes de teste, mensagens de commit, nomes de branch e descrições de PR.
- **Português apenas em:** a documentação (`docs/`) e a conversa com o autor.
- Commits seguem **Conventional Commits** em inglês (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`…).

## Arquitetura (decisões fechadas)

- **Monorepo.** `api/` = core em **Python (FastAPI)** + **Postgres**. `web/` = front em **React** (básico; "backend-heavy fullstack").
- **Kotlin** fica reservado pro futuro **serviço de autenticação/sessão** (release R8) e virá num **repositório separado**, não neste monorepo.
- Arquitetura event-driven (mensageria) entra mais tarde, não no início.
- v1 é **single-user, sem auth real** (auth gerenciado até o R8).
- Detalhes de stack, ferramentas e comandos de cada parte ficam em `api/CLAUDE.md` e `web/CLAUDE.md`, não aqui.

## Estrutura do repositório

```
api/                 # core Python (FastAPI) — tem seu próprio CLAUDE.md
web/                 # front React — tem seu próprio CLAUDE.md
docs/                # documentação (PT-BR):
                     #   roadmaps/, process/, data-model/, adr/, rfc/,
                     #   specs/, epicos/, templates/, prompts/
.github/workflows/   # pipelines de CI (uma por subprojeto, com filtro de caminho)
CLAUDE.md            # este arquivo (regras compartilhadas)
```

## Modo professor (importante)

O autor está aprendendo Python e React. Ao implementar ou alterar código:

- Explique cada passo como se ensinasse alguém que não conhece a linguagem.
- **Sempre que possível, compare com o equivalente em Kotlin/Java/Spring/Gradle/Maven** pra ancorar o conceito (ex.: "esse `pyproject.toml` faz o papel do `build.gradle`").
- Justifique as decisões e diga **por que** tal configuração está em tal lugar.
- Aponte o que é idiomático e o que é trade-off.
- De vez em quando, faça uma pergunta de verificação pra confirmar que o autor entendeu.

## Princípios de código (todo o monorepo)

- **Clean Code acima de tudo: legibilidade primeiro.** O código é escrito pra outro humano ler, não só pra máquina rodar — como diz Martin Fowler, qualquer um escreve código que a máquina entende; o difícil é escrever código que outro humano entenda. **Norte:** se uma pessoa de negócio lê os nomes dos métodos em sequência, ela entende o que o sistema faz.
- **Nomes que se explicam.** Método, função e variável dizem o que fazem e por quê; nada de abreviação enigmática. O nome carrega a intenção.
- **Comentários só quando necessário** (postura do Clean Code). Comentário é sinal de que o código não conseguiu se explicar — "Comments are always failures" (Robert C. Martin, *Clean Code*). Não comente código ruim: reescreva-o. Prefira extrair um método com nome bom a explicar um trecho com comentário. O comentário legítimo é o raro: o *porquê* não-óbvio (uma decisão, um workaround, uma restrição externa), nunca o *o quê* — isso o próprio código tem que dizer.
- **SOLID** vale pra todo código. A aplicação concreta (em Python no `api/`, nos componentes no `web/`) fica em cada subprojeto.
- **YAGNI — construa só o necessário pra feature de agora.** Não antecipe. Ex.: ao criar um repository de acesso ao banco, crie **só os métodos que a feature atual usa**, não o conjunto que você imagina que será útil. Isso vale pra tudo — endpoints, componentes, abstrações, config: nada "pro futuro" sem demanda real agora.

Arquitetura detalhada (Clean Architecture, DDD) fica no `api/CLAUDE.md`; os idiomas do front (React) ficam no `web/CLAUDE.md` — porque boa prática num não é necessariamente boa prática no outro.

## Testes

- Não fazemos TDD clássico. Os testes são **derivados da Spec** (unitários + integração) e devem passar antes do merge.
- **Nunca** apague nem enfraqueça um teste que falha pra "fazer passar". Conserte o código.

## Processo

- Seguimos SDD: Spec → Tasks → Implement → Verify. Ver `docs/process/processo-desenvolvimento-sdd.md`.
- Em dúvida sobre qual documento criar (ADR, RFC, Spec, data-model), ver `docs/process/quando-usar-cada-documento.md`.
- Branch, PR, deploy e ambientes: `docs/process/estrategia-branch-pr.md`. Testes de integração com terceiros: `docs/process/estrategia-testes-integracao.md`. Feature flags: `docs/process/estrategia-feature-flags.md`.
- Toda feature tem Spec; ADR só pra decisão com bifurcação real; RFC só pra feature grande.
- Antes de codar uma feature, gere/atualize a Spec; a partir dela, decomponha em Story + subtasks (você aprova); use plan mode.

## Convenções

- Toda branch **de código** referencia a issue que implementa (normalmente uma subtask). Fluxo completo em `docs/process/estrategia-branch-pr.md`.
- Commits pequenos e descritivos (Conventional Commits).
- **Documentação em markdown: um parágrafo por linha.** Não quebre o parágrafo no meio com quebra manual — alguns renderizadores (GitHub em comentários, Obsidian) tratam a quebra simples como quebra real e o texto fica torto. Uma linha por parágrafo reflui certo em qualquer lugar.
- Rode os testes antes de declarar uma tarefa concluída.
- README e ADRs atualizados quando a decisão muda.

## Peça confirmação antes de

- Adicionar dependências novas.
- Ações destrutivas (apagar dados/arquivos, migrations que removem colunas).
- Mudar configuração de infra/segurança.

## Nota

Mantenha este arquivo enxuto e **leve** (ele carrega em toda sessão). Procedimento longo ou específico de uma parte do código vai pro CLAUDE.md daquele subprojeto, pra um doc em `docs/`, ou pra uma skill — não aqui.