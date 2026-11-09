# Documentation reading index

[Project context](KIT_CONTEXT.md) owns the repository map and development
commands. [README](../README.md) owns consumer setup and upgrades.

## Engineering practices

- [Code and repository practices](../rules/engineering/code.md): diagnostics, consumed output and generated files.
- [Efficient implementation](../rules/engineering/performance.md): routine efficiency and workload-scoped measurements.
- [Execution and shared resources](../rules/engineering/execution.md): environment identity, budgets, evidence, supervision and cleanup.
- [Delivery](../rules/engineering/delivery.md): assignment, ownership, parallel work and escalation.
- [Handoffs](../rules/engineering/handoffs.md): completion, blockers, durable evidence and receipt.
- [Git practices](../rules/engineering/git.md): deliverables, validation, messages, staging and history.

## Experiments

- [Experiment workflow](../rules/experiments/workflow.md): keeping experiments small, investigations and qualifications, baselines, stopping and required content; final runs only for learned or fitted models.
- [Proportionate verification](../rules/experiments/verification.md): evidence gaps, application logic, numerical correctness and regression gates.

Projects keep concrete questions, recipes, decisions and accepted execution
contracts in their owning records. [Evidence reporting](../rules/writing/evidence.md)
and [execution](../rules/engineering/execution.md) retain their separate ownership.

## Documentation and writing

[Project conformance check](../rules/conformance.md) is what a project checks when its pin moves.
[Documentation policy](../rules/documentation.md) owns canonical homes and
lifecycle. The [writing router](../rules/writing.md) links to page design,
explanations, measurements, figures, mathematics and code guides.

## Reference website

The [website record](topics/website/website.md) owns the kit's own site: its
structure, source registry, build command and open hosting decision.
[Open work](open/KIT_OPEN.md) routes owed workstreams to their owners.

## Site development

The [site router](../rules/maintenance.md) links to authoring, validation,
resources, publication and shared-reader contracts.
[Panel-switcher contract](topics/panel-switcher/panel-switcher.md) owns the
shared independent-comparison component.

## Evidence and chronology

[Releases and upgrades](topics/releases/releases.md) owns version changes and
stable interfaces. The [2.0.0 migration guide](topics/releases/migrations/2.0.0.md)
moves 1.1.0 consumers to the current release; the
[1.1.0 guide](topics/releases/migrations/1.1.0.md) covers the earlier step.

The extraction record, policy map, source hashes and initial receipts remain at
the [`v1.1.0` tag](https://github.com/davszi/documentation-kit/tree/v1.1.0).
[Worklog](KIT_WORKLOG.md) is append-only chronology.
