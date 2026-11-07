# Kit reference website

The kit publishes its own reference website with the same renderer, theme and
components that consumers use. Readers can learn the toolkit, read the shared
practices, inspect releases and follow migration guides in rendered HTML.
Every detailed guide keeps one editable Markdown source.

## Structure and sources

[`docs/site/site.toml`](../../site/site.toml) is the registry: its `[[nav]]`
tables give the navigation and its `[[source_pages]]` tables map canonical
Markdown files to routes. Four topic pages add orientation only:

| Page | Source | Role |
|---|---|---|
| Home | [`home/index.md`](../home/index.md) | Three paths, the three adoption steps and a router snippet |
| Get started | [`getting-started/index.md`](../getting-started/index.md) | Reader chapters: what the kit provides, setup steps, site and upgrades, adoption routes |
| Site toolkit | [`site-toolkit/index.md`](../site-toolkit/index.md) | Reader chapters: build pipeline, task-to-guide map, source pages, build checks |
| Project practices | [`project-practices/index.md`](../project-practices/index.md) | Reader chapters: task routing and one guide table per area |

Everything else renders whole from its canonical file: `README.md`, the guides
in `rules/`, the release notes and migration guides, the panel-switcher
contract and the kit's own context, index and extraction records.

Material is grouped by purpose, not by folder. For example,
`rules/site/authoring.md` explains toolkit operation and sits under Site
toolkit although it lives in `rules/`. The writing and maintenance routers are
built as hidden pages so existing links to their section anchors keep working.
Overview pages link to commands and contracts instead of restating them.

The site uses the kit's own presentation: `chapter_reader = true`, every
registered page sets `reader = true`, and the topic pages are Markdown with the
shared `home.css` and `build-sheet.css` blocks and no site-local stylesheet.
Only the home page is reader-free, with `toc = []` so its sidebar shows the
same tree as the reader pages.

## Build and preview

Build from the kit root with `python docsite.py build --project .`; the output
is `.build/docs/`. [Project context](../../PROJECT_CONTEXT.md) lists the full
check sequence, which builds and lints this site beside the starter.

## Open decision: hosting and audience

The website has been built and reviewed locally only. Before any deployment,
deivid chooses the hosting destination and whether the audience is public or
private. The repository is private and GitHub Pages is disabled as of
2026-11-07. Source and edit links point to `gh_repo` and therefore work only for
readers with repository access.
