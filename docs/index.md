# Documentation reading index

[Project context](PROJECT_CONTEXT.md) owns the repository map and development
commands. [README](../README.md) owns consumer setup and upgrades.

## Engineering practices

- [Code and repository practices](../rules/engineering/code.md): diagnostics, consumed output and generated files.
- [Efficient implementation](../rules/engineering/performance.md): routine efficiency and workload-scoped measurements.
- [Execution and shared resources](../rules/engineering/execution.md): environment identity, budgets, evidence, supervision and cleanup.
- [Delivery](../rules/engineering/delivery.md): assignment, ownership, parallel work and escalation.
- [Handoffs](../rules/engineering/handoffs.md): completion, blockers, durable evidence and receipt.
- [Git practices](../rules/engineering/git.md): deliverables, validation, messages, staging and history.

## Experiments

- [Experiment workflow](../rules/experiments/workflow.md): investigations, final runs, question design, evaluation and stopping conditions.
- [Proportionate verification](../rules/experiments/verification.md): evidence gaps, application errors and scoped numerical correctness.

Projects keep concrete questions, recipes, decisions and accepted execution
contracts in their owning records. [Evidence reporting](../rules/writing/evidence.md)
and [execution](../rules/engineering/execution.md) retain their separate ownership.

## Documentation and writing

[Documentation policy](../rules/documentation.md) owns canonical homes and
lifecycle. The [writing router](../rules/writing.md) links to page design,
explanations, measurements, figures, mathematics and code guides.

## Site development

The [site router](../rules/maintenance.md) links to authoring, validation,
resources, publication and shared-reader contracts.
[Panel-switcher contract](topics/panel-switcher/panel-switcher.md) owns the
shared independent-comparison component.

## Evidence and chronology

[Releases and upgrades](topics/releases/releases.md) owns version changes and
stable interfaces. The [1.1.0 migration guide](topics/releases/migrations/1.1.0.md)
routes existing consumers through policy, layout and adapter changes.

[Extraction record](topics/extraction/extraction.md) owns initial scope,
evidence and limits. [Extraction map](../rules/extraction-map.md) accounts for
policy source sections; [provenance](../provenance.json) records source
identities. [Worklog](worklog.md) is append-only chronology.
