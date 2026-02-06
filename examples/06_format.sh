#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/06_format.sh
# Usage: bash examples/06_format.sh
#
# Demonstrates: scitex-linter format command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Example 06: Format Command ==="

# Check if formatting is needed (dry run)
echo
echo "--- Check if formatting is needed ---"
scitex-linter format "$SCRIPT_DIR/sample_bad.py" --check || true

# Show diff of proposed changes
echo
echo "--- Show diff of proposed changes ---"
scitex-linter format "$SCRIPT_DIR/sample_bad.py" --diff || true

# Apply formatting to a temp copy and show results
echo
echo "--- Apply formatting to sample file ---"
TEMP_FILE=$(mktemp /tmp/sample_bad_XXXXXX.py)
cp "$SCRIPT_DIR/sample_bad.py" "$TEMP_FILE"

echo "Original file: $SCRIPT_DIR/sample_bad.py"
echo "Temp copy: $TEMP_FILE"
echo

echo "Running formatter..."
scitex-linter format "$TEMP_FILE" || true

echo
echo "Formatted file saved to: $TEMP_FILE"
echo "You can view it with: cat $TEMP_FILE"

# Clean up
rm "$TEMP_FILE"
echo "Temp file cleaned up"

# EOF
