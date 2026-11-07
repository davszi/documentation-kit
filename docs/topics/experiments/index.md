+++
title = "Experiments"
brand = "Documentation kit"
brand_sub = "small · bounded · proportionate"
description = "How the kit's two experiment guides keep experiments small, choose their purpose, state their content and match verification to the claim."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css"]
toc = [["Guides", "#routes"], ["Keep it small", "#keep-experiments-small"], ["Purpose", "#choose-the-purpose"], ["Evidence and stopping", "#start-from-evidence"], ["Before and after", "#required-content"], ["Learned models only", "#learned-or-fitted-models-only"], ["Evidence gap", "#identify-the-evidence-gap"], ["Checks and failures", "#checks-and-failures"]]
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

Projects keep their questions, criteria, contracts and decisions in their own records. Existing contracts still apply. Resources, provenance, benchmarks and placement stay with their [existing owners](experiment-workflow.html#use-the-existing-owners).

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

These limits never waive the required content. Do more only when an open question matters to the next decision. See [keep experiments small](experiment-workflow.html#keep-experiments-small).

</section>

<section class="card" id="choose-the-purpose">

## Classify an experiment by what its result decides, not by the project's field

<p class="bs-lead">Ask one question: does it accept or reject a named system against a bar fixed before the run?</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">No · investigation</span><h3>Answers a question</h3><p>"No" or "inconclusive" is a finding. Declare one kind before running:</p><ul><li><b>Exploratory</b>: choices may develop from observations.</li><li><b>Confirmatory</b>: claim and judgment are fixed before evaluation results. A paper's headline comparison is confirmatory.</li></ul></div>
<div class="bs-part bs-orange"><span class="bs-label">Yes · qualification</span><h3>Gives a verdict on a named system</h3><p>Pass, fail or inconclusive for a named system, build or model:</p><ul><li>platform qualification</li><li>a benchmark contract</li><li>a parity check</li><li>model release evaluation</li></ul></div>
</div>

An exploratory finding is not a confirmation or qualification. Before a decision relies on it, test it on evidence that did not shape it. See [choose the purpose](experiment-workflow.html#choose-the-purpose).

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
<figcaption><b>Figure 1.</b> The path from prior evidence to a stop. Data, cases or scenarios that guide choices stay apart from those that evaluate the claim, as far as the claim requires.</figcaption>
</figure>

Repeating one case, scenario, seed or dataset does not replicate across others. See [start from evidence](experiment-workflow.html#start-from-evidence-and-bound-the-question) and [keep evaluation separate from tuning](experiment-workflow.html#keep-evaluation-separate-from-tuning).

</section>

<section class="card" id="required-content">

## Every experiment states its plan before running and reports every attempt after

<p class="bs-lead">Exploratory work included, the plan comes first and the report keeps failures beside the best result.</p>

<div class="bs-grid g2">
<div class="bs-part bs-teal"><span class="bs-label">Before running</span><h3>State the plan</h3><ul><li>question and measured motivation</li><li>kind: exploratory, confirmatory or qualification</li><li>the decision it informs</li><li>baseline, budget and stopping condition</li></ul><p><b>Confirmatory or qualification</b> also fixes its bar or expected observation, tolerances, workload, analysis, and what counts as failure or inconclusive.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">After running</span><h3>Report the whole run</h3><ul><li>reproduction details under the <a href="evidence.html#numbers-and-staleness">measurement rules</a></li><li>results with units and scope</li><li>the verdict, for confirmatory work or a qualification</li><li>every attempt, failure and changed setting, with its reason</li><li>for exploration, how the interpretation developed</li><li>caveats and next step</li></ul></div>
</div>

A failed bar is [never lowered](experiment-verification.html#respond-to-changes-and-failures). See [required content](experiment-workflow.html#required-content).

</section>

<section class="card" id="learned-or-fitted-models-only">

## Final runs apply only when results depend on a learned or fitted model

<p class="bs-lead">Skip this rule unless results depend on a model learned or fitted from data; nothing in it applies to other experiments.</p>

<div class="bs-grid g2">
<div class="bs-part bs-muted"><span class="bs-label">Results do not depend on a learned or fitted model</span><h3>Skip the section</h3><p>No final run and no model-specific checks. Do not import learned-model practices into the experiment.</p></div>
<div class="bs-part bs-violet"><span class="bs-label">Results depend on a learned or fitted model</span><h3>Apply three rules</h3><ul><li>A <b>final run</b> trains a selected recipe to produce the model that will be reported or used. It is a production step, not a rigor tier. Fix the recipe and usable-result criteria first; a recipe change is a new attempt. An investigation or qualification judges its output.</li><li>Check splits, preprocessing and label or target alignment.</li><li>Comparing training objectives does not require reimplementing each one.</li></ul></div>
</div>

The test is dependence on such a model, not the project's field. An engineering or simulation experiment falls under this rule only when its results depend on a learned or fitted model. See [learned or fitted models only](experiment-workflow.html#learned-or-fitted-models-only).

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
<figcaption><b>Figure 2.</b> Follow the arrows from naming the gap to the cheapest check that closes it. Adopted project requirements remain binding.</figcaption>
</figure>

See [identify the evidence gap](experiment-verification.html#identify-the-evidence-gap).

</section>

<section class="card" id="checks-and-failures">

## Each check applies where its risk applies, and a failed bar is never lowered

<p class="bs-lead">The verification guide names five situations; each check is required only when its condition holds.</p>

<div class="bs-checks r32">
<div class="bs-check"><span class="bs-badge bs-wait">Where it affects the claim</span><h3>Application logic</h3><p>Check data identity and composition, leakage, metric definitions and aggregation, and how configuration, library calls and saved outputs compose. Pick cases that can expose a plausible wiring error, including one that still looks reasonable. Ordinary library use needs no recertification.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Custom numerical code</span><h3>Independent reference</h3><p>Where no trusted reference covers it, compare with a reference derived from the stated formulas or an independent source, never from production or generated logic. Use claim-based tolerances over the relevant regimes; a self-check fails its exit status beyond them. State observed agreement and its scope; do not presume parity.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Defect could return</span><h3>Regression gate</h3><p>The project decides its scope. Keep the fixed defect or difficult case, document tolerances and, where available, show the gate fails on a known-bad state. Keep routine gates thin: target under five seconds for a fast gate. The target limits gates, not experiments.</p></div>
<div class="bs-check"><span class="bs-badge bs-wait">Inputs or conditions changed</span><h3>Rerun what is affected</h3><p>Rerun the affected checks before treating their evidence as current. Reuse unaffected evidence only after confirming its identity and scope. Where interruptions could affect validity or cost, verify the recovery that matters to that run; add no universal interruption suite.</p></div>
<div class="bs-check"><span class="bs-badge bs-bad">Check failed</span><h3>Keep the bar</h3><p>Investigate against the agreed criteria. Do not lower a failed bar to make the same result pass. Changing an obsolete criterion needs an explicit project decision and rationale, with the original failure retained.</p></div>
</div>

Report checks executed, results, inspection-only conclusions and remaining uncertainty under the [handoff guide](handoffs.html). See [application logic](experiment-verification.html#check-the-experiments-application-logic), [custom numerical code](experiment-verification.html#validate-custom-numerical-implementations), [regression gates](experiment-verification.html#maintain-regression-gates) and [changes and failures](experiment-verification.html#respond-to-changes-and-failures).

</section>
