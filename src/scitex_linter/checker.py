"""AST-based checker that detects SciTeX anti-patterns."""

import ast
from dataclasses import dataclass
from pathlib import Path

from . import rules
from .rules import Rule

S001, S002, S003 = rules.S001, rules.S002, rules.S003
S004, S005, S006 = rules.S004, rules.S005, rules.S006
I001, I002, I003 = rules.I001, rules.I002, rules.I003
I006, I007 = rules.I006, rules.I007

# Phase 2: Call-level rule lookup table {(module_alias, func_name): Rule}
# module_alias=None means match func_name on any object
_CALL_RULES: dict = {
    # IO rules
    ("np", "save"): rules.IO001,
    ("numpy", "save"): rules.IO001,
    ("np", "load"): rules.IO002,
    ("numpy", "load"): rules.IO002,
    ("pd", "read_csv"): rules.IO003,
    ("pandas", "read_csv"): rules.IO003,
    (None, "to_csv"): rules.IO004,
    ("pickle", "dump"): rules.IO005,
    ("pickle", "dumps"): rules.IO005,
    ("json", "dump"): rules.IO006,
    ("plt", "savefig"): rules.IO007,
    # Plot rules
    (None, "show"): rules.P004,  # plt.show()
    # Stats rules — scipy.stats.X()
    ("stats", "ttest_ind"): rules.ST001,
    ("stats", "mannwhitneyu"): rules.ST002,
    ("stats", "pearsonr"): rules.ST003,
    ("stats", "f_oneway"): rules.ST004,
    ("stats", "wilcoxon"): rules.ST005,
    ("stats", "kruskal"): rules.ST006,
    # Path rules
    ("os", "makedirs"): rules.PA003,
    ("os", "mkdir"): rules.PA003,
    ("os", "chdir"): rules.PA004,
}

# Axes method suggestions {func_name: Rule}
_AXES_HINTS: dict = {
    "plot": rules.P001,
    "scatter": rules.P002,
    "bar": rules.P003,
}

# print() inside session
_PRINT_RULE = rules.P005


@dataclass
class Issue:
    rule: Rule
    line: int
    col: int
    source_line: str = ""


def is_script(filepath: str, config=None) -> bool:
    """Check if file is a script (not a library module).

    Uses config.library_patterns and config.library_dirs to determine
    which files are library modules (exempt from script-only rules).
    """
    from .config import LinterConfig, matches_library_pattern

    if config is None:
        config = LinterConfig()

    path = Path(filepath)
    name = path.name

    # Check filename against library patterns (e.g., __*__.py, test_*.py)
    if matches_library_pattern(name, config):
        return False

    # Check if file is inside a library directory (e.g., src/)
    parts = path.parts
    for lib_dir in config.library_dirs:
        if lib_dir in parts:
            return False

    return True


class SciTeXChecker(ast.NodeVisitor):
    """AST visitor detecting non-SciTeX patterns."""

    def __init__(self, source_lines: list, filepath: str = "<stdin>", config=None):
        from .config import LinterConfig

        self.source_lines = source_lines
        self.filepath = filepath
        self.config = config or LinterConfig()
        self.issues: list = []

        # Tracking state
        self._has_stx_import = False
        self._has_main_guard = False
        self._has_session_decorator = False
        self._session_func_returns_int = False
        self._imports: dict = {}  # alias -> full module path
        self._is_script = is_script(filepath, self.config)

    # -----------------------------------------------------------------
    # Import visitors
    # -----------------------------------------------------------------

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            self._imports[name] = alias.name

            if alias.name == "scitex":
                self._has_stx_import = True

            self._check_import(alias.name, node)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        for alias in node.names:
            name = alias.asname or alias.name
            full = f"{module}.{alias.name}"
            self._imports[name] = full

        self._check_import_from(module, node)
        self.generic_visit(node)

    def _check_import(self, module_name: str, node: ast.Import) -> None:
        """Check bare `import X` statements."""
        line = self._get_source(node.lineno)

        # import matplotlib.pyplot as plt
        if "matplotlib.pyplot" in module_name:
            self._add(I001, node.lineno, node.col_offset, line)

        if module_name == "argparse":
            self._add(S003, node.lineno, node.col_offset, line)

        if module_name == "pickle":
            self._add(I003, node.lineno, node.col_offset, line)

        if module_name == "random":
            self._add(I006, node.lineno, node.col_offset, line)

        if module_name == "logging":
            self._add(I007, node.lineno, node.col_offset, line)

    def _check_import_from(self, module: str, node: ast.ImportFrom) -> None:
        """Check `from X import Y` statements."""
        line = self._get_source(node.lineno)

        # from matplotlib import pyplot / from matplotlib.pyplot import *
        if module == "matplotlib":
            for alias in node.names:
                if alias.name == "pyplot":
                    self._add(I001, node.lineno, node.col_offset, line)
                    break
        elif module and "matplotlib.pyplot" in module:
            self._add(I001, node.lineno, node.col_offset, line)

        # from scipy import stats / from scipy.stats import *
        if module in ("scipy", "scipy.stats"):
            if module == "scipy":
                for alias in node.names:
                    if alias.name == "stats":
                        self._add(I002, node.lineno, node.col_offset, line)
                        break
            else:
                self._add(I002, node.lineno, node.col_offset, line)

        # from argparse import *
        if module == "argparse":
            self._add(S003, node.lineno, node.col_offset, line)

    # -----------------------------------------------------------------
    # Call visitors (Phase 2)
    # -----------------------------------------------------------------

    def visit_Call(self, node: ast.Call) -> None:
        self._check_call(node)
        self.generic_visit(node)

    def _check_call(self, node: ast.Call) -> None:
        """Check function calls against Phase 2 rules."""
        func = node.func

        # module.func() pattern — e.g., np.save(), stats.ttest_ind()
        if isinstance(func, ast.Attribute):
            func_name = func.attr
            mod_name = None

            if isinstance(func.value, ast.Name):
                mod_name = func.value.id
            elif isinstance(func.value, ast.Attribute):
                # module.sub.func() — e.g., scipy.stats.ttest_ind()
                if isinstance(func.value.value, ast.Name):
                    mod_name = func.value.attr  # use "stats" from scipy.stats

            # Check stx.io path patterns before skipping stx.* calls
            if mod_name == "stx" or (
                isinstance(func.value, ast.Attribute)
                and isinstance(func.value.value, ast.Name)
                and func.value.value.id == "stx"
            ):
                self._check_stx_io_path(node)
                return

            # Resolve alias: if user did `import numpy as np`, resolve np -> numpy
            resolved = self._imports.get(mod_name, mod_name)

            # Check (module, func) against rule table
            rule = _CALL_RULES.get((mod_name, func_name))
            if rule is None and resolved != mod_name:
                rule = _CALL_RULES.get((resolved, func_name))
            if rule is None:
                rule = _CALL_RULES.get((None, func_name))

            # Special cases
            if rule is not None:
                # plt.show() — only flag if mod resolves to matplotlib
                if rule is rules.P004:
                    if mod_name not in ("plt", "pyplot") and resolved not in (
                        "matplotlib.pyplot",
                    ):
                        return

                # to_csv — only flag on DataFrame-like objects (not stx)
                if rule is rules.IO004:
                    if mod_name in ("stx", "os", "sys", "Path"):
                        return

                line = self._get_source(node.lineno)
                self._add(rule, node.lineno, node.col_offset, line)
                return

            # Axes hints: ax.plot(), ax.scatter(), ax.bar()
            if func_name in _AXES_HINTS and mod_name not in (
                "stx",
                "os",
                "sys",
                "Path",
                "math",
                "np",
                "numpy",
                "pd",
                "pandas",
            ):
                # Heuristic: if variable name looks like axes
                if mod_name and (
                    mod_name.startswith("ax") or mod_name in ("axes", "subplot")
                ):
                    line = self._get_source(node.lineno)
                    self._add(
                        _AXES_HINTS[func_name], node.lineno, node.col_offset, line
                    )
                return

            # Path(...).mkdir() pattern
            if func_name == "mkdir" and mod_name not in (
                "os",
                "stx",
                "sys",
            ):
                # Heuristic: if it's called on something that looks like a Path
                line = self._get_source(node.lineno)
                if "Path" in line or "path" in line.lower():
                    self._add(rules.PA003, node.lineno, node.col_offset, line)

        # bare func() pattern — e.g., print(), open()
        elif isinstance(func, ast.Name):
            if func.id == "print" and self._has_session_decorator:
                line = self._get_source(node.lineno)
                self._add(_PRINT_RULE, node.lineno, node.col_offset, line)
            elif func.id == "open" and self._has_session_decorator:
                line = self._get_source(node.lineno)
                self._add(rules.PA002, node.lineno, node.col_offset, line)

    # -----------------------------------------------------------------
    # stx.io path checking
    # -----------------------------------------------------------------

    def _check_stx_io_path(self, node: ast.Call) -> None:
        """Check path arguments in stx.io.save() / stx.io.load() calls."""
        func = node.func
        if not isinstance(func, ast.Attribute):
            return

        func_name = func.attr

        # Determine which positional arg holds the path
        # stx.io.save(obj, path, ...) -> index 1
        # stx.io.load(path, ...) -> index 0
        if func_name == "save":
            path_idx = 1
        elif func_name == "load":
            path_idx = 0
        else:
            return

        # Check if this is stx.io.save/load (not stx.plt.save, etc.)
        # Pattern: stx.io.save(...) where func.value is Attribute(value=Name('stx'), attr='io')
        is_stx_io = False
        if isinstance(func.value, ast.Attribute):
            if (
                isinstance(func.value.value, ast.Name)
                and func.value.value.id == "stx"
                and func.value.attr == "io"
            ):
                is_stx_io = True
        # Also: io.save(...) if io was imported from stx
        elif isinstance(func.value, ast.Name):
            resolved = self._imports.get(func.value.id, "")
            if "scitex" in resolved and "io" in resolved:
                is_stx_io = True

        if not is_stx_io:
            return

        # Extract path string from positional args or 'path' kwarg
        path_str = None
        if len(node.args) > path_idx:
            arg = node.args[path_idx]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                path_str = arg.value
        else:
            for kw in node.keywords:
                if kw.arg == "path":
                    if isinstance(kw.value, ast.Constant) and isinstance(
                        kw.value.value, str
                    ):
                        path_str = kw.value.value
                    break

        if path_str is None:
            return

        line = self._get_source(node.lineno)

        # PA001: absolute path
        if path_str.startswith("/"):
            self._add(rules.PA001, node.lineno, node.col_offset, line)
        # PA005: missing ./ prefix (bare relative path)
        elif not path_str.startswith("./") and not path_str.startswith("../"):
            self._add(rules.PA005, node.lineno, node.col_offset, line)

    # -----------------------------------------------------------------
    # Function/decorator visitors
    # -----------------------------------------------------------------

    @property
    def _REQUIRED_INJECTED(self):
        return set(self.config.required_injected)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self._has_session_deco(node):
            self._has_session_decorator = True
            self._check_session_return(node)
            self._check_injected_params(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _has_session_deco(self, node: ast.FunctionDef) -> bool:
        """Check if function has @stx.session or @session decorator."""
        for deco in node.decorator_list:
            # @stx.session
            if isinstance(deco, ast.Attribute):
                if (
                    isinstance(deco.value, ast.Name)
                    and deco.value.id == "stx"
                    and deco.attr == "session"
                ):
                    return True
            # @session (bare)
            if isinstance(deco, ast.Name) and deco.id == "session":
                return True
        return False

    def _check_session_return(self, node: ast.FunctionDef) -> None:
        """Check that session function returns an int."""
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                if isinstance(child.value, ast.Constant) and isinstance(
                    child.value.value, int
                ):
                    self._session_func_returns_int = True
                    return
        # No int return found
        line = self._get_source(node.lineno)
        self._add(S004, node.lineno, node.col_offset, line)

    def _check_injected_params(self, node: ast.FunctionDef) -> None:
        """Check that @stx.session function declares all INJECTED parameters."""
        declared = {arg.arg for arg in node.args.args}
        missing = sorted(self._REQUIRED_INJECTED - declared)
        if missing:
            line = self._get_source(node.lineno)
            missing_str = ", ".join(missing)
            dynamic_rule = Rule(
                id=S006.id,
                severity=S006.severity,
                category=S006.category,
                message=(
                    f"@stx.session function missing INJECTED parameters: {missing_str}. "
                    f"All 5 must be declared: CONFIG, COLORS, logger, plt, rngg"
                ),
                suggestion=S006.suggestion,
            )
            self._add(dynamic_rule, node.lineno, node.col_offset, line)

    # -----------------------------------------------------------------
    # Module-level checks (run after visiting entire tree)
    # -----------------------------------------------------------------

    def visit_If(self, node: ast.If) -> None:
        """Detect if __name__ == '__main__' guard."""
        if self._is_main_guard(node):
            self._has_main_guard = True
        self.generic_visit(node)

    def _is_main_guard(self, node: ast.If) -> bool:
        test = node.test
        if isinstance(test, ast.Compare):
            if (
                isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):
                return True
        return False

    # -----------------------------------------------------------------
    # Finalization
    # -----------------------------------------------------------------

    def get_issues(self) -> list:
        """Return all issues, including post-visit structural checks."""
        if not self._is_script:
            return self.issues

        if not self._has_main_guard:
            self._add(S002, 1, 0, "")

        if self._has_main_guard and not self._has_session_decorator:
            self._add(S001, 1, 0, "")

        if self._has_main_guard and not self._has_stx_import:
            self._add(S005, 1, 0, "")

        # Sort: errors first, then by line
        from .rules import SEVERITY_ORDER

        self.issues.sort(key=lambda i: (-SEVERITY_ORDER[i.rule.severity], i.line))
        return self.issues

    def _add(self, rule: Rule, line: int, col: int, source_line: str) -> None:
        if rule.id in self.config.disable:
            return
        sev = self.config.per_rule_severity.get(rule.id)
        if sev:
            rule = Rule(rule.id, sev, rule.category, rule.message, rule.suggestion)
        self.issues.append(
            Issue(rule=rule, line=line, col=col, source_line=source_line)
        )

    def _get_source(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].rstrip()
        return ""


# =============================================================================
# Public API
# =============================================================================


def lint_source(source: str, filepath: str = "<stdin>", config=None) -> list:
    """Lint Python source code and return list of Issues."""
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return []

    lines = source.splitlines()
    checker = SciTeXChecker(lines, filepath=filepath, config=config)
    checker.visit(tree)
    if config and "FM" in config.enable:
        from ._fm_checker import FMChecker

        fm = FMChecker(lines, config)
        fm.visit(tree)
        checker.issues.extend(fm.issues)
    return checker.get_issues()


def lint_file(filepath: str, config=None) -> list:
    """Lint a Python file and return list of Issues."""
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return []
    source = path.read_text(encoding="utf-8")
    return lint_source(source, filepath=str(path), config=config)
