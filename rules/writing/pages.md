# Page design and review

## Page design

Give each section one coherent purpose: answer a question, show a construction or compare alternatives. Split when the purpose changes; merge thin sections into their concept. Heading levels do not require separate cards. Use cards, tiles, tabs and callouts for distinct roles, without arbitrary word limits or one-screen constraints.

Titles state the takeaway. A one-sentence `bs-lead` states the claim before the evidence. When reporting on the reader's questions, use each question as a heading, answer directly, then show evidence. Follow the [explanation prerequisites](explanations.md#story-and-reading-layers) and keep a formal, plain human voice. Internal registry tags, bug-hunt narratives, file-routing tables and debugging chronology stay off rendered surfaces.

When the purpose of a section is to explain a mechanism or spatial
relationship, place the figure after the heading or a one-sentence takeaway. Follow it with the
prose needed to interpret it. A table or equation may lead when exact values
or a derivation carry the explanation. Apply the
[visual completion gate](figures.md#figures-and-comparisons) to the claims in the section.

Navigation follows prerequisite order. Important comparisons have direct entries opening onto controls and plots. Follow the [shared reader contract](../site/reader.md#shared-reading-layout); do not use page-wide audience tabs. Local method, scenario and diagram-mode tabs are useful within a comparison.

Use available width. Text, figures and tables share a left edge. Avoid narrow centered text columns and half-empty rows. Expressive details may include short transitions, rich syntax colors, gradient hairlines and hover emphasis; they must respect reduced motion and accessibility.

### Project-owned homepages

Each project chooses its homepage composition, information hierarchy, sections,
hero treatment and visual story. Using the shared kit does not require projects
to have matching homepages. A research narrative, an engineering reference and
a navigation dashboard can use different arrangements and local presentation.

Shared visual components are optional building blocks with clear recurring
uses, such as disclosures, comparison controls and table treatment. Sharing one
component does not transfer ownership of the surrounding page. Keep project
illustrations, scientific figures, domain widgets and distinctive compositions
local. The starter homepage is an example, not a required project template.

Navigation is shared, not owned by one page. When readers expand their chapters
under the site tree, a homepage that lists its own sections instead makes every
move to a reader feel like a different site; keep the same tree on every page and
let the homepage present the pages through cards or its own composition.

## Build-sheet pages

Opt in with `page_css = ["build-sheet.css"]`. Keep page-specific extras in a separate local stylesheet. The shared theme supplies Saira Condensed headings, IBM Plex Sans body text and IBM Plex Mono labels/units. Follow the [shared dependency rules](../site/reader.md#shared-reading-layout) for fonts.

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

One `bs-board` holds current status: Done, Decided, Passed, Open or Parked. Use `bs-ok`, `bs-wait`, `bs-bad` and `bs-off` as appropriate. Parked includes a reopening condition. An Open row owns remaining work; do not repeat it in limits prose. Scope caveats stay beside their evidence. Status does not substitute for evidence: Decided is not implemented; a local/CPU test is not a native runtime check.

## Slide faces

A chapter may open with one slide face: a 16:9 summary that states the chapter's takeaway with one visual. The full chapter follows it and remains the complete, end-to-end readable source. A reader skimming slides sees the argument; a reader continuing sees every definition, qualification and piece of evidence.

- The title states the finding as a sentence, not a topic. The eyebrow names the subject without a chapter number; the reader card and extracted deck supply numbers.
- Use one visual built from the shared slide vocabulary (tiles, factor grids, equation terms, numbered steps, a figure beside headline numbers) or a project-local diagram. Reuse the chapter's own figure assets rather than drawing a second version of the same data.
- End with a scope line saying what the numbers cover and what remains unmeasured. Caveats that change a claim's meaning belong on the slide, not only in the chapter.
- No fact exists only on a slide. Every number and claim on it is stated, with its evidence, in the chapter below; update both in the same edit. This is the one sanctioned repetition of a fact: the slide is a view of the chapter, never its owner.
- Keep the canvas uncrowded. A face that does not fit 16:9 has too much content for one slide; move detail into the chapter instead of shrinking type. Below 720 px the face stacks into a readable column.
- Slide figures are views of numbered chapter figures; they carry a short caption without a new number.
- Give each tone one meaning across all of a project's slides: the accent and warm tones identify the compared methods, `is-alert` marks failures and warnings, `is-held` marks held-out, hidden or pending items, and everything else stays neutral.

## Completion and review

Follow the requested review arrangement: separate prototype or uncommitted in-place trial. Preserve content, evidence, media identities and public anchors during layout work. Follow the [documentation review gate](../documentation.md#rules-for-changes-and-chronology) and complete [site validation](../site/validation.md#validation-and-review), including the project-required checks. A decision page ends with a criteria-based options table and a clear verdict.
