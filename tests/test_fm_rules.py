"""Tests for FM (Figure/Millimeter) rules (OPT-IN category)."""

from scitex_linter.checker import lint_source
from scitex_linter.config import LinterConfig


def _rule_ids(source, filepath="script.py", enable_fm=False):
    """Helper to extract rule IDs from lint results.

    Args:
        source: Python source code to lint
        filepath: Filepath to use for linting
        enable_fm: If True, create config with FM rules enabled

    Returns:
        List of rule IDs found
    """
    config = LinterConfig(enable=["FM"]) if enable_fm else None
    return [i.rule.id for i in lint_source(source, filepath=filepath, config=config)]


# =============================================================================
# FM rules disabled by default
# =============================================================================


class TestFMDisabledByDefault:
    def test_fm001_disabled_by_default(self):
        """FM001 should not fire without enable_fm=True."""
        src = """
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" not in _rule_ids(src, enable_fm=False)

    def test_fm002_disabled_by_default(self):
        """FM002 should not fire without enable_fm=True."""
        src = """
import matplotlib.pyplot as plt

plt.tight_layout()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM002" not in _rule_ids(src, enable_fm=False)

    def test_fm006_disabled_by_default(self):
        """FM006 should not fire without enable_fm=True."""
        src = """
import matplotlib.pyplot as plt

plt.savefig("output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" not in _rule_ids(src, enable_fm=False)


# =============================================================================
# FM001: figsize= parameter
# =============================================================================


class TestFM001Figsize:
    def test_plt_figure_figsize_fires(self):
        """plt.figure(figsize=...) triggers FM001."""
        src = """
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" in _rule_ids(src, enable_fm=True)

    def test_plt_subplots_figsize_fires(self):
        """plt.subplots(figsize=...) triggers FM001."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" in _rule_ids(src, enable_fm=True)

    def test_plt_figure_no_figsize_clean(self):
        """plt.figure() without figsize is clean."""
        src = """
import matplotlib.pyplot as plt

fig = plt.figure()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" not in _rule_ids(src, enable_fm=True)

    def test_stx_plt_subplots_exempt(self):
        """stx.plt.subplots with figsize should not fire."""
        src = """
import scitex as stx

fig, ax = stx.plt.subplots(figsize=(10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM002: tight_layout()
# =============================================================================


class TestFM002TightLayout:
    def test_plt_tight_layout_fires(self):
        """plt.tight_layout() triggers FM002."""
        src = """
import matplotlib.pyplot as plt

plt.tight_layout()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM002" in _rule_ids(src, enable_fm=True)

    def test_fig_tight_layout_fires(self):
        """fig.tight_layout() triggers FM002."""
        src = """
fig.tight_layout()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM002" in _rule_ids(src, enable_fm=True)

    def test_no_tight_layout_clean(self):
        """No tight_layout call is clean."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM002" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM003: bbox_inches="tight"
# =============================================================================


class TestFM003BboxInches:
    def test_plt_savefig_bbox_inches_fires(self):
        """plt.savefig with bbox_inches="tight" triggers FM003."""
        src = """
import matplotlib.pyplot as plt

plt.savefig("x.png", bbox_inches="tight")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM003" in _rule_ids(src, enable_fm=True)

    def test_plt_savefig_no_bbox_clean(self):
        """plt.savefig without bbox_inches is clean."""
        src = """
import matplotlib.pyplot as plt

plt.savefig("x.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM003" not in _rule_ids(src, enable_fm=True)

    def test_stx_io_save_exempt(self):
        """stx.io.save should not trigger FM003."""
        src = """
import scitex as stx

stx.io.save(fig, "x.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM003" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM004: constrained_layout=True
# =============================================================================


class TestFM004ConstrainedLayout:
    def test_plt_subplots_constrained_layout_fires(self):
        """plt.subplots(constrained_layout=True) triggers FM004."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots(constrained_layout=True)

if __name__ == "__main__":
    pass
"""
        assert "STX-FM004" in _rule_ids(src, enable_fm=True)

    def test_plt_subplots_no_constrained_layout_clean(self):
        """plt.subplots() without constrained_layout is clean."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM004" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM005: subplots_adjust()
# =============================================================================


class TestFM005SubplotsAdjust:
    def test_fig_subplots_adjust_fires(self):
        """fig.subplots_adjust() triggers FM005."""
        src = """
fig.subplots_adjust(left=0.1)

if __name__ == "__main__":
    pass
"""
        assert "STX-FM005" in _rule_ids(src, enable_fm=True)

    def test_no_subplots_adjust_clean(self):
        """No subplots_adjust call is clean."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM005" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM006: plt.savefig() / fig.savefig()
# =============================================================================


class TestFM006Savefig:
    def test_plt_savefig_fires(self):
        """plt.savefig() triggers FM006."""
        src = """
import matplotlib.pyplot as plt

plt.savefig("output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" in _rule_ids(src, enable_fm=True)

    def test_fig_savefig_fires(self):
        """fig.savefig() triggers FM006."""
        src = """
fig.savefig("output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" in _rule_ids(src, enable_fm=True)

    def test_stx_io_save_clean(self):
        """stx.io.save() should not trigger FM006."""
        src = """
import scitex as stx

stx.io.save(fig, "output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM007: rcParams modification
# =============================================================================


# =============================================================================
# fr.* namespace exemption
# =============================================================================


class TestFRExemption:
    def test_fr_save_exempt_from_fm006(self):
        """fr.save() should not trigger FM006."""
        src = """
import figrecipe as fr

fr.save(fig, "output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" not in _rule_ids(src, enable_fm=True)

    def test_fr_subplots_figsize_exempt_from_fm001(self):
        """fr.subplots(figsize=...) should not trigger FM001."""
        src = """
import figrecipe as fr

fig, ax = fr.subplots(figsize=(10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM001" not in _rule_ids(src, enable_fm=True)

    def test_fr_sub_module_exempt(self):
        """fr.io.save() should not trigger FM rules."""
        src = """
import figrecipe as fr

fr.io.save(fig, "output.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-FM006" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM007: rcParams modification
# =============================================================================


class TestFM007RcParams:
    def test_plt_rcparams_fires(self):
        """plt.rcParams modification triggers FM007."""
        src = """
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 12

if __name__ == "__main__":
    pass
"""
        assert "STX-FM007" in _rule_ids(src, enable_fm=True)

    def test_mpl_rcparams_fires(self):
        """mpl.rcParams modification triggers FM007."""
        src = """
import matplotlib as mpl

mpl.rcParams["lines.linewidth"] = 1.5

if __name__ == "__main__":
    pass
"""
        assert "STX-FM007" in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM008: set_size_inches()
# =============================================================================


class TestFM008SetSizeInches:
    def test_fig_set_size_inches_fires(self):
        """fig.set_size_inches() triggers FM008."""
        src = """
fig.set_size_inches(10, 8)

if __name__ == "__main__":
    pass
"""
        assert "STX-FM008" in _rule_ids(src, enable_fm=True)

    def test_set_size_inches_with_tuple_fires(self):
        """fig.set_size_inches((10, 8)) triggers FM008."""
        src = """
fig.set_size_inches((10, 8))

if __name__ == "__main__":
    pass
"""
        assert "STX-FM008" in _rule_ids(src, enable_fm=True)

    def test_no_set_size_inches_clean(self):
        """No set_size_inches call is clean."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM008" not in _rule_ids(src, enable_fm=True)

    def test_stx_exempt(self):
        """stx.* set_size_inches is exempt."""
        src = """
import scitex as stx

stx.fig.set_size_inches(10, 8)

if __name__ == "__main__":
    pass
"""
        assert "STX-FM008" not in _rule_ids(src, enable_fm=True)

    def test_fr_exempt(self):
        """fr.* set_size_inches is exempt."""
        src = """
import figrecipe as fr

fr.fig.set_size_inches(10, 8)

if __name__ == "__main__":
    pass
"""
        assert "STX-FM008" not in _rule_ids(src, enable_fm=True)


# =============================================================================
# FM009: ax.set_position()
# =============================================================================


class TestFM009SetPosition:
    def test_ax_set_position_fires(self):
        """ax.set_position() triggers FM009."""
        src = """
ax.set_position([0.1, 0.1, 0.8, 0.8])

if __name__ == "__main__":
    pass
"""
        assert "STX-FM009" in _rule_ids(src, enable_fm=True)

    def test_no_set_position_clean(self):
        """No set_position call is clean."""
        src = """
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

if __name__ == "__main__":
    pass
"""
        assert "STX-FM009" not in _rule_ids(src, enable_fm=True)

    def test_stx_exempt(self):
        """stx.* set_position is exempt."""
        src = """
import scitex as stx

stx.ax.set_position([0.1, 0.1, 0.8, 0.8])

if __name__ == "__main__":
    pass
"""
        assert "STX-FM009" not in _rule_ids(src, enable_fm=True)
