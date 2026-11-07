# Proportionate experiment verification

Choose verification for the claim and its consequential failure modes. Run
requirements already adopted by the project remain binding. This guide does
not replace or relax an existing execution or acceptance contract.

## Identify the evidence gap

Before adding a substantial check, name the consequential error it could expose
and the evidence gap left by existing checks. Start with applicable prior
evidence, tests and runtime assertions; verify their source, inputs and scope.
Reuse them when they cover the question.

Choose the cheapest credible diagnostic that can expose the error. A miniature
pipeline, targeted case or source inspection may answer a narrow question;
state what remains untested. A broader check is justified when a smaller one
cannot resolve the gap. A final-run label or planned paper does not itself
require an additional audit.

## Check the experiment's application logic

Check data identity and composition, preprocessing, split boundaries, leakage,
label or target alignment, metric definitions and aggregation where they affect
the claim. Check how the application configures and composes models, objectives,
optimizers, library calls and saved outputs. Select cases that can expose a
plausible application error, including incorrect wiring that still produces
apparently reasonable results.

Ordinary use of a library does not require recertifying that library. Verify
the application's use and relevant assumptions. Investigate library or backend
behavior further when a concrete risk, discrepancy or claim depends on it.
Training-objective comparisons do not automatically require independently
reimplementing each objective.

## Validate custom numerical implementations

When the experiment evaluates correctness of a custom numerical implementation,
use an independent derivation or suitable reference that can expose errors
shared by production code. Choose comparison regimes and tolerances according
to the claimed behavior.

For method-level numerical experiments, derive the reference from the stated
formulas or an appropriate independent source rather than copying generated or
production implementation logic. Compare it with the production implementation
over the relevant regimes. An executable self-check must report disagreement
and fail its exit status when the stated tolerance is exceeded. State observed
agreement and its scope rather than presuming parity.

Use independent derivations, higher precision, exhaustive replay or comparisons
with a native implementation or another backend only when they address the
claim and an uncovered error risk. Guard optional native comparisons so their
availability and execution are explicit. A reference sharing the suspected
error is not independent evidence against that error.

For numerical regression gates, retain historically difficult regimes and
document tolerances. Include a known-bad state or implementation where available
to show the gate detects the failure. Keep routine engineering gates thin;
target under five seconds for a fast regression gate. This engineering target
is not a time limit or required audit for every research comparison.

## Respond to changes and failures

When source, inputs, splits, metrics, composition or runtime conditions change,
rerun the affected checks before treating their evidence as current. Reuse
unaffected evidence only after confirming its identity and scope. The
[evidence guide](../writing/evidence.md#numbers-and-staleness) owns measured-claim
staleness and historical reporting.

Investigate failed checks against the agreed criteria. Do not lower a failed
bar to make the same result pass. Changes to an obsolete or inappropriate
criterion need an explicit project decision and rationale, with the original
failure retained.

When interruptions or lost work could affect validity or cost, verify the
relevant recovery behavior: checkpoint integrity, resume identity, partial
outputs and restart semantics. Choose the cases that matter to that run; do not
add a universal interruption suite.

Report checks executed, results, inspection-only conclusions and remaining
uncertainty through the [handoff guide](../engineering/handoffs.md). Keep
artifacts under the [evidence rules](../writing/evidence.md) and run checks under
the [execution rules](../engineering/execution.md).
