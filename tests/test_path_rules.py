"""Tests for path linting rules (PA001-PA005)."""

from scitex_linter.checker import lint_source


def _rule_ids(source, filepath="script.py"):
    return [i.rule.id for i in lint_source(source, filepath=filepath)]


# =========================================================================
# PA001: Absolute path in stx.io calls
# =========================================================================


class TestPA001:
    def test_absolute_path_save_fires(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "/tmp/out.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA001" in _rule_ids(src)

    def test_absolute_path_load_fires(self):
        src = (
            "import scitex as stx\n"
            'data = stx.io.load("/home/user/data.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA001" in _rule_ids(src)

    def test_relative_path_clean(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "./out.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA001" not in _rule_ids(src)


# =========================================================================
# PA002: open() detected
# =========================================================================


class TestPA002:
    def test_open_in_session_fires(self):
        src = (
            "import scitex as stx\n\n"
            "@stx.session\n"
            "def main():\n"
            '    f = open("data.txt", "r")\n'
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        assert "STX-PA002" in _rule_ids(src)

    def test_open_without_session_clean(self):
        src = (
            "import scitex as stx\n\n"
            "def main():\n"
            '    f = open("data.txt", "r")\n'
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        assert "STX-PA002" not in _rule_ids(src)


# =========================================================================
# PA003: os.makedirs / Path.mkdir
# =========================================================================


class TestPA003:
    def test_os_makedirs_fires(self):
        src = (
            "import os\nos.makedirs(\"output\")\nif __name__ == '__main__':\n    pass\n"
        )
        assert "STX-PA003" in _rule_ids(src)

    def test_path_mkdir_fires(self):
        src = (
            "from pathlib import Path\n"
            'Path("output").mkdir(exist_ok=True)\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA003" in _rule_ids(src)


# =========================================================================
# PA004: os.chdir
# =========================================================================


class TestPA004:
    def test_os_chdir_fires(self):
        src = "import os\nos.chdir(\"/tmp\")\nif __name__ == '__main__':\n    pass\n"
        assert "STX-PA004" in _rule_ids(src)


# =========================================================================
# PA005: Missing ./ prefix in stx.io calls
# =========================================================================


class TestPA005:
    def test_bare_filename_fires(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "results.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" in _rule_ids(src)

    def test_bare_subdir_fires(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "data/results.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" in _rule_ids(src)

    def test_dot_slash_clean(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "./results.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" not in _rule_ids(src)

    def test_dot_dot_slash_clean(self):
        src = (
            "import scitex as stx\n"
            'stx.io.save(df, "../shared/results.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" not in _rule_ids(src)

    def test_load_bare_fires(self):
        src = (
            "import scitex as stx\n"
            'data = stx.io.load("input.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" in _rule_ids(src)

    def test_load_dot_slash_clean(self):
        src = (
            "import scitex as stx\n"
            'data = stx.io.load("./input.csv")\n'
            "if __name__ == '__main__':\n"
            "    pass\n"
        )
        assert "STX-PA005" not in _rule_ids(src)
