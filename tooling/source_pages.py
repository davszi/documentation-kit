"""Render registered repository Markdown files as whole-file site pages.

A project registers an existing, tracked Markdown file under a public route:

    [[source_pages]]
    source = "rules/engineering/git.md"
    slug = "git"

By default every other tracked Markdown file is listed too, under a route
derived from its path (`automatic_pages`). `reference_listing = false` in
site.toml turns that off; `reference_exclude` skips files by repository-relative glob.
An automatically listed page never fails the build: what a registered page
would reject is rendered tolerantly and returned as a note. Its raw HTML keeps
only the tags and attributes of `ADMITTED_HTML` (`ListedHtml`).

The file stays the single editable source. Its relative links and media resolve
from the file's own folder: links to other registered files become their HTML
routes, and every other repository link becomes the logical generated-site path
that the bundle turns into a source link or packaged media. Fragments into
registered routes are checked against the rendered target page.
"""
from __future__ import annotations

from bisect import bisect
from collections import Counter
from dataclasses import dataclass
import hashlib
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
    automatic: bool = False  # listed by `reference_listing`, not by a [[source_pages]] table

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


REFERENCE_ERROR = "site.toml: reference_listing must be true or false"
EXCLUDE_ERROR = ('site.toml: reference_exclude must list distinct repository-relative glob patterns, '
                 'such as "experiments/**" or "**/drafts/*.md"')


def reference_settings(site: dict) -> tuple[bool, tuple[str, ...]]:
    """`reference_listing` (default true) and `reference_exclude` (default empty); ValueError when invalid."""
    enabled = site.get("reference_listing", True)
    if not isinstance(enabled, bool):
        raise ValueError(REFERENCE_ERROR)
    patterns = site.get("reference_exclude", [])
    if (not isinstance(patterns, list) or any(not isinstance(pattern, str) for pattern in patterns)
            or len(set(patterns)) != len(patterns)):
        raise ValueError(EXCLUDE_ERROR)
    for pattern in patterns:
        if (not pattern.strip() or pattern != pattern.strip() or pattern.startswith("/") or "\\" in pattern
                or any(part in {"", ".", ".."} for part in pattern.rstrip("/").split("/"))):
            raise ValueError(f"site.toml: reference_exclude pattern {pattern!r} must be a repository-relative "
                             'glob without a leading slash, backslashes, "." or ".." parts, such as "experiments/**"')
        try:
            glob_regex(pattern)
        except re.error as problem:
            raise ValueError(f"site.toml: reference_exclude pattern {pattern!r} is not a valid glob ({problem}); "
                             'write a character class in order, such as "[a-z]"') from None
    return enabled, tuple(patterns)


def glob_regex(pattern: str) -> re.Pattern:
    """A repository-relative glob as a regular expression over a whole POSIX path.

    `*` and `?` stay inside one path segment, `[...]` is a character class,
    `**` spans any number of segments and a pattern ending in `/` matches
    everything below that folder.
    """
    if pattern.endswith("/"):
        pattern += "**"
    out, index = [], 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            out.append("(?:[^/]*/)*")
            index += 3
        elif pattern.startswith("**", index):
            out.append(".*")
            index += 2
        elif pattern[index] == "*":
            out.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            out.append("[^/]")
            index += 1
        elif pattern[index] == "[" and "]" in pattern[index + 2:]:
            end = pattern.index("]", index + 2)
            body = pattern[index + 1:end]
            negate = body.startswith("!")
            body = body[1:] if negate else body
            out.append("(?!/)[" + ("^" if negate else "") + body.replace("\\", "\\\\").replace("^", "\\^") + "]")
            index = end + 1
        else:
            out.append(re.escape(pattern[index]))
            index += 1
    return re.compile("".join(out))


_SEGMENT_RUN = re.compile(r"[^a-z0-9_-]+")
MAX_ROUTE_BASE = 180


def automatic_route_base(source: str) -> tuple[str, bool]:
    """The route base of an automatically listed file and whether it is lossless.

    Each path segment is lowercased and every run of characters other than
    `a-z`, `0-9`, `_` and `-` becomes one `-`; segments join with `.` and the
    `.md` suffix stays: `docs/Design Notes/API.md` becomes
    `docs.design-notes.api.md`. The base is lossless when the path already has
    that form, so no other path can have the same base.
    """
    parts = source[:-len(".md")].split("/")
    segments = [_SEGMENT_RUN.sub("-", part.lower()) for part in parts]
    base = ".".join(segments) + ".md"
    return base, segments == parts


def _hashed(base: str, source: str) -> str:
    digest = hashlib.sha256(source.encode()).hexdigest()[:8]
    return base[:-len(".md")][:MAX_ROUTE_BASE] + "-" + digest + ".md"


def read_source(path: Path) -> tuple[str, bool]:
    """The file's text, and whether bytes that are not UTF-8 were replaced.

    U+0000 becomes U+FFFD, as CommonMark asks; `ListedHtml` marks tags with it.
    """
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
        replaced = False
    except UnicodeDecodeError:
        text = data.decode("utf-8", errors="replace")
        replaced = True
    return text.removeprefix("﻿").replace("\x00", "\ufffd"), replaced


def automatic_pages(site: dict, root: Path, tracked: frozenset[Path], explicit: list[SourcePage],
                    taken_routes: set[str], kit_root: Path | None = None) -> tuple[list[SourcePage], list[str]]:
    """Every tracked Markdown file a [[source_pages]] table does not register.

    Skipped: files inside a submodule or the kit, files in a folder or with a
    name that starts with a dot, topic entry pages, files that start with `+++`
    frontmatter, symlinked files, files matching `reference_exclude` and files
    that `[publication] private_prefixes` or `private_suffixes` mark private.
    Returns the pages, in path order, and notes about what was tolerated.
    Settings must have passed `reference_settings`.
    """
    enabled, patterns = reference_settings(site)
    if not enabled:
        return [], []
    excludes = [glob_regex(pattern) for pattern in patterns]
    publication = site.get("publication") if isinstance(site.get("publication"), dict) else {}
    prefixes, suffixes = (tuple(value for value in publication.get(key, []) if isinstance(value, str) and value)
                          if isinstance(publication.get(key, []), list) else ()
                          for key in ("private_prefixes", "private_suffixes"))
    registered = {page.source for page in explicit}
    groups = topic_group_folders(root)
    kit = kit_root.resolve() if kit_root is not None else None
    candidates: list[tuple[str, str, str | None, bool]] = []
    notes: list[str] = []
    for path in sorted(tracked):
        if path.suffix != ".md" or not path.is_relative_to(root):
            continue
        source = path.relative_to(root).as_posix()
        if source in registered or any(parent in tracked for parent in path.parents):
            continue  # a tracked parent is a gitlink: the file belongs to a submodule
        if kit is not None and kit != root and path.is_relative_to(kit):
            continue
        if any(part.startswith(".") for part in source.split("/")):
            continue  # .github/, .claude/ and other dot folders hold tool files, not records
        if (any(pattern.fullmatch(source) for pattern in excludes) or source.startswith(prefixes)
                or source.endswith(suffixes)):
            continue
        if (any(parent.is_symlink() for parent in (path, *path.parents) if parent.is_relative_to(root) and parent != root)
                or not path.is_file() or is_topic_page(path, root, groups)):
            continue
        text, replaced = read_source(path)
        if text.startswith(("+++\n", "+++\r\n")):
            continue
        if replaced:
            notes.append(f"{source}: not valid UTF-8; undecodable bytes are shown as �")
        title = first_heading(text)
        if not title:
            title = path.name[:-len(".md")] or path.name
            notes.append(f"{source}: no level-one heading; the title is the file name")
        candidates.append((source, *automatic_route_base(source), title))
    claims: dict[str, list[str]] = {}
    for source, base, _, _ in candidates:
        claims.setdefault(base, []).append(source)
    pages = []
    for source, base, lossless, title in candidates:
        rivals = [other for other in claims[base] if other != source]
        if base + ".html" in taken_routes or (rivals and not lossless):
            # A lossless path keeps its plain route against every other file,
            # and at most one path is lossless per base. The others, and a file
            # that meets a topic or registered route, take a hash of their path.
            hashed = _hashed(base, source)
            notes.append(f"{source}: route {base}.html is also claimed by "
                         f"{', '.join(rivals) or 'a topic or registered page'}; "
                         f"this file is published as {hashed}.html")
            base = hashed
        elif len(base) > MAX_ROUTE_BASE + len(".md"):
            base = _hashed(base, source)
        pages.append(SourcePage(source, base, title, None, False, False, False, automatic=True))
    return pages, notes


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
# Schemes that lint and the browser accept on a link from an automatic page.
LINK_SCHEMES = {"http", "https", "mailto", "vscode"}
_C0_OR_SPACE = "".join(map(chr, range(0x21)))
_SCHEME = re.compile(r"([A-Za-z][A-Za-z0-9+.-]*):")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
# The only media an automatically listed file shows: raster images, as files or
# data: addresses. Any other file it named, SVG and HTML included, would be
# published under _media/ and run its own script when opened at its address.
RASTER_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"})
_RASTER_DATA = re.compile(r"data:image/(?:png|jpeg|gif|webp|avif)[;,]", re.I)
RASTER_NOTE = "is not a PNG, JPEG, GIF, WebP or AVIF image; shown as text"


def raster_image(path: Path) -> bool:
    """Whether a file is a raster image by both its suffix and its first bytes, so
    that no other content is published under an image name, where a host that
    sends no media type could let a browser read it as a page."""
    if path.suffix.lower() not in RASTER_SUFFIXES:
        return False
    try:
        with path.open("rb") as file:
            head = file.read(32)
    except OSError:
        return False
    return (head.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF87a", b"GIF89a"))
            or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")
            or (head[4:8] == b"ftyp" and any(brand in head[8:32] for brand in (b"avif", b"avis"))))


def _visible(raw: str) -> str:
    """An address for a message, with control characters such as a tab written as `\\x09`."""
    return _CONTROL.sub(lambda match: f"\\x{ord(match[0]):02x}", raw)


def browser_address(value: str) -> tuple[str, str | None, bool]:
    """An attribute's address as a browser resolves it, from its entity-decoded value.

    As the URL standard does, leading and trailing C0 controls and spaces are
    stripped and every tab, CR and LF is removed. Returns that address, its
    scheme in lowercase or None, and whether it names another host without a
    scheme: two leading slashes or backslashes, which a page served over
    HTTP(S) or opened from disk resolves to another host.
    """
    address = re.sub(r"[\t\n\r]", "", value.strip(_C0_OR_SPACE))
    scheme = _SCHEME.match(address)
    if scheme:
        return address, scheme[1].lower(), False
    return address, None, len(address) > 1 and address[0] in "/\\" and address[1] in "/\\"


def web_address(address: str, scheme: str | None) -> str:
    """An http(s) or protocol-relative address from `browser_address` as `scheme://host/…`.

    Browsers find the host after any run of slashes and backslashes that
    follows `http:` or `https:`; in this form lint and every browser read the
    same host. A protocol-relative address takes https, as the site is served.
    """
    rest = address[len(scheme) + 1:] if scheme else address
    return (scheme or "https") + "://" + rest.lstrip("/\\")


def rewrite_links(markup: str, page: SourcePage, routes: dict[str, str], root: Path,
                  exists, links_checked_from: str | None = None,
                  media_ok=None) -> tuple[str, list[str], set[str]]:
    """Resolve relative link/media targets from the source file's own folder.

    Registered sources become `<route>#fragment`; other repository paths become
    the logical `docs/html/` URL the site bundle already understands. Returns
    the markup, any containment or missing-target problems, and the link
    targets whose fragments are not checked.

    `links_checked_from` is given for the project's worklog only. In an entry
    dated before it, a link or image whose target is gone renders as its text
    inside `LINK_GONE` instead of failing the build, and a link that appears
    only in such entries keeps its fragment unchecked.

    An automatically listed page (`page.automatic`) never fails: every
    address is read as a browser reads it (`browser_address`), every link or
    image the build cannot serve renders as its text inside `LINK_GONE`, other
    media lose the attribute, an external image becomes a link to it (its text
    inside a link), and the returned problems are notes. `media_ok(path)` then
    says whether an existing media file can be packaged (tracked, not private).
    """
    problems: list[str] = []
    folder = posixpath.dirname(page.source)
    tolerant = page.automatic
    unchecked = unchecked_spans(markup, links_checked_from, HTML_HEADING)
    old_hrefs: set[str] = set()
    new_hrefs: set[str] = set()

    def resolve(raw: str, old: bool, media: bool) -> str | None:
        value = html.unescape(raw)
        if tolerant:
            # Only data: media, links with a served scheme and paths inside the
            # repository stay; the address is written as the browser reads it.
            value, scheme, other_host = browser_address(value)
            if media and scheme == "data":
                if _RASTER_DATA.match(value):
                    return value
                problems.append(f"{page.source}: media address {_visible(raw)[:60]} {RASTER_NOTE}")
                return _GONE
            if media and (scheme or other_host):
                problems.append(f"{page.source}: media address {_visible(raw)} is not served")
                return _GONE
            if other_host or scheme in {"http", "https"}:
                return web_address(value, scheme)
            if scheme in LINK_SCHEMES:
                return value
            if scheme:
                problems.append(f"{page.source}: link scheme {scheme}: is not served; shown as text: {_visible(raw)}")
                return _GONE
            value = value.replace("\\", "/")  # as browsers read a path under http(s) and file
        url = urlsplit(value)
        if tolerant and media and not url.path:
            problems.append(f"{page.source}: media address {_visible(raw)} names no file")
            return _GONE
        if url.scheme or url.netloc or not url.path:
            return value if tolerant else None  # external, same-page fragment or empty
        if url.path.startswith("/"):
            problems.append(f"{page.source}: absolute link {_visible(raw)}; use a path relative to the source file")
            return _GONE if tolerant else None
        target = posixpath.normpath(posixpath.join(folder, unquote(url.path)))
        if target == ".." or target.startswith("../"):
            problems.append(f"{page.source}: link escapes the repository: {_visible(raw)}")
            return _GONE if tolerant else None
        suffix = ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")
        if target in routes and not media:
            return routes[target] + suffix
        if not exists(root / target):
            if old:
                return _GONE
            problems.append(f"{page.source}: link target not found: {_visible(raw)}")
            return _GONE if tolerant else None
        if tolerant and media and posixpath.splitext(target)[1].lower() not in RASTER_SUFFIXES:
            problems.append(f"{page.source}: media file {_visible(raw)} {RASTER_NOTE}")
            return _GONE
        file = root / target
        if tolerant and media and not file.is_symlink() and file.is_file() and not raster_image(file):
            problems.append(f"{page.source}: media file {_visible(raw)} is not the image its name says; shown as text")
            return _GONE
        if tolerant and media and not media_ok(file):
            problems.append(f"{page.source}: media file is not packaged (untracked, private or symlinked): "
                            f"{_visible(raw)}")
            return _GONE
        logical = posixpath.relpath(target, "docs/html")
        if url.path.endswith("/") and not logical.endswith("/"):
            logical += "/"
        return quote(logical, safe="/-_.~") + suffix

    # An external image inside a link becomes text, so links never nest.
    link_starts = [found.start() for found in re.finditer(r"<a\b", markup)]
    link_ends = [found.start() for found in re.finditer(r"</a>", markup)]

    def tag(match: re.Match) -> str:
        original = match[0]
        name = match[1].lower()
        old = within(unchecked, match.start())
        updated = original
        for attribute, raw in _ATTR.findall(original):
            media = name != "a" and attribute in {"src", "poster"}
            address, scheme, other_host = browser_address(html.unescape(raw))
            if tolerant and media and (other_host or scheme in {"http", "https"}):
                problems.append(f"{page.source}: external media is not loaded; shown as a link: {_visible(raw)}")
                if name == "img":
                    target = html.escape(web_address(address, scheme), quote=True)
                    alt = _ALT.search(original)
                    text = alt[1] if alt and alt[1] else target
                    if bisect(link_starts, match.start()) > bisect(link_ends, match.start()):
                        return text
                    return f'<a href="{target}">{text}</a>'
                updated = re.sub(r"\s" + attribute + '="' + re.escape(raw) + '"', "", updated, count=1)
                continue
            replacement = resolve(raw, old, media and tolerant)
            if replacement == _GONE and name in {"a", "img"}:
                if name == "a":
                    return _GONE  # the closing </a> becomes </span> below
                alt = _ALT.search(original)
                return LINK_GONE + (alt[1] if alt else raw) + "</span>"
            if replacement == _GONE and tolerant:
                updated = re.sub(r"\s" + attribute + '="' + re.escape(raw) + '"', "", updated, count=1)
                continue
            if replacement == _GONE:  # other media keep failing the build
                problems.append(f"{page.source}: link target not found: {_visible(raw)}")
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


_CSS_URL = re.compile(r"url\((?=\s*['\"]?(?:https?:)?//)", re.I)
_QUOTED_ATTRIBUTE = re.compile(r"""\s[^\s"'<>/=]+\s*=\s*(?:"[^"]*"|'[^']*')""")

# The raw HTML an automatically listed file keeps: these tags, each with these
# attributes. Every other tag shows as text and every other attribute is
# dropped, so no class, style, data-* or on… attribute passes, and no tag that
# loads, runs, embeds or encloses content.
_ANY = frozenset({"id", "title", "align"})
ADMITTED_HTML: dict[str, frozenset[str]] = {
    **dict.fromkeys(("abbr", "b", "blockquote", "br", "caption", "code", "dd", "del", "div", "dl", "dt", "em",
                     "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "ins", "kbd", "li", "mark", "ol", "p", "pre",
                     "s", "small", "span", "strong", "sub", "summary", "sup", "tbody", "tfoot", "thead", "tr", "u",
                     "ul"), _ANY),
    "a": _ANY | {"href", "name"},
    "details": _ANY | {"open"},
    "img": _ANY | {"src", "alt", "width", "height"},
    "table": _ANY | {"width"},
    "td": _ANY | {"colspan", "rowspan", "width"},
    "th": _ANY | {"colspan", "rowspan", "width"},
}
# Ids the kit's shell, sidebar and components own or look up, and the globals
# its scripts read, which an element's id or name would define. A listed file
# gives none of them to an element, in any letter case, so its content cannot
# stand in for a part of the kit. tests/test_listed_html.py keeps the list
# complete against the shell and the components.
KIT_IDS = frozenset({
    "backdrop", "menu", "sidebar", "toc", "top", "repo-tree-label", "chapter-reader", "reader-chapter-list",
    "plot-toggle-labels", "page-lock", "page-lock-data", "page-lock-form", "page-lock-keys", "page-lock-message",
    "page-lock-password", "page-lock-remember", "page-lock-status",
    "docsreferencetree", "docslockedreferencetree", "figtoggles", "module",
})
_VOID = frozenset({"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track",
                   "wbr"})
# Marks a tag the file wrote, between "<" and its name, until `ListedHtml.finish`.
# `read_source` turns every U+0000 of a file into U+FFFD, so no text carries it.
_RAW = "\x00"
_OUTPUT_TAG = re.compile(r"<(/?)(\x00?)([A-Za-z][A-Za-z0-9]*)([^>]*)>")
_SPACE = "\t\n\f\r "
_ASCII_LOWER = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")


def _as_text(text: str) -> str:
    """Raw text between tags, keeping its character references. Quotes are
    escaped too, since the renderer writes image text into an `alt` value."""
    return text.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")


def _read_tag(raw: str, start: int) -> tuple[int, bool, str, list[tuple[str, str | None]]] | None:
    """The tag that starts at `raw[start]`, as the HTML tokenizer splits it.

    Returns its end, whether it is an end tag, its name and its attributes in
    order, each name in lowercase with its raw value or None; None when no
    complete tag starts there, such as `<` before a space or a tag the
    fragment ends inside.
    """
    end = start + 1
    closing = raw.startswith("/", end)
    end += closing
    if end >= len(raw) or not (raw[end].isascii() and raw[end].isalpha()):
        return None
    begin = end
    while end < len(raw) and raw[end] not in _SPACE + "/>":
        end += 1
    name, attributes = raw[begin:end].translate(_ASCII_LOWER), []
    while True:
        while end < len(raw) and raw[end] in _SPACE + "/":
            end += 1
        if end >= len(raw):
            return None
        if raw[end] == ">":
            return end + 1, closing, name, attributes
        begin = end
        end += 1  # an attribute name may start with "="
        while end < len(raw) and raw[end] not in _SPACE + "/>=":
            end += 1
        attribute, value = raw[begin:end].translate(_ASCII_LOWER), None
        after = end
        while after < len(raw) and raw[after] in _SPACE:
            after += 1
        if after < len(raw) and raw[after] == "=":
            end = after + 1
            while end < len(raw) and raw[end] in _SPACE:
                end += 1
            if end < len(raw) and raw[end] in "\"'":
                close = raw.find(raw[end], end + 1)
                if close < 0:
                    return None
                value, end = raw[end + 1:close], close + 1
            else:
                begin = end
                while end < len(raw) and raw[end] not in _SPACE + ">":
                    end += 1
                value = raw[begin:end]
        attributes.append((attribute, value))


def _counted(counts: Counter) -> str:
    return ", ".join(name + (f" ({count})" if count > 1 else "") for name, count in sorted(counts.items()))


class ListedHtml:
    """The raw HTML of one automatically listed file, admitted by allowlist.

    The Markdown renderer hands each block and inline HTML fragment of the file
    to `fragment`; the markup the renderer writes itself never passes through
    it, so the kit's own classes and styles stay. A complete comment is dropped.
    A tag in `ADMITTED_HTML` is written again with its admitted attributes
    only, each entity-decoded and escaped in double quotes, and marked with
    `_RAW`. Every other tag, an unclosed comment and every other `<` show as
    text. `finish` then matches the marked tags with the renderer's markup and
    removes the marks.
    """

    def __init__(self, source: str) -> None:
        self.source = source
        self.tags: Counter = Counter()        # shown as text, by tag name
        self.attributes: Counter = Counter()  # dropped, by attribute name
        self.identifiers: Counter = Counter()  # ids and names of the kit, dropped
        self.unclosed_comments = 0
        self.unmatched = 0                    # end tags that close nothing the file opened
        self.nested_links = 0                 # links opened inside a link

    def admits_identifier(self, value: str) -> bool:
        """Whether an id or name may stay: not one of `KIT_IDS`."""
        if value.translate(_ASCII_LOWER) in KIT_IDS:
            self.identifiers[value] += 1
            return False
        return True

    def fragment(self, raw: str, block: bool = False) -> str:
        """One block or inline HTML fragment of the file, with only admitted tags left as markup.

        A link the file opens in an HTML block (`block`) ends with that block,
        so it cannot take in the Markdown that follows.
        """
        raw = raw.replace(_RAW, "\ufffd")
        out, at, link = [], 0, False
        while (start := raw.find("<", at)) >= 0:
            out.append(_as_text(raw[at:start]))
            if raw.startswith("<!--", start):
                end = raw.find("-->", start + 4)
                if end >= 0:
                    at = end + 3
                    continue
                self.unclosed_comments += 1
            tag = _read_tag(raw, start)
            if tag is None:
                if raw.startswith(("<!", "<?"), start) and not raw.startswith("<!--", start):
                    self.tags["<" + raw[start + 1] + "…>"] += 1
                out.append("&lt;")
                at = start + 1
                continue
            end, closing, name, attributes = tag
            if name in ADMITTED_HTML:
                out.append(self._admit(name, closing, attributes))
                if name == "a":  # as `finish` pairs them: a link inside a link is dropped
                    link = not closing
            else:
                self.tags[name] += 1
                out.append(html.escape(raw[start:end], quote=True))
            at = end
        out.append(_as_text(raw[at:]))
        if block and link:
            out.append("</" + _RAW + "a>")
        return "".join(out)

    def _admit(self, name: str, closing: bool, attributes: list[tuple[str, str | None]]) -> str:
        if closing:
            if name in _VOID:
                self.unmatched += 1
                return ""
            return "</" + _RAW + name + ">"
        kept, seen = [], set()
        for attribute, value in attributes:
            if attribute in seen:
                continue  # as in browsers, the first of a repeated attribute counts
            seen.add(attribute)
            if attribute not in ADMITTED_HTML[name]:
                self.attributes["on…" if attribute.startswith("on")
                                else "data-…" if attribute.startswith("data-") else attribute] += 1
                continue
            value = html.unescape(value or "")
            if attribute in {"id", "name"} and not self.admits_identifier(value):
                continue
            kept.append(attribute if attribute == "open" else f'{attribute}="{html.escape(value, quote=True)}"')
        return "<" + _RAW + name + "".join(" " + item for item in kept) + ">"

    def finish(self, markup: str) -> tuple[str, list[str]]:
        """The rendered file with the file's elements matched, and notes on what was not admitted.

        An element the file opened ends at the latest where the element the
        renderer put around it ends, and at the end of the file. An end tag
        ends only an element the file opened inside the renderer's current
        element; any other is dropped, so the file can neither close the
        kit's markup nor leave an element open past its own content. A link
        opened inside a link is dropped, and `fragment` ends a link with the
        HTML block that opened it, so links do not spill over.
        """
        out, stack, at = [], [], 0  # stack: (tag name, written by the file)
        for match in _OUTPUT_TAG.finditer(markup):
            out.append(markup[at:match.start()].replace("<", "&lt;"))
            at = match.end()
            closing, raw, name, rest = match[1], bool(match[2]), match[3].lower(), match[4]
            if not raw:
                if closing:
                    while stack and stack[-1][1]:
                        out.append(f"</{stack.pop()[0]}>")
                    if stack and stack[-1][0] == name:
                        stack.pop()
                elif name not in _VOID:
                    stack.append((name, False))
                out.append(match[0])
            elif closing:
                depth = next((index for index in range(len(stack) - 1, -1, -1)
                              if not stack[index][1] or stack[index][0] == name), None)
                if depth is None or not stack[depth][1]:
                    self.unmatched += 1
                    continue
                while len(stack) > depth:
                    out.append(f"</{stack.pop()[0]}>")
            elif name == "a" and any(open_name == "a" for open_name, _ in stack):
                self.nested_links += 1
            else:
                out.append("<" + name + rest + ">")
                if name not in _VOID:
                    stack.append((name, True))
        out.append(markup[at:].replace("<", "&lt;"))
        out.extend(f"</{name}>" for name, raw in reversed(stack) if raw)
        return "".join(out), self.notes()

    def notes(self) -> list[str]:
        source, notes = self.source, []
        if self.tags:
            notes.append(f"{source}: {sum(self.tags.values())} raw HTML tag(s) outside the allowlist shown as text: "
                         f"{_counted(self.tags)}")
        if self.attributes:
            notes.append(f"{source}: {sum(self.attributes.values())} raw HTML attribute(s) outside the allowlist "
                         f"removed: {_counted(self.attributes)}")
        if self.identifiers:
            notes.append(f"{source}: {sum(self.identifiers.values())} id or name value(s) of the kit's page removed: "
                         f"{_counted(self.identifiers)}")
        if self.unclosed_comments:
            notes.append(f"{source}: unclosed HTML comment shown as text")
        if self.unmatched:
            notes.append(f"{source}: {self.unmatched} raw HTML end tag(s) that close nothing the file opened removed")
        if self.nested_links:
            notes.append(f"{source}: {self.nested_links} raw HTML link(s) inside another link removed")
        return notes


def quiet_text(markup: str) -> str:
    """Keep page text from reading as markup to the site's checks.

    Outside tags, a double quote becomes `&quot;` and a CSS `url(` before an
    external address becomes `url&#40;`; both render the same. Inside a tag,
    an attribute whose value loads an external `url(...)` is removed.
    """
    parts = re.split(r"(<[^>]*>)", markup)
    for index, part in enumerate(parts):
        if index % 2 == 0:
            parts[index] = _CSS_URL.sub("url&#40;", part.replace('"', "&quot;"))
        elif _CSS_URL.search(part):
            parts[index] = _QUOTED_ATTRIBUTE.sub(lambda m: "" if _CSS_URL.search(m[0]) else m[0], part)
    return "".join(parts)


_SAME_PAGE_LINK = re.compile(r'<a\b[^>]*?\bhref="#([^"]+)"[^>]*>', re.I)


def unlink_missing_fragments(page_html: str, source: str) -> tuple[str, list[str]]:
    """Show a same-page link whose anchor the built page lacks as unlinked text."""
    identifiers = set(_ID.findall(page_html))
    notes: list[str] = []

    def unlink(match: re.Match) -> str:
        if match[1] in identifiers:
            return match[0]
        notes.append(f"{source}: anchor #{match[1]} not found on its own page; shown as text")
        return _GONE

    page_html = _SAME_PAGE_LINK.sub(unlink, page_html)
    if notes:
        page_html = re.sub(re.escape(_GONE) + r"(.*?)</a>", lambda m: LINK_GONE + m[1] + "</span>", page_html,
                           flags=re.S)
    return page_html, notes


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


_ROUTE_FRAGMENT = re.compile(r'<a\b[^>]*?\bhref="([^"/?#:]+\.html)#([^"]+)"', re.I)


def fragment_notes(pages: dict[str, str], automatic: set[str]) -> list[str]:
    """Missing anchors in links from or into automatically listed pages; these never fail."""
    identifiers: dict[str, set[str]] = {}
    notes = []
    for name in sorted(pages):
        for target, fragment in _ROUTE_FRAGMENT.findall(pages[name]):
            if (name not in automatic and target not in automatic) or target not in pages:
                continue
            if target not in identifiers:
                identifiers[target] = set(_ID.findall(pages[target]))
            if html.unescape(unquote(fragment)) not in identifiers[target]:
                notes.append(f"{name}: anchor #{fragment} not found in {target}; the link opens the page top")
    return notes


def exists_in(root: Path, resolver):
    """Existence test honoring the project's legacy path resolver."""
    def exists(path: Path) -> bool:
        return os.path.lexists(path) or os.path.lexists(resolver(path, root=root))
    return exists
