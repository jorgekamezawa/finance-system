# Prompt — Verificar contra a Spec (Claude Code)

> Roda no Claude Code. Apoio ao seu **Verify**: confere a implementação contra a Spec, sem alterar nada. Cole o bloco abaixo, trocando `<spec>`.

```text
Aja como revisor (Tech Lead) do projeto Sistema de Finanças.
Compare a implementação atual com a Spec @docs/specs/<spec>.md e me dê os achados. NÃO altere código — isto é apoio ao meu Verify; a decisão é minha.
- Cada critério de aceite (EARS) tem teste correspondente? Quais faltam?
- As linhas da tabela de exemplos viraram casos de teste?
- Há desvio entre o construído e o que a Spec define (contratos, modelo de dados, NFRs)?
- Algum teste foi enfraquecido ou removido pra "fazer passar"? Isso é inegociável — sinalize na hora.
```
