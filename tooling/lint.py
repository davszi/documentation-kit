#!/usr/bin/env python3
"""Doc-system lint — run before pushing docs.

    python .docs-kit/docsite.py lint --project . [--strict] [--registry] [--since <rev>]

Checks (shared rules/writing.md is the spec):
  1. markdown links + anchors resolve (docs/**, AGENTS.md, CLAUDE.md, README.md)
  2. built-html internal anchors + relative hrefs resolve
  3. snippet drift: fenced blocks tagged `source=<path>#L<a>-L<b>` must appear
     in their source file (error), at the stated lines (warning otherwise)
  4. figure manifest: files ↔ entries both ways, generator scripts exist,
     doc-referenced figures are in the manifest; unreferenced figure = warning
  5. INVARIANT / DON'T-REDO marker form (bold, colon); never in worklog/OPEN
     (--registry dumps the marker registry and exits)
  6. OPEN.md format: every bullet links its owning doc; no strikethrough /
     checkboxes / DONE markers (lines get deleted, not struck)
  7. worklog format: ## YYYY-MM-DD sections newest-first; probe-line shape;
     landing entries without a commit hash = warning
  8. .build/docs/html freshness (`build.py --check`)
  9. built html loads no external resources (external <a> navigation is fine)
 10. relocated evidence records retain their manifest bytes and identities
 11. the project's pinned kit commit is on a remote branch of the kit
 12. topic structure: each docs/topics/<topic>/ page has a record beside it
     (another .md outside evidence/) or declares `page_only = "<reason>"`;
     an empty page_only is an error, an unneeded one a warning; home exempt

Notes (never fail, not even under --strict): a changed record section
(working tree vs HEAD, or vs --since <rev>) lists the topic pages that link
it, so someone rereads them.

Exit 0 clean (warnings print unless --strict fails them), 1 on errors.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

REPO = Path(os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd())).resolve()
DOCS = REPO / "docs"

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def retained_locally(dest: Path) -> bool:
    """Explicitly deferred artifacts may be absent from a fresh Git checkout."""
    manifest = _paths.local_artifacts_manifest(REPO)
    if manifest is None:
        return False
    try:
        path = str(dest.relative_to(REPO))
    except ValueError:
        return False
    return path in json.loads(manifest.read_text())["omitted_files"]


# ---------------------------------------------------------------- helpers
_paths_spec = importlib.util.spec_from_file_location(
    "docsite_paths", Path(__file__).with_name("site_paths.py"))
_paths = importlib.util.module_from_spec(_paths_spec)
_paths_spec.loader.exec_module(_paths)


def resolve_path(path: Path, *, recorded_roots=()) -> Path:
    """Resolve the public/historical documentation layout to current files."""
    return _paths.resolve_legacy_path(path, root=REPO, recorded_roots=recorded_roots)


_evidence_spec = importlib.util.spec_from_file_location(
    "docsite_evidence_documents", Path(__file__).with_name("evidence_documents.py"))
_evidence = importlib.util.module_from_spec(_evidence_spec)
_evidence_spec.loader.exec_module(_evidence)
from project_extensions import load_extension
_project_evidence = load_extension(REPO, 'evidence_validator')
if _project_evidence is not None:
    if not all(callable(getattr(_project_evidence, name, None)) for name in ('manifest_documents', 'verify')) or not hasattr(_project_evidence, 'MANIFESTS'):
        raise ValueError('evidence_validator must export MANIFESTS, manifest_documents and verify')
    _evidence = _project_evidence


def evidence_document_locations() -> dict[Path, Path]:
    """Historical origins from all exact-byte relocation collections."""
    if not any((REPO / manifest).is_file() for manifest in _evidence.MANIFESTS):
        return {}
    rows, _ = _evidence.manifest_documents(REPO)
    return {REPO / row["original_path"]: REPO / row["path"] for row in rows}


def recorded_source_roots(source: Path | None = None) -> tuple[str, ...]:
    """Explicit host origins apply only to their frozen collection or chronology."""
    roots = []
    for relative in _evidence.MANIFESTS:
        path = REPO / relative
        if not path.is_file():
            continue
        manifest = json.loads(path.read_text())
        if "source_root" not in manifest:
            continue
        origin = manifest["source_root"]
        # Validate even if there is no rebasing to perform for this source.
        resolve_path(REPO, recorded_roots=(origin,))
        if (source is None or is_entry(source, "worklog")
                or any(REPO / row["path"] == source for row in manifest["documents"])):
            roots.append(origin)
    return tuple(dict.fromkeys(roots))


def markdown_origin(path: Path) -> Path:
    resolver = getattr(_evidence, "document_origin", None)
    if resolver is not None:
        if not callable(resolver):
            raise ValueError("evidence_validator document_origin must be callable")
        origin = resolver(path, root=REPO)
        if origin is not None:
            if not isinstance(origin, (str, Path)) or not str(origin):
                raise ValueError("document_origin must return a repository path or None")
            origin = Path(origin)
            origin = Path(os.path.abspath(origin if origin.is_absolute() else REPO / origin))
            if (not origin.is_relative_to(REPO) or not origin.resolve().is_relative_to(REPO)
                    or any(parent.is_symlink() for parent in (origin, *origin.parents)
                           if parent.is_relative_to(REPO))):
                raise ValueError("document_origin must stay inside the project without symlinks")
            return origin
    return next((old for old, current in evidence_document_locations().items()
                 if current == path), path)


def md_files() -> list[Path]:
    files = set(DOCS.rglob("*.md"))
    files.update(path for path in evidence_document_locations().values() if path.is_file())
    for extra in (REPO / "AGENTS.md", REPO / "CLAUDE.md", REPO / "README.md"):
        if extra.is_file():
            files.add(extra)
    # Registered source pages render from their own folder, so their Markdown
    # links are checked as ordinary records wherever they live.
    config = DOCS / "site" / "site.toml"
    site = tomllib.loads(config.read_text()) if config.is_file() else {}
    for entry in site.get("source_pages", []) if isinstance(site.get("source_pages"), list) else []:
        source = entry.get("source") if isinstance(entry, dict) else None
        if isinstance(source, str) and (REPO / source).is_file():
            files.add(REPO / source)
    return sorted(files)


FENCE_RE = re.compile(r"^(```|~~~)", re.M)


def strip_code(text: str) -> str:
    """Blank out fenced blocks + inline code so link/marker scans skip them."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def slugify(text: str) -> str:
    """GitHub-style: strip punctuation, then EVERY space becomes a hyphen
    (consecutive spaces left by stripped punctuation stay as -- runs)."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s", "-", text.strip())


def md_anchors(path: Path) -> set[str]:
    text = re.sub(r"<!--[\s\S]*?-->", "", path.read_text())
    anchors = set(re.findall(r'''<[A-Za-z][^>]*\bid\s*=\s*["']([^"']+)["']''', strip_code(text)))
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"#{1,6}\s+(.*)", line)
        if not m:
            continue
        text = m.group(1)
        idm = re.search(r"\{#([A-Za-z0-9][\w-]*)\}\s*$", text)
        anchors.add(idm.group(1) if idm else slugify(re.sub(r"\{#.*\}\s*$", "", text)))
    return anchors


def html_ids(path: Path) -> set[str]:
    return set(re.findall(r'id="([^"]+)"', path.read_text()))


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")


# ---------------------------------------------------------------- checks
def check_md_links() -> None:
    for f in md_files():
        # Page sources render into docs/html/ — links ABOVE <!-- page-end -->
        # target the output location; the working-notes tail below it is
        # consumed as source (GitHub), so its links resolve from the file.
        text = f.read_text()
        chunks = [(text, markdown_origin(f).parent)]
        if _paths.is_topic_page(f, REPO):
            page, _, tail = text.partition("<!-- page-end -->")
            chunks = [(page, DOCS / "html"), (tail, f.parent)]
        for chunk, base in chunks:
            _check_chunk_links(f, chunk, base)


_ENTRY_DEFAULTS = {"worklog": "docs/worklog.md", "open_work": "docs/open/OPEN.md"}
_entry_cache: dict = {}


def entry_path(key: str) -> Path | None:
    """The project's configured chronology or open-work file, validated once.

    Projects keep docs/worklog.md and docs/open/OPEN.md; a project with
    established names may set `worklog` or `open_work` in docs/site/site.toml.
    """
    if key in _entry_cache:
        return _entry_cache[key]
    config = REPO / 'docs/site/site.toml'
    site = tomllib.loads(config.read_text()) if config.is_file() else {}
    relative = site.get(key, _ENTRY_DEFAULTS[key])
    path = None
    if (not isinstance(relative, str) or Path(relative).is_absolute()
            or '..' in Path(relative).parts):
        error(f'{key} must name a project-relative file')
    else:
        candidate = REPO / relative
        if candidate.is_symlink() or not candidate.resolve().is_relative_to(REPO):
            error(f'{key} must stay inside the project')
        else:
            path = candidate
    _entry_cache[key] = path
    return path


def is_entry(f: Path, key: str) -> bool:
    path = entry_path(key)
    return path is not None and f.resolve() == path.resolve()


def _check_chunk_links(f: Path, text: str, base: Path) -> None:
        locations = evidence_document_locations()
        frozen_source = f in locations.values()
        origins = recorded_source_roots(f) if frozen_source or is_entry(f, "worklog") else ()
        for target in LINK_RE.findall(strip_code(text)):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, frag = target.partition("#")
            path_part = path_part.partition("?")[0]  # versioned asset URLs carry ?v=<hash>
            rel = f.relative_to(REPO)
            if not path_part:  # same-file anchor
                if frag and frag not in md_anchors(f):
                    error(f"{rel}: dead same-file anchor #{frag}")
                continue
            dest = resolve_path(base / path_part, recorded_roots=origins)
            if ((frozen_source or is_entry(f, "worklog")) and Path(path_part).is_absolute()
                    and not dest.is_relative_to(REPO)):
                error(f"{rel}: unknown historical checkout root in {target}")
                continue
            relocated = locations.get(dest)
            if relocated is not None:
                # Frozen source links resolve in their recorded historical layout,
                # including other frozen originals that now also have a live plan.
                # Live sources validate a surviving reduced plan's actual contents.
                historical_log = is_entry(f, "worklog")
                # Keep dated worklog entries append-only. A reduced surviving
                # original can lose an old anchor; consult its exact record only
                # when that specific historical anchor exists there. Current
                # sources still fail on stale anchors and neither target may
                # conceal a genuinely missing worklog anchor.
                historical_anchor = (historical_log and frag and dest.suffix == ".md"
                                     and dest.exists() and frag not in md_anchors(dest)
                                     and relocated.exists() and frag in md_anchors(relocated))
                if frozen_source or (historical_log and not dest.exists()) or historical_anchor:
                    dest = relocated
                elif not dest.exists():
                    error(f"{rel}: stale evidence document link {target}; use {relocated.relative_to(REPO)}")
                    continue
            if not dest.exists():
                if retained_locally(dest):
                    warn(f"{rel}: artifact retained locally, omitted from push: {target}")
                else:
                    error(f"{rel}: dead link {target}")
                continue
            if frag and dest.suffix == ".md" and frag not in md_anchors(dest):
                error(f"{rel}: anchor #{frag} not found in {path_part}")
            if frag and dest.suffix == ".html" and frag not in html_ids(dest):
                error(f"{rel}: anchor #{frag} not found in {path_part}")


def check_html() -> None:
    for f in sorted(resolve_path(DOCS / "html").glob("*.html")):
        text = f.read_text()
        ids = html_ids(f)
        rel = f.relative_to(REPO)
        for m in re.finditer(r'href="([^"]+)"', text):
            href = m.group(1)
            if href.startswith(("http://", "https://", "mailto:", "vscode:")):
                continue
            path_part, _, frag = href.partition("#")
            path_part = path_part.partition("?")[0]
            if not path_part:
                if frag and frag not in ids:
                    error(f"{rel}: dead internal anchor #{frag}")
                continue
            if not resolve_path(DOCS / "html" / path_part).exists():
                if retained_locally(resolve_path(DOCS / "html" / path_part)):
                    warn(f"{rel}: artifact retained locally, omitted from push: {href}")
                else:
                    error(f"{rel}: dead relative href {href}")
        # external resource loads (navigation <a> is allowed, resources are not)
        for attr, tag in (("src", "script"), ("src", "img"), ("href", "link"),
                          ("src", "video"), ("src", "audio"), ("src", "source")):
            for m in re.finditer(rf"<{tag}[^>]*\s{attr}=\"([^\"]+)\"", text):
                target = m.group(1)
                if target.startswith(("http://", "https://", "//")):
                    error(f"{rel}: external {tag} resource {target}")
                elif not target.startswith("data:"):
                    resource = resolve_path(DOCS / "html" / target.partition("#")[0].partition("?")[0])
                    if not resource.is_file():
                        if retained_locally(resource):
                            warn(f"{rel}: artifact retained locally, omitted from push: {target}")
                        else:
                            error(f"{rel}: dead {tag} resource {target}")
        for m in re.finditer(r"url\(\s*['\"]?(https?:)?//", text):
            error(f"{rel}: external url() resource reference")


SNIPPET_RE = re.compile(r"^```\S*\s+.*?source=(\S+?)#L(\d+)-L(\d+).*?\n(.*?)^```", re.M | re.S)


def check_snippets() -> None:
    for f in md_files():
        rel = f.relative_to(REPO)
        for m in SNIPPET_RE.finditer(f.read_text()):
            src, lo, hi, body = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            src_path = resolve_path(REPO / src)
            if not src_path.is_file():
                src_path = resolve_path(markdown_origin(f).parent / src)
            if not src_path.is_file():
                error(f"{rel}: snippet source missing: {src}")
                continue
            norm = lambda s: re.sub(r"\s+", " ", s).strip()
            hay = norm(src_path.read_text())
            if norm(body) not in hay:
                error(f"{rel}: snippet body no longer appears in {src}")
                continue
            lines = src_path.read_text().splitlines()
            window = norm("\n".join(lines[lo - 1: hi]))
            if norm(body) not in window:
                warn(f"{rel}: snippet drifted from {src}#L{lo}-L{hi} (present elsewhere in file)")


def check_figures() -> None:
    figdir = DOCS / "figures"
    manifest_path = figdir / "manifest.json"
    if not manifest_path.is_file():
        if any(figdir.glob("*.png")) or any(figdir.glob("*.svg")):
            error("docs/figures/manifest.json missing but figures exist")
        return
    manifest = json.loads(manifest_path.read_text())
    files = {p.name for p in figdir.glob("*.png")} | {p.name for p in figdir.glob("*.svg")}
    for name in files - set(manifest):
        error(f"docs/figures/{name}: no manifest entry (write it via save_fig)")
    for name in set(manifest) - files:
        error(f"manifest entry without figure file: {name}")
    referenced = set()
    for f in md_files():
        if is_entry(f, "worklog"):
            continue  # chronology names retired figures — not a live reference
        text = f.read_text()
        # Included galleries are live figures on the built page too. Resolve
        # their markup in the containing page's emitted link context.
        if _paths.is_topic_page(f, REPO):
            def include_fragment(match, depth=0):
                fragment = DOCS / "site" / match.group(1)
                if not fragment.is_file() or depth >= 8:  # the builder reports cycles and depth
                    return match.group(0)
                return re.sub(r"<!--\s*include:\s*(\S+)\s*-->", lambda m: include_fragment(m, depth + 1), fragment.read_text())
            text = re.sub(r"<!--\s*include:\s*(\S+)\s*-->", include_fragment, text)
        # Linked retained figures have a canonical doc reference too, even
        # when the page no longer embeds the full comparison.
        targets = re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", text)
        targets += re.findall(r'<img[^>]+src="([^"]+)"', text)  # raw-HTML figures (carousels)
        for target in targets:
            if "figures/" in target:
                if Path(target).suffix.lower() not in {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"}:
                    continue
                figure = resolve_path(markdown_origin(f).parent / target)
                if _paths.is_topic_page(f, REPO) and not figure.is_file():
                    # Page-body links use the emitted HTML location, as above.
                    figure = resolve_path(DOCS / "html" / target)
                if figure.parent == figdir.resolve():
                    referenced.add(figure.name)
                    # A vector figure's raster export shares its generator
                    # and is retained for previews/downloads, not a second plot.
                    if figure.suffix == ".svg":
                        raster = figure.with_suffix(".png").name
                        if (raster in manifest and figure.name in manifest
                                and manifest[figure.name].get("script")
                                and manifest[raster].get("script") == manifest[figure.name].get("script")):
                            referenced.add(raster)
                    continue
                # Experiments retain figures beside their own generated manifest.
                # A basename alone does not make them shared docs/figures assets.
                if re.match(r"https?://", target):
                    continue
                owned_manifest = figure.parent / "manifest.json"
                if not owned_manifest.is_file():
                    error(f"{f.relative_to(REPO)}: figure manifest missing: {target}")
                    continue
                entry = json.loads(owned_manifest.read_text()).get(figure.name)
                if entry is None:
                    error(f"{f.relative_to(REPO)}: figure absent from owned manifest: {target}")
                    continue
                script = entry.get("script", "")
                if script and not (REPO / script).is_file():
                    error(f"figure {target}: generator script missing: {script}")
    for name in referenced - set(manifest):
        error(f"figure referenced by docs but not in manifest: {name}")
    for name in set(manifest) - referenced:
        warn(f"figure in manifest referenced by no doc: {name}")
    for name, entry in manifest.items():
        script = entry.get("script", "")
        if script and not (REPO / script).is_file():
            error(f"manifest {name}: generator script missing: {script}")


MARKER_RE = re.compile(r"INVARIANT|DON'T-REDO")
MARKER_OK_RE = re.compile(r"\*\*(INVARIANT:|DON'T-REDO:)\*\*")


def check_markers(dump: bool = False) -> None:
    registry = []
    historical = set(evidence_document_locations().values())
    for f in sorted(DOCS.rglob("*.md")):
        if f in historical:
            continue  # Historical declarations are provenance, not current rules.
        rel = f.relative_to(REPO)
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if not MARKER_RE.search(line):
                continue
            if is_entry(f, "worklog") or is_entry(f, "open_work"):
                # declarations are banned here; prose MENTIONS of markers are fine
                if MARKER_OK_RE.search(line):
                    error(f"{rel}:{i}: INVARIANT/DON'T-REDO declarations belong on pages or class docs, not {f.name}")
                continue
            if MARKER_OK_RE.search(line):
                registry.append(f"{rel}:{i}: {line.strip()}")
            elif "**" in line and ("INVARIANT" in line or "DON'T-REDO" in line):
                warn(f"{rel}:{i}: marker-ish line not in **INVARIANT:** / **DON'T-REDO:** form")
    if dump:
        print("\n".join(registry) if registry else "(no markers)")
        print(f"\n{len(registry)} markers")


def check_open() -> None:
    f = entry_path("open_work")
    if f is None:
        return
    if not f.is_file():
        error(f"{f.relative_to(REPO)} missing")
        return
    text = f.read_text()
    if "~~" in text:
        error("OPEN.md: strikethrough found — delete finished lines instead")
    if re.search(r"- \[[xX ]\]", text):
        error("OPEN.md: checkbox found — items are plain bullets, deleted when done")
    if re.search(r"\bDONE\b", text):
        error("OPEN.md: 'DONE' marker found — finished items get deleted")
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("- ") and not re.search(r"\[[^\]]+\]\([^)]+\)", line):
            error(f"OPEN.md:{i}: bullet without an owning-doc link")


def check_worklog() -> None:
    f = entry_path("worklog")
    if f is None:
        return
    if not f.is_file():
        error(f'{f.relative_to(REPO)} missing')
        return
    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", f.read_text(), re.M)
    starts = [d[:10] for d in dates]
    if starts != sorted(starts, reverse=True):
        error("worklog.md: date sections are not newest-first")
    for i, line in enumerate(f.read_text().splitlines(), 1):
        if re.match(r"^- probed\b", line) and "→" not in line:
            error(f"worklog.md:{i}: probe line missing '→ verdict'")
        if re.match(r"^- \*\*", line) and not re.search(r"\b[0-9a-f]{7}\b", line):
            # landing bullets usually open with their hashes on the same line
            entry_ok = False
            # allow hash on the following 3 lines of the same entry
            lines = f.read_text().splitlines()
            for j in range(i, min(i + 3, len(lines))):
                if re.search(r"\b[0-9a-f]{7}\b", lines[j]):
                    entry_ok = True
                    break
            if not entry_ok:
                warn(f"worklog.md:{i}: landing without a commit hash nearby")


def check_tails() -> None:
    """A working-notes tail (below <!-- page-end -->) must be reachable:
    OPEN.md links into it, else it silently rots off the hosted page."""
    open_md = entry_path("open_work")
    open_text = open_md.read_text() if open_md is not None and open_md.is_file() else ""
    for f in _paths.topic_pages(REPO):
        if "<!-- page-end -->" not in f.read_text():
            continue
        if f.relative_to(DOCS).as_posix() not in open_text:
            warn(f"{f.relative_to(REPO)}: working-notes tail with no OPEN.md link into it")


def check_build() -> None:
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("build.py")), "--check"],
                       capture_output=True, text=True)
    if r.returncode == 2:
        error(".build/docs/html is stale — run `python .docs-kit/docsite.py build --project .`")
    elif r.returncode != 0:
        error(f"build.py --check failed:\n{r.stderr.strip()}")


def check_topic_structure() -> None:
    from topic_structure import topic_structure_problems
    found_errors, found_warnings = topic_structure_problems(REPO)
    errors.extend(found_errors)
    warnings.extend(found_warnings)


def record_change_notes(since: str | None) -> list[str]:
    """Reminders, never failures: pages that explain a changed record section."""
    from record_changes import record_change_notes as notes
    try:
        return notes(REPO, slugify, since)
    except ValueError as problem:
        error(str(problem))
        return []


def check_kit_pin() -> None:
    from kit_pin import unpublished_pin
    problem = unpublished_pin(Path(__file__).resolve().parents[1], REPO)
    if problem:
        error(problem)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="warnings fail the run")
    ap.add_argument("--registry", action="store_true", help="dump the INVARIANT/DON'T-REDO registry and exit")
    ap.add_argument("--since", metavar="REV",
                    help="list pages explaining record sections changed since REV (default: HEAD)")
    args = ap.parse_args()

    if args.registry:
        check_markers(dump=True)
        return 1 if errors else 0

    try:
        _evidence.verify(REPO, require_all_manifests=True)
        recorded_source_roots()
    except (ValueError, OSError) as problem:
        print(f"ERROR: evidence document verification failed: {problem}", file=sys.stderr)
        return 1
    check_md_links()
    check_html()
    check_snippets()
    check_figures()
    check_markers()
    check_open()
    check_worklog()
    check_tails()
    check_topic_structure()
    check_build()
    check_kit_pin()
    notes = record_change_notes(args.since)

    for w in warnings:
        print(f"WARN: {w}")
    for note in notes:
        print(note)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1
    print(f"lint clean ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
