# Shared reader and interactions

## Shared reading layout

Keep fonts and browser/math dependencies vendored with licenses and source/version notices. The shared build-sheet theme uses its bundled font families; pages load no external fonts. Local page CSS adds only page-specific needs.

`chapter_reader = true` in site configuration enables the common reader. Reuse its header, tree navigation, One chapter / Two chapters / All chapters arrangements, pinning, positions and layer choices. Chapters retain their full headline in the body; the toolbar uses a short label. Flat second-level sections and existing cards are adapted by the shared engine. In One chapter view a card takes 88% of the stage, so neighbouring chapters stay visible at the edges. Do not duplicate the reader on individual pages.

The tree contains home, ordered groups/pages and the current page's chapters, followed by the [repository tree](authoring.md#registered-source-pages) when the site registers source pages. Wide screens use a docked sidebar by default; narrow screens start closed and open it over content. Preserve the shared breakpoint behavior and remembered choices. Adjacent chapters and keyboard navigation remain discoverable; pinned columns remain fixed while the other navigates. Controls adapt to actual column width.

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
component and follow its [authoring contract](../../docs/topics/panel-switcher/panel-switcher.md).
It owns local switching and generic controls; projects keep their comparison
content, data and specialized figure styling.

Load optional heavy components only on pages that use them. Recorded or linked viewers declare their local data and follow the [interaction and access rules](../writing/figures.md#interaction-and-access). Preserve their no-JavaScript reading.

Version-specific renderer/color-space behavior, application viewers, recording protocols and domain datasets belong in the consuming project's component or topic records. Their availability must be checked against the pinned kit; do not promote application-specific or planned features into shared guarantees.
