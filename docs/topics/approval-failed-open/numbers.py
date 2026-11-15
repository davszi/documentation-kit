#!/usr/bin/python3 -I
"""Recompute every number the approval-failed-open record cites and write numbers.md.

Usage: python3 -I numbers.py [--check] [measurement folder] [numbers.md]
The measurement folder (default: measurement/ beside this script) holds
timeline.csv, cleanups.csv, approvals.csv and approvals_commit_messages.csv,
measured read-only from ADP `main` at b8b80e0b025051d81eaf60d906655049bbe4f12b
on 2026-11-15. With --check the script writes nothing and exits 1 when
numbers.md differs from what it would write. Stdlib only. Prints a check line
when a value differs from the headline the project's session reported, or
when the record shows a number this script does not know.
"""
import csv
import io
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if a != "--check"]
check = "--check" in sys.argv[1:]
src = args[0] if args else os.path.join(HERE, "measurement")
out = args[1] if len(args) > 1 else os.path.join(HERE, "numbers.md")
RECORD_FILE = "approval-failed-open.md"


def load(name):
    with open(os.path.join(src, name), newline="") as f:
        return list(csv.DictReader(f))


T = load("timeline.csv")
K = load("cleanups.csv")
A = load("approvals.csv")
C = load("approvals_commit_messages.csv")
BY = {r["date"]: r for r in T}
BUILD = ("2026-09-24", "2026-11-09")
CLEAN = ("2026-11-10", "2026-11-15")
BEFORE = ("2026-07-01", "2026-09-23")

rows = []  # (id, value, unit, source)


def add(i, value, unit, source):
    rows.append((i, value, unit, source))
    return value


def v(day, col):
    return int(BY[day][col])


def peak(col):
    best = max(T, key=lambda r: int(r[col]))  # first day of the maximum
    return int(best[col]), best["date"]


def first_nonzero(col):
    r = next(r for r in T if int(r[col]))
    return int(r[col]), r["date"]


def span(a, b):
    return [r for r in T if a <= r["date"] <= b]


def ssum(rs, col):
    return sum(int(r[col]) for r in rs)


def words(r):
    return (int(r["added_words_open"]) + int(r["added_words_worklog"])
            + int(r["added_words_sessions"]))


def commit(c):
    return next(r for r in K if r["commit"] == c)


TL = "`timeline.csv`"
CL = "`cleanups.csv`"

# --- period -----------------------------------------------------------------
add("rows", len(T), "days", f"{TL}: rows {T[0]['date']} to {T[-1]['date']}")

# --- supporting code and product code --------------------------------------
add("sup_0923", v("2026-09-23", "code_supporting_total"), "lines", f"{TL} `code_supporting_total`, 2026-09-23")
add("sup_0927", v("2026-09-27", "code_supporting_total"), "lines", f"{TL} `code_supporting_total`, 2026-09-27")
add("sup_1001", v("2026-10-01", "code_supporting_total"), "lines", f"{TL} `code_supporting_total`, 2026-10-01")
p, d = peak("code_supporting_total")
add("sup_peak", p, f"lines on {d}", f"{TL} max of `code_supporting_total`")
add("sup_now", v("2026-11-15", "code_supporting_total"), "lines", f"{TL} `code_supporting_total`, 2026-11-15")
add("prod_1001", v("2026-10-01", "code_product"), "lines", f"{TL} `code_product`, 2026-10-01")
p, d = peak("code_product")
add("prod_peak", p, f"lines on {d}", f"{TL} max of `code_product`")
add("prod_now", v("2026-11-15", "code_product"), "lines", f"{TL} `code_product`, 2026-11-15")
add("sup_over_prod_now", round(v("2026-11-15", "code_supporting_total") / v("2026-11-15", "code_product"), 2),
    "ratio", "`sup_now` / `prod_now`")
add("pq_0927", v("2026-09-27", "code_pq_other"), "lines", f"{TL} `code_pq_other`, 2026-09-27 (first non-zero day)")
add("pq_now", v("2026-11-15", "code_pq_other"), "lines", f"{TL} `code_pq_other`, 2026-11-15")

# --- harnesses ---------------------------------------------------------------
val, d = first_nonzero("code_harness")
add("harn_first", val, f"lines on {d}", f"{TL} first non-zero `code_harness`")
add("harn_first_files", v(d, "files_harness"), "files", f"{TL} `files_harness`, {d}")
add("harn_1013", v("2026-10-13", "code_harness"), "lines", f"{TL} `code_harness`, 2026-10-13")
p, d = peak("code_harness")
add("harn_peak", p, f"lines on {d}", f"{TL} max of `code_harness`")
add("harn_peak_files", v(d, "files_harness"), "files", f"{TL} `files_harness`, {d}")
add("harn_now", v("2026-11-15", "code_harness"), "lines", f"{TL} `code_harness`, 2026-11-15")
add("harn_now_files", v("2026-11-15", "files_harness"), "files", f"{TL} `files_harness`, 2026-11-15")
add("harn_commits", ssum(T, "commits_harness"), "commits", f"{TL} sum of `commits_harness`, all rows")

# --- attended evidence ------------------------------------------------------
val, d = first_nonzero("code_attended")
add("att_first", val, f"lines on {d}", f"{TL} first non-zero `code_attended`")
add("att_1103", v("2026-11-03", "code_attended"), "lines", f"{TL} `code_attended`, 2026-11-03")
add("att_1104", v("2026-11-04", "code_attended"), "lines", f"{TL} `code_attended`, 2026-11-04")
p, d = peak("code_attended")
add("att_peak", p, f"lines on {d}", f"{TL} max of `code_attended`")
add("att_peak_files", v(d, "files_attended"), "files", f"{TL} `files_attended`, {d}")
add("att_now", v("2026-11-15", "code_attended"), "lines", f"{TL} `code_attended`, 2026-11-15")
add("att_now_files", v("2026-11-15", "files_attended"), "files", f"{TL} `files_attended`, 2026-11-15")

# --- pool and slot -----------------------------------------------------------
val, d = first_nonzero("code_pool")
add("pool_first", val, f"lines on {d}", f"{TL} first non-zero `code_pool`")
add("pool_1104", v("2026-11-04", "code_pool"), "lines", f"{TL} `code_pool`, 2026-11-04")
p, d = peak("code_pool")
add("pool_peak", p, f"lines on {d}", f"{TL} max of `code_pool`")
add("pool_now", v("2026-11-15", "code_pool"), "lines", f"{TL} `code_pool`, 2026-11-15")
add("pool_now_files", v("2026-11-15", "files_pool"), "files", f"{TL} `files_pool`, 2026-11-15")

# --- documentation and evidence tooling -------------------------------------
p, d = peak("code_doctools")
add("doc_peak", p, f"lines on {d}", f"{TL} max of `code_doctools`")
add("doc_now", v("2026-11-15", "code_doctools"), "lines", f"{TL} `code_doctools`, 2026-11-15")
p, d = peak("code_evidencetools")
add("evt_peak", p, f"lines on {d}", f"{TL} max of `code_evidencetools`")
add("evt_now", v("2026-11-15", "code_evidencetools"), "lines", f"{TL} `code_evidencetools`, 2026-11-15")

# --- plans (docs/open) -------------------------------------------------------
add("open_0923", v("2026-09-23", "open_lines"), "lines", f"{TL} `open_lines`, 2026-09-23")
add("open_1001", v("2026-10-01", "open_lines"), "lines", f"{TL} `open_lines`, 2026-10-01")
p, d = peak("open_lines")
add("open_peak", p, f"lines on {d}", f"{TL} max of `open_lines`")
add("open_peak_files", v(d, "open_files"), "files", f"{TL} `open_files`, {d}")
add("open_1017", v("2026-10-17", "open_lines"), "lines", f"{TL} `open_lines`, 2026-10-17")
add("open_1017_files", v("2026-10-17", "open_files"), "files", f"{TL} `open_files`, 2026-10-17")
add("open_now", v("2026-11-15", "open_lines"), "lines", f"{TL} `open_lines`, 2026-11-15")
add("open_now_files", v("2026-11-15", "open_files"), "files", f"{TL} `open_files`, 2026-11-15")
add("worklog_1001", v("2026-10-01", "worklog_lines"), "lines", f"{TL} `worklog_lines`, 2026-10-01")
add("worklog_now", v("2026-11-15", "worklog_lines"), "lines", f"{TL} `worklog_lines`, 2026-11-15")

# --- frozen copies -----------------------------------------------------------
add("frozen_1017_files", v("2026-10-17", "frozen_doc_copy_files"), "files", f"{TL} `frozen_doc_copy_files`, 2026-10-17")
add("frozen_1017_lines", v("2026-10-17", "frozen_doc_copy_lines"), "lines", f"{TL} `frozen_doc_copy_lines`, 2026-10-17")
p, d = peak("frozen_doc_copy_lines")
add("frozen_peak_lines", p, f"lines on {d}", f"{TL} max of `frozen_doc_copy_lines`")
add("frozen_peak_files", v(d, "frozen_doc_copy_files"), "files", f"{TL} `frozen_doc_copy_files`, {d}")
add("loc_1017", v("2026-10-17", "locations_documents"), "entries", f"{TL} `locations_documents`, 2026-10-17")
add("loc_1018", v("2026-10-18", "locations_documents"), "entries", f"{TL} `locations_documents`, 2026-10-18")
add("loc_files_1017", v("2026-10-17", "locations_files"), "manifests", f"{TL} `locations_files`, 2026-10-17")
add("frozen_1111", v("2026-11-11", "frozen_doc_copy_files"), "files", f"{TL} `frozen_doc_copy_files`, 2026-11-11")
p, d = peak("docs_evidence_lines")
add("docev_peak", p, f"lines on {d}", f"{TL} max of `docs_evidence_lines` (all `docs/**/evidence/`)")

# --- run output in Git -------------------------------------------------------
add("exp_b_0923", v("2026-09-23", "exp_bytes_total"), "bytes", f"{TL} `exp_bytes_total`, 2026-09-23")
add("exp_b_1001", v("2026-10-01", "exp_bytes_total"), "bytes", f"{TL} `exp_bytes_total`, 2026-10-01")
add("exp_b_1004", v("2026-10-04", "exp_bytes_total"), "bytes", f"{TL} `exp_bytes_total`, 2026-10-04")
add("exp_b_1005", v("2026-10-05", "exp_bytes_total"), "bytes", f"{TL} `exp_bytes_total`, 2026-10-05")
p, d = peak("exp_bytes_total")
add("exp_b_peak", p, f"bytes on {d}", f"{TL} max of `exp_bytes_total`")
add("exp_b_now", v("2026-11-15", "exp_bytes_total"), "bytes", f"{TL} `exp_bytes_total`, 2026-11-15")
add("exp_f_1001", v("2026-10-01", "exp_files_total"), "files", f"{TL} `exp_files_total`, 2026-10-01")
add("exp_f_now", v("2026-11-15", "exp_files_total"), "files", f"{TL} `exp_files_total`, 2026-11-15")
add("exp_py_b_now", v("2026-11-15", "exp_bytes_py"), "bytes", f"{TL} `exp_bytes_py`, 2026-11-15")
add("exp_py_f_now", v("2026-11-15", "exp_files_py"), "files", f"{TL} `exp_files_py`, 2026-11-15")
add("exp_npz_b_now", v("2026-11-15", "exp_bytes_npz"), "bytes", f"{TL} `exp_bytes_npz`, 2026-11-15")
for c in ("15d3e02a", "a93ab550", "ff6ede7e", "0c1c2b99"):
    r = commit(c)
    add(f"add_b_{c}", int(r["bytes_added"]), f"bytes added on {r['date']}", f"{CL} `bytes_added`, commit `{c}`")
    add(f"add_f_{c}", int(r["files_added"]), "files added", f"{CL} `files_added`, commit `{c}`")
r1005 = [r for r in K if r["date"] == "2026-10-05"]
add("add_b_1005_all", sum(int(r["bytes_added"]) for r in r1005), "bytes", f"{CL} sum of `bytes_added`, all commits dated 2026-10-05")

# --- text written for the developer -----------------------------------------
b = span(*BUILD)
add("days_build", len(b), "days", f"{TL} rows {BUILD[0]} to {BUILD[1]}")
add("commit_days_build", sum(1 for r in b if int(r["commits_total"])), "days", f"{TL} rows in build-up with `commits_total` > 0")
add("w_open_build", ssum(b, "added_words_open"), "words", f"{TL} sum of `added_words_open`, build-up")
add("w_worklog_build", ssum(b, "added_words_worklog"), "words", f"{TL} sum of `added_words_worklog`, build-up")
add("w_sessions_build", ssum(b, "added_words_sessions"), "words", f"{TL} sum of `added_words_sessions`, build-up")
wb = add("w_build", sum(words(r) for r in b), "words", "sum of the three rows above")
add("w_per_day_build", round(wb / len(b)), "words per calendar day", "`w_build` / `days_build`")
wd = [words(r) for r in b if words(r)]
add("w_median_writing_day", round(statistics.median(wd)), "words", "median of daily words over build-up days with any words")
add("w_days_writing", len(wd), "days", "build-up days with any words written")
mx = max(b, key=words)
add("w_max_day", words(mx), f"words on {mx['date']}", f"{TL} max of open+worklog+sessions words per day, build-up")
add("w_max_day_open", int(mx["added_words_open"]), f"words on {mx['date']}", f"{TL} `added_words_open`, {mx['date']}")
second = sorted(b, key=words)[-2]
add("w_second_day", words(second), f"words on {second['date']}", f"{TL} second-largest daily total, build-up")
add("w_days_over_10k", sum(1 for r in b if words(r) >= 10000), "days", "build-up days with at least 10,000 words")
cl = span(*CLEAN)
add("w_clean", sum(words(r) for r in cl), "words", f"{TL} open+worklog+sessions words, {CLEAN[0]} to {CLEAN[1]}")

# --- commits per period -----------------------------------------------------
add("commits_before", ssum(span(*BEFORE), "commits_total"), "commits", f"{TL} sum of `commits_total`, {BEFORE[0]} to {BEFORE[1]}")
add("commits_build", ssum(b, "commits_total"), "commits", f"{TL} sum of `commits_total`, build-up")
add("commits_clean", ssum(cl, "commits_total"), "commits", f"{TL} sum of `commits_total`, cleanup")

# --- approvals ---------------------------------------------------------------
first = [a for a in A if a["repeat_of_earlier"] == "0"]
for lab, (a0, a1) in (("before", BEFORE), ("build", BUILD), ("clean", CLEAN)):
    f = [x for x in first if a0 <= x["date"] <= a1]
    add(f"appr_{lab}", len(f), "statements", f"`approvals.csv` rows with `repeat_of_earlier` = 0, {a0} to {a1}")
    add(f"appr_cm_{lab}", len({x['commit'] for x in C if a0 <= x["date"] <= a1}), "commits",
        f"`approvals_commit_messages.csv` distinct `commit`, {a0} to {a1}")
fb = [x for x in first if BUILD[0] <= x["date"] <= BUILD[1]]
add("appr_build_named", sum(1 for x in fb if "the developer" in x["phrase"].lower()), "statements",
    "build-up first occurrences whose `phrase` names the developer")
add("appr_build_generic", sum(1 for x in fb if "the developer" not in x["phrase"].lower()), "statements",
    "build-up first occurrences whose `phrase` says user, owner or human")
random.seed(20261115)
sample = random.sample(fb, 25)
add("appr_sample", len(sample), "rows", "`random.seed(20261115)`; `random.sample` of build-up first occurrences; read by hand, see the note below the table")

# --- cleanup -------------------------------------------------------------------
nr = [r for r in K if r["net_removal"] == "1" and r["date"] >= CLEAN[0]]
add("nr_commits", len(nr), "commits", f"{CL} rows with `net_removal` = 1 from {CLEAN[0]}")
add("nr_days", len({r['date'] for r in nr}), "days", "distinct dates of those commits")
add("nr_lines_del", sum(int(r["lines_deleted"]) for r in nr), "lines", "sum of `lines_deleted` over those commits")
add("nr_lines_add", sum(int(r["lines_added"]) for r in nr), "lines", "sum of `lines_added` over those commits")
add("nr_files_del", sum(int(r["files_deleted"]) for r in nr), "files", "sum of `files_deleted` over those commits")
add("nr_bytes_del", sum(int(r["bytes_deleted"]) for r in nr), "bytes", "sum of `bytes_deleted` over those commits")
add("nr_del_docev", sum(int(r["deleted_docs_evidence"]) for r in nr), "lines", "sum of `deleted_docs_evidence` over those commits")
add("nr_del_att", sum(int(r["deleted_attended"]) for r in nr), "lines", "sum of `deleted_attended` over those commits")
nr4 = [r for r in K if r["net_removal"] == "1" and r["date"] >= "2026-11-04"]
add("nr4_commits", len(nr4), "commits", f"{CL} rows with `net_removal` = 1 from 2026-11-04")
add("nr4_lines_del", sum(int(r["lines_deleted"]) for r in nr4), "lines", "sum of `lines_deleted` over those commits")
for c in ("a18d94e5", "1a541cf2", "3197ab3e", "1797bc4b", "b72475d9", "79edb62e"):
    r = commit(c)
    add(f"del_{c}", int(r["lines_deleted"]), f"lines deleted on {r['date']}", f"{CL} `lines_deleted`, commit `{c}`")
    add(f"addl_{c}", int(r["lines_added"]), "lines added", f"{CL} `lines_added`, commit `{c}`")
    add(f"delf_{c}", int(r["files_deleted"]), "files deleted", f"{CL} `files_deleted`, commit `{c}`")
add("pool_del_b72475d9", int(commit("b72475d9")["deleted_pool"]), "lines", f"{CL} `deleted_pool`, commit `b72475d9`")
sup_peak_v, att_peak_v = peak("code_supporting_total")[0], peak("code_attended")[0]
add("sup_drop_lines", sup_peak_v - v("2026-11-15", "code_supporting_total"), "lines", "`sup_peak` - `sup_now`")
add("sup_drop_pct", round(100 * (sup_peak_v - v("2026-11-15", "code_supporting_total")) / sup_peak_v, 1),
    "percent", "`sup_drop_lines` / `sup_peak` x 100")
falls = [(T[i]["date"], int(T[i]["code_supporting_total"]) - int(T[i - 1]["code_supporting_total"]))
         for i in range(1, len(T)) if int(T[i]["code_supporting_total"]) < int(T[i - 1]["code_supporting_total"])]
add("sup_first_fall", falls[0][1], f"lines on {falls[0][0]}", f"{TL} first day `code_supporting_total` is below the day before; "
    f"all falls: {', '.join(f'{d} {x:,}' for d, x in falls)}")
add("docev_now_lines", v("2026-11-15", "docs_evidence_lines"), "lines", f"{TL} `docs_evidence_lines`, 2026-11-15")
add("docev_now_files", v("2026-11-15", "docs_evidence_files"), "files", f"{TL} `docs_evidence_files`, 2026-11-15")
cross = next(r for r in T if int(r["code_supporting_total"]) > int(r["code_product"]))
add("cross_day", int(cross["code_supporting_total"]), f"supporting lines on {cross['date']}, against {int(cross['code_product']):,} product lines",
    f"{TL} first row with `code_supporting_total` > `code_product`")
pk = max(T, key=lambda r: int(r["code_supporting_total"]))
add("sup_over_prod_peak", round(int(pk["code_supporting_total"]) / int(pk["code_product"]), 2), f"ratio on {pk['date']}",
    f"{TL} `code_supporting_total` / `code_product`, {pk['date']}")
add("w_0924_0925", words(BY["2026-09-24"]) + words(BY["2026-09-25"]), "words", f"{TL} open+worklog+sessions words, 2026-09-24 plus 2026-09-25")
add("harn_cleanup_removed", peak("code_harness")[0] - v("2026-11-15", "code_harness"), "lines", "`harn_peak` - `harn_now`")
add("del_ab1e3c9f", int(commit("ab1e3c9f")["lines_deleted"]), "lines deleted on 2026-10-17", f"{CL} `lines_deleted`, commit `ab1e3c9f` (generated site sources)")
add("att_drop_lines", att_peak_v - v("2026-11-15", "code_attended"), "lines", "`att_peak` - `att_now`")

# --- numbers that only the page's figures draw (draw_figures.py) -----------------
add("prod_1110", v("2026-11-10", "code_product"), "lines", f"{TL} `code_product`, 2026-11-10, the day of `sup_peak`")
add("frozen_now_lines", v("2026-11-15", "frozen_doc_copy_lines"), "lines", f"{TL} `frozen_doc_copy_lines`, 2026-11-15")
NAMED = ("a18d94e5", "1a541cf2", "3197ab3e", "1797bc4b")
assert all(c in {r["commit"] for r in nr} for c in NAMED), "a named removal is not a net-removal commit of the cleanup"
add("nr_other_commits", len(nr) - len(NAMED), "commits",
    "`nr_commits` minus the four commits of `del_a18d94e5`, `del_1a541cf2`, `del_3197ab3e` and `del_1797bc4b`")
add("nr_other_lines", sum(int(r["lines_deleted"]) for r in nr) - sum(int(commit(c)["lines_deleted"]) for c in NAMED),
    "lines", "`nr_lines_del` minus the lines those four commits deleted")

# --- headline checks -----------------------------------------------------------
HEAD = {"sup_1001": 7976, "sup_peak": 269241, "sup_now": 247082, "prod_1001": 40254, "prod_now": 90261,
        "harn_peak": 132652, "harn_peak_files": 480, "att_peak": 25330, "att_now": 4588,
        "open_peak": 15785, "w_build": 354333, "w_max_day_open": 50588, "appr_build": 181,
        "appr_cm_build": 3, "commits_build": 499, "appr_cm_clean": 80, "commits_clean": 125,
        "nr_commits": 34, "nr_lines_del": 145353, "del_a18d94e5": 92813, "del_1a541cf2": 14166,
        "days_build": 47}
val = {i: x for i, x, _, _ in rows}
for k, h in HEAD.items():
    if val[k] != h:
        print(f"DIFFERS {k}: recomputed {val[k]}, headline {h}")

# Values not in the CSV files: (value, unit, how obtained). "Checked" = read in Git when the record was drafted.
OTHER = [
    ("185,782", "bytes", "checked: `git cat-file -s c0684183:docs/open/platform-refactor/README.md` (ADP snapshot of 2026-10-16)"),
    ("21,413", "words", "checked: `git show c0684183:docs/open/platform-refactor/README.md | wc -w`"),
    ("103,809", "bytes", "checked: `git cat-file -s c0684183:docs/open/vehicle-and-training-design-review.md`"),
    ("11,389 files from 616 runs; 639 named entries", "files, runs", "checked: commit message of ADP `0c1c2b99` (2026-11-12)"),
    ("53", "frozen documents", "kit worklog 2026-11-11 and `docs/open/simplify-frozen-record-machinery.md`; matches `loc_1018`"),
    ("164 of 3,946", "links needing the path adapter", "kit worklog 2026-11-11, measured on ADP `origin/main` at `7d85f2a4` by two sessions; not rechecked"),
    ("52 of 53", "documents whose bytes Git returns", "kit worklog 2026-11-11; not rechecked"),
    ("10,125 / 7,194", "lines of attended-only code / tests", "ADP record `docs/topics/attended-sessions/attended-sessions.md` at `b68a1d02` (deleted in `3197ab3e`), section What it costs; not rechecked"),
    ("18", "attended sessions launched 2026-10-28 to 2026-11-05", "same record, section Results today; not rechecked"),
    ("3", "sessions that passed their whole (smaller) question under the older checks", "same record, section Results today"),
    ("0", "sessions that passed all Plan 11 parts", "same record, section Results today"),
    ("6 + 2", "preparation stages + independent reviews before a session", "same record, section What it costs"),
    ("161 / 51", "lines of `tooling/number_ledger.py` / `tooling/verbatim_blocks.py` when added", "checked: kit `git show --stat 072b063` (2026-11-06); removed 2026-11-09 per kit worklog"),
    ("2026-11-04", "date of the kit's first commit, holding the section Evidence identity and frozen records", "checked: kit `git grep -n frozen ffa232a -- rules`"),
    ("2026-11-04", "date the adapter support was added", "checked: kit commit `190b5c2`"),
    ("36; 0", "slide faces on adaptation; faces that met the fixed arrangement", "kit worklog 2026-11-14, Slide faces: no prescribed arrangement"),
    ("42 of 78", "adaptation's HTML links to repository files that fail once its path adapter is gone", "kit release notes 5.0.0; not rechecked"),
    ("13,640.3", "seconds: summed run time of the 18 attended sessions, not the developer's time", "ADP attended-sessions record at `b68a1d02`, section Results today; not rechecked"),
    ("2", "local branches in the ADP checkout on 2026-11-15 (`main`, `last-pyqt`)", "checked: `git for-each-ref refs/heads`; earlier branches and worktrees are not in Git"),
]

# Numbers the short record cites: id -> the form it shows. Other forms are
# from the OTHER list or the approval sample and are named in RECORD_OTHER.
RECORD = {
    "sup_0923": "832", "sup_peak": "269,241", "sup_over_prod_peak": "three times",
    "nr_lines_del": "145,353", "prod_1001": "40,254", "prod_now": "90,261", "sup_drop_pct": "8.2 %",
    "sup_0927": "7,976", "w_0924_0925": "42,773", "add_f_15d3e02a": "22,378", "add_b_15d3e02a": "1.59 GB",
    "w_max_day": "51,556", "open_peak": "15,785", "nr_commits": "34", "sup_now": "247,082",
    "harn_peak": "132,652", "harn_peak_files": "480 files", "harn_now": "132,638", "pq_now": "101,630",
    "att_peak": "25,330", "att_peak_files": "48 files", "att_now": "4,588", "frozen_peak_lines": "6,225",
    "frozen_peak_files": "42 copies", "loc_1018": "53 manifest", "del_a18d94e5": "92,813",
    "open_peak_files": "76 files", "open_now": "5,202", "open_now_files": "21 files",
    "exp_b_peak": "6.26 GB", "exp_b_now": "6.25 GB", "exp_f_now": "83,428", "pool_peak": "8,151",
    "pool_now": "8,063", "harn_cleanup_removed": "14 harness", "days_build": "47 days",
    "w_build": "354,333", "w_per_day_build": "7,539", "appr_build": "181", "appr_build_generic": "177",
    "appr_cm_build": "3 of 499", "commits_build": "499", "appr_cm_clean": "80 of 125",
    "commits_clean": "125 commits", "nr_files_del": "221", "del_3197ab3e": "18,459",
    "del_1797bc4b": "8,814", "del_1a541cf2": "14,166", "nr4_commits": "40 net-removal",
    "nr4_lines_del": "243,416", "w_clean": "40,447", "nr_days": "6 cleanup days",
    "add_b_0c1c2b99": "325 MB",
}
RECORD_OTHER = ["13,640.3", "18 attended sessions", "36 faces", "24 of 25", "Three attended sessions"]

# Hand reading of the sample (by row number); rows not listed record an approval or choice.
VERDICT = {4: "not a given approval: lists a user-approved order as a blocker still needed"}

import re as _re
rec_path = os.path.join(HERE, RECORD_FILE)
rec = open(rec_path).read() if os.path.exists(rec_path) else ""
missing = [f"{k}: {d}" for k, d in RECORD.items() if d not in rec] + [d for d in RECORD_OTHER if d not in rec]
if missing:
    print(f"NOT IN {RECORD_FILE}:", missing)
covered = " ".join(list(RECORD.values()) + RECORD_OTHER)
body = _re.sub(r"<!--.*?-->|\]\([^)]*\)|`[^`]*`|\d{4}-\d{2}-\d{2}|\d{2}-\d{2}", " ", rec, flags=_re.S)
stray = sorted({t for t in _re.findall(r"\d[\d,]*(?:\.\d+)?", body)
                if len(t.replace(",", "")) > 1 and t not in covered})
if stray:
    print(f"numbers in {RECORD_FILE} without a RECORD entry:", stray)

f = io.StringIO()
if True:  # one block, so the table layout below reads as before
    f.write("# Numbers cited in the approval-failed-open record\n\n")
    f.write("Generated by `numbers.py` from the measurement folder's CSV files "
            "(ADP `main` at `b8b80e0b`, measured 2026-11-15). Do not edit the table by hand; "
            "rerun the script. Byte values are blob sizes; the record converts them with "
            "1 MB = 10^6 bytes and 1 GB = 10^9 bytes.\n\n")
    f.write(f"[The record]({RECORD_FILE}) cites {len(RECORD)} numbers from the first table, marked in its last "
            f"column with the form it shows, and {len(RECORD_OTHER)} from the second table and the "
            "approval sample. [background.md](background.md) cites more of the first table. The page's "
            "figures draw only numbers of these tables; [draw_figures.py](draw_figures.py) checks each "
            "one it draws against this file.\n\n")
    f.write("| Id | Value | Unit | Source column, row or computation | In the record as |\n|---|---:|---|---|---|\n")
    for i, x, u, s in rows:
        xs = f"{x:,}" if isinstance(x, int) else str(x)
        f.write(f"| `{i}` | {xs} | {u} | {s} | {RECORD.get(i, '')} |\n")
    f.write("\n## Numbers checked in Git or taken from records\n\n")
    f.write("Not computed by this script. Each row names how it was obtained.\n\n")
    f.write("| Value | Unit | Source |\n|---:|---|---|\n")
    for row in OTHER:
        f.write("| " + " | ".join(row) + " |\n")
    f.write("\n## Sample for the approval search\n\n")
    f.write("The 25 rows of `appr_sample`, as the script draws them. The verdict column "
            "is a reading by hand of the quoted line, made when the record was drafted.\n\n")
    f.write("| # | Date | Commit | File:line | Quote (start) | Verdict |\n|---|---|---|---|---|---|\n")
    for n, x in enumerate(sample, 1):
        q = x["quote"][:110].replace("|", "\\|")
        verdict = VERDICT.get(n, "records an approval or choice the person gave")
        f.write(f"| {n} | {x['date']} | `{x['commit']}` | `{x['file']}:{x['line']}` | {q} | {verdict} |\n")
    f.write(f"\nResult: {sum(1 for n in range(1, 26) if n not in VERDICT)} of 25 rows record an "
            "approval or choice the person gave; the rest are listed with their reason. "
            "Rows 2, 9, 12 and 18 quote the answer itself: \"Oke\", \"oke\", \"yes shared start\", \"yes\".\n")
text = f.getvalue()
if check:
    current = open(out).read() if os.path.exists(out) else ""
    if current != text:
        print(f"STALE {out}: rerun numbers.py without --check")
        sys.exit(1)
    print("numbers.md is current:", len(rows), "numbers")
else:
    with open(out, "w") as fh:
        fh.write(text)
    print("wrote", out, len(rows), "numbers")
