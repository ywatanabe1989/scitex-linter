<!-- ---
!-- Timestamp: 2026-02-06 19:10:00
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/scitex-linter/GITIGNORED/LINT_PATTERNS.md
!-- --- -->

# SciTeX Linter — Rule Planning

## Investigation Summary

Deeply investigated `~/proj/scitex-python/src/scitex/` modules:
- `session/` — decorator, auto-CLI, injected globals (CONFIG, plt, COLORS, rngg, logger)
- `io/` — 30+ format handlers, save/load with metadata & provenance
- `plt/` — figrecipe wrapper, `__getattr__` fallback to matplotlib.pyplot, AxisWrapper with stx_* methods
- `stats/` — 23+ tests, recommend_tests(), effect sizes, power analysis, journal formatting
- `__init__.py` — 43+ lazy-loaded modules, _CallableModuleWrapper for session

Reviewed examples: `examples/session/`, `examples/bridge/`, `examples/audio/`, etc.

---

## Design Principles

1. **API similarity** — The linter should NOT force users to learn new APIs.
   If `plt.savefig()` is flagged, scitex-python should provide `stx.plt.savefig()`.
   The linter's job: "prefix with `stx.`", not "rewrite your call".

2. **Import-level detection first** — Flagging `import matplotlib.pyplot as plt`
   is simpler and higher-signal than matching individual function calls.
   One import rule covers all functions from that module.

3. **Structural checks are the highest value** — Missing `@stx.session`,
   missing `if __name__ == '__main__'`, using `argparse` — these are
   the most impactful rules for reproducibility.

4. **Minimal false positives** — Library/utility code should not require
   `@stx.session`. Rules should apply to **scripts** (files with `__name__ == '__main__'`),
   not to library modules.

---

## Rule Categories

### Category S: Structure (errors — highest priority)

These enforce the canonical script template:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Top-level docstring"""

import scitex as stx

@stx.session
def main(
    arg1="default",
    CONFIG=stx.session.INJECTED,
    plt=stx.session.INJECTED,
    logger=stx.session.INJECTED,
):
    """Docstring becomes --help."""
    return 0

if __name__ == '__main__':
    main()
```

| Rule ID | Severity | Pattern | Message |
|---------|----------|---------|---------|
| STX-S001 | error | No `@stx.session` on any function in a script with `__name__ == '__main__'` guard | Add `@stx.session` decorator to your main function for reproducible session tracking |
| STX-S002 | error | No `if __name__ == '__main__'` guard in a script file | Add `if __name__ == '__main__': main()` guard |
| STX-S003 | error | `import argparse` or `argparse.ArgumentParser()` | Remove argparse — `@stx.session` auto-generates CLI from function signature |
| STX-S004 | warning | `@stx.session` function does not `return 0` (or any int) | Return an integer exit code (0 for success) from your session function |
| STX-S005 | warning | Missing `import scitex as stx` | Add `import scitex as stx` |

**Scope:** Only applies to files containing `if __name__ == '__main__'` (scripts).
Library modules (`__init__.py`, utility files) are exempt from S001/S002.

---

### Category I: Imports (warnings — high priority)

Flag imports of libraries that scitex wraps. The fix is always "use `stx.X` instead".

| Rule ID | Severity | Flagged Import | Replacement |
|---------|----------|---------------|-------------|
| STX-I001 | warning | `import matplotlib.pyplot as plt` / `from matplotlib import pyplot` | Use `stx.plt` (or `plt` injected by `@stx.session`) |
| STX-I002 | warning | `from scipy import stats` / `from scipy.stats import *` | Use `stx.stats` |
| STX-I003 | warning | `import pickle` / `import json` (for I/O purposes) | Use `stx.io.save()`/`stx.io.load()` |
| STX-I004 | warning | `import pandas as pd` with `pd.read_csv`/`pd.to_csv` usage | Use `stx.io.load()`/`stx.io.save()` for file I/O |
| STX-I005 | warning | `import numpy as np` with `np.save`/`np.load` usage | Use `stx.io.save()`/`stx.io.load()` for file I/O |
| STX-I006 | info | `import random` / `np.random.seed()` | Use `rngg` injected by `@stx.session` for reproducible randomness |
| STX-I007 | warning | `import logging` | Use `logger` injected by `@stx.session` |

**Note on I003:** `import json` for parsing API responses is fine.
Only flag when used with file I/O (`json.dump()`/`json.load()` with file objects).
Phase 1 can flag the import with a softer message; Phase 2 can do AST-level call detection.

**Note on I004/I005:** `import pandas`/`import numpy` themselves are fine.
The anti-pattern is using their I/O functions. Phase 1: flag only when
combined with `.read_csv`, `.to_csv`, `np.save`, `np.load` calls.

---

### Category P: Plotting (info — medium priority)

These are softer suggestions for using stx.plt enhanced features.

| Rule ID | Severity | Pattern | Message |
|---------|----------|---------|---------|
| STX-P001 | info | `ax.plot()` | Consider `ax.stx_line()` for automatic CSV data export |
| STX-P002 | info | `ax.scatter()` | Consider `ax.stx_scatter()` for automatic CSV data export |
| STX-P003 | info | `ax.bar()` | Consider `ax.stx_bar()` for automatic sample size annotation |
| STX-P004 | info | `ax.imshow()` | Consider `ax.stx_imshow()` for tracked image display |
| STX-P005 | info | `plt.show()` | `plt.show()` is non-reproducible in batch/CI environments |
| STX-P006 | info | `print()` inside `@stx.session` function | Use `logger.info()` (injected by `@stx.session`) for tracked logging |

**Scope:** P001-P004 only apply when the axes object comes from `stx.plt.subplots()`.
Hard to detect statically in Phase 1 — defer to Phase 2 with type inference.
Phase 1 can show these as optional hints only.

---

### Category IO: File I/O (warnings — medium priority)

Specific function call patterns that bypass provenance tracking.

| Rule ID | Severity | Pattern | Replacement |
|---------|----------|---------|-------------|
| STX-IO001 | warning | `np.save(arr, path)` | `stx.io.save(arr, path)` — tracks output hashes |
| STX-IO002 | warning | `np.load(path)` | `stx.io.load(path)` — records input hashes |
| STX-IO003 | warning | `pd.read_csv(path)` | `stx.io.load(path)` — records input hashes |
| STX-IO004 | warning | `df.to_csv(path)` | `stx.io.save(df, path)` — tracks output hashes |
| STX-IO005 | warning | `pickle.dump(obj, f)` | `stx.io.save(obj, 'file.pkl')` |
| STX-IO006 | warning | `json.dump(obj, f)` | `stx.io.save(obj, 'file.json')` |
| STX-IO007 | warning | `open(path, 'w')` for writing | `stx.io.save(data, path)` — tracks output |
| STX-IO008 | warning | `plt.savefig(path)` | `stx.io.save(fig, path)` or `stx.plt.savefig(path)` |

**Note:** IO rules overlap with I-rules. Import-level rules (Category I) are
Phase 1. Call-level rules (Category IO) are Phase 2 refinements.

---

### Category ST: Statistics (warnings — lower priority)

| Rule ID | Severity | Pattern | Replacement |
|---------|----------|---------|-------------|
| STX-ST001 | warning | `scipy.stats.ttest_ind()` | `stx.stats.ttest_ind()` — auto effect size + CI |
| STX-ST002 | warning | `scipy.stats.mannwhitneyu()` | `stx.stats.mannwhitneyu()` — auto effect size + CI |
| STX-ST003 | warning | `scipy.stats.pearsonr()` | `stx.stats.pearsonr()` — auto CI + power analysis |
| STX-ST004 | warning | `scipy.stats.f_oneway()` | `stx.stats.anova_oneway()` — with post-hoc + effect sizes |
| STX-ST005 | warning | `scipy.stats.wilcoxon()` | `stx.stats.wilcoxon()` — auto effect size + CI |
| STX-ST006 | warning | `scipy.stats.kruskal()` | `stx.stats.kruskal()` — with post-hoc + effect sizes |
| STX-ST007 | info | Any scipy.stats test without effect size | Consider `stx.stats` which auto-calculates effect sizes |

---

## Implementation Phases

### Phase 1: Structural + Import rules (MVP)

**Rules:** STX-S001 through S005, STX-I001 through I007

**Detection method:** AST-based
- Parse with `ast.parse()`
- Walk tree for Import/ImportFrom nodes
- Walk tree for FunctionDef with decorator check
- Check for `if __name__ == '__main__'` at module level

**Deliverables:**
- `stx-lint` CLI command (single Python file, no dependencies beyond stdlib)
- Exit codes: 0 (clean), 1 (warnings), 2 (errors)
- Human-readable terminal output + JSON output (`--json`)
- Claude Code hook script (`enforce_scitex_patterns.sh` in `pre-tool-use/`)

**Scope exclusions for scripts detection:**
- Files without `if __name__ == '__main__'` are treated as library modules
- `__init__.py` files always exempt from session/guard rules
- `test_*.py` / `conftest.py` files exempt from session rules
- Files under `setup.py`, `pyproject.toml` context exempt

### Phase 2: Call-level rules

**Rules:** STX-IO001 through IO008, STX-P001 through P006, STX-ST001 through ST007

**Detection method:** AST visitor tracking import aliases
- Resolve `import numpy as np` → track that `np.save` means numpy.save
- Match `module.func()` patterns against rule database

### Phase 3: flake8 plugin

**Distribution:** `pip install flake8-scitex`
- Reuse AST visitor from Phase 1/2
- Register via `entry_points` in `pyproject.toml`
- Error codes: `STX` prefix (e.g., `STX001`)
- Editor integration comes free (VS Code, Emacs, etc.)

### Phase 4: `scitex run` integration

**Command:** `scitex run script.py`
- Lint → show warnings → execute
- Option: `scitex run --strict script.py` (abort on errors)
- Lives in scitex-python, not scitex-linter (imports linter as dependency)

---

## Hook Integration

### Claude Code hook (`pre-tool-use`)

Location: `~/proj/.claude/hooks/pre-tool-use/enforce_scitex_patterns.sh`

**Behavior:**
- Triggers on Write/Edit tool for `.py` files
- Runs `stx-lint --json` on the file content
- If errors found → `exit 2` (BLOCKED) with message to stderr
- If warnings only → `exit 0` but print suggestions to stderr
- Skips non-Python files, skips test files

**Message format for agents:**
```
BLOCKED: SciTeX pattern violation

STX-S001: Missing @stx.session decorator on main()
  Add @stx.session to enable reproducible session tracking, auto-CLI, and provenance.

STX-S003: argparse detected — @stx.session auto-generates CLI from function signature.
  Remove `import argparse` and define parameters as function arguments with type hints.

Template:
  @stx.session
  def main(param1="default", CONFIG=stx.session.INJECTED, plt=stx.session.INJECTED):
      ...
      return 0
```

---

## Action Items for scitex-python side

The linter assumes these wrappers exist in scitex-python. Verify or create:

| Function | Status | Notes |
|----------|--------|-------|
| `stx.plt.savefig()` | EXISTS (via `__getattr__` fallback) | Falls through to `matplotlib.pyplot.savefig` — works but loses metadata. Consider explicit wrapper. |
| `stx.plt.show()` | EXISTS (via `__getattr__` fallback) | Falls through to `matplotlib.pyplot.show` |
| `stx.plt.subplots()` | EXISTS (explicit) | Returns FigWrapper/AxisWrapper |
| `stx.io.save(fig, path)` | EXISTS | Full provenance tracking |
| `stx.io.load(path)` | EXISTS | Full provenance tracking |
| `stx.stats.ttest_ind()` | EXISTS | With effect size + CI |
| `stx.stats.recommend_tests()` | EXISTS | Auto test selection |

**TODO (scitex-python):** Consider making `stx.plt.savefig()` an explicit wrapper
that calls `stx.io.save()` internally, rather than falling through to bare matplotlib.
This way `stx.plt.savefig()` gets provenance tracking too, and users keep familiar API.

---

## Open Questions

1. Should `import numpy as np` itself be flagged, or only `np.save`/`np.load`?
   → Decision: Only flag I/O functions, not the import itself. numpy is core.

2. Should `print()` inside session be an error or info?
   → Decision: info (P006). Not blocking, just a suggestion.

3. How to handle multi-file projects where session is in a runner script?
   → Decision: Per-file linting. If a file has `__main__` guard, it needs session.

4. Should the hook block (exit 2) on warnings or only on errors?
   → Decision: Block only on errors (S-category). Warnings printed but not blocking.

<!-- EOF -->