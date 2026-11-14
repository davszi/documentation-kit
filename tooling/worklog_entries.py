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


def configured_entry(site: dict, key: str):
    """The configured value of `worklog` or `open_work`, or its default path."""
    return site.get(key, ENTRY_DEFAULTS[key])


def links_checked_from(site: dict) -> str | None:
    """The configured cut-off date as `YYYY-MM-DD`, or None when unset.

    Raises ValueError with CUTOFF_ERROR for a value that is not an ISO date.
    """
    value = site.get("worklog_links_checked_from")
    if value is None:
        return None
    try:
        if isinstance(value, str):
            return date.fromisoformat(value).isoformat()
    except ValueError:
        pass
    raise ValueError(CUTOFF_ERROR)


def unchecked_spans(text: str, first: str | None, heading: re.Pattern = MARKDOWN_HEADING) -> list[tuple[int, int]]:
    """(start, end) offsets of the entries dated before `first`.

    `heading` finds the level-two headings: MARKDOWN_HEADING in the source,
    HTML_HEADING in rendered markup. An undated section belongs to the dated
    entry above it.
    """
    if first is None:
        return []
    spans: list[tuple[int, int]] = []
    entry_date, start = None, 0
    for match in heading.finditer(text):
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
