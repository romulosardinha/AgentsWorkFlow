---
description: Pipeline completo de qualidade — revisa, corrige e testa, iterando até passar
argument-hint: <caminho-do-arquivo>
---

Execute o pipeline de qualidade no arquivo: **$1**

O pipeline executa em **ciclos** de três fases (revisão → correção → validação). Repita o ciclo até que os testes passem totalmente ou um dos critérios de parada seja atingido.

**Limite:** no máximo **10 ciclos**. Cada ciclo é caro (aciona quantos subagentes forem necessários).

## Em cada ciclo

### Fase 1 — Revisão
Use o subagente `code-reviewer` para analisar `$1`.

A partir do **ciclo 2**, inclua no prompt do reviewer o relatório de falhas do `test-runner` do ciclo anterior, para que ele saiba o que ainda está quebrado.

Se o reviewer não encontrar nada **e** os testes do ciclo anterior passaram, encerre reportando: `Arquivo $1 está limpo. Pipeline encerrado.`

### Fase 2 — Correção
Passe a lista do reviewer ao `code-fixer` junto com o caminho `$1`. Faça a triagem antes de delegar: marque explicitamente quais itens aplicar e quais pular (com justificativa). Itens que são preferência estilística sobre código que já funciona devem ser pulados por padrão.

### Fase 3 — Validação
Use o `test-runner` apontando para `$1`. Capture status final (PASS/FAIL) e mensagens de falha.

## Critérios de parada (verifique após Fase 3)

Pare e imprima o resumo final quando **qualquer** uma destas condições for verdadeira:

1. **Sucesso:** todos os testes passam.
2. **Limite:** já completou 10 ciclos.
3. **Estagnação:** a lista de problemas do reviewer neste ciclo é essencialmente a mesma do ciclo anterior (mesmo arquivo, mesmas linhas) — indica que o fixer não consegue progredir e iterar mais é desperdício.
4. **Sem testes:** o `test-runner` não encontrou arquivo de teste correspondente — reporte e pare (não tem como validar).

Se nenhuma condição foi atingida, **inicie o próximo ciclo** voltando à Fase 1.

## Resumo final

Ao parar, imprima:

```
## Pipeline de qualidade — $1

- Ciclos executados: C de 10
- Problemas identificados (último ciclo): N
- Correções aplicadas (último ciclo): M (P puladas)
- Testes: X/Y passando — <PASS|FAIL>
- Motivo da parada: <sucesso | limite | estagnação | sem testes>

Próximos passos: <opcional, se algo ficou pendente>
```

## Regras

- Não invoque os subagentes em paralelo — cada fase depende da anterior.
- Não tente "ajudar" o reviewer fazendo edições no meio. O pipeline existe justamente pra separar responsabilidades.
- Não exceda 10 ciclos mesmo que pareça promissor — pare e reporte para o usuário decidir.
