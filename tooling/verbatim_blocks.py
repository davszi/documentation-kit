"""Hash locks for source blocks a redesign keeps verbatim.

When a page is redesigned, the paragraphs, tables and callouts it keeps unchanged should stay exactly
as reviewed. A lock names a block by unique start text and the first end text after it and records the
SHA-256 of the block. `verify` reports every lock whose block is missing, ambiguous or changed, so a later
edit to kept evidence wording fails a check instead of passing silently.

    LOCKS = (("<p>The audit covered", "</p>", True, "<sha256>"), ...)
    problems = verbatim_blocks.verify(source_text, LOCKS)

`lock_lines` prints new lock tuples from the current text, for a reviewer to paste after confirming the
blocks are the ones intended.
"""
from __future__ import annotations

import hashlib


def block(source: str, start: str, end: str, inclusive: bool = True) -> str:
    """The text from `start` to the first `end` after it (including `end` when inclusive)."""
    if source.count(start) != 1:
        raise ValueError(f"start text occurs {source.count(start)} times: {start[:60]!r}")
    i = source.index(start)
    j = source.index(end, i + len(start))
    return source[i:j + len(end)] if inclusive else source[i:j]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def verify(source: str, locks, normalize=None) -> list[str]:
    """Problems, one per failing lock. `normalize(block) -> block` may remove approved wrapper changes."""
    problems = []
    for start, end, inclusive, expected in locks:
        try:
            text = block(source, start, end, inclusive)
        except ValueError as error:
            problems.append(str(error))
            continue
        if normalize:
            text = normalize(text)
        if digest(text) != expected:
            problems.append(f"changed block: {start[:60]!r}")
    return problems


def lock_lines(source: str, spans) -> str:
    """Python tuple lines for `(start, end, inclusive)` spans, hashed from `source`."""
    return "\n".join(f"    ({start!r},\n     {end!r}, {inclusive}, \"{digest(block(source, start, end, inclusive))}\"),"
                     for start, end, inclusive in spans)
