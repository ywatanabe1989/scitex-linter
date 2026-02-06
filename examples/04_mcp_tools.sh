#!/bin/bash
# -*- coding: utf-8 -*-
# File: examples/04_mcp_tools.sh
# Usage: bash examples/04_mcp_tools.sh
#
# Demonstrates: scitex-linter mcp subcommands

set -e

echo "=== Example 04: MCP Tools ==="

# List available MCP tools
echo
echo "--- MCP tool list ---"
scitex-linter mcp list-tools

# Health check
echo
echo "--- MCP doctor ---"
scitex-linter mcp doctor

# Installation guide
echo
echo "--- MCP installation ---"
scitex-linter mcp installation

# EOF
