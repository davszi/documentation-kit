#!/usr/bin/python3 -I
"""Per-day measurement of ADP's first-parent history (read-only).

Reads only Git commit objects: `git log`, `git ls-tree`, `git cat-file`.
Never touches the working tree or index. Writes timeline.csv next to this
script (or to --out).

Usage:
  nice /usr/bin/python3 -I measure.py --repo /path/to/ADP --ref <commit> \
       [--start 2026-07-01] [--end 2026-11-15] [--out timeline.csv]
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys

GIT = ["git", "--no-optional-locks"]

# --------------------------------------------------------------------------
# Path classification (documented in method.md; keep the two in sync)
# --------------------------------------------------------------------------
EXCLUDED_ROOTS = (".docs-kit/", "third_party/")
# Directories that hold run output, frozen copies or generated snapshots:
# a .py file inside them is not counted as supporting code.
CODE_EXCLUDED_DIR = re.compile(
    r"/(data|runs|evidence|source_snapshot|__pycache__|pytest-tmp)/|/\d{4}-\d{2}-\d{2}/")

SI = "experiments/platform_qualification/sdk_integration/"
PQ = "experiments/platform_qualification/"

ATTENDED_NAMES = (
    "sealed_judge|sdk_attended_app_supervision|sdk_app_demo_probe|"
    "sdk_unattended_app_demo_probe|sdk_app_visual_probe|"
    "sdk_app_close_boundary|sdk_app_native_subscriptions")
POOL_NAMES = (
    r"native_resource_\w+|native_scope|native_pool_\w+|native_prebirth|"
    r"native_supervision|meter_review_selection|legacy_cpu_slot|"
    r"resource_slot\w*|resource_usage|current_legacy_meter_admission|"
    r"parallel_native_\w+")
HARNESS_SUFFIX = re.compile(
    r"(^|_)(supervision|supervisor|run|review|protocol|authority|closeout|"
    r"collection|preparation|configuration|check|budget|ledger|guard|"
    r"admission|scope)\.py$")

GROUP_RULES = [
    ("attended", [
        re.compile(r"^" + re.escape(SI) + r"attended_parts/"),
        re.compile(r"^tools/run_journal_candidates/"),
        re.compile(r"^" + re.escape(SI) + r"(test_)?(" + ATTENDED_NAMES + r")\.py$"),
    ]),
    ("doctools", [
        re.compile(r"^docs/tools/"),
        re.compile(r"^tools/docs/"),
    ]),
    ("evidencetools", [
        re.compile(r"^tools/(evidence|check_evidence|check_experiment_data)\.py$"),
        re.compile(r"^tools/tests/test_evidence\.py$"),
    ]),
    ("pool", [
        re.compile(r"^tools/coordination/"),
        re.compile(r"^" + re.escape(SI) + r"(test_)?(" + POOL_NAMES + r")\.py$"),
    ]),
]
GROUPS = ["attended", "doctools", "evidencetools", "pool", "harness",
          "pq_other", "product", "other_code"]


def code_group(path):
    """Return the supporting-code group of a tracked path, or None."""
    if not path.endswith(".py") or path.startswith(EXCLUDED_ROOTS):
        return None
    if CODE_EXCLUDED_DIR.search(path):
        return None
    for name, pats in GROUP_RULES:
        if any(p.search(path) for p in pats):
            return name
    if path.startswith(PQ):
        base = path.rsplit("/", 1)[-1]
        if base.startswith("test_"):
            base = base[5:]
        if HARNESS_SUFFIX.search(base):
            return "harness"
        return "pq_other"
    if path.startswith(("adp_ext/", "ada_ext/")):
        return "product"
    return "other_code"


DOCS_EVIDENCE = re.compile(r"^docs/(.*/)?evidence/")
FROZEN_DOC_COPY = re.compile(r"(^|/)evidence/documents/")
LOCATIONS = re.compile(r"(^|/)(evidence-)?locations\.json$")
HANDOFF = re.compile(r"^docs/(project/)?sessions/")


def ext_class(path):
    p = path.lower()
    for e in (".npz", ".jsonl", ".json", ".gz", ".py"):
        if p.endswith(e):
            return e[1:]
    return "other"


# --------------------------------------------------------------------------
# Git helpers
# --------------------------------------------------------------------------
class Blobs:
    """Line/word counts by blob SHA through one `git cat-file --batch`."""

    def __init__(self, repo):
        self.p = subprocess.Popen(GIT + ["-C", repo, "cat-file", "--batch"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.cache = {}

    def read(self, sha):
        self.p.stdin.write(sha.encode() + b"\n")
        self.p.stdin.flush()
        hdr = self.p.stdout.readline().split()
        size = int(hdr[2])
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return data

    def lines(self, sha):
        """(lines, is_text). Binary = NUL byte in the first 8000 bytes."""
        hit = self.cache.get(sha)
        if hit is not None:
            return hit
        data = self.read(sha)
        if b"\0" in data[:8000]:
            res = (0, False)
        else:
            n = data.count(b"\n")
            if data and not data.endswith(b"\n"):
                n += 1
            res = (n, True)
        self.cache[sha] = res
        return res


def git(repo, *args):
    return subprocess.run(GIT + ["-C", repo] + list(args), check=True,
                          stdout=subprocess.PIPE).stdout


def first_parent_commits(repo, ref):
    """[(sha, committer-local-date)] oldest first."""
    out = git(repo, "log", "--first-parent", "--reverse", "--format=%H %cI", ref)
    res = []
    for line in out.decode().splitlines():
        sha, iso = line.split()
        res.append((sha, iso[:10]))
    return res


def ls_tree(repo, sha):
    """Yield (mode, type, blob, size, path) for every tracked blob."""
    out = git(repo, "ls-tree", "-r", "-l", "-z", sha)
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, typ, obj, size = meta.split()
        if typ != b"blob":
            continue  # submodule gitlinks (.docs-kit, third_party/IsaacLab)
        yield obj.decode(), int(size), path.decode("utf-8", "surrogateescape")


# --------------------------------------------------------------------------
def snapshot_metrics(repo, sha, blobs):
    m = {f"code_{g}": 0 for g in GROUPS}
    m.update({f"files_{g}": 0 for g in GROUPS})
    for k in ("open_lines", "open_files", "worklog_lines",
              "docs_evidence_files", "docs_evidence_lines",
              "frozen_doc_copy_files", "frozen_doc_copy_lines",
              "locations_files", "locations_documents",
              "locations_distinct_originals", "sessions_lines"):
        m[k] = 0
    for e in ("npz", "json", "gz", "jsonl", "py", "other"):
        m[f"exp_files_{e}"] = 0
        m[f"exp_bytes_{e}"] = 0
    originals = set()
    for blob, size, path in ls_tree(repo, sha):
        if path.startswith(EXCLUDED_ROOTS):
            continue
        g = code_group(path)
        if g:
            n, txt = blobs.lines(blob)
            m[f"code_{g}"] += n
            m[f"files_{g}"] += 1
        if path.startswith("docs/open/"):
            m["open_lines"] += blobs.lines(blob)[0]
            m["open_files"] += 1
        elif path == "docs/worklog.md":
            m["worklog_lines"] = blobs.lines(blob)[0]
        elif HANDOFF.search(path):
            m["sessions_lines"] += blobs.lines(blob)[0]
        if DOCS_EVIDENCE.search(path):
            m["docs_evidence_files"] += 1
            m["docs_evidence_lines"] += blobs.lines(blob)[0]
        if FROZEN_DOC_COPY.search(path):
            m["frozen_doc_copy_files"] += 1
            m["frozen_doc_copy_lines"] += blobs.lines(blob)[0]
        if LOCATIONS.search(path):
            try:
                doc = json.loads(blobs.read(blob))
                docs = doc.get("documents", []) if isinstance(doc, dict) else []
            except ValueError:
                docs = []
            m["locations_files"] += 1
            m["locations_documents"] += len(docs)
            for d in docs:
                if isinstance(d, dict):
                    originals.add(d.get("original_path"))
        if path.startswith("experiments/"):
            e = ext_class(path)
            m[f"exp_files_{e}"] += 1
            m[f"exp_bytes_{e}"] += size
    m["locations_distinct_originals"] = len(originals)
    m["code_supporting_total"] = sum(m[f"code_{g}"] for g in GROUPS
                                     if g not in ("product", "other_code"))
    m["exp_files_total"] = sum(m[f"exp_files_{e}"] for e in
                               ("npz", "json", "gz", "jsonl", "py", "other"))
    m["exp_bytes_total"] = sum(m[f"exp_bytes_{e}"] for e in
                               ("npz", "json", "gz", "jsonl", "py", "other"))
    return m


def per_commit_activity(repo, ref, since):
    """Per first-parent commit: touched groups and written-text counts."""
    # Touched paths (no rename detection: both old and new path count).
    out = git(repo, "log", "--first-parent", "--diff-merges=first-parent",
              "--no-renames", "--name-only", "--format=C %H %cI",
              "--since=" + since, ref)
    touch = {}
    cur = None
    for line in out.decode("utf-8", "surrogateescape").splitlines():
        if line.startswith("C "):
            _, sha, iso = line.split()
            cur = touch.setdefault(sha, (iso[:10], set()))[1]
            continue
        if not line or cur is None:
            continue
        g = code_group(line)
        if g:
            cur.add(g)
        if line.startswith("docs/open/"):
            cur.add("docs_open")
        if line == "docs/worklog.md":
            cur.add("worklog")
        if HANDOFF.search(line):
            cur.add("sessions")
    # Written text: '+' lines with rename detection, per destination.
    out = subprocess.run(
        GIT + ["-C", repo, "log", "--first-parent", "--diff-merges=first-parent",
               "-M", "-p", "--format=C %H %cI", "--since=" + since, ref, "--",
               "docs/open", "docs/sessions", "docs/project/sessions",
               "docs/worklog.md"],
        check=True, stdout=subprocess.PIPE).stdout
    text = {}
    sha = None
    dest = None
    for raw in out.split(b"\n"):
        if raw.startswith(b"C ") and len(raw) > 50 and raw[2:42].isalnum():
            parts = raw.decode().split()
            sha = parts[1]
            day = parts[2][:10]
            text.setdefault(sha, [day, {}])
            dest = None
            continue
        if raw.startswith(b"+++ "):
            p = raw[4:].decode("utf-8", "surrogateescape")
            p = p[2:] if p.startswith("b/") else p
            if p.startswith("docs/open/"):
                dest = "open"
            elif p == "docs/worklog.md":
                dest = "worklog"
            elif HANDOFF.search(p):
                dest = "sessions"
            else:
                dest = None
            continue
        if raw.startswith(b"+") and dest and sha:
            body = raw[1:].decode("utf-8", "replace")
            d = text[sha][1].setdefault(dest, [0, 0])
            d[0] += 1
            d[1] += len(body.split())
    return touch, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--start", default="2026-07-01")
    ap.add_argument("--end", default="2026-11-15")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "timeline.csv"))
    a = ap.parse_args()

    commits = first_parent_commits(a.repo, a.ref)
    day_last = {}
    for sha, day in commits:
        day_last[day] = sha  # later in first-parent order wins
    start = dt.date.fromisoformat(a.start)
    end = dt.date.fromisoformat(a.end)
    carry = None
    for sha, day in commits:
        if day < a.start:
            carry = sha
    blobs = Blobs(a.repo)
    touch, text = per_commit_activity(a.repo, a.ref, a.start)
    snap_cache = {}
    rows = []
    d = start
    while d <= end:
        day = d.isoformat()
        sha = day_last.get(day, carry)
        carry = sha
        if sha not in snap_cache:
            snap_cache.clear()
            snap_cache[sha] = snapshot_metrics(a.repo, sha, blobs)
            print(day, sha[:8], file=sys.stderr, flush=True)
        row = {"date": day, "snapshot_commit": sha[:8],
               "snapshot_is_from_that_day": int(day in day_last)}
        row.update(snap_cache[sha])
        day_commits = [s for s, (dd, _) in touch.items() if dd == day]
        row["commits_total"] = len(day_commits)
        for g in GROUPS + ["docs_open", "worklog", "sessions"]:
            row[f"commits_{g}"] = sum(1 for s in day_commits if g in touch[s][1])
        for dest in ("open", "sessions", "worklog"):
            ln = wd = 0
            for s, (dd, dests) in text.items():
                if dd == day and dest in dests:
                    ln += dests[dest][0]
                    wd += dests[dest][1]
            row[f"added_lines_{dest}"] = ln
            row[f"added_words_{dest}"] = wd
        rows.append(row)
        d += dt.timedelta(days=1)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", os.path.basename(a.out), len(rows), "rows", file=sys.stderr)


if __name__ == "__main__":
    main()
