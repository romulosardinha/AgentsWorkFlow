# AgentsWorkFlow

Projeto-laboratório para aprender **workflows multi-agente** no Claude Code: subagentes, slash commands e hooks trabalhando juntos.

## Quickstart

Pré-requisitos: [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) instalado, Python 3.10+ com `pytest`.

```bash
cd AgentsWorkFlow
claude
```

Dentro do Claude Code, rode:

```
/review examples/buggy_calculator.py
```

Você vai ver o subagente `code-reviewer` ser disparado, analisar o arquivo e listar 3 bugs. Depois experimente o pipeline completo:

```
/quality-check examples/buggy_calculator.py
```

Agora `code-reviewer` → `code-fixer` → `test-runner` rodam em sequência. Os bugs são corrigidos e validados com `pytest`.

## O que tem aqui

```
.claude/
├── settings.json       # registra hooks
├── agents/             # 4 subagentes especialistas
├── commands/           # 4 slash commands
├── hooks/              # scripts de observabilidade
└── logs/               # PostToolUse loga aqui
examples/               # código com bugs/baguça pra praticar
CLAUDE.md               # contexto pro Claude Code
```

## Comandos

| Comando | Efeito |
|---|---|
| `/quality-check <arquivo>` | Pipeline completo: revisa → corrige → testa |
| `/review <arquivo>` | Só revisa, não modifica |
| `/explain <arquivo>` | Explica em português |
| `/document <arquivo>` | Adiciona docstrings |

## Como aprender com este projeto

1. **Leia um agente** em `.claude/agents/code-reviewer.md`. Veja como o frontmatter declara `tools` e como o prompt define a persona.
2. **Leia um comando** em `.claude/commands/quality-check.md`. Veja como ele orquestra múltiplos subagentes.
3. **Modifique algo pequeno.** Mude a lista de problemas que o `code-reviewer` procura. Rode `/review` de novo. Veja a diferença.
4. **Crie um subagente novo.** Por exemplo, `security-auditor.md` que procura `eval`, `exec`, SQL concatenado. Adicione um `/audit <arquivo>`.
5. **Olhe os logs.** Depois de um `/quality-check`, abra `.claude/logs/edits.log` e veja o rastro de quem editou o quê.

Detalhes de arquitetura: veja [CLAUDE.md](CLAUDE.md).
