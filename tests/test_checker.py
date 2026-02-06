"""Tests for scitex_linter.checker — Phase 1 rules."""

from scitex_linter.checker import lint_source


def _rule_ids(source, filepath="script.py"):
    return [i.rule.id for i in lint_source(source, filepath=filepath)]


# =========================================================================
# S001: Missing @stx.session
# =========================================================================


class TestS001:
    def test_missing_session_fires(self):
        src = """
import scitex as stx

def main():
    pass

if __name__ == "__main__":
    main()
"""
        assert "STX-S001" in _rule_ids(src)

    def test_with_session_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S001" not in _rule_ids(src)

    def test_bare_session_clean(self):
        src = """
import scitex as stx

@session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S001" not in _rule_ids(src)

    def test_library_module_exempt(self):
        src = """
def helper():
    pass
"""
        # No __main__ guard => treated as library if is_script still true
        # but S001 only fires when has_main_guard and no session
        assert "STX-S001" not in _rule_ids(src)


# =========================================================================
# S002: Missing __main__ guard
# =========================================================================


class TestS002:
    def test_missing_guard_fires(self):
        src = """
import scitex as stx

def main():
    pass
"""
        assert "STX-S002" in _rule_ids(src)

    def test_with_guard_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S002" not in _rule_ids(src)

    def test_init_py_exempt(self):
        src = """
def helper():
    pass
"""
        assert "STX-S002" not in _rule_ids(src, filepath="__init__.py")

    def test_test_file_exempt(self):
        src = """
def test_something():
    pass
"""
        assert "STX-S002" not in _rule_ids(src, filepath="test_foo.py")


# =========================================================================
# S003: argparse detected
# =========================================================================


class TestS003:
    def test_import_argparse_fires(self):
        src = """
import argparse

if __name__ == "__main__":
    pass
"""
        assert "STX-S003" in _rule_ids(src)

    def test_from_argparse_fires(self):
        src = """
from argparse import ArgumentParser

if __name__ == "__main__":
    pass
"""
        assert "STX-S003" in _rule_ids(src)

    def test_no_argparse_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S003" not in _rule_ids(src)


# =========================================================================
# S004: Session function should return int
# =========================================================================


class TestS004:
    def test_no_return_fires(self):
        src = """
import scitex as stx

@stx.session
def main():
    pass

if __name__ == "__main__":
    main()
"""
        assert "STX-S004" in _rule_ids(src)

    def test_return_0_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S004" not in _rule_ids(src)

    def test_return_1_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 1

if __name__ == "__main__":
    main()
"""
        assert "STX-S004" not in _rule_ids(src)


# =========================================================================
# S005: Missing import scitex as stx
# =========================================================================


class TestS005:
    def test_missing_stx_import_fires(self):
        src = """
def main():
    pass

if __name__ == "__main__":
    main()
"""
        assert "STX-S005" in _rule_ids(src)

    def test_has_stx_import_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S005" not in _rule_ids(src)


# =========================================================================
# I001: matplotlib.pyplot
# =========================================================================


class TestI001:
    def test_import_matplotlib_pyplot(self):
        src = """
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pass
"""
        assert "STX-I001" in _rule_ids(src)

    def test_from_matplotlib_import_pyplot(self):
        src = """
from matplotlib import pyplot

if __name__ == "__main__":
    pass
"""
        assert "STX-I001" in _rule_ids(src)

    def test_from_matplotlib_pyplot_import_star(self):
        src = """
from matplotlib.pyplot import subplots

if __name__ == "__main__":
    pass
"""
        assert "STX-I001" in _rule_ids(src)

    def test_stx_plt_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    fig, ax = stx.plt.subplots()
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-I001" not in _rule_ids(src)


# =========================================================================
# I002: scipy.stats
# =========================================================================


class TestI002:
    def test_from_scipy_import_stats(self):
        src = """
from scipy import stats

if __name__ == "__main__":
    pass
"""
        assert "STX-I002" in _rule_ids(src)

    def test_from_scipy_stats_import_func(self):
        src = """
from scipy.stats import ttest_ind

if __name__ == "__main__":
    pass
"""
        assert "STX-I002" in _rule_ids(src)

    def test_stx_stats_clean(self):
        src = """
import scitex as stx

@stx.session
def main():
    stx.stats.ttest_ind(a, b)
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-I002" not in _rule_ids(src)


# =========================================================================
# I003: pickle
# =========================================================================


class TestI003:
    def test_import_pickle_fires(self):
        src = """
import pickle

if __name__ == "__main__":
    pass
"""
        assert "STX-I003" in _rule_ids(src)


# =========================================================================
# I006: random
# =========================================================================


class TestI006:
    def test_import_random_fires(self):
        src = """
import random

if __name__ == "__main__":
    pass
"""
        assert "STX-I006" in _rule_ids(src)


# =========================================================================
# I007: logging
# =========================================================================


class TestI007:
    def test_import_logging_fires(self):
        src = """
import logging

if __name__ == "__main__":
    pass
"""
        assert "STX-I007" in _rule_ids(src)


# =========================================================================
# S006: Missing INJECTED parameters
# =========================================================================


class TestS006:
    def test_missing_injected_fires(self):
        src = """
import scitex as stx

@stx.session
def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S006" in _rule_ids(src)

    def test_partial_injected_fires(self):
        src = """
import scitex as stx

@stx.session
def main(CONFIG=stx.session.INJECTED, plt=stx.session.INJECTED):
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S006" in _rule_ids(src)

    def test_all_injected_clean(self):
        src = """
import scitex as stx

@stx.session
def main(
    CONFIG=stx.session.INJECTED,
    plt=stx.session.INJECTED,
    COLORS=stx.session.INJECTED,
    rngg=stx.session.INJECTED,
    logger=stx.session.INJECTED,
):
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S006" not in _rule_ids(src)

    def test_no_session_no_s006(self):
        """S006 should not fire on functions without @stx.session."""
        src = """
import scitex as stx

def main():
    return 0

if __name__ == "__main__":
    main()
"""
        assert "STX-S006" not in _rule_ids(src)


# =========================================================================
# Clean script (golden path)
# =========================================================================


class TestCleanScript:
    def test_perfect_script_no_issues(self):
        src = """
import scitex as stx

@stx.session
def main(
    data_path="input.csv",
    CONFIG=stx.session.INJECTED,
    plt=stx.session.INJECTED,
    COLORS=stx.session.INJECTED,
    rngg=stx.session.INJECTED,
    logger=stx.session.INJECTED,
):
    fig, ax = stx.plt.subplots()
    return 0

if __name__ == "__main__":
    main()
"""
        issues = lint_source(src, filepath="script.py")
        assert len(issues) == 0


# =========================================================================
# CLI exit codes
# =========================================================================


class TestExitCodes:
    def test_clean_returns_0(self):
        from scitex_linter.cli import main as cli_main

        src = """
import scitex as stx

@stx.session
def main(
    CONFIG=stx.session.INJECTED,
    plt=stx.session.INJECTED,
    COLORS=stx.session.INJECTED,
    rngg=stx.session.INJECTED,
    logger=stx.session.INJECTED,
):
    return 0

if __name__ == "__main__":
    main()
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = cli_main(["lint", f.name, "--no-color"])
                assert code == 0
            finally:
                os.unlink(f.name)

    def test_errors_return_2(self):
        from scitex_linter.cli import main as cli_main

        src = """
import argparse

if __name__ == "__main__":
    pass
"""
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = cli_main(["lint", f.name, "--no-color"])
                assert code == 2
            finally:
                os.unlink(f.name)
