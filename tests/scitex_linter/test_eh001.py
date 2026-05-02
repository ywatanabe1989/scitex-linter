"""Tests for STX-EH001: narrow `except ImportError` after lazy optional-dep import."""

from scitex_linter.checker import lint_source


def _rule_ids(source, filepath="lib.py"):
    return [i.rule.id for i in lint_source(source, filepath=filepath)]


class TestEH001Positive:
    def test_narrow_import_error_fires(self):
        """The exact pattern that bit _RandomStateManager.py."""
        src = """
def _seed_tf():
    try:
        import tensorflow as tf
    except ImportError:
        pass
"""
        assert "STX-EH001" in _rule_ids(src)

    def test_module_not_found_only_fires(self):
        src = """
try:
    import torch
except ModuleNotFoundError:
    pass
"""
        assert "STX-EH001" in _rule_ids(src)

    def test_from_import_narrow_fires(self):
        src = """
try:
    from optional_dep import thing
except ImportError:
    pass
"""
        assert "STX-EH001" in _rule_ids(src)

    def test_tuple_narrow_fires(self):
        src = """
try:
    import tensorflow
except (ImportError, ModuleNotFoundError):
    pass
"""
        assert "STX-EH001" in _rule_ids(src)


class TestEH001Negative:
    def test_already_broad_exception_clean(self):
        """Already broad — the fix we want users to apply."""
        src = """
try:
    import tensorflow as tf
except Exception:
    pass
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_broad_with_logger_clean(self):
        src = """
try:
    import tensorflow as tf
except Exception as e:
    logger.debug(f"tf skipped: {type(e).__name__}: {e}")
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_unwrapped_import_clean(self):
        """Plain top-level import without try-block — rule must not fire."""
        src = """
import tensorflow as tf
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_stdlib_tomllib_clean(self):
        """tomllib — stdlib, narrow ImportError is correct."""
        src = """
try:
    import tomllib
except ImportError:
    import tomli as tomllib
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_importlib_metadata_clean(self):
        src = """
try:
    from importlib.metadata import version
except ImportError:
    pass
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_two_handlers_one_broad_clean(self):
        src = """
try:
    import tensorflow
except ImportError:
    pass
except Exception:
    pass
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_bare_except_clean(self):
        src = """
try:
    import tensorflow
except:
    pass
"""
        assert "STX-EH001" not in _rule_ids(src)

    def test_try_body_has_extra_statements_clean(self):
        """Body has more than just the import — too complex; skip."""
        src = """
try:
    import tensorflow as tf
    tf.config.experimental.enable_op_determinism()
except ImportError:
    pass
"""
        assert "STX-EH001" not in _rule_ids(src)
