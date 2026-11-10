+++
title = "Experiments"
brand_sub = "small · bounded · proportionate"
description = "How the kit's two experiment guides keep experiments small, choose their purpose, state their content and match verification to the claim, with the reason for each rule and an illustrative case."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Guides", "#routes"], ["Keep it small", "#keep-experiments-small"], ["Purpose", "#choose-the-purpose"], ["Evidence and stopping", "#start-from-evidence"], ["Before and after", "#required-content"], ["Learned models only", "#learned-or-fitted-models-only"], ["Evidence gap", "#identify-the-evidence-gap"], ["Targeted checks", "#checks-and-failures"], ["Changes and failures", "#changes-and-failures"]]
page_only = "Explains the experiment guides; they are the records, in rules/experiments/."
+++

# Experiments

<section class="card" id="routes">

## Two guides cover how to design an experiment and how to check it

<p class="bs-lead">Read the workflow guide before designing or running an experiment, and the verification guide before choosing checks.</p>

<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Experiment guides by task">

| Before… | Read… | It covers |
|---|---|---|
| Designing or running an experiment | [Experiment workflow](experiment-workflow.html) | Keeping experiments small, investigations and qualifications, baselines, stopping and required content |
| Choosing checks or interpreting failures | [Proportionate verification](experiment-verification.html) | Evidence gaps, application logic, custom numerical code, regression gates, changes and failures |

</div>

Both guides exist to keep experiments small enough to finish and honest enough to rely on. Each chapter below states one rule, explains the failure it prevents and shows an illustrative case. The cases come from different fields because the rules apply by what a result decides, not by the project's field.

Projects keep their questions, criteria, contracts and decisions in their own records. Existing contracts still apply. Resources, provenance, benchmarks and placement stay with their [existing owners](experiment-workflow.html#use-the-existing-owners).

<!-- fold: experiment Which guides own resources, provenance, benchmarks and placement -->

The experiment guides do not restate what other guides own. When an experiment touches one of these subjects, follow the owning guide:

- Checks: [proportionate verification](experiment-verification.html).
- Resources and cleanup: [execution](execution.html).
- Provenance of measured numbers: [numbers and staleness](records.html#numbers-and-staleness), in the guide for writing records.
- Run visuals and live experiment reports: [figures](figures.html#run-visuals-and-experiment-lifecycle), one of the page guides.
- Benchmarks: [performance](performance.html).
- Placement: [documentation policy](documentation-system.html).

See [use the existing owners](experiment-workflow.html#use-the-existing-owners).

<!-- /fold -->

</section>

<section class="card" id="keep-experiments-small">

## Start with the smallest experiment that can change a decision

<p class="bs-lead">Read this first: before adding a run, check, document or gate, name the decision it changes and the error it would catch.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-ok">Start</span><h3>Smallest first</h3><p>A one-line probe before an experiment. One comparison before a grid. A probe that needs more than its line is an investigation.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">Each addition</span><h3>Name its purpose</h3><p>Name the decision it changes and the error it would catch. If you cannot, do not add it. There is no quota.</p></div>
<div class="bs-check"><span class="bs-badge bs-ok">First</span><h3>Agree the budget</h3><p>Agree time, compute and files, and when to change approach. Ask before exceeding the budget or widening the question.</p></div>
<div class="bs-check"><span class="bs-badge bs-bad">Unless asked</span><h3>Add no process</h3><p>No registries, receipts, templates, approval steps, audit files or status boards unless the project asks.</p></div>
<div class="bs-check"><span class="bs-badge bs-bad">Unless needed</span><h3>Import no other field's methods</h3><p>No preregistration, ablation grids or learned-model practices unless the results depend on them.</p></div>
</div>

Without this limit, an experiment grows by additions that each look careful: another sweep, another check, another file. An addition that changes no decision and catches no error costs time and compute without telling anyone more. The rule therefore asks for a reason before each addition, not a minimum amount of work: there is no quota.

<p><b>Illustrative case:</b> does a higher steering-controller gain reduce overshoot in a simulated lane change?</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · overbuilt</span><h3>A sweep before a question</h3><ul><li>a grid of gains, speeds and road surfaces before any single comparison</li><li>a new run registry and a template for every run</li><li>an ablation grid borrowed from another field</li><li>no agreed budget, so the sweep has no stopping point</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · proportionate</span><h3>One comparison first</h3><ul><li>a one-line probe: current gain against one higher gain on the existing lane-change scenario</li><li>the decision it informs: whether a tuning investigation is worth opening</li><li>budget agreed first: a few runs, no new files</li><li>speeds and surfaces wait for an open question that matters to the next decision</li></ul></div>
</div>

<!-- fold: dead-end Why borrowed rigor is not added by default -->

Preregistration, ablation grids and learned-model practices serve experiments whose results depend on them. Elsewhere they add steps and files without changing a decision, so the guide imports them only when the results depend on them. Registries, receipts, templates, approval steps, audit files and status boards follow the same logic: they appear when the project asks for them.

Keeping an experiment small never removes its required content. The smallest probe still states its plan and reports every attempt; see [before and after](#required-content).

<!-- /fold -->

See [keep experiments small](experiment-workflow.html#keep-experiments-small).

</section>

<section class="card" id="choose-the-purpose">

## Classify an experiment by what its result decides, not by the project's field

<p class="bs-lead">Ask one question: does it accept or reject a named system against a bar fixed before the run?</p>

<figure id="fig-purpose">
<div class="bs-flow n2" role="img" aria-label="Ask whether the experiment accepts or rejects a named system against a bar fixed before the run. If not, it is an investigation, declared exploratory or confirmatory before running. If so, it is a qualification with a pass, fail or inconclusive verdict. An exploratory finding is not a confirmation or qualification.">
<div class="bs-node bs-blue"><span class="bs-label">Ask</span><b>Accept or reject a named system?</b><ul><li>against a bar fixed before the run</li><li>the project's field does not decide</li></ul></div>
<div class="bs-arrow"><span>classify</span></div>
<div class="bs-stack">
<div class="bs-node bs-teal"><span class="bs-label">No · investigation</span><b>Answers a question</b><ul><li><em>Exploratory</em>: choices may develop from observations</li><li><em>Confirmatory</em>: claim and judgment fixed before evaluation results; a paper's headline comparison is confirmatory</li></ul></div>
<div class="bs-node bs-orange"><span class="bs-label">Yes · qualification</span><b>Verdict on a named system</b><ul><li>pass, fail or inconclusive for a system, build or model</li><li>platform qualification, benchmark contract, parity check, model release evaluation</li></ul></div>
</div>
<div class="bs-back"><span>×</span> An exploratory finding is not a confirmation or qualification. Before a decision relies on it, test it on evidence that did not shape it.</div>
</div>
<figcaption><b>Figure 1.</b> One question sorts an experiment; an investigation declares its kind before running.</figcaption>
</figure>

The kind decides what must be fixed before the run and what the result can support. A verdict needs its bar before the run; otherwise the bar can bend toward whatever the run produced. An investigation may end in "no" or "inconclusive" and still be a finding. Without a declared kind, a pattern found while exploring can be reported as if it had been tested.

<p><b>Illustrative case:</b> is a new cache layer faster for the project's request workload?</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · mislabelled</span><h3>Exploration reported as a verdict</h3><ul><li>try several cache sizes and request mixes, keep the best</li><li>report "the cache is faster" as if a bar had been fixed first</li><li>the requests that picked the size also judge it</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · declared</span><h3>Exploratory first, then fresh evidence</h3><ul><li>declared exploratory: cache sizes may change as results come in</li><li>the speed-up reported as an exploratory finding, with its scope</li><li>before the release decision relies on it, tested on requests that did not shape it</li><li>a release check against a bar fixed first is a qualification</li></ul></div>
</div>

See [choose the purpose](experiment-workflow.html#choose-the-purpose).

</section>

<section class="card" id="start-from-evidence">

## Build on existing evidence and stop once the question is answered

<p class="bs-lead">Read what is already known, run the smallest comparison that resolves the rest, and keep tuning apart from evaluation.</p>

<figure id="fig-bound">
<div class="bs-flow" role="img" aria-label="Read prior evidence and check that it applies. Choose the smallest comparison with a verified baseline. Stop when the question is answered, the budget is reached or the approach cannot answer it. Evaluation results that shaped selection must be stated; repeating runs does not repair leakage.">
<div class="bs-node bs-teal"><span class="bs-label">Read first</span><b>Prior evidence</b><ul><li>results, failures, code and decisions</li><li>check their inputs and scope apply</li></ul></div>
<div class="bs-arrow"><span>bound</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Design</span><b>Smallest comparison</b><ul><li>resolves only what remains</li><li>before changing measured behavior, verify that the strongest relevant baseline the budget allows measures the intended behavior</li><li>shipped behavior: run the shipped path</li><li>replication matched to the claim</li></ul></div>
<div class="bs-arrow"><span>stop</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Stop when</span><b>One condition holds</b><ul><li>the question is answered</li><li>the budget is reached</li><li>the approach cannot answer it</li></ul></div>
<div class="bs-back"><span>×</span> Repeating runs does not repair leakage. If evaluation results influenced selection, say so, then narrow the claim or get fresh evidence.</div>
</div>
<figcaption><b>Figure 2.</b> The path from prior evidence to a stop. Data, cases or scenarios that guide choices stay apart from those that evaluate the claim, as far as the claim requires.</figcaption>
</figure>

An experiment that skips prior results can repeat a known failure or re-measure what is already settled. A baseline that does not measure the intended behavior makes any improvement against it meaningless, which is why it is verified before measured behavior changes. Tuning on the cases that later judge the claim lets the evaluation confirm its own choices, and more repeats of those cases do not undo that.

<p><b>Illustrative case:</b> do new path-planner cost weights reduce near-misses at simulated intersections?</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · unbounded</span><h3>Tuned and judged on the same cases</h3><ul><li>prior planner results and failure notes left unread</li><li>baseline: a simplified planner script, not the planner that ships</li><li>weights tuned on the intersections that also report the result</li><li>one intersection rerun with many seeds, called replication across intersections</li><li>sweeping continues after the question is answered</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · bounded</span><h3>Shipped baseline, separate cases, clear stop</h3><ul><li>prior results read; their map inputs and scope still apply</li><li>baseline runs the shipped planner path</li><li>weights tuned on some intersections, the claim evaluated on others kept apart</li><li>stop when answered, at the budget, or when the approach cannot answer it</li></ul></div>
</div>

<!-- fold: dead-end When evaluation results already shaped a choice -->

Say so in the report. Then either narrow the claim to what the untouched evidence supports or get fresh evidence. Rerunning the same evaluation more times does not help: every repeat carries the same influence it was meant to test. Repeating one case, scenario, seed or dataset also does not replicate across others.

The separation between tuning and evaluation goes as far as the claim requires, not further.

<!-- /fold -->

See [start from evidence](experiment-workflow.html#start-from-evidence-and-bound-the-question) and [keep evaluation separate from tuning](experiment-workflow.html#keep-evaluation-separate-from-tuning).

</section>

<section class="card" id="required-content">

## Every experiment states its plan before running and reports every attempt after

<p class="bs-lead">Exploratory work included, the plan comes first and the report keeps failures beside the best result.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Before running</span><h3>State the plan</h3><ul><li>question and measured motivation</li><li>kind: exploratory, confirmatory or qualification</li><li>the decision it informs</li><li>baseline, budget and stopping condition</li></ul><p><b>Confirmatory or qualification</b> also fixes its bar or expected observation, tolerances, workload, analysis, and what counts as failure or inconclusive.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">After running</span><h3>Report the whole run</h3><ul><li>reproduction details under the <a href="records.html#numbers-and-staleness">measurement rules</a></li><li>results with units and scope</li><li>the verdict, for confirmatory work or a qualification</li><li>every attempt, failure and changed setting, with its reason</li><li>for exploration, how the interpretation developed</li><li>caveats and next step</li></ul></div>
</div>

A plan written before results exist keeps the decision, baseline and stopping condition from drifting toward whichever outcome appears. Reporting every attempt matters because a best-only report hides how many tries the result needed and which settings failed. This is content, not a form: a short note in the project's own record can hold it, and no template is added unless the project asks.

<p><b>Illustrative case:</b> does a streaming parser fix the slow import of large log files?</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · form without content</span><h3>Process added, attempts dropped</h3><ul><li>a new experiment template, a sign-off step and a status board</li><li>no stated decision or stopping condition</li><li>a report showing only the configuration that finally worked</li><li>the crashed attempt and the changed buffer setting left out</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · content in the existing note</span><h3>A short plan, a complete report</h3><ul><li>before: the question; the measured slow import that prompted it; exploratory; decision: switch the import path or not; baseline: the current parser; budget and stop</li><li>after: reproduction details, results with units and scope, every attempt including the crash and why the setting changed, caveats and next step</li></ul></div>
</div>

<!-- fold: experiment What the reproduction details include -->

The [measurement rules](records.html#numbers-and-staleness) say what makes a measured claim reproducible: its source commit, exact reproduction command, runtime or environment, workload, units, baseline, method and scope, with links to its raw result and limitations. When code, input data, method, workload or runtime conditions affecting the claim change, rerun before quoting it as current.

<!-- /fold -->

A failed bar is [never lowered](experiment-verification.html#respond-to-changes-and-failures). See [required content](experiment-workflow.html#required-content).

</section>

<section class="card" id="learned-or-fitted-models-only">

## Final runs apply only when results depend on a learned or fitted model

<p class="bs-lead">Skip this rule unless results depend on a model learned or fitted from data; nothing in it applies to other experiments.</p>

<div class="bs-grid g2">
<div class="bs-part bs-muted"><span class="bs-label">Results do not depend on a learned or fitted model</span><h3>Skip the section</h3><p>No final run and no model-specific checks. Do not import learned-model practices into the experiment.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Results depend on a learned or fitted model</span><h3>Apply three rules</h3><ul><li>A <b>final run</b> trains a selected recipe to produce the model that will be reported or used. It is a production step, not a rigor tier. Fix the recipe and usable-result criteria first; a recipe change is a new attempt. An investigation or qualification judges its output.</li><li>Check splits, preprocessing and label or target alignment.</li><li>Comparing training objectives does not require reimplementing each one.</li></ul></div>
</div>

When a result depends on a model learned from data, the model that is reported or used comes from a final run of the selected recipe. Fixing the recipe and the usable-result criteria first keeps that run from becoming another round of tuning; a recipe change is a new attempt and is reported as one. A final run is a production step, not a rigor tier, so adding one to other experiments makes them longer, not more rigorous.

<p><b>Illustrative case:</b> a lane-detection network trained for release.</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · hidden tuning</span><h3>A final run that keeps changing</h3><ul><li>train, inspect the output, adjust the learning rate, retrain, and still call it the final run</li><li>the final run treated as its own proof that the model is good</li><li>every training objective reimplemented from scratch to compare them</li><li>no check that labels line up with their images</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · production step</span><h3>Fixed recipe, judged output</h3><ul><li>recipe and usable-result criteria fixed before the final run</li><li>a changed learning rate starts a new, reported attempt</li><li>an investigation or qualification judges the trained model</li><li>splits, preprocessing and label alignment checked</li><li>objectives compared without reimplementing each one</li></ul></div>
</div>

<!-- fold: dead-end Engineering and simulation work that skips this section -->

The test is whether results depend on a model learned or fitted from data, not the project's field. A controller comparison in a physics simulation, a parser benchmark or a check of a numerical routine skips the section: no final run and no split checks. If such an experiment does depend on a fitted model, for example a simulation whose result rests on a tire model fitted from measurements, the section applies to that model.

<!-- /fold -->

See [learned or fitted models only](experiment-workflow.html#learned-or-fitted-models-only).

</section>

<section class="card" id="identify-the-evidence-gap">

## Add a check only when it closes a named gap that existing evidence leaves

<p class="bs-lead">Match verification to the claim and its consequential failures, within the limits that keep experiments small.</p>

<figure id="fig-gap">
<div class="bs-flow" role="img" aria-label="Name the error a check could expose and the gap existing checks leave. Reuse covering evidence. Use the cheapest credible diagnostic and state what remains untested; go broader only when a smaller check cannot close the gap. The experiment's kind or a planned publication does not by itself require an extra audit.">
<div class="bs-node bs-teal"><span class="bs-label">Name</span><b>The error and the gap</b><ul><li>the error a check could expose</li><li>the gap existing checks leave</li></ul></div>
<div class="bs-arrow"><span>reuse</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Covered already?</span><b>Prior evidence first</b><ul><li>tests, assertions and results</li><li>only when source, inputs and scope cover the question</li></ul></div>
<div class="bs-arrow"><span>cheapest</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Still open</span><b>Cheapest credible check</b><ul><li>miniature pipeline, targeted case or source inspection</li><li>state what remains untested</li><li>broader only when a smaller check cannot close the gap</li></ul></div>
<div class="bs-back"><span>×</span> Neither the experiment's kind nor a planned publication by itself requires an extra audit.</div>
</div>
<figcaption><b>Figure 3.</b> Follow the arrows from naming the gap to the cheapest check that closes it. Adopted project requirements remain binding.</figcaption>
</figure>

A check that cannot expose a named error adds time without adding confidence, and a check that repeats existing coverage adds nothing new. Naming the error first also points to the cheapest check that could find it, and stating what remains untested keeps the claim within its evidence. Neither a confirmatory label nor a planned publication changes this by itself.

<p><b>Illustrative case:</b> a rewritten CSV reader should give the same totals as the old one.</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · audit by default</span><h3>Everything checked because it will be published</h3><ul><li>a review of the whole parsing library</li><li>a broad fuzzing campaign</li><li>the full test suite rerun under several settings</li><li>no named error that any of these could catch</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · gap first</span><h3>Name the gap, close it cheaply</h3><ul><li>existing tests already cover quoting and empty fields for this reader</li><li>open gap: files that end with a trailing delimiter</li><li>one miniature file with that case; totals compared, old against new</li><li>reported as untested: encodings other than UTF-8</li></ul></div>
</div>

See [identify the evidence gap](experiment-verification.html#identify-the-evidence-gap).

</section>

<section class="card" id="checks-and-failures">

## Check application logic, custom numerical code and regressions only where their risk applies

<p class="bs-lead">The verification guide names three targeted checks; each is required only when its condition holds.</p>

<div class="bs-checks">
<div class="bs-check"><span class="bs-badge bs-wait">Where it affects the claim</span><h3>Application logic</h3><p>Check data identity and composition, leakage, metric definitions and aggregation, and how configuration, library calls and saved outputs compose. Pick cases that can expose a plausible wiring error, including one that still looks reasonable. Ordinary library use needs no recertification. For learned or fitted models, also apply the <a href="#learned-or-fitted-models-only">model-specific checks</a>.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Custom numerical code</span><h3>Independent reference</h3><p>Where no trusted reference covers it, compare with a reference derived from the stated formulas or an independent source, never from production or generated logic. Use claim-based tolerances over the relevant regimes; a self-check fails its exit status beyond them. State observed agreement and its scope; do not presume parity.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Defect could return</span><h3>Regression gate</h3><p>The project decides its scope. Keep the fixed defect or difficult case, document tolerances and, where available, show the gate fails on a known-bad state. Keep routine gates thin: target under five seconds for a fast gate. The target limits gates, not experiments.</p></div>
</div>

Each targets a place where a plausible error can survive ordinary testing. Application logic can be wired wrong and still give results that look reasonable. Custom numerical code can agree with a reference that shares its error. A fixed defect can return unnoticed. Outside those conditions the check adds cost, not evidence.

<p><b>Illustrative case:</b> a custom integrator in a vehicle-dynamics simulation.</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · shared error, heavy gate</span><h3>A reference that cannot disagree</h3><ul><li>reference values generated by the production integrator itself</li><li>higher precision, exhaustive replay and a native-backend comparison run by default</li><li>a routine gate that replays every scenario</li><li>parity presumed after one matching case</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · independent and thin</span><h3>Derived reference, thin gate</h3><ul><li>reference derived from the stated motion equations for a case with a known solution</li><li>compared over the relevant step sizes and speeds, with tolerances chosen for the claim</li><li>a self-check that fails its exit status beyond tolerance</li><li>a fast gate keeps the fixed defect case and fails on the known-bad version</li><li>observed agreement reported with its scope</li></ul></div>
</div>

<!-- fold: experiment When higher precision, exhaustive replay or another backend is justified -->

Use higher precision, exhaustive replay or a native or other-backend comparison only when it addresses the claim and a risk the reference comparison leaves uncovered. Make optional native comparisons explicitly guarded.

A reference that shares the suspected error is no evidence against it, which is why the reference is never derived from generated or production logic.

<!-- /fold -->

<!-- fold: dead-end Why the library itself is not re-tested -->

Re-testing a well-used library before trusting an experiment looks rigorous and mostly checks the wrong thing. Using a library in the ordinary way does not call for certifying it again. The errors that matter sit in the experiment's own wiring: how it puts together configuration, library calls and saved outputs, wherever those affect the claim. Verify that. Look into the library itself only when a concrete risk, or the claim, depends on how the library behaves.

<!-- /fold -->

See [application logic](experiment-verification.html#check-the-experiments-application-logic), [custom numerical code](experiment-verification.html#validate-custom-numerical-implementations) and [regression gates](experiment-verification.html#maintain-regression-gates).

</section>

<section class="card" id="changes-and-failures">

## Rerun what a change affects, and never lower a failed bar

<p class="bs-lead">A change makes the affected evidence stale; a failed check is investigated against the agreed criteria, not redefined.</p>

<figure id="fig-failure">
<div class="bs-flow" role="img" aria-label="When source, inputs, splits, metrics, composition or runtime conditions change, rerun the affected checks and reuse unaffected evidence only after confirming its identity and scope. Investigate a failed check against the agreed criteria. Changing an obsolete criterion needs an explicit project decision and rationale, with the original failure retained. A failed bar is not lowered to make the same result pass.">
<div class="bs-node bs-teal"><span class="bs-label">Changed</span><b>Something the evidence used</b><ul><li>source, inputs or splits</li><li>metrics or composition</li><li>runtime conditions</li></ul></div>
<div class="bs-arrow"><span>rerun</span></div>
<div class="bs-node bs-violet"><span class="bs-label">Before it counts as current</span><b>Affected checks rerun</b><ul><li>unaffected evidence reused only after confirming identity and scope</li></ul></div>
<div class="bs-arrow"><span>if it fails</span></div>
<div class="bs-node bs-orange"><span class="bs-label">Failed check</span><b>Investigate against the criteria</b><ul><li>the agreed criteria stay the reference</li><li>obsolete criterion: explicit project decision and rationale</li><li>original failure retained</li></ul></div>
<div class="bs-back"><span>×</span> Do not lower a failed bar to make the same result pass.</div>
</div>
<figcaption><b>Figure 4.</b> From a change to current evidence, and from a failure to an open decision.</figcaption>
</figure>

Evidence describes the source, inputs and conditions that produced it. After a change, affected results no longer describe the current state, while unaffected ones can still be reused once their identity and scope are confirmed. Lowering a failed bar to make the same result pass would turn the check into a description of the result, so the original criterion and failure stay on record; replacing an obsolete criterion is an explicit project decision.

<p><b>Illustrative case:</b> a dependency update lands before a performance comparison of two request handlers is reported.</p>

<div class="bs-grid g2">
<div class="bs-part bs-red"><span class="bs-label">Not this · stale and softened</span><h3>Old numbers, moved bar</h3><ul><li>timings from before the update quoted as current</li><li>the agreed tolerance widened until the new handler passes</li><li>the original failure dropped from the record</li><li>an interruption test suite added to every experiment</li></ul></div>
<div class="bs-part bs-green"><span class="bs-label">This · rerun and decide openly</span><h3>Rerun, investigate, keep the record</h3><ul><li>timings the update affects rerun</li><li>unaffected parser tests reused after confirming the same source and inputs</li><li>the failure investigated against the agreed criteria</li><li>if a criterion is obsolete: a project decision with rationale, original failure kept</li></ul></div>
</div>

<!-- fold: experiment Interruptions and what the report states -->

A long run can be interrupted. Where that could affect the validity or the cost of a run, verify the recovery behaviour that matters for that run: its checkpoints, the identity it resumes under, its partial outputs or its restart. There is no universal interruption suite to add on top.

The report then keeps four things apart, under the [handoff guide](handoffs.html): the checks that were executed, their results, the conclusions reached by inspection only, and the uncertainty that remains. Reusing a result after something changed follows the [staleness rules](records.html#numbers-and-staleness).

<!-- /fold -->

See [changes and failures](experiment-verification.html#respond-to-changes-and-failures).

</section>
