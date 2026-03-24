---
name: scitex-linter
description: SciTeX code convention checker with pluggable rules for imports, naming, path handling, and package-specific patterns. Use when checking code quality or learning SciTeX conventions.
allowed-tools: mcp__scitex__linter_*
---

# Code Convention Checking with scitex-linter

## Quick Start

```python
from scitex_linter import check, list_rules

# Check a file
results = check("script.py")
for r in results:
    print(f"{r['rule']}: {r['message']} (line {r['line']})")

# List all rules
rules = list_rules()
rules = list_rules(category="imports")
```

## Rule Categories

### Core (S001-S008)
- S001: Use `stx.io.save/load` not raw `open()`
- S002: Use `@stx.session` for experiments
- S003: Use `stx.plt.subplots()`
- S004: Use `stx.io.load_configs()`
- S005: Avoid hardcoded paths
- S006: Use `stx.rng` for reproducibility
- S007: `load_configs()` result → UPPER_CASE
- S008: Magic numbers → config

### Imports (I001-I007)
- I001: Use `import scitex as stx`
- I002: No star imports
- I003-I007: Import organization

### Path (PA001-PA005)
- PA001: Use `Path` not string concat
- PA002-PA005: Path best practices

### Plugins
Downstream packages add rules via `scitex_linter.plugins` entry points.

## CLI Commands

```bash
scitex-linter check script.py
scitex-linter check src/ --recursive
scitex-linter rules
scitex-linter rules --category core

# Skills
scitex-linter skills list
scitex-linter skills get SKILL
scitex-linter skills get rule-catalog
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `linter_check` | Check a file for violations |
| `linter_check_source` | Check source code string |
| `linter_list_rules` | List rules with descriptions |

## Specific Topics

* **Rule catalog** [references/rule-catalog.md](references/rule-catalog.md)
