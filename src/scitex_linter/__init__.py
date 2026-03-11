"""SciTeX Linter — enforce reproducible research patterns via AST analysis."""

__version__ = "0.3.0"


def list_rules(category: str = None) -> list:
    """Return all rules (built-in + plugin), optionally filtered by category.

    Parameters
    ----------
    category : str, optional
        If provided, only return rules whose category matches this value.

    Returns
    -------
    list of Rule
        All matching Rule objects from built-in definitions and loaded plugins.
    """
    from ._plugin_loader import load_plugins
    from ._rules import ALL_RULES

    all_rules = dict(ALL_RULES)
    plugin_rules = load_plugins()["rules"]
    all_rules.update(plugin_rules)

    rules = list(all_rules.values())
    if category is not None:
        rules = [r for r in rules if r.category == category]
    return rules


__all__ = ["list_rules"]
