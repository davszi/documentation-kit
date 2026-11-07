+++
title = "Project practices"
brand = "Documentation kit"
brand_sub = "engineering · writing · experiments"
description = "How a project routes contributors to the shared rules, and what each guide covers."
reader = false
body_class = "reference-page"
components = ["toc", "nav", "filelinks"]
page_css = ["build-sheet.css", "../site/assets/kit-site.css"]
toc = [["How contributors find a rule", "#how-contributors-find-a-rule"], ["Engineering", "#engineering"], ["Documentation and writing", "#documentation-and-writing"], ["Experiments", "#experiments"], ["What stays with the project", "#what-stays-with-the-project"]]
+++

# Shared practices, read before the action they govern

<p class="bs-lead">Each shared rule lives in one focused guide. A project's task router names the guide to read before each kind of action, so contributors load only what applies.</p>

## How contributors find a rule

<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="A contributor is about to commit. The project's AGENTS.md router has a row for staging and committing that names the shared Git guide and the project's own validation requirements. The contributor reads both, then acts.">
<div class="bs-node bs-teal"><span class="bs-label">About to act</span><b>Commit a change</b><small>The trigger is the action, not the topic.</small></div>
<div class="bs-arrow"><span>router row</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Project · <code>AGENTS.md</code></span><b>Before staging or committing…</b><ul><li>read the shared <a href="git.html">Git guide</a></li><li>read the project's validation requirements</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Two owners</span><b>Shared rule + project specifics</b><ul><li><code>rules/engineering/git.md</code></li><li>project test commands and gates</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> One router row joins a shared rule with the project's own specifics. The router points to both; it copies neither. See <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</figcaption>
</figure>

## Engineering

<div class="kit-cards kit-cards-3">
<a class="kit-card" href="code-practices.html"><span class="kit-tag">before changing code</span><strong>Code and repository</strong><span>Program output, diagnostics and generated files.</span></a>
<a class="kit-card" href="performance.html"><span class="kit-tag">before performance claims</span><strong>Efficient implementation</strong><span>Efficient by default; claims scoped to a stated workload.</span></a>
<a class="kit-card" href="execution.html"><span class="kit-tag">before expensive jobs</span><strong>Execution and shared resources</strong><span>Execution routes, budgets, usage records, failure attribution, supervision and cleanup.</span></a>
<a class="kit-card" href="delivery.html"><span class="kit-tag">before assigning work</span><strong>Ownership and delivery</strong><span>Assignment scope, owner responsibility, coordination, parallel work and blockers.</span></a>
<a class="kit-card" href="handoffs.html"><span class="kit-tag">before reporting</span><strong>Handoffs</strong><span>Completion and blocker reports, durable evidence and receiving a handoff.</span></a>
<a class="kit-card" href="git.html"><span class="kit-tag">before committing</span><strong>Git</strong><span>Deliverables and validation, explanatory messages, shared checkouts and history.</span></a>
</div>

## Documentation and writing

<div class="kit-cards kit-cards-3">
<a class="kit-card kit-card-wide" href="documentation-system.html"><span class="kit-tag">before creating, moving or retiring a document</span><strong>Documentation system</strong><span>One canonical home per fact, the path from open work to subject knowledge, evidence identity, chronology, publishing and agent entrypoints.</span></a>
<a class="kit-card" href="page-design.html"><span class="kit-tag">before writing a page</span><strong>Page design and review</strong><span>Section purpose, figure placement, homepages, build-sheet pages, slides and completion review.</span></a>
<a class="kit-card" href="explanations.html"><span class="kit-tag">before explaining</span><strong>Explanations</strong><span>Reading order, Story and optional layers, naming and honest claims.</span></a>
<a class="kit-card" href="evidence.html"><span class="kit-tag">before quoting a number</span><strong>Measurements and evidence</strong><span>What a measured claim needs, when to rerun, ledgers and experiment records.</span></a>
<a class="kit-card" href="figures.html"><span class="kit-tag">before drawing</span><strong>Figures and access</strong><span>Choosing a representation, comparisons, interaction and accessibility.</span></a>
<a class="kit-card" href="math.html"><span class="kit-tag">before deriving</span><strong>Mathematics</strong><span>Building from known constructions, notation, worked examples and rendering.</span></a>
<a class="kit-card" href="code-excerpts.html"><span class="kit-tag">before excerpting code</span><strong>Code excerpts and diagrams</strong><span>Verified excerpts with real line numbers and data-backed diagrams.</span></a>
</div>

## Experiments

<div class="kit-cards kit-cards-3">
<a class="kit-card" href="experiment-workflow.html"><span class="kit-tag">before designing a run</span><strong>Experiment workflow</strong><span>Keep experiments small; investigation or qualification; baselines, stopping and required content. Final runs only for learned models.</span></a>
<a class="kit-card" href="experiment-verification.html"><span class="kit-tag">before choosing checks</span><strong>Proportionate verification</strong><span>Checks chosen for the claim: evidence gaps, application logic, numerical correctness, regression gates and failures.</span></a>
</div>

The original [writing](writing.html) and [site maintenance](maintenance.html)
entrypoints remain as short routers, so links to their section anchors still
arrive at the right guide.

## What stays with the project

The shared guides state rules that transfer between projects. Each consuming
project keeps, in its own records:

- its repository map, commands and named documentation routes in `docs/PROJECT_CONTEXT.md`;
- concrete tools, workloads, resource profiles, acceptance thresholds and runtime requirements;
- any exception to a shared rule, recorded where the project's contributors will find it.

Change a common rule in the kit, not in a consumer's copy. See
[canonical homes](documentation-system.html#canonical-homes).
