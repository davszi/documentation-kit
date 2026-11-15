#!/usr/bin/python3 -I
"""Find added lines and commit messages that state the developer approved,
chose, decided, accepted, asked for or answered something.

Read-only: `git log -p` over first-parent commits of the given ref.
The developer's handle is passed with --name so it is not stored here;
every written quote replaces it with "the developer".

Usage:
  nice /usr/bin/python3 -I approvals.py --repo /path/ADP --ref <commit> \
       --name <handle> [--since 2026-07-01]
Writes approvals.csv and approvals_commit_messages.csv next to this script.
"""
import argparse
import csv
import os
import re
import subprocess

GIT = ["git", "--no-optional-locks"]
VERBS = (r"approved|accepted|chose|decided|agreed|confirmed|selected|"
         r"authori[sz]ed|signed off|asked|answered|requested|validated|said|"
         r"picked|opted|retired|wanted|preferred")


def build_pattern(name):
    who = r"(?:%s|the user|user|the owner|owner|human)" % re.escape(name)
    return re.compile(
        r"\b" + who + r"(?:'s)?(?:[ -](?:" + VERBS + r")\b|'s (?:decision|choice|answer))"
        r"|\b(?:as|per) " + re.escape(name) + r"\b"
        # quoted answers: (name: "lets build it now fully")
        r"|\b" + re.escape(name) + r"\s*:\s*[\"\u201c\u201e]",
        re.I)


SKIP = re.compile(r"^(\.docs-kit|third_party)/|(^|/)evidence/documents/|/(data|runs)/")


def category(path):
    if path.startswith("docs/open/"):
        return "plan/open-work"
    if path == "docs/worklog.md":
        return "worklog"
    if re.match(r"docs/(project/)?sessions/", path):
        return "session/handoff"
    if path.startswith("docs/topics/") or path.startswith("experiments/"):
        return "topic/experiment record"
    return "guide/other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--since", default="2026-07-01")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    pat = build_pattern(a.name)
    redact = re.compile(re.escape(a.name), re.I)

    def clean(s):
        s = redact.sub("the developer", s)
        return re.sub(r"/home/[^/\s]+", "/home/<user>", s)

    out = subprocess.run(
        GIT + ["-C", a.repo, "log", "--first-parent", "--diff-merges=first-parent",
               "-M", "-p", "-U0", "--format=C %H %cI", "--since=" + a.since,
               a.ref, "--", "*.md"],
        check=True, stdout=subprocess.PIPE).stdout
    rows, seen = [], set()
    sha = day = path = None
    lineno = 0
    for raw in out.split(b"\n"):
        if raw.startswith(b"C ") and len(raw) > 50 and raw[2:42].isalnum():
            _, sha, iso = raw.decode().split()
            day = iso[:10]
            path = None
            continue
        if raw.startswith(b"+++ "):
            p = raw[4:].decode("utf-8", "surrogateescape")
            path = p[2:] if p.startswith("b/") else None
            if path and SKIP.search(path):
                path = None
            continue
        if raw.startswith(b"@@"):
            m = re.search(rb"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
            continue
        if raw.startswith(b"+") and path:
            text = raw[1:].decode("utf-8", "replace")
            for m in pat.finditer(text):
                s = max(0, m.start() - 60)
                quote = text[s:m.end() + 100].strip()
                key = re.sub(r"\s+", " ", text[m.start():m.end() + 60].lower())
                rows.append({
                    "date": day, "commit": sha[:8], "file": path,
                    "line": lineno, "category": category(path),
                    "phrase": clean(m.group(0)), "repeat_of_earlier": int(key in seen),
                    "quote": clean(quote)})
                seen.add(key)
            lineno += 1
    with open(os.path.join(here, "approvals.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    out = subprocess.run(
        GIT + ["-C", a.repo, "log", "--first-parent", "--format=%H%x1f%cI%x1f%s%n%b%x1e",
               "--since=" + a.since, a.ref], check=True, stdout=subprocess.PIPE).stdout
    crow = []
    for rec in out.decode("utf-8", "replace").split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        h, iso, msg = rec.split("\x1f", 2)
        subj = msg.split("\n", 1)[0]
        for m in pat.finditer(msg):
            s = max(0, m.start() - 40)
            crow.append({"date": iso[:10], "commit": h[:8], "subject": clean(subj),
                         "phrase": clean(m.group(0)),
                         "quote": clean(re.sub(r"\s+", " ", msg[s:m.end() + 100]))})
    with open(os.path.join(here, "approvals_commit_messages.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(crow[0].keys()))
        w.writeheader()
        w.writerows(crow)
    print(len(rows), "added doc lines;", sum(1 for r in rows if not r["repeat_of_earlier"]),
          "first occurrences;", len(crow), "commit-message matches")


if __name__ == "__main__":
    main()
