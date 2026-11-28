# Engineering and documentation kit context

This repository owns reusable engineering and documentation policy and the shared site engine.
The [README](../README.md) owns consumer setup and update commands;
[shared maintenance](../rules/maintenance.md) owns the authoring contract.

| Location | Responsibility |
|---|---|
| `rules/` | Canonical engineering/documentation policy and writing/layout rules |
| `theme/` | Shared shell, reader, CSS/JS, fonts and local math assets |
| `tooling/`, `docsite.py` | Consumer-root-independent build/lint and safe initialization |
| `examples/starter/` | Neutral consuming project and visual guide; its entry files are `*.tmpl` templates that `init` writes under their real names |
| `docs/topics/`, `docs/site/` | The kit's own records and its reference website: pages for people plus the guides rendered as reference pages |
| `docs/KIT_*.md`, `docs/open/KIT_OPEN.md` | The kit's own context, reading index, capability map, worklog and open work; `KIT_` names keep them apart from a consuming project's files |
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
The current release is 6.0.0. The kit keeps one
[migration guide](topics/releases/migration.md) at a fixed address; it holds
every step from 5.7.0, each under a heading that says which versions need it.
At a release, add the new version's steps there, set the tag in its commands
and, on the owner's word, drop the steps for versions no project is on. Do not
rename the file: projects link it. The guides of versions up to 5.8.0 are in
the repository at the tag `v5.9.0`. Before a tag, run
`python docsite.py lint --project . --since <last tag>` and settle each note
about a changed rule section: the kit's own page follows in the same release.

The [website record](topics/website/website.md) owns the kit's own site.
Build it from the kit root with `python docsite.py build --project .`.

Development checks use Python 3.12, the pinned root `requirements.txt` and
`requirements-lock.txt` (the page lock's optional dependency), Node
22 and the Playwright that the root `package.json` and `package-lock.json` pin,
installed with `npm ci` into the ignored `node_modules/`. Run
`bash tests/run_checks.sh` with `DOCS_PYTHON` selecting that interpreter;
it checks the starter, builds and strictly lints the kit's own website, checks
that every shared script parses and runs the browser suites when Playwright
loads from `node_modules/`, as documented in README. `DOCS_NODE` selects the
Node binary. The Pages workflow runs the same script with the browser suites
required before it deploys.

One full run takes about five minutes, about four of them in the browser
suites. While a release is being built, run the build, strict lint and the
tests of the files a change touched, and judge by their exit codes. Run the
full script once, on the final state before the tag; a commit after it that
changes only records needs the build and strict lint again, not the full
script.
No application runtime or simulator is needed.
