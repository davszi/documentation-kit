# Experiment workflow

This guide owns shared experiment design. Projects keep questions, criteria,
contracts and decisions in their own records; existing contracts still apply.

## Keep experiments small

Read first. These limits never waive the required content.

- Start smallest: a one-line
  [probe](../documentation.md#rules-for-changes-and-chronology) before an
  experiment, one comparison before a grid. A probe needing more than its line
  is an investigation.
- Before adding a run, check, document or gate, name the decision it changes
  and the error it would catch. If you cannot, do not add it.
- Add no registries, receipts, templates, approval steps, audit files or status
  boards unless the project asks.
- Import no other field's methods (preregistration, ablation grids,
  [learned-model practices](#learned-or-fitted-models-only)) unless the results
  depend on them.
- Agree the budget (time, compute, files) and when to change approach first.
  Ask before exceeding it or widening the question.
- There is no quota. Do more only when an open question matters to the next
  decision.

## Choose the purpose

Classify by what the result decides, not by the project's field. Test: does it
accept or reject a named system against a bar fixed before the run? Then it is
a qualification; otherwise an investigation.

- An **investigation** answers a question; "no" or "inconclusive" is a
  finding. Declare it before running as *exploratory* (choices may develop from
  observations) or *confirmatory* (claim and judgment fixed before evaluation
  results). A paper's headline comparison is confirmatory.
- A **qualification** gives a pass, fail or inconclusive verdict on a named
  system, build or model: platform qualification, a benchmark contract, a
  parity check, model release evaluation.

An exploratory finding is not a confirmation or qualification. Before a
decision relies on it, test it on evidence that did not shape it.

## Start from evidence and bound the question

Read prior results, failures, code and decisions first; check that their inputs
and scope apply. Choose the smallest comparison that resolves what remains.
Before changing measured behavior, verify that the strongest relevant baseline
the budget allows measures the intended behavior; for shipped behavior it runs
the shipped path. Match replication to the claim: repeating one case, scenario,
seed or dataset does not replicate across others. Stop when the question is
answered, the budget is reached or the approach cannot answer it.

## Keep evaluation separate from tuning

Separate the data, cases or scenarios that guide choices from those that
evaluate the claim, as far as the claim requires. If evaluation results
influenced selection, say so and narrow the claim or get fresh evidence;
repeating runs does not repair leakage.

## Required content

Every experiment, exploratory included, states before running its question and
measured motivation, kind, the decision it informs, baseline, budget and
stopping condition. A confirmatory investigation or qualification also fixes
its bar or expected observation, tolerances, workload, analysis and what counts
as failure or inconclusive.

Every experiment reports: reproduction details under the
[measurement rules](../records.md#numbers-and-staleness); results with
units and scope; the verdict for a confirmatory investigation or qualification;
every attempt, failure and changed setting with its reason, never only the best
one; for exploration, how the interpretation developed; caveats and next step.
A failed bar is [never lowered](verification.md#respond-to-changes-and-failures).

## Learned or fitted models only

Skip this section unless results depend on a model learned or fitted from data.
Nothing here applies to other experiments.

- A **final run** trains a selected recipe to produce the model that will be
  reported or used. It is a production step, not a rigor tier. Fix the recipe
  and usable-result criteria first; a recipe change is a new attempt. An
  investigation or qualification judges its output.
- Check splits, preprocessing and label or target alignment.
- Comparing training objectives does not require reimplementing each one.

## Use the existing owners

Checks: [verification](verification.md). Resources and cleanup:
[execution](../engineering/execution.md). Provenance and visuals:
[evidence](../records.md#numbers-and-staleness). Benchmarks:
[performance](../engineering/performance.md). Placement:
[documentation policy](../documentation.md).
