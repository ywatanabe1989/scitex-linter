"""FM (Figure/Millimeter) rule detection — opt-in category.

Detects inch-based matplotlib patterns and suggests mm-based alternatives.
Used as a second-pass AST visitor from lint_source when "FM" is enabled.
"""

import ast

from . import rules
from .checker import Issue
from .rules import Rule


def _is_exempt_call(node):
    """Check if the call is on a stx.* or fr.* object (exempt from FM rules)."""
    func = node.func
    if not isinstance(func, ast.Attribute):
        return False
    if isinstance(func.value, ast.Name) and func.value.id in ("stx", "fr"):
        return True
    if isinstance(func.value, ast.Attribute):
        if isinstance(func.value.value, ast.Name) and func.value.value.id in (
            "stx",
            "fr",
        ):
            return True
    return False


def _has_kwarg(node, name, value=None):
    """Check if call has a specific keyword argument."""
    for kw in node.keywords:
        if kw.arg == name:
            if value is None:
                return True
            if isinstance(kw.value, ast.Constant) and kw.value.value == value:
                return True
    return False


class FMChecker(ast.NodeVisitor):
    """AST visitor for FM (Figure/Millimeter) rules."""

    def __init__(self, source_lines, config):
        self.source_lines = source_lines
        self.config = config
        self.issues = []

    def _get_source(self, lineno):
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1].rstrip()
        return ""

    def _add(self, rule, line, col, source_line):
        if rule.id in self.config.disable:
            return
        sev = self.config.per_rule_severity.get(rule.id)
        if sev:
            rule = Rule(rule.id, sev, rule.category, rule.message, rule.suggestion)
        self.issues.append(
            Issue(rule=rule, line=line, col=col, source_line=source_line)
        )

    def visit_Call(self, node):
        self._check_call(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        self._check_assign(node)
        self.generic_visit(node)

    def _check_call(self, node):
        """Check Call nodes for FM001-FM006."""
        if _is_exempt_call(node):
            return

        func = node.func
        if not isinstance(func, ast.Attribute):
            return

        func_name = func.attr
        line = self._get_source(node.lineno)

        # FM002: tight_layout()
        if func_name == "tight_layout":
            self._add(rules.FM002, node.lineno, node.col_offset, line)
            return

        # FM005: subplots_adjust()
        if func_name == "subplots_adjust":
            self._add(rules.FM005, node.lineno, node.col_offset, line)
            return

        # FM006: savefig() + FM003: bbox_inches="tight"
        if func_name == "savefig":
            if _has_kwarg(node, "bbox_inches", "tight"):
                self._add(rules.FM003, node.lineno, node.col_offset, line)
            self._add(rules.FM006, node.lineno, node.col_offset, line)
            return

        # FM008: set_size_inches()
        if func_name == "set_size_inches":
            self._add(rules.FM008, node.lineno, node.col_offset, line)
            return

        # FM009: set_position()
        if func_name == "set_position":
            self._add(rules.FM009, node.lineno, node.col_offset, line)
            return

        # FM001: figsize= kwarg on figure()/subplots()
        # FM004: constrained_layout=True kwarg
        if func_name in ("figure", "subplots", "Figure"):
            if _has_kwarg(node, "figsize"):
                self._add(rules.FM001, node.lineno, node.col_offset, line)
            if _has_kwarg(node, "constrained_layout", True):
                self._add(rules.FM004, node.lineno, node.col_offset, line)

    def _check_assign(self, node):
        """Check Assign nodes for FM007 (rcParams modification)."""
        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            val = target.value
            if not isinstance(val, ast.Attribute) or val.attr != "rcParams":
                continue
            if isinstance(val.value, ast.Name) and val.value.id in (
                "plt",
                "mpl",
                "matplotlib",
            ):
                line = self._get_source(node.lineno)
                self._add(rules.FM007, node.lineno, node.col_offset, line)
                break
