#!/usr/bin/python3 -I
"""Per first-parent commit: what it removed and added (read-only).

For each first-parent commit of --ref committed on or after --since:
files added/deleted, text lines added/deleted (numstat, rename detection on,
.docs-kit and third_party excluded), bytes of deleted and added blobs, and
deleted lines per supporting-code group (classifier from measure.py).
A commit is flagged `net_removal` when it deletes more text lines than it
adds or deletes more files than it adds.

Usage: nice /usr/bin/python3 -I cleanups.py --repo R --ref C [--since 2026-11-01]
       [--extra c1,c2] [--name <handle>]
Writes cleanups.csv next to this script.
"""
import argparse
import csv
import importlib.util
import os
import re
import subprocess

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("measure", os.path.join(here, "measure.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
GIT = M.GIT


def run(repo, *args):
    return subprocess.run(GIT + ["-C", repo] + list(args), check=True,
                          stdout=subprocess.PIPE).stdout.decode("utf-8", "surrogateescape")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--since", default="2026-11-01")
    ap.add_argument("--extra", default="", help="comma-separated earlier commits to include")
    ap.add_argument("--name", default="", help="handle to replace with 'the developer' in subjects")
    a = ap.parse_args()
    shas = run(a.repo, "log", "--first-parent", "--reverse", "--format=%H %cs %s",
               "--since=" + a.since, a.ref).splitlines()
    for e in filter(None, a.extra.split(",")):
        shas.insert(0, run(a.repo, "show", "-s", "--format=%H %cs %s", e).strip())
    check = subprocess.Popen(GIT + ["-C", a.repo, "cat-file", "--batch-check"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def size(obj):
        check.stdin.write(obj.encode() + b"\n")
        check.stdin.flush()
        parts = check.stdout.readline().split()
        return int(parts[2]) if len(parts) == 3 else 0

    rows = []
    for line in shas:
        sha, day, subj = line.split(" ", 2)
        if a.name:
            subj = re.sub(re.escape(a.name), "the developer", subj, flags=re.I)
        r = {"date": day, "commit": sha[:8], "subject": subj,
             "files_added": 0, "files_deleted": 0, "lines_added": 0, "lines_deleted": 0,
             "bytes_added": 0, "bytes_deleted": 0}
        for g in M.GROUPS:
            r[f"deleted_{g}"] = 0
        r["deleted_docs_open"] = 0
        r["deleted_docs_evidence"] = 0
        raw = run(a.repo, "diff-tree", "-r", "-M", "--no-commit-id", "--raw",
                  "--first-parent", "-m", sha)
        for rec in raw.splitlines():
            if not rec.startswith(":"):
                continue
            meta, *paths = rec.split("\t")
            _, _, old, new, status = meta.split()
            path = paths[-1]
            if path.startswith(M.EXCLUDED_ROOTS):
                continue
            if status == "D":
                r["files_deleted"] += 1
                r["bytes_deleted"] += size(old)
            elif status == "A":
                r["files_added"] += 1
                r["bytes_added"] += size(new)
        num = run(a.repo, "diff-tree", "-r", "--no-renames", "--no-commit-id", "--numstat",
                  "--first-parent", "-m", sha)
        for rec in num.splitlines():
            parts = rec.split("\t")
            if len(parts) != 3:
                continue
            ad, de, path = parts
            if path.startswith(M.EXCLUDED_ROOTS):
                continue
            if ad == "-":
                continue
            ad, de = int(ad), int(de)
            r["lines_added"] += ad
            r["lines_deleted"] += de
            g = M.code_group(path)
            if g:
                r[f"deleted_{g}"] += de
            if path.startswith("docs/open/"):
                r["deleted_docs_open"] += de
            if M.DOCS_EVIDENCE.search(path):
                r["deleted_docs_evidence"] += de
        r["net_lines"] = r["lines_added"] - r["lines_deleted"]
        r["net_removal"] = int(r["lines_deleted"] > r["lines_added"]
                               or r["files_deleted"] > r["files_added"])
        rows.append(r)
    with open(os.path.join(here, "cleanups.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "commits;", sum(r["net_removal"] for r in rows), "net-removal")


if __name__ == "__main__":
    main()
