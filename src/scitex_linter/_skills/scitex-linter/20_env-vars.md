---
description: |
  [TOPIC] Env Vars
  [DETAILS] Environment variables read by scitex-linter at import / runtime. Follow SCITEX_<MODULE>_* convention — see general/10_arch-environment-variables.md.
tags: [scitex-linter-env-vars]
---

# scitex-linter — Environment Variables

| Variable | Purpose | Default | Type |
|---|---|---|---|
| `SCITEX_LINTER_DISABLE` | Disable scitex-linter entirely (opt-out). | `false` | bool |
| `SCITEX_LINTER_ENABLE` | Comma-separated list of rule IDs to force-enable. | unset | string (CSV) |
| `SCITEX_LINTER_SEVERITY` | Minimum severity surfaced (`error` / `warning` / `info`). | `warning` | string |
| `SCITEX_LINTER_EXCLUDE_DIRS` | Extra directories to skip during linting (colon or comma separated). | unset | string (paths) |
| `SCITEX_LINTER_LIBRARY_DIRS` | Directories classified as "library code" (stricter ruleset). | unset | string (paths) |
| `SCITEX_LINTER_LIBRARY_PATTERNS` | Glob patterns matching library files. | `src/**/*.py` | string (glob CSV) |
| `SCITEX_LINTER_SCRIPT_DIRS` | Directories classified as "script code" (relaxed ruleset — allows top-level side effects). | unset | string (paths) |
| `SCITEX_LINTER_REQUIRED_INJECTED` | Comma-separated names the `@stx.session` injection rule must enforce. | `CONFIG,plt,logger` | string (CSV) |

## Feature flags

- **opt-out:** `SCITEX_LINTER_DISABLE=true` turns the linter off globally.
- No opt-in flags.

## Notes

The trailing-underscore matches (`SCITEX_LINTER_`, `SCITEX_LINTER`) in the grep
output are f-string prefixes, not real env vars — filtered out above.

## Audit

```bash
grep -rhoE 'SCITEX_[A-Z0-9_]+' $HOME/proj/scitex-linter/src/ | sort -u
```
