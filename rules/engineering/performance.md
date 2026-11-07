# Efficient implementation

## Efficient by default

Use the [delivery rules](delivery.md#decisions-and-blockers) for scope and
architecture decisions arising from performance work.

- Write invariant data, such as headers, manifests, source hashes and recipes,
  once and reference it. Do not repeat it per step or call.
- Use batch operations where the API allows. Read and write related state
  together instead of making repeated engine or service calls per item.
- Keep debug and evidence work, such as checkers, observers and full per-step
  records, opt-in and outside the normal path. It must not set normal-run cost.
- Avoid repeated allocation and copying of large structures in hot paths.
- Fix waste in the current implementation when found within the assigned scope.
  Moving code to another language requires an explicit decision with the project
  owner; it is never the default response to waste.
- Follow the [measurement rules](../writing/evidence.md#numbers-and-staleness)
  when claiming a speed-up.

## Workload and evidence

Measure the declared workload and execution path. Claims about shipped
performance use the shipped path with its required work. Label diagnostic and
ablation timings by the paths they measure.

A production benchmark drives shipped paths end to end. Use honestly labelled
ablations, reusable case generation and metrics, runtime reporting and
provenanced figures. Verify the baseline before changing measured behavior and
use the strongest relevant cheap baseline for the comparison.

For engineering benchmarks and numerical validation tools, provide a quick mode
when the full run exceeds about one minute. Label the quick mode's coverage;
it does not replace the full workload or its acceptance criteria. This is
engineering iteration guidance, not a requirement that every research run
finish quickly or provide a shortened scientific protocol.

Use [proportionate verification](../experiments/verification.md) for numerical
correctness and regression gates.

The [evidence guide](../writing/evidence.md) owns measurement identity, baselines,
reruns, historical results and reporting. Projects retain concrete workloads,
thresholds and performance contracts.
