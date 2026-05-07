"""SciTeX Linter CLI — soft-migration shim.

The canonical home is `scitex_dev.lint.cli`. The `scitex-linter` console
script (registered in `pyproject.toml`) calls `main()` here, which
delegates to the engine.
"""

from scitex_dev.lint.cli import main, main_group  # noqa: F401

__all__ = ["main", "main_group"]
