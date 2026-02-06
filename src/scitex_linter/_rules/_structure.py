"""Category S: Structure rules."""

from ._base import Rule

S001 = Rule(
    id="STX-S001",
    severity="error",
    category="structure",
    message="Missing @stx.session decorator on main function",
    suggestion=(
        "Add @stx.session to enable reproducible session tracking, "
        "auto-CLI, and provenance.\n"
        "  @stx.session\n"
        "  def main(...):\n"
        "      return 0"
    ),
    requires="scitex",
)

S002 = Rule(
    id="STX-S002",
    severity="error",
    category="structure",
    message="Missing `if __name__ == '__main__'` guard",
    suggestion="Add `if __name__ == '__main__': main()` at the end of the script.",
)

S003 = Rule(
    id="STX-S003",
    severity="error",
    category="structure",
    message="argparse detected — @stx.session auto-generates CLI from function signature",
    suggestion=(
        "Remove `import argparse` and define parameters as function arguments:\n"
        "  @stx.session\n"
        "  def main(data_path: str, threshold: float = 0.5):\n"
        "      # Auto-generates: --data-path, --threshold"
    ),
    requires="scitex",
)

S004 = Rule(
    id="STX-S004",
    severity="warning",
    category="structure",
    message="@stx.session function should return an integer exit code",
    suggestion="Add `return 0` for success at the end of your session function.",
    requires="scitex",
)

S005 = Rule(
    id="STX-S005",
    severity="warning",
    category="structure",
    message="Missing `import scitex as stx`",
    suggestion="Add `import scitex as stx` to use SciTeX modules.",
    requires="scitex",
)

S006 = Rule(
    id="STX-S006",
    severity="warning",
    category="structure",
    message="@stx.session function missing explicit INJECTED parameters",
    suggestion=(
        "Declare auto-injected values explicitly in the function signature:\n"
        "  @stx.session\n"
        "  def main(\n"
        "      CONFIG=stx.session.INJECTED,\n"
        "      plt=stx.session.INJECTED,\n"
        "      COLORS=stx.session.INJECTED,\n"
        "      rngg=stx.session.INJECTED,\n"
        "      logger=stx.session.INJECTED,\n"
        "  ):\n"
        "      return 0"
    ),
    requires="scitex",
)
