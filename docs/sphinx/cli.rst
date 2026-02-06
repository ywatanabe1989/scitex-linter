CLI Reference
=============

SciTeX Linter provides a single ``scitex-linter`` command with subcommands.

Global Options
--------------

.. code-block:: text

    scitex-linter [-h] [-V] [--help-recursive] {check,python,rule,mcp} ...

``-V, --version``
    Show version and exit.

``--help-recursive``
    Show help for all commands and subcommands.

scitex-linter check
-------------------

Check Python files for SciTeX pattern compliance.

.. code-block:: text

    scitex-linter check <path> [--json] [--no-color] [--severity LEVEL] [--category CAT]

``path``
    Python file or directory to check. Directories are searched recursively.

``--json``
    Output results as JSON.

``--no-color``
    Disable colored output.

``--severity {error,warning,info}``
    Minimum severity to report (default: ``info``).

``--category``
    Filter by category (comma-separated): ``structure``, ``import``, ``io``, ``plot``, ``stats``, ``path``.

**Exit codes:**

- ``0`` — No issues (or only info-level)
- ``1`` — Warnings found
- ``2`` — Errors found

**Examples:**

.. code-block:: bash

    # Check a single file
    scitex-linter check script.py

    # Check a directory, errors only
    scitex-linter check ./src/ --severity error

    # JSON output for CI
    scitex-linter check . --json --no-color

scitex-linter python
--------------------

Lint a Python script, then execute it.

.. code-block:: text

    scitex-linter python <script> [--strict] [-- script_args...]

``script``
    Python script to lint and execute.

``--strict``
    Abort execution if lint errors are found (exit code 2).

``-- args...``
    Arguments passed to the script (after ``--`` separator).

**Examples:**

.. code-block:: bash

    # Lint and run
    scitex-linter python experiment.py

    # Strict mode
    scitex-linter python experiment.py --strict

    # Pass arguments to script
    scitex-linter python experiment.py -- --epochs 100 --lr 0.001

scitex-linter rule
------------------

List all available lint rules.

.. code-block:: text

    scitex-linter rule [--json] [--category CAT] [--severity LEVEL]

``--json``
    Output as JSON.

``--category``
    Filter by category (comma-separated).

``--severity {error,warning,info}``
    Filter by exact severity level.

scitex-linter mcp
------------------

MCP (Model Context Protocol) server commands.

.. code-block:: text

    scitex-linter mcp {start,list-tools}

``scitex-linter mcp start [--transport {stdio,sse}]``
    Start the MCP server. Default transport is ``stdio``.

``scitex-linter mcp list-tools``
    List available MCP tools.

Requires the ``mcp`` extra: ``pip install scitex-linter[mcp]``
