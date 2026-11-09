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
<div class="home-hero-text">
<p class="home-eyebrow">Documentation kit</p>
<h1>Shared working rules, pinned into each project</h1>
<p>Add the kit to your repository as one Git submodule. Then add rows to your <code>AGENTS.md</code>: each row names an action and the kit guide to read before it. Contributors and agents follow those rows. Building a documentation site with the kit is optional.</p>
<div class="home-cta">
<a href="getting-started.html">Get started</a>
<a class="alt" href="build-a-site.html">Build a site</a>
</div>
<a class="home-link" href="getting-started.html#set-up">Set up a project in three commands →</a>
</div>
<figure class="home-router" aria-label="Three rows of a project's AGENTS.md: before writing or changing a record, read rules/records.md; before designing an experiment, read rules/experiments/workflow.md; before handing off work, read rules/engineering/handoffs.md.">
<div class="home-router-bar"><span></span><span></span><span></span><code>AGENTS.md</code></div>
<div class="home-router-head"><span>Before…</span><span>Read…</span></div>
<div class="home-router-row" style="--g:#6ee7c5"><span>Writing or changing a record</span><code>rules/records.md</code></div>
<div class="home-router-row" style="--g:#b69cff"><span>Designing an experiment</span><code>rules/experiments/workflow.md</code></div>
<div class="home-router-row" style="--g:#ffb35c"><span>Handing off work</span><code>rules/engineering/handoffs.md</code></div>
<figcaption>Each row pairs a kit guide with your own records. The <a href="../../examples/starter/AGENTS.md.tmpl">starter's router</a> has every row.</figcaption>
</figure>
</header>

<section class="home-section" aria-label="How a project uses the kit">
<h2>How a project uses the kit</h2>
<ol class="home-steps">
<li style="--g:#6ee7c5"><span class="home-step-n">01</span><span class="home-step-when">Once</span><strong>Pin the kit</strong><p><code>git submodule add &lt;kit-url&gt; .docs-kit</code>. The submodule commit is your version.</p></li>
<li style="--g:#b69cff"><span class="home-step-n">02</span><span class="home-step-when">In AGENTS.md</span><strong>Route each action</strong><p>One row per action, such as <em>before making a performance claim</em>, naming the kit guide and your record.</p></li>
<li style="--g:#ffb35c"><span class="home-step-n">03</span><span class="home-step-when">Every time</span><strong>Read before acting</strong><p>The contributor or agent opens that guide; project specifics stay in project records.</p></li>
</ol>
</section>

<section class="home-section home-map" aria-label="Every page">
<!-- site-map -->
</section>
</div>
