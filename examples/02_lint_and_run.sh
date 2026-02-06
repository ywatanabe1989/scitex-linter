#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/02_lint_and_run.sh
# Usage: bash examples/02_lint_and_run.sh
#
# Demonstrates: scitex-linter python command (lint then execute)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Example 02: Lint and Run ==="

# Lint then execute a clean script
echo
echo "--- Lint + execute clean script ---"
scitex-linter python "$SCRIPT_DIR/sample_clean.py" || true

# Strict mode blocks on errors
echo
echo "--- Strict mode (blocks on errors) ---"
scitex-linter python "$SCRIPT_DIR/sample_bad.py" --strict || true

# EOF
