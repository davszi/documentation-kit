#!/usr/bin/python3 -I
"""List the largest files per supporting-code group at one commit.
Usage: inspect_groups.py --repo R --commit C [--top 12]
Reuses measure.py's classifier by loading it from this directory."""
import argparse, importlib.util, os, collections
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("measure", os.path.join(here, "measure.py"))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
ap = argparse.ArgumentParser(); ap.add_argument("--repo"); ap.add_argument("--commit"); ap.add_argument("--top", type=int, default=12)
ap.add_argument("--groups", default=",".join(M.GROUPS))
a = ap.parse_args()
b = M.Blobs(a.repo)
per = collections.defaultdict(list)
dirs = collections.defaultdict(collections.Counter)
for blob, size, path in M.ls_tree(a.repo, a.commit):
    g = M.code_group(path)
    if g:
        n = b.lines(blob)[0]
        per[g].append((n, path))
        dirs[g]["/".join(path.split("/")[:3])] += n
for g in a.groups.split(","):
    L = sorted(per[g], reverse=True)
    print(f"== {g}: {sum(n for n,_ in L)} lines, {len(L)} files")
    for d, n in dirs[g].most_common(6): print("   dir", n, d)
    for n, p in L[:a.top]: print("  ", n, p)
