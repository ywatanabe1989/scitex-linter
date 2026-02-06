"""Configuration system for scitex-linter."""

from __future__ import annotations

import fnmatch
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore


@dataclass
class LinterConfig:
    """Configuration for scitex-linter behavior."""

    severity: str = "info"
    exclude_dirs: list[str] = field(
        default_factory=lambda: [
            "__pycache__",
            ".git",
            "node_modules",
            ".tox",
            "venv",
            ".venv",
        ]
    )
    library_patterns: list[str] = field(
        default_factory=lambda: [
            "__*__.py",
            "test_*.py",
            "conftest.py",
            "setup.py",
            "manage.py",
        ]
    )
    library_dirs: list[str] = field(default_factory=lambda: ["src"])
    disable: list[str] = field(default_factory=list)
    enable: list[str] = field(default_factory=list)
    per_rule_severity: dict[str, str] = field(default_factory=dict)
    required_injected: list[str] = field(
        default_factory=lambda: ["CONFIG", "plt", "COLORS", "rngg", "logger"]
    )


# =============================================================================
# Configuration Loading
# =============================================================================


def load_config(start_path: str | None = None) -> LinterConfig:
    """
    Load configuration from defaults, pyproject.toml, and environment variables.

    Priority: env vars > pyproject.toml > defaults

    Args:
        start_path: Starting directory for pyproject.toml search (defaults to cwd)

    Returns:
        Merged configuration
    """
    # Start with defaults
    config_dict = {}

    # Load from pyproject.toml
    start_dir = Path(start_path).resolve() if start_path else Path.cwd()
    pyproject_config = _load_pyproject(start_dir)
    config_dict.update(pyproject_config)

    # Load from environment variables (highest priority)
    env_config = _load_env()
    config_dict.update(env_config)

    # Build LinterConfig with merged values
    return LinterConfig(**config_dict)


def _load_pyproject(start_dir: Path) -> dict:
    """
    Walk up directories to find pyproject.toml with [tool.scitex-linter].

    Args:
        start_dir: Starting directory for search

    Returns:
        Configuration dict from [tool.scitex-linter], or empty dict if not found
    """
    if tomllib is None:
        return {}

    current = start_dir
    while True:
        pyproject_path = current / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    tool_config = data.get("tool", {}).get("scitex-linter", {})
                    if tool_config:
                        # Flatten nested sections
                        config = {}
                        for key, value in tool_config.items():
                            if key == "per-rule-severity":
                                config["per_rule_severity"] = value
                            elif key == "session":
                                # Handle [tool.scitex-linter.session]
                                if "required_injected" in value:
                                    config["required_injected"] = value[
                                        "required_injected"
                                    ]
                            else:
                                # Convert kebab-case to snake_case
                                config[key.replace("-", "_")] = value
                        return config
            except Exception:
                pass

        # Move up one directory
        parent = current.parent
        if parent == current:
            # Reached filesystem root
            break
        current = parent

    return {}


def _load_env() -> dict:
    """
    Load configuration from environment variables with SCITEX_LINTER_ prefix.

    Returns:
        Configuration dict with snake_case keys
    """
    config = {}

    # Simple string values
    if "SCITEX_LINTER_SEVERITY" in os.environ:
        config["severity"] = os.environ["SCITEX_LINTER_SEVERITY"]

    # Comma-separated list values
    if "SCITEX_LINTER_DISABLE" in os.environ:
        config["disable"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_DISABLE"].split(",")
            if x.strip()
        ]

    if "SCITEX_LINTER_ENABLE" in os.environ:
        config["enable"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_ENABLE"].split(",")
            if x.strip()
        ]

    if "SCITEX_LINTER_EXCLUDE_DIRS" in os.environ:
        config["exclude_dirs"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_EXCLUDE_DIRS"].split(",")
            if x.strip()
        ]

    if "SCITEX_LINTER_LIBRARY_DIRS" in os.environ:
        config["library_dirs"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_LIBRARY_DIRS"].split(",")
            if x.strip()
        ]

    if "SCITEX_LINTER_LIBRARY_PATTERNS" in os.environ:
        config["library_patterns"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_LIBRARY_PATTERNS"].split(",")
            if x.strip()
        ]

    if "SCITEX_LINTER_REQUIRED_INJECTED" in os.environ:
        config["required_injected"] = [
            x.strip()
            for x in os.environ["SCITEX_LINTER_REQUIRED_INJECTED"].split(",")
            if x.strip()
        ]

    return config


# =============================================================================
# Utility Functions
# =============================================================================


def matches_library_pattern(filename: str, config: LinterConfig) -> bool:
    """
    Check if filename matches any library pattern in config.

    Args:
        filename: Filename to check (e.g., "__init__.py", "test_foo.py")
        config: Linter configuration

    Returns:
        True if filename matches any pattern
    """
    for pattern in config.library_patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False
