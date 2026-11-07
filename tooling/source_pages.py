"""Render registered repository Markdown files as whole-file site pages.

A project registers an existing, tracked Markdown file under a public route:

    [[source_pages]]
    source = "rules/engineering/git.md"
    slug = "git"

The file stays the single editable source. Its relative links and media resolve
from the file's own folder: links to other registered files become their HTML
routes, and every other repository link becomes the logical generated-site path
that the bundle turns into a source link or packaged media. Fragments into
registered routes are checked against the rendered target page.
"""
from __future__ import annotations

from dataclasses import dataclass
import html
import os
from pathlib import Path
import posixpath
import re
from urllib.parse import quote, unquote, urlsplit

SOURCE_KEYS = {"source", "slug", "title", "description", "math", "reader"}
_SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
_TAG = re.compile(r"<(a|img|video|audio|source|iframe)\b[^>]*>", re.I)
_ATTR = re.compile(r'(?<![\w-])(href|src|poster)="([^"]*)"')
_HEADING = re.compile(r'<h([23]) id="([^"]+)">(.*?)</h\1>', re.S)
_FENCE = re.compile(r"^(```|~~~)")


@dataclass(frozen=True)
class SourcePage:
    source: str          # repository-relative POSIX path of the Markdown file
    slug: str
    title: str | None
    description: str | None
    math: bool
    reader: bool

    @property
    def route(self) -> str:
        return self.slug + ".html"


def load_registry(site: dict, root: Path, tracked: frozenset[Path]) -> tuple[list[SourcePage], list[str]]:
    """Validate `[[source_pages]]`; return the pages and every problem found."""
    entries = site.get("source_pages", [])
    problems: list[str] = []
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        return [], ["site.toml: source_pages must be a list of [[source_pages]] tables"]
    pages: list[SourcePage] = []
    seen_sources: dict[str, str] = {}
    for entry in entries:
        label = entry.get("source", "?")
        unknown = sorted(set(entry) - SOURCE_KEYS)
        if unknown or not {"source", "slug"} <= set(entry):
            problems.append(f"site.toml [[source_pages]] {label}: unknown keys {unknown} or missing source/slug")
            continue
        types = {"source": str, "slug": str, "title": str, "description": str, "math": bool, "reader": bool}
        wrong = sorted(key for key, value in entry.items() if not isinstance(value, types[key]))
        if wrong:
            problems.append(f"site.toml [[source_pages]] {label}: wrong value types for {wrong}")
            continue
        source, slug = entry["source"], entry["slug"]
        if not _SLUG.fullmatch(slug):
            problems.append(f"source page {source}: slug must be a lowercase filename stem without directories")
            continue
        for key in ("title", "description"):
            if key in entry and not entry[key].strip():
                problems.append(f"source page {source}: {key} must be a non-empty string")
        relative = Path(source)
        if (relative.is_absolute() or "\\" in source or relative.as_posix() != source
                or ".." in relative.parts or relative.suffix != ".md"):
            problems.append(f"source page {source}: source must be a contained relative .md path")
            continue
        path = root / relative
        if (any(parent.is_symlink() for parent in (path, *path.parents) if parent.is_relative_to(root))
                or not path.resolve().is_relative_to(root)):
            problems.append(f"source page {source}: source escapes the project through a symlink")
            continue
        if path not in tracked or not path.is_file():
            problems.append(f"source page {source}: source must be a tracked file")
            continue
        if relative.parts[:2] == ("docs", "topics") and len(relative.parts) == 4 and relative.name == "index.md":
            problems.append(f"source page {source}: topic entry pages render through their own frontmatter")
            continue
        if path.read_text().startswith("+++\n"):
            problems.append(f"source page {source}: registered sources are plain Markdown without +++ frontmatter")
            continue
        if source in seen_sources:
            problems.append(f"source page {source}: registered twice ({seen_sources[source]}, {slug})")
            continue
        seen_sources[source] = slug
        pages.append(SourcePage(source, slug, entry.get("title"), entry.get("description"),
                                entry.get("math", False), entry.get("reader", False)))
    return pages, problems


def first_heading(text: str) -> str | None:
    """The first level-one ATX heading outside fenced code."""
    fenced = False
    for line in text.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("# "):
            return re.sub(r"\s*\{#[^}]*\}\s*$", "", line[2:]).strip()
    return None


def rewrite_links(markup: str, page: SourcePage, routes: dict[str, str], root: Path,
                  exists) -> tuple[str, list[str]]:
    """Resolve relative link/media targets from the source file's own folder.

    Registered sources become `<route>#fragment`; other repository paths become
    the logical `docs/html/` URL the site bundle already understands. Returns
    the markup and any containment or missing-target problems.
    """
    problems: list[str] = []
    folder = posixpath.dirname(page.source)

    def resolve(raw: str) -> str | None:
        url = urlsplit(html.unescape(raw))
        if url.scheme or url.netloc or not url.path:
            return None  # external, same-page fragment or empty
        if url.path.startswith("/"):
            problems.append(f"{page.source}: absolute link {raw}; use a path relative to the source file")
            return None
        target = posixpath.normpath(posixpath.join(folder, unquote(url.path)))
        if target == ".." or target.startswith("../"):
            problems.append(f"{page.source}: link escapes the repository: {raw}")
            return None
        suffix = ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")
        if target in routes:
            return routes[target] + suffix
        if not exists(root / target):
            problems.append(f"{page.source}: link target not found: {raw}")
            return None
        logical = posixpath.relpath(target, "docs/html")
        if url.path.endswith("/") and not logical.endswith("/"):
            logical += "/"
        return quote(logical, safe="/-_.~") + suffix

    def tag(match: re.Match) -> str:
        original = match[0]
        updated = original
        for attribute, raw in _ATTR.findall(original):
            replacement = resolve(raw)
            if replacement is not None:
                updated = updated.replace(f'{attribute}="{raw}"',
                                          f'{attribute}="{html.escape(replacement, quote=True)}"', 1)
        return updated

    return _TAG.sub(tag, markup), problems


def table_of_contents(markup: str) -> list[list[str]]:
    """Sidebar entries for a scrolling page: second-level headings, third-level as subentries."""
    entries = []
    for level, identifier, inner in _HEADING.findall(markup):
        text = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        entries.append([("-" if level == "3" else "") + text, "#" + identifier])
    return entries


def origin_banner(page: SourcePage, repository: str, edit_ref: str) -> str:
    """Name the canonical source and offer its edit page; the source link is rewritten by the bundle."""
    logical = quote(posixpath.relpath(page.source, "docs/html"), safe="/-_.~")
    links = [f'<a class="source-origin-path" href="{logical}"><code>{html.escape(page.source)}</code></a>']
    if repository:
        edit = (repository.rstrip("/") + "/edit/" + quote(edit_ref, safe="") + "/"
                + quote(page.source, safe="/-_.~"))
        links.append(f'<a class="source-origin-edit" href="{html.escape(edit, quote=True)}">Edit source</a>')
    return ('<p class="source-origin" data-source-page="' + html.escape(page.source, quote=True) + '">'
            '<span class="source-origin-label">Canonical source</span> ' + " · ".join(links) + "</p>\n")


_TABLE = re.compile(r"<table>(.*?)</table>", re.S)


def wrap_tables(markup: str) -> str:
    """Give each table a labelled, keyboard-scrollable region so narrow screens scroll it in place."""
    def wrap(match: re.Match) -> str:
        header = re.search(r"<thead>(.*?)</thead>", match[1], re.S)
        cells = [html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()
                 for cell in re.findall(r"<th[^>]*>(.*?)</th>", header[1] if header else "", re.S)]
        label = "Table: " + ", ".join(cell for cell in cells if cell) if any(cells) else "Table"
        return ('<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="'
                + html.escape(label, quote=True) + '">' + match[0] + "</div>")
    return _TABLE.sub(wrap, markup)


_ID = re.compile(r'\bid="([^"]+)"')
_FRAGMENT_LINK = re.compile(r'<a\b[^>]*?\bhref="([a-z0-9][a-z0-9-]*\.html)?#([^"]+)"', re.I)


def fragment_problems(pages: dict[str, str], sources: set[str], targets: set[str]) -> list[str]:
    """Missing anchors in links between generated pages.

    `pages` maps public file names (`git.html`) to rendered markup. Links from
    every page in `sources` into a page in `targets` are verified; a link
    without a file name targets its own page.
    """
    identifiers = {name: set(_ID.findall(markup)) for name, markup in pages.items()}
    problems = []
    for name in sorted(sources & set(pages)):
        for target, fragment in _FRAGMENT_LINK.findall(pages[name]):
            destination = target or name
            if destination not in identifiers or destination not in targets:
                continue  # an unbuilt route is reported by the resource checks
            if html.unescape(unquote(fragment)) not in identifiers[destination]:
                problems.append(f"{name}: anchor #{fragment} not found in {destination}")
    return problems


def exists_in(root: Path, resolver):
    """Existence test honoring the project's legacy path resolver."""
    def exists(path: Path) -> bool:
        return os.path.lexists(path) or os.path.lexists(resolver(path, root=root))
    return exists
