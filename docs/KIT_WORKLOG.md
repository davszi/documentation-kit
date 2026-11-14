# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

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
