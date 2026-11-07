+++
title = "Engineering practices"
brand = "Documentation kit"
brand_sub = "code · execution · delivery · Git"
description = "What the kit's six engineering guides require and which action each one governs."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Routes", "#routes"], ["Code", "#code"], ["Efficiency", "#performance"], ["Execution", "#execution"], ["Delivery", "#delivery"], ["Handoffs", "#handoffs"], ["Git", "#git"]]
+++

# Engineering practices

<section class="card" id="routes">

## Each engineering guide governs one kind of action

<p class="bs-lead">Find the action you are about to take; its row names the guide that governs it.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Engineering guides by action">

| Before… | Read… | It covers |
|---|---|---|
| Changing program output or a generated file | [Code and repository practices](code-practices.html) | Diagnostics and consumed output; changing generated files at their source |
| Writing code on a hot path or claiming a speed-up | [Efficient implementation](performance.html) | Routine efficiency; measuring the declared workload and path |
| Running an expensive job on shared resources | [Execution and shared resources](execution.html) | Execution route, coordination, budgets, usage records, failure attribution, cleanup |
| Delegating work or editing in parallel | [Ownership and delivery](delivery.html) | Assignments, owner responsibility, integration, parallel work, escalation |
| Reporting completion or a blocker, or receiving a handoff | [Handoffs and progress reports](handoffs.html) | Report contents, return channel, durable records, checking received claims |
| Staging, committing or rewriting history | [Git changes and shared checkouts](git.html) | Commit scope and messages, staging, shared checkouts, recovery |

</div>

The guides state shared principles. Each project adds its own concrete controls, workloads, thresholds and required records.

</section>

<section class="card" id="code">

## Consumed output is an interface, and a generated file changes at its source

<p class="bs-lead">Keep diagnostics out of streams other programs read, and make changes in the source or generator, then regenerate.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">stdout · stderr</span><h3>Output another program reads</h3><ul>
<li>Use the project's logging conventions for diagnostics.</li>
<li>Treat consumed output as an interface.</li>
<li>Keep diagnostics from corrupting that stream.</li>
<li>Preserve its format unless an interface change is agreed.</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">Generated file</span><h3>Output a generator writes</h3><ul>
<li>Identify the source or generator first.</li>
<li>Make the change there.</li>
<li>Regenerate the affected outputs.</li>
<li>Keep the project's rules for which outputs are tracked or ignored.</li>
</ul></div>
</div>

Full guide: [Code and repository practices](code-practices.html) · [Logging and program output](code-practices.html#logging-and-program-output) · [Generated files](code-practices.html#generated-files)

</section>

<section class="card" id="performance">

## Efficient code is the default, and a performance claim measures the path it names

<p class="bs-lead">Avoid routine waste as you write; before you claim performance, measure the declared workload and execution path.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Every implementation</span><h3>Avoid routine waste</h3><ul>
<li>Write invariant data, such as headers and manifests, once and reference it.</li>
<li>Batch related reads and writes where the API allows.</li>
<li>Keep checkers, observers and full per-step records opt-in, outside the normal path.</li>
<li>Avoid repeated allocation and copying of large structures in hot paths.</li>
<li>Fix waste you find within your assigned scope.</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">Every performance claim</span><h3>Measure what the claim covers</h3><ul>
<li>Shipped-performance claims use the shipped path with its required work.</li>
<li>Label diagnostic and ablation timings by the paths they measure.</li>
<li>Verify the baseline before changing measured behavior.</li>
<li>Compare against the strongest relevant cheap baseline.</li>
<li>A quick mode labels its coverage and does not replace the full workload.</li>
</ul></div>
</div>

Moving code to another language requires an explicit decision with the project owner. It is never the default response to waste.

Full guide: [Efficient implementation](performance.html) · [Efficient by default](performance.html#efficient-by-default) · [Workload and evidence](performance.html#workload-and-evidence)

</section>

<section class="card" id="execution">

## An expensive job runs on the project's route, under a stated budget, with an owner through cleanup

<p class="bs-lead">Read the project's execution instructions first, reserve resources on evidence, and keep ownership until children and temporary resources are cleaned up.</p>

<figure id="fig-execution">
<div class="bs-flow" role="img" aria-label="Before launch, use the project's execution route and verify the executable, source, inputs and environment. Then coordinate an adequate, stated reservation. The owner supervises the job and confirms cleanup before releasing the reservation. Estimates and failed bounds never count as successful measurements.">
<div class="bs-node bs-teal"><span class="bs-label">Before launch</span><b>The project's execution route</b><ul><li>Verify executable, loaded source, inputs and environment</li><li>Use the supported entrypoint and resource controls</li><li>Meet admission, review and attendance requirements</li></ul></div>
<div class="bs-arrow"><span>reserve</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Shared resources</span><b>An adequate, stated budget</b><ul><li>Coordinate admission; respect headroom and existing reservations</li><li>Use a comparable successful measurement, or reserve generously</li><li>State the basis; reserved is not measured</li></ul></div>
<div class="bs-arrow"><span>run</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Owned job</span><b>Supervision through cleanup</b><ul><li>Record command and resource outcomes separately</li><li>Stop only owned jobs and services</li><li>Confirm cleanup before releasing the reservation</li></ul></div>
<div class="bs-back"><span>×</span> Estimates and failed bounds are not successful measurements. Timeouts and missing peaks do not measure memory needs.</div>
</div>
<figcaption><b>Figure 1.</b> The guide's sequence for one expensive job. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

Do not lower an adequate budget to force admission or bypass controls with local overrides. Reuse a successful reservation only when the workload, command, source state, executable, environment and inputs match.

Full guide: [Execution and shared resources](execution.html) · [Select a resource budget](execution.html#select-a-resource-budget) · [Own supervision and cleanup](execution.html#own-supervision-and-cleanup)

</section>

<section class="card" id="delivery">

## The assigned owner finishes routine work and escalates changes to the agreement

<p class="bs-lead">An assignment sets the scope and completion condition; routine work inside it needs no separate coordinator approval.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Within the agreed scope</span><h3>The owner completes</h3><ul>
<li>Implementation</li>
<li>Focused checks and routine fixes</li>
<li>Associated documentation and evidence</li>
<li>Any review the project requires</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Beyond the agreement</span><h3>Report it or get a decision</h3><ul>
<li>Changes to agreed goals, design, scope or acceptance requirements</li>
<li>Ownership conflicts, resolved with the affected owners</li>
<li>Resource-limit hits and recurring unexplained failures</li>
<li>A next approach that exceeds agreed scope or limits</li>
<li>Reopening deferred work</li>
</ul></div>
</div>

An assignment names the deliverable, scope, required inputs, file or module ownership, completion condition, recipient and return channel. In parallel work, preserve others' changes and restrict work only around the actual conflict.

Full guide: [Ownership and delivery](delivery.html) · [Assigning work](delivery.html#assigning-work) · [Decisions and blockers](delivery.html#decisions-and-blockers)

</section>

<section class="card" id="handoffs">

## A report leads with the outcome and says how each claim is known

<p class="bs-lead">Distinguish work completed from behavior verified, and send the report through the agreed return channel.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Outcome and changes</h3><p>State the outcome first, then what changed and where.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Checks</h3><p>Checks actually run, their results and relevant skipped checks.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Limits</h3><p>Failures, limitations and unresolved questions.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Links</h3><p>The delivered changes and the owning records.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Next owner</h3><p>The next owner and action, when further work remains.</p></div>
</div>

Say whether each claim comes from an executed check, source inspection or an inference. Chat and temporary files must not be the only copy of evidence later work needs. Before relying on a consequential claim you receive, check its evidence and scope.

Full guide: [Handoffs and progress reports](handoffs.html) · [Reporting completion](handoffs.html#reporting-completion) · [Receiving a handoff](handoffs.html#receiving-a-handoff)

</section>

<section class="card" id="git">

## Each commit holds one logical deliverable, reviewed as a whole before it is created

<p class="bs-lead">Stage only what belongs, review the complete proposed commit, and preserve everyone else's changes.</p>

<figure id="fig-git">
<div class="bs-flow" role="img" aria-label="Inspect the branch, working changes and staging area. Stage explicit paths or selected changes. Review the complete proposed commit, including deletions and earlier staged changes. Creating a commit does not establish that its tests passed.">
<div class="bs-node bs-teal"><span class="bs-label">Inspect</span><b>Branch, changes, staging area</b><ul><li>Check the current branch</li><li>Read working changes and the staging area</li><li>Identify what belongs to the deliverable</li></ul></div>
<div class="bs-arrow"><span>stage</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Stage</span><b>Explicit paths or selected changes</b><ul><li>Stage everything only when every change belongs</li><li>Preserve unrelated working and staged changes</li></ul></div>
<div class="bs-arrow"><span>review</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Review</span><b>The complete proposed commit</b><ul><li>Include deletions and changes staged before you started</li><li>Match file versions to the source state the checks covered</li></ul></div>
<div class="bs-back"><span>×</span> Creating a commit does not establish that its tests passed or that its acceptance requirements were met.</div>
</div>
<figcaption><b>Figure 2.</b> The guide's steps for preparing one commit. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

Write a short imperative subject and a body that explains what changed and why, without Conventional Commits prefixes. In a shared checkout, one owner stages and commits; if that interval cannot be protected, prepare the commit in an isolated staging area or worktree.

Full guide: [Git changes and shared checkouts](git.html) · [Commit messages](git.html#commit-messages) · [Sharing a checkout](git.html#sharing-a-checkout)

</section>
