# Releases and upgrades

The kit's version is in [`VERSION`](../../../VERSION); each release is tagged `v<version>`.
A consuming project pins an exact commit or tag and upgrades deliberately, following
[Pin and upgrade](../../../README.md#pin-and-upgrade). This record lists what each
release changes for consumers and how to move to it. Chronology stays in the
[worklog](../../KIT_WORKLOG.md); consumer adoption status stays in each consuming project.

## What a version number promises

The [stable and provisional interfaces](#100--first-stable-version) list what a
project may rely on. From 3.0.0 the version number means this:

- A **major** release removes or renames a stable interface, including a
  section anchor under `rules/`, or adds a lint error or build failure that
  stops a project that passed before. A major release also changes a default
  so that a site publishes content it did not publish before.
- A **minor** release adds to the stable interfaces. It may also add lint
  warnings, which fail `--strict`, change how the shared theme looks, and change
  or remove a provisional interface.
- A **patch** release corrects a defect or relaxes a check. A project that
  passed before still passes, and it needs no migration step.

The release notes list every such change, and the version's migration guide
gives the step for each. A minor upgrade can therefore need work: the
[project conformance check](../../../rules/conformance.md) runs strict lint and
shows the new warnings.

## 5.0.0 — Reference section by default, page lock and Presentation view

5.0.0 is a major release under
[what a version number promises](#what-a-version-number-promises) for six
reasons:

- **A default now publishes more.** Every tracked Markdown file of a project
  becomes a page of its site and is listed in the sidebar's Reference section,
  unless one of the exceptions in
  [automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing)
  keeps it out. **A private repository with a public site publishes these
  files at its next publish, unless it excludes them or turns the listing
  off.** The first step of the [5.0.0 migration guide](migrations/5.0.0.md)
  settles the list before the moved pin reaches a branch that publishes.
- **`publish` refuses a private source page.** `publish` now fails when a
  `[[source_pages]]` table registers a file that the project's own
  `[publication]` `private_prefixes` or `private_suffixes` cover. Up to 4.0.0
  such a page was published. A project in that case passed before and fails
  now.
- **A new lint error for slide faces.** `docsite.py lint` now fails on a
  chapter with more than one slide face, on a face that does not open its
  chapter and on a face outside every chapter. Up to 4.0.0 such a page built
  and linted clean. A project in that case passed before and fails now.
- **The path and evidence adapter hooks and the kept-copy settings are removed.** The kit no longer loads
  a project module named by `path_resolver` or `evidence_validator`, nor the
  evidence adapter's `document_origin`. A `site.toml` that still names one of
  the two settings fails the build, and the links that only the adapter
  resolved fail lint. deivid decided it, asked which of three options: "remove
  all 3". The hooks let a project keep old documents as unedited copies in its
  live tree, which the rule on
  [finished working documents](../../../rules/records.md#finished-working-documents)
  ended in 4.0.0. At this release adaptation still names both settings; ADP
  and Tempo name none. Two settings of the kit's own that served the same
  practice go with them: `evidence_manifests`, which declared collections of
  copies that had to stay byte for byte, and `legacy_files`, which mapped
  single old paths to current files. A `site.toml` that names either fails the
  build the same way. deivid decided it: "Yes, remove both". No known project
  sets either.
- **A new lint error for HTML links to repository files.** Lint now checks a
  link written as `<a href="…">` that points at a repository file, in a topic
  page, a fragment it includes or a registered source page: the target must
  exist, and a fragment into a Markdown file must match an anchor. Up to 4.0.0
  only Markdown links were checked, so a dead HTML link passed strict lint. A
  project in that case passed before and fails now. deivid decided it: "add
  it". Measured on 2026-11-15 with this check: ADP's 129 such links, read from
  its last build output, all resolve;
  adaptation at `e28472e` has 78, of which 42 fail once its path adapter is
  gone, 41 because they name paths only the adapter mapped and one because
  its target exists nowhere.
- **A new lint error for formulas.** Lint now compiles every formula on the
  built pages with the KaTeX the kit ships, whenever it finds Node.js, and
  fails on a formula that does not compile, on one that Markdown split and on
  an opening delimiter that does not close. Up to 4.0.0 such a formula showed
  as raw text on the page and lint passed. A project in that case passed
  before and fails now. deivid decided to move ADP's own formula test into the
  kit: "lets move it to kit".

Apart from the two adapter settings and the two kept-copy settings, no
command, flag, configuration key or marker is removed.
No section anchor under `rules/` is removed or renamed: every heading of every
file under `rules/` at `v4.0.0` is still present.
`rules/site/authoring.md` gains the sections "Automatic reference listing" and
"Capability map settings", and `rules/site/publication.md` gains "Page lock"
with five subsections. `rules/engineering/code.md` gains "Name the need first"
and "The capability map" with its subsection "The check";
`rules/experiments/workflow.md` gains "Show the total" and "Step back across
experiments". Apart from the slide-face checks, a removed adapter or kept-copy setting,
a dead HTML link to a repository file and a formula that does not compile, a
project that does not set
`tooling_roots` gets no new lint warning or error; a problem in an
automatically listed file is a lint note, which never fails. The slide-face
checks apply to every project with slide faces: the error above, and a
warning, which fails `lint --strict`, for a number that a face shows and its
chapter does not. The capability map check adds lint errors and one warning
only for a project that opts in.

The new top-level `site.toml` settings `reference_listing`,
`reference_exclude` and `formula_check_required` and the `[publication]` key
`lock` join the stable interfaces as configuration keys. `site.toml` has no check for unknown
top-level keys, so a project that already used `reference_listing` or
`reference_exclude` for its own value now fails the build when that value is
not valid for the new setting.

What is provisional:

- **The version number.** The kit owner recommends 5.0.0 because of the
  changed default. deivid has not confirmed the number; the
  [open record](../../open/release-5.0.0-waits.md) keeps the question. Without
  the publication default, the publish refusal and the slide-face lint error
  above still make the release major under the promise as written.
- **The page lock's rule text.** Details of the
  [page lock](../../../rules/site/publication.md#page-lock) are still being
  finished. This record names its settings; the rule section owns how it
  works and what it does not protect.
- **The capability map's format and check.** The settings `tooling_roots`,
  `capability_map` and `experiment_roots`, the command
  `docsite.py capability-map`, the table's columns and the wording of the
  generated column were tried on the kit's own tooling only. They may change
  in a minor release.
- **What the slide-face number check reads.** Which numbers count as one and
  which are not counted were tried on the faces of the kit's own site, the
  starter and one consuming project. They may change in a minor release; the
  check's level, a warning, and the `data-face-only` mark do not.
- **New generated files and component internals.** `reference.tree.js`,
  `reference.index.html`, the `reference_tree` key of `site-build.json`, the
  components `page-lock.js` and `page-lock.css`, and the reader's new controls
  and classes are build output or theme internals. None is in the
  [stable list](#100--first-stable-version).

Known open points are in the [open record](../../open/release-5.0.0-waits.md).

| Area | Consumer change | Owning contract |
|---|---|---|
| Configuration | Changed default: every tracked Markdown file is a source page with its own public address, listed in the Reference section. Not listed: files inside a Git submodule, the kit's `.docs-kit/` included; files whose path has a folder or file name starting with a dot; files that start with `+++` frontmatter, and topic entry pages; symbolic links and files below one; files that match `reference_exclude`; files that the `[publication]` private prefixes or suffixes cover. A file with `---` YAML frontmatter is listed and shows the frontmatter as text. A `[[source_pages]]` table still wins and is never excluded | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing) |
| Configuration | New `reference_listing = false` turns the automatic listing off; the site then lists only its `[[source_pages]]` tables, as in 4.0.0. New `reference_exclude = [...]` takes repository-relative glob patterns; `**` spans folders and a pattern ending in `/` matches everything below that folder. A wrong type or pattern fails the build with a `site.toml:` error | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing) |
| Build | An automatically listed page has a route derived from its path: lowercased parts joined with `.`, ending `.md.html`, so `README.md` becomes `readme.md.html`. Moving or renaming the file changes its address. A collision adds eight hexadecimal digits of the path's SHA-256 and never fails | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing) |
| Build | An automatically listed page never fails the build. Dead links, missing anchors, unpackageable or external images, unsafe raw HTML, a missing level-one heading and bytes that are not UTF-8 are shown tolerantly. The build prints how many problems it tolerated; `lint` prints each as a `NOTE:` line, also under `--strict`. Registered pages keep their strictness | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing) |
| Build | Raw HTML in an automatically listed file cannot run a script or load content from outside the bundle: `<script>`, `<style>`, `<iframe>`, `<svg>`, `<math>` and similar tags show as text, and every other tag loses event handlers, loading attributes and outside addresses. Registered pages are not filtered | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing) |
| Theme | The Reference section now ends the sidebar of every page whenever at least one file is listed, also on a site without `[[source_pages]]` tables | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages), [shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Build | On a source page, a link to a tracked Markdown file that is listed automatically now goes to that file's page. In 4.0.0 it was a source link to the repository | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Build output | Above 60 listed files, or with the page lock on, the folder tree is written once as `reference.tree.js` and as the page `reference.index.html` in the html root, and each page carries a short form of the section. `site-build.json` gains `reference_tree`, which names both files or is `null`; its `source_pages` also maps every automatic route to its file. The name `reference.index.html` is reserved in that case: another page with that address fails the build with `route collision` | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Configuration | Removed: the settings `path_resolver` and `evidence_validator`, and the evidence adapter's optional `document_origin`. A `site.toml` that names either setting fails the build with `site.toml: <setting> was removed in kit 5.0.0`, which points to the migration step, and lint prints that error. The kit resolves links with its own rules only, so a link that only the project's adapter mapped is a dead link or a missing anchor in lint. `content_transform` and `worklog_links_checked_from` stay | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Publication | New optional page lock: `lock = true` in `[publication]`, the passwords `DOCSITE_GENERAL_PASSWORD` and `DOCSITE_REFERENCE_PASSWORD` from the environment of the `publish` step, and the optional dependency `requirements-lock.txt`. The general password opens the topic pages; the reference password also opens the Reference pages and the exported Markdown files. It is not access control; its limits are listed in the rule. A project that does not set `lock = true` gets the same bundle as from `publish` without the lock | [Page lock](../../../rules/site/publication.md#page-lock) |
| Publication | `publish` refuses a `[[source_pages]]` table whose file the private prefixes or suffixes cover, with `Private source cannot be published as a page` | [Configured publication](../../../rules/site/publication.md#configured-publication) |
| Publication | Fix: an exported source link carries `data-repo-exported`, and `filelinks.js` leaves it alone. With a source remote, a link to an admitted file such as `tools/fit.py` no longer becomes a GitHub address with a wrong `docs/html/` part. This changes the published bytes of admitted links | [Configured publication](../../../rules/site/publication.md#configured-publication) |
| Publication | Fix for a project without a source remote (`gh_repo = ""`): source links keep their local paths, and HTTP previews no longer rewrite them to GitHub. `publish` rewrites the source links of every generated page in the html root, not only the pages named in `[publication] pages`. A link to a tracked file that is not admitted keeps its local path, which leads outside the bundle | [Tooling and ownership](../../../rules/site/authoring.md#tooling-and-ownership) |
| Reader | New fourth view, Presentation, on pages with at least one slide face: the slide fills the window at 16:9 and the full chapter follows when the reader scrolls. "Presentation" starts at the current chapter, "From start" at the first; the address keeps `?view=present` and the chapter. On such pages the view buttons move into the view menu at 980 px | [Shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Reader | All chapters hides slide faces until its Slides switch shows them. The choice is remembered per page, and printing from All chapters follows it. One chapter, Two chapters and Presentation always show the faces | [Shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Rules | Slide faces get no prescribed arrangement. Each face's layout follows the shape of its content; the faces of a project share a frame: the label row, the title, the scope line, the type roles and the tones. The shared slide components are parts to choose from. A review of existing faces sorts them into three groups: redraw or remove, redesign, keep | [Slide faces](../../../rules/writing/pages.md#slide-faces) |
| Rules | Chapters and slide faces are asked for visual ambition: the most telling picture each claim allows, in the form that fits it, varied across a page. A face is limited to one finding, not to one visual. It may crop, combine, annotate or redraw the chapter's figures and draw numbers the chapter states in a table or in text, using the chapter's numbers and no others | [Page design](../../../rules/writing/pages.md#page-design), [slide faces](../../../rules/writing/pages.md#slide-faces) |
| Rules | A report or message names a file by its full path from the repository root, as a link where the reader's tool opens links; a file outside the repository gets an absolute path | [Reporting completion](../../../rules/engineering/handoffs.md#reporting-completion) |
| Rules | Before building supporting code, such as a harness, a judge or a run recorder, an agent writes the need in one sentence that names no experiment and reads the project's capability map. It uses code the map lists as `exists`; otherwise it adds the need to the map's list of needs seen but not built, stops and brings the person three options: build it once as a tool, build the minimum inside the experiment, or do not build. Each project keeps the map at `docs/CAPABILITY_MAP.md`: one table with the columns Need, Code, State and Imported by, and the list of needs seen but not built with the person's decisions | [Name the need first](../../../rules/engineering/code.md#name-the-need-first), [the capability map](../../../rules/engineering/code.md#the-capability-map) |
| Rules | At each attempt an experiment's record gets one line with the running total: attempts, usable results, lines of supporting code and of its tests, and the person's minutes. The total counts the machinery, not the runs, seeds, controls or repetitions; it is information for the person, has no threshold and stops nothing, and an experiment is never weakened to shrink it. After every third finished experiment, or another interval the project names, and whenever the person asks, a fresh agent that only reads looks for needs solved more than once, work the person keeps doing by hand and what the totals show | [Show the total](../../../rules/experiments/workflow.md#show-the-total), [step back across experiments](../../../rules/experiments/workflow.md#step-back-across-experiments) |
| Lint | New error: a chapter with more than one slide face, a face that does not open its chapter and a face outside every chapter, each with the page and the chapter. Lint reads the built pages; a face opens its chapter when nothing readable comes before it there | [Slide faces and decks](../../../rules/site/authoring.md#slide-faces-and-decks) |
| Lint | New warning, which fails `--strict`: a number that a slide face shows and its chapter does not show outside the face, with the page, the chapter and the numbers. It needs no list from the project. Thousands separators, the Unicode minus, trailing zeros and a space before a percent sign do not make two numbers; numbering such as `01`, figure and table numbers, versions and digits after a letter are not counted. `data-face-only="<reason>"` on an element that holds exactly one number on a face accepts that number; lint prints the acceptance as a note, and a mark without one number, without a reason or no longer needed as a warning | [Slide faces and decks](../../../rules/site/authoring.md#slide-faces-and-decks), [module description](../../../tooling/slide_face_checks.py) |
| Browser checks | `slideFaces(page, {within?})` measures faces where the page shows them, in a page at reader widths or in a deck: a stacked face's sideways overflow, text cut off by a box and parts that stick out of the face, as `problems`, besides the 16:9 fit. Per face it also reports `emptyBand`, the height of the largest empty band of the canvas, as information with no threshold, and `drawingText`, the smallest rendered size of a label in the face's inline SVG drawings; a label below the 11 px of the figure rule is a problem, at every width. A face the page does not show has `shown: false`. New `assertSlideFaces(page, {within?, expectShown?})` fails with every problem. The kit's own browser review and the starter review call it at 1600 and 390 px | [Reusable browser checks](../../../rules/site/validation.md#reusable-browser-checks) |
| Theme | Fix: in a chapter narrower than 520 px the slide face that opens it bled 22 px into a chapter body padded 14 px, so the chapter scrolled sideways by 8 px and cut the face's edges at phone width. The bleed now matches the padding | [Slide faces and decks](../../../rules/site/authoring.md#slide-faces-and-decks) |
| Rules | A claim and its limit are one finding: the visual carries the claim and the face shows the limit second, smaller. Two findings that do not depend on each other do not share a title; the face takes the main one and the chapter keeps the other. A stacked face does not overflow sideways, cut text or let a part stick out | [Slide faces](../../../rules/writing/pages.md#slide-faces) |
| Rules | Clarified where the slide-face rule gave two readings: tiles that hold only numbers or counts are boxes, not a visual; the grid of options that may stand as the visual has one column per option and one row per factor, and a list of each factor's levels is not such a grid; in a chapter that teaches, the finding a title states is how the thing works. A notice that a project writes itself for vendored code or data is named after its subject; only files that arrive with third-party code keep their names | [Slide faces](../../../rules/writing/pages.md#slide-faces), [README is the bounded exception](../../../rules/documentation.md#readme-is-the-bounded-exception) |
| Rules | Faces are checked in their page as well as in the deck, because page styles add space the deck lacks. A review by eye says for each face what draws the eye first and whether a band of the canvas is empty; "no band left over" and the designer's standard stay judgment with no number. The kit's lint checks the slide-face part of the numbers rule; the ledger of sources stays the project's | [Validation and review](../../../rules/site/validation.md#validation-and-review), [numbers and staleness](../../../rules/records.md#numbers-and-staleness) |
| Configuration | Removed: the settings `evidence_manifests` and `legacy_files`. Lint no longer verifies the bytes of a declared collection of copies, resolves a copy's links from its original path, applies a collection's recorded `source_root` to worklog links, or maps single old paths to current files. A `site.toml` that names either setting fails the build with `site.toml: <setting> was removed in kit 5.0.0`, which points to the migration step. `worklog_links_checked_from` stays the way to stop checking links in old worklog entries; the declared local evidence of `local_artifacts_manifest` and `local_media` is unchanged | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Configuration | New optional top-level settings `tooling_roots`, `capability_map` and `experiment_roots` turn on the capability map check. A wrong value, or `capability_map` or `experiment_roots` without `tooling_roots`, fails the build with a `site.toml:` error. With the check on, lint fails when the map is missing or untracked, when a tracked file or folder directly under a tooling root has no row, when a link in the map is dead wherever it lies, and when the generated Imported by column is out of date; a Python file under a tooling root that imports from an experiment folder is a warning. The new command `docsite.py capability-map` rewrites the Imported by column from Python imports. Without `tooling_roots` nothing is checked | [Capability map settings](../../../rules/site/authoring.md#capability-map-settings), [the check](../../../rules/engineering/code.md#the-check) |
| Rules | An experiment's folder holds only that experiment's own code, inputs and records. Code that other experiments or tools reuse lives in the project's tooling or source tree, and is moved there before a second user imports it | [Where code lives](../../../rules/engineering/code.md#where-code-lives) |
| Build output | Changed shared files get a new `?v=` query on every page that loads them: `base.css`, `chapter-reader.css`, `chapter-reader.js`, `filelinks.js`, `lightbox.js`, `nav.js`, `plot-toggles.js` and `slide-face.css`. A locked bundle also holds `assets/page-lock.js` and `assets/page-lock.css` | [Authoring and configuration](../../../rules/site/authoring.md) |
| Starter | The starter's `site.toml` explains the listing and excludes `CLAUDE.md`, and carries the capability map settings commented out. The starter adds an empty `docs/CAPABILITY_MAP.md` with a short explanation, linked from `docs/index.md`, and its `AGENTS.md` gains the route "Building tooling, a harness or other supporting code". The guide's text on slide faces describes the layout as one example | [Automatic reference listing](../../../rules/site/authoring.md#automatic-reference-listing), [slide faces](../../../rules/writing/pages.md#slide-faces), [the capability map](../../../rules/engineering/code.md#the-capability-map) |
| Build | Fix: a `**INVARIANT:**` or `**DON'T-REDO:**` marker inside a fenced code block, with backticks or tildes and also one left open to the end of the page, stays text in the block. Up to 4.0.0 it became a card and broke the block, which failed the reader build or showed a stray closing tag. A marker paragraph followed by a fence without a blank line ends where the fence starts. `lint --registry` no longer lists a marker inside a fenced block or a code span, and lint no longer warns about a line that names the markers in code spans | [Rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology) |
| Theme | Fix: in the zoomed figure the plot toggle chips show the colour of their series; up to 4.0.0 every dot there was grey, because the lightbox built its chips on a copy of the figure that was not yet in the page, and a detached element has no computed colour. A chip keeps its label on one line, and the zoomed figure's chip bar spans the window less a margin and wraps whole chips; up to 4.0.0 the bar was half the window wide, so at 390 px a label such as "Menger joints (default)" broke inside its chip. A click beside the chips still closes the zoomed figure | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Lint | New error: a link written as HTML, `<a href="…">`, to a repository file whose target does not exist, or whose fragment into a Markdown file matches no anchor. Lint reads the source links the build marked in the built pages, so it uses the build's resolution, with a source remote and without one. It covers topic pages, the fragments they include and registered source pages; the message names the page's source, the built page and the repository path. On an automatically listed page the problem is a note; links in worklog entries before `worklog_links_checked_from` are not checked. A built relative link without a source remote is no longer also reported as `dead relative href` | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Lint | New error: a formula on a built page that does not compile with the kit's KaTeX, with KaTeX's message; a formula that Markdown split with markup; an opening `$$` or `\(` whose closing delimiter is not in the same text. Each names the page's source, the built page and the formula. Lint finds the formulas as the page's renderer does, on every page that loads it, and compiles them in Node.js: `DOCS_NODE`, or `node` on `PATH`. Building still needs no Node. Without Node lint prints a note and passes; with the new setting `formula_check_required = true` it fails, so that a project's checks cannot skip the check silently. After the check lint prints how many formulas compiled. A project test that compiles its formulas itself may be dropped | [Formula check](../../../rules/site/authoring.md#formula-check), [mathematical explanation](../../../rules/writing/math.md#mathematical-explanation) |
| Kit checks | `requirements-lock.txt` pins `cryptography` 50.0.2 for the page-lock checks; the Pages workflow installs it. New checks: `tests/test_formula_checks.py`, `tests/test_reference_listing.py`, `tests/test_capability_map.py`, `tests/test_page_lock.py`, `tests/test_slide_face_checks.py`, `tests/test_markers.py`, `tests/test_source_links.py`, the WebCrypto cross-check and two browser suites, `tests/test_reference_tree.cjs` and `tests/test_page_lock_browser.cjs`. `tests/test_browser_checks.cjs` now checks stacked slide faces at 390 px and the plot toggle chips in the zoomed figure | [README](../../../README.md#develop-the-kit) |
| Kit site | New page for people, "Approval that failed open", and its record: how supporting code piled up in ADP, the project the kit was extracted from, measured from its Git history, and which kit rules answer each pile. Its figures are generated from the measurement by a script beside the record, which `tests/run_checks.sh` runs with `--check`. No consumer change | [Approval that failed open](../approval-failed-open/approval-failed-open.md) |

## 4.0.0 — finished working documents, neutral theme names and group colours

4.0.0 is a major release under
[what a version number promises](#what-a-version-number-promises) for one
reason: it removes a section anchor under `rules/`. `rules/records.md` loses
`#evidence-identity-and-frozen-records`; its section is replaced by
[finished working documents](../../../rules/records.md#finished-working-documents),
which says the opposite: a finished plan, decision record, review or
coordination note is deleted and cited from Git, not kept as an unedited copy.
Lint fails on a Markdown link to the old anchor until the project repoints it;
links written as HTML `<a href>` are not checked. No other anchor under
`rules/` changed, and no command, flag, configuration key, marker or adapter
signature is removed. The new `build --check-reader` flag and the new
`site.toml` settings `worklog_links_checked_from`, `[group_colors]` and
`[plot_toggle_labels]` join the stable interfaces. A project that already
used one of these three names as a top-level `site.toml` key for something
else fails the build until it renames its own key. Follow the [4.0.0 migration guide](migrations/4.0.0.md).

Removed or renamed interfaces, with their status under the
[stable and provisional interfaces](#100--first-stable-version):

- The section anchor `rules/records.md#evidence-identity-and-frozen-records`:
  stable, removed. This makes the release major.
- The CSS variables `--adp` and `--ada`: theme internals, never listed as
  authoring markup, so provisional. Renamed to `--accent` and `--secondary`,
  which they only pointed to.
- The classes `badge adp`, `badge ada`, `card ada`, `band-adp`, `band-ada`,
  `b-adp` and `b-ada`: theme class names outside the documented authoring
  markup, so provisional. Renamed to `badge accent`, `badge secondary`,
  `card secondary`, `band-accent`, `band-secondary`, `b-accent` and
  `b-secondary`, with the same styling. The new variable and class names are
  provisional as well: no guide under `rules/` lists them as authoring markup.
- The colours of the navigation groups `method`, `road`, `racing`, `sim` and
  `related work`, hard-coded in four theme stylesheets: provisional theme
  styling, removed. `[group_colors]` replaces them.
- The `reader-drawer-pin` button: a theme class, provisional, removed. The
  reader built it and never added it to the page.
- The chip labels of nine plot group keys in `plot-toggles.js`, such as
  "Menger joints (default)" for `menger`: undocumented component internals,
  so provisional, removed. `[plot_toggle_labels]` replaces them.

No lint or build check reports a project that still uses one of the renamed
theme names; the element only loses its style. The migration guide gives a
search for each.

| Area | Consumer change | Owning contract |
|---|---|---|
| Rules | Removed: the section "Evidence identity and frozen records". New: finished working documents. A plan, decision record, review or coordination note is deleted once its work has landed and its lasting content is in the owning record, with the person's approval; Git keeps it, and whatever still needs it cites the commit and path. No unedited copy stays in the tree or moves into an evidence folder | [Finished working documents](../../../rules/records.md#finished-working-documents), [rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology) |
| Rules | Run output that a stated number or verdict rests on is tracked in the experiment directory before the experiment is reported complete; a claim that rests on output only in an untracked folder is not measured. Keeping run output outside Git is the person's decision, recorded as an unresolved choice until answered. The 3.2.1 sentence that let repository size decide where material is stored is gone | [Numbers and staleness](../../../rules/records.md#numbers-and-staleness) |
| Rules | Uncommitted code of a run is kept as a diff against the commit the run started from, with new files and submodule changes; a run does not copy the working tree, and an unavoidable copy holds no ignored files. A plan, protocol or review document that a run recorded by hash is identified by its commit, path and hash | [Numbers and staleness](../../../rules/records.md#numbers-and-staleness) |
| Rules | Work alone happens in the project's checkout on its current branch. A separate branch or worktree is used only when other work changes the same repository at the same time, when a running job depends on files the work would change, when the project's workflow asks for one, or when the person asks for one | [Parallel work](../../../rules/engineering/delivery.md#parallel-work) |
| Rules | A question for the person that is not answered before work stops is written into open work as an unresolved choice, routed from `OPEN.md` | [Decisions and blockers](../../../rules/engineering/delivery.md#decisions-and-blockers) |
| Rules | New section: scratch files. An agent deletes the untracked drafts, review captures and temporary test folders its own work created, without approval; run output is never scratch. A record cites no scratch file by path or hash | [Scratch files](../../../rules/engineering/handoffs.md#scratch-files), [validation and review](../../../rules/site/validation.md#validation-and-review) |
| Rules | A full refactor deletes a caller that is a finished probe or one-time script instead of updating it, when nothing imports it, no rerun is planned and its result is recorded with a source pin; claims that rest on it are historical from then on. A source pin still stands for code after the code is deleted from the current tree | [Refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility), [Numbers and staleness](../../../rules/records.md#numbers-and-staleness) |
| Rules | New section: dependencies. Every dependency is declared in the project's dependency file and installed; a pinned Git submodule counts as declared | [Dependencies](../../../rules/engineering/code.md#dependencies) |
| Rules | A repository has one `README.md`, at its root; any other folder's guide is named after its subject. Not enforced by lint; the conformance check lists it | [README is the bounded exception](../../../rules/documentation.md#readme-is-the-bounded-exception), [conformance](../../../rules/conformance.md) |
| Rules | A page that explains how something works names the people who do the work by role, not by name | [Page design](../../../rules/writing/pages.md#page-design) |
| Rules | Slide faces are added only when the person says yes, after the chapters are built. A face shows one finding with a real visual; a face whose main area only repeats its title and lead in boxes is removed. A missing figure is work for the page author, made from what exists | [Slide faces](../../../rules/writing/pages.md#slide-faces), [figures](../../../rules/writing/figures.md#figures-and-comparisons) |
| Rules | A generated figure names its generator and its input data; the manifest no longer records revision, date or output hash, which Git holds. Lint reads only `script`, as before | [Figures](../../../rules/writing/figures.md#figures-and-comparisons) |
| Rules | The path and evidence adapters exist only for projects that keep old documents whose links name old paths; a project removes its adapter once no record that is not edited afterwards names an old path. The hooks still work in 4.0.0, and the kit removes each one once no project uses it | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Configuration | New optional `worklog_links_checked_from = "YYYY-MM-DD"`: lint checks links only in worklog entries dated on or after that day. Any value but a `YYYY-MM-DD` date is an error | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Configuration | New optional `[group_colors]` table: one hex colour per navigation group, written to `assets/group-colors.css` and linked on every page after `base.css`. The build rejects a value that is not a table, a colour that is not a 3, 4, 6 or 8 digit hex colour, and a name no visible `[[nav]]` entry uses. Groups without an entry take the `nav.js` tones | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Build | A worklog registered as a source page applies `worklog_links_checked_from`: in an entry dated before that day, a link or image whose target is gone renders as its text, unlinked, in `<span class="link-gone">` with a dotted underline from `base.css`, and a fragment into a registered page is not checked. Links whose target exists stay links; newer entries fail on a missing target as before. The build, not only lint, now rejects a value that is not a date | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Configuration | New optional `[plot_toggle_labels]` table: one chip label per plot group key for pages that load `plot-toggles`, written into each such page as a JSON block. The build rejects a value that is not a table and a label that is not text | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Command | New `docsite.py build --project . --check-reader`: renders every topic page with and without the chapter reader, writes nothing and exits with status 1 when the reader changes a page's content | [Validation and review](../../../rules/site/validation.md#validation-and-review) |
| Theme | `--adp` and `--ada` renamed to `--accent` and `--secondary`; seven classes renamed, as listed above. The hard-coded colours of five group names are gone, so those groups take `nav.js` tones until the project sets `[group_colors]`; with the table, their home-map card edges take the group colour. The unused pin button is removed | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Theme | `plot-toggles.js` no longer holds the labels of nine group keys, which were one project's plot series; without `[plot_toggle_labels]` a chip shows its group key | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Theme | New slide-face classes `slide-points` and `slide-facts`, and a keyed `figcaption.slide-legend` inside `slide-figure` | [Slide faces and decks](../../../rules/site/authoring.md#slide-faces-and-decks) |
| Build output | Changed shared files get a new `?v=` query on every page: `base.css`, `chapter-reader.css`, `chapter-reader.js`, `panel-switcher.css`, `plot-toggles.js`, `slide-face.css`, `home.css`, `build-sheet.css` and three font `SOURCE.txt` notices. A site with `[group_colors]` gains `assets/group-colors.css`; no other built file is added or removed | [Authoring and configuration](../../../rules/site/authoring.md) |
| Lint | A configuration error in `site.toml` was reported as a stale site; lint now prints the build's error | [Validation and review](../../../rules/site/validation.md#validation-and-review) |
| Starter | The guide page's two slide faces are rebuilt around SVG figures in two new fragments. The starter router is unchanged | [Slide faces](../../../rules/writing/pages.md#slide-faces) |
| Kit checks | Node checks of the reader, fold controls and panel switcher run in an imitation page without a browser; a test checks that a built site ships the kit's component files unchanged | [README](../../../README.md#develop-the-kit) |
| Kit checks | The browser suites load Playwright from the kit's own `node_modules/`, installed by `npm ci` from a root `package.json` and `package-lock.json` that pin version 1.62.1; the Pages workflow installs from the same files. `DOCS_PLAYWRIGHT` and `DOCS_CHROMIUM` are gone. Only kit development is affected: building a site needs no Node.js | [README](../../../README.md#develop-the-kit) |

## 3.2.1 — rule wording corrected

3.2.1 is a patch release under
[what a version number promises](#what-a-version-number-promises): it corrects
rule text, changes no tooling, and needs no migration step.

- [Rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology)
  said that `INVARIANT` and `DON'T-REDO` markers must not appear on rendered
  pages. The build renders a marker at the start of its own
  paragraph as a labelled card, and lint says that such declarations belong on
  pages. The rule now says what the tooling does: a page may carry a marked
  statement as an unindented paragraph of its own, followed by a blank line.
  Anywhere else, such as inside a sentence, a list item or a quote, the raw
  label still shows. ADP met the disagreement: 28 of the 35 markers on seven
  of its pages already rendered as cards.
- Two sentences used "evidence" for different things, and together they read
  as a contradiction. [Rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology)
  now says that its limit concerns byte-exact copies of superseded documents,
  kept for the purposes that
  [evidence identity and frozen records](https://github.com/davszi/documentation-kit/blob/v3.2.1/rules/records.md#evidence-identity-and-frozen-records)
  names, and that it does not shorten what an experiment retains.
  [Numbers and staleness](../../../rules/records.md#numbers-and-staleness)
  gains the principle behind it: repository size decides where an
  experiment's material is stored, not whether it is kept, and material held
  outside Git is located and identified from the experiment directory.
- [Numbers and staleness](../../../rules/records.md#numbers-and-staleness)
  listed "producing code" and "source pins" side by side and did not say when
  one replaces the other. It now does: a pin stands for code in the repository
  when the run started from a clean tree with its submodule pointers
  committed, the commit stays reachable on a branch or tag that is never
  rewritten, and the experiment directory records the pin, the command and the
  input identities.
  Uncommitted code, or code outside the repository, is kept as a copy or a
  diff. A project need not copy its source into every run folder.
- [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown)
  told a project to preserve a hidden stub while dated or frozen links depend
  on a removed page, while
  [refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility)
  leaves such a choice to the owner and tells it to add no redirects when
  compatibility is not needed. The first rule now defers to the second: the
  owner chooses between a hidden stub, which keeps the published address, and
  the project's path adapter, which keeps the links resolving for lint and
  lets the address go. Lint rejects an uncovered link in the files it checks.

## 3.2.0 — topic group folders and folded navigation groups

3.2.0 is a minor release under
[what a version number promises](#what-a-version-number-promises): it adds two
optional settings to the stable interfaces, and a project that sets neither
builds the same pages, addresses and sidebar as before. The
[3.2.0 migration guide](migrations/3.2.0.md) gives the steps.

- `topic_group_folders = ["parked"]` in `docs/site/site.toml` lets topic
  folders live one level deeper, at `docs/topics/<group>/<topic>/index.md`.
  A nested topic counts like any other in the build, in lint, in the
  record-or-`page_only` check and in the lint notes. Its address stays
  `<topic>.html`, so moving a topic into a group folder changes no published
  address. [Topic group folders](../../../rules/site/authoring.md#topic-group-folders)
  has the rules: one group level, no Markdown file directly in a group folder,
  and no two topics with the same folder name.
- `folded_groups = ["parked"]` folds the named navigation groups in the flat
  site tree, on pages with and without the chapter reader. A folded group is
  closed unless it holds the current page, remembers a reader's choice in the
  browser and works without JavaScript.
  [Authoring paths](../../../rules/site/authoring.md#authoring-paths) describes
  it beside `nested_nav`, which folds every group and only on pages without
  the reader.
- Lint prints a note for a page two levels below `docs/topics/` whose parent
  folder is not a declared group folder and has no page of its own. Such a
  page was never built, and before this release nothing said so. The note
  never fails lint.

`site.toml` has no check for unknown top-level keys, so a project that already
used a key named `topic_group_folders` or `folded_groups` for something else
must rename its own key.

ADP asked for both settings, to keep four parked topics apart from its current
ones in the source tree and in the sidebar.

## 3.1.0 — one site name in the sidebar header, two lint warnings relaxed

3.1.0 is a minor release under
[what a version number promises](#what-a-version-number-promises): the header
change alters how the shared theme looks, every key still parses and no project
that built before fails. One stable key loses its effect, as the first item
says. The [3.1.0 migration guide](migrations/3.1.0.md) gives the steps.

- The sidebar header shows the site's name on every page: `home_label`, or
  `title` when `home_label` is not set or blank. Up to 2.0.0 a page with the
  chapter reader showed `home_label` in its drawer and a page without the
  reader showed its own `brand` frontmatter. 3.0.0 showed the page's `brand`
  everywhere, so a project whose pages set different values got a header that
  named the current page while linking to the home page. 3.1.0 returns to one
  name for the site and applies it to every page.
- The page frontmatter key `brand` is deprecated. It is still accepted and has
  no effect; there is no per-page replacement. Registered source pages, which
  showed `title`, now show `home_label` too when it is set.
- The browser stores a reader's open navigation groups and pinned drawer under
  the site's name. A project that changes or removes `home_label` resets those
  two saved preferences once for its readers.
- A one-character `brand_mark` is drawn larger. At the size meant for two or
  three characters it was faint in its tile.
- A link to a file that the local-artifact manifest lists under
  `omitted_files` now gets a note when the file is absent. It was a warning,
  so `lint --strict` failed on a state the project had declared on purpose.
  A missing file that the manifest does not list is still an error.
- Lint no longer warns about a worklog entry without a commit hash. The check
  recognised only entries written as a bold bullet, so it skipped every other
  entry, and an append-only worklog could never clear its old hits. The rule
  that a landing records its commit stays in
  [rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology).
- Two migration guides gain an instruction that ADP's upgrade showed was
  missing. The [2.0.0 guide](migrations/2.0.0.md#experiment-guides) tells a
  project to add the router rows for the two experiment guides and to compare
  its router with the starter's. The
  [3.0.0 guide](migrations/3.0.0.md#router-anchors) says that a link about the
  experiment floor goes to the experiment workflow guide, not to the figures
  guide that the anchor table names.

The starter no longer sets `home_label`, and neither the starter pages nor the
kit's own pages set `brand`. [What a version number promises](#what-a-version-number-promises)
gains the patch level.

## 3.0.0 — router anchors removed, topic records and repository files in the sidebar

3.0.0 is a major release under
[what a version number promises](#what-a-version-number-promises) for one
reason: it removes section anchors under `rules/`. `rules/writing.md` and
`rules/maintenance.md` lose their section anchors, sections move out of
`rules/documentation.md` and `rules/writing/explanations.md`, and
`rules/writing/evidence.md` is removed. Lint fails on a Markdown link to an old
location until the project repoints it; links written as HTML `<a href>` are
not checked. No command, configuration key, marker or adapter signature is
removed.
Follow the [3.0.0 migration guide](migrations/3.0.0.md).
One check can fail a strict lint run: a topic page without a record
must add one or declare `page_only`. Two provisional tooling modules that no
known consumer imported are removed. A project that wants to keep the
∿ sidebar mark sets `brand_mark = "∿"`. Build-sheet flows now stack
vertically when their chapter card or page is narrow; grids, checks and
chapter headlines follow the card's width; box lists use dashes and tinted code
chips, and code keeps its case inside uppercase titles.

| Area | Consumer change | Owning contract |
|---|---|---|
| Sidebar | A site with at least one `[[source_pages]]` entry gets a **Reference** section after its navigation: records with `pinned = true` listed first, then a **Browse by folder** tree of every registered file, closed on pages for people. Sites without registered files are unchanged | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Assets | Pages load shared assets with a content-hash query, `assets/<file>?v=<hash>`, so browsers fetch a changed stylesheet or script after a rebuild; unchanged assets stay cached | [Authoring and configuration](../../../rules/site/authoring.md) |
| Sidebar header | The ∿ mark is no longer shared: optional `brand_mark` sets a project's own mark (up to three characters or a tracked SVG); without it the mark is the title's initials. To keep ∿, set `brand_mark = "∿"`. The reader drawer shows the same mark and name as other pages and no longer shows a chapter counter; hiding the menu applies across the site instead of per page. Groups without a CSS colour get tones in order | [Authoring and configuration](../../../rules/site/authoring.md) |
| Topics | Every topic has a record; a topic page without one declares `page_only = "<reason>"` in its frontmatter. Lint warns about a topic page with neither, so `--strict` fails until the project adds a record or the declaration | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Lint | When a record section changes, lint prints notes naming the pages that link to it; `--since <rev>` compares with an older commit. Notes never fail lint | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Lint | New optional setting `page_number_notes = true`: lint prints a note for each number in a topic page's prose that none of the page's linked records state. Values shown as code, labels, versions, dates and ratios are not read; a page that links no record is skipped. Notes never fail lint. Off by default, and not meant for pages that report measurements from experiment data | [Rendered pages are for people](../../../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown) |
| Reader rule | The sidebar docks by default on screens wider than 900 px; the guide now states the value the shared reader already used | [Shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Conformance | New guide: the project conformance check to run when a kit pin moves or a repository changes hands; the starter router routes to it | [Project conformance check](../../../rules/conformance.md) |
| Configuration | A registered source page no longer needs a `[[nav]]` entry; topic pages still do. `[[source_pages]]` accepts optional `pinned = true` | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Rules | Removed: the stub headings in `rules/writing.md` and `rules/maintenance.md`, which only forwarded old links. Both files are now plain indexes of the focused guides. A link to one of their former anchors must point at the focused guide's own section; links to the files without an anchor still work | [Router anchors](migrations/3.0.0.md#router-anchors) |
| Rules | Records and pages are documented in a fixed order: the working agent writes the record first, and a page for people is made on request, by a separate agent where the runtime supports delegation. New guide `rules/records.md` gathers what a record needs; `rules/writing/` now covers pages; its rules about what a code excerpt, a formula or an experiment visual may claim still apply to records. `rules/writing/evidence.md` is removed and six sections moved, so links to them must be repointed. The starter router has three documentation rows in place of two | [Record first, page on request](../../../rules/documentation.md#record-first-page-on-request), [sections that moved](migrations/3.0.0.md#sections-that-moved) |
| Theme | Sidebar groups are toned sections, wrapped in `div.nav-section` in the built HTML. The home hero (`.home-hero`) lays out in two columns with a larger headline. Numbered steps in build-sheet boxes show their number in the box's tone | [Shared reading layout](../../../rules/site/reader.md#shared-reading-layout) |
| Rules | The Git guide now says what the pin check always did: it counts the kit's remote branches, not tags | [The shared kit submodule](../../../rules/engineering/git.md#the-shared-kit-submodule) |
| Rules | Every visual change is reviewed by eye before it is reported done, from whole-element captures at each supported width and reader view | [Validation and review](../../../rules/site/validation.md#validation-and-review) |
| Rules | A worklog entry and its commit message cover the same landing on purpose and are written in the same step. `OPEN.md` format, which lint already checked, is now stated | [Rules for changes and chronology](../../../rules/documentation.md#rules-for-changes-and-chronology), [open work](../../../rules/documentation.md#from-open-work-to-subject-knowledge) |
| Starter | The home page links `../PROJECT_CONTEXT.md`; the 2.0.0 starter linked a file that does not exist. The reading index has three documentation rows in place of two | [Starter home link](migrations/3.0.0.md#starter-home-link), [reading index](migrations/3.0.0.md#reading-index) |
| Build fix | A paragraph that follows a fold now renders as Markdown, with or without a blank line after the closing marker. Before, the paragraph, typically a "Full guide" line with links, appeared as raw text. Pages with such paragraphs change in the built output | [Story and reading layers](../../../rules/writing/explanations.md#story-and-reading-layers) |
| License | The kit's own rules, tooling, theme and starter are under the MIT License; bundled fonts and KaTeX keep their own licenses. Earlier versions granted no license. Every built site gains one file, `html/assets/documentation-kit/LICENSE`; a project asset with that output name fails the build | [License](../../../README.md#license) |
| Tooling | Removed: `tooling/number_ledger.py` and `tooling/verbatim_blocks.py`, both provisional since 1.0.0. The rule that a redesign records number sources in a ledger and locks kept blocks stays; each project keeps its own ledger format and checks. `tooling/svg_figures.py` stays | [Numbers and staleness](../../../rules/records.md#numbers-and-staleness) |

## 2.0.0 — source pages, kit website, configured publication and compatibility removals

2.0.0 is a major release because it breaks the 1.x contract in two places,
under [refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility):
the exporter no longer renames or relocates files, and the old local-artifact
manifest location is no longer read. `docsite.py lint` also fails a project
whose pinned kit commit is on no remote branch of the kit. Everything else adds
to the 1.x surface. Every consumer follows the
[2.0.0 migration guide](migrations/2.0.0.md); a consumer that uses neither
removed form only adds one router row. The 1.0.0 stable and provisional
interfaces below still apply to 2.x, apart from these removals.

| Area | Consumer change | Owning contract |
|---|---|---|
| Configuration | Optional `[[source_pages]]` tables render an existing tracked Markdown file as a whole-file page at a chosen route; links and media resolve from the file's own folder | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Build checks | Fragments into a registered page, and every fragment a registered page links, must match a rendered anchor; registry, containment and route-collision errors fail the build | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Lint | Registered files' Markdown links are checked as ordinary records | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Theme | Additive `base.css` rules for the source line (`.source-origin`) and the opt-in `reference-page` body class, whose Markdown tables also get the labelled narrow-screen scroll region; existing pages render unchanged | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Build manifest | `site-build.json` gains a `source_pages` map from route to source file | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Navigation | Optional `nested_nav = true` folds navigation groups and nests the current page's sections under its entry; the flat tree remains the default | [Authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Reader | A registered page with `reader = true` merges a short opening and its source line into the first chapter; longer openings stay a separate chapter | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Sidebar | A registered page without the reader that is listed in the navigation keeps the site tree in its sidebar, marked as current; hidden registered pages, and pages under `nested_nav`, still list their sections | [Registered source pages](../../../rules/site/authoring.md#registered-source-pages) |
| Theme fixes | A carousel inside a build-sheet grid figure now shows one slide at a time (its rule outranks `.bs-grid figure img`); the reader help describes docking with `«` and `☰` instead of a pin button that is not shown | [Reader](../../../rules/site/reader.md#shared-reading-layout) |
| Repository | Extraction history is removed: `provenance.json`, `verification/`, `preview/`, the extraction record and `rules/extraction-map.md`. Nothing consumers run or route to used them; they remain at the `v1.1.0` tag | [Kit context](../../KIT_CONTEXT.md) |
| Starter | Entry files are stored as `*.tmpl` and written under their real names by `init`, which gains `--title` and `--repository` for `site.toml`; generated projects are unchanged apart from those values | [Start a project](../../../README.md#start-a-project) |
| Lint | Optional `open_work` setting names the open-work file (default `docs/open/OPEN.md`); every worklog check now honours the existing `worklog` setting | [Resources and evidence](../../../rules/site/resources.md) |
| Repository | The kit's own entry files are `docs/KIT_CONTEXT.md`, `docs/KIT_INDEX.md`, `docs/KIT_WORKLOG.md` and `docs/open/KIT_OPEN.md`; its `AGENTS.md` and `CLAUDE.md` state they apply only to the kit repository | [Kit context](../../KIT_CONTEXT.md) |
| Engineering guide | New "Refactoring over compatibility" section in the code guide: ask the owner, with evidence, before changing a form others may still use; once the owner decides no compatibility is needed, update every reference and remove the old form. The documentation guide no longer allows compatibility routes by default | [Refactoring over compatibility](../../../rules/engineering/code.md#refactoring-over-compatibility) |
| Publication export | Removed: `export_pages` no longer takes `page_routes`; every generated file keeps its name. `public_files` is a list of tracked paths published at the same path, not a mapping | [Publication export](../../../rules/site/publication.md) |
| Evidence configuration | Removed: an absent `docs/evidence/local-artifacts.json` no longer falls back to `docs/project/local-artifacts.json`. The resources guide records why the path adapter is kept and when a project removes it | [Resources and evidence](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Publication command | New `docsite.py publish --project . --out _site` builds and exports a fresh public bundle configured by `[publication]` (`assets_manifest`, `pages`, `private_suffixes`, `private_prefixes`); other keys fail. `site-build.json` gains `resource_origins` | [Configured publication](../../../rules/site/publication.md#configured-publication) |
| Kit pin | `docsite.py lint` fails when a consumer's pinned kit commit is on none of the kit's remote branches. The Git guide forbids commits inside `.docs-kit` and the starter router routes kit changes there | [The shared kit submodule](../../../rules/engineering/git.md#the-shared-kit-submodule) |
| Kit website | The kit builds its own reference site from the repository root | [Website record](../website/website.md) |
| Experiment guides | New shared guides: experiments are investigations or qualifications, start small and state a budget; a pre-stated bar and verdict are required for confirmatory investigations and qualifications; terms for learned or fitted models, such as final runs, are scoped to their own section; claim-scoped verification and regression gates; routes added to the starter's `AGENTS.md` | [Workflow](../../../rules/experiments/workflow.md), [verification](../../../rules/experiments/verification.md) |

When the kit website was added, the starter's generated pages were
byte-identical to 1.1.0 output, with only `assets/base.css` and
`site-build.json` differing; later 2.0.0 changes were not compared byte for
byte. Validation is recorded in the
[worklog](../../KIT_WORKLOG.md#2026-11-07--build-the-kits-reference-website).

## 1.1.0 — focused engineering and documentation guides

1.1.0 adds compatible policy routes and optional evidence configuration to the
1.0.0 stable surface. Existing commands, configuration and adapter signatures
remain available. Follow the [1.1.0 migration guide](migrations/1.1.0.md); adopting
the kit does not require moving an existing consumer's documentation layout.

| Area | Consumer change | Owning contract |
|---|---|---|
| Engineering and delivery | Focused code, performance, execution, delivery and handoff guides; shared Git rules require an explanatory commit body and explicit ownership of shared staging | [Engineering guides](../../../README.md#focused-guides), [Git](../../../rules/engineering/git.md) |
| Contributor entrypoints | One task-triggered `AGENTS.md` router, with a bare `@AGENTS.md` import for Claude; revised starter orientation and reading index | [Agent entrypoints](../../../rules/documentation.md#agent-entrypoints-import-versus-point) |
| Writing and site ownership | Focused `rules/writing/` and `rules/site/` guides; original writing/maintenance routes and their anchors remain available (the anchors until 3.0.0) | [Writing](../../../rules/writing.md), [site](../../../rules/maintenance.md) |
| Visual and evidence guidance | Figures lead mechanism/geometric explanations; scope stays beside evidence; representation follows the question; failed attempts and original settings remain with their evidence | [Page design](../../../rules/writing/pages.md#page-design), [figures](../../../rules/writing/figures.md#figures-and-comparisons), [evidence](../../../rules/records.md#numbers-and-staleness) |
| Optional project layout | New starter uses `docs/PROJECT_CONTEXT.md` and `docs/index.md`; existing project destinations and historical routes stay project-owned | [Canonical homes](../../../rules/documentation.md#canonical-homes), [optional layout migration](migrations/1.1.0.md#optional-project-layout-migration) |
| Local media inventories | Optional `local_artifacts_manifest` selects the inventory path; omitted settings retain the legacy fallback and explicitly missing configured files fail | [Resources](../../../rules/site/resources.md#resource-closure-and-evidence) |
| Exact source snapshots | Optional evidence-adapter `document_origin(path, *, root)` preserves registered snapshot origins, with containment checks and all link/anchor/snippet validation retained | [Evidence adapter](../../../rules/site/resources.md#resource-closure-and-evidence) |

### Validation and adoption scope

The integrated kit passed starter strict lint with zero warnings, all 86 Python
tests, reader-content preservation and both Node checks. Real Chromium checks
covered 1600 × 1000 and 390 × 844 reader/home layouts, paired navigation,
browser-helper and panel-switcher fixtures, slide fit and Continue/Back, deck
presentation/print and narrow no-JavaScript reading. Saved wide, narrow, paired
and deck screenshots were inspected. The [worklog](../../KIT_WORKLOG.md#2026-11-07--integrate-upstream-releases-and-slide-support)
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
| `site.toml` keys and `[[nav]]` keys (`evidence_manifests` and `legacy_files` were removed in 5.0.0); page frontmatter keys | `tooling/browser_checks.cjs` exports |
| Markers: `<!-- include: … -->`, `<!-- site-map -->`, `<!-- slide -->`, `<!-- page-end -->`, typed folds | `tooling/publication.py` (`export_pages`) |
| Shared components by name and their authoring markup | Theme CSS class names other than documented authoring markup |
| Project adapter signatures (`content_transform`; `path_resolver` and `evidence_validator` were removed in 5.0.0) | |
| `rules/` policies (wording may be refined) | |

### What 1.0.0 contains (since 0.1.0)

| Area | Change | Owning contract |
|---|---|---|
| Reader | Chapter slide faces (`<!-- slide -->`), the `slides` deck command, wider One-chapter cards (88% of the stage) | [maintenance](../../../rules/site/authoring.md#slide-faces-and-decks), [writing](../../../rules/writing/pages.md#slide-faces) |
| Components | `panel-switcher` local comparisons | [panel switcher](../panel-switcher/panel-switcher.md) |
| Includes | Shared theme includes resolve first; included fragments may include others (eight levels, cycles fail) | [authoring paths](../../../rules/site/authoring.md#authoring-paths) |
| Configuration | `[[nav]]` tables accept only `label`, `file`, `group`, `short`, `hidden`; project adapters (`path_resolver`, `evidence_validator`, `content_transform`), `extra_assets`, `body_class`, a configured `worklog` path (`extra_components` already existed in 0.1.0) | [maintenance](../../../rules/maintenance.md) |
| Home page | Site-map cards use frontmatter `description` and `thumbnail` when present; guidance to keep the same site tree on every page (`toc = []` on a reader-free home) | [shared reading layout](../../../rules/site/reader.md#shared-reading-layout), [writing](../../../rules/writing/pages.md#project-owned-homepages) |
| Publication | Exporter into an existing publication (`tooling/publication.py`) | [exporting](../../../rules/site/publication.md#exporting-into-an-existing-publication) |
| Generators and checks | `tooling/svg_figures.py`, `tooling/number_ledger.py`, `tooling/verbatim_blocks.py`; browser helpers `slideFaces` and `captureElement` | [generated figures](../../../rules/site/authoring.md#generated-figures), [browser checks](../../../rules/site/validation.md#reusable-browser-checks) |
| Rules | Numbers restated by a redesign need ledger sources; generated SVG uses literal colours | [numbers and staleness](../../../rules/records.md#numbers-and-staleness) |

### Migrating to 1.0.0

Do this as one reviewed deliverable in the consuming project, on its own branch.
Run the commands with the project's documentation interpreter, written `python`
below: the Python environment that has `.docs-kit/requirements.txt` installed.
The [4.0.0 guide](migrations/4.0.0.md#move-the-pin) says how to find or create
it.

1. **Record where you start.** Note the current pin (`git -C .docs-kit rev-parse HEAD`)
   and keep a build of the current site for comparison:

   ```bash
   python .docs-kit/docsite.py build --project .
   (cd .build/docs && find . -name '*.html' -type f | sort | xargs sha256sum) > /tmp/docs-before.txt
   ```

2. **Move the pin.**

   ```bash
   git -C .docs-kit fetch --tags
   git -C .docs-kit checkout v1.0.0
   python -m pip install -r .docs-kit/requirements.txt
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
   python .docs-kit/docsite.py build --project .
   python .docs-kit/docsite.py build --project . --check
   python .docs-kit/docsite.py lint --project . --strict
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
changes, from pins 37ac1dc and 80b42f4; [the receipt](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/v1.0.0-consumers.json)
records inputs, commands and results. No consumer pinned at v0.1.0 was available
to test. Each consumer still adopts 1.0.0 through its own reviewed change.
