# Engineering and documentation kit development

Read `docs/PROJECT_CONTEXT.md` once for repository orientation, unless already
loaded. Its `docs/index.md` links to focused guides. Policies live in `rules/`;
do not duplicate them here.

## Read before the relevant action

Apply every matching route before its action. Load more routes when scope
expands. These routes grant no execution or publication permission.

| Before… | Read… |
|---|---|
| Changing source, tests or repository configuration | `rules/engineering/code.md` and the owning topic or implementation contract |
| Changing runtime cost or making performance claims | `rules/engineering/performance.md` |
| Designing or running an experiment, qualification or benchmark | `rules/experiments/workflow.md` and the project's owning experiment records |
| Choosing or changing experiment checks or interpreting their failures | `rules/experiments/verification.md` and the project's accepted verification contract |
| Running tests, builds, benchmarks or other expensive jobs | `rules/engineering/execution.md` and the environment/check commands in `docs/PROJECT_CONTEXT.md` |
| Assigning work, coordinating contributors or editing in parallel | `rules/engineering/delivery.md` |
| Reporting completion or blockers, handing off work or integrating a handoff | `rules/engineering/handoffs.md` |
| Staging, committing or rewriting Git history | `rules/engineering/git.md` and repository validation requirements |
| Creating, editing, moving, reviewing, publishing or retiring documentation | `rules/documentation.md` |
| Writing explanations, mathematics, code excerpts, figures or evidence | The applicable focused guides linked from `rules/writing.md` |
| Building, checking, publishing or changing the site or reader | The applicable focused guides linked from `rules/maintenance.md` and the checks in `docs/PROJECT_CONTEXT.md` |

`docsite.py` owns the consumer entrypoint, `tooling/` implements rendering and
validation, `theme/` owns the shared reader, and `examples/starter/` demonstrates
the supported authoring contract. `provenance.json` records extraction inputs.

Preserve reader behavior, source/public anchors, local assets and evidence
boundaries when changing the shared implementation. Run the README checks and
rendered wide/narrow inspection after relevant changes. Do not edit generated
`.build/` output. Consumer-specific compatibility stays with its project.
