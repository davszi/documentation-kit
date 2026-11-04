# Documentation kit development

Read `rules/documentation.md`, `rules/writing.md`, `rules/maintenance.md` and
`README.md` before editing. Policies live in `rules/`; do not duplicate them here.
Read `docs/project/PROJECT_CONTEXT.md` for repository-specific context and checks.

`docsite.py` owns the consumer entrypoint, `tooling/` implements rendering and
validation, `theme/` owns the shared reader, and `examples/starter/` demonstrates
the supported authoring contract. `provenance.json` records extraction inputs.

Preserve reader behavior, source/public anchors, local assets and evidence
boundaries when changing the shared implementation. Run the README checks and
rendered wide/narrow inspection after relevant changes. Do not edit generated
`.build/` output. Consumer-specific compatibility stays with its project.
