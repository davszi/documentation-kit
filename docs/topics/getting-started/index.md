+++
title = "Get started"
brand = "Documentation kit"
brand_sub = "what it provides · set up · adopt"
description = "What the kit provides, how a project pins it and which adoption route fits."
components = ["toc", "nav", "code", "filelinks", "panel-switcher"]
page_css = ["build-sheet.css"]
toc = [["What it provides", "#what-the-kit-provides"], ["Set it up", "#set-it-up"], ["Site and upgrades", "#site-and-upgrades"], ["Adoption route", "#choose-how-to-adopt-it"]]
+++

# Get started with the documentation kit

<section class="card" id="what-the-kit-provides">

## One pinned submodule gives a project shared rules and tools

<p class="bs-lead">The kit supplies rules, a reader and a site toolchain. Your project keeps its content and decides when to upgrade.</p>

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">The kit supplies · <code>.docs-kit/</code></span><h3>Shared and pinned</h3><ul>
<li><code>rules/</code>: practices your router points to (<a href="project-practices.html">overview</a>)</li>
<li><code>theme/</code>: chapter reader, build-sheet layout, fonts and math (<a href="reader.html">reader</a>)</li>
<li><code>docsite.py</code>, <code>tooling/</code>: build, lint, slides and export (<a href="site-toolkit.html">toolkit</a>)</li>
<li><code>examples/starter/</code>: a project that <code>init</code> copies in without overwriting</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">Your project keeps</span><h3>Owned and local</h3><ul>
<li>orientation and the task router in <code>AGENTS.md</code></li>
<li>topic records, pages, navigation and local assets</li>
<li>evidence, figures and their provenance</li>
<li>when to adopt a reviewed kit revision</li>
</ul></div>
</div>

<div class="bs-specs"><div><span class="bs-label">Install</span><b>One submodule</b></div><div><span class="bs-label">Needed to use the rules</span><b>Router rows</b></div><div><span class="bs-label">Site build</span><b>Optional</b></div></div>

[Ownership](readme.html#ownership) lists every path on each side.

</section>

<section class="card" id="set-it-up">

## Three steps make the rules part of everyday work

<p class="bs-lead">Pin the kit once, add one router row per action, and read the named guide before acting.</p>

<figure id="fig-setup">
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit with git submodule add. Step 2: in AGENTS.md, add a row that names an action and the kit guide for it, for example quoting a measured number and rules/writing/evidence.md. Step 3: before that action, a contributor or agent reads the guide together with the project's own record.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>git submodule add &lt;kit-url&gt; .docs-kit</code></li><li>the submodule commit is your version</li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · AGENTS.md</span><b>Route each action</b><ul><li>one row per action</li><li>names the kit guide and your record</li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read before acting</b><ul><li>the contributor or agent opens both</li><li>nothing is copied into the project</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> Adoption is a pointer, not a copy. The row below is step 2 for one action.</figcaption>
</figure>

```markdown
| Before…                   | Read…                                                           |
|---------------------------|-----------------------------------------------------------------|
| Quoting a measured number | `.docs-kit/rules/writing/evidence.md` and our benchmark records |
```

The [starter's router](../../examples/starter/AGENTS.md.tmpl) has every row; keep the ones you need.

</section>

<section class="card" id="site-and-upgrades">

## A site build and an upgrade are separate, deliberate choices

<p class="bs-lead">The rules work without a site. A kit upgrade moves the pinned commit only after you read what changed.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Optional</span><h3>Build a site</h3><ol>
<li>Create the documentation environment and run <code>docsite.py init .</code></li>
<li>Set the title, source repository and navigation in <code>docs/site/site.toml</code></li>
<li>Track the sources, then <code>build</code> and <code>lint --strict</code></li>
<li>Serve <code>.build/docs/</code> on loopback and review it</li>
</ol><p><a href="commands.html#start-a-project">Commands</a> · <a href="validation.html#validation-and-review">what the checks cover</a></p></div>
<div class="bs-part bs-orange"><span class="bs-label">When you choose</span><h3>Upgrade the pin</h3><ol>
<li>Read the release notes between your pin and the target</li>
<li>Move the submodule to the reviewed commit</li>
<li>Apply any consumer changes in the same commit</li>
<li>Rerun your checks before relying on the new rules</li>
</ol><p><a href="releases.html">Release notes</a> · <a href="commands.html#upgrade">upgrade commands</a></p></div>
</div>

</section>

<section class="card" id="choose-how-to-adopt-it">

## Pick the adoption route that matches what you already have

<p class="bs-lead">A new project starts from the starter; existing documentation stays where it is; a project can also adopt the rules alone.</p>

<div class="panel-switcher" data-panel-switcher data-panel-default="new">
<div class="panel-switcher-controls" role="group" aria-label="Adoption route">
<button type="button" data-panel-choice="new" aria-pressed="false" aria-controls="route-new">New project</button>
<button type="button" data-panel-choice="existing" aria-pressed="false" aria-controls="route-existing">Existing documentation</button>
<button type="button" data-panel-choice="practices" aria-pressed="false" aria-controls="route-practices">Practices only</button>
</div>
<div id="route-new" data-panel="new">
<h3 id="route-new-project">New project</h3>
<p>Start from the starter. <code>docsite.py init</code> checks every destination first and refuses to overwrite existing files.</p>
<ul>
<li>Run the steps in <a href="commands.html#start-a-project">Start a project</a>.</li>
<li>Replace the starter's guide with your topics, following <a href="authoring.html#authoring-paths">authoring paths</a>.</li>
<li>Keep the single task router the starter adds; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
</ul>
</div>
<div id="route-existing" data-panel="existing">
<h3 id="route-existing-documentation">Existing documentation</h3>
<p>Keep the existing content and destinations. Add the configuration deliberately, page by page.</p>
<ul>
<li>Render existing Markdown in place with <a href="authoring.html#registered-source-pages">registered source pages</a>; nothing moves.</li>
<li>Keep historical public routes with the <a href="publication.html">publication exporter</a> and project <a href="resources.html#resource-closure-and-evidence">path adapters</a>.</li>
<li>Replace copied shared rules only after their project-specific parts have a linked home, as the <a href="migrate-1-1-0.html#prepare-the-deliverable">migration guide</a> describes.</li>
</ul>
</div>
<div id="route-practices" data-panel="practices">
<h3 id="route-practices-only">Practices only</h3>
<p>The rules are plain Markdown. A project can route contributors to them without building a site.</p>
<ul>
<li>Add the router rows from <a href="#set-it-up">step 2</a>; see <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</li>
<li>Choose rows from the <a href="project-practices.html">practices overview</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in the project's own records.</li>
</ul>
</div>
</div>

</section>
