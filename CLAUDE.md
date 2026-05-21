# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre o projeto

**AgentsWorkFlow** é um projeto-laboratório para aprender workflows multi-agente no Claude Code. Não tem stack de produção — o "produto" são os próprios artefatos em `.claude/`: subagentes, slash commands e hooks que orquestram um pipeline de qualidade de código Python.

Use os arquivos em `examples/` como playground. Eles contêm bugs e código bagunçado de propósito.

## Arquitetura do workflow

O fluxo principal é o **pipeline de qualidade**, acionado por `/quality-check <arquivo>`. Ele encadeia três subagentes e **itera** até os testes passarem (máx 10 ciclos):

```
/quality-check arquivo.py
    │
    ├── ciclo N (até 10):
    │     ├── code-reviewer    (Read, Grep, Glob, Bash)    → lista problemas
    │     ├── code-fixer       (Read, Edit, Write)         → aplica correções
    │     └── test-runner      (Read, Bash)                → valida com pytest
    │
    └── para quando: testes passam | 10 ciclos | lista estagnou | sem teste
```

A partir do ciclo 2, o reviewer recebe o output das falhas do ciclo anterior pra focar no que ainda quebra.

Princípios que regem essa estrutura — e que você deve preservar ao mexer:

1. **Cada subagente tem ferramentas mínimas.** O `code-reviewer` não tem `Edit` de propósito: revisão e correção são fases separadas pra que a revisão não "consert" sem deixar rastro. Se você der `Edit` ao reviewer, o pipeline perde a auditabilidade.
2. **O orquestrador (slash command) é burro de propósito.** Ele só chama os subagentes na ordem certa. Toda a inteligência fica nos prompts dos agentes — é mais fácil iterar.
3. **Hooks são observabilidade, não lógica.** `.claude/hooks/log-tool-use.sh` registra toda escrita em `.claude/logs/edits.log`. Não use hooks pra modificar o comportamento do pipeline; use-os pra observar.

## Comandos disponíveis (slash commands)

| Comando | O que faz |
|---------|-----------|
| `/quality-check <arquivo>` | Pipeline completo: revisa → corrige → testa. Itera até passar (máx 10 ciclos). |
| `/review <arquivo>` | Só revisa, não modifica nada |
| `/explain <arquivo>` | Explica o código em português, sem mexer |
| `/document <arquivo>` | Adiciona docstrings via `docs-writer` |

Definições em [.claude/commands/](.claude/commands/). Comandos recebem argumentos via `$1`, `$2`, ou `$ARGUMENTS` (string completa).

## Subagentes disponíveis

Definições em [.claude/agents/](.claude/agents/). Frontmatter YAML especifica `name`, `description` (usado pra delegação automática) e `tools` (lista de ferramentas permitidas). Corpo do `.md` é o system prompt do agente.

| Agente | Ferramentas | Quando usar |
|--------|-------------|-------------|
| `code-reviewer` | Read, Grep, Glob, Bash | Antes de mudar qualquer arquivo Python |
| `code-fixer` | Read, Edit, Write | Pra aplicar correções já identificadas |
| `test-runner` | Read, Bash | Pra validar mudanças com pytest |
| `docs-writer` | Read, Edit | Pra adicionar docstrings sem mexer em lógica |

## Hooks configurados

Veja [.claude/settings.json](.claude/settings.json).

- **PostToolUse** (matcher `Edit|Write|MultiEdit`) → `.claude/hooks/log-tool-use.sh` registra cada edição em `.claude/logs/edits.log` com timestamp, tool e arquivo. Útil pra depois ver "o que o pipeline tocou na última execução".
- **SessionStart** → `.claude/hooks/session-start.sh` injeta contexto curto lembrando os comandos disponíveis.

Hooks rodam como shell scripts independentes — eles leem JSON do stdin e podem responder com JSON no stdout. Veja os scripts em `.claude/hooks/` pra entender o formato.

## Rodando os exemplos

Os arquivos em `examples/` são propositalmente problemáticos:

- [`buggy_calculator.py`](examples/buggy_calculator.py) — calculadora com 3 bugs (divisão por zero não tratada, off-by-one, tipo errado)
- [`test_buggy_calculator.py`](examples/test_buggy_calculator.py) — testes que pegam os bugs (rodando `pytest`, falham)
- [`messy_data.py`](examples/messy_data.py) — código funcional mas sem docstrings, com nomes ruins

Fluxo sugerido pra praticar:
```
/review examples/buggy_calculator.py       # vê o que reviewer aponta
/quality-check examples/buggy_calculator.py # pipeline completo
/document examples/messy_data.py            # docs-writer em ação
```

## Convenções ao estender

- **Novo subagente** → criar `.claude/agents/<nome>.md` com frontmatter. Mantenha o conjunto de `tools` mínimo possível.
- **Novo comando** → criar `.claude/commands/<nome>.md` com frontmatter (`description`, `argument-hint`). O corpo é o prompt que será expandido quando o usuário digitar `/<nome>`.
- **Novo hook** → adicione entrada em `.claude/settings.json` e script em `.claude/hooks/`. Torne o script `chmod +x`. Hooks lentos travam o Claude Code, então mantenha-os rápidos.

## O que NÃO existe aqui (e por quê)

- **Sem build, sem `package.json`, sem `requirements.txt`** — os exemplos em `examples/` usam só stdlib + pytest, que se assume instalado globalmente. Isso é proposital pra reduzir setup.
- **Sem CI** — este é um projeto de aprendizado local. Se quiser adicionar, comece por um workflow simples que rode `pytest examples/`.
