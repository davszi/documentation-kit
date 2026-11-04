# Worklog

Chronology is append-only, newest first. Shared policy stays in `rules/`.

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
