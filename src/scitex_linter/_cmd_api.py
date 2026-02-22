"""CLI handler for the 'api' subcommand."""

import json
import sys

# (module, kind, name, signature)
# kind: F=Function, C=Class, V=Variable
_PUBLIC_API = [
    (
        "scitex_linter.checker",
        "F",
        "lint_file",
        "(filepath, config=None) -> list[Issue]",
    ),
    (
        "scitex_linter.checker",
        "F",
        "lint_source",
        "(source, filepath, config=None) -> list[Issue]",
    ),
    ("scitex_linter.checker", "F", "is_script", "(filepath, config=None) -> bool"),
    ("scitex_linter.checker", "C", "Issue", "(rule, line, col, source_line)"),
    (
        "scitex_linter.fixer",
        "F",
        "fix_source",
        "(source, filepath, config=None) -> str",
    ),
    (
        "scitex_linter.fixer",
        "F",
        "fix_file",
        "(filepath, write=True, config=None) -> tuple",
    ),
    (
        "scitex_linter.formatter",
        "F",
        "format_issue",
        "(issue, filepath, color=False) -> str",
    ),
    (
        "scitex_linter.formatter",
        "F",
        "format_summary",
        "(issues, filepath, color=False) -> str",
    ),
    ("scitex_linter.formatter", "F", "to_json", "(issues, filepath) -> list[dict]"),
    ("scitex_linter.rules", "V", "ALL_RULES", "dict[str, Rule]"),
    ("scitex_linter.rules", "V", "SEVERITY_ORDER", "dict[str, int]"),
    ("scitex_linter.config", "C", "LinterConfig", "dataclass (load via load_config())"),
]


def register(subparsers) -> None:
    p = subparsers.add_parser(
        "api",
        help="List public Python API",
        description="List all public Python API functions and classes.",
    )
    p.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    p.set_defaults(func=_cmd_api)


def _cmd_api(args) -> int:
    if args.as_json:
        data = [
            {"module": m, "kind": k, "name": n, "signature": s}
            for m, k, n, s in _PUBLIC_API
        ]
        print(json.dumps(data, indent=2))
        return 0

    use_color = sys.stdout.isatty()
    cyan = "\033[96m" if use_color else ""
    green = "\033[92m" if use_color else ""
    yellow = "\033[93m" if use_color else ""
    blue = "\033[94m" if use_color else ""
    reset = "\033[0m" if use_color else ""

    kind_color = {"F": green, "C": yellow, "V": blue}

    print(f"API tree of scitex_linter ({len(_PUBLIC_API)} items):")
    print("Legend: [M]=Module [C]=Class [F]=Function [V]=Variable")

    current_mod = None
    for mod, kind, name, sig in _PUBLIC_API:
        if mod != current_mod:
            print(f"{cyan}[M] {mod}{reset}")
            current_mod = mod
        kc = kind_color.get(kind, "")
        sep = "" if sig.startswith("(") else " "
        print(f"  {kc}[{kind}]{reset} {name}{sep}{sig}")

    return 0
