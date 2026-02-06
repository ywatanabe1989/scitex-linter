"""Lint MCP tools for scitex-linter."""

from typing import Optional


def register_lint_tools(mcp) -> None:
    """Register lint-related MCP tools."""

    @mcp.tool()
    def linter_lint(
        path: str, severity: str = "info", category: Optional[str] = None
    ) -> dict:
        """[linter] Lint a Python file for SciTeX pattern compliance."""
        from ...checker import lint_file
        from ...formatter import to_json
        from ...rules import SEVERITY_ORDER

        issues = lint_file(path)
        min_sev = SEVERITY_ORDER.get(severity, 0)
        categories = set(category.split(",")) if category else None

        issues = [
            i
            for i in issues
            if SEVERITY_ORDER[i.rule.severity] >= min_sev
            and (categories is None or i.rule.category in categories)
        ]

        return to_json(issues, path)

    @mcp.tool()
    def linter_list_rules(
        category: Optional[str] = None, severity: Optional[str] = None
    ) -> dict:
        """[linter] List all available lint rules."""
        from ...rules import ALL_RULES

        rules_list = list(ALL_RULES.values())

        if category:
            cats = set(category.split(","))
            rules_list = [r for r in rules_list if r.category in cats]
        if severity:
            rules_list = [r for r in rules_list if r.severity == severity]

        return {
            "rules": [
                {
                    "id": r.id,
                    "severity": r.severity,
                    "category": r.category,
                    "message": r.message,
                    "suggestion": r.suggestion,
                }
                for r in rules_list
            ],
            "count": len(rules_list),
        }

    @mcp.tool()
    def linter_check_source(source: str, filepath: str = "<stdin>") -> dict:
        """[linter] Lint Python source code string for SciTeX pattern compliance."""
        from ...checker import lint_source
        from ...formatter import to_json

        issues = lint_source(source, filepath=filepath)
        return to_json(issues, filepath)
