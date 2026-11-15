# Method: ADP debt timeline

All numbers come from Git commit objects of the ADP repository, read with
`git --no-optional-locks log / ls-tree / cat-file / diff-tree`. No working
tree, index or remote was read; nothing was written in the repository.

- **Ref measured:** `main` at `b8b80e0b025051d81eaf60d906655049bbe4f12b`
  (pinned at the start of the measurement; `main` still pointed there at the
  end).
- **History:** first-parent chain of that ref. A merge counts as one commit on
  the day it landed; work done on a side branch shows up on the merge day.
- **Day:** the committer date's calendar day, in the committer's time zone
  (`%cI`). The snapshot for a day is the last first-parent commit of that day.
  A day without commits carries the previous snapshot forward
  (`snapshot_is_from_that_day = 0`).
- **Period:** 2026-07-01 to 2026-11-15 (138 rows). The data put the start of
  growth at 2026-09-24/27 (first `experiments/platform_qualification/` code,
  first big plan drafts). July is kept as a baseline: it holds the product
  rewrite (PyQt retirement, racing stack), which is not part of the debt.

## Reproduce

```sh
cd <this folder>
R=<ADP checkout>; C=b8b80e0b025051d81eaf60d906655049bbe4f12b
nice /usr/bin/python3 -I measure.py   --repo $R --ref $C --start 2026-07-01 --end 2026-11-15   # a few minutes
nice /usr/bin/python3 -I approvals.py --repo $R --ref $C --name <developer handle>
nice /usr/bin/python3 -I cleanups.py  --repo $R --ref $C --since 2026-10-01 --extra 7f3f0f7f,cc7e98e3 --name <developer handle>
/usr/bin/python3 -I summarize.py > summary.txt
nice /usr/bin/python3 -I inspect_groups.py --repo $R --commit <sha>   # largest files per group
```

`--name` takes the developer's handle so the scripts do not store it; every
written quote and subject replaces it with "the developer" and home paths
with `/home/<user>`. Stdlib only.

## Files

| File | Content |
|---|---|
| `timeline.csv` | one row per day, one column per series (below) |
| `approvals.csv` | every added Markdown line stating an approval/choice by the developer (or "user/owner/human") |
| `approvals_commit_messages.csv` | the same pattern in first-parent commit messages |
| `cleanups.csv` | per first-parent commit since 2026-10-01 (plus `7f3f0f7f`, `cc7e98e3`): files/lines/bytes added and deleted, deleted lines per group |
| `summary.txt` | output of `summarize.py`: peaks, period totals, approval counts, cleanup totals |
| `events.md` | dated events with commits and paths |

## Line counting

`git ls-tree -r -l -z <snapshot>` lists every blob; gitlinks (`.docs-kit`,
`third_party/IsaacLab`) are skipped, and anything under `.docs-kit/` or
`third_party/` is excluded. Line counts read the blob with one
`git cat-file --batch` process and cache by blob SHA. Lines = number of `\n`,
plus one if the last line has none. A blob with a NUL byte in its first
8000 bytes is binary and counts 0 lines.

## Supporting-code groups (`code_*`, `files_*` columns)

Only `.py` files count as code. A `.py` file is **not** code when its path
contains `/data/`, `/runs/`, `/evidence/`, `/source_snapshot/`,
`/__pycache__/`, `/pytest-tmp/` or a dated folder `/YYYY-MM-DD/` (run output,
frozen source copies, dated one-off scripts). First matching group wins.
`SI` = `experiments/platform_qualification/sdk_integration/`.

1. **attended** (attended evidence)
   - `SI/attended_parts/`
   - `tools/run_journal_candidates/` (exists only from 2026-11-15)
   - the files matching

     ```text
     SI/(test_)?(sealed_judge|sdk_attended_app_supervision|sdk_app_demo_probe|sdk_unattended_app_demo_probe|sdk_app_visual_probe|sdk_app_close_boundary|sdk_app_native_subscriptions).py
     ```

     (the last two exist only as `test_*`; they test the recorder and were
     deleted with it in `1797bc4b`)
2. **doctools** (documentation tooling): `docs/tools/` and `tools/docs/`
   (the folder moved on 2026-10-17, `8a691041`; includes `site_paths.py`,
   `evidence_documents.py` and their tests).
3. **evidencetools** (central evidence store tooling):
   `tools/evidence.py`, `tools/check_evidence.py`,
   `tools/check_experiment_data.py`, `tools/tests/test_evidence.py`.
4. **pool** (resource slot and native pool):
   - `tools/coordination/` (`resource_slot.py`, `resource_usage.py`, `legacy_cpu_slot.py`)
   - the files matching

     ```text
     SI/(test_)?(native_resource_*|native_scope|native_pool_*|native_prebirth|native_supervision|meter_review_selection|legacy_cpu_slot|resource_slot*|resource_usage|current_legacy_meter_admission|parallel_native_*).py
     ```

     — the keeper is `SI/native_resource_keeper.py`.
5. **harness** (per-experiment harnesses): any other `.py` under
   `experiments/platform_qualification/` whose name, after dropping a `test_`
   prefix, ends in `_supervision`, `_supervisor`, `_run`, `_review`,
   `_protocol`, `_authority`, `_closeout`, `_collection`, `_preparation`,
   `_configuration`, `_check`, `_budget`, `_ledger`, `_guard`, `_admission`
   or `_scope` (or is exactly one of those words, e.g. `sdk_reuse/supervision.py`).
   Reason for the group: every qualified question got its own
   probe + `_run` + `_supervision` + `_review` (+ `_protocol`, `_authority`
   in `sdk_reuse`) quartet with tests; they grew in lockstep with the pool
   and attended code and none were retired.
6. **pq_other**: remaining `.py` under `experiments/platform_qualification/`
   (probes, plots, preview app, runtime environment).
7. **product**: `.py` under `adp_ext/` and `ada_ext/`. Contrast series. It
   includes the app-side SDK demo/recorder modules (`ada_ext/ada/sdk_demo_*`)
   and their tests; these were not split out.
8. **other_code**: every other `.py` (other experiments such as
   `experiments/compact_vehicle/`, `docs/site/fragments/`, other `tools/`).

`code_supporting_total` = groups 1–6.

## Other series

- **Plans/open work:** `open_lines`, `open_files` = all files under `docs/open/`.
  `worklog_lines` = `docs/worklog.md`. `sessions_lines` = `docs/sessions/` and
  `docs/project/sessions/` (handoff/coordination notes).
- **Frozen copies:** `docs_evidence_*` = files/lines under any `evidence/`
  folder inside `docs/` (`docs/evidence/`, `docs/topics/*/evidence/`; JSON
  included). `frozen_doc_copy_*` = files under any `evidence/documents/`
  folder (where the exact-byte document copies lived, e.g.
  `experiments/platform_qualification/evidence/documents/`).
  `locations_*`: files named `locations.json` or `evidence-locations.json`
  (`docs/evidence/locations.json` / `docs/project/evidence-locations.json`,
  `experiments/platform_qualification/sdk_reuse/evidence/locations.json`);
  `locations_documents` = sum of the lengths of their `documents` arrays (one
  entry per frozen copy: original path, copy path, SHA-256, bytes);
  `locations_distinct_originals` = distinct `original_path` values.
  `receipt-locations.json` is not matched.
- **Run output in Git:** `exp_files_*`, `exp_bytes_*` = tracked blobs under
  `experiments/`, by extension `.npz`, `.json`, `.gz` (incl. `.json.gz`),
  `.jsonl`, `.py`, other. Bytes are blob sizes from `ls-tree -l`.
- **Commits:** `commits_total` = first-parent commits that day.
  `commits_<group>` = those whose first-parent diff (`--no-renames`, so both
  old and new path of a move) touches a path of that group; also
  `commits_docs_open`, `commits_worklog`, `commits_sessions`.
- **Text written for the developer:** `added_lines_*`, `added_words_*` = `+`
  lines of the first-parent diff (`-M`, rename detection on) and their
  whitespace-split word count, for `docs/open/**` (`open`),
  `docs/sessions/**` + `docs/project/sessions/**` (`sessions`) and
  `docs/worklog.md` (`worklog`). Lines and words only; no reading-time
  estimate.

## Approval statements (`approvals.py`)

Pattern (case-insensitive) over added lines of `*.md` (first-parent, `-M`,
`-U0`), excluding `.docs-kit/`, `third_party/`, `evidence/documents/`,
`/data/`, `/runs/`:

- the pattern

  ```text
  <who>[ -](approved|accepted|chose|decided|agreed|confirmed|selected|authori[sz]ed|signed off|asked|answered|requested|validated|said|picked|opted|retired|wanted|preferred)
  ```

  where `<who>` = the developer's handle, `the user`, `user`, `the owner`,
  `owner`, `human` (also `user-approved` style)
- `<who>'s (decision|choice|answer)`
- `as <handle>` / `per <handle>`
- `<handle>: "` (quoted answers, e.g. Plan 11's status line)

`line` = line number in the new file from the hunk header. `repeat_of_earlier`
= 1 when the matched phrase plus the next 60 characters already appeared in an
earlier match (re-wraps, moves, copies). Counts in `events.md` use first
occurrences. Pending-approval wording ("awaits user approval", "needs the
developer's approval") is deliberately not matched.

Limits: wording outside the pattern is missed; a match can still be a rule
("the user-requested pause") rather than a decision; approvals given only in
chat and never written to Git are invisible.

**Built without a recorded approval:** for each subsystem, `summarize.py`
lists first-occurrence approval statements from the 7 days before and on the
day the subsystem's first file appeared, filtered by subsystem keywords. No
hit, or hits that approve something else, is reported as "no approval
recorded". This is a lower bound on what Git shows, not proof that no
approval was given.

## Cleanups (`cleanups.py`)

Per first-parent commit: files added/deleted (`diff-tree --raw -M`, so a move
is not a deletion), bytes of deleted/added blobs (`cat-file --batch-check`),
text lines added/deleted (`diff-tree --numstat --no-renames`, so a move counts
as deleted + added lines), deleted lines per group. `net_removal = 1` when
deleted lines > added lines or deleted files > added files.

## Renames and moves

Snapshot series are measured **by path at each snapshot**; renames are not
followed. A file that moves between groups (e.g. `attended_parts/closure.py`
to `tools/run_journal_candidates/` on 2026-11-15, both attended) changes the
series only if the groups differ. Moves of plan drafts out of `docs/open/`
into `evidence/documents/` (2026-10-17) show as a fall in `open_lines` and a
rise in `frozen_doc_copy_lines`; they are not deletions.

## Reliability

- `exp_bytes_*`: 39 `sdk_reuse/runs/**/physics.jsonl|measurements.jsonl` files
  are Git LFS pointers; their bytes are pointer sizes (~130 B), so
  `exp_bytes_jsonl` undercounts. `.gz` bytes are compressed sizes.
- `exp_files_py` / `exp_bytes_py` are mostly source snapshots stored in run
  folders (e.g. 32,403 `.py` files, 259 MB under
  `experiments/compact_vehicle/physx_vehicle_followthrough/**/runs/` at the
  pinned ref), not maintained code.
- `docs_evidence_lines` is dominated by generated JSON
  (`docs/evidence/artifacts.json`, `retention.json`, ~92 k lines on
  2026-11-09–10).
- Large single-day jumps (2026-10-05, 2026-10-08) are bulk landings of work
  done earlier in other worktrees; the day is the landing day, not the
  writing day.
- `product` includes SDK-integration and attended app-side code; it is not a
  clean "product" measure.
- Committer dates were used; author dates may differ for rebased commits.

## Not measured

- Content outside Git: `.build/`, local evidence stores, chats, agent
  transcripts, Codex worktrees, GitHub.
- Side-branch history before merge; non-first-parent commits.
- Non-Python code (`.rs`, `.sh`, `.js`, `.css`) in the code groups.
- Text written in topic records (`docs/topics/**`), experiment READMEs,
  commit messages, review receipts under `data/` or `evidence/` (they are
  outside the three "written for the developer" destinations).
- Reading time, effort or cost.
