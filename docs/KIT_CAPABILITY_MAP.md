# Capability map

This map lists what the kit's own tooling does, one need per row, so that a
need is solved once and found again. Read it before building tooling.
[Name the need first](../rules/engineering/code.md#name-the-need-first) says
how to use it, and [capability map settings](../rules/site/authoring.md#capability-map-settings)
give its format and its lint check, which `tooling_roots = ["tooling/"]` in
`docs/site/site.toml` applies to the kit.

The Need, Code and State columns are written by hand. The Imported by column
is generated from Python imports; never edit it. After adding a row or
changing an import, run `python docsite.py capability-map --project .`, and
lint fails while the column is out of date. It does not show code that is
loaded by file path or run as a command: `tooling/lint.py` loads
`tooling/site_paths.py` by path and runs
`tooling/build.py`, and `docsite.py` runs `build.py`, `lint.py`, `slides.py`
and `capability_map.py`. Node scripts under `tests/` load
`tooling/browser_checks.cjs`, and `tooling/formula_checks.py` runs
`tooling/formula_compile.cjs` with Node.

## Capabilities

| Need | Code | State | Imported by |
|---|---|---|---|
| Run the kit's commands from a project without copying the kit into it | [docsite.py](../docsite.py) | exists | no Python imports |
| Render topic pages and Markdown records into a static site, and check that the generated site is fresh | [build.py](../tooling/build.py), [site_bundle.py](../tooling/site_bundle.py) | exists | `tests/test_asset_versions.py`, `tests/test_brand_mark.py`, `tests/test_chapter_layout.py`, `tests/test_listed_html.py`, `tests/test_math_rendering.py`, `tests/test_slide_faces.py` |
| Find a project's documentation paths wherever the kit is installed, and map the logical `docs/html/` origin to the build output | [site_paths.py](../tooling/site_paths.py) | exists | `tests/test_portability.py`, `tooling/build.py`, `tooling/site_bundle.py`, `tooling/slides.py` |
| Load a project's own tracked Python module that its site settings name, the content transform | [project_extensions.py](../tooling/project_extensions.py) | exists | `tooling/build.py` |
| Fit the sections of an existing page into the chapter reader without editing its source | [chapter_layout.py](../tooling/chapter_layout.py) | exists | `tests/test_chapter_layout.py`, `tests/test_slide_faces.py`, `tooling/build.py`, `tooling/page_lock.py`, `tooling/publication.py`, `tooling/reader_content.py`, `tooling/slide_face_checks.py`, `tooling/slides.py` |
| Show that the chapter reader keeps every word, link and figure of a page | [reader_content.py](../tooling/reader_content.py) | exists | `tests/test_chapter_layout.py`, `tooling/build.py` |
| Render a whole repository Markdown file as a page, and list such files in a folder tree | [source_pages.py](../tooling/source_pages.py), [source_tree.py](../tooling/source_tree.py) | exists | `tests/test_listed_html.py`, `tests/test_page_lock.py`, `tests/test_reference_listing.py`, `tests/test_source_tree.py`, `tooling/build.py`, `tooling/page_lock.py` |
| Pair each topic page with the record it explains, and name the source file of each built page | [topic_structure.py](../tooling/topic_structure.py) | exists | `tests/test_record_notes.py`, `tooling/build.py`, `tooling/lint.py`, `tooling/record_changes.py`, `tooling/site_paths.py`, `tooling/slide_face_checks.py`, `tooling/source_pages.py` |
| Find the chronology file, date its entries and decide which entries keep checked links | [worklog_entries.py](../tooling/worklog_entries.py) | exists | `tooling/build.py`, `tooling/lint.py`, `tooling/source_pages.py` |
| Find the fenced code blocks of Markdown source, so that a check or a conversion can leave code alone | [worklog_entries.py](../tooling/worklog_entries.py) | exists | `tooling/build.py`, `tooling/lint.py`, `tooling/source_pages.py` |
| Check links, HTML links to repository files included, anchors, snippets, figures, markers and record formats before a push | [lint.py](../tooling/lint.py) | exists | `tests/test_capability_map.py`, `tests/test_lint.py`, `tests/test_page_numbers.py`, `tests/test_record_notes.py` |
| List the pages that explain a record section that changed | [record_changes.py](../tooling/record_changes.py) | exists | `tests/test_record_notes.py`, `tooling/lint.py`, `tooling/page_numbers.py` |
| List numbers on a page that none of its linked records state | [page_numbers.py](../tooling/page_numbers.py) | exists | `tests/test_page_numbers.py`, `tooling/lint.py` |
| Detect a kit pin that nobody else can fetch | [kit_pin.py](../tooling/kit_pin.py) | exists | `tests/test_kit_pin.py`, `tooling/lint.py` |
| Check that a project's tooling is listed in its capability map, and find who imports each part | [capability_map.py](../tooling/capability_map.py) | exists | `tests/test_capability_map.py`, `tooling/build.py`, `tooling/lint.py` |
| Export a public bundle of the site into a publication tree | [publication.py](../tooling/publication.py) | exists | `docsite.py`, `tests/test_page_lock.py`, `tests/test_publication.py`, `tests/test_publish_project.py` |
| Store the text of a published bundle encrypted behind passwords | [page_lock.py](../tooling/page_lock.py) | exists | `tests/page_lock_fixture.py`, `tests/test_page_lock.py`, `tooling/project_check.py`, `tooling/publication.py` |
| Extract chapter slide faces from built pages into one deck | [slides.py](../tooling/slides.py) | exists | `tests/test_slide_faces.py`, `tooling/slide_face_checks.py` |
| Check in the built pages that each chapter opens with at most one slide face and that every number a face shows also appears in its chapter, with no list from the project | [slide_face_checks.py](../tooling/slide_face_checks.py) | exists | `tests/test_slide_face_checks.py`, `tooling/lint.py` |
| Check that every formula on a project's built pages compiles with the KaTeX the kit ships, and that none is split by Markdown or left unclosed | [formula_checks.py](../tooling/formula_checks.py), [formula_compile.cjs](../tooling/formula_compile.cjs) | exists | `tests/test_formula_checks.py`, `tooling/lint.py` |
| Run a project's build, strict lint, trial publish and declared checks in order, stopping at the first failure, for the pre-push hook `hooks/pre-push` | [project_check.py](../tooling/project_check.py) | exists | `docsite.py`, `tests/test_project_check.py` |
| Give a figure generator one dark and one light colour palette, matplotlib settings for either, and both figure files under fixed names | [figure_themes.py](../tooling/figure_themes.py) | exists | `tests/test_figure_themes.py`, `tooling/lint.py`, `tooling/svg_figures.py` |
| Write inline SVG figures from a project's figure generator | [svg_figures.py](../tooling/svg_figures.py) | exists | `docs/topics/approval-failed-open/draw_figures.py`, `tests/test_figure_themes.py`, `tests/test_figure_tooling.py` |
| Check rendered pages in a real browser: layout, overflow, visible media, and slide faces in their page or deck, stacked below 720 px included | [browser_checks.cjs](../tooling/browser_checks.cjs) | exists | not scanned: no Python code |

## Seen but not built

Each entry is a need that was noticed and not built, with the decision. An
entry without a decision says where the question waits. Seen 2026-11-15 in
adaptation's report on its slide faces; decided 2026-11-15 by the kit's
maintaining session, not by deivid, which deivid allowed with "you can
settle them but with evaling if its worth even adding cuz we're bloating the
docs":

- Warn when the picture of a home-page card changes because a page's first
  image changed. Decision: not built; the review by eye covers it.
- Put a chapter's figure on its slide face without a second copy of the
  figure: a project wrote a second fragment through `slide_svg`. Decision:
  not built; a face may redraw the chapter's figure.
- Let a project's own slide classes win over the shared canvas rules without
  `!important` on every declaration. Decision: not built; the rule keeps
  `!important`.
