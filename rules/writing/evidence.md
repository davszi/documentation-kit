# Measurements and experiment evidence

## Numbers and staleness

A current measured claim requires a source commit, exact reproduction command, runtime/environment, workload, units, baseline, method and scope. Link its raw result and limitations. Config values, derivations and design arithmetic are not measurements; cite their source and label them accordingly.

When code, input data, method, workload or runtime conditions affecting a claim change, rerun before quoting it as current qualification. Keep the old record's date, runtime, inputs and scope; a historical label does not qualify changed inputs. Presentation-only edits may reuse captured results only after checking identities, numbers and treatments remain intact.

When a redesign restates numbers in new prose, figures or slides, record each number's source in a ledger and lock the evidence blocks kept verbatim (see [generated figures](../site/authoring.md#generated-figures)). A slide face may show only numbers that its chapter also shows; every distinct number a redesigned chapter shows, figure labels included, has a ledger source.

Keep protocols, outputs, snapshots, failed attempts, changed settings, actual outcomes, reviews and relevant uncertainty with the work that produced them. For experiments, also retain producing code, inputs, full result tables, source pins and independent reviews in the experiment directory. The page explains what they establish. The worklog records the landing and hashes without duplicating tables. Retained measured content remains subject to the [deletion gate](../documentation.md#rules-for-changes-and-chronology).

Historical records preserve their original source pins, inputs, runtime, settings, resource limits, deadlines and verdicts where those fields apply.

## Run visuals and experiment lifecycle

Prefer scripted captures with the same provenance as other figures. An inherently interactive screenshot must state commit, date and scenario/preset; it illustrates appearance, never a quantitative claim. Derive overlays from recorded artifacts rather than screenshots when data exists. Show dynamic behavior through an intentionally packaged short clip or useful frame sequence, with normal captions and provenance. For large local captures, posters/keyframes and their published notices, follow the [local-media packaging rules](../site/resources.md#resource-closure-and-evidence).

A live public experiment report uses `ongoing = true`; remove it only when findings and limits are settled. Apply the [experiment retention rules](#numbers-and-staleness). The owning topic explains scope and links to evidence.

Every complete experiment includes:

- Reproduction command and runtime; provide a quick mode when the full run exceeds about one minute.
- Measured motivation, strongest cheap baseline and acceptance bar stated before results.
- Results with units, verdict against the bar (including failure), caveats and path forward.

Verify the baseline before changing measured behavior. A production benchmark drives shipped paths end to end with honestly labelled ablations, reusable case generation/metrics, runtime reporting and provenanced figures. A method experiment adds an independent derivation from published formulas rather than copying implementation, a guarded optional native comparison and an exit self-check. State observed agreement, not presumed parity.

Use a thin regression gate covering historically difficult regimes, documented band tolerances and a known-bad failure when available. Keep fast gates short (target under five seconds). Suitable experiment visuals include actual-geometry quality overlays, convergence, reference parity, timing/scaling and trade-off plots; omit inapplicable views explicitly. Update topic, worklog and open routing in the same deliverable.
