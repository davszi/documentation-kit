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

The [evidence guide](../writing/evidence.md) owns measurement identity, baselines,
reruns, historical results and reporting. Projects retain concrete workloads,
thresholds and performance contracts.
