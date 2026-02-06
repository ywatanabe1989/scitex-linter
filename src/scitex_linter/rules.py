"""Rule definitions for SciTeX linter."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str  # "error", "warning", "info"
    category: str  # "structure", "import", "io", "plot", "stats"
    message: str
    suggestion: str


# =============================================================================
# Category S: Structure
# =============================================================================

S001 = Rule(
    id="STX-S001",
    severity="error",
    category="structure",
    message="Missing @stx.session decorator on main function",
    suggestion=(
        "Add @stx.session to enable reproducible session tracking, "
        "auto-CLI, and provenance.\n"
        "  @stx.session\n"
        "  def main(...):\n"
        "      return 0"
    ),
)

S002 = Rule(
    id="STX-S002",
    severity="error",
    category="structure",
    message="Missing `if __name__ == '__main__'` guard",
    suggestion="Add `if __name__ == '__main__': main()` at the end of the script.",
)

S003 = Rule(
    id="STX-S003",
    severity="error",
    category="structure",
    message="argparse detected — @stx.session auto-generates CLI from function signature",
    suggestion=(
        "Remove `import argparse` and define parameters as function arguments:\n"
        "  @stx.session\n"
        "  def main(data_path: str, threshold: float = 0.5):\n"
        "      # Auto-generates: --data-path, --threshold"
    ),
)

S004 = Rule(
    id="STX-S004",
    severity="warning",
    category="structure",
    message="@stx.session function should return an integer exit code",
    suggestion="Add `return 0` for success at the end of your session function.",
)

S005 = Rule(
    id="STX-S005",
    severity="warning",
    category="structure",
    message="Missing `import scitex as stx`",
    suggestion="Add `import scitex as stx` to use SciTeX modules.",
)

S006 = Rule(
    id="STX-S006",
    severity="warning",
    category="structure",
    message="@stx.session function missing explicit INJECTED parameters",
    suggestion=(
        "Declare auto-injected values explicitly in the function signature:\n"
        "  @stx.session\n"
        "  def main(\n"
        "      CONFIG=stx.session.INJECTED,\n"
        "      plt=stx.session.INJECTED,\n"
        "      COLORS=stx.session.INJECTED,\n"
        "      rngg=stx.session.INJECTED,\n"
        "      logger=stx.session.INJECTED,\n"
        "  ):\n"
        "      return 0"
    ),
)


# =============================================================================
# Category I: Imports
# =============================================================================

I001 = Rule(
    id="STX-I001",
    severity="warning",
    category="import",
    message="Use `stx.plt` instead of importing matplotlib.pyplot directly",
    suggestion="Replace with `stx.plt` (or `plt` injected by @stx.session).",
)

I002 = Rule(
    id="STX-I002",
    severity="warning",
    category="import",
    message="Use `stx.stats` instead of importing scipy.stats directly",
    suggestion="Replace with `stx.stats` which adds effect sizes, CI, and power analysis.",
)

I003 = Rule(
    id="STX-I003",
    severity="warning",
    category="import",
    message="Use `stx.io` instead of pickle for file I/O",
    suggestion="Replace with `stx.io.save(obj, 'file.pkl')` / `stx.io.load('file.pkl')`.",
)

I004 = Rule(
    id="STX-I004",
    severity="warning",
    category="import",
    message="Use `stx.io` for CSV/DataFrame I/O instead of pandas I/O functions",
    suggestion="Replace `pd.read_csv()` with `stx.io.load()`, `df.to_csv()` with `stx.io.save()`.",
)

I005 = Rule(
    id="STX-I005",
    severity="warning",
    category="import",
    message="Use `stx.io` for array I/O instead of numpy save/load",
    suggestion="Replace `np.save()`/`np.load()` with `stx.io.save()`/`stx.io.load()`.",
)

I006 = Rule(
    id="STX-I006",
    severity="info",
    category="import",
    message="Use `rngg` (injected by @stx.session) for reproducible randomness",
    suggestion="Remove `import random` and use `rngg` from @stx.session injection.",
)

I007 = Rule(
    id="STX-I007",
    severity="warning",
    category="import",
    message="Use `logger` (injected by @stx.session) instead of logging module",
    suggestion="Remove `import logging` and use `logger` from @stx.session injection.",
)


# =============================================================================
# Category IO: Call-level I/O (Phase 2)
# =============================================================================

IO001 = Rule(
    id="STX-IO001",
    severity="warning",
    category="io",
    message="`np.save()` detected — use `stx.io.save()` for provenance tracking",
    suggestion="Replace `np.save(path, arr)` with `stx.io.save(arr, path)`.",
)

IO002 = Rule(
    id="STX-IO002",
    severity="warning",
    category="io",
    message="`np.load()` detected — use `stx.io.load()` for provenance tracking",
    suggestion="Replace `np.load(path)` with `stx.io.load(path)`.",
)

IO003 = Rule(
    id="STX-IO003",
    severity="warning",
    category="io",
    message="`pd.read_csv()` detected — use `stx.io.load()` for provenance tracking",
    suggestion="Replace `pd.read_csv(path)` with `stx.io.load(path)`.",
)

IO004 = Rule(
    id="STX-IO004",
    severity="warning",
    category="io",
    message="`.to_csv()` detected — use `stx.io.save()` for provenance tracking",
    suggestion="Replace `df.to_csv(path)` with `stx.io.save(df, path)`.",
)

IO005 = Rule(
    id="STX-IO005",
    severity="warning",
    category="io",
    message="`pickle.dump()` detected — use `stx.io.save()` for provenance tracking",
    suggestion="Replace `pickle.dump(obj, f)` with `stx.io.save(obj, 'file.pkl')`.",
)

IO006 = Rule(
    id="STX-IO006",
    severity="warning",
    category="io",
    message="`json.dump()` detected — use `stx.io.save()` for provenance tracking",
    suggestion="Replace `json.dump(obj, f)` with `stx.io.save(obj, 'file.json')`.",
)

IO007 = Rule(
    id="STX-IO007",
    severity="warning",
    category="io",
    message="`plt.savefig()` detected — use `stx.io.save(fig, path)` for metadata embedding",
    suggestion="Replace `plt.savefig(path)` with `stx.io.save(fig, path)`.",
)


# =============================================================================
# Category P: Plotting (Phase 2)
# =============================================================================

P001 = Rule(
    id="STX-P001",
    severity="info",
    category="plot",
    message="`ax.plot()` — consider `ax.stx_line()` for automatic CSV data export",
    suggestion="Replace `ax.plot(x, y)` with `ax.stx_line(x, y)` for tracked plotting.",
)

P002 = Rule(
    id="STX-P002",
    severity="info",
    category="plot",
    message="`ax.scatter()` — consider `ax.stx_scatter()` for automatic CSV data export",
    suggestion="Replace `ax.scatter(x, y)` with `ax.stx_scatter(x, y)` for tracked plotting.",
)

P003 = Rule(
    id="STX-P003",
    severity="info",
    category="plot",
    message="`ax.bar()` — consider `ax.stx_bar()` for automatic sample size annotation",
    suggestion="Replace `ax.bar(x, y)` with `ax.stx_bar(x, y)` for tracked plotting.",
)

P004 = Rule(
    id="STX-P004",
    severity="info",
    category="plot",
    message="`plt.show()` is non-reproducible in batch/CI environments",
    suggestion="Remove `plt.show()` — figures are auto-saved in session output directory.",
)

P005 = Rule(
    id="STX-P005",
    severity="info",
    category="plot",
    message="`print()` inside @stx.session — use `logger` for tracked logging",
    suggestion="Replace `print(msg)` with `logger.info(msg)` (injected by @stx.session).",
)


# =============================================================================
# Category ST: Statistics (Phase 2)
# =============================================================================

ST001 = Rule(
    id="STX-ST001",
    severity="warning",
    category="stats",
    message="`scipy.stats.ttest_ind()` — use `stx.stats.ttest_ind()` for auto effect size + CI",
    suggestion="Replace with `stx.stats.ttest_ind(a, b)` which includes Cohen's d and CI.",
)

ST002 = Rule(
    id="STX-ST002",
    severity="warning",
    category="stats",
    message="`scipy.stats.mannwhitneyu()` — use `stx.stats.mannwhitneyu()` for auto effect size",
    suggestion="Replace with `stx.stats.mannwhitneyu(a, b)` which includes Cliff's delta.",
)

ST003 = Rule(
    id="STX-ST003",
    severity="warning",
    category="stats",
    message="`scipy.stats.pearsonr()` — use `stx.stats.pearsonr()` for auto CI + power",
    suggestion="Replace with `stx.stats.pearsonr(a, b)` which includes CI and power analysis.",
)

ST004 = Rule(
    id="STX-ST004",
    severity="warning",
    category="stats",
    message="`scipy.stats.f_oneway()` — use `stx.stats.anova_oneway()` for post-hoc + effect sizes",
    suggestion="Replace with `stx.stats.anova_oneway(*groups)` which includes eta-squared.",
)

ST005 = Rule(
    id="STX-ST005",
    severity="warning",
    category="stats",
    message="`scipy.stats.wilcoxon()` — use `stx.stats.wilcoxon()` for auto effect size",
    suggestion="Replace with `stx.stats.wilcoxon(a, b)` which includes effect size and CI.",
)

ST006 = Rule(
    id="STX-ST006",
    severity="warning",
    category="stats",
    message="`scipy.stats.kruskal()` — use `stx.stats.kruskal()` for post-hoc + effect sizes",
    suggestion="Replace with `stx.stats.kruskal(*groups)` which includes epsilon-squared.",
)


# =============================================================================
# Category PA: Path Handling
# =============================================================================

PA001 = Rule(
    id="STX-PA001",
    severity="warning",
    category="path",
    message="Absolute path in `stx.io` call — use relative paths for reproducibility",
    suggestion="Use `stx.io.save(obj, './relative/path.ext')` — paths resolve to script_out/.",
)

PA002 = Rule(
    id="STX-PA002",
    severity="warning",
    category="path",
    message="`open()` detected — use `stx.io.save()`/`stx.io.load()` which includes auto-logging",
    suggestion=(
        "Replace `open(path)` with `stx.io.load(path)` or `stx.io.save(obj, path)`.\n"
        "  stx.io automatically logs all I/O operations for provenance tracking."
    ),
)

PA003 = Rule(
    id="STX-PA003",
    severity="info",
    category="path",
    message="`os.makedirs()`/`mkdir()` detected — `stx.io.save()` creates directories automatically",
    suggestion=(
        "Remove manual directory creation.\n"
        "  `stx.io.save(obj, './subdir/file.ext')` auto-creates `subdir/` inside script_out/."
    ),
)

PA004 = Rule(
    id="STX-PA004",
    severity="warning",
    category="path",
    message="`os.chdir()` detected — scripts should be run from project root",
    suggestion="Remove `os.chdir()` and run scripts from the project root directory.",
)

PA005 = Rule(
    id="STX-PA005",
    severity="info",
    category="path",
    message="Path without `./` prefix in `stx.io` call — use `./` for explicit relative intent",
    suggestion="Use `./filename.ext` instead of `filename.ext` to clarify relative path intent.",
)


# =============================================================================
# Category FM: Figure/Millimeter
# =============================================================================

FM001 = Rule(
    id="STX-FM001",
    severity="warning",
    category="figure",
    message="`figsize=` detected — inch-based figure sizing is imprecise for publications",
    suggestion=(
        "Use mm-based sizing: `stx.plt.subplots(axes_width_mm=40, axes_height_mm=28)` "
        "or `fig, ax = fr.subplots(axes_width_mm=40, axes_height_mm=28)` for precise control."
    ),
)

FM002 = Rule(
    id="STX-FM002",
    severity="warning",
    category="figure",
    message="`tight_layout()` detected — layout is unpredictable across plot types",
    suggestion=(
        "Use mm-based margins: `stx.plt.subplots(margin_left_mm=15, margin_bottom_mm=12)` "
        "for deterministic layout control."
    ),
)

FM003 = Rule(
    id="STX-FM003",
    severity="warning",
    category="figure",
    message='`bbox_inches="tight"` detected — can crop important elements unpredictably',
    suggestion="Use `fr.save(fig, './plot.png')` or `stx.io.save(fig, './plot.png')` which handle cropping intelligently.",
)

FM004 = Rule(
    id="STX-FM004",
    severity="info",
    category="figure",
    message="`constrained_layout=True` detected — conflicts with mm-based layout control",
    suggestion="Use mm-based layout from `stx.plt.subplots()` instead of constrained_layout.",
)

FM005 = Rule(
    id="STX-FM005",
    severity="info",
    category="figure",
    message="`subplots_adjust()` with hardcoded fractions — fragile across figure sizes",
    suggestion=(
        "Use mm-based spacing: `stx.plt.subplots(space_w_mm=8, space_h_mm=10)` "
        "for size-independent layout."
    ),
)

FM006 = Rule(
    id="STX-FM006",
    severity="info",
    category="figure",
    message="`plt.savefig()` detected — no provenance tracking",
    suggestion="Use `fr.save(fig, './plot.png')` or `stx.io.save(fig, './plot.png')` for recipe tracking and provenance.",
)

FM007 = Rule(
    id="STX-FM007",
    severity="info",
    category="figure",
    message="`rcParams` direct modification detected — hard to maintain across figures",
    suggestion="Use figrecipe style presets: `fr.load_style('SCITEX')` for consistent styling.",
)

FM008 = Rule(
    id="STX-FM008",
    severity="warning",
    category="figure",
    message="`set_size_inches()` detected — bypasses mm-based layout control",
    suggestion=(
        "Use mm-based sizing: `fr.subplots(axes_width_mm=40, axes_height_mm=28)` "
        "or `stx.plt.subplots(axes_width_mm=40, axes_height_mm=28)` for precise control."
    ),
)

FM009 = Rule(
    id="STX-FM009",
    severity="warning",
    category="figure",
    message="`ax.set_position()` detected — conflicts with mm-based layout control",
    suggestion=(
        "Use mm-based margins: `fr.subplots(margin_left_mm=15, margin_bottom_mm=12)` "
        "or `stx.plt.subplots(margin_left_mm=15, margin_bottom_mm=12)` for deterministic layout."
    ),
)


# All rules indexed by ID
ALL_RULES = {
    r.id: r
    for r in [
        S001,
        S002,
        S003,
        S004,
        S005,
        S006,
        I001,
        I002,
        I003,
        I004,
        I005,
        I006,
        I007,
        IO001,
        IO002,
        IO003,
        IO004,
        IO005,
        IO006,
        IO007,
        P001,
        P002,
        P003,
        P004,
        P005,
        ST001,
        ST002,
        ST003,
        ST004,
        ST005,
        ST006,
        PA001,
        PA002,
        PA003,
        PA004,
        PA005,
        FM001,
        FM002,
        FM003,
        FM004,
        FM005,
        FM006,
        FM007,
        FM008,
        FM009,
    ]
}

SEVERITY_ORDER = {"error": 2, "warning": 1, "info": 0}
