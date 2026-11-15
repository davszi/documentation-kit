#!/usr/bin/env python3
"""Doc-system lint — run before pushing docs.

    python .docs-kit/docsite.py lint --project . [--strict] [--registry] [--since <rev>]

Checks (the shared guides under rules/ are the spec):
  1. markdown links + anchors resolve (docs/**, AGENTS.md, CLAUDE.md, README.md);
     worklog entries dated before `worklog_links_checked_from` are skipped
  2. built-html internal anchors + relative hrefs resolve; links to repository
     files, which the build marks with data-repo-path, must exist and a
     fragment into a Markdown file must match an anchor, `<a href>` in page
     bodies, included fragments and registered source pages included (errors;
     notes on automatically listed pages)
  3. snippet drift: fenced blocks tagged `source=<path>#L<a>-L<b>` must appear
     in their source file (error), at the stated lines (warning otherwise)
  4. figure manifest: files ↔ entries both ways, generator scripts exist,
     doc-referenced figures are in the manifest; unreferenced figure = warning
  5. INVARIANT / DON'T-REDO marker form (bold, colon); never in worklog/OPEN;
     fenced code blocks and code spans are skipped, as the build skips them
     (--registry dumps the marker registry and exits)
  6. OPEN.md format: every bullet links its owning doc; no strikethrough /
     checkboxes / DONE markers (lines get deleted, not struck)
  7. worklog format: ## YYYY-MM-DD sections newest-first; probe-line shape
  8. .build/docs/html freshness (`build.py --check`)
  9. built html loads no external resources (external <a> navigation is fine)
 10. the project's pinned kit commit is on a remote branch of the kit
 11. topic structure: each topic page, docs/topics/<topic>/index.md or one level
     deeper in a folder named by `topic_group_folders`, has a record beside it
     (another .md outside evidence/) or declares `page_only = "<reason>"`;
     an empty page_only is an error, an unneeded one a warning; home exempt
 12. capability map: site.toml sets `tooling_roots` (error); when it names a folder, the map exists
     and is tracked; every tracked file or folder directly under a tooling root
     is linked from its table; its generated Imported by column matches the Python
     imports (errors); a tooling module that imports from a folder under
     `experiment_roots` is a warning. The map's links are checked as in 1.
 13. slide faces in the built pages (`slide_face_checks.py`): a chapter with more
     than one face, a face that does not open its chapter and a face outside
     every chapter are errors; a number shown on a face and nowhere else in its
     chapter is a warning; a `data-face-only` mark that is unusable or no
     longer needed is a warning, and a usable one is a note
 14. formulas in the built pages (`formula_checks.py`): every formula on a page
     that loads the kit's KaTeX compiles with it, no formula is split by
     Markdown and none is left unclosed (errors). KaTeX runs in Node.js; without
     Node the check is a note, or an error when site.toml sets
     `formula_check_required = true`

Notes (never fail, not even under --strict): a changed record section
(working tree vs HEAD, or vs --since <rev>) lists the topic pages that link
it, so someone rereads them.
A topic page also gets a note for each number in its prose that none of its
linked records state; values shown as code are not checked.
A link to a file that the local-artifact manifest lists under `omitted_files`
gets a note when the file is absent: the project declared that state.
Each problem the build tolerated in an automatically listed reference page
(see `reference_listing` in site.toml) is a note too.
A number that a project accepts on one slide face with `data-face-only` is a
note that names the number and the reason.
A formula check skipped because Node.js is missing is a note, unless the
project requires the check.

Exit 0 clean (warnings print unless --strict fails them), 1 on errors.
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

REPO = Path(os.environ.get("DOCSITE_PROJECT_ROOT", Path.cwd())).resolve()
DOCS = REPO / "docs"

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


notices: list[str] = []


def notice(msg: str) -> None:
    """A declared state worth showing; it never fails, not even under --strict."""
    notices.append(msg)


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


def resolve_path(path: Path) -> Path:
    """Resolve the logical `docs/html/` origin to the build output."""
    return _paths.resolve_site_path(path, root=REPO)


import worklog_entries as _worklog_entries


def md_files() -> list[Path]:
    files = set(DOCS.rglob("*.md"))
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
    # The capability map's links are checked wherever the project keeps it.
    from capability_map import settings as capability_settings
    try:
        capability = capability_settings(site)
    except ValueError:
        capability = None  # the build reports the setting
    if capability is not None and (REPO / capability["map"]).is_file():
        files.add(REPO / capability["map"])
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
        if is_entry(f, "worklog"):
            text = link_checked_worklog_text(text)
        chunks = [(text, f.parent)]
        if _paths.is_topic_page(f, REPO):
            page, _, tail = text.partition("<!-- page-end -->")
            chunks = [(page, DOCS / "html"), (tail, f.parent)]
        for chunk, base in chunks:
            _check_chunk_links(f, chunk, base)


# (source file, resolved target, fragment) of every Markdown link checked above.
markdown_checked: set[tuple[Path, Path, str]] = set()

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
    relative = _worklog_entries.configured_entry(site, key)
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


def worklog_links_checked_from() -> str | None:
    """The date of the oldest worklog entry whose links are still checked.

    A project sets `worklog_links_checked_from = "YYYY-MM-DD"` in
    docs/site/site.toml. Entries are append-only, so a link in an older entry
    cannot follow a later move or removal of its target. The build rejects a
    value that is not a date, and lint prints the build's error.
    """
    if "links_from" not in _entry_cache:
        config = REPO / 'docs/site/site.toml'
        site = tomllib.loads(config.read_text()) if config.is_file() else {}
        try:
            value = _worklog_entries.links_checked_from(site)
        except ValueError:
            value = None
        _entry_cache["links_from"] = value
    return _entry_cache["links_from"]


def link_checked_worklog_text(text: str) -> str:
    """The worklog without the dated entries older than the configured date.

    Text before the first dated heading is always kept. Any other `## ` section
    belongs to the dated heading above it.
    """
    kept, position = [], 0
    for start, end in _worklog_entries.unchecked_spans(text, worklog_links_checked_from()):
        kept.append(text[position:start])
        position = end
    kept.append(text[position:])
    return "".join(kept)


def _check_chunk_links(f: Path, text: str, base: Path) -> None:
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
            dest = resolve_path(base / path_part)
            # The built page carries this link as a source link too; the HTML
            # source-link check leaves it to this check.
            markdown_checked.add((f, dest, unquote(frag)))
            if not dest.exists():
                if retained_locally(dest):
                    notice(f"{rel}: artifact retained locally, omitted from push: {target}")
                else:
                    error(f"{rel}: dead link {target}")
                continue
            if frag and dest.suffix == ".md" and frag not in md_anchors(dest):
                error(f"{rel}: anchor #{frag} not found in {path_part}")
            if frag and dest.suffix == ".html" and frag not in html_ids(dest):
                error(f"{rel}: anchor #{frag} not found in {path_part}")


SOURCE_LINK_RE = re.compile(r'<a\b[^>]*?\sdata-repo-path="([^"]*)"\s+data-repo-fragment="([^"]*)"[^>]*>', re.I)


def built_page_sources() -> tuple[dict[str, str], set[str], set[str]]:
    """Built page name to its source, the registered sources and the automatic ones."""
    from topic_structure import page_sources
    names = page_sources(REPO)
    config = DOCS / "site" / "site.toml"
    site = tomllib.loads(config.read_text()) if config.is_file() else {}
    entries = site.get("source_pages", []) if isinstance(site.get("source_pages"), list) else []
    registered = {entry["source"] for entry in entries if isinstance(entry, dict) and isinstance(entry.get("source"), str)}
    try:
        listed = set(json.loads((resolve_path(DOCS / "html").parent / "site-build.json").read_text())["source_pages"].values())
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        listed = set()
    return names, registered, listed - registered


def check_source_links() -> None:
    """Links in built pages to repository files, `<a href>` in a page body included.

    The build resolves every such link and marks it with `data-repo-path`, the
    repository file it found, and `data-repo-fragment`, with a source remote and
    without one. This check reads those marks, so it uses the build's own
    resolution: the target must exist, and a fragment into a Markdown file must
    match one of its anchors, as for a Markdown link. It covers topic pages, the
    fragments they include and registered source pages; links that the Markdown
    check already checked in the same source are left to it. On an
    automatically listed page a problem is a note. Links in worklog entries
    dated before `worklog_links_checked_from` are not checked.
    """
    names, registered, automatic = built_page_sources()
    worklog = entry_path("worklog")
    for f in sorted(resolve_path(DOCS / "html").glob("*.html")):
        source = names.get(f.name)
        source_path = REPO / source if source else None
        label = f"{source} ({f.name})" if source else f.relative_to(REPO).as_posix()
        report = notice if source in automatic else error
        markup = f.read_text()
        old = []
        if source_path is not None and worklog is not None and source_path == worklog:
            old = _worklog_entries.unchecked_spans(markup, worklog_links_checked_from(),
                                                   _worklog_entries.HTML_HEADING)
        seen = set()
        for match in SOURCE_LINK_RE.finditer(markup):
            if _worklog_entries.within(old, match.start()):
                continue
            path = html.unescape(match[1])
            fragment = unquote(html.unescape(match[2]))
            dest = REPO / path
            if (source_path, dest, fragment) in markdown_checked or (path, fragment) in seen:
                continue
            seen.add((path, fragment))
            shown = path + ("#" + fragment if fragment else "")
            if not dest.exists():
                if retained_locally(dest):
                    notice(f"{label}: artifact retained locally, omitted from push: {shown}")
                else:
                    report(f"{label}: dead link to repository file {shown}")
            elif fragment and dest.suffix == ".md" and fragment not in md_anchors(dest):
                report(f"{label}: anchor #{fragment} not found in {path}")
            elif fragment and dest.suffix == ".html" and fragment not in html_ids(dest):
                report(f"{label}: anchor #{fragment} not found in {path}")


def check_html() -> None:
    for f in sorted(resolve_path(DOCS / "html").glob("*.html")):
        text = f.read_text()
        ids = html_ids(f)
        rel = f.relative_to(REPO)
        # Source links are checked by check_source_links from the build's marks.
        source_links = [(m.start(), m.end()) for m in SOURCE_LINK_RE.finditer(text)]
        for m in re.finditer(r'href="([^"]+)"', text):
            if _worklog_entries.within(source_links, m.start()):
                continue
            href = m.group(1)
            if href.startswith(("http://", "https://", "//", "mailto:", "vscode:")):
                continue
            path_part, _, frag = href.partition("#")
            path_part = path_part.partition("?")[0]
            if not path_part:
                if frag and frag not in ids:
                    error(f"{rel}: dead internal anchor #{frag}")
                continue
            if not resolve_path(DOCS / "html" / path_part).exists():
                if retained_locally(resolve_path(DOCS / "html" / path_part)):
                    notice(f"{rel}: artifact retained locally, omitted from push: {href}")
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
                            notice(f"{rel}: artifact retained locally, omitted from push: {target}")
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
                src_path = resolve_path(f.parent / src)
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
                figure = resolve_path(f.parent / target)
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


CODE_SPAN_RE = re.compile(r"(`+)[^\n]*?\1")


def without_code(text: str) -> str:
    """The text with fenced code blocks and code spans blanked, lines kept.

    The build converts no marker inside a fenced block, so a marker there, or
    in a code span, is an example: neither listed nor warned about.
    """
    for start, end in reversed(_worklog_entries.fenced_spans(text)):
        text = text[:start] + re.sub(r"[^\n]", "", text[start:end]) + text[end:]
    return CODE_SPAN_RE.sub("", text)


def check_markers(dump: bool = False) -> None:
    registry = []
    for f in sorted(DOCS.rglob("*.md")):
        rel = f.relative_to(REPO)
        raw_lines = f.read_text().splitlines()
        for i, line in enumerate(without_code("\n".join(raw_lines)).split("\n"), 1):
            if not MARKER_RE.search(line):
                continue
            if is_entry(f, "worklog") or is_entry(f, "open_work"):
                # declarations are banned here; prose MENTIONS of markers are fine
                if MARKER_OK_RE.search(line):
                    error(f"{rel}:{i}: INVARIANT/DON'T-REDO declarations belong on pages or class docs, not {f.name}")
                continue
            if MARKER_OK_RE.search(line):
                registry.append(f"{rel}:{i}: {raw_lines[i - 1].strip()}")
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
    starts = _worklog_entries.markdown_entry_dates(f.read_text())
    if starts != sorted(starts, reverse=True):
        error("worklog.md: date sections are not newest-first")
    for i, line in enumerate(f.read_text().splitlines(), 1):
        if re.match(r"^- probed\b", line) and "→" not in line:
            error(f"worklog.md:{i}: probe line missing '→ verdict'")


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
    # A configuration error also exits with 2; it is reported as a failure, not as staleness.
    if r.returncode == 2 and "build.py: error:" not in r.stderr:
        error(".build/docs/html is stale — run `python .docs-kit/docsite.py build --project .`")
    elif r.returncode != 0:
        error(f"build.py --check failed:\n{r.stderr.strip()}")
    # What automatically listed reference pages tolerated; notes never fail.
    for line in r.stdout.splitlines():
        if line.startswith("NOTE: "):
            notice(line[len("NOTE: "):])


def check_topic_structure() -> None:
    from topic_structure import topic_structure_problems, undeclared_nested_pages
    found_errors, found_warnings = topic_structure_problems(REPO)
    for note in undeclared_nested_pages(REPO):
        notice(note)
    errors.extend(found_errors)
    warnings.extend(found_warnings)


def check_capability_map() -> None:
    from capability_map import check
    found_errors, found_warnings = check(REPO)
    errors.extend(found_errors)
    warnings.extend(found_warnings)


def check_slide_faces() -> None:
    from slide_face_checks import check
    found_errors, found_warnings, found_notes, _ = check(REPO)
    errors.extend(found_errors)
    warnings.extend(found_warnings)
    for note in found_notes:
        notice(note)


summaries: list[str] = []


def check_formulas() -> None:
    from formula_checks import check
    from topic_structure import page_sources
    config = DOCS / "site" / "site.toml"
    site = tomllib.loads(config.read_text()) if config.is_file() else {}
    found_errors, found_notes, summary = check(REPO, site, resolve_path(DOCS / "html"), page_sources(REPO))
    errors.extend(found_errors)
    for note in found_notes:
        notice(note)
    if summary:
        summaries.append(summary)


def record_change_notes(since: str | None) -> list[str]:
    """Reminders, never failures: pages that explain a changed record section."""
    from record_changes import record_change_notes as notes
    try:
        return notes(REPO, slugify, since)
    except ValueError as problem:
        error(str(problem))
        return []


def page_number_notes() -> list[str]:
    """Reminders, never failures: page numbers that no linked record states."""
    from page_numbers import page_number_notes as notes
    return notes(REPO, slugify)


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

    check_md_links()
    check_source_links()
    check_html()
    check_snippets()
    check_figures()
    check_markers()
    check_open()
    check_worklog()
    check_tails()
    check_topic_structure()
    check_capability_map()
    check_build()
    check_slide_faces()
    check_formulas()
    check_kit_pin()
    notes = record_change_notes(args.since) + page_number_notes()

    for w in warnings:
        print(f"WARN: {w}")
    for n in notices:
        print(f"NOTE: {n}")
    for note in notes:
        print(note)
    for summary in summaries:
        print(summary)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1
    print(f"lint clean ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
