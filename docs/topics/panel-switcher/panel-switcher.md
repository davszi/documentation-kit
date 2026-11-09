# Local comparison panels

The shared `panel-switcher` selects one option inside an independent local
comparison. Its content may be text, figures or a grouped treatment. It does not
change the page's chapters, reading layers or navigation.

## Authoring contract

Add `"panel-switcher"` to a page's frontmatter `components`. The builder supplies
both its script and control stylesheet; no project extension is required.

```html
<div class="panel-switcher" data-panel-switcher data-panel-default="overview">
  <div class="panel-switcher-controls" role="group" aria-label="Comparison view">
    <button type="button" data-panel-choice="overview" aria-pressed="false" aria-controls="example-overview">Overview</button>
    <button type="button" data-panel-choice="detail" aria-pressed="false" aria-controls="example-detail">Detail</button>
  </div>
  <div id="example-overview" data-panel="overview">Overview content.</div>
  <div id="example-detail" data-panel="detail">Detail content.</div>
</div>
```

Use one distinct choice value per button/panel pair and globally unique HTML
IDs. Keep groups independent rather than nesting them. Supply a valid default;
without one, the first panel is selected. Do not author panels as hidden: all
options remain readable without JavaScript, and controls appear only after
initialization. Native buttons retain keyboard activation and pressed states.

A hash targeting a panel or its descendant reveals that option, both on load
and after a hash change. An invalidly encoded hash is ignored. Printing exposes
every panel and hides controls, then restores the previous selection. Groups
with missing or unequal button/panel counts remain uninitialized and readable.

## Ownership and source compatibility

The kit owns switching, deep-link reveal, print restoration and generic control
styling. Projects own option labels, explanatory content, figures, data,
generators and specialized layouts/legends.

This implementation is extracted from ADP's `width-lessons.js` with neutral
attribute names. The [origin receipt](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/panel-switcher-origin.json)
records source and extracted identities. Each consuming project's
documentation owns its adoption and compatibility status.

## Verification

`tests/test_portability.py` checks a standalone Git consumer can select and
package the shared script/stylesheet without a local extension. The optional
real-browser check `node tests/test_panel_switcher.cjs` covers independent
groups, defaults, buttons and keyboard, hash reveal, printing, invalid input,
wide/narrow containment and no-JavaScript reading. Use the Playwright/Chromium
environment variables documented in the README.

The [verification record](https://github.com/davszi/documentation-kit/blob/v1.1.0/verification/panel-switcher-checks.json)
records the checks actually run for this extraction; the original kit's initial
receipts retain their original scope.
