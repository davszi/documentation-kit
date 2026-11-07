# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

## 2026-11-07 — Final local kit suite after QA-provenance changes

- Rerun the complete `tests/run_checks.sh` on the QA-provenance hook and its
  regression tests with Python 3.12.3 and Node 22.22.3. Starter build is current;
  strict lint has zero warnings; all 54 Python tests pass in 2.961 s. Reader
  preservation and both Node math/source-link checks pass.
- Attempt 04 retains its exact command, changed-source hashes, environment and
  diff under the consuming ADP checkout's ignored
  `.build/coordination/docs-final-20261107/kit-local/attempt-04/`. The 4 GiB
  zero-swap scope uses a 180 s worker deadline, 10 s cleanup reserve and 220 s
  outside deadline. Terminal owned peak is 72,253,440 bytes; elapsed time is
  5.742 s; owned-process absence is verified. Earlier attempts remain retained.
- No intentional rendered layout changed, and browser pixel inspection was not
  run. This validates the recorded local source, not deployment or later origin
  integration. The landing commit supplies its identity.

## 2026-11-07 — Local restructure regression validation

- Run the complete `tests/run_checks.sh` suite with Python 3.12.3 and Node
  22.22.3. Starter build is current; strict lint has zero warnings; all 52 Python
  tests pass in 2.999 s. Reader preservation, vendored math integration and
  source-file links pass, including text/code/media/anchor/figure identities.
- Fix the existing alternate-worklog fixture to update both project context and
  the new reading index after explicitly moving its worklog. Keep strict
  dead-link detection and the original acceptance requirement unchanged.
- Preserve the first attempt's systemd setup failure (suite not started) and
  the second attempt's stale fixture-link failure. The third attempt passes
  under a 4 GiB zero-swap scope, 180 s worker deadline and 10 s cleanup reserve;
  its outside deadline is 220 s. Terminal owned peak is 68,677,632 bytes, elapsed
  time is 5.703 s, and owned-process absence is verified.
- Exact commands, source/environment identities, diffs, failed attempts and
  receipts remain in the consuming ADP checkout's ignored
  `.build/coordination/docs-final-20261107/kit-local/`. No intentional rendered
  layout changed; browser pixel inspection was not run. This is a local suite
  result, not a hosted deployment check. The landing commit assigns identity.

## 2026-11-07 — Focused engineering and documentation guides

- Add portable [code practices](../rules/engineering/code.md),
  [efficiency rules](../rules/engineering/performance.md) and
  [execution/resource guidance](../rules/engineering/execution.md). Keep
  project-specific tools, workloads, profiles and acceptance requirements local.
- Move the existing writing and site contracts into focused `rules/writing/`
  and `rules/site/` guides. Keep the original entrypoints and section anchors as
  short routers; preserve their clauses and rebase moved relative links.
- Move kit and starter orientation to `docs/PROJECT_CONTEXT.md`, add
  `docs/index.md` reading indexes, update canonical destinations and action
  routes, and keep both worklogs at `docs/worklog.md`. Claude entrypoints import
  only `AGENTS.md`. README now routes engineering, writing and site work.
- Consolidate repeated execution, performance, evidence, figure-provenance,
  review and local-media rules into their owning guides, with links from
  callers. Preserve unique context and the figure output-hash requirement.
- Focused checks passed on 31 changed kit and 38 ADP Markdown files with no
  errors or warnings. Old anchors, moved manifest bytes and the ADP worklog
  were preserved. The earlier 17 path-compatibility tests passed in 0.545 s.
  Independent source review found no consequential requirement lost in the
  overlap consolidation. Full site and rendered checks remain deferred.
  Changes are uncommitted; the landing commit will assign their identity.

## 2026-11-07 — Shared delivery and handoff policy

- Add the [approved delivery guide](../rules/engineering/delivery.md) for
  assignment scope, owner responsibility, coordination, parallel work and
  escalation, and the [handoff guide](../rules/engineering/handoffs.md) for
  completion, blockers, durable evidence and receiving work. Add action routes
  for kit contributors and starter projects.
  Validation is deferred to the agreed documentation batch.

## 2026-11-07 — Shared Git practices

- Add the [Git guide](../rules/engineering/git.md) for coherent commits,
  applicable validation, preservation of unrelated changes and staging safety.
  Require an explanatory body after the short imperative subject. Preserve
  repository-owned commands, acceptance gates and publication permissions.
- Route kit contributors and new starter projects to the guide before Git
  actions. Starter build and strict lint, 52 Python tests, both Node 22 checks,
  focused policy links and both client routes passed. Correct the route-check
  harness's initial assumption that the starter Claude file had no heading.
  Independent Sol High review is clear after fixing Claude's route and
  clarifying preservation of staged intent during isolated-index landing.
  This landing supplies the commit identity.

## 2026-11-06 — Task-triggered agent reading

- Define one [repository router](../rules/documentation.md#agent-entrypoints-import-versus-point)
  for orientation, prerequisites and action-specific reads. Update the starter
  so Codex and Claude use the same task routes and apply every matching rule
  before its action.
- Starter build, strict lint, 52 Python tests and both Node 22 checks passed.
  A fresh initializer smoke check verified the generated router, its three
  shared policy paths and Claude's single import. This landing supplies the
  commit identity.

## 2026-11-06 — Visual ordering and evidence presentation

- Clarify the [page lead](../rules/writing.md#page-design),
  [scope notes](../rules/writing.md#story-and-reading-layers) and
  [choice of representation](../rules/writing.md#figures-and-comparisons).
  Put the figure early in mechanism and geometry explanations. Keep brief
  qualifications beside the relevant evidence and the full rationale in its
  record. Use diagrams for relationships and tables for precise comparisons.
- The starter build, strict lint, 52 Python tests and both Node 22 checks
  passed. Checked the final policy text for preserved headings, its new
  internal link and whitespace. This landing supplies the commit identity.

## 2026-11-04 — Shared publication and browser checks

- Extract the optional existing-site exporter and common browser checks from
  adaptation. Projects retain publication admission, stable URLs, historical
  packaging, credentials and scientific assertions. The
  [maintenance contracts](../rules/maintenance.md#exporting-into-an-existing-publication)
  own both APIs. Homepage composition stays project-owned; the starter is an
  optional example, as recorded in the [writing rules](../rules/writing.md#project-owned-homepages).
- Preserve embedded JavaScript/JSON and unrelated HTML bytes. Align source-span
  offsets with HTMLParser's LF counting and cover literal Unicode/control
  separators plus mixed mapped/unmapped routes. Browser checks retain real
  clipping/visibility rules and report impossible short-reader cases as skipped.
- Strict starter lint has zero warnings; all 52 Python checks, JavaScript checks,
  real browser failure fixtures and desktop/phone reader checks pass. Independent
  source review findings are resolved. [Receipts](../verification/publication-browser.json)
  retain tested inputs and bounded resources under the shared lock. Consumer
  adoption and public-bundle comparison remain project-owned. This landing
  supplies the commit identity.

## 2026-11-04 — Generated-content compatibility

- Support a tracked project `content_transform` for importing scientific or
  sealed reader content into the shared presentation. Revalidate derived
  metadata; preserve source-declared slugs and page CSS. Allow validated scoped
  `body_class` values and existing canonical worklog paths. The
  [maintenance contract](../rules/maintenance.md) owns these extension points.
- Strict starter build/lint, all 31 Python checks, math/source-link JavaScript
  checks and desktop/phone reader browser checks pass. [Receipts](../verification/content-imports.json)
  record tested inputs and resources under the shared lock in an owned
  4 GiB/zero-swap scope. Consumer scientific-preservation checks remain
  project-owned. This landing supplies the commit identity.

## 2026-11-04 — Shared reader includes

- Resolve matching shared-template includes from the kit before looking for
  project fragments. Existing `components/chapter-reader.html` markers keep
  their behavior without a duplicate consumer toolbar file. Relative/contained
  include paths remain required.
- Strict build/lint, all 27 Python checks, JavaScript math/source-link checks
  and desktop/phone reader browser checks pass under the shared lock and an
  owned 4 GiB/zero-swap scope. [Receipts](../verification/shared-includes.json)
  retain tested inputs and output. This landing supplies the commit identity.

## 2026-11-04 — Consumer compatibility adapters

- Add explicit tracked/contained project path and evidence adapters, keeping
  consumer historical identities and schema policy out of the shared engine.
  Declare project-only dynamic dependencies through `extra_assets`; reject
  shared-asset collisions and noncanonical/escaping target paths. The
  [maintenance contract](../rules/maintenance.md) owns configuration and API.
- Strict starter build/lint, all 26 Python checks, math/source-link JavaScript
  checks and existing desktop/phone reader browser checks pass. [Receipts](../verification/project-extensions.json)
  retain inputs, output and the owned 4 GiB/zero-swap scope under the shared
  lock. No application runtime was launched. This landing supplies the commit
  identity; consumer adoption and its content validation remain project-owned.

## 2026-11-04 — Shared local comparison controls

- Extract the reusable width-lesson interaction as `panel-switcher`, with neutral
  authoring attributes and shared control CSS. Track scenarios, figures, legends
  and specialized layouts stay project-owned; ADP's original compatibility copy
  remains until its kit adoption. The [component contract](topics/panel-switcher/panel-switcher.md)
  owns usage and behavior; [origin identities](../verification/panel-switcher-origin.json)
  preserve the exact producing source. After attribute renaming, executable
  behavior matches the original source.
- Verify original/shared defaults, independent groups, buttons/keyboard, deep
  links, print restoration and fallback reading at desktop/phone widths. Strict
  build/lint reports zero warnings, all 22 Python tests pass, both JavaScript
  checks and the existing reader browser regression pass. [Receipts](../verification/panel-switcher-checks.json)
  retain the complete run and screenshots. Checks held the shared lock in an
  owned 4 GiB/zero-swap scope; no simulator was launched. The first invocation
  timed out, its owned scope was stopped, and the corrected browser harness
  passed in a complete rerun. This entry's landing commit supplies its identity.

## 2026-11-04

- Extract the reusable documentation kit from inspected source `9930b919`:
  portable policies, shared chapter/home layouts, generic toolchain and a neutral
  starter. The user selected a pinned dependency suitable for a Git submodule.
  [Extraction evidence](topics/extraction/extraction.md) records source hashes,
  independent review and the passing build/lint, 21 Python tests, JavaScript
  checks and desktop/phone browser review. No simulator or source-project
  migration was performed. This initial commit owns the coherent deliverable.
