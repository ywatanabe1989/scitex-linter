"""AST-based checker that detects SciTeX anti-patterns.

Soft-migration shim. The canonical home is `scitex_dev.linter.checker`.
External plugins import ``Issue`` and ``_is_allowed_by_comment`` from this
module — kept as named re-exports for back-compat.
"""

from scitex_dev.linter.checker import *  # noqa: F401,F403
from scitex_dev.linter.checker import (  # noqa: F401  back-compat names
    Issue,
    SciTeXChecker,
    _is_allowed_by_comment,
    is_script,
    lint_file,
    lint_source,
)

__all__ = ["Issue", "SciTeXChecker", "is_script", "lint_file", "lint_source"]
