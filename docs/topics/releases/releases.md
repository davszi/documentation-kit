# Releases and upgrades

The kit's version is in [`VERSION`](../../../VERSION); each release is tagged `v<version>`.
A consuming project pins an exact commit or tag and upgrades deliberately, following
[Pin and upgrade](../../../README.md#pin-and-upgrade). This record lists what each
release changes for consumers and how to move to it. Chronology stays in the
[worklog](../../worklog.md); consumer adoption status stays in each consuming project.

## 1.1.0 — focused engineering and documentation guides

1.1.0 adds compatible policy routes and optional evidence configuration to the
1.0.0 stable surface. Existing commands, configuration and adapter signatures
remain available. Follow the [1.1.0 migration guide](migrations/1.1.0.md); adopting
the kit does not require moving an existing consumer's documentation layout.

| Area | Consumer change | Owning contract |
|---|---|---|
| Engineering and delivery | Focused code, performance, execution, delivery and handoff guides; shared Git rules require an explanatory commit body and explicit ownership of shared staging | [Engineering guides](../../../README.md#focused-guides), [Git](../../../rules/engineering/git.md) |
| Contributor entrypoints | One task-triggered `AGENTS.md` router, with a bare `@AGENTS.md` import for Claude; revised starter orientation and reading index | [Agent entrypoints](../../../rules/documentation.md#agent-entrypoints-import-versus-point) |
| Writing and site ownership | Focused `rules/writing/` and `rules/site/` guides; original writing/maintenance routes and their anchors remain available | [Writing](../../../rules/writing.md), [site](../../../rules/maintenance.md) |
| Visual and evidence guidance | Figures lead mechanism/geometric explanations; scope stays beside evidence; representation follows the question; failed attempts and original settings remain with their evidence | [Page design](../../../rules/writing/pages.md#page-design), [figures](../../../rules/writing/figures.md#figures-and-comparisons), [evidence](../../../rules/writing/evidence.md#numbers-and-staleness) |
| Optional project layout | New starter uses `docs/PROJECT_CONTEXT.md` and `docs/index.md`; existing project destinations and historical routes stay project-owned | [Canonical homes](../../../rules/documentation.md#canonical-homes), [optional layout migration](migrations/1.1.0.md#optional-project-layout-migration) |
| Local media inventories | Optional `local_artifacts_manifest` selects the inventory path; omitted settings retain the legacy fallback and explicitly missing configured files fail | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Exact source snapshots | Optional evidence-adapter `document_origin(path, *, root)` preserves registered snapshot origins, with containment checks and all link/anchor/snippet validation retained | [Evidence adapter](../../../rules/site/resources.md#resource-closure-and-evidence) |

### Validation and adoption scope

The integrated kit passed starter strict lint with zero warnings, all 86 Python
tests, reader-content preservation and both Node checks. Real Chromium checks
covered 1600 × 1000 and 390 × 844 reader/home layouts, paired navigation,
browser-helper and panel-switcher fixtures, slide fit and Continue/Back, deck
presentation/print and narrow no-JavaScript reading. Saved wide, narrow, paired
and deck screenshots were inspected. The [worklog](../../worklog.md#2026-11-07--integrate-upstream-releases-and-slide-support)
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
| Reader | Chapter slide faces (`<!-- slide -->`), the `slides` deck command, wider One-chapter cards (88% of the stage) | [maintenance](../../../rules/maintenance.md#slide-faces-and-decks), [writing](../../../rules/writing.md#slide-faces) |
| Components | `panel-switcher` local comparisons | [panel switcher](../panel-switcher/panel-switcher.md) |
| Includes | Shared theme includes resolve first; included fragments may include others (eight levels, cycles fail) | [authoring paths](../../../rules/maintenance.md#authoring-paths) |
| Configuration | `[[nav]]` tables accept only `label`, `file`, `group`, `short`, `hidden`; project adapters (`path_resolver`, `evidence_validator`, `content_transform`), `extra_assets`, `body_class`, a configured `worklog` path (`extra_components` already existed in 0.1.0) | [maintenance](../../../rules/maintenance.md) |
| Home page | Site-map cards use frontmatter `description` and `thumbnail` when present; guidance to keep the same site tree on every page (`toc = []` on a reader-free home) | [shared reading layout](../../../rules/maintenance.md#shared-reading-layout), [writing](../../../rules/writing.md#project-owned-homepages) |
| Publication | Exporter into an existing publication (`tooling/publication.py`) | [exporting](../../../rules/maintenance.md#exporting-into-an-existing-publication) |
| Generators and checks | `tooling/svg_figures.py`, `tooling/number_ledger.py`, `tooling/verbatim_blocks.py`; browser helpers `slideFaces` and `captureElement` | [generated figures](../../../rules/maintenance.md#generated-figures), [browser checks](../../../rules/maintenance.md#reusable-browser-checks) |
| Rules | Numbers restated by a redesign need ledger sources; generated SVG uses literal colours | [numbers and staleness](../../../rules/writing.md#numbers-and-staleness) |

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
changes, from pins 37ac1dc and 80b42f4; [the receipt](../../../verification/v1.0.0-consumers.json)
records inputs, commands and results. No consumer pinned at v0.1.0 was available
to test. Each consumer still adopts 1.0.0 through its own reviewed change.
