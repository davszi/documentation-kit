# Execution and shared resources

Apply reservation, usage-cache and receipt rules when the project uses those
mechanisms. The project defines its concrete controls and required records.

## Choose the project's execution route

Before an expensive job, read the project's execution and environment
instructions. Verify the executable, loaded source, inputs and relevant
environment. Use its supported entrypoint and resource controls, including
applicable admission, review and attendance requirements.

## Coordinate conflicting work

For jobs competing for significant shared resources, coordinate admission and
adequate reservations. Respect host headroom and existing reservations. Do not
lower an adequate budget to force admission or bypass controls with local
overrides. An idle host does not remove required containment.

Follow the [parallel-work rules](delivery.md#parallel-work) for protecting active
inputs and outputs. Use exclusive execution when interference would invalidate
timing or when lifecycle, runaway, signal or resource-stress work requires it.

## Select a resource budget

Use a sufficiently comparable successful measurement when available. Otherwise,
choose a deliberately generous initial reservation covering startup,
compilation, children and cleanup. Avoid repeated small increases after
preventable memory failures. State the reservation basis and distinguish
reserved capacity from measured consumption.

Choose deadlines and cleanup reserves appropriate to the operation. Apply the
project's separate timing rules for bounded jobs and attended sessions.

## Reuse successful usage records conservatively

Reuse a successful reservation only when workload, command, checkout/source
state, executable, relevant environment, environment metadata and input identity
match. Explicitly identify external or dynamic inputs and import roots. Changed
identity requires an explicit adequate reservation again. Estimates and failed
bounds cannot serve as successful measurements.

A temporary cache supports budget selection and confers no execution authority.
For immutable run requests, bind limits before freezing the request and validate
those pinned limits at launch instead of selecting replacements from mutable
cache. Retain evidential measurements under the
[evidence rules](../records.md#numbers-and-staleness).

## Attribute failures from evidence

Record command and resource outcomes separately. Test failures alone do not
establish exhaustion. Use actual memory-limit evidence for an insufficient
memory bound. Missing peaks, timeouts and cleanup failures do not measure memory
needs. Do not attribute host free-memory changes to a job. An unavailable
terminal peak remains unmeasured.

For unexpected pressure or inadequate budgets, follow the
[escalation rules](delivery.md#decisions-and-blockers). Preserve attempts and
their original settings under the [evidence rules](../records.md#numbers-and-staleness).

## Own supervision and cleanup

Name the owner of admission, launch, supervision, results and cleanup. Retain
ownership through cleanup of children and temporary resources. Job records
include process and source identity, actual limits, exit outcome and observed
cleanup. Apply the [durable-record rules](handoffs.md#evidence-and-durable-records).

Stop only owned jobs and services. Resolve uncertain ownership and confirm
cleanup before releasing a reservation. Treat failed or incomplete cleanup as
a [handoff blocker](handoffs.md#reporting-blockers).

Scale records to the work. Routine checks need concise command, limits and
result records. A [qualification](../experiments/workflow.md#choose-the-purpose) follows the project's full evidence chain and
the [claim-scope rules](../records.md#naming-and-honest-claims).
