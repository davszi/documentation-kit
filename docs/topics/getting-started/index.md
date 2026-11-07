+++
title = "Get started"
brand = "Documentation kit"
brand_sub = "what it provides · install · adopt"
description = "What the kit provides, how a project pins it and which adoption route fits."
reader = false
body_class = "reference-page"
components = ["toc", "nav", "filelinks", "panel-switcher"]
page_css = ["build-sheet.css", "../site/assets/kit-site.css"]
toc = [["What the kit provides", "#what-the-kit-provides"], ["Install and pin it", "#install-and-pin-it"], ["Choose how to adopt it", "#choose-how-to-adopt-it"]]
+++

# Get started with the documentation kit

<p class="bs-lead">A project adds the kit as one pinned Git submodule. The kit supplies shared practices and tools; the project keeps its content and decides when to upgrade.</p>

This page orients you. Commands and exact contracts stay in the guides it links,
so each instruction has one place to change.

## What the kit provides

<div class="kit-cards kit-cards-4">
<a class="kit-card" href="project-practices.html"><span class="kit-tag">rules/</span><strong>Shared practices</strong><span>Engineering, documentation and writing rules that a project's task router points contributors to.</span></a>
<a class="kit-card" href="reader.html"><span class="kit-tag">theme/</span><strong>Reader and theme</strong><span>The chapter reader, build-sheet layout, components, fonts and local math rendering.</span></a>
<a class="kit-card" href="authoring.html"><span class="kit-tag">docsite.py · tooling/</span><strong>Site toolchain</strong><span>Build, freshness check, lint, slide decks and publication export, with no JavaScript install.</span></a>
<a class="kit-card" href="readme.html#start-a-project"><span class="kit-tag">examples/starter/</span><strong>Starter project</strong><span>A neutral consumer that <code>init</code> copies into a new project without overwriting files.</span></a>
</div>

The project keeps its orientation, task routes, topic records, pages,
navigation, figures, evidence and upgrade timing.
[Ownership](readme.html#ownership) lists the paths on each side.

## Install and pin it

<ol class="kit-steps">
<li><strong>Add the submodule and a documentation environment.</strong> Add the kit at <code>.docs-kit</code>, create a Python 3.12 environment and install the pinned requirements. <a href="readme.html#start-a-project">Start a project</a></li>
<li><strong>Configure the site.</strong> Set the title, home label, source repository and navigation in <code>docs/site/site.toml</code>. <a href="authoring.html#tooling-and-ownership">Tooling and ownership</a></li>
<li><strong>Track sources, then build and lint.</strong> The build packages tracked files only. Serve <code>.build/docs/</code> on loopback to review it. <a href="readme.html#start-a-project">Build commands</a> · <a href="validation.html#validation-and-review">What validation covers</a></li>
<li><strong>Upgrade deliberately.</strong> The submodule pointer is the pin; a reviewed upgrade moves it together with any consumer changes. <a href="readme.html#pin-and-upgrade">Pin and upgrade</a> · <a href="releases.html">Release notes</a></li>
</ol>

## Choose how to adopt it

<p class="bs-lead">Pick the route that matches what the project already has.</p>

<div class="panel-switcher kit-routes" data-panel-switcher data-panel-default="new">
<div class="panel-switcher-controls" role="group" aria-label="Adoption route">
<button type="button" data-panel-choice="new" aria-pressed="false" aria-controls="route-new">New project</button>
<button type="button" data-panel-choice="existing" aria-pressed="false" aria-controls="route-existing">Existing documentation</button>
<button type="button" data-panel-choice="practices" aria-pressed="false" aria-controls="route-practices">Practices only</button>
</div>
<div id="route-new" data-panel="new" class="kit-route">
<h3 id="route-new-project">New project</h3>
<p>Start from the starter. <code>docsite.py init</code> checks every destination first and refuses to overwrite existing files.</p>
<ul>
<li>Run the steps in <a href="readme.html#start-a-project">Start a project</a>.</li>
<li>Replace the starter's guide with your topics, following <a href="authoring.html#authoring-paths">authoring paths</a>.</li>
<li>Keep the single task router the starter adds; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
</ul>
</div>
<div id="route-existing" data-panel="existing" class="kit-route">
<h3 id="route-existing-documentation">Existing documentation</h3>
<p>Keep the existing content and destinations. Add the configuration deliberately, page by page.</p>
<ul>
<li>Render existing Markdown in place with <a href="authoring.html#registered-source-pages">registered source pages</a>; nothing moves.</li>
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a> and project <a href="resources.html#resource-closure-and-evidence">path adapters</a>.</li>
<li>Replace copied shared rules only after their project-specific parts have a linked home, as the <a href="migrate-1-1-0.html#prepare-the-deliverable">migration guide</a> describes.</li>
</ul>
</div>
<div id="route-practices" data-panel="practices" class="kit-route">
<h3 id="route-practices-only">Practices only</h3>
<p>The rules are plain Markdown. A project can route contributors to them without building a site.</p>
<ul>
<li>Add one task-triggered router that names the guide to read before each action; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
<li>Start from the <a href="project-practices.html">practices overview</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in the project's own records.</li>
</ul>
</div>
</div>
