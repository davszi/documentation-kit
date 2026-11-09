# Site tooling and authoring

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
tagged `v<version>`; [release notes](../../docs/topics/releases/releases.md) list each
version's changes and its migration steps. Upgrade the pin as a reviewed deliverable, run the shared and consumer checks, and record the adopted revision and compatibility evidence. Change the kit only in its own repository, following [the shared kit submodule](../engineering/git.md#the-shared-kit-submodule). Engine and shared-theme changes belong upstream; project content and optional extensions stay local.

From the consuming project root, use the pinned kit directly:

```bash
python -m pip install -r .docs-kit/requirements.txt
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py lint --project .
```

Use `--page <slug>` with build for targeted iteration. Lint supports `--strict` and `--registry`. The kit README owns installation and shared-engine development checks. The project's `docs/PROJECT_CONTEXT.md` records its tested environment and additional checks. Pin dependency versions; documentation builds must not require importing the consuming application's runtime or initializing a GPU.

## Authoring paths

Two kinds of page render: topic entry pages at `docs/topics/*/index.md` and [registered source pages](#registered-source-pages). Every new entry page needs frontmatter with `title` and `toc` (an empty list is valid with automatic chapters), plus a corresponding `[[nav]]` entry in `docs/site/site.toml`. The folder supplies its public slug; set `slug = "index"` on the home page. Slugs are lowercase filename stems without directories. Use `hidden = true` for a built, directly reachable page outside navigation, subject to the documentation deletion policy.

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
base. Do not introduce machine-specific absolute paths or remote media dependencies.
Fonts follow the [shared dependency rules](reader.md#shared-reading-layout).

An included fragment may include further fragments, up to eight levels; a cycle
fails the build. A `[[nav]]` table accepts only `label`, `file`, `group`, `short`
and `hidden`. TOML assigns every key written after a table header to that table,
so keep top-level settings such as `extra_components` above the first `[[nav]]`;
the build rejects any other key inside a nav entry.

`nested_nav = true` folds each navigation group into a native disclosure,
opens the current page's group (the first group on a page outside every
group) and places the current page's sections directly under its entry. It
applies to pages without the chapter reader, which nests chapters itself, and
keeps working without JavaScript. Groups a reader opens stay open on later
pages through browser storage, and open or close with a short transition that
respects reduced motion. The default is the flat site tree.

Register project-specific script components with `extra_components = ["viewer"]`;
each uses a tracked `docs/site/components/<name>.js`. For dynamically loaded
dependencies, `[extra_assets]` maps output names below `html/assets/` to tracked
project files, for example `"viewer/renderer.js" = "docs/site/assets/vendor/renderer.js"`.
List licenses/source notices alongside their dependencies. Paths must stay
inside the project, and project assets cannot overwrite shared kit assets.

The starter's reader-free home page selects shared `home.css` for its hero,
links and generated topic cards. That stylesheet and arrangement are optional;
projects may author their own homepage and local styles. Follow
[project-owned homepage composition](../writing/pages.md#project-owned-homepages).

Wrap a wide comparison table in `.scroll` with `role="region"`, a useful
`aria-label`, `tabindex="0"` and `data-reader-horizontal`. This keeps scrolling
and keyboard arrows inside the table instead of changing chapters. Pages with
`body_class = "reference-page"` get this region on every Markdown table
automatically.

### Registered source pages

A `[[source_pages]]` table renders an existing, tracked Markdown file as one
whole-file page without moving or copying it. Use it for records and guides
whose Markdown must stay the canonical source:

```toml
[[source_pages]]
source = "rules/engineering/git.md"  # contained, tracked .md file without +++ frontmatter
slug = "git"                         # public route: git.html
description = "Commits, shared checkouts and history."  # optional
pinned = true                        # optional: list first in the sidebar
```

`title` defaults to the file's first level-one heading. `description` supplies
the site-map card text and the sidebar tooltip. `math = true` enables formulas.
`reader = true` uses the chapter reader when the site enables it; otherwise the
page scrolls. In the
reader, a short opening (under 600 characters, without subheadings, figures or
tables) joins the first chapter with the source line instead of becoming a
nearly empty Introduction chapter; a longer opening stays its own chapter. One
slug belongs to one page. Topic entry pages keep their own frontmatter path and
cannot be registered.

Once a site registers a source page, every sidebar ends with a **Reference**
section that lists the registered files. There is no setting: a site
without source pages shows no section. `pinned = true` lists a file at the top
of the section by its title, always visible, in the order the tables are
declared. Below the pinned files, one **Browse by folder** disclosure holds every
registered file in a folder tree at its repository path, pinned files included.
Each file shows its name and title.

The disclosure starts closed on pages for people, on pinned pages and on
registered pages listed in the navigation, because their entry already marks
them. On any other registered page it starts open, with only the folders that
lead to that page unfolded. While closed, the section stays docked to the bottom
of the menu.

A registered file needs no `[[nav]]` entry, because the section lists it. Keep
`[[nav]]` for pages written for people, and for records every reader needs,
such as release notes and migration guides; such an entry lists the record
among those pages. A scrolling source page's sidebar shows the
site navigation and the repository section, not the page's own headings. With
`nested_nav = true`, a page that has a visible `[[nav]]` entry lists its
headings under that entry.

Links and media resolve from the file's own folder, exactly as when reading the
Markdown. A link to another registered file becomes that page's route. Other
repository files become source links, and tracked media are packaged. Absolute
paths, links that leave the project and missing targets fail the build. Every
fragment that points into a registered page, from any page, must match an
anchor of the rendered target. The page opens with its source path and an edit
link built from `gh_repo` and the configured `gh_ref`; `site-build.json` maps
each such route to its source file. Wide tables scroll inside
labelled regions. The page body carries the classes `source-page` and
`reference-page`; another scrolling page can opt into the same reading layout
with `body_class = "reference-page"`.

Topic-page markers are not interpreted in a registered file: includes, typed
folds, registry callouts and `<!-- page-end -->` stay literal, so a record can
show them as examples. Lint checks a registered file's Markdown links as an
ordinary record.

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
