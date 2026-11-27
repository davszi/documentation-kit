+++
title = "Writing pages"
brand_sub = "chapters · folds · figures · math · code"
description = "How a page for people explains its record: one claim per chapter, page types, build-sheet blocks, the visible story and its folds, figures, mathematics and code excerpts, with illustrative examples."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css", "writing-practices/writing-practices.css"]
toc = [["Guide per task", "#routes"], ["Chapters", "#page-design"], ["Build sheets", "#build-sheets"], ["Story and folds", "#explanations"], ["Figures", "#figures"], ["Mathematics", "#mathematics"], ["Code excerpts", "#code-excerpts"]]
page_only = "Explains the page guides; they are the records, in rules/writing.md and rules/writing/."
+++

# Writing pages

<section class="card" id="routes">

## Five page guides decide how a page for people presents its record

<p class="bs-lead">This page answers one question: how is a page for people written so that it explains its record, from the order of its chapters to its figures, formulas and code?</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Page guides by task">

| Before… | Read… | Explained here |
|---|---|---|
| Making a new page for people, once a person asked for one, or page work on an existing page beyond a small sync | The [page index](writing.html) and the [site guides](maintenance.html), after [record first, page on request](documentation-system.html#record-first-page-on-request) | [Chapters](#page-design) |
| Laying out a rendered page | [Page design](page-design.html) | [Chapters](#page-design), [Build sheets](#build-sheets) |
| Writing an explanation on a page | [Explanations](explanations.html) | [Story and folds](#explanations) |
| Adding a figure or comparison | [Figures](figures.html) | [Figures](#figures) |
| Writing mathematics | [Math](math.html) | [Mathematics](#mathematics) |
| Showing code or a code diagram | [Code excerpts](code-excerpts.html) | [Code excerpts](#code-excerpts) |

</div>

The table is a lookup: find the action, read the guide, then the chapter here that explains it. A page explains a record that already exists; when page work starts, who does it and who checks it are on [Records and documents](documentation-practices.html#record-first). Whoever writes the page reads the guides above first.

Each chapter says why a rule exists, shows it and links the section that holds the exact text. The examples are invented and contain no measured results.

</section>

<section class="card" id="page-design">

## Each chapter carries one claim; the page's question sets their order

<p class="bs-lead">A chapter is one <code>##</code> section or card with one claim: its title states the takeaway, a one-sentence lead states the claim, and the evidence follows. The page as a whole answers one question of its reader.</p>

<figure id="fig-page-types">
<div class="wp-fig wp-types">
<div class="wp-type"><b>Design</b><em>How does this system, or this part, work?</em><ol><li>purpose</li><li>parts</li><li>one step from start to end</li><li>settings</li><li>how it was checked</li><li>limits</li></ol></div>
<div class="wp-type"><b>Method</b><em>How is this problem solved, and why this way?</em><ol><li>problem</li><li>formulation</li><li>solution</li><li>whether it worked</li><li>alternatives</li><li>limits</li></ol></div>
<div class="wp-type"><b>Specification</b><em>What is agreed, or what exists, item by item?</em><ol><li>scope</li><li>each item with its status or guarantee</li><li>origin and checks</li><li>what is left out</li></ol></div>
<div class="wp-type"><b>Investigation</b><em>What is the answer to this question?</em><ol><li>question</li><li>answer</li><li>what was run</li><li>evidence</li><li>limits</li><li>next step</li></ol></div>
<div class="wp-type"><b>Qualification</b><em>Is this system accepted against its bar?</em><ol><li>system and bar</li><li>status at a glance</li><li>verdict for each gate</li><li>exceptions</li><li>what remains</li></ol></div>
<div class="wp-type"><b>Related work</b><em>What did others do, and what does it mean for us?</em><ol><li>what the other work does</li><li>what matches ours</li><li>what it means for us</li><li>sources</li></ol></div>
</div>
<figcaption><b>Figure 1.</b> Six page types: the reader's question, and the default order of chapters that answers it. Drawn from the table in <a href="page-design.html#page-types">page types</a>.</figcaption>
</figure>

A heading that only names a topic, such as "Results", makes the reader search the chapter for its point, and a chapter with two purposes buries both. So each chapter answers a question, shows a construction or compares alternatives, and splits when its purpose changes. A chapter that would only repeat what another chapter or page shows gives its point to the one that owns the subject, and its anchor still leads there.

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">A topic title</span><h3>Results</h3><p>The chapter opens with setup, walks through each measurement and says in its last sentence which option was kept.</p></div>
<div class="bs-part bs-green"><span class="bs-label">A takeaway title</span><h3>Option B is kept because it needs one fewer manual step</h3><p>The lead states the claim, the comparison figure follows, and the prose says what the figure shows and where the claim stops.</p></div>
</div>

[Figure 1](#fig-page-types) moves up one level. A page answers one question, and the question sets a default order of chapters. The order is a starting point: a part with nothing to say is left out, and the subject may reorder the rest. A page that needs two types is usually two pages. A project may name one of its pages as the reference for a type, or name its own type with one reference page; nothing checks a page's type. A page that supports a decision ends with an options table against stated criteria and a clear verdict.

A page starts with its first chapter. Text above it has no heading that states its point, and in the reader it opens the first chapter anyway; strict lint warns with its length, and the author moves it into a chapter or keeps it on purpose with `opening = "keep"` in the frontmatter. A page that explains how something works names the people who do it by role, one role word each; a name stays only where the page says who decided, approved or said something. Text and figures share a left edge, use the available width and render at 11 px or more, small labels included.

<!-- fold: dead-end Why homepages are not one shared template -->

Each project composes its own homepage: the order of information, the sections, the hero and the visual story. A research narrative and a navigation dashboard can look quite different and still use the kit, and the starter's homepage is an example. Navigation is the shared part: the same site tree on every page, so that moving from the homepage into a reader page does not feel like entering a different site.

<!-- /fold -->

Full guide: [page design](page-design.html#page-design), [page types](page-design.html#page-types), [project-owned homepages](page-design.html#project-owned-homepages) and, for the frontmatter, [authoring paths](authoring.html#authoring-paths).

</section>

<section class="card" id="build-sheets">

## Build-sheet blocks keep one meaning, and status never replaces evidence

<p class="bs-lead">Each shared block means the same on every page; a status board and a slide face point to evidence and never stand in for it.</p>

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-ok">Done</span><b>Work is finished</b><span>Status does not substitute for evidence; scope caveats stay beside their evidence.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Decided</span><b>A choice is made</b><span>Decided is not implemented.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Passed</span><b>A check passed</b><span>A local or CPU test is not a native runtime check.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Work remains</b><span>The Open row owns the remaining work; limits prose does not repeat it.</span></div>
<div class="bs-row"><span class="bs-state bs-off">Parked</span><b>Set aside</b><span>A Parked row includes its reopening condition.</span></div>
</div>

The board above is the real block, filled with what each of its five states means; it reports no project's status. Shared blocks help only if each means the same thing everywhere: a row reading "Decided" can be mistaken for shipped work, so the board says what each state does not prove. A page has one board. The other blocks, from the one-sentence `bs-lead` to flows, tiles and checks, are listed by purpose in [build-sheet pages](page-design.html#build-sheet-pages), with the rule that every row is filled: two, three or four items, or a fixed split for more.

<!-- fold: detail Slide faces -->

A chapter may open with one 16:9 slide face, a summary that states its takeaway and shows it; the chapter below stays the complete source. Faces are added last and only on request: build the chapters, then ask the person, and add none without a yes. A face earns its place by its visual, drawn from the chapter's own figures and numbers and laid out for the shape of its finding. Boxes of text are not a visual, except the terms of a formula the chapter explains or a grid that compares options factor by factor; a chapter with nothing to show gets no face. No fact lives only on a face: lint warns about a number a face shows and its chapter does not. A review of existing faces sorts each into redraw or remove, redesign, or keep, with a reason. Examples are on [Build a site](build-a-site.html#figures-and-slides).

<!-- /fold -->

Full guide: [build-sheet pages](page-design.html#build-sheet-pages) and [slide faces](page-design.html#slide-faces).

</section>

<section class="card" id="explanations">

## Keep one visible story in order of understanding, with optional depth in typed folds

<p class="bs-lead">A reader can follow the complete argument and its verdict with every fold closed; a fold the author marks open shows depth that most readers of the chapter need.</p>

<figure id="fig-story">
<div class="bs-flow n2" role="img" aria-label="The visible Story holds the complete argument in order of understanding: purpose and prerequisites, ingredients and mechanism, examples, evidence and limits, comparison cases and verdict. Typed folds for math, experiment, code and dead-end add optional depth. A fold starts closed unless its author marks it open for depth most readers of the chapter need. Folds never hide a separate required argument.">
<div class="bs-node bs-teal"><span class="bs-label">Always visible</span><b>The Story</b><ul><li>Purpose and prerequisites</li><li>Ingredients and mechanism</li><li>Examples, evidence and limits</li><li>Comparison cases and verdict</li></ul></div>
<div class="bs-arrow"><span>go deeper</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Optional</span><b>Typed folds</b><ul><li><code>math</code>, <code>experiment</code>, <code>code</code>, <code>dead-end</code> (Not chosen)</li><li>closed by default</li><li><code>(open)</code>: depth most readers of the chapter need</li><li>a reader's own click is remembered</li></ul></div>
<div class="bs-back"><span>×</span> A fold never hides a separate required argument.</div>
</div>
<figcaption><b>Figure 2.</b> Optional depth branches from a complete visible argument. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An explanation fails when the reader meets a number before the instrument that produced it, or a term before its definition, so the Story runs in order of understanding: purpose, prerequisites, ingredients, mechanism, examples, evidence and limits. It also fails when the decisive step hides in a section many readers never open. [Figure 2](#fig-story) shows the guard: the arrow goes one way, and the argument, its narrative figures, comparison cases and verdict stay readable with every fold closed.

A fold is chosen by narrative weight, not by element type: a table may carry the Story and a plot may be supporting detail. It starts closed. Writing `(open)` after its kind, as in `<!-- fold: math (open) Derivation -->`, starts it open, for depth that most readers of that chapter need. The reader's section options open every fold of one kind across the page, and a reader's own click on a fold is remembered until an option sets its kind again, as the [reader guide](reader.html#shared-reading-layout) describes. A fold's title is already its heading and is not repeated inside.

Each concept or formula is explained in one place and linked elsewhere, and a short scope label stays beside any evidence it changes the reading of. When detail moves into a record, the former page anchor stays on the summary that replaces it, and the summary links the record. A new kind of fold is added only for recurring content the four kinds cannot express, through a shared [kit change](reader.html#extending-reading-layers).

Full guide: [story and reading layers](explanations.html#story-and-reading-layers).

</section>

<section class="card" id="figures">

## Draw what can be drawn: every mechanism, spatial claim and measured comparison needs a visual

<p class="bs-lead">A chapter is not done until a mechanism has a diagram, a spatial claim a picture and a measured comparison, ranking or trend a plot; a single value or an exact lookup may stand in text or a table.</p>

<figure id="fig-forms">
<div class="wp-fig wp-forms">
<div class="wp-chooser">
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><rect x="2" y="12" width="18" height="16" rx="3"/><rect x="44" y="12" width="18" height="16" rx="3"/><path d="M20 20h20M36 16l5 4-5 4"/></svg><b>Diagram</b><span>a mechanism, structure, ownership or flow</span></div>
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M4 34 L24 8 L44 30 L60 18"/><circle cx="24" cy="8" r="3"/><circle cx="44" cy="30" r="3"/></svg><b>Picture</b><span>a geometric or spatial claim</span></div>
<div class="wp-form wp-hot"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M6 4v32h54"/><path d="M10 30 L24 22 L38 16 L54 8"/><circle cx="24" cy="22" r="2.5"/><circle cx="38" cy="16" r="2.5"/></svg><b>Plot</b><span>values compared, ranked or changing over a setting</span></div>
<div class="wp-form"><svg viewBox="0 0 64 40" aria-hidden="true"><path d="M4 6h56M4 18h56M4 30h56M28 6v28"/></svg><b>Text or table</b><span>a single value or an exact lookup; a table may sit beside a figure</span></div>
</div>
<div class="wp-schematic"><span class="wp-tag">Numbers on a page · schematic, no data</span>
<svg viewBox="0 0 240 120" aria-hidden="true"><path class="wp-axis" d="M24 8v96h208"/><path class="wp-line" d="M40 88 L84 70 L128 52"/><circle cx="40" cy="88" r="4"/><circle cx="84" cy="70" r="4"/><circle cx="128" cy="52" r="4"/><circle class="wp-gap" cx="172" cy="36" r="9"/><path class="wp-dash" d="M128 52 L172 36"/></svg>
<ul class="wp-keys"><li><b>x</b> the setting that changes the value</li><li><b>y</b> in the unit of the claim</li><li><b class="wp-gapkey">○</b> not run, where its point would stand</li></ul>
</div>
</div>
<figcaption><b>Figure 3.</b> What the claim shows decides its form; a value that depends on a setting is drawn over that setting. This illustrative diagram is authored in the page source; the plot is a schematic and carries no data.</figcaption>
</figure>

Prose alone leaves each reader to build the picture, and different readers build different ones; a visual that only repeats the text has not earned its place either. The four tiles of [Figure 3](#fig-forms) show the choice: what the claim shows sets the form, and a table is for reading off single values, not for comparing them. Within that, aim for the most telling picture the claim allows, and vary the forms across a page; this page uses flows, a matrix, tiles beside a schematic and a real excerpt.

The schematic beside them applies the same idea to numbers. A value shown at one setting alone hides how it depends on that setting, so it becomes a plot over the settings that change it. The axis stays in the unit of the claim: a claim about accuracy is not restated in seconds. A setting that has not run is named as not run in the place its result would take, and a result that carries no pass or fail says so in its heading.

A missing figure is work to do. The page author makes it from what exists, measured data for a plot, code and configuration for a flow, geometry for a picture, records its generator and inputs, and puts any number it computes into the record first. A claim stays without its figure only when nothing true can be drawn, and the completion report then says which figure is missing and what it would take. Invented data is never drawn, and a sketch never reads as a measurement; the schematic above has no numbers for that reason.

Every figure has a stable anchor, a numbered caption, a prose reference like the one above that links its number and says what to notice, a named source and useful alternative text; an image that only shows appearance gets a caption and no number. Chart labels stay at 11 px or more, controls are at least 44 px as touch targets, and nothing overflows the page at any width.

<!-- fold: detail Comparisons, captures and live reports -->

Compared views share orientation, scale, framing and input cases, keep their zoom while switching and use one set of markers and colours; method names, not colours alone, carry identity. For independent changes, show the baseline, each change alone and their combination, beside an ablation table, and explain a zero effect honestly. Prefer scripted captures with their generator and inputs; an interactive screenshot states its commit, date and scenario and never supports a quantitative claim. A public report on a live experiment carries `ongoing = true` until its findings and limits are settled.

<!-- /fold -->

<!-- fold: detail Generated figures, palettes and colour meanings -->

A generated figure names its generator and input data in a manifest or metadata; Git holds its revision, date and bytes. It takes its colours from the kit's figure palettes and is written in a dark file for pages and a light file for slides and print. A project whose figures give a colour a meaning keeps those meanings in one table in its development conventions, and a new meaning gets its row before its first figure. Flows written in the page source, like the figures here, count as local diagrams: the page source is their generator, and their layout passes the same overflow review. A figure left unreferenced on purpose carries a source comment beside it:

```html
<!-- unreferenced figure: reason -->
```

<!-- /fold -->

Full guide: [figures and comparisons](figures.html#figures-and-comparisons), [interaction and access](figures.html#interaction-and-access), [run visuals and experiment lifecycle](figures.html#run-visuals-and-experiment-lifecycle) and, for numbers, [page design](page-design.html#page-design).

</section>

<section class="card" id="mathematics">

## Derive mathematics from a construction the reader already has

<p class="bs-lead">Define every symbol before use, show the intermediate steps and tie the equation back to the Story's picture.</p>

<figure id="fig-math">
<div class="bs-flow" role="img" aria-label="Math reuses the Story's geometry, orientation, colors and example inputs. Variables, vectors, constraints and error terms are marked where they act, identifying inputs, geometry-derived values and solved quantities. From those marks the explanation walks to the equation and a worked numerical example. A disconnected formula plot or a duplicate picture without useful annotations is not added.">
<div class="bs-node bs-teal"><span class="bs-label">From the Story</span><b>The same picture</b><ul><li>Same geometry and orientation</li><li>Same colors</li><li>Same example inputs</li></ul></div>
<div class="bs-arrow"><span>mark</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Marked where they act</span><b>Named quantities</b><ul><li>Variables, vectors and constraints</li><li>Error terms</li><li>Inputs, geometry-derived values, solved quantities</li></ul></div>
<div class="bs-arrow"><span>derive</span></div>
<div class="bs-node bs-blue"><span class="bs-label">Result</span><b>Equation and example</b><ul><li>Intermediate steps</li><li>Worked numerical example</li></ul></div>
<div class="bs-back"><span>×</span> No disconnected formula plot or duplicate picture without useful annotations.</div>
</div>
<figcaption><b>Figure 4.</b> The Math layer walks from marks on the Story's picture to the equation and a worked example. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A formula with undefined symbols asks the reader to trust it rather than follow it, and a formula plot unconnected to the Story adds a second picture to decode. [Figure 4](#fig-math) shows the alternative: the equation is reached through marks on the picture the reader already has, then worked with the Story's own inputs. Along the way, symbols, units and prerequisites are defined before use, intermediate steps such as a chain rule are shown, and local conditions are kept apart from global validity. A non-obvious formula gets its derivation or a precise citation of the section that derives it; a claim about an analytic derivative or Jacobian names its numerical tolerance and the self-test that checked it.

<!-- fold: detail KaTeX syntax and the formula check -->

With `math = true` in the frontmatter, write `$…$` and `$$…$$` in Markdown and `\(…\)` inside raw HTML. The kit renders with its bundled KaTeX, fetches nothing, and lint compiles every formula of the built pages, naming each one that would show as raw text. A long expression wraps or scrolls in its own box; the type is never shrunk until it is hard to read.

<!-- /fold -->

Full guide: [mathematical explanation](math.html#mathematical-explanation) and the [formula check](authoring.html#formula-check).

</section>

<section class="card" id="code-excerpts">

## Excerpt only real code, and draw code diagrams with shared meanings

<p class="bs-lead">A snippet shows real repository lines with source metadata that drift checks verify; a diagram's boxes, edges and dashes mean the same on every page.</p>

<figure id="fig-excerpt">

```python source=tooling/build.py#L96-L103
# `<!-- fold: math (open) The route-level problem -->` makes the fold start open.
# Types drive the color + the reader's "Also show" options (fold-controls.js).
FOLD_TYPES = ("math", "experiment", "code", "dead-end")
# The markers match to the end of their own line only. Matching further would
# swallow the blank line after a closing marker, and Markdown would then read
# the next paragraph as part of the HTML block and show it as raw text.
_FOLD_OPEN_RE = re.compile(
    r"^<!--\s*fold:\s*(" + "|".join(FOLD_TYPES) + r")\s+(\(open\)\s+)?(.+?)\s*-->[ \t]*$", re.M)
```

<div class="wp-legend">
<span><svg viewBox="0 0 40 20" aria-hidden="true"><rect x="2" y="3" width="36" height="14" rx="3"/></svg>a box is a named component</span>
<span><svg viewBox="0 0 40 20" aria-hidden="true"><path d="M2 10h30M28 5l7 5-7 5"/></svg>a solid edge is ownership, a call or data flow</span>
<span><svg viewBox="0 0 40 20" aria-hidden="true"><path class="wp-dash" d="M2 10h30"/><path d="M28 5l7 5-7 5"/></svg>a dashed edge is a documented optional path</span>
</div>
<figcaption><b>Figure 5.</b> A real excerpt from the kit's builder, where the four fold kinds of <a href="#fig-story">Figure 2</a> and the open marker are defined, and the shared meanings of a code diagram. The excerpt is checked against <code>tooling/build.py</code> on every lint.</figcaption>
</figure>

Code on a page can go stale silently: the file changes and the excerpt does not. Idealized pseudocode shown as an excerpt is worse, because it looks verified. [Figure 5](#fig-excerpt) is the remedy at work: eight real lines, usually a signature and 3–10 decisive ones, tagged with their source range so lint fails if they drift, shown with the shared chrome: the real line numbers, a source chip, a language badge and a copy button. A snippet earns its place only when it explains a seam or a difficult contract better than prose, here the exact fold kinds the builder accepts.

Diagrams come from data or explicit local source and pass an overflow and collision check. Their parts keep the meanings in the legend of Figure 5 on every page, with a legend and a named source in the caption. Numbered sequence steps, mode views over common data and generated quantitative SVGs are useful patterns.

<!-- fold: detail Interactive diagram controls not yet built -->

Pan, fullscreen and annotation controls exist and may be used. Edge highlighting, drill-down and semantic zoom are only planned, so no page describes them as working. If one is built, drill-down with a breadcrumb suits independent child diagrams, and semantic zoom suits a diagram whose context must stay visible.

<!-- /fold -->

Full guide: [code and diagrams](code-excerpts.html#code-and-diagrams).

</section>
