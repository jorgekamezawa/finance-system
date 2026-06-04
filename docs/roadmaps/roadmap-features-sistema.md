# Roadmap de Features — Sistema de Finanças

**Projeto:** sistema de finanças pessoais (substituir a planilha + crescer com IA).
**Foco deste documento:** **as features e a ordem de entrega** (o "o quê" e o "quando"). O "como" (implementação detalhada) fica pra cada release.
**Documento irmão:** `roadmap-infra-devops.md` (a infra que sustenta tudo isso).

## Princípio de sequenciamento

Cada release é ordenado por três forças ao mesmo tempo:
- **Tech Lead:** cada release fininho e **no ar** (mesma filosofia do roadmap de infra).
- **PM:** cada release entrega **valor** que justifique existir.
- **Aprendizado:** cada release cobre uma **skill nova de propósito** (Python, React, IA, etc.) — porque o sistema também é seu veículo de evolução técnica.

> Como usar: faça em ordem; cada release deve ficar no ar antes do próximo. Marque conforme conclui. As inserções flexíveis no fim podem entrar entre releases sem quebrar a sequência.

## Decisões fechadas (sementes de ADR)

1. **Core em Python (FastAPI)** desde o R0 — para praticar Python desde o início e ficar coeso com a IA. **Kotlin** reentra como o **serviço de auth/sessão** (R8), o "continuo forte no meu forte".
2. **Import do histórico vem depois dos dashboards** (o painel fica mais útil já com histórico dentro).
3. **Foto da NF vem antes da integração bancária** (mais simples e destrava o nível de item).
4. **v1 é single-user, sem auth real** — proteção mínima no começo; auth gerenciado quando precisar; auth próprio no R8.
5. **Agregados (totais, médias, saldo, % da receita) são sempre calculados, nunca armazenados** — por isso a aba de média quebrada da planilha é irrelevante pro sistema.

---

## R0 — Esqueleto no ar (walking skeleton)
**Objetivo:** ter o end-to-end deployado fazendo quase nada, mas funcionando.
**Escopo:** CRUD mínimo de transação (data, descrição, valor, categoria) + uma listagem. Core em FastAPI, front em React, banco Postgres, tudo no ar.
**Valor:** ~nenhum (é fundação). **Aprende:** o end-to-end + pipeline. **Casa com:** Nível 0 da infra.
**Tensão PM×TL:** PM odeia "subir o nada"; TL insiste no esqueleto. Resolvido limitando a ~1-2 semanas.

## R1 — Substituir a planilha (MVP de verdade)
**Objetivo:** você para de usar a planilha daqui pra frente.
**Escopo:**
- CRUD completo de transações com as ~20 categorias nas duas faixas.
- Lançamento de receitas (Salário, VA, etc.).
- Visão mensal agrupada por categoria.
- Cálculos da planilha: total por categoria, % da receita, saldo, **meta vs. realizado** (os "Objetivos de gasto").
- Filtro por mês/ano; campo de parcelamento e flag "precisa estorno" (vistos nos seus dados).

**Valor:** altíssimo — depois daqui você **vive no app**. É o "definition of done" de substituir a planilha.
**Aprende:** consolida o CRUD, modelagem e o front básico.

## R2 — Visão e tendências (dashboards)
**Objetivo:** o que a aba "Média dos Gastos" fazia, e melhor.
**Escopo:** média por categoria, média dos últimos 3 meses, evolução mês a mês, gráfico de meta vs. realizado, quebra por categoria.
**Valor:** médio-alto — primeiro momento "melhor que a planilha".
**Aprende:** React pra valer (gráficos/visualização).

## R3 — Importar o histórico (backfill)
**Objetivo:** carregar 2025/2026 pra alimentar as tendências.
**Escopo:** importador que lê o layout da planilha → transações, com tela de **preview/confirmar** antes de gravar. Um único importador cobre os dois anos (estrutura é consistente).
**Valor:** médio — enriquece o R2 com histórico real.
**Aprende:** ETL/normalização de dados (e bom uso de IA pra mapear).
**Depende de:** modelo de dados do R1 estável. **Posição:** depois do R2 (decisão fechada).

## R4 — Primeira IA: planejamento financeiro
**Objetivo:** primeira integração com IA (valor + sinal pro mercado).
**Escopo:** a partir dos dados do mês, a IA gera análise + sugestões ("estourou Mercado, dá pra cortar aqui"). Pode ser um módulo no core ou um primeiro serviço de IA separado (decisão de implementação depois — ambos em Python).
**Valor:** alta diferenciação. **Aprende:** integração com LLM, prompt, custo/limites.

## R5 — Pergunte às suas finanças: RAG + chatbot
**Objetivo:** consulta conversacional aos seus próprios dados.
**Escopo:** chatbot que responde via **RAG** ("quanto gastei com Mercado em abril?", "qual minha média de Carro?").
**Valor:** médio-alto. **Aprende:** RAG. **Depende de:** a base de IA do R4.

## R6 — Foto da nota fiscal (visão + nível de item)
**Objetivo:** matar a digitação manual e destravar análise por item.
**Escopo:** tira/sobe foto da NF → modelo de visão extrai os itens → cria lançamentos detalhados.
**Valor:** alto — remove sua maior dor (lançar tudo na mão).
**Aprende:** IA de visão, parsing estruturado. **Posição:** antes da integração bancária (decisão fechada).

## R7 — Comparação de preços (single-user)
**Objetivo:** sua ideia de economizar no mercado, versão pessoal.
**Escopo:** histórico de preço por item e por mercado a partir das suas NFs; "onde X costuma estar mais barato".
**Valor:** médio. **Depende de:** o nível de item do R6.
**Nota:** a versão **regional/com dados de várias pessoas** é efeito de rede — fica como Norte de longo prazo (e exige multiusuário, R8).

## R8 — Login próprio + multiusuário
**Objetivo:** o serviço de auth/sessão que você quer construir, e a porta pro multiusuário.
**Escopo:** serviço dedicado de autenticação e sessão — o **momento Kotlin** (sua praia do BTG: Spring Security, Gateway, sessão no Redis). Substitui o auth gerenciado usado até aqui.
**Valor:** alto como aprendizado/portfólio; pré-requisito pras features sociais/regionais.
**Aprende:** auth do zero, arquitetura multi-serviço e multi-linguagem — onde a observabilidade/tracing distribuído passa a brilhar.

---

## Inserções flexíveis (entram entre releases)

- **Projetos/Envelopes** (as abas "Mobiliar Apto" / "Praia Fim de Ano"): sub-controle com orçamento próprio pra um objetivo. Uma transação ganha um `projeto_id` opcional. Encaixe natural perto do R2-R3.
- **Import de CSV**: substituto barato da integração bancária (todo banco exporta extrato). Pode entrar junto do R3.
- **Integração bancária (Open Finance via Pluggy/Belvo)**: épico **opcional** a partir do R6+. Alto valor (sincroniza transações automaticamente), mas alta complexidade (agregador, consentimento, sandbox). Lembrar: é **sincronização periódica**, não interceptação em tempo real da compra.

## Norte de longo prazo (fora do roadmap por enquanto)

- **Comparação de preços regional** com dados de vários usuários (efeito de rede) — depende de multiusuário (R8) e de massa de dados.
- **App Android nativo** — o padrão será web responsivo/PWA; Android nativo fica como sonho de stretch.

---

## Apêndice — modelo de dados base (extraído da planilha)

Só pra ancorar o R1 (o esquema detalhado vem na hora de implementar):

- **transação:** data, descrição, valor (negativo = estorno/crédito), categoria, tipo (receita/despesa), mês, ano; opcionais: parcelamento, forma de pagamento (Pix/cartão/VA), `precisa_estorno`/dividido com quem, `projeto_id` (futuro), notas.
- **categoria:** nome, faixa (1 ou 2), **meta de gasto**.
- **receita:** mês, ano, fonte (Salário/VA/Lívia), valor.
- **agregados:** sempre calculados (totais, médias, média 3 meses, % da receita, saldo).
- **futuro:** itens da NF (nível de item), preço por mercado, usuário/multiusuário.

Categorias mapeadas (duas faixas): Itens para casa, Streaming, Mensal, Contas da Casa, Mercado, Transporte, Mãe, Carro, Presentes · Milhas, Estudos, Perfumaria, Farmácia, Pets, Extra, Comida/Rolê, Mensal Lívia, Não Sei, Viagem, Precisa de Estorno.
