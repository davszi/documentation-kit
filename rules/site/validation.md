# Site validation and browser checks

## Validation and review

Run checks from the consuming project root using the pinned kit. A complete validation must cover:

- Full build, freshness check and link/anchor/snippet/figure lint, HTML links to repository files and the [formula check](authoring.md#formula-check) included.
- Shared engine regression suite and applicable project content/interaction checks.
- Exact evidence identities and manifest closure where registered.
- Browser rendering at wide and narrow widths, plus equal-column layout when the reader is used.
- Keyboard navigation/focus, labels/touch targets, reduced motion, no-JavaScript fallback and print.

A page-only build is useful for iteration; it does not validate unrelated output. A freshness check must not mutate output. A strict lint run may treat warnings as errors; document any intentionally retained warning rather than hiding it. A registry listing shows current source declarations; raw searches may also include historical evidence and must not be mistaken for the current registry.

When the project uses the chapter reader, `build --check-reader` renders every topic page with and without the reader and fails when the reader changes its words, links, media, tables, folds, anchors or SVG figures. It writes nothing. Use this command for that check; a project test that imports the kit's build module breaks whenever the kit changes inside.

Tests that compare DOM/structure, content or numerical identities are useful evidence. They do not establish browser pixel inspection. Report results under the [handoff rules](../engineering/handoffs.md#reporting-completion). Never call a layout checked from source inspection alone.

Check slide faces in their page as well as in an extracted deck. Page styles add space, for example around images, that the deck does not have, so a face that fits in the deck can fail in its page. Check each face in its reader chapter at the widths the site supports, a phone width below 720 px included, with the [browser check below](#reusable-browser-checks).

Review every visual change by eye before reporting it done. Capture each element the change touched, whole, at every width the site supports and in each reader view it appears in, such as one or two chapters; `captureElement` with `unclip` captures a reader chapter whole. Look at each capture for alignment, spacing, list markers, typography, colour and overflow, and compare it with the page around it. Passing browser suites do not replace this look. When page work builds or redesigns several chapters, finish, capture and review one chapter before starting the next. Look also for what no check sees, such as a sign that reads as a minus or a rounded value that crosses a threshold. Finish with one pass over the whole page for what shows only across chapters: terms, colours and links. Report which captures were reviewed and what they showed. When slide faces are reviewed by eye, the reviewer says for each face what draws the eye first and whether a band of the canvas is empty, so that another person can disagree with something concrete. "No band left over" and the designer's standard stay judgment, with no number: the empty band that the browser check reports is information for the reviewer, never a limit. The captures are [scratch files](../engineering/handoffs.md#scratch-files), except one that a page uses as a figure: a record states what the review found and cites no capture by path or hash, and the captures are kept until whoever must look at them has done so.

For local review, follow [local review and browser access](#local-review-and-browser-access), using `.build/docs/` and `/html/<slug>.html`. Follow the [publishing gate](publication.md#publishing-gate) before deployment.

## Reviewing a page against its rules

Rules change and the pages that explain them stay behind unless someone looks. Lint helps to find them: it notes a changed record section with the pages that link it, a changed section that no page links although a page explains the record, which means it links two or more of its other sections, and a numbered figure the text never cites. `lint --since <tag>` lists them for everything since a release.

A review is a task of its own, asked for by the person; it is not part of an upgrade. Give one page to one agent. For each chapter the agent writes down which rule sections the chapter explains, what those sections say now that the chapter does not, what the chapter says that they no longer say, whether the chapter has a real visual and whether each numbered figure is cited. It reports that list first and fixes after. A change of structure, such as splitting or merging pages, goes to the person. The page is then checked as any page work is: at a wide and a narrow width, with the captures the agent looked at.

## One command and a pre-push gate

`python .docs-kit/docsite.py check --project .` runs the checks a push should
not break, in this order, and stops at the first that fails:

1. `build`, because lint compares the built site with its sources.
2. `lint --strict`.
3. A trial `publish` into a temporary folder, when `docs/site/site.toml` has a
   `[publication]` table. With the [page lock](publication.md#page-lock) on
   and its passwords not in the environment, it runs with two throwaway
   passwords; it is skipped with a note only when the lock's package
   `cryptography` is not installed.
4. Each check the project declares in `docs/site/site.toml`, in the order
   written:

   ```toml
   [[checks]]
   name = "public paths"
   command = ["{python}", "-m", "unittest", "docs/site/checks/test_public_paths.py"]
   ```

   `command` is an argument list, run from the project root without a shell.
   An element that is exactly `{python}` becomes the interpreter that runs
   the check; any other program is named as the project calls it. `name` is
   optional. After a trial `publish`, each check finds that bundle, as it is
   before the page lock, in the folder the environment variable
   `DOCSITE_PLAIN_BUNDLE` names; the folder is removed when the checks end.
   Without a trial publish the variable is unset, whatever the caller's
   environment holds. The page lock's passwords reach the trial publish
   only, not `build`, `lint` or a declared check.
   [Checks that read published pages](publication.md#checks-that-read-published-pages)
   has the use.

It runs no browser check and replaces no review by eye. It reads the
checked-out tree, not a commit.

The gate is opt-in, per clone. `hooks/pre-push` in the kit calls the command
before a push and stops the push when it fails. Switch it on once, in the
main checkout:

```bash
git config core.hooksPath "$(git rev-parse --show-toplevel)/.docs-kit/hooks"
```

The path is absolute, so linked worktrees use the same hook; set it again
when the clone moves. `core.hooksPath` replaces the clone's hooks folder: a
project with hooks of its own copies `.docs-kit/hooks/pre-push` into its
tracked hooks folder and points the setting there. The hook:

- refuses the push while tracked files have uncommitted changes, because the
  checks would then not read what is pushed; `DOCS_GATE_ALLOW_CHANGES=1`
  checks the tree as it is;
- refuses it in a checkout without `.docs-kit`, such as a new worktree before
  `git submodule update --init .docs-kit`;
- uses `$DOCS_PYTHON`, else `.build/docs-env/bin/python` of the checkout or of
  the main checkout;
- runs nothing for a push that only deletes, and says so when a pushed commit
  is not the checked-out one.

`git push --no-verify` skips it once. The project's workflow stays the check
that counts; the gate finds the failure before the push.

## A page's source for checks

A project's check that looks at what a page says, without building it, reads
the page through `tooling/page_source.py`:

```python
import sys; sys.path.insert(0, ".docs-kit/tooling")
from page_source import page_source, PageSourceError

meta, body = page_source("docs/topics/guide/guide.md", project=".")
```

- `meta` is the `+++` frontmatter as a dict. `body` is the text after it, up
  to a `<!-- page-end -->` marker, with every `<!-- include: path -->` marker
  replaced by its fragment, fragments in fragments included. The build cuts
  at the marker and expands includes with the same functions.
- Nothing else of the build is applied: a project's `content_transform` does
  not run, slide and fold markers, tabs and the site-map marker stay as
  written, and no Markdown is rendered. Frontmatter keys are not validated;
  `build` and `lint` do that.
- A page with a problem raises `PageSourceError`, a `ValueError`; its
  `problems` names every one: a frontmatter fence or TOML that cannot be
  read, an include that is missing, untracked, empty, unreadable, outside
  the theme and the project, part of a cycle or nested too deep. An include
  must be a tracked file, as in the build, so a new fragment is added with
  `git add` before the check reads it.
- `page_source(path, project)`, `PageSourceError` and its `problems` are
  stable interfaces. The module's other names serve the build and may
  change; so may every name in `tooling/build.py`, which a check does not
  import.

## Local review and browser access

Use the pinned kit from the consuming project root and the concrete commands in the project's context. Complete the [validation above](#validation-and-review) before review. Share the rendered page with its figures first, then source or evidence links where useful.

Serve only generated output on loopback for local browser review. Confirm the listener's owner and served checkout before reuse. Do not expose the repository root or stop another session's server. Stop owned temporary servers after review unless retained for the user's preview.

Browser approval remains scoped to the supported origin. If access is rejected on policy grounds, preserve the rejection and resolve the permission with the owner. Do not change transport, browser or control API to bypass the block. A manual file URL is not evidence that an agent inspected the rendering.

## Reusable browser checks

`tooling/browser_checks.cjs` accepts an existing Playwright page. It never starts
a browser, server or experiment. Projects own those lifetimes, page routes,
expected counts, screenshots and domain assertions. The shared module provides:

- `slideFaces(page, {within?})` measures every slide face the page shows, or
  those inside the `within` selector, in a page or in an extracted deck. Per
  face it gives the chapter, the size, whether the face is stacked (`compact`,
  below 720 px), whether a 16:9 face holds its content (`fits`), the pixels it
  overflows sideways (`sideways`), the text that a box cuts off (`clipped`), the
  parts that stick out of the face (`outside`) and `problems`, these faults in
  words. `emptyBand` is the height in pixels of the largest horizontal band of
  the canvas that holds nothing; it is information for the reviewer, fails
  nothing and has no threshold. `drawingText` is the smallest size at which a
  label of the face's inline SVG drawings renders, the font size times the
  drawing's scale on screen, with that label's text and the number of labels
  below 11 px; a label below the 11 px that
  [figures](../writing/figures.md#figures-and-comparisons) asks of chart
  labels is a problem. A drawing that shrinks into a phone column shrinks its
  labels with it; an SVG loaded as an image is not read. A face the page does not show, such as one in
  an inactive reader chapter, has `shown: false` and no measurements.
  `assertSlideFaces(page, {within?, expectShown = 1})` fails with every problem
  of every shown face, and when fewer faces than `expectShown` are shown.
  A project checks each face in its chapter at each reader width, for example:

  ```js
  // Run from the project root; the kit is the project's .docs-kit submodule.
  const {goHash, assertSlideFaces} = require(require('node:path').resolve('.docs-kit/tooling/browser_checks.cjs'));
  for (const id of chapterIdsWithFaces) {   // at 390 px and at the wide widths
    await goHash(page, url, id);
    await assertSlideFaces(page, {within: '#' + id});
  }
  ```
- `smallText(page, {min = 11, ignore?})` lists the text of the page that
  renders below the 11 px that [page design](../writing/pages.md#page-design)
  asks of all text: where it sits, its size, how often and a sample.
  `assertTextSize(page, {min?, ignore?})` fails with that list. HTML text
  counts at its computed font size whether it is shown or not, so a closed
  fold, an inactive chapter and a closed drawer are read without opening
  them. SVG text counts at its size on screen while the drawing is rendered,
  and `::before` and `::after` count when they hold a letter or a digit. A
  size counts at one decimal, so 10.96 px passes as 11.0. The check leaves
  out formulas, slide faces and what the `ignore` selector matches or
  contains. A drawing in an inactive reader chapter or a closed fold is not
  rendered: show all chapters and open the folds before the check. It does not read text in an SVG loaded as an image,
  and it does not see a `transform` that scales HTML text.
- `settle`, `visibleMedia`, `measureOverflow`, `assertHorizontalContainment` and
  `checkLayout` for fonts, running transitions, actually visible images and
  viewport containment.
  Image visibility includes ancestor clipping; hidden/inert and offscreen lazy
  images do not become broken-image failures merely because they are mounted.
- `setView`, `activeChapter`, `waitActive` and `goHash` for shared reader control.
- `captureElement(page, selector, file, {unclip?, hide?})` captures one figure,
  face or chapter; `unclip` removes height limits and clipping on the element and
  its ancestors so a reader chapter is captured whole.
- `readerChecks(page, {url, expectedChapters, check?, onPair?})` for real
  navigation/history and comparison pinning. It returns
  `{chapterIds, checked, skipped}`; short readers report impossible interactions
  as skipped rather than passed. Caller callbacks may retain project reports
  and capture the paired state.

Kit fixtures verify both failures and valid contained layouts, including readers
with one to three chapters. The kit's visual review and consuming-project
harnesses use the same functions. Domain numbers, recordings, task controls and
qualification verdicts remain project assertions. Run browser jobs under the [execution rules](../engineering/execution.md)
and the consumer's concrete controls; importing these helpers grants no
permission to start another heavy job.
