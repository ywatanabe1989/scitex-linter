#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/00_run_all.sh
# Usage: bash examples/00_run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== SciTeX Linter Examples ==="
echo

bash "$SCRIPT_DIR/01_lint_files.sh"
echo
bash "$SCRIPT_DIR/02_lint_and_run.sh"
echo
bash "$SCRIPT_DIR/03_list_rules.sh"
echo
bash "$SCRIPT_DIR/04_mcp_tools.sh"

echo
echo "=== All examples completed ==="

# EOF
