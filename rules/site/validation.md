# Site validation and browser checks

## Validation and review

Run checks from the consuming project root using the pinned kit. A complete validation must cover:

- Full build, freshness check and link/anchor/snippet/figure lint.
- Shared engine regression suite and applicable project content/interaction checks.
- Exact evidence identities and manifest closure where registered.
- Browser rendering at wide and narrow widths, plus equal-column layout when the reader is used.
- Keyboard navigation/focus, labels/touch targets, reduced motion, no-JavaScript fallback and print.

A page-only build is useful for iteration; it does not validate unrelated output. A freshness check must not mutate output. A strict lint run may treat warnings as errors; document any intentionally retained warning rather than hiding it. A registry listing shows current source declarations; raw searches may also include historical evidence and must not be mistaken for the current registry.

Tests that compare DOM/structure, content or numerical identities are useful evidence. They do not establish browser pixel inspection. Report results under the [handoff rules](../engineering/handoffs.md#reporting-completion). Never call a layout checked from source inspection alone.

For local review, follow the [owned-server and browser rules](../documentation.md#review-build-and-publishing), using `.build/docs/` and `/html/<slug>.html`. Follow the [publication gate](../documentation.md#review-build-and-publishing) before deployment.

## Reusable browser checks

`tooling/browser_checks.cjs` accepts an existing Playwright page. It never starts
a browser, server or experiment. Projects own those lifetimes, page routes,
expected counts, screenshots and domain assertions. The shared module provides:

- `settle`, `visibleMedia`, `measureOverflow`, `assertHorizontalContainment` and
  `checkLayout` for fonts, actually visible images and viewport containment.
  Image visibility includes ancestor clipping; hidden/inert and offscreen lazy
  images do not become broken-image failures merely because they are mounted.
- `setView`, `activeChapter`, `waitActive` and `goHash` for shared reader control.
- `readerChecks(page, {url, expectedChapters, check?, onPair?})` for real
  navigation/history and comparison pinning. It returns
  `{chapterIds, checked, skipped}`; short readers report impossible interactions
  as skipped rather than passed. Caller callbacks may retain project reports
  and capture the paired state.

Kit fixtures verify both failures and valid contained layouts, including readers
with one to three chapters. The kit's visual review and consuming-project
harnesses use the same functions. Domain numbers, recordings, task controls and
scientific qualification remain project assertions. Run browser jobs under the [execution rules](../engineering/execution.md)
and the consumer's concrete controls; importing these helpers grants no
permission to start another heavy job.
