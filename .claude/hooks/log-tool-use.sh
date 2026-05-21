#!/usr/bin/env bash
# PostToolUse hook — registra cada Edit/Write/MultiEdit em .claude/logs/edits.log
#
# Recebe JSON via stdin no formato:
#   { "tool_name": "Edit", "tool_input": { "file_path": "...", ... }, ... }
#
# Saída: nenhuma (vazia = sucesso silencioso). Logging puro, não bloqueia o tool call.

set -euo pipefail

LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/edits.log"

mkdir -p "$LOG_DIR"

INPUT=$(cat)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if command -v jq >/dev/null 2>&1; then
  TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"')
  FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // "unknown"')
else
  TOOL="unknown(no-jq)"
  FILE="unknown(no-jq)"
fi

printf '[%s] %s %s\n' "$TS" "$TOOL" "$FILE" >> "$LOG_FILE"

exit 0
