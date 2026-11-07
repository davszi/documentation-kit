+++
title = "Project practices"
brand = "Documentation kit"
brand_sub = "engineering · writing · experiments"
description = "How a project routes contributors to the shared rules, and what each guide covers."
body_class = "reference-page"
components = ["toc", "nav", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["How contributors find a rule", "#how-contributors-find-a-rule"], ["Engineering", "#engineering"], ["Documentation and writing", "#documentation-and-writing"], ["Experiments", "#experiments"], ["What stays with the project", "#what-stays-with-the-project"]]
+++

# Shared practices, read before the action they govern

## How contributors find a rule

<p class="bs-lead">Each shared rule lives in one focused guide. A project's task router names the guide to read before each kind of action, so contributors load only what applies.</p>

<figure id="fig-routing">
<div class="bs-flow" role="img" aria-label="A contributor is about to quote a measured number. The project's AGENTS.md has a row for quoting numbers that names the shared evidence guide and the project's own measurement records. The contributor reads both, then writes the claim.">
<div class="bs-node bs-teal"><span class="bs-label">About to act</span><b>Quote a number</b><small>The trigger is the action, not the topic.</small></div>
<div class="bs-arrow"><span>router row</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Project · <code>AGENTS.md</code></span><b>Before quoting a number…</b><ul><li>read the shared <a href="evidence.html">evidence guide</a></li><li>read the project's measurement records</li></ul></div>
<div class="bs-arrow"><span>read</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Two owners</span><b>Shared rule + project specifics</b><ul><li><code>rules/writing/evidence.md</code></li><li>project workloads and thresholds</li></ul></div>
</div>
<figcaption><b>Figure 1.</b> One router row joins a shared rule with the project's own specifics. The router points to both; it copies neither. See <a href="documentation-system.html#agent-entrypoints-import-versus-point">agent entrypoints</a>.</figcaption>
</figure>

To adopt a guide, copy its row into your project's `AGENTS.md` and add the
project record it pairs with. The
[starter's router](../../examples/starter/AGENTS.md) has every row; delete the
ones your project does not need.

## Engineering

| Before… | Read… | It covers |
|---|---|---|
| Changing source, tests or configuration | [Code and repository](code-practices.html) | Program output, diagnostics and generated files |
| Changing runtime cost or claiming performance | [Efficient implementation](performance.html) | Efficient defaults; claims scoped to a stated workload |
| Running tests, builds or other expensive jobs | [Execution and shared resources](execution.html) | Execution routes, budgets, usage records, supervision and cleanup |
| Assigning work or editing in parallel | [Ownership and delivery](delivery.html) | Assignment scope, coordination, parallel work and blockers |
| Reporting completion or blockers | [Handoffs](handoffs.html) | Completion and blocker reports, durable evidence, receiving a handoff |
| Staging, committing or rewriting history | [Git](git.html) | Deliverables and validation, commit messages, shared checkouts |

## Documentation and writing

| Before… | Read… | It covers |
|---|---|---|
| Creating, moving or retiring a document | [Documentation system](documentation-system.html) | One canonical home per fact, chronology, publishing and agent entrypoints |
| Writing or reviewing a page | [Page design and review](page-design.html) | Section purpose, figure placement, homepages, build-sheet pages and slides |
| Explaining something | [Explanations](explanations.html) | Reading order, optional layers, naming and honest claims |
| Quoting a measured number | [Measurements and evidence](evidence.html) | What a measured claim needs, when to rerun, ledgers and experiment records |
| Drawing a figure | [Figures and access](figures.html) | Choosing a representation, comparisons, interaction and accessibility |
| Deriving mathematics | [Mathematics](math.html) | Known constructions, notation, worked examples and rendering |
| Excerpting code | [Code excerpts and diagrams](code-excerpts.html) | Verified excerpts with real line numbers and data-backed diagrams |

## Experiments

| Before… | Read… | It covers |
|---|---|---|
| Designing or running an experiment | [Experiment workflow](experiment-workflow.html) | Keeping experiments small, investigation or qualification, baselines, stopping and required content; final runs only for learned models |
| Choosing checks or interpreting failures | [Proportionate verification](experiment-verification.html) | Evidence gaps, application logic, numerical correctness, regression gates and failures |

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
