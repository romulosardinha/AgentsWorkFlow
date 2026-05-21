---
description: Revisa o arquivo apontando problemas, sem modificar nada
argument-hint: <caminho-do-arquivo>
---

Use o subagente `code-reviewer` para analisar `$1` e reportar todos os problemas encontrados.

**Não modifique o arquivo.** Não chame `code-fixer`. Apenas mostre o relatório do reviewer.

Se o usuário quiser aplicar as correções depois, ele rodará `/quality-check $1`.
