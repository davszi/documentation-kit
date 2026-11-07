# Experiment workflow

This guide owns shared experiment purposes and design choices. Projects link
here and keep their questions, selected recipes, acceptance criteria, execution
contracts and decisions in project-owned records. Existing execution contracts
remain in force; adopting this guide does not silently change them.

## Choose the purpose

- An investigation answers a question or reduces uncertainty. Its useful
  outcome may be negative or inconclusive.
- A final run uses a selected recipe to produce the intended artifact or model.
  It has a different purpose, not an automatic rigor or publication tier.
  Keep the selected recipe fixed during the run. Record a recipe change as a
  distinct attempt.

Several investigations may inform one final run. There is no fixed number or
quota. Choose further work because an unresolved question matters to the next
decision, not because a run has a particular label.

Exploration and confirmation describe another distinction. Exploration develops
questions, methods or choices from observed evidence. Confirmation evaluates a
specified claim with choices fixed before examining its evaluation results.
State which role the evidence serves; a final run is not automatically a
confirmatory test, and an investigation can test a fixed claim.

## Start from evidence and bound the question

Read relevant prior results, failures, code and accepted decisions first. Check
whether their inputs and scope apply. Identify the uncertainty that remains and
the decision its resolution would change.

Choose the smallest credible question or comparison that can resolve it. For
confirmation and agreed acceptance checks, state the expected observation, what
would count as failure or inconclusive evidence, and interpretation criteria
before inspecting results. Exploratory interpretation may evolve as evidence
arrives; label it accordingly and retain changes and their reasons. For a final
run, state the selected recipe, intended output and criteria for a usable result.

Use relevant baselines and verify that they measure the intended behavior.
Choose variation and independent replication according to the claim: datasets,
environments, subjects, cases, seeds or initializations may answer different
questions. Repeated initializations on one dataset do not establish replication
across independent datasets. Explain the remaining limits.

Agree on resource bounds, stopping conditions and conditions for changing
approach. Stop when the question is answered, the stated limits are reached or
the evidence shows that the approach cannot answer it. Preserve failed attempts
and changed settings rather than silently replacing them.

## Keep evaluation separate from tuning

Identify which data and observations guide method, hyperparameter or recipe
selection, and which evaluate the resulting claim. Keep evaluation independent
of tuning to the extent the claim requires. If evaluation results influence
selection, report that use and narrow the claim or obtain fresh evaluation
evidence. Repeating runs does not repair evaluation leakage.

Preserve negative and inconclusive results, deviations, failure criteria and
their observed outcomes. Do not report only the best seed, successful case or
completed attempt as though it represented the full comparison.

## Use the existing owners

Choose checks through [proportionate verification](verification.md). The
[execution guide](../engineering/execution.md) owns environment identity,
resource controls, supervision and cleanup. The
[evidence guide](../writing/evidence.md) owns provenance, retention, reporting
and run visuals. The [documentation policy](../documentation.md) owns canonical
placement, topic/worklog updates and open-work routing. These links do not add
an approval, receipt or parallel status system.
