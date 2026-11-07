# Engineering and documentation kit context

This repository owns reusable engineering and documentation policy and the shared site engine.
The [README](../README.md) owns consumer setup and update commands;
[shared maintenance](../rules/maintenance.md) owns the authoring contract.

| Location | Responsibility |
|---|---|
| `rules/` | Canonical engineering/documentation policy, writing/layout rules and source coverage |
| `theme/` | Shared shell, reader, CSS/JS, fonts and local math assets |
| `tooling/`, `docsite.py` | Consumer-root-independent build/lint and safe initialization |
| `examples/starter/` | Neutral consuming project and visual guide |
| `docs/topics/`, `docs/site/` | The kit's own records and its reference website, which renders the canonical guides in place |
| `tests/` | Portability, content preservation, formulas, links and optional browser review |
| `provenance.json` | Extraction origins and source/extracted byte hashes |
| `verification/`, `preview/` | Initial check receipts and illustration captures |

The [extraction record](topics/extraction/extraction.md) owns initial scope,
evidence and limits. [Worklog](worklog.md) owns chronology. Source files in
`rules/` remain canonical for transferable rules; consumer exceptions stay in
the consuming repository. Consumer adoption and compatibility status belong in
each consuming project's own documentation.

The [documentation index](index.md) routes readers to focused engineering,
writing and site guides. Read each guide before the action it governs.

The [experiment workflow](../rules/experiments/workflow.md) and
[verification guide](../rules/experiments/verification.md) own shared experiment
design and check selection. Project-specific study decisions, recipes, results
and execution contracts remain with consumers.

The [local comparison contract](topics/panel-switcher/panel-switcher.md)
owns the shared panel switcher's authoring, behavior and extraction checks.

[Releases and upgrades](topics/releases/releases.md) owns version notes and
consumer migration steps; `VERSION` holds the current version.
The [1.1.0 migration guide](topics/releases/migrations/1.1.0.md) covers focused
policy owners, optional project layout changes and compatibility adapters.

The [website record](topics/website/website.md) owns the kit's own site.
Build it from the kit root with `python docsite.py build --project .`.

Development checks use Python 3.12, the pinned root `requirements.txt` and Node
22. Run `bash tests/run_checks.sh` with `DOCS_PYTHON` selecting that interpreter;
it checks the starter and builds and strictly lints the kit's own website.
Browser review additionally uses Playwright/Chromium as documented in README.
No application runtime or simulator is needed.
