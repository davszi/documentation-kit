# Shared reader and interactions

## Shared reading layout

Keep fonts and browser/math dependencies vendored with licenses and source/version notices. The shared build-sheet theme uses its bundled font families; pages load no external fonts. Local page CSS adds only page-specific needs.

`chapter_reader = true` in site configuration enables the common reader. Reuse its tree navigation, One chapter / Two chapters / All chapters / Presentation arrangements, pinning, positions and section options. Chapters retain their full headline in the body; the chapter list of the sidebar uses a short label. Flat second-level sections and existing cards are adapted by the shared engine. In One chapter view a card takes 89.8% of the stage, so neighbouring chapters stay visible at the edges, at full size. A click on the visible strip of a neighbour, or a sideways swipe, turns the chapter. In that view the chapter shows no strip with its number and name; its headline starts the full chapter. A chapter without a headline of its own keeps the strip. Do not duplicate the reader on individual pages.

While the sidebar is docked the reader has no top bar. One row of icons under the site name holds the arrangements, Presentation, About and Help. A stepper floats at the bottom centre of the chapter: previous, the position, next. While a chapter is at its top, its Full chapter row sits on the stepper's line, the label and reading time at the left and Continue reading at the right; the row leaves when the chapter is scrolled. A chapter that opens with a slide face shows the face alone in that first view: the face stands in the middle of the room above the row, and the headline starts the full chapter below the fold. When the sidebar is not docked, a bar with the menu button and the page name stays, and the same controls are in the drawer. In a window up to 900 px wide, Continue reading is a round arrow button beside the stepper.

A page with at least one [slide face](authoring.md#slide-faces-and-decks) also offers Presentation, a fourth view. It fills the window with the current chapter's slide, kept at 16:9 and letterboxed, and hides the navigation and the reader's controls; it opens at the current chapter. A thin overlay shows the chapter position and has previous, next, restart, fullscreen and close controls; it fades when idle and returns on pointer movement or a key press. Left and right arrows, Page Up and Page Down and the overlay arrows change chapter and always land on the slide; Home and End go to the first and last chapter. Scrolling, Up, Down and Space move only within the chapter: the full chapter follows its slide, and a small scroll near the top snaps back to the slide. At 720 px and wider, a chapter without a face shows a title card built at run time from its headline and its `bs-lead` sentence; the card is not a slide face and is not in the built page. Narrower, such a chapter shows no card and starts at its heading. When a chapter holds several faces, the first is its slide and the rest stay in the chapter. F and the fullscreen control use the browser's fullscreen; Escape leaves the view when the browser is not fullscreen, and focus returns to the control that started it, or to the chapter when that control sits in a drawer that has closed. The address carries `?view=present` with the chapter, so a reload or a shared link reopens the same slide. Below 720 px the slide stacks above the chapter as in the other views. Keys typed into controls inside a chapter keep their own meaning. Pages without a slide face show no Presentation control.

All chapters reads as one document: it hides slide faces and their bridges until the Slides switch shows them, which sits under Also show in the sidebar in that arrangement. The choice is remembered per page, beside the section options, and printing from All chapters follows it. One chapter, Two chapters and Presentation always show the faces.

The tree contains home, ordered groups/pages and the current page's chapters, followed by the [repository files section](authoring.md#registered-source-pages) when the site has source pages, registered or [listed automatically](authoring.md#automatic-reference-listing). Screens wider than 900 px use a docked sidebar by default; narrower screens start closed and open it over content. Preserve the shared breakpoint behavior and remembered choices. Adjacent chapters and keyboard navigation remain discoverable; pinned columns remain fixed while the other navigates. Controls adapt to actual column width.

The home page has the reader off: it sets `reader = false`. The reader's frame is for the chapters of a topic page; the home page is the project's own composition. The optional `<!-- site-map -->` marker derives one card per visible, grouped `[[nav]]` page: its nav label, its frontmatter `description` (else `brand_sub`) and its frontmatter `thumbnail` (else the first `<img>` or Markdown image in its body; inline SVG figures are not detected). Local SVG thumbnails are inlined like other local figures and hidden from assistive technology, since the card names the page; a thumbnail must be a local, tracked image. Projects may instead compose their own homepage. When the other pages use the chapter reader, give the home page `toc = []` so its sidebar shows the same site tree as every reader page instead of its own section list; moving between pages then keeps the navigation in place. Handwritten status summaries are dated and updated when their underlying state changes; they must not become another status owner.

One set of section options serves the whole page, under Also show at the bottom of the sidebar. Each option opens every fold of one kind in every chapter and in both columns: Math, Experiments, Code and Not chosen, of which a page offers only the kinds it has. A fold of no kind (`fold: detail`) has no option of its own. All is a switch for every fold, folds of no kind included; a page whose only folds have no kind offers All alone. With nothing switched on, the Story stays visible. A fold starts closed, or open where its author marked it. A reader's own click on a fold is saved for that fold and wins on the next visit, until an option sets its kind again. Preserve the options, individual fold states and reading positions across revisits. Changing an option preserves the visible anchor or its closed summary. A deep link opens its containing fold. History restores arrangements without undoing current reading preferences. Without JavaScript, content and native folds remain usable; print includes every layer; transitions respect reduced motion.

A page without folds shows no options. Subsection jumps remain beneath their containing chapter, reveal folded targets and highlight their exact location. They do not create extra chapters or reorder prerequisites. Preserve public anchors, tables, figures, media paths and manual folds during adaptation. Local comparison tabs keep their behavior.

An explicitly structured guide may use `data-reader-unit="section"` on its `data-reader-title` marker to change reader labels to Sections. Preserve behavior and accessibility labels consistently; do not fork the reader merely to rename a unit.

## Extending reading layers

Add a layer only for recurring content that Math, Experiments, Code and Not chosen cannot express and that needs an option of its own; other optional detail is a fold of no kind. A new source marker requires a coordinated shared-kit change:

- Register its marker and balance validation in the builder.
- Register its human label, accepted saved preferences and its option in the reader.
- Add reader and print styles, plus equivalent no-reader/fallback fold controls.
- Add checks for both columns, deep-link reveal, saved preferences, printing and fallback reading; inspect wide/narrow output.

Keep existing marker names and saved values stable. Human labels may differ from source markers (`dead-end` displays as Not chosen). Content placement follows the writing guide.

## Maintaining shared interactions

For independent option comparisons, select the shared `panel-switcher`
component and follow its [authoring contract](../../docs/topics/panel-switcher/panel-switcher.md).
It owns local switching and generic controls; projects keep their comparison
content, data and specialized figure styling.

Load optional heavy components only on pages that use them. Recorded or linked viewers declare their local data and follow the [interaction and access rules](../writing/figures.md#interaction-and-access). Preserve their no-JavaScript reading.

Version-specific renderer/color-space behavior, application viewers, recording protocols and domain datasets belong in the consuming project's component or topic records. Their availability must be checked against the pinned kit; do not promote application-specific or planned features into shared guarantees.
