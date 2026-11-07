+++
title = "Reader tour"
brand = "Documentation kit"
brand_sub = "chapters · docking · layers · slides"
description = "A live tour of the chapter reader: chapters, docked navigation, pinned columns, reading layers, figures, comparisons and slides."
components = ["toc", "nav", "code", "filelinks", "lightbox", "carousel", "panel-switcher"]
page_css = ["build-sheet.css"]
math = true
toc = [["Chapters", "#move-through-chapters"], ["Dock and pin", "#dock-and-pin"], ["Reading layers", "#reading-layers"], ["Figures", "#figures"], ["Compare", "#compare"], ["Status and numbers", "#status-and-numbers"], ["Slides and print", "#slides-and-print"]]
+++

# Reader tour

<section class="card" id="move-through-chapters">

<!-- slide -->
<p class="slide-eyebrow">Reader tour</p>
<p class="slide-title">Every page is a row of chapters you can dock, pin and fold</p>
<p class="slide-lead">This page uses each reader feature once. Try it as you read: every chapter says what to press.</p>
<div class="slide-main"><div class="slide-row"><div class="slide-tile is-term"><h4>Move</h4><p>arrows or ← → keys · One, Two or All chapters</p></div><div class="slide-tile"><h4>Dock and pin</h4><p>dock the navigation · hold one chapter while the other moves</p></div><div class="slide-tile is-held"><span class="slide-tag">optional</span><h4>Go deeper</h4><p>Math, Experiments, Code and Alternatives layers</p></div></div></div>
<p class="slide-scope">A slide face: the 16:9 summary that opens a chapter and exports to a deck</p>
<!-- /slide -->

## Every page is a row of chapters you move through

<p class="bs-lead">One chapter fills the stage while its neighbours stay visible at the edges; each chapter remembers where you stopped.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Move</h3><p>Press <kbd>→</kbd> or use the arrows in the top bar. Come back with <kbd>←</kbd>: the chapter resumes at the same scroll position.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Jump</h3><p>The navigation lists this page's chapters under its entry. Choose one to go straight to it.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">try</span><h3>Change the layout</h3><p><b>One chapter</b>, <b>Two chapters</b> or <b>All chapters</b> in the top bar. All chapters reads the page as one long scroll.</p></div>
</div>

The card above the heading is a slide face. [Slides and print](#slides-and-print) shows how faces become a deck.

</section>

<section class="card" id="dock-and-pin">

## Dock the navigation and pin a chapter to keep it in view

<p class="bs-lead">Docking keeps the navigation beside the page; pinning holds one chapter still while the other column moves.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Navigation · <code>«</code> and <code>☰</code></span><h3>Dock the sidebar</h3><ol>
<li>On screens wider than 900 px the navigation starts docked beside the page. You keep reading, and chapter links keep it open.</li>
<li>Press <code>«</code> to hide it and <code>☰</code> to bring it back docked. Each page remembers your choice.</li>
<li>On a phone it opens over the page and closes after you choose a chapter.</li>
</ol></div>
<div class="bs-part bs-violet"><span class="bs-label">Two chapters · <code>⌖</code> on a column</span><h3>Pin a reference</h3><ol>
<li>Choose <b>Two chapters</b> in the top bar.</li>
<li>Press <code>⌖</code> on the left column's header. It turns purple and reads <b>Pinned</b>.</li>
<li>Press <kbd>→</kbd>: only the right column moves. Pin, then compare any chapter with this one.</li>
</ol></div>
</div>

<figure id="fig-pinning">
<div class="bs-flow n2" role="img" aria-label="In Two chapters, the left column is pinned and holds its chapter. The arrows move only the right, unpinned column through the other chapters.">
<div class="bs-node bs-violet"><span class="bs-label">Left column · pinned</span><b>Holds its chapter</b><ul><li>own scroll position</li><li>own layer buttons</li></ul></div>
<div class="bs-arrow"><span>→ moves</span></div>
<div class="bs-node bs-teal"><span class="bs-label">Right column · free</span><b>Steps through the rest</b><ul><li>arrows and keys move it alone</li><li>select it, then pick a chapter in the navigation</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> Pinning splits the page into a fixed reference and a moving reader. Press the pin again to release it.</figcaption>
</figure>

</section>

<section class="card" id="reading-layers">

## Depth stays folded until a reader asks for it

<p class="bs-lead">The story is always visible. Math, Experiments, Code and Alternatives are layers each column can open on its own.</p>

Use the layer buttons under this chapter's heading to open every fold of one kind, or open a single fold below. In Two chapters, each column keeps its own choice. In source, a layer is a typed fold such as `<!-- fold: math Title -->` … `<!-- /fold -->`.

<!-- fold: math How the progress bar counts -->

The bar under the site name shows the active chapter $k$ out of the page's $n$ chapters:

$$
\text{progress} = \frac{k}{n}, \qquad 1 \le k \le n
$$

On this page $n = 7$, so the fourth chapter fills $4/7$ of the bar.

<!-- /fold -->

<!-- fold: experiment What the site review checks on this page -->

`tests/own_site_review.cjs` opens this page at 1600 × 1000 and 390 × 844 with Chromium. It fails on a page error, horizontal page overflow or a missing chapter card. At 1600 px it also checks the steps in this tour: the navigation starts docked, `«` undocks it and `☰` docks it again; a pinned left column keeps its chapter while two arrow presses move the right one; the carousel shows one capture at a time. It checks the rendered page, not reading speed or comprehension.

<!-- /fold -->

<!-- fold: code The configuration that turns the reader on -->

These lines of the kit site's own configuration enable the reader for every page that does not opt out:

```toml source=docs/site/site.toml#L3-L7
title = "Documentation kit"
home_label = "Kit"
gh_repo = "https://github.com/davszi/documentation-kit"
gh_ref = "main"
chapter_reader = true
```

<!-- /fold -->

<!-- fold: dead-end Why the rule guides are not laid out like this page -->

The guides under `rules/` are also read as plain Markdown by agents, so they render as they are: one chapter per section, without figures written for the reader. Rewriting them as reader pages would put HTML into agent-facing rules; separate reader summaries would be a second copy that drifts. Only the site's own overview pages are written for the reader.

<!-- /fold -->

</section>

<section class="card" id="figures">

## Figures come from the page source and open full screen

<p class="bs-lead">Diagrams are HTML written in the page; images and SVG figures are tracked files the build packages and open full screen.</p>

<div class="bs-grid g2">
<figure id="fig-captures">
<div class="fig-carousel">
<img src="../../preview/desktop.png" alt="The starter guide's first chapter in the reader at 1600 by 1000 pixels: chapter tree on the left, the ownership flow in the active card, the next chapter at the right edge.">
<img src="../../preview/home.png" alt="The starter home page at 1600 by 1000 pixels with its hero and topic cards.">
</div>
<figcaption><b>Figure 2.</b> A carousel of the starter captures in <code>preview/</code> (2026-11-04). It advances by itself, pauses on hover and opens the visible capture in the lightbox.</figcaption>
</figure>
<div>
<div class="bs-part bs-orange"><span class="bs-label">Try</span><h3>Zoom and pan</h3><p>Click the visible capture. Scroll to zoom, drag to pan, double-click to reset, <kbd>Esc</kbd> to close. HTML diagrams such as <a href="#fig-pinning">Figure 1</a> stay in the page.</p></div>
<div class="bs-specs"><div><span class="bs-label">Images</span><b>Tracked only</b></div><div><span class="bs-label">Diagrams</span><b>HTML + labels</b></div></div>
<p>Every figure has a text alternative or <code>aria-label</code>. <a href="figures.html">Figures and access</a> owns the rules.</p>
</div>
</div>

</section>

<section class="card" id="compare">

## One switch compares two views of the same thing

<p class="bs-lead">The panel switcher shows one option at a time and keeps the others a click away; print and no-JavaScript reading show all of them.</p>

<div class="panel-switcher" data-panel-switcher data-panel-default="markdown">
<div class="panel-switcher-controls" role="group" aria-label="View of a rule">
<button type="button" data-panel-choice="markdown" aria-pressed="false" aria-controls="view-markdown">As agents read it</button>
<button type="button" data-panel-choice="page" aria-pressed="false" aria-controls="view-page">As this site renders it</button>
</div>
<div id="view-markdown" data-panel="markdown">

```markdown source=rules/experiments/workflow.md#L36-L38
- A **qualification** gives a pass, fail or inconclusive verdict on a named
  system, build or model: platform qualification, a benchmark contract, a
  parity check, model release evaluation.
```

</div>
<div id="view-page" data-panel="page">
<div class="bs-part bs-orange"><span class="bs-label">Rendered from the same lines</span><h3>Qualification</h3><p>A <b>qualification</b> gives a pass, fail or inconclusive verdict on a named system, build or model: platform qualification, a benchmark contract, a parity check, model release evaluation.</p><p><a href="experiment-workflow.html#choose-the-purpose">Open it in the guide</a></p></div>
</div>
</div>

The [panel switcher contract](panel-switcher.html) documents its markup.

</section>

<section class="card" id="status-and-numbers">

## Status and measured numbers have their own blocks

<p class="bs-lead">A status board holds one current state per item; headline numbers carry their scope.</p>

<div class="bs-stats">
<div><b>36</b><span>pages on this site</span></div>
<div><b>31</b><span>rendered straight from tracked Markdown</span></div>
<div><b>7</b><span>chapters on this page</span></div>
</div>

<div class="bs-board">
<div class="bs-row"><span class="bs-state bs-ok">Done</span><b>Reader on every page but home</b><span>Chapter cards, Two chapters, pinning and layers.</span></div>
<div class="bs-row"><span class="bs-state bs-ok">Passed</span><b>Local site review</b><span>Chromium at 1600 and 390 px; see the Experiments layer in <a href="#reading-layers">Reading layers</a>.</span></div>
<div class="bs-row"><span class="bs-state bs-wait">Open</span><b>Hosting and audience</b><span>Not deployed; the destination is undecided. See <a href="website.html#open-decision-hosting-and-audience">the website record</a>.</span></div>
</div>

Counts are from this kit revision's build on 2026-11-07; the board is the [website record](website.html)'s state, not a second status owner.

</section>

<section class="card" id="slides-and-print">

## Slide faces become a deck, and print keeps everything

<p class="bs-lead">One command collects chapter slide faces into a presentable deck; printing a page opens every layer and panel.</p>

```bash
python .docs-kit/docsite.py slides --project . --select reader-tour --out reader-tour
```

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Present</span><h3>Decks from faces</h3><p>Repeat <code>--select</code> to combine pages; <code>page#chapter</code> picks single chapters. Each face stays tied to the chapter that backs its claims. See <a href="authoring.html#slide-faces-and-decks">slide faces and decks</a>.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Print · no JavaScript</span><h3>Nothing stays hidden</h3><p>Print shows every chapter, open folds and every switcher panel. Without JavaScript, chapters read top to bottom and folds open natively.</p></div>
</div>

</section>
