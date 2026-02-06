#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/01_lint_files.sh
# Usage: bash examples/01_lint_files.sh
#
# Demonstrates: scitex-linter lint command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Example 01: Lint Files ==="

# Lint a clean SciTeX script
echo
echo "--- Linting a clean script ---"
scitex-linter lint "$SCRIPT_DIR/sample_clean.py" || true

# Lint a script with issues
echo
echo "--- Linting a script with issues ---"
scitex-linter lint "$SCRIPT_DIR/sample_bad.py" || true

# Lint with severity filter
echo
echo "--- Errors only ---"
scitex-linter lint "$SCRIPT_DIR/sample_bad.py" --severity error || true

# JSON output for CI
echo
echo "--- JSON output ---"
scitex-linter lint "$SCRIPT_DIR/sample_bad.py" --json --no-color || true

# EOF
