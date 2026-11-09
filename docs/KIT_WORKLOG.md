# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

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
