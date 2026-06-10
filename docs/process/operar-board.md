# Operar o board via gh CLI

> Como o Claude Code cria e conecta Stories e subtasks no board (GitHub Projects) deste projeto, via GitHub CLI (`gh`). É o procedimento que `docs/prompts/planejar-release.md` e `docs/prompts/decompor-spec.md` consomem. A decisão de usar `gh` (e não um servidor MCP) e o passo a passo de **configuração** do board moram em `docs/setup/` (fora do workflow do projeto); aqui fica só o **como operar**.

## Princípio: o Claude Code só CRIA; os Workflows cuidam do board

O board tem Workflows que, ao criar uma issue, já a adicionam ao projeto e setam Status = `Backlog`; sub-issues entram sozinhas. Então o Claude Code **só cria a issue** (título, body, label, assignee) e **linka a sub-issue** — não adiciona ao board nem seta status na mão. Mantém o fluxo mínimo (YAGNI) e evita passo redundante.

## Pré-requisitos de scope do token

- **Criar issue e linkar sub-issue:** basta o scope **`repo`** (presente numa auth padrão do `gh`).
- **Ler o board** (status, em qual coluna o item está): exige **`read:project`**. Sem ele, `gh project ...` e queries `projectV2` falham com `INSUFFICIENT_SCOPES`, e `gh issue view --json projectItems` volta vazio silenciosamente.
- Conferir os scopes: `gh auth status`. Adicionar o de leitura de board (interativo, abre o browser): `gh auth refresh -h github.com -s read:project`.

Resumo: a **criação** (o que os prompts fazem) funciona só com `repo`; o `read:project` é pra **verificar/ler** o board depois.

## Criar uma Story

O título carrega o prefixo de release (liga o card ao Épico); o body é resumo + link pra Spec; label `type: story`; assignee `@me`. Rode de dentro do repo (ou acrescente `--repo jorgekamezawa/finance-system`):

```bash
STORY_URL=$(gh issue create \
  --title "R0: <título da Story>" \
  --body "<resumo curto + link pra Spec>" \
  --label "type: story" \
  --assignee "@me")
STORY_NUM=$(echo "$STORY_URL" | grep -oE '[0-9]+$')
```

## Criar uma subtask e conectá-la à Story

Labels múltiplas usam **um `--label` por label** — nunca vírgula numa string só:

```bash
SUBTASK_URL=$(gh issue create \
  --title "R0: <título da subtask>" \
  --body "<o que entrega>" \
  --label "type: subtask" \
  --label "area: backend" \
  --assignee "@me")
SUBTASK_NUM=$(echo "$SUBTASK_URL" | grep -oE '[0-9]+$')
```

O `gh` **não** cria sub-issue nativamente — o vínculo pai→filho é via GraphQL `addSubIssue`, usando os **node IDs** (não os números). A mutation opera em Issues (não em Project), então **não exige `read:project`** — só `repo`:

```bash
STORY_ID=$(gh issue view "$STORY_NUM" --json id --jq '.id')
SUBTASK_ID=$(gh issue view "$SUBTASK_NUM" --json id --jq '.id')

gh api graphql -f query="
mutation {
  addSubIssue(input: { issueId: \"$STORY_ID\", subIssueId: \"$SUBTASK_ID\" }) {
    issue { number title }
    subIssue { number title }
  }
}"
```

## Verificar

- **Label e assignee** (o `gh` expõe direto):
  ```bash
  gh issue view "$STORY_NUM" --json title,labels,assignees
  ```
- **Sub-issues de uma Story** e **pai de uma subtask**: o `gh issue view` **não** expõe esses campos — use GraphQL:
  ```bash
  # sub-issues de uma Story
  gh api graphql -f query='
  query { repository(owner: "jorgekamezawa", name: "finance-system") {
    issue(number: <story_num>) { title subIssues(first: 50) { totalCount nodes { number title } } }
  }}'

  # pai de uma subtask
  gh api graphql -f query='
  query { repository(owner: "jorgekamezawa", name: "finance-system") {
    issue(number: <subtask_num>) { title parent { number title } }
  }}'
  ```
- **Status no board** (precisa de `read:project`):
  ```bash
  gh project item-list <project_number> --owner jorgekamezawa --format json
  ```

## Convenções (resumo)

- As labels precisam **já existir** no repo: `type: story`, `type: subtask`, `area: backend`, `area: frontend`, `bug`.
- Título carrega o **prefixo de release** (ex.: `R0: ...`) — é o que liga o card ao Épico (agrupamento por release + prefixo numérico).
- Assignee: `@me` (projeto solo; resolve pro login autenticado).
- `gh issue create` **não** abre prompt interativo quando título, body e label vêm nos flags.
- **Não** usar `gh issue view --json projectCards` — dá erro de Projects (classic), depreciado.
