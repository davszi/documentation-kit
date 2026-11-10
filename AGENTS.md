# Engineering and documentation kit development

> **Scope:** these instructions apply only when the working repository is the
> documentation kit itself. If you reached this file through a consuming
> project's `.docs-kit/` submodule, ignore it and follow that project's own
> `AGENTS.md`.

Read `docs/KIT_CONTEXT.md` once for repository orientation, unless already
loaded. Its `docs/KIT_INDEX.md` links to focused guides. Policies live in `rules/`;
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
| Running tests, builds, benchmarks or other expensive jobs | `rules/engineering/execution.md` and the environment/check commands in `docs/KIT_CONTEXT.md` |
| Assigning work, coordinating contributors or editing in parallel | `rules/engineering/delivery.md` |
| Reporting completion or blockers, handing off work or integrating a handoff | `rules/engineering/handoffs.md` |
| Staging, committing or rewriting Git history | `rules/engineering/git.md` and repository validation requirements |
| Writing or changing a record: a guide, topic record, plan, worklog or open-work entry | `rules/records.md`, and in `rules/documentation.md` the sections from **Record first, page on request** through **Rules for changes and chronology** |
| Creating, moving, splitting or retiring a document | `rules/documentation.md` |
| Making a new page for people, only when a person asked for one, or page work on an existing page beyond a small sync | **Record first, page on request** and **Rendered pages are for people** in `rules/documentation.md`; the page author reads the applicable focused guides linked from `rules/writing.md` and `rules/maintenance.md` |
| Building, checking, reviewing rendered output, publishing or changing the site or reader | The applicable focused guides linked from `rules/maintenance.md` and the checks in `docs/KIT_CONTEXT.md` |

`docsite.py` owns the consumer entrypoint, `tooling/` implements rendering and
validation, `theme/` owns the shared reader, and `examples/starter/` demonstrates
the supported authoring contract.

Preserve reader behavior, source/public anchors, local assets and evidence
boundaries when changing the shared implementation. Run the README checks and
rendered wide/narrow inspection after relevant changes. Do not edit generated
`.build/` output. Consumer-specific compatibility stays with its project.
