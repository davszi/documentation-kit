# Writing and visual evidence

Human pages explain. Agent records preserve exact contracts and evidence. The [documentation system](documentation.md) owns placement and lifecycle; this guide owns content and presentation.

## Page design

Give each section one coherent purpose: answer a question, show a construction or compare alternatives. Split when the purpose changes; merge thin sections into their concept. Heading levels do not require separate cards. Use cards, tiles, tabs and callouts for distinct roles, without arbitrary word limits or one-screen constraints.

Titles state the takeaway. A one-sentence `bs-lead` states the claim before the evidence. When reporting on the reader's questions, use each question as a heading, answer directly, then show evidence. Define jargon before use and keep a formal, plain human voice. Internal registry tags, bug-hunt narratives, file-routing tables and debugging chronology stay off rendered surfaces.

Navigation follows prerequisite order. Important comparisons have direct entries opening onto controls and plots. Use the shared reader; do not maintain per-page reader copies or page-wide audience tabs. Local method, scenario and diagram-mode tabs are useful within a comparison.

Use available width. Text, figures and tables share a left edge. Avoid narrow centered text columns and half-empty rows. Expressive details may include short transitions, rich syntax colors, gradient hairlines and hover emphasis; they must respect reduced motion and accessibility.

## Build-sheet pages

Opt in with `page_css = ["build-sheet.css"]`. Keep page-specific extras in a separate local stylesheet. The shared theme supplies vendored Saira Condensed headings, IBM Plex Sans body text and IBM Plex Mono labels/units; do not fetch remote fonts.

Cards keep the reader stage height. Each chapter carries its claim and a meaningful visual block: figure, flow, table or tiles. At 1600 × 1000 it should fill about half a card; merge a thin chapter rather than padding it. Main media uses full width (`bs-grid g1`); photos/renders use at most two per row; paired animations sit together. Fill every row: two, three or four items; five as three over two (`bs-checks r32`); six as three by two; seven as four over three; eight as four by two. Reflow for narrow columns.

| Block | Purpose |
|---|---|
| `bs-lead` | One-sentence chapter claim |
| `bs-specs` | Labelled key values |
| `bs-stats` | Two to four headline measurements, with units and scope |
| `bs-chips` | Short option tags; rejected options retain their reason |
| `bs-grid g1` through `g4` | Visual or parallel-content rows |
| `bs-checks`, `bs-check`, `bs-badge` | Checkable parallel claims with explicit state |
| `bs-board`, `bs-row`, `bs-state` | Single current-status board |
| `bs-flow`, `bs-node`, `bs-arrow`, `bs-back` | One-way mechanism with labelled arrows and explicit prohibited feedback |
| `bs-stack` | Two or three boxes merging or fanning out within a flow column |
| `bs-part` | Contrasting parallel lists |
| `bs-orange` through `bs-muted` | Shared semantic tones, never meaning by color alone |

A flow may use `n2` for two boxes. Keep arrow labels near 12 characters and box titles near 30; put identifiers and field details in small diagram labels, with full mappings in the topic record.

One `bs-board` holds current status: Done, Decided, Passed, Open or Parked. Use `bs-ok`, `bs-wait`, `bs-bad` and `bs-off` as appropriate. Parked includes a reopening condition. An Open row owns remaining work; do not repeat it in limits prose. Scope qualifications stay beside their evidence. Status does not substitute for evidence: Decided is not implemented; a local/CPU test is not a native runtime check.

## Story and reading layers

Order by understanding: purpose, prerequisites, ingredients, mechanism, examples, evidence and limits. Introduce the instrument before its numbers and evidence before a shipping consequence. Define terms before using them. Explain each concept or formula in one canonical place; elsewhere bridge to it. An essential repeated equation needs a back-reference.

Keep one visible Story. Optional depth uses typed folds:

```markdown
<!-- fold: math Derivation of the bound -->
Supporting derivation.
<!-- /fold -->
```

Use `math`, `experiment`, `code` and `dead-end` (displayed as Alternatives). The complete argument, narrative figures, comparison cases and verdict remain intelligible with every fold closed. Optional layers deepen that argument; they do not hide a separate required argument. A fold title is already its heading; do not repeat it inside. Preserve deep-link anchors when consolidating.

Choose by narrative weight, not element type: a table or equation may carry the Story; a plot may be supporting detail. Default to visible figures and folded reference density. Keep competing formulations together, with assumptions and verdict explicit. Add a new layer only for recurring content and follow the [maintenance procedure](maintenance.md#extending-reading-layers).

When moving detail into a record, keep the former page anchor on the summary that replaces it and link to the matching record anchor. Keep concise lessons from rejected methods reachable, with verdict up front; detailed captures/reproduction remain evidence.

## Naming and honest claims

Use one term per object across prose, controls, legends, tables, figures and output. Name a mechanism the reader sees; use formulation internals only when explaining that formulation. A rename sweeps all surfaces. State what a function receives, returns and optimizes/interpolates, and which inputs vary or stay fixed.

Decision rationale belongs beside the decision, including why an instrument/default was chosen and why alternatives lost. Current baselines measure what ships; label retired baselines historical. An experimental verdict and deployment measurements are distinct content kinds.

Separate claims requiring different evidence: visual fidelity, smoothness, input preservation, correspondence with a source and physical accuracy. A local check or smoother drawing proves only its tested property. Label accepted future behavior, implemented behavior, CPU checks and native/runtime observations separately. Say "not measured" plainly and provide a supported bound where available. Never manufacture an estimate to fill an empty metric.

## Numbers and staleness

A current measured claim requires a source commit, exact reproduction command, runtime/environment, workload, units, baseline, method and scope. Link its raw result and limitations. Config values, derivations and design arithmetic are not measurements; cite their source and label them accordingly.

When code, input data, method, workload or runtime conditions affecting a claim change, rerun before quoting it as current qualification. Keep the old record's date, runtime, inputs and scope; a historical label does not qualify changed inputs. Presentation-only edits may reuse captured results only after checking identities, numbers and treatments remain intact.

Keep full result tables, failures, protocols, snapshots and reviews with the experiment. The page explains what they establish. The worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the deletion gate.

## Figures and comparisons

A visual must answer an actual understanding or evidence need. Prefer a worked construction, comparison or counterexample; do not add a decorative plot because a formula exists. Use a small table when it communicates sparse data better.

Every mechanism needs a diagram; every geometric/spatial claim needs a picture; every measured claim needs a plot or table. This is a completion gate. Budget visual production before declaring a section done. Figures, tables and headings alone should convey the story.

Every included figure has:

- A stable HTML anchor and visible numbered caption. Use page-wide numbers or a named sequence such as P1; numbers are unique and follow reading order within a sequence.
- An explanatory prose reference linking its number to that anchor. Say what to notice and why it supports the claim; identify relevant panels. Alt text, a title or caption alone is not a prose reference.
- Clickable references everywhere, including table cells, panel labels and references to other figures inside captions. A caption's own number is its identifying label.
- Source/provenance and useful alternative text. Generated figures name their generator, source revision, inputs and date in a manifest or metadata. Preserve provenance for SVG, PNG and interactive data alike.

A plot, diagram, flow, interactive comparison or evidence capture is a figure. An appearance-only image gets a short caption without a number. A deliberate unreferenced figure needs an adjacent source comment: `<!-- unreferenced figure: reason -->`.

Design comparisons together: matched orientation, scale, framing and input cases; persistent zoom across switching; overview locating a detail; consistent markers and colors across profiles/tables. Method names in controls/legends carry identity independently of color. Offer every option named in the comparison, grouped by method with roles such as current, selected, previous or rejected. An interactive comparison replaces its redundant static gallery, while retaining a useful loading/fallback image.

Draw the finding directly rather than making the eye compute it. Show the actual sample locations and construction; distinguish measurements, solved points, continuous geometry and its rendering polygon. For independent changes, show baseline, each change alone and their combination across relevant scenarios, with a neighboring ablation table and metric definitions. Explain a zero effect honestly.

Charts fit their actual column with labels at least 11 px. Keep bar labels short or move them into a legend. Crop empty margins; avoid baked title bars, badges and debugging chronology. Use one camera/view across a series. Do not shrink an important comparison to fit a screen at the cost of legibility. Bound overview height and retain full-size inspection.

Use the project's shared dark-compatible figure style, never ad hoc per-figure styles. Generated assets are outputs: edit their data/generator, not their bytes. Keep an explicit figure-to-generator manifest and check for missing/orphaned resources. Source-authored HTML flows count as local diagrams: their page source is the generator, and layout must pass the same collision/overflow review.

## Interaction and access

Interactive views load independently, confine drag/scroll/keys to their region and never steal page focus. Linked views follow the same selected state. Data comes from the exact run inputs/outputs, checked by hash; show a static main render while loading. SVG toggles and their zoomed/lightbox controls stay synchronized. Carousel autoplay stops on engagement and pauses while a lightbox is open.

Use shared components rather than duplicating handlers. Keep controls visible, labelled, keyboard accessible and at least 44 px touch targets. Give scrollable tables/equations labelled local regions. Nothing may overflow the page at any viewport. Verify wide, narrow and equal-column layouts, keyboard/focus behavior, reduced motion, no-JavaScript reading and print. DOM checks do not replace rendered inspection.

## Mathematical explanation

Build from the reader's known construction. Define symbols, units, mathematical terms and prerequisites before use. Show intermediate reasoning, including product/chain rules when relevant. State structural assumptions and distinguish local conditions from global validity. A non-obvious formula needs a derivation or precise companion-section citation.

Reuse Story geometry, orientation, colors and example inputs in Math. Mark variables, vectors, constraints and error terms where they act; identify inputs, geometry-derived values and solved quantities. Walk from those marks to the equation and a worked numerical example. Do not add a disconnected formula plot or duplicate picture without useful annotations.

Use `$…$` and `$$…$$` in Markdown when `math = true`; inside raw HTML use `\(…\)`. Math uses bundled KaTeX without a CDN. Wrap long expressions or provide contained scrolling; never make type unreadably small. Inspect rendered raw-HTML formulas too. Analytic derivative/Jacobian claims name their numerical verification tolerance and executable self-test.

## Code and diagrams

Use a snippet only when it explains a seam or difficult contract better than prose. Excerpt real repository code, usually a signature and 3–10 decisive lines; link the rest. Use source metadata such as `python source=src/example.py#L42-L49` so drift checks can verify content and real line numbers. Do not present idealized pseudocode as a verified implementation excerpt. Put concise design rationale beside the code. Render excerpts with distinct type/class/function colors, a copy button, source chip, language badge and a line-number gutter showing actual source lines. Reuse shared code chrome and keep every control accessible.

Diagrams come from data or explicit local source and include overflow/collision checks or rendered QA. Shared color/edge semantics apply across pages: boxes denote named components, edges explicitly mean ownership/calls/data flow, dashed lines mean a documented optional path. Include a legend and name the data source in the caption. Numbered sequence steps, common-data mode views and quantitative generated SVGs are useful patterns.

Reuse supported pan/fullscreen/annotation controls where relevant. Do not claim planned edge highlighting, drill-down or semantic zoom as implemented. If added, choose drill-down for independent child diagrams with a breadcrumb, or semantic zoom when surrounding context must remain visible.

## Run visuals and experiment lifecycle

Prefer scripted captures with the same provenance as other figures. An inherently interactive screenshot must state commit, date and scenario/preset; it illustrates appearance, never a quantitative claim. Derive overlays from recorded artifacts rather than screenshots when data exists. Show dynamic behavior through an intentionally packaged short clip or useful frame sequence, with normal captions and provenance. Large local captures remain with the producing experiment and retained hashes; publish tracked posters/keyframes and an honest local-media notice.

A live public experiment report uses `ongoing = true`; remove it only when findings and limits are settled. Keep protocol, producing code, inputs, outputs, failures, pins and independent reviews with its experiment. The owning topic explains scope and links to evidence.

Every complete experiment includes:

- Reproduction command and runtime; provide a quick mode when the full run exceeds about one minute.
- Measured motivation, strongest cheap baseline and acceptance bar stated before results.
- Results with units, verdict against the bar (including failure), caveats and path forward.

Verify the baseline before changing measured behavior. A production benchmark drives shipped paths end to end with honestly labelled ablations, reusable case generation/metrics, runtime reporting and provenanced figures. A method experiment adds an independent derivation from published formulas rather than copying implementation, a guarded optional native comparison and an exit self-check. State observed agreement, not presumed parity.

Use a thin regression gate covering historically difficult regimes, documented band tolerances and a known-bad failure when available. Keep fast gates short (target under five seconds). Suitable experiment visuals include actual-geometry quality overlays, convergence, reference parity, timing/scaling and trade-off plots; omit inapplicable views explicitly. Update topic, worklog and open routing in the same deliverable.

## Completion and review

Follow the requested review arrangement: separate prototype or uncommitted in-place trial. Preserve content, evidence, media identities and public anchors during layout work. A review request stops adoption, commit and push until approved. Finish with rendered wide/narrow inspection, evidence/provenance checks and the project-required validations. A decision page ends with a criteria-based options table and a clear verdict.
