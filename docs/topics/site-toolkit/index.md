+++
title = "Site toolkit"
brand = "Documentation kit"
brand_sub = "sources · build · checks"
description = "How a build turns tracked sources into a checked site, and which guide covers each task."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["How a build works", "#how-a-build-works"], ["Guide per task", "#find-the-guide-for-a-task"], ["Existing Markdown", "#render-existing-markdown-in-place"], ["Checks", "#checks-before-publishing"]]
+++

# The site toolkit turns tracked sources into a checked static site

<section class="card" id="how-a-build-works">

## One build turns tracked sources into a self-contained site

<p class="bs-lead">The pinned kit reads the project's tracked sources and writes a site under <code>.build/docs/</code>; lint and the freshness check verify it.</p>

<figure id="fig-build">
<div class="bs-flow" role="img" aria-label="Tracked project sources and the pinned kit enter docsite.py build. The build writes generated HTML, assets and a build manifest. Lint and the freshness check read that output. Generated output never flows back into source.">
<div class="bs-node bs-teal"><span class="bs-label">Project sources · tracked</span><b>Content and configuration</b><ul><li><code>docs/topics/*/index.md</code> pages</li><li>registered Markdown records</li><li><code>docs/site/site.toml</code>, fragments, local CSS</li><li><code>docs/figures/</code> and media</li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Pinned kit</span><b>Renderer and theme</b><ul><li>Markdown, includes and slide faces</li><li>shell, reader and components</li><li>link rewriting and resource closure</li></ul></div>
<div class="bs-arrow"><span>writes</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated · ignored by Git</span><b><code>.build/docs/</code></b><ul><li><code>html/*.html</code> and <code>assets/</code></li><li>packaged media under <code>_media/</code></li><li><code>site-build.json</code> manifest</li></ul></div>
<div class="bs-back"><span>×</span> Output is never edited. Change a source, configuration or generator, then rebuild.</div>
</div>
<figcaption><b>Figure 1.</b> Follow the arrows from tracked inputs to generated output. Pages link to each other by generated name, such as <code>evidence.html#numbers-and-staleness</code>; links to other repository files become source links. <a href="authoring.html#authoring-paths">Authoring paths</a> gives the exact rules.</figcaption>
</figure>

</section>

<section class="card" id="find-the-guide-for-a-task">

## Each toolkit task has one owning guide

<p class="bs-lead">Commands, page authoring, the reader, figures, packaging and checks each live in one place.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Toolkit guides by task">

| To… | Read… | It covers |
|---|---|---|
| Run commands and configure the site | [Setup and commands](commands.html), [tooling and ownership](authoring.html#tooling-and-ownership) | `init`, `build`, `lint` and `slides`; `site.toml` keys, navigation, adapters |
| Write pages | [Authoring paths](authoring.html#authoring-paths) | Entry pages and frontmatter, link origins, includes, local components |
| Use the reader and components | [Reader](reader.html), [panel switcher](panel-switcher.html) | Chapter views, reading layers, the home site map, the panel switcher |
| Draw, derive and present | [Generated figures](authoring.html#generated-figures), [slide faces](authoring.html#slide-faces-and-decks) | Generated figures and number ledgers, KaTeX math, slide faces and decks |
| Package images, media and evidence | [Resources and evidence](resources.html) | Resource closure, local-only captures, inventories, path adapters |
| Check and publish | [Validation](validation.html), [publication export](publication.html) | Complete validation, browser checks, export into an existing publication |

</div>

Related writing rules: [slide faces](page-design.html#slide-faces), [mathematical explanation](math.html) and [figures and access](figures.html).

</section>

<section class="card" id="render-existing-markdown-in-place">

## Existing Markdown renders in place, without copies

<p class="bs-lead">One registry entry publishes a tracked Markdown file as a page; the file stays where it is and stays the only copy.</p>

<figure id="fig-source-page">
<div class="bs-flow" role="img" aria-label="A tracked Markdown file, for example docs/notes/decision.md, stays unchanged. A source_pages entry in site.toml names the file and its route. The build renders decision.html with a source line and edit link, resolving links from the file's own folder and checking their anchors.">
<div class="bs-node bs-teal"><span class="bs-label">Tracked file · unchanged</span><b>Canonical Markdown</b><ul><li><code>docs/notes/decision.md</code></li><li>still read as Markdown by agents</li></ul></div>
<div class="bs-arrow"><span>register</span></div>
<div class="bs-node bs-violet"><span class="bs-label"><code>docs/site/site.toml</code></span><b>One registry entry</b><ul><li><code>[[source_pages]]</code></li><li><code>source = "docs/notes/decision.md"</code></li><li><code>slug = "decision"</code></li></ul></div>
<div class="bs-arrow"><span>build</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Generated page</span><b><code>decision.html</code></b><ul><li>source line and edit link</li><li>links resolved from the file's folder</li><li>anchors between pages checked</li></ul></div>
</div>
<figcaption><b>Figure 2.</b> Every detailed guide on this site is published this way. <a href="authoring.html#registered-source-pages">Registered source pages</a> owns the contract.</figcaption>
</figure>

</section>

<section class="card" id="checks-before-publishing">

## Checks fail the build instead of publishing a broken page

<p class="bs-lead">Missing, untracked or escaping inputs stop the build; lint and the freshness check catch the rest before review.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">build</span><h3>Tracked sources only</h3><p>Untracked pages, figures and media fail instead of being published.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">build</span><h3>Contained paths</h3><p>Links, includes and media that leave the project or escape through a symlink fail.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">build</span><h3>Routes and anchors</h3><p>Route collisions fail; links into registered pages must reach a rendered anchor.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">lint</span><h3>Records and links</h3><p><code>lint --strict</code> checks Markdown records and their links, warnings included.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">check</span><h3>Fresh output</h3><p><code>build --check</code> fails when the generated site no longer matches its sources.</p></div>
</div>

[Validation](validation.html) lists what a complete check covers, including browser review.

</section>
