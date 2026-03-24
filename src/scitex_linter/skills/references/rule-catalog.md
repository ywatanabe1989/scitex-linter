---
name: rule-catalog
description: Complete catalog of all built-in and plugin linter rules.
---

# Rule Catalog

## Core Rules (S001-S008)

| ID | Severity | Description |
|----|----------|-------------|
| S001 | warning | Use `stx.io.save/load` not raw `open()` |
| S002 | info | Use `@stx.session` for experiments |
| S003 | warning | Use `stx.plt.subplots()` |
| S004 | info | Use `stx.io.load_configs()` |
| S005 | warning | Avoid hardcoded paths |
| S006 | info | Use `stx.rng` for reproducibility |
| S007 | warning | `load_configs()` → UPPER_CASE variable |
| S008 | info | Magic numbers → centralize in config |

## Import Rules (I001-I007)

| ID | Severity | Description |
|----|----------|-------------|
| I001 | warning | Use `import scitex as stx` alias |
| I002 | error | No star imports from scitex |
| I003 | info | Submodule imports for large modules |
| I004 | info | Group: stdlib → third-party → scitex |
| I005 | warning | Don't import private modules |
| I006 | info | Lazy imports for optional deps |
| I007 | info | Prefer relative imports in packages |

## Path Rules (PA001-PA005)

| ID | Severity | Description |
|----|----------|-------------|
| PA001 | warning | Use `Path` not string concatenation |
| PA002 | info | Use `Path /` not `os.path.join` |
| PA003 | info | Use `stx.path` utilities |
| PA004 | error | No hardcoded absolute paths |
| PA005 | info | Use `__file__` for package data |

## Plugin Rules

| Source | IDs | Description |
|--------|-----|-------------|
| scitex-io | IO001-IO007 | I/O conventions |
| scitex-stats | ST001-ST006 | Statistics conventions |
| figrecipe | FM001-FM009, P001-P005 | Figure conventions |
| scitex-clew | (placeholder) | Claim conventions |
