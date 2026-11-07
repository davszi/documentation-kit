# Agent entrypoint

Read `docs/PROJECT_CONTEXT.md` once for orientation, unless already loaded.
Use `docs/index.md` for named documentation routes. Initialize the pinned
`.docs-kit` submodule before relying on its rules. If required shared policy is
missing, report it and resolve the prerequisite before proceeding with the
work it governs.

## Read before the relevant action

Apply every matching route before its action. Load additional routes when
scope expands. Follow named topic and experiment links for task-specific
inputs. These routes grant no execution or publication permission.

| Before… | Read… |
|---|---|
| Changing source, tests or repository configuration | `.docs-kit/rules/engineering/code.md` and the owning project topic or development guide |
| Changing runtime cost or making performance claims | `.docs-kit/rules/engineering/performance.md` and the project's workload/acceptance contract |
| Designing an investigation or final run | `.docs-kit/rules/experiments/workflow.md` and the project's owning experiment records |
| Choosing or changing experiment checks or interpreting their failures | `.docs-kit/rules/experiments/verification.md` and the project's accepted verification contract |
| Running tests, builds, benchmarks or other expensive jobs | `.docs-kit/rules/engineering/execution.md` and the project's recorded environment and execution requirements |
| Assigning work, coordinating contributors or editing in parallel | `.docs-kit/rules/engineering/delivery.md` |
| Reporting completion or blockers, handing off work or integrating a handoff | `.docs-kit/rules/engineering/handoffs.md` |
| Staging, committing or rewriting Git history | `.docs-kit/rules/engineering/git.md` and the project's recorded validation requirements |
| Creating, editing, moving, reviewing, publishing or retiring documentation | `.docs-kit/rules/documentation.md` |
| Writing explanations, mathematics, code excerpts, figures or evidence | The applicable focused guides linked from `.docs-kit/rules/writing.md` |
| Building, checking, reviewing rendered output, publishing or changing the site | The applicable focused guides linked from `.docs-kit/rules/maintenance.md` and **Build and review** in `docs/PROJECT_CONTEXT.md` |
