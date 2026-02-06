"""Tests for scitex_linter.config — configuration system."""

import textwrap

from scitex_linter.config import LinterConfig, load_config, matches_library_pattern

# =========================================================================
# TestLinterConfigDefaults
# =========================================================================


class TestLinterConfigDefaults:
    """Test default values of LinterConfig."""

    def test_default_severity(self):
        config = LinterConfig()
        assert config.severity == "info"

    def test_default_exclude_dirs(self):
        config = LinterConfig()
        assert "__pycache__" in config.exclude_dirs
        assert ".git" in config.exclude_dirs
        assert "venv" in config.exclude_dirs
        assert ".venv" in config.exclude_dirs

    def test_default_library_patterns(self):
        config = LinterConfig()
        assert "__*__.py" in config.library_patterns
        assert "test_*.py" in config.library_patterns
        assert "conftest.py" in config.library_patterns

    def test_default_library_dirs(self):
        config = LinterConfig()
        assert "src" in config.library_dirs

    def test_default_disable(self):
        config = LinterConfig()
        assert config.disable == []

    def test_default_required_injected(self):
        config = LinterConfig()
        expected = ["CONFIG", "plt", "COLORS", "rngg", "logger"]
        assert config.required_injected == expected


# =========================================================================
# TestMatchesLibraryPattern
# =========================================================================


class TestMatchesLibraryPattern:
    """Test fnmatch-based library pattern matching."""

    def test_init_py_matches(self):
        config = LinterConfig()
        assert matches_library_pattern("__init__.py", config)

    def test_test_file_matches(self):
        config = LinterConfig()
        assert matches_library_pattern("test_foo.py", config)

    def test_conftest_matches(self):
        config = LinterConfig()
        assert matches_library_pattern("conftest.py", config)

    def test_script_no_match(self):
        config = LinterConfig()
        assert not matches_library_pattern("my_script.py", config)

    def test_custom_pattern(self):
        config = LinterConfig(library_patterns=["util_*.py"])
        assert matches_library_pattern("util_helpers.py", config)
        assert not matches_library_pattern("other.py", config)


# =========================================================================
# TestLoadConfigFromPyproject
# =========================================================================


class TestLoadConfigFromPyproject:
    """Test loading configuration from pyproject.toml."""

    def test_load_from_pyproject(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent(
                """
                [tool.scitex-linter]
                severity = "warning"
                disable = ["STX-P004"]
                """
            )
        )

        config = load_config(start_path=tmp_path)
        assert config.severity == "warning"
        assert config.disable == ["STX-P004"]

    def test_load_nested_session(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent(
                """
                [tool.scitex-linter.session]
                required_injected = ["CONFIG", "logger"]
                """
            )
        )

        config = load_config(start_path=tmp_path)
        assert config.required_injected == ["CONFIG", "logger"]

    def test_load_per_rule_severity(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent(
                """
                [tool.scitex-linter.per-rule-severity]
                STX-S003 = "warning"
                """
            )
        )

        config = load_config(start_path=tmp_path)
        assert config.per_rule_severity == {"STX-S003": "warning"}

    def test_no_pyproject_uses_defaults(self, tmp_path):
        config = load_config(start_path=tmp_path)
        assert config.severity == "info"
        assert config.disable == []
        assert "CONFIG" in config.required_injected


# =========================================================================
# TestLoadConfigFromEnv
# =========================================================================


class TestLoadConfigFromEnv:
    """Test loading configuration from environment variables."""

    def test_env_severity_override(self, monkeypatch):
        monkeypatch.setenv("SCITEX_LINTER_SEVERITY", "error")
        config = load_config()
        assert config.severity == "error"

    def test_env_disable_override(self, monkeypatch):
        monkeypatch.setenv("SCITEX_LINTER_DISABLE", "STX-P004,STX-I003")
        config = load_config()
        assert config.disable == ["STX-P004", "STX-I003"]

    def test_env_overrides_pyproject(self, tmp_path, monkeypatch):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent(
                """
                [tool.scitex-linter]
                severity = "warning"
                """
            )
        )

        monkeypatch.setenv("SCITEX_LINTER_SEVERITY", "error")
        config = load_config(start_path=tmp_path)
        assert config.severity == "error"

    def test_env_exclude_dirs(self, monkeypatch):
        monkeypatch.setenv("SCITEX_LINTER_EXCLUDE_DIRS", "build,dist")
        config = load_config()
        assert config.exclude_dirs == ["build", "dist"]
