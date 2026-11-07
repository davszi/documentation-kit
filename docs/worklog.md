# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

## 2026-11-07 — Read the kit site in the shared chapter reader

- The kit site had `chapter_reader = false` and `reader = false` on every page,
  so it showed none of the kit's reader: chapter cards, One / Two / All
  chapters, pinning and reading layers. The site now enables the reader, every
  registered page sets `reader = true`, and only the home page stays
  reader-free. `nested_nav` is off so the home sidebar shows the same tree as
  the reader pages.
- The reader keeps text before the first `##` as its own chapter, which left a
  nearly empty Introduction card on every guide. Registered pages now merge a
  short opening and the source line into the first chapter; the three
  overview pages moved their lead sentence under their first heading.
- The site review now checks reader chapters on every page, the merged
  opening, the two-chapter view and the reader's narrow menu, replacing the
  folded-navigation browser check (the unit tests still cover `nested_nav`).
- The `reference-page` line-length cap (`.content>*{max-width:1040px}`) also
  capped the reader stage, leaving the right third of a 1600 px screen blank.
  The cap now applies only to pages without the reader; the site review fails
  if the active chapter card is narrower than 80% of the content area.

## 2026-11-07 — Build the kit site's own pages from kit components

- The home, getting-started, practices and site-toolkit pages used a private
  component set (`kit-site.css`: path cards, guide cards, numbered steps and a
  hand-drawn source diagram) instead of the kit's own Markdown and shared
  `home.css`/`build-sheet.css` blocks. The pages are now Markdown with shared
  blocks only: `home-hero`, `now-card`, `bs-flow`, `bs-grid` and Markdown
  tables in the router's `Before… | Read…` shape. `kit-site.css` is removed and
  the home page is no longer `raw`.
- The home page now shows how a project uses the kit in three steps (pin, add
  `AGENTS.md` rows, read before acting) and a literal router snippet. Examples
  use the evidence, experiment and handoff guides instead of the Git guide.
- Markdown tables on `reference-page` entry pages get the same narrow-screen
  scroll region as registered source pages.

## 2026-11-07 — Make folded navigation keep its state

- Opening a group and then following a link in another group closed the
  first group, because only the current page's group is open in the served
  page. `nav.js` now remembers groups the reader opened (browser storage,
  saved when a group header is clicked; groups the served page opens are not
  stored) and scrolls the sidebar to the current entry. Group headers use
  sentence-case text instead of uppercase monospace, page counts are removed,
  and groups open and close with a short `::details-content` transition that
  respects reduced motion.
- A Chromium check opens a group, follows a link in another group, confirms
  both stay open, closes one and confirms it stays closed on the next page.

## 2026-11-07 — Fold the kit site's navigation

- The kit site's flat sidebar listed about 37 entries, put the current page's
  sections at the top far from its entry and repeated "Overview" twice. Add the
  optional `nested_nav = true`: navigation groups fold into native disclosures
  with page counts, the current page's group opens and its sections sit under
  its entry. Pages with the chapter reader and sites without the key keep the
  flat tree. The four orientation pages now share a "start here" group.
- Three new tests cover nesting, the flat default and key validation (102
  Python tests). Wide and narrow sidebar captures were inspected.

## 2026-11-07 — Classify experiments by what they decide

- Replace the field-based reading of the experiment guides with two kinds,
  decided by the result: investigation (exploratory or confirmatory) and
  qualification (verdict on a named system against a bar fixed before the run).
  A first section, "Keep experiments small", limits scope and process before
  any other rule. Final runs and other learned-model practices stay in the kit
  in one section scoped to learned or fitted models.
- Restore the mandatory required content softened in `d072852`: every
  experiment states question, measured motivation, kind, decision, baseline,
  budget and stopping condition; confirmatory investigations and
  qualifications fix their bar first and report a verdict. The strongest
  relevant baseline applies to all kinds. Numerical verification applies
  whenever results depend on custom numerical code; regression gates and quick
  modes are no longer tied to one field. "Qualification" in other senses is
  reworded (`evidence.md`, `pages.md`, `site/validation.md`).
- An independent review found eleven issues in the first rewrite (dropped
  rules, model-only narrowing of data checks, a floor that read as optional,
  length) and a re-check found three more; all are fixed. The two guides total
  1125 words against 1126 before, and the required-content list left
  `writing/evidence.md`. `tests/run_checks.sh` passes (99 tests, strict lint
  clean for starter and kit site).

## 2026-11-07 — Merge experiment guides and publish them on the site

- Merge `experiment-workflow-guides-20261107` (`d072852`) into `main` beside
  the website commits. Git merges README, project context, reading index and
  documentation policy automatically; the worklog conflict keeps both entries
  unchanged.
- Register `rules/experiments/workflow.md` and `verification.md` as source
  pages in a new Experiments navigation group (35 pages), add them to the
  practices overview and home path, and list them in the unreleased notes.

## 2026-11-07 — Build the kit's reference website

- Add registered source pages: `[[source_pages]]` in `site.toml` renders an
  existing tracked Markdown file whole at a chosen route. Links and media
  resolve from the file's folder; registered targets become routes, other
  files become source links and tracked media are packaged. The page names its
  canonical source with an edit link, which keeps the configured branch when
  `GITHUB_SHA` pins source links. Registry, containment, route-collision,
  missing-target and fragment errors fail the build; lint checks registered
  files' Markdown links. Implementation: `tooling/source_pages.py`, with
  `build.py` sharing its page assembly through `finish_page`.
- Build the kit's own site from the repository root: 33 pages, four of them new
  orientation pages (home, get started, site toolkit, project practices); the
  rest render the README, `rules/`, release notes, the 1.1.0 migration guide,
  the panel-switcher contract and the kit's context, index and extraction
  records in place. The writing and maintenance routers are hidden pages that
  keep their anchors. The [website record](topics/website/website.md) owns the
  structure and the open hosting decision; nothing is deployed.
- Checks, run with Python 3.12.3 and Node 22.23.3: `tests/run_checks.sh`
  passes, including 99 Python tests (86 existing, 13 new registration tests),
  strict lint with zero warnings for both the starter and the kit site, and
  both Node checks. Real Chromium (Playwright 1.62.1, browser build 1234) passes the existing
  visual review, browser-helper and panel-switcher fixtures, and the new
  `tests/own_site_review.cjs`: all 33 pages contained with visible media at
  1600 × 1000 and 390 × 844, deep links, panel hash reveal, keyboard path
  focus, narrow menu and table scrolling, print and no-JavaScript reading.
  Saved wide and narrow screenshots were inspected; path text inside condensed
  capitals and figure margins were corrected after the first inspection.
- Compatibility: a starter copy built with v1.1.0 and with this revision
  differs only in `assets/base.css` (additive rules) and `site-build.json`
  (new `source_pages` key and asset hash); every HTML page is byte-identical.
  The consuming ADP checkout's non-writing `build --check` reports no errors
  with either kit; the new kit adds only `assets/base.css` to its stale list.

## 2026-11-07 — Scope shared experiment workflow and verification

- Add shared experiment workflow and proportionate verification guides.
  Distinguish investigations from final artifact/model runs and exploration from
  confirmation. Keep local decisions and existing execution contracts with
  consumers; add no automatic audit tier or approval framework.
- Move production benchmark and engineering quick-mode guidance to performance.
  Preserve independent numerical reference/derivation, production comparison,
  self-check, optional native comparison and fast regression guidance under
  numerical implementation correctness. Retain evidence provenance, actual
  reviews, failed outcomes, visuals and existing public anchors.
- Route root/starter agents and reading indexes to the canonical guides. Update
  current extraction ownership without changing frozen provenance, historical
  release records or `VERSION`. This remains unreleased local work; the landing
  commit supplies its identity.
- Address policy review by scoping fixed pre-results criteria to confirmation
  and agreed acceptance checks. Allow labelled exploratory interpretation with
  retained changes and reasons. Keep the selected recipe fixed during a final
  run; record a recipe change as a distinct attempt. Independent re-review
  found no remaining findings in that scope.
- With `/home/deivid/dev/.venvs/adaptation-slide-faces-docs/bin/python`, starter
  build, freshness and strict lint pass with zero warnings. Focused Markdown
  link/fragment and existing-anchor checks pass. No rendered source, theme or
  tooling changed; no browser or application-runtime checks were run.

## 2026-11-07 — Integrate upstream releases and slide support

- Merge origin `072b063e6dbb` into local kit `4ab0bd10ce82`. Preserve focused
  engineering, writing and site guides and the strict QA snapshot-origin hook.
  Move upstream release, include, navigation, figure and slide contracts into
  their focused owners; retain both old and new router anchors and original
  dated worklog entries. Correct the moved context's release-record link.
- Package the compatible local changes as 1.1.0 with release notes and a focused
  consumer migration guide. Cover all four local policy/adapter commits absent
  origin, preserve the original 1.0.0 notes and receipt, and leave consumer
  adoption evidence with its owner. Version tagging remains a separate step.
- The integrated implementation passes strict starter lint with zero warnings,
  all 86 Python tests, reader preservation and both Node checks. Browser checks
  pass at 1600 × 1000 and 390 × 844, including seven guide chapters, navigation,
  paired columns, helpers, panel switching and no-JavaScript reading. Update the
  browser fixture's exact chapter count from six to seven for the upstream-added
  slide chapter. Focused slide/deck checks cover fit, Continue/Back, presentation
  keys, print and narrow no-JavaScript stacking. Inspect saved wide, narrow,
  paired and deck screenshots; no overflow or collision issue remains.
- Preserve all attempts under the consuming ADP checkout's ignored
  `.build/coordination/docs-final-20261107/kit-origin/`. Attempt 01 passes the
  suite in 6.830 s with a terminal owned peak of 75,419,648 bytes. Attempt 02
  stops Chromium after it leaves the capped scope; its peak is unmeasured.
  Attempt 03 keeps headless Chromium contained by setting a per-job D-Bus
  address to a nonexistent socket; the guard remains unchanged. Its checked-in
  fixtures and wide/narrow slide/deck phases pass, but the supplementary
  no-JavaScript phase incorrectly calls an animation-frame settle helper and
  fails. Attempt 04 runs only that corrected phase and passes. Attempts 03/04
  record peaks of 577,044,480 / 356,950,016 bytes. Every attempt retains the
  command, source identity and cleanup receipt; owned-process absence is
  verified under a 4 GiB/zero-swap scope, 180 s worker deadline and 10 s cleanup
  reserve, with a 220 s outside deadline. No simulator or deployment is checked.
- Final document checks pass on 14 changed kit Markdown files, 185 local links
  and 87 Markdown fragments. Both parents' router anchors, all 21 checked
  historical worklog entries and the original 1.0.0 notes/receipt are preserved.
  Hash comparisons confirm 124 tested implementation/fixture inputs remain
  unchanged. Attempt 05 identifies only stale generated version metadata;
  attempt 06 selects the system Python by resolving the virtualenv symlink and
  fails before building because Mistune is absent there. Attempt 07 uses the
  requested virtualenv path, refreshes `site-build.json` and passes freshness;
  every rendered page and asset remains byte-identical to browser-reviewed
  output. All seven attempts verify owned-process absence. No unchanged suite
  or browser phase is repeated for release prose/version-only edits. The
  landing supplies the merge commit identity; consumer adoption and tagging
  remain separate.

## 2026-11-07 — Final local kit suite after QA-provenance changes

- Rerun the complete `tests/run_checks.sh` on the QA-provenance hook and its
  regression tests with Python 3.12.3 and Node 22.22.3. Starter build is current;
  strict lint has zero warnings; all 54 Python tests pass in 2.961 s. Reader
  preservation and both Node math/source-link checks pass.
- Attempt 04 retains its exact command, changed-source hashes, environment and
  diff under the consuming ADP checkout's ignored
  `.build/coordination/docs-final-20261107/kit-local/attempt-04/`. The 4 GiB
  zero-swap scope uses a 180 s worker deadline, 10 s cleanup reserve and 220 s
  outside deadline. Terminal owned peak is 72,253,440 bytes; elapsed time is
  5.742 s; owned-process absence is verified. Earlier attempts remain retained.
- No intentional rendered layout changed, and browser pixel inspection was not
  run. This validates the recorded local source, not deployment or later origin
  integration. The landing commit supplies its identity.

## 2026-11-07 — Local restructure regression validation

- Run the complete `tests/run_checks.sh` suite with Python 3.12.3 and Node
  22.22.3. Starter build is current; strict lint has zero warnings; all 52 Python
  tests pass in 2.999 s. Reader preservation, vendored math integration and
  source-file links pass, including text/code/media/anchor/figure identities.
- Fix the existing alternate-worklog fixture to update both project context and
  the new reading index after explicitly moving its worklog. Keep strict
  dead-link detection and the original acceptance requirement unchanged.
- Preserve the first attempt's systemd setup failure (suite not started) and
  the second attempt's stale fixture-link failure. The third attempt passes
  under a 4 GiB zero-swap scope, 180 s worker deadline and 10 s cleanup reserve;
  its outside deadline is 220 s. Terminal owned peak is 68,677,632 bytes, elapsed
  time is 5.703 s, and owned-process absence is verified.
- Exact commands, source/environment identities, diffs, failed attempts and
  receipts remain in the consuming ADP checkout's ignored
  `.build/coordination/docs-final-20261107/kit-local/`. No intentional rendered
  layout changed; browser pixel inspection was not run. This is a local suite
  result, not a hosted deployment check. The landing commit assigns identity.

## 2026-11-07 — Focused engineering and documentation guides

- Add portable [code practices](../rules/engineering/code.md),
  [efficiency rules](../rules/engineering/performance.md) and
  [execution/resource guidance](../rules/engineering/execution.md). Keep
  project-specific tools, workloads, profiles and acceptance requirements local.
- Move the existing writing and site contracts into focused `rules/writing/`
  and `rules/site/` guides. Keep the original entrypoints and section anchors as
  short routers; preserve their clauses and rebase moved relative links.
- Move kit and starter orientation to `docs/PROJECT_CONTEXT.md`, add
  `docs/index.md` reading indexes, update canonical destinations and action
  routes, and keep both worklogs at `docs/worklog.md`. Claude entrypoints import
  only `AGENTS.md`. README now routes engineering, writing and site work.
- Consolidate repeated execution, performance, evidence, figure-provenance,
  review and local-media rules into their owning guides, with links from
  callers. Preserve unique context and the figure output-hash requirement.
- Focused checks passed on 31 changed kit and 38 ADP Markdown files with no
  errors or warnings. Old anchors, moved manifest bytes and the ADP worklog
  were preserved. The earlier 17 path-compatibility tests passed in 0.545 s.
  Independent source review found no consequential requirement lost in the
  overlap consolidation. Full site and rendered checks remain deferred.
  Changes are uncommitted; the landing commit will assign their identity.

## 2026-11-07 — Shared delivery and handoff policy

- Add the [approved delivery guide](../rules/engineering/delivery.md) for
  assignment scope, owner responsibility, coordination, parallel work and
  escalation, and the [handoff guide](../rules/engineering/handoffs.md) for
  completion, blockers, durable evidence and receiving work. Add action routes
  for kit contributors and starter projects.
  Validation is deferred to the agreed documentation batch.

## 2026-11-07 — Shared Git practices

- Add the [Git guide](../rules/engineering/git.md) for coherent commits,
  applicable validation, preservation of unrelated changes and staging safety.
  Require an explanatory body after the short imperative subject. Preserve
  repository-owned commands, acceptance gates and publication permissions.
- Route kit contributors and new starter projects to the guide before Git
  actions. Starter build and strict lint, 52 Python tests, both Node 22 checks,
  focused policy links and both client routes passed. Correct the route-check
  harness's initial assumption that the starter Claude file had no heading.
  Independent Sol High review is clear after fixing Claude's route and
  clarifying preservation of staged intent during isolated-index landing.
  This landing supplies the commit identity.

## 2026-11-06 — Version 1.0.0

- Declare the first stable version: `VERSION` 1.0.0 and a
  [releases record](topics/releases/releases.md) with the 1.0.0 contents and the
  consumer migration steps. Knowledge gathered while redesigning the adaptation
  readers moves upstream.
- Fix: included fragments may include others (eight levels; cycles fail). The
  figure-reference lint resolves nested includes the same way.
- Fix: a `[[nav]]` entry with keys other than `label`, `file`, `group`, `short`
  and `hidden` fails the build with a hint. A top-level `extra_components` written
  below a nav table had silently become a nav key and surfaced only as an
  "unknown component" error.
- Fix: site-map cards take frontmatter `description` and `thumbnail` when present
  (the maintenance rule claimed a description and a first-figure thumbnail, while
  the code read `brand_sub` and found only `<img>`, never inline SVG figures).
- Add `tooling/svg_figures.py` (figure, slide and standalone SVG markup with a
  literal palette; the region label no longer double-escapes apostrophes),
  `tooling/number_ledger.py` (every shown number has a checked source),
  `tooling/verbatim_blocks.py` (hash locks for kept blocks) and the browser helper
  `captureElement`. Rules add the shared-navigation homepage pattern, literal
  colours for generated SVG and ledger use for redesigns.
- Compatibility: both known consumers build with this tree without source
  changes. Against their current pins, every page is byte-identical except each
  home page, whose site-map thumbnails are now marked decorative (ADP 87 of 88,
  adaptation 7 of 8; [receipt](../verification/v1.0.0-consumers.json)).
- One independent review (Opus, high effort) found no blocking defect; fixes
  landed here: ledger semantics and trust boundary stated (distinct unsigned
  values, expressions are reviewed code, not a sandbox), kept-block edges reported
  instead of raised, an explicit stable/provisional surface in the release notes,
  decorative and local-only thumbnails, typed `[[nav]]` validation, include errors
  that name the chain (a missing fragment no longer ends in a traceback),
  `standalone`/`slide_svg` edge cases, and release-note accuracy.
- Checks: starter build, strict lint, the Python suite (new site-contract and
  figure-tooling tests), math and file-link JavaScript checks, browser-helper
  regression. The landing commit supplies the revision.

## 2026-11-06 — Task-triggered agent reading

- Define one [repository router](../rules/documentation.md#agent-entrypoints-import-versus-point)
  for orientation, prerequisites and action-specific reads. Update the starter
  so Codex and Claude use the same task routes and apply every matching rule
  before its action.
- Starter build, strict lint, 52 Python tests and both Node 22 checks passed.
  A fresh initializer smoke check verified the generated router, its three
  shared policy paths and Claude's single import. This landing supplies the
  commit identity.

## 2026-11-06 — Visual ordering and evidence presentation

- Clarify the [page lead](../rules/writing.md#page-design),
  [scope notes](../rules/writing.md#story-and-reading-layers) and
  [choice of representation](../rules/writing.md#figures-and-comparisons).
  Put the figure early in mechanism and geometry explanations. Keep brief
  qualifications beside the relevant evidence and the full rationale in its
  record. Use diagrams for relationships and tables for precise comparisons.
- The starter build, strict lint, 52 Python tests and both Node 22 checks
  passed. Checked the final policy text for preserved headings, its new
  internal link and whitespace. This landing supplies the commit identity.

## 2026-11-05 — Slide faces and extracted decks

- Add optional chapter slide faces: `<!-- slide -->` blocks become a fixed 16:9
  canvas at the top of a chapter, sized entirely in container units so fit is
  identical at every width; below 720 px faces stack. The reader adds a bridge
  (reading time, figure count, Continue/Back control), keeps a duplicated eyebrow
  for assistive technology only and gives faced chapters sentence-case headings.
  Canvas declarations are `!important`, because a consumer's id-scoped `p` rule
  shrank slide titles from 34.6 to 15 px. The narrow layout is a CSS container
  query, so it needs no JavaScript; print
  keeps the slide palette. Flat Markdown pages start a chapter at a face written
  before its heading; code examples of the markers stay literal.
  The [writing rules](../rules/writing.md#slide-faces) own content guidance; the
  [maintenance contract](../rules/maintenance.md#slide-faces-and-decks) owns
  markers, vocabulary and the `slides` command, which writes presentable and
  printable decks to `.build/slides/` outside the published bundle. Decks prefix
  slide ids, re-root all relative URLs, link other anchors back to their page,
  render KaTeX and accept pages without the reader (outermost section cards).
- Add an `is-alert` tone for failures and warnings, so the accent and warm tones
  can identify compared methods only (found by the consumer's slide review).
- Widen One chapter cards from 80% to 88% of the stage. Derived from a reviewed
  prototype on the adaptation Cursor reader; the starter guide carries two faces.
- One independent review (Opus, high effort) found placement, scrolling,
  no-JavaScript, print, URL and keyboard defects; all fourteen are addressed.
- Checks: starter build, strict lint (0 warnings), Python suite including
  14 slide tests, math and file-link JavaScript checks. Browser-pane
  inspection at 1600×1000 and 375×812: faces fit 16:9, compact stacking without
  horizontal overflow, bridge and Continue/Back scrolling, deck overview and
  presentation mode. Playwright fixtures were not run (Playwright unavailable).
  This landing supplies the commit identity.

## 2026-11-04 — Shared publication and browser checks

- Extract the optional existing-site exporter and common browser checks from
  adaptation. Projects retain publication admission, stable URLs, historical
  packaging, credentials and scientific assertions. The
  [maintenance contracts](../rules/maintenance.md#exporting-into-an-existing-publication)
  own both APIs. Homepage composition stays project-owned; the starter is an
  optional example, as recorded in the [writing rules](../rules/writing.md#project-owned-homepages).
- Preserve embedded JavaScript/JSON and unrelated HTML bytes. Align source-span
  offsets with HTMLParser's LF counting and cover literal Unicode/control
  separators plus mixed mapped/unmapped routes. Browser checks retain real
  clipping/visibility rules and report impossible short-reader cases as skipped.
- Strict starter lint has zero warnings; all 52 Python checks, JavaScript checks,
  real browser failure fixtures and desktop/phone reader checks pass. Independent
  source review findings are resolved. [Receipts](../verification/publication-browser.json)
  retain tested inputs and bounded resources under the shared lock. Consumer
  adoption and public-bundle comparison remain project-owned. This landing
  supplies the commit identity.

## 2026-11-04 — Generated-content compatibility

- Support a tracked project `content_transform` for importing scientific or
  sealed reader content into the shared presentation. Revalidate derived
  metadata; preserve source-declared slugs and page CSS. Allow validated scoped
  `body_class` values and existing canonical worklog paths. The
  [maintenance contract](../rules/maintenance.md) owns these extension points.
- Strict starter build/lint, all 31 Python checks, math/source-link JavaScript
  checks and desktop/phone reader browser checks pass. [Receipts](../verification/content-imports.json)
  record tested inputs and resources under the shared lock in an owned
  4 GiB/zero-swap scope. Consumer scientific-preservation checks remain
  project-owned. This landing supplies the commit identity.

## 2026-11-04 — Shared reader includes

- Resolve matching shared-template includes from the kit before looking for
  project fragments. Existing `components/chapter-reader.html` markers keep
  their behavior without a duplicate consumer toolbar file. Relative/contained
  include paths remain required.
- Strict build/lint, all 27 Python checks, JavaScript math/source-link checks
  and desktop/phone reader browser checks pass under the shared lock and an
  owned 4 GiB/zero-swap scope. [Receipts](../verification/shared-includes.json)
  retain tested inputs and output. This landing supplies the commit identity.

## 2026-11-04 — Consumer compatibility adapters

- Add explicit tracked/contained project path and evidence adapters, keeping
  consumer historical identities and schema policy out of the shared engine.
  Declare project-only dynamic dependencies through `extra_assets`; reject
  shared-asset collisions and noncanonical/escaping target paths. The
  [maintenance contract](../rules/maintenance.md) owns configuration and API.
- Strict starter build/lint, all 26 Python checks, math/source-link JavaScript
  checks and existing desktop/phone reader browser checks pass. [Receipts](../verification/project-extensions.json)
  retain inputs, output and the owned 4 GiB/zero-swap scope under the shared
  lock. No application runtime was launched. This landing supplies the commit
  identity; consumer adoption and its content validation remain project-owned.

## 2026-11-04 — Shared local comparison controls

- Extract the reusable width-lesson interaction as `panel-switcher`, with neutral
  authoring attributes and shared control CSS. Track scenarios, figures, legends
  and specialized layouts stay project-owned; ADP's original compatibility copy
  remains until its kit adoption. The [component contract](topics/panel-switcher/panel-switcher.md)
  owns usage and behavior; [origin identities](../verification/panel-switcher-origin.json)
  preserve the exact producing source. After attribute renaming, executable
  behavior matches the original source.
- Verify original/shared defaults, independent groups, buttons/keyboard, deep
  links, print restoration and fallback reading at desktop/phone widths. Strict
  build/lint reports zero warnings, all 22 Python tests pass, both JavaScript
  checks and the existing reader browser regression pass. [Receipts](../verification/panel-switcher-checks.json)
  retain the complete run and screenshots. Checks held the shared lock in an
  owned 4 GiB/zero-swap scope; no simulator was launched. The first invocation
  timed out, its owned scope was stopped, and the corrected browser harness
  passed in a complete rerun. This entry's landing commit supplies its identity.

## 2026-11-04

- Extract the reusable documentation kit from inspected source `9930b919`:
  portable policies, shared chapter/home layouts, generic toolchain and a neutral
  starter. The user selected a pinned dependency suitable for a Git submodule.
  [Extraction evidence](topics/extraction/extraction.md) records source hashes,
  independent review and the passing build/lint, 21 Python tests, JavaScript
  checks and desktop/phone browser review. No simulator or source-project
  migration was performed. This initial commit owns the coherent deliverable.
