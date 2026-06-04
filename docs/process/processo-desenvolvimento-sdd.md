# Processo de Desenvolvimento — SDD com IA

Documento de referência do projeto **Sistema de Finanças**. Define como a gente trabalha: quais documentos existem, pra que servem, em que ordem, e como humano e IA dividem o trabalho. (Documentos irmãos: `roadmap-infra-devops.md`, `roadmap-features-sistema.md`.)

## Papéis (era da IA)

- **Humano (você):** dono da intenção, da arquitetura, das decisões e da **verificação**.
- **IA (Claude Code):** dona da decomposição em tasks e da implementação, com porteiras humanas.
- Princípio: o engenheiro vira "líder de agentes" — foca em decidir o que construir e em revisar, não em digitar cada linha.

## A pirâmide de documentos (o que é cada um)

- **PRD / Épico** — o *porquê* e o *o quê* no nível de produto (problema, usuário, resultado, métrica). Não técnico. No projeto solo, equivale a um *release* e quem veste o chapéu de PM é o Project. **Todo release tem.**
- **RFC (Request for Comments)** — proposta de solução pra uma feature parruda/arriscada, pra discutir o desenho antes de comprometer. Costuma *parir* ADRs. **Só pra coisa grande** (ex: o importador, o serviço de auth).
- **ADR (Architecture Decision Record)** — registra **uma decisão**: contexto, escolha, consequências. Curto, imutável. **Só quando há bifurcação real** com trade-off.
- **Spec** — a especificação **detalhada e executável por agente** de uma feature (requisitos + critérios de aceite + design + restrições/NFRs). É a **fonte da verdade** do SDD. **Toda feature tem.**
- **Task / Issue** — unidade de trabalho decomposta da Spec; vai no board kanban. Tem objetivo + critério de aceite.

Regra da pirâmide: **muitas Specs, alguns ADRs, poucas RFCs.** Não force documento onde não há decisão.

## O fluxo (Spec-Driven Development)

> Épico/PRD (intenção) → RFC + ADRs (solução macro + decisões) → **Spec** (detalhe executável) → Tasks (Claude Code decompõe) → Implement (Claude Code) → **Verify** (você, contra a Spec) → docs/CLAUDE.md atualizados.

A spec é o artefato canônico; código, testes e docs são gerados a partir dela. O passo que mais importa é o **Verify**: conferir o output contra a Spec. Ferramenta é secundária — markdown + agente já bastam (GitHub Spec Kit é a instância portátil, opcional).

## Cadência por release

1. Decisão fininha (ADR só se houver bifurcação).
2. Quebra em Issues no board kanban.
3. Claude Code constrói por issue (plan mode → código → testes → PR).
4. Revisão e merge.
5. Atualiza docs/CLAUDE.md só se a implementação mudou alguma decisão.

Board: Backlog → Pronto → Em andamento → Em revisão → Concluído. "Pronto" = issue tem objetivo + critério de aceite. "Concluído" = PR mergeado + testes passando + docs atualizados se preciso.

## Testes (decisão consciente: não é TDD clássico)

- A gente **não** faz o micro-ciclo manual red-green-refactor em cada unidade.
- Mas **testes não somem** — eles viram a porteira de verificação, **derivados da Spec**.
- Nível de comportamento/aceite: a expectativa é escrita **primeiro**, na Spec (critérios de aceite).
- Nível de unidade/integração: a IA **gera** os testes a partir da Spec; você revisa; têm que passar antes do merge.
- **Regra inegociável:** o agente nunca apaga nem enfraquece um teste pra "fazer passar".

## Modos de aprendizado (Python/React)

- **Modo professor (autopilot + explicação):** Claude Code constrói e explica cada passo como se ensinasse um iniciante na linguagem; você lê e entende. Configurado no `CLAUDE.md`.
- **Modo aprendizado (você dirige):** você escreve, a IA revisa e critica. Pros fundamentos que quer internalizar.
- **Régua de verificação:** só dá merge no que conseguir **explicar linha a linha**. Se não consegue revisar, não merge.
- **Três trilhas em paralelo:** (1) Claude Code em modo professor; (2) Alura pros fundamentos ordenados (nas pausas/limites); (3) reps de mão na massa, crescendo com o tempo.

## Mapa de arquivos (onde cada coisa mora)

**Repositório (GitHub) — fonte canônica:**
- `CLAUDE.md` (raiz) — regras/decisões/modo-professor, pro Claude Code.
- `docs/roadmaps/` — os dois roadmaps. `docs/process/` — este documento. `docs/data-model/` — modelo de dados.
- `docs/adr/`, `docs/rfc/`, `docs/specs/` — os documentos reais.
- `docs/templates/` — esqueletos (ADR/RFC/Spec). `docs/prompts/` — starter prompts.

**Project (Claude.ai):**
- Instruções personalizadas — o papel permanente.
- Conhecimento — os roadmaps + este processo + o modelo de dados (upload, ou via integração GitHub com Sync manual).

**Claude Code:** lê `CLAUDE.md` + `docs/` direto do repo.

Fluxo de um doc: rascunha no Project (com contexto dos roadmaps) → salva em `docs/` no repo → Claude Code lê ao implementar. O repo é a casa oficial.

## Starter prompts (pra gerar os documentos)

**Gerar ADR:**
> Aja como Tech Lead. Escreva um ADR usando o template em `docs/templates/adr.md` para a decisão: [DECISÃO]. Contexto: [CONTEXTO]. Liste alternativas consideradas e as consequências. Seja conciso.

**Gerar RFC:**
> Aja como Tech Lead. Escreva uma RFC usando `docs/templates/rfc.md` para a feature: [FEATURE]. Inclua motivação, design proposto, alternativas, riscos/NFRs e questões em aberto. Aponte quais ADRs essa RFC deve gerar.

**Gerar Spec:**
> Aja como Tech Lead. Escreva uma Spec executável usando `docs/templates/spec.md` para: [FEATURE/ISSUE]. Inclua critérios de aceite claros e testáveis, o toque no modelo de dados, NFRs e o que está fora de escopo. Ao final, proponha a quebra em tasks.

**Planejar um release:**
> Somos PM + Tech Lead. Vamos planejar o release [Rx] do roadmap de features. Liste os épicos, as decisões que precisam de ADR, e proponha a quebra inicial em issues com objetivo + critério de aceite.
