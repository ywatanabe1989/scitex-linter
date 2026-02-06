"""Tests for Phase 2 call-level rules (IO, Plot, Stats)."""

from scitex_linter.checker import lint_source


def _rule_ids(source, filepath="script.py"):
    return [i.rule.id for i in lint_source(source, filepath=filepath)]


# =========================================================================
# IO001: np.save()
# =========================================================================


class TestIO001:
    def test_np_save_fires(self):
        src = """
import numpy as np

np.save("data.npy", arr)

if __name__ == "__main__":
    pass
"""
        assert "STX-IO001" in _rule_ids(src)

    def test_stx_io_save_clean(self):
        src = """
import scitex as stx

stx.io.save(arr, "data.npy")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO001" not in _rule_ids(src)


# =========================================================================
# IO002: np.load()
# =========================================================================


class TestIO002:
    def test_np_load_fires(self):
        src = """
import numpy as np

data = np.load("data.npy")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO002" in _rule_ids(src)


# =========================================================================
# IO003: pd.read_csv()
# =========================================================================


class TestIO003:
    def test_pd_read_csv_fires(self):
        src = """
import pandas as pd

df = pd.read_csv("data.csv")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO003" in _rule_ids(src)


# =========================================================================
# IO004: df.to_csv()
# =========================================================================


class TestIO004:
    def test_to_csv_fires(self):
        src = """
df.to_csv("output.csv")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO004" in _rule_ids(src)

    def test_stx_not_flagged(self):
        src = """
import scitex as stx

stx.io.save(df, "output.csv")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO004" not in _rule_ids(src)


# =========================================================================
# IO005: pickle.dump()
# =========================================================================


class TestIO005:
    def test_pickle_dump_fires(self):
        src = """
import pickle

pickle.dump(obj, f)

if __name__ == "__main__":
    pass
"""
        assert "STX-IO005" in _rule_ids(src)


# =========================================================================
# IO006: json.dump()
# =========================================================================


class TestIO006:
    def test_json_dump_fires(self):
        src = """
import json

json.dump(data, f)

if __name__ == "__main__":
    pass
"""
        assert "STX-IO006" in _rule_ids(src)


# =========================================================================
# IO007: plt.savefig()
# =========================================================================


class TestIO007:
    def test_plt_savefig_fires(self):
        src = """
import matplotlib.pyplot as plt

plt.savefig("fig.png")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO007" in _rule_ids(src)


# =========================================================================
# P001: ax.plot() hint
# =========================================================================


class TestP001:
    def test_ax_plot_hint(self):
        src = """
ax.plot(x, y)

if __name__ == "__main__":
    pass
"""
        assert "STX-P001" in _rule_ids(src)

    def test_ax_stx_line_clean(self):
        src = """
ax.stx_line(x, y)

if __name__ == "__main__":
    pass
"""
        assert "STX-P001" not in _rule_ids(src)

    def test_np_plot_not_flagged(self):
        """np.plot doesn't exist but should not trigger axes hint."""
        src = """
import numpy as np

np.plot(x)

if __name__ == "__main__":
    pass
"""
        assert "STX-P001" not in _rule_ids(src)


# =========================================================================
# P002: ax.scatter() hint
# =========================================================================


class TestP002:
    def test_ax_scatter_hint(self):
        src = """
ax.scatter(x, y)

if __name__ == "__main__":
    pass
"""
        assert "STX-P002" in _rule_ids(src)


# =========================================================================
# P003: ax.bar() hint
# =========================================================================


class TestP003:
    def test_ax_bar_hint(self):
        src = """
ax.bar(x, y)

if __name__ == "__main__":
    pass
"""
        assert "STX-P003" in _rule_ids(src)


# =========================================================================
# P004: plt.show()
# =========================================================================


class TestP004:
    def test_plt_show_fires(self):
        src = """
import matplotlib.pyplot as plt

plt.show()

if __name__ == "__main__":
    pass
"""
        assert "STX-P004" in _rule_ids(src)


# =========================================================================
# P005: print() inside @stx.session
# =========================================================================


class TestP005:
    def test_print_in_session_fires(self):
        src = """
import scitex as stx

@stx.session
def main():
    print("hello")
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-P005" in _rule_ids(src)

    def test_print_without_session_clean(self):
        src = """
def helper():
    print("hello")

if __name__ == "__main__":
    helper()
"""
        assert "STX-P005" not in _rule_ids(src)


# =========================================================================
# ST001-ST006: scipy.stats calls
# =========================================================================


class TestSTRules:
    def test_scipy_stats_ttest_ind(self):
        src = """
from scipy import stats

stats.ttest_ind(a, b)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST001" in _rule_ids(src)

    def test_scipy_stats_mannwhitneyu(self):
        src = """
from scipy import stats

stats.mannwhitneyu(a, b)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST002" in _rule_ids(src)

    def test_scipy_stats_pearsonr(self):
        src = """
from scipy import stats

stats.pearsonr(a, b)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST003" in _rule_ids(src)

    def test_scipy_stats_f_oneway(self):
        src = """
from scipy import stats

stats.f_oneway(a, b, c)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST004" in _rule_ids(src)

    def test_scipy_stats_wilcoxon(self):
        src = """
from scipy import stats

stats.wilcoxon(a, b)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST005" in _rule_ids(src)

    def test_scipy_stats_kruskal(self):
        src = """
from scipy import stats

stats.kruskal(a, b, c)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST006" in _rule_ids(src)

    def test_stx_stats_clean(self):
        src = """
import scitex as stx

stx.stats.ttest_ind(a, b)

if __name__ == "__main__":
    pass
"""
        assert "STX-ST001" not in _rule_ids(src)


# =========================================================================
# Alias resolution
# =========================================================================


class TestAliasResolution:
    def test_aliased_numpy_save(self):
        src = """
import numpy as np

np.save("data.npy", arr)

if __name__ == "__main__":
    pass
"""
        assert "STX-IO001" in _rule_ids(src)

    def test_aliased_pandas_read_csv(self):
        src = """
import pandas as pd

pd.read_csv("data.csv")

if __name__ == "__main__":
    pass
"""
        assert "STX-IO003" in _rule_ids(src)
