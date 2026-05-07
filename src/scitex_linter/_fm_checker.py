"""FM (Figure / Millimeter) rule detection — opt-in category.

Soft-migration shim. The canonical home is `scitex_dev.lint._fm_checker`.
"""

from scitex_dev.lint._fm_checker import *  # noqa: F401,F403
from scitex_dev.lint._fm_checker import FMChecker  # noqa: F401

__all__ = ["FMChecker"]
