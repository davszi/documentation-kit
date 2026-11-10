"""Changed record sections and the topic pages that explain them.

A record is a tracked Markdown file of the project other than a topic page
(`docs/topics/<topic>/index.md`). When a record section changes, the pages
that link that section, its enclosing sections or the whole record may need
rereading. `record_change_notes` names those pages; lint prints the result as
notes, which never fail a run.

Changes compare the working tree (staged and unstaged) with HEAD, or with
another revision. A project outside Git, without a first commit or with no
changed record has no notes.
"""

from __future__ import annotations

import codecs
import posixpath
import re
import subprocess
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
HEADING_RE = re.compile(r"(#{1,6})\s+(.*)")
EXPLICIT_ID_RE = re.compile(r"\{#([A-Za-z0-9][\w-]*)\}\s*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?")
REFERENCE_LINK_RE = re.compile(r"^[ ]{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", re.M)
HREF_RE = re.compile(r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
SECTION_RE = re.compile(r"<section\b([^>]*)>|</section\s*>", re.I)
CHAPTER_HEADING_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
SCHEME_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
PAGE_END = "<!-- page-end -->"


@dataclass(frozen=True)
class Heading:
    line: int  # 1-based line of the heading in the new file
    level: int
    text: str
    anchor: str


@dataclass
class ChangedSection:
    record: str
    heading: Heading | None  # None: above the first heading, or the whole record
    anchors: set[str] = field(default_factory=set)  # this section and its enclosing ones
    whole_record: bool = False  # the record itself was deleted


@dataclass(frozen=True)
class RecordLink:
    page: str
    record: str
    fragment: str | None
    chapter: str | None
    position: int


# ------------------------------------------------------------------ Git
def _git(root: Path, *args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["git", "-C", str(root), "-c", "core.quotepath=off", *args],
                              capture_output=True, text=True)
    except OSError:
        return None


def _commit(root: Path, revision: str) -> bool:
    if revision.startswith("-"):
        return False
    result = _git(root, "rev-parse", "--verify", "--quiet", revision + "^{commit}")
    return result is not None and result.returncode == 0


def _diff_path(raw: str) -> str | None:
    """The repository path from a `--- a/…` or `+++ b/…` diff line."""
    raw = raw.rstrip("\n")
    if raw.startswith('"') and raw.endswith('"'):
        raw = codecs.escape_decode(raw[1:-1].encode())[0].decode("utf-8", "replace")
    else:
        raw = raw.split("\t", 1)[0]  # Git ends an unquoted name that contains a space with a tab
    if raw == "/dev/null":
        return None
    return raw[2:] if raw[:2] in ("a/", "b/") else raw


def changed_lines(root: Path, since: str | None = None) -> dict[str, list[int] | None]:
    """Changed Markdown files mapped to new-file line positions.

    A position is a changed or added line, or for a pure deletion the line
    after which the content was removed (0 at the top of the file). A file
    deleted from the working tree maps to None. Raises ValueError when an
    explicit `since` revision does not name a commit.
    """
    root = Path(root)
    base = since or "HEAD"
    if not _commit(root, base):
        if since is not None:
            raise ValueError(f"--since {since}: not a commit in this repository")
        return {}
    result = _git(root, "diff", "--relative", "--no-color", "--no-ext-diff", "--no-textconv",
                  "--no-renames", "--ignore-submodules", "--src-prefix=a/", "--dst-prefix=b/",
                  "-U0", base, "--", "*.md")
    if result is None or result.returncode != 0:
        return {}
    changes: dict[str, list[int] | None] = {}
    old = new = None
    header = False  # file names are read only between "diff --git" and the first hunk
    for line in result.stdout.splitlines():
        if line.startswith("diff --git "):
            old = new = None
            header = True
        elif header and line.startswith("--- "):
            old = _diff_path(line[4:])
        elif header and line.startswith("+++ "):
            new = _diff_path(line[4:])
            if new is None and old is not None:
                changes[old] = None
            elif new is not None:
                changes.setdefault(new, [])
        elif new is not None and (match := HUNK_RE.match(line)):
            header = False
            start, count = int(match.group(1)), int(match.group(2) or 1)
            positions = changes[new]
            if count:
                positions.extend(range(start, start + count))
            else:
                positions.append(start)
    return changes


# ------------------------------------------------------------- Markdown
def headings(text: str, slugify) -> list[Heading]:
    """ATX headings outside fenced code and TOML frontmatter, as lint anchors them."""
    found, in_fence = [], False
    lines = text.splitlines()
    start = 0
    if lines and lines[0] == "+++":
        closing = next((i for i in range(1, len(lines)) if lines[i] == "+++"), None)
        if closing is not None:
            start = closing + 1
    for number, line in enumerate(lines[start:], start + 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        body = match.group(2)
        explicit = EXPLICIT_ID_RE.search(body)
        title = re.sub(r"\{#.*\}\s*$", "", body).strip()
        anchor = explicit.group(1) if explicit else slugify(re.sub(r"\{#.*\}\s*$", "", body))
        found.append(Heading(number, len(match.group(1)), title, anchor))
    return found


def _enclosing(heads: list[Heading], line: int) -> list[Heading]:
    """Headings enclosing a line, outermost first."""
    chain: list[Heading] = []
    for head in heads:
        if head.line > line:
            break
        while chain and chain[-1].level >= head.level:
            chain.pop()
        chain.append(head)
    return chain


def changed_sections(root: Path, slugify, since: str | None = None) -> list[ChangedSection]:
    """Changed sections of records: tracked Markdown files that are not topic pages."""
    root = Path(root)
    pages = {page.relative_to(root).as_posix() for page in topic_pages(root)}
    sections: dict[tuple[str, int], ChangedSection] = {}
    for record, positions in changed_lines(root, since).items():
        if record in pages:
            continue
        if positions is None:
            sections[(record, -1)] = ChangedSection(record, None, whole_record=True)
            continue
        path = root / record
        if not path.is_file():
            continue
        heads = headings(path.read_text(errors="replace"), slugify)
        for position in positions:
            chain = _enclosing(heads, position)
            key = (record, chain[-1].line if chain else 0)
            section = sections.setdefault(key, ChangedSection(record, chain[-1] if chain else None))
            section.anchors.update(head.anchor for head in chain)
    return [sections[key] for key in sorted(sections)]


def _blank(chars: list[str], start: int, end: int) -> None:
    for i in range(start, end):
        if chars[i] != "\n":
            chars[i] = " "


def masked(text: str) -> str:
    """Text of the same length with frontmatter, comments and code blanked."""
    chars = list(text)
    if text.startswith("+++\n"):
        end = text.find("\n+++\n", 4)
        if end >= 0:
            _blank(chars, 0, end + 4)
    for match in re.finditer(r"<!--[\s\S]*?-->", text):
        _blank(chars, match.start(), match.end())
    offset, in_fence = 0, False
    for line in "".join(chars).splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            _blank(chars, offset, offset + len(line))
        elif in_fence:
            _blank(chars, offset, offset + len(line))
        else:
            for match in re.finditer(r"`[^`\n]*`", line):
                _blank(chars, offset + match.start(), offset + match.end())
        offset += len(line)
    return "".join(chars)


def _chapter_index(text: str, slugify) -> list[tuple[int, str, str | None]]:
    """Ordered (position, kind, value) events for card sections and `## ` headings."""
    events = []
    for match in SECTION_RE.finditer(text):
        if match.group(0).startswith("</"):
            events.append((match.start(), "close", None))
            continue
        attributes = match.group(1)
        classes = re.search(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""", attributes)
        ident = re.search(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)')""", attributes)
        card = classes and "card" in (classes.group(1) or classes.group(2) or "").split()
        events.append((match.start(), "open", (ident.group(1) or ident.group(2)) if card and ident else None))
    for match in CHAPTER_HEADING_RE.finditer(text):
        body = match.group(1)
        explicit = EXPLICIT_ID_RE.search(body)
        events.append((match.start(), "heading",
                       explicit.group(1) if explicit else slugify(re.sub(r"\{#.*\}\s*$", "", body))))
    return sorted(events, key=lambda event: event[0])


def _chapter_at(events, position: int) -> str | None:
    stack: list[str | None] = []
    heading = None
    for at, kind, value in events:
        if at > position:
            break
        if kind == "open":
            stack.append(value)
        elif kind == "close":
            if stack:
                stack.pop()
        else:
            heading = value
    card = next((value for value in reversed(stack) if value), None)
    return card or heading


def page_links(root: Path, page: Path, records: set[str], routes: dict[str, str], slugify) -> list[RecordLink]:
    """Links from a topic page to records, by file path or by built route."""
    root = Path(root)
    raw = page.read_text(errors="replace")
    page_end = raw.find(PAGE_END)  # read before masking, which blanks the marker with every comment
    text = masked(raw)
    events = _chapter_index(text, slugify)
    html = root / "docs/html"
    links = []
    found = [(m.start(), m.group(1)) for m in MARKDOWN_LINK_RE.finditer(text)]
    found += [(m.start(), m.group(1)) for m in REFERENCE_LINK_RE.finditer(text)]
    found += [(m.start(), m.group(1) if m.group(1) is not None else m.group(2)) for m in HREF_RE.finditer(text)]
    for position, target in sorted(found):
        target = target.strip()
        if not target or SCHEME_RE.match(target):
            continue
        path_part, _, fragment = target.partition("#")
        path_part = unquote(path_part.partition("?")[0])
        if not path_part:
            continue
        # Page bodies are emitted into docs/html; a working-notes tail below
        # the page-end marker is read from its own folder (as lint resolves them).
        base = page.parent if 0 <= page_end < position else html
        destination = Path(posixpath.normpath((base / path_part).as_posix()))
        try:
            relative = destination.relative_to(root).as_posix()
        except ValueError:
            continue
        record = relative if relative in records else None
        if record is None and destination.parent == html and destination.suffix == ".html":
            record = routes.get(destination.stem)
        if record is None:
            continue
        links.append(RecordLink(page.relative_to(root).as_posix(), record, unquote(fragment) or None,
                                _chapter_at(events, position), position))
    return links


# ------------------------------------------------------------- Project
def topic_pages(root: Path) -> list[Path]:
    from topic_structure import topic_pages as pages
    return pages(Path(root))


def source_routes(root: Path) -> dict[str, str]:
    """Built route stem (slug) to the record it renders, from [[source_pages]]."""
    config = Path(root) / "docs/site/site.toml"
    try:
        site = tomllib.loads(config.read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    entries = site.get("source_pages", [])
    if not isinstance(entries, list):
        return {}  # the build reports a malformed registry
    return {entry["slug"]: entry["source"] for entry in entries
            if isinstance(entry, dict) and isinstance(entry.get("slug"), str)
            and isinstance(entry.get("source"), str)}


def record_change_notes(root: Path, slugify, since: str | None = None) -> list[str]:
    """Formatted notes, one per changed record section that a page explains."""
    root = Path(root)
    sections = changed_sections(root, slugify, since)
    if not sections:
        return []
    changed = {section.record for section in sections}
    routes = {slug: source for slug, source in source_routes(root).items() if source in changed}
    links = [link for page in topic_pages(root) for link in page_links(root, page, changed, routes, slugify)]
    notes = []
    for section in sections:
        readers: dict[tuple[str, str | None], int] = {}
        for link in links:
            if link.record != section.record:
                continue
            # A link to a whole record (no #section) is a pointer to the guide, as in
            # routes tables; it depends on the record's opening text only. Section
            # changes reach the pages that link that section.
            if link.fragment is None:
                if not (section.whole_record or section.heading is None):
                    continue
            elif not (section.whole_record or link.fragment in section.anchors):
                continue
            readers.setdefault((link.page, link.chapter), link.position)
        if not readers:
            continue
        title = section.record + (f" › {section.heading.text}" if section.heading else "")
        lines = [f"NOTE: {title} changed.", "      Pages that explain it — reread them:"]
        for (page, chapter), _ in sorted(readers.items(), key=lambda item: (item[0][0], item[1])):
            lines.append(f"        {page}" + (f"  (chapter: {chapter})" if chapter else ""))
        notes.append("\n".join(lines))
    return notes
