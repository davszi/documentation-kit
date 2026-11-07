+++
title = "Documentation and writing"
brand = "Documentation kit"
brand_sub = "homes · pages · evidence · figures"
description = "Where each kind of documentation belongs and how the kit's writing guides shape pages, explanations, evidence, figures, math and code."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Guide per task", "#routes"], ["One home", "#homes"], ["Records and pages", "#records-and-pages"], ["Page design", "#page-design"], ["Explanations", "#explanations"], ["Evidence", "#evidence"], ["Figures", "#figures"], ["Math and code", "#math-and-code"]]
+++

# Documentation and writing

<section class="card" id="routes">

## Each guide owns one kind of documentation decision

<p class="bs-lead">The documentation system decides where content lives; six focused writing guides decide how a page presents it.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Documentation and writing guides by task">

| Before… | Read… | It covers |
|---|---|---|
| Creating, moving or retiring a document | [Documentation system](documentation-system.html) | Canonical homes, the path from open work to topic, evidence identity, deletion and worklog rules, publishing, agent entrypoints |
| Laying out a rendered page | [Page design](page-design.html) | Section purpose, takeaway titles, build-sheet blocks, slide faces, review |
| Writing an explanation | [Explanations](explanations.html) | Story order, typed folds, naming, honest claims |
| Quoting a measured number | [Evidence](evidence.html) | Required provenance, staleness, number ledgers, run visuals, experiment records |
| Adding a figure or comparison | [Figures](figures.html) | The visual completion gate, captions and references, comparisons, interaction and access |
| Writing mathematics | [Math](math.html) | Definitions, derivations, KaTeX use, verification of analytic claims |
| Showing code or a code diagram | [Code excerpts](code-excerpts.html) | Real excerpts with source metadata, shared diagram semantics |

</div>

The guides are records for agents and own the complete rules. This page explains them for people and links back to each one.

</section>

<section class="card" id="homes">

## Every fact has one home, and finished work settles in its subject

<p class="bs-lead">Other documents link to the owner; as work matures, each kind of content moves to the record that owns it.</p>

[Figure 1](#fig-homes) follows content from open work to subject knowledge. Unfinished work stays with its open owner. Evidence stays with the work that produced it. Established behavior moves to the topic, and the worklog records the landing.

<figure id="fig-homes">
<div class="bs-flow" role="img" aria-label="Open work in a named plan, routed from OPEN.md, is investigated in producing work that keeps its evidence. Established findings move to the owning topic record. A closed record supports current knowledge through a link and never becomes a second knowledge home.">
<div class="bs-node bs-orange"><span class="bs-label">Open owner</span><b>Unfinished work</b><ul><li>Named plan or decision record</li><li>Unresolved choices and owners</li><li>Prospective acceptance</li><li>One-line route in <code>OPEN.md</code></li></ul></div>
<div class="bs-arrow"><span>investigate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Producing work</span><b>Protocol and evidence</b><ul><li>Inputs and raw results</li><li>Failures and source pins</li><li>Reproduction instructions</li></ul></div>
<div class="bs-arrow"><span>establish</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Owning topic</span><b>Current knowledge</b><ul><li>Established behavior</li><li>Accepted requirements</li><li>Durable rationale</li></ul></div>
<div class="bs-back"><span>×</span> A closed record supports current knowledge through a link. It never becomes a second current knowledge home.</div>
</div>
<figcaption><b>Figure 1.</b> Promotion moves knowledge to its subject; the producing evidence stays where it was made. This source-authored diagram illustrates the rule and contains no measured results.</figcaption>
</figure>

Proposals stay proposals until someone explicitly accepts them. Nothing is deleted without user approval.

Full guide: [documentation system](documentation-system.html), especially [canonical homes](documentation-system.html#canonical-homes) and [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge).

</section>

<section class="card" id="records-and-pages">

## Records preserve the contract; pages explain what it means

<p class="bs-lead">Agents work from plain Markdown records, and a rendered page exists only when a person has something to learn or act on.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Record for agents</span><h3>Plain Markdown, exact detail</h3><ul><li>Headings, tables, lists, exact file references and evidence links</li><li>No layout HTML; a needed diagram lives in a separate linked file</li><li>Holds contracts, handoff and resume state, readiness boards, bookkeeping and long chronology</li><li>Keeps anchors that other documents reference</li></ul></div>
<div class="bs-part bs-violet"><span class="bs-label">Page for people</span><h3>Conclusions, figures and next decisions</h3><ul><li>Current conclusions and accepted specifications</li><li>Demonstrated behavior with its evidence scope</li><li>Useful figures and the decisions needed next</li><li>Links to records instead of reproducing them</li></ul></div>
</div>

Agents find the records through one thin router in `AGENTS.md`. It names the project context and the rules every task needs, and routes the rest by action; Claude Code imports it with a bare `@AGENTS.md` line in `CLAUDE.md`. Reading a route grants no permission to execute or publish.

Full guide: [rendered pages and records](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown) and [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

</section>

<section class="card" id="page-design">

## A page states its takeaway first, then shows the evidence

<p class="bs-lead">Each section has one purpose, a title that states its takeaway and a one-sentence claim before the evidence.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">section</span><h3>One purpose</h3><p>Answer a question, show a construction or compare alternatives. Split when the purpose changes; merge thin sections.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">heading</span><h3>Takeaway titles</h3><p>Titles state the takeaway. A one-sentence <code>bs-lead</code> states the claim before the evidence.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">figure</span><h3>Mechanism first</h3><p>Place the figure after the heading or takeaway, then the prose that interprets it. A table or equation may lead when it carries the explanation.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">card</span><h3>About half a card</h3><p>At 1600 × 1000 a chapter fills about half a card. Merge a thin chapter rather than padding it, and fill every row.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">voice</span><h3>Formal and plain</h3><p>Registry tags, bug-hunt narratives, file-routing tables and debugging chronology stay off rendered pages.</p></div>
</div>

A chapter may open with one 16:9 slide face. No fact exists only on a slide: the chapter below states every number and claim with its evidence.

Full guide: [page design](page-design.html), especially [build-sheet pages](page-design.html#build-sheet-pages) and [slide faces](page-design.html#slide-faces).

</section>

<section class="card" id="explanations">

## Keep one visible story and put optional depth in typed folds

<p class="bs-lead">A reader can follow the complete argument and its verdict with every fold closed.</p>

[Figure 2](#fig-story) shows the two reading layers. The Story carries the argument. Folds deepen it but never hold a separate required argument.

<figure id="fig-story">
<div class="bs-flow n2" role="img" aria-label="The visible Story holds the complete argument, narrative figures, comparison cases and verdict. Typed folds for math, experiment, code and dead-end add optional depth. Folds never hide a separate required argument.">
<div class="bs-node bs-teal"><span class="bs-label">Always visible</span><b>The Story</b><ul><li>Purpose and prerequisites</li><li>Mechanism and examples</li><li>Evidence and limits</li><li>Comparison cases and verdict</li></ul></div>
<div class="bs-arrow"><span>go deeper</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Optional</span><b>Typed folds</b><ul><li><code>math</code> derivations</li><li><code>experiment</code> detail</li><li><code>code</code> excerpts</li><li><code>dead-end</code>, shown as Alternatives</li></ul></div>
<div class="bs-back"><span>×</span> A fold never hides a separate required argument.</div>
</div>
<figcaption><b>Figure 2.</b> Optional depth branches from a complete visible argument. This source-authored diagram illustrates the rule and contains no measured results.</figcaption>
</figure>

Use one term per object everywhere. Label accepted future behavior, implemented behavior, CPU checks and runtime observations separately. Say "not measured" plainly; never manufacture an estimate.

Full guide: [explanations](explanations.html), especially [story and reading layers](explanations.html#story-and-reading-layers) and [naming and honest claims](explanations.html#naming-and-honest-claims).

</section>

<section class="card" id="evidence">

## A measured number is current only with its full provenance

<p class="bs-lead">Quote a number as current evidence only when its source and conditions are recorded and still hold.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Measured claim</span><h3>Record how it was produced</h3><ul><li>Source commit and exact reproduction command</li><li>Runtime or environment, and workload</li><li>Units, baseline, method and scope</li><li>Links to the raw result and its limitations</li></ul></div>
<div class="bs-part bs-muted"><span class="bs-label">Not a measurement</span><h3>Cite and label the source</h3><ul><li>Configuration values</li><li>Derivations</li><li>Design arithmetic</li></ul></div>
</div>

When code, input data, method, workload or runtime conditions change, rerun before quoting the claim as current. A historical label does not qualify changed inputs. A redesign that restates numbers records each number's source in a ledger.

Full guide: [evidence](evidence.html), especially [numbers and staleness](evidence.html#numbers-and-staleness) and [run visuals and experiment lifecycle](evidence.html#run-visuals-and-experiment-lifecycle). Experiment kinds and required content live in the [experiment workflow](experiment-workflow.html).

</section>

<section class="card" id="figures">

## Every mechanism, spatial claim and measurement needs a visual

<p class="bs-lead">A section is not done until a mechanism has a diagram, a spatial claim a picture and a measured claim a plot or table.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">anchor</span><h3>Number and caption</h3><p>A stable HTML anchor and a visible numbered caption, unique and in reading order.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">prose</span><h3>Prose reference</h3><p>Text links the number to the anchor and says what to notice. A caption or alt text alone is not enough.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">links</span><h3>Clickable references</h3><p>Every reference is a link, including in table cells, panel labels and other captions.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">source</span><h3>Provenance and alt text</h3><p>Name the source and give useful alt text. Generated figures record generator, revision, inputs, date and output hash.</p></div>
</div>

Use diagrams for structure, ownership, flow or sequence; tables for exact lookup; plots for patterns, variation or trade-offs. Nothing may overflow the page at any viewport.

Full guide: [figures](figures.html), especially [figures and comparisons](figures.html#figures-and-comparisons) and [interaction and access](figures.html#interaction-and-access).

</section>

<section class="card" id="math-and-code">

## Derive from what the reader knows, and excerpt only real code

<p class="bs-lead">Mathematics builds on a construction the reader already has; a code excerpt shows real repository lines that drift checks can verify.</p>

<div class="bs-grid g2">
<div class="bs-part bs-blue"><span class="bs-label">Mathematics</span><h3>Define, then derive</h3><ul><li>Define symbols, units, terms and prerequisites before use</li><li>Show intermediate reasoning and state structural assumptions</li><li>A non-obvious formula needs a derivation or a precise citation</li><li>Analytic derivative claims name their numerical tolerance and executable self-test</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">Code excerpts</span><h3>Real lines, linked source</h3><ul><li>Use a snippet only when it explains a seam or hard contract better than prose</li><li>Usually a signature and 3–10 decisive lines; link the rest</li><li>Source metadata lets drift checks verify content and line numbers</li><li>Never present idealized pseudocode as a verified excerpt</li></ul></div>
</div>

In code diagrams, boxes are named components, edges mean ownership, calls or data flow, and dashed lines mean a documented optional path.

Full guides: [mathematical explanation](math.html#mathematical-explanation) and [code and diagrams](code-excerpts.html#code-and-diagrams).

</section>
