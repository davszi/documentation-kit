# Capability map

This map lists what the kit's own tooling does, one need per row, so that a
need is solved once and found again. Read it before building tooling.
[Name the need first](../rules/engineering/code.md#name-the-need-first) says
how to use it, and [the capability map](../rules/engineering/code.md#the-capability-map)
owns its format and its lint check. `tooling_roots = ["tooling/"]` in
`docs/site/site.toml` turns the check on for the kit.

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
| Render topic pages and Markdown records into a static site, and check that the generated site is fresh | [build.py](../tooling/build.py), [site_bundle.py](../tooling/site_bundle.py) | exists | `tests/test_asset_versions.py`, `tests/test_brand_mark.py`, `tests/test_chapter_layout.py`, `tests/test_math_rendering.py`, `tests/test_slide_faces.py` |
| Find a project's documentation paths wherever the kit is installed, and map the logical `docs/html/` origin to the build output | [site_paths.py](../tooling/site_paths.py) | exists | `tests/test_portability.py`, `tooling/build.py`, `tooling/site_bundle.py`, `tooling/slides.py` |
| Load a project's own tracked Python module that its site settings name, the content transform | [project_extensions.py](../tooling/project_extensions.py) | exists | `tooling/build.py` |
| Fit the sections of an existing page into the chapter reader without editing its source | [chapter_layout.py](../tooling/chapter_layout.py) | exists | `tests/test_chapter_layout.py`, `tests/test_slide_faces.py`, `tooling/build.py`, `tooling/page_lock.py`, `tooling/publication.py`, `tooling/reader_content.py`, `tooling/slide_face_checks.py`, `tooling/slides.py` |
| Show that the chapter reader keeps every word, link and figure of a page | [reader_content.py](../tooling/reader_content.py) | exists | `tests/test_chapter_layout.py`, `tooling/build.py` |
| Render a whole repository Markdown file as a page, and list such files in a folder tree | [source_pages.py](../tooling/source_pages.py), [source_tree.py](../tooling/source_tree.py) | exists | `tests/test_page_lock.py`, `tests/test_reference_listing.py`, `tests/test_source_tree.py`, `tooling/build.py`, `tooling/page_lock.py` |
| Pair each topic page with the record it explains, and name the source file of each built page | [topic_structure.py](../tooling/topic_structure.py) | exists | `tests/test_record_notes.py`, `tooling/build.py`, `tooling/lint.py`, `tooling/record_changes.py`, `tooling/site_paths.py`, `tooling/slide_face_checks.py`, `tooling/source_pages.py` |
| Find the chronology file, date its entries and decide which entries keep checked links | [worklog_entries.py](../tooling/worklog_entries.py) | exists | `tooling/build.py`, `tooling/lint.py`, `tooling/source_pages.py` |
| Find the fenced code blocks of Markdown source, so that a check or a conversion can leave code alone | [worklog_entries.py](../tooling/worklog_entries.py) | exists | `tooling/build.py`, `tooling/lint.py`, `tooling/source_pages.py` |
| Check links, HTML links to repository files included, anchors, snippets, figures, markers and record formats before a push | [lint.py](../tooling/lint.py) | exists | `tests/test_capability_map.py`, `tests/test_lint.py`, `tests/test_page_numbers.py`, `tests/test_record_notes.py` |
| List the pages that explain a record section that changed | [record_changes.py](../tooling/record_changes.py) | exists | `tests/test_record_notes.py`, `tooling/lint.py`, `tooling/page_numbers.py` |
| List numbers on a page that none of its linked records state | [page_numbers.py](../tooling/page_numbers.py) | exists | `tests/test_page_numbers.py`, `tooling/lint.py` |
| Detect a kit pin that nobody else can fetch | [kit_pin.py](../tooling/kit_pin.py) | exists | `tests/test_kit_pin.py`, `tooling/lint.py` |
| Check that a project's tooling is listed in its capability map, and find who imports each part | [capability_map.py](../tooling/capability_map.py) | exists | `tests/test_capability_map.py`, `tooling/build.py`, `tooling/lint.py` |
| Export a public bundle of the site into a publication tree | [publication.py](../tooling/publication.py) | exists | `docsite.py`, `tests/test_page_lock.py`, `tests/test_publication.py`, `tests/test_publish_project.py` |
| Store the text of a published bundle encrypted behind passwords | [page_lock.py](../tooling/page_lock.py) | exists | `tests/page_lock_fixture.py`, `tests/test_page_lock.py`, `tooling/publication.py` |
| Extract chapter slide faces from built pages into one deck | [slides.py](../tooling/slides.py) | exists | `tests/test_slide_faces.py`, `tooling/slide_face_checks.py` |
| Check in the built pages that each chapter opens with at most one slide face and that every number a face shows also appears in its chapter, with no list from the project | [slide_face_checks.py](../tooling/slide_face_checks.py) | exists | `tests/test_slide_face_checks.py`, `tooling/lint.py` |
| Check that every formula on a project's built pages compiles with the KaTeX the kit ships, and that none is split by Markdown or left unclosed | [formula_checks.py](../tooling/formula_checks.py), [formula_compile.cjs](../tooling/formula_compile.cjs) | exists | `tests/test_formula_checks.py`, `tooling/lint.py` |
| Write inline SVG figures from a project's figure generator | [svg_figures.py](../tooling/svg_figures.py) | exists | `docs/topics/approval-failed-open/draw_figures.py`, `tests/test_figure_tooling.py` |
| Check rendered pages in a real browser: layout, overflow, visible media, and slide faces in their page or deck, stacked below 720 px included | [browser_checks.cjs](../tooling/browser_checks.cjs) | exists | not scanned: no Python code |

## Seen but not built

Each entry is a need that was noticed and not built, with the person's
decision. An entry without a decision says where the question waits.

- Check that every fact on a slide face appears in its chapter. Seen
  2026-11-15: a consuming project wrote its own test that compares the numbers
  on a face with its chapter, in
  [the slide-face findings](open/upgrade-to-4.0.0-findings.md#tooling-a-project-had-to-build-itself-for-slide-faces).
  Decision 2026-11-15 by deivid: build it in the kit before the 5.0.0
  release; asked "Before or after?", he answered "before". Built for numbers,
  as a lint warning in `slide_face_checks.py`; claims and other words are not
  checked.
- Check that a page has at most one slide face per chapter, and check faces
  below 720 px. Seen 2026-11-15 in the same report. Decision 2026-11-15 by
  deivid: build both in the kit before the 5.0.0 release, as above. Built as a
  lint error in `slide_face_checks.py` and as the stacked-face measurements of
  `slideFaces` in `browser_checks.cjs`.
- Warn when the picture of a home-page card changes because a page's first
  image changed. Seen 2026-11-15 in the same report. Decision: not taken; the
  question waits in [the findings record](open/upgrade-to-4.0.0-findings.md#questions-for-deivid).
- Put a chapter's figure on its slide face without a second copy of the
  figure. Seen 2026-11-15 in the same report: a project wrote a second
  fragment through `slide_svg`. Decision: not taken; the question waits in the
  same record.
- Let a project's own slide classes win over the shared canvas rules without
  `!important` on every declaration. Seen 2026-11-15 in the same report.
  Decision: not taken; the question waits in the same record.
- Check that a link written as HTML to a repository file resolves. Seen
  2026-11-09 and 2026-11-10. Decision 2026-11-15 by deivid: add it to 5.0.0;
  his word: "add it". Built as a lint error in `lint.py`, which reads the
  source links the build marks in the built pages; the row "Check links, HTML
  links to repository files included, …" covers it.
- Check that every formula on a project's built pages compiles. Seen
  2026-11-15: a consuming project, ADP, keeps its own test that compiles every
  formula of its built pages with the kit's KaTeX and fails on one that does
  not compile or that Markdown split. Decision 2026-11-15 by deivid: "lets
  move it to kit". Built as a lint error in `formula_checks.py`, which finds
  the formulas in Python and compiles them in Node with
  `formula_compile.cjs`; without Node it is a note, or an error when the
  project sets `formula_check_required = true`.
