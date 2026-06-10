# Setup do GitHub — Sistema de Finanças

> Runbook das configurações do GitHub deste projeto. Documento operacional (PT-BR). Cresce em etapas: cada bloco de config que a gente fecha entra aqui, na ordem em que foi feito.

## O que este documento cobre

- **1. Branch protection na `main`** — feito (esta seção).
- **2. Board no GitHub Projects** — feito (esta seção).
- **3. Operar o board via gh CLI (e por que não MCP agora)** — feito (esta seção).

As seções "a vir" são preenchidas só quando a config existir de fato — nada especulativo aqui.

---

## 1. Branch protection na `main`

### Objetivo

Garantir que ninguém — nem você com pressa — commite direto na `main`: todo trabalho entra por branch curta → PR → squash merge, como define `docs/process/estrategia-branch-pr.md`. A `main` é o tronco único do trunk-based e fica sempre liberável.

### Clássico vs. Ruleset (por que clássico)

O GitHub oferece dois caminhos na tela de Branches: **Add classic branch protection rule** (o sistema clássico) e **Add branch ruleset** (o sistema novo, pra onde o GitHub está migrando o investimento). Os dois entregam a mesma proteção neste cenário. Escolhemos o **clássico** porque, para um repositório único, uma só branch protegida e fluxo solo, ele resolve com menos cliques e mapeia 1:1 com esta config. Rulesets tem extras (camadas de regras, listas de bypass, ligar/desligar sem apagar) que hoje seriam over-engineering. Fica registrado como evolução futura: migrar esta regra para um Ruleset é um exercício de fim de semana, sem perda — as opções são quase as mesmas, muda mais a tela do que o conceito.

### Pré-requisitos

- Repositório **público** (no GitHub Free, branch protection só é grátis em repo público; em repo privado exigiria GitHub Pro). É o nosso caso.
- Você ser **admin** do repositório (é o dono).

### Passo a passo

1. No repositório, abra **Settings** → no menu lateral, **Branches**.
2. Clique em **Add classic branch protection rule**.
3. **Branch name pattern**: digite `main`.
4. Marque **Require a pull request before merging**.
5. **Desmarque** a sub-opção **Require approvals**. É assim que se exige 0 aprovações — o dropdown de número some (o mínimo dele é 1). O PR continua obrigatório, mas sem revisor humano: você mergeia o próprio PR. É a config trunk-based solo.
6. Deixe **desmarcadas** as demais sub-opções de revisão: **Dismiss stale pull request approvals when new commits are pushed**, **Require review from Code Owners** e **Require approval of the most recent reviewable push** (todas dependem de revisor, que não temos).
7. **Require status checks to pass before merging**: deixe **desmarcado por enquanto**. Os checks (lint/testes) só aparecem nesta lista depois que um workflow de CI rodar ao menos uma vez — e o CI nasce no R0. Voltar aqui e ligar quando o pipeline existir (ver Pendências).
8. **Require conversation resolution before merging**: **marque** (opcional; te obriga a resolver os comentários antes de mergear — disciplina a custo zero).
9. **Require signed commits**: deixe **desmarcado** (assinatura GPG/SSH adiciona setup; dá pra ligar depois sem dor).
10. **Require linear history**: **marque** (com squash merge o histórico já é linear; isto só impõe a regra e bate com "um commit por unidade de trabalho").
11. **Require deployments to succeed before merging**: deixe **desmarcado** (não há ambientes de deploy configurados).
12. **Lock branch**: deixe **desmarcado** (lock deixaria a branch somente-leitura — bloquearia até os merges).
13. **Do not allow bypassing the above settings**: **marque** (faz as regras valerem inclusive para admins — ou seja, para você). Com aprovações em 0, marcar isto **não te tranca**: você segue mergeando seus PRs; só perde o atalho de empurrar direto na `main`. É a escolha que faz você de fato praticar o fluxo.
14. **Allow force pushes**: deixe **desmarcado**.
15. **Allow deletions**: deixe **desmarcado** (junto com o anterior, impede reescrever ou apagar a `main`).
16. Clique em **Create** (ou **Save changes**).

### Configuração final (referência rápida)

| Opção | Estado | Por quê |
|---|---|---|
| Branch name pattern | `main` | a branch protegida |
| Require a pull request before merging | ✅ | todo trabalho passa por PR |
| Require approvals | ⬜ | solo: 0 aprovações (você não aprova o próprio PR) |
| Dismiss stale approvals on new commits | ⬜ | depende de revisor |
| Require review from Code Owners | ⬜ | depende de revisor |
| Require approval of the most recent reviewable push | ⬜ | depende de revisor |
| Require status checks to pass | ⬜ (por ora) | ligar quando o CI do R0 existir |
| Require conversation resolution | ✅ | resolver comentários antes do merge |
| Require signed commits | ⬜ | evita setup de assinatura agora |
| Require linear history | ✅ | casa com squash merge |
| Require deployments to succeed | ⬜ | sem ambientes ainda |
| Lock branch | ⬜ | não tornar a branch somente-leitura |
| Do not allow bypassing the above settings | ✅ | regras valem até para admin (você) |
| Allow force pushes | ⬜ | proteger a `main` |
| Allow deletions | ⬜ | proteger a `main` |

### Pendências (voltar aqui depois)

- **Required status checks**: ligar **Require status checks to pass before merging** e selecionar os checks de CI (lint + testes) assim que o workflow do GitHub Actions do R0 rodar pela primeira vez (o nome do check só aparece depois disso).
- **Commits assinados** e **migração para Ruleset**: opcionais, sem data — entram como estudo se/quando fizer sentido.

---

## 2. Board no GitHub Projects

### Objetivo

Ter um kanban dedicado a este projeto, integrado às issues do repo, com colunas que refletem o fluxo SDD (`docs/process/processo-desenvolvimento-sdd.md`). O board **rastreia o trabalho** (Stories e subtasks como cards); a intenção (Épico) e o plano (Spec) moram nos `docs/`, não aqui.

### Conceito que destrava tudo (leia antes de clicar)

No GitHub Projects a "coluna" **não é uma entidade própria**. As colunas do board são **as opções de um campo único de seleção** — por padrão o campo **Status**. Arrastar um card de uma coluna pra outra **muda o valor desse campo**. Comparando com Jira: lá a coluna reflete um workflow de status com transições; aqui é mais simples — a coluna **é** o valor do campo Status. Portanto "criar/renomear coluna" significa "editar as opções do campo Status".

Detalhe que vai importar mais pra frente: cada opção de Status tem um **ID interno** que **não muda quando você renomeia** a opção. Qualquer automação (Workflow) que aponta pra uma opção continua apontando pra ela mesma depois do rename — só que agora sob o nome novo. Guarde isto; é a origem do bug clássico explicado na subseção de Workflows.

### Caminho feliz — criar o board

1. **Tipo de projeto.** No GitHub não existe mais "projeto preso a um repo" (o *Projects classic* foi descontinuado). Todo projeto pertence à sua **conta** (ou a uma organização) e se **dedica** a um repo pelo vínculo de itens. Então "um board só pra essa aplicação" = um projeto da sua conta, ligado ao `finance-system`. Tanto faz criar pelo seu perfil → aba **Projects** → **New project**, quanto pela aba **Projects** dentro do repo — o dono é a sua conta nos dois casos.
2. **Template e nome.** Escolha o template **Board**. Nome: `finance-system-board` (em inglês — é artefato de board).
3. **Import items from repository.** Selecione **Open issues**, from **finance-system**. **Não** escolha "Open pull requests" nem "both": PR não é unidade de planejamento (todo PR já se vincula à sua issue via `Closes #NNN`; PR como card separado só polui). Esse import é um **seed único**, não uma sincronização viva — se o repo ainda não tem issues, o board nasce vazio (que é o certo pra começar).
4. **Create project.** O board abre com o campo **Status** e colunas padrão (algo como `Todo / In Progress / Done`).

### As colunas (opções do campo Status)

Deixe as opções do Status **nesta ordem** (esquerda → direita; a ordem das opções = ordem das colunas). A `description` vai em inglês (artefato de board) e codifica as "portas" do fluxo:

| Coluna (Status) | Cor | Description (cole no campo) |
|---|---|---|
| `Backlog` | cinza | `Captured but not refined yet — missing objective, acceptance criteria, or Spec. Not ready to be worked on.` |
| `Ready To Start` | amarelo | `Story has an objective, acceptance criteria, and a written Spec. Ready to be picked up.` |
| `In Progress` | azul | `Actively in development — branch open, implementation and tests underway.` |
| `In Review` | roxo | `PR open and under review — CI green and checked against the Spec before merge.` |
| `Done` | verde | `PR merged, tests passing, and docs updated if needed.` |

As duas "portas" que importam: o que separa **Backlog** de **Ready To Start** é a **Spec existir** (definition of ready); o que separa **In Review** de **Done** é o **PR mergeado com CI verde + verificação contra a Spec** (definition of done).

**Como editar uma coluna.** No cabeçalho da coluna, **⋯** → **Edit details** (renomeia, muda cor e description). Pra adicionar: role até a direita das colunas e clique em **+ New column** (cria uma nova opção de Status). Pra apagar sobra: **⋯** → **Delete**. Pra reordenar: arraste o cabeçalho. (Alternativa, tudo num lugar só: **⋯** do topo direito → **Settings** → campo **Status**.)

**Default status.** Uma das opções fica marcada como **Default** (é a que todo item novo recebe ao entrar no board). O esperado é o **Backlog** ser o default. Se você renomeou a opção que já era default (`Todo` → `Backlog`), o "ser default" segue junto — então normalmente já estará certo. Confira em **Settings** → campo **Status**.

**Pegadinha do rename (importante).** Como cada opção tem um ID interno, **renomear** uma opção que automações referenciam **reaponta as automações em silêncio** pra essa opção (agora com outro nome). Se algum dia você renomear colunas, **revise os Workflows depois** (subseção adiante) — ou prefira **criar opções novas e apagar as antigas** em vez de renomear as que os Workflows usam.

### Labels

**Por que labels (e não Issue Types).** O jeito "tipado" de marcar Story/Bug/Task seria o **Issue Types**, mas ele é **exclusivo de organização** — em repo de conta pessoal **não existe**. Por isso usamos **labels** com convenção de nome.

**Entenda o nome da label.** Uma label é **um único campo de texto** (o "name"). **Não** existe "chave e valor" de verdade. `type: story` é **o nome inteiro** (com os dois-pontos e o espaço inclusos). O prefixo `type:` / `area:` é só **convenção visual** pra você ler agrupado e filtrar fácil — o GitHub trata como texto puro. (Analogia: é como uma constante `TYPE_STORY` — parece estruturada, mas é só um identificador string.)

**Onde editar.** Repo → **Issues** → botão **Labels**; ou direto na URL `github.com/<seu-usuário>/finance-system/labels`. (O "Edit labels" que aparece ao criar uma issue leva à mesma tela, mas é fácil de perder — prefira o caminho fixo.)

**O conjunto (enxuto — YAGNI).** Apague os defaults de triagem open-source que não servem ao fluxo solo: `duplicate`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix` e `enhancement` (num greenfield tudo é enhancement → vira ruído). Mantenha/crie:

| Label (name exato) | Cor (hex) | Description |
|---|---|---|
| `type: story` | `#5319E7` | `Vertical slice of user value (INVEST). Parent issue, broken down into subtasks.` |
| `type: subtask` | `#1D76DB` | `Sub-issue under a Story. Usually a backend or frontend slice.` |
| `area: backend` | `#0E8A16` | `Work in api/ (FastAPI core).` |
| `area: frontend` | `#FBCA04` | `Work in web/ (React front).` |
| `bug` | `#D73A4A` | `Something isn't working.` |

Acrescente `area: infra`, `area: docs`, prioridade etc. **só quando a necessidade aparecer** — nada de zoológico de labels antes da hora. O Claude Code aplica essas labels sozinho via `gh issue create --label ...` ao decompor a Spec.

**Cor.** Clique no input de cor e escolha um swatch padrão (caminho mais fácil) ou cole o hex (ex.: `#5319e7`).

### Hierarquia: Story × subtask

A relação Story → subtask é **nativa** (sub-issues): uma **Story** é a issue-pai; uma **subtask** é a sub-issue filha (até 100 sub-issues por pai, 8 níveis). Você cria a sub-issue dentro da própria issue (no fim da descrição, **Create sub-issue**); com o Workflow "Auto-add sub-issues" ligado, ela entra no board sozinha. A distinção Story/subtask é **estrutural** (pai vs. filho) — a label `type:` é só pra leitura rápida e filtro.

### Campos exibidos no card

Em **Settings** → seção de campos (ou no menu da view → **Fields**), deixe visíveis:

- **Title** (obrigatório), **Status** (campo das colunas), **Assignees** (o "quem-fez-o-quê" sai daqui; o Claude Code seta nas subtasks), **Linked pull requests** (amarra issue ↔ PR), **Sub-issues progress** (mostra X/Y subtasks concluídas na Story).
- **Habilite também:** **Labels** (pra ver/filtrar as labels no card) e **Parent issue** (pra agrupar/filtrar subtasks pela Story-pai).
- **Deixe pra depois** um campo de **Release/Milestone** — quando R0 e R1 coexistirem; hoje o prefixo numérico no título já resolve.

### Filtros úteis (não aparece tudo sempre — dá pra filtrar)

O jeito **mais fácil** é filtrar **por label**:
- Só Stories: `label:"type: story"`.
- Só subtasks: `label:"type: subtask"`.

Filtros nativos de hierarquia (complemento):
- `has:parent-issue` → só sub-issues (subtasks).
- `has:sub-issues-progress` → só issues-pai (Stories que já têm subtasks).
- Subtasks de **uma** Story específica: campo **Parent issue**, ou `parent-issue:<seu-usuário>/finance-system#<N>`.
- Toggle **Show hierarchy** (menu da view) aninha pai→filho. Com a hierarquia **ligada**, sub-issues aparecem mesmo sem casar com o filtro; pra ver uma **lista plana filtrada**, **desligue** o Show hierarchy e aplique o filtro.
- Salve **múltiplas views** (ex.: "Board" kanban por Status; "Subtasks abertas"; futuramente uma por release).

### Workflows (automações embutidas)

Todo Project vem com o **mesmo conjunto** de workflows built-in; a maioria nasce **desligada**, algumas ligadas. Você **não cria nada** — só garante que as ligadas apontem pros status certos. Estes devem ficar **ligados**, com **estes alvos**:

| Workflow | Gatilho → Ação |
|---|---|
| Auto-add sub-issues to project | item tem sub-issues → adiciona as sub-issues ao board |
| Auto-add to project | filtro `finance-system` + `is:issue is:open` → adiciona o item |
| Auto-close issue | Status vira **Done** → fecha a issue |
| Item added to project | item adicionado → Status: **Backlog** |
| Item closed | item fechado → Status: **Done** |
| Pull request linked to issue | PR linkado à issue → Status: **In Progress** |
| Pull request merged | PR mergeado → Status: **Done** |

Os demais (~4: auto-archive etc.) ficam **desligados** — ligamos sob demanda.

**O bug clássico (e como consertar).** Quando você renomeia uma opção de Status, o ID dela não muda, então **os workflows que apontavam pra ela continuam apontando** — agora pro nome novo. Sintoma real que tivemos: depois de renomear a antiga opção "Done" pra "In Progress", arrastar um card pra "In Progress" **fechava** a issue (o "Auto-close" ainda enxergava aquilo como o Done original); e "Item closed" / "PR merged" passaram a mandar o status pro lugar errado; e "Pull request linked to issue" ficou apontando pra "Ready To Start" (a antiga "In Progress" renomeada). **Correção:** **Settings** → **Workflows**, abra cada workflow afetado e **reaponte o status** (gatilho e/ou alvo) pra opção correta — `Auto-close` → **Done**; `Item closed` → **Done**; `PR merged` → **Done**; `PR linked to issue` → **In Progress**.

**Por que abrir um PR não duplica nada.** O **Auto-add to project** só pega **`is:issue`**, então **PR não vira card** — ele aparece dentro do card da issue, no campo **Linked pull requests**. Os workflows de PR (linked/merged) **agem sobre o card da issue que já existe**, não criam card novo. E os workflows não entram em loop entre si: fechar→Done, Done→fechar e merge→Done são **idempotentes** (se já está no estado, é no-op); o GitHub converge e para.

### Gotchas gerais de issues (pra não te pegar)

- **Issue "sumida".** A aba **Issues** abre com o filtro `is:issue state:open`, que **esconde as fechadas**. Pra achar/gerenciar fechadas, limpe o filtro ou use `is:closed`.
- **Número de issue não reseta.** Os números de issue/PR são **monotônicos por repositório e nunca reaproveitados** — apagar uma issue **não** libera o número. O único jeito de voltar pro `#1` é criar um repo novo (não vale a pena). É a mesma regra dos ADRs (numeração monotônica, nunca reutilizada): a primeira Story real pode ser `#7` em vez de `#1`, e tudo bem.

---

## 3. Operar o board via gh CLI (e por que não MCP agora)

> Esta seção é o **registro do experimento**: como deixei o Claude Code apto a mexer no board, com os comandos que validei. O procedimento **canônico** que o workflow do projeto consome mora em `docs/process/operar-board.md` — esta seção é a versão "diário", autocontida.

### Por que gh CLI e não MCP (por enquanto)

O Claude Code mexe no board rodando `gh`/`git` no terminal — os mesmos comandos que eu digitaria. Isso **não** é MCP. MCP (Model Context Protocol) seria um servidor expondo "tools" tipadas (`create_issue`, etc.) que o modelo chama de forma estruturada. Optei pelo `gh` CLI agora porque: já preciso do `gh` de qualquer forma (git/PR), o `gh auth` gerencia o próprio token (não exijo uma PAT de longa duração pra guardar), e os prompts de ação já assumem "via gh CLI". O **servidor MCP do GitHub** fica como estudo futuro — hoje ele exige PAT (o OAuth pro servidor remoto ainda não é suportado por todos os clientes Claude) e a cobertura de Projects v2 é parcial, então não eliminaria o GraphQL/CLI pro board. Resumo: `gh` resolve com menos peças; MCP vira uma sessão dedicada de aprendizado depois.

### Pré-requisito: gh instalado e autenticado (Ubuntu/WSL2)

Instale pelo repositório APT oficial (mais novo que o pacote padrão do Ubuntu; não use a versão Snap — sandboxing atrapalha SSH/git no WSL):

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
&& sudo mkdir -p -m 755 /etc/apt/keyrings \
&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
   | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```

Depois autentique e confira os scopes:

```bash
gh auth login        # GitHub.com → HTTPS → "Login with a web browser"
gh auth status
```

No WSL, se o browser não abrir sozinho, copie a URL exibida pro navegador do Windows e cole o código.

**Scopes do token:** criar issue e linkar sub-issue precisam só de **`repo`**. **Ler o board** (status/coluna) exige **`read:project`** — sem ele, `gh project ...` e queries `projectV2` dão `INSUFFICIENT_SCOPES` e `projectItems` volta vazio. Adicione (interativo, abre browser):

```bash
gh auth refresh -h github.com -s read:project
```

### Exemplo validado: criar Story, subtask e conectá-las

Lembrando o princípio: os Workflows do board adicionam a issue e setam `Backlog` sozinhos — aqui a gente **só cria e linka**.

```bash
# Criar Story
STORY_URL=$(gh issue create \
  --repo jorgekamezawa/finance-system \
  --title "R0: walking skeleton (TESTE)" \
  --body "Issue de validação do fluxo de board." \
  --label "type: story" \
  --assignee "@me")
STORY_NUM=$(echo "$STORY_URL" | grep -oE '[0-9]+$')

# Criar Subtask (múltiplos --label, um por flag — NUNCA vírgula numa string só)
SUBTASK_URL=$(gh issue create \
  --repo jorgekamezawa/finance-system \
  --title "R0: esqueleto backend (TESTE)" \
  --body "Subtask de validação." \
  --label "type: subtask" \
  --label "area: backend" \
  --assignee "@me")
SUBTASK_NUM=$(echo "$SUBTASK_URL" | grep -oE '[0-9]+$')

# Node IDs (o vínculo usa ID, não número)
STORY_ID=$(gh issue view "$STORY_NUM" --repo jorgekamezawa/finance-system --json id --jq '.id')
SUBTASK_ID=$(gh issue view "$SUBTASK_NUM" --repo jorgekamezawa/finance-system --json id --jq '.id')

# Linkar subtask como sub-issue da Story (GraphQL — o gh não faz nativo)
gh api graphql -f query="
mutation {
  addSubIssue(input: { issueId: \"$STORY_ID\", subIssueId: \"$SUBTASK_ID\" }) {
    issue { number title }
    subIssue { number title }
  }
}"
```

### Verificação

```bash
# Label e assignee (gh expõe direto)
gh issue view "$STORY_NUM" --repo jorgekamezawa/finance-system --json title,labels,assignees

# Sub-issues e pai — só via GraphQL (gh issue view não expõe esses campos)
gh api graphql -f query='
query { repository(owner: "jorgekamezawa", name: "finance-system") {
  issue(number: 24) { title subIssues(first: 50) { totalCount nodes { number title } } }
}}'

# Status no board — precisa de read:project
gh project item-list <project_number> --owner jorgekamezawa --format json
```

### O que não funciona (e o workaround)

- `gh issue view --json subIssues` / `--json parent`: **não existem** no CLI → use as queries GraphQL acima.
- `gh issue view --json projectCards`: erro de Projects classic (depreciado) → não usar.
- Qualquer leitura de board sem `read:project`: bloqueada → adicione o scope.

### Limpeza das issues de teste

```bash
gh issue delete <num> --repo jorgekamezawa/finance-system --yes
```

Lembrete: o número **não** reseta ao apagar (monotônico, igual à regra dos ADRs) — a próxima issue continua do contador.
