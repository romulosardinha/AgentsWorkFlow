---
description: Descobre arquivos não comitados via change-scout e roda review + fix em cada um (test-runner só nos .py)
---

Pipeline de revisão sobre todas as mudanças não comitadas do repositório. Você não recebe um caminho — você descobre os arquivos via o subagente `change-scout` e itera.

## Fase 0 — Triagem

Use o subagente `change-scout` para listar e classificar as mudanças não comitadas.

Casos de saída antecipada:
- Se o scout responder `Nenhuma mudança não comitada encontrada.` — imprima isso e encerre.
- Se responder `Nada que valha revisar.` — repasse a lista de ignorados e encerre.

Caso contrário, extraia do relatório do scout duas listas:
- **PY** — arquivos em "Revisar (Python)"
- **OUTROS** — arquivos em "Revisar (outro)"

## Fase 1 — Loop por arquivo

Para **cada** arquivo em `PY ∪ OUTROS`, execute, na ordem:

1. **Revisão** — invoque `code-reviewer` passando o caminho do arquivo. Capture o relatório.
2. **Correção** — se o reviewer apontou problemas, invoque `code-fixer` passando o caminho **e** o relatório do reviewer. Faça triagem antes: marque itens a aplicar vs. pular (preferências estilísticas sobre código que já funciona devem ser puladas por padrão). Se o reviewer não apontou nada, pule esta etapa.
3. **Testes** — **somente se o arquivo estiver em `PY`**, invoque `test-runner` apontando para ele. Para arquivos em `OUTROS`, pule esta etapa.

Faça **uma passada por arquivo** — não itere ciclos como o `/quality-check`. Se o usuário quiser iterar em um arquivo específico depois, ele roda `/quality-check <arquivo>`.

Processe os arquivos **sequencialmente**, não em paralelo — facilita ler os logs e evita corridas se dois arquivos compartilharem dependências.

## Resumo final

Ao terminar todos os arquivos, imprima:

```
## Code review de mudanças não comitadas

Arquivos processados: N (P Python, O outros)
Arquivos ignorados pelo scout: K

Por arquivo:
- `caminho/a.py` — R problemas / F corrigidos / testes: <PASS|FAIL|sem-teste>
- `caminho/b.md` — R problemas / F corrigidos / testes: n/a
- ...

Próximos passos:
<liste arquivos que falharam testes ou ficaram com problemas não corrigidos>
```

## Regras

- Não pule a Fase 0. A lista de arquivos vem **sempre** do scout — não invente a partir de `git status` direto.
- Não invoque os subagentes em paralelo dentro do mesmo arquivo (review → fix → test é sequencial).
- Não chame `test-runner` em arquivos não-Python — ele só sabe rodar `pytest`.
- Se um subagente falhar (erro de ferramenta, timeout), registre no resumo e siga para o próximo arquivo — não trave o pipeline inteiro por um arquivo problemático.
