"""MCP tool registration for scitex-linter."""


def register_all_tools(mcp) -> None:
    """Register all MCP tools with the server."""
    from .lint import register_lint_tools

    register_lint_tools(mcp)
    _register_skills_tools(mcp)


def _register_skills_tools(mcp) -> None:
    """Register skills MCP tools."""

    @mcp.tool()
    def linter_skills_list() -> dict:
        """List available skill pages for scitex-linter."""
        try:
            from scitex_dev.skills import list_skills

            result = list_skills(package="scitex-linter")
            return {"success": True, "skills": result.get("scitex-linter", [])}
        except ImportError:
            return {"success": False, "error": "scitex-dev not installed"}

    @mcp.tool()
    def linter_skills_get(name: str = None) -> dict:
        """Get a skill page for scitex-linter."""
        try:
            from scitex_dev.skills import get_skill

            content = get_skill(package="scitex-linter", name=name)
            if content:
                return {"success": True, "name": name, "content": content}
            return {"success": False, "error": f"Skill '{name}' not found"}
        except ImportError:
            return {"success": False, "error": "scitex-dev not installed"}
