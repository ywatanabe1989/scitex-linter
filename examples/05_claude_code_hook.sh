#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/05_claude_code_hook.sh
# Usage: Copy this to ~/.claude/to_claude/hooks/post-tool-use/
#
# Minimal Claude Code post-tool-use hook for SciTeX Linter.
# When Claude writes or edits a .py file, this hook runs scitex-linter
# to enforce SciTeX patterns. Errors block Claude (exit 2).
#
# Full version: https://github.com/ywatanabe1989/scitex-linter/blob/main/examples/05_claude_code_hook.sh

set -euo pipefail

# Read hook input JSON from stdin
INPUT=$(cat)

# Extract file_path from hook input
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', '') or '')
" 2>/dev/null || echo "")

# Skip if no file or not Python
[ -n "$FILE_PATH" ] || exit 0
[ -f "$FILE_PATH" ] || exit 0
case "$FILE_PATH" in *.py) ;; *) exit 0 ;; esac

# Find the linter command
STX_LINT=""
if command -v scitex-linter &>/dev/null; then
    STX_LINT="scitex-linter"
elif command -v scitex &>/dev/null && scitex linter --help &>/dev/null; then
    STX_LINT="scitex linter"
fi

# Run linter if available
if [ -n "$STX_LINT" ]; then
    # Errors block Claude (exit 2)
    $STX_LINT check "$FILE_PATH" --severity error --no-color >&2 || exit 2
    # Warnings shown but don't block
    $STX_LINT check "$FILE_PATH" --severity warning --no-color >&2 || true
fi

# Standard Python linting (optional)
if command -v ruff &>/dev/null; then
    ruff check --fix "$FILE_PATH" 2>&1 || exit 2
fi

exit 0

# EOF
