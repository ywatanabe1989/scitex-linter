<!-- ---
!-- Timestamp: 2026-02-06 20:53:45
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/scitex-linter/README.md
!-- --- -->

# SciTeX Linter

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-banner.png" alt="SciTeX Linter" width="400">
  </a>
</p>

<p align="center">
  <a href="https://badge.fury.io/py/scitex-linter"><img src="https://badge.fury.io/py/scitex-linter.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/scitex-linter/"><img src="https://img.shields.io/pypi/pyversions/scitex-linter.svg" alt="Python Versions"></a>
  <a href="https://scitex-linter.readthedocs.io/"><img src="https://readthedocs.org/projects/scitex-linter/badge/?version=latest" alt="Documentation"></a>
  <a href="https://github.com/ywatanabe1989/scitex-linter/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ywatanabe1989/scitex-linter" alt="License"></a>
</p>

<p align="center">
  <a href="https://scitex.ai">scitex.ai</a> · <a href="https://scitex-linter.readthedocs.io/">docs</a> · <code>pip install scitex-linter</code>
</p>

---

**AST-based Python linter enforcing [SciTeX](https://scitex.ai) reproducible research patterns.**

Part of the [SciTeX](https://scitex.ai) ecosystem — guides both human researchers and AI agents toward reproducible science.

## Why SciTeX Linter?

SciTeX scripts follow strict patterns for reproducibility: `@stx.session` decorators, `stx.io` for provenance-tracked I/O, `stx.stats` for complete statistical reporting, and relative paths for portability. SciTeX Linter enforces these patterns at the AST level — catching issues before they become irreproducible results.

## Quick Start

```bash
pip install scitex-linter
```

```bash
# Lint a file
scitex-linter check script.py

# Lint then execute
scitex-linter python experiment.py --strict

# List all 47 rules
scitex-linter rule
```

## Six Interfaces

| Interface | For | Description |
|-----------|-----|-------------|
| 🖥️ **CLI** | Terminal users | `scitex-linter check`, `scitex-linter python` |
| ✨ **Format** | Auto-fix | `scitex-linter format` — savefig, np.save/load, pd.read_csv |
| 🐍 **Python API** | Programmatic use | `scitex-linter api` or `from scitex_linter.checker import lint_file` |
| 🔌 **flake8 Plugin** | CI pipelines | `flake8 --select STX` |
| 🔧 **MCP Server** | AI agents | 3 tools for Claude/GPT integration |
| 📋 **Claude Code Hook** | AI coding | Auto-lint on every file write/edit |

<details>
<summary><strong>🖥️ CLI Commands</strong></summary>

<br>

```bash
scitex-linter --help                              # Show all commands
scitex-linter --help-recursive                    # Show help for all subcommands

# Check - Check for SciTeX pattern violations
scitex-linter check script.py                      # Check a file
scitex-linter check ./src/                         # Check a directory
scitex-linter check script.py --severity error     # Only errors
scitex-linter check script.py --category path      # Only path rules
scitex-linter check script.py --json               # JSON output for CI

# Format - Auto-fix SciTeX pattern issues
scitex-linter format script.py                     # Fix in place
scitex-linter format script.py --check             # Dry run (exit 1 if changes needed)
scitex-linter format script.py --diff              # Show diff of changes
scitex-linter format ./src/                        # Format a directory

# Python - Lint then execute
scitex-linter python experiment.py                # Lint and run
scitex-linter python experiment.py --strict       # Abort on errors
scitex-linter python experiment.py -- --lr 0.001  # Pass script args

# Rules - Browse available rules
scitex-linter rule                          # List all 47 rules
scitex-linter rule --category stats         # Filter by category
scitex-linter rule --json                   # JSON output

# API - Inspect public Python API
scitex-linter api                           # Tree view of 12 public APIs
scitex-linter api --json                    # JSON output

# MCP - AI agent server
scitex-linter mcp start                           # Start MCP server (stdio)
scitex-linter mcp list-tools                      # List MCP tools
```

</details>

<details>
<summary><strong>🐍 Python API</strong></summary>

<br>

```python
from scitex_linter.checker import lint_file
from scitex_linter.formatter import format_issue

# Lint a file
issues = lint_file("script.py")
for issue in issues:
    print(format_issue(issue, "script.py"))

# Check source code directly
from scitex_linter.checker import lint_source
issues = lint_source("import argparse\npass\n")
```

</details>

<details>
<summary><strong>🔌 flake8 Plugin</strong></summary>

<br>

SciTeX Linter registers as a flake8 plugin with the `STX` prefix:

```bash
flake8 --select STX script.py
flake8 --select STX ./src/ --format=json
```

Integrates with existing flake8 workflows, pre-commit hooks, and CI pipelines.

</details>

<details>
<summary><strong>🔧 MCP Server — 3 Tools for AI Agents</strong></summary>

<br>

| Tool | Description |
|------|-------------|
| `linter_check` | Check a Python file for SciTeX compliance |
| `linter_list_rules` | List all available rules |
| `linter_check_source` | Lint source code string |

**Claude Desktop** (`~/.config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "scitex-linter": {
      "command": "scitex-linter",
      "args": ["mcp", "start"]
    }
  }
}
```

Install MCP extra: `pip install scitex-linter[mcp]`

</details>

## 45 Rules Across 8 Categories

| Category | Rules | Severity | What It Enforces |
|----------|------:|----------|-----------------|
| **S** Structure | 6 | error/warning | `@stx.session`, `__main__` guard, INJECTED params |
| **I** Import | 7 | warning/info | Use `stx.plt`, `stx.stats`, `stx.io` instead of raw libs |
| **IO** I/O Calls | 7 | warning | Use `stx.io.save()`/`stx.io.load()` for provenance |
| **P** Plot | 5 | info | Use `stx.plt` tracked methods, `logger` over `print()` |
| **ST** Stats | 6 | warning | Use `stx.stats` for auto effect size + CI + power |
| **PA** Path | 5 | warning/info | Relative paths with `./`, no `open()`, no `os.chdir()` |
| **FM** Figure | 9 | warning/info | mm-based layout, `stx.io.save()` for figures (opt-in) |

<details>
<summary><strong>Example Output</strong></summary>

<br>

```
script.py:1   STX-S003  [error]    argparse detected — @stx.session auto-generates CLI
  Suggestion: Remove `import argparse` and define parameters as function arguments:
    @stx.session
    def main(data_path: str, threshold: float = 0.5):
        # Auto-generates: --data-path, --threshold

script.py:5   STX-PA001 [warning]  Absolute path in `stx.io` call — use relative paths
  Suggestion: Use `stx.io.save(obj, './relative/path.ext')` — paths resolve to script_out/.

script.py: 2 issues (1 error, 1 warning)
```

</details>

<details>
<summary><strong>Full Rules Reference</strong></summary>

<br>

See [Rules Reference](https://scitex-linter.readthedocs.io/en/latest/rules.html) for all 47 rules with descriptions and suggestions.

</details>

## Claude Code Hook

SciTeX Linter works as a **post-tool-use hook** for Claude Code, automatically linting every Python file Claude writes or edits:

```bash
# In ~/.claude/to_claude/hooks/post-tool-use/run_lint.sh
# Errors (exit 2) → Claude must fix
# Warnings (exit 1) → Claude sees feedback
```

This ensures AI-generated code follows SciTeX patterns from the start.

## Configuration

<details>
<summary><strong>Configure via pyproject.toml or environment variables</strong></summary>

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

## What a Clean Script Looks Like

```python
import scitex as stx

@stx.session
def main(data_path="./data.csv", threshold=0.5):
    df = stx.io.load(data_path)
    results = stx.stats.ttest_ind(df["group_a"], df["group_b"])
    stx.io.save(results, "./results.csv")
    return 0

if __name__ == "__main__":
    main()
```

Zero lint issues. Fully reproducible. Auto-CLI from function signature.

## Lint Rules

Detected by [scitex-linter](https://github.com/ywatanabe1989/scitex-linter) when this package is installed.

| Rule | Severity | Message |
|------|----------|---------|
| `STX-S001` | error | Missing @stx.session or @stx.module decorator on main function |
| `STX-S002` | error | Missing `if __name__ == '__main__'` guard |
| `STX-S003` | error | argparse detected — @stx.session auto-generates CLI from function signature |
| `STX-S004` | warning | @stx.session function should return an integer exit code |
| `STX-S005` | warning | Missing `import scitex as stx` |
| `STX-S006` | warning | @stx.session function missing explicit INJECTED parameters |
| `STX-S007` | warning | load_configs() result should be assigned to an UPPER_CASE variable |
| `STX-S008` | info | Magic number in module scope — consider centralizing in config/ |
| `STX-I001` | warning | Use `stx.plt` instead of importing matplotlib.pyplot directly |
| `STX-I002` | warning | Use `stx.stats` instead of importing scipy.stats directly |
| `STX-I003` | warning | Use `stx.io` instead of pickle for file I/O |
| `STX-I004` | warning | Use `stx.io` for CSV/DataFrame I/O instead of pandas I/O functions |
| `STX-I005` | warning | Use `stx.io` for array I/O instead of numpy save/load |
| `STX-I006` | info | Use `rngg` (injected by @stx.session) for reproducible randomness |
| `STX-I007` | warning | Use `logger` (injected by @stx.session) instead of logging module |
| `STX-PA001` | warning | Absolute path in `stx.io` call — use relative paths for reproducibility |
| `STX-PA002` | warning | `open()` detected — use `stx.io.save()`/`stx.io.load()` which includes auto-logging |
| `STX-PA003` | info | `os.makedirs()`/`mkdir()` detected — `stx.io.save()` creates directories automatically |
| `STX-PA004` | warning | `os.chdir()` detected — scripts should be run from project root |
| `STX-PA005` | info | Path without `./` prefix in `stx.io` call — use `./` for explicit relative intent |

Additional rules are contributed by downstream packages via the `scitex_linter.plugins` entry point. Install a package to activate its rules automatically.

## Documentation

📚 **[Full Documentation on Read the Docs](https://scitex-linter.readthedocs.io/)**

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
