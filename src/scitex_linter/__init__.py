"""SciTeX Linter — soft-migration shim.

The engine has moved to `scitex_dev.lint`. This package re-exports the
public API so existing imports (`import scitex_linter`,
`from scitex_linter import list_rules`, etc.) keep working.

The `scitex-linter` console script is also kept as an alias for
`scitex-dev lint`. New work should target `scitex_dev.lint` directly.
"""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _v

    try:
        __version__ = _v("scitex-linter")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"


from scitex_dev.lint import list_rules  # noqa: F401,E402

__all__ = ["__version__", "list_rules"]
