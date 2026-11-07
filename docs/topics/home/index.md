+++
title = "Documentation kit"
slug = "index"
brand = "Documentation kit"
brand_sub = "shared practices · reader · site toolchain"
reader = false
raw = true
components = ["nav", "filelinks"]
page_css = ["build-sheet.css", "home.css", "../site/assets/kit-site.css"]
body_class = "kit-home"
toc = []
+++

<div class="home">
<header class="home-hero kit-hero">
<div>
<p class="kit-eyebrow">Engineering and documentation kit</p>
<h1>One pinned kit for how a project builds, records and explains its work</h1>
<p>Shared engineering and documentation practices, a chapter reader and a small static-site toolchain. A project pins one reviewed revision as a Git submodule and keeps its own pages, navigation and evidence.</p>
<div class="home-cta">
<a href="getting-started.html">Get started</a>
<a class="alt" href="readme.html#start-a-project">Setup commands</a>
</div>
</div>
<figure class="kit-sources" aria-labelledby="kit-sources-caption">
<div class="kit-sources-diagram" role="img" aria-label="Each guide is one Markdown file. Contributors and agents read it as Markdown through the project's task router. The site build renders the same file as an HTML page. Edits go to the Markdown file only.">
<div class="kit-src"><span class="kit-tag">one editable source</span><code>rules/engineering/git.md</code><small>Markdown in the kit repository</small></div>
<div class="kit-fork">
<div class="kit-branch kit-branch-agent"><span class="kit-arrow" aria-hidden="true"></span><div><b>Read as Markdown</b><small>contributors and agents, routed by <code>AGENTS.md</code></small></div></div>
<div class="kit-branch kit-branch-site"><span class="kit-arrow" aria-hidden="true"></span><div><b>Rendered as a page</b><small><code>git.html</code> on this site, with source and edit links</small></div></div>
</div>
</div>
<figcaption id="kit-sources-caption"><b>Every guide has one source.</b> This site renders the kit's own Markdown files in place, so a correction lands once and both readers see it.</figcaption>
</figure>
</header>

<section class="kit-paths" aria-label="Choose a path">
<a class="kit-path kit-path-build" href="site-toolkit.html">
<span class="kit-path-step">Path 1</span>
<strong>Build a site</strong>
<span>Turn tracked Markdown, figures and configuration into a checked static site with the shared reader.</span>
<span class="kit-path-links">Toolkit overview · authoring · validation</span>
</a>
<a class="kit-path kit-path-practices" href="project-practices.html">
<span class="kit-path-step">Path 2</span>
<strong>Adopt project practices</strong>
<span>Route contributors to shared rules for code, execution, delivery, Git, documentation and writing.</span>
<span class="kit-path-links">Engineering · documentation · writing</span>
</a>
<a class="kit-path kit-path-upgrade" href="releases.html">
<span class="kit-path-step">Path 3</span>
<strong>Upgrade a pinned kit</strong>
<span>See what each version changes for consumers, what stays stable in 1.x and how to migrate.</span>
<span class="kit-path-links">Release notes · migration guides</span>
</a>
</section>

<section class="kit-split" aria-label="Ownership">
<div class="kit-own kit-own-kit">
<span class="kit-tag">the kit owns</span>
<ul>
<li>Shared rules in <code>rules/</code></li>
<li>Theme, reader, fonts and math assets in <code>theme/</code></li>
<li>Renderer, packaging and checks in <code>tooling/</code></li>
<li>The neutral starter in <code>examples/starter/</code></li>
</ul>
</div>
<div class="kit-own kit-own-project">
<span class="kit-tag">each project owns</span>
<ul>
<li>Orientation, task routes and project-specific choices</li>
<li>Topic records, pages, navigation and local assets</li>
<li>Evidence, figures and their provenance</li>
<li>When to adopt a reviewed kit revision</li>
</ul>
</div>
<p class="kit-own-note">The full split, with paths, is in <a href="readme.html#ownership">Ownership</a>.</p>
</section>

<section class="home-now" aria-label="Every page">
<h2>Every page</h2>
<!-- site-map -->
</section>
</div>
