Rules Reference
===============

SciTeX Linter enforces 45 rules across 8 categories. Rules use the ``STX-`` prefix.

Category S: Structure
---------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-S001
     - error
     - Missing ``@stx.session`` decorator on main function
   * - STX-S002
     - error
     - Missing ``if __name__ == '__main__'`` guard
   * - STX-S003
     - error
     - ``argparse`` detected — ``@stx.session`` auto-generates CLI from function signature
   * - STX-S004
     - warning
     - ``@stx.session`` function should return an integer exit code
   * - STX-S005
     - warning
     - Missing ``import scitex as stx``
   * - STX-S006
     - warning
     - ``@stx.session`` function missing explicit INJECTED parameters

Category I: Imports
-------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-I001
     - warning
     - Use ``stx.plt`` instead of importing ``matplotlib.pyplot`` directly
   * - STX-I002
     - warning
     - Use ``stx.stats`` instead of importing ``scipy.stats`` directly
   * - STX-I003
     - warning
     - Use ``stx.io`` instead of ``pickle`` for file I/O
   * - STX-I004
     - warning
     - Use ``stx.io`` for CSV/DataFrame I/O instead of pandas I/O functions
   * - STX-I005
     - warning
     - Use ``stx.io`` for array I/O instead of numpy save/load
   * - STX-I006
     - info
     - Use ``rngg`` (injected by ``@stx.session``) for reproducible randomness
   * - STX-I007
     - warning
     - Use ``logger`` (injected by ``@stx.session``) instead of logging module

Category IO: I/O Calls
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-IO001
     - warning
     - ``np.save()`` detected — use ``stx.io.save()`` for provenance tracking
   * - STX-IO002
     - warning
     - ``np.load()`` detected — use ``stx.io.load()`` for provenance tracking
   * - STX-IO003
     - warning
     - ``pd.read_csv()`` detected — use ``stx.io.load()`` for provenance tracking
   * - STX-IO004
     - warning
     - ``.to_csv()`` detected — use ``stx.io.save()`` for provenance tracking
   * - STX-IO005
     - warning
     - ``pickle.dump()`` detected — use ``stx.io.save()`` for provenance tracking
   * - STX-IO006
     - warning
     - ``json.dump()`` detected — use ``stx.io.save()`` for provenance tracking
   * - STX-IO007
     - warning
     - ``plt.savefig()`` detected — use ``stx.io.save(fig, path)`` for metadata embedding

Category P: Plotting
--------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-P001
     - info
     - ``ax.plot()`` — consider ``ax.stx_line()`` for automatic CSV data export
   * - STX-P002
     - info
     - ``ax.scatter()`` — consider ``ax.stx_scatter()`` for automatic CSV data export
   * - STX-P003
     - info
     - ``ax.bar()`` — consider ``ax.stx_bar()`` for automatic sample size annotation
   * - STX-P004
     - info
     - ``plt.show()`` is non-reproducible in batch/CI environments
   * - STX-P005
     - info
     - ``print()`` inside ``@stx.session`` — use ``logger`` for tracked logging

Category ST: Statistics
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-ST001
     - warning
     - ``scipy.stats.ttest_ind()`` — use ``stx.stats.ttest_ind()`` for auto effect size + CI
   * - STX-ST002
     - warning
     - ``scipy.stats.mannwhitneyu()`` — use ``stx.stats.mannwhitneyu()`` for auto effect size
   * - STX-ST003
     - warning
     - ``scipy.stats.pearsonr()`` — use ``stx.stats.pearsonr()`` for auto CI + power
   * - STX-ST004
     - warning
     - ``scipy.stats.f_oneway()`` — use ``stx.stats.anova_oneway()`` for post-hoc + effect sizes
   * - STX-ST005
     - warning
     - ``scipy.stats.wilcoxon()`` — use ``stx.stats.wilcoxon()`` for auto effect size
   * - STX-ST006
     - warning
     - ``scipy.stats.kruskal()`` — use ``stx.stats.kruskal()`` for post-hoc + effect sizes

Category PA: Path Handling
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-PA001
     - warning
     - Absolute path in ``stx.io`` call — use relative paths for reproducibility
   * - STX-PA002
     - warning
     - ``open()`` detected — use ``stx.io.save()``/``stx.io.load()`` which includes auto-logging
   * - STX-PA003
     - info
     - ``os.makedirs()``/``mkdir()`` detected — ``stx.io.save()`` creates directories automatically
   * - STX-PA004
     - warning
     - ``os.chdir()`` detected — scripts should be run from project root
   * - STX-PA005
     - info
     - Path without ``./`` prefix in ``stx.io`` call — use ``./`` for explicit relative intent

Category FM: Figure/Millimeter (opt-in)
----------------------------------------

These rules detect inch-based matplotlib anti-patterns and suggest mm-based alternatives.
FM rules require ``figrecipe`` or ``scitex[plt]`` to be installed, and must be explicitly
enabled via ``enable = ["FM"]`` in config or ``SCITEX_LINTER_ENABLE=FM``.

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Rule
     - Severity
     - Description
   * - STX-FM001
     - warning
     - ``figsize=`` detected — inch-based figure sizing is imprecise for publications
   * - STX-FM002
     - warning
     - ``tight_layout()`` detected — layout is unpredictable across plot types
   * - STX-FM003
     - warning
     - ``bbox_inches="tight"`` detected — can crop important elements unpredictably
   * - STX-FM004
     - info
     - ``constrained_layout=True`` detected — conflicts with mm-based layout control
   * - STX-FM005
     - info
     - ``subplots_adjust()`` with hardcoded fractions — fragile across figure sizes
   * - STX-FM006
     - info
     - ``plt.savefig()`` detected — no provenance tracking
   * - STX-FM007
     - info
     - ``rcParams`` direct modification detected — hard to maintain across figures
   * - STX-FM008
     - warning
     - ``set_size_inches()`` detected — bypasses mm-based layout control
   * - STX-FM009
     - warning
     - ``ax.set_position()`` detected — conflicts with mm-based layout control

Severity Summary
----------------

.. list-table::
   :header-rows: 1
   :widths: 15 10 75

   * - Severity
     - Count
     - Behavior
   * - error
     - 3
     - Must fix. Exit code 2. Blocks execution in ``--strict`` mode.
   * - warning
     - 25
     - Should fix. Exit code 1. Does not block execution.
   * - info
     - 17
     - Suggestions. Exit code 0.
