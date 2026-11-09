# Releases and upgrades

The kit's version is in [`VERSION`](../../../VERSION); each release is tagged `v<version>`.
A consuming project pins an exact commit or tag and upgrades deliberately, following
[Pin and upgrade](../../../README.md#pin-and-upgrade). This record lists what each
release changes for consumers and how to move to it. Chronology stays in the
[worklog](../../KIT_WORKLOG.md); consumer adoption status stays in each consuming project.

## What a version number promises

The [stable and provisional interfaces](#100--first-stable-version) list what a
project may rely on. From 3.0.0 the version number means this:

- A **major** release removes or renames a stable interface, including a
  section anchor under `rules/`, or adds a lint error that fails without
  `--strict`.
- A **minor** release adds to the stable interfaces. It may also add lint
  warnings, which fail `--strict`, change how the shared theme looks, and change
  or remove a provisional interface.

The release notes list every such change, and the version's migration guide
gives the step for each. A minor upgrade can therefore need work: the
[project conformance check](../../../rules/conformance.md) runs strict lint and
shows the new warnings.

## 3.0.0 — router anchors removed, topic records and repository files in the sidebar

Not tagged yet: these changes are on `main` after 2.0.0, and `VERSION` changes
when the release is tagged. It is a major release under
[what a version number promises](#what-a-version-number-promises) for one
reason: it removes section anchors under `rules/`. `rules/writing.md` and `rules/maintenance.md` lose their
section anchors, and record rules move into the new `rules/records.md`, so a
project that links to the old locations fails lint until it repoints the links. No command, configuration key, marker or adapter signature is removed.
Follow the [3.0.0 migration guide](migrations/3.0.0.md).
One check can fail a strict lint run: a topic page without a record
must add one or declare `page_only`. Two provisional tooling modules that no
known consumer imported are removed. A project that wants to keep the
∿ sidebar mark sets `brand_mark = "∿"`. Build-sheet flows now stack
vertically when their chapter card or page is narrow; grids, checks and
chapter headlines follow the card's width; box lists use dashes and tinted code
chips, and code keeps its case inside uppercase titles.

| Area | Consumer change | Owning contract |
|---|---|---|
| Sidebar | A site with at least one `[[source_pages]]` entry gets a **Reference** section after its navigation: records with `pinned = true` listed first, then a **Browse by folder** tree of every registered file, closed on pages for people. Sites without registered files are unchanged | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Assets | Pages load shared assets with a content-hash query, `assets/<file>?v=<hash>`, so browsers fetch a changed stylesheet or script after a rebuild; unchanged assets stay cached | [Authoring and configuration](../../../rules/site/authoring.md) |
| Sidebar header | The ∿ mark is no longer shared: optional `brand_mark` sets a project's own mark (up to three characters or a tracked SVG); without it the mark is the title's initials. To keep ∿, set `brand_mark = "∿"`. The reader drawer shows the same mark and name as other pages and no longer shows a chapter counter; hiding the menu applies across the site instead of per page. Groups without a CSS colour get tones in order | [Authoring and configuration](../../../rules/site/authoring.md) |
| Topics | Every topic has a record; a topic page without one declares `page_only = "<reason>"` in its frontmatter. Lint warns about a topic page with neither, so `--strict` fails until the project adds a record or the declaration | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Lint | When a record section changes, lint prints notes naming the pages that link to it; `--since <rev>` compares with an older commit. Notes never fail lint | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Lint | New optional setting `page_number_notes = true`: lint prints a note for each number in a topic page's prose that none of the page's linked records state. Values shown as code, labels, versions, dates and ratios are not read; a page that links no record is skipped. Notes never fail lint. Off by default, and not meant for pages that report measurements from experiment data | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Reader rule | The sidebar docks by default on screens wider than 900 px; the guide now states the value the shared reader already used | [Shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Conformance | New guide: the project conformance check to run when a kit pin moves or a repository changes hands; the starter router routes to it | [Project conformance check](../../../rules/conformance.md) |
| Configuration | A registered source page no longer needs a `[[nav]]` entry; topic pages still do. `[[source_pages]]` accepts optional `pinned = true` | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Rules | Removed: the stub headings in `rules/writing.md` and `rules/maintenance.md`, which only forwarded old links. Both files are now plain indexes of the focused guides. A link to one of their former anchors must point at the focused guide's own section; links to the files without an anchor still work | [Router anchors](migrations/3.0.0.md#router-anchors) |
| Rules | Records and pages are documented in a fixed order: the working agent writes the record first, and a page for people is made on request, by a separate agent where the runtime supports delegation. New guide `rules/records.md` gathers what a record needs; `rules/writing/` now covers pages; its rules about what a code excerpt, a formula or an experiment visual may claim still apply to records. `rules/writing/evidence.md` is removed and six sections moved, so links to them must be repointed. The starter router has three documentation rows in place of two | [Record first, page on request](../../../rules/documentation.md#record-first-page-on-request), [sections that moved](migrations/3.0.0.md#sections-that-moved) |
| Rules | Every visual change is reviewed by eye before it is reported done, from whole-element captures at each supported width and reader view | [Validation and review](../../../rules/site/validation.md#validation-and-review) |
| Rules | A worklog entry and its commit message cover the same landing on purpose and are written in the same step. `OPEN.md` format, which lint already checked, is now stated | [Rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology), [open work](../../../rules/documentation.md#from-open-work-to-subject-knowledge) |
| Starter | The home page links `../PROJECT_CONTEXT.md`; the 2.0.0 starter linked a file that does not exist. The reading index has three documentation rows in place of two | [Starter home link](migrations/3.0.0.md#starter-home-link), [reading index](migrations/3.0.0.md#reading-index) |
| Build fix | A paragraph that directly follows a fold now renders as Markdown. Before, the closing fold marker swallowed the blank line after it, and the paragraph, typically a "Full guide" line with links, appeared as raw text. Pages with such paragraphs change in the built output | [Story and reading layers](../../../rules/writing/explanations.md#story-and-reading-layers) |
| License | The kit's own rules, tooling, theme and starter are under the MIT License; bundled fonts and KaTeX keep their own licenses. Earlier versions granted no license. Every built site gains one file, `html/assets/documentation-kit/LICENSE`; a project asset with that output name fails the build | [License](../../../README.md#license) |
| Tooling | Removed: `tooling/number_ledger.py` and `tooling/verbatim_blocks.py`, both provisional since 1.0.0. The rule that a redesign records number sources in a ledger and locks kept blocks stays; each project keeps its own ledger format and checks. `tooling/svg_figures.py` stays | [Numbers and staleness](../../../rules/records.md#numbers-and-staleness) |

## 2.0.0 — source pages, kit website, configured publication and compatibility removals

2.0.0 is a major release because it breaks the 1.x contract in two places,
under [refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility):
the exporter no longer renames or relocates files, and the old local-artifact
manifest location is no longer read. `docsite.py lint` also fails a project
whose pinned kit commit is on no remote branch of the kit. Everything else adds
to the 1.x surface. Every consumer follows the
[2.0.0 migration guide](migrations/2.0.0.md); a consumer that uses neither
removed form only adds one router row. The 1.0.0 stable and provisional
interfaces below still apply to 2.x, apart from these removals.

| Area | Consumer change | Owning contract |
|---|---|---|
| Configuration | Optional `[[source_pages]]` tables render an existing tracked Markdown file as a whole-file page at a chosen route; links and media resolve from the file's own folder | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Build checks | Fragments into a registered page, and every fragment a registered page links, must match a rendered anchor; registry, containment and route-collision errors fail the build | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Lint | Registered files' Markdown links are checked as ordinary records | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Theme | Additive `base.css` rules for the source line (`.source-origin`) and the opt-in `reference-page` body class, whose Markdown tables also get the labelled narrow-screen scroll region; existing pages render unchanged | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Build manifest | `site-build.json` gains a `source_pages` map from route to source file | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Navigation | Optional `nested_nav = true` folds navigation groups and nests the current page's sections under its entry; the flat tree remains the default | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Reader | A registered page with `reader = true` merges a short opening and its source line into the first chapter; longer openings stay a separate chapter | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Sidebar | A registered page without the reader that is listed in the navigation keeps the site tree in its sidebar, marked as current; hidden registered pages, and pages under `nested_nav`, still list their sections | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Theme fixes | A carousel inside a build-sheet grid figure now shows one slide at a time (its rule outranks `.bs-grid figure img`); the reader help describes docking with `«` and `☰` instead of a pin button that is not shown | [Reader](../../../rules/site/reader.md#shared-reading-layout) |
| Repository | Extraction history is removed: `provenance.json`, `verification/`, `preview/`, the extraction record and `rules/extraction-map.md`. Nothing consumers run or route to used them; they remain at the `v1.1.0` tag | [Kit context](../../KIT_CONTEXT.md) |
| Starter | Entry files are stored as `*.tmpl` and written under their real names by `init`, which gains `--title` and `--repository` for `site.toml`; generated projects are unchanged apart from those values | [Start a project](../../../README.md#start-a-project) |
| Lint | Optional `open_work` setting names the open-work file (default `docs/open/OPEN.md`); every worklog check now honours the existing `worklog` setting | [Resources and evidence](../../../rules/site/resources.md) |
| Repository | The kit's own entry files are `docs/KIT_CONTEXT.md`, `docs/KIT_INDEX.md`, `docs/KIT_WORKLOG.md` and `docs/open/KIT_OPEN.md`; its `AGENTS.md` and `CLAUDE.md` state they apply only to the kit repository | [Kit context](../../KIT_CONTEXT.md) |
| Engineering guide | New "Refactoring over compatibility" section in the code guide: ask the owner, with evidence, before changing a form others may still use; once the owner decides no compatibility is needed, update every reference and remove the old form. The documentation guide no longer allows compatibility routes by default | [Refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility) |
| Publication export | Removed: `export_pages` no longer takes `page_routes`; every generated file keeps its name. `public_files` is a list of tracked paths published at the same path, not a mapping | [Publication export](../../../rules/site/publication.md) |
| Evidence configuration | Removed: an absent `docs/evidence/local-artifacts.json` no longer falls back to `docs/project/local-artifacts.json`. The resources guide records why the path adapter is kept and when a project removes it | [Resources and evidence](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Publication command | New `docsite.py publish --project . --out _site` builds and exports a fresh public bundle configured by `[publication]` (`assets_manifest`, `pages`, `private_suffixes`, `private_prefixes`); other keys fail. `site-build.json` gains `resource_origins` | [Configured publication](../../../rules/site/publication.md#configured-publication) |
| Kit pin | `docsite.py lint` fails when a consumer's pinned kit commit is on none of the kit's remote branches. The Git guide forbids commits inside `.docs-kit` and the starter router routes kit changes there | [The shared kit submodule](../../../rules/engineering/git.md#the-shared-kit-submodule) |
| Kit website | The kit builds its own reference site from the repository root | [Website record](../website/website.md) |
| Experiment guides | New shared guides: experiments are investigations or qualifications, start small and state a budget; a pre-stated bar and verdict are required for confirmatory investigations and qualifications; terms for learned or fitted models, such as final runs, are scoped to their own section; claim-scoped verification and regression gates; routes added to the starter's `AGENTS.md` | [Workflow](../../../rules/experiments/workflow.md), [verification](../../../rules/experiments/verification.md) |

When the kit website was added, the starter's generated pages were
byte-identical to 1.1.0 output, with only `assets/base.css` and
`site-build.json` differing; later 2.0.0 changes were not compared byte for
byte. Validation is recorded in the
[worklog](../../KIT_WORKLOG.md#2026-11-07--build-the-kits-reference-website).

## 1.1.0 — focused engineering and documentation guides

1.1.0 adds compatible policy routes and optional evidence configuration to the
1.0.0 stable surface. Existing commands, configuration and adapter signatures
remain available. Follow the [1.1.0 migration guide](migrations/1.1.0.md); adopting
the kit does not require moving an existing consumer's documentation layout.

| Area | Consumer change | Owning contract |
|---|---|---|
| Engineering and delivery | Focused code, performance, execution, delivery and handoff guides; shared Git rules require an explanatory commit body and explicit ownership of shared staging | [Engineering guides](../../../README.md#focused-guides), [Git](../../../rules/engineering/git.md) |
| Contributor entrypoints | One task-triggered `AGENTS.md` router, with a bare `@AGENTS.md` import for Claude; revised starter orientation and reading index | [Agent entrypoints](../../../rules/documentation.md#agent-entrypoints-import-versus-point) |
| Writing and site ownership | Focused `rules/writing/` and `rules/site/` guides; original writing/maintenance routes and their anchors remain available (the anchors until 3.0.0) | [Writing](../../../rules/writing.md), [site](../../../rules/maintenance.md) |
| Visual and evidence guidance | Figures lead mechanism/geometric explanations; scope stays beside evidence; representation follows the question; failed attempts and original settings remain with their evidence | [Page design](../../../rules/writing/pages.md#page-design), [figures](../../../rules/writing/figures.md#figures-and-comparisons), [evidence](../../../rules/records.md#numbers-and-staleness) |
| Optional project layout | New starter uses `docs/PROJECT_CONTEXT.md` and `docs/index.md`; existing project destinations and historical routes stay project-owned | [Canonical homes](../../../rules/documentation.md#canonical-homes), [optional layout migration](migrations/1.1.0.md#optional-project-layout-migration) |
| Local media inventories | Optional `local_artifacts_manifest` selects the inventory path; omitted settings retain the legacy fallback and explicitly missing configured files fail | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Exact source snapshots | Optional evidence-adapter `document_origin(path, *, root)` preserves registered snapshot origins, with containment checks and all link/anchor/snippet validation retained | [Evidence adapter](../../../rules/site/resources.md#resource-closure-and-evidence) |

### Validation and adoption scope

The integrated kit passed starter strict lint with zero warnings, all 86 Python
tests, reader-content preservation and both Node checks. Real Chromium checks
covered 1600 × 1000 and 390 × 844 reader/home layouts, paired navigation,
browser-helper and panel-switcher fixtures, slide fit and Continue/Back, deck
presentation/print and narrow no-JavaScript reading. Saved wide, narrow, paired
and deck screenshots were inspected. The [worklog](../../KIT_WORKLOG.md#2026-11-07--integrate-upstream-releases-and-slide-support)
records failed browser attempts, corrected harness settings and cleanup scope.

These are kit/starter checks. Each consumer still owns its exact-pin adoption,
source/content comparison, required checks and wide/narrow rendered review;
no consumer adoption or deployment is established by this release record.

## 1.0.0 — first stable version

1.0.0 is the first version with a stable contract. Later 1.x releases add to it
without breaking it; a 2.0.0 would announce a breaking change here with its
migration steps.

| Stable in 1.x | Provisional in 1.x (may change in a minor release, with a note here) |
|---|---|
| `docsite.py` commands and flags (`init`, `build`, `lint`, `slides`) | `tooling/svg_figures.py`, `tooling/number_ledger.py`, `tooling/verbatim_blocks.py` |
| `site.toml` keys and `[[nav]]` keys; page frontmatter keys | `tooling/browser_checks.cjs` exports |
| Markers: `<!-- include: … -->`, `<!-- site-map -->`, `<!-- slide -->`, `<!-- page-end -->`, typed folds | `tooling/publication.py` (`export_pages`) |
| Shared components by name and their authoring markup | Theme CSS class names other than documented authoring markup |
| Project adapter signatures (`path_resolver`, `evidence_validator`, `content_transform`) | |
| `rules/` policies (wording may be refined) | |

### What 1.0.0 contains (since 0.1.0)

| Area | Change | Owning contract |
|---|---|---|
| Reader | Chapter slide faces (`<!-- slide -->`), the `slides` deck command, wider One-chapter cards (88% of the stage) | [maintenance](../../../rules/site/authoring.md#slide-faces-and-decks), [writing](../../../rules/writing/pages.md#slide-faces) |
| Components | `panel-switcher` local comparisons | [panel switcher](../panel-switcher/panel-switcher.md) |
| Includes | Shared theme includes resolve first; included fragments may include others (eight levels, cycles fail) | [authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Configuration | `[[nav]]` tables accept only `label`, `file`, `group`, `short`, `hidden`; project adapters (`path_resolver`, `evidence_validator`, `content_transform`), `extra_assets`, `body_class`, a configured `worklog` path (`extra_components` already existed in 0.1.0) | [maintenance](../../../rules/maintenance.md) |
| Home page | Site-map cards use frontmatter `description` and `thumbnail` when present; guidance to keep the same site tree on every page (`toc = []` on a reader-free home) | [shared reading layout](../../../rules/site/reader.md#shared-reading-layout), [writing](../../../rules/writing/pages.md#project-owned-homepages) |
| Publication | Exporter into an existing publication (`tooling/publication.py`) | [exporting](../../../rules/site/publication.md#exporting-into-an-existing-publication) |
| Generators and checks | `tooling/svg_figures.py`, `tooling/number_ledger.py`, `tooling/verbatim_blocks.py`; browser helpers `slideFaces` and `captureElement` | [generated figures](../../../rules/site/authoring.md#generated-figures), [browser checks](../../../rules/site/validation.md#reusable-browser-checks) |
| Rules | Numbers restated by a redesign need ledger sources; generated SVG uses literal colours | [numbers and staleness](../../../rules/records.md#numbers-and-staleness) |

### Migrating to 1.0.0

Do this as one reviewed deliverable in the consuming project, on its own branch.

1. **Record where you start.** Note the current pin (`git -C .docs-kit rev-parse HEAD`)
   and keep a build of the current site for comparison:

   ```bash
   .build/docs-env/bin/python .docs-kit/docsite.py build --project .
   (cd .build/docs && find . -name '*.html' -type f | sort | xargs sha256sum) > /tmp/docs-before.txt
   ```

2. **Move the pin.**

   ```bash
   git -C .docs-kit fetch --tags
   git -C .docs-kit checkout v1.0.0
   .build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
   ```

3. **Fix configuration the build now rejects.**
   - A `[[nav]]` entry with any key other than `label`, `file`, `group`, `short` or
     `hidden` fails the build. This almost always means a top-level setting was
     written below a `[[nav]]` header, where TOML assigns it to that table: move
     the setting above the first `[[nav]]`.
   - A fragment that contains a literal `<!-- include: … -->` marker it does not
     mean to expand would now be expanded. Includes expand before Markdown, so a
     fenced code block does not protect the marker: write such examples in raw
     HTML as `<code>&lt;!-- include: … --&gt;</code>`. No known consumer had one.
   - Includes resolve a shared theme file first (since 37ac1dc): a project fragment
     named like a theme file, such as `components/shell.html` or
     `components/chapter-reader.html`, is no longer used. Rename it.
   - Include paths must be relative and contained; an absolute path or `..` stops
     the build. Move the file under `docs/site/` or the theme.
   - `description` and `thumbnail` are now page frontmatter keys. If a content
     transform already emits keys with these names, they must be non-empty strings.

4. **Build, lint and compare.**

   ```bash
   .build/docs-env/bin/python .docs-kit/docsite.py build --project .
   .build/docs-env/bin/python .docs-kit/docsite.py build --project . --check
   .build/docs-env/bin/python .docs-kit/docsite.py lint --project . --strict
   (cd .build/docs && find . -name '*.html' -type f | sort | xargs sha256sum) > /tmp/docs-after.txt
   diff /tmp/docs-before.txt /tmp/docs-after.txt
   ```

   For projects pinned at 37ac1dc or later, pages without slide markers or nested
   includes were byte-identical in the compatibility builds below, except site-map
   cards: their thumbnails are now marked decorative (`data-decorative`, and an
   inlined SVG thumbnail gets `aria-hidden="true"` instead of an unlabelled image
   role). Shared CSS and JavaScript assets change. From older pins, expect page
   differences from the reader and include changes. Explain every page that differs. Run the project's own checks and its rendered wide/narrow review.

5. **Commit the pointer with any adaptations** and record the adopted version,
   the comparison and the checks in the project's worklog.

### Optional adoption after upgrading

None of these is required; adopt them when a page needs them.

- **Slide faces.** Add one `<!-- slide -->` block at the start of a chapter. A
  face summarises its chapter and shows no number the chapter does not show.
- **Consistent navigation.** On a reader-free home page, set `toc = []` and add
  `<!-- site-map -->`; give each listed page a `description` and, when its first
  image is not a good card picture, a `thumbnail`.
- **Generated figures.** Import `svg_figures` from `.docs-kit/tooling` in a project
  generator with a `--check` mode, and run that check with the project's tests.
- **Number ledgers and verbatim locks.** When a redesign restates numbers, keep a
  ledger per section and call `number_ledger.check` from a project test with the
  project's evidence namespace; lock blocks kept unchanged with `verbatim_blocks`.
- **Captures.** Use `captureElement` from `tooling/browser_checks.cjs` for figure,
  slide and whole-chapter screenshots in review scripts.

### Compatibility evidence

Before release, both known consumers were built with this version without source
changes, from pins 37ac1dc and 80b42f4; [the receipt](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/v1.0.0-consumers.json)
records inputs, commands and results. No consumer pinned at v0.1.0 was available
to test. Each consumer still adopts 1.0.0 through its own reviewed change.
