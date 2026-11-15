# Site validation and browser checks

## Validation and review

Run checks from the consuming project root using the pinned kit. A complete validation must cover:

- Full build, freshness check and link/anchor/snippet/figure lint.
- Shared engine regression suite and applicable project content/interaction checks.
- Exact evidence identities and manifest closure where registered.
- Browser rendering at wide and narrow widths, plus equal-column layout when the reader is used.
- Keyboard navigation/focus, labels/touch targets, reduced motion, no-JavaScript fallback and print.

A page-only build is useful for iteration; it does not validate unrelated output. A freshness check must not mutate output. A strict lint run may treat warnings as errors; document any intentionally retained warning rather than hiding it. A registry listing shows current source declarations; raw searches may also include historical evidence and must not be mistaken for the current registry.

When the project uses the chapter reader, `build --check-reader` renders every topic page with and without the reader and fails when the reader changes its words, links, media, tables, folds, anchors or SVG figures. It writes nothing. Use this command for that check; a project test that imports the kit's build module breaks whenever the kit changes inside.

Tests that compare DOM/structure, content or numerical identities are useful evidence. They do not establish browser pixel inspection. Report results under the [handoff rules](../engineering/handoffs.md#reporting-completion). Never call a layout checked from source inspection alone.

Check slide faces in their page as well as in an extracted deck. Page styles add space, for example around images, that the deck does not have, so a face that fits in the deck can fail in its page. Check each face in its reader chapter at the widths the site supports, a phone width below 720 px included, with the [browser check below](#reusable-browser-checks).

Review every visual change by eye before reporting it done. Capture each element the change touched, whole, at every width the site supports and in each reader view it appears in, such as one or two chapters; `captureElement` with `unclip` captures a reader chapter whole. Look at each capture for alignment, spacing, list markers, typography, colour and overflow, and compare it with the page around it. Passing browser suites do not replace this look. Report which captures were reviewed and what they showed. When slide faces are reviewed by eye, the reviewer says for each face what draws the eye first and whether a band of the canvas is empty, so that another person can disagree with something concrete. "No band left over" and the designer's standard stay judgment, with no number: the empty band that the browser check reports is information for the reviewer, never a limit. The captures are [scratch files](../engineering/handoffs.md#scratch-files), except one that a page uses as a figure: a record states what the review found and cites no capture by path or hash, and the captures are kept until whoever must look at them has done so.

For local review, follow [local review and browser access](#local-review-and-browser-access), using `.build/docs/` and `/html/<slug>.html`. Follow the [publishing gate](publication.md#publishing-gate) before deployment.

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
  nothing and has no threshold. A face the page does not show, such as one in
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
- `settle`, `visibleMedia`, `measureOverflow`, `assertHorizontalContainment` and
  `checkLayout` for fonts, actually visible images and viewport containment.
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
