# Proportionate experiment verification

Match verification to the claim and its consequential failures, within
[keeping experiments small](workflow.md#keep-experiments-small). Adopted
project requirements remain binding.

## Identify the evidence gap

Before adding a check, name the error it could expose and the gap existing
checks leave. Reuse prior evidence, tests and assertions whose source, inputs
and scope cover the question.

Choose the cheapest credible diagnostic, such as a miniature pipeline, targeted
case or source inspection, and state what remains untested. Go broader only
when a smaller check cannot close the gap. Neither the
experiment's kind nor a planned publication by itself requires an extra audit.

## Check the experiment's application logic

Check data identity and composition, leakage, metric definitions and
aggregation, and how the experiment composes configuration, library calls and
saved outputs, where they affect the claim. Pick cases that can
expose a plausible wiring error, including one that still looks reasonable.
For learned or fitted models, also apply the
[model-specific checks](workflow.md#learned-or-fitted-models-only).

Ordinary library use needs no recertification of the library; verify the
application's use, and look deeper only when a concrete risk or claim depends
on library behavior.

## Validate custom numerical implementations

When results depend on custom numerical code that no trusted reference already
covers, compare it with an independent derivation or suitable reference that
can expose errors shared by production code. Derive the reference from the
stated formulas or an independent source, never from generated or production
logic: a reference sharing the suspected error is no evidence against it.
Compare over the relevant regimes with tolerances chosen for the claim.
An executable self-check reports disagreement and fails its exit status when the
tolerance is exceeded. State observed agreement and its scope; do not presume
parity.

Use higher precision, exhaustive replay or a native or other-backend comparison
only when it addresses the claim and an uncovered risk. Make optional native
comparisons explicitly guarded.

## Maintain regression gates

Add a regression gate when a fixed defect or historically difficult case
could return unnoticed; the project decides its scope. A gate keeps those
cases, documents its tolerances and, where available, shows it fails on a
known-bad state or implementation. Keep routine gates thin: target under five
seconds for a fast gate. The target limits gates, not experiments.

## Respond to changes and failures

When source, inputs, splits, metrics, composition or runtime conditions change,
rerun the affected checks before treating their evidence as current; reuse
unaffected evidence only after confirming its identity and scope (see
[staleness](../records.md#numbers-and-staleness)).

Investigate failed checks against the agreed criteria. Do not lower a failed
bar to make the same result pass. Changing an obsolete criterion needs an
explicit project decision and rationale, with the original failure retained.

When interruptions could affect validity or cost, verify the recovery behavior
that matters to that run (checkpoints, resume identity, partial outputs, restart); add no
universal interruption suite.

Report checks executed, results, inspection-only conclusions and remaining
uncertainty under the [handoff guide](../engineering/handoffs.md).
