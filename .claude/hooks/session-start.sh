#!/usr/bin/env bash
# SessionStart hook — injeta um lembrete com os comandos disponíveis.
#
# Resposta deve ser JSON com hookSpecificOutput.additionalContext
# que será adicionado ao contexto do Claude.

set -euo pipefail

CONTEXT=$(cat <<'EOF'
[AgentsWorkFlow] Workflow multi-agente carregado.

Comandos disponíveis:
  /quality-check <arquivo>   pipeline: code-reviewer → code-fixer → test-runner
  /review <arquivo>          só revisa, não modifica
  /explain <arquivo>         explica em português
  /document <arquivo>        adiciona docstrings via docs-writer

Subagentes em .claude/agents/, hooks em .claude/hooks/.
Exemplos pra praticar em examples/.
EOF
)

# Escapa pra JSON e responde
if command -v jq >/dev/null 2>&1; then
  jq -n --arg ctx "$CONTEXT" '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $ctx
    }
  }'
else
  # Fallback sem jq — escape manual mínimo
  ESCAPED=$(printf '%s' "$CONTEXT" | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}')
  printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$ESCAPED"
fi

exit 0
