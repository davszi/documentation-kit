# ADP debt timeline: events

Ref `main` at `b8b80e0b` (2026-11-15). Paths are from the repository root.
Every number is recomputable with the scripts in this folder (see
`method.md`); `summary.txt` holds the derived totals. Labels:
**measured** (from Git), **account** (what the developer said; context, not
measurement), **reading** (my interpretation).

## Phases (measured)

| Phase | Dates | First-parent commits | What the series do |
|---|---|---|---|
| Product rewrite | 2026-07-02 – 07-26 | 395 (07-01 – 07-31) | `product` code 25,453 → 39,739 lines; supporting code ≈ 0 (only 832 lines of doc tooling) |
| Quiet | 07-27 – 09-23 | 10 | flat |
| Build-up | 09-24 – 11-09 | 499 on 35 days | supporting code 836 → 269,241 lines (peak 11-10); `docs/open/` up to 15,785 lines; run output in `experiments/` 11 → 70,902 files, 0 → 5.83 GB |
| Cleanup | 11-10 – 11-15 | 125 on 6 days | 34 net-removal commits delete 145,353 text lines and 221 files; attended code 25,330 → 4,588 lines |

The cleanup by net removal begins **2026-11-10** (`460bd326`, "Retire the
eleven topic pages that held no content"). Documentation consolidation began
earlier, on **2026-11-04** (`79edb62e` adopts the shared documentation kit,
`7bda98a7` moves coordination rules), while attended and pool code was still
being added (11-04/11-05). From 11-04 to 11-15 there are 40 net-removal
commits.

## Series: start, peak, now (measured, `timeline.csv`)

| Series | 2026-10-01 | Peak (date) | 2026-11-15 |
|---|---|---|---|
| attended code, lines | 0 | 25,330 (11-13) | 4,588 (all in `tools/run_journal_candidates/`: parked `sealed_judge.py`, `observe.py`, `closure.py` and tests) |
| doc tooling code | 836 | 2,492 (11-01) | 0 |
| evidence-store tooling | 0 | 1,219 (11-09) | 163 |
| resource slot + native pool | 0 | 8,151 (11-05) | 8,063 |
| per-experiment harnesses | 0 | 132,652 (11-05) | 132,638 |
| other qualification code | 7,140 | 101,630 (11-15) | 101,630 |
| supporting total (groups 1–6) | 7,976 | 269,241 (11-10) | 247,082 |
| product (`adp_ext`, `ada_ext`), contrast | 40,254 | 90,602 (11-05) | 90,261 |
| `docs/open/` lines | 7,130 | 15,785 (10-16) | 5,202 |
| `docs/open/` files | 32 | 76 (10-11) | 21 |
| `docs/worklog.md` lines | 2,719 | 10,835 (11-15) | 10,835 |
| `docs/**/evidence/` files / lines | 0 / 0 | 419 / 229,055 (11-09) | 405 / 128,526 |
| frozen document copies (`evidence/documents/`) files / lines | 0 | 42 / 6,225 (11-09) | 0 |
| documents listed in `locations.json` files | 0 | 53 (10-18) | 0 |
| `experiments/` tracked files | 2,276 | 83,494 (11-12) | 83,428 |
| `experiments/` tracked bytes | 455 MB | 6.26 GB (11-12) | 6.25 GB |
| of which `.npz` / `.json` / `.gz` / `.jsonl` / `.py` / other, bytes now | | | 2.73 GB / 1.49 GB / 0.74 GB / 0.58 GB / 0.42 GB / 0.28 GB |

`locations_documents` counts one entry per frozen copy in the two manifests
`docs/evidence/locations.json` (later `docs/project/evidence-locations.json`)
and `experiments/platform_qualification/sdk_reuse/evidence/locations.json`:
51 on 10-17, 53 from 10-18 until both were deleted on 11-11 (`1a541cf2`,
"Delete the 53 frozen document copies"). All 53 entries have distinct
original paths.

**Text written for the developer** (measured, `+` lines/words of first-parent
diffs): build-up 09-24 – 11-09: plans and proposals in `docs/open/**`
22,848 lines / 268,837 words; worklog 9,170 / 83,278; session notes 217 /
2,218. Total 354,333 words in 47 days (35 days with commits). The largest day
was 2026-10-08: 50,588 words added to `docs/open/**`. In the cleanup days:
40,447 words. On 2026-10-16 the single file `docs/open/platform-refactor/README.md`
was 185,782 bytes and `docs/open/vehicle-and-training-design-review.md`
103,809 bytes.

## When each subsystem first appeared (measured; "asked for by" cites Git)

- **Plan drafts and the worklog.** `docs/worklog.md` from 2026-07-16
  (`a6c65780`, "adopt the doc-system spec"); `docs/open/` from 07-20
  (`fd1e9c4a`). Plan drafting took off 09-24/25 (35,886 words added on 09-25;
  `687aded0` "Combine accepted runtime and platform design histories").
- **Documentation tooling.** `docs/tools/` from 2026-07-20 (`fd1e9c4a`);
  moved to `tools/docs/` on 10-17 (`8a691041`); grew to 11 files / 2,492 lines;
  most of it replaced by the shared kit 11-04 (`79edb62e`); last 7 files
  removed 11-11 (`c026884d`, `e21c2e84`, `1a541cf2`). Asked for by: the doc
  system spec in `docs/writing-docs.md` (07-16/19).
- **Qualification code.** `experiments/platform_qualification/` from
  2026-09-27 (`11b6c494`, "Build offline GT3 qualification tools"), after
  `experiments/platform_qualification/tooling-contract.md` records "the user
  authorized the proposed" tooling (`b2f93b83`, line 132).
- **Run output committed to Git.** `experiments/` jumped from 2,339 files (10-03) to 54,136
  files (10-05) (`15d3e02a` adds 22,378 files / 1.59 GB; `c9c60f81`
  0.80 GB; `696f13bc` 0.39 GB). `a93ab550` on 10-08 adds 0.87 GB and Git LFS
  for SDK traces; `docs/worklog.md` that day: "User requested all preserved
  work be committed". During the cleanup, `0c1c2b99` (11-12) adds another
  11,389 files / 325 MB ("Store the output of the remaining named runs in
  Git"); the developer agreed, quoted in the commit: "Yes, store it".
- **Per-experiment harnesses.** First `*_supervision.py` and `sdk_reuse/` on
  2026-10-08 (`a93ab550`, 21,703 Python lines in one landing). `sdk_integration/`
  from 10-18 (`64a3b3d8`). Harness lines: 9,201 (10-08) → 72,804 (10-13) →
  132,652 (11-05). Asked for by: per-question native protocols in the
  platform-refactor plans (`docs/open/platform-refactor/01-model-and-execution-qualification.md`,
  `execution-plan.md` from 10-17 `0c29312a`).
- **Frozen document copies.** 2026-10-17 (`9a90cde0`, `00eacb82` "Move
  historical SDK documents into experiment evidence"); plan drafts moved from
  `docs/open/platform-refactor/drafts/` into
  `experiments/platform_qualification/evidence/documents/` and
  `.../sdk_reuse/evidence/documents/`, with `locations.json` manifests.
  `open_lines` fell 15,785 → 2,704 the same day (a move, not a deletion).
- **Central evidence store.** `docs/evidence/` from 10-17 (`4f52e2b6`);
  `docs/evidence/artifacts.json` (4,094 lines), `retention.json` (15,018 lines)
  and `tools/evidence.py` added 11-09 (`ff6ede7e`, "Retain compact evidence
  and complete proof records", 223 MB including media).
- **Attended evidence.** Recorder `sdk_app_demo_probe.py` from 2026-10-28
  (`396fcb1b`, "Prepare reviewed manual SDK app qualification"; 3,780 lines
  that day). Plan 11 `docs/open/platform-refactor/11-attended-evidence-parts.md`
  adopted 11-02 (`1afda78b`, 273 lines; 335 lines and 13 revisions by 11-14).
  `attended_parts/` and `sealed_judge.py` landed 11-04 (`9d164580`,
  15,592 insertions in 50 files). Attended code 8,609 → 23,624 lines that day.
- **Resource slot and native pool.** `native_supervision.py` from 10-18
  (`14bbaf1f`); `native_resource_pool.py`, `native_scope.py`,
  `native_resource_keeper.py`, `tools/coordination/resource_slot.py`,
  `legacy_cpu_slot.py`, `resource_usage.py` all on 11-05 (`9c8642a6`,
  9,955 insertions in 52 files; then `fe565384` "Make execution budgets
  explicit and reusable", 7,539 insertions). Pool 751 → 8,151 lines that day.
  Asked for by: the coordination note `docs/project/sessions/2026-11-04-platform-coordination.md`
  line 35 and `docs/topics/isaac-sim-runtime-qualification/isaac-sim-runtime-qualification.md`
  line 72: "The human requested two simulator runs in parallel."

## Recorded approvals (measured, `approvals.csv`)

337 first-occurrence approval statements in Markdown (436 matched lines with
repeats), July – 11-15:

| Period | Statements | by destination | Commit messages with an approval |
|---|---|---|---|
| 07-01 – 09-23 | 9 | | 2 of 405 commits |
| build-up 09-24 – 11-09 | 181 | plans 57, topic/experiment records 58, worklog 47, guides 18, sessions 1 | **3 of 499** commits |
| cleanup 11-10 – 11-15 | 147 | worklog 74, plans 40, records 32, guides 1 | **80 of 125** commits |

148 statements name the developer; 189 say "the user", "user-approved",
"owner" or "human". Examples (short quotes, first-occurrence rows):

- 2026-09-27 `11b6c494` `docs/open/platform-refactor/drafts/01-qualification.md:284`: "user-approved candidate order/budgets"
- 2026-10-08 `a93ab550` `docs/worklog.md:25`: "User requested all preserved work be committed"
- 2026-10-29 `b846a167` `docs/worklog.md:24`: "Implement the developer's approved attended responsiveness policy"
- 2026-11-02 `1afda78b` `docs/open/platform-refactor/11-attended-evidence-parts.md:3`: "adopted 2026-11-02 (the developer: \"lets build it now fully\")"
- 2026-11-05 `9c8642a6` `docs/project/sessions/2026-11-04-platform-coordination.md:35`: "The human requested updated budgets and isolation"
- 2026-11-11 `a18d94e5` commit message: deleting the central store approved with "ok"
- 2026-11-15 `3197ab3e` commit message: "Judge+capture+closure", "Yes, delete", "Retire all"
- 2026-11-15 `1797bc4b` commit message: "Right after phase 1"

**Built with no recorded approval** (method: no keyword-matching approval
statement in the 7 days before or on the first day; see `method.md`):

- Recorder `sdk_app_demo_probe.py` (10-28): none.
- Resource slot, native pool, keeper, `legacy_cpu_slot.py` (11-05): the record
  says the developer requested *two parallel simulator runs*; no statement
  approves the pool, keeper, slot or ledger design. The one approval nearby
  ("the user said \"yes lets use an…\"", `plan05_lifecycle_preparation_20261104-policy-v2.md:164`)
  is about a single run's memory budget.
- Per-experiment harnesses and `sdk_reuse/` (10-08): only "authorized
  committing and pushing all preserved work" (`docs/open/platform-refactor/README.md:1180`),
  which approves committing, not the harness pattern.
- Run output in Git (10-04/05, 1.6 GB+): no statement before; the 10-08
  worklog line comes after.
- Frozen document copies and `locations.json` (10-17): none.
- Central evidence store (11-09): none.
- Attended parts (11-04): approved in Plan 11 on 11-02 ("lets build it now
  fully").

## Cleanups (measured, `cleanups.csv`)

| Date | Commit | Removed | Text lines −/+ | Files −/+ |
|---|---|---|---|---|
| 2026-07-05 | `7f3f0f7f` | legacy PyQt desktop app (product era, not debt) | 5,832 / 303 | 52 / 0 |
| 2026-07-25 | `cc7e98e3` | SAC/TD3 RL machinery (product era) | 1,497 / 74 | 20 / 0 |
| 2026-10-17 | `95586ac7`, `ab1e3c9f` | open docs consolidated; generated site sources (−425,657 lines, 15.8 MB) | | |
| 2026-11-04 | `79edb62e` | own doc tooling replaced by the shared kit | 5,655 / 2,652 | 87 / 28 |
| 2026-11-10 | `460bd326` | 11 empty topic pages (**start of net-removal run**) | 417 / 80 | 11 / 0 |
| 2026-11-11 | `1a541cf2` | 53 frozen document copies + both `locations.json` | 14,166 / 337 | 60 / 0 |
| 2026-11-11 | `a18d94e5` | central evidence store, `tools/evidence.py`, its test | 92,813 / 151 | 6 / 1 |
| 2026-11-11 | `c026884d`, `e21c2e84`, `e41ab54e`, `d3316426`, `c81954f2` | doc command delegates, reader page check, file-identity checks | 2,335 / 177 | 12 / 0 |
| 2026-11-12 | `db0c85b2`, `ac773782` | finished topic-records plan; finished parts of five open records | 733 / 117 | 1 / 0 |
| 2026-11-12 | `98790e76`, `70fff715` | 56 unused PNG copies; figure manifests | 1,428 / 77 | 56 / 0 |
| 2026-11-14 | `de095a4c` | kit 4.0.0 upgrade (theme renames; not a net removal) | 131 / 252 | |
| 2026-11-14 | `42c38a90` | compatibility-layers record and two leftovers | 75 / 23 | 1 / 0 |
| 2026-11-14 | `6a876ed2` | 2026-11-04 coordination note | 179 / 22 | 1 / 0 |
| 2026-11-15 | `b72475d9` | CPU resource slot replaced by a small one | 1,084 / 1,254 (−1,041 pool lines) | 2 / 0 |
| 2026-11-15 | `3197ab3e` | attended evidence retired; 3 pieces parked | 18,459 / 4,732* | 38 / 1 |
| 2026-11-15 | `1797bc4b` | attended recorder and attended branch of native supervision | 8,814 / 182 | 10 / 1 |
| 2026-11-15 | `76e80224` | `attended_responsiveness` selector | 25 / 21 | 0 / 0 |

\* counted without rename detection; the commit's own `-M` stat is 13,903
deletions / 176 insertions.

Totals of net-removal commits: from 11-10, 34 commits, 145,353 lines deleted
and 7,524 added, 221 files and 22.6 MB deleted; from 11-04, 40 commits,
243,416 / 102,371 lines, 309 files. Deleted lines by group from 11-10:
attended 25,340 (incl. moved lines), pool 1,135, doc tooling 1,241, evidence
tooling 1,178, `docs/open/` 1,584, `docs/**/evidence/` 100,829.

Not cleaned by 11-15 (measured): harnesses 132,638 lines, pool 8,063,
run output 6.25 GB / 83,428 files in `experiments/`, worklog 10,835 lines.

## Turning points (account, not measurement)

- The developer said he could not read all the agents' proposals because it
  was too much for one person.
- Asked whether he approved plans he could not read in full, he answered:
  "i most probably said yes without seeing or understanding it all".
- He spent about two weeks cleaning up (account). The measured net-removal run
  covers 11-10 – 11-15; documentation consolidation started 11-04.

## Interpretation (reading, optional)

- Growth was not gradual. Supporting code went from 7,976 lines (10-01) to
  269,241 (11-10), about 3× the product code, mostly in a few bulk landings
  (10-08, 10-12, 11-04, 11-05). Run output in Git went from 455 MB to 6.26 GB.
- Text for the developer to read peaked at the same time: ~354,000 words of
  plans, worklog and notes in 47 days. That volume matches the account that
  proposals could not all be read.
- During the build-up, approvals appear inside records written by agents
  (181 statements, many as "user-approved" labels), but only 3 of 499 commit
  messages cite one, and several subsystems (recorder, pool/slot design,
  harness pattern, frozen copies, evidence store, run output in Git) have no
  recorded approval of their design. During the cleanup, 80 of 125 commit
  messages quote the developer's decision. The way approvals were recorded
  changed with the cleanup.
- The cleanup removed the attended system, the frozen copies, the evidence
  store and the doc tooling. Harnesses, the native pool and committed run
  output remain the largest unreduced items.
