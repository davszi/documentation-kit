#!/usr/bin/python3 -I
"""Summaries quoted in events.md, recomputed from the CSV outputs.

Usage: /usr/bin/python3 -I summarize.py   (run after measure.py, approvals.py, cleanups.py)
Prints: peak/current per timeline series, approval counts by period and kind,
approval statements near each subsystem's first commit, cleanup totals.
"""
import collections
import csv
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
T = list(csv.DictReader(open(os.path.join(here, "timeline.csv"))))
A = list(csv.DictReader(open(os.path.join(here, "approvals.csv"))))
C = list(csv.DictReader(open(os.path.join(here, "approvals_commit_messages.csv"))))
K = list(csv.DictReader(open(os.path.join(here, "cleanups.csv"))))
BUILD = ("2026-09-24", "2026-11-09")
CLEAN = ("2026-11-10", "2026-11-15")

print("== series: first nonzero, peak, value on 2026-10-01, current")
for k in T[0]:
    if k in ("date", "snapshot_commit", "snapshot_is_from_that_day"):
        continue
    v = [int(x[k]) for x in T]
    if not any(v):
        continue
    i = max(range(len(v)), key=lambda j: v[j])
    f = next(j for j in range(len(v)) if v[j])
    extra = f" sum={sum(v)}" if k.startswith(("commits", "added")) else ""
    d10 = next(x for x in T if x["date"] == "2026-10-01")[k]
    print(f"{k}: first {T[f]['date']} peak {v[i]} on {T[i]['date']} 10-01 {d10} now {v[-1]}{extra}")

print("\n== text written, by period (lines/words)")
for lab, (a, b) in (("build", BUILD), ("cleanup", CLEAN)):
    rows = [x for x in T if a <= x["date"] <= b]
    for d in ("open", "sessions", "worklog"):
        print(lab, d, sum(int(x[f"added_lines_{d}"]) for x in rows),
              sum(int(x[f"added_words_{d}"]) for x in rows))

print("\n== approval statements (first occurrences) by period and category")
first = [x for x in A if x["repeat_of_earlier"] == "0"]
for lab, (a, b) in (("before", ("0000", "2026-09-23")), ("build", BUILD), ("cleanup", CLEAN)):
    rows = [x for x in first if a <= x["date"] <= b]
    print(lab, len(rows), dict(collections.Counter(x["category"] for x in rows)),
          "| commit messages:", sum(1 for x in C if a <= x["date"] <= b))
named = [x for x in first if "the developer" in x["phrase"].lower()]
print("naming the developer:", len(named), "| generic user/owner/human:", len(first) - len(named))

SUBS = {
    "attended (Plan 11, recorder)": ("2026-10-28", r"(?i)attend|plan 11|recorder|judge|demo"),
    "attended_parts (Plan 11 implementation)": ("2026-11-04", r"(?i)attend|plan 11|parts|judge|build it"),
    "native pool / slot": ("2026-11-05", r"(?i)pool|slot|budget|parallel|isolat|keeper|lease|ledger"),
    "per-experiment harnesses (sdk_reuse)": ("2026-10-08", r"(?i)supervis|harness|tooling|reuse|preserved|retain"),
    "run output in Git": ("2026-10-04", r"(?i)retain|preserv|commit|run output|lfs|keep"),
    "frozen document copies": ("2026-10-17", r"(?i)cop(y|ies)|frozen|historical|evidence"),
    "central evidence store": ("2026-11-09", r"(?i)evidence|retain|store|artifact"),
    "documentation tooling": ("2026-07-20", r"(?i)doc|tool|site|lint"),
}
print("\n== approval statements within 7 days before (and on) each subsystem's first day, keyword-filtered")
import datetime as dt
for name, (day, kw) in SUBS.items():
    d = dt.date.fromisoformat(day)
    lo = (d - dt.timedelta(days=7)).isoformat()
    hits = [x for x in first if lo <= x["date"] <= day and re.search(kw, x["quote"])]
    chits = [x for x in C if lo <= x["date"] <= day and re.search(kw, x["quote"])]
    print(f"- {name} ({day}): {len(hits)} doc lines, {len(chits)} commit messages")
    for x in hits[:6]:
        print("   ", x["date"], x["commit"], x["file"], x["line"], "|", x["quote"][:140])

print("\n== cleanup commits (net_removal=1)")
for lab, lo in (("from 2026-11-04", "2026-11-04"), ("from 2026-11-10", "2026-11-10")):
    rows = [x for x in K if x["net_removal"] == "1" and x["date"] >= lo]
    s = lambda k: sum(int(x[k]) for x in rows)
    print(lab, len(rows), "commits: lines -", s("lines_deleted"), "+", s("lines_added"),
          "files -", s("files_deleted"), "+", s("files_added"), "bytes -", s("bytes_deleted"),
          "| by group: attended", s("deleted_attended"), "pool", s("deleted_pool"),
          "doctools", s("deleted_doctools"), "evidencetools", s("deleted_evidencetools"),
          "docs/open", s("deleted_docs_open"), "docs evidence", s("deleted_docs_evidence"))

print("\n== commit messages with approval statements: distinct commits per period")
for lab, (a, b) in (("before", ("0000", "2026-09-23")), ("build", BUILD), ("cleanup", CLEAN)):
    rows = [x for x in C if a <= x["date"] <= b]
    print(lab, len(rows), "matches in", len({x["commit"] for x in rows}), "commits")
