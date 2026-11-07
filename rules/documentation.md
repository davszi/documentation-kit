# Documentation system

Every fact has exactly one canonical home. Other documents link to it. When copies disagree, verify the owning source, correct the stray copy and update affected summaries in the same deliverable.

These rules are shared policy. A consuming project's `docs/PROJECT_CONTEXT.md` owns its repository map, commands, named documentation routes and project-specific choices. Do not copy these rules into project entrypoints.

## Canonical homes

| Artifact | Owns |
|---|---|
| `docs/PROJECT_CONTEXT.md` | Project purpose, repository map, run/build instructions and named documentation routes |
| `docs/index.md` | Documentation reading index: routes to development guidance, topics, evidence, sessions and open work |
| `docs/development/`, including conventions when needed | Project-specific engineering choices, commands and current repository invariants |
| `.docs-kit/rules/documentation.md` | Documentation placement, lifecycle, review and agent routing |
| `.docs-kit/rules/writing.md` and `writing/` | Writing router and focused human-facing content, evidence, figures and presentation guides |
| `.docs-kit/rules/maintenance.md` and `site/` | Site router and focused authoring, reader, resources, validation and publication guides |
| `.docs-kit/rules/engineering/code.md` | Logging, consumed program output and generated-file practices |
| `.docs-kit/rules/engineering/performance.md` | Routine efficiency, representative workloads and measured performance claims |
| `.docs-kit/rules/engineering/execution.md` | Execution identity, conditional shared-resource budgeting, supervision and cleanup |
| `.docs-kit/rules/engineering/git.md` | Commit scope, messages, validation and safety when sharing a Git checkout |
| `.docs-kit/rules/engineering/delivery.md` | Assignment scope, delivery ownership, parallel work and escalation |
| `.docs-kit/rules/engineering/handoffs.md` | Completion and blocker reports, durable evidence and handoff receipt |
| `docs/topics/<topic>/<topic>.md` and further descriptively named records | Canonical mechanisms, accepted specifications, methods, scoped results, limits and topic-owned research notes |
| `docs/topics/<topic>/index.md`, when needed | Human explanation drawn from the topic records: current conclusions, figures, decisions and blockers |
| `docs/open/OPEN.md` | One-line routes to every owed workstream, each with its owning document; never a duplicate task board |
| Named unfinished plans/decision records | Unfinished delivery, prospective acceptance, unresolved choices and their owners |
| `docs/worklog.md` | Append-only chronology: landed work, reasons, measured effects and probes |
| Producing experiment directory | Protocol, producing code, inputs, raw results, failures, source pins, reviews and reproduction instructions |
| `docs/topics/<topic>/evidence/` | Topic-owned supporting sources and dated reviews retained for a concrete citation or reproduction purpose |
| `docs/evidence/`, when needed | Supporting evidence spanning topics, with an explicit owner and concrete citation or reproduction purpose |
| `docs/sessions/`, when needed | Dated temporary coordination, assignments and resume state; current requirements and results remain in their owning records |
| `docs/site/` | Consumer configuration, local assets/fragments and explicit overrides |
| `.docs-kit/` | Version-pinned shared rules, engine and theme; update its revision deliberately |
| `.build/docs/` | Ignored generated site; never hand-edit or commit |
| `README.md` | Bounded human landing summary, with links to canonical homes |

These are canonical roles for new projects; existing projects may retain explicit
local destinations and compatibility routes. Create a directory or document only
when content needs it, and link that owner from `docs/index.md`.

Other Markdown must have a defined role: a subject record, log, experiment contract/guide, exact evidence, or unfinished plan/decision. Do not create a generic archive, review collection or second status system to avoid choosing an owner. Names explain the subject or mechanism; avoid vague `Info` or `Manager` labels.

## Rendered pages are for people; records stay Markdown

Start a topic as `docs/topics/<topic>/<topic>.md`; split growing records into descriptively named files. Do not name subject records `README.md`. Add `index.md` only when a human has something to learn or act on.

A rendered page explains current conclusions, accepted specifications, demonstrated behavior with its evidence scope, useful figures and the decisions needed next. Contracts, handoff/resume state, readiness boards, bookkeeping and long run chronology stay in records. Link to those records instead of reproducing them.

Records use plain Markdown headings, tables, lists, exact file references and evidence links. Keep layout HTML out of agent records. Store a needed diagram in a separate file and link it. Preserve anchors referenced by other documents.

When a page becomes predominantly agent-facing, move that material into records and retain its human-facing core in a page. Removing it from navigation or publication follows the deletion gate. Preserve a hidden stub and former anchors while dated or frozen links still depend on them.

## From open work to subject knowledge

Review a mixed document section by section as work matures:

- Move established behavior, accepted requirements and durable rationale to the owning topic. Label an accepted future specification separately from implemented behavior and runtime evidence.
- Follow the [experiment retention rules](writing/evidence.md#numbers-and-staleness). A closed record supports current knowledge through a link; it does not become a second current knowledge home.
- Keep unfinished implementation, unresolved choices and prospective acceptance in the open owner. Topic research notes may remain with their topic; `OPEN.md` routes there.
- Record the landing in the worklog. Retire a completed source only after accounting for its unique content, references and user-approved deletion.

Assistant proposals remain proposals until explicitly accepted. Migration, silence or continued discussion does not make them accepted requirements.

Plans distinguish investigation readiness from implementation readiness. A workstream's execution owner carries order, prerequisites, status and resume instructions; implementation plans carry prospective acceptance; coverage maps obligations to evidence. Do not distribute this state among competing boards.

## Evidence identity and frozen records

Retain exact original bytes only for a specific citation, source pin or reproduction dependency. Preserve the necessary reference closure, original logical path, source revision, byte count and cryptographic hash in a location manifest. Record a per-document source revision when it differs from the collection default.

Do not rewrite frozen links, add banners to originals or silently replace missing bytes. Current prose links to current knowledge or explicit evidence locations. A manifest indexes identity and location; it is not a second content home.

If a project implements historical link resolution, limit rebasing to explicitly registered origins and records. Current links and missing targets remain strict. A reading view must distinguish exact originals from mutable supporting current files. Do not describe a symlink as a frozen source or write protection.

Restore an original only into an absent destination. Preserve a newer live file separately; do not overwrite unrelated pending work. Source relocation, hash verification and a reading view establish document integrity, not runtime qualification or permission to execute old procedures.

## Shelved investigations

Shelving is a scope decision recorded in the experiment guide and owning topic. Preserve inputs, code, failures and concrete recovery conditions there. Resumption requires a new explicit assignment. A hidden page may remain directly linkable with `hidden = true`; hiding neither deletes evidence nor qualifies a replacement.

## Rules for changes and chronology

- Nothing is deleted without user approval: documents, figures and content lines. Propose removal with the concrete material identified. A requested review or prototype is a gate: present it and stop before adopting, committing or publishing.
- Keep code, owning documentation, tests and worklog in the same logical deliverable commit. Generated output stays ignored. Commit messages and push authorization follow the consuming project's working agreements.
- Keep the worklog append-only and newest-first. Each landing records what changed, why, measured effect with units when applicable, checks and commit identity. A pending entry may say the hash is assigned by its landing commit; resolve it through version history rather than rewriting dated entries.
- Record probes in one line: `probed <subject> → <verdict>, <decisive reason>, <time spent>`. Detailed artifacts follow the [experiment retention rules](writing/evidence.md#numbers-and-staleness).
- Current invariants live in owning records and cross-cutting conventions. Source markers such as `INVARIANT` and `DON'T-REDO` must not leak as internal labels onto rendered pages.
- Measured claims follow [numbers and staleness](writing/evidence.md#numbers-and-staleness).
- A page may keep topic-owned drafts below `<!-- page-end -->`. Only content above is rendered. Chronology still belongs in the worklog; owed work still needs an `OPEN.md` route to its owner. Do not leave unreachable notes tails.
- Remove approved superseded sources in the landing commit. Do not add an archive staging layer. Preserve exact evidence only when its identity has a concrete purpose.

## Review, build and publishing

Use the pinned kit from the consuming project root. Follow the concrete commands in the project's context and the shared [validation guide](site/validation.md). Complete the linked validation before review. Share the rendered page with its figures first, then source or evidence links where useful.

Serve only generated output on loopback for local browser review. Confirm the listener's owner and served checkout before reuse. Do not expose the repository root or stop another session's server. Stop owned temporary servers after review unless retained for the user's preview.

Browser approval remains scoped to the supported origin. If access is rejected on policy grounds, preserve the rejection and resolve the permission with the owner. Do not change transport, browser or control API to bypass the block. A manual file URL is not evidence that an agent inspected the rendering.

Builds on feature branches must not publish production documentation. Publishing requires the consuming project's chosen branch/environment, authorization and successful checks. Hosting source changes are a separate explicit operation; a source build does not imply a deployed version. Rollback must preserve unrelated work and rebuild/verify the chosen revision.

## Agent entrypoints: import versus point

Keep one thin repository router in `AGENTS.md`. Name the project context and
prerequisites there. Read the orientation and rules that apply to every task
at the start of work, unless they are already loaded.

Route the remaining rules by action. For each trigger, name the required files
or sections and say when to read them. Apply every matching route before its
action. Recheck the routes when the task expands. Find task-specific plans,
topics and evidence through named links in the project context or applicable
rule. Reading a route grants no execution or publication permission.

Codex uses the named paths and triggers in `AGENTS.md`. For Claude Code, use a
bare, standalone `@AGENTS.md` import in `CLAUDE.md` so both clients use the same
router. Import paths are relative to the importing file. Keep the import chain
short. Backticks and fences make an import literal.

Submodule consumers must initialize `.docs-kit` before relying on its rules.
If a required policy is missing, report it and resolve the prerequisite before
proceeding with the work it governs.

## README is the bounded exception

A human arriving cold may need the project's purpose, installation and run commands in `README.md`, even when those facts have a canonical home elsewhere. Keep repetition short. Sweep the README in the same deliverable when those facts change; the verified canonical owner wins on conflict.
