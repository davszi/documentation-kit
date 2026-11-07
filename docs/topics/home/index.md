+++
title = "Documentation kit"
slug = "index"
brand = "Documentation kit"
brand_sub = "shared practices · reader · site toolchain"
reader = false
components = ["nav", "filelinks"]
page_css = ["build-sheet.css", "home.css"]
toc = []
+++

<div class="home">
<header class="home-hero">
<div>
<h1>Shared working rules, pinned into each project</h1>
<p>Add the kit to your repository as one Git submodule. Then add rows to your <code>AGENTS.md</code>: each row names an action and the kit guide to read before it. Contributors and agents follow those rows. Building a documentation site with the kit is optional.</p>
<div class="home-cta">
<a href="getting-started.html">Get started</a>
<a class="alt" href="reader-tour.html">Reader tour</a>
<a class="alt" href="readme.html#start-a-project">Setup commands</a>
</div>
</div>
<div class="bs-grid g1" role="navigation" aria-label="Choose a path">
<a class="now-card" href="project-practices.html"><strong>1 · Adopt the practices</strong><span>Which kit guide to read before which action: code, execution, delivery, Git, documentation, writing and experiments.</span></a>
<a class="now-card" href="site-toolkit.html"><strong>2 · Build a site (optional)</strong><span>Turn tracked Markdown, figures and configuration into a checked static site with the shared reader.</span></a>
<a class="now-card" href="releases.html"><strong>3 · Upgrade a pinned kit</strong><span>What each version changes for consumers, what stays stable in 1.x and how to migrate.</span></a>
</div>
</header>

<section class="home-now" aria-label="How a project uses the kit">
<h2>How a project uses the kit</h2>
<div class="bs-flow" role="img" aria-label="Step 1: pin the kit at .docs-kit with git submodule add. Step 2: in AGENTS.md, add a row that names an action, for example quoting a measured number, and the kit guide for it, rules/writing/evidence.md. Step 3: before quoting a number, a contributor or agent opens that guide and follows it, together with the project's own records.">
<div class="bs-node bs-teal"><span class="bs-label">Step 1 · once</span><b>Pin the kit</b><ul><li><code>git submodule add &lt;kit-url&gt; .docs-kit</code></li><li>the submodule commit is the pinned version</li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Step 2 · in AGENTS.md</span><b>Route each action</b><ul><li>one row per action: <em>before quoting a number</em></li><li>names the guide: <code>rules/writing/evidence.md</code></li></ul></div>
<div class="bs-arrow"><span>then</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Step 3 · every time</span><b>Read before acting</b><ul><li>the contributor or agent opens that guide</li><li>project specifics stay in project records</li></ul></div>
</div>
</section>

<section class="home-now" aria-label="What step 2 looks like">
<h2>What step 2 looks like in your AGENTS.md</h2>

```markdown
| Before…                   | Read…                                                                |
|---------------------------|----------------------------------------------------------------------|
| Quoting a measured number | `.docs-kit/rules/writing/evidence.md` and our benchmark records      |
| Designing an experiment   | `.docs-kit/rules/experiments/workflow.md` and our experiment records |
| Handing off work          | `.docs-kit/rules/engineering/handoffs.md`                            |
```

<p class="home-foot">Each row pairs a kit guide with the project record that holds your specifics. The <a href="../../examples/starter/AGENTS.md.tmpl">starter's router</a> has every row; keep the ones you need. Full commands: <a href="readme.html#start-a-project">Start a project</a>.</p>
</section>

<section class="home-now" aria-label="Every page">
<h2>Every page</h2>
<!-- site-map -->
</section>
</div>
