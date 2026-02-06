"""Tests for CLI subcommand structure."""

import os
import tempfile

from scitex_linter.cli import main


class TestMainCLI:
    def test_no_args_returns_0(self):
        code = main([])
        assert code == 0

    def test_version(self, capsys):
        try:
            main(["--version"])
        except SystemExit as e:
            assert e.code == 0
        out = capsys.readouterr().out
        assert "scitex-linter" in out

    def test_help_recursive(self, capsys):
        code = main(["--help-recursive"])
        out = capsys.readouterr().out
        assert "lint" in out
        assert "python" in out
        assert "list-rules" in out
        assert "mcp" in out
        assert code == 0


class TestLintSubcommand:
    def test_lint_file(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["lint", f.name])
                assert code == 2  # has errors
            finally:
                os.unlink(f.name)

    def test_lint_clean_file(self):
        src = (
            "import scitex as stx\n\n"
            "@stx.session\n"
            "def main(\n"
            "    CONFIG=stx.session.INJECTED,\n"
            "    plt=stx.session.INJECTED,\n"
            "    COLORS=stx.session.INJECTED,\n"
            "    rngg=stx.session.INJECTED,\n"
            "    logger=stx.session.INJECTED,\n"
            "):\n"
            "    return 0\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["lint", f.name])
                assert code == 0
            finally:
                os.unlink(f.name)

    def test_lint_json(self, capsys):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["lint", f.name, "--json"])
                out = capsys.readouterr().out
                assert "STX-S003" in out
                assert code == 2
            finally:
                os.unlink(f.name)

    def test_lint_severity_filter(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["lint", f.name, "--severity", "error"])
                assert code == 2
            finally:
                os.unlink(f.name)

    def test_lint_not_found(self):
        code = main(["lint", "/nonexistent/path.py"])
        assert code == 2


class TestPythonSubcommand:
    def test_python_clean_script(self):
        src = "pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["python", f.name])
                assert code == 0
            finally:
                os.unlink(f.name)

    def test_python_strict_blocks(self):
        src = "import argparse\n\nif __name__ == '__main__':\n    pass\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                code = main(["python", f.name, "--strict"])
                assert code == 2
            finally:
                os.unlink(f.name)


class TestListRules:
    def test_list_rules(self, capsys):
        code = main(["list-rules"])
        out = capsys.readouterr().out
        assert "STX-S001" in out
        assert "36 rules" in out
        assert code == 0

    def test_list_rules_json(self, capsys):
        code = main(["list-rules", "--json"])
        out = capsys.readouterr().out
        assert "STX-S001" in out
        assert code == 0

    def test_list_rules_filter_category(self, capsys):
        code = main(["list-rules", "--category", "structure"])
        out = capsys.readouterr().out
        assert "STX-S001" in out
        # Should not include import rules
        assert "STX-I001" not in out
        assert code == 0

    def test_list_rules_filter_severity(self, capsys):
        code = main(["list-rules", "--severity", "error"])
        out = capsys.readouterr().out
        assert "STX-S001" in out
        # Info rules should not appear
        assert "STX-P001" not in out
        assert code == 0


class TestMCPSubcommand:
    def test_mcp_list_tools(self, capsys):
        code = main(["mcp", "list-tools"])
        out = capsys.readouterr().out
        assert "linter_lint" in out
        assert "linter_list_rules" in out
        assert "linter_check_source" in out
        assert code == 0

    def test_mcp_no_subcommand(self):
        code = main(["mcp"])
        assert code == 0
