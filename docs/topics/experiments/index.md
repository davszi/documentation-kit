+++
title = "Experiments"
brand_sub = "small · bounded · proportionate"
description = "How the kit's two experiment guides keep experiments small, bound the question, state the plan, show the running total and match verification to the claim, with the reason for each rule and a drawn example."
components = ["toc", "nav", "code", "filelinks"]
page_css = ["build-sheet.css", "experiments/experiments.css"]
toc = [["Keep it small", "#keep-experiments-small"], ["Purpose", "#choose-the-purpose"], ["Evidence and stopping", "#start-from-evidence"], ["Measured settings", "#decide-on-a-measurement"], ["Plan and report", "#required-content"], ["The total", "#show-the-total"], ["Learned models only", "#learned-or-fitted-models-only"], ["Evidence gap", "#identify-the-evidence-gap"], ["Targeted checks", "#checks-and-failures"], ["Changes and failures", "#changes-and-failures"]]
page_only = "Explains the experiment guides; they are the records, in rules/experiments/."
+++

# Experiments

<section class="card" id="keep-experiments-small">

<span id="routes"></span>

## Start with the smallest experiment that can change a decision

<p class="bs-lead">A run, check, document or gate is added only when it names the decision it changes and the error it would catch.</p>

<figure id="fig-small">
<div class="xp-fig" role="img" aria-label="A budget of time, compute and files is agreed first and spans the whole climb. Three steps rise from left to right: a one-line probe, one comparison, then a grid. Each step up passes a gate: an open question that matters to the next decision, naming the decision and the error. Below, crossed out: registries, receipts, templates, approval steps, audit files and status boards beyond the running total, and other fields' methods, unless the project asks or the results depend on them.">
<div class="xp-rail"><span class="xp-tag">Agreed first</span>the budget in time, compute and files, and when to change approach · ask before exceeding it or widening the question</div>
<div class="xp-stair">
<div class="xp-box xp-teal"><span class="xp-tag">Smallest</span><b>A one-line probe</b><p>A probe that needs more than its line is an investigation.</p><i>Current steering gain against one higher gain, on the existing lane-change scenario.</i></div>
<div class="xp-arrow"><span>names a decision and an error</span></div>
<div class="xp-box xp-violet"><span class="xp-tag">Then</span><b>One comparison</b><p>An experiment with its plan and baseline.</p><i>Whether a tuning investigation is worth opening.</i></div>
<div class="xp-arrow"><span>an open question needs it</span></div>
<div class="xp-box xp-orange"><span class="xp-tag">Only if needed</span><b>A grid</b><p>More settings, cases or scenarios. There is no quota.</p><i>Speeds and road surfaces wait until a question needs them.</i></div>
</div>
<div class="xp-no"><span>×</span><span>Not added unless the project asks: registries, receipts, templates, approval steps, audit files, status boards beyond the running total. Not imported unless the results depend on them: preregistration, ablation grids, learned-model practices.</span></div>
</div>
<figcaption><b>Figure 1.</b> An experiment climbs one step at a time inside a budget agreed first. The steering case is illustrative; the diagram is authored in the page source and holds no measured results.</figcaption>
</figure>

[Figure 1](#fig-small) shows the climb. Without the limit an experiment grows by additions that each look careful: another sweep, another check, another file. One that changes no decision and catches no error costs time and tells nobody more, so the rule asks for a reason before each addition instead of a minimum amount of work. [Approval that failed open](approval-failed-open.html) measured where unexamined additions lead. Small never waives the [plan and the report](#required-content), and supporting code such as a harness or a judge starts with [naming the need](code-practices.html#name-the-need-first) and reading the project's capability map. See [keep experiments small](experiment-workflow.html#keep-experiments-small).

An experiment starts like other work: its design is discussed and agreed before it runs, and [an experiment takes the same path, with extra gates](discuss-build-record.html#experiments) shows where each gate sits. This page explains the gates. Their rules are in the [experiment workflow](experiment-workflow.html) and [proportionate verification](experiment-verification.html); resources, provenance, visuals, benchmarks and placement stay with [their existing owners](experiment-workflow.html#use-the-existing-owners).

</section>

<section class="card" id="choose-the-purpose">

## Classify an experiment by what its result decides, not by the project's field

<p class="bs-lead">One question sorts it: does it accept or reject a named system against a bar fixed before the run?</p>

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
<figcaption><b>Figure 2.</b> One question sorts an experiment; an investigation declares its kind before running.</figcaption>
</figure>

[Figure 2](#fig-purpose) sorts by what the result decides. The kind fixes what must be settled before the run: a verdict needs its bar first, or the bar bends toward whatever the run produced. An investigation may end in "no" or "inconclusive" and still be a finding. Declaring it exploratory or confirmatory before running keeps a pattern found while exploring from being reported as tested.

For example, trying several cache sizes on the project's requests and keeping the fastest is exploratory. The speed-up is reported as an exploratory finding with its scope, and before a release decision relies on it, it is tested on requests that did not shape it; a release check against a bar fixed first is a qualification. See [choose the purpose](experiment-workflow.html#choose-the-purpose).

</section>

<section class="card" id="start-from-evidence">

## Build on existing evidence, keep tuning apart from evaluation, and stop once the question is answered

<p class="bs-lead">Read what is known, compare against a baseline that measures the intended behavior on cases kept apart from tuning, and stop at one of three conditions.</p>

<figure id="fig-bound">
<div class="xp-fig" role="img" aria-label="Three stages from left to right. Read first: prior results, failures, code and decisions, after checking that their inputs and scope apply. The smallest comparison: a baseline verified to measure the intended behavior, the shipped path for shipped behavior, and two pools of cases kept apart, one that guides choices and one that evaluates the claim. Stop when the question is answered, the budget is reached or the approach cannot answer it. Crossed out below: evaluation results that shaped selection are stated, and the claim narrowed or fresh evidence found; repeating runs does not repair leakage.">
<div class="xp-bound">
<div class="xp-box xp-teal"><span class="xp-tag">Read first</span><b>Prior evidence</b><ul><li>results, failures, code and decisions</li><li>used only where their inputs and scope apply</li></ul><i>Earlier planner results; their map inputs still hold.</i></div>
<div class="xp-arrow"><span>what remains</span></div>
<div class="xp-box xp-violet"><span class="xp-tag">Smallest comparison</span><b>A verified baseline, two pools of cases</b><ul><li>before measured behavior changes, the strongest baseline the budget allows is checked to measure the intended behavior; shipped behavior runs the shipped path</li><li>replication matches the claim: many seeds on one intersection replicate only that one</li></ul>
<div class="xp-pools"><div class="xp-pool" style="--pool: var(--blue)"><span class="xp-tag">Guide choices</span>cost weights tuned on these intersections</div><div class="xp-wall" aria-hidden="true"></div><div class="xp-pool" style="--pool: var(--orange)"><span class="xp-tag">Evaluate the claim</span>near-misses judged on these, kept apart</div></div></div>
<div class="xp-arrow"><span>stop</span></div>
<div class="xp-box xp-orange"><span class="xp-tag">Stop when</span><b>One condition holds</b><ul><li>the question is answered</li><li>the budget is reached</li><li>the approach cannot answer it</li></ul></div>
</div>
<div class="xp-no"><span>×</span><span>Evaluation results that shaped a choice are stated; the claim is narrowed or fresh evidence found. More repeats of the same cases do not repair the leak.</span></div>
</div>
<figcaption><b>Figure 3.</b> From prior evidence to a stop, on an illustrative question: do new path-planner cost weights reduce near-misses at simulated intersections? The diagram is authored in the page source and holds no measured results.</figcaption>
</figure>

[Figure 3](#fig-bound) follows the planner question. Reading first avoids repeating a known failure. A baseline that does not measure the intended behavior makes any improvement against it meaningless, so it is checked before measured behavior changes. Tuning on the cases that later judge the claim lets the evaluation confirm its own choices, and every repeat of those cases carries the same influence. The separation goes as far as the claim requires, not further.

An investigation set aside before its question is answered is [shelved](records.html#shelved-investigations): a scope decision recorded with its inputs, code, failures and the conditions for taking it up again; resuming it needs a new explicit assignment. See [start from evidence](experiment-workflow.html#start-from-evidence-and-bound-the-question) and [keep evaluation separate from tuning](experiment-workflow.html#keep-evaluation-separate-from-tuning).

</section>

<section class="card" id="decide-on-a-measurement">

## A setting the person decides rests on a measurement taken before the question is put

<p class="bs-lead">Where measuring is cheap next to what the decision costs, a list of candidate values, a training length or a number of workers is chosen from a measured number.</p>

<figure id="fig-setting">
<div class="xp-fig">
<div class="xp-plots">
<div class="xp-plot"><span class="xp-tag">Decide a setting · workers per run</span>
<svg class="xp-wide" viewBox="0 0 400 300" role="img" aria-label="Example plot with invented values. The vertical axis is minutes per run, from 0 to 90, the unit the question is asked in; the horizontal axis is the number of workers per run: 1, 2, 4 and 8 measured, 16 not run. A dashed line marks a budget of 30 minutes per run. The measured runs take 80, 44, 26 and 21 minutes: the line flattens, so 8 workers save only 5 minutes over 4, and both stay within the budget. The column for 16 workers holds no point and is labelled not run.">
<text class="xt" x="6" y="20">↑ minutes per run</text>
<text class="xstamp" x="394" y="20" text-anchor="end">INVENTED VALUES</text>
<path class="xgrid" d="M62 105H392M62 40H392"/>
<path class="xax" d="M62 34V236H392"/>
<path class="xlim" d="M62 171H392"/>
<text class="xt" x="68" y="192">budget 30 min</text>
<rect class="xcol" x="343" y="70" width="34" height="166" rx="5"/>
<text class="xtn" x="360" y="60" text-anchor="middle">not run</text>
<polyline class="xln" points="100,62 170,140 240,179 310,190"/>
<circle class="xpt" cx="100" cy="62" r="6"/><circle class="xpt" cx="170" cy="140" r="6"/><circle class="xpt" cx="240" cy="179" r="6"/><circle class="xpt" cx="310" cy="190" r="6"/>
<text class="xval" x="114" y="60">80</text><text class="xval" x="183" y="136">44</text><text class="xval" x="240" y="207" text-anchor="middle">26</text><text class="xval" x="310" y="217" text-anchor="middle">21</text>
<text class="xtick" x="54" y="241" text-anchor="end">0</text><text class="xtick" x="54" y="176" text-anchor="end">30</text><text class="xtick" x="54" y="110" text-anchor="end">60</text><text class="xtick" x="54" y="45" text-anchor="end">90</text>
<text class="xtick" x="100" y="260" text-anchor="middle">1</text><text class="xtick" x="170" y="260" text-anchor="middle">2</text><text class="xtick" x="240" y="260" text-anchor="middle">4</text><text class="xtick" x="310" y="260" text-anchor="middle">8</text><text class="xtick" x="360" y="260" text-anchor="middle">16</text>
<text class="xt" x="228" y="292" text-anchor="middle">workers per run →</text>
</svg>
<svg class="xp-narrow" viewBox="0 0 300 264" role="img" aria-label="Example plot with invented values, narrow version. Minutes per run over the number of workers: 80, 44, 26 and 21 minutes for 1, 2, 4 and 8 workers, against a dashed budget of 30 minutes; the line flattens. The column for 16 workers is labelled not run.">
<text class="xt" x="4" y="18">↑ minutes per run</text>
<text class="xstamp" x="296" y="18" text-anchor="end">INVENTED VALUES</text>
<path class="xgrid" d="M44 100H292"/>
<path class="xax" d="M44 50V200H292"/>
<path class="xlim" d="M44 150H292"/>
<text class="xt" x="48" y="172">budget 30 min</text>
<rect class="xcol" x="256" y="62" width="28" height="138" rx="5"/>
<text class="xtn" x="296" y="52" text-anchor="end">not run</text>
<polyline class="xln" points="74,67 124,127 174,157 224,165"/>
<circle class="xpt" cx="74" cy="67" r="5.5"/><circle class="xpt" cx="124" cy="127" r="5.5"/><circle class="xpt" cx="174" cy="157" r="5.5"/><circle class="xpt" cx="224" cy="165" r="5.5"/>
<text class="xval" x="86" y="66">80</text><text class="xval" x="136" y="124">44</text><text class="xval" x="174" y="182" text-anchor="middle">26</text><text class="xval" x="224" y="189" text-anchor="middle">21</text>
<text class="xtick" x="38" y="205" text-anchor="end">0</text><text class="xtick" x="38" y="155" text-anchor="end">30</text><text class="xtick" x="38" y="105" text-anchor="end">60</text><text class="xtick" x="38" y="55" text-anchor="end">90</text>
<text class="xtick" x="74" y="222" text-anchor="middle">1</text><text class="xtick" x="124" y="222" text-anchor="middle">2</text><text class="xtick" x="174" y="222" text-anchor="middle">4</text><text class="xtick" x="224" y="222" text-anchor="middle">8</text><text class="xtick" x="270" y="222" text-anchor="middle">16</text>
<text class="xt" x="168" y="254" text-anchor="middle">workers per run →</text>
</svg></div>
<div class="xp-plot"><span class="xp-tag">Size a later run · twice the steps</span>
<svg class="xp-wide" viewBox="0 0 400 300" role="img" aria-label="Example bars with invented values. The vertical axis is minutes, with gridlines every 40 up to 120. Step 1, the earlier run: a dashed bar shows its estimate of 40 minutes and a filled bar its measured cost of 65 minutes, 25 minutes more. Step 2, the later run with twice the steps: a dashed bar sized from the measured cost, 2 × 65 = 130 minutes. The report gives the measured cost against the estimate before the sizing.">
<text class="xt" x="6" y="20">↑ minutes</text>
<text class="xstamp" x="394" y="20" text-anchor="end">INVENTED VALUES</text>
<path class="xgrid" d="M62 180H392M62 124H392M62 68H392"/>
<path class="xax" d="M62 34V236H392"/>
<rect class="xest" x="72" y="180" width="48" height="56" rx="3"/>
<rect class="xmeas" x="162" y="145" width="48" height="91" rx="3"/>
<path class="xguide" d="M120 180H162"/>
<text class="xval" x="96" y="172" text-anchor="middle">40</text><text class="xval" x="186" y="137" text-anchor="middle">65</text>
<text class="xdiff" x="141" y="168" text-anchor="middle">+25</text>
<path class="xarr" d="M222 145H286M278 138l8 7-8 7"/>
<rect class="xnext" x="300" y="54" width="60" height="182" rx="3"/>
<text class="xval" x="330" y="46" text-anchor="middle">2 × 65 = 130</text>
<text class="xtick" x="54" y="241" text-anchor="end">0</text><text class="xtick" x="54" y="185" text-anchor="end">40</text><text class="xtick" x="54" y="129" text-anchor="end">80</text><text class="xtick" x="54" y="73" text-anchor="end">120</text>
<text class="xtick" x="96" y="260" text-anchor="middle">estimate</text><text class="xtick" x="186" y="260" text-anchor="middle">measured</text><text class="xtick" x="330" y="260" text-anchor="middle">sized</text>
<text class="xtb" x="141" y="292" text-anchor="middle">1 · earlier run</text><text class="xtb" x="330" y="292" text-anchor="middle">2 · later run</text>
</svg>
<svg class="xp-narrow" viewBox="0 0 300 264" role="img" aria-label="Example bars with invented values, narrow version. Step 1, the earlier run: estimate 40 minutes, dashed, and measured cost 65 minutes, filled, 25 more. Step 2, the later run with twice the steps: a dashed bar sized from the measured cost, 2 × 65 = 130 minutes.">
<text class="xt" x="4" y="18">↑ minutes</text>
<text class="xstamp" x="296" y="18" text-anchor="end">INVENTED VALUES</text>
<path class="xgrid" d="M44 157H292M44 114H292M44 71H292"/>
<path class="xax" d="M44 50V200H292"/>
<rect class="xest" x="57" y="157" width="34" height="43" rx="3"/>
<rect class="xmeas" x="135" y="130" width="34" height="70" rx="3"/>
<path class="xguide" d="M91 157H135"/>
<text class="xval" x="74" y="150" text-anchor="middle">40</text><text class="xval" x="152" y="123" text-anchor="middle">65</text>
<text class="xdiff" x="113" y="148" text-anchor="middle">+25</text>
<path class="xarr" d="M176 130H218M211 124l7 6-7 6"/>
<rect class="xnext" x="228" y="61" width="48" height="139" rx="3"/>
<text class="xval" x="296" y="52" text-anchor="end">2 × 65 = 130</text>
<text class="xtick" x="38" y="205" text-anchor="end">0</text><text class="xtick" x="38" y="162" text-anchor="end">40</text><text class="xtick" x="38" y="119" text-anchor="end">80</text><text class="xtick" x="38" y="76" text-anchor="end">120</text>
<text class="xtick" x="74" y="224" text-anchor="middle">estimate</text><text class="xtick" x="152" y="224" text-anchor="middle">measured</text><text class="xtick" x="252" y="224" text-anchor="middle">sized</text>
<text class="xtb" x="113" y="255" text-anchor="middle">1 · earlier run</text><text class="xtb" x="296" y="255" text-anchor="end">2 · later run</text>
</svg></div>
</div>
</div>
<figcaption><b>Figure 4.</b> A measured number where the person decides, drawn with example values, invented for this page. Left: minutes per run over the number of workers, against the budget; the largest candidate was not run and holds no point. Right: an earlier run's estimate beside its measured cost, then a later run of twice the steps sized from the measured cost. Filled marks are measured; dashed marks are estimates, sizings and runs not made. The plots are drawn in the page source.</figcaption>
</figure>

In the left panel of [Figure 4](#fig-setting), the minutes per run are plotted over the number of workers, because a cost that depends on a setting tells little at one setting alone. Read from the first run alone, more workers would seem to cut the time in proportion; the measured line flattens instead, and the person sees that the most workers measured save little over half as many, while both stay within the budget. The axis keeps the unit the question is asked in, and the candidate that was not measured stands in its place as *not run* ([page design](page-design.html#page-design)). The number meets the [measurement rules](records.html#numbers-and-staleness) before the question reaches the person: its script and its output are tracked, so the person can check what the choice rests on.

In the right panel a later run is sized from an earlier one. The report first gives the earlier run's measured cost against its estimate, then the sizing, so the person sees how far the last estimate held before trusting the next. Here the earlier run took well over its estimate, so the later run is sized from the measured cost; sized from the estimate, it would fall short by the same proportion. See [start from evidence](experiment-workflow.html#start-from-evidence-and-bound-the-question).

</section>

<section class="card" id="required-content">

## Every experiment states its plan before running and reports every attempt after

<p class="bs-lead">Exploratory work included, the plan comes first, and the report keeps every failure and changed setting beside the best result.</p>

<figure id="fig-record">
<div class="xp-fig" role="img" aria-label="An experiment's life from left to right. Before the first attempt, the plan: question and measured motivation, kind, the decision it informs, baseline, budget and stopping condition; a confirmatory investigation or qualification also fixes its bar or expected observation, tolerances, workload, analysis and what counts as failure or inconclusive. Three attempts follow, each adding a line to the running total; the second crashed and its buffer setting changed. The run output is tracked before completion is reported. Then the report: reproduction details, results with units and scope, the verdict where one is due, every attempt, failure and changed setting with its reason, how an exploratory interpretation developed, caveats and next step. Crossed out: a failed bar is lowered.">
<ol class="xp-life">
<li class="xp-box xp-teal"><span class="xp-tag">Before running · plan</span><ul><li>question and measured motivation</li><li>kind and the decision it informs</li><li>baseline, budget, stopping condition</li><li><b>confirmatory or qualification:</b> bar or expected observation, tolerances, workload, analysis, what counts as failure or inconclusive</li></ul></li>
<li class="xp-box xp-step xp-muted"><span class="xp-tag">First attempt</span><b>runs</b><span class="xp-chip">+ total line</span></li>
<li class="xp-box xp-step xp-red"><span class="xp-tag">Second attempt</span><b>crashed; buffer setting changed</b><span class="xp-chip">+ total line</span></li>
<li class="xp-box xp-step xp-muted"><span class="xp-tag">Third attempt</span><b>runs with the new buffer</b><span class="xp-chip">+ total line</span></li>
<li class="xp-box xp-step xp-blue"><span class="xp-tag">Before done</span><b>run output tracked</b></li>
<li class="xp-box xp-violet"><span class="xp-tag">After · report</span><ul><li>reproduction details, results with units and scope</li><li>the verdict, where one is due</li><li>every attempt, failure and changed setting, with its reason</li><li>exploration: how the interpretation developed</li><li>caveats and next step</li></ul></li>
</ol>
<div class="xp-no"><span>×</span><span>A failed bar is never lowered, and the report never shows only the best attempt.</span></div>
</div>
<figcaption><b>Figure 5.</b> The plan before the first attempt, the report after the last, on an illustrative case: does a streaming parser fix the slow import of large log files? The diagram is authored in the page source and holds no measured results.</figcaption>
</figure>

[Figure 5](#fig-record) lays the required content along the experiment. A plan written before results exist keeps the decision, baseline and stop from drifting toward whatever appears. A report of every attempt shows how many tries the result needed and which settings failed; a best-only report hides both. The run output behind the reported results is [tracked in the experiment directory](records.html#numbers-and-staleness) before completion is reported, and a failed bar is [never lowered](#changes-and-failures). This is content, not a form: a short note in the project's own record holds it, and no template is added unless the project asks.

<!-- fold: detail What the reproduction details include -->

The [measurement rules](records.html#numbers-and-staleness) make a measured claim reproducible: its source commit, exact reproduction command, runtime or environment, workload, units, baseline, method and scope, with links to its raw result and limitations. When something affecting the claim changes, it is rerun before it is quoted as current.

<!-- /fold -->

See [required content](experiment-workflow.html#required-content).

</section>

<section class="card" id="show-the-total">

## The running total shows what the machinery costs, and a step back reads it across experiments

<p class="bs-lead">Each attempt adds one line of counts for the person to read; after every third finished experiment, a fresh agent reads them all.</p>

<figure id="fig-total">
<div class="xp-fig" role="img" aria-label="Left: the guide's example line, Total after attempt 7, split into five counts: attempts, usable results, lines of supporting code, lines of its tests, and the person's minutes. Counted: harness, judges, preparation steps and other supporting code, and the person's time. Not counted: runs, seeds, controls and repetitions. Right: three finished experiments, each with its total lines; after the third, a fresh agent reads the capability map, the experiment records with their totals, the tooling tree and the worklog, changes nothing, and answers three questions. Its findings go to the person and into the capability map's list of needs seen but not built, each decision open.">
<div class="xp-total">
<div class="xp-box xp-orange"><span class="xp-tag">One line per attempt · the guide's example</span>
<code class="xp-line">Total after attempt 7: <mark data-n="1">7 attempts</mark>, <mark data-n="2">2 usable results</mark>, <mark data-n="3">1,240 lines of supporting code</mark> and <mark data-n="4">610 lines of tests</mark>, <mark data-n="5">95 minutes of the person's time</mark>.</code>
<ol class="xp-key">
<li>each run of the experiment's procedure</li>
<li>output a finding or verdict can rest on; a "no" counts, an attempt stopped before its output was complete does not</li>
<li>every line written or changed for this experiment, in its folder and in the tooling tree</li>
<li>counted apart from the code, with one counting command named in the record</li>
<li>from session records or from the person; otherwise "not recorded", never estimated</li>
</ol>
<div class="xp-count"><div class="xp-pool" style="--pool: var(--orange)"><span class="xp-tag">Counted · machinery</span>harness, judges, preparation steps, other supporting code, the person's time</div><div class="xp-pool" style="--pool: var(--muted)"><span class="xp-tag">Not counted · science</span>runs, seeds, controls, repetitions</div></div>
</div>
<div class="xp-box xp-violet xp-back"><span class="xp-tag">Step back · after every third finished experiment</span>
<div class="xp-three"><span>first experiment · its totals</span><span>second · its totals</span><span>third · its totals</span></div>
<div class="xp-down">counted in the worklog; review asked</div>
<p><b>A fresh agent only reads</b> the capability map, the experiment records with their totals, the tooling tree and the worklog, and changes nothing.</p>
<ol><li>Which needs were solved more than once, and where?</li><li>What does the person keep doing by hand?</li><li>What do the totals show across experiments?</li></ol>
<div class="xp-down">findings</div>
<p>To the person, and into the capability map's needs seen but not built, each decision open.</p>
</div>
</div>
</div>
<figcaption><b>Figure 6.</b> The total for each attempt, and the read across experiments. The line is the example the workflow guide gives; the diagram is authored in the page source.</figcaption>
</figure>

The left half of [Figure 6](#fig-total) takes the guide's example line apart. It counts the machinery and the person's time, not the science, so a well-controlled experiment does not look expensive for being careful. It is information, not a target: it has no threshold, stops nothing, and an experiment is never weakened to shrink it; its question decides what it needs. [Approval that failed open](approval-failed-open.html#kit) shows supporting code that grew while nobody added it up.

The right half is the step back: after every third finished experiment unless the project's context names another interval, and whenever the person asks. The agent that asked writes the findings into the capability map and brings the person the options of [name the need first](code-practices.html#name-the-need-first). Where the runtime cannot start a fresh agent, the review is a separate step that reads everything before anything is written, and its report says so. See [show the total](experiment-workflow.html#show-the-total) and [step back across experiments](experiment-workflow.html#step-back-across-experiments).

</section>

<section class="card" id="learned-or-fitted-models-only">

## Final runs apply only when results depend on a learned or fitted model

<p class="bs-lead">Skip this rule unless results depend on a model learned or fitted from data; nothing in it applies to other experiments.</p>

<figure id="fig-final-run">
<div class="xp-fig" role="img" aria-label="The question: do results depend on a model learned or fitted from data? If not, skip the section: no final run, no split checks, no learned-model practices. If so: fix the recipe and usable-result criteria, run the final run as a production step, and let an investigation or qualification judge its output. A recipe change loops back as a new attempt. Alongside: check splits, preprocessing and label or target alignment; comparing training objectives does not require reimplementing each one.">
<div class="xp-fork">
<div class="xp-box xp-blue xp-q"><span class="xp-tag">Ask</span><b>Do the results depend on a model learned or fitted from data?</b><p>Not the project's field: a controller comparison in a physics simulation says no; a simulation resting on a tire model fitted from measurements says yes for that model.</p></div>
<div class="xp-box xp-muted xp-dashed xp-no-side"><span class="xp-tag">No · skip</span><b>Nothing here applies</b><p>No final run, no split checks, no learned-model practices imported.</p></div>
<div class="xp-box xp-violet"><span class="xp-tag">Yes · a lane-detection network trained for release</span>
<div class="xp-chain">
<div class="xp-box xp-teal"><span class="xp-tag">First</span><b>Fix the recipe</b><p>and the usable-result criteria</p></div>
<div class="xp-arrow"><span>train</span></div>
<div class="xp-box xp-orange"><span class="xp-tag">Final run</span><b>A production step</b><p>not a rigor tier</p></div>
<div class="xp-arrow"><span>judge</span></div>
<div class="xp-box xp-blue"><span class="xp-tag">Then</span><b>Investigation or qualification</b><p>judges the model it produced</p></div>
<div class="xp-loop"><span>↺</span>A changed learning rate is a recipe change: a new attempt, reported as one.</div>
</div>
<p class="xp-also">Also: check splits, preprocessing and label or target alignment; compare training objectives without reimplementing each one.</p>
</div>
</div>
</div>
<figcaption><b>Figure 7.</b> Whether the section applies, and what a final run is where it does. The cases are illustrative; the diagram is authored in the page source.</figcaption>
</figure>

[Figure 7](#fig-final-run) starts with the test, which is about the result, not the field. Where it applies, fixing the recipe and the usable-result criteria first keeps the final run from becoming another round of tuning, so a recipe change is a new attempt. A final run produces the model that will be reported or used, and an investigation or qualification judges it; as a production step, not a rigor tier, it makes other experiments longer, not more rigorous. See [learned or fitted models only](experiment-workflow.html#learned-or-fitted-models-only).

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
<figcaption><b>Figure 8.</b> Follow the arrows from naming the gap to the cheapest check that closes it. Adopted project requirements remain binding.</figcaption>
</figure>

[Figure 8](#fig-gap) runs from the gap to the check. A check that cannot expose a named error adds time without confidence, and one that repeats existing coverage adds nothing. Naming the error points to the cheapest check that could find it; stating what remains untested keeps the claim within its evidence.

For example, a rewritten CSV reader should give the old reader's totals. Existing tests cover quoting and empty fields, so the open gap is a file that ends in a trailing delimiter: one miniature file with that case, totals compared old against new, closes it, and the report names other encodings as untested. See [identify the evidence gap](experiment-verification.html#identify-the-evidence-gap).

</section>

<section class="card" id="checks-and-failures">

## Check application logic, custom numerical code and regressions only where their risk applies

<p class="bs-lead">Each targeted check covers a place where a plausible error survives ordinary testing, and is required only when its condition holds.</p>

<figure id="fig-reference">
<div class="xp-fig" role="img" aria-label="At the top, the stated formulas or an independent source. The custom numerical code implements them; the independent reference is derived from them. A reference derived from the production or generated logic is crossed out: it shares the suspected error. Both feed a comparison over the relevant regimes with tolerances chosen for the claim; an executable self-check fails its exit status beyond the tolerance and reports observed agreement with its scope.">
<div class="xp-ref">
<div class="xp-box xp-blue xp-src"><span class="xp-tag">Source</span><b>Stated formulas or an independent source</b><p>the motion equations, a case with a known solution</p></div>
<div class="xp-down a1">implements</div>
<div class="xp-down a2">derived from</div>
<div class="xp-box xp-orange xp-prod"><span class="xp-tag">Under test</span><b>Custom numerical code</b><p>the simulation's integrator</p></div>
<div class="xp-cross"><b>not derived from production or generated logic</b>a reference that shares the suspected error is no evidence against it</div>
<div class="xp-box xp-teal xp-refr"><span class="xp-tag">Reference</span><b>Independent derivation</b><p>can expose errors shared by production code</p></div>
<div class="xp-down a3">compare</div>
<div class="xp-down a4">compare</div>
<div class="xp-box xp-violet xp-cmp"><span class="xp-tag">Self-check</span><b>Over the relevant regimes</b><p>step sizes and speeds, tolerances chosen for the claim; the exit status fails beyond them, and agreement is stated with its scope, never presumed.</p></div>
</div>
</div>
<figcaption><b>Figure 9.</b> A custom integrator checked against a reference that can disagree with it. The case is illustrative; the diagram is authored in the page source.</figcaption>
</figure>

[Figure 9](#fig-reference) draws the check for custom numerical code that no trusted reference covers: the reference comes from the formulas, not from the code under test, because one derived from that code agrees with its errors. The other two checks:

- **Application logic**, where it affects the claim: data identity and composition, leakage, metric definitions and aggregation, and how configuration, library calls and saved outputs compose. Pick cases that can expose a plausible wiring error, including one that still looks reasonable. Ordinary library use needs no recertification: verify the application's use, and look into the library only when a concrete risk or the claim depends on its behavior. Learned or fitted models add the [model-specific checks](#learned-or-fitted-models-only).
- **A regression gate**, where a fixed defect or difficult case could return unnoticed; the project decides its scope. It keeps those cases, documents its tolerances and, where available, fails on a known-bad state. A fast gate targets under five seconds; the target limits gates, not experiments.

<!-- fold: detail When higher precision, exhaustive replay or another backend is justified -->

Only when it addresses the claim and a risk the reference comparison leaves uncovered. Optional native comparisons are explicitly guarded.

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
<figcaption><b>Figure 10.</b> From a change to current evidence, and from a failure to an open decision.</figcaption>
</figure>

[Figure 10](#fig-failure) follows a change to a decision. Evidence describes the source, inputs and conditions that produced it, so a change leaves the affected results describing an older state. Lowering a failed bar to make the same result pass would turn the check into a description of the result, so the original criterion and failure stay on record.

For example, a dependency update lands before a performance comparison of two request handlers is reported. The timings it affects are rerun, unaffected parser tests are reused after confirming the same source and inputs, and a failure is investigated against the agreed tolerance instead of widening it.

<!-- fold: detail Interruptions and what the report states -->

Where an interruption could affect a run's validity or cost, verify the recovery that matters for that run: checkpoints, resume identity, partial outputs or restart. No universal interruption suite is added. The report keeps apart, under the [handoff guide](handoffs.html), the checks executed, their results, conclusions by inspection only and the remaining uncertainty; reuse after a change follows the [staleness rules](records.html#numbers-and-staleness).

<!-- /fold -->

See [changes and failures](experiment-verification.html#respond-to-changes-and-failures).

</section>
