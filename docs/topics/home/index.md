+++
title = "Documentation kit"
slug = "index"
brand_sub = "shared rules · the path of work · site toolchain"
reader = false
components = ["nav", "filelinks", "lightbox"]
page_css = ["build-sheet.css", "home.css", "../site/assets/kit-story.css", "home/home-story.css"]
toc = []
+++

<div class="home">
<header class="home-hero">
<div class="home-hero-text">
<p class="home-eyebrow">Documentation kit</p>
<h1>Rules that people and agents read right before they act</h1>
<p>One pinned Git submodule gives a project shared rules, a chapter reader and a site toolchain. The project's <code>AGENTS.md</code> names the rule to read before each kind of action, and every piece of work follows one path: discuss, build, record.</p>
<div class="home-cta">
<a href="discuss-build-record.html">Discuss, build, record</a>
<a class="alt" href="getting-started.html">Get started</a>
<a class="alt" href="build-a-site.html">Build a site</a>
<a class="alt" href="https://github.com/davszi/documentation-kit">GitHub repository ↗</a>
</div>
<nav class="hs-jump" aria-label="The story on this page">
<a href="#what-the-kit-provides">One kit</a><a href="#how-it-works">Read before acting</a><a href="#three-words">Three words</a><a href="#the-path">The path</a><a href="#finished-page">A finished page</a><a href="#practice-areas">Practices</a><a href="#routes">Every page</a>
</nav>
</div>
<!-- unreferenced figure: the hero's picture of three router rows illustrates the headline; Figure 2 below explains the mechanism -->
<figure class="home-router" aria-label="Three rows of a project's AGENTS.md: before writing or changing a record, read rules/records.md; before designing an experiment, read rules/experiments/workflow.md; before handing off work, read rules/engineering/handoffs.md.">
<div class="home-router-bar"><span></span><span></span><span></span><code>AGENTS.md</code></div>
<div class="home-router-head"><span>Before…</span><span>Read…</span></div>
<div class="home-router-row" style="--g:#6ee7c5"><span>Writing or changing a record</span><code>rules/records.md</code></div>
<div class="home-router-row" style="--g:#b69cff"><span>Designing an experiment</span><code>rules/experiments/workflow.md</code></div>
<div class="home-router-row" style="--g:#ffb35c"><span>Handing off work</span><code>rules/engineering/handoffs.md</code></div>
<figcaption>Each row pairs a kit guide with your own records. The <a href="../../examples/starter/AGENTS.md.tmpl">starter's router</a> has every row.</figcaption>
</figure>
</header>

<section class="hs-sec" id="what-the-kit-provides" style="--g:#bc8cff" aria-labelledby="what-the-kit-provides-title">
<div class="hs-text">
<p class="hs-kicker">One kit, many projects</p>
<h2 id="what-the-kit-provides-title">A rule fixed once in the kit reaches each project that moves its pin</h2>
<p><a href="#fig-kit-pin">Figure 1</a> shows two projects that hold the kit as a <code>.docs-kit</code> submodule, each pinned to the revision it chose. A shared rule has one home, the kit, while each project keeps its own records, pages, commands and exceptions.</p>
<a class="hs-more" href="readme.html#ownership">Which paths belong to whom →</a>
</div>
<figure id="fig-kit-pin">
<svg class="inline-fig" viewBox="0 0 600 400" role="img" aria-label="Two projects share one kit. The kit repository is a line of revisions; a rule fix lands there once. Each project holds the kit as a .docs-kit submodule pinned to the revision it chose, next to its own records, pages, commands and exceptions. Project A is still pinned to an older revision; project B moved its pin and has the fix.">
<text x="8" y="30" font-size="25" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">KIT REPOSITORY</text>
<path d="M20 70H584" stroke="#bc8cff" stroke-width="3" opacity=".55"/>
<circle cx="60" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="170" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="280" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<circle cx="390" cy="70" r="12" fill="#39d2c0" stroke="#39d2c0" stroke-width="3"/>
<circle cx="520" cy="70" r="9" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/>
<text x="390" y="110" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">rule fix lands once</text>
<rect x="8" y="130" width="286" height="266" rx="16" fill="none" stroke="#2f3b4a" stroke-width="2"/>
<text x="24" y="162" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">project A</text>
<rect x="24" y="176" width="254" height="84" rx="10" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="40" y="210" font-size="28" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="40" y="246" font-size="25" fill="#a9b4c2" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">older pin</text>
<rect x="24" y="272" width="254" height="110" rx="10" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="40" y="304" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">own records,</text>
<text x="40" y="333" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pages, commands,</text>
<text x="40" y="362" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">exceptions</text>
<path d="M170 82V176" stroke="#bc8cff" stroke-width="3" stroke-dasharray="7 6"/>
<circle cx="170" cy="176" r="6" fill="#bc8cff"/>
<rect x="306" y="130" width="286" height="266" rx="16" fill="none" stroke="#2f3b4a" stroke-width="2"/>
<text x="322" y="162" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">project B</text>
<rect x="322" y="176" width="254" height="84" rx="10" fill="#17142a" stroke="#bc8cff" stroke-width="2.5"/>
<text x="338" y="210" font-size="28" fill="#bc8cff" text-anchor="start" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">.docs-kit/</text>
<text x="338" y="246" font-size="25" fill="#39d2c0" text-anchor="start" font-weight="600" font-family="'IBM Plex Sans',system-ui,sans-serif">moved its pin</text>
<rect x="322" y="272" width="254" height="110" rx="10" fill="#0f1d22" stroke="#39d2c0" stroke-width="2.5"/>
<text x="338" y="304" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">own records,</text>
<text x="338" y="333" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">pages, commands,</text>
<text x="338" y="362" font-size="25" fill="#e6edf3" text-anchor="start" font-weight="400" font-family="'IBM Plex Sans',system-ui,sans-serif">exceptions</text>
<path d="M520 82V176" stroke="#bc8cff" stroke-width="3" stroke-dasharray="7 6"/>
<circle cx="520" cy="176" r="6" fill="#bc8cff"/>
<circle cx="262" cy="24" r="22" fill="#0d1117" stroke="#bc8cff" stroke-width="3"/><text x="262" y="33" font-size="25" fill="#bc8cff" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">01</text>
<circle cx="274" cy="278" r="22" fill="#0d1117" stroke="#39d2c0" stroke-width="3"/><text x="274" y="287" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">02</text>
<circle cx="574" cy="182" r="22" fill="#0d1117" stroke="#39d2c0" stroke-width="3"/><text x="574" y="191" font-size="25" fill="#39d2c0" text-anchor="middle" font-weight="600" font-family="'IBM Plex Mono',ui-monospace,monospace">03</text>
</svg>
<figcaption><b>Figure 1.</b> Two projects share one kit. A rule fix lands in the kit once; each project picks it up when it moves its pin. The numbers mark the shared kit (01), the project's own content (02) and the pin each project moves (03). This illustrative SVG diagram is authored in the page source and contains no measured results.</figcaption>
</figure>
</section>

<section class="hs-sec is-wide" id="how-it-works" style="--g:#6ee7c5" aria-labelledby="how-it-works-title">
<div class="hs-text">
<p class="hs-kicker">Read before acting</p>
<h2 id="how-it-works-title">Each rule is read right before the action it governs</h2>
<p><a href="#fig-routing">Figure 2</a> is the whole mechanism: one router row joins a shared rule with the project's own record for one kind of action. The row fires on the action, not the topic, so an agent about to commit reads the Git guide and not every guide; <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a> has the rule.</p>
</div>
<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit. Step 2: in AGENTS.md, add a row for each kind of action that names the kit guide and the project's own record, for example staging or committing with rules/engineering/git.md and the project's validation records. Step 3: before that action, a contributor or agent reads both, then acts.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>.docs-kit</code> submodule</li><li>its commit is your version</li></ul></div>
<div class="bs-arrow"><span>route</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · <code>AGENTS.md</code></span><b>One row per action</b><ul><li>before committing…</li><li>…read <code>rules/engineering/git.md</code> and your validation records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read both, then act</b><ul><li>shared rule + project specifics</li><li>nothing is copied</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> Adoption is a pointer, not a copy: one router row joins a shared rule with the project's own specifics. The <a href="../../examples/starter/AGENTS.md.tmpl">starter's router</a> has every row. This diagram contains no measured results.</figcaption>
</figure>
</section>

<section class="hs-sec is-flip" id="three-words" style="--g:#bc8cff" aria-labelledby="three-words-title">
<div class="hs-text">
<p class="hs-kicker">Three words</p>
<h2 id="three-words-title">A record is for agents, a page is for people, a chapter is one claim</h2>
<p><a href="#fig-three-words">Figure 3</a> puts the three words in one topic folder. The page explains its record in its own words; when the two disagree, the record decides.</p>
<a class="hs-more" href="discuss-build-record.html#three-words">The three words in full →</a>
</div>
<figure id="fig-three-words">
<!-- include: fragments/kit-story/three-words.html -->
<figcaption><b>Figure 3.</b> One topic folder: the record an agent follows, the page a person reads, and one of the page's chapters. This illustrative diagram contains no measured results.</figcaption>
</figure>
</section>

<section class="hs-sec is-wide" id="the-path" style="--g:#39d2c0" aria-labelledby="the-path-title">
<div class="hs-text">
<p class="hs-kicker">Discuss, build, record</p>
<h2 id="the-path-title">Every piece of work takes one path: the yes before the build, the record before the page</h2>
<p><a href="#fig-path">Figure 4</a> follows a piece of work from the first discussion to the landed change. Nothing is built before the person's yes, and the record lands before any page. <a class="hs-more" href="discuss-build-record.html#the-path">Each step and its rule →</a></p>
</div>
<figure id="fig-path">
<!-- include: fragments/kit-story/path.html -->
<figcaption><b>Figure 4.</b> The path of work. Dashed: optional. The filled step is the gate; nothing is built before it. This illustrative diagram contains no measured results.</figcaption>
</figure>
</section>

<section class="hs-sec" id="finished-page" style="--g:#ffb35c" aria-labelledby="finished-page-title">
<div class="hs-text">
<p class="hs-kicker">A finished page</p>
<h2 id="finished-page-title">A chapter can open with a slide and continue as the full chapter</h2>
<p><a href="#fig-showcase">Figure 5</a> shows one chapter of a project built with the kit: its slide face, then the same chapter in the reader, scrolled to its main figure. Click a picture to open it full screen.</p>
<a class="hs-more" href="build-a-site.html#figures-and-slides">More chapters and how they are made →</a>
</div>
<figure id="fig-showcase">
<div class="hs-shots">
<img src="../topics/build-a-site/media/showcase/environment-face.webp" alt="Slide face from the adaptation project: four contributions, drawn head to tail, add up to the next velocity.">
<img src="../topics/build-a-site/media/showcase/environment-reader.webp" alt="Its chapter in the reader: the sum built over four panels, one contribution in each.">
</div>
<figcaption><b>Figure 5.</b> One chapter of the adaptation project: the slide face, then the chapter in the reader. An example of what a project can build with the kit, not a template. Captured from that project at its commit <code>d22ef36</code>, the slide face on 2026-11-25 and the reader picture on 2026-11-26 with the reader of 5.7.0; not maintained. The text and numbers are the project's.</figcaption>
</figure>
</section>

<section class="hs-sec is-wide" id="practice-areas" style="--g:#ffb35c" aria-labelledby="practice-areas-title">
<div class="hs-text">
<p class="hs-kicker">Practices</p>
<h2 id="practice-areas-title">Four practice areas, each explained on its own page</h2>
<p>Each page explains its guides with reasons and examples and starts with the router rows for its guides, ready to copy into your <code>AGENTS.md</code>. The guides stay the exact reference.</p>
</div>
<div class="bs-grid g4">
<div class="bs-part bs-teal"><span class="bs-label">Code, runs and delivery</span><h3><a href="engineering-practices.html">Engineering</a></h3><ul>
<li>consumed output is an interface; generated files change at their source</li>
<li>efficient by default; a performance claim names its workload and path</li>
<li>expensive jobs run on the project's route, under a stated budget, owned through cleanup</li>
<li>the owner finishes routine work; changes to the agreement go back for a decision</li>
<li>reports lead with the outcome and say how each claim is known</li>
<li>one commit per logical deliverable, reviewed as a whole</li>
</ul><p><b>Read before:</b> changing code, running heavy jobs, handing off, committing.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Records for agents</span><h3><a href="documentation-practices.html">Records and documents</a></h3><ul>
<li>every fact has one home; finished work moves to its subject</li>
<li>the record is written first; a new page only when a person asks</li>
<li>a record names each object once; a measured number carries its provenance</li>
</ul><p><b>Read before:</b> creating or moving a document, writing a record.</p></div>
<div class="bs-part bs-blue"><span class="bs-label">Pages for people</span><h3><a href="writing-practices.html">Writing pages</a></h3><ul>
<li>each chapter carries one claim and states it before the evidence</li>
<li>one visible story; optional depth in typed folds</li>
<li>figures, mathematics and code excerpts follow shared conventions</li>
</ul><p><b>Read before:</b> making or updating a page.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Investigations and qualifications</span><h3><a href="experiments.html">Experiments</a></h3><ul>
<li>start with the smallest experiment that can change a decision</li>
<li>classify by what the result decides: investigation or qualification</li>
<li>build on existing evidence and stop once the question is answered</li>
<li>state the plan before running; report every attempt after</li>
<li>final runs only when results depend on a learned or fitted model</li>
<li>add a check only for a named gap; never lower a failed bar</li>
</ul><p><b>Read before:</b> designing or running an experiment, choosing its checks.</p></div>
</div>
</section>

<section class="home-map hs-routes" id="routes" aria-label="Every page">
<p class="hs-kicker">Every page</p>
<section class="map-group" data-group="start here"><h2>Start here</h2><div class="map-grid">
<a class="map-card" href="discuss-build-record.html"><span class="map-text"><strong>Discuss, build, record</strong><span>What a record, a page and a chapter are, and the one path every piece of work takes, experiments included.</span></span></a>
<a class="map-card" href="getting-started.html"><span class="map-text"><strong>Get started</strong><span>Set up a project: three commands, the files the starter writes and the adoption route that fits.</span></span></a>
<a class="map-card" href="build-a-site.html"><span class="map-text"><strong>Build a site</strong><span>How the kit turns tracked Markdown into a checked website, and every command from build to upgrade.</span></span></a>
<a class="map-card" href="global-agent-instructions.html"><span class="map-text"><strong>The owner's global agent instructions</strong><span>How the kit's owner has agents report, delegate, ask for a decision and check facts in every project. Optional to adopt, and not loaded by the kit.</span></span></a>
</div></section>
<section class="map-group" data-group="practices"><h2>Practices</h2><div class="map-grid">
<a class="map-card" href="engineering-practices.html"><span class="map-text"><strong>Engineering</strong><span>Why the six engineering guides exist, what each requires and what following them looks like.</span></span></a>
<a class="map-card" href="documentation-practices.html"><span class="map-text"><strong>Records and documents</strong><span>Where each document lives, why the record comes before any page, and what a record says about claims and numbers.</span></span></a>
<a class="map-card" href="writing-practices.html"><span class="map-text"><strong>Writing pages</strong><span>How a page for people explains its record: one claim per chapter, folds, figures, math and code.</span></span></a>
<a class="map-card" href="experiments.html"><span class="map-text"><strong>Experiments</strong><span>Keep experiments small, choose their purpose, state their content and match verification to the claim.</span></span></a>
<a class="map-card" href="approval-failed-open.html"><span class="map-text"><strong>Approval that failed open</strong><span>A measured case: how supporting code piled up in the project the kit was extracted from, and the rules that answer it.</span></span></a>
</div></section>
<section class="map-group" data-group="releases"><h2>Releases and source</h2><div class="map-grid">
<a class="map-card" href="https://github.com/davszi/documentation-kit"><span class="map-text"><strong>Repository on GitHub</strong><span>The kit's source: the rules, the site tooling, the reader theme and the starter, with every released version as a tag.</span></span></a>
<a class="map-card" href="releases.html"><span class="map-text"><strong>Release notes and migration guides</strong><span>What each version changes for consumers, and the steps to move a project from one version to the next.</span></span></a>
</div></section>
</section>
</div>
