#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/01_check_files.sh
# Usage: bash examples/01_check_files.sh
#
# Demonstrates: scitex-linter check command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Example 01: Check Files ==="

# Check a clean SciTeX script
echo
echo "--- Checking a clean script ---"
scitex-linter check "$SCRIPT_DIR/sample_clean.py" || true

# Check a script with issues
echo
echo "--- Checking a script with issues ---"
scitex-linter check "$SCRIPT_DIR/sample_bad.py" || true

# Check with severity filter
echo
echo "--- Errors only ---"
scitex-linter check "$SCRIPT_DIR/sample_bad.py" --severity error || true

# JSON output for CI
echo
echo "--- JSON output ---"
scitex-linter check "$SCRIPT_DIR/sample_bad.py" --json --no-color || true

# EOF
