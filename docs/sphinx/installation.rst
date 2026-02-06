Installation
============

Requirements
------------

- Python 3.8 or higher

Install from PyPI
-----------------

.. code-block:: bash

    pip install scitex-linter

With MCP server support:

.. code-block:: bash

    pip install scitex-linter[mcp]

With all optional dependencies:

.. code-block:: bash

    pip install scitex-linter[all]

Install from Source
-------------------

.. code-block:: bash

    git clone https://github.com/ywatanabe1989/scitex-linter.git
    cd scitex-linter
    pip install -e .

For development:

.. code-block:: bash

    pip install -e ".[dev]"

Verification
------------

Verify the installation:

.. code-block:: bash

    scitex-linter --version
    scitex-linter --help

Via SciTeX
----------

If you have the main ``scitex`` package installed, the linter is also available as:

.. code-block:: bash

    scitex linter lint script.py
    scitex linter python experiment.py
