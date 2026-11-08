+++
title = "Get started"
brand = "Documentation kit"
brand_sub = "what it provides · how it works · set up · adopt"
description = "What the kit provides, how a project routes contributors to its rules, the three practice areas, setup and which adoption route fits."
components = ["toc", "nav", "code", "filelinks", "panel-switcher"]
page_css = ["build-sheet.css"]
toc = [["What it provides", "#what-the-kit-provides"], ["How it works", "#how-it-works"], ["Practice areas", "#practice-areas"], ["Set up", "#set-up"], ["Adoption route", "#choose-how-to-adopt-it"]]
+++

# Get started with the documentation kit

<section class="card" id="what-the-kit-provides">

## One pinned submodule gives a project shared rules and tools

<p class="bs-lead">The kit supplies rules, a reader and a site toolchain. Your project keeps its content, its specifics and the decision when to upgrade.</p>

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">The kit supplies · <code>.docs-kit/</code></span><h3>Shared and pinned</h3><ul>
<li><code>rules/</code>: engineering, documentation, writing and experiment guides your router points to</li>
<li><code>theme/</code>: chapter reader, build-sheet layout, fonts and math (<a href="reader-tour.html">reader tour</a>)</li>
<li><code>docsite.py</code>, <code>tooling/</code>: build, lint, slides and export (<a href="commands.html">commands</a>)</li>
<li><code>examples/starter/</code>: the project that <code>init</code> writes without overwriting</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">Your project keeps</span><h3>Owned and local</h3><ul>
<li>repository map, commands and routes in <code>docs/PROJECT_CONTEXT.md</code> and <code>AGENTS.md</code></li>
<li>tools, workloads, resource profiles and acceptance thresholds</li>
<li>topic records, pages, navigation, evidence and figures</li>
<li>any exception to a shared rule, where contributors will find it</li>
<li>when to adopt a reviewed kit revision</li>
</ul></div>
</div>

<div class="bs-specs"><div><span class="bs-label">Install</span><b>One submodule</b></div><div><span class="bs-label">Needed to use the rules</span><b>Router rows</b></div><div><span class="bs-label">Site build</span><b>Optional</b></div></div>

A common rule changes in the kit, never in a consumer's copy; a project's exception stays in the project. [Ownership](readme.html#ownership) lists every path on each side; [canonical homes](documentation-system.html#canonical-homes) explains why.

</section>

<section class="card" id="how-it-works">

## Each rule is read right before the action it governs

<p class="bs-lead">Pin the kit once; your <code>AGENTS.md</code> names, for each kind of action, the kit guide and your own record to read first.</p>

<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit. Step 2: in AGENTS.md, add a row for each kind of action that names the kit guide and the project's own record, for example quoting a measured number with rules/writing/evidence.md and the project's benchmark records. Step 3: before that action, a contributor or agent reads both, then acts.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>.docs-kit</code> submodule</li><li>its commit is your version</li></ul></div>
<div class="bs-arrow"><span>route</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · <code>AGENTS.md</code></span><b>One row per action</b><ul><li>before quoting a number…</li><li>…read <code>rules/writing/evidence.md</code> and your benchmark records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read both, then act</b><ul><li>shared rule + project specifics</li><li>nothing is copied</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> Adoption is a pointer, not a copy: one router row joins a shared rule with the project's own specifics. This diagram contains no measured results.</figcaption>
</figure>

The trigger is the action, not the topic, so contributors and agents load only what applies. Step 2 for one action looks like this:

```markdown
| Before…                   | Read…                                                           |
|---------------------------|-----------------------------------------------------------------|
| Quoting a measured number | `.docs-kit/rules/writing/evidence.md` and our benchmark records |
```

The [starter's router](../../examples/starter/AGENTS.md.tmpl) has every row; keep the ones you need. See [agent entrypoints](documentation-system.html#agent-entrypoints-import-versus-point).

</section>

<section class="card" id="practice-areas">

## Three practice areas, each explained on its own page

<p class="bs-lead">Each page explains its guides with reasons and examples and lists the router row for every guide; the guides stay the exact reference.</p>

<div class="bs-grid g3">
<div class="bs-part bs-teal"><span class="bs-label">6 guides</span><h3><a href="engineering-practices.html">Engineering</a></h3><ul>
<li>code and repository</li><li>efficient implementation and performance claims</li><li>execution and shared resources</li><li>ownership, delivery and handoffs</li><li>Git and shared checkouts</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">7 guides</span><h3><a href="writing-practices.html">Documentation and writing</a></h3><ul>
<li>documentation system: homes, records and pages</li><li>page design and build sheets</li><li>explanations and honest claims</li><li>measurements and evidence</li><li>figures, mathematics and code excerpts</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">2 guides</span><h3><a href="experiments.html">Experiments</a></h3><ul>
<li>keep experiments small</li><li>investigation or qualification</li><li>proportionate verification</li><li>final runs only for learned or fitted models</li>
</ul></div>
</div>

The [writing](writing.html) and [site maintenance](maintenance.html) entrypoints remain as short routers, so old links to their section anchors still arrive at the right guide.

</section>

<section class="card" id="set-up">

## A new project needs one submodule, one environment and one init

<p class="bs-lead">Pin the kit, install its pinned Python packages, then let <code>init</code> add the starter without overwriting anything.</p>

```bash
git submodule add <kit-url> .docs-kit
git submodule update --init --recursive
python3.12 -m venv .build/docs-env
.build/docs-env/bin/python -m pip install -r .docs-kit/requirements.txt
.build/docs-env/bin/python .docs-kit/docsite.py init . --title "My project" --repository https://github.com/owner/repo
git add docs AGENTS.md CLAUDE.md .gitmodules .docs-kit
```

`init` checks every destination first and writes nothing if any starter file already exists. It writes `AGENTS.md`, `CLAUDE.md`, `docs/PROJECT_CONTEXT.md`, the reading index, worklog, open-work file and `docs/site/site.toml`, with the title (default: the folder name) and repository filled in. Add `.build/` to `.gitignore` and track the sources: the build only publishes tracked files.

<div class="bs-specs"><div><span class="bs-label">Python</span><b>3.12+</b></div><div><span class="bs-label">Packages</span><b>Pinned</b></div><div><span class="bs-label">JavaScript install</span><b>None</b></div></div>

Then [build, lint and preview](commands.html) the site, and [upgrade](commands.html#upgrade) the pin when you choose. A project that only adopts the rules can stop after the submodule and its router rows.

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
<li>Run the commands in <a href="#set-up">set up</a>.</li>
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
<li>Add the submodule and the router rows from <a href="#how-it-works">how it works</a>.</li>
<li>Choose rows from the <a href="#practice-areas">practice pages</a>.</li>
<li>Keep concrete commands, thresholds and resource profiles in the project's own records.</li>
</ul>
</div>
</div>

</section>
