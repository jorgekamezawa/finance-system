# Processo de Desenvolvimento — SDD com IA

Documento de referência do projeto **Sistema de Finanças**. Define como a gente trabalha: quais documentos existem, pra que servem, em que ordem, e como humano e IA dividem o trabalho. (Documentos irmãos: `roadmap-infra-devops.md`, `roadmap-features-sistema.md`.)

## Papéis (era da IA)

- **Humano (você):** dono da intenção, da arquitetura, das decisões e da **verificação**.
- **IA (Claude Code):** dona da decomposição em tasks e da implementação, com porteiras humanas.
- Princípio: o engenheiro vira "líder de agentes" — foca em decidir o que construir e em revisar, não em digitar cada linha.

## A pirâmide de documentos (o que é cada um)

- **Épico** — o *porquê* e o *o quê* no nível de produto (problema, usuário, resultado, métrica). Não técnico. Funde dois papéis: o de **Épico** (agrupador das Stories do release) e o de **PRD** (a intenção); como o agrupamento no board já é feito pelo release + prefixo numérico, o documento carrega só a intenção — um **PRD enxuto**. No projeto solo equivale a um *release* e quem veste o chapéu de PM é o Project do Claude.ai. É um **documento** (mora em `docs/epicos/`), **fora do board**. **Todo release tem.** (O detalhe dos dois papéis mora em `quando-usar-cada-documento.md`.)
- **RFC (Request for Comments)** — proposta de solução pra uma feature parruda/arriscada, pra discutir o desenho antes de comprometer. Costuma *parir* ADRs. **Só pra coisa grande** (ex: o importador, o serviço de auth).
- **ADR (Architecture Decision Record)** — registra **uma decisão**: contexto, escolha, consequências. Curto, imutável. **Só quando há bifurcação real** com trade-off.
- **Spec** — a especificação **detalhada e executável por agente** de uma feature (requisitos + critérios de aceite em **EARS** + design + contratos + restrições/NFRs). É a **fonte da verdade** do SDD, **centralizada e viva** (o Claude Code a consome ao implementar). **Uma Spec por Story.**
- **Story / Task** — a **fatia vertical de valor**; é o card que anda no board (INVEST na Story, SMART na Task). Back e front são **subtasks sob uma Story**, não Stories separadas.
- **Subtask** — sub-issue sob uma Story; **também anda no board e tem responsável (assignee)**, de onde sai o quem-fez-o-quê. Status compartilhado com a Story + views filtradas.

Regra da pirâmide: **muitas Specs, alguns ADRs, poucas RFCs.** Não force documento onde não há decisão.

## O fluxo (Spec-Driven Development)

> Épico (intenção) → RFC + ADRs (decisões macro) → **commit dos docs macro** → Claude Code **planeja o release** (propõe as Stories; você aprova) → cria as cascas de Story no board → você escolhe a Story e escreve a **Spec** (uma por Story, just-in-time) → **commit da Spec** → Claude Code **ajusta a descrição da Story e cria as subtasks** (você aprova) → Implement (Claude Code, por subtask) → **Verify** (você, contra a Spec) → docs/CLAUDE.md atualizados.

A spec é o artefato canônico; código, testes e docs são gerados a partir dela. O passo que mais importa é o **Verify**: conferir o output contra a Spec. Uma Spec por Story; o card do board carrega só **resumo + link** pra Spec (o link é só na direção card → Spec). Ferramenta é secundária — markdown + agente já bastam (GitHub Spec Kit é a instância portátil, opcional).

## Cadência por release

1. Épico do release + decisão fininha (ADR só se houver bifurcação); commit dos docs macro.
2. Claude Code planeja o release e cria as Stories no board (você aprova). O Épico fica **fora do board**; o prefixo numérico liga os cards a ele.
3. Por Story: você escreve a Spec → Claude Code decompõe em subtasks (você aprova) → constrói por subtask (plan mode → código → testes → PR).
4. Revisão e merge (squash; ver `estrategia-branch-pr.md`).
5. Verify contra a Spec; atualiza docs/CLAUDE.md só se a implementação mudou alguma decisão.

Board: Backlog → Ready To Start → In Progress → In Review → Done. **Story/Task** = o card que anda no board; **Subtask** = sub-issue sob a Story, que também anda no board e tem **assignee** — o quem-fez-o-quê sai do assignee, não de garimpar commit/PR. Status compartilhado + views filtradas (limitação do GitHub vs. Jira). "Ready To Start" = a Story tem objetivo + critério de aceite e Spec escrita. "Done" = PR mergeado + testes passando + docs atualizados se preciso.

## Testes (decisão consciente: não é TDD clássico)

- A gente **não** faz o micro-ciclo manual red-green-refactor em cada unidade.
- Mas **testes não somem** — eles viram a porteira de verificação, **derivados da Spec**.
- Nível de comportamento/aceite: a expectativa é escrita **primeiro**, na Spec (critérios de aceite **em EARS**).
- Nível de unidade/integração: a IA **gera** os testes a partir da Spec; você revisa; têm que passar antes do merge.
- Integração com terceiros (LLM, visão, Open Finance, pagamento): ver `estrategia-testes-integracao.md`.
- **Regra inegociável:** o agente nunca apaga nem enfraquece um teste pra "fazer passar".

## Modos de aprendizado (Python/React)

- **Modo professor (autopilot + explicação):** Claude Code constrói e explica cada passo como se ensinasse um iniciante na linguagem; você lê e entende. Configurado no `CLAUDE.md`.
- **Modo aprendizado (você dirige):** você escreve, a IA revisa e critica. Pros fundamentos que quer internalizar.
- **Régua de verificação:** só dá merge no que conseguir **explicar linha a linha**. Se não consegue revisar, não merge.
- **Três trilhas em paralelo:** (1) Claude Code em modo professor; (2) Alura pros fundamentos ordenados (nas pausas/limites); (3) reps de mão na massa, crescendo com o tempo.

## Mapa de arquivos (onde cada coisa mora)

**Repositório (GitHub) — fonte canônica:**
- `CLAUDE.md` (raiz) — regras/decisões/modo-professor, pro Claude Code.
- `docs/roadmaps/` — os dois roadmaps. `docs/process/` — este documento, `quando-usar-cada-documento.md` e as estratégias (`estrategia-branch-pr.md`, `estrategia-testes-integracao.md`, `estrategia-feature-flags.md`). `docs/data-model/` — modelo de dados (conceitual).
- `docs/epicos/` — os épicos por release. `docs/adr/`, `docs/rfc/`, `docs/specs/` — os documentos reais.
- `docs/templates/` — esqueletos (ADR/RFC/Spec/Épico). `docs/prompts/` — starter prompts (um arquivo por prompt).

**Convenção de nomes:**
- ADR: `docs/adr/ADR-NNNN-slug.md` (NNNN monotônico, nunca reutilizado).
- RFC: `docs/rfc/RFC-NNNN-slug.md`.
- Spec: `docs/specs/<release>-<slug>.md` (ex.: `r1-crud-transacoes.md`; pode incluir o número da issue: `r1-123-crud-transacoes.md`).
- Épico: `docs/epicos/<release>-<slug>.md`.
- data-model: docs vivos por entidade em `docs/data-model/`, sem numeração.

**Project (Claude.ai):**
- Instruções personalizadas — o papel permanente.
- Conhecimento — os roadmaps + este processo + o modelo de dados (upload, ou via integração GitHub com Sync manual).

**Claude Code:** lê `CLAUDE.md` + `docs/` direto do repo.

Fluxo de um doc: rascunha no Project (com contexto dos roadmaps) → salva em `docs/` no repo → Claude Code lê ao implementar. O repo é a casa oficial.

## Starter prompts

Moram em `docs/prompts/` (um arquivo por prompt). Os de **autoria** (gerar ADR/RFC/Spec/Épico) rodam no **Claude.ai**, que já carrega persona + Knowledge. Os de **ação** (planejar release, decompor Spec, verificar contra Spec) rodam no **Claude Code** e referenciam arquivos com path exato e `@` no começo (ex.: `@docs/templates/spec.md`).