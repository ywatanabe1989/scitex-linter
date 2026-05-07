"""Rule dataclass definition.

Soft-migration shim. The canonical home is `scitex_dev.lint._rules._base`.
This module re-exports `Rule` so existing imports
(`from scitex_linter._rules._base import Rule`) keep working.
"""

from scitex_dev.lint._rules._base import Rule  # noqa: F401

__all__ = ["Rule"]
