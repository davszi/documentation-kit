"""Numbers on pages for people, checked against the records the page links.

A page explains records and adds no number they lack. `page_number_notes`
lists, for each topic page (`docs/topics/<topic>/index.md`), the numbers in its
prose that appear in none of the records the page links. Lint prints the result
as notes, which never fail a run.

The check is tied to the page, not to who wrote it, and needs nothing from the
author. It answers one question only: is this number stated in a linked record?
Whether the record's number is correct stays with the record's own rules.

Not checked: frontmatter, comments, code (fences, backticks, `<code>`, `<pre>`),
inline SVG, HTML attributes, link targets, version numbers, dates, labels such
as "Figure 3" or "01", and everything below the page-end marker. A literal or
illustrative value therefore goes in code. A page that links no record has
nothing to be compared with and is skipped.

The notes are off unless the site sets `page_number_notes = true`. The check
suits pages that explain Markdown records. It does not suit pages that report
measurements read from experiment data: those numbers are rounded or derived,
so they match no text, and such a project needs its own ledger check instead.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from record_changes import PAGE_END, _chapter_at, _chapter_index, _git, masked, page_links, source_routes, topic_pages

NUMBER_RE = re.compile(r"(?<![\w.,#/-])\d[\d,]*(?:\.\d+)?(?![\w/-])")
RECORD_NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
# Blanked before numbers are read: each pattern covers text that is not a stated quantity.
NOT_PROSE = (
    re.compile(r"<(svg|pre|code|script|style)\b[\s\S]*?</\1\s*>", re.I),
    re.compile(r"<[^>]+>"),
    re.compile(r"\]\([^)\n]*\)"),
    re.compile(r"&#?\w+;"),
    re.compile(r"\b\d+(?:\.\d+){2,}\b"),                      # versions, addresses
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                     # dates
    re.compile(r"\b\d+(?::\d+)+\b"),                         # ratios such as 16:9, times
    re.compile(r"\b(?:Figure|Fig\.|Table|Step|Chapter|Section|Part)\s+\d+\b", re.I),
)


def _blank(text: str, pattern: re.Pattern) -> str:
    return pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


def prose(text: str) -> str:
    """Page text of the same length with everything that is not prose blanked."""
    text = masked(text)
    end = text.find(PAGE_END)
    if end >= 0:
        text = text[:end] + re.sub(r"[^\n]", " ", text[end:])
    for pattern in NOT_PROSE:
        text = _blank(text, pattern)
    return text


def _normal(number: str) -> str:
    return number.replace(",", "").rstrip(".")


def stated_numbers(text: str) -> set[str]:
    """Every number a record states anywhere, code and tables included."""
    return {_normal(match) for match in RECORD_NUMBER_RE.findall(text)}


def shown_numbers(text: str) -> list[tuple[int, str]]:
    """(position, number) for each quantity in a page's prose; labels such as 01 are skipped."""
    found = []
    for match in NUMBER_RE.finditer(prose(text)):
        number = _normal(match.group(0))
        if number and not (len(number) > 1 and number.startswith("0") and "." not in number):
            found.append((match.start(), number))
    return found


def _records(root: Path) -> set[str]:
    """Markdown files of the project other than topic pages."""
    listed = _git(root, "ls-files", "-z", "--", "*.md")
    if listed is not None and listed.returncode == 0:
        names = [name for name in listed.stdout.split("\0") if name]
    else:
        skip = {".git", ".build", ".docs-kit", "node_modules"}
        names = [path.relative_to(root).as_posix() for path in root.rglob("*.md")
                 if not skip & set(path.relative_to(root).parts)]
    pages = {page.relative_to(root).as_posix() for page in topic_pages(root)}
    return {name for name in names if name not in pages}


LISTED = 12  # numbers named per chapter before the rest is counted


def enabled(root: Path) -> bool:
    try:
        site = tomllib.loads((Path(root) / "docs/site/site.toml").read_text())
    except (OSError, tomllib.TOMLDecodeError):
        return False
    return site.get("page_number_notes") is True


def page_number_notes(root: Path, slugify) -> list[str]:
    """Formatted notes, one per page that shows numbers its linked records do not state."""
    root = Path(root)
    if not enabled(root):
        return []
    records, routes = _records(root), source_routes(root)
    notes = []
    for page in topic_pages(root):
        text = page.read_text(errors="replace")
        linked = sorted({link.record for link in page_links(root, page, records, routes, slugify)})
        if not linked:
            continue
        stated: set[str] = set()
        for record in linked:
            try:
                stated |= stated_numbers((root / record).read_text(errors="replace"))
            except OSError:
                continue  # lint reports the missing link target
        events = _chapter_index(masked(text), slugify)
        by_chapter: dict[str | None, list[str]] = {}
        for position, number in shown_numbers(text):
            if number in stated:
                continue
            chapter = _chapter_at(events, position)
            if number not in by_chapter.setdefault(chapter, []):
                by_chapter[chapter].append(number)
        if not by_chapter:
            continue
        lines = [f"NOTE: {page.relative_to(root).as_posix()} shows numbers that none of its linked records state:"]
        for chapter, numbers in by_chapter.items():
            more = f" and {len(numbers) - LISTED} more" if len(numbers) > LISTED else ""
            lines.append(f"        {', '.join(numbers[:LISTED])}{more}" + (f"  (chapter: {chapter})" if chapter else ""))
        lines.append("      State each in its record, show it as code if it is a literal value, or take it off the page.")
        notes.append("\n".join(lines))
    return notes
