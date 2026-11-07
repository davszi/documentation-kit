# Kit reference website

The kit publishes its own reference website with the same renderer, theme and
components that consumers use. Readers can learn the toolkit, read the shared
practices, inspect releases and follow migration guides in rendered HTML.
Every detailed guide keeps one editable Markdown source.

## Structure and sources

The site follows the kit's own split between records and pages. Guides in
`rules/`, the README, release notes and the kit's records are **records**: agents
read them as Markdown, and the site renders each whole from its canonical file
through a `[[source_pages]]` entry as a plain reference page with a source line.
**Pages for people** are hand-written topic pages in the chapter reader that
explain those records and link into them. A record is never rewritten for the
reader; when a page and its record disagree, the record wins and the page is
corrected.

[`docs/site/site.toml`](../../site/site.toml) is the registry: `[[nav]]`
tables give the navigation and `[[source_pages]]` tables map records to routes.

| Page for people | Source | Explains |
|---|---|---|
| Home | [`home/index.md`](../home/index.md) | Three paths, the three adoption steps and a router snippet |
| Get started | [`getting-started/index.md`](../getting-started/index.md) | What the kit provides, setup steps, site and upgrades, adoption routes |
| Setup and commands | [`commands/index.md`](../commands/index.md) | Setup, build, lint, preview, slides and upgrade commands, with what each checks or writes |
| Reader tour | [`reader-tour/index.md`](../reader-tour/index.md) | Chapters, docking, pinning, layers, figures, comparisons, status blocks and slides |
| Practices overview | [`project-practices/index.md`](../project-practices/index.md) | Task routing, the three practice areas and project specifics |
| Engineering | [`engineering-practices/index.md`](../engineering-practices/index.md) | The six engineering guides |
| Documentation and writing | [`writing-practices/index.md`](../writing-practices/index.md) | The documentation system and the writing guides |
| Experiments | [`experiments/index.md`](../experiments/index.md) | The experiment workflow and verification guides |
| Site toolkit | [`site-toolkit/index.md`](../site-toolkit/index.md) | Build pipeline, task-to-guide map, source pages and build checks |

Rule guides are hidden from the navigation and reached from these pages; release
notes, migration guides, the README and the kit-development records stay listed. The
writing and maintenance routers remain hidden pages so existing links to their
section anchors keep working.

The site sets `chapter_reader = true`; records keep the registry default
`reader = false`. Topic pages use only the shared `home.css` and
`build-sheet.css` blocks, with no site-local stylesheet. The home page is
reader-free, with `toc = []`.

## Build and preview

Build from the kit root with `python docsite.py build --project .`; the output
is `.build/docs/`. [Project context](../../KIT_CONTEXT.md) lists the full
check sequence, which builds and lints this site beside the starter.

## Open decision: hosting and audience

The website has been built and reviewed locally only. Before any deployment,
deivid chooses the hosting destination and whether the audience is public or
private. The repository is private and GitHub Pages is disabled as of
2026-11-07. Source and edit links point to `gh_repo` and therefore work only for
readers with repository access.
