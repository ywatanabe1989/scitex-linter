---
description: SciTeX code convention checker with pluggable rules for imports, naming, path handling, and package-specific patterns.
allowed-tools: mcp__scitex__linter_*
---

# scitex-linter

Code convention checker for SciTeX ecosystem packages.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-linter
import scitex_linter
scitex_linter.list_rules(...)

# Umbrella — pip install scitex
import scitex.linter
scitex.linter.list_rules(...)
```

`pip install scitex-linter` alone does NOT expose the `scitex` namespace;
`import scitex.linter` raises `ModuleNotFoundError`. To use the
`scitex.linter` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

## Sub-skills

### Core
- [01_quick-start.md](01_quick-start.md) — Basic usage
- [02_rule-catalog.md](02_rule-catalog.md) — All built-in rules

### Workflows
- [10_cli-reference.md](10_cli-reference.md) — CLI commands
- [11_mcp-tools.md](11_mcp-tools.md) — MCP tools for AI agents

## CLI

```bash
scitex-linter check [path]
scitex-linter list-rules
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `linter_check` | Check files for convention violations |
| `linter_check_source` | Check source code string |
| `linter_list_rules` | List available rules |
