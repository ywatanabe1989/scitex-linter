"""MCP tool registration for scitex-linter."""


def register_all_tools(mcp) -> None:
    """Register all MCP tools with the server."""
    from .lint import register_lint_tools

    register_lint_tools(mcp)
