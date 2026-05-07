"""Rule definitions — soft-migration shim.

The canonical home is `scitex_dev.linter._rules`. This re-exports all
rule symbols so existing imports
(`from scitex_linter._rules import ALL_RULES, Rule, …`) keep working.
"""

from scitex_dev.linter._rules import *  # noqa: F401,F403
from scitex_dev.linter._rules import ALL_RULES, SEVERITY_ORDER, Rule  # noqa: F401

__all__ = ["ALL_RULES", "Rule", "SEVERITY_ORDER"]
