# Engineering and documentation kit context

This repository owns reusable engineering and documentation policy and the shared site engine.
The [README](../README.md) owns consumer setup and update commands;
[shared maintenance](../rules/maintenance.md) owns the authoring contract.

| Location | Responsibility |
|---|---|
| `rules/` | Canonical engineering/documentation policy, writing/layout rules and source coverage |
| `theme/` | Shared shell, reader, CSS/JS, fonts and local math assets |
| `tooling/`, `docsite.py` | Consumer-root-independent build/lint and safe initialization |
| `examples/starter/` | Neutral consuming project and visual guide; its entry files are `*.tmpl` templates that `init` writes under their real names |
| `docs/topics/`, `docs/site/` | The kit's own records and its reference website: pages for people plus the guides rendered as reference pages |
| `docs/KIT_*.md`, `docs/open/KIT_OPEN.md` | The kit's own context, reading index, worklog and open work; `KIT_` names keep them apart from a consuming project's files |
| `tests/` | Portability, content preservation, formulas, links and optional browser review |

Extraction history (record, policy map, source hashes, initial receipts and
captures) remains at the [`v1.1.0` tag](https://github.com/davszi/documentation-kit/tree/v1.1.0).
[Worklog](KIT_WORKLOG.md) owns chronology. Source files in
`rules/` remain canonical for transferable rules; consumer exceptions stay in
the consuming repository. Consumer adoption and compatibility status belong in
each consuming project's own documentation.

The [documentation index](KIT_INDEX.md) routes readers to focused engineering,
writing and site guides. Read each guide before the action it governs.

The [experiment workflow](../rules/experiments/workflow.md) and
[verification guide](../rules/experiments/verification.md) own shared experiment
design and check selection. Project-specific study decisions, recipes, results
and execution contracts remain with consumers.

The [local comparison contract](topics/panel-switcher/panel-switcher.md)
owns the shared panel switcher's authoring, behavior and extraction checks.

[Releases and upgrades](topics/releases/releases.md) owns version notes and
consumer migration steps; `VERSION` holds the current version.
The [2.0.0 migration guide](topics/releases/migrations/2.0.0.md) covers the
removed compatibility forms, configured publication and the kit-pin check; the
[1.1.0 guide](topics/releases/migrations/1.1.0.md) covers focused policy owners,
optional project layout changes and adapters.

The [website record](topics/website/website.md) owns the kit's own site.
Build it from the kit root with `python docsite.py build --project .`.

Development checks use Python 3.12, the pinned root `requirements.txt` and Node
22. Run `bash tests/run_checks.sh` with `DOCS_PYTHON` selecting that interpreter;
it checks the starter and builds and strictly lints the kit's own website.
Browser review additionally uses Playwright/Chromium as documented in README.
No application runtime or simulator is needed.
