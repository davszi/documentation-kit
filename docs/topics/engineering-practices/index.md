+++
title = "Engineering practices"
brand = "Documentation kit"
brand_sub = "code · execution · delivery · Git"
description = "Why the kit's six engineering guides exist, what each requires, and what following them looks like."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Routes", "#routes"], ["Code", "#code"], ["Compatibility", "#compatibility"], ["Efficiency", "#performance"], ["Claims", "#performance-claims"], ["Execution", "#execution"], ["Cleanup", "#supervision"], ["Delivery", "#delivery"], ["Decisions", "#decisions"], ["Handoffs", "#handoffs"], ["Git", "#git"], ["Shared checkout", "#shared-checkout"]]
page_only = "Explains the engineering guides; they are the records, in rules/engineering/."
+++

# Engineering practices

<section class="card" id="routes">

## Each engineering guide governs one kind of action

<p class="bs-lead">Find the action you are about to take; its row names the guide that governs it and the chapters here that explain it.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Engineering guides by action">

| Before… | Read… | It covers | Explained in |
|---|---|---|---|
| Changing program output, a generated file or an interface others use | [Code and repository practices](code-practices.html) | Diagnostics and consumed output; changing generated files at their source; refactoring instead of keeping old forms | [Code](#code), [Compatibility](#compatibility) |
| Writing code on a hot path or claiming a speed-up | [Efficient implementation](performance.html) | Routine efficiency; measuring the declared workload and path | [Efficiency](#performance), [Claims](#performance-claims) |
| Running an expensive job on shared resources | [Execution and shared resources](execution.html) | Execution route, coordination, budgets, usage records, failure attribution, cleanup | [Execution](#execution), [Cleanup](#supervision) |
| Delegating work or editing in parallel | [Ownership and delivery](delivery.html) | Assignments, owner responsibility, integration, parallel work, escalation | [Delivery](#delivery), [Decisions](#decisions) |
| Reporting completion or a blocker, or receiving a handoff | [Handoffs and progress reports](handoffs.html) | Report contents, return channel, durable records, checking received claims | [Handoffs](#handoffs) |
| Staging, committing or rewriting history | [Git changes and shared checkouts](git.html) | Commit scope and messages, staging, shared checkouts, recovery | [Git](#git), [Shared checkout](#shared-checkout) |

</div>

The guides state shared principles. Each project adds its own concrete controls, workloads, thresholds and required records. Each chapter below says why a guide asks for something, shows the mechanism and gives an illustrative example; folds hold the remaining detail, and the linked guide keeps the exact wording.

</section>

<section class="card" id="code">

## Consumed output is an interface, and a generated file changes at its source

<p class="bs-lead">Keep diagnostics out of streams other programs read, and change a generated file in its source or generator, then regenerate.</p>

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
<li>Follow the project's toolchain, reproducibility and validation requirements, and its rules for which outputs are tracked or ignored.</li>
</ul></div>
</div>

When another program reads stdout or stderr, every line in that stream is input to it. A diagnostic written there corrupts that input, so the guide treats consumed output as an interface and preserves its format unless an interface change is agreed. A generated file has the opposite problem: its content comes from somewhere else. Without changing it at the source or generator, the next regeneration can undo a hand edit and leave the source and its output disagreeing.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Patch the generated file</h3><p>A wrong default appears in a generated configuration file. The fix is typed into that file directly. The generator's input still holds the old value.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Fix the source, then regenerate</h3><p>The same wrong default is traced to the generator's input. The fix goes there, the affected outputs are regenerated, and the project's rules decide which of them are tracked.</p></div>
</div>

<!-- fold: dead-end Printing diagnostics on the consumed stream -->

Progress lines or warnings on stdout look harmless while developing, but a program that parses that stream reads them as data. The guide routes diagnostics through the project's logging conventions instead and changes the consumed format only through an agreed interface change.

<!-- /fold -->

Full guide: [Code and repository practices](code-practices.html) · [Logging and program output](code-practices.html#logging-and-program-output) · [Generated files](code-practices.html#generated-files)

</section>

<section class="card" id="compatibility">

## Refactor fully once the owner has decided no old form is needed

<p class="bs-lead">Before changing something others may still use, ask the owner with the evidence; on a no, update every reference and delete the old form in the same change.</p>

<div class="bs-flow">
<div class="bs-node"><span class="bs-label">1 · Check</span><h3>Who uses the old form?</h3><ul><li>Published URLs or packages</li><li>Other repositories</li><li>Saved data, frozen records</li><li>Running jobs</li></ul></div>
<div class="bs-arrow">→</div>
<div class="bs-node"><span class="bs-label">2 · Ask</span><h3>Give the owner the decision</h3><ul><li>What changes and why</li><li>Who uses it, with evidence</li><li>What breaks</li><li>What keeping it costs</li></ul></div>
<div class="bs-arrow">→</div>
<div class="bs-node"><span class="bs-label">3a · No compatibility</span><h3>Refactor fully</h3><ul><li>Update every caller and reference</li><li>Remove the old form</li><li>No aliases, shims or redirects</li></ul></div>
<div class="bs-arrow">or</div>
<div class="bs-node"><span class="bs-label">3b · Keep it</span><h3>Record it</h3><ul><li>Why it exists</li><li>When it can be removed</li></ul></div>
</div>

The project prefers clean refactors. An alias, fallback or redirect looks cheap when it is added, but every later reader must learn both forms, every check must cover both, and nobody remembers when the old one may go. The guide therefore removes the old form by default. Only the owner can know whether a link went out to people, whether another repository depends on a path, or whether a frozen record still names it, so the decision is theirs; the agent's part is to find the users and state what would break. When nothing outside the change uses the old form, no question is needed: the refactor goes ahead.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Keep the old key just in case</h3><p>A configuration key is renamed. The loader also accepts the old name, silently, with no record of who needed it. A year later two spellings are in use and nobody knows if the old one can go.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Ask, then rename everywhere</h3><p>The agent finds that one other repository reads the key and tells the owner what would break. The owner says no compatibility is needed. The rename lands with every reference updated, and the other repository is changed alongside it.</p></div>
</div>

<!-- fold: dead-end Silent fallbacks for moved files -->

Accepting a file at its old location when the new one is missing hides typos and stale references: a wrong path keeps working by accident. If an old path must keep working, the owner approves it and the record says why and until when.

<!-- /fold -->

Full guide: [Refactoring over compatibility](code-practices.html#refactoring-over-compatibility)

</section>

<section class="card" id="performance">

## Efficient code is the default, and waste found within scope is fixed where it is

<p class="bs-lead">Write invariant data once, batch related calls, keep evidence work opt-in and fix waste you find within your assigned scope.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Write invariant data once</h3><p>Headers, manifests, source hashes and recipes are written once and referenced, not repeated per step or call.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Batch related calls</h3><p>Use batch operations where the API allows. Read and write related state together instead of calling per item.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Keep evidence work opt-in</h3><p>Checkers, observers and full per-step records stay outside the normal path.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Avoid copies in hot paths</h3><p>Avoid repeated allocation and copying of large structures in hot paths.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">default</span><h3>Fix waste in scope</h3><p>Fix waste in the current implementation when you find it within the assigned scope.</p></div>
</div>

Waste that repeats per step or per call grows with every step and every run. Debug and evidence work left in the normal path makes every normal run pay for it, which is why the guide says such work must not set normal-run cost. These are habits applied while writing, not a separate optimization project: waste found within the assigned scope is fixed in the current implementation.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Every step pays for everything</h3><p>Each step's record repeats the run's manifest and source hash, and a consistency checker runs inside every step of every normal run.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Written once, checked on request</h3><p>The manifest and source hash are written once at the start and each step references them. The checker is an opt-in mode that a normal run does not pay for.</p></div>
</div>

<!-- fold: dead-end Moving the code to another language -->

Rewriting a slow component in another language can look like the quickest answer to waste. The guide says moving code to another language requires an explicit decision with the project owner and is never the default response to waste; the default is to fix the waste in the current implementation. Scope and architecture decisions that arise from performance work follow the [delivery rules for decisions and blockers](delivery.html#decisions-and-blockers).

<!-- /fold -->

Full guide: [Efficient implementation](performance.html) · [Efficient by default](performance.html#efficient-by-default)

</section>

<section class="card" id="performance-claims">

## A performance claim measures the workload and path it names

<p class="bs-lead">Declare the workload and execution path, verify the baseline, and label every timing by the path it actually measured.</p>

<figure id="fig-claims">
<div class="bs-flow" role="img" aria-label="Declare the workload and execution path the claim covers. Compare against a verified baseline, the strongest relevant cheap one. Report timings labelled by the path they measured; shipped claims use the shipped path with its required work. A quick mode labels its coverage and does not replace the full workload, its acceptance criteria or an experiment's agreed protocol.">
<div class="bs-node bs-teal"><span class="bs-label">Declare</span><b>Workload and execution path</b><ul><li>The workload the claim covers</li><li>The path: shipped, diagnostic or ablation</li></ul></div>
<div class="bs-arrow"><span>baseline</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Compare</span><b>A verified, strong baseline</b><ul><li>Verify it before changing measured behavior</li><li>Use the strongest relevant cheap baseline</li></ul></div>
<div class="bs-arrow"><span>measure</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Report</span><b>Timings labelled by path</b><ul><li>Shipped claims use the shipped path with its required work</li><li>Diagnostic and ablation timings name their paths</li></ul></div>
<div class="bs-back"><span>×</span> A quick mode labels its coverage. It does not replace the full workload, its acceptance criteria or an experiment's agreed protocol.</div>
</div>
<figcaption><b>Figure 1.</b> The guide's sequence for one performance claim. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

A timing is evidence only for the path that produced it. A diagnostic run or an ablation that skips required work can differ from what ships, so a claim about shipped performance uses the shipped path with its required work. A comparison also inherits its baseline's weaknesses: the guide asks you to verify the baseline before changing measured behavior and to compare against the strongest relevant cheap baseline.

[Figure 1](#fig-claims) fixes the claim's scope before anything is timed; the dashed line marks what a quick run cannot stand in for.

An illustrative example, not taken from a real project; ‹result› stands for a measured value:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An unscoped speed-up</h3><p>“The new loader is faster.” The claim names no workload, path or baseline, and the timing came from a run with validation turned off.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A claim with its scope</h3><p>“On the declared workload, through the shipped load path with validation included, against the verified current baseline: ‹result›.” A separate timing without validation is labelled as a diagnostic path.</p></div>
</div>

<!-- fold: experiment Production benchmarks and quick modes -->

A production benchmark answers one question: how fast is the thing users actually get? So it runs the shipped code from start to finish, with nothing skipped. The useful extras sit around it: ablations whose labels say plainly what they leave out, case generators and metrics that the next benchmark can reuse, a report of the runtime it ran on, and figures that record where their data came from.

When a benchmark or validation tool needs more than about a minute for its full run, give it a quick mode for everyday checks, and have that mode say what it covers. A quick result is a smoke test. It never stands in for the full workload, for its acceptance criteria or for the protocol an experiment agreed on.

<!-- /fold -->

<!-- fold: experiment Where the measurement rules live -->

This chapter covers what to time. What a speed-up claim must carry is spread over three other places:

- [Evidence](records.html#numbers-and-staleness) says what makes a number quotable: its identity, its baseline, reruns after a change, and how older results are labelled and reported. Follow it whenever you claim a speed-up.
- [Proportionate verification](experiment-verification.html) covers whether the numerical code is correct in the first place, and the regression gates that keep a fixed defect from returning.
- Your project's own records hold the concrete workloads, thresholds and performance contracts. The kit does not set them.

<!-- /fold -->

Full guide: [Efficient implementation](performance.html) · [Workload and evidence](performance.html#workload-and-evidence)

</section>

<section class="card" id="execution">

## An expensive job runs on the project's route under an adequate, stated budget

<p class="bs-lead">Read the project's execution instructions first, coordinate shared resources, and reserve from a comparable measurement or generously, saying which.</p>

<figure id="fig-execution">
<div class="bs-flow" role="img" aria-label="Before launch, read the project's execution and environment instructions, verify the executable, loaded source, inputs and environment, and use the supported entrypoint and resource controls. Then coordinate admission and adequate reservations, respecting host headroom and existing reservations. Then reserve from a comparable successful measurement or a deliberately generous initial reservation, and state the basis. Do not lower an adequate budget to force admission or bypass controls with local overrides.">
<div class="bs-node bs-teal"><span class="bs-label">Before launch</span><b>The project's execution route</b><ul><li>Read its execution and environment instructions</li><li>Verify executable, loaded source, inputs and environment</li><li>Use the supported entrypoint and resource controls, with admission, review and attendance requirements</li></ul></div>
<div class="bs-arrow"><span>coordinate</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Shared resources</span><b>Admission without squeezing</b><ul><li>Coordinate admission and adequate reservations</li><li>Respect host headroom and existing reservations</li><li>An idle host does not remove required containment</li></ul></div>
<div class="bs-arrow"><span>reserve</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Budget</span><b>An adequate, stated budget</b><ul><li>A sufficiently comparable successful measurement, or</li><li>A deliberately generous initial reservation covering startup, compilation, children and cleanup</li><li>State the basis; reserved is not measured</li></ul></div>
<div class="bs-back"><span>×</span> Do not lower an adequate budget to force admission or bypass controls with local overrides. Avoid repeated small increases after preventable memory failures.</div>
</div>
<figcaption><b>Figure 2.</b> The guide's steps before one expensive job starts. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

A job that skips the project's route can spend its resources on the wrong executable, source, inputs or environment; the guide asks you to verify these before launch. On shared resources, lowering an adequate budget to force admission, or bypassing controls with local overrides, does not make the job need less, and the guide says to do neither. A reservation also says nothing about what the job consumed, so state its basis and keep reserved capacity distinct from measured consumption.

[Figure 2](#fig-execution) covers everything before launch: the route, coordination, then the budget and its stated basis. The project supplies the concrete controls; reservation, usage-cache and receipt rules apply when the project uses those mechanisms.

An illustrative example, not taken from a real project; ‹amount› stands for a reservation size:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A guess, then small raises</h3><p>“Reserved plenty; it should be fine.” After a preventable memory failure the reservation is raised a little, then a little again.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A budget with its basis</h3><p>“No sufficiently comparable successful run exists, so this is a deliberately generous initial reservation covering startup, compilation, children and cleanup. ‹amount› is reserved capacity, not measured consumption.”</p></div>
</div>

<!-- fold: experiment Reusing an earlier reservation -->

A reservation is the capacity, such as memory, that you set aside for a job before it starts. If the same job ran successfully before, its measured use is the best basis for the next reservation. The catch is the word "same". Reuse the earlier figure only when nothing that drives resource use has changed:

- the workload and the command;
- the checkout or source state;
- the executable;
- the relevant environment and its recorded metadata;
- the identity of the inputs.

Inputs that come from outside or change between runs, and the roots that code is imported from, are easy to overlook, so name them explicitly. If any item differs, the old figure no longer applies: make a new, explicit and adequate reservation. An estimate, or a limit that a job failed at, is not a successful measurement and cannot be reused as one.

Some projects keep a temporary cache of earlier usage. It helps you choose a budget; it gives nobody permission to run a job. For a run request that is frozen and must not change, set the limits before freezing it and check those same limits at launch, instead of picking replacements from a cache that may have changed since. Measurements that serve as evidence are kept under the [evidence rules](records.html#numbers-and-staleness).

<!-- /fold -->

<!-- fold: experiment Deadlines and cleanup reserves -->

A budget has a time side too. Give the job a deadline that fits the operation, and keep a reserve for cleanup, so that stopping the job still leaves room to clean up after it. Projects set their own timing rules for bounded jobs and for sessions that someone attends; apply those.

<!-- /fold -->

<!-- fold: dead-end Relying on an idle host instead of containment or exclusive execution -->

When nobody else is using the machine, limits can feel like ceremony. The guide disagrees: an idle host does not remove required containment. Limits guard against what was not expected, and an empty machine does not make a job predictable.

Two related points. Protect the inputs and outputs of work that is already running, under the [parallel-work rules](delivery.html#parallel-work). And run a job alone when sharing would spoil the result: when interference would invalidate a timing, or when the job exercises lifecycle, runaway, signal or resource-stress behaviour.

<!-- /fold -->

Full guide: [Execution and shared resources](execution.html) · [Choose the project's execution route](execution.html#choose-the-projects-execution-route) · [Coordinate conflicting work](execution.html#coordinate-conflicting-work) · [Select a resource budget](execution.html#select-a-resource-budget) · [Reuse successful usage records conservatively](execution.html#reuse-successful-usage-records-conservatively)

</section>

<section class="card" id="supervision">

## A job's owner reads failures from evidence and keeps ownership through cleanup

<p class="bs-lead">Record command and resource outcomes separately, stop only what you own, and confirm cleanup before releasing the reservation.</p>

<figure id="fig-supervision">
<div class="bs-flow" role="img" aria-label="Name one owner for admission, launch, supervision, results and cleanup. Record command and resource outcomes separately, with process and source identity, actual limits, exit outcome and observed cleanup. Resolve uncertain ownership and confirm cleanup of children and temporary resources before releasing the reservation. Stop only owned jobs and services; treat failed or incomplete cleanup as a handoff blocker.">
<div class="bs-node bs-teal"><span class="bs-label">Name</span><b>One owner for the job</b><ul><li>Admission and launch</li><li>Supervision and results</li><li>Cleanup of children and temporary resources</li></ul></div>
<div class="bs-arrow"><span>record</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Record</span><b>Outcomes kept apart</b><ul><li>Command outcome and resource outcome, separately</li><li>Process and source identity, actual limits, exit outcome, observed cleanup</li></ul></div>
<div class="bs-arrow"><span>release</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Release</span><b>Cleanup confirmed first</b><ul><li>Resolve uncertain ownership</li><li>Confirm cleanup</li><li>Then release the reservation</li></ul></div>
<div class="bs-back"><span>×</span> Stop only owned jobs and services. Treat failed or incomplete cleanup as a handoff blocker.</div>
</div>
<figcaption><b>Figure 3.</b> The guide's ownership of one job from launch to release. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

When a job fails, "it ran out of memory" is a tempting explanation. The guide does not accept the guess: test failures alone do not establish exhaustion, and missing peaks, timeouts and cleanup failures do not measure memory needs. The end of a run has a similar trap. Without a named owner who stays until children and temporary resources are cleaned up, a released reservation can leave work behind that nobody is responsible for.

[Figure 3](#fig-supervision) ends at the release of the reservation, not at the job's exit: ownership lasts through cleanup.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A failure read as memory</h3><p>“Tests failed, so the job ran out of memory. Raised the budget and reran.”</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Two outcomes, each from evidence</h3><p>“Command outcome: tests failed. Resource outcome: no memory-limit evidence; the terminal peak was unavailable, so memory use remains unmeasured. The budget is not changed on this evidence, and the attempt is kept with its original settings.”</p></div>
</div>

<!-- fold: experiment What counts as memory evidence -->

To say that a job needed more memory than its limit, you need evidence that it actually hit the limit. Several things look like that evidence and are not:

- failed tests, which show that the command failed, not why;
- a missing peak reading, a timeout or a failed cleanup, none of which measures memory;
- a drop in the host's free memory, which must not be attributed to your job.

If the peak at the end of the run could not be read, report memory use as unmeasured. Do not fill the gap with a guess.

When pressure was unexpected or the budget turned out too small, follow the [escalation rules](delivery.html#decisions-and-blockers). Keep each attempt together with the settings it actually ran under, as the [evidence rules](records.html#numbers-and-staleness) require.

<!-- /fold -->

<!-- fold: experiment How much a job record holds -->

Match the record to the weight of the work. For a routine check a short note is enough: the command, the limits and the result. A [qualification](experiment-workflow.html#choose-the-purpose), which passes or fails a named system, needs the project's full evidence chain and follows the [claim-scope rules](records.html#naming-and-honest-claims). In both cases the record has to outlive the conversation it came from; the [durable-record rules](handoffs.html#evidence-and-durable-records) say where it goes.

<!-- /fold -->

Full guide: [Execution and shared resources](execution.html) · [Attribute failures from evidence](execution.html#attribute-failures-from-evidence) · [Own supervision and cleanup](execution.html#own-supervision-and-cleanup)

</section>

<section class="card" id="delivery">

## An assignment fixes the scope, and the owner finishes the routine work inside it

<p class="bs-lead">Define the deliverable, scope, inputs, ownership, completion condition and return channel; the owner then completes routine work without separate coordinator approval.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">The assignment defines</span><h3>What and where</h3><ul>
<li>The deliverable and its scope</li>
<li>Required inputs</li>
<li>File or module ownership</li>
<li>The completion condition</li>
<li>The recipient and agreed return channel</li>
</ul></div>
<div class="bs-part bs-violet"><span class="bs-label">Within the agreed scope</span><h3>The owner completes</h3><ul>
<li>Implementation</li>
<li>Focused checks and routine fixes</li>
<li>Associated documentation and evidence</li>
<li>Any review the project requires</li>
</ul></div>
</div>

A vague assignment leaves the owner guessing where the work stops and where to send the result, and leaves parallel owners guessing whose files are whose. The guide asks whoever assigns delegated or parallel work to define these up front, scaled to the work: a small, self-contained task can use a short brief. In return, routine work within the agreed scope needs no separate coordinator approval, so the owner carries it through to evidence and any required review.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An open-ended request</h3><p>“Have a look at the failing export and fix whatever you find.”</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A short, complete brief</h3><p>“Deliverable: a fix for the export failure. Scope: the export module, whose files you own. Input: the failing case and its log. Done when a focused check covers the case and passes and the fix is documented. Report back in this thread.”</p></div>
</div>

<!-- fold: dead-end Routing routine work through a coordinator -->

Sending each routine step to a coordinator for approval adds a wait without adding a decision. Inside the agreed scope the owner simply does the work; the guide requires no separate coordinator approval for it. A coordinator earns its place on what one owner cannot settle alone: overall goals, priorities, dependencies between pieces of work, open questions and conflicts over who owns what.

One hand-over does need names. When changes from several owners must come together, say who combines them, who checks the combined result and who lands it, and follow the [shared Git rules](git.html).

<!-- /fold -->

Full guide: [Ownership and delivery](delivery.html) · [Assigning work](delivery.html#assigning-work) · [Owner responsibility](delivery.html#owner-responsibility) · [Coordination and integration](delivery.html#coordination-and-integration)

</section>

<section class="card" id="decisions">

## Changes to the agreement go back for a decision; independent work continues

<p class="bs-lead">Escalate changes to goals, design, scope or acceptance; report limit hits and recurring failures; keep independent authorized work moving.</p>

<div class="bs-grid g3">
<div class="bs-part bs-orange"><span class="bs-label">Escalate</span><h3>Changes to the agreement</h3><ul>
<li>Agreed goals, design, scope or acceptance requirements</li>
<li>Ownership conflicts, resolved with the affected owners</li>
</ul></div>
<div class="bs-part bs-red"><span class="bs-label">Report</span><h3>Signs the plan may not hold</h3><ul>
<li>Resource-limit hits</li>
<li>Recurring unexplained failures</li>
</ul></div>
<div class="bs-part bs-blue"><span class="bs-label">Seek a decision</span><h3>Before going further</h3><ul>
<li>A next approach that exceeds agreed scope or limits</li>
<li>Reopening deferred work</li>
</ul></div>
</div>

An owner's autonomy covers routine work inside the agreement, not the agreement itself. Without escalation, an owner who quietly widens scope or relaxes an acceptance requirement leaves others planning against terms that no longer hold. Resource-limit hits and recurring unexplained failures are reported for a related reason: they suggest the agreed approach or limits may not hold, and the next approach may need a decision.

Respect explicit stops and required approvals. While a decision is pending, continue independent authorized work where possible.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Scope widened silently</h3><p>“Hit the memory limit again, so I raised it and also reworked the scheduler, which seemed related.”</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>A decision requested</h3><p>“Blocked: the memory limit was hit again on the same step (evidence linked). The likely fix changes the scheduler, outside the agreed scope, so I need a scope decision. Meanwhile I am continuing the independent documentation work.”</p></div>
</div>

<!-- fold: dead-end Freezing everything around a conflict -->

When two pieces of parallel work collide, stopping all nearby work looks safe. It also stops everyone who was never part of the collision. The guide asks for a narrower response: restrict only what actually conflicts, so that unrelated work continues.

In practice, keep other contributors' changes intact, agree on edits that overlap, and leave alone what running work depends on: its source, inputs, dependencies, execution settings and outputs. When two efforts need to move independently, give each its own worktree or another suitable form of isolation.

<!-- /fold -->

Full guide: [Ownership and delivery](delivery.html) · [Decisions and blockers](delivery.html#decisions-and-blockers) · [Parallel work](delivery.html#parallel-work)

</section>

<section class="card" id="handoffs">

## A report leads with the outcome and says how each claim is known

<p class="bs-lead">Distinguish work completed from behavior verified, send the report through the agreed return channel, and link the records that hold the evidence.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Outcome and changes</h3><p>State the outcome first, then what changed and where.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Checks</h3><p>Checks actually run, their results and relevant skipped checks.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Limits</h3><p>Failures, limitations and unresolved questions.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Links</h3><p>The delivered changes and the owning records.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">include</span><h3>Next owner</h3><p>The next owner and action, when further work remains.</p></div>
</div>

The recipient of a report has to decide what to trust and what to do next, usually without rerunning the work. A report that says "done" without naming what was checked leaves them unable to tell finished work from verified behavior. The guide asks you to say whether each claim comes from an executed check, source inspection or an inference. Chat, temporary coordination state and temporary files must not be the only retained copy of evidence later work needs.

On the receiving side, before relying on a consequential claim, check its supporting evidence and whether its source, inputs and scope match the work being integrated.

An illustrative example, not taken from a real project; ‹link› stands for a link to the change:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>Done, with nothing to check</h3><p>“All done, everything works now and the tests should pass.”</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Outcome, checks, sources of each claim</h3><p>“Outcome: the export fix is delivered in ‹link›. Checks run: the focused export check, passed. Skipped: the full suite, outside this scope. Verified: the failing case now passes. Inferred from source inspection: other formats are unaffected. Next: the integration owner lands it.”</p></div>
</div>

<!-- fold: experiment What a blocker report contains -->

A blocker report should let its reader decide without having to ask you anything first. Send it through the return channel you agreed on, and say:

- what is blocked;
- the evidence that settles it;
- what you already tried;
- the decision or dependency you need before you can go on.

Use the same channel to report that you finished. A closing message in some other chat proves nothing about whether the right person saw it. The [delivery guide](delivery.html#decisions-and-blockers) covers when to escalate and which independent work can continue in the meantime.

<!-- /fold -->

<!-- fold: experiment Durable records and receiving a handoff -->

A handoff message is a pointer, not an archive. Detailed results and the steps to reproduce them go into the records that own them, under the [documentation](documentation-system.html) and [evidence rules](records.html#numbers-and-staleness); the handoff links to those records.

On the receiving side, two small acts keep work from stalling. Confirm receipt when the sender is waiting for it before going on. And when responsibility moves, say who owns the work now and what they do next.

<!-- /fold -->

Full guide: [Handoffs and progress reports](handoffs.html) · [Reporting completion](handoffs.html#reporting-completion) · [Reporting blockers](handoffs.html#reporting-blockers) · [Evidence and durable records](handoffs.html#evidence-and-durable-records) · [Receiving a handoff](handoffs.html#receiving-a-handoff)

</section>

<section class="card" id="git">

## Each commit holds one logical deliverable, reviewed as a whole before it is created

<p class="bs-lead">Stage only what belongs, review the complete proposed commit, and explain what changed and why.</p>

<figure id="fig-git">
<div class="bs-flow" role="img" aria-label="Inspect the branch, working changes and staging area. Stage explicit paths or selected changes. Review the complete proposed commit, including deletions and earlier staged changes. Creating a commit does not establish that its tests passed.">
<div class="bs-node bs-teal"><span class="bs-label">Inspect</span><b>Branch, changes, staging area</b><ul><li>Check the current branch</li><li>Read working changes and the staging area</li><li>Identify what belongs to the deliverable</li></ul></div>
<div class="bs-arrow"><span>stage</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Stage</span><b>Explicit paths or selected changes</b><ul><li>Stage everything only when every change belongs</li><li>Preserve unrelated working and staged changes</li></ul></div>
<div class="bs-arrow"><span>review</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Review</span><b>The complete proposed commit</b><ul><li>Include deletions and changes staged before you started</li><li>Match file versions to the source state the checks covered</li></ul></div>
<div class="bs-back"><span>×</span> Creating a commit does not establish that its tests passed or that its acceptance requirements were met.</div>
</div>
<figcaption><b>Figure 4.</b> The guide's steps for preparing one commit. This diagram illustrates the rules; it contains no measured results.</figcaption>
</figure>

Later readers inspect, revert and cite commits one at a time, so a commit that mixes unrelated work, or splits one deliverable into scattered fragments, is harder to use. When other changes are present in the working tree or staging area, staging everything can sweep them in. The guide therefore asks you to stage explicit paths or selected changes and to review the complete proposed commit, including deletions and changes staged before you started.

[Figure 4](#fig-git) ends with a review of the whole commit, not only the files you remember changing. The message then uses a short imperative subject and an explanatory body, separated by a blank line, that says what changed and why. Include validation results or limitations when they help assess the change. Do not use Conventional Commits prefixes.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>A prefix and no reason</h3><pre><code>fix: updates</code></pre><p>A Conventional Commits prefix, a subject that does not say what changed, and no body explaining why.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Imperative subject, explanatory body</h3><pre><code>Keep progress messages out of the export stream&#10;&#10;The export command printed progress on stdout, which the
import tool parses. Progress now goes through the project's
logger, and stdout carries only the export format.&#10;&#10;The export round-trip check passed.</code></pre></div>
</div>

<!-- fold: dead-end One commit per tweak, or one commit for everything -->

Committing every intermediate file change scatters one deliverable across many commits; bundling unrelated work hides each change inside the others. The guide's unit sits between the two: one logical deliverable per commit. A fix, a feature, an experiment or one coherent stage of a refactor is a deliverable, and the small edits made on the way to it are folded in.

Two refinements. Stages that were verified separately stay separate commits when that separate verification means something. And a deliverable is more than its code: the tests, documentation and worklog entry that belong to it are covered by the [documentation rules](documentation-system.html#rules-for-changes-and-chronology).

<!-- /fold -->

<!-- fold: experiment Validation before landing -->

A commit records what changed. It does not show that the change works: creating a commit establishes neither that its tests passed nor that its acceptance requirements were met. So the checks come first. Pass the checks that apply before landing an implementation, within the repository's validation requirements and publication permissions, and write down what really happened: results, skipped checks and limitations.

One trap is checking one version and committing another. Before committing, confirm that the files you are about to commit match the source state that the recorded checks covered.

A failed or negative outcome can still be a sound deliverable. Investigation and evidence work may keep such results, provided they are documented accurately.

<!-- /fold -->

<!-- fold: dead-end Committing inside the kit submodule -->

A fix to the kit made inside a project's `.docs-kit` folder looks finished: the project builds, and the pin moves to the new commit. But that commit exists only on that disk. Once the project is pushed, every fresh clone and CI checkout fails to fetch the pinned kit commit. The guide sends kit changes to the kit's own repository first; the project moves its pin to the pushed commit afterwards. `docsite.py lint` fails when the pinned commit is on none of the kit's remote branches.

<!-- /fold -->

Full guide: [Git changes and shared checkouts](git.html) · [Deliverables and validation](git.html#deliverables-and-validation) · [Commit messages](git.html#commit-messages) · [Preparing a commit](git.html#preparing-a-commit) · [The shared kit submodule](git.html#the-shared-kit-submodule)

</section>

<section class="card" id="shared-checkout">

## In a shared checkout, one owner holds staging from final review to commit

<p class="bs-lead">Protect the interval between reviewing a commit and creating it; when you cannot, prepare the commit in isolation and reconcile afterward.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Interval protected</span><h3>One owner commits in place</h3><ul>
<li>One owner for staging and committing during the operation</li>
<li>No concurrent staging between final review and commit creation</li>
<li>Overlapping file edits coordinated separately</li>
</ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Interval not protected</span><h3>Prepare in isolation, then reconcile</h3><ul>
<li>Prepare and verify the commit in an isolated staging area or worktree</li>
<li>Coordinate updates to the shared branch</li>
<li>Reconcile the shared staging area, preserving others' staged intent and working changes</li>
<li>Resolve overlapping paths with their owner, then verify the resulting status</li>
</ul></div>
</div>

Git's locks around individual commands do not protect the interval between those commands. If another contributor stages a change after your final review but before your commit, that change can enter your commit unreviewed. The guide closes that gap by giving staging and committing one owner for the duration of the operation and by protecting the proposed commit from concurrent staging until it is created.

An illustrative example, not taken from a real project:

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Example · not this</span><h3>An unprotected gap</h3><p>“Reviewed the staged changes, answered a message, then committed.” Meanwhile another contributor had staged its own files in the same checkout, and they entered the commit.</p></div>
<div class="bs-part bs-green"><span class="bs-label">Example · this</span><h3>Prepared in isolation</h3><p>Another contributor was active in the checkout, so the commit was prepared and verified in a separate worktree. When it landed, the shared staging area kept the other contributor's staged paths, an overlapping path was settled with its owner, and the resulting status was checked.</p></div>
</div>

<!-- fold: dead-end Relying on Git's locks or a staging-area lock -->

Git locks the repository only while a single command runs. Between your final review and your commit there is a gap that no lock covers, and another contributor can stage something in it. A lock on the staging area does not help with the files themselves either: two people can still edit the same working file at the same time. Overlapping file edits need their own coordination.

<!-- /fold -->

<!-- fold: dead-end Rewriting shared history to undo a mistake -->

Rewriting history can look like the quickest way to remove changes that entered a commit by mistake. It is safe only where nobody else stands: squash temporary checkpoints only in history that is isolated and unshared, and leave alone any history that another contributor or a running job uses.

If unrelated changes did get into a commit, do not repair it quietly. Record which commit is affected, tell the owner of those changes through the agreed channel, and agree on the recovery before rewriting anything that someone else may be building on.

<!-- /fold -->

Full guide: [Git changes and shared checkouts](git.html) · [Sharing a checkout](git.html#sharing-a-checkout) · [History and recovery](git.html#history-and-recovery)

</section>
