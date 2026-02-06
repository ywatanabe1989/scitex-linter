Claude Code Hook
================

SciTeX Linter integrates with Claude Code as a post-tool-use hook that automatically lints Python files after every Write/Edit operation.

How It Works
------------

When Claude Code writes or edits a ``.py`` file, the hook:

1. Runs ``scitex-linter check`` with ``--severity error`` — **blocks** Claude on errors (exit code 2)
2. Runs ``scitex-linter check`` with ``--severity warning`` — shows warnings but **does not block**
3. Runs ``ruff check --fix`` (or ``flake8``) for standard Python linting

This ensures Claude follows SciTeX patterns automatically.

Installation
------------

The hook file is located at:

.. code-block:: text

    ~/.claude/to_claude/hooks/post-tool-use/run_lint.sh

It is part of the dotfiles configuration and automatically activates when ``scitex-linter`` is installed.

Command Detection
-----------------

The hook auto-detects the available linter command:

.. code-block:: bash

    # Priority 1: standalone package
    if command -v scitex-linter &>/dev/null; then
        stx_lint="scitex-linter"
    # Priority 2: subcommand of main scitex package
    elif command -v scitex &>/dev/null && scitex linter --help &>/dev/null; then
        stx_lint="scitex linter"
    fi

Exit Codes
----------

The hook uses exit codes to control Claude's behavior:

.. list-table::
   :header-rows: 1
   :widths: 10 30 60

   * - Code
     - Meaning
     - Effect
   * - 0
     - Success
     - Claude continues normally
   * - 1
     - Warning
     - Claude sees feedback but continues
   * - 2
     - Error
     - Claude must fix the issue before proceeding

Example Output
--------------

When Claude writes a file with structural errors:

.. code-block:: text

    script.py:1  STX-S003  [error]  argparse detected — @stx.session auto-generates CLI
      Suggestion: Remove `import argparse` and define parameters as function arguments:
        @stx.session
        def main(data_path: str, threshold: float = 0.5):
            # Auto-generates: --data-path, --threshold

    script.py: 1 issue (1 error)

Claude is forced to fix the error before the write is accepted.

Disabling
---------

To temporarily disable the SciTeX linting in the hook, uninstall ``scitex-linter`` or rename the hook file:

.. code-block:: bash

    mv ~/.claude/to_claude/hooks/post-tool-use/run_lint.sh \
       ~/.claude/to_claude/hooks/post-tool-use/run_lint.sh.disabled
