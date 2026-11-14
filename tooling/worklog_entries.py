"""Which file is the worklog, how its entries are dated, and which keep checked links.

Lint and build share these rules. A worklog entry is a level-two section whose
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

ENTRY_DEFAULTS = {"worklog": "docs/worklog.md", "open_work": "docs/open/OPEN.md"}
CUTOFF_ERROR = 'worklog_links_checked_from must be a date written as "YYYY-MM-DD"'

# Level-two headings in Markdown source and in rendered HTML; group 1 is the
# heading text, which starts with the entry's date.
MARKDOWN_HEADING = re.compile(r"(?m)^## (.*)$")
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


def _fenced_spans(text: str) -> list[tuple[int, int]]:
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


def unchecked_spans(text: str, first: str | None, heading: re.Pattern = MARKDOWN_HEADING) -> list[tuple[int, int]]:
    """(start, end) offsets of the entries dated before `first`.

    `heading` finds the level-two headings: MARKDOWN_HEADING in the source,
    HTML_HEADING in rendered markup. An undated section belongs to the dated
    entry above it. A `## ` line inside a fenced code block of the Markdown
    source is not a heading, as in the rendered page.
    """
    if first is None:
        return []
    fenced = _fenced_spans(text) if heading is MARKDOWN_HEADING else []
    spans: list[tuple[int, int]] = []
    entry_date, start = None, 0
    for match in heading.finditer(text):
        if within(fenced, match.start()):
            continue
        dated = _DATE.match(match.group(1).strip())
        if not dated:
            continue
        if entry_date is not None and entry_date < first:
            spans.append((start, match.start()))
        entry_date, start = dated.group(0), match.start()
    if entry_date is not None and entry_date < first:
        spans.append((start, len(text)))
    return spans


def within(spans: list[tuple[int, int]], offset: int) -> bool:
    return any(start <= offset < end for start, end in spans)
