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

Initialize the submodule before building. Upgrade the pin as a reviewed deliverable, run the shared and consumer checks, and record the adopted revision and compatibility evidence. Do not edit a detached submodule as a substitute for a shared-kit change. Engine and shared-theme changes belong upstream; project content and optional extensions stay local.

From the consuming project root, use the pinned kit directly:

```bash
python -m pip install -r .docs-kit/requirements.txt
python .docs-kit/docsite.py build --project .
python .docs-kit/docsite.py build --project . --check
python .docs-kit/docsite.py lint --project .
```

Use `--page <slug>` with build for targeted iteration. Lint supports `--strict` and `--registry`. The kit README owns installation and shared-engine development checks. The project's `docs/PROJECT_CONTEXT.md` records its tested environment and additional checks. Pin dependency versions; documentation builds must not require importing the consuming application's runtime or initializing a GPU.

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
base. Do not introduce machine-specific absolute paths or remote media dependencies.
Fonts follow the [shared dependency rules](reader.md#shared-reading-layout).

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
and keyboard arrows inside the table instead of changing chapters.
