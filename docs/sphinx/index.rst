.. SciTeX Linter documentation master file

SciTeX Linter - AST-based Python Linter
========================================

**SciTeX Linter** is an AST-based Python linter that enforces `SciTeX <https://scitex.ai>`_ reproducible research patterns. It provides four interfaces: CLI, Python API, flake8 plugin, and MCP server for AI agents.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: Reference

   rules
   cli
   hook

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/scitex_linter

Key Features
------------

- **35 Rules** across 7 categories: Structure, Import, I/O, Plot, Stats, Path
- **Four Interfaces**: CLI, Python API, flake8 plugin (STX prefix), MCP server
- **Lint + Execute**: ``scitex-linter python script.py`` lints then runs your script
- **Claude Code Hook**: Auto-lints Python files on every Write/Edit
- **Severity Filtering**: ``--severity error`` to focus on blockers only

Quick Example
-------------

CLI:

.. code-block:: bash

    # Lint a file
    scitex-linter check script.py

    # Lint then execute
    scitex-linter python experiment.py --strict

    # List all rules
    scitex-linter rule

flake8:

.. code-block:: bash

    # Uses STX prefix
    flake8 --select STX script.py

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
