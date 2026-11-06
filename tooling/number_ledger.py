"""Number ledgers: every number a section shows has a declared, checked source.

A redesigned section (prose, generated figures, slide face) can show many numbers. A ledger lists each one
with the source that establishes it; `check` extracts every number from the section's visible text and
reports numbers without a source, sources whose value no longer matches, and ledger entries no longer shown.

Ledger (JSON):

    {"chapter": "results", "config": "configs/study.json",
     "facts": [{"value": "139", "kind": "extract", "expr": "data['adapted']['lower']", "note": "..."}, ...]}

Kinds:
  config         `pointer` (JSON pointer into the ledger's `config` file) equals the value
  config_text    the value occurs as a number in the text at `pointer`
  arithmetic     `expr` over `cfg` (the config) and `math` rounds to the value
  extract        `expr` over the project's evidence namespace rounds to the value
  extract_set    `expr` returns a list of strings; all must be shown, and all count as listed
  record         `pointer` into the JSON `file` rounds to the value
  text           `phrase` occurs in `file` and contains the value
  teaching       an illustrative value (axis tick, label); `note` says why it needs no evidence
  pinned_fragment  the text of `file` (locked elsewhere) is removed before counting
  kept_block     the block from `start` to `end` (locked by verbatim_blocks) is removed before counting

What counts: the check works on distinct unsigned values as written in the text. "3 seeds, 3 failures" needs
one source for 3; a value can have only one ledger entry. Signs are not part of a value ("−0.5" and "-0.5"
are 0.5), thousands commas are removed ("1,036" is 1036) and dates or scientific notation split into their
digit groups. Write ledger values the same way: unsigned, with or without thousands commas. Values are
compared at the precision written: "0.390" is checked to three decimals.

Expressions are executable project code. They run without Python builtins, with only the names the project
passes in `evidence` and a few helpers, but that is a convenience, not a sandbox: review ledger expressions as
code and never evaluate a ledger from an untrusted source.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re

# Numbers as written: 104, 0.500, 1,036, 3.7; a comma separates thousands only before exactly three digits.
NUMBER = re.compile(r"(?<![\w.])(?:\d{1,3}(?:,\d{3})+(?!\d)|\d+)(?:\.\d+)?")
SAFE = {"len": len, "min": min, "max": max, "sum": sum, "sorted": sorted, "abs": abs, "all": all, "any": any,
        "range": range, "str": str, "round": round, "zip": zip, "math": math}


class _Text(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def numbers(markup: str) -> set[str]:
    """Every number in the visible text of `markup` (script and style excluded), thousands commas removed."""
    text = " ".join(" ".join(_Text(markup).parts).split())
    return {value.replace(",", "") for value in NUMBER.findall(text)}


def pointer(document, path):
    for part in path.strip("/").split("/"):
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def decimals(value: str) -> int:
    return len(value.split(".")[1]) if "." in value else 0


def _remove_block(markup: str, fact: dict, kept, problems: list) -> str:
    """Remove one locked block (start to its first end, end included unless `inclusive` is false)."""
    label = f"{fact['start'][:60]!r}"
    if (fact["start"], fact["end"]) not in kept:
        problems.append(f"{label}: not a locked block")
        return markup
    if markup.count(fact["start"]) != 1:
        problems.append(f"{label}: block not shown exactly once")
        return markup
    i = markup.index(fact["start"])
    j = markup.find(fact["end"], i + len(fact["start"]))
    if j < 0:
        problems.append(f"{label}: end text {fact['end'][:40]!r} no longer follows the start")
        return markup
    return markup[:i] + markup[j + (len(fact["end"]) if fact.get("inclusive", True) else 0):]


def check(markup: str, ledger: dict, *, root: Path, evidence: dict | None = None,
          pinned=frozenset(), kept=frozenset()) -> list[str]:
    """Problems for one section. `pinned` and `kept` are the locked fragments and (start, end) blocks a
    ledger may remove; anything else must be listed."""
    problems = []
    config = json.loads((root / ledger["config"]).read_text()) if ledger.get("config") else {}
    namespace = {"__builtins__": {}, **SAFE, **(evidence or {})}
    for fact in ledger["facts"]:
        if fact["kind"] == "pinned_fragment":
            if fact["file"] not in pinned:
                problems.append(f"{fact['file']}: not a locked fragment")
                continue
            fragment = (root / fact["file"]).read_text()
            if markup.count(fragment) != 1:
                problems.append(f"{fact['file']}: fragment not shown exactly once")
            markup = markup.replace(fragment, "")
        elif fact["kind"] == "kept_block":
            markup = _remove_block(markup, fact, kept, problems)
    shown, listed, singles = numbers(markup), set(), set()
    for fact in ledger["facts"]:
        kind = fact["kind"]
        if kind in ("pinned_fragment", "kept_block"):
            continue
        try:
            if kind == "extract_set":
                values = eval(fact["expr"], dict(namespace))  # noqa: S307 - ledger expressions are reviewed project code
                missing = sorted(set(values) - shown)
                if missing or not values:
                    problems.append(f"{fact.get('note', fact['expr'])}: not shown {missing}")
                listed.update(values)
                continue
            value = fact["value"].replace(",", "")
            if value in singles:
                problems.append(f"{value}: listed twice")
            singles.add(value)
            listed.add(value)
            number, places = float(value), decimals(value)
            if kind == "config":
                ok = float(pointer(config, fact["pointer"])) == number
            elif kind == "config_text":
                rule = pointer(config, fact["pointer"])
                ok = value in numbers(" ".join(rule) if isinstance(rule, list) else str(rule))
            elif kind == "arithmetic":
                ok = round(eval(fact["expr"], {**namespace, "cfg": config}), places) == number  # noqa: S307
            elif kind == "extract":
                ok = round(eval(fact["expr"], dict(namespace)), places) == number  # noqa: S307
            elif kind == "record":
                ok = round(float(pointer(json.loads((root / fact["file"]).read_text()), fact["pointer"])), places) == number
            elif kind == "text":
                ok = fact["phrase"] in (root / fact["file"]).read_text() and value in numbers(fact["phrase"])
            elif kind == "teaching":
                ok = bool(fact.get("note"))
            else:
                problems.append(f"{value}: unknown kind {kind!r}")
                continue
            if not ok:
                problems.append(f"{value}: {kind} source does not give this value ({fact.get('note', '')})")
        except Exception as error:  # a broken expression or pointer is a ledger problem, not a crash
            problems.append(f"{fact.get('value', fact.get('expr', '?'))}: {type(error).__name__}: {error}")
    problems += [f"{value}: shown without a ledger source" for value in sorted(shown - listed)]
    problems += [f"{value}: in the ledger but no longer shown" for value in sorted(listed - shown)]
    return problems
