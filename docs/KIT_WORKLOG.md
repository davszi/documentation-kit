# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

## 2026-11-26 — Release 5.7.0

- deivid gave the go: "Yes, release 5.7.0". The ask named what the go
  covers: moving `main` to the release commit, the tag `v5.7.0` and the
  push, which publishes the kit's own site with the new reader. It gave the
  size against 5.6.1 at `011b0a2`: 56 files, 3,233 lines added, 643
  removed, and the result of the full check script there: exit 0, 501
  tests.
- The message with the ask named what is not verified: the commits that fix
  the review findings not reviewed again; no real phone, Firefox or Safari;
  the swipe exemptions and pinch zoom not run in a browser; the palette's
  author not having seen the change to its series check.
- 5.7.0 holds the changes of the entries below, down to the two on 5.6.2.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-26 — Review of 5.7.0: not fit to tag, then fixed

- One independent review read the whole branch against `v5.6.1`, with no
  browser, and ran builds and tests in a scratch clone. The full check
  script had passed on `68684d1`: exit 0, 500 tests. Its verdict: not fit
  to tag, for one finding in the figure-series check.
- Fixed, medium, the blocker: the series check compared only neighbours in
  the series order. An amber accent built although it was 4.7 from the warm
  series, and a blue equal to the accent passed with no problem named.
  Adding the check after the release would make a passing build fail,
  which the version promise allows only in a major release. Any two series
  that are not neighbours must now be 10 apart; the kit's palettes pass,
  their closest pair is 12.7.
- Fixed, low: two series with one colour were named by the wrong place.
- Kept, medium, and now stated: the site's `accent` is always the first
  figure series, so a light accent outside the band is refused on a project
  without generated figures too. The build's message says that the series
  check failed, and the release note says that accent is held to the band.
  Relaxing it later is a patch.
- Fixed, low, on the reader's side, in the commit before: a dead All switch
  on a page without the reader whose folds have no known kind; a rule
  sentence on the chapter strip; the release note's sentence on swipe.
- Not fixed: the test for properties that the kit does not define scans
  stylesheets only, not scripts.
- The palette session could not be reached at its address after a restart
  of the app, so the kit owner's session made the palette fix itself.
- Confirmed by the review: no palette edit was lost in the join; a project
  that built on `v5.6.1` builds and passes strict lint, and its pages differ
  only in `<title>` and the `?v=` queries; no stable interface is removed.

## 2026-11-26 — 5.7.0 on one branch: the new reader joined with the site colours

- One release, by deivid's decisions in order. On the id fix: "well maybe
  make it one relase not 2". On the order of reader and palette: "Palette
  first". On releasing the id fix alone before both: "No, keep it with the
  reader". On one release for palette and reader, owned by the kit owner's
  session: "Yes, combine here". There is no 5.6.2 tag; its two entries below
  describe the id fix that ships here.
- The reader. deivid compared adaptation's home page with a chapter and
  found the chapter's frame too busy. Four prototypes, laid over a built
  page as styles, then a fifth from his choices, which he tried in a local
  copy and changed step by step: views into the sidebar, the stepper as a
  floating island, the Full chapter row on its line, the chapter's name as
  headline, narrower and smaller neighbours with fitted click zones, swipe,
  and the section options back as one set for the page at the bottom of the
  sidebar, without "Story". "Yes, build 5.7.0."
- Built by one implementer agent in three commits, with tests, from a
  written brief and the prototype. An independent review, with no browser,
  found it not fit to release: hidden click zones that still took clicks in
  All chapters and on the first and last chapter, folds that closed again
  on return, keyboard focus under the fade, swipes that fired on sliders,
  and four smaller points. The implementer confirmed each in a browser and
  fixed all in one commit with tests.
- Joined. The palette session handed over branch `site-palette` at
  `9584cb3` and stopped writing. The reader's eight commits were replayed
  on it as branch `release-5.7.0`. Conflicts: three blocks in
  `chapter-reader.css`, where the reader's structure and the palette's
  colour were both kept, and the two records.
- The reader's new parts and the bar of `fold-controls.js` read the theme
  properties, and the three reader scripts are no longer exempt from the
  script colour test. Without a table, a capture of a chapter before and
  after differs by at most 2 of 255 in the island and the options panel,
  where the nearest existing property was taken; nothing else differs. With
  the brown palette of the first project, the reader's parts are brown.
- Closed and removed: `docs/open/reader-release-colour-follow-ups.md` with
  its route. Both of its items are done; the four fold hues are named as
  kept in the authoring guide. The link to it in the entry of the review
  fixes below is now plain text.
- Rules: the reader rules describe the new reader, the explanation rules
  the `(open)` word, and the home page is said to have the reader off.
- Not checked: a real phone; swipe exemptions and pinch zoom in a browser;
  the fold bar of a page without the reader under a project's colours.
- Not pushed and not tagged. Release waits for deivid's go.

## 2026-11-26 — `accent` colours the first figure series

- deivid decided against separate interface and content colours: `accent`
  stays the first series, so `HUE_KEYS` now maps all five hues.
- The kit's own hues on the brown surfaces, with only surface and text keys
  set, pass every figure check: neighbours at least 13.1 apart with any
  deficiency (violet and warm, tritanopia), the alert 11.2 from warm, marks
  at least 5.47:1 on the figure panel. The site's text checks fail one pair:
  the kit's red #f47067 on the brown panel2, 4.15:1; with `red = "#ff7b72"`
  every check passes.

## 2026-11-26 — Figure series follow `[theme_colors]`, checked as a categorical palette

- deivid asked that the content colour map follow the project palette too.
  `figure_themes.project_dark` now takes violet, warm and blue and the alert
  from `secondary`, `orange`, `blue` and `red` when the table sets them. The
  first series, accent, is held: deivid is deciding whether interface and
  content colours get separate keys, so `HUE_KEYS` leaves it out and gains
  one entry when that is decided.
- `figure_themes.problems` adds the series checks of the dataviz method:
  OKLCH lightness band and chroma floor, neighbours 15 apart (OKLab x100)
  with full vision and 8 with protanopia, deuteranopia and tritanopia
  (Machado 2009, severity 1.0), and the alert 10 apart from every series.
  Two deviations keep the kit's own palettes passing, both measured: the
  dark band ends at 0.80, not the method's 0.70, because the kit's dark
  hues reach 0.799 (warm); the alert has no colour-deficiency floor, because
  the kit's light alert and warm are 3.4 apart with deuteranopia and its
  dark ones 7.8.
- New text pairs: `accent` and `red` on `panel2` (step numbers, build-sheet
  chips). With the project's proposed hues two pairs fail and are reported,
  not loosened: `secondary` #b180d4 on panel 4.41:1 and `accent` #56ae6c on
  panel2 4.33:1. The kit's red #f47067 is 4.15:1 on the brown panel2, so the
  test palette sets red #ff7b72.
- The theme's content hues already follow the keys: `--accent`,
  `--secondary`, `--blue`, `--orange`, `--red`, `--green` and every build-sheet
  tone (`.bs-violet` through the second group tone). Still literal: the
  tinted diagram box edges `#2f7f76`, `#7c5cad`, `#a35d5d`, syntax colours
  and fold hues.
- A four-series chart drawn with `write_both` on the brown palette puts the
  kit's teal accent, the project's lilac, ochre and blue and the red alert on
  the brown background; the light file is unchanged.

## 2026-11-26 — Review fixes for `[theme_colors]` and tab titles; lock pages keep "Locked page"

- An independent review of branch `site-palette` said "ready after fixes".
  Fixed: the release note no longer says no default changes, since tab
  titles change on every site with `title`, and it warns projects whose
  browser checks read the title; it names the fold-control bar as still
  navy and lists the five scripts whose bytes change; the guide says that
  setting a key recomputes its derived colours even at the kit's value
  (`accent = "#39d2c0"` moves the first group tone to `#74e0d3`), that a
  project's own literal colours stay as written, and that the fourth group
  tone is `blue` itself.
- The build names every bad `[theme_colors]` key in one error instead of
  stopping at the first; code comments (`faint` on `bg2`) join the contrast
  pairs; a failing ratio is cut, not rounded, so 4.497 shows as 4.49.
- deivid decided that a lock page reveals nothing, not even the site's
  title: lock pages and `404.html` keep "Locked page". The site title is no
  longer passed to the lock, `page_lock.py`, `publication.py`,
  `page-lock.html` and two tests are back to their state before the tab
  titles, and a test checks that no lock page holds the site's title.
- New open work: two theme-colour follow-ups for the reader release (closed, and the record removed, in the 5.7.0 entry at the top),
  the fold controls and the redone colour commit of `chapter-reader.css`.

## 2026-11-26 — Scripts and group tones follow `[theme_colors]`

- Asked by the coordinator before the independent review: the owner wants
  the whole site in the project's palette, so the colours that scripts
  inject and the default group tones follow the table too.
- `lightbox.js`, `carousel.js`, `plot-toggles.js`, `page-lock.js` and
  `nav.js` now write `var(--name, <kit value>)`, with eleven new derived
  colours. `nav.js` gives a group without a colour `var(--group-tone-N)`;
  the six tones, the reader's chapter parts and the sidebar's mint and
  violet glows are lighter steps of the hue colours.
- Left literal: `fold-controls.js`, reserved for the reader branch, with its
  fold hues and its bar of see-through greys; the fold and layer hues in
  `chapter-reader.css`; syntax colours; the tinted diagram box edges; the
  light backdrop of site-map pictures.
- The `chapter-reader.css` part of this change was folded into its own
  earlier commit, so that file still changes in one commit; that rewrote the
  three unpushed commits after it.

## 2026-11-26 — Browser tabs name the site first

- deivid added it to the same release through the coordinator: tab titles
  with the project's name first, the in-page titles unchanged.
- Choices the request left open: the home page shows the site's `title`
  alone, because its `[[nav]]` label (often "Home" or "Overview") would only
  repeat that it is the start; a site without `title` keeps today's tab
  titles instead of a made-up "Documentation". A `[[nav]]` entry always has
  a label, so the `short` value the request named second is never reached.
- The shell's `<title>` reads a new `{{TAB_TITLE}}`; `{{TITLE}}` stays for
  the top bar. The lock page takes the site's title from `publish` through
  `prepare_lock`, never from the page it locks.
- Tests: `tests/test_tab_titles.py`; the expectations in five test files
  that quoted a page's `<title>` now quote the tab title or the top bar.

## 2026-11-26 — A project's own site colours: `[theme_colors]`

- Asked for by the embodied-safety-gates project through the coordinator: its
  whole site in a warm dark brown instead of the kit's navy. Built on branch
  `site-palette` for the next release, which has no number yet.
- Two commits before this one move every navy and grey literal of the theme
  CSS to custom properties on `:root`; `chapter-reader.css` has a commit of
  its own so that the reader branch can redo it on its restructured file.
  Colours used see-through read `--<name>-rgb` channels in `rgba()`: a first
  try with `color-mix()` moved gradients to Oklab and differed from the old
  pages by up to 5 of 255 in a channel, and by 1 after forcing sRGB.
- Default look unchanged, checked two ways: screenshots of the page-lock
  fixture's reader, reader-free, record, listed, Reference index, home and
  lock pages at 1600 and 390 px, viewport and full page, are pixel-identical
  to `origin/main`; resolving every `:root` property in the old and new
  stylesheets gives the same text for all eight files. Diagrams and slide
  faces read copies of base colours that the reader's print style does not
  turn light, as their literals did.
- This commit adds `tooling/theme_colors.py`, the stylesheet and its links,
  the contrast checks, the dark figure palette on the project's colours,
  `tests/test_theme_colors.py`, the guide section and the release note. The
  tests of the touched files pass, and the kit's own site builds and lints
  strictly clean; the full check script runs on the final commit.
## 2026-11-26 — Review of 5.6.2: fit to tag, four low points

- One independent review read the commit on `v5.6.1`, read-only, and ran
  the old and the new function side by side in a scratch clone. Its
  verdict: fit to tag. The full check script had passed on the same
  commit: exit 0, 454 tests.
- Its evidence: on 1,092 SVG files of local projects, grouped into 137
  pages of 8 figures, the reader path gave byte-identical output; without
  the reader 112 pages repeated ids before and none after, and every
  reference stayed inside its own figure.
- Fixed, low: a rule of a figure's own `<style>` that selects a renamed id
  now follows it; only a selector is rewritten, never a colour.
- Fixed, low: a toggle group whose id has no `--` keeps its `tg-<group>`
  start when renamed.
- Fixed, low: a new name that is itself taken gets a counter.
- Corrected, low: the release note named "the references" without saying
  which forms, and said lint no longer warns without the limits. The entry
  below overstated two points; both are corrected in place.
- These fixes were not reviewed again. Each has a test or a direct run.

## 2026-11-26 — 5.6.2 built on a branch: inlined figures repeat no id

- 5.6.1 is released: tag `v5.6.1` on `b176311`, pushed with `main`. The
  Pages workflow passed, and the live site serves the retaken pictures.
- deivid pasted a finding from the ADP session: its home page repeats 242
  ids, because `tooling/build.py` makes the ids of inlined SVG figures
  unique on chapter-reader pages only, and the lint check of 5.5.0 then
  flags them. Checked in the code: `inline_svg_figures` was called with
  `namespace_ids="chapter-reader" in comps`.
- Reproduced on a fixture before the change: a page with `reader = false`
  and three inlined figures held `clip`, `mark` and `tg-series--a` three
  times each.
- Fixed: on a page without the reader an id is renamed when an earlier
  figure of the page has it, with its references. The first figure keeps
  its ids, so a link from the page's text keeps its target. Reader pages
  take the same path as before.
- Checked: the test for a page without the reader fails before the change
  and passes after it; the test for a reader page passes before and after.
  The kit's own 60 built pages are byte-identical with and without it.
- Not checked: ADP's own home page. ADP's tracked files hold about 6.6 GB
  and nothing is written into its checkout from here.
- Also in this session, not part of the release: four prototypes of a
  calmer chapter reader and a fifth built from deivid's choices, as
  scratch files. Nothing of them is in the kit.
- Not pushed and not tagged. Release waits for deivid's go.

## 2026-11-25 — Release 5.6.1

- deivid gave the go: "Yes, release 5.6.1". The ask named what the go
  covers: moving `main` to `7c88751`, the tag `v5.6.1` and the push, which
  publishes the kit's own site with the retaken pictures. It gave the size
  against 5.6.0 at `7c88751`: 13 files, 91 lines added, 11 removed, and
  the result of the full check script there: exit 0, 452 tests.
- The message with the ask named what is not checked: the two review
  fixes not reviewed again, Chromium only, and the carousel not looked at
  after the change of its alternative texts.
- 5.6.1 holds the changes of the two entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-25 — Review of 5.6.1: fit to tag, three low points

- One independent review read the commit on `v5.6.0`, read-only, opened
  all twelve pictures and ran no build and no browser. Its verdict: fit
  to tag. It found no footer or other overlay, each reader picture on its
  figure, and each of the five new lines supported by its two pictures.
  It confirmed the byte total and the tag commits.
- Fixed, low: the alternative text of the retaken picture of "Against the
  minimal reference" quoted a heading that is no longer in view. The six
  reader pictures now say what is in view.
- Fixed, low: the release note said that only the site and the README
  picture change; the current-release lines change too.
- Not checked by the reviewer: the rendered carousel, and the scroll
  offset this log gives.

## 2026-11-25 — 5.6.1 built on a branch: showcase pictures retaken

- 5.6.0 is released: tag `v5.6.0` on `d705a2f`, pushed with `main`. The
  Pages workflow passed, and the live site shows the 5.6.0 note, the page
  types and the twelve pictures. Branch `rules-5.6.0`, this session's
  scratch files and the brief from the adaptation session are removed.
- deivid pasted a review of the showcase from the adaptation project with
  three points. Checked before acting: the footer over the reader in the
  picture of "Against the minimal reference" was visible in the picture;
  the adaptation commit `33ccf8f`, "Remove the footers after the last
  chapter of the three Cursor readers", exists in the local checkout.
- My miss in 5.6.0: I had looked at three of the six reader pictures
  before the release, saw the footer line in one and let it pass, and
  did not check that each picture showed its chapter's figure. I had also
  proposed one line per example and then wrote only alternative texts.
- Retaken: all six reader pictures, from adaptation at `d22ef36` built
  with kit `v5.5.1` in a scratch clone, 1440 by 810 px, footer hidden,
  the chapter scrolled so that its main figure starts 16 px below the
  chapter head. The twelve pictures are 545,768 bytes together.
- Limit: the chapter "Step downhill, but not too far" has its two figures
  1,223 px apart at this width, more than one window shows. The picture
  shows the first, the error valley; the recorded failed run is on the
  slide face.
- Added under Figure 3: five lines that name the kind of chapter and what
  to look at, in the review's wording where the pictures support it.
- Looked at by eye: a sheet of all six retaken pictures, the chapter at
  1440 px, and slides 10 and 12 in the carousel at 390 px.
- Not pushed and not tagged. Release waits for deivid's go.

## 2026-11-25 — Release 5.6.0

- deivid gave the go: "Yes, release 5.6.0". The ask named what the go
  covers: moving `main` to `19fa3c4`, the tag `v5.6.0` and the push, which
  publishes the kit's own site and with it six adaptation chapters as
  pictures. It gave the size against 5.5.2 at `19fa3c4`: 28 files, 225
  lines added, 20 removed, and the result of the full check script there:
  exit 0, 452 tests.
- The message with the ask named what is not verified: the review fixes
  not reviewed again, the carousel fix for a closed fold not run in a
  browser, Chromium only, and page types that rest on chapter headings.
- 5.6.0 holds the changes of the two entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-25 — Review of 5.6.0: not fit to tag, then fixed

- One independent review read the three commits on `v5.5.2`, read-only,
  and ran no build and no browser. Its verdict: not fit to tag, for one
  wrong count. The full check script had passed on the same state: exit 0,
  452 tests.
- Fixed, medium: the release note's heading, the entry below and the
  first commit's subject said "six" smaller rules. There are five: of the
  seven proposals, two became the page types. The commit subject was
  corrected on the unpushed branch, so its three commits have new hashes.
- Fixed, low: a carousel inside a closed fold has no height when the page
  loads, so its arrows kept the old place until the next slide. The
  carousel now also places them when its box changes size. Inferred by
  the reviewer from the code; not run in a browser before or after.
- Fixed, low: the alternative texts of two slide faces quoted only the
  first clause of a title in quotation marks. All six now describe the
  picture and quote nothing.
- Not changed, low: the rule that a decision page ends with an options
  table names no page type. The default order of a type may change, so
  the two do not conflict.
- The reviewer confirmed the links and anchors of the new rule text, the
  two byte counts, that no check was added and that no mention of the
  removed pictures remains outside this worklog. It could not check the
  count of 48 pages or the review by eye.

## 2026-11-25 — 5.6.0 built on a branch: page types, five rules, a showcase

- 5.5.2 is released: tag `v5.5.2` on `9415956`, pushed with `main`. The
  Pages workflow passed, and the live site shows the 5.5.2 note and the
  new rule for inline code. Branch `fixes-5.5.2` is deleted after the
  merge.
- Source of the rules: seven proposals from adaptation's refactor, K1 to
  K7. K3, named reference pages, and K4, site structure, became the page
  types; the other five became one rule each. They were pasted
  by deivid with the aim that ML and engineering projects alike "dont feel
  forced to follow" what does not fit them. Each was discussed and its
  wording shown before anything was written.
- Page types. The first sort by chapter headings gave one group of 23
  pages; deivid: "from adp u could extract more meaningful ones". Reading
  ADP's chapters and records split it; he asked to merge some, and
  architecture went into design and collection into specification. He
  asked where adaptation was: the first count had missed 12 pages in
  nested folders, 7 of them adaptation's. Its related-work page and two
  of ADP's share one order, and he answered "Yes, add it". Final: six
  types from 48 pages.
- Wording accepted by deivid: the page types section ("yes"), the colour
  table and the term list ("Yes, both"), the new reading, the review
  order and the merge ("Yes, all three"). Against the pasted proposals:
  a colour row says where its meaning holds, the palette keeps the
  values, the term list links to definitions, and the addendum has three
  parts, not six.
- Showcase. A brief from the adaptation session asked for five chapters
  as HTML snapshots in the kit. deivid on publishing them: "they can be
  public no need to lock, but these shouldnt be templates just examples";
  on the form: "yea maybe picture is best"; on when: "Yes, in 5.6.0".
  adaptation was built at `d22ef36` with kit `v5.5.1` in a scratch clone
  and captured there; nothing was written into adaptation. Twelve WebP
  pictures, 611,034 bytes together.
- Removed on deivid's word ("remove the examples from your own docs"):
  `docs/topics/build-a-site/media/reader.png` and `home.png`, two captures
  of the kit's own site from 2026-11-08, 773,647 bytes together. Both
  were tracked and stay in Git at `v5.5.2`. Kept: the two slide faces of
  the kit's own pages, which the site suite runs on, and the starter.
- Found while placing the pictures: with twelve slides the carousel's
  arrows covered its dots at 390 px. The arrows now follow the slide
  shown; the site suite checks it at 1600 and 390 px.
- Looked at by eye: the showcase figure at 1440 and 390 px, both slides
  of the first example, and a sheet of all six faces.
- Not pushed and not tagged. Release waits for deivid's go.

## 2026-11-25 — Release 5.5.2: the go after the second review

- deivid gave the go again: "Yes, release". The ask said that the release
  now includes the fix of the second review, `82f677c`, that this fix had
  no third review, and that nothing was tagged or pushed. It gave the
  result of the full check script on `82f677c`: exit 0, 452 tests.
- Size against 5.5.1 at `82f677c`: 18 files, 498 lines added, 43 removed.
- 5.5.2 holds the changes of the four entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-25 — Second review of 5.5.2: not fit to tag, then fixed

- The second review read `8d2e73d`, read-only, ran Python on scratch
  projects and ran no browser. Its verdict: not fit to tag. The release
  stopped before the tag, as the entry below says; nothing was pushed. The
  full check script had passed on `8454ec4`.
- Fixed, medium: the reader's id was taken on a page that lists the
  `chapter-reader` component without placing the bar. A heading "Chapter
  reader" became `chapter-reader-1` and a link to it failed lint, which
  passed on 5.5.1. Reproduced with the reviewer's script on `8454ec4`:
  build 0, lint 1, "dead internal anchor #chapter-reader". The id is now
  taken where the build places the bar or the page's own source does;
  after the fix build and lint return 0 and the heading keeps its id.
- Not changed, named in the release note: a bar that arrives through a
  project's own fragment; a general-password reader of a locked site, whose
  page has no Reference section; the record notes, which count the reader's
  bar only.
- Not changed, named in the open list: the lock suite tells the fix from
  the defect only when the page is decrypted before the lock page has
  loaded. The reviewer reasoned this from the code. The suite did fail on
  5.5.1 and on the first form in the runs made.
- Corrected in the release note: "32 of 32" counted 22 runs of the first
  form under an assertion that could not see its defect; the note now gives
  the 10 runs of the released form. The three seconds count from the
  decryption, not from the start of the load.
- This fix was not reviewed a third time. It was checked with the
  reviewer's script before and after, and with two new tests.

## 2026-11-25 — Release 5.5.2

- deivid gave the go: "release first". It answered the question whether to
  build the next rule changes as 5.6.0 on a branch, whose other choice was
  "Release 5.5.2 first". The earlier ask named what the release covers:
  moving `main` to the release state, the tag `v5.5.2` and the push, which
  publishes the kit's own site. Size against 5.5.1 at `8d2e73d`: 18 files,
  375 lines added, 42 removed.
- The messages with the ask named what is not verified: Chromium only, the
  cause of the dropped scripts in Chromium not known, the three-second
  fallback that replaces the page in the old state, and the review fixes
  not reviewed again.
- For the last point a second review, read-only, reads the fix commit
  `8d2e73d` while the checks run. The tag waits for both; a finding stops
  the release.
- 5.5.2 holds the changes of the two entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-25 — Review of 5.5.2: not fit to tag, then fixed

- One independent review of `4494301`, read-only, by a reviewer agent that
  ran Python on scratch projects, read Chromium's source and ran no
  browser. Its verdict: not fit to tag. The full check script had passed on
  the same commit.
- Fixed, medium: the first form of the lock fix resumed inside the lock
  page's load event. Chromium then gives the written page no load event of
  its own, so the lock's scroll to a fragment and every `load` listener of
  a component never ran. The reviewer read this from
  `DispatchLoadEventAndFinalize` in Chromium's `document.cc`. Confirmed in
  the browser: the tab recorded `complete` at the replacement and no load
  after it. The replacement now runs in the task after the load event, and
  the suite checks both; it fails on 5.5.1 with `interactive` and on the
  first form with the missing load. 10 of 10 runs at 40 % of a processor
  pass on the final form.
- Fixed, medium: `repo-tree-label` was reserved on every site. On a site
  without a Reference tree a heading "Repo tree label" was renamed and a
  link to it failed lint, which passed on 5.5.1; the reviewer reproduced
  it. An id is now taken only on a page that holds its element: the tree's
  label with a tree, the reader's bar with the reader, the plot labels with
  labelled plot toggles.
- Fixed, low: the record notes named a chapter by the id it had before the
  shell was counted. They start as the build does on a reader page.
- Found while fixing the test: the suite's step "the same shared link on a
  new load" changes only the fragment, so the browser stays on the page and
  no lock page opens. The tab therefore sees two replacements, one by
  password and one by saved key, not three. The step is unchanged.
- Corrected in the release note: the three-second fallback replaces the
  page in the old state; a typed password is usually, not always, after the
  load; a page with "Menu" and "Menu 1" shifts its second id; inline code
  that relied on the general rule wraps in two header bars. The open list
  keeps the unexplained cause, the fallback and the other engines.
- Not changed: the theme's rule from 5.5.1 for Reference pages stays,
  though the new rule covers most of it; it still outranks a build-sheet
  label on a topic page with the body class `reference-page`.
- These fixes were not reviewed again.

## 2026-11-25 — 5.5.2 built on a branch: three open points closed

- After the release of 5.5.1 the closing message named three open points
  of the kit's list, and deivid answered "well work on these". Tag and push
  are not part of that answer.
- The timeout of the page lock's browser suite. Reproduced with the suite
  limited to 40 % of a processor: 4 of 10 runs failed at the same line as
  in the Pages workflow. In a failing run the unlocked page was complete
  and none of its scripts had run: no reader view, no code chips, no style
  from the lightbox, and a second DOMContentLoaded started nothing. The
  lock had replaced its page in the state `interactive`, as it does in
  every opening from a saved key; in passing runs too, so that state is
  needed for the failure and does not always cause it. With a wait for the
  lock page's load event 22 of 22 runs passed at the same limit. Why
  Chromium drops the scripts was not found. An attempt to force the failure
  by delaying the lock page's fonts did not reproduce it.
- Fixed in `page-lock.js`: wait for the load event, at most three seconds.
  The suite now records the document state at each replacement and fails
  when one is not `complete`; without the fix it fails on `interactive`.
- A topic page without the reader: measured on a scratch project, 1235 px
  wide in a 1100 px and a 901 px window with a 108-character command.
  Fixed with one rule for inline code in the content of any page, written
  so that it weighs no more than the theme's general rule for `code`.
- A heading with an id of the shell. The build now starts the numbering of
  a page's headings with the ids of the shell, and of the reader's bar on a
  page that has it. Decided by me, not asked: only ids that the built page
  holds are reserved. An id that exists only while a script runs, or only
  on the lock page, is left alone, because renaming such a heading could
  break a link that lint passes today. Lint's anchor list still reads the
  file as GitHub shows it.
- One test expectation changed, in `tests/test_listed_html.py`: a heading
  "Menu" of a listed file lost its id before and now gets `menu-1`. The
  goal of the old expectation holds: the page's content gets no id of the
  kit.
- Not verified: Chromium only.

## 2026-11-24 — Release 5.5.1

- deivid gave the go: "Yes, release 5.5.1". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.5.1` and the push,
  which publishes the kit's own site. It gave the size against 5.5.0 as 9
  files and about 130 lines added, not recounted after the review fixes;
  counted for this entry at `5ae694f`: 9 files, 135 lines added, 4 removed.
- The message with the ask named what is not verified: Chromium only,
  adaptation's own page not measured again, the review fixes not reviewed
  again, and a topic page without the reader not measured.
- 5.5.1 holds the changes of the two entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-24 — Review of 5.5.1: not fit to tag, then fixed

- One independent review of `e32aaba`, read-only, by a reviewer agent that
  built a scratch clone and ran no browser. Its verdict: not fit to tag. It
  judged the change a patch under the version promise, as long as tables
  are left alone. The full check script had passed on the same commit.
- Fixed, medium: the rule also reached code in table cells. There
  `overflow-wrap: anywhere` lowers a column's narrowest width, so on a
  window wider than 900 px a wide table would squeeze its code columns and
  break paths inside a word instead of scrolling in its box. The reviewer
  reasoned this from the CSS and did not see it in a browser. The rule now
  leaves out code in `td` and `th`.
- Fixed, low: the rule matched code deeper inside a hand-written `pre`,
  such as `<pre><b><code>`, and would have removed its line breaks. It now
  leaves out every `pre code`. The test covers both cases and fails with
  the first form of the rule: "code deeper inside a hand-written pre keeps
  its lines".
- Fixed, low, in the release note: a topic page with
  `body_class = "reference-page"` gets the wrapping too; the reader's
  chapters already wrapped inline code; a project that follows the 5.5.0
  guide uses the tag `v5.5.1`.
- Checked on the reviewer's doubt about one number: the failing run on the
  old theme printed "notes.long.md.html at 1100 px: the command reaches
  1242 px, the page is 1242 px wide". The note's page width is that value.
- Recorded, not fixed: a topic page without the reader keeps inline code on
  one line. The open list has the point.
- These fixes were not reviewed again.

## 2026-11-24 — 5.5.1 built on a branch: inline code wraps on Reference pages

- deivid passed on a defect from adaptation: inline code is kept on one
  line above phone width, so a 100-character command made a Reference page
  of adaptation 1507 px wide in a 1440 px window. Asked to build 5.5.1 on a
  branch with inline code wrapping on Reference pages: "Yes, build 5.5.1".
  Tag and push are not part of that answer.
- Confirmed before the fix on a scratch project in headless Chromium: with
  a 108-character command a listed and a registered Reference page were
  1318 px wide in a 1100 px and a 901 px window, and fine at 390 px. A
  reader topic page did not widen. adaptation's own 1507 px was not measured.
- Fixed with one rule for inline code on Reference pages; a code block is
  left alone. The new check in `tests/test_page_shell.cjs` failed on the old
  theme, "the command reaches 1242 px", and passes now.
- After the release of 5.5.0, recorded here: the Pages workflow for
  `8fe485f` failed on its first attempt, in the check job, with a 30-second
  timeout at `tests/test_page_lock_browser.cjs:258`, where the page waits
  for a reader chapter after an unlock. The rerun of the failed job passed
  and published the site. The same suite passed in six local runs on that
  commit. The cause is not known; it was the first failed run of the last
  twelve.
- adaptation pins `v5.5.0` since its commit `d5228b5`, read in its
  checkout. What its upgrade met is in its own records.

## 2026-11-24 — Release 5.5.0

- deivid gave the go: "Yes, release 5.5.0". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.5.0` and the push,
  which publishes the kit's own site. It gave the size against 5.4.1: 25
  files changed, 820 lines added and 47 removed.
- The message with the ask named two choices that were mine: the rule
  holds for all text of a page, a project's own styles included, and a
  migration guide was written. It named what is not verified: Chromium
  only, the review fixes not reviewed again, and no project built against
  5.5.0.
- 5.5.0 holds the changes of the three entries below.
- This commit adds only this entry. The full check script runs on it before
  the tag; the Pages workflow runs it again on the push.

## 2026-11-24 — 5.5.0 waits on its branch for deivid's go

- State: branch `release-5.5.0`, five commits on `v5.4.1` with this one, not pushed, no
  tag. `main` is still 5.4.1.
- The full check script passed on `710bb80`: 444 Python tests, 2 skipped,
  and every browser suite, in Chromium. The text-size suite read 60 pages
  of the kit's site, the new migration guide among them.
- Reviewed by eye at 1600 and 390 px, after the review fixes: the home
  page, a Reference page with its folder tree and code blocks, a reader
  page with its chapter numbers and an open fold, the flow labels and both
  drawers. No label wraps, sticks out of its box or collides. The
  Presentation title card was measured, not looked at.
- This commit corrects the page count in the release note from 59 to 60
  and adds this entry. Checks on it: `build` and `lint --strict`.

## 2026-11-24 — Review of 5.5.0: not fit to tag, then fixed

- One independent review of `bdf9857`, read-only, by a reviewer agent that
  ran Python in a scratch clone and no browser. Its verdict: not fit to tag.
  It found no change that the version promise keeps for a major release.
  The full check script had passed on the same commit.
- Fixed, medium to high: lint stopped with a traceback when a tracked record
  under `record_roots` was missing from disk, as after a deletion or in a
  sparse checkout. Such a file is not read now. A record that is not UTF-8
  text is an error with the file's name instead of a traceback, and an
  exclusion of `.` is refused.
- Fixed, medium: the release note said the warning for a repeated id finds
  ids written by hand. A heading whose id is an id of the page shell, such
  as "Top" or "Menu", gets the warning too; the reviewer showed it on the
  starter. The note and the new migration guide name the case. The shell's
  ids are still not reserved; the open list has the point.
- Fixed, medium: the note left out that `record_roots` also brings the
  figure-manifest errors to those records. The rule and the guide say it.
- Fixed, low to medium: the eyebrow of the Presentation title card was
  below 11 px, which the suite could not see. Measured before the fix:
  4.68 px in a 390 px window. It stops at 11 px, tested at 390, 800 and
  1440 px.
- Fixed, low: the version promise says a migration guide gives the step for
  each change; 5.5.0 had none. `migrations/5.5.0.md` is written and listed.
- Fixed, low: repeated ids are counted with Python's HTML parser instead of
  two regular expressions, which read `template` and `textarea` content as
  elements and missed an upper-case or unquoted `id`. Tests added: the
  warning against the note on a listed page, the deleted record, the
  unreadable record, overlapping roots, the skips of `smallText`, inline
  code at 11 px and on a slide face. `tests/test_lint.py` run as a file ran
  6 of its tests; its `__main__` block is at the end now.
- Changed on the reviewer's remark that drawings in inactive chapters were
  never measured: the suite now shows all chapters of the 6 reader pages and
  opens every fold before it reads a page.
- Not changed: a flow-arrow label of 12 or more characters would not fit
  its 88 px column at 11 px; the longest label of the kit has 11. Estimated
  from font metrics by the reviewer, not measured.
- These fixes were not reviewed again.

## 2026-11-24 — 5.5.0 built on a branch: text limit, record roots, repeated ids

- Decisions by deivid. Asked whether 11 px becomes a rule for all text of
  the kit or only three named labels are raised: "Yes, all kit text". Asked
  to build 5.5.0 on a branch with formulas and scaled slide faces outside
  the limit: "Yes, build it". Tag and push are not part of either answer.
- A count corrected before the build: the theme had 24 font sizes below
  11 px, not the 20 that the proposal for 5.4.1 named. A probe in headless
  Chromium found 27 kinds of text below 11 px on the 61 built pages of the
  kit's site and starter, at 1440 and 390 px. Three kinds came from relative
  sizes that no search for `px` finds: inline code in small labels and table
  headings, and the brand subtitle.
- Built: the 24 sizes are 11 px; inline code stops at 11 px and keeps its
  scaling on slide faces; `smallText` and `assertTextSize` in
  `browser_checks.cjs`; `tests/test_text_size.cjs` on all 59 pages of the
  kit's site and on a fixture of labels those pages lack. With the old theme
  the suite fails, on 26 kinds of text on the fixture page.
- Built: `record_roots` and `record_roots_exclude` for lint, and a lint
  warning for an id that a built page carries more than once. On the kit's
  own pages no id is repeated.
- A reading of mine, not asked: the rule in `rules/writing/pages.md` says
  all text of a page, a page's own styles included, since the limit for
  chart labels binds projects the same way. The kit checks only its own
  site; a project is checked when it calls `assertTextSize`.
- Not verified: Chromium only. No project was built against this state.
  The check does not exempt `sub` and `sup` outside formulas.
- Commits `eedb5e0` and `37d873f`, then the release notes and version.

## 2026-11-24 — Release 5.4.1

- deivid gave the go: "Yes, release 5.4.1". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.4.1` and the push,
  which publishes the kit's own site. It gave the size against 5.4.0: 21
  files changed, 544 lines added and 34 removed, and no migration step.
- The message with the ask named where the build differs from the proposal:
  the page behind an open drawer is inert, and print switches off the fold
  fade and the panel fade only. It named what is recorded and not fixed: an
  explicit `{#id}` takes part in the numbering, and lint and the build find
  headings differently.
- 5.4.1 holds the changes of the three entries below. One independent
  review; its findings are fixed or recorded and the fixes were not reviewed
  again. Chromium only.
- This commit adds only this entry. Checks on it: `build` and `lint
  --strict` of the kit pass. The full script passed on `cc59447`, the
  commit before; the Pages workflow runs it on the push.

## 2026-11-24 — Review of 5.4.1: not fit to tag, then fixed

- One independent review of `50a3574`, read-only, by a reviewer agent that
  ran Python in a scratch copy and no browser. Its verdict: not fit to tag.
  It found nothing that makes a project's build or lint fail where it
  passed. The same hour the full check script failed once on that commit,
  at `own_site_review.cjs`: "edit link hidden in print".
- Fixed, medium: `.source-origin a` had become `inline-flex`, which outranks
  the print rule that hides the edit link, so the link printed. Links and
  chips now reach 24 px by line height alone; their `display` and
  `box-sizing` are as in 5.4.0, so no rule of the kit or of a project is
  outranked and the pencil before "Edit source" keeps its space.
- Fixed, medium: the menu button sits in the page content, which the open
  drawer made inert. The button then left the focus order with
  `aria-expanded="true"` unread, and a touch screen-reader user could close
  the drawer only by following a link. The top bar is now left out of the
  inert part.
- Fixed, low to medium: each tab of a page was numbered on its own, so
  "Result" in two tabs still shared an id while lint listed `result-1`. A
  page's tabs now share one numbering.
- Fixed, low: an edit meant for the print rule also narrowed the panel
  switcher's reduced-motion rule. It is as in 5.4.0 again.
- Narrowed on my own reading of the review's risk note: the print rule
  switched every animation and transition of a reader page off, which would
  hide project content that animates in from `opacity: 0`. It now switches
  off the fold fade only, the measured defect.
- Recorded, not fixed: an explicit `{#id}` takes part in the numbering, and
  lint, the record notes and the build find headings differently. The
  release notes and the open list say so.
- New checks: the menu button closes the open drawer by keyboard, a window
  widened with the drawer open leaves nothing inert, and three "Result"
  headings across tabs get three ids. The tab check was seen to fail on the
  commit under review.
- The fixes were not reviewed again.

## 2026-11-24 — The page lock opens on a real host, in Firefox on Windows

- deivid reported on 2026-11-23 about adaptation's live, locked site on
  GitHub Pages: "the unlocking works". Asked which browser and device, he
  answered on 2026-11-24: "windows pc firefox".
- This is the first report of the lock on a real host; the kit's checks
  open locked pages from a local server only. The open item
  [Safari and the real host](open/known-open-after-5.0.0.md) now says so
  and stays open for real Safari.
- Not known: which of the two passwords he used, whether a Reference page
  was opened, and the Firefox version. Nobody but deivid saw the unlock; the
  kit records his report, not a check.

## 2026-11-24 — Seven corrections from adaptation's review, for 5.4.1

- deivid pasted a request from the adaptation project: propose fixes for
  nine defects, propose only. Eight came from its accessibility, print and
  responsive review of 23 November 2026, one from its conformance check. He
  answered the proposal with "Build 5.4.1". The go covers building the seven
  patch fixes on the branch `fixes-5.4.1`; it covers no tag and no push.
- All nine reproduced on 5.4.0, in a scratch project in headless Chromium
  at 390, 768 and 1600 px. Two reports were corrected. The 11 px minimum
  covers chart labels and slide-drawing labels, not interface text. KaTeX
  widened the page for a formula far right in a scrolling table, 578 px in
  a 390 px window, and not for the kit's display-equation box in 12
  combinations of width, view and page type.
- Fixed in `7477f65`: the closed drawer's focus order, the menu button's
  state and keys, 24 px targets, wrapping of long addresses, the KaTeX
  rule, and print with animations off. Fixed in `30c9e9c`:
  repeated heading ids, numbered as GitHub numbers them. The
  [release notes](topics/releases/releases.md#541--seven-corrections-from-adaptations-accessibility-print-and-phone-review)
  give the measurements.
- One addition the proposal did not name: the page behind an open drawer is
  inert below 900 px, so focus cannot leave the drawer for content the
  backdrop covers. The reader does the same for its drawer.
- The project's `visibility: hidden` workaround was not taken over. Without
  JavaScript the menu button does nothing, and the off-screen links are the
  only navigation; `inert` set by the script leaves that path open.
- `tests/test_page_shell.cjs` is new and runs with motion on. The other
  browser suites ask for reduced motion, which switches the fold fade off,
  so no check had seen it. Each of its assertions was run against the kit
  with the matching fix taken out and failed; the panel switcher's print
  check likewise.
- Left for a minor release, on deivid's decision: text below 11 px (20
  `px` declarations of 9 to 10.5 px in the theme) and lint for records
  outside `docs/`.
- Not done: no browser but Chromium; no printout on paper; adaptation's own
  pages and CSS were not opened.

## 2026-11-23 — Release 5.4.0

- deivid gave the go: "Yes, release 5.4.0". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.4.0` and the push,
  which publishes the kit's own site. It gave the size against 5.3.0: 12
  files changed, 609 lines added and 61 removed, and no migration step.
- The message with the ask named the visible change in the build: three
  include failures end in an error line where they ended in a traceback.
- 5.4.0 holds the changes of the two entries below. One independent
  review; its findings are fixed and the fixes were not reviewed again.
- This commit adds only this entry. Checks on it: `build` and `lint
  --strict` of the kit pass. The full script passed on `574e5c1`, the
  commit before; the Pages workflow runs it on the push.

## 2026-11-23 — Review of 5.4.0: not fit to tag, then fixed

- One independent review of `c8d1a4e`, read-only, by a reviewer agent. Its
  verdict: not fit to tag. It found no change in the build's behaviour, by
  reading old and new code line by line and by running both on scratch
  projects, and three gaps between the helper and its own description.
- Fixed, medium: the helper expanded includes below `<!-- page-end -->`,
  which the build cuts off first. It returned the tail and raised for a
  missing include there. It now cuts at the marker through
  `rendered_part`, which the build calls in both places too.
- Fixed, medium: an absolute path or `..` in an include, and a fragment
  that is not text, stopped the expansion at once, so later problems of the
  page were lost. Both are now reported like the others. In the build these
  cases ended in a traceback; they now end in an error line, still with
  exit status 1.
- Fixed, medium to low: a fragment without read permission, a link loop
  and a tracked file whose name is not UTF-8 left the helper as other
  exception types; the last one failed every page of a project.
  Unreadable fragments and loops are named problems now, and the helper
  decodes tracked names as the system reads them.
- Measured after that fix, on a starter project with such a file: `build`
  and `lint` still stop with a traceback, `UnicodeDecodeError`, at another
  place that reads Git's output. That is older than this change and not
  fixed here; it is listed in
  [known open after 5.0.0](open/known-open-after-5.0.0.md). A sentence in
  my draft of the release notes claimed the opposite and is removed.
- Measured on the same project: an absolute include followed by a missing
  one gives two `ERROR:` lines and no traceback.
- Fixed, low: the texts did not say that a project's `content_transform`
  does not run; the stability promise left out the name `PageSourceError`.
- Correction to the entry below and to the message of `c8d1a4e`: the two
  comparisons with the 5.3.0 tooling covered the built HTML folder.
  `site-build.json` beside it differs in its version field.
- Not changed: the helper names a page by its path in the project, the
  build by its path under `docs/topics/`; no text promises the same
  wording. The helper reads whatever page path it is given, also outside
  the project; includes cannot leave the theme and the project.
- Tests added for each fix, and the comparison with the build now runs the
  page-end cut. The fixes were not reviewed again.

## 2026-11-23 — A page's source for a project's checks; prepare 5.4.0

- deivid pasted a request from the adaptation agent: a documented helper
  that returns a topic page's source as the build reads it, because two of
  adaptation's checks import `parse_frontmatter` and `expand_includes`
  from `tooling/build.py`. I checked its facts in the kit and in
  adaptation's `docs/site/checks/`; they hold.
- One premise was wrong and makes the case stronger: the request called the
  errors "printed build errors". The build collects them in a list and
  returns text all the same, so adaptation's checks could pass on a page
  whose include is missing.
- I proposed three changes to the request: the project is an argument and
  importing reads no environment; every problem of a page is collected and
  raised once, as the build lists them all; the helper says exactly what it
  returns, frontmatter and include-expanded text and nothing later.
  deivid's go: "Yes, build it".
- `tooling/page_source.py`: `page_source(path, project)`,
  `PageSourceError` with `problems`, and the functions the build shares:
  `split_frontmatter`, `expand_includes`, `local_resource`,
  `tracked_paths`. Frontmatter keys are not validated there.
- `tooling/build.py` calls them; `parse_frontmatter` and `expand_includes`
  keep their names and behaviour there, so adaptation's checks still run
  after it moves the pin.
- Measured: an identical starter project with nested includes, built with
  the tooling of `v5.3.0` and with the new tooling, gives the same output
  under `diff -r`; the kit's own site from the same sources gives the same
  145 files by SHA-256.
- Tests in `tests/test_page_source.py`: frontmatter, nested includes, a
  cycle, paths that leave the project, a missing, untracked and empty
  include, the depth limit, all problems at once, two projects in one
  process, and equality with what the build's own functions return,
  problems included.
- `rules/site/validation.md` gets the section "A page's source for checks"
  with the stability promise; the capability map gets a row.
- Prepared as minor 5.4.0 without a migration guide: nothing has to change,
  and the release notes carry the line for projects that import the two
  build functions.
- Not in this change: adaptation also removes slide blocks with a regular
  expression of its own, a second dependence on the kit's syntax.

## 2026-11-22 — Release 5.3.0

- deivid gave the go: "Yes, release 5.3.0". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.3.0` and the push,
  which publishes the kit's own site. It gave the size against 5.2.1: 15
  files changed, 612 lines added and 40 removed, and no migration step.
- The message with the ask named the exception to the versioning promise,
  that `check` no longer hands the lock's passwords to the project's
  checks, and offered to take it out. The go came after it, so the
  exception stands.
- 5.3.0 holds the changes of the two entries below. One independent
  review; its findings are fixed and the fixes were not reviewed again.
- This commit adds only this entry. Checks on it: `build` and `lint
  --strict` of the kit pass. The full script passed on `64ef496`, the
  commit before; the Pages workflow runs it on the push.

## 2026-11-22 — Review of 5.3.0: not fit to tag, then fixed

- One independent review of `9b50d6f`, read-only, by a reviewer agent. Its
  verdict: not fit to tag, two medium findings. It ran four Python test
  files and probes of its own, and no browser suite. It found no path that
  puts unlocked text, a password or a content key into `--out`, the command
  output or an error message.
- Fixed, medium: a `DOCSITE_PLAIN_BUNDLE` the caller's environment held
  reached the declared checks when no trial publish ran, so a check could
  pass on stale pages. `check` now drops the variable and sets it only for
  its own plain copy.
- Fixed, medium: the check after locking did not look at the offset where a
  reference-password reader's browser puts the Reference section back, so
  a wrong offset passed. It now reads the offset from the written lock page
  and puts page and section together again; the result must be the page as
  it was. The rule and the release notes said more than the check proved;
  they now say what it proves and that it runs in Python.
- Fixed, low: an interrupt between the two last moves left a plain copy
  without its bundle; the overlap test with the build output did not
  resolve a linked `.build`; the rule did not say that a site without a
  Reference tree has `reference.tree.js` only in the locked bundle, nor
  that a killed publish can leave `.docsite-publish-*` and
  `.docsite-plain-*` with unlocked pages. The starter's `.gitignore` names
  both.
- Fixed, low, older than this change: `check` handed the lock's passwords
  to every step. They now reach the trial publish only. By the letter of
  the promise this can stop a `check` that passed before; the release notes
  state the exception and why no project is affected. deivid has not
  decided on this exception yet; it is named in the ask for the release.
- Not changed: the check after locking does not cover the lock page's other
  attributes, the padding sizes or the two lock assets. A publish that
  fails leaves an empty parent folder it created, as `--out` always did.
- Tests added for each fix. Checks after the fixes: `build` and `lint
  --strict` pass, and 405 Python tests pass with 2 skipped for missing
  matplotlib. The full script failed once: `tests/test_reference_tree.cjs`
  timed out at line 158, a click without JavaScript on the link to the
  Reference index that the `summary` above it intercepted. The same suite
  then passed three times alone, and the two suites the script had not
  reached, listed HTML and the page lock in the browser, passed alone. The
  fixes touch no file that suite loads. Cause not found; it is the second
  browser timeout of this kind after the page-lock one of 2026-11-21. The
  fixes were not reviewed again.

## 2026-11-22 — A plain copy of the bundle for checks; prepare 5.3.0

- The adaptation session reported, while switching the page lock on: a
  project's checks cannot read its published pages once they are locked.
  `docsite.py check` removed its trial bundle before the project's checks
  ran and gave them no passwords; three of adaptation's checks read
  published pages; the build output differs from the published pages,
  because `publish` rewrites links and media paths. Its note and a
  prototype that decrypts a bundle lie outside this repository. I confirmed
  the first point in `tooling/project_check.py`; the others are its
  findings.
- I proposed that `publish` writes the same bundle twice, plain for checks
  and locked to deploy, and that it opens its own locked files again.
  deivid asked whether this is the best approach; I named the weakness,
  that checks would test the bundle before encryption, and the fix. His go:
  "okay do it".
- Not built, with the reason: a `lock` command of its own after a plain
  `publish`, because a forgotten step would then publish a locked site in
  the clear; a command that decrypts the deployed bundle, because the checks
  would need the passwords or a second publish.
- `tooling/publication.py`: `publish_project(..., plain_copy=)` and
  `docsite.py publish --plain-copy DIR`. The copy is taken before the lock
  step, staged beside its place and moved with the bundle; it must be
  fresh, outside `--out` and outside the build output. A lock that fails
  leaves neither.
- `tooling/page_lock.py`: `open_locked`, `page_header` and `open_tree`
  reverse the three writers. `PageLock.apply` ends with `_open_again`: it
  opens the key header with each password, reads every locked file back
  from disk and compares level, bytes and header with what it locked.
  Measured on this machine: the two extra key derivations take 0.16 s next
  to 0.24 s for the three before.
- `tooling/project_check.py`: the trial publish writes a plain copy, and
  each `[[checks]]` command gets its folder in `DOCSITE_PLAIN_BUNDLE`.
- Tests: each of the three writers broken in turn, and a key header that a
  password does not open, stop the lock; the plain copy equals the bundle
  of an unlocked publish of the same build; the locked bundle opens to it;
  wrong places for the copy are refused; a declared check reads a plain
  page of a locked site.
- Rules: `rules/site/publication.md` gets the option, the sentence on
  opening again and the section "Checks that read published pages";
  `rules/site/validation.md` names the variable.
- Prepared as minor 5.3.0: an option and an environment variable join the
  stable interfaces. No migration guide: no project must change anything,
  and the release notes say what a project with such checks changes.
- Not covered: the browser's own unlock code runs only in the kit's browser
  suite, on the kit's fixture.

## 2026-11-22 — Release 5.2.1

- deivid gave the go: "Yes, release 5.2.1". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.2.1` and the push,
  which publishes the kit's own site. It gave the size against 5.2.0: 9
  files changed, 124 lines added and 26 removed, and no migration step.
- 5.2.1 holds the changes of the two entries below: no rule on the length
  or the characters of a page-lock password, and the refusal of a password
  that is not UTF-8. One independent review; its finding is fixed and the
  fix was not reviewed again.
- This commit adds only this entry. Checks on it: `build` and `lint
  --strict` of the kit pass. The full script last passed on `828feac`; by
  the practice of 2026-11-21 it was not run again. The Pages workflow runs
  it on the push.

## 2026-11-22 — Review of 5.2.1: fit to tag after one fix, fixed

- One independent review of `828feac`, read-only, by a reviewer agent. Its
  verdict: fit to tag after one fix. It ran `tests/test_page_lock.py` and no
  browser suite.
- Fixed, medium: a password holding bytes that are not UTF-8 reaches Python
  as a lone surrogate. The removed check used to refuse it. Without it the
  value passed, and `publish` failed after the build with an encoding error
  that named one byte of the password and a position. `read_passwords` now
  refuses such a value before the build and names only the variable. This
  is not a rule on characters: no key can be derived from the value.
  Reproduced before the fix; a test covers it.
- Fixed, low: a comment about the deleted length check, and the module's
  docstring.
- Not changed: the note also appears for a no-break space and for
  private-use characters, which the texts call "invisible"; the reviewer
  judged the wording accurate enough. Two passwords with line breaks can
  share a salt; no reader can type either.
- The reviewer found no other place that states or enforces the old rules,
  and no path by which the note shows a value. Not verified by it or by me:
  unlocking in a browser with a password of spaces or a tab.
- Checks after the fixes: `build`, `lint --strict` and
  `tests/test_page_lock.py` pass. The full script last passed on `828feac`;
  the fixes touch no theme file, not the build and no browser suite, so by
  the practice of 2026-11-21 it was not run again. The fixes were not
  reviewed again.

## 2026-11-22 — No rule on the lock's passwords; prepare 5.2.1

- deivid asked why the kit decides how long a password is, and decided:
  "no rules on characters or pw size". Before that I had named the reason
  for the minimum, guessing offline without a lockout, and advised keeping
  it.
- `read_passwords` in `tooling/page_lock.py` no longer fails for a password
  shorter than 20 characters, nor for one that starts or ends with
  whitespace or holds a control or invisible character. `MIN_PASSWORD_LENGTH`
  is deleted. A missing password and two equal passwords still fail.
- My choice, not asked for: the second case prints a note on standard error
  and `publish` goes on. A secret pasted with a line break gives a password
  no reader can type, and without the note nothing says so. The note names
  the variable and never the value.
- `rules/site/publication.md`, section "Turn it on", says the new
  behaviour. Tests in `tests/test_page_lock.py` changed with the approved
  behaviour: the short and untypable cases now assert that the password is
  kept, and that the note appears only for the second case.
- Prepared as patch 5.2.1: the promise names "relaxes a check" as a patch.
  `VERSION`, the release notes and the three lines that name the current
  release are updated. No migration guide.
- Checks on this state: `build` and `lint --strict` pass. The full check
  script with the browser suites passes: exit 0, 389 Python tests, 2 skipped
  for missing matplotlib. No review by a second agent yet. Not tagged and
  not pushed.

## 2026-11-21 — Release 5.2.0

- deivid gave the go: "Yes, release 5.2.0". The ask named what the go
  covers: moving `main` to the release state, the tag `v5.2.0` and the push,
  which publishes the kit's own site. It gave the size: 8 commits on `main`,
  29 files changed, 1,715 lines added and 82 removed, and a new migration
  guide.
- 5.2.0 holds the changes of the entries below: lint warnings for untracked
  files, figures in a dark and a light theme, and the check command with its
  opt-in pre-push gate. One independent review; its findings are fixed and
  the fixes were not reviewed again.
- This commit adds only this entry. Checks on it: `build` and `lint
  --strict` of the kit pass. The full script last passed on `5a68f6f`; by
  the practice of 2026-11-21 it was not run again, because nothing after
  that commit touches the theme, the build or a browser suite. The Pages
  workflow runs it on the push.

## 2026-11-21 — Review of 5.2.0: not fit to tag, then fixed

- An independent reviewer tried the three changes on throwaway projects,
  with real pushes to a local bare remote, and recomputed the colour values
  by another path. Verdict: not fit to tag, two major findings, both in the
  pre-push gate.
- Major, fixed: in a new linked worktree the gate was silently off. The
  relative `core.hooksPath` resolved inside the worktree, where the kit
  submodule was not set up yet, so Git ran no hook. The setting is now an
  absolute path to the main checkout's kit, and the hook refuses a push from
  a checkout without `.docs-kit` and names the submodule command.
- Major, fixed: `rules/engineering/git.md` said the gate checks the
  committed state; it reads the working tree. A commit without its map row
  was pushed while the row sat uncommitted in the tree. The hook now refuses
  a push while tracked files have uncommitted changes;
  `DOCS_GATE_ALLOW_CHANGES=1` checks the tree as it is. Untracked files do
  not stop it; lint warns about those that matter.
- Also fixed in the gate: a push that only deletes runs no check; a pushed
  commit that is not the checked-out one gets a line; a locked site's trial
  publish runs with two throwaway passwords, where it was skipped and so hid
  real publish failures.
- Fixed in lint: `__pycache__` under a tooling root no longer warns; the
  import warnings for experiment folders and unreadable files also read
  untracked files; an untracked file whose name is not UTF-8 no longer
  crashes lint; the second import scan runs only when an untracked Python
  file exists.
- Fixed in the palette: light violet and blue were 13.1 apart for full
  colour vision and about 2 for a red or green deficiency. The test had
  compared only neighbours in the series order, and a line chart shows all
  four. Light violet is now `#8a55fb` and light blue `#0a5fbb`: every pair
  of light series colours is at least 17.6 apart, 10.4 for a red and 11.6
  for a green deficiency, and the test checks every pair. The dark colours
  stay; their close pairs, violet with blue (14.8, 6.0 for a green
  deficiency) and accent with blue (12.7), are asserted as known, and the
  rule asks for labelled lines. PDF files from `write_both` carry no
  creation date now.
- Corrected in the records: `publish` does not export a light file, but the
  local build output copies all of `docs/figures/`; the release notes no
  longer repeat the measured values; `[[checks]]` need not stand above the
  first `[[nav]]` table.
- Tried after the fixes with real pushes under dash, with a stub in place of
  the kit: a failing check stops the push and the remote stays unchanged, a
  passing one pushes, an uncommitted change to a tracked file stops it, a
  new worktree without the kit stops it, a deletion runs no check.
- Not reviewed again: these fixes. Checks: the tests of the three areas
  pass, 53 tests with 2 skipped; build and strict lint of the kit pass. The
  full script was not run again: no fix touches the theme, the build or a
  browser suite.

## 2026-11-21 — The full check script runs once per release

- Why: deivid asked why the checks take so long. One run of
  `tests/run_checks.sh` takes about five minutes: the Python tests 47 s,
  measured, and the seven browser suites the rest, not timed one by one. The
  kit owner ran it after each change set, four times on 2026-11-21 before
  the review, and before each tag even for a commit that only added a
  worklog entry.
- deivid decided: "Yes, once per release". Between changes the build, strict
  lint and the tests of the touched files run, judged by exit code; the full
  script runs once on the final state before the tag. `docs/KIT_CONTEXT.md`
  holds the practice.
- The risk taken: a browser problem shows at the end of a release's work,
  not after the change that caused it.

## 2026-11-21 — A check command and an opt-in pre-push gate

- Why: asked for from adaptation, by deivid's message of 2026-11-21. A
  project that wants a push stopped when lint fails had to write its own Git
  hook; adaptation pushed a commit whose publish workflow then failed on
  lint.
- `docsite.py check --project .` runs `build`, `lint --strict`, a trial
  `publish` into a temporary folder when `[publication]` is configured, and
  the commands a project declares in `[[checks]]` tables, and stops at the
  first failure. `tooling/project_check.py` holds it. A command is an
  argument list run without a shell; `{python}` stands for the interpreter
  that runs the check.
- `hooks/pre-push` calls the command. One line switches it on in a clone:
  `git config core.hooksPath .docs-kit/hooks`. The hook lies in the kit, not
  in the starter, so no project gets it without choosing it and `init` need
  not copy an executable file.
- Limits, stated in the rule: the checks read the working tree, not the
  pushed commits, and the hook prints a line when the tree has uncommitted
  changes; with the page lock on and no passwords in the environment the
  trial publish is skipped with a note; browser checks are not part of it;
  `--no-verify` skips the hook.
- Rule: `rules/site/validation.md#one-command-and-a-pre-push-gate`; one
  bullet in `rules/engineering/git.md`.
- `tests/test_project_check.py`, 13 tests: the order, the stop at the first
  failure, a lint failure before declared checks, a missing program, wrong
  configuration, the trial publish and its skip, and the hook with a stub in
  place of the kit. The hook was not run by a real `git push`.

## 2026-11-21 — Figures in a dark and a light theme; prepare 5.2.0

- Why: asked for from adaptation. The kit had only the dark colours of
  `tooling/svg_figures.py` and nothing for matplotlib, so one generator wrote
  matplotlib's white default onto the dark reader, and no light figure
  existed for slides. The kit owner first proposed to build only a helper
  and no second copy of each figure, because the reader has no light theme.
  deivid: "i specifically asked tto have light already so i can use for
  presentations if light is needed". He builds those in his own slides, not
  in the kit's deck, so the deck and the reader stay dark.
- `tooling/figure_themes.py`: a dark palette equal to the SVG helper's
  constants, a light one, `matplotlib_rc(theme)`, `variant_path` and
  `write_both(path, draw)`. Naming: `<name>.<ext>` dark, `<name>.light.<ext>`
  light. The kit does not depend on matplotlib.
- The colour check was run with the palette validator of the `dataviz` skill
  and is kept as `tests/test_figure_themes.py`, whose numbers agree with it.
  Light palette: all checks pass. Dark palette: with violet next to blue the
  pair measured 6.0 for a green colour deficiency and 14.8 for full colour
  vision, below both floors; the fixed series order accent, violet, warm,
  blue keeps them apart. The dark series colours are brighter than the
  validator's range for a dark chart; they stay, because they match the
  reader and every existing figure.
- Seen in a render of one sample plot with four lines and five bars, in both
  themes, with matplotlib 3.10.6: text, grid, legend and marks read in both.
- Rule: `rules/writing/figures.md` asks for both themes;
  `rules/site/authoring.md#generated-figures` has the naming, the helper and
  what stays dark. No lint check demands the light file: the build knows no
  generator, and a generator that uses `write_both` cannot leave it out.
- Lint's figure manifest check warned about every file in `docs/figures/`
  that no page shows, so each light file would have failed strict lint. It
  now counts the light file of a shown figure as kept, like the raster
  export, when the manifest gives both the same script. Shown by a test
  that fails without the change.
- The kit's own generator follows the rule:
  `docs/topics/approval-failed-open/draw_figures.py` writes
  `pileup-wide.light.svg` and `pileup-upright.light.svg`, lists them in its
  manifest, and `--check` covers them. The dark files and the page's
  fragments are the same bytes as before. Its five group colours got light
  counterparts, measured: marks at least 3.0:1 on white and on the shaded
  band, white labels 4.5:1 on their bands, neighbours in the stack at least
  16.4 apart and 9.9 for a red or green colour deficiency. Seen in a
  browser render of both light files.
- Not built: a light reader, a light deck, a variant switch on pages.
- The kit's test environment has no matplotlib, so the two matplotlib tests
  are skipped in `tests/run_checks.sh`. They pass in adaptation's
  documentation environment.
- Checks on the 5.2.0 state with all three changes: `build`, `lint --strict`
  and `build --check-reader` pass; `DOCS_REQUIRE_BROWSER=1 bash
  tests/run_checks.sh` passes with 379 Python tests, 2 of them skipped, and
  seven browser suites. A first full run failed once: the page-lock browser
  suite timed out after 30 s waiting for `guide.html#locked-detail` to show
  its chapter. The suite then passed twice alone and in the second full run;
  the cause was not found, and no change of this release touches the lock.

## 2026-11-21 — Lint warns about untracked files under a tooling root

- Why: reported from adaptation, pinned at `v5.0.0`. A new file
  `docs/site/checks/test_public_paths.py` under a tooling root had no row in
  the capability map. `lint --strict` passed while the file was untracked
  and failed once it was committed; the commit was pushed on the clean lint
  and the project's publish workflow failed.
- The capability-map check read only `git ls-files`. It now also reads the
  files Git neither tracks nor ignores, and warns for an entry directly
  under a tooling root that no row links: "not tracked yet; no row links
  it, so lint fails once it is committed". A warning fails `--strict`.
- It is a warning, not an error. The test this replaces,
  `test_untracked_tooling_is_not_required`, held the assumption that an
  untracked file is scratch and none of the map's business; that assumption
  let the two lint runs disagree. An error would stop a project that passed
  before, which the version promise allows only in a major release.
- An untracked file that imports a tool changes the Imported by column only
  after its commit. The check now warns for that too: it reads the imports
  once more with the untracked files and compares the column. The kit owner
  met this case twice while building 5.2.0.
- Tried on a throwaway project: warning while untracked, the announced
  error after `git add`. `tests/test_capability_map.py` passes with 19
  tests. Full checks are not run yet; not released.

## 2026-11-15 — Release 5.1.0

- deivid gave the go: "oke lets move and release and clean up". The ask
  named what the go covers: moving `main` to the release state, the tag
  `v5.1.0` and the push of `main` and the tag, which publishes the kit's own
  site. It gave the size: 6 commits on `main`, 27 files changed, 806 lines
  added and 174 removed, a migration guide of 695 words and the snapshot
  `examples/global-agent-context.md` of 1,817 words, which becomes public.
- 5.1.0 holds the two changes of the entries below: the Reference section
  lists named folders only, and the optional snapshot of the owner's global
  agent instructions. Both were reviewed independently; neither review found
  a blocker, and their findings are fixed. The fixes from the second review
  were not reviewed again.
- This commit adds only this entry. Checks on it: `build`, `lint --strict`
  and `build --check-reader` of the kit pass, and
  `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` passes with 353 Python
  tests and seven browser suites.

## 2026-11-15 — An optional snapshot of the owner's global agent instructions

- Why: deivid asked for it in the 5.1.0 release: "we could add an optional
  choice for the person to add/override their global context with a
  snapshot of mine", then "add the snapshot just remove the personal thingas"
  and "the agent should also keep prompting the user if they want it if its
  not already overlaping until the users says no".
- `examples/global-agent-context.md` is his global agent file of 2026-11-15,
  1,754 words, with three passages changed: his user name, twice, and his
  full name with e-mail address now read "the user". Nothing else is
  removed; a first line marks the file as a snapshot and names what it
  assumes: the Caveman plugin, the Graphify skill and the owner's models.
- No command was built. The need is to let a person add the file or replace
  theirs with it; two shell lines in the README do that, the second keeping
  the old file. `README.md#optional-the-owners-global-agent-instructions`
  owns the description and the offer rule.
- The offer reaches agents through a section of the starter's `AGENTS.md`,
  so a new project offers it by default. An existing project copies the
  section in an optional step of the 5.1.0 guide; its owner decides. The
  kit's own `AGENTS.md` does not carry it. The owner's own global file holds
  the snapshot's headings, so he is not asked.
- A no lasts across sessions only as a line in the person's global file.
  The agent offers that line and writes it only on a yes to it; without it
  a later session asks again.
- `tests/test_global_context_snapshot.py` fails when the snapshot holds an
  e-mail address or a home folder path, or when the README section or the
  routes to the file are gone.
- Review of the delta since the first review: no blocker; the snapshot holds
  nothing that identifies a person. Two major findings are fixed in the
  README: the no was recorded in the global file without asking, and
  running replace twice overwrote the kept old file. Also fixed: add now
  starts on a new line; a global file that only imports or links to another
  is named; the Windows path pattern of the test; the exception to the
  version promise says "no known project"; the 5.1.0 guide says what the
  5.0.0 guide's opening warning means at 5.1.0.
- Not tested: whether agents ask as described; it rests on the agent
  following the starter's section.
- Checks: `build`, `lint --strict` and `build --check-reader` of the kit
  pass, and `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` passes with 353
  Python tests and seven browser suites.

## 2026-11-15 — The Reference section lists named folders only; prepare 5.1.0

- Why: after the release of 5.0.0 deivid asked whether the Reference section
  looks beyond `docs/` and said he had meant `docs/` only: "fix that i was
  talking about just docs and then we dont need the ref exclude no? or do u
  have a counterarg". The counterargument was measured: most records lie
  outside `docs/`. ADP has 329 tracked Markdown files, 95 under `docs/` and
  230 under `experiments/`; adaptation has 84, 20 under `docs/` and 61 under
  `studies/`; the kit has 63, 31 under `docs/` and 23 under `rules/`. With
  `docs/` alone both projects would lose the records he had asked to show.
- deivid chose the proposal "Yes, docs plus named": the default lists
  `docs/` only, a project names further folders, and `reference_exclude`
  goes. He was told that removing a setting 5.0.0 released makes this 6.0.0
  under the promise as written, and that no project is on 5.0.0 yet.
- The number: it was first prepared as 6.0.0. deivid: "this is a pretty small
  thing for 6.0", then "5.1 and add a new migration". It is 5.1.0, a minor
  release by his decision; the release notes state the exception to the
  promise and the fact it rests on, that no known project had moved to
  5.0.0.
- `reference_roots` names the listed folders and single Markdown files as
  plain paths; its default is `["docs"]`. A file is listed when it equals an
  entry or lies below it. An entry that lists no file gets a note.
  `reference_exclude` fails the build with a message that names
  `reference_roots`, `private_prefixes` and the 5.1.0 guide. The glob
  matcher that only `reference_exclude` used is deleted.
- The kit's own site sets `reference_roots = ["docs", "AGENTS.md",
  "THIRD_PARTY.md"]` and lists the same pages as before. The starter keeps
  the default, so a new project no longer lists its `AGENTS.md`.
- Records: `rules/site/authoring.md#automatic-reference-listing` and one
  sentence of `rules/site/publication.md` are rewritten; no heading changes.
  Release notes gain a 5.1.0 section, and
  `docs/topics/releases/migrations/5.1.0.md` is new, with one content step.
  The 5.0.0 guide gains a paragraph that sends a project moving on to 5.1.0
  to that step in place of its section "Settle what the Reference section
  lists". `VERSION` is 5.1.0.
- Review: an independent reviewer built 25 throwaway projects and found no
  file listed outside a root and none missed inside one; no blocker and no
  major finding. Fixed from its findings: a root whose only file is
  registered no longer gets the note that it lists nothing; four summaries
  now say that a set value replaces the default; the guide keeps the step
  table and the conformance check of the 5.0.0 guide for a project that
  comes from 4.0.0, names `reference_roots` as a new key, and deletes
  `reference_exclude` in the commit that moves the pin.
- Tests: fixtures that keep records outside `docs/` name their folders. New
  cases cover the default, a file outside the roots, whole path segments, a
  root that lists nothing and the removed setting.
- Checks: `build`, `lint --strict` and `build --check-reader` of the kit
  pass, and `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` passes with 350
  Python tests and seven browser suites.
- Not tagged and not pushed; the tag and the push wait for deivid's go.

## 2026-11-15 — Release 5.0.0

- deivid gave the go: "Yes, release 5.0.0". The ask named what the go covers:
  moving `main` to the release state, the number 5.0.0, the merge of the
  source-link fix branch `fix/local-source-links-20261114` (in `ee5ae78`),
  the tag `v5.0.0`, and the push of `main` and the tag, which publishes the
  kit's own site. It also gave the size: 56 commits after `v4.0.0`, 141
  files changed, 18,137 lines added and 1,116 removed, and a migration guide
  of 3,896 words.
- The release state was reviewed at `93d0b58`. The independent reviewer's
  verdict on the last fix: fit to release, no blocker and no major finding.
- This commit only closes records. `docs/open/release-5.0.0-waits.md` is
  deleted with its route: all three of its questions are answered. Its open
  points, with three more from the final reviews, are now in
  [known open after 5.0.0](open/known-open-after-5.0.0.md). The release
  notes no longer call the version number provisional. Two links to the
  deleted record in older entries below are now plain paths.
- Checks on this commit: `build`, `lint --strict` and `build --check-reader`
  of the kit pass, and `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh`
  passes with 347 Python tests and seven browser suites.

## 2026-11-15 — Show only raster images on automatically listed pages

- Why: a review of the allowlist found every listed page clean, in three
  browsers and against 14,000 fuzzed documents, but a listed file could
  still publish any tracked file as same-origin media. `<img
  src="media/evil.html">` or an SVG was copied to `_media/`, and opened at
  its address its script ran on the site's origin. Under the page lock the
  HTML file was sealed like a page, so a reader who had unlocked with
  "remember" got it opened and written, and its script read the remembered
  key.
- An automatically listed page now shows only PNG, JPEG, GIF, WebP and AVIF
  images, and a file counts only when its first bytes match its suffix.
  Any other type renders as `link-gone` with a note and is not packaged, so
  a listed file publishes nothing but its page and the raster images it
  shows. A `data:` image must be one of these types too. A link to a
  tracked file never packaged it, and nothing else on a listed page does.
- deivid confirmed the rule: "yes lets do 1". Two listed records of the
  kit's own site showed an SVG figure, `pileup-wide.svg`: the
  approval-failed-open record and its background. Both are now registered
  with `[[source_pages]]` tables and keep it, at
  `approval-failed-open-record.html` and
  `approval-failed-open-background.html`. Of adaptation's 81 tracked
  Markdown files, none listed today, 21 SVG references in five result
  records would not show if listed; 22 raster ones would.
- Also from the review: the shell's placeholders are filled in one pass, so
  `{{SCRIPTS}}` in a file's text no longer writes the scripts a second time;
  a link that a file opens in an HTML block ends with that block.
- Checks: `build`, `lint --strict` and `build --check-reader` of the kit
  pass, and `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` passes with 347
  Python tests and seven browser suites. The browser suite now also opens
  the SVG, HTML and misnamed files at their addresses; it passes in Firefox
  and WebKit and fails on the previous commit, which packages all three.

## 2026-11-15 — A run does not copy its environment

- deivid asked in ADP's session whether the kit now prohibits what a cleanup
  of ADP's build folder had just removed: "will the kit now prohibit it or do
  we need to add rules?", and answered "yes" to sending the rule to the kit.
- Reported by ADP's session, not checked here: the cleanup freed
  111,002,214,400 bytes in one deletion run, and about 136 GB in total when
  earlier deletions of the same day are added, summed from `df` and `du`.
  About 100 GB were four copies of environments: two sealed copies of 25.2 GB
  each, kept to prove exact bytes and used by several runs, a restored
  reference environment and a superseded one, 25 GB each.
- The rules on scratch files and on source copies did not name an
  environment. `rules/engineering/code.md`, Dependencies, now says that a run
  names its environment by package versions and file hashes and does not copy
  it, that a project keeps one environment per toolchain, and that an
  environment a new one replaces is proposed for deletion in the same change.
- The 5.0.0 release notes list the rule. Three sentences, written short on
  deivid's word that the rule text is growing too much. Not reviewed.
- Also noted: deivid looked at pages listed both in the navigation and in the
  Reference section and decided to keep the section as it is: "neh keep as is
  i was wrong".
- Checks: build and strict lint.

## 2026-11-15 — Admit only known raw HTML in automatically listed files

- Why: the kit promises that raw HTML in an automatically listed file runs no
  script and loads nothing from outside the bundle. Three reviews broke the
  filter behind that promise, each with input it did not know: event
  handlers, unquoted `javascript:` links, `srcset` and SVG `href`; then a CSS
  escape in `style` (`u\72l(…)`); then, verified in Chromium, Firefox and
  WebKit, a record that built the sidebar's tree box from `class` and
  `data-` attributes, so nav.js loaded an outside script on load (B1), and an
  image or poster address with a leading space, tab or newline that loaded
  from another host (B2). B1 shows why a filter that removes known-bad input
  cannot win: the kit's own components are driven by classes and `data-`
  attributes, so any class a record may keep is a way to drive them.
- The filter now admits known input. The Markdown renderer hands each HTML
  fragment of a listed file to `ListedHtml` in `tooling/source_pages.py`,
  while its own markup, classes and styles stay untouched. Listed tags keep
  listed attributes; any other tag shows as text; other attributes,
  comments, ids and names the kit's page uses and end tags that close
  nothing the file opened are dropped; the file's elements end inside the
  element around them. Every address is read as browsers read it
  (`browser_address`). A listed page no longer inlines SVG figures or turns
  on components from its text, and nav.js takes its tree box only from the
  shell's sidebar and loads only `reference.tree.js`.
- Also from the third review: lint compares link schemes without regard to
  case; the 5.0.0 guide's dead-link command decodes targets and skips `//`;
  the capability-map rule says that `init` writes the map.
- Effect: on the kit's own site one listed page changed, by an explicit
  `</p>` before a table cell ends, and nothing was refused. adaptation lists
  no file, since `.md` is one of its private suffixes.
- Checks: `build`, `lint --strict` and `build --check-reader` of the kit
  pass, and `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` passes with 344
  Python tests and seven browser suites. The new browser suite also passes in
  Firefox and WebKit; on the kit before this change it fails, as `evil.js`
  and five of the B2 addresses load from the stand-in host.

## 2026-11-15 — Correct and shorten the 5.0.0 guide and release notes

- Why: a review followed the 5.0.0 guide on a clone of adaptation and found
  steps that mislead, and deivid's concern stands: "we're bloating the docs".
- The guide: the listing check needs a passing build and fails on a
  `site-build.json` without `reference_tree`; a build error that names a
  removed or renamed setting is fixed in the step below and the agent comes
  back; narrowing a private suffix sends the agent back to the first step; the
  adapter file goes once a search finds no other user; links in pages locked
  by hash need an approved revision first; the Markdown link check no longer
  reaches records outside `docs/` that only the removed evidence settings
  brought in, and a command lists their dead links; the own-keys search
  includes `formula_check_required`; a file that exists on one machine only;
  where Playwright comes from. "Adopt the capability map" became the required
  "Set the tooling folders". The lists of changes that need no edit became a
  table of what a project's own checks meet and a command that lists the
  changed rule files. 4,558 words before, 3,867 after.
- Release notes: a seventh reason for a major release, the missing
  `tooling_roots`; `tooling_roots` joins the stable keys; the sections "Where
  code lives" and "Formula check" are named; the bleed fix links slide faces;
  one of adaptation's dead links is an ignored local file, not a missing one;
  the code fixes of this day are in their rows; lint timings measured by the
  code review are stated.
- Checks: listed in the entry "Fix the findings of the code review".

## 2026-11-15 — Settle the nine questions of the upgrades to 4.0.0

- Why: `docs/open/upgrade-to-4.0.0-findings.md` held nine questions for
  deivid. On the first he said: "i think its is low importance asking or not
  is fine", so no rule changed. On the rest: "you can settle them but with
  evaling if its worth even adding cuz we're bloating the docs". The kit's
  maintaining session settled them; these are its choices, not deivid's,
  except the user name in a path.
- Nothing added: which finished experiments the run-output rule covers; "no
  two faces share a layout" holds per page, as written; a face title states
  the finding, as written; a face may redraw the chapter's figure;
  `!important` on project slide classes and the home card picture stay under
  "Seen but not built" in the [capability map](KIT_CAPABILITY_MAP.md).
- Changed: the tone rule, see the next entry; the user name in a path, on
  deivid's word "username we dont do".
- The record keeps only the owed trial of the slide-face rule on adaptation's
  faces. The capability map drops four needs that are built and have rows.

## 2026-11-15 — Apply deivid's rule decisions and correct rule wording

- User names: deivid said "username we dont do". [Page design](../rules/writing/pages.md#page-design)
  now says a user name inside a path is a name and is replaced before the page
  is published; the 4.0.0 guide's step on names and "Documentation and
  writing" say the same.
- Tones: the slide-face rule no longer gives the accent and warm tones to the
  compared methods, because the kit's own figures use them otherwise; each
  tone keeps one meaning across a project's slides, and `is-alert` and
  `is-held` keep theirs. "Documentation and writing" follows.
- Wording that gave two readings: a face shape "one decisive number" is gone,
  since tiles of numbers are boxes; a reported path is a link's text and its
  target stays as the record writes links; "attempt" is each run of the
  experiment's procedure, the agent that finishes an experiment counts for
  the step-back review, and the running total is not one of the registries
  the workflow forbids; "Where code lives" copies reused code out of a
  finished experiment instead of moving it. "Documentation and writing" no
  longer makes a slide figure a view of a numbered chapter figure, and "Build
  a site" no longer gives a chapter card one visual.

## 2026-11-15 — Fix the findings of the code review

- Why: an independent review of the code and checks found two defects that
  block the release and fourteen minor ones.
- Automatically listed pages keep a `style` attribute only when it holds no
  parentheses, backslashes, quotes or slashes: a CSS escape such as `u\72l(`
  passed the old filter and loaded an outside address. Plain declarations,
  such as the build's line numbering on code blocks, stay.
- Formula check: a project's own math wrapper with a child element and no
  open delimiter is not a split; a Node that cannot run the compiler is a
  note unless `formula_check_required = true`; lint refuses a value of that
  setting that is not true or false; the compiler loads with `require('path')`;
  the rule says how to write a literal `$$`.
- Slide-face checks: only a tag with the attribute is a face, findings on an
  automatically listed page are notes, and "Figure 3.2" or "Section 4.1.2" is
  no number.
- Page lock: frames found through unquoted and root-relative addresses get
  the reference level; the comment on stored keys now says what the code does,
  which drops a remembered key whose salt differs, also for a cached old page.
- Lint skips protocol-relative links; the rule says only a double-quoted
  `href` is checked; `publish` counts the automatically listed Reference
  pages in its summary.
- Checks: build, `lint --strict`, `build --check-reader` and
  `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh`; results in the report of
  this work.

## 2026-11-15 — Wait for the reader's chapter slide before measuring faces

- Why: the documented loop, `goHash` then `assertSlideFaces` per chapter,
  measured faces while the reader's strip still moved. On the review's clone
  of adaptation it reported sideways overflow on 31 of 33 faces at 390 and at
  1600 px; after a fixed wait, none.
- `settle` now waits for every running transition and finite animation, and
  `slideFaces` settles first. The same loop on the same clone now reports no
  sideways overflow; 14 faces at 390 px and 7 at 1600 px keep drawing labels
  below 11 px. A new browser test fails with the old helper.
- Rows for faces the page does not show carry `chapter`, `shown: false` and
  `problems` only; the release notes and the guide say so.

## 2026-11-15 — Require the tooling folders in every project

- Why: the guide and release notes called the capability map optional while
  the rules required it. deivid, asked which: "Required".
- Every project sets `tooling_roots` in `docs/site/site.toml`; `[]` states it
  has no tooling, and lint fails without the setting. A project with tooling
  keeps the map, and the existing check applies. The starter sets `[]`.
- [The capability map](../rules/engineering/code.md#the-capability-map) keeps
  four sentences; the format, the check and the import reading moved to
  [capability map settings](../rules/site/authoring.md#capability-map-settings),
  as deivid agreed: "i agree with your code .md proposal". The subsection "The
  check" was never released and is gone. Name the need first says what it
  means in a project without tooling.
- Code review fixes in the same module: a file that does not parse warns only
  under a tooling or experiment root; a link with a title or an encoded space
  is read; the command keeps CRLF line endings; a folder without
  `__init__.py` is a package only when Python lies below it, and never under a
  standard-library name.
## 2026-11-15 — Land the approval-failed-open record and its page

- Why: a record drafted outside the repository explains how supporting code
  piled up in ADP, the project the kit was extracted from, and why several
  kit rules exist. deivid read the draft and its figure, agreed its length
  ("lets agree in the middle?") and asked for a page: "ill read it directly on
  the page with all the visuals and html styling so land it".
- Record: [approval-failed-open.md](topics/approval-failed-open/approval-failed-open.md)
  with [background.md](topics/approval-failed-open/background.md),
  [numbers.md](topics/approval-failed-open/numbers.md) and its script
  `numbers.py`, and the measurement in `topics/approval-failed-open/measurement/`
  (four CSV files, `method.md`, `events.md`, `summary.txt`, `run.log` and the
  five scripts), measured read-only from ADP `main` at `b8b80e0b`. Moved
  unchanged in substance: the draft comment is gone, links point to the new
  places, the record links the new open record, and background no longer says
  the two ideas are outside the open work. `numbers.py` now reads the
  measurement folder beside it by default, has `--check`, and adds four rows
  that only the figures draw (`prod_1110`, `frozen_now_lines`,
  `nr_other_commits`, `nr_other_lines`); its headline check compared the
  plans-only maximum, 50,588 words, with the all-text maximum, 51,556, and
  now compares it with `w_max_day_open`. Rerun after the move: 145 numbers,
  `numbers.md` current, every number of the record covered. In the copy of
  `method.md` the three longest path and keyword patterns stand in code
  blocks instead of inline code, because on its page at 1600 px they pushed
  the page 530 px wider than the window; their text is unchanged.
- Names and paths: the draft and the measurement name people by role; no
  personal name, e-mail address or home path with a user name was found in
  the files, data and scripts included. The scripts take the developer's
  handle as an argument and write "the developer" in its place; `method.md`
  and `approvals.py` show `/home/<user>` as the placeholder they write. Nothing
  was replaced.
- Page: [Approval that failed open](topics/approval-failed-open/index.md),
  in the navigation's practices group after the three practice pages it draws
  on. Eight chapters follow the record; six figures are generated by
  `draw_figures.py` beside the record from the measurement and `numbers.md`,
  which it checks every drawn number against, into
  `docs/site/fragments/approval-failed-open/`, each with a wide and an upright
  drawing; a seventh figure, the table of rules against piles, is in the page.
  The record's figure is now the generated `figures/pileup-wide.svg` with its
  upright version and manifest; the draft's PNG sketch was not landed.
  Measured statements, the developer's words and interpretation carry their
  own marks on the page. No slide faces: they wait for deivid's yes.
- Open work: two questions for deivid, whether an approval covers only what
  the ask said and whether an ask states the size of what it would build, in
  [approval-scope-and-ask-size.md](open/approval-scope-and-ask-size.md),
  routed from `KIT_OPEN.md`.
- Other records: the [website record](topics/website/website.md) lists the
  page and its own stylesheet; the 5.0.0 table of the
  [release notes](topics/releases/releases.md) has a row for the page and its
  record.
- Correction of the entry "Capability map, need first, running totals and a
  step-back review" of this day: it says the 18 attended sessions "used about
  3.8 hours of the person's time at the machine". 13,640.3 s is the summed run
  time of the 18 sessions, from ADP's attended-sessions record; the person's
  time was never recorded.
- Checks: `tests/own_site_review.cjs` listed the kit's pages for people as
  the five start and practice pages; the obsolete assumption was that no
  other page for people exists, and the new page joins the list.
  `tests/run_checks.sh` runs `draw_figures.py --check`, which runs
  `numbers.py --check`. The capability map's Imported by column for
  `svg_figures.py` now names `draw_figures.py`. Build, `lint --strict`
  (0 warnings), `build --check-reader` (6 reader pages) and
  `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` (316 Python tests, six
  browser suites) pass. The page's chapters were captured at 1600 and 390 px
  and looked at; every figure label renders at 11 px or more at both widths.
  The hash is assigned by the landing commit.

## 2026-11-15 — Close the gaps the upgrades reported in the guides and rules

- Why: the upgrades of adaptation and ADP to 3.2.0 and 4.0.0 reported gaps
  in the migration guides and rules, recorded in
  `docs/open/upgrade-to-4.0.0-findings.md` and
  `docs/open/adaptation-upgrade-findings.md`. deivid decided: "Fix them now".
  Each case was sorted into a wrong or missing step (corrected in every guide
  where it occurs), an unclear rule (one sentence made to say one thing), or a
  question of policy (left to deivid).
- The hard-coded `.build/docs-env/bin/python`, which a fresh worktree and ADP
  lack: the 4.0.0 guide's "Move the pin" and `--check-reader` command, the
  5.0.0 guide's "Move the pin", the 1.0.0 migration steps in the release notes
  and the README's "Pin and upgrade" now say "the project's documentation
  interpreter", and the 4.0.0 guide shows how to check one
  (`<python> -c "import mistune, pygments"`) and how to create it.
- Where the slide-face rule gave two readings: settled before today by the
  changed rule were which requirements fail a face (the three-group review),
  counts in boxes (a face without a real visual), drawn boxes (a drawing of
  the mechanism or a row of steps is a visual, a list in boxes is not), the
  missing measures (judgment by the validation rule; drawing labels now
  measured against 11 px) and the person's yes (asked for new faces only).
  Made to say one thing in [slide faces](../rules/writing/pages.md#slide-faces):
  tiles that hold only numbers are boxes; the factor grid has one column per
  option and one row per factor, and a list of levels is not such a grid; in a
  teaching chapter the finding is how the thing works. A question as a title
  goes to deivid.
- What the 4.0.0 guide step on faces left out: removing a face changes checks
  that count faces or hash pages, and faces are looked at in their reader
  chapter at the site's widths and in the deck; both are now in the step and
  were already in the 5.0.0 guide. Legend text cut off inside a figure is
  reported by `slideFaces` as clipped text since 5.0.0.
- The other gaps of the 4.0.0 guide, in the guide: a plan that a run hashed
  stands for itself by commit, path and hash, while an archived publication
  and copied tool sources are not finished working documents; the import of
  `tooling/svg_figures.py` by a figure generator is the provisional
  interface and stays, and scripts kept as evidence stay as written; scratch
  folders of other sessions are listed with path, date and size for the owner;
  a project that uses the chapter reader adds `--check-reader` to its checks;
  names on pages get a search through the names Git knows. Questions for
  deivid: a checkout out of step with its remote, a user name in a data path,
  and the bound of "each experiment reported as complete".
- ADP's gaps: a group colour set by project CSS stays with or without
  `[group_colors]`; a generator whose environment is gone is recreated from the
  setup guide or the figure waits for the owner; the import search leaves
  historical scripts; a notice the project writes itself for vendored data is
  named after its subject, in the guide and in
  [README is the bounded exception](../rules/documentation.md#readme-is-the-bounded-exception);
  a runner that refuses uncommitted paths commits the pin first, in the 4.0.0
  and 5.0.0 "Land the upgrade".
- Adaptation's six cases from its upgrade to 3.2.0: the 2.0.0 guide gains the
  steps for publication keys of the unreleased `101cea4`, the advice for a pin
  that cannot be fetched and the instruction to pin the newest release once;
  the 3.0.0 guide says a check compares asset URL paths without the query and
  that a page locked by hash needs an approved revision before a link is
  added. `home.css` needs no release note: every tag from `v1.0.0` to `v4.0.0`
  packages it only through a page's `page_css`, so no release changed it; what
  adaptation saw came from its unpushed pin `101cea4`, which this repository
  does not have. Importing the tooling as a library is settled by the 4.0.0
  guide, which says it is not stable and documents `DOCSITE_PROJECT_ROOT`.
- Records: `docs/open/adaptation-upgrade-findings.md` (63 lines) is deleted
  with its route, since none of its six cases is open; Git keeps it at its
  path in the commit before this one. `docs/open/upgrade-to-4.0.0-findings.md`
  keeps nine questions for deivid, each with options and a recommendation,
  and the owed trial on adaptation's faces. The capability map lists two more
  needs seen but not built, a chapter figure on a face and project slide
  classes without `!important`. The open record of the release no longer
  lists the kit's example faces as unseen; deivid accepted them today. The
  5.0.0 release notes list the clarified rules, and the 5.0.0 guide's reread
  list names them; "Documentation and writing" follows in three sentences.
- Every heading under `rules/` at `v4.0.0` and at `976e5cd` is still present.
- Checks: build, `lint --strict` (0 warnings) and `build --check-reader`.

## 2026-11-15 — Measure drawing labels on slide faces

- Why: `slideFaces` passed a face whose SVG labels render at a few pixels at
  390 px, because a wide drawing shrinks into the phone column with its text.
  [Figures](../rules/writing/figures.md#figures-and-comparisons) already says
  that charts carry labels of at least 11 px; the check uses that number.
- What: per shown face, `slideFaces` reports `drawingText`, the smallest
  rendered size of a label in the face's inline SVG drawings (font size times
  the drawing's scale on screen), with its text and the number of labels
  below 11 px, or null. A label below 11 px is a problem, so
  `assertSlideFaces` fails on it at every width. An SVG loaded as an image is
  not read.
- Found, with the helper at 1600 and 390 px, after each chapter settled:
  - the kit's four example faces pass. Smallest labels: "Get started" 14.7 px
    wide and 12.2 px at 390; "Build a site" 14.3 and 12.2; the starter's
    slide-face face 13.9 and 11.4; the starter's ownership face is a matrix in
    HTML and has no SVG labels.
  - adaptation, a clone of `e28472e` built with this kit after removing its
    adapter settings in the clone: 33 faces, 25 on `cursor-rerun` and 8 on
    `robotics`; 14 carry SVG labels. At 1600 px 7 of them fail, 173 labels in
    all, the smallest 7.4 px on `robotics#curves`; at 390 px all 14 fail, 394
    labels, the smallest 2.3 px on `cursor-rerun#evidence-families` (an
    11 px font in a drawing scaled by 0.21). The first pass of the scratch
    harness also reported sideways overflow on 31 faces at 1600 px; it came
    from measuring before the reader's chapter transition ended and is gone
    with a wait, so it is not a finding.
- Rules and records: [reusable browser checks](../rules/site/validation.md#reusable-browser-checks)
  describes `drawingText`; the [slide-face rule](../rules/writing/pages.md#slide-faces)
  says the labels keep the 11 px at every width; the 5.0.0 release row, the
  migration step on slide-face checks, the open record of the release, which
  lists adaptation's case, and one sentence on "Documentation and writing".
- Tests: `tests/test_browser_checks.cjs` adds a face whose drawing labels
  fall below 11 px at 390 px and pass at 1600 px; with the new problem
  disabled the suite fails.

## 2026-11-15 — Compile every formula on the built pages in lint

- Why: ADP keeps its own test, `tools/docs/test_content_math.cjs`, that
  compiles the formulas of its built pages with the kit's KaTeX and fails on
  one that does not compile or that Markdown split. The need is general and
  the capability map did not list it. deivid decided: "lets move it to kit".
- What: `docsite.py lint` reads every built page that loads the kit's math
  renderer and finds the formulas as the vendored auto-render does: in the
  `content` element, in runs of adjacent text outside `pre`, `code`,
  `script` and `style`, between `$$` or `\(` and their closing delimiter
  with braces balanced. `tooling/formula_compile.cjs` compiles them in one
  Node process with `theme/assets/vendor/katex/katex.min.js`. Errors: a
  formula that does not compile, with KaTeX's message; a formula that
  Markdown split, ADP's guard, now for every page; an opening delimiter not
  closed in the same text. Each names the page's source, the built page and
  the formula. Lint then prints how many formulas compiled with which KaTeX.
- How it runs without breaking the promise that building needs no Node.js:
  inside lint, as its one Node step, rather than as a helper a project calls
  like the browser checks. Inside lint every project with Node gets the check
  without adding anything, and a project with its own test can drop it. Node
  is `DOCS_NODE` or `node` on `PATH`; a `DOCS_NODE` that names nothing is an
  error. Without Node lint prints a note and passes, so building and linting
  still work without Node. A project whose checks must not skip it sets
  `formula_check_required = true` in `site.toml`; lint then fails without
  Node, so its CI cannot pass silently. The kit's own site sets it.
- Level: an error, as decided for 5.0.0; a formula that does not compile
  shows as raw text on the page.
- Trials, all with KaTeX 0.16.11:
  - the kit's site: 5 of 5 formulas on 1 page compile; the starter: 3 of 3
    on 1 page;
  - adaptation, a clone of `e28472e` built with its pin `v4.0.0` and again
    with this kit after removing its two adapter settings in the clone: no
    page sets `math = true`, so 0 formulas;
  - ADP, its existing build output from 2026-11-15 read in place, ADP at
    `b8b80e0b`: 396 of 396 formulas on 8 pages compile, 310 inline and 86
    display. ADP's own test reads the same pages as 355 formulas, 269 inline
    and 86 display: the 41 more are `\(…\)` formulas written in raw HTML,
    which its pattern for the build's wrapper does not see. No formula is
    split or unclosed.
- Rules and records: the new section [formula check](../rules/site/authoring.md#formula-check),
  a sentence in [mathematical explanation](../rules/writing/math.md#mathematical-explanation)
  and in [validation and review](../rules/site/validation.md#validation-and-review),
  the README's Node.js paragraph, a reason, a lint row and the stable key in
  the 5.0.0 release notes, the step "Fix formulas that do not compile" in the
  migration guide, a row and a seen-but-not-built entry with the decision in
  the capability map, a commented setting in the starter's `site.toml`, and a
  sentence on "Build a site" and "Documentation and writing".
- Tests: `tests/test_formula_checks.py`, 15 tests, among them a broken formula
  in a starter project that fails `docsite.py lint` with its page. With the
  call in lint disabled, that test fails.
- Checks: build, `lint --strict` (0 warnings), `build --check-reader` and the
  316 Python tests.

## 2026-11-15 — The kit keeps its name; close the open record

- Decision 2026-11-15 by deivid on the open question of the kit's name, raised
  on 2026-11-10: "we leave it". The site stays "Documentation kit", the README
  and `AGENTS.md` keep "Engineering and documentation kit", the repository
  stays `documentation-kit` and the folder in every project stays `.docs-kit`.
- What the record held, for whoever raises the question again: about a quarter
  of the rule text, measured in words on 2026-11-10, is about engineering,
  experiments and delivery rather than documentation. Names proposed and not
  accepted: Shared practices kit, Working agreements kit, Agent practices kit,
  Project practices kit, Engineering and documentation kit, and handbook or
  playbook variants. A display title costs one setting; the repository name
  changes the public site URL; the folder `.docs-kit` would break every
  project.
- `docs/open/kit-name.md` is deleted with its route in `docs/open/KIT_OPEN.md`,
  as the rule on [finished working documents](../rules/records.md#finished-working-documents)
  asks; deivid was told it would be. Git keeps it at its path in the commit
  before this one.

## 2026-11-15 — Sync three pages with the removed adapters and kept copies

- Sentence-level sync after the removal of the adapter hooks and of
  `evidence_manifests` and `legacy_files`; lint listed these pages for reread.
- "Documentation and writing": the project's path adapter no longer maps an
  old path for lint; a later `worklog_links_checked_from` does that for
  worklog entries, as [rendered pages are for people](../rules/documentation.md#rendered-pages-are-for-people-records-stay-markdown)
  says. The fold on the archive staging layer said a byte-exact copy of a
  superseded document may be kept; since 4.0.0 none is, and Git keeps the
  bytes.
- "Build a site": the reference-guide table no longer names adapters or path
  adapters; the resources row names old links in the worklog instead.
- "Get started": the route for existing documentation said Markdown is
  published as registered records; since the automatic listing every tracked
  Markdown file becomes a source page unless excluded, and the example says
  the project settles what the Reference section lists.
- Checks: build, `lint --strict` (0 warnings) and `build --check-reader`. Text
  only; no capture was taken.

## 2026-11-15 — Give the built-page source map a public name

- `tooling/lint.py` imported the private `_page_names` from
  `tooling/slide_face_checks.py` to name the source of a built page. The
  function maps built pages to sources and has nothing to do with slide faces,
  and the formula check needs it too, so it moved to
  `tooling/topic_structure.py` as the public `page_sources(root)`. Lint and the
  slide-face check import it from there; behaviour is unchanged.
- The capability map's row for `topic_structure.py` names the need. A new test
  in `tests/test_record_notes.py` checks the mapping for a topic page with its
  own slug, a plain topic page and a source page from `site-build.json`.
- Checks: build, `lint --strict` (0 warnings) and the 301 Python tests.

## 2026-11-15 — Remove `evidence_manifests` and `legacy_files` in 5.0.0

- Why: both settings served the practice that the rule on finished working
  documents ended in 4.0.0, keeping old documents as copies in the live tree.
  `evidence_manifests` declared collections of copies that had to stay byte
  for byte; `legacy_files` mapped single old paths to current files and was
  described in no rule. No project sets either: ADP, adaptation and Tempo
  were read on 2026-11-15, and neither the kit's own `docs/site/site.toml`,
  the starter's `site.toml.tmpl` nor any test fixture other than one lint test
  sets them. Asked whether to remove both in 5.0.0 with the adapter hooks,
  deivid answered: "Yes, remove both".
- A `site.toml` that names either setting now fails the build with
  `site.toml: <setting> was removed in kit 5.0.0`, which points to the
  migration step "Remove the adapter hooks", and lint prints that error.
- Removed with them: `tooling/evidence_documents.py` (68 lines), the
  verification of declared collections at the start of lint, the resolution
  of a copy's links from its original path, the worklog handling of a
  collection's recorded `source_root` and relocated targets, and the
  `legacy_files` and recorded-roots parts of the path resolution in
  `tooling/site_paths.py`. What stays: the mapping of the logical `docs/html/`
  origin to the build output, which every page link needs, now named
  `resolve_site_path`; `worklog_links_checked_from`; and the declared local
  evidence of `local_artifacts_manifest` and `local_media`, which serves files
  that exist on one machine only, not kept copies.
- Rules and records: [resources](../rules/site/resources.md#resource-closure-and-evidence)
  names the four removed settings and checks a stated hash against the file at
  its commit; the 5.0.0 release notes, the migration step, the capability map,
  `README.md` and `docs/KIT_CONTEXT.md` follow. The
  [frozen-record record](open/simplify-frozen-record-machinery.md) is reduced
  to adaptation's cleanup at its upgrade, which is all that remains; it is kept
  rather than deleted because two worklog entries of 2026-11-15 link it, and
  deleting it would mean moving `worklog_links_checked_from` past today.
- Tests: `tests/test_portability.py` checks that each setting fails build and
  lint with the message. Two tests went: the lint test of a byte mismatch in a
  declared collection, and the test that a relocated document resolves its
  links from its original path. Both encoded the assumption that the kit
  keeps and checks copies of old documents, which no longer holds.
- Checks: build, `lint --strict` (0 warnings), `build --check-reader` and the
  300 Python tests.

## 2026-11-15 — deivid accepts the four example slide faces

- Shown the old and the new faces side by side at 1600 px and the new ones at
  390 px, deivid answered "Yes, accept".
- One label on the starter's slide-face face still said "a view of the
  chapter's figure", the wording that the rule dropped when a chapter's
  figures became material for a face. The face, its narrow drawing, both
  aria labels and the Figure 4 caption now say that the visual shows the
  finding and is drawn from the chapter's figures and numbers.
- Decisions of the same day: all three adapter hooks are removed in 5.0.0
  ("remove all 3"); the guide gaps from the upgrades are fixed before the
  release ("Fix them now"); the check that every formula on a built page
  compiles moves from ADP into the kit ("lets move it to kit"); the HTML link
  check is added ("add it"); the kit's name stays ("we leave it").
- Checks: build, strict lint and `build --check-reader`. The browser suites
  were not rerun after the label change.

## 2026-11-15 — The kit's four example slide faces redesigned

- Why: deivid decided that the kit's own example faces are redone before the
  release: "redo them". The four faces, built on 2026-11-12, followed the
  arrangement the rule has since dropped (figure on one side, numbered points
  beside it, a row of facts below) and looked alike. The starter's faces are
  the first an agent sees in a new project.
- Each face now takes the layout that the shape of its finding asks for, and
  no two share one:
  - "Get started": a rule fixed once in the kit reaches each project that
    moves its pin, and a copied rule never gets it. A sequence in time with
    three consumers, so one timeline across the canvas, with the copied
    rule, project A and project B hanging from the revisions they took.
  - "Build a site": tracked Markdown in, a checked, self-contained site out,
    with the two things that never happen as its limit. A one-way flow, so
    one pipeline across the canvas above two ruled conclusions.
  - Starter, ownership chapter: who writes which folder and when it changes.
    Three parts compared factor by factor, so a three-by-three matrix.
  - Starter, slide-face chapter: a face is a view of its chapter. A detail
    and its place, so the face drawn large beside the chapter card it opens,
    with a chapter without a face as the smaller limit.
- The frame is unchanged: label row, title, scope line, type roles and
  tones. The four faces carry no lead sentence. `theme/components/slide-face.css`
  is unchanged. Each face keeps its local classes in a `<style>` element
  inside the face, so they travel into an extracted deck; below 720 px the
  matrix stacks into cards and the drawings give way to upright versions.
- The starter's Figure 4 lost the text tiles beside its visual, which taught
  the old arrangement; its chapter, the record `guide.md`, the two fragment
  comments, the slide list on "Build a site" and three sentences on
  "Documentation and writing" now describe the new faces.
- `tests/test_slide_face_checks.py` named the old title of the starter's
  slide-face face; it now names the new one. The obsolete assumption was that
  example face's wording, not any behaviour of the check.
  `tests/own_site_review.cjs` clicked the first drawing on the presented face
  to open the lightbox and assumed it was shown; below 720 px the wide
  drawing gives way to the upright one, so the test now clicks the drawing
  that is shown.
- Checks: `build`, `lint --strict` (0 warnings), `build --check-reader` and
  `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` with 288 Python tests and
  six browser suites pass. Reviewed by eye in the page at 1600 × 1000 and
  390 × 844 and in the Presentation view at 1600 × 1000; deivid has not yet
  looked at them.
## 2026-11-15 — Lint checks HTML links to repository files

- Decision: deivid decided to add the check to 5.0.0; his word: "add it".
  5.0.0 is a major release, the only kind that may add a lint error. The open
  record held the evidence: on 2026-11-09 the 2.0.0 starter home page linked
  a `PROJECT_CONTEXT.md` that did not exist, and on 2026-11-10 a reviewer put
  an HTML link to a removed kit anchor into a page body; strict lint passed
  both.
- How it works: the build already resolves every link from a page to a
  repository file in `SiteBundle.rewrite_page` and marks it with
  `data-repo-path` and `data-repo-fragment`, with a source remote and without
  one. `check_source_links` in `tooling/lint.py` reads those marks in the
  built pages, so it uses the build's resolution and no second resolver: the
  target must exist, a fragment into a Markdown file must match an anchor
  from `md_anchors`, and one into an HTML file an `id`, as for a Markdown
  link. It covers topic pages, the fragments they include and registered
  source pages. A link that the Markdown check already checked in the same
  source is left to it, so each dead link is reported once; without a source
  remote the built relative link is no longer also reported as `dead relative
  href`. On an automatically listed page a problem is a note; in the worklog's
  page the entries before `worklog_links_checked_from` are skipped; a file
  listed under `omitted_files` gets a note. The page's source comes from the
  mapping `slide_face_checks._page_names` already builds, imported rather
  than copied.
- Level: an error. No class of links was found that the kit's resolution
  cannot decide. Its limits are those of the Markdown check: an existing file
  that Git does not track passes, although its published source link leads
  nowhere, and a link into a submodule that is not checked out fails.
- Measured with this check, links counted once per built page:
  - The kit: 1 HTML link in a topic page and 11 links on automatically listed
    pages that no Markdown check covers, 0 failing.
  - adaptation, cloned at `e28472e` into a scratch folder, its kit submodule
    checked out at its pin `df089ef`, its two adapter settings removed and
    built with this kit: 78 HTML links on its three topic pages (94
    occurrences), 42 failing; Markdown links: 322 checked, 0 failing. Each
    failing link was given to adaptation's own `docs/site/layout_paths.py` to
    classify it. 34 name an old path that the adapter mapped to a tracked file
    (for example `configs/cursor-rerun-v2.json` to
    `studies/cursor/configs/cursor-rerun-v2.json`, and 20 links to
    `minigroot/reports/` on the robotics page). 7 name an old path that the
    adapter mapped to a file listed under `omitted_files`, which would have
    been a note. 1 is dead: `results/cursor-exploration-next-2026-10-29/digest-profile/review.json`,
    which the adapter leaves alone and which exists neither in the clone nor
    in the live checkout. None is a fault of the check. With the adapter
    removed by deivid's decision, the 41 are adaptation's cleanup at its
    upgrade: repoint each to its current path. The kit owner's rough count,
    83 links with 40 unresolved, used a script that ignored the adapter.
  - ADP: no clone and no build, as deivid decided. The check's functions ran
    on ADP's last build output, written on 2026-11-15 at 02:38 by its pinned
    kit 4.0.0, and on its sources in place, with bytecode writing off; no file
    in ADP changed during the run. 129 HTML links in topic pages (167
    occurrences) and 2,582 Markdown links, 0 failing. No topic page or
    fragment was newer than that build output; 6 other files under `docs/`
    were. The kit owner's rough count was 173 links with 0 unresolved.
- Tests: new `tests/test_source_links.py`, 8 tests on a fixture project: a
  dead target and a missing anchor in a page body, a dead target in an
  included fragment, a missing anchor in a registered page, one report per
  link without a source remote, a note on an automatically listed page, and
  old worklog entries skipped. Against the previous `lint.py` 7 fail; the
  eighth is the clean case. `tests/test_source_pages.py`
  › `test_no_remote_source_links_build_lint_and_export_locally` expected
  `dead relative href` for a missing Markdown link target; that encoded the
  assumption that the built-href check reports source links in a project
  without a remote. It now expects the Markdown check's message once and no
  `dead relative href`.
- Rules: `rules/site/authoring.md` › Authoring paths describes the check and
  › Registered source pages names it; `rules/site/validation.md` lists it
  among the lint checks. No anchor changed.
- Records: the 5.0.0 release notes give the new error as a fifth reason for
  the major release, with the measurements, and gain a row; the migration
  guide gains "Repoint or remove dead HTML links" with its row; the
  capability map records deivid's decision on the need; the release-waits
  record notes that his two decisions of this day make the release major on
  their own. `docs/open/lint-html-source-links.md` and its line in
  `docs/open/KIT_OPEN.md` are deleted, as the record and the rule on finished
  working documents ask.
- Checks after the last code and test edit of the day: on the kit
  `docsite.py build`, `lint --strict` (0 warnings) and `build --check-reader`
  (5 reader pages); `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` exits 0
  with 301 Python tests and the six browser suites, each run alone under a
  4 GB memory limit after another agent's browser run had finished. This
  worklog text was the only edit after that run.

## 2026-11-15 — Remove the path and evidence adapter hooks

- Decision: deivid decided to remove the kit's three adapter hooks,
  `path_resolver`, `evidence_validator` and the evidence adapter's
  `document_origin`, in 5.0.0. Asked which of three options, he answered
  "remove all 3". Why, with evidence, is in
  [the frozen-record record](open/simplify-frozen-record-machinery.md): the
  hooks let a project keep old documents as unedited copies in its live tree
  and still pass the link check, which the rule on finished working documents
  ended. State read from each `docs/site/site.toml` on this day: adaptation
  names `path_resolver` and `evidence_validator` (`docs/site/layout_paths.py`);
  ADP and Tempo name no hook; no project sets `evidence_manifests` or
  `legacy_files`.
- Removed: in `tooling/site_paths.py` the adapter loading and the per-run
  answer cache added on this branch (16 lines out); in `tooling/lint.py` the
  evidence adapter swap and the `document_origin` branch of
  `markdown_origin` (21 lines out); in `tooling/build.py` the exception
  handling that treated an adapter error on an automatically listed page as
  "no mapping". No file is deleted.
- Kept, with what needs it: `tooling/project_extensions.py`, which also loads
  `content_transform`; `resolve_legacy_path` in `tooling/site_paths.py`, now
  the kit's own resolution only (build output alias, `legacy_files`, and the
  recorded roots of evidence collections); `tooling/evidence_documents.py` and
  the relocation and worklog handling in `tooling/lint.py`, which the kit's
  own `evidence_manifests` setting drives, not a hook. The record's plan named
  that worklog handling as going with the hooks; `worklog_links_checked_from`
  replaces it only for entries before its date, so it stays while
  `evidence_manifests` stays. Whether `evidence_manifests` and `legacy_files`
  also go is left to deivid in the record. Automatically listed pages still
  ask the kit's own resolution, as every other page does.
- New: the build fails on `path_resolver` or `evidence_validator` in
  `site.toml` with `site.toml: <setting> was removed in kit 5.0.0`, naming the
  migration step "Remove the adapter hooks"; lint prints the build's error.
  The adapter module is never executed.
- Tests: `tests/test_portability.py` checks that each removed setting fails
  build and lint with that message and runs no module, and that the project
  builds again without it. The test that the kit used a project's adapters is
  gone, because it encoded the removed behaviour. The two tests that an
  untracked or symlinked module is refused before it runs now name
  `content_transform`, the remaining user of the same loader; they assumed
  `path_resolver` only as a convenient key. In `tests/test_lint.py` the two
  `document_origin` tests are replaced by one test of the relocation fallback
  that remains.
- Rules: `rules/site/resources.md` › Resource closure and evidence describes
  the kit's own resolution and the removal instead of the adapters;
  `rules/documentation.md` › Rendered pages are for people names a later
  `worklog_links_checked_from` instead of the path adapter for dated links;
  `rules/conformance.md` item 9 no longer names a path adapter as an example.
  No anchor changed. Not synced, because another agent is redesigning these
  pages: the writing-practices page still says the path adapter maps old
  paths for lint, and the build-a-site page's table names adapters and path
  adapters.
- Records: the 5.0.0 release notes give the removal as a fourth reason for
  the major release, replace the adapter cache row with the removal row, and
  mark the two settings removed in the list of stable interfaces; the 5.0.0
  migration guide replaces "Check the path adapter" with "Remove the adapter
  hooks", where each deletion of a document stays the owner's decision; the
  frozen-record record gains the decision and a new next step, and its route
  in `docs/open/KIT_OPEN.md` says what remains; `docs/KIT_CONTEXT.md` and the
  resources page description follow; the capability map row of
  `project_extensions.py` now names the content transform.
- Checks before the commit: on the kit `docsite.py build`, `lint --strict`
  (0 warnings) and `build --check-reader`; the starter builds and lints
  strictly; 293 Python tests pass. The browser suites run after the last
  change of the day.

## 2026-11-15 — Plot toggle chips in the zoomed figure

- Decision: deivid asked for the fix before the 5.0.0 release ("fix now").
- Grey dots, cause confirmed: the lightbox calls `buildChips` on its clone of
  the figure before the clone is in the page. In Chromium a detached path's
  computed `stroke` is the empty string (probe: page figure
  `rgb(228, 87, 46)`, detached clone `""`, the same clone attached
  `rgb(228, 87, 46)`), so `strokeOf` fell back to `#9aa4b2`. Fix in
  `theme/components/plot-toggles.js`: a chip's dot takes its colour from the
  page figure's group when there is one, which is the case in the lightbox.
- Wrapped label, cause found: the zoomed figure's chip bar was placed with
  `left: 50%` and `translateX(-50%)`, so its width was limited to the right
  half of the window, about 195 px at 390 px, and a chip's label broke inside
  it. Fix: the bar in `theme/components/lightbox.js` spans the window less 4vw
  on each side and wraps whole chips; `.fig-chip` keeps its label on one line
  (`white-space: nowrap`). The bar ignores pointer events and only the chips
  take them, so a click beside the chips still closes the zoomed figure, as
  before when the bar was only as wide as its chips.
- Built scratch page with the kit theme at 390 px, before: every dot
  `rgb(154, 164, 178)`, and the chips "Menger joints (default)" and
  "least-squares fit (smoothed)" 62 px high, two lines, against 44 px for one
  line; after: each dot in its series colour, every chip 44 px high, and the
  bar in three rows of whole chips. At 1600 px the four chips stand in one row
  before and after; only the colour changed.
- Test: `reviewPlotToggleChips` in `tests/test_browser_checks.cjs` loads the
  real `plot-toggles.js` and `lightbox.js` with five series coloured four ways
  (stroke attribute, a class styled inside the SVG, fill only, a path inside a
  group), opens the zoomed figure at 1600 and 390 px, and checks the dot
  colours on the page and zoomed, one line per label, chips inside the window,
  more than one row at 390 px, and that a zoomed toggle still hides the page
  group. Against the old two files it fails on the grey dots; with only the
  colour fix it fails at 390 px on the label "least-squares fit (smoothed,
  5-point window)", which the fixture uses because its system font is
  narrower than the kit's and "Menger joints (default)" alone fits there.
- Reviewed by eye: the zoomed figure with its chips on the built scratch page
  at 1600×1000 and 390×844 after the fix, and the test fixture at both widths.
  Dots match the lines; labels sit on one line; at 390 px the chips wrap
  under each other centred and stay above the figure.
- Rules: `rules/site/authoring.md` › Authoring paths says the dot has its
  series colour in the lightbox too, and that labels stay on one line while
  the bar wraps whole chips. No anchor changed.
- Records: `docs/open/plot-toggle-chips-in-lightbox.md` and its line in
  `docs/open/KIT_OPEN.md` are deleted, as the record asked; the 5.0.0 release
  notes gain a row and name `lightbox.js` and `plot-toggles.js` among the
  shared files with a new `?v=` query. No capability map row changes; the
  theme is not a tooling root.
- The entry of 2026-11-14 "Close the findings of the review before the 4.0.0
  tag" links the deleted record, and the worklog is not rewritten, so
  `worklog_links_checked_from` in `docs/site/site.toml` moves from 2026-11-12
  to 2026-11-15, as the resources rule asks. Lint no longer checks links in
  the entries of 2026-11-12 to 2026-11-14; on the worklog's page a link there
  whose target is gone shows as unlinked text.
- Checks before the commit: on the kit `docsite.py build`, `lint --strict`
  (0 warnings) and `build --check-reader`; `tests/test_browser_checks.cjs`
  and `tests/visual_review.cjs` pass, each run alone under a 4 GB memory
  limit. The other browser suites run after the last change of the day.

## 2026-11-15 — A marker inside a code block stays text

- Decision: deivid asked for the fix before the 5.0.0 release ("fix now",
  recorded in the entry on his decisions below).
- Cause, reproduced before the change: `markers_to_callouts` in
  `tooling/build.py` rewrote every marker at line start before Markdown was
  rendered, inside fenced code blocks too. A fixture page with markers in
  three fences failed the build with `chapter layout: Mismatched document
  closing tag: div`; rendered without the reader, the block showed the card's
  opening tag as code and a stray `</div>` followed it.
- Fix: the conversion now runs only on the text between fenced blocks.
  `fenced_spans` in `tooling/worklog_entries.py`, which already found the
  fences for the worklog's dated headings, is now public and is the one fence
  reader for both; it covers backtick and tilde fences, a closing fence at
  least as long as the opening one, and a fence left open to the end. A marker
  paragraph that runs into a fence without a blank line now ends where the
  fence starts, with a blank line written after the card so the fence is not
  swallowed by the card's HTML block.
- Lint, the second case of the open record: `check_markers` warned about a
  line that named the markers in code spans when the line also held bold
  text, as ADP met on 2026-11-11, and `lint --registry` listed markers inside
  code. Both now read the line with fenced blocks and code spans blanked, so
  the registry lists what the build turns into cards, plus markers that stay
  text outside code (list items, quotes, inside a sentence).
- Left as they are, with the reason in the rule text: a marker in a list item
  or a quote stays a bold label, because a card is a block of its own and the
  conversion does not parse containers; a marker without a blank line after
  it takes the following lines into its card up to the next blank line or
  fence, which is how Markdown continues the paragraph. `rules/documentation.md`
  › Rules for changes and chronology now says both, and that a marker inside
  a fenced block or code span is an example that stays text. No anchor
  changed. The writing-practices page explains this rule; its sentences stay
  true and were not touched, because another agent is redesigning that page.
- New `tests/test_markers.py`, six tests on a fixture page: cards only outside
  code, markers kept in a backtick fence, a tilde fence holding a shorter
  backtick fence, a fence after a card and an open fence at the end; the list
  item keeps its label; the registry and the warning skip code. With the old
  `build.py` and `lint.py` five tests fail; with the old `lint.py` alone two.
- Records: `docs/open/marker-in-fenced-code.md` and its line in
  `docs/open/KIT_OPEN.md` are deleted, as the record asked once the defect is
  closed. The capability map gains a row for finding fenced code blocks; the
  5.0.0 release notes gain a row.
- Checks before the commit: on the kit `docsite.py build`, `lint --strict`
  (0 warnings) and `build --check-reader` (5 reader pages); the starter
  builds and lints strictly; 294 Python tests pass, 288 before plus the six
  new ones. The browser suites were not run for this change, which touches no
  theme file; they run after the last change of the day.

## 2026-11-15 — Decisions by deivid on the open list

- The step-back review after every third finished experiment: "Yes, every
  third".
- Five choices the implementer of 4.0.0 made on its own stay as released: old
  worklog entries also tolerate a missing image and a stale anchor; a wrong
  date in `worklog_links_checked_from` fails the build; `[plot_toggle_labels]`
  is a stable setting; `DOCS_CHROMIUM` is removed; `package.json` has no name.
  His word: "thats fine".
- The kit's own four example slide faces are redone under the changed rule
  before the release: "redo them".
- The two open defects, a marker inside a code block and the chips in the
  zoomed figure, are fixed before the release: "fix now".
- No trial build of ADP with the new Reference default before the release:
  "we wont run the build now". ADP's first build with it happens at its
  upgrade. ADP's tracked tree is 6.59 GB in 84,850 files; its 329 Markdown
  files are 6.1 MB.
- Deleted with his yes: 15 old log files and the folders
  `experiment-guides-20261107`, `page-tools`, `qa` and `review` under
  `.build/`, and the two merged agent worktrees with their branches.
  `.build/panel-switcher` stays; a current test writes there.

## 2026-11-15 — Lint and browser checks for slide faces

- Decision: deivid decided to build the slide-face checks in the kit before
  the 5.0.0 release. Asked "Before or after?", he answered "before". The
  capability map had listed them under "Seen but not built" with "Decision:
  not taken".
- Why: adaptation wrote its own test that every number on a face appears in
  its chapter, two faces in one chapter built without a word, and six
  stacking faults below 720 px were found only by eye, as that project's
  session reported in
  [the slide-face findings](open/upgrade-to-4.0.0-findings.md#tooling-a-project-had-to-build-itself-for-slide-faces).
  `tooling/number_ledger.py` was removed on 2026-11-09 (`0550cbf`) because it
  needed a hand-kept list and no project imported it, so the new check needs
  no list from the project.
- `tooling/slide_face_checks.py`, lint check 14, reads the built pages. A
  chapter with more than one face, a face that does not open its chapter and
  a face outside every chapter are errors. A number that a face shows and its
  chapter does not show outside the face is a warning, which fails
  `--strict`. `data-face-only="<reason>"` on an element holding exactly one
  number accepts it as a note; a mark without exactly one number, without a
  reason or no longer needed is a warning. The module's description lists
  every normalisation and exemption. `slides.py` gains
  `chapters_with_faces`, shared with the deck's chapter selection.
- Trial before the rules were settled, with adaptation cloned and built with
  this kit in a scratch folder, never in its checkout: the kit's site has 2
  faces, the starter 2, adaptation at `e28472e` 33. The first version found
  20 numbers in 4 warnings on adaptation, all false: text was joined across
  inline elements, so "Mean error" followed by 3,975,163,966 read as a name
  and then 975163966, and chapters' `noscript` fallbacks were skipped,
  which hid a results table. Changed: text splits at every element, a
  `noscript` fallback is read, and digits after a separator that does not
  start a group of three are not read. Compared with adaptation's own test,
  which passes, the check read 341 face numbers and that test 338; the only
  numbers the test read and the check skipped were "step 50 of 200" and
  similar, which an exemption for "Step" followed by a number had removed. The
  exemption was dropped. Final result: 0 findings on all 37 faces. Inserting a
  number the chapter lacks into each of adaptation's 33 faces gave 33
  warnings. Older adaptation revisions built with this kit: `09ec123`, the
  old/new comparison, gave 30 errors for its 30 chapters with two faces and no
  number finding; `1b0b3f1` (36 faces) and `b6e9431` (30 faces) gave nothing.
  No real number fault was found.
- `slideFaces` in `tooling/browser_checks.cjs` now measures faces where the
  page shows them, in a page or a deck, optionally inside one chapter, and
  reports a stacked face's sideways overflow, text cut off by a box and parts
  outside the face as `problems`, besides the 16:9 fit. `emptyBand`, the
  height of the largest empty band of the canvas, is information with no
  threshold. New `assertSlideFaces` fails on any problem. Tried at 390, 1024
  and 1600 px on the same faces: every face at 390 px overflowed sideways by
  8 px, a real fault of the kit. The face that opens a chapter bled 22 px into
  a chapter body that is padded 14 px in a chapter 520 px wide or narrower,
  so the chapter scrolled sideways and cut the face's edges.
  `theme/components/slide-face.css` now bleeds 14 px there. Two false
  findings were fixed in the helper: the deliberate bleed was compared with
  the face's parent instead of the nearest box that cuts or scrolls, and an
  SVG label in capitals whose glyph box passes the SVG's top by 1 to 2 px
  counted as cut; a vertical cut now counts beyond a quarter of the line.
  After the fixes: no problem on the kit, the starter or adaptation at
  `e28472e` (99 measurements). On `09ec123` one real fault, the labels
  "+13 · seed 0" and "+13 · seed 1" cut at the right edge of a face's SVG at
  390 px; on `b6e9431` the face of the chapter adaptation-value does not fit
  16:9 in the page at 1600 px, the fault that adaptation fixed in `a011651`.
  Not tried: the six faults adaptation's session found by eye, because no
  revision with them was identified.
- `tests/own_site_review.cjs` and `tests/visual_review.cjs` assert every face
  in its chapter at 1600 and 390 px. Reviewed by eye: both kit faces in their
  chapters at 390 and 1600 px after the theme fix. Both edges of each stacked
  face now show; the diagram draws the eye first on both faces, and no band of
  either canvas is empty.
- Rules: `rules/writing/pages.md` › Slide faces gains the sentences on a claim
  and its limit and on a stacked face; `rules/site/validation.md` asks for
  faces to be checked in their page, says what a review by eye states for each
  face, and documents the helper; `rules/records.md` says lint checks the
  slide-face part of the numbers rule and the ledger stays the project's;
  `rules/site/authoring.md` › Slide faces and decks describes the lint checks
  and the mark. No section anchor changed. Pages synced: build-a-site and
  writing-practices; the starter record.
- Records: the 5.0.0 release notes name the new lint error as a third reason
  for the major release and list the checks; the 5.0.0 migration guide gains
  "Settle the slide-face checks"; the capability map gains a row and the
  owner's decision on both entries; the open findings mark items 1, 2, 3 and 7
  as built.
- Checks, after the last edit: `docsite.py build`, `lint --strict` (0
  warnings) and `build --check-reader` (5 reader pages) on the kit;
  `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh` exits 0 with 288 Python
  tests, 27 of them new, and six browser suites.

## 2026-11-15 — Four confirmations by deivid

- The case "when a running job depends on files the work would change" in
  [parallel work](../rules/engineering/delivery.md#parallel-work), released in
  4.0.0 and added by the kit owner without asking, stays. deivid: "Keep it".
- Wide chapter figures on slide faces are settled: the rule that a chapter's
  figures are material for a face already resolves it, and no sentence is
  added. deivid: "Yes, settled".
- A claim and its limit count as one finding. Asked which of three options,
  deivid answered "first": the visual carries the claim and shows the limit
  second, smaller but on the face; two independent findings do not share a
  title. Written into [slide faces](../rules/writing/pages.md#slide-faces).
- The standards without a measure stay judgment: "no band left over" and the
  designer's standard get no number. Asked "Keep both as judgment, with no
  number?", deivid answered "yes". Written into
  [validation and review](../rules/site/validation.md#validation-and-review);
  the browser check's empty band is information with no threshold.

## 2026-11-15 — Capability map, need first, running totals and a step-back review

- Evidence, read by deivid in ADP on 2026-11-15: ADP built 10,125 lines of
  code and 7,194 lines of tests in ten days to check one kind of run,
  attended sessions, inside one experiment's folder. 18 sessions used about
  3.8 hours of the person's time at the machine, and none passed all parts.
  General tools import from that experiment folder. Recording what a run did
  was solved three times in three forms. The total cost was first written
  down after everything was built. The kit's budget named time, compute and
  files, not supporting code or the person's time, and nothing made anyone
  look at the whole. These numbers are as reported; not checked here.
- deivid's words: "i think another failure is that we build something for a
  single experiment instead of looking for the big picture and ithinking ifwe
  need for ex the journal thing". On who holds the big picture: "i think there
  should be a written map cuz its the only object ive one which cannot fail".
  On unlisted tooling: "yes it should fail". On the proposals: "your proposal
  i like aside from the 3 strickes one, and regarding count evertyhing im
  scared the agent will not do good experiments cuz its scared". Then:
  "build". So there is no rule that stops work after a number of failed
  attempts, and no cap on what an experiment may cost.
- `rules/engineering/code.md`: new sections "Name the need first" (write the
  need in one sentence without the experiment, read the map, and when it is
  not met stop and bring three options; building stays the person's
  decision, noticing is the agent's duty) and "The capability map" with "The
  check". `rules/experiments/workflow.md`: "Show the total" (one line per
  attempt with attempts, usable results, lines of supporting code and tests,
  and the person's minutes; information, not a target, no threshold) and
  "Step back across experiments" (a fresh read-only agent after every third
  finished experiment or on request). The interval of three is this
  session's choice; deivid did not name one.
- `tooling/capability_map.py` and lint check 13: off unless `site.toml`
  names `tooling_roots`. Then the map (default `docs/CAPABILITY_MAP.md`, or
  `capability_map`) must exist and be tracked, every tracked file or folder
  directly under a tooling root needs a row, the map's links are checked
  wherever it lies, and its Imported by column must match what
  `docsite.py capability-map` generates from Python imports; these are
  errors. A tool that imports from a folder under `experiment_roots` is a
  warning. The build rejects wrong values of the three settings.
- The kit's own map, `docs/KIT_CAPABILITY_MAP.md`, covers the 21 entries of
  `tooling/` plus `docsite.py`, and the kit's `site.toml` turns the check on.
  Writing it changed the design: the generated column was first called "Used
  by", but static imports miss `lint.py` loading `site_paths.py` and
  `evidence_documents.py` by path and running `build.py`, so it is named
  "Imported by", says "no Python imports" instead of a dash, and marks a row
  without Python code as not scanned. The map's opening text names those
  users by hand. Needs seen but not built in the kit are the slide-face
  checks and the HTML source-link check, each with its decision still open.
- Starter: an empty map, the settings commented out in `site.toml`, a link
  from `docs/index.md` and a router row in `AGENTS.md`. The kit's own
  `AGENTS.md` gains the same row. `rules/conformance.md` gains a capability
  map item; `rules/documentation.md` lists the map among the canonical homes;
  `rules/site/authoring.md` gains "Capability map settings". Release notes
  and the 5.0.0 migration guide have the change and the optional step "Adopt
  the capability map"; the format and check are listed as provisional.
- Pages synced in a sentence each: the experiments page and the canonical
  homes table of the writing-practices page. The build-a-site page's snippet
  from the workflow guide moved three lines.
- Not reviewed independently. Checks: build, strict lint, `--check-reader`
  and `tests/run_checks.sh` with the browser suites required; the commit
  message has the counts. The commit hash is assigned by its landing commit.

## 2026-11-15 — deivid agrees that chapter figures are material

- Shown the proposal that a chapter's figures and numbers are material for a
  slide face, not its fixed picture, deivid answered: "and on the meterial
  thing i agree". That confirms the direction of the entry below. He has not
  read the rule sentences themselves.

## 2026-11-15 — Visual ambition for chapters and slide faces

- deivid asked whether the slide wording forces agents to make single
  figures: "i want them to be as visually creative as possible not limit
  them", and then "visually creastive as possiblei m eant in general for
  slides and chapter content".
- Four phrases did limit them: a face "with one visual", "Use one visual",
  the chapter's own figure first, and "Slide figures are views of numbered
  chapter figures". Ten of adaptation's redesigned faces share one skeleton,
  a wide chapter figure above one row of text.
- `rules/writing/pages.md`, page design: a new paragraph asks for the most
  telling picture each claim allows, in chapters and on faces, varied across
  a page, limited by honesty, readable labels and accessibility and not by
  caution. Slide faces: the limit is one finding, not one visual; the
  chapter's figures and numbers are material that a face may crop, split,
  combine, annotate or redraw; repeating a chapter figure unchanged is the
  fallback. The requirement that a slide figure is a view of a numbered
  chapter figure is dropped. `rules/writing/figures.md` points to the
  paragraph.
- This replaces the sentence of the entry "Slide faces: the chapter's figure
  first, drawings from its numbers allowed", which had put the chapter's own
  figure first.
- One sentence of the kit's writing-practices page is synced. The 5.0.0
  release notes list the change. Not reviewed independently.
- Checks: build and strict lint.

## 2026-11-15 — Slide faces: the chapter's figure first, drawings from its numbers allowed

- Adaptation's session sent its proposals on deivid's word, with his
  direction on face drawings: use the drawings a chapter already has, improve
  the chapter's figure when it is not good enough, and drawing from a table is
  allowed.
- `rules/writing/pages.md`, slide faces: the sentence that forbade "a second
  version of the same data" is replaced. A face shows the chapter's own
  figure when it shows the finding; a figure that falls short is improved in
  the chapter; numbers stated only in a table or in text may be drawn on the
  face, using those numbers and no others.
- The proposals' tooling items stay in
  `docs/open/upgrade-to-4.0.0-findings.md`, with one added: a face that fits
  in the deck can fail on the page.
- The rule sentence follows adaptation's reading of deivid's words; deivid
  has not confirmed the wording. Not reviewed independently.
- Checks: build and strict lint.

## 2026-11-15 — Slide-face tooling gaps reported by adaptation

- Adaptation's session listed what the project had to build or catch itself
  for slide faces: no lint check for facts on a face, none for one face per
  chapter, none below 720 px, no supported chapter-figure view, `!important`
  on every local declaration, and a home card picture that changes silently.
- Added to `docs/open/upgrade-to-4.0.0-findings.md`. Nothing is built.
- Checks: build and strict lint.

## 2026-11-15 — Where reused code lives

- deivid asked in ADP's session for a second kit rule. ADP's reusable
  native-run tooling sits inside one experiment,
  `experiments/platform_qualification/sdk_integration/`, and tools under
  `tools/coordination/` import from it. His words as that session relayed
  them: "its also incorrect that its in a random place in exerpeimnts instead
  of an experiment tools or in general tools sectin?", then "again rule in
  the kit".
- `rules/engineering/code.md` has a new section, Where code lives: an
  experiment's folder holds only its own code, inputs and records; code that
  other experiments or tools reuse lives in the project's tooling or source
  tree and is moved there before a second user imports it. A finished
  experiment is not edited for the move; its source pin stands for the code
  it ran. `rules/experiments/workflow.md` links the section from "Use the
  existing owners".
- The 5.0.0 release notes list the rule. Like the path rule, it was added
  after the independent release review and was not reviewed. ADP moves no
  code now; that waits for deivid's decision on the attended runs.
- Checks: build and strict lint.

## 2026-11-15 — Page lock run in Firefox and WebKit

- deivid asked why the lock was tested in Chromium only. The kit installs
  only Chromium for Playwright, and nobody had installed the other engines.
- The lock's browser suite takes `DOCS_BROWSER` now, default `chromium`. In
  Firefox 153 it passes after one fix: a fragment landed too low because
  Firefox scrolled before the rewritten page's image and frame had loaded.
- WebKit needed two system libraries, which deivid installed
  (`libgstreamer-plugins-bad1.0-0`, `libavif16`). The kit owner then ran the
  suite with `DOCS_BROWSER=webkit`: it passes in WebKit 26.5, exit 0.
- The Limits text of the lock rule and the open record say what is tested in
  which engine. Safari on macOS or iOS stays untested.

## 2026-11-15 — Full paths in reports

- deivid asked in ADP's session for a kit rule, after a report had named
  `attended_parts/registry.py` in place of
  `experiments/platform_qualification/sdk_integration/attended_parts/registry.py`.
  His words as that session relayed them: "can we put a rule into the kit that
  ays when u give me a path to a file u give it from root not only partial".
- `rules/engineering/handoffs.md`, Reporting completion: a file is named by
  its full path from the repository root, as a link where the reader's tool
  opens links, and a file outside the repository by an absolute path.
- The 5.0.0 release notes list the rule. It was added after the independent
  release review and was not reviewed.
- Checks: build and strict lint.

## 2026-11-15 — Prepare release 5.0.0

- The unreleased changes since `v4.0.0` make every tracked Markdown file a
  page by default, add the opt-in page lock, the Presentation view and the
  Slides switch, drop the prescribed slide-face arrangement and fix source
  links with and without a remote.
- Version 5.0.0 is the kit owner's recommendation, not confirmed by deivid.
  The changed default publishes content that was not published before. The
  version promise gains the sentence that such a change is major. Checked in
  `tooling/publication.py`: `publish` now also refuses a `[[source_pages]]`
  table whose file is private, which 4.0.0 published, so the release is major
  under the promise as written as well.
- The release notes gain a 5.0.0 section with the reasons, the provisional
  points and a table of changes with the owning rule per row. The new
  [5.0.0 migration guide](topics/releases/migrations/5.0.0.md) starts with the
  publication warning and the step that settles what the Reference section
  lists, before the pin moves anywhere that publishes; it ends with the
  optional page lock and how to land the upgrade.
- `VERSION` is 5.0.0; `README.md`, `docs/KIT_CONTEXT.md` and
  `docs/KIT_INDEX.md` name the release and its guide.
- The 5.0.0 guide is registered as a source page with the slug
  `migrate-5-0-0` and listed first in the navigation's release group, as the
  4.0.0 guide was; `tests/own_site_review.cjs` expects its route.
- Compared with `v4.0.0`: no heading of any file under `rules/` is removed or
  renamed; `rules/site/authoring.md` and `rules/site/publication.md` gain
  sections.
- The open record `docs/open/release-5.0.0-waits.md` holds the
  go to tag and push, the number, the merge of the source-link fix branch and
  six known open points. The slide-face findings record now lists only what
  is still owed.
- Checks on this state: build and strict lint of the kit. The full check
  script and the browser suites were not run for this entry. The hash is
  assigned by the landing commit. Not tagged and not pushed.

## 2026-11-15 — Release review: findings fixed in the Reference listing and exports

- An independent review of the release state found these, all fixed in
  `9e35757`:
  - The automatic listing listed files that `[publication]` private prefixes
    or suffixes mark private. It now skips them, so a configuration with `.md`
    among the private suffixes lists no file. `publish` refuses a source page
    whose origin is private, however it was listed.
  - Raw HTML on automatic pages: every remaining tag is written again with
    quoted attributes and loses event handlers, loading attributes and styles
    that load a `url()`; `<svg>` and `<math>` show as text. Unquoted
    `javascript:` links and outside loads through single-quoted or unquoted
    `src` are now caught.
  - With a remote, an exported link to an admitted file such as `tools/fit.py`
    became a broken `.../blob/main/docs/html/...` address. Exported links now
    carry `data-repo-exported`, and `filelinks.js` leaves them alone. This
    changes the published bytes of admitted links.
  - Without a remote, `publish` rewrites every generated page, so the source
    lines of automatic pages point at admitted copies.
  - Paths with a dot segment, such as `.github/` and `.claude/`, are no longer
    listed automatically. An invalid `reference_exclude` class such as `[z-a]`
    fails with a `site.toml` error instead of a traceback. Tests pin the
    symlink exclusion.
  - Rule text: the Reference condition in `rules/site/reader.md`, the
    no-remote paragraph, the lock's byte-for-byte promise, YAML frontmatter and
    agent files in the listing, and the slide-face sentences that still assumed
    a lead, points beside the visual and a facts row. The four page and
    starter places that described the old face arrangement are corrected.
    `.gitignore` ignores `.claude/`.
- Checks recorded in the commit: `DOCS_REQUIRE_BROWSER=1 tests/run_checks.sh`
  passed with 240 Python tests, starter and kit strict lint, 29 scripts and
  six browser suites; kit `build --check-reader` passed.

## 2026-11-15 — Reference tree kept from general readers; remembered readers

- An earlier review of the merged branch found that the page lock still
  showed every Reference title to a reader with the general password: each
  page carried the sidebar tree, and above 60 files `reference.tree.js` stayed
  readable and `reference.index.html` opened with the general password.
  Fixed in `4968088`.
- With `lock = true` the build always writes the Reference tree once.
  `publish` cuts the sidebar's Reference section out of every page the general
  password opens. `reference.tree.js` holds the tree and that section, sealed
  for the reference password and padded to a power of two of at least 64 KiB;
  `reference.index.html` needs the reference password. For a
  reference-password reader `page-lock.js` puts the section back. `nav.js` and
  the reader are unchanged. The summary counts Reference pages that general
  pages still link to.
- Readers who ask to be remembered now keep the password's derived key. The
  salt is PBKDF2 of both passwords, so it stays the same across publishes and
  changes, locking out every remembered reader, when either password changes.
- Two test assumptions changed: exactly two reference-level files, from before
  every tracked Markdown file was a Reference page; and a fresh salt per
  publish, which remembering across publishes replaces.
- Checks recorded in the commit: `DOCS_REQUIRE_BROWSER=1 bash
  tests/run_checks.sh` passed with `cryptography` 50.0.2: 232 Python tests, 29
  scripts, the WebCrypto cross-check and six browser suites. Lock-off
  publishes of the fixture (96 files) and of a 70-file Reference tree (168
  files) are byte-identical to `0959e8b`'s.

## 2026-11-15 — Opt-in page lock

- Projects with a private repository and a public GitHub Pages site need the
  page text unreadable without a password; deivid asked for two levels, one
  for general access and one that also opens the Markdown records, and for an
  opt-in that a project such as Tempo leaves off.
- With `lock = true` in `[publication]`, `publish` ends by encrypting the
  bundle in place. `DOCSITE_GENERAL_PASSWORD` opens the topic pages and every
  other HTML file; `DOCSITE_REFERENCE_PASSWORD` also opens the Reference pages
  and every exported Markdown file. Passwords come only from the environment;
  `publish` fails before building when one is missing, both are equal, one is
  shorter than 20 characters or one holds untypable characters. Local build
  output and `export_pages` stay plain.
- PBKDF2-HMAC-SHA-256 at 600,000 iterations derives a key per password; files
  are sealed with AES-256-GCM. The build side uses the pinned `cryptography`
  package from the new optional `requirements-lock.txt`; the browser side is
  `theme/components/page-lock.js` with WebCrypto.
  [Page lock](../rules/site/publication.md#page-lock) documents setup and
  limits.
- Commit `5ebbef6`, landed on `integration-next` by the merge `0959e8b`.
  Checks recorded in the commit: `DOCS_REQUIRE_BROWSER=1 bash
  tests/run_checks.sh` passed with `cryptography` 50.0.2 (211 Python tests, 28
  scripts, the WebCrypto cross-check and five browser suites). A lock-off
  publish of the fixture matched the base commit's: 89 files and stdout
  identical.

## 2026-11-15 — Reference section on by default, large trees written once

- deivid decided that the Reference section is opt-out: "make it optout
  instead and make them both show it all". Every tracked Markdown file of a
  project is now a source page, listed under Reference, except files in a
  submodule or the kit, files that start with `+++` frontmatter, topic entry
  pages, symlinked files, files under `[publication]` private prefixes and
  files that `reference_exclude` matches. A `[[source_pages]]` table still
  wins; pinning stays explicit.
- Routes derive from the path, such as `readme.md.html`, and cannot meet a
  slug; a collision adds eight hex digits of the path's SHA-256. Automatic
  pages never fail the build or add lint warnings; their problems are lint
  notes. The path adapter is asked once per distinct path per run: without
  that, a 388-page site with adaptation's adapter took 52.7 s instead of
  13.2 s.
- The opt-out switch was first named `reference = false` and is renamed
  `reference_listing = false` in `77a02e0`, because the first name read as "no
  Reference section".
- Above 60 listed files the tree is written once as `reference.tree.js` and
  `reference.index.html`, named under `reference_tree` in `site-build.json`.
  On the 415-file scale clone one automatic page dropped from 211,160 to
  13,441 bytes, total HTML from 98.5 MB to 22.6 MB and the build from 13.2 s
  to 6.4 s. At 60 files or fewer pages are unchanged.
- Commits `43ac3d5` and `77a02e0`, landed on `integration-next` by the merge
  `2277b12`. Checks recorded in `77a02e0`: `DOCS_REQUIRE_BROWSER=1
  tests/run_checks.sh` passed (202 Python tests, starter and kit strict lint,
  26 scripts, five browser suites); kit `build --check-reader` passed.

## 2026-11-15 — Source-link fix branch merged into integration-next

- `ee5ae78` merges `origin/fix/local-source-links-20261114` (`108ea6b`, the
  no-remote source-link fix of the two entries dated 2026-11-14 below) into
  `integration-next`. The worklog conflict was resolved by keeping both
  sides, so those two entries sit below the Presentation entry.
- deivid approved publishing that branch and pinning a consuming project to
  it. He has been told that it is merged into the release state; he has not
  said in words to merge it. The
  open record `docs/open/release-5.0.0-waits.md` keeps the question.

## 2026-11-15 — Presentation view and a Slides switch for All chapters

- deivid asked for a view that shows the slides full screen, with the chapter
  text reachable by scrolling, started from the first chapter or from the
  current one, and asked whether All chapters should show the slides.
- The reader has a fourth view, Presentation, on pages with at least one slide
  face. The slide fills the window at 16:9; arrow keys, Page Up and Page Down,
  Home and End change the chapter and land on the slide; scrolling moves only
  within the chapter, and a small scroll near the top snaps back. "Presentation"
  starts at the current chapter, "From start" at the first. The address keeps
  `?view=present` and the chapter. At 720 px and wider a chapter without a
  face shows a title card built at run time from its headline and lead;
  narrower it starts at its heading.
- All chapters hides slide faces and their bridges until its Slides switch
  shows them. The choice is remembered per page and printing follows it.
- A page with slide faces switches its view buttons to the view menu at
  980 px instead of 600 px, because the added buttons overflowed in between.
  Pages without faces keep their toolbar.
- Files: `theme/components/chapter-reader.{html,js,css}`,
  `tests/own_site_review.cjs`, `rules/site/reader.md`, one sentence in
  `rules/site/authoring.md`, and the layout sentence of the kit's own
  "Build a site" page.
- Built by a delegated agent. Its checks on the final state: build, strict
  lint, `build --check-reader` for 5 pages, and `tests/run_checks.sh` with
  187 unit tests and four browser suites, exit 0. The kit owner viewed its
  ten captures at 1600×1000 and 390×844 and reran build, strict lint and
  `--check-reader` after the page sentence.
- Not checked: real phones, Firefox, Safari, screen readers, widths between
  390 and 1600 for the view itself, and a chapter with several faces.

## 2026-11-14 — Publish the approved isolated source-link fix

- deivid approved publishing the prepared fix on its own branch and updating
  the consuming project's pin. The target is
  `fix/local-source-links-20261114`, based only on published commit
  `df089ef22838a3c776eb692e8c785d3b2816113a`. The kit's other local commits
  remain outside this branch; no release, tag or merge is included.
- The primary agent reviewed the complete patch and verified it was byte-for-byte
  identical to the tested preparation. The implementation and test inputs are
  unchanged, so the 188-test evidence below is reused. A focused browser check
  also preserved an exported canonical Markdown link after JavaScript ran;
  clicking it requested the correct local file with HTTP 200.
- The build guide's source-link paragraph now explains the absent-remote
  boundary and explicit HTTP export requirement; its prior blanket GitHub
  description no longer matched the authoring record.
- The consuming project's final build, strict lint and reader checks follow the
  published pin. Its wider content/design and evidence-retention work remain
  owned by that project.

## 2026-11-14 — Prepare no-remote source-link correction

- Prepared a review patch against `df089ef22838a3c776eb692e8c785d3b2816113a`.
  No release, tag, push or consumer pin change is part of this patch.
- With `gh_repo = ""`, generated source links retain their logical local
  paths, so strict lint checks the real source targets. HTTP source-link
  handling preserves exported relative Markdown, Python and directory paths.
  Configured hosted source behavior remains covered by the existing tests.
- Both added regression checks failed against the original implementation
  and passed with the fix. The build/export check also deletes a source and
  confirms that strict lint still rejects the missing target.
- `bash tests/run_checks.sh`, selecting the installed Python documentation
  environment with `DOCS_PYTHON` and Node 22.23.3 with `DOCS_NODE`, passed:
  188 Python tests, starter and kit builds
  and strict lint, math/source-link/reader/fold/panel logic, and syntax checks
  for 25 scripts. Runtime: Python 3.12.3, mistune 3.3.4, Pygments 2.21.0,
  Node 22.23.3; pinned Python dependencies were already installed.
- Browser suites were skipped because this scratch checkout has no local
  Playwright installation. No browser pixel inspection is claimed. A build
  does not serve the source checkout; HTTP source access still requires the
  explicit publication resource allowlist.
## 2026-11-14 — Adaptation's redesign under the changed slide-face rule

- deivid asked for all of adaptation's faces to be redesigned under the
  changed rule, with the old and the new face one after the other for
  comparison. The session did all 30.
- The kit owner viewed the 30 pairs: the new faces differ from each other.
  Weak points and the session's eight rule findings and three kit behaviours
  are added to `docs/open/upgrade-to-4.0.0-findings.md`.
- Checks: build and strict lint.

## 2026-11-14 — Adaptation's redraw under the released rule

- Adaptation's session removed six failing faces and redrew six, on deivid's
  decision there, under the slide-face rule as released in 4.0.0.
- The kit owner viewed the six redrawn faces: all six have one arrangement.
  That and five mechanism gaps the session met are added to
  `docs/open/upgrade-to-4.0.0-findings.md`.
- Adaptation pins `v4.0.0`, which holds the old rule. The changed rule of the
  entry below is local and unreleased, so no project can read it from its pin.
- Checks: build and strict lint.

## 2026-11-14 — Slide faces: no prescribed arrangement

- deivid decided that slide faces get no fixed layout: each face is designed
  for its own content, to the standard of an expert designer. He named his
  deck "CORE Labs" as the example.
- The rule of 2026-11-12 had turned one reference deck into one arrangement:
  visual, three to five points beside it, a row of facts. On adaptation that
  arrangement was met by none of 36 faces. Eight slides of "CORE Labs" share
  the frame and vary the body on seven.
- `rules/writing/pages.md`, slide faces: the prescribed arrangement is
  replaced by a layout that follows the shape of the content, the shared
  frame, a designer's standard, components as parts to choose from, and three
  groups for a review of existing faces.
- Not done: independent review of the rule, the kit's four example faces, the
  4.0.0 guide step. Listed in `docs/open/upgrade-to-4.0.0-findings.md`.
- Checks: build and strict lint.

## 2026-11-14 — ADP's upgrade to 4.0.0 reported, findings record renamed

- ADP's session reported its move to 4.0.0: one local commit, strict lint
  clean, no slide faces in ADP. Its six guide gaps are added to the findings
  record.
- The record of the entry below is renamed to
  `docs/open/upgrade-to-4.0.0-findings.md`, because it now holds the gaps of
  both upgrades.
- Correction to what the kit owner told ADP: a navigation group with its own
  colour needs no line in `[group_colors]`, and only five of the nine plot
  toggle keys need a label line.
- Checks: build and strict lint.

## 2026-11-14 — Slide-face rule evaluated on adaptation's upgrade to 4.0.0

- deivid asked for ADP and adaptation to move to 4.0.0 and to evaluate what
  the slide-face rule does on adaptation. Both sessions got the request; ADP's
  has not reported yet.
- Adaptation's session judged its 36 faces by the rule and the guide step
  alone: 12 fail, 24 pass, nothing removed. The kit owner viewed all 36
  captures and agrees with the 12 verdicts.
- The rule finds faces that are text boxes on an empty canvas. It was decided
  by one sentence; the composition requirements, read strictly, fail almost
  every face, and the guide does not say which requirements count.
- Recorded in `docs/open/adaptation-upgrade-to-4.0.0-findings.md`: eight
  places where the rule gave two readings, three omissions of the guide step
  and eight other gaps of the 4.0.0 guide. Nothing is fixed.
- Checks: build and strict lint.

## 2026-11-14 — Release 4.0.0

- deivid gave the go for the tag and the push on 2026-11-14, in answer to
  "Tag v4.0.0 and push the kit to main?".
- The tag `v4.0.0` is set on the commit that holds this entry and is pushed
  with `main`. The push publishes the kit's site.
- The open record `docs/open/next-release-version.md` and its route are
  deleted, as the record itself asked. What it settled is in the release
  notes: the version is 4.0.0 and the migration guides stay.
- Checks on this state: build and strict lint. The full check script last ran
  on the commit before, which differs only by this entry and the deleted
  record.
- Not verified before the push: the Pages workflow with its new `npm ci`
  install has not run on GitHub.

## 2026-11-14 — Two points left by the second look at the review fixes

- The reviewer checked the fixes of the entry below: eight of ten findings
  closed, two not fully. It removed each part of the cut-off fix in turn and
  the test failed each time.
- Lint's newest-first check of the worklog still counted a dated `## ` line
  inside a fenced code block, so the case the fix targeted still failed strict
  lint with "date sections are not newest-first". `check_worklog` now reads
  the entry dates through `markdown_entry_dates` in
  `tooling/worklog_entries.py`, which skips fenced lines, and the test asserts
  that the error is absent.
- Correction to the entry below: a configuration error does not always exit
  with status 2. The checks of `site.toml` at the start of the build exit 2
  with `build.py: error: …`; a configuration error found while rendering, such
  as an unknown `[[source_pages]]` key or a TOML syntax error, exits 1. The
  header of `tooling/build.py` now says so.
- The release notes say that any value but a `YYYY-MM-DD` date is an error for
  the cut-off, where they said "not an ISO date".
- Left as they are: rare Markdown forms on which lint and the build still
  date entries differently, such as a closing fence that carries text or a
  heading in a `<pre>` block; and the sentence on retained producing code in
  `rules/records.md`, which agrees with the probe-script rule only through
  the source-pin paragraph.

## 2026-11-14 — Close the findings of the review before the 4.0.0 tag

- An independent review of the unreviewed commits, from the release
  preparation to the solo-work rule, found no blocker, three major and eight
  minor points. It ran the full checks once, 187 unit tests and all four
  browser suites, and took a throwaway project from `v3.2.1` through the
  migration guide to a clean build and strict lint.
- Migration guide: it still called the worklog cut-off in the build an open
  defect, which this release fixes; the search for the old theme names had its
  options after `--`, so grep read them as file names and searched `.docs-kit`
  and `.build`; the lead said one step is enforced where the table names
  three; the reread list for site authoring lacked `[plot_toggle_labels]` and
  the worklog source page. All four are corrected.
- [Parallel work](../rules/engineering/delivery.md#parallel-work): the new
  default named no case for a running job that reads the checkout, which
  [execution](../rules/engineering/execution.md) sends to that section. A
  separate branch or worktree is now also used when a running job depends on
  files the work would change. This adds to the wording deivid accepted.
- [Refactoring over compatibility](../rules/engineering/code.md#refactoring-over-compatibility)
  and the [deletion gate](../rules/documentation.md#rules-for-changes-and-chronology)
  now say that the deletion of a finished probe script also covers a script
  in an experiment directory and is an exception to the gate.
- `tooling/worklog_entries.py`: a `## ` line inside a fenced code block of the
  worklog no longer starts an entry for lint, as in the rendered page; before,
  such a line dated before the cut-off hid dead links in the newer entry
  around it. The cut-off accepts the text "YYYY-MM-DD" or the same TOML date
  without quotes and rejects other ISO spellings such as "20000102". The test
  of the cut-off covers both. The header of `tooling/build.py` states that a
  configuration error exits with status 2.
- Release notes: a project that already used one of the three new `site.toml`
  names fails the build; the new theme names are provisional; the plot-label
  row links the authoring guide. The README names the `--with-deps` form of
  the Chromium install.
- New open record for two older flaws of the plot toggle chips in the zoomed
  figure, [grey dots and a wrapping label](open/plot-toggle-chips-in-lightbox.md).
- Not changed: the reviewer's note that the README does not say the fixture
  commits need a Git identity was inspected only and is older than this
  release. Old logs and review folders under `.build/` from earlier work are
  proposed to deivid for deletion, not deleted.

## 2026-11-14 — Work alone stays in the checkout on its current branch

- deivid reported on 2026-11-14 that agents now use a branch and a worktree
  for all work, also when they work alone. No rule asked for it: the kit said
  only "Use separate worktrees or other suitable isolation when independent
  work requires it", and neither ADP's guides nor his personal instructions
  name worktrees. The habit comes from how sessions are started in the desktop
  app, where a session started from a session in a worktree gets its own
  worktree and branch by default. That cause is read from the app's tool
  description, not measured.
- [Parallel work](../rules/engineering/delivery.md#parallel-work) now states
  the default: work alone happens in the project's checkout on its current
  branch, and a separate branch or worktree is used only when other work
  changes the same repository at the same time, when the project's workflow
  asks for one, or when the person asks for one. deivid chose the kit over his
  personal instructions as the home and accepted the wording.
- The parallel-work chapter of the engineering-practices page, the 4.0.0
  release notes and the 4.0.0 migration guide name the rule. The rule does not
  reach a session a person starts by hand in the app.

## 2026-11-14 — Plot toggle labels come from the project

- `theme/components/plot-toggles.js` no longer holds a fixed table of nine
  chip labels (`pinned`, `menger`, `stacked`, `heuristic`, `free_psi`,
  `free_kappa`, `free_both`, `corridor`, `waypoints`), which were one
  project's plot series. A project now sets them in a `[plot_toggle_labels]`
  table in `docs/site/site.toml`, one text label per group key. The build
  writes the table as `<script type="application/json"
  id="plot-toggle-labels">` into each page that loads `plot-toggles`, with
  `<`, `>` and `&` escaped, and the component reads it once, so the lightbox
  chips, built by `window.figToggles.buildChips`, use the same labels. A key
  without a label, or a site without the table, shows the group key as
  before. The build rejects a value that is not a table and a label that is
  not text, and lint prints the build's error, as for `[group_colors]`.
- Before the change, ADP loaded the component on four pages; adaptation and
  Tempo do not use it. The 4.0.0 migration guide gains the step "Label plot
  toggle chips" with the nine removed labels to copy; nothing enforces it. The
  authoring guide documents the table beside `[group_colors]`, and the release
  notes list it as a stable setting, the removed labels as provisional
  internals and `plot-toggles.js` among the changed shared files. The open
  record on theme leftovers is deleted, which closes the release's list of
  known open defects.
- Checked: a new test in `tests/test_site_contract.py` builds a starter page
  that loads the component, without and with the table, checks the JSON block,
  its escaping and its place before the script, that a page without the
  component gets no block, strict lint, and three configuration errors in both
  build and lint. No Node logic check covers `plot-toggles.js`. A throwaway
  page with four groups, three labelled, was reviewed by eye at 1600×1000 and
  390×844, on the page and in the lightbox.

## 2026-11-14 — The build applies the worklog link cut-off

- A worklog registered as a source page now honours
  `worklog_links_checked_from` in the build, as lint already did. In an entry
  dated before that day, a link or image whose target is gone renders as its
  text, or an image's alternative text, unlinked inside
  `<span class="link-gone" title="The target of this link no longer exists.">`,
  instead of failing the build with `link target not found`. A link in such an
  entry whose target exists stays a link, and a fragment that appears only in
  such entries is not checked against the target page's anchors. Entries from
  the cut-off date on fail on a missing target as before. `base.css` gives
  `.link-gone` a dotted underline in the muted text colour.
- The new `tooling/worklog_entries.py` holds what lint and build share: the
  configured worklog path and its default, the validation of the cut-off date,
  and which `## ` sections form an entry dated when, read from the Markdown
  source for lint and from the rendered `<h2>` headings for the build. The
  build now rejects a cut-off that is not a date, and lint prints the build's
  error instead of its own. Other media, such as a video, with a missing
  target still fail the build in any entry.
- [Resources](../rules/site/resources.md#resource-closure-and-evidence) no
  longer states the limit and describes the build's behaviour; the
  registered-source-pages section of the authoring guide names the exception,
  and the writing-practices page says how such a link shows.
- Checked: a new unit test in `tests/test_portability.py` builds a starter
  whose worklog is a source page: an old dead link and image render as the
  span and the build and strict lint pass, an old live link stays a link, an
  old link to a removed section of a registered page passes, the same entries
  fail with the cut-off on their own date, and a dead link in a newer entry
  still fails. The lint cut-off test now expects the build to reject an
  invalid date. A throwaway project's rendered worklog was reviewed by eye at
  1600×1000 and 390×844. The open record on the defect is deleted.

## 2026-11-14 — The browser suites' Playwright is declared

- The kit now declares Playwright 1.62.1, exactly, as a development dependency
  in a private root `package.json`, with a committed `package-lock.json`, as
  the [dependencies rule](../rules/engineering/code.md#dependencies) asks.
  `npm ci` installs it into `node_modules/`, which Git ignores. The four browser
  suites and `tests/run_checks.sh` load it from the kit's own `node_modules/`;
  the Pages workflow runs `npm ci` and `npx playwright install --with-deps
  chromium` instead of installing a version written in the workflow. The
  README's development steps gain both install commands.
- `DOCS_PLAYWRIGHT` and `DOCS_CHROMIUM` are removed. Only the kit's own suites
  and runner read them; `tooling/browser_checks.cjs`, which consuming projects
  use, takes a Playwright page from its caller and reads neither. Chromium
  revision 1234, which Playwright 1.62.1 expects, is found in the Playwright
  browser cache, so no path override is needed. A missing install still skips
  the browser suites with a printed line, and `DOCS_REQUIRE_BROWSER=1` still
  turns that into a failure.
- Checked: `npm ci` reinstalled 1.62.1 from the lock file; the kit site build
  and `lint --strict` passed; `DOCS_REQUIRE_BROWSER=1 bash tests/run_checks.sh`
  with Node v22.23.3 passed with all four browser suites in about 2 min 20 s;
  with `node_modules/` moved aside, the runner's browser section printed the
  skip line and exited 0, and with `DOCS_REQUIRE_BROWSER=1` exited 1. The
  workflow change was not run on GitHub. The open record on the undeclared
  dependency is deleted.

## 2026-11-14 — Font notices state the font version

- The notices of IBM Plex Mono, IBM Plex Sans and Saira Condensed under
  `theme/assets/vendor/` now give the font version: 2.3, 3.201 and 0.072. Each
  was read from name record 5 of every bundled WOFF2 file of the family with
  fontTools; all files of one family agree. This closes the font point of the
  open record on theme leftovers, which keeps the plot labels.

## 2026-11-14 — A finished probe script that a refactor breaks is deleted

- deivid accepted the last rule proposal from the ADP cleanup on 2026-11-14
  ("do proposal 4"). [Refactoring over compatibility](../rules/engineering/code.md#refactoring-over-compatibility)
  gains one paragraph: a caller that is a finished probe or one-time script is
  deleted in the same change instead of updated, when nothing else imports it,
  no rerun is planned and its result is recorded with a source pin that stands
  for it; claims that rest on it are historical from then on, and the deletion
  needs no separate approval. [Numbers and staleness](../rules/records.md#numbers-and-staleness)
  gains one sentence: the pin still stands for the code after the code is
  deleted from the current tree.
- A pin stands for code only under the conditions the source-pin paragraph
  already gives, a clean tree at the start of the run among them. A script
  whose run had uncommitted code is therefore not deleted this way.
- The compatibility chapter of the engineering-practices page, the 4.0.0
  release notes and the 4.0.0 migration guide name the rule. The open record
  `docs/open/rule-proposals-from-adp-cleanup.md` is deleted; all seven
  proposals are now answered.

## 2026-11-14 — Prepare release 4.0.0

- The release notes gain a 4.0.0 section and the new
  [4.0.0 migration guide](topics/releases/migrations/4.0.0.md) gives each step
  a consumer takes from `v3.2.1`, in order, with how to check it is done and
  whether lint or the build enforces it. `VERSION` is `4.0.0`. The guide is a
  registered source page in `docs/site/site.toml` and listed in the
  navigation, and `tests/own_site_review.cjs` expects its route. The README,
  the project context and the reading index name 4.0.0 as the current release.
- The content comes from `git diff v3.2.1..HEAD` and the entries of 2026-11-11
  to 2026-11-14. The consumer steps those entries recorded were checked
  against the diff before they were written. Corrections: the five hard-coded
  group colours applied only to groups named exactly `method`, `road`,
  `racing`, `sim` and `related work`, so a project with other group names
  sees no colour change; a project CSS rule with a weaker selector loses only
  for a group that `[group_colors]` names, because the generated stylesheet
  exists only with the table; review captures left from earlier work are
  proposed for deletion rather than deleted, since the scratch rule covers
  only what the current work created. Added: the theme names also live in
  figure generators; a project that set its own `--adp` or `--ada` value sets
  `--accent` or `--secondary`; the changed shared files that get a new `?v=`
  query, and `assets/group-colors.css` as the only file a build can gain; an
  `[extra_assets]` file named `group-colors.css` fails the build with the
  table; the new keys may collide with a project's own; lint now reports
  `site.toml` errors instead of a stale site; the new slide-face classes; the
  tooling modules read the project root from `DOCSITE_PROJECT_ROOT`; the
  starter router is unchanged.
- The guide covers the six gaps that adaptation's upgrade met in earlier
  guides: steps name which projects they affect, the pin is moved straight to
  the target with advice for an unfetchable old pin, project checks compare
  asset URL paths without the query, the release notes name every packaged
  file that changes, importing the tooling is named as unstable with the
  environment variable it reads, and pages locked by hash get an approved
  content revision before an edit.
- probed lint on an old-anchor link and a `badge adp` class → link fails, class passes silently, lint printed `anchor #evidence-identity-and-frozen-records not found` and nothing for the class, 2 min.
- The release notes state three open defects: the worklog cut-off is not
  applied by the build to a rendered worklog, the theme's plot labels and
  font versions, and the undeclared Playwright of the kit's browser suites.
- Checks: `docsite.py build` and `lint --strict` of the kit site, clean.
  `bash tests/run_checks.sh` with `DOCS_PLAYWRIGHT` (Playwright 1.62.1),
  `DOCS_CHROMIUM`, Node v22.23.3 and `DOCS_REQUIRE_BROWSER=1`, under a 4 GB
  memory cap, passed: 185 unit tests, the Node logic checks, 25 scripts parse,
  and the four browser suites, the own-site suite on 41 pages. Only this
  checks line was added after that run; build and strict lint ran again on
  the final state. The guide page and the changed release notes were looked
  at by eye at 1600×1000 and 390×844: no page overflow, the tables sit in
  their labelled scroll regions at 390 px as the older release tables do, and
  the navigation lists "Migrate to 4.0.0" above the 3.2.0 guide.
- Not tagged and not pushed; `docs/open/next-release-version.md` keeps the
  release waiting for deivid's go. The commit hash is assigned by this
  landing's commit.

## 2026-11-14 — Keep the migration guides

- deivid withdrew his decision of 2026-11-11 to remove all migration guides.
  Asked whether to release as 4.0.0 with the guides removed in it, he
  answered: "no we still need migrations sadly".
- The open record for the removal is deleted and its route is gone from
  `docs/open/KIT_OPEN.md`. The five existing guides stay, and the next release
  gets a guide of its own.
- `docs/open/next-release-version.md` now states what is settled, the guide
  and the version number 4.0.0 that the release record requires, and what the
  release still waits for.

## 2026-11-14 — Close the second review's findings and correct the ADP pin

The same reviewer read the previous landing. It found the rule text ready for
release, with six minor points and one wrong fact in an open record.

- Wrong fact: `docs/open/next-release-version.md` and
  `docs/open/remove-migration-guides.md` said ADP's `main` was not on kit
  3.2.x. ADP's `origin/main` pins `f34cf63` (`v3.2.1`) since 2026-11-11; the
  records had read ADP's stale local `main` branch. The trigger deivid set for
  removing the migration guides is therefore met, and the version record now
  recommends 4.0.0 with the guides removed in the same release.
- Scratch files: the item that is never scratch is the output of an
  experiment or measurement run, so that a test's temporary folder is not
  read as run output. A by-eye capture written into a tool's fixed output
  folder is still scratch. A kept capture is named in the report, and
  delegated work counts as this work. The deletion gate calls scratch files
  "an exception", not "the one exception", because finished open-work lines
  are also deleted.
- `rules/records.md` says "temporary folder" where it said "scratch folder".
  A pinned submodule may be loaded from its checkout. A project that needs
  `worklog_links_checked_from` does not register its worklog as a source page
  until the build applies the setting.
- Pages: three sentences in `docs/topics/engineering-practices/index.md` and
  `docs/topics/writing-practices/index.md` follow the rule text again.
- Open records: the Playwright record gained its question sentence, and the
  rule proposal names the approval point its wording has to settle.

These last edits were not reviewed a third time.

## 2026-11-14 — Close the findings of the independent review

An independent reviewer read every unreleased change after `v3.2.1`. It found
the release not ready: two blockers and three majors in the four new rules,
one tooling defect and smaller points. This landing closes the rule and page
findings.

Rules:

- **Scratch files** (`rules/engineering/handoffs.md`). Scratch is now an
  untracked, never committed file. The output of a run is never scratch,
  whether or not a stated number rests on it; before, an agent could read
  output without a stated number as scratch and delete it without asking. A
  capture stays while the person or a delegating agent is still to look at
  it; before, a delegated page author had to delete captures its delegating
  agent must review. Tracked files, working documents, a tool's fixed output
  folder and a capture used as a figure are named as not scratch.
  `rules/documentation.md` names scratch files as the one exception to the
  deletion gate.
- **Dependencies** (`rules/engineering/code.md`). A pinned Git submodule is a
  declared dependency, a dependency file inside it counts as declared, and
  the environment may live in an ignored folder. Without this every consumer
  of the kit could be read as breaking the rule.
- **Commit and diff** (`rules/records.md`). The diff is taken against the
  commit the run started from, which is recorded and stays reachable, and it
  includes changes inside submodules. "Never committed" became "not committed
  when the run started". A declared dependency is identified by its version,
  and an ignored file a run reads is recorded as an input.
- **Roles, not names** (`rules/writing/pages.md`). One role word for each
  role; names stay in a method's name, a citation or a contact line.
- Smaller alignments: the lists of working documents now all name the
  decision record; an answered question is deleted once nothing waits on it
  (`rules/engineering/delivery.md`); `rules/site/resources.md` says which
  projects register no adapter and states that `worklog_links_checked_from`
  does not reach a worklog rendered as a source page; the last "frozen or
  dated link" wording is gone.

Pages: the handoffs, code, evidence and page-design paragraphs follow the
rule text again. Four older sentences that said more or less than their rule
are corrected in `docs/topics/writing-practices/index.md` and
`docs/topics/build-a-site/index.md`. Text only; no figure or layout changed.

Theme: three vendored font notices named an ADP page and now name the
build-sheet theme.

Correction to the consumer step in the entry below: citations of review
captures are removed from records other than worklog entries and historical
experiment records, which stay as written.

Open after this landing, each routed from `docs/open/KIT_OPEN.md`: the version
number and migration guide of the next release, which the release record
makes 4.0.0 because a section anchor under `rules/` was removed; the worklog
cut-off in the build; the plot labels and font versions in the theme; the
Playwright declaration; and the last rule proposal, now in a narrower form.

## 2026-11-14 — Write four rules from the ADP cleanup

deivid accepted proposals 1, 2, 3 and 6 ("Yes, write them"). Each answers
something the ADP cleanup met.

- **Scratch files**, new section in `rules/engineering/handoffs.md`: before
  reporting completion an agent deletes the drafts, review captures and
  temporary test folders its work created, and a record cites no scratch file
  by path or hash. `rules/site/validation.md` says the by-eye captures are
  scratch files.
- **Dependencies**, new section in `rules/engineering/code.md`: every
  dependency is declared in the dependency file and installed; code loads no
  third-party library from an untracked checkout or a folder under build
  output; the setup guide produces the environment the project runs.
- **Commit and diff**, in `rules/records.md` under numbers and staleness:
  uncommitted code is kept as a diff against the pinned commit, new files
  included; a run does not copy the working tree, and an unavoidable copy
  holds no ignored files. The earlier wording allowed "a copy or a diff".
- **Roles, not names**, in `rules/writing/pages.md` under page design: a page
  that explains how something works uses one role word per role; a name
  appears only where the page states who decided, approved or said something.

The pages that explain these sections are synced: the handoffs and code
chapters of `docs/topics/engineering-practices/index.md`, the evidence and
page-design chapters of `docs/topics/writing-practices/index.md`, and the
preview chapter of `docs/topics/build-a-site/index.md`. Each gained one
paragraph or sentence of prose; no figure or layout changed.

What a consumer has to do, for the release notes:

- remove citations of review captures by path or hash from its records, and
  delete the captures;
- declare any dependency its code loads from a checkout or build folder;
- change any run tooling that copies the working tree to record the commit
  and a diff instead;
- replace a person's name by a role word on pages that explain how something
  works.

No lint check enforces any of the four.

Still open: the proposal to delete one-off probe scripts, now the only content
of `docs/open/rule-proposals-from-adp-cleanup.md`. New open item: the kit's own
browser suites use a Playwright that no dependency file declares,
`docs/open/browser-test-dependency-not-declared.md`.

## 2026-11-14 — Drop the rule proposal on naming the case

- deivid dropped proposal 7 after its second look. It leaves the open question
  in `docs/open/rule-proposals-from-adp-cleanup.md`, which keeps his answer
  and the reasons. Proposals 1, 2, 3, 4 and 6 remain unanswered.
- No rule text changed.

## 2026-11-14 — Withdraw one rule proposal and rework two

- deivid called proposal 5, pictures are chosen and not collected, specific to
  ADP. It is withdrawn from the kit proposals.
- He asked for a critical second look at proposal 7. Its first wording, the
  general rule before the example, is dropped: the explanation order is
  already a rule, and an explanation may open with an example. What remains
  is one sentence, that a statement holding for one case names the case.
- He asked what the problem with proposal 4 is. The record now names three
  gaps: which reading of the source-pin rule applies, runs that started from
  uncommitted code, and what counts as one-off.
- All of this is in `docs/open/rule-proposals-from-adp-cleanup.md`. No rule
  text changed.

## 2026-11-14 — Add two rule proposals from a page review

- deivid read ADP's attended-sessions page and corrected two things: the page
  named him instead of a role, and a chapter presented one session's step list
  as what every session requires.
- Both are added as proposals 6 and 7 to
  `docs/open/rule-proposals-from-adp-cleanup.md`, with his words and a
  recommendation to write them into the page rules.
- No rule text changed.

## 2026-11-13 — Record the open question about rule proposals

- Five rule proposals drawn from the ADP cleanup were put to deivid in chat and
  are not answered yet. Under the rule on unanswered questions they are now an
  unresolved choice in `docs/open/rule-proposals-from-adp-cleanup.md`, routed
  from `docs/open/KIT_OPEN.md`: the question, the proposals with what ADP met,
  the recommendation and what waits on the answer.
- No rule text changed.

## 2026-11-13 — Remove ADP names from the shared theme

deivid asked to remove the names of the kit's first consumer, ADP, from the
shared theme before the next release. The theme carried ADP's accent variable
names, seven class names and the colours of ADP's five navigation groups.

The variables `--adp` and `--ada` are gone. Every theme stylesheet now uses
`--accent` and `--secondary`, which the two names only pointed to, and the
panel-switcher browser test fixture sets `--accent`. The classes are renamed
with the same styling: `.badge.adp` to `.badge.accent`, `.badge.ada` to
`.badge.secondary`, `.card.ada` to `.card.secondary`, `svg .band-adp` to
`svg .band-accent`, `svg .band-ada` to `svg .band-secondary`, `svg .b-adp` to
`svg .b-accent` and `svg .b-ada` to `svg .b-secondary`. No kit page, example or
rule used the old classes. `docs/open/simplify-frozen-record-machinery.md`
named the variable and the hard-coded groups as an open coupling; it now says
they are gone.

The colours of the groups `method`, `road`, `racing`, `sim` and `related work`
were hard-coded in `theme/components/base.css`,
`theme/components/chapter-reader.css`, `theme/assets/home.css` and
`theme/assets/build-sheet.css`. A project could not replace them site-wide,
because project CSS is loaded per page. They are removed, and a new
`[group_colors]` table in `site.toml` maps a group name to a hex colour. The
name follows `folded_groups`, the existing setting for navigation groups. The
build writes the table to `assets/group-colors.css` and links it on every page,
right after `base.css`, so a page's own CSS can still set `--g`. The
stylesheet sets `--g` on the group's sidebar header, section and page links and
on its home-page map group, gives that group's map cards the same 2 px top edge
the hard-coded rules gave them, and sets `--bs-number`, the build-sheet chapter
number colour, on pages in the group. A group without an entry keeps the
`nav.js` tones. The build rejects a value that is not a table, a colour that is
not a 3, 4, 6 or 8 digit hex colour, and a name that no visible `[[nav]]` entry
uses as its group. A group name is written into the stylesheet as an escaped
CSS string, so any name keeps the rule well formed. The built site still ships
the kit's component files unchanged, because the generated stylesheet has no
source in `theme/components`. The build adds no inline style, and no content
security policy exists in the build that it would need to satisfy.

Lint ran `build.py --check` and read its exit status 2 as a stale site.
`argparse` also exits with 2 on a configuration error, so lint reported every
`site.toml` error, such as a wrong `folded_groups` entry, as "stale". Lint now
reports the build's error message when the output names a `build.py` error.

`rules/site/authoring.md` names the new table. No page under `docs/topics/`
repeats that sentence; the guide renders as its own reference page. The
starter's `site.toml` shows no optional settings, so it does not show the
table either.

The release notes have no section for unreleased changes, so the steps for
consumers are recorded here until the next release's notes are written:

- Rename `--adp` to `--accent` and `--ada` to `--secondary` in project CSS and
  inline styles.
- Rename the seven classes in pages and SVG figures: `badge adp` to
  `badge accent`, `badge ada` to `badge secondary`, `card ada` to
  `card secondary`, `band-adp` to `band-accent`, `band-ada` to
  `band-secondary`, `b-adp` to `b-accent` and `b-ada` to `b-secondary`.
- Add a `[group_colors]` table for the groups that should keep a fixed colour.
  ADP's former values are `"method" = "#85b7eb"`, `"road" = "#ffb35c"`,
  `"racing" = "#6ee7c5"`, `"sim" = "#b69cff"` and
  `"related work" = "#8394a7"`. A name must match the group exactly: ADP's
  `site.toml` on 2026-11-13 names the last group `Related work`, which the old
  lowercase rule never matched, so that page group showed a `nav.js` tone.
  Without the table, every group takes the `nav.js` tones in order.
- On the home-page map, the old rules gave the cards of `road`, `racing`,
  `sim` and `related work` a top edge in `--orange`, the accent, the secondary
  colour and `--muted`, which differ from the sidebar colours. With the table
  the cards take the sidebar colour of their group. A project that wants the
  old edge colours sets them in its home page's own CSS.

Checks: `DOCS_PYTHON=.build/docs-env/bin/python bash tests/run_checks.sh` with
`DOCS_PLAYWRIGHT`, `DOCS_CHROMIUM` and Node 22 set, so the four browser suites
ran, each under a 4 GB memory cap. New tests in `tests/test_site_contract.py`
cover the table when valid, missing and invalid, the escaped group name, the
lint message, and a scan of the theme for the old variables, classes and group
names. The kit's own site and the starter were built before and after the
change and captured at 1600×1000 and 390×844 on the home page, a chapter-reader
topic page and a build-sheet page. The kit's groups already took the `nav.js`
tones, and the captures before and after match. A starter built with a
`[group_colors]` entry showed that colour on the sidebar group, the map card
and the build-sheet chapter number.

## 2026-11-13 — Replace the remaining "frozen records" wording

- deivid asked for this before the next release. Finished working documents
  are deleted since the decision on frozen documents, so no rule may still
  speak of frozen records.
- `rules/engineering/code.md`: the users of an old name are now "saved data or
  historical records".
- `rules/site/resources.md`: the path adapter exists for records that are not
  edited afterwards, named as old worklog entries and historical experiment
  records; a project removes it once no such record names an old path.
- `rules/documentation.md`: "dated or frozen links" is now "dated links, such
  as those in old worklog entries".
- Pages synced: `docs/topics/engineering-practices/index.md` (two places) and
  `docs/topics/writing-practices/index.md` (the link sentence and the table
  cell that listed "frozen evidence", now "finished working documents").
- Left as it is: "a run request that is frozen" in the engineering page, which
  means a fixed run request and not a document.

## 2026-11-12 — Align the run-output and unanswered-question wording with its neighbours

- deivid asked for a review of the wording added in the entry below against
  the lines around it. Problems found and corrected:
- `rules/records.md`: the sentence above said to keep "outputs" and failed
  attempts while the new one said some output is not stored and some runs are
  deleted. Now one term, "run output", is used in both, tied to the "raw
  result" the section already asks a claim to link. Every attempt keeps its
  entry; its output counts as run output when a stated number or verdict rests
  on it. The source-copy clause is gone because the source-pin paragraph
  already covers it. "Compress large text files" is gone: storage format is
  the project's choice. "Not measured" links its existing rule. While the
  outside-Git question is unanswered, the experiment is not complete.
- `rules/engineering/delivery.md`: no second person, the existing terms "open
  owner" and "unresolved choice", and "before stopping work or reporting
  completion" in place of "task or turn". A delegated owner sends its question
  through the return channel. "One question at a time" is removed as a
  personal preference, and the silence sentence is removed because
  `rules/documentation.md` already states it. Routine choices link owner
  responsibility.
- `rules/experiments/workflow.md` keeps a pointer only; the rule about
  untracked folders now stands once, in `rules/records.md`.
  `rules/engineering/handoffs.md` and the three pages follow.

## 2026-11-12 — Store run output with the experiment and record unanswered questions

- Found in ADP on 2026-11-12: the measured series behind its page figures and
  behind 639 further runs existed only in an untracked build folder on one
  machine. Git held summary records with numbers only. The kit's rules allowed
  this: they said to keep outputs, let bulky files live outside Git when the
  experiment directory names the place and a hash, and named no step that puts
  run output into the experiment when the work ends.
- deivid's direction, in his words: "put the runs output into experiment if we
  need it for a claim otherwise its no experiment at all"; storing bulky files
  outside Git "should be discussed with me and if i dont react put into open";
  and an agent that really needs his feedback puts the question into open work
  when he does not react.
- `rules/records.md`, "Numbers and staleness": the run output a claim rests on
  is stored in the experiment directory, in Git, before completion is
  reported. A claim without it is "not measured". Run output is the measured
  data, summaries and tables, the run's own records and logs. Caches,
  environment copies, bytecode and pinned source copies are not stored. A run
  that no claim rests on is proposed for deletion. Storing run output outside
  Git is the person's decision. This replaces the sentence, approved by deivid
  earlier, that repository size decides where material is stored and that a
  project may hold bulky files outside Git.
- `rules/experiments/workflow.md`, "Required content": the same step named at
  the point where an experiment reports.
- `rules/engineering/delivery.md`, "Decisions and blockers": a question that
  needs the person's answer goes into open work when the task or turn ends
  unanswered. Only questions whose answer changes the work are recorded;
  small, reversible choices are made and reported.
  `rules/engineering/handoffs.md` points to it.
- The writing-practices, engineering-practices and experiments pages carry the
  same wording.
- No tooling changed. Not released; the independent review of this release's
  rule changes is still owed.

## 2026-11-12 — Ask a generated figure only for its generator and input data

- deivid decided this after a measurement of ADP's figure records. Its shared
  manifest held `script`, `caption`, `commit` and `date` for 286 figures. Only
  `script` was read, by kit lint. 277 of the recorded commits ended in
  `-dirty`, so they named no state that exists in Git.
- Offered: record hashes of generator and inputs and let lint warn on a
  mismatch, or cut the record. deivid chose the cut. Nothing checks whether a
  figure still matches its generator; a person notices a stale figure, as
  before.
- `rules/writing/figures.md`: a generated figure names its generator and its
  input data. Git holds the revision, the date and the exact bytes of the
  figure and of its generator, and the manifest does not record them again.
  The rule for a screenshot that can only be taken by hand is unchanged: it
  states commit, date and scenario.
- `docs/topics/writing-practices/index.md` carries the same wording.
- No tooling changed. Lint read only the generator before and reads only the
  generator now.
- Not released. ADP's session cuts its manifests on its own branch.

## 2026-11-12 — Require a real visual on slide faces and rebuild the examples

- deivid reported two problems. Slide faces were often a title over three text
  boxes on an empty canvas, and a page author gave up on a figure when none
  existed yet. The kit's own examples showed exactly that slide: all six faces
  in the kit pages, the starter and Tempo were text boxes only.
- `rules/writing/pages.md`, "Slide faces": faces are added after the chapters
  are built and the person said yes. A face needs a visual that shows the
  finding; text and boxes sit beside it and do not replace it; a chapter with
  nothing to show gets no face. A new list says how a face is composed from top
  to bottom. deivid named his deck "CORE — Cognitive Software (Klinikum)" as
  the level to reach; the list describes its structure in the kit's words.
- `rules/writing/figures.md`: a missing figure is work to do. The page author
  makes it from data, run outputs, code or geometry, and leaves a claim without
  one only when nothing true can be drawn, saying so in the completion report.
- `theme/components/slide-face.css` gains `slide-points`, `slide-facts` and a
  keyed `figcaption.slide-legend` inside `slide-figure`. No existing rule
  changed. `rules/site/authoring.md` lists them.
- The four example faces are rebuilt on the layout deivid chose from three
  variants: getting-started, build-a-site and the starter's two. Three chapters
  had no figure and got one first. The starter's two figures live in
  `examples/starter/docs/site/fragments/`. The writing-practices and
  build-a-site pages follow the rule text.
- `tests/test_site_contract.py`: the page-number-note test relied on numbers
  that only the old starter slide showed. It now adds its own unstated number
  and also asserts that the clean starter prints no note.
- Checks: `bash tests/run_checks.sh` with the four browser suites passed, run
  by the page author after the last edit. All four faces fit at 1600 × 1000 and
  stack at 390 × 844 with text of at least 11 px; three captures were reviewed
  by eye by the kit owner and all four by deivid.
- Not done: the extracted deck and print were not rendered. The shared label,
  scope and caption sizes are smaller than in the reference deck and were left,
  because raising them changes other projects' faces.
- Not released.

## 2026-11-11 — Allow one README.md, at the repository root

- deivid decided: no folder below the root has a `README.md`. ADP holds 109
  of them, and a search hit, a link or a file list does not say which one is
  meant. Files that arrive with third-party code keep their names. He applies
  it to ADP in full, including READMEs whose hash a record names.
- `rules/documentation.md`, "README is the bounded exception": one new
  paragraph. A folder that needs a guide gets a file named after its subject,
  such as `experiments/<name>/<name>.md`.
- `rules/records.md` and the conformance check now say the same for every
  record, where they covered only topic records before.
- The writing-practices page follows in two places.
- Not enforced by lint: ADP would fail until its renames are done.
- Checks: `bash tests/run_checks.sh` passed without the browser suites; the
  page edits are two sentences of text and were not reviewed by eye.
- Not released.

## 2026-11-11 — Remove the pin button the reader built but never showed

- `theme/components/chapter-reader.js` created a button with the class
  `reader-drawer-pin`, gave it a click handler and updated its pressed state,
  text and label on every navigation sync, but never added it to the page. A
  review breakage of its pressed state went unnoticed by the new logic test,
  which is how it was found. deivid decided to delete it.
- Removed: the button, its handler and its four update lines in the script,
  and its two rules in `theme/components/chapter-reader.css`. Docking, its
  stored choice and the close and menu buttons are unchanged.
- The open record `docs/open/reader-unused-pin-button.md` is deleted with this
  landing; it is in Git at `7af628a`.
- The entry below links that record, and worklog entries are never rewritten.
  The kit therefore sets `worklog_links_checked_from = "2026-11-12"` in
  `docs/site/site.toml`, its first use of the setting: lint checks links in
  worklog entries from that day on. Entries dated today, this one included,
  are no longer link-checked.
- Checks: `bash tests/run_checks.sh` passed with Playwright set, so the logic
  tests and the four browser suites ran and passed on Node v20.20.2; 183 unit
  tests. The navigation header was read by eye at 1600×1000 and shows the site
  name and the close button as before. At 390×844 navigation starts closed;
  that width was covered by the own-site browser suite, not by eye.
- Not released.

## 2026-11-11 — Check that a built site ships the kit's component files unchanged

- ADP's cross-check of the ported tests found one assertion left in neither
  repository: its road check compared the built `assets/chapter-reader.js`
  with the kit source byte for byte. The kit compared only the panel switcher.
- `tests/test_portability.py` now builds the starter and compares every
  component script and stylesheet in the built `assets/` with its source in
  `theme/components`, and requires `chapter-reader.js` and `fold-controls.js`
  to be among them. A source with `{{placeholders}}`, such as `filelinks.js`,
  is filled in by the build and is left out.
- Checks: the `tests/test_portability.py` module passed.

## 2026-11-11 — Test the reader's logic in the kit, without a browser

- ADP's Node check `experiments/track_geometry/test_road_review_topics.cjs`
  ran the kit's reader and fold-control scripts in an imitation page. A
  coverage map of the kit's tests showed that most of that behaviour was
  tested nowhere in the kit, and `fold-controls.js` not at all. deivid decided:
  logic checks and source rules move into the kit, layout arithmetic and exact
  style values are dropped, and ADP keeps only checks of its own content.
- New `tests/test_reader_logic.cjs` with `tests/reader_harness.cjs`, and
  `tests/test_panel_switcher_logic.cjs`, ported from ADP at its commit
  `e21c2e84` onto a synthetic kit page. `tests/run_checks.sh` runs both on
  every run. Covered: navigation, pins, scroll restore, history, deep links,
  fold wrapping and key ownership, dialogs, per-column layers and fold caches,
  presets and their storage, migration of old stored state, the navigation
  drawer and its keyboard loop, full-page mode, print, reduced motion, pages
  with separate stored preferences, redirects for moved chapters, jump groups,
  the fold-controls opt-in and default path, the panel switcher, and the rule
  that neither script makes a network request.
- Not ported: the 88% strip width, column-width arithmetic, twelve stylesheet
  strings and other exact style values. Not ported because they are ADP
  content: page counts, group names, the list of reader pages, fold placement.
- An implementer subagent wrote the port. It reports 22 deliberate breakages
  of the scripts on scratch copies, each failing with a message that names the
  behaviour. This session ran four more: three failed as intended; the fourth
  changed a pin button that the script never adds to the page, recorded as
  [open work](open/reader-unused-pin-button.md). One ADP check could never
  fail (the fold was already open before its deep link); the port closes the
  fold first.
- Measured: the reader test takes 0.94 s, the panel-switcher test under 0.1 s.
- Checks: `bash tests/run_checks.sh` passed with Playwright set, so the four
  browser suites ran and passed, on Node v20.20.2: 182 unit tests, 25 scripts
  parse, own site 40 pages. This run also covers the three earlier commits of
  this day, whose entries say the browser suites were skipped.
- Not released.

## 2026-11-11 — Offer the reader content check as a build command

- ADP kept a copy of the kit test that renders every topic page with and
  without the chapter reader and compares the content. The copy imported the
  kit's build module and used its internal names, so a kit change could break
  ADP's test. deivid decided the kit offers the check as a command and ADP
  deletes its copy.
- New `docsite.py build --project . --check-reader`. It renders every topic
  page both ways, reports by page what the reader changed (text or code,
  links, media, anchors, tables, SVG figures, folds, a missing or unexpected
  reader) and writes nothing. Exit status 1 on a difference; with
  `chapter_reader` off it says so and exits 0.
- The comparison moved from `tests/test_chapter_layout.py` to
  `tooling/reader_content.py`; the kit test now calls it, and two tests cover
  the reported differences and the command.
- Measured: the command passes on the starter (1 reader page), the kit's own
  site (5) and a snapshot of ADP's `docs/` at its branch commit `c214372d`
  (21 reader pages, 5.1 s). The ADP run used a scratch copy, not ADP's
  checkout or its resource slot.
- [Validation](../rules/site/validation.md#validation-and-review), the README
  command list and the build-a-site page name the command.
- Checks: `bash tests/run_checks.sh` passed, 182 unit tests, browser suites
  skipped because `DOCS_PLAYWRIGHT` was not set. The new card on the
  build-a-site page was read by eye at 1600×1000 and 390×844.
- Not released.

## 2026-11-11 — Delete finished working documents instead of freezing them

- deivid approved the rule as an exact diff. A plan, decision record, review or
  coordination note is deleted once its work has landed and its lasting content
  is in the owning record; whatever still needs it cites the commit and path in
  Git. No unedited copy stays in the tree. He first considered a kept copy
  guarded by its recorded hash and dropped it the same day.
- `rules/records.md`: the section "Evidence identity and frozen records" is
  replaced by [finished working documents](../rules/records.md#finished-working-documents),
  so its anchor changes. The source-pin paragraph now also covers a plan,
  protocol or review document that a run recorded by hash.
- `rules/documentation.md`: the deletion bullet names the new rule, a new
  bullet covers links in old worklog entries, and "dated reviews" leaves the
  role of `docs/topics/<topic>/evidence/`.
- `rules/site/resources.md`: the path and evidence adapters are marked as
  existing only for projects that already keep such documents.
- Pages synced: the fold in writing practices and one line in getting started.
  Release notes and the 1.1.0 and 3.0.0 migration guides now link the old
  section at the `v3.2.1` tag.
- Checks: `bash tests/run_checks.sh` passed, 180 unit tests, browser suites
  skipped because `DOCS_PLAYWRIGHT` was not set. The changed fold was read by
  eye at 1600×1000 and 390×844; the other page edits are single lines of text
  and were not.
- Not released. deivid wants further changes before a release. The independent
  review of the rule change is owed before the release tag.

## 2026-11-11 — Let a project stop link checks in old worklog entries

- deivid decided to delete all 53 exact-byte documents from ADP's tree and
  cite them from Git. Old worklog entries link to those documents and are never
  rewritten, so their links would fail lint after the deletion.
- New optional setting `worklog_links_checked_from = "YYYY-MM-DD"` in
  `docs/site/site.toml`. Lint checks links only in worklog entries dated on or
  after that day. Text above the first dated heading is always checked, and an
  undated `## ` section belongs to the dated heading above it. A value that is
  not an ISO date is an error. Without the setting nothing changes.
- [Resources](../rules/site/resources.md#resource-closure-and-evidence)
  describes the setting. The
  [open record](open/simplify-frozen-record-machinery.md) holds the decision and
  the remaining steps. Not released; the forward rule's wording is still a
  draft for deivid.
- Checks: `bash tests/run_checks.sh` passed without the browser suites, which
  were skipped because `DOCS_PLAYWRIGHT` was not set. One sentence on the
  build-a-site page now names the setting; the page was rebuilt and linted, not
  reviewed by eye.

## 2026-11-11 — Record deivid's decision on frozen documents

- This session and ADP's documentation session measured what ADP's
  frozen-record chain serves, on ADP `origin/main` at `7d85f2a4`. The counts
  agree: 164 of 3,946 links need the path adapter, all in exact-byte documents
  or the worklog, and Git returns the exact bytes of 52 of the 53 documents.
- deivid decided: a replaced document is deleted by default and cited from
  Git; a copy stays in the tree only with his approval per file; a kept copy is
  guarded by its recorded hash and changes only with an approved diff. The
  rule applies backwards to ADP's 53 documents.
- The measurements, the decision and the open points are in
  [open work](open/simplify-frozen-record-machinery.md). The worklog question
  and the rule wording are open.
- No rule, tool or consumer file changed.
- Checks: strict lint of the kit site.

## 2026-11-11 — Record the decision to remove the migration guides

- deivid asked whether the migration guides can go, since ADP and adaptation
  are the only consumers and both are being moved to 3.2.x. He decided: all
  guides at once, after ADP's `main` is on 3.2.x. The guides stay at tag
  `v3.2.1`.
- The trigger, the kit files that change and the steps each consumer takes
  are in [open work](open/remove-migration-guides.md). Consumers link to the
  guides through the starter's router row and through their adoption
  records, so the removal needs a version decision.
- Nothing is removed.
- Checks: strict lint of the kit site.

## 2026-11-11 — Record the kit gaps that adaptation's upgrade met

- Adaptation, the second consumer, moved from 1.1.0 with an unpushed kit pin
  to 3.2.0 in its own session and published. Its session reports that the
  build, strict lint, publication and its site checks pass.
- It reported six cases where a migration guide, the release notes or the
  tooling did not cover what it met: publication keys from the unpushed kit
  commit, an old pin that cannot be fetched, versioned asset names in project
  checks, `assets/home.css` no longer in every bundle, the tooling imported
  as a library from a subfolder, and pages whose content a project locks.
  They are in [open work](open/adaptation-upgrade-findings.md) with what was
  checked here. Nothing is fixed.
- Checks: strict lint of the kit site.

## 2026-11-11 — Release 3.2.1

- deivid approved the release after the pre-tag review and its corrections.
  `VERSION` is `3.2.1`. The release notes no longer say that the release is
  untagged. The README, project context and index name 3.2.1 as the current
  release; it is a patch with no migration step, so the 3.2.0 guide stays the
  newest guide.
- The tag `v3.2.1` goes on the commit of `main` whose Pages workflow passes.
- Not read by an independent reviewer: the corrections made after the review
  and this commit.
- Checks: `tests/run_checks.sh` with the browser suites passes (179 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-11 — Correct the four rule changes after the pre-tag review

- An independent reviewer read everything since `v3.2.0` before the 3.2.1
  tag. No blocker, four corrections, five minor points. deivid approved the
  four corrections to wording he had approved before.
- The sentence on byte-exact copies was narrower than the rule it sits
  beside: it named a check or a citation, while the record rules also allow a
  source pin or a reproduction dependency. A project that conformed to 3.2.0
  could have stopped conforming, which a patch release may not cause. The
  sentence now points to the record rule.
- "Its own paragraph" was not what the build tests. The pattern matches a
  marker at the very start of a line, so an indented paragraph in a list item
  or a quote stays raw, and a marker without a blank line after it pulls the
  next lines into its card. The reviewer ran the pattern through the
  renderer. The rule now says an unindented paragraph followed by a blank
  line.
- "Lint rejects a frozen or dated link that neither covers" claimed more
  than lint does. Lint checks files under `docs/`, the entry files and
  registered pages. The sentence now says "in the files it checks".
- The source-pin sentence now says what a pin buys: the experiment directory
  need not hold a copy of that code. The page for people gets the full
  conditions, which it had shortened. The release notes no longer read as if
  ADP had 35 markers in total.
- A defect that predates these changes is recorded in
  [open work](open/marker-in-fenced-code.md): a marker inside a fenced code
  block is rendered as a card and breaks the block.
- Not read by an independent reviewer: these corrections.
- Checks: strict lint of the kit site. The full suite passed on the state
  before these corrections (179 tests, four browser suites).

## 2026-11-11 — Let the owner choose how links to a removed page keep resolving

- Two rules disagreed. The documentation rule said to preserve a hidden stub
  and the former anchors while dated or frozen links depend on a removed
  page. Refactoring over compatibility leaves the choice to the owner and
  says to add no redirects when compatibility is not needed.
- ADP met it. On deivid's decision it removed eleven stub pages; three had
  frozen or dated links, which now resolve through rows in ADP's location
  map. The coordinator advised that without having read the stub sentence.
- deivid chose "owner decides". The sentence now names both ways and what
  each costs: a hidden stub also keeps the published address; the path
  adapter keeps the links resolving for lint and lets the address go. Lint
  already rejects a frozen or dated link that neither covers.
- The page for people that repeats the sentence is brought in step, and the
  3.2.1 notes list the change.
- Checks: strict lint of the kit site.

## 2026-11-11 — Say when a source pin stands for producing code

- ADP's experiment folders carry a source copy per run, and its open record
  on experiment paths proposes a commit pin instead. The record rule listed
  "producing code" and "source pins" together without saying when a pin is
  enough.
- deivid approved the sentence: a pin stands for code in the repository when
  the run started from a clean tree, the commit stays reachable on a branch
  or tag that is never rewritten, and the experiment directory records the
  pin, the command and the input identities. Code that was never committed,
  or that lives outside the repository, stays as a copy or a diff.
- How a project keeps a pinned commit reachable is its own choice. A run
  made from a dirty tree cannot be converted to a pin afterwards.
- The page for people that restates the retention list, Documentation and
  writing, gains both this sentence and the storage principle from the entry
  below, which had not been added to it. The 3.2.1 notes list the change.
- Checks: strict lint of the kit site.

## 2026-11-11 — Separate experiment retention from exact copies of superseded documents

- ADP asked whether its sentence "retain the smallest set of files that lets
  a reader check a named finding" conflicts with the kit. The kit's own text
  invited the question: `rules/records.md` lists what an experiment keeps,
  and `rules/documentation.md` said "preserve exact evidence only when its
  identity has a concrete purpose" in a bullet about removing superseded
  documents. Neither named its scope.
- deivid approved two wording changes. The documentation rule now speaks of
  a byte-exact copy of a superseded document and says that it does not
  shorten what an experiment retains. The record rule gains the principle
  that repository size decides where material is stored, not whether it is
  kept, and that material outside Git is located and identified from the
  experiment directory.
- A first draft pointed to the local-artifact manifest. deivid questioned
  it: the manifest only covers files that documents link to, so the sentence
  names no mechanism and leaves storage to the project.
- deivid approved this "for now". Whether a project may narrow the kit's
  list for size reasons is not decided; ADP's choice between scoping its
  sentence to Git and a recorded exception is still open in ADP.
- The page for people that repeats the documentation rule is brought in
  step, and the 3.2.1 notes list the change.
- Checks: strict lint of the kit site.

## 2026-11-10 — Let pages carry invariant markers, as the build already renders them

- ADP's topic-record work was about to remove 35 `INVARIANT` and `DON'T-REDO`
  labels from seven pages, because the rule said such markers must not appear
  on rendered pages. deivid asked to change the rule instead.
- The rule and the tooling disagreed. `markers_to_callouts` in
  `tooling/build.py` turns a marker at the start of its own paragraph into a
  card with a reader label, and lint says the declarations belong on pages.
  On ADP's built pages 28 of the 35 markers are cards and 7 show the raw
  label; those 7 sit inside a sentence or a list item (counted by ADP's
  session; three pages checked here and they match).
- deivid approved this wording: a page may show a marked statement in its own
  paragraph; a marker inside a sentence or a list item gets its own paragraph.
  The record still owns the rule. He chose this over rendering inline markers
  as a chip, which would have needed new build code.
- The page for people that repeats the rule, Documentation and writing, is
  brought in step. The release notes gain a 3.2.1 section, not yet tagged.
- Not read by an independent reviewer yet; three more wording fixes are
  queued and the review covers them together.
- Checks: strict lint of the kit site.

## 2026-11-10 — Withdraw the 375 px drawer observation

- The entry on ADP's trial recorded an open observation: the reader drawer
  looked clipped at 375 px. ADP withdrew it after tracing it. The cascade is
  correct: `.reader-enabled.reader-nav-open .sidebar {transform:none}` wins.
  The computed transform stayed at its start value because the browser pane
  used for the check was hidden, so the page ran in the background and the
  transition never advanced.
- No kit change. The kit's captures at 390 px, taken in a visible headless
  page, show the drawer in place.
- Checks: strict lint of the kit site.

## 2026-11-10 — Release 3.2.0

- deivid chose to release after ADP's trial. The trial passed without a kit
  defect, so `VERSION` is `3.2.0`. The release notes no longer say that the
  release is untagged, and the README, project context and index name 3.2.0 as
  the current release with its guide first.
- The tag `v3.2.0` goes on the commit of `main` whose Pages workflow passes.
- Not read by an independent reviewer: the corrections made after the review
  of the two settings, the three clarified guide steps and this commit.
- Checks: `tests/run_checks.sh` with the browser suites passes (179 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Clarify three steps of the 3.2.0 guide after ADP's trial

- ADP tried kit commit `d7a9d2d` on a local branch that was never pushed. It
  moved four topics into `docs/topics/parked/`, two of them renamed on
  deivid's decision, and folded the "Parked" group. Its report: the build
  gives the same 24 pages apart from the two renamed ones, lint has no dead
  link and only the expected error for the unpushed pin, and the folded group
  behaves as designed, wide and at 375 px. Checked here: the trial branch
  pins `d7a9d2d` and holds the four folders. ADP's twelve checks were not
  rerun here.
- ADP found no kit defect. Its own code needed two changes, both outside the
  kit's sight: an evidence validator that accepted a topic path only at one
  depth, and a test that listed the folders under `docs/topics/`.
- Three guide steps were unclear and are corrected: the search step now names
  code that checks the shape or depth of a topic path; the frozen-file step
  says to update the recorded path before any bulk edit, because a bulk
  replacement rewrote ADP's frozen file and only its evidence check caught
  it; the comparison step says that a folder renamed on purpose changes its
  address.
- Open observation from the trial, not from 3.2.0: at 375 px ADP saw the
  reader drawer clipped at its left edge, on the published 3.1.0 site as well.
  The kit's own captures at 390 px show the drawer in place. Not reproduced
  here yet.

## 2026-11-10 — Topic group folders and folded navigation groups

- deivid asked, through ADP's topic-record work, for a folder of folders under
  `docs/topics/` and for one sidebar group that folds. ADP keeps four parked
  topics and wants them apart from its current ones in the source tree and in
  the sidebar.
- `topic_group_folders` names folders under `docs/topics/` that hold topic
  folders. Discovery is now one function, `topic_pages` in
  `tooling/topic_structure.py`; `site_paths`, `record_changes`, `source_pages`
  and the topic structure check all use it. The setting is explicit because a
  topic folder may already hold a file named `index.md` two levels down, and
  guessing would turn such a file into a page.
- The page's address stays `<topic>.html`. The build already took the address
  from the topic folder's name, and it already rejected a duplicate.
- `folded_groups` turns a named group of the flat site tree into a native
  disclosure. It keeps the section's look and gains a chevron. `nav.js` stores
  the reader's choice with the same code as `nested_nav`.
- Lint gains a note for a page two levels down in an undeclared folder.
- The rule text is in `rules/site/authoring.md` and one sentence in
  `rules/documentation.md`. The [release notes](topics/releases/releases.md)
  and the [3.2.0 migration guide](topics/releases/migrations/3.2.0.md)
  describe the change for consumers. `VERSION` stays `3.1.0` until deivid
  approves the release.
- An independent reviewer read the working tree before the commit: no blocker,
  two corrections and six minor points. Corrected: the rule and the guide said
  that page-body links stay as they are, which is wrong for a link into the
  moved folder itself; the guide omitted `page_css`, `[[source_pages]]`,
  `[extra_assets]` and `OPEN.md` paths; a folded group that other entries
  split is now rejected; the home entry's group no longer counts as a group to
  fold. Left as they are: a stored group cannot be closed on the page where it
  is open by default, which `nested_nav` has too, and a page three levels down
  gets no note.
- By eye, on a scratch site at 1600×1000 and 390×844: the folded group closed
  on pages outside it, open with the chapters inside it on its own pages, no
  horizontal overflow, the reader's choice kept on the next page, and opening
  without JavaScript.
- No browser suite covers the folded group; the kit's own site and the starter
  do not set it.
- Not checked in a consumer: ADP's four pages, its own code that walks
  `docs/topics/`, and frozen files inside a moved folder.
- The pages for people that explain the changed rule sections (Build a site,
  Get started, Documentation and writing) describe the default layout,
  `docs/topics/*/index.md`, which is unchanged. They do not mention the two
  settings.
- Checks: `tests/run_checks.sh` with the browser suites passes (179 tests,
  strict lint, 22 scripts, four suites, 40 pages).

## 2026-11-10 — Release 3.1.0

- deivid approved the release after the pre-tag review and its corrections.
  `VERSION` is `3.1.0`. The release notes no longer say that the release is
  untagged, and the README, project context and index name 3.1.0 as the
  current release with its guide first.
- The tag `v3.1.0` goes on the commit of `main` whose Pages workflow passes.
- Not read by an independent reviewer: the review corrections (`7bea608`), the
  name decision record (`119c0ec`) and this commit.
- Checks: `tests/run_checks.sh` with the browser suites passes (172 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Record the open decision on the kit's name

- deivid asked whether "Documentation kit" is still the right name. About a
  quarter of the rule text is engineering and experiment practice, and the kit
  names itself two ways. Six candidates were proposed; deivid is not happy with
  any of them. The question, the candidates and the cost of each rename layer
  are in [open work](open/kit-name.md). Nothing is renamed.
- Checks: strict lint of the kit site.

## 2026-11-10 — Correct the 3.1.0 changes after the pre-tag review

- An independent reviewer read everything since `v3.0.0` before the tag. It
  found no blocker and ten findings; all are addressed here.
- A blank `home_label` built in 3.0.0, and the new validation made it fail,
  which the version promise counts as a major change. A blank value now counts
  as unset; only a value that is not text is rejected, and that already failed
  in 3.0.0 with a traceback.
- The 3.1.0 guide said `home_label` was not shown anywhere before 3.1.0. That
  holds only for 3.0.0: up to 2.0.0 the reader drawer showed it. The guide and
  the release notes now give that history, name `brand` as deprecated without
  a replacement, say that source pages show `home_label` too, and say that
  changing the name resets two saved browser preferences once.
- The 3.0.0 guide routed regression gates to the experiment workflow guide;
  they live in the verification guide. The 2.0.0 guide said every consumer adds
  three router rows; only a project that runs experiments adds the two
  experiment rows.
- Correction to the entry below: it counts three new tests. Its commit added
  two. This commit adds one more, for the source-page header, and extends two:
  the declared local artifact is now also checked in built HTML, and blank and
  non-text `home_label` values are covered. Not covered by a test: the note for
  a missing image or script resource, because the build fails first.
- Checks: `tests/run_checks.sh` with the browser suites passes (172 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Name the site once in the sidebar header

- deivid chose this over changing ADP's pages. The sidebar header now shows
  `home_label`, or `title` when `home_label` is not set, on every page. It
  used to show each page's `brand` frontmatter. The kit and adapt copied their
  site name onto every page; ADP wrote page names there, so its header read
  "track-geometry" while linking to the home page. `brand` is still accepted
  and no longer read.
- Before this change `home_label` was not shown anywhere in 3.0.0. The kit's
  own `home_label = "Kit"` and the starter's `home_label = "Docs"` are removed,
  so both show their title. The `brand` lines are removed from the kit's six
  pages and the starter's two.
- A one-character `brand_mark` gets the class `brand-mark-glyph` and is drawn
  at 21 px instead of 12 px. An independent reviewer of ADP's upgrade had
  judged ∿ faint.
- The header change alters the shared look, so the pending release is 3.1.0,
  not 3.0.1 as the entry below says. It has a
  [migration guide](topics/releases/migrations/3.1.0.md) with one step. The
  open-work record for ADP's upgrade findings is removed: all five gaps are
  fixed. Two worklog links to it now point at the release notes; their wording
  is unchanged.
- Three new tests fail on the old code and pass now. Checks:
  `tests/run_checks.sh` with the browser suites passes (171 tests, strict lint,
  22 scripts, four suites).

## 2026-11-10 — Add two instructions that ADP's upgrade showed were missing

- The 2.0.0 guide gains a section for the experiment guides: add the two router
  rows, compare the router with the starter's row by row, and repoint sentences
  about the experiment floor. ADP had followed the guide and had neither row.
- The 3.0.0 guide says that `#run-visuals-and-experiment-lifecycle` covered two
  subjects. A link about the experiment floor goes to
  `rules/experiments/workflow.md#required-content`; the anchor table sent it to
  the figures guide, which only forwards. Lint cannot tell the two apart.
- Both gaps leave open work; the reader header and the mark size remain there.
  ADP already has both corrections, in its commits `b44a55d2` and `1b7e0087`.
- Checks: `tests/run_checks.sh` with the browser suites passes (169 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Let strict lint pass where a project declared the state

- ADP could never pass `lint --strict`: 2 warnings reported files that its
  local-artifact manifest lists as kept locally on purpose, and 19 reported old
  worklog entries without a commit hash, which an append-only worklog cannot
  change. deivid approved both changes.
- A link to a file listed under `omitted_files` now gets a note when the file
  is absent. Notes never fail. A missing file that is not listed stays an
  error.
- The worklog hash check is removed. It recognised only bold-bullet entries, so
  it checked neither the kit's own worklog nor ADP's newer entries. The written
  rule that a landing records its commit is unchanged.
- The version promise gains the patch level: a patch corrects a defect or
  relaxes a check and needs no migration step. The release notes carry these
  changes as 3.0.1, not tagged yet.
- Two new tests fail on the old code and pass now. Checks:
  `tests/run_checks.sh` with the browser suites passes (169 tests, strict lint,
  22 scripts, four suites). ADP's branch `upgrade-kit-3.0.0` linted with this
  code reports 24 warnings, down from 45, all of them topic pages without a
  record.

## 2026-11-10 — Add ADP's couplings to the simplification record

- The [simplification record](open/simplify-frozen-record-machinery.md) gains
  three couplings that ADP's upgrade showed: tests that use private kit names,
  Node checks that read kit theme sources, and ADP's group names and `--adp`
  in four kit stylesheets. deivid decided to keep ADP's five compatibility
  layers until the frozen-record shape is chosen; ADP's own open-work record
  holds their sizes.
- Checks: strict lint of the kit site.

## 2026-11-10 — Add the missing router step to the upgrade findings

- A fifth gap from ADP's upgrade: kit 2.0.0 added the two experiment guides and
  their starter router rows, but the 2.0.0 migration guide has no step that
  adds the rows to an existing project. ADP added them in its commit
  `1b7e0087`. The gap is in [open work](topics/releases/releases.md#310--one-site-name-in-the-sidebar-header-two-lint-warnings-relaxed).
- Correction: the reviewer of ADP's upgrade reported the missing rows as older
  than the upgrade. `rules/experiments/` does not exist at `v1.1.0`.
- Checks: strict lint of the kit site.

## 2026-11-10 — Record what ADP's upgrade to 3.0.0 showed about the kit

- ADP was upgraded from 1.1.0 to 3.0.0 on its own branch, not yet merged. Its
  12 validation commands pass, and all 35 pages keep their chapter, fold,
  figure, formula and link counts against the 1.1.0 build.
- The upgrade showed four gaps in the kit, now in
  [open work](topics/releases/releases.md#310--one-site-name-in-the-sidebar-header-two-lint-warnings-relaxed): the 3.0.0 guide maps one anchor to
  a guide that only forwards the experiment floor; the reader header shows each
  page's `brand`, which ADP sets per page; strict lint cannot pass in ADP; the
  ∿ mark is faint in its box. No kit code changed.
- Checks: strict lint of the kit site.

## 2026-11-10 — Release 3.0.0

- deivid approved the release after the pre-tag review. `VERSION` is `3.0.0`.
  The release notes and the 3.0.0 migration guide no longer say that the
  release is untagged, and the README, project context and index name 3.0.0 as
  the current release with its guide first.
- The tag `v3.0.0` goes on the commit of `main` whose Pages workflow passes.
  This push is the first run of the workflow's split into a check job without
  deploy rights and a publish job.
- Not read by an independent reviewer: the review fixes (`59cb1e8`), the page
  sync (`71e66e6`) and this commit.
- Checks: `tests/run_checks.sh` with the browser suites passes (167 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Bring the pages in step with the pre-tag rule changes

- The rule changes from the pre-tag reviews were more than a small sync, so
  they went to the page agent that wrote these pages before. Its brief named
  the guides to read. It changed Documentation and writing, Engineering and
  Get started: a new page needs a request while an existing page follows its
  record, also across added or removed chapters; delegation applies where the
  runtime supports it; gaps go to the delegating agent; captures cover each
  supported width and reader view; `page_number_notes` is one setting for the
  whole site.
- The page agent reported two record wordings back, and they are fixed here.
  The record-change paragraph said "in the same change" where the order of
  work says "in the same deliverable, after the record". The delivery guide
  said "the owner's own page writing"; it now names the working agent. The
  documentation guide also says why a chapter links the section it explains:
  a chapter that links only the whole record is not listed when a section
  changes. Two page phrases were synced to these by the record's editor.
- Checks: `tests/run_checks.sh` with the browser suites passes (167 tests,
  strict lint, 22 scripts, four suites); no fold is 50% or more copied. The
  page agent captured each changed chapter at 1600 and 390 px, and Record
  first also in the Two chapters view; the Record first captures in both views
  were looked at here.

## 2026-11-10 — Fix what the two pre-tag reviews found

- Before the release tag, two independent reviewers looked at `b806c5d`, each in
  its own clone. One reviewed the code changed since `v2.0.0`. The other built
  a simulated 2.0.0 consumer, moved it to `b806c5d` and followed the 3.0.0
  migration guide cold. Both ran the full gate and it passed. Neither found a
  defect that blocks a consumer; the release reviewer noted that `VERSION` and
  the "not tagged yet" text still need the release commit. Every finding below
  was confirmed against the files first.
- Code, each with a test that fails without the fix:
  - The page-end marker was never found, because comments were blanked before
    the search. Numbers below the marker were read, and links in the notes
    tail resolved against the wrong folder. The earlier test passed for the
    wrong reason.
  - A page number such as `2.5x` was read as `2`; numbers are now read whole.
  - A "<" in prose blanked everything up to the next ">".
  - A changed record whose name contains a space, and a content line that
    starts with `++ `, were lost from the record-change notes.
  - `docsite.py slides` loaded `slide-face.css` twice once asset links carried
    a version query.
  - A pinned record that is also in the navigation was marked current twice.
  - A brand-mark SVG that starts with an XML prolog or a comment was rejected.
  - The page-number note read a registered route that points outside the
    project.
- Also in code: a paragraph glued to a closing fold, with no blank line, now
  renders too; the group selector in `nav.js` is escaped with `CSS.escape`; one
  source-page test no longer depends on `GITHUB_SHA`, so the workflow stops
  unsetting it; `tests/run_checks.sh` fails when `DOCS_PLAYWRIGHT` is set but
  does not load, and gives the unreachable bus address to the suites only.
- `.github/workflows/pages.yml` is split into two jobs. The job that installs
  and runs third-party code has no deploy rights; the second job only deploys.
- Rules: a page means a page for people; a new page needs a request, and an
  existing page follows its record also when it gains or loses a chapter; a
  small sync needs no page guides; a gap or contradiction a page agent finds
  goes back to the delegating agent; the conformance pin item matches the Git
  guide; `page_number_notes` is described as one setting for the whole site,
  with what it does not read.
- 3.0.0 guide and release notes: lint checks Markdown links only, so the
  searches must be worked through; the topic-record steps name the deletion
  approval first and say what "exact" means; landing steps are linked; theme
  changes and the Git-guide correction are listed; the version promise covers
  new build failures.
- Open work added: lint does not check HTML links to repository files.
- Not fixed, by choice: anchors removed from the kit's own pages are not listed
  in the release notes; hard-coded group names for colours remain in
  `base.css` and `chapter-reader.css` from before 2.0.0; flat navigation no
  longer scrolls the current entry into view.
- Checks: `tests/run_checks.sh` with the browser suites passes, also with
  `GITHUB_SHA` set as on a runner.

## 2026-11-10 — Take the guide and chapter counts off the Get started cards

- The three practice cards on Get started were labelled with counts such as
  "6 guides · 12 chapters". No record states those counts, the page-number note
  listed 6, 12 and 7, and the counts had drifted when the guides were
  restructured. deivid approved removing them. Each card is now labelled by
  what it covers: code, runs and delivery; records and pages; investigations
  and qualifications.
- Checks: `tests/run_checks.sh` with the browser suites passes (157 tests,
  strict lint, 22 scripts, four suites); lint prints no page-number note for
  the kit site; the cards were captured at 1600 and 390 px and reviewed.

## 2026-11-10 — Add optional lint notes for page numbers no linked record states

- deivid asked whether a rule ensures that numbers on pages for people have a
  verified source. The rule chain existed: a page adds no number its record
  lacks, and a record's number needs its provenance. No check enforced the
  first link. A report by a page agent was rejected as the mechanism, because
  often no page agent exists.
- `tooling/page_numbers.py` is new. For each topic page it reads the numbers
  in the prose and lists those that appear in none of the records the page
  links, grouped by chapter. Code, inline SVG, attributes, link targets,
  versions, dates, ratios and labels are not read; a page that links no record
  is skipped. Lint prints the result as notes, which never fail a run.
- The notes are off unless the site sets `page_number_notes = true`. Run
  against the consumers' working trees with the note forced on, it listed
  1,790 numbers on 17 pages in ADP and 2,679 on one page in adapt. Those pages
  report measurements from experiment data, rounded or derived, so the numbers
  match no text. The setting suits pages that explain Markdown records; a
  project with measured pages keeps its own ledger check, as adapt does.
- On the kit's own site, turned on, the note found two cases. The 900 px
  sidebar breakpoint on Build a site was in the reader code
  (`chapter-reader.js`) and in no guide; `rules/site/reader.md` now states it.
  The counts of guides and chapters on the Get started cards (6, 12, 7) are in
  no record; the note stays until deivid decides about them.
- The documentation guide, the authoring guide, the conformance check, the
  release notes, the 3.0.0 guide and the In step chapter describe the setting.
- Checks: `tests/run_checks.sh` with the browser suites passes (157 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-10 — Render the paragraph after a fold; make the page brief name its guides

- The page agent reported that a paragraph directly after a fold showed as raw
  Markdown, for example a "Full guide" line with its links unrendered. The
  built kit site had 24 such lines on two pages. The cause is in
  `tooling/build.py`, unchanged since 2026-11-04: the closing fold marker
  matched trailing whitespace across lines, swallowed the blank line after it,
  and Markdown then read the next paragraph as part of the HTML block.
- Both fold markers now match to the end of their own line only. A new test in
  `tests/test_site_contract.py` builds a page with a paragraph after a fold; it
  fails without the change and passes with it.
- deivid asked whether a delegated page agent is told which guides to read.
  The rule told the page author to read them but did not require the brief to
  say so, and a delegated agent knows only its brief.
  `rules/engineering/delivery.md` now requires the brief to name the guides.
  Two page sentences that describe the brief were synced by the record's
  editor, as a small sync.
- Checks: `tests/run_checks.sh` with the browser suites passes (149 tests,
  strict lint, 22 scripts, four suites). No raw "Full guide" line remains in
  the built site; the end of the Record first chapter was captured at 1600 and
  390 px and reviewed.

## 2026-11-10 — Fix what an independent review found in the restructured guides

- deivid asked whether a subagent had reviewed the changes. None had. A
  read-only reviewer then compared the guides at `30bfbb2` with `588d9e9` and
  with `v2.0.0`. It found no dropped rule sentence and no blocker, and these
  defects, all confirmed against the files and fixed here.
- Two rules disagreed about pages. One said a page changes only on a person's
  request; another said to update the explaining pages whenever a record
  section changes. Now: a new page or chapter needs a request, an existing
  page is always kept in step with its record, and the size decides who does
  it. One term, small sync, replaces two.
- Moving record rules out of the page guides had dropped math, code and visual
  claim rules from the record author's route. `rules/records.md` now names
  them in Excerpts, formulas and figures.
- The router rows reached too little. The record row now names the sections of
  `rules/documentation.md` from Record first through Rules for changes; the
  page row names Rendered pages are for people; the publishing gate links the
  review and deletion gates. `OPEN.md` format, checked by lint since before
  2.0.0, is now written down.
- The 3.0.0 guide gained a frozen-copy exception, a search for section names
  written without a link, three title anchors, the starter reading-index rows
  and a complete list of changed guides. The release notes gained three rows
  and say outright that section anchors under `rules/` are stable.
- Stale wording fixed in `tooling/lint.py`, `rules/conformance.md`,
  `rules/engineering/performance.md`, `rules/experiments/workflow.md`,
  `docs/KIT_INDEX.md`, `docs/KIT_CONTEXT.md` and the 1.1.0 guide.
- Left as it is: the ledger paragraph in Numbers and staleness speaks about
  page redesigns but binds the numbers a record states.
- Correction to the entry below: it said a record edit routes to about 1,130
  words. That route was incomplete. Counting whitespace-separated words, the
  record row now leads to `rules/records.md` (966) plus `rules/documentation.md`
  from Record first through Rules for changes (1,066): 2,032 words. At
  `588d9e9` the same job led to at least 2,862 words (`documentation.md` 2,028,
  `evidence.md` 423, `explanations.md` 411) and to 3,971 with `pages.md`.
- The six pages for people were updated by a page agent (Opus, effort high)
  from the records, as the new rule asks. It aligned them with the fixes above
  while they were being made. Documentation and writing gains the chapter
  Record first with a flow figure, and its chapters are ordered system,
  records, pages; anchors added are `#record-first` and `#fig-record-first`,
  none renamed. The page agent took the word counts off the page because the
  earlier figure had no stated method.
- The page agent found a renderer defect that predates this work: a paragraph
  directly after a fold renders as raw Markdown. It is fixed in the next entry.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites), run again here after the page agent's
  own run. 42 captures of the changed chapters at 1600 and 390 px are under
  `.build/visual-review/pages-restructure/`; the new chapter and the routes
  chapter were looked at here.

## 2026-11-09 — Give records their own guide; record first, page on request

- deivid decided how documentation work is split. The agent that did the work
  writes the record in Markdown first. A page for people is made only when a
  person asked for one, by a separate agent that receives the finished record
  as its brief and is kept for later page requests in the same work. A
  one-line page sync stays with the agent that edited the record.
- Why: the rule files did not separate the two jobs. The router row for
  writing fired for records too, record rules sat inside page guides, and page
  review sat in the placement guide. A record writer was led to between 2,941
  and 4,050 words of guides.
- `rules/records.md` is new and gathers what a record needs: one record per
  topic, format, naming and honest claims, numbers and staleness, frozen
  evidence and shelved investigations. `rules/documentation.md` keeps placement,
  the new section Record first, page on request, lifecycle and changes.
  `rules/writing/` covers pages only; `rules/writing/evidence.md` is removed
  and its run-visuals section moved to `figures.md`. Local review and browser
  access moved to `rules/site/validation.md`, the publishing gate to
  `rules/site/publication.md`. `rules/engineering/delivery.md` gains Delegating
  a page for people. No rule text was dropped; moved sections keep their
  anchor names.
- The kit router and the starter router have three documentation rows in
  place of two. A record edit now routes to `rules/records.md` and one section
  of `rules/documentation.md`: about 1,130 words.
- 42 links in the kit were repointed to the new locations. The 3.0.0 guide lists the moved sections and the new router
  rows; the release notes carry a row.
- The pages for people still explain the old guide layout; only their link
  targets were repointed here. Their update is delegated next, as the new rule
  asks.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-09 — Keep the worklog and state why it repeats commit messages

- Measured: this worklog has one entry per commit, 62 and 62, and an entry
  repeats its commit message. Over the last 12 commits the messages hold 2,051
  words and the entries 2,236, and 81% of a message's vocabulary also appears
  in its entry. ADP's worklog is 10,611 lines and 777 KB.
- deivid decided to keep the worklog as it is. The cost is small: a second
  write per commit, and rare link repairs. The file reads without Git,
  survives squashed or rebased history and holds probes and decisions that
  belong to no single commit.
- `rules/documentation.md` now states that the overlap is deliberate, gives
  those reasons and names when to reconsider: a worklog that becomes slow to
  lint or awkward to search. The worklog fold on Documentation and writing
  says the same in its own words.
- Node 22 was listed as a concern earlier today. It is void: Node 22.23.3 is
  installed here under nvm, and only the default shell uses Node 20.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-09 — Remove the router stub headings; the pending release becomes 3.0.0

- deivid decided to remove the stub headings from `rules/writing.md` and
  `rules/maintenance.md` now and to name the pending release 3.0.0. This
  replaces the 2.1.0 name chosen earlier today. The stubs only forwarded links
  written before the guides were split; both files are now plain indexes that
  list each focused guide and what it owns.
- Why major: ADP holds 25 live links to the removed anchors, adapt 2 and
  adaptation 3. Their lint fails without `--strict` until the links are
  repointed, which the version promise calls a major change.
- The migration guide is renamed to `migrations/3.0.0.md` and gains a Router
  anchors step with the mapping from each former anchor to its guide; the
  mapping was checked against the guides' headings. The release-notes section,
  the site navigation and route, the own-site browser test and the pointers in
  README, context and index now say 3.0.0. Nine links in the release notes
  point at the focused guides. `VERSION` stays 2.0.0 until the tag.
- Lint also checks this worklog. 7 links in older entries pointed at the
  removed anchors; only their targets were repointed, the entries' wording is
  unchanged. The migration guide tells projects to do the same.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites); the two index pages and the new guide
  were captured at 1600 and 390 px and reviewed.

## 2026-11-09 — Remove consumer-specific text and a dead compatibility name

- deivid asked to fix the places where the kit broke its own placement rules,
  since the consumer upgrades are coordinated from here anyway.
- `tooling/lint.py` loses `sdk_document_locations()`, a compatibility name
  with no caller in the kit, ADP, adapt or adaptation.
- `docs/KIT_CONTEXT.md` no longer lists source coverage under `rules/`; that
  map was removed in 2.0.0.
- The 2.0.0 migration guide loses its section for adapt, and the
  panel-switcher record loses its instruction for ADP's adoption. Consumer
  steps belong in each consuming project. Both texts remain at the pushed
  [`v2.0.0` tag](https://github.com/davszi/documentation-kit/blob/v2.0.0/docs/topics/releases/migrations/2.0.0.md);
  adapt still pins the unpushed commit `101cea4`, so its upgrade plan takes
  those eight steps from there.
- Not changed: the stub headings in `rules/writing.md` and
  `rules/maintenance.md`. ADP, adapt and adaptation hold 30 live links to
  them; removing them breaks lint without `--strict`, which the version
  promise calls a major change. That choice is deivid's.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites).

## 2026-11-09 — Rewrite the remaining copied folds for people

- deivid approved the style of the Engineering pilot below. The same rewrite
  is applied to 25 folds on Documentation and writing and 2 on Experiments:
  situation and reason first, plain wording, labelled paragraphs where a fold
  covers several things. Reference tables and code samples stay; no rule,
  number or limit was added.
- One fold was stale against its record: The README exception said existing
  projects may retain compatibility routes, while `rules/documentation.md`
  sends that question to refactoring over compatibility. The fold now links
  there.
- Measured with the same seven-word count: fold text copied from rules went
  from 78% to 13% on Documentation and writing (2,794 to 3,745 words) and from
  36% to 17% on Experiments (471 to 544 words). No fold on any page is 50% or
  more copied. The pages now hold 22,749 words. Whole pages are 15%, 11% and
  19% copied; what remains is in the visible story, which was not changed.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites); five rewritten folds, including the
  block table and two code samples, were captured open at 1600 and 390 px and
  reviewed.

## 2026-11-09 — Rewrite the Engineering page's copied folds for people

- The gate from the entry below is verified on GitHub: workflow run
  42705539031 for `d6b45aa` passed every step, including 148 tests and the four
  browser suites on a runner, and deployed the site.
- Measured: the pages for people hold 21,081 words against 13,238 under
  `rules/`. Counting runs of seven or more consecutive words identical to rule
  text, the folds were mostly pasted rules: 78% of 2,794 fold words on
  Documentation and writing, 62% of 1,084 on Engineering, 36% of 471 on
  Experiments. The visible story was 14–19% copied.
- deivid decided that the pages stay, that folds do not become links to the
  records, and that readers should not have to leave the HTML pages; pasted
  agent-centric text is rewritten for people instead.
- Engineering: 15 folds rewritten in plain wording, each opening with the
  situation and the reason before the steps. No rule, number or limit was
  added. The folds went from 62% to 4% copied and from 1,084 to 1,728 words.
- Still to do: 24 folds on Documentation and writing and 2 on Experiments.
- Checks: `tests/run_checks.sh` with the browser suites passes (148 tests,
  strict lint, 22 scripts, four suites); four rewritten folds were captured
  open at 1600 and 390 px and reviewed.

## 2026-11-09 — Gate checks and the Pages deploy on the browser suites

- deivid chose a local and a CI gate for the shared scripts. The four browser
  suites passed but ran only by hand, and the Pages workflow ran no tests: a
  push to `main` published the site even with failing unit tests.
- `tests/run_checks.sh` now runs `node --check` on 22 shared scripts and then
  the four browser suites when Playwright resolves; otherwise it prints that
  they were skipped. `DOCS_REQUIRE_BROWSER=1` makes a missing Playwright fail.
  `DOCS_NODE` selects the Node binary. Each suite gets a 280-second limit and,
  where `systemd-run --user` works, the 4G cap without swap.
- `.github/workflows/pages.yml` installs Node 22 and Playwright 1.62.1 with
  Chromium, runs the script with the browser suites required and deploys only
  after it passes. It unsets `GITHUB_SHA` for the checks: with it set,
  `test_source_origin_routes_media_and_literal_markers` fails because source
  links then pin the commit instead of `main`.
- Measured here on Node 22.23.3: the suites take 6.6 s, 2.2 s, 0.8 s and
  100.8 s; the whole script takes 121 s with them and about 11 s without.
- Checks: the script passes with the suites (148 tests, strict lint, 22
  scripts, four suites), passes with a skip message without Playwright, and
  exits 1 when the suites are required but Playwright is missing. Not checked:
  the workflow itself, which runs only after a push; the suites have not run
  on a GitHub runner.

## 2026-11-09 — Ship the kit's license in every built site

- deivid asked that built sites carry the kit's license. A built site holds
  the kit's styles and scripts, and the MIT License asks that its notice go
  with copies; the build already copied the vendor licenses but not the kit's
  own. `gather_assets` now writes `html/assets/documentation-kit/LICENSE`.
- A project `extra_assets` entry with that output name fails the build through
  the existing shared-asset collision check; a test covers it.
- The README License section, the 2.1.0 release notes and the 2.1.0 migration
  guide name the new file.
- Checks: `tests/run_checks.sh` (148 tests) and strict lint pass.

## 2026-11-09 — License the kit under MIT

- deivid chose the MIT License for the kit's own files. The repository was
  public without a first-party license, so nobody else could legally reuse it,
  while the README invites projects to add it as a submodule. `LICENSE` is
  added; the README gains a License section in place of the sentence that no
  license was selected; `THIRD_PARTY.md` says the MIT License does not cover
  the bundled fonts and KaTeX.
- Not checked: whether anyone besides deivid holds rights to the kit. All 55
  commits before this one have deivid as author.
- Checks: `tests/run_checks.sh` (146 tests) and strict lint pass.

## 2026-11-09 — State what a version number promises; add the 2.1.0 migration guide

- deivid decided the untagged work after 2.0.0 becomes 2.1.0, a minor release,
  and that the release notes say what a version number promises: a major
  release removes or renames a stable interface or adds a lint error that fails
  without `--strict`; a minor release may add lint warnings, change the theme's
  look and change or remove a provisional interface.
- Why minor: adapt, adaptation and ADP all run lint without `--strict` in their
  workflows, so the new topic-record warning fails none of them. The upgrade
  still costs work, because the conformance check runs strict lint; measured in
  the working trees, 24 of ADP's 35 topic pages and 2 of 3 in adapt and in
  adaptation have neither a record nor `page_only`.
- `docs/topics/releases/migrations/2.1.0.md` gives the steps: topic records,
  the router row for the conformance check, the sidebar mark, the removed
  ledger modules and the starter home link. The site lists it in the Releases
  group. The release-notes section is headed 2.1.0 and marked not yet tagged;
  `VERSION` stays 2.0.0 until the tag.
- Checks: `tests/run_checks.sh` (146 tests) and strict lint pass; the own-site
  browser suite passes; the new page and the sidebar were captured at 1600 and
  390 px and reviewed.

## 2026-11-09 — Open the work to simplify frozen-record machinery

- deivid stated that parts of ADP's documentation system became too
  complicated and that simplifying them is our work. The frozen-record chain
  is one such part: old documents kept byte-exact in the live tree and still
  link-checked need a path translator, hash manifests and a validator in ADP
  and adapt, plus adapter hooks and rule text in the kit.
- `docs/open/simplify-frozen-record-machinery.md` holds the direction, the
  measured sizes, the order constraint and the undecided choices;
  `docs/open/KIT_OPEN.md` routes to it. No target shape is decided.
- Checks: strict lint passes for the kit's own site.

## 2026-11-09 — Remove the unused number-ledger and verbatim-lock modules

- deivid approved removing shared tooling that no project uses. A search of
  adapt, adaptation and ADP, across every local and remote-tracking branch and
  the working trees, found no import of `tooling/number_ledger.py` or
  `tooling/verbatim_blocks.py`. adapt and adaptation check their ledgers and
  locks with their own `docs/site/checks/test_chapter_facts.py` and
  `test_content.py`. Both modules, their tests and their paragraph in
  `rules/site/authoring.md` are removed.
- `tooling/svg_figures.py` stays: generators in adapt and adaptation import it.
- The ledger and lock rule in `rules/writing/evidence.md` stays and now says
  the project owns the ledger format and checks. The Evidence chapter of
  Documentation and writing says the same.
- Checks: `tests/run_checks.sh` (146 tests) and strict lint pass.

## 2026-11-09 — State why pages and records overlap; document capped browser suites

- deivid approved two drafts. `rules/documentation.md` now says a page and its
  record overlap on purpose for different readers, and that the record is
  authoritative: a page adds no rule, number or limit the record lacks. The
  Topics chapter of Documentation and writing says the same in its own words.
- `README.md` now shows the browser suites run under a 4G memory cap without
  swap, with `DBUS_SESSION_BUS_ADDRESS` pointed at a missing socket. This
  machine's Playwright, Chromium and Node paths stay out of the kit.

## 2026-11-09 — Fix what a fresh reader found, require by-eye review, undock the Reference section

- A fresh agent read the kit with no session context. It found stale or
  contradictory statements; fixed: the 2.0.0 notes no longer say the release
  number is undecided; the reading index and the website source page no longer
  call hosting open; `git.md` now matches `kit_pin.py` (remote branches only,
  tags do not count, shallow checkouts and copies without Git are skipped); the
  1.1.0 guide notes that 2.0.0 removes the old manifest fallback; the
  publication source page mentions `publish`.
- The starter home linked `../project/PROJECT_CONTEXT.md`, which resolved to a
  missing `docs/project/` file; it now links `docs/PROJECT_CONTEXT.md`. Strict
  lint did not catch the broken repository link in the raw home page.
- deivid: which topics may be page-only is not settled; the rule now says so
  and names the kit's explanation pages as the one known case.
- deivid asked that visual changes be reviewed by eye; `rules/site/validation.md`
  now requires whole-element captures at each supported width and reader view,
  looked at before reporting done. The Preview chapter says the same.
- deivid asked to unpin **Browse by folder**: the Reference section now follows
  the navigation in the normal flow instead of docking to the menu bottom.
- Checks: `tests/run_checks.sh` (153 tests) and strict lint pass; own-site,
  visual, browser-helper and panel-switcher suites pass; sidebar captures at
  1400 px reviewed.

## 2026-11-09 — Require topic records, remind about explaining pages, add the conformance check

- deivid decided that every topic has a record; a page-only topic is a
  declared exception, `page_only = "<reason>"` in its frontmatter. Lint warns
  about a topic page with neither, so strict lint fails. The kit's five
  explanation pages declare it: their records are the guides in `rules/`.
  ADP has page-only topics and will see the warning when it upgrades.
- Pages explain records in their own words, so drift is caught by a reminder
  instead of quoting: when a record section changes, lint prints notes naming
  the pages and chapters that link to it (`--since <rev>` for older
  comparisons). Links to a whole record count only for its opening text.
- `rules/conformance.md` is the checklist a project runs when its pin moves or
  the repository changes hands; both migration guides, the README, the
  authoring guide and the starter router link it. Documentation and writing
  gains Topics (with a folder figure) and In step chapters.

## 2026-11-09 — Fit the chapter peek targets to the visible slivers

- In One chapter view the previous/next click targets were a fixed 10% of the
  stage (93px at 1400 wide) while only about 49px of the neighbouring card
  shows, so their hover outline overlapped the current card. The reader now
  sizes each target to the neighbour's visible sliver when it aligns the cards.
- Checks: 135 tests, strict lint, all four browser suites; target and sliver
  measured at x 1339–1388 on Get started at 1400 wide.

## 2026-11-09 — Publish the kit website on GitHub Pages

- deivid decided to publish the site publicly. Pages was already enabled
  with GitHub Actions as its source, but the repository had no workflow, so
  https://davszi.github.io/documentation-kit/ returned 404.
  `.github/workflows/pages.yml` now builds the site from `main`, runs strict
  lint and deploys `.build/docs`. The website record's hosting section and
  the open-work route are updated.

## 2026-11-09 — Redesign the home page

- The hero repeated the page links as three numbered text cards, the step
  flow's command ran into its arrow, the AGENTS.md example sat in a wide
  separate code block, and the page map mixed one stale screenshot with empty
  boxes. The hero now pairs the claim with an AGENTS.md router card; the steps
  are three numbered cards; the page map shows uniform cards per group in the
  sidebar's group tones, which `nav.js` now also applies to map groups.
- Checks: 135 tests, strict lint, all four browser suites (the keyboard check
  now targets page cards, which gained focus outlines); captures at 1400, 1024
  and 390 reviewed by eye.

## 2026-11-09 — Redesign the sidebar navigation

- Each navigation group is now a section styled like the Reference block:
  a tinted top gradient and sans label in the group's tone, light page rows,
  and the current page marked by a tone bar. Groups without a CSS colour get
  tones in order from `nav.js`. Page rows outrank the current page's chapter
  list, which is a smaller muted sub-list with small outlined numbers.
- The ∿ mark was ADP's and had spread to every project. `brand_mark` in
  `site.toml` sets a project's own mark (up to three characters or a tracked
  SVG); without it the mark is the title's initials. The kit uses a layered
  SVG. The reader drawer shows the same mark and name as other pages and no
  longer shows a chapter counter.
- Hiding the menu was remembered per page, so a page could open with it
  hidden while the previous page had it docked. The choice now holds across
  the site.
- The Compatibility chapter gains its short menu label.
- Checks: 135 tests, strict lint, all four browser suites; sidebar captures at
  1400 and 390 reviewed by eye; dock choice verified across three pages.

## 2026-11-09 — List releases in the menu; rename the records section

- Release notes and migration guides matter to every reader, so they form a
  Releases group in the main menu instead of being pinned inside the records
  section; README stays pinned. A record listed in the menu keeps the folder
  tree closed, because its menu entry already marks it.
- The section holds documents, not loose files: it is now **Reference**, and
  its disclosure **Browse by folder**.
- Checks: 132 tests, strict lint, all four browser suites; checked in the pane
  on Build a site and the release notes.

## 2026-11-09 — Version asset URLs and dock the repository section

- After rebuilds, browsers paired cached old stylesheets with new pages, so
  the repository section and fixed figures appeared unstyled or stale. Pages
  now load shared assets as `assets/<file>?v=<first 10 hex of its SHA-256>`;
  lint and the resource checks ignore the query.
- On reader pages the chapter list pushed the repository section below the
  window. While **All files** is closed the section is docked to the bottom
  of the menu; opened, it returns to the normal flow and the menu scrolls to
  the current file.
- Checks: 130 tests, strict lint for starter and kit site, own-site, visual,
  browser-helper and panel-switcher suites; reviewed in the app pane on Build a
  site and in the narrow menu on `git.html`.

## 2026-11-09 — Fix figure styling found in a visual review

- Earlier checks proved containment and overflow, not appearance. A review
  in the 1024px app pane found: repository paths uppercased inside box
  titles, default disc bullets and mismatched code chips in boxes, arrow
  labels detached from stacked arrows, three-column grids and 46px headlines
  crushed inside Two chapters cards (grids followed the window, not the
  card), and the active carousel dot filling its 44px touch target as a
  large disc.
- Boxes now use short tone-coloured dashes and tinted code chips; code keeps
  its case in titles and labels; a stacked box puts its title beside its
  list; arrow labels sit next to the arrow; grids, checks and headlines
  follow the chapter card's width; the carousel dot keeps its small mark.
- Checks: 128 tests, strict lint for starter and kit site, own-site, visual,
  browser-helper and panel-switcher suites; reviewed in the pane at 1024px in
  One and Two chapters views.

## 2026-11-09 — Pin key records; keep the file tree out of the way

- The first tree repeated every page for people as a one-file folder,
  unfolded file paths on the home page and stayed open everywhere. The tree
  now lists registered records only, inside an **All files** disclosure that
  is closed on pages for people and opens to the current file on other
  record pages. `pinned = true` on `[[source_pages]]` lists README, release
  notes and the 2.0.0 migration guide above it.
- Build-sheet flows stack vertically when their card or page is too narrow
  for three boxes without breaking code paths (about 940px of flow).
- Checks: 128 tests, strict lint for starter and kit site, own-site, visual,
  browser-helper and panel-switcher browser suites.

## 2026-11-09 — List repository files in the sidebar; lead with writing pages

- The site's 30 registered records were mostly hidden nav entries reachable
  only by in-page links. The sidebar now lists pages for people first, then a
  Repository files folder tree generated from `[[source_pages]]`, with topic
  page sources marked as pages and linked to their existing page. Records need
  no nav entry; the kit site's 30 record entries are removed.
- Build a site no longer opens with two chapters on publishing existing
  Markdown, a feature only the kit's own site uses (ADP and adapt register
  none). A new chapter shows how to write a topic page; existing Markdown is
  one shorter chapter after figures and slides.
- Checks: 127 tests, strict lint for starter and kit site, own-site, visual,
  browser-helper and panel-switcher browser suites.

## 2026-11-09 — Release 2.0.0

- The changes after 1.1.0 become 2.0.0. It is a major release because the
  exporter's renaming and relocation and the old local-artifact manifest
  location are removed, and lint now fails an unpushed kit pin. `VERSION` is
  `2.0.0`, the migration guide is `migrations/2.0.0.md` and consumers pin
  tag `v2.0.0`.

## 2026-11-09 — Port configured publication and guard the kit pin

- adapt pinned kit commit `101cea4`, made inside its `.docs-kit` folder and
  never pushed; its Pages run fails with `not our ref`. The commit's
  `docsite.py publish` command is ported without page renaming, file
  relocation and retirement pages; `[publication]` rejects those keys.
- The rule against editing a detached submodule sat in the site-authoring
  guide, which no consumer router sends agents to. The Git guide now owns it
  as "The shared kit submodule", the starter router routes kit changes there,
  and `docsite.py lint` fails when the pinned kit commit is on no remote
  branch (skipped for shallow checkouts, copies without Git and the kit's own
  repository). Against the real checkouts it flags adapt's `101cea4` and
  passes ADP's pin. The migration guide lists adapt's steps.

## 2026-11-09 — Remove the exporter's renaming and the old manifest location

- The owner decided no compatibility is needed for either. `export_pages`
  drops `page_routes`; every generated file keeps its name, and
  `public_files` lists tracked paths published at the same path. Tests that
  only covered renaming are removed; a test proves names are kept. The
  `docs/project/local-artifacts.json` fallback is removed, with a test that
  the old location is ignored. The path adapter stays: the resources guide
  records that it exists for frozen records and goes once none names an old
  path. A migration guide for the next release covers both removals.
  Kit checks: 107 tests and strict lint pass.

## 2026-11-09 — Prefer refactoring to backward compatibility

- The code guide gains "Refactoring over compatibility": before changing a
  name, path, format, API, URL or configuration key that something outside
  the change may use, the agent asks the owner with the evidence (what
  changes, who uses it, what breaks, what keeping it costs). Without a need
  for compatibility, every reference is updated and the old form removed;
  kept compatibility records its reason and removal condition. The
  documentation guide's allowance for compatibility routes now defers to it.
  Engineering practices gains a Compatibility chapter.

## 2026-11-08 — Fold the toolkit and reader tour into Build a site

- Site toolkit only listed what exists, and the Reader tour demonstrated
  features without content behind them. Both pages and Commands are
  replaced by one reader page, Build a site: how a build works, the two
  kinds of pages, publishing existing Markdown (problem, mechanism, what
  the build adds, a live source-versus-rendered switcher, the full registry
  entry), what readers get (docking, pinning and layers, with real folds),
  figures and slides (carousel of site captures, slide-face deck command),
  then build, lint, preview, upgrade and the reference guides per task.
  Get started and Build a site each open with a slide face. Start here now
  holds both pages; the Site toolkit group is gone. The site review's
  docking, pinning, carousel and switcher checks run on Build a site.

## 2026-11-08 — Keep the site tree on listed reference pages

- Opening a listed reference page (README, release notes, kit records)
  replaced the sidebar's site tree with that page's section list. A listed
  registered page now keeps the site tree with itself marked as current;
  hidden registered pages, which have no entry to mark, and pages under
  `nested_nav`, which nest sections under their entry, still list them.
  A unit test covers the listed and hidden cases.

## 2026-11-08 — Show the starter's files on Get started

- Get started gains a "Starter files" chapter: the annotated tree of what
  `init` writes, one line per file stating its job, the files grouped by
  role (agent entry and orientation, records, the site), an example of a
  fact written into the wrong file, and a fold on `.docs-kit/`, `.build/`
  and the `*.tmpl` storage inside the kit.

## 2026-11-08 — Give Get started full-depth cards

- The merged Get started kept one claim and one visual per card and dropped
  the explanation; its adoption chapter hid two of three routes behind a
  switcher and left most of the card empty. Each chapter now has a reason,
  a not-this/this example and folds where detail helps; the practice-area
  cards show each page's chapter claims; setup shows the full commands
  beside what `init` writes and why it is safe to run; the three adoption
  routes sit side by side with steps and what stays as is. The site review's
  panel-switcher hash check moves to the Reader tour's switcher.

## 2026-11-08 — Merge the start pages

- Start here had four overlapping pages (Get started, Reader tour, Setup and
  commands, Practices overview). Get started now holds what the kit
  provides, how routing works, the three practice areas, setup and the
  adoption routes in five chapters; the Practices overview page is removed.
  Commands keeps build, lint, preview, slides and upgrade. The Reader tour
  moves to the Site toolkit group. Start here now has two pages, Practices
  three.

## 2026-11-08 — Give setup and commands their own page

- "Setup and commands" opened the README as a plain reference page in the
  middle of the reader pages: its sidebar changed shape, its title and hero
  screenshot did not match the menu label, and it ended in kit-development
  sections. A new reader page, `commands`, explains setup, build,
  `build --check`, lint, loopback preview, slides and upgrades, each with the
  exact command and what it checks or writes. The README moves to Kit
  development; home, Get started and Site toolkit link to the new page.

## 2026-11-08 — Explain the practice pages instead of listing rules

- deivid found the three practice pages too fast: each card gave one claim,
  one visual and one paragraph, so it said what a rule is but not why. The
  rules themselves were not shortened (11,591 words; 9,943 at v1.1.0).
- Each chapter now adds why the rule exists, a labelled illustrative
  not-this/this example and typed folds (Experiments, Code, Alternatives)
  for details the earlier pages omitted. Engineering grows to 11 chapters,
  Documentation and writing to 13, Experiments to 9. Examples on the
  experiments page come from several fields; final runs stay scoped to
  learned or fitted models.
- The "why" paragraph follows each chapter's visual, so the figure comes
  right after the heading and lead as `rules/writing/pages.md` requires.
  Rendered review at 1600 × 1000 and 390 × 844: no page errors or
  horizontal overflow; cards with folds closed run about 0.9–1.5 screens.

## 2026-11-08 — Keep kit, starter and project entry files apart

- In a consuming project the kit's own `AGENTS.md`, `CLAUDE.md` and
  `docs/PROJECT_CONTEXT.md`, the starter's copies and the project's own files
  shared names, and Claude Code can load a nested `CLAUDE.md` when reading
  files under `.docs-kit/`. The kit's entry files are now
  `docs/KIT_CONTEXT.md`, `docs/KIT_INDEX.md`, `docs/KIT_WORKLOG.md` and
  `docs/open/KIT_OPEN.md`; its `AGENTS.md` and `CLAUDE.md` say they apply
  only to the kit repository. Lint gains an `open_work` setting, and every
  worklog check honours `worklog`.
- The starter's entry files are `*.tmpl` templates; `init` writes them under
  their real names and fills `--title` and `--repository` into `site.toml`.
  `tests/run_checks.sh` generates the starter under `.build/starter/` and
  builds, lints and unit-tests that output; the starter guide's config excerpt
  now shows lines that do not vary per project.

## 2026-11-08 — Remove the extraction history

- Removed `provenance.json`, `verification/`, `preview/`,
  `docs/topics/extraction/` and `rules/extraction-map.md` on deivid's request.
  No code, test or consumer route used them; they remain at the `v1.1.0` tag.
  Links to them in the README, indexes, panel-switcher record, release notes
  and earlier worklog entries now point to that tag; worklog text is
  unchanged. The README and Reader tour use two new captures of this site
  (`docs/topics/reader-tour/media/`, 2026-11-08, commit 83e5a59).

## 2026-11-07 — Separate pages for people from rendered records

- The kit site showed its rule guides in the chapter reader, one card per
  section of agent-facing text. It now follows the split ADP and the starter
  use: records stay Markdown, pages for people explain them. New reader pages
  explain the guides: Engineering (7 chapters), Documentation and writing (8)
  and Experiments (8); Project practices became a short overview of the three
  areas. Every registered record renders as a plain reference page with its
  source line (`reader` default `false`); rule guides are hidden from the
  navigation and reached from the pages.
- The three pages were drafted from the full rule texts, each section anchor
  checked against the build's slug rule, then reviewed rendered; claims were
  spot-checked against the rules.
- The site review now requires reader chapters on pages for people and plain
  reference pages, with a visible source line, for every record. It checks
  both narrow menus: the reader bar and the reference-page shell.

## 2026-11-07 — Add a reader tour

- The kit site had no page demonstrating the reader. `reader-tour` uses each
  feature once with steps to try: a slide face, chapter movement, docked
  navigation, a pinned column in Two chapters, the four reading layers,
  a carousel with the lightbox, the panel switcher, status and stat blocks and
  deck extraction. It is linked from the home page and the Start here group.
- Two kit defects found while testing it: the carousel showed every slide when
  placed in a `.bs-grid` figure, because `.bs-grid figure img` outranked its
  hide rule; and the reader help told readers to "Pin Explore", a button that
  is created but never shown. The carousel rule now uses a doubled class, and
  the help describes the actual `«` and `☰` docking behavior. The unused pin
  button code remains.
- The site review now walks the tour at 1600 px: docking, undocking, pinning
  while the other column moves, and one visible carousel slide.

## 2026-11-07 — Write the overview pages as reader chapters

- Get started, Project practices and Site toolkit were scrolling pages
  dropped into the chapter reader. Each chapter is now an explicit
  `section.card` with a claim heading, a `bs-lead` sentence and one visual
  block (flow, contrasting parts, checks or a scrollable table), with short
  toolbar labels in `toc`. New chapters: site build and upgrades (Get started)
  and the checks that fail a build (Site toolkit). The registered guides keep
  their plain Markdown; only these site-only pages changed.

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
  adaptation 7 of 8; [receipt](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/v1.0.0-consumers.json)).
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

- Clarify the [page lead](../rules/writing/pages.md#page-design),
  [scope notes](../rules/writing/explanations.md#story-and-reading-layers) and
  [choice of representation](../rules/writing/figures.md#figures-and-comparisons).
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
  The [writing rules](../rules/writing/pages.md#slide-faces) own content guidance; the
  [maintenance contract](../rules/site/authoring.md#slide-faces-and-decks) owns
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
  [maintenance contracts](../rules/site/publication.md#exporting-into-an-existing-publication)
  own both APIs. Homepage composition stays project-owned; the starter is an
  optional example, as recorded in the [writing rules](../rules/writing/pages.md#project-owned-homepages).
- Preserve embedded JavaScript/JSON and unrelated HTML bytes. Align source-span
  offsets with HTMLParser's LF counting and cover literal Unicode/control
  separators plus mixed mapped/unmapped routes. Browser checks retain real
  clipping/visibility rules and report impossible short-reader cases as skipped.
- Strict starter lint has zero warnings; all 52 Python checks, JavaScript checks,
  real browser failure fixtures and desktop/phone reader checks pass. Independent
  source review findings are resolved. [Receipts](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/publication-browser.json)
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
  checks and desktop/phone reader browser checks pass. [Receipts](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/content-imports.json)
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
  owned 4 GiB/zero-swap scope. [Receipts](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/shared-includes.json)
  retain tested inputs and output. This landing supplies the commit identity.

## 2026-11-04 — Consumer compatibility adapters

- Add explicit tracked/contained project path and evidence adapters, keeping
  consumer historical identities and schema policy out of the shared engine.
  Declare project-only dynamic dependencies through `extra_assets`; reject
  shared-asset collisions and noncanonical/escaping target paths. The
  [maintenance contract](../rules/maintenance.md) owns configuration and API.
- Strict starter build/lint, all 26 Python checks, math/source-link JavaScript
  checks and existing desktop/phone reader browser checks pass. [Receipts](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/project-extensions.json)
  retain inputs, output and the owned 4 GiB/zero-swap scope under the shared
  lock. No application runtime was launched. This landing supplies the commit
  identity; consumer adoption and its content validation remain project-owned.

## 2026-11-04 — Shared local comparison controls

- Extract the reusable width-lesson interaction as `panel-switcher`, with neutral
  authoring attributes and shared control CSS. Track scenarios, figures, legends
  and specialized layouts stay project-owned; ADP's original compatibility copy
  remains until its kit adoption. The [component contract](topics/panel-switcher/panel-switcher.md)
  owns usage and behavior; [origin identities](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/panel-switcher-origin.json)
  preserve the exact producing source. After attribute renaming, executable
  behavior matches the original source.
- Verify original/shared defaults, independent groups, buttons/keyboard, deep
  links, print restoration and fallback reading at desktop/phone widths. Strict
  build/lint reports zero warnings, all 22 Python tests pass, both JavaScript
  checks and the existing reader browser regression pass. [Receipts](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/panel-switcher-checks.json)
  retain the complete run and screenshots. Checks held the shared lock in an
  owned 4 GiB/zero-swap scope; no simulator was launched. The first invocation
  timed out, its owned scope was stopped, and the corrected browser harness
  passed in a complete rerun. This entry's landing commit supplies its identity.

## 2026-11-04

- Extract the reusable documentation kit from inspected source `9930b919`:
  portable policies, shared chapter/home layouts, generic toolchain and a neutral
  starter. The user selected a pinned dependency suitable for a Git submodule.
  [Extraction evidence](https://github.com/davszi/documentation-kit/blob/v1.1.0/docs/topics/extraction/extraction.md) records source hashes,
  independent review and the passing build/lint, 21 Python tests, JavaScript
  checks and desktop/phone browser review. No simulator or source-project
  migration was performed. This initial commit owns the coherent deliverable.
