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

from topic_structure import is_topic_page, topic_group_folders
from worklog_entries import HTML_HEADING, unchecked_spans, within

SOURCE_KEYS = {"source", "slug", "title", "description", "math", "reader", "pinned"}
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
    pinned: bool         # listed first in the sidebar's repository section

    @property
    def route(self) -> str:
        return self.slug + ".html"


def load_registry(site: dict, root: Path, tracked: frozenset[Path]) -> tuple[list[SourcePage], list[str]]:
    """Validate `[[source_pages]]`; return the pages and every problem found."""
    entries = site.get("source_pages", [])
    problems: list[str] = []
    topic_groups = topic_group_folders(root)
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
        types = {"source": str, "slug": str, "title": str, "description": str, "math": bool, "reader": bool,
                 "pinned": bool}
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
        if is_topic_page(root / relative, root, topic_groups):
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
                                entry.get("math", False), entry.get("reader", False), entry.get("pinned", False)))
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


LINK_GONE = '<span class="link-gone" title="The target of this link no longer exists.">'
_GONE = "\x00link-gone\x00"
_ALT = re.compile(r'(?<![\w-])alt="([^"]*)"')


def rewrite_links(markup: str, page: SourcePage, routes: dict[str, str], root: Path,
                  exists, links_checked_from: str | None = None) -> tuple[str, list[str], set[str]]:
    """Resolve relative link/media targets from the source file's own folder.

    Registered sources become `<route>#fragment`; other repository paths become
    the logical `docs/html/` URL the site bundle already understands. Returns
    the markup, any containment or missing-target problems, and the link
    targets whose fragments are not checked.

    `links_checked_from` is given for the project's worklog only. In an entry
    dated before it, a link or image whose target is gone renders as its text
    inside `LINK_GONE` instead of failing the build, and a link that appears
    only in such entries keeps its fragment unchecked.
    """
    problems: list[str] = []
    folder = posixpath.dirname(page.source)
    unchecked = unchecked_spans(markup, links_checked_from, HTML_HEADING)
    old_hrefs: set[str] = set()
    new_hrefs: set[str] = set()

    def resolve(raw: str, old: bool) -> str | None:
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
            if old:
                return _GONE
            problems.append(f"{page.source}: link target not found: {raw}")
            return None
        logical = posixpath.relpath(target, "docs/html")
        if url.path.endswith("/") and not logical.endswith("/"):
            logical += "/"
        return quote(logical, safe="/-_.~") + suffix

    def tag(match: re.Match) -> str:
        original = match[0]
        name = match[1].lower()
        old = within(unchecked, match.start())
        updated = original
        for attribute, raw in _ATTR.findall(original):
            replacement = resolve(raw, old)
            if replacement == _GONE and name in {"a", "img"}:
                if name == "a":
                    return _GONE  # the closing </a> becomes </span> below
                alt = _ALT.search(original)
                return LINK_GONE + (alt[1] if alt else raw) + "</span>"
            if replacement == _GONE:  # other media keep failing the build
                problems.append(f"{page.source}: link target not found: {raw}")
                replacement = None
            href = raw
            if replacement is not None:
                href = html.escape(replacement, quote=True)
                updated = updated.replace(f'{attribute}="{raw}"', f'{attribute}="{href}"', 1)
            if name == "a" and attribute == "href":
                (old_hrefs if old else new_hrefs).add(href)
        return updated

    markup = _TAG.sub(tag, markup)
    markup = re.sub(re.escape(_GONE) + r"(.*?)</a>", lambda m: LINK_GONE + m[1] + "</span>", markup, flags=re.S)
    return markup, problems, old_hrefs - new_hrefs


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


_H1 = re.compile(r"<h1\b[^>]*>.*?</h1>\s*", re.S)
_H2 = re.compile(r"<h2\b[^>]*>.*?</h2>\s*", re.S)
SHORT_INTRODUCTION = 600


def merge_short_introduction(markup: str) -> str:
    """Move a short opening (source line plus a few sentences) into the first chapter.

    The chapter reader keeps text before the first second-level heading as its
    own chapter. A registered file usually opens with one or two sentences, which
    would leave a nearly empty card, so a short opening joins the first chapter.
    A longer opening, or one with its own figures or subheadings, stays separate.
    """
    first = _H2.search(markup)
    if not first:
        return markup
    title = _H1.search(markup, 0, first.start())
    heading = markup[title.start():title.end()] if title else ""
    opening = (markup[:title.start()] + markup[title.end():first.start()]) if title else markup[:first.start()]
    text = html.unescape(re.sub(r"<[^>]+>", "", opening)).strip()
    if not text or len(text) > SHORT_INTRODUCTION or re.search(r"<(h3|figure|img|table|svg)\b", opening):
        return markup
    return heading + markup[first.start():first.end()] + opening + markup[first.end():]


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


def fragment_problems(pages: dict[str, str], sources: set[str], targets: set[str],
                      unchecked: dict[str, set[str]] | None = None) -> list[str]:
    """Missing anchors in links between generated pages.

    `pages` maps public file names (`git.html`) to rendered markup. Links from
    every page in `sources` into a page in `targets` are verified; a link
    without a file name targets its own page. `unchecked` maps a page to the
    link targets it does not verify: the worklog's links that appear only in
    entries dated before `worklog_links_checked_from`.
    """
    identifiers = {name: set(_ID.findall(markup)) for name, markup in pages.items()}
    problems = []
    for name in sorted(sources & set(pages)):
        skipped = (unchecked or {}).get(name, set())
        for target, fragment in _FRAGMENT_LINK.findall(pages[name]):
            if f"{target}#{fragment}" in skipped:
                continue
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
