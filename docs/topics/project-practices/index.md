+++
title = "Project practices"
brand = "Documentation kit"
brand_sub = "engineering · writing · experiments"
description = "How a project routes contributors to the shared rules, and what each guide covers."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Routing", "#how-contributors-find-a-rule"], ["Engineering", "#engineering"], ["Documentation and writing", "#documentation-and-writing"], ["Experiments", "#experiments"], ["Project specifics", "#what-stays-with-the-project"]]
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

To adopt a guide, copy its row from the [starter's router](../../examples/starter/AGENTS.md) into your `AGENTS.md` and name the project record it pairs with. The next three chapters list every row.

</section>

<section class="card" id="engineering">

## Engineering guides cover code, jobs, delivery and history

<p class="bs-lead">Six guides, each read before one kind of engineering action.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Engineering guides by action">

| Before… | Read… | It covers |
|---|---|---|
| Changing source, tests or configuration | [Code and repository](code-practices.html) | Program output, diagnostics and generated files |
| Changing runtime cost or claiming performance | [Efficient implementation](performance.html) | Efficient defaults; claims scoped to a stated workload |
| Running tests, builds or other expensive jobs | [Execution and resources](execution.html) | Execution routes, budgets, usage records, supervision and cleanup |
| Assigning work or editing in parallel | [Ownership and delivery](delivery.html) | Assignment scope, coordination, parallel work and blockers |
| Reporting completion or blockers | [Handoffs](handoffs.html) | Completion and blocker reports, durable evidence, receiving work |
| Staging, committing or rewriting history | [Git](git.html) | Deliverables and validation, commit messages, shared checkouts |

</div>

</section>

<section class="card" id="documentation-and-writing">

## Writing guides cover documents, pages, explanations and evidence

<p class="bs-lead">One guide decides where a fact lives; six more govern how it is written, drawn and backed.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Documentation and writing guides by action">

| Before… | Read… | It covers |
|---|---|---|
| Creating, moving or retiring a document | [Documentation system](documentation-system.html) | One canonical home per fact, chronology, publishing, agent entrypoints |
| Writing or reviewing a page | [Page design and review](page-design.html) | Section purpose, figure placement, homepages, build-sheet pages, slides |
| Explaining something | [Explanations](explanations.html) | Reading order, optional layers, naming and honest claims |
| Quoting a measured number | [Measurements and evidence](evidence.html) | What a measured claim needs, when to rerun, ledgers, experiment records |
| Drawing a figure | [Figures and access](figures.html) | Choosing a representation, comparisons, interaction, accessibility |
| Deriving mathematics | [Mathematics](math.html) | Known constructions, notation, worked examples, rendering |
| Excerpting code | [Code excerpts and diagrams](code-excerpts.html) | Verified excerpts with real line numbers, data-backed diagrams |

</div>

The [writing](writing.html) and [site maintenance](maintenance.html) entrypoints remain as short routers, so old links to their section anchors still arrive at the right guide.

</section>

<section class="card" id="experiments">

## Experiment guides keep runs small and checks proportionate

<p class="bs-lead">An experiment is classified by what its result decides, not by the project's field.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Answers a question</span><h3>Investigation</h3><p>"No" or "inconclusive" is a finding. Declared before running as exploratory or confirmatory.</p></div>
<div class="bs-part bs-orange"><span class="bs-label">Gives a verdict</span><h3>Qualification</h3><p>Pass, fail or inconclusive for a named system, build or model against a bar fixed before the run.</p></div>
</div>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Experiment guides by action">

| Before… | Read… | It covers |
|---|---|---|
| Designing or running an experiment | [Experiment workflow](experiment-workflow.html) | Keeping experiments small, baselines, stopping and required content |
| Choosing checks or interpreting failures | [Proportionate verification](experiment-verification.html) | Evidence gaps, application logic, numerical correctness, regression gates |

</div>

Final runs apply only when results depend on a learned or fitted model; see [learned or fitted models only](experiment-workflow.html#learned-or-fitted-models-only).

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
