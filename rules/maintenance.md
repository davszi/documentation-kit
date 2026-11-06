# Site authoring and maintenance

The shared kit owns the engine, theme and reader. A consuming repository owns its content, local assets, navigation and pinned kit revision. The [documentation system](documentation.md) owns canonical homes and lifecycle; [writing rules](writing.md) own content and evidence.

## Tooling and ownership

| Location in consuming repository | Responsibility |
|---|---|
| `.docs-kit/` | Git submodule at a reviewed commit: shared rules, engine, templates, components, dependencies and checks |
| `docs/topics/<topic>/index.md` | Editable rendered page, with supporting records beside it |
| `docs/site/site.toml` | Project title, source repository/ref, navigation, reader and project resource configuration |
| `docs/site/assets/`, `docs/site/fragments/` | Project-owned assets and explicit overrides; do not copy the entire theme |
| `docs/figures/` | Shared project figures with declared provenance |
| `.build/docs/` | Reproducible generated output, ignored by Git |

Initialize the submodule before building. The kit is versioned in `VERSION` and
tagged `v<version>`; [release notes](../docs/topics/releases/releases.md) list each
version's changes and its migration steps. Upgrade the pin as a reviewed deliverable, run the shared and consumer checks, and record the adopted revision and compatibility evidence. Do not edit a detached submodule as a substitute for a shared-kit change. Engine and shared-theme changes belong upstream; project content and optional extensions stay local.

From the consuming project root, use the pinned kit directly:

```bash
python -m pip install -r .docs-kit/requirements.txt
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py lint --project .
```

Use `--page <slug>` with build for targeted iteration. Lint supports `--strict` and `--registry`. The kit README owns installation and shared-engine development checks. The project's `docs/project/PROJECT_CONTEXT.md` records its tested environment and additional checks. Pin dependency versions; documentation builds must not require importing the consuming application's runtime or initializing a GPU.

## Authoring paths

Only registered `docs/topics/*/index.md` entry pages render. Every new entry page needs frontmatter with `title` and `toc` (an empty list is valid with automatic chapters), plus a corresponding `[[nav]]` entry in `docs/site/site.toml`. The folder supplies its public slug; set `slug = "index"` on the home page. Slugs are lowercase filename stems without directories. Use `hidden = true` for a built, directly reachable page outside navigation, subject to the documentation deletion policy.

A rendered page body above `<!-- page-end -->` uses the logical public `docs/html/` URL origin, mapped to `.build/docs/html/`. Its source-only notes tail resolves from the actual source folder. Normal Markdown records resolve links from their own folder.

| Context | Example | Meaning |
|---|---|---|
| Rendered page body | `guide.html#publish` | Generated page and stable anchor |
| Rendered page body | `../figures/example.svg` | Shared project figure |
| Rendered page body | `../../experiments/example/results.json` | Repository evidence/source |
| Rendered page body | `../topics/guide/guide.md` | Explicit agent record/source |
| Notes tail | `../other/other.md` | Sibling topic record, source-relative |
| Notes tail | `evidence/source.md` | Supporting record in the current topic |

Prefer `.html` links when the purpose is reading a page and explicit source links when inspecting source is intended. Raw Markdown viewing does not apply generated-origin interpretation. Preserve source path and fragment metadata so local and hosted source links retain identity.

Includes select a matching shared theme file first (for example,
`components/chapter-reader.html`); project fragments otherwise resolve from
`docs/site/`. Include paths stay relative and contained. `page_css = ["build-sheet.css"]`
selects the kit's shared theme resource. Local stylesheet entries such as
`../site/assets/example.css` resolve from the shared `docs/topics/` configuration
base. Do not introduce machine-specific absolute paths or remote font/media dependencies.

An included fragment may include further fragments, up to eight levels; a cycle
fails the build. A `[[nav]]` table accepts only `label`, `file`, `group`, `short`
and `hidden`. TOML assigns every key written after a table header to that table,
so keep top-level settings such as `extra_components` above the first `[[nav]]`;
the build rejects any other key inside a nav entry.

### Generated figures

A figure generator reads tracked data, asserts the values its page states and
writes fragments the page includes; a `--check` mode compares without writing and
runs in the project's checks. `tooling/svg_figures.py` supplies the shared markup:
`figure` (numbered caption and a labelled, keyboard-scrollable region), `slide_svg`
(a face without ids), `standalone` (a file usable as `<img>`, such as a slide
shown as an image) and drawing helpers with a literal colour palette. Generated
SVG uses literal colours: surrounding cards may redefine page variables, and an
SVG loaded as an image cannot read them.

`tooling/number_ledger.py` checks that every distinct number a redesigned section
shows has a declared source: a configuration value, project evidence expression,
arithmetic, saved record, quoted text or an explained illustrative value. Values
are unsigned as written. Projects pass their own evidence namespace and keep the
ledgers beside the page. Ledger expressions are executable project code: review
them as code; they are not evaluated in a sandbox. `tooling/verbatim_blocks.py`
hash-locks the blocks a redesign keeps unchanged, so kept evidence wording cannot
change silently; locked blocks and fragments are the only text a ledger may set aside.

Register project-specific script components with `extra_components = ["viewer"]`;
each uses a tracked `docs/site/components/<name>.js`. For dynamically loaded
dependencies, `[extra_assets]` maps output names below `html/assets/` to tracked
project files, for example `"viewer/renderer.js" = "docs/site/assets/vendor/renderer.js"`.
List licenses/source notices alongside their dependencies. Paths must stay
inside the project, and project assets cannot overwrite shared kit assets.

The starter's reader-free home page selects shared `home.css` for its hero,
links and generated topic cards. That stylesheet and arrangement are optional;
projects may author their own homepage and local styles. Follow
[project-owned homepage composition](writing.md#project-owned-homepages).

Wrap a wide comparison table in `.scroll` with `role="region"`, a useful
`aria-label`, `tabindex="0"` and `data-reader-horizontal`. This keeps scrolling
and keyboard arrows inside the table instead of changing chapters.

### Slide faces and decks

Write a chapter's slide face between standalone `<!-- slide -->` and `<!-- /slide -->` lines at the start of the chapter: inside its `section.card`, or directly before its `##` heading on a flat Markdown page. The build converts it into `<div class="slide-face" data-slide-face><div class="slide-canvas">…</div></div>` and loads the shared `slide-face` component automatically. Markdown pages match markers after rendering, so examples inside code blocks stay literal. Unbalanced or nested markers fail the build. Use `p.slide-eyebrow` and `p.slide-title`, not headings: the reader names a chapter by its first heading, which opens the full chapter below the slide.

| Class | Use |
|---|---|
| `slide-lead`, `slide-main`, `slide-scope` | Lead sentence, the flexible visual area, closing scope line |
| `slide-tile` (`is-term`, `is-accent`, `is-warm`, `is-alert`, `is-held`), `slide-tag` | Labelled boxes; emphasised term; dashed held-out or generated item |
| `slide-row`, `slide-steps` | Equal tiles in one row; numbered argument steps |
| `slide-equation`, `slide-column`, `slide-op`, `slide-note` | Terms of a formula with variants listed under each term |
| `slide-factors`, `slide-chip` (`is-key`, `is-alt`, `is-warm`, `is-alert`, `is-held`, `is-mono`) | Labelled rows of options |
| `slide-split` (`is-wide-side`), `slide-figure`, `slide-stats`, `slide-stat` (`is-alt`, `is-warm`, `is-alert`, `is-plain`), `slide-big` | Figure or grid beside headline numbers |
| `slide-legend` | Line and border keys |

The outer face is the size container and every size inside the canvas is a container unit of it, so a face fits identically at every width or not at all. Below 720 px a CSS container query stacks the canvas into a readable column, without JavaScript. Canvas declarations are marked `!important` so page-wide element rules (for example an id-scoped `p` style) cannot change the fixed layout; local slide classes must do the same. Open a page with `?slide-check` to outline faces that do not fit; the deck always shows the outline. Projects add local classes for domain diagrams under the same rule. In the reader, the first heading after the face becomes the chapter's bridge title; an eyebrow immediately before it stays only for assistive technology. A Continue/Back control moves between the slide and the full chapter.

Extract a deck with `python .docs-kit/docsite.py slides --project . --select <slug>[#chapter,…] --out <name> [--title …]`. Repeat `--select` to combine pages; listed chapters keep the given order, a bare slug takes every face in reading order. Chapters are the reader's chapter sections, or the outermost `section.card` elements on pages without the reader. Slide ids are prefixed per slide so pages can share one deck; relative URLs (including `srcset`, `xlink:href` and CSS `url()`) point back into the built site, and links to the rest of a page open that page. Faces from math pages render with the vendored KaTeX. The command builds the site first and writes `.build/slides/<name>.html`, which reuses the built site's assets and stays outside the published bundle. The deck offers an overview, a presentation mode (`P`, arrow keys, `F`, `Esc`) and one-slide-per-page printing for PDF export. Serve `.build/` on loopback to open it.

## Validation and review

Run checks from the consuming project root using the pinned kit. A complete validation must cover:

- Full build, freshness check and link/anchor/snippet/figure lint.
- Shared engine regression suite and applicable project content/interaction checks.
- Exact evidence identities and manifest closure where registered.
- Browser rendering at wide and narrow widths, plus equal-column layout when the reader is used.
- Keyboard navigation/focus, labels/touch targets, reduced motion, no-JavaScript fallback and print.

A page-only build is useful for iteration; it does not validate unrelated output. A freshness check must not mutate output. A strict lint run may treat warnings as errors; document any intentionally retained warning rather than hiding it. A registry listing shows current source declarations; raw searches may also include historical evidence and must not be mistaken for the current registry.

Tests that compare DOM/structure, content or numerical identities are useful evidence. They do not establish browser pixel inspection. Report what was actually run, what passed/skipped and what remains unchecked. Never call a layout checked from source inspection alone.

For local review, serve the generated `.build/docs/` directory on loopback and open `/html/<slug>.html`. Verify the listener belongs to the current checkout. Follow the browser-permission and owned-server rules in the documentation system. Publish only after the consuming project's deployment gate passes; source verification does not verify a hosted deployment.

## Resource closure and evidence

Package only allowlisted tracked inputs actually needed by pages. Do not mirror the repository, include untracked fragments, follow symlinks into unrelated files or upload large local captures automatically. Verify physical closure: referenced CSS, scripts, fonts, figures, media and nested resources must resolve inside the intended bundle or be explicitly declared source/local-evidence links.

Register intentionally retained local media in the project's supported local-artifact manifest or `local_media` configuration. Do not mask a typo or genuinely missing required resource as local evidence. Preserve large recordings and hashes with the producing experiment; publish a tracked poster/keyframe and visible local-capture notice. A deliberately tracked, approved small clip may be packaged. File-mode access to a local recording is not proof that a hosted reader can open it.

Projects with existing historical-path or evidence schemas can register local
Python adapters using `path_resolver = "tools/docs/site_paths.py"` and
`evidence_validator = "tools/docs/evidence_documents.py"` in `site.toml`.
Adapter files must be tracked, contained regular Python files without symlink
components. They execute as project tooling, so review them with configuration.
The path adapter exports `resolve_legacy_path(path, root, *, recorded_roots=())`
and owns the complete mapping, including generated documentation paths. The
evidence adapter exports `MANIFESTS`, `manifest_documents(root, *, require_all_manifests=False)`
returning `(documents, revisions)`, and `verify` with the same arguments; invalid
evidence raises `ValueError`. Projects keep adapter tests and schema policy;
the kit keeps one build/lint engine and uses the adapters consistently.

For generated or sealed content formats, `content_transform` may name a tracked
project module exporting `transform(body, *, metadata, source, root)`. The hook
runs after frontmatter parsing and returns the document body as text, before
shared rendering. It may derive ordinary metadata such as chapter navigation
from the owning source; metadata is validated again afterward. The project owns
source admission, preservation and format-specific tests. This keeps scientific
generators and their immutable outputs separate from current presentation.
Keep `slug` and `page_css` in source frontmatter; the hook cannot change those
structural declarations after page/asset registration.
Use `body_class` for plain project CSS class names when content needs scoped
styles. Common shell, typography and reader behavior stay in the kit.

An existing project may set `worklog = "docs/development/worklog.md"` to retain
its canonical history path. The worklog remains project-owned; the configured
path must stay inside the repository. New projects use `docs/worklog.md`.

Generated figures retain generator, revision, inputs, date and output hash. Frozen document collections retain original logical paths, revisions, bytes and hashes. Validate those identities separately from link resolution and presentation. Do not rewrite historical originals to make current lint convenient.

## Exporting into an existing publication

`tooling/publication.py` exports an already-generated kit bundle into a
project-owned publication directory. It does not build a second site or choose
which repository files are public. Import `export_pages` from the pinned kit's
`tooling` directory after building. Supply:

- `generated_root`, `destination` and repository `root` as explicit paths.
- `tracked` repository paths and `public_files`, a repository-to-public path
  mapping admitted by the project and already present in the publication.
- `page_routes` for generated-to-public paths and `pages` for output HTML to
  rewrite. Unmapped generated outputs retain their names. Relative links account
  for moved pages and their unchanged siblings.
- `private_suffixes`, `private_prefixes` and `local_notice` for the project's
  source-link and unavailable-evidence policy.
- `replace` for the exact existing output paths that may be overwritten.
  Byte-identical copies need no replacement permission.

The exporter validates paths, symlinks, mapped resources and collisions before
writing. It modifies actual HTML attributes and unavailable-evidence anchors;
embedded JavaScript/JSON and unrelated source bytes remain opaque. The shared
source-span parser counts LF exactly as `HTMLParser` does. Keep output selection,
historical guide packaging, source URLs, privacy decisions and deployment
credentials in the consuming project. The generated input is the trusted kit
build, not an arbitrary repository directory.

## Reusable browser checks

`tooling/browser_checks.cjs` accepts an existing Playwright page. It never starts
a browser, server or experiment. Projects own those lifetimes, page routes,
expected counts, screenshots and domain assertions. The shared module provides:

- `slideFaces` lists every slide face with its chapter, size, compact state and
  whether it fits its 16:9 canvas.
- `settle`, `visibleMedia`, `measureOverflow`, `assertHorizontalContainment` and
  `checkLayout` for fonts, actually visible images and viewport containment.
  Image visibility includes ancestor clipping; hidden/inert and offscreen lazy
  images do not become broken-image failures merely because they are mounted.
- `setView`, `activeChapter`, `waitActive` and `goHash` for shared reader control.
- `captureElement(page, selector, file, {unclip?, hide?})` captures one figure,
  face or chapter; `unclip` removes height limits and clipping on the element and
  its ancestors so a reader chapter is captured whole.
- `readerChecks(page, {url, expectedChapters, check?, onPair?})` for real
  navigation/history and comparison pinning. It returns
  `{chapterIds, checked, skipped}`; short readers report impossible interactions
  as skipped rather than passed. Caller callbacks may retain project reports
  and capture the paired state.

Kit fixtures verify both failures and valid contained layouts, including readers
with one to three chapters. The kit's visual review and consuming-project
harnesses use the same functions. Domain numbers, recordings, task controls and
scientific qualification remain project assertions. Run browser jobs under the
consumer's shared local resource policy; importing these helpers grants no
permission to start another heavy job.

## Shared reading layout

Keep fonts and browser/math dependencies vendored with licenses and source/version notices. The shared build-sheet theme uses its bundled font families; pages load no external fonts. Local page CSS adds only page-specific needs.

`chapter_reader = true` in site configuration enables the common reader. Reuse its header, tree navigation, One chapter / Two chapters / All chapters arrangements, pinning, positions and layer choices. Chapters retain their full headline in the body; the toolbar uses a short label. Flat second-level sections and existing cards are adapted by the shared engine. In One chapter view a card takes 88% of the stage, so neighbouring chapters stay visible at the edges. Do not duplicate the reader on individual pages.

The tree contains home, ordered groups/pages and the current page's chapters. Wide screens use a docked sidebar by default; narrow screens start closed and open it over content. Preserve the shared breakpoint behavior and remembered choices. Adjacent chapters and keyboard navigation remain discoverable; pinned columns remain fixed while the other navigates. Controls adapt to actual column width.

A reader-free home uses `reader = false`. The optional `<!-- site-map -->` marker derives one card per visible, grouped `[[nav]]` page: its nav label, its frontmatter `description` (else `brand_sub`) and its frontmatter `thumbnail` (else the first `<img>` or Markdown image in its body; inline SVG figures are not detected). Local SVG thumbnails are inlined like other local figures and hidden from assistive technology, since the card names the page; a thumbnail must be a local, tracked image. Projects may instead compose their own homepage. When the other pages use the chapter reader, give the home page `toc = []` so its sidebar shows the same site tree as every reader page instead of its own section list; moving between pages then keeps the navigation in place. Handwritten status summaries are dated and updated when their underlying state changes; they must not become another status owner.

Each column independently selects Math, Experiments, Code and Alternatives; Story stays visible. Preserve layer preferences, individual fold states and reading positions across revisits. Changing a layer preserves the visible anchor or its closed summary. A deep link opens its containing fold. History restores arrangements without undoing current reading preferences. Without JavaScript, content and native folds remain usable; print includes every layer; transitions respect reduced motion.

A chapter without typed folds hides empty layer controls. Subsection jumps remain beneath their containing chapter, reveal folded targets and highlight their exact location. They do not create extra chapters or reorder prerequisites. Preserve public anchors, tables, figures, media paths and manual folds during adaptation. Local comparison tabs keep their behavior.

An explicitly structured guide may use `data-reader-unit="section"` on its `data-reader-title` marker to change reader labels to Sections. Preserve behavior and accessibility labels consistently; do not fork the reader merely to rename a unit.

## Extending reading layers

Add a layer only for recurring content that Math, Experiments, Code and Alternatives cannot express. A new source marker requires a coordinated shared-kit change:

- Register its marker and balance validation in the builder.
- Register its human label, accepted saved preferences and column controls in the reader.
- Add reader and print styles, plus equivalent no-reader/fallback fold controls.
- Add checks for both columns, deep-link reveal, saved preferences, printing and fallback reading; inspect wide/narrow output.

Keep existing marker names and saved values stable. Human labels may differ from source markers (`dead-end` displays as Alternatives). Content placement follows the writing guide.

## Maintaining shared interactions

For independent option comparisons, select the shared `panel-switcher`
component and follow its [authoring contract](../docs/topics/panel-switcher/panel-switcher.md).
It owns local switching and generic controls; projects keep their comparison
content, data and specialized figure styling.

Load optional heavy components only on pages that use them. Recorded or linked viewers consume declared local data with stable identities and one shared selected state. Keep a poster while loading, confine gestures and keyboard handling to the component, and preserve no-JavaScript reading.

Version-specific renderer/color-space behavior, application viewers, recording protocols and domain datasets belong in the consuming project's component or topic records. Their availability must be checked against the pinned kit; do not promote application-specific or planned features into shared guarantees.
