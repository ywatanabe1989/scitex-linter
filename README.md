<!-- ---
!-- Timestamp: 2026-03-14 12:00:00
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/scitex-linter/README.md
!-- --- -->

# SciTeX Linter (<code>scitex-linter</code>)

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-banner.png" alt="SciTeX Linter" width="400">
  </a>
</p>

<p align="center"><b>AST-based Python linter enforcing reproducible research patterns</b></p>

<p align="center">
  <a href="https://badge.fury.io/py/scitex-linter"><img src="https://badge.fury.io/py/scitex-linter.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/scitex-linter/"><img src="https://img.shields.io/pypi/pyversions/scitex-linter.svg" alt="Python Versions"></a>
  <a href="https://scitex-linter.readthedocs.io/"><img src="https://readthedocs.org/projects/scitex-linter/badge/?version=latest" alt="Documentation"></a>
  <a href="https://github.com/ywatanabe1989/scitex-linter/actions/workflows/python-tests.yml"><img src="https://github.com/ywatanabe1989/scitex-linter/actions/workflows/python-tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://www.gnu.org/licenses/agpl-3.0"><img src="https://img.shields.io/badge/License-AGPL--3.0-blue.svg" alt="License: AGPL-3.0"></a>
</p>

<p align="center">
  <a href="https://scitex-linter.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-linter</code>
</p>

---

## Problem

SciTeX scripts follow strict patterns for reproducibility — `@scitex.session` decorators, `scitex.io` for provenance-tracked I/O, `scitex.stats` for complete statistical reporting, and relative paths for portability. Deviations from these patterns silently undermine reproducibility, and manual code review does not scale across large research projects or AI-generated code.

## Solution

SciTeX Linter analyzes Python source code at the AST (Abstract Syntax Tree) level to detect violations of SciTeX patterns before they become irreproducible results. It provides 47 rules across 7 categories, covering structure, imports, I/O, plotting, statistics, paths, and figure layout. The linter integrates into terminal workflows, CI pipelines, and AI agent toolchains — ensuring both human researchers and AI assistants produce reproducible science.

## Installation

```bash
pip install scitex-linter
```

## Quick Start

```bash
# Lint a file
scitex-linter check script.py

# Lint then execute
scitex-linter python experiment.py --strict

# Auto-fix issues
scitex-linter format script.py

# List all 47 rules
scitex-linter rule
```

## Four Interfaces

<details>
<summary><strong>Python API</strong></summary>

<br>

```python
from scitex_linter.checker import lint_file, lint_source
from scitex_linter.formatter import format_issue

# Lint a file
issues = lint_file("script.py")
for issue in issues:
    print(format_issue(issue, "script.py"))

# Check source code directly
issues = lint_source("import argparse\npass\n")
```

<details>
<summary>Full API reference</summary>

<br>

```
scitex_linter
  list_rules(category=None) -> list[Rule]

scitex_linter.checker
  lint_file(filepath, config=None) -> list[Issue]
  lint_source(source, filepath, config=None) -> list[Issue]
  is_script(filepath, config=None) -> bool

scitex_linter.fixer
  fix_source(source, filepath, config=None) -> str
  fix_file(filepath, write=True, config=None) -> tuple

scitex_linter.formatter
  format_issue(issue, filepath, color=False) -> str
  format_summary(issues, filepath, color=False) -> str
  to_json(issues, filepath) -> list[dict]
```

</details>

</details>

<details>
<summary><strong>CLI Commands</strong></summary>

<br>

```bash
scitex-linter --help                              # Show all commands
scitex-linter --help-recursive                    # Show help for all subcommands

# Check
scitex-linter check script.py                      # Check a file
scitex-linter check ./src/                         # Check a directory
scitex-linter check script.py --severity error     # Only errors
scitex-linter check script.py --category path      # Only path rules
scitex-linter check script.py --json               # JSON output for CI

# Format (auto-fix)
scitex-linter format script.py                     # Fix in place
scitex-linter format script.py --check             # Dry run (exit 1 if changes needed)
scitex-linter format script.py --diff              # Show diff of changes

# Lint then execute
scitex-linter python experiment.py                 # Lint and run
scitex-linter python experiment.py --strict        # Abort on errors
scitex-linter python experiment.py -- --lr 0.001   # Pass script args

# Rules
scitex-linter rule                                 # List all 47 rules
scitex-linter rule --category stats                # Filter by category
scitex-linter rule --json                          # JSON output
```

<details>
<summary>Additional integrations</summary>

<br>

**flake8 plugin** — registers with the `STX` prefix for CI pipelines:

```bash
flake8 --select STX script.py
```

**Claude Code hook** — auto-lints every Python file Claude writes or edits:

```bash
# In ~/.claude/to_claude/hooks/post-tool-use/run_lint.sh
# Errors (exit 2) → Claude must fix
# Warnings (exit 1) → Claude sees feedback
```

</details>

</details>

<details>
<summary><strong>MCP Server</strong></summary>

<br>

Three tools for AI agents (Claude, GPT, etc.):

| Tool | Description |
|------|-------------|
| `linter_check` | Check a Python file for SciTeX compliance |
| `linter_check_source` | Lint source code string |
| `linter_list_rules` | List all available rules |

```bash
scitex-linter mcp start          # Start server (stdio)
scitex-linter mcp list-tools     # List available tools
scitex-linter mcp doctor         # Health check
scitex-linter mcp installation   # Show Claude Desktop config
```

Install MCP extra: `pip install scitex-linter[mcp]`

</details>

<details>
<summary><strong>Skills — for AI Agent Discovery</strong></summary>

<br>

Skills provide workflow-oriented guides that AI agents query to discover capabilities and usage patterns.

```bash
scitex-linter skills list              # List available skill pages
scitex-linter skills get SKILL         # Show main skill page
scitex-dev skills export --package scitex-linter  # Export to Claude Code
```

| Skill | Content |
|-------|---------|
| `quick-start` | Basic usage |
| `rule-catalog` | All built-in rules |
| `cli-reference` | CLI commands |
| `mcp-tools` | MCP tools for AI agents |

</details>

## 47 Rules Across 7 Categories

| Category | Count | Severity | What It Enforces |
|----------|------:|----------|-----------------|
| **S** Structure | 8 | error/warning/info | `@scitex.session`, `__main__` guard, INJECTED params |
| **I** Import | 7 | warning/info | Use `scitex.plt`, `scitex.stats`, `scitex.io` instead of raw libs |
| **IO** I/O Calls | 7 | warning | Use `scitex.io.save()`/`scitex.io.load()` for provenance |
| **P** Plot | 5 | info | Use `scitex.plt` tracked methods, `logger` over `print()` |
| **ST** Stats | 6 | warning | Use `scitex.stats` for auto effect size + CI + power |
| **PA** Path | 5 | warning/info | Relative paths with `./`, no `open()`, no `os.chdir()` |
| **FM** Figure | 9 | warning/info | mm-based layout, `scitex.io.save()` for figures |

<p align="center"><sub><b>Table 1.</b> Rule categories. Run <code>scitex-linter rule</code> for the full list, or see the <a href="https://scitex-linter.readthedocs.io/en/latest/rules.html">Rules Reference</a>.</sub></p>

<details>
<summary>Example output</summary>

<br>

```
script.py:1   STX-S003  [error]    argparse detected — @scitex.session auto-generates CLI
  Suggestion: Remove `import argparse` and define parameters as function arguments:
    @scitex.session
    def main(data_path: str, threshold: float = 0.5):
        # Auto-generates: --data-path, --threshold

script.py:5   STX-PA001 [warning]  Absolute path in `scitex.io` call — use relative paths
  Suggestion: Use `scitex.io.save(obj, './relative/path.ext')` — paths resolve to script_out/.

script.py: 2 issues (1 error, 1 warning)
```

</details>

<details>
<summary>Full rules listing</summary>

<br>

| Rule | Severity | Message |
|------|----------|---------|
| `STX-S001` | error | Missing `@scitex.session` or `@scitex.module` decorator on main function |
| `STX-S002` | error | Missing `if __name__ == '__main__'` guard |
| `STX-S003` | error | argparse detected — `@scitex.session` auto-generates CLI from function signature |
| `STX-S004` | warning | `@scitex.session` function should return an integer exit code |
| `STX-S005` | warning | Missing `import scitex` |
| `STX-S006` | warning | `@scitex.session` function missing explicit INJECTED parameters |
| `STX-S007` | warning | `load_configs()` result should be assigned to an UPPER_CASE variable |
| `STX-S008` | info | Magic number in module scope — consider centralizing in config/ |
| `STX-I001` | warning | Use `scitex.plt` instead of importing matplotlib.pyplot directly |
| `STX-I002` | warning | Use `scitex.stats` instead of importing scipy.stats directly |
| `STX-I003` | warning | Use `scitex.io` instead of pickle for file I/O |
| `STX-I004` | warning | Use `scitex.io` for CSV/DataFrame I/O instead of pandas I/O functions |
| `STX-I005` | warning | Use `scitex.io` for array I/O instead of numpy save/load |
| `STX-I006` | info | Use `rngg` (injected by `@scitex.session`) for reproducible randomness |
| `STX-I007` | warning | Use `logger` (injected by `@scitex.session`) instead of logging module |
| `STX-IO001` | warning | Use `scitex.io.save()` instead of `np.save()` / `np.savez()` |
| `STX-IO002` | warning | Use `scitex.io.load()` instead of `np.load()` / `np.loadtxt()` |
| `STX-IO003` | warning | Use `scitex.io.save()` instead of `pd.to_csv()` / `to_excel()` |
| `STX-IO004` | warning | Use `scitex.io.load()` instead of `pd.read_csv()` / `read_excel()` |
| `STX-IO005` | warning | Use `scitex.io.save()` instead of `pickle.dump()` |
| `STX-IO006` | warning | Use `scitex.io.load()` instead of `pickle.load()` |
| `STX-IO007` | warning | Use `scitex.io.save()` instead of `plt.savefig()` |
| `STX-P001` | info | Use `scitex.plt.subplots()` instead of `plt.subplots()` |
| `STX-P002` | info | Use `scitex.plt.figure()` instead of `plt.figure()` |
| `STX-P003` | info | Use `scitex.plt.show()` instead of `plt.show()` |
| `STX-P004` | info | Use `logger` instead of `print()` for output |
| `STX-P005` | info | Use `scitex.plt` methods for consistent plotting |
| `STX-ST001` | warning | Use `scitex.stats.ttest_ind()` for complete statistical reporting |
| `STX-ST002` | warning | Use `scitex.stats.ttest_1samp()` for complete statistical reporting |
| `STX-ST003` | warning | Use `scitex.stats.mannwhitneyu()` for complete statistical reporting |
| `STX-ST004` | warning | Use `scitex.stats.wilcoxon()` for complete statistical reporting |
| `STX-ST005` | warning | Use `scitex.stats.chi2_contingency()` for complete statistical reporting |
| `STX-ST006` | warning | Use `scitex.stats.f_oneway()` for complete statistical reporting |
| `STX-PA001` | warning | Absolute path in `scitex.io` call — use relative paths for reproducibility |
| `STX-PA002` | warning | `open()` detected — use `scitex.io.save()`/`scitex.io.load()` which includes auto-logging |
| `STX-PA003` | info | `os.makedirs()`/`mkdir()` detected — `scitex.io.save()` creates directories automatically |
| `STX-PA004` | warning | `os.chdir()` detected — scripts should be run from project root |
| `STX-PA005` | info | Path without `./` prefix in `scitex.io` call — use `./` for explicit relative intent |
| `STX-FM001` | warning | Use `scitex.io.save()` instead of `fig.savefig()` |
| `STX-FM002` | info | Use `scitex.plt.subplots()` for mm-based figure layout |
| `STX-FM003` | info | Use mm units for figure dimensions |
| `STX-FM004` | warning | `tight_layout()` conflicts with mm-based layout |
| `STX-FM005` | warning | `constrained_layout` conflicts with mm-based layout |
| `STX-FM006` | warning | `subplots_adjust()` conflicts with mm-based layout |
| `STX-FM007` | info | `rcParams` direct modification detected — hard to maintain across figures |
| `STX-FM008` | warning | `set_size_inches()` detected — bypasses mm-based layout control |
| `STX-FM009` | warning | `ax.set_position()` detected — conflicts with mm-based layout control |

Additional rules are contributed by downstream packages via the `scitex_linter.plugins` entry point.

</details>

## What a Clean Script Looks Like

```python
import scitex

@scitex.session
def main(data_path="./data.csv", threshold=0.5):
    df = scitex.io.load(data_path)
    results = scitex.stats.ttest_ind(df["group_a"], df["group_b"])
    scitex.io.save(results, "./results.csv")
    return 0

if __name__ == "__main__":
    main()
```

Zero lint issues. Fully reproducible. Auto-CLI from function signature.

## Configuration

<details>
<summary>Configure via pyproject.toml or environment variables</summary>

<br>

```toml
[tool.scitex-linter]
severity = "info"                    # Minimum severity: error, warning, info
disable = ["STX-P004", "STX-I003"]   # Disable specific rules
exclude-dirs = ["venv", ".venv"]     # Directories to skip
library-dirs = ["src"]               # Exempt from script-only rules

[tool.scitex-linter.per-rule-severity]
STX-S003 = "warning"                 # Downgrade argparse rule

[tool.scitex-linter.session]
required-injected = ["CONFIG", "plt", "COLORS", "rngg", "logger"]
```

Environment variables (highest priority):
```bash
SCITEX_LINTER_SEVERITY=error
SCITEX_LINTER_DISABLE=STX-P004,STX-I003
```

Priority: CLI flags > env vars > pyproject.toml > defaults

</details>

## Part of SciTeX

SciTeX Linter is part of [SciTeX](https://scitex.ai). When used inside the orchestrator package `scitex`, the linter automatically enforces patterns for all SciTeX modules — `scitex.io`, `scitex.stats`, `scitex.plt`, and `scitex.session` — ensuring consistency across the entire research pipeline.

The SciTeX ecosystem follows the Four Freedoms for researchers, inspired by [the Free Software Definition](https://www.gnu.org/philosophy/free-sw.en.html):

- **Freedom 0** — Run research for any purpose
- **Freedom 1** — Study and modify the research pipeline
- **Freedom 2** — Redistribute results and methods
- **Freedom 3** — Distribute modified versions to advance science

## Documentation

[Full Documentation on Read the Docs](https://scitex-linter.readthedocs.io/)

- [Installation](https://scitex-linter.readthedocs.io/en/latest/installation.html)
- [Quick Start](https://scitex-linter.readthedocs.io/en/latest/quickstart.html)
- [Rules Reference](https://scitex-linter.readthedocs.io/en/latest/rules.html)
- [CLI Reference](https://scitex-linter.readthedocs.io/en/latest/cli.html)
- [Claude Code Hook](https://scitex-linter.readthedocs.io/en/latest/hook.html)

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
  <br>
  AGPL-3.0
</p>

<!-- EOF -->
