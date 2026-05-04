---
name: scitex-linter
description: |
  [WHAT] AST-based linter for reproducible-research Python — 47 built-in rules across 7 categories — STX-I* (imports, e.g. enforce `import scitex as stx`, no star imports, stdlib ordering), STX-IO* (forbid raw `pd.read_csv` / `np.load` / `pickle` / `fig.savefig` → use `stx.io.save` / `stx.io.load`), STX-P* (path handling — no hardcoded `/home/...`, always resolve via `stx.path`), STX-PA* (plot/axes — axis…
  [WHEN] Use whenever the user asks to "lint my scitex code", "check scitex conventions", "is this using stx.
  [HOW] io correctly?", "what scitex rules does this violate?", "list linter rules", "show STX-IO001 meaning", "enforce reproducible-research style", or mentions STX-*, scitex-linter, scitex conventions, reproducibility lint.
tags: [scitex-linter]
allowed-tools: mcp__scitex__linter_*
primary_interface: hook
interfaces:
  python: 1
  cli: 2
  mcp: 1
  skills: 2
  http: 0
---

# scitex-linter

> **Interfaces:** Python ⭐ · CLI ⭐⭐ · MCP ⭐ · Skills ⭐⭐ · Hook ⭐⭐⭐ (primary) · HTTP —

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

### Mandatory leaves
- [01_installation.md](01_installation.md) — pip install + extras + smoke verify
- [02_quick-start.md](02_quick-start.md) — minimal `check-files` example
- [03_python-api.md](03_python-api.md) — top-level Python surface
- [04_cli-reference.md](04_cli-reference.md) — `scitex-linter` subcommand summary

### Core
- [06_quick-start.md](06_quick-start.md) — basic usage (legacy detail)
- [07_rule-catalog.md](07_rule-catalog.md) — all built-in rules

### Workflows
- [10_cli-reference.md](10_cli-reference.md) — CLI commands (legacy detail)
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


## Environment

- [20_env-vars.md](20_env-vars.md) — SCITEX_* env vars read by scitex-linter at runtime
