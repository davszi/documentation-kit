+++
title = "Discuss, build, record"
brand_sub = "record · page · chapter · the path of work"
description = "What a record, a page and a chapter are, and the one path every piece of work takes: discussion, the person's yes, the build, the record before the page, and the extra gates of an experiment."
components = ["toc", "nav", "filelinks"]
page_css = ["build-sheet.css", "../site/assets/kit-story.css"]
toc = [["Three words", "#three-words"], ["The path", "#the-path"], ["Discuss", "#discuss"], ["The yes", "#the-yes"], ["Build and close", "#build-record-close"], ["Experiments", "#experiments"]]
page_only = "Explains how work runs under the kit; its records are the rule files in rules/."
+++

# Discuss, build, record

<section class="card" id="three-words">

## A record is for agents, a page is for people, a chapter is one claim

<p class="bs-lead">The rules use three words for three different things: the record an agent is routed to, the page that explains it to a person, and the chapters that page is made of.</p>

<figure id="fig-three-words">
<!-- include: fragments/kit-story/three-words.html -->
<figcaption><b>Figure 1.</b> One topic folder and its three words: the record an agent follows, the page a person reads, and one of the page's chapters. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 1](#fig-three-words) puts the three words in one folder. A **record** is the Markdown document an agent is routed to: a topic record, a guide, a plan or a log. The agent that did the work writes it first, and it keeps the exact wording an agent must find again ([writing records](records.html)).

A **page** is a page for people: a topic's `index.md`. It explains its record in its own words, leads with the conclusion and shows a figure. It never adds a rule, number or limit that its record lacks; when the two disagree, the record decides ([rendered pages are for people](documentation-system.html#rendered-pages-are-for-people-records-stay-markdown)). A Markdown file that the site shows whole is a [registered source page](authoring.html#registered-source-pages): it stays a record, and editing it is editing a record ([record first, page on request](documentation-system.html#record-first-page-on-request)).

A **chapter** is one `##` section of a page, or a `section.card` when the author wants control over its contents, and it carries one claim ([page design](page-design.html#page-design)); [the reader](build-a-site.html#the-reader) on Build a site shows how it is drawn. Its title states the takeaway, a one-sentence lead states the claim before the evidence, and it carries a visual block of its own ([page design](page-design.html#page-design)). A chapter with nothing of its own to claim merges into the chapter that owns its subject.

</section>

<section class="card" id="the-path">

<!-- slide -->
<style>
/* Local to this face: the path across the canvas; a tall drawing replaces it below 720 px. */
.slide-main.fx-path {justify-content:flex-start!important;gap:0!important;}
.fx-path > figure {flex:1 1 0!important;min-height:0!important;display:flex!important;flex-direction:column!important;gap:.4cqi!important;margin:0!important;}
.fx-path svg {display:block!important;width:100%!important;}
.fx-path svg.fx-wide {flex:1 1 0!important;min-height:0!important;height:100%!important;}
.fx-path svg.fx-tall {display:none!important;}
.fx-path figcaption {font:1cqi/1.3 "IBM Plex Mono",monospace!important;color:var(--sf-dim)!important;text-align:right!important;}
@container (max-width: 719.98px) {
  .fx-path > figure {flex:none!important;}
  .fx-path svg.fx-wide {display:none!important;}
  .fx-path svg.fx-tall {display:block!important;height:auto!important;}
  .fx-path figcaption {font-size:12px!important;text-align:left!important;}
}
</style>
<p class="slide-eyebrow">Discuss, build, record</p>
<p class="slide-title">Every piece of work takes one path: the yes before the build, the record before the page</p>
<div class="slide-main fx-path">
<figure>
<svg class="inline-fig fx-wide" viewBox="0 0 1200 500" role="img" aria-label="Six steps on one line. An optional open item, then the discussion, then the person's yes, which is the gate: nothing is built before it. Then the build, then the record first and the page after it, then landing and closing the open item. Below, the first three steps carry the claim that nothing is built before the yes; the last three carry the claim that the record lands before any page.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<text x="502" y="34" font-size="19" fill="#39d2c0" font-weight="600" text-anchor="middle">nothing is built before this</text>
<path d="M502 44V62" stroke="#39d2c0" stroke-width="3"/>
<path d="M60 112H1140" stroke="#2f3b4a" stroke-width="4"/>
<path d="M502 112H1140" stroke="#bc8cff" stroke-width="4" stroke-opacity=".55"/>
<circle cx="110" cy="112" r="30" fill="#0d1117" stroke="#7d8896" stroke-width="3" stroke-dasharray="7 6"/>
<circle cx="306" cy="112" r="30" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="502" cy="112" r="50" fill="#39d2c0" fill-opacity=".14"/>
<circle cx="502" cy="112" r="36" fill="#39d2c0"/>
<circle cx="698" cy="112" r="30" fill="#0d1117" stroke="#ffa657" stroke-width="3"/>
<circle cx="894" cy="112" r="30" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="1090" cy="112" r="30" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<g font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="19" font-weight="600" text-anchor="middle">
<text x="110" y="119" fill="#7d8896">01</text><text x="306" y="119" fill="#bc8cff">02</text><text x="502" y="120" fill="#0d1117" font-size="22">03</text>
<text x="698" y="119" fill="#ffa657">04</text><text x="894" y="119" fill="#bc8cff">05</text><text x="1090" y="119" fill="#bc8cff">06</text>
</g>
<g font-size="24" font-weight="600" fill="#e6edf3" text-anchor="middle">
<text x="110" y="196" fill="#a9b4c2">Open item</text><text x="306" y="196">Discuss</text><text x="502" y="196" fill="#39d2c0">The yes</text>
<text x="698" y="196">Build</text><text x="894" y="196">Record first</text><text x="1090" y="196">Land, close</text>
</g>
<g font-size="17" fill="#a9b4c2" text-anchor="middle">
<text x="110" y="226">optional, when work</text><text x="110" y="249">is owed or will pause</text>
<text x="306" y="226">chat first; a page</text><text x="306" y="249">when the topic is hard</text>
<text x="502" y="226">in words; silence</text><text x="502" y="249">is not a yes</text>
<text x="698" y="226">code, checks, fixes</text><text x="698" y="249">and documentation</text>
<text x="894" y="226">then the page, which</text><text x="894" y="249">follows its record</text>
<text x="1090" y="226">worklog entry;</text><text x="1090" y="249">open line deleted</text>
</g>
<path d="M70 300V288H542V300" fill="none" stroke="#39d2c0" stroke-width="2.5"/>
<path d="M658 300V288H1130V300" fill="none" stroke="#bc8cff" stroke-width="2.5"/>
<text x="70" y="344" font-size="16" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">BEFORE THE BUILD</text>
<text x="70" y="390" font-size="32" fill="#39d2c0" font-weight="600">Nothing is built before the yes</text>
<text x="70" y="428" font-size="20" fill="#a9b4c2">A proposal stays a proposal until</text>
<text x="70" y="456" font-size="20" fill="#a9b4c2">the person accepts it in words.</text>
<text x="658" y="344" font-size="16" fill="#7d8896" font-weight="600" letter-spacing="2" font-family="'IBM Plex Mono',ui-monospace,monospace">AFTER THE BUILD</text>
<text x="658" y="390" font-size="32" fill="#e6edf3" font-weight="600">The record lands before any page</text>
<text x="658" y="428" font-size="20" fill="#a9b4c2">An existing page follows it in the same</text>
<text x="658" y="456" font-size="20" fill="#a9b4c2">deliverable; a new page waits for a request.</text>
</g>
</svg>
<svg class="inline-fig fx-tall" viewBox="0 0 340 830" role="img" aria-label="Six steps from top to bottom: an optional open item, the discussion, the person's yes as the gate, the build, the record first and then the page, landing and closing. Nothing is built before the yes, and the record lands before any page.">
<g font-family="'IBM Plex Sans',system-ui,sans-serif">
<path d="M30 30V500" stroke="#2f3b4a" stroke-width="3"/>
<path d="M30 220V500" stroke="#bc8cff" stroke-width="3" stroke-opacity=".55"/>
<circle cx="30" cy="40" r="20" fill="#0d1117" stroke="#7d8896" stroke-width="2.5" stroke-dasharray="5 4"/>
<circle cx="30" cy="130" r="20" fill="#0d1117" stroke="#bc8cff" stroke-width="2.5"/>
<circle cx="30" cy="220" r="30" fill="#39d2c0" fill-opacity=".16"/><circle cx="30" cy="220" r="23" fill="#39d2c0"/>
<circle cx="30" cy="310" r="20" fill="#0d1117" stroke="#ffa657" stroke-width="2.5"/>
<circle cx="30" cy="400" r="20" fill="#0d1117" stroke="#bc8cff" stroke-width="2.5"/>
<circle cx="30" cy="490" r="20" fill="#0d1117" stroke="#bc8cff" stroke-width="2.5"/>
<g font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="14" font-weight="600" text-anchor="middle">
<text x="30" y="45" fill="#7d8896">01</text><text x="30" y="135" fill="#bc8cff">02</text><text x="30" y="225" fill="#0d1117">03</text>
<text x="30" y="315" fill="#ffa657">04</text><text x="30" y="405" fill="#bc8cff">05</text><text x="30" y="495" fill="#bc8cff">06</text>
</g>
<g font-size="20" font-weight="600" fill="#e6edf3">
<text x="68" y="38" fill="#a9b4c2">Open item</text><text x="68" y="128">Discuss</text><text x="68" y="214" fill="#39d2c0">The yes</text>
<text x="68" y="308">Build</text><text x="68" y="398">Record first</text><text x="68" y="488">Land, close</text>
</g>
<g font-size="15" fill="#a9b4c2">
<text x="68" y="60">optional; when work is owed</text>
<text x="68" y="150">chat first; a page when hard</text>
<text x="68" y="238">in words; silence is not a yes</text>
<text x="68" y="330">code, checks, fixes, docs</text>
<text x="68" y="420">then the page, which follows it</text>
<text x="68" y="510">worklog entry; open line deleted</text>
</g>
<path d="M0 560H340" stroke="#2f3b4a" stroke-width="1.5"/>
<text x="0" y="590" font-size="14" fill="#7d8896" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">BEFORE THE BUILD</text>
<text x="0" y="620" font-size="21" fill="#39d2c0" font-weight="600">Nothing is built before the yes</text>
<text x="0" y="646" font-size="15" fill="#a9b4c2">A proposal stays a proposal until</text>
<text x="0" y="668" font-size="15" fill="#a9b4c2">the person accepts it in words.</text>
<text x="0" y="712" font-size="14" fill="#7d8896" font-weight="600" letter-spacing="1.5" font-family="'IBM Plex Mono',ui-monospace,monospace">AFTER THE BUILD</text>
<text x="0" y="742" font-size="21" fill="#e6edf3" font-weight="600">The record lands before any page</text>
<text x="0" y="768" font-size="15" fill="#a9b4c2">An existing page follows it; a new</text>
<text x="0" y="790" font-size="15" fill="#a9b4c2">page waits for a request.</text>
</g>
</svg>
<figcaption>Figure 2 redrawn, with its two conclusions</figcaption>
</figure>
</div>
<p class="slide-scope">The path the rules describe · no measured results</p>
<!-- /slide -->

## Every piece of work takes the same path, from the first discussion to a closed open item

<p class="bs-lead">A feature, an experiment or a change of direction is discussed first, built only after the person's yes, and lands with its record before any page.</p>

<figure id="fig-path">
<!-- include: fragments/kit-story/path.html -->
<figcaption><b>Figure 2.</b> The path of work. Dashed: optional. The filled step is the gate; nothing is built before it. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 2](#fig-path) shows the path. Read it as two halves around the gate. Before it, nothing is built: a proposal stays a proposal until the person accepts it in words. After it, the record lands before any page. An existing page follows its record in the same deliverable; a new page waits until a person asks for one. Only the open item is optional. Open one when work is owed but not started, or when it will pause; it ends when the work lands. When an assignment already fixes what to build, there is nothing left to discuss, and the work starts at the build.

| Step | What happens | Rule |
|---|---|---|
| Open item | One line in `OPEN.md` routes to the document that owns the work | [discussion before the work](delivery.html#discussion-before-the-work) |
| Discuss | Chat first; a proposal page when chat is not enough | [discussion before the work](delivery.html#discussion-before-the-work) |
| The yes | The person accepts the proposal in words; the agreement becomes the assignment | [discussion before the work](delivery.html#discussion-before-the-work), [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge) |
| Build | The owner completes the implementation, focused checks, routine fixes and documentation | [owner responsibility](delivery.html#owner-responsibility), [deliverables and validation](git.html#deliverables-and-validation) |
| Record, then page | The agent that did the work writes the record; pages follow it | [record first, page on request](documentation-system.html#record-first-page-on-request) |
| Land and close | The worklog records the landing; the open line and a finished plan are deleted | [from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge), [rules for changes](documentation-system.html#rules-for-changes-and-chronology) |

</section>

<section class="card" id="discuss">

## Discussion starts in chat; a page grows only when the topic is hard

<p class="bs-lead">Chat is the main channel. When chat stops being enough, the agent offers a page and builds it when the person asks.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">always</span><h3>Chat first</h3><p>Explain there first, and lead with what the person has to decide.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">when chat is not enough</span><h3>A page for a hard topic</h3><p>A mechanism, a geometry or options to compare side by side. The agent offers the page, builds it when asked and extends it as the discussion moves.</p></div>
<div class="bs-check"><span class="bs-badge bs-off">while no record exists</span><h3>Marked as a proposal</h3><p>The page says at its top that it is a proposal and declares <code>page_only = "proposal under discussion"</code>.</p></div>
</div>

A feature, an experiment or a change of direction starts with a discussion between the person and the agent, unless an assignment already fixes what to build. The page that may grow during it is the one page that comes before its record: there is no record yet, because nothing has been agreed. [Record first, page on request](documentation-system.html#record-first-page-on-request) names this exception and points to [discussion before the work](delivery.html#discussion-before-the-work), which holds the rule.

</section>

<section class="card" id="the-yes">

## Nothing is agreed until the person says yes

<p class="bs-lead">A proposal stays a proposal until the person accepts it in words. After the yes, the agreement is the assignment, written down as far as the work needs.</p>

<figure id="fig-yes">
<div class="ks-yes" role="img" aria-label="On the left, three things that are not a yes: silence, continued discussion, and moving the proposal into another document. A blocked arrow leads from them to the gate. The gate is the person's yes, given in words. From the gate the way forks. A change that one session finishes needs no more than the chat, and its record follows the work. Work that outlives the chat, with a second session, a second owner or an expensive run, has its deliverable, scope and completion condition written into its open item or plan before building starts.">
<div class="ks-yes-grid">
<div class="ks-yes-col"><span class="ks-yes-label">Not a yes</span><ul class="ks-not"><li>silence</li><li>continued discussion</li><li>moving the proposal into another document</li></ul></div>
<div class="ks-to is-blocked" aria-hidden="true"></div>
<div class="ks-gate"><b>Yes</b><span>the person accepts the proposal in words</span></div>
<div class="ks-to" aria-hidden="true"></div>
<div class="ks-fork">
<div class="ks-branch is-chat"><span class="ks-yes-label">One session finishes it</span><b>The chat is enough</b><p>The record follows the work.</p></div>
<div class="ks-branch is-written"><span class="ks-yes-label">It outlives the chat</span><b>Written down before building</b><p>A second session, a second owner or an expensive run: deliverable, scope and completion condition go into its open item or plan.</p></div>
</div>
</div>
</div>
<figcaption><b>Figure 3.</b> What counts as a yes, and how much of the agreement is written down after it. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 3](#fig-yes) reads from left to right. The crossed-out arrow is the rule that keeps proposals honest: silence, continued discussion or moving a proposal into another document never turns it into an accepted requirement ([from open work to subject knowledge](documentation-system.html#from-open-work-to-subject-knowledge)). Only the person's words do.

The fork after the yes scales the paperwork to the work. A change that one session finishes needs no more than the chat. Work that outlives the chat gets its deliverable, scope and completion condition written into its open item or plan before building starts, so that a second session or a second owner starts from the agreement and not from a memory of it. For delegated or parallel work, [assigning work](delivery.html#assigning-work) lists what that note holds: also the required inputs, file or module ownership, the recipient and the return channel.

</section>

<section class="card" id="build-record-close">

## After the yes, the owner builds, writes the record and closes the open item

<p class="bs-lead">The owner finishes the routine work, the record lands before any page, and the open line is deleted once the work has landed.</p>

<figure id="fig-build-close">
<div class="bs-flow" role="img" aria-label="Step 1, build: the assigned owner completes the implementation, focused checks, routine fixes and associated documentation, and commits one logical deliverable. Step 2, record then page: the agent that did the work writes the record, what changed, what was measured and why; an existing page follows in the same deliverable after the record; a new page is made only when a person asks. Step 3, land and close: the worklog records the landing, the open line is deleted rather than ticked, and a finished plan is deleted with the person's approval. A change to the agreement goes back to the person for a decision instead of being built.">
<div class="bs-node bs-orange"><span class="bs-label">1 · The owner</span><b>Build</b><ul><li>implementation, focused checks, routine fixes</li><li>documentation and evidence that go with it</li><li>one logical deliverable per commit</li></ul></div>
<div class="bs-arrow"><span>lands</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Record first</span><b>Record, then page</b><ul><li>what changed, what was measured, why</li><li>an existing page follows, after the record</li><li>a new page only on a person's request</li></ul></div>
<div class="bs-arrow"><span>closes</span></div>
<div class="bs-node bs-teal"><span class="bs-label">3 · The open item ends</span><b>Land and close</b><ul><li>a worklog entry for the landing</li><li>the open line deleted, not ticked</li><li>a finished plan deleted, with approval</li></ul></div>
<div class="bs-back"><span>×</span> A change to the agreed goal, design, scope or acceptance goes back to the person for a decision; it is not built on the way.</div>
</div>
<figcaption><b>Figure 4.</b> From the build to the closed open item. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 4](#fig-build-close) covers the second half of the path. Routine work inside the agreed scope needs no further approval; the owner finishes it, checks included ([owner responsibility](delivery.html#owner-responsibility)). The crossed way back is what the owner does not decide alone: a change to the agreed goal, design, scope or acceptance requirements is escalated ([decisions and blockers](delivery.html#decisions-and-blockers)).

Each step has its own page with the reasons and examples: [Engineering](engineering-practices.html#delivery) for ownership, decisions and [commits](engineering-practices.html#git), and Records and documents for [the record written first](documentation-practices.html#record-first) and [finished work that moves to its subject](documentation-practices.html#open-to-topic).

</section>

<section class="card" id="experiments">

## An experiment takes the same path, with extra gates

<p class="bs-lead">Its design is discussed like any other work; its plan must hold more before it runs, and each attempt and its end leave more behind.</p>

| Step | What an experiment adds | Rule |
|---|---|---|
| Discuss | Agree the budget (time, compute, files) and when to change approach; ask before exceeding it or widening the question | [keep experiments small](experiment-workflow.html#keep-experiments-small) |
| Before it runs | State the question and its measured motivation, the kind, the decision it informs, the baseline, the budget and the stopping condition; a confirmatory investigation or a qualification also fixes its bar, tolerances, workload, analysis and what counts as failure or inconclusive | [required content](experiment-workflow.html#required-content) |
| Each attempt | Add a check only for a named gap; add one line with the running total; stop when the question is answered, the budget is reached or the approach cannot answer it | [evidence gap](experiment-verification.html#identify-the-evidence-gap), [show the total](experiment-workflow.html#show-the-total), [bound the question](experiment-workflow.html#start-from-evidence-and-bound-the-question) |
| Record | Report every attempt, failure and changed setting with its reason, and the verdict where one is due; track the run output before reporting completion; never lower a failed bar | [required content](experiment-workflow.html#required-content), [changes and failures](experiment-verification.html#respond-to-changes-and-failures) |
| After it | After every third finished experiment, a fresh agent reads the whole and changes nothing | [step back](experiment-workflow.html#step-back-across-experiments) |

The [delivery guide](delivery.html#discussion-before-the-work) says an experiment's design is discussed the same way as other work, and the experiment workflow adds what its plan must hold. The table lists only what differs; everything else on the path stays as above. The [Experiments page](experiments.html) explains each gate with its reason and an example.

</section>
