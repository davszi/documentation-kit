+++
title = "Practices overview"
brand = "Documentation kit"
brand_sub = "engineering · writing · experiments"
description = "How a project routes contributors to the shared rules, and what each guide covers."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Routing", "#how-contributors-find-a-rule"], ["Practice areas", "#areas"], ["Project specifics", "#what-stays-with-the-project"]]
+++

# Shared practices, read before the action they govern

<section class="card" id="how-contributors-find-a-rule">

## Each rule is read right before the action it governs

<p class="bs-lead">A project's router names one guide per kind of action, so contributors and agents load only what applies.</p>

<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="A contributor is about to quote a measured number. The project's AGENTS.md has a row for quoting numbers that names the shared evidence guide and the project's own measurement records. The contributor reads both, then writes the claim.">
<div class="bs-node bs-teal"><span class="bs-label">About to act</span><b>Quote a number</b><p>The trigger is the action, not the topic.</p></div>
<div class="bs-arrow"><span>router row</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Project · <code>AGENTS.md</code></span><b>Before quoting a number</b><ul><li>read the shared <a href="evidence.html">evidence guide</a></li><li>read the project's measurement records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Two owners</span><b>Shared rule + specifics</b><ul><li><code>rules/writing/evidence.md</code></li><li>project workloads and thresholds</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> One router row joins a shared rule with the project's own specifics. It points to both and copies neither. See <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</figcaption>
</figure>

To adopt a guide, copy its row from the [starter's router](../../examples/starter/AGENTS.md) into your `AGENTS.md` and name the project record it pairs with. Each practice page lists the rows for its guides.

</section>

<section class="card" id="areas">

## Three practice areas, each explained on its own page

<p class="bs-lead">Each page explains its guides in cards and lists the router row for every guide; the guides themselves stay the exact reference.</p>

<div class="bs-grid g3">
<div class="bs-part bs-teal"><span class="bs-label">6 guides</span><h3><a href="engineering-practices.html">Engineering</a></h3><ul>
<li>code and repository</li><li>efficient implementation</li><li>execution and shared resources</li><li>ownership, delivery and handoffs</li><li>Git</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">7 guides</span><h3><a href="writing-practices.html">Documentation and writing</a></h3><ul>
<li>documentation system</li><li>page design and review</li><li>explanations</li><li>measurements and evidence</li><li>figures, mathematics and code excerpts</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">2 guides</span><h3><a href="experiments.html">Experiments</a></h3><ul>
<li>experiment workflow: keep experiments small</li><li>proportionate verification</li><li>final runs only for learned or fitted models</li>
</ul></div>
</div>

The [writing](writing.html) and [site maintenance](maintenance.html) entrypoints remain as short routers, so old links to their section anchors still arrive at the right guide.

</section>

<section class="card" id="what-stays-with-the-project">

## Each project keeps its specifics and its exceptions

<p class="bs-lead">Guides state rules that transfer between projects. Anything concrete to one project stays in that project.</p>

<div class="bs-grid g2">
<div class="bs-part bs-violet"><span class="bs-label">In the kit</span><h3>Common rules</h3><ul>
<li>one canonical guide per rule</li>
<li>changed in the kit, never in a consumer's copy</li>
<li>reaches projects when they move their pin</li>
</ul></div>
<div class="bs-part bs-teal"><span class="bs-label">In the project</span><h3>Specifics</h3><ul>
<li>repository map, commands and routes in <code>docs/PROJECT_CONTEXT.md</code></li>
<li>tools, workloads, resource profiles and acceptance thresholds</li>
<li>any exception to a shared rule, where contributors will find it</li>
</ul></div>
</div>

See [canonical homes](documentation-system.html#canonical-homes).

</section>
