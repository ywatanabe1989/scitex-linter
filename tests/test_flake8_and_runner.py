"""Tests for flake8 plugin (Phase 3) and runner (Phase 4)."""

import ast
import os
import tempfile

from scitex_linter.flake8_plugin import SciTeXFlake8Checker
from scitex_linter.runner import run_script

# =========================================================================
# Phase 3: flake8 plugin
# =========================================================================


class TestFlake8Plugin:
    def test_yields_issues(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        tree = ast.parse(src)
        lines = src.splitlines(True)
        checker = SciTeXFlake8Checker(tree, filename="script.py", lines=lines)
        results = list(checker.run())
        codes = [r[2].split()[0] for r in results]
        assert "STXS003" in codes

    def test_clean_yields_nothing(self):
        src = (
            "import scitex as stx\n\n"
            "@stx.session\n"
            "def main():\n"
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        tree = ast.parse(src)
        lines = src.splitlines(True)
        checker = SciTeXFlake8Checker(tree, filename="script.py", lines=lines)
        results = list(checker.run())
        assert len(results) == 0

    def test_format_is_tuple(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        tree = ast.parse(src)
        lines = src.splitlines(True)
        checker = SciTeXFlake8Checker(tree, filename="script.py", lines=lines)
        for result in checker.run():
            assert isinstance(result, tuple)
            assert len(result) == 4
            line, col, msg, cls = result
            assert isinstance(line, int)
            assert isinstance(col, int)
            assert isinstance(msg, str)
            assert msg.startswith("STX")


# =========================================================================
# Phase 4: run_script function
# =========================================================================


class TestRunner:
    def test_strict_blocks_on_errors(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = run_script(f.name, strict=True)
                assert code == 2
            finally:
                os.unlink(f.name)

    def test_clean_runs_script(self):
        src = "pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = run_script(f.name)
                assert code == 0
            finally:
                os.unlink(f.name)
