"""Which file is the worklog, how its entries are dated, and which keep checked links.

Lint and build share these rules, and `fenced_spans`, which finds the fenced
code blocks of Markdown source for every caller that must skip them, such as
the build's marker cards. A worklog entry is a level-two section whose
heading starts with its date, `## YYYY-MM-DD`. A level-two section without a
date belongs to the dated entry above it; text before the first dated heading
belongs to no entry.

`worklog_links_checked_from = "YYYY-MM-DD"` in docs/site/site.toml names the
oldest entry whose links are still checked. Entries are append-only, so a link
in an older entry cannot follow a later move or removal of its target: lint
skips those links, and the build renders such a link whose target is gone as
its text, unlinked.
"""
from __future__ import annotations

from datetime import date
import re

from page_source import ENTRY_HEADING, markdown_headings

ENTRY_DEFAULTS = {"worklog": "docs/worklog.md", "open_work": "docs/open/OPEN.md"}
CUTOFF_ERROR = 'worklog_links_checked_from must be a date written as "YYYY-MM-DD"'

# Level-two headings in rendered HTML; group 1 is the heading text, which
# starts with the entry's date. `_entry_headings` finds them in Markdown source.
HTML_HEADING = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.S)
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_FENCE = re.compile(r"(?m)^ {0,3}(`{3,}|~{3,})")


def configured_entry(site: dict, key: str):
    """The configured value of `worklog` or `open_work`, or its default path."""
    return site.get(key, ENTRY_DEFAULTS[key])


def links_checked_from(site: dict) -> str | None:
    """The configured cut-off date as `YYYY-MM-DD`, or None when unset.

    The value is the text "YYYY-MM-DD" or the same date written as a TOML date
    without quotes. Raises ValueError with CUTOFF_ERROR for anything else,
    other ISO spellings such as "20000102" included.
    """
    value = site.get("worklog_links_checked_from")
    if value is None:
        return None
    if type(value) is date:
        return value.isoformat()
    try:
        if isinstance(value, str) and _DATE.fullmatch(value):
            return date.fromisoformat(value).isoformat()
    except ValueError:
        pass
    raise ValueError(CUTOFF_ERROR)


def fenced_spans(text: str) -> list[tuple[int, int]]:
    """(start, end) offsets of fenced code blocks in Markdown source.

    A block opens at a line of three or more backticks or tildes and closes at
    the next fence line of the same character that is at least as long; a block
    left open runs to the end of the text.
    """
    spans: list[tuple[int, int]] = []
    opened = None
    for match in _FENCE.finditer(text):
        marker = match.group(1)
        if opened is None:
            opened = (match.start(), marker)
        elif marker[0] == opened[1][0] and len(marker) >= len(opened[1]):
            spans.append((opened[0], match.end()))
            opened = None
    if opened is not None:
        spans.append((opened[0], len(text)))
    return spans


def _entry_headings(text: str) -> list[tuple[int, str]]:
    """(offset, text) of each `## ` line of Markdown source outside fenced code, the whole line after `## ` kept."""
    found = markdown_headings(text, syntax=ENTRY_HEADING, fences=None, skip=fenced_spans(text),
                              line_breaks="newline", id_suffix=None)
    return [(heading.offset, heading.text) for heading in found]


def markdown_entry_dates(text: str) -> list[str]:
    """The dates of the dated entry headings in Markdown source, in file order."""
    dates = []
    for _, heading in _entry_headings(text):
        dated = _DATE.match(heading)
        if dated:
            dates.append(dated.group(0))
    return dates


def unchecked_spans(text: str, first: str | None, heading: re.Pattern | None = None) -> list[tuple[int, int]]:
    """(start, end) offsets of the entries dated before `first`.

    `heading` finds the level-two headings of rendered markup, HTML_HEADING;
    None reads Markdown source. An undated section belongs to the dated
    entry above it. A `## ` line inside a fenced code block of the Markdown
    source is not a heading, as in the rendered page.
    """
    if first is None:
        return []
    if heading is None:
        found = _entry_headings(text)
    else:
        found = [(match.start(), match.group(1).strip()) for match in heading.finditer(text)]
    spans: list[tuple[int, int]] = []
    entry_date, start = None, 0
    for position, title in found:
        dated = _DATE.match(title)
        if not dated:
            continue
        if entry_date is not None and entry_date < first:
            spans.append((start, position))
        entry_date, start = dated.group(0), position
    if entry_date is not None and entry_date < first:
        spans.append((start, len(text)))
    return spans


def within(spans: list[tuple[int, int]], offset: int) -> bool:
    return any(start <= offset < end for start, end in spans)
