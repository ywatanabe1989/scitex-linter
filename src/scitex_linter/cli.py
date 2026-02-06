"""CLI entry point for scitex-linter.

Usage:
    scitex-linter check <path> [--json] [--severity] [--category] [--no-color]
    scitex-linter format <path> [--check] [--diff]
    scitex-linter python <script.py> [--strict] [-- script_args...]
    scitex-linter rule [--json] [--category] [--severity]
    scitex-linter mcp start
    scitex-linter mcp list-tools
    scitex-linter --help-recursive
"""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from ._cmd_format import register as _register_format
from .checker import lint_file
from .formatter import format_issue, format_summary, to_json
from .rules import ALL_RULES, SEVERITY_ORDER

# =========================================================================
# File collection helper
# =========================================================================


def _collect_files(path: Path, recursive: bool = True) -> list:
    """Collect Python files from a path."""
    if path.is_file():
        return [path]
    if path.is_dir():
        pattern = "**/*.py" if recursive else "*.py"
        skip = {"__pycache__", ".git", "node_modules", ".tox", "venv", ".venv"}
        return sorted(
            p for p in path.glob(pattern) if not any(s in p.parts for s in skip)
        )
    return []


# =========================================================================
# Subcommand: check
# =========================================================================


def _register_check(subparsers) -> None:
    p = subparsers.add_parser(
        "check",
        help="Check Python files for SciTeX pattern compliance",
        description="Check Python files for SciTeX pattern compliance.",
    )
    p.add_argument("path", help="Python file or directory to check")
    p.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    p.add_argument("--no-color", action="store_true", help="Disable colored output")
    p.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="info",
        help="Minimum severity to report (default: info)",
    )
    p.add_argument(
        "--category",
        help="Filter by category (comma-separated: structure,import,io,plot,stats)",
    )
    p.set_defaults(func=_cmd_check)


def _cmd_check(args) -> int:
    use_color = not args.no_color and sys.stdout.isatty()
    min_sev = SEVERITY_ORDER[args.severity]
    categories = set(args.category.split(",")) if args.category else None

    target = Path(args.path)
    if not target.exists():
        print(f"Error: {args.path} not found", file=sys.stderr)
        return 2

    files = _collect_files(target)
    if not files:
        print(f"No Python files found in {args.path}", file=sys.stderr)
        return 0

    all_results = {}
    for f in files:
        issues = lint_file(str(f))
        issues = [
            i
            for i in issues
            if SEVERITY_ORDER[i.rule.severity] >= min_sev
            and (categories is None or i.rule.category in categories)
        ]
        if issues:
            all_results[str(f)] = issues

    # JSON output
    if args.as_json:
        combined = {fp: to_json(issues, fp) for fp, issues in all_results.items()}
        print(json.dumps(combined, indent=2))
        has_errors = any(
            any(i.rule.severity == "error" for i in issues)
            for issues in all_results.values()
        )
        return 2 if has_errors else (1 if all_results else 0)

    # Terminal output
    if not all_results:
        msg = "All files clean"
        if use_color:
            print(f"\033[92m{msg}\033[0m")
        else:
            print(msg)
        return 0

    has_errors = False
    for filepath, issues in all_results.items():
        for issue in issues:
            print(format_issue(issue, filepath, color=use_color))
            if issue.rule.severity == "error":
                has_errors = True
        print(format_summary(issues, filepath, color=use_color))
        print()

    return 2 if has_errors else 1


# =========================================================================
# Subcommand: python (lint then execute)
# =========================================================================


def _register_python(subparsers) -> None:
    p = subparsers.add_parser(
        "python",
        help="Lint then execute a Python script",
        description=(
            "Lint a Python script, then execute it.\n"
            "Use -- to separate script arguments: scitex-linter python script.py -- --arg1"
        ),
    )
    p.add_argument("script", help="Python script to run")
    p.add_argument("--strict", action="store_true", help="Abort on lint errors")
    p.set_defaults(func=_cmd_python)


def _cmd_python(args) -> int:
    from .runner import run_script

    # Extract script args: everything after -- in sys.argv (or test argv)
    # argparse already consumed known flags; remaining unknown args go to script
    script_args = getattr(args, "_script_args", [])
    return run_script(args.script, strict=args.strict, script_args=script_args)


# =========================================================================
# Subcommand: rule
# =========================================================================


def _register_rule(subparsers) -> None:
    p = subparsers.add_parser(
        "rule",
        help="List all lint rules",
        description="List all available SciTeX lint rules.",
    )
    p.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    p.add_argument(
        "--category",
        help="Filter by category (comma-separated: structure,import,io,plot,stats)",
    )
    p.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        help="Filter by severity",
    )
    p.set_defaults(func=_cmd_rule)


def _cmd_rule(args) -> int:
    categories = set(args.category.split(",")) if args.category else None
    rules_list = list(ALL_RULES.values())

    if categories:
        rules_list = [r for r in rules_list if r.category in categories]
    if args.severity:
        rules_list = [r for r in rules_list if r.severity == args.severity]

    if args.as_json:
        data = [
            {
                "id": r.id,
                "severity": r.severity,
                "category": r.category,
                "message": r.message,
                "suggestion": r.suggestion,
            }
            for r in rules_list
        ]
        print(json.dumps(data, indent=2))
        return 0

    use_color = sys.stdout.isatty()
    sev_color = {"error": "\033[91m", "warning": "\033[93m", "info": "\033[94m"}
    reset = "\033[0m"

    for r in rules_list:
        if use_color:
            c = sev_color.get(r.severity, "")
            print(f"  {c}{r.id}{reset}  [{r.severity}]  {r.message}")
        else:
            print(f"  {r.id}  [{r.severity}]  {r.message}")

    print(f"\n  {len(rules_list)} rules")
    return 0


# =========================================================================
# Subcommand: mcp
# =========================================================================


def _register_mcp(subparsers) -> None:
    p = subparsers.add_parser(
        "mcp",
        help="MCP server commands",
        description="Manage the scitex-linter MCP server.",
    )
    mcp_sub = p.add_subparsers(dest="mcp_command")

    start_p = mcp_sub.add_parser("start", help="Start the MCP server (stdio)")
    start_p.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport mode (default: stdio)",
    )
    start_p.set_defaults(func=_cmd_mcp_start)

    list_p = mcp_sub.add_parser("list-tools", help="List available MCP tools")
    list_p.set_defaults(func=_cmd_mcp_list_tools)

    doctor_p = mcp_sub.add_parser("doctor", help="Check MCP server health")
    doctor_p.set_defaults(func=_cmd_mcp_doctor)

    install_p = mcp_sub.add_parser(
        "installation", help="Show Claude Desktop configuration"
    )
    install_p.set_defaults(func=_cmd_mcp_installation)

    p.set_defaults(func=lambda args: _cmd_mcp_help(p, args))


def _cmd_mcp_help(parser, args) -> int:
    if not hasattr(args, "mcp_command") or args.mcp_command is None:
        parser.print_help()
        return 0
    return 0


def _cmd_mcp_start(args) -> int:
    try:
        from ._server import run_server

        run_server(transport=args.transport)
        return 0
    except ImportError:
        print(
            "fastmcp is required for MCP server. "
            "Install with: pip install scitex-linter[mcp]",
            file=sys.stderr,
        )
        return 1


def _cmd_mcp_list_tools(args) -> int:
    tools = [
        ("linter_check", "Check a Python file for SciTeX pattern compliance"),
        ("linter_list_rules", "List all available lint rules"),
        ("linter_check_source", "Lint Python source code string"),
    ]
    for name, desc in tools:
        print(f"  {name:30s} {desc}")
    print(f"\n  {len(tools)} tools")
    return 0


def _cmd_mcp_doctor(args) -> int:
    import shutil

    print(f"scitex-linter {__version__}\n")
    print("Health Check")
    print("=" * 40)

    checks = []

    try:
        import fastmcp

        checks.append(("fastmcp", True, fastmcp.__version__))
    except ImportError:
        checks.append(("fastmcp", False, "not installed"))

    try:
        from ._mcp.tools import register_all_tools  # noqa: F401

        checks.append(("MCP tools", True, "3 tools"))
    except Exception as e:
        checks.append(("MCP tools", False, str(e)))

    cli_path = shutil.which("scitex-linter")
    if cli_path:
        checks.append(("CLI", True, cli_path))
    else:
        checks.append(("CLI", False, "not in PATH"))

    rule_count = len(ALL_RULES)
    checks.append(("Rules", True, f"{rule_count} rules"))

    all_ok = True
    for name, ok, info in checks:
        status = "\u2713" if ok else "\u2717"
        if not ok:
            all_ok = False
        print(f"  {status} {name}: {info}")

    print()
    if all_ok:
        print("All checks passed!")
    else:
        print("Some checks failed. Run 'pip install scitex-linter[mcp]' to fix.")

    return 0 if all_ok else 1


def _cmd_mcp_installation(args) -> int:
    import shutil

    print(f"scitex-linter {__version__}\n")
    print("Add this to your Claude Desktop config file:\n")
    print("  macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("  Linux: ~/.config/Claude/claude_desktop_config.json\n")

    cli_path = shutil.which("scitex-linter")
    if cli_path:
        print(f"Your installation path: {cli_path}\n")

    config = (
        "{\n"
        '  "mcpServers": {\n'
        '    "scitex-linter": {\n'
        f'      "command": "{cli_path or "scitex-linter"}",\n'
        '      "args": ["mcp", "start"]\n'
        "    }\n"
        "  }\n"
        "}"
    )
    print(config)
    return 0


# =========================================================================
# --help-recursive
# =========================================================================


def _print_help_recursive(parser, subparsers_actions) -> None:
    """Print help for all commands recursively."""
    cyan = "\033[96m" if sys.stdout.isatty() else ""
    bold = "\033[1m" if sys.stdout.isatty() else ""
    reset = "\033[0m" if sys.stdout.isatty() else ""

    bar = "\u2501" * 3
    print(f"\n{cyan}{bar} scitex-linter {bar}{reset}\n")
    parser.print_help()

    for action in subparsers_actions:
        for choice, subparser in action.choices.items():
            print(f"\n{cyan}{bar} scitex-linter {choice} {bar}{reset}\n")
            subparser.print_help()

            # Nested subparsers (e.g., mcp -> start, list-tools)
            if subparser._subparsers is not None:
                for sub_action in subparser._subparsers._group_actions:
                    if not hasattr(sub_action, "choices") or not sub_action.choices:
                        continue
                    for sub_choice, sub_subparser in sub_action.choices.items():
                        print(
                            f"\n{cyan}{bar} scitex-linter {choice} {sub_choice} {bar}{reset}\n"
                        )
                        sub_subparser.print_help()


# =========================================================================
# Main entry point
# =========================================================================


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scitex-linter",
        description="SciTeX Linter \u2014 enforce reproducible research patterns",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--help-recursive",
        action="store_true",
        help="Show help for all commands",
    )

    subparsers = parser.add_subparsers(dest="command")

    _register_check(subparsers)
    _register_format(subparsers)
    _register_python(subparsers)
    _register_rule(subparsers)
    _register_mcp(subparsers)

    # Split on -- to capture script args for the 'python' subcommand
    raw = argv if argv is not None else sys.argv[1:]
    script_args = []
    if "--" in raw:
        idx = raw.index("--")
        script_args = raw[idx + 1 :]
        raw = raw[:idx]

    args = parser.parse_args(raw)

    # Attach script_args for the run subcommand
    args._script_args = script_args

    if args.help_recursive:
        subparsers_actions = [
            a for a in parser._subparsers._group_actions if hasattr(a, "choices")
        ]
        _print_help_recursive(parser, subparsers_actions)
        return 0

    if args.command is None:
        parser.print_help()
        return 0

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
