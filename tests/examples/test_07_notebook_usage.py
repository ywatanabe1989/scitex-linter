#!/usr/bin/env python3
"""Smoke test: notebook examples/07_notebook_usage.ipynb exists and is valid JSON."""

import json
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples/07_notebook_usage.ipynb"


def test_notebook_valid():
    assert EXAMPLE.is_file(), f"missing example: {EXAMPLE}"
    nb = json.loads(EXAMPLE.read_text())
    assert "cells" in nb, "notebook missing cells"


if __name__ == "__main__":
    test_notebook_valid()
