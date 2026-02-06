Quick Start
===========

This guide helps you get started with SciTeX Linter.

Lint a File
-----------

.. code-block:: bash

    scitex-linter check script.py

The output shows issues grouped by severity:

.. code-block:: text

    script.py:1  STX-S003  [error]  argparse detected — @stx.session auto-generates CLI
    script.py:0  STX-S001  [error]  Missing @stx.session decorator on main function

    script.py: 2 issues (2 errors)

Severity Levels
---------------

- **error**: Must fix before running. Exit code 2.
- **warning**: Should fix for best practices. Exit code 1.
- **info**: Optional suggestions. Exit code 0.

Filter by severity:

.. code-block:: bash

    # Only show errors
    scitex-linter check script.py --severity error

    # Show warnings and above (default: info)
    scitex-linter check script.py --severity warning

Lint then Execute
-----------------

The ``python`` subcommand lints your script and then runs it:

.. code-block:: bash

    scitex-linter python experiment.py

Use ``--strict`` to abort if lint errors are found:

.. code-block:: bash

    scitex-linter python experiment.py --strict

Pass arguments to the script after ``--``:

.. code-block:: bash

    scitex-linter python experiment.py -- --epochs 100 --lr 0.001

Browse Rules
------------

List all 35 rules:

.. code-block:: bash

    scitex-linter rule

Filter by category:

.. code-block:: bash

    scitex-linter rule --category path
    scitex-linter rule --category structure,import

JSON output:

.. code-block:: bash

    scitex-linter rule --json

flake8 Integration
------------------

SciTeX Linter registers as a flake8 plugin with the ``STX`` prefix:

.. code-block:: bash

    flake8 --select STX script.py

This integrates with existing flake8 workflows and CI pipelines.

What a Clean Script Looks Like
------------------------------

.. code-block:: python

    import scitex as stx

    @stx.session
    def main(data_path="./data.csv", threshold=0.5):
        df = stx.io.load(data_path)
        results = stx.stats.ttest_ind(df["group_a"], df["group_b"])
        stx.io.save(results, "./results.csv")
        return 0

    if __name__ == "__main__":
        main()
