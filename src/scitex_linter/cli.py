"""SciTeX Linter CLI — soft-migration shim.

The canonical home is `scitex_dev.linter.cli`. The `scitex-linter` console
script (registered in `pyproject.toml`) calls `main()` here, which
delegates to the engine.
"""

from scitex_dev.linter.cli import main, main_group  # noqa: F401

__all__ = ["main", "main_group"]
