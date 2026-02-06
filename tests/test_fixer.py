"""Tests for scitex_linter.fixer -- S006 auto-fix."""

import os
import tempfile
import textwrap

from scitex_linter.fixer import fix_file, fix_source

# =========================================================================
# TestFixSource: core fix_source() logic
# =========================================================================


class TestFixSource:
    def test_insert_all_params_bare_main(self):
        """def main(): with @stx.session -> add all 5 INJECTED params."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed
        assert "def main(\n" in fixed
        assert "):\n" in fixed

    def test_insert_missing_params(self):
        """def main(logger=stx.INJECTED): -> adds other 4."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(logger=stx.INJECTED):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed
        # logger should use canonical form now
        assert "logger=stx.session.INJECTED" in fixed

    def test_preserve_user_params(self):
        """def main(data_path="x"): -> adds INJECTED after data_path."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(data_path="input.csv"):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        # User param preserved
        assert 'data_path="input.csv"' in fixed
        # All INJECTED added
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed
        # User param comes before INJECTED params
        data_pos = fixed.index("data_path")
        config_pos = fixed.index("CONFIG=stx.session.INJECTED")
        assert data_pos < config_pos

    def test_idempotent_already_clean(self):
        """All 5 present -> no change."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(
                CONFIG=stx.session.INJECTED,
                plt=stx.session.INJECTED,
                COLORS=stx.session.INJECTED,
                rngg=stx.session.INJECTED,
                logger=stx.session.INJECTED,
            ):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert fixed == src

    def test_non_session_function_untouched(self):
        """def main(): without @stx.session -> no change."""
        src = textwrap.dedent("""\
            import scitex as stx

            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert fixed == src

    def test_multiline_existing_params(self):
        """Multi-line def with partial INJECTED -> append missing."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(
                CONFIG=stx.session.INJECTED,
                plt=stx.session.INJECTED,
            ):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed

    def test_preserves_body(self):
        """Ensure the function body is preserved after fix."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                x = 1
                y = 2
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert "    x = 1\n" in fixed
        assert "    y = 2\n" in fixed
        assert "    return 0\n" in fixed

    def test_preserves_code_before_and_after(self):
        """Ensure code before and after the function is preserved."""
        src = textwrap.dedent("""\
            import scitex as stx
            import numpy as np

            CONSTANT = 42

            @stx.session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert "import numpy as np\n" in fixed
        assert "CONSTANT = 42\n" in fixed
        assert 'if __name__ == "__main__":\n' in fixed
        assert "    main()\n" in fixed

    def test_non_python_returns_unchanged(self):
        """Non-parseable source returns unchanged."""
        src = "this is not valid python {{{"
        fixed = fix_source(src)
        assert fixed == src

    def test_no_stx_session_at_all(self):
        """File with no @stx.session function returns unchanged."""
        src = textwrap.dedent("""\
            def helper():
                pass

            def another():
                return 1
        """)
        fixed = fix_source(src)
        assert fixed == src

    def test_user_param_with_type_annotation(self):
        """def main(data_path: str = "x"): preserves annotation."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(data_path: str = "input.csv"):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert 'data_path: str = "input.csv"' in fixed
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed

    def test_canonical_order_of_injected(self):
        """INJECTED params should appear in canonical order: CONFIG, plt, COLORS, rngg, logger."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        positions = []
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            pos = fixed.index(f"{param}=stx.session.INJECTED")
            positions.append(pos)
        # Verify ascending order
        assert positions == sorted(positions)

    def test_bare_session_decorator(self):
        """@session (bare) also triggers fix."""
        src = textwrap.dedent("""\
            import scitex as stx

            @session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed

    def test_multiple_session_functions(self):
        """Multiple @stx.session functions in one file -- both get fixed."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                return 0

            @stx.session
            def experiment():
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        # Both functions should have all 5 params
        # Count occurrences of CONFIG=stx.session.INJECTED
        assert fixed.count("CONFIG=stx.session.INJECTED") == 2
        assert fixed.count("logger=stx.session.INJECTED") == 2

    def test_mixed_user_and_injected_params(self):
        """User params + some INJECTED -> adds only missing INJECTED."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(
                data_path="input.csv",
                threshold=0.5,
                CONFIG=stx.session.INJECTED,
                logger=stx.session.INJECTED,
            ):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        assert 'data_path="input.csv"' in fixed
        assert "threshold=0.5" in fixed
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed

    def test_stx_injected_shorthand_normalized(self):
        """stx.INJECTED (shorthand) is normalized to stx.session.INJECTED."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(
                CONFIG=stx.INJECTED,
                plt=stx.INJECTED,
                COLORS=stx.INJECTED,
                rngg=stx.INJECTED,
                logger=stx.INJECTED,
            ):
                return 0

            if __name__ == "__main__":
                main()
        """)
        fixed = fix_source(src)
        # All should be normalized to canonical form
        for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
            assert f"{param}=stx.session.INJECTED" in fixed
        # No stx.INJECTED (without .session) should remain
        # Check that every INJECTED has session in it
        assert "stx.INJECTED" not in fixed.replace("stx.session.INJECTED", "")


# =========================================================================
# TestFixFile: file-level operations
# =========================================================================


class TestFixFile:
    def test_fix_file_writes(self):
        """Verify file is written with fixes."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                fixed, changed = fix_file(f.name, write=True)
                assert changed is True
                # Read back and verify
                with open(f.name) as rf:
                    written = rf.read()
                assert written == fixed
                for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
                    assert f"{param}=stx.session.INJECTED" in written
            finally:
                os.unlink(f.name)

    def test_fix_file_no_write(self):
        """write=False returns fixed source but does not write."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main():
                return 0

            if __name__ == "__main__":
                main()
        """)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                fixed, changed = fix_file(f.name, write=False)
                assert changed is True
                # File should still have original content
                with open(f.name) as rf:
                    on_disk = rf.read()
                assert on_disk == src
                # But returned fixed source has the fix
                for param in ("CONFIG", "plt", "COLORS", "rngg", "logger"):
                    assert f"{param}=stx.session.INJECTED" in fixed
            finally:
                os.unlink(f.name)

    def test_fix_file_already_clean(self):
        """Already-clean file -> changed=False, no write."""
        src = textwrap.dedent("""\
            import scitex as stx

            @stx.session
            def main(
                CONFIG=stx.session.INJECTED,
                plt=stx.session.INJECTED,
                COLORS=stx.session.INJECTED,
                rngg=stx.session.INJECTED,
                logger=stx.session.INJECTED,
            ):
                return 0

            if __name__ == "__main__":
                main()
        """)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(src)
            f.flush()
            try:
                fixed, changed = fix_file(f.name, write=True)
                assert changed is False
                assert fixed == src
            finally:
                os.unlink(f.name)

    def test_fix_file_nonexistent(self):
        """Non-existent file returns ('', False)."""
        fixed, changed = fix_file("/nonexistent/path.py")
        assert fixed == ""
        assert changed is False


# =========================================================================
# TestFormatCLI: placeholder for post-integration tests
# =========================================================================


class TestFormatCLI:
    """CLI integration tests -- to be added after cli.py integration."""

    pass
