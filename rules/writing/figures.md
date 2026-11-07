# Figures, comparisons and access

## Figures and comparisons

A visual must answer an actual understanding or evidence need. Prefer a worked construction, comparison or counterexample; do not add a decorative plot because a formula exists.

Use diagrams for structure, ownership, flow or sequence. Label the relevant
objects and transitions in place. Use tables for exact lookup and comparison of
values, conditions or criteria. Use plots for patterns, variation or trade-offs.
Pair formats when they answer different questions. Show the details the reader
needs to understand or check the claim. Keep complete field mappings and
implementation inventories in linked records.

Every mechanism needs a diagram; every geometric/spatial claim needs a picture; every measured claim needs a plot or table. This is a completion gate. Budget visual production before declaring a section done. Figures, tables and headings alone should convey the story.

Every included figure has:

- A stable HTML anchor and visible numbered caption. Use page-wide numbers or a named sequence such as P1; numbers are unique and follow reading order within a sequence.
- An explanatory prose reference linking its number to that anchor. Say what to notice and why it supports the claim; identify relevant panels. Alt text, a title or caption alone is not a prose reference.
- Clickable references everywhere, including table cells, panel labels and references to other figures inside captions. A caption's own number is its identifying label.
- Source/provenance and useful alternative text. Generated figures name their generator, source revision, inputs, date and output hash in a manifest or metadata. Preserve provenance for SVG, PNG and interactive data alike.

A plot, diagram, flow, interactive comparison or evidence capture is a figure. An appearance-only image gets a short caption without a number. A deliberate unreferenced figure needs an adjacent source comment: `<!-- unreferenced figure: reason -->`.

Design comparisons together: matched orientation, scale, framing and input cases; persistent zoom across switching; overview locating a detail; consistent markers and colors across profiles/tables. Method names in controls/legends carry identity independently of color. Offer every option named in the comparison, grouped by method with roles such as current, selected, previous or rejected. An interactive comparison replaces its redundant static gallery, while retaining a useful loading/fallback image.

Draw the finding directly rather than making the eye compute it. Show the actual sample locations and construction; distinguish measurements, solved points, continuous geometry and its rendering polygon. For independent changes, show baseline, each change alone and their combination across relevant scenarios, with a neighboring ablation table and metric definitions. Explain a zero effect honestly.

Charts fit their actual column with labels at least 11 px. Keep bar labels short or move them into a legend. Crop empty margins; avoid baked title bars, badges and debugging chronology. Use one camera/view across a series. Do not shrink an important comparison to fit a screen at the cost of legibility. Bound overview height and retain full-size inspection.

Use the project's shared dark-compatible figure style, never ad hoc per-figure styles. Follow the shared [generated-file practices](../engineering/code.md#generated-files) when changing generated assets. Keep an explicit figure-to-generator manifest and check for missing/orphaned resources. Source-authored HTML flows count as local diagrams: their page source is the generator, and layout must pass the same collision/overflow review.

## Interaction and access

Interactive views load independently, confine drag/scroll/keys to their region and never steal page focus. Linked views follow the same selected state. Data comes from the exact run inputs/outputs, checked by hash; show a static main render while loading. SVG toggles and their zoomed/lightbox controls stay synchronized. Carousel autoplay stops on engagement and pauses while a lightbox is open.

Use shared components rather than duplicating handlers. Keep controls visible, labelled, keyboard accessible and at least 44 px touch targets. Give scrollable tables/equations labelled local regions. Nothing may overflow the page at any viewport. Apply the [site validation and review requirements](../site/validation.md#validation-and-review).
