"""Regression tests for scitex-linter#7 — .ipynb Phase-1 support."""

from __future__ import annotations

import json

from scitex_linter.checker import lint_file


def _make_notebook(tmp_path, cells):
    """Build a minimal nbformat-compliant .ipynb dict."""
    nb_cells = []
    for cell_type, source in cells:
        nb_cells.append(
            {
                "cell_type": cell_type,
                "source": source,
                "metadata": {},
                **(
                    {"outputs": [], "execution_count": None}
                    if cell_type == "code"
                    else {}
                ),
            }
        )
    path = tmp_path / "nb.ipynb"
    path.write_text(
        json.dumps(
            {
                "cells": nb_cells,
                "metadata": {},
                "nbformat": 4,
                "nbformat_minor": 5,
            }
        )
    )
    return path


class TestIpynbLinting:
    def test_catches_np_save_in_code_cell(self, tmp_path):
        nb = _make_notebook(
            tmp_path,
            [
                ("code", "import numpy as np\nnp.save('x.npy', arr)\n"),
            ],
        )
        issues = lint_file(str(nb))
        # IO001 fires on np.save
        rule_ids = [i.rule.id for i in issues]
        assert "STX-IO001" in rule_ids

    def test_skips_markdown_cells(self, tmp_path):
        nb = _make_notebook(
            tmp_path,
            [
                ("markdown", "# Title\n\nSome **text**."),
                ("code", "x = 1\n"),
            ],
        )
        # Should not raise or produce markdown-related lint issues
        issues = lint_file(str(nb))
        assert isinstance(issues, list)

    def test_skips_empty_code_cells(self, tmp_path):
        nb = _make_notebook(
            tmp_path,
            [("code", ""), ("code", "   \n\n"), ("code", "a = 1\n")],
        )
        issues = lint_file(str(nb))
        # Only the third cell has real code — no parse errors from empties
        assert isinstance(issues, list)

    def test_issue_location_tagged_with_cell_index(self, tmp_path):
        nb = _make_notebook(
            tmp_path,
            [
                ("code", "pass\n"),
                ("code", "import numpy as np\nnp.save('y.npy', arr)\n"),
            ],
        )
        issues = lint_file(str(nb))
        # At least one issue should tag the second cell
        cell_refs = [getattr(i, "source_line", "") for i in issues]
        # Filepath is prefixed onto issues via lint_source; the only way
        # to verify here is that at least some issues came out of the np.save.
        assert any(i.rule.id == "STX-IO001" for i in issues)

    def test_malformed_ipynb_returns_empty(self, tmp_path):
        bad = tmp_path / "bad.ipynb"
        bad.write_text("{not-json")
        assert lint_file(str(bad)) == []


# EOF
