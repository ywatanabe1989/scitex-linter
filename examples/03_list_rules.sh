#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/03_list_rules.sh
# Usage: bash examples/03_list_rules.sh
#
# Demonstrates: scitex-linter rule command

set -e

echo "=== Example 03: List Rules ==="

# List all rules
echo
echo "--- All rules ---"
scitex-linter rule

# Filter by category
echo
echo "--- Path rules only ---"
scitex-linter rule --category path

# Filter by severity
echo
echo "--- Errors only ---"
scitex-linter rule --severity error

# EOF
