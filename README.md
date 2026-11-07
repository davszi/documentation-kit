# Engineering and documentation kit

Reusable engineering and documentation policy, a complete HTML reader and a
small static-site toolchain. Projects consume one pinned [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) while keeping their own
topic records, pages, figures, navigation and evidence.

![The shared chapter reader](preview/desktop.png)

[Phone view](preview/mobile.png) · [Home page](preview/home.png) ·
[Extraction and validation](docs/topics/extraction/extraction.md)

The kit carries the existing chapter reader and build-sheet layout: full-width
cards, docked navigation, one/two/all-chapter views, pinned comparisons, optional
reading layers, code highlighting, local math rendering, diagrams, figure
controls, carousels, lightboxes and locally bundled fonts. It needs no JavaScript
package installation for building a site.

Independent comparisons can use the shared [panel switcher](docs/topics/panel-switcher/panel-switcher.md),
including button controls, hash reveal, print restoration and no-script reading.

## Start a project

Add this repository at `.docs-kit` using its shared repository URL:

```bash
git submodule add <shared-repository-url> .docs-kit
git submodule update --init --recursive
python3.12 -m venv .build/docs-env
.build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
.build/docs-env/bin/python .docs-kit/docsite.py init .
```

`init` adds the starter only after checking every destination. It refuses to
overwrite existing files. For an existing documentation system, keep its
content, add the configuration deliberately and follow [adoption](rules/maintenance.md).

For local-only use, add the kit with
`git -c protocol.file.allow=always submodule add /path/to/documentation-kit .docs-kit`.
Use a shared remote URL when distributing consuming repositories to others.

Edit `docs/site/site.toml`: set the project title, sidebar home label, source
repository/ref and navigation. Set `page_css = ["build-sheet.css"]` on pages
that use the shared layout. Add `.build/` to the project's `.gitignore`, then
track the authored sources before building:

```bash
git add docs AGENTS.md CLAUDE.md .gitmodules .docs-kit
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
python3.12 -m http.server 8321 --bind 127.0.0.1 --directory .build/docs
```

Open `http://127.0.0.1:8321/html/guide.html` to inspect the starter. The home
page is `html/index.html`. The server exposes generated output only.

## Ownership

| Shared kit | Each project |
|---|---|
| `rules/`: canonical engineering, documentation, writing and site practices | `docs/PROJECT_CONTEXT.md` and `docs/index.md`: orientation, reading routes and project-specific additions |
| `theme/`: HTML shell, chapter reader, common CSS/JS, fonts and math assets | `docs/topics/`: records and optional rendered `index.md` pages |
| `tooling/` and `docsite.py`: renderer, packaging and checks | `docs/site/site.toml`, local CSS/components/fragments, `docs/figures/` |
| `examples/starter/`: authoring reference and initial project skeleton | `docs/development/` when needed, open plans, evidence, dated sessions and `docs/worklog.md` |

The starter uses one [task router](examples/starter/AGENTS.md) with named paths
for Codex and a [Claude import](examples/starter/CLAUDE.md) of that same router.
Read the shared rules before the actions named by the router. Keep project
exceptions in project-owned records. Change common rules in this repository.

The [shared Git guide](rules/engineering/git.md) covers commit scope, required
explanatory message bodies, validation, shared staging areas and history.
Projects route contributors to it before Git actions and keep concrete test
commands and acceptance gates in their own records.
The [delivery guide](rules/engineering/delivery.md) covers assignment scope,
owner responsibility, coordination, parallel work and escalation.
The [handoff guide](rules/engineering/handoffs.md) covers completion, blockers,
supporting records and receipt of work.

## Focused guides

Read only the guides matching the action. [Documentation reading index](docs/index.md)
links to the kit's contracts, evidence and chronology.

| Area | Guides |
|---|---|
| Engineering | [Code and generated files](rules/engineering/code.md), [performance](rules/engineering/performance.md), [execution and resources](rules/engineering/execution.md) |
| Delivery | [Ownership](rules/engineering/delivery.md), [handoffs](rules/engineering/handoffs.md), [Git](rules/engineering/git.md) |
| Documentation | [Canonical homes and lifecycle](rules/documentation.md) |
| Writing | [Pages and review](rules/writing/pages.md), [explanations](rules/writing/explanations.md), [measurements](rules/writing/evidence.md), [figures and access](rules/writing/figures.md), [math](rules/writing/math.md), [code and diagrams](rules/writing/code.md) |
| Site | [Authoring](rules/site/authoring.md), [validation](rules/site/validation.md), [resources](rules/site/resources.md), [publication](rules/site/publication.md), [reader](rules/site/reader.md) |

The original [writing](rules/writing.md) and [maintenance](rules/maintenance.md)
entrypoints remain short routers with their existing section anchors. Projects
keep concrete tools, workloads, resource profiles, acceptance thresholds and
runtime requirements in their own records.

## Pin and upgrade

A project records the kit's exact commit as its submodule pointer. Changes here
do not silently upgrade consumers. Clone consuming repositories recursively:

```bash
git clone --recurse-submodules <project-url>
```

To adopt a reviewed kit update:

```bash
git -C .docs-kit fetch --tags
git -C .docs-kit checkout <reviewed-kit-commit-or-tag>
.build/docs-env/bin/python .docs-kit/docsite.py build --project .
.build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
git add .docs-kit
```

The kit is versioned in `VERSION` and tagged `v<version>`. [Releases and
upgrades](docs/topics/releases/releases.md) lists what each version changes for
consumers and the migration steps; 1.0.0 is the first stable version.
The current 1.1.0 release has a focused [consumer migration guide](docs/topics/releases/migrations/1.1.0.md).

Review changed human pages at wide and narrow widths before committing the
pointer and any consumer adaptations together. Share common changes upstream;
avoid editing a consumer's detached submodule checkout as its only live copy.

## Commands

```bash
python .docs-kit/docsite.py build --project . --page guide
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py lint --project . --registry
python .docs-kit/docsite.py slides --project . --select guide --select other#intro,result --out review --title "Review"
```

Python 3.12 is the validated runtime; the entrypoint requires at least 3.12.
Dependencies are pinned in `requirements.txt`. Node.js 22 is used for kit
development checks, not for building a consuming site.

The build packages tracked resources only, rejects missing media and symlink
escapes, checks resource closure and detects stray generated files. Local-only
captures require explicit configuration. Optional `evidence_manifests` enable
exact-byte verification without requiring any platform-specific collection.
See [maintenance](rules/maintenance.md) for source paths and extension points.

Chapters can open with a 16:9 [slide face](rules/site/authoring.md#slide-faces-and-decks);
the `slides` command collects faces from any reader or card-structured pages into a presentable, printable deck
under `.build/slides/`.

Existing sites can use the shared [publication exporter](rules/site/publication.md#exporting-into-an-existing-publication)
to preserve their public routes and selected evidence. The
[browser-check helpers](rules/site/validation.md#reusable-browser-checks) support
project harnesses without moving their domain assertions. Homepage composition
stays [project-owned](rules/writing/pages.md#project-owned-homepages); the starter is
optional.

## Develop the kit

```bash
python -m pip install -r requirements.txt
python docsite.py build --project examples/starter
python docsite.py lint --project examples/starter --strict
DOCSITE_PROJECT_ROOT="$PWD/examples/starter" PYTHONPATH=tooling python -m unittest discover -s tests -p 'test_*.py'
node tests/test_math_runtime.cjs
node tests/test_site_filelinks.cjs
```

The independent-consumer tests create disposable Git repositories. Build output
stays under each consumer's `.build/docs/`; tools never infer the consumer from
where the kit happens to be installed.

Optional real-browser review uses Playwright and Chromium supplied by the
development environment:

```bash
DOCS_PLAYWRIGHT=/path/to/playwright DOCS_CHROMIUM=/path/to/chromium node tests/visual_review.cjs
DOCS_PLAYWRIGHT=/path/to/playwright DOCS_CHROMIUM=/path/to/chromium node tests/test_browser_checks.cjs
DOCS_PLAYWRIGHT=/path/to/playwright DOCS_CHROMIUM=/path/to/chromium node tests/test_panel_switcher.cjs
```

It starts an owned loopback server, checks desktop/phone and paired layouts,
mobile table scrolling and no-JavaScript reading, then closes browser and server.
Screenshots stay under `.build/visual-review/`.

## Provenance

Extracted from the Autonomous Driving Platform documentation system on
2026-11-04. [Source hashes](provenance.json) identify the original files and
inspected revision; [policy coverage](rules/extraction-map.md) accounts for the
source sections. This repository contains shared rules and presentation code,
not simulator code, research results or historical evidence collections.

Vendor licenses and source notes are retained beside their assets; see
[third-party notices](THIRD_PARTY.md). A first-party license has not been
selected for this initial local repository.
