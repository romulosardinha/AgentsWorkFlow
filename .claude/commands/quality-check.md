---
description: Pipeline completo de qualidade — revisa, corrige e testa o arquivo
argument-hint: <caminho-do-arquivo>
---

Execute o pipeline de qualidade no arquivo: **$1**

Siga estas fases **em ordem**, sem pular:

## Fase 1 — Revisão
Use o subagente `code-reviewer` para analisar `$1` e produzir uma lista numerada de problemas.

Se o reviewer não encontrar nada, encerre aqui reportando: `Arquivo $1 está limpo. Pipeline encerrado.`

## Fase 2 — Correção
Passe a lista produzida pelo reviewer ao subagente `code-fixer` junto com o caminho `$1`. Ele aplicará as correções e retornará um relatório.

## Fase 3 — Validação
Use o subagente `test-runner` apontando para `$1` (ele descobre o arquivo de teste correspondente).

## Resumo final

Ao terminar, imprima:

```
## Pipeline de qualidade — $1

- Problemas identificados: N
- Correções aplicadas: M (P puladas)
- Testes: X/Y passando

Próximos passos: <opcional, se algo ficou pendente>
```

Importante:
- Não invoque os subagentes em paralelo — cada fase depende da anterior.
- Não tente "ajudar" o reviewer fazendo edições no meio. O pipeline existe justamente pra separar responsabilidades.
