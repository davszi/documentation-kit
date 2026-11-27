+++
title = "Engineering practices"
brand_sub = "code · execution · delivery · Git"
description = "Why the kit's six engineering guides exist, what each requires, and what following them looks like."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css", "engineering-practices/engineering-practices.css"]
toc = [["Routes", "#routes"], ["Code", "#code"], ["Supporting code", "#supporting-code"], ["Compatibility", "#compatibility"], ["Performance", "#performance"], ["Execution", "#execution"], ["Cleanup", "#supervision"], ["Delivery", "#delivery"], ["Decisions", "#decisions"], ["Handoffs", "#handoffs"], ["Git", "#git"], ["Shared checkout", "#shared-checkout"]]
page_only = "Explains the engineering guides; they are the records, in rules/engineering/."
+++

# Engineering practices

<section class="card" id="routes">

## Each engineering guide governs one kind of action

<p class="bs-lead">Find the action you are about to take: its row names what to read before it, and the chapter here that explains why.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Engineering guides by action">

| Before… | Read… | Explained in |
|---|---|---|
| Changing source, tests or repository configuration | [Code and repository practices](code-practices.html) and the owning project topic or development guide | [Code](#code), [Compatibility](#compatibility) |
| Building tooling, a harness or other supporting code | `docs/CAPABILITY_MAP.md`, then [Name the need first](code-practices.html#name-the-need-first) | [Supporting code](#supporting-code) |
| Changing runtime cost or making performance claims | [Efficient implementation](performance.html) and the project's workload/acceptance contract | [Performance](#performance) |
| Running tests, builds, benchmarks or other expensive jobs | [Execution and shared resources](execution.html) and the project's recorded environment and execution requirements | [Execution](#execution), [Cleanup](#supervision) |
| Discussing a feature, an experiment or a change of direction before work starts | [Discussion before the work](delivery.html#discussion-before-the-work) | [Discuss, build, record](discuss-build-record.html#discuss) |
| Assigning work, coordinating contributors or editing in parallel | [Ownership and delivery](delivery.html) | [Delivery](#delivery), [Decisions](#decisions) |
| Reporting completion or blockers, handing off work or integrating a handoff | [Handoffs and progress reports](handoffs.html) | [Handoffs](#handoffs) |
| Staging, committing or rewriting Git history | [Git changes and shared checkouts](git.html) and the project's recorded validation requirements | [Git](#git), [Shared checkout](#shared-checkout) |
| Changing anything under `.docs-kit/` or moving its pin | [The shared kit submodule](git.html#the-shared-kit-submodule) | [Git](#git) |

</div>

These are the engineering rows of the router that `init` writes into a project's `AGENTS.md`, in its words; the rows for experiments, records and pages lead to [Experiments](experiments.html), [Records and documents](documentation-practices.html) and [Writing pages](writing-practices.html). The guides state shared principles, and each project adds its own controls, workloads, thresholds and records. Each chapter below says why a guide asks for something and shows how it works; the linked guide keeps the exact wording.

</section>

<section class="card" id="code">

## What other programs read, regenerate or load has one source, and changes there

<p class="bs-lead">Consumed output is an interface, a generated file changes at its generator, and a dependency is declared where the setup installs it.</p>

<figure id="fig-one-source">
<div class="ep-fig ep-src" role="img" aria-label="Three rows. Consumed output: the agreed output format feeds stdout and stderr, which another program parses line by line; a diagnostic printed there is read as data, so diagnostics go through the project's logging. Generated file: the source or generator writes the generated file, which the build and readers use; a hand edit is undone by the next regeneration, so the change goes into the source and the outputs are regenerated. Dependency: the dependency file is installed into the environment, from which the code imports; a library loaded from an untracked checkout or build output is missing after a fresh clone, so every dependency is declared.">
<div class="ep-src-row bs-teal"><span class="ep-tag">Consumed output</span><div class="ep-box"><b>Agreed output format</b><small>an interface</small></div><i class="ep-to"></i><div class="ep-box"><b>stdout · stderr</b></div><i class="ep-to"></i><div class="ep-box"><b>Another program</b><small>parses every line</small></div><div class="ep-x"><span>✕</span>A diagnostic printed here is read as data. Diagnostics go through the project's logging.</div></div>
<div class="ep-src-row bs-violet"><span class="ep-tag">Generated file</span><div class="ep-box"><b>Source or generator</b><small>where the change goes</small></div><i class="ep-to"></i><div class="ep-box"><b>Generated file</b><small>regenerated after the change</small></div><i class="ep-to"></i><div class="ep-box"><b>Build and readers</b></div><div class="ep-x"><span>✕</span>A hand edit is undone by the next regeneration and leaves source and output disagreeing.</div></div>
<div class="ep-src-row bs-orange"><span class="ep-tag">Dependency</span><div class="ep-box"><b>Dependency file</b><small>every dependency declared</small></div><i class="ep-to"></i><div class="ep-box"><b>Environment</b><small>installed from that file</small></div><i class="ep-to"></i><div class="ep-box"><b>The code</b><small>imports from the environment</small></div><div class="ep-x"><span>✕</span>A library loaded from an untracked checkout or build output is missing after a fresh clone.</div></div>
</div>
<figcaption><b>Figure 1.</b> Three things others depend on, each with its one source and the shortcut that breaks it. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Each row of [Figure 1](#fig-one-source) has a reader the author does not see: a parser, the next regeneration, a fresh clone. The crossed shortcut in each row works on the author's machine today and fails for that reader later, which is why the guide moves every change to the source on the left. A consumed format changes only through an agreed interface change.

Two other forms also count as declared: a vendored copy tracked in the repository, with its license and a notice of its source and version, and a Git submodule pinned to a commit. The environment itself may sit in an ignored folder. The test is a fresh clone: the setup guide, followed from one, produces the environment the project runs, and when the two differ the dependency file or the guide is corrected. A run names its environment by package versions and file hashes instead of copying it, and a project keeps one environment per toolchain; a replacement comes with a proposal to delete the old one.

Guide: [Logging and program output](code-practices.html#logging-and-program-output) · [Generated files](code-practices.html#generated-files) · [Dependencies](code-practices.html#dependencies)

</section>

<section class="card" id="supporting-code">

## Supporting code starts from a need written without the task, looked up in the capability map

<p class="bs-lead">Before building a harness, a judge or another tool, write the need in one sentence, look it up, and let the person decide anything the map does not already answer.</p>

<figure id="fig-need">
<div class="bs-flow" role="img" aria-label="Step one: write the need in one sentence that does not mention the experiment or task, such as record what a native run did. Step two: read the project's capability map. If the map lists the need as exists, use that code. If the need is partly met or not listed, add it to the needs seen but not built with the date and where it came up, stop building, and bring the person three options with what each would take and leave out: build it once as a tool in the tooling tree, build the minimum inside the experiment, or do not build it. Building is the person's decision; noticing the need is the agent's duty. The decision is recorded beside the need, and a need to be built becomes a row, missing until its code exists.">
<div class="bs-node bs-teal"><span class="bs-label">1 · Name</span><b>The need in one sentence</b><ul><li>without the experiment or task at hand</li><li>such as “record what a native run did”</li></ul></div>
<div class="bs-arrow"><span>look up</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Read</span><b>The capability map</b><ul><li><code>docs/CAPABILITY_MAP.md</code></li><li>needs with their code, state and importers</li></ul></div>
<div class="bs-arrow"><span>state</span></div>
<div class="bs-stack">
<div class="bs-node bs-green"><span class="bs-label"><code>exists</code></span><b>Use that code</b></div>
<div class="bs-node bs-orange"><span class="bs-label"><code>partly</code> or not listed</span><b>Record it, stop, ask</b><ul><li>add it to the needs seen but not built, with the date and where it came up</li><li>options for the person: a tool in the tooling tree, the minimum inside the experiment, or nothing; each with what it takes and leaves out</li></ul></div>
</div>
<div class="bs-back"><span>✕</span> Building is the person's decision; noticing the need is the agent's duty. The decision is recorded beside the need, and a need to be built becomes a row, <code>missing</code> until its code exists.</div>
</div>
<figcaption><b>Figure 2.</b> The path from a noticed need to code, or to a decision not to build. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Supporting code is code that runs, supervises, records, judges or prepares work instead of answering its question. An agent that builds it for the task in front of it writes a harness named after that task, and the next task writes another. The sentence in step 1 of [Figure 2](#fig-need) leaves the task out, so that two tasks with the same need write the same sentence and find the same row. The stop in the orange branch exists because a tool is a lasting cost that the person, not the agent, takes on. [Approval that failed open](approval-failed-open.html) is a measured case of what happens without it.

The [capability map](code-practices.html#the-capability-map) is a checked record, not a wish list. Every project sets `tooling_roots` in `docs/site/site.toml`, and lint fails when the setting is missing, when a file or folder directly under a tooling root has no row, or when the generated column is stale; [capability map settings](authoring.html#capability-map-settings) give the columns. A project without tooling sets `tooling_roots = []`: nothing is listed, so every need goes to the person, and the first one recorded starts the map.

<figure id="fig-where-code-lives">
<div class="ep-fig ep-home" role="img" aria-label="Two running experiments each hold only their own code, inputs and records, and both import a shared run harness, supervisor or judge from the project's tooling or source tree. When a second user appears, the code moves there before the second import. A finished experiment is not changed: its code is copied into the tooling tree, and the experiment keeps its copy, its links and its source pin.">
<div><div class="ep-box bs-teal"><span class="ep-tag">experiment A</span><b>Its own code, inputs and records</b></div><div class="ep-box bs-teal"><span class="ep-tag">experiment B</span><b>Its own code, inputs and records</b><small>the second user: the code moves before this import</small></div></div>
<div class="ep-link"><span>import</span></div>
<div class="ep-tree"><div class="ep-box bs-violet"><span class="ep-tag">tooling or source tree</span><b>Reused code</b><small>a run harness, a supervisor, a judge</small></div></div>
<div class="ep-box bs-muted"><span class="ep-tag">finished experiment</span><b>Keeps its copy, its links and its source pin</b></div>
<div class="ep-link is-copy"><span>copy</span></div>
</div>
<figcaption><b>Figure 3.</b> Where reused code lives. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

[Figure 3](#fig-where-code-lives) is where the code goes once it is built. An experiment's folder holds only what belongs to that experiment, so it can be read, rerun or deleted on its own. Code a second user needs moves into the tooling tree before the second import, while there is one caller to update. A finished experiment is not edited to import the moved code: its copy stays, with the [source pin](records.html#numbers-and-staleness) that its results cite.

Guide: [Where code lives](code-practices.html#where-code-lives) · [Name the need first](code-practices.html#name-the-need-first) · [The capability map](code-practices.html#the-capability-map)

</section>

<section class="card" id="compatibility">

## Refactor fully once the project owner has decided no old form is needed

<p class="bs-lead">Before changing something others may still use, ask the project owner with the evidence; on a no, update every reference and delete the old form in the same change.</p>

<figure id="fig-compatibility">
<div class="bs-flow" role="img" aria-label="Step one: check who uses the old name, path, format, API, URL or configuration key: published URLs or packages, other repositories, saved data or historical records, running jobs. Step two: ask the project owner, giving what changes and why, who uses it with evidence, what would break and whether it can be updated in the same change, and what keeping it would cost; then wait. If no compatibility is needed, refactor fully: update every caller and reference and remove the old form, with no aliases, shims, fallbacks, redirects or deprecation periods. If compatibility is kept, record why it exists and when it can be removed.">
<div class="bs-node"><span class="bs-label">1 · Check</span><b>Who uses the old form?</b><ul><li>published URLs or packages</li><li>other repositories</li><li>saved data, historical records</li><li>running jobs</li></ul></div>
<div class="bs-arrow"><span>ask</span></div>
<div class="bs-node bs-violet"><span class="bs-label">2 · Ask and wait</span><b>The project owner decides</b><ul><li>what changes and why</li><li>who uses it, with evidence</li><li>what breaks, and whether it can be updated in the same change</li><li>what keeping it costs</li></ul></div>
<div class="bs-arrow"><span>decision</span></div>
<div class="bs-stack">
<div class="bs-node bs-green"><span class="bs-label">No compatibility</span><b>Refactor fully</b><ul><li>every caller and reference updated</li><li>old form removed; no aliases, shims, fallbacks or redirects</li></ul></div>
<div class="bs-node bs-orange"><span class="bs-label">Keep it</span><b>Record it</b><ul><li>why it exists, when it can go</li></ul></div>
</div>
</div>
<figcaption><b>Figure 4.</b> Changing a name, path, format, API, URL or configuration key that others may use. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An alias or fallback looks cheap when it is added, but every later reader learns both forms, every check covers both, and nobody remembers when the old one may go; a fallback for a moved file also keeps a wrong path working by accident. So the default in [Figure 4](#fig-compatibility) is the green branch. Only the project owner knows whether a link went out to people or another repository reads the path, so the decision is theirs; the agent's part is to find the users and say what would break. When nothing outside the change uses the old form, no question is needed.

One kind of caller is deleted instead of updated: a finished probe or one-time script that nothing imports and nothing will rerun, once its result is recorded with a source pin that stands for it. Claims that rest on it become historical, and the deletion needs no separate approval.

Guide: [Refactoring over compatibility](code-practices.html#refactoring-over-compatibility)

</section>

<section class="card" id="performance">

## The normal path pays only for required work, and a timing speaks only for the path that ran it

<p class="bs-lead">Write invariant data once, batch related calls, keep evidence work opt-in, and label every timing by the workload and path it measured.</p>

<figure id="fig-claims">
<div class="ep-fig ep-lanes" role="img" aria-label="Two lanes. The normal path, which ships: invariant data such as headers, manifests, source hashes and recipes written once and referenced; batch operations, with related state read and written together; no repeated allocation or copying of large structures in hot paths. A claim about shipped performance times this path with its required work, on the declared workload, against a verified baseline, the strongest relevant cheap one. The opt-in path: checkers, observers, full per-step records, diagnostic runs and ablations. Its timings are labelled by the path they measured. Below: a quick mode, for a benchmark or validation tool whose full run exceeds about one minute, labels its coverage and does not replace the full workload, its acceptance criteria or an experiment's agreed protocol.">
<div class="ep-lane bs-teal"><span class="ep-tag">Normal path · ships</span><div class="ep-steps"><span>invariant data written once, then referenced</span><span>batched calls, related state together</span><span>no repeated copies of large structures in hot paths</span></div><div class="ep-box bs-teal"><span class="ep-tag">its timing</span><b>A shipped claim</b><small>the declared workload, this path with its required work, a verified and strong baseline</small></div></div>
<div class="ep-lane bs-violet"><span class="ep-tag">Opt-in path</span><div class="ep-steps"><span>checkers and observers</span><span>full per-step records</span><span>diagnostic runs and ablations</span></div><div class="ep-box bs-violet"><span class="ep-tag">its timing</span><b>Labelled by its path</b><small>never quoted as shipped performance</small></div></div>
<div class="ep-note"><b>Quick mode.</b> A benchmark or validation tool whose full run exceeds about one minute gets one. It labels its coverage and replaces neither the full workload, its acceptance criteria nor an experiment's agreed protocol.</div>
</div>
<figcaption><b>Figure 5.</b> What runs on the normal path, and which path each timing speaks for. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Work that repeats per step grows with every step and every run, and evidence work left in the normal path makes every normal run pay for it. The upper lane of [Figure 5](#fig-claims) is therefore kept to required work; the lower lane runs on request. These are habits applied while writing, not a separate optimisation project: waste found within the assigned scope is fixed in the current implementation. Moving code to another language is never the default answer to waste; it needs an explicit decision with the project owner.

<span id="performance-claims"></span>The same split decides what a timing proves. A run of the lower lane, or an ablation that skips required work, can differ from what ships, so a claim about shipped performance times the upper lane. A comparison also inherits its baseline's weaknesses, so the baseline is verified before the measured behavior changes, and it is the strongest relevant cheap one. A claim then reads like this, with ‹result› standing for a measured value: “on the declared workload, through the shipped load path with validation included, against the verified current baseline: ‹result›.”

What makes such a number quotable — its identity, baseline, reruns and labels — is in [numbers and staleness](records.html#numbers-and-staleness); whether the numerical code is correct at all is [proportionate verification](experiment-verification.html). The project's own records hold its workloads, thresholds and performance contracts.

Guide: [Efficient by default](performance.html#efficient-by-default) · [Workload and evidence](performance.html#workload-and-evidence)

</section>

<section class="card" id="execution">

## An expensive job runs on the project's route under an adequate budget with a stated basis

<p class="bs-lead">Read the project's execution instructions first, coordinate shared resources, and reserve from a comparable measurement or generously, saying which.</p>

<figure id="fig-execution">
<div class="bs-flow" role="img" aria-label="Before launch, read the project's execution and environment instructions, verify the executable, loaded source, inputs and environment, and use the supported entrypoint and resource controls. Then coordinate admission and adequate reservations, respecting host headroom and existing reservations; an idle host does not remove required containment. Then reserve from a sufficiently comparable successful measurement or a deliberately generous initial reservation, and state the basis; reserved capacity is not measured consumption. Do not lower an adequate budget to force admission or bypass controls with local overrides, and avoid repeated small increases after preventable memory failures.">
<div class="bs-node bs-teal"><span class="bs-label">Route</span><b>The project's way to run</b><ul><li>read its execution and environment instructions</li><li>verify executable, loaded source, inputs, environment</li><li>supported entrypoint and resource controls</li></ul></div>
<div class="bs-arrow"><span>coordinate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Shared resources</span><b>Admission without squeezing</b><ul><li>adequate reservations, coordinated</li><li>host headroom and existing reservations respected</li><li>an idle host keeps required containment</li></ul></div>
<div class="bs-arrow"><span>reserve</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Budget</span><b>Adequate, with its basis</b><ul><li>a comparable successful measurement, or</li><li>a deliberately generous first reservation: startup, compilation, children, cleanup</li><li>reserved is not measured</li></ul></div>
<div class="bs-back"><span>✕</span> Do not lower an adequate budget to force admission or bypass controls with local overrides. Avoid repeated small increases after preventable memory failures.</div>
</div>
<figcaption><b>Figure 6.</b> The steps before one expensive job starts. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A job that skips the project's route can spend its budget on the wrong executable, source or inputs, so [Figure 6](#fig-execution) starts by checking them. Squeezing a budget to get admitted does not make the job need less. And because a reservation says nothing about consumption, its basis is stated with it: “no comparable successful run exists, so this is a deliberately generous first reservation; it is reserved capacity, not measured use.” Deadlines and cleanup reserves fit the operation under the project's timing rules. A job runs alone when interference would spoil a timing or when it tests lifecycle, runaway, signal or resource-stress behaviour. The project supplies the concrete controls; reservation, usage-cache and receipt rules apply when it uses those mechanisms.

<!-- fold: experiment Reusing an earlier reservation -->

The measured use of a successful earlier run is the best basis for the next reservation, but only for the same job. Reuse it when the workload, command, checkout or source state, executable, relevant environment and its metadata, and input identity all match; name external or changing inputs and import roots explicitly, since they are easy to miss. If anything differs, make an explicit, adequate reservation again. An estimate or a limit a job failed at is not a successful measurement.

A temporary usage cache helps choose a budget and gives nobody permission to run. For a frozen run request, bind the limits before freezing it and check those same limits at launch, instead of picking replacements from a cache that may have changed. Evidential measurements are kept under [numbers and staleness](records.html#numbers-and-staleness).

<!-- /fold -->

Guide: [Choose the project's execution route](execution.html#choose-the-projects-execution-route) · [Coordinate conflicting work](execution.html#coordinate-conflicting-work) · [Select a resource budget](execution.html#select-a-resource-budget) · [Reuse successful usage records conservatively](execution.html#reuse-successful-usage-records-conservatively)

</section>

<section class="card" id="supervision">

## A job's owner reads failures from evidence and keeps ownership through cleanup

<p class="bs-lead">Record command and resource outcomes separately, stop only what you own, and confirm cleanup before releasing the reservation.</p>

<figure id="fig-supervision">
<div class="ep-fig" role="img" aria-label="A job's life on one line: admission, launch, supervision, exit, cleanup of children and temporary resources, and release of the reservation. One named owner holds the job from admission to release, past the exit. The record keeps two outcomes apart. The command outcome is what the command returned. The resource outcome rests only on actual memory-limit evidence; failed tests, a missing peak, a timeout, a failed cleanup or a change in the host's free memory are not that evidence, and an unavailable terminal peak stays unmeasured.">
<div class="ep-life">
<div class="ep-phase bs-teal"><b>Admission</b>coordinated reservation</div>
<div class="ep-phase bs-teal"><b>Launch</b>supported entrypoint</div>
<div class="ep-phase bs-teal"><b>Supervision</b>watched by its owner</div>
<div class="ep-phase bs-violet"><b>Exit</b>outcomes recorded</div>
<div class="ep-phase bs-orange"><b>Cleanup</b>children and temporary resources</div>
<div class="ep-phase bs-green"><b>Release</b>after cleanup is confirmed</div>
<div class="ep-own">one named owner, from admission to release</div>
<div class="ep-exit">↑ the exit is not the end of ownership</div>
</div>
<div class="ep-outcomes">
<div class="ep-box bs-violet"><span class="ep-tag">Command outcome</span><b>What the command returned</b><ul><li>its exit outcome: tests passed or failed</li><li>beside it in the job record: process and source identity, actual limits, observed cleanup</li></ul></div>
<div class="ep-box bs-orange"><span class="ep-tag">Resource outcome</span><b>Only from memory-limit evidence</b><ul><li>not evidence: failed tests, a missing peak, a timeout, a failed cleanup, the host's free memory</li><li>no terminal peak: memory use stays unmeasured</li></ul></div>
</div>
</div>
<figcaption><b>Figure 7.</b> One job from admission to release, and the two outcomes its record keeps apart. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

When a job fails, “it ran out of memory” is a tempting guess, and raising the budget on that guess hides the real cause. The two boxes of [Figure 7](#fig-supervision) keep the guess out: test failures alone do not establish exhaustion, so the resource outcome is written only from memory-limit evidence. The ownership bar runs past the exit because children and temporary resources outlive it; a reservation released before cleanup is confirmed leaves work behind that nobody owns. Stop only owned jobs and services, resolve uncertain ownership first, and treat failed or incomplete cleanup as a [handoff blocker](handoffs.html#reporting-blockers).

Unexpected pressure or an inadequate budget goes through the [escalation rules](delivery.html#decisions-and-blockers), and each attempt is kept with its original settings. The record scales to the work: a routine check needs the command, limits and result; a [qualification](experiment-workflow.html#choose-the-purpose) follows the project's full evidence chain and the [claim-scope rules](records.html#naming-and-honest-claims). Either way it outlives the conversation, under the [durable-record rules](handoffs.html#evidence-and-durable-records).

Guide: [Attribute failures from evidence](execution.html#attribute-failures-from-evidence) · [Own supervision and cleanup](execution.html#own-supervision-and-cleanup)

</section>

<section class="card" id="delivery">

## An assignment fixes the scope, and the owner finishes the routine work inside it

<p class="bs-lead">The brief defines the deliverable, scope, inputs, ownership, completion condition and return channel; inside it, the owner completes the routine work without asking a coordinator.</p>

A feature, an experiment or a change of direction begins earlier, with a discussion in chat and the person's yes; after the yes, the agreement is the assignment. [Discuss, build, record](discuss-build-record.html#discuss) explains that part ([discussion before the work](delivery.html#discussion-before-the-work)). This chapter starts where work is handed to an owner.

<figure id="fig-delivery">
<div class="ep-fig ep-roles" role="img" aria-label="Above, a coordinator, only when one is needed: overall goals, priorities, dependencies, questions and ownership conflicts. In the middle, three roles from left to right. The assigning agent writes the brief: deliverable and scope, required inputs, file or module ownership, completion condition, recipient and return channel. The owner completes implementation, focused checks, routine fixes, associated documentation and evidence, and any review the project requires, without separate coordinator approval. When several owners' changes meet, the integration names who combines them, who checks the integration and who lands it, under the shared Git rules. Below, the way back: reports and blockers return through the agreed return channel.">
<div class="ep-bar"><span class="ep-tag">Coordinator · only when needed</span>overall goals, priorities, dependencies, questions, ownership conflicts; not routine steps</div>
<div class="bs-flow">
<div class="bs-node bs-teal"><span class="bs-label">Assigning agent</span><b>Writes the brief</b><ul><li>deliverable and scope</li><li>required inputs</li><li>file or module ownership</li><li>completion condition</li><li>recipient and return channel</li></ul></div>
<div class="bs-arrow"><span>brief</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Owner</span><b>Completes the routine work</b><ul><li>implementation</li><li>focused checks and routine fixes</li><li>documentation and evidence</li><li>any review the project requires</li></ul></div>
<div class="bs-arrow"><span>changes</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Integration</span><b>Named for several owners</b><ul><li>who combines the changes</li><li>who checks the integration</li><li>who lands it, under the Git rules</li></ul></div>
</div>
<div class="ep-bar is-back"><span class="ep-tag">Return channel</span>reports and blockers go back the way the brief names</div>
</div>
<figcaption><b>Figure 8.</b> Who does what in delegated or parallel work. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

A vague assignment leaves the owner guessing where the work stops and where the result goes, and leaves parallel owners guessing whose files are whose. The brief on the left of [Figure 8](#fig-delivery) settles that up front, scaled to the work: a small, self-contained task can use a short brief. In return the owner needs no separate approval for routine work inside the scope, so the coordinator above stays free for what one owner cannot settle alone. A brief that says only “have a look at the failing export and fix whatever you find” names no scope, no completion condition and no return channel.

Page work for people is one recurring assignment. Where the runtime supports delegation, page work larger than a small sync goes to a separate page agent once the record is finished. Its brief also names the guides to read, because a delegated agent knows only its brief, and the delegating agent looks at the captures itself before calling the page done. [Delegating a page for people](delivery.html#delegating-a-page-for-people) lists the brief; [record first](documentation-practices.html#record-first) shows where it sits among the documentation steps.

Guide: [Discussion before the work](delivery.html#discussion-before-the-work) · [Assigning work](delivery.html#assigning-work) · [Owner responsibility](delivery.html#owner-responsibility) · [Delegating a page for people](delivery.html#delegating-a-page-for-people) · [Coordination and integration](delivery.html#coordination-and-integration)

</section>

<section class="card" id="decisions">

## Changes to the agreement go back for a decision, and an open question is written down with the case against

<p class="bs-lead">Routine choices are made and reported; changes to goals, design, scope or acceptance are escalated; a question the person has not answered goes into the open owner before work stops.</p>

<figure id="fig-decisions">
<div class="ep-fig ep-sort" role="img" aria-label="On the left, three kinds of thing that come up during work. A routine choice within the agreed scope is made and reported. A change to agreed goals, design, scope or acceptance requirements, a next approach that exceeds agreed scope or limits, or reopening deferred work is escalated for a decision while independent authorized work continues. A resource-limit hit or a recurring unexplained failure is reported. An arrow leads from the escalated kind to the right: when the person has not answered before work stops or completion is reported, the question is written into the open owner as an unresolved choice, routed from OPEN.md. It holds the question, the options, the recommendation, the strongest case against it, and what waits on the answer. An option that rests on a number names the measurement; one that rests on an unmeasured premise says so.">
<div class="ep-bins">
<div class="ep-box bs-green"><span class="ep-tag">Make and report</span><b>A routine choice within the agreed scope</b></div>
<div class="ep-box bs-orange"><span class="ep-tag">Escalate and wait</span><b>A change to goals, design, scope or acceptance</b><small>also a next approach beyond agreed scope or limits, and reopening deferred work; independent authorized work continues</small></div>
<div class="ep-box bs-red"><span class="ep-tag">Report</span><b>A resource-limit hit or a recurring unexplained failure</b></div>
</div>
<div class="ep-link"><span>not answered<br>before stopping</span></div>
<div class="ep-entry"><div class="ep-entry-head">Open owner · unresolved choice · routed from <code>OPEN.md</code></div><dl>
<dt>Question</dt><dd>what the person has to decide</dd>
<dt>Options</dt><dd>each resting on a named measurement, or saying its premise is unmeasured</dd>
<dt>Recommendation</dt><dd>the agent's pick</dd>
<dt class="is-new">Case against</dt><dd>the strongest one, against that pick</dd>
<dt>Waits on it</dt><dd>what cannot go on until the answer</dd>
</dl></div>
</div>
<figcaption><b>Figure 9.</b> Where something that comes up during work goes, and what a question for the person holds when it is written down. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

An owner's autonomy covers routine work inside the agreement, not the agreement itself. An owner who quietly widens scope or relaxes an acceptance requirement leaves everyone else planning against terms that no longer hold, so the middle box of [Figure 9](#fig-decisions) goes back to the person. Limit hits and recurring failures are reported because they suggest the agreed approach may not hold. While a decision is pending, explicit stops and required approvals are respected and independent authorized work goes on.

The unresolved-choice card exists because a question asked only in chat is lost when the chat ends. The strongest case against the recommendation is part of it so that the person sees what the yes would cost before giving it, not only why the agent prefers it. A delegated owner sends its question through the return channel, and the agent that reports to the person records it; once answered, the answer goes where the work continues and the entry is deleted when nothing waits on it. Only questions that change the work are asked.

<!-- fold: dead-end Freezing everything around a conflict -->

When parallel work collides, stopping everything nearby also stops work that was never part of the collision. The guide restricts only what actually conflicts: keep other contributors' changes, agree on overlapping edits, and leave alone what running work depends on, its source, inputs, dependencies, execution settings and outputs. Work done alone stays in the project's checkout on its current branch; a separate branch or worktree is for other work changing the same repository at the same time, a running job that depends on the files, a project workflow that asks for one, or a person who asks.

<!-- /fold -->

Guide: [Decisions and blockers](delivery.html#decisions-and-blockers) · [Parallel work](delivery.html#parallel-work)

</section>

<section class="card" id="handoffs">

## A report leads with the outcome and says how each claim is known

<p class="bs-lead">Separate work completed from behavior verified, name files by full path, link the page that covers the work, and send the report through the agreed return channel.</p>

<figure id="fig-report">
<div class="ep-fig ep-doc" role="img" aria-label="An example completion report, one line per part, each tagged. Outcome: the export fix is delivered, with a link. Changed: the export writer, named by its full path from the repository root. Checks run: the focused export check passed; skipped: the full suite, outside this scope. Executed check: the failing case now passes. Source inspection and inference: other formats are unaffected. Waits on the person: one unresolved choice, recorded in the open owner. Page: the result in a few lines with a link to the page section that covers it. Next: the integration owner lands it.">
<div class="ep-doc-head">An illustrative completion report, not taken from a real project</div>
<div class="ep-doc-line bs-teal"><span class="ep-tag">outcome</span><span>The export fix is delivered in ‹link›.</span></div>
<div class="ep-doc-line bs-teal"><span class="ep-tag">what and where</span><span>Changed <code>src/export/writer.py</code>, named by its full path from the repository root.</span></div>
<div class="ep-doc-line bs-violet"><span class="ep-tag">checks</span><span>Focused export check: passed. Skipped: the full suite, outside this scope.</span></div>
<div class="ep-doc-line bs-green"><span class="ep-tag">executed check</span><span>The failing case now passes.</span></div>
<div class="ep-doc-line bs-orange"><span class="ep-tag">inspected · inferred</span><span>From source inspection: other formats are unaffected.</span></div>
<div class="ep-doc-line bs-red"><span class="ep-tag">waits on the person</span><span>One unresolved choice, recorded in the open owner.</span></div>
<div class="ep-doc-line bs-blue"><span class="ep-tag">page</span><span>The result in a few lines; the detail is in ‹page›, section ‹section›.</span></div>
<div class="ep-doc-line bs-muted"><span class="ep-tag">next</span><span>The integration owner lands it.</span></div>
</div>
<figcaption><b>Figure 10.</b> A completion report with each line tagged by its part and by how its claim is known. This illustrative example is authored in the page source and contains no measured results.</figcaption>
</figure>

The recipient of a report has to decide what to trust and what to do next, usually without rerunning the work. “All done, the tests should pass” leaves them unable to tell finished work from verified behavior. The tags in [Figure 10](#fig-report) make the difference visible: a claim is marked as coming from an executed check, from source inspection or from an inference. A full path from the repository root spares the reader a search. When a rendered page covers the work, the report does not repeat it: it gives the result in a few lines and links the page and its section, and keeps only what waits on the person.

A report is a pointer, not an archive: results and reproduction steps go into their owning records, and chat is never the only copy of evidence later work needs. A blocker report takes the same return channel and says what is blocked, the decisive evidence, what was tried and what decision is needed; a message in another chat does not show that the recipient got it. The receiver checks a consequential claim's evidence and scope before relying on it, and names the next owner when responsibility moves.

Before reporting, the work deletes the scratch files it created, without asking: drafts, captures for a review by eye, temporary test folders, anything untracked that no record, claim, person or delegating agent still needs. A capture someone is still to look at stays until seen. Run output, tracked files, working documents, a build's fixed output folder and a capture used as a figure are never scratch, and a record never cites a scratch file by path or hash, so nothing breaks when it goes.

Guide: [Reporting completion](handoffs.html#reporting-completion) · [Scratch files](handoffs.html#scratch-files) · [Reporting blockers](handoffs.html#reporting-blockers) · [Evidence and durable records](handoffs.html#evidence-and-durable-records) · [Receiving a handoff](handoffs.html#receiving-a-handoff)

</section>

<section class="card" id="git">

## Each commit holds one logical deliverable, reviewed whole and checked as committed

<p class="bs-lead">Stage only what belongs, review the complete proposed commit, explain what changed and why, and run the checks on the committed state before pushing.</p>

<figure id="fig-git">
<div class="bs-flow" role="img" aria-label="Inspect the branch, working changes and staging area and identify what belongs to the deliverable. Stage explicit paths or selected changes, preserving unrelated working and staged changes. Review the complete proposed commit, including deletions and changes staged earlier, and confirm the file versions match the source state the recorded checks covered. A commit does not establish that its tests passed; run the project's checks on the committed state before pushing. The optional pre-push gate runs them before a push and refuses it while tracked files have uncommitted changes.">
<div class="bs-node bs-teal"><span class="bs-label">Inspect</span><b>Branch, changes, staging area</b><ul><li>what belongs to the deliverable</li></ul></div>
<div class="bs-arrow"><span>stage</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Stage</span><b>Explicit paths or selected changes</b><ul><li>everything only when every change belongs</li><li>unrelated changes preserved</li></ul></div>
<div class="bs-arrow"><span>review</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Review</span><b>The complete proposed commit</b><ul><li>deletions and earlier staged changes too</li><li>the same file versions the checks covered</li></ul></div>
<div class="bs-back"><span>✕</span> A commit does not show that its tests passed. Run the checks on the committed state before pushing; the optional <a href="validation.html#one-command-and-a-pre-push-gate">pre-push gate</a> does so and refuses a push while tracked files have uncommitted changes.</div>
</div>
<figcaption><b>Figure 11.</b> Preparing one commit. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

Later readers inspect, revert and cite commits one at a time, so the unit is one logical deliverable — a fix, a feature, an experiment or one coherent stage of a refactor — with its small edits folded in and its tests, documentation and chronology included under the [documentation rules](documentation-system.html#rules-for-changes-and-chronology). Separately verified stages stay separate when that verification means something. [Figure 11](#fig-git) ends with a review of the whole commit, because staging everything can sweep in changes that were already there, and puts the checks after it, because a check that passed with a file untracked can fail on the commit. A failed or negative outcome can still be a sound deliverable when it is documented accurately.

The message has a short imperative subject and a body that says what changed and why, with validation results when they help; no Conventional Commits prefix:

```text
Keep progress messages out of the export stream

The export command printed progress on stdout, which the
import tool parses. Progress now goes through the project's
logger, and stdout carries only the export format.

The export round-trip check passed.
```

<!-- fold: dead-end Committing inside the kit submodule -->

A fix made inside a project's `.docs-kit` folder looks finished: the project builds and the pin moves. But that commit exists only on that disk, so every fresh clone and CI checkout fails to fetch it. Kit changes go to the kit's own repository first, with its checks and review, are pushed there, and the project then moves its pin to the pushed commit as a deliverable of its own, following the migration guide. `docsite.py lint` fails when the pinned commit is on none of the kit's remote branches; a tag does not count, because a local tag looks like a pushed one.

<!-- /fold -->

Guide: [Deliverables and validation](git.html#deliverables-and-validation) · [Commit messages](git.html#commit-messages) · [Preparing a commit](git.html#preparing-a-commit) · [The shared kit submodule](git.html#the-shared-kit-submodule)

</section>

<section class="card" id="shared-checkout">

## In a shared checkout, one owner holds staging from final review to commit

<p class="bs-lead">Git locks only while a command runs; protect the interval between reviewing a commit and creating it, or prepare the commit in isolation and reconcile afterwards.</p>

<figure id="fig-shared-checkout">
<div class="ep-fig" role="img" aria-label="Two contributors share one checkout. Time runs left to right. The first makes its final review of the staged changes. Then comes an interval that no lock covers, because Git holds its lock only while a single command runs. In it, the other contributor stages its own file. The first then commits, and the other file enters the commit unreviewed. Below, the two answers: one owner holds staging and committing for the whole operation, with no concurrent staging between final review and commit; or, when that cannot be established, the commit is prepared and verified in an isolated staging area or worktree and reconciled with the shared staging area on landing.">
<div class="ep-gap">
<span class="ep-who is-you">Committing owner</span>
<span class="ep-who is-other">Another contributor</span>
<div class="ep-ev e1" data-who="Committing owner"><b>final review</b>of the staged changes</div>
<div class="ep-ev e2 is-open" data-who="Committing owner"><b>no lock</b>between the two commands</div>
<div class="ep-ev e3 is-lock" data-who="Another contributor"><b>stage</b>its own file</div>
<div class="ep-ev e4 is-lock is-bad" data-who="Committing owner"><b>commit</b>the other file enters unreviewed</div>
</div>
<div class="ep-key"><span><i class="k-lock"></i>Git holds its lock</span><span><i class="k-open"></i>the interval nothing protects</span></div>
<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Interval protected</span><b>One owner commits in place</b><ul><li>one owner for staging and committing, for the whole operation</li><li>no concurrent staging from final review to commit</li></ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Cannot be protected</span><b>Prepare in isolation, then reconcile</b><ul><li>prepare and verify in an isolated staging area or worktree</li><li>on landing, keep others' staged intent and working changes</li><li>settle overlapping paths with their owner, then verify the status</li></ul></div>
</div>
</div>
<figcaption><b>Figure 12.</b> The interval between review and commit in a shared checkout, and the two ways to close it. This illustrative diagram is authored in the page source and contains no measured results.</figcaption>
</figure>

The hatched box in [Figure 12](#fig-shared-checkout) is why a careful review is not enough on its own: Git's locks protect single commands, not the time between them, and whatever another contributor stages in that time enters the commit unreviewed. A staging-area lock does not protect working files either, so overlapping file edits are coordinated separately.

When something unrelated has entered a commit anyway, it is not repaired quietly. Temporary checkpoints are consolidated only in isolated, unshared history; history another contributor or an active job uses is preserved. Record the affected commit, tell the owner of those changes through the agreed channel, and agree on recovery before rewriting anything someone else may be using.

Guide: [Sharing a checkout](git.html#sharing-a-checkout) · [History and recovery](git.html#history-and-recovery)

</section>
