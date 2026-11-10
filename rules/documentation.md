# Documentation system

Every fact has exactly one canonical home. Other documents link to it. When copies disagree, verify the owning source, correct the stray copy and update affected summaries in the same deliverable.

This guide owns where a document lives, the order in which documentation is written and how documents change. [Writing records](records.md) owns what a record says. These rules are shared policy. A consuming project's `docs/PROJECT_CONTEXT.md` owns its repository map, commands, named documentation routes and project-specific choices. Do not copy these rules into project entrypoints.

## Canonical homes

| Artifact | Owns |
|---|---|
| `docs/PROJECT_CONTEXT.md` | Project purpose, repository map, run/build instructions and named documentation routes |
| `docs/index.md` | Documentation reading index: routes to development guidance, topics, evidence, sessions and open work |
| `docs/development/`, including conventions when needed | Project-specific engineering choices, commands and current repository invariants |
| `.docs-kit/rules/documentation.md` | Documentation placement, order of work, lifecycle and agent routing |
| `.docs-kit/rules/records.md` | What a record says and how it is written: format, honest claims, measured numbers and frozen evidence |
| `.docs-kit/rules/writing.md` and `writing/` | Index and focused guides for pages written for people: page design, explanations, figures, mathematics and code |
| `.docs-kit/rules/maintenance.md` and `site/` | Index and focused authoring, reader, resources, validation and publication guides, including page review and the publishing gate |
| `.docs-kit/rules/engineering/code.md` | Logging, consumed program output and generated-file practices |
| `.docs-kit/rules/engineering/performance.md` | Routine efficiency, representative workloads and measured performance claims |
| `.docs-kit/rules/engineering/execution.md` | Execution identity, conditional shared-resource budgeting, supervision and cleanup |
| `.docs-kit/rules/engineering/git.md` | Commit scope, messages, validation and safety when sharing a Git checkout |
| `.docs-kit/rules/engineering/delivery.md` | Assignment scope, delivery ownership, parallel work and escalation |
| `.docs-kit/rules/engineering/handoffs.md` | Completion and blocker reports, durable evidence and handoff receipt |
| `.docs-kit/rules/experiments/workflow.md` | Shared experiment kinds (investigation, qualification), scope limits, baselines, evaluation, stopping and required content |
| `.docs-kit/rules/experiments/verification.md` | Claim-scoped check selection, numerical correctness, regression gates and changed-input verification |
| `docs/topics/<topic>/<topic>.md` and further descriptively named records; every topic has one unless its page declares `page_only` | Canonical mechanisms, accepted specifications, methods, scoped results, limits and topic-owned research notes |
| `docs/topics/<topic>/index.md`, when a person asked for a page | Human explanation drawn from the topic records: current conclusions, figures, decisions and blockers |
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

A project may keep topic folders one level deeper, inside a
[topic group folder](site/authoring.md#topic-group-folders); the `docs/topics/<topic>/`
paths above then gain the group folder's name.

These are canonical roles for new projects. Existing projects may keep explicit
local destinations; follow [refactoring over compatibility](engineering/code.md#refactoring-over-compatibility)
before keeping old routes. Create a directory or document only
when content needs it, and link that owner from `docs/index.md`.

Other Markdown must have a defined role: a subject record, log, experiment contract/guide, exact evidence, or unfinished plan/decision. Do not create a generic archive, review collection or second status system to avoid choosing an owner. Names explain the subject or mechanism; avoid vague `Info` or `Manager` labels.

## Record first, page on request

In these rules a page means a page for people, a topic's `index.md`. A [registered source page](site/authoring.md#registered-source-pages) is a record shown whole; editing it is editing a record.

Document work in this order:

1. The agent that did the work writes or updates the record, following [writing records](records.md). It holds the facts: what changed, what was measured and why.
2. A new page is made only when a person asked for it.
3. A page that exists stays true to its record. When a record changes, update the pages that explain it in the same deliverable, after the record; that needs no new request, also when the page gains or loses a chapter because the record did. [Rendered pages are for people](#rendered-pages-are-for-people-records-stay-markdown) says how lint lists those pages.
4. The size of the page work decides who does it. A small sync changes a sentence or two that a record edit made stale; it needs no page guides and stays with the agent that edited the record. Anything larger, or anything that needs layout, a figure or a new block, goes to a separate agent where the runtime supports delegation; follow [delegating a page for people](engineering/delivery.md#delegating-a-page-for-people) for its brief. Without delegation, do the page as a separate step after the record.

The page author reads the applicable [page guides](writing.md) and [site guides](maintenance.md). The record author needs them only for what [excerpts, formulas and figures](records.md#excerpts-formulas-and-figures) names.

## Rendered pages are for people; records stay Markdown

Every topic has a record; [writing records](records.md#one-record-per-topic) says
how it is named and written. Add `index.md` when a person asked for a page; the page explains the record in
its own words and links its sections.

A page and its record cover the same subject for different readers, so their
overlap is expected, not duplication to remove. The record holds the exact
wording an agent is routed to and must find again. The page leads with the
conclusion, shows a figure and orders the explanation for a person. The record
is authoritative: a page never adds a rule, number or limit its record lacks.

A topic without a record is an exception. Which cases need it is not settled
yet; the kit's own pages that explain its guides, whose records live in
`rules/`, are one known case. Declare it in the page's frontmatter as
`page_only = "<reason>"`. Lint warns about a topic page with neither a record
nor that declaration. Once the page
gains a rule, specification or limit, that part moves into a record.

When a record section changes, `docsite.py lint` prints a note listing the pages
that link to that section; a link to the whole record is listed only when its
opening text changes, so a chapter links the section it explains. Reread each
listed page and update its explanation in the same deliverable, after the
record. `--since <rev>` compares with an older commit; notes never fail lint.

`page_number_notes = true` is one setting for the whole site. With it, lint also
lists the numbers in a page's prose that none of its linked records state. State such a number in its
record, show it as code when it is a literal value, or take it off the page.
The check reads prose only and does not judge whether the record's number is
right; [numbers and staleness](records.md#numbers-and-staleness) owns that.
These notes never fail lint either. Turn the setting on for a site whose pages
explain Markdown records. Leave it off for a site with pages that report
measurements from experiment data: those numbers are rounded or derived, match
no text, and need the project's own ledger check.

A rendered page explains current conclusions, accepted specifications, demonstrated behavior with its evidence scope, useful figures and the decisions needed next. Contracts, handoff/resume state, readiness boards, bookkeeping and long run chronology stay in records. Link to those records instead of reproducing them.

A site may also render a whole record as a [registered source page](site/authoring.md#registered-source-pages). The Markdown file stays the record and its only editable copy; the page adds no content of its own.

When a page becomes predominantly agent-facing, move that material into records and retain its human-facing core in a page. Removing it from navigation or publication follows the deletion gate. Preserve a hidden stub and former anchors while dated or frozen links still depend on them.

## From open work to subject knowledge

Review a mixed document section by section as work matures:

- Move established behavior, accepted requirements and durable rationale to the owning topic. Label an accepted future specification separately from implemented behavior and runtime evidence.
- Follow the [experiment retention rules](records.md#numbers-and-staleness). A closed record supports current knowledge through a link; it does not become a second current knowledge home.
- Keep unfinished implementation, unresolved choices and prospective acceptance in the open owner. Topic research notes may remain with their topic; `OPEN.md` routes there.
- Record the landing in the worklog. Retire a completed source only after accounting for its unique content, references and user-approved deletion.

Assistant proposals remain proposals until explicitly accepted. Migration, silence or continued discussion does not make them accepted requirements.

Plans distinguish investigation readiness from implementation readiness. A workstream's execution owner carries order, prerequisites, status and resume instructions; implementation plans carry prospective acceptance; coverage maps obligations to evidence. Do not distribute this state among competing boards.

`OPEN.md` holds one-line routes, and every bullet links its owning document. A finished line is deleted; it is not struck through, ticked or marked done. Lint checks both.

## Rules for changes and chronology

- Nothing is deleted without user approval: documents, figures and content lines. Propose removal with the concrete material identified. A requested review or prototype is a gate: present it and stop before adopting, committing or publishing.
- Keep code, owning documentation, tests and worklog in the same logical deliverable commit. Generated output stays ignored. Commit messages and push authorization follow the consuming project's working agreements.
- Keep the worklog append-only and newest-first. Each landing records what changed, why, measured effect with units when applicable, checks and commit identity. A pending entry may say the hash is assigned by its landing commit; resolve it through version history rather than rewriting dated entries.
- A worklog entry and its commit message cover the same landing. That overlap is deliberate, like the [README exception](#readme-is-the-bounded-exception). The worklog is one file that reads without Git, survives squashed or rebased history, and holds what no commit carries: probes, and decisions or events that belong to no single commit. Write the entry and the commit message in the same step so they agree. Reconsider this only when a worklog becomes slow to lint or awkward to search.
- Record probes in one line: `probed <subject> → <verdict>, <decisive reason>, <time spent>`. Detailed artifacts follow the [experiment retention rules](records.md#numbers-and-staleness).
- Current invariants live in owning records and cross-cutting conventions. Source markers such as `INVARIANT` and `DON'T-REDO` must not leak as internal labels onto rendered pages.
- Measured claims follow [numbers and staleness](records.md#numbers-and-staleness).
- A page may keep topic-owned drafts below `<!-- page-end -->`. Only content above is rendered. Chronology still belongs in the worklog; owed work still needs an `OPEN.md` route to its owner. Do not leave unreachable notes tails.
- Remove approved superseded sources in the landing commit. Do not add an archive staging layer. Preserve exact evidence only when its identity has a concrete purpose.

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
