#!/usr/bin/env python3
"""Extract chapter slide faces from built pages into one presentation deck.

Reads the generated pages under .build/docs/html (run the build first; the
docsite.py ``slides`` command does so) and writes .build/slides/<name>.html.
Faces are copied byte-for-byte; only relative URLs are re-rooted so the deck
reuses the built site's assets. The deck lives outside .build/docs so the
site's stray-file check and publication bundle are unaffected.

Selection: ``--select <slug>`` takes every face on a page in chapter order;
``--select <slug>#<chapter-id>,<chapter-id>`` takes the named chapters in the
given order. Repeat ``--select`` to combine pages.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import sys

from chapter_layout import Structure, label
from site_paths import OUTPUT_ROOT, KIT_SITE

DECK_ROOT = OUTPUT_ROOT.parent / "slides"
SITE_PREFIX = "../docs/html/"
_URL_ATTR = re.compile(
    r'''(?P<lead>\s(?:xlink:href|href|src|poster|data|data-gif|data-poster|data-src)\s*=\s*)(?P<q>["\'])(?P<v>.*?)(?P=q)''', re.I | re.S)
_SRCSET = re.compile(r'''(?P<lead>\ssrcset\s*=\s*)(?P<q>["\'])(?P<v>.*?)(?P=q)''', re.I | re.S)
_CSS_URL = re.compile(r'''url\(\s*(?P<q>["\']?)(?P<v>[^)"\']+)(?P=q)\s*\)''', re.I)
_ID_ATTR = re.compile(r'''(\sid\s*=\s*)(["\'])(.*?)\2''', re.I)
_ID_REFS = re.compile(r'''(\s(?:aria-labelledby|aria-describedby|aria-controls|for)\s*=\s*)(["\'])(.*?)\2''', re.I)
_STYLESHEET = re.compile(r'<link\s+rel="stylesheet"\s+href="([^"]+)">')
_BODY_CLASS = re.compile(r'<body[^>]*\bclass="([^"]*)"')
_KATEX = "assets/katex/katex.min.js"


def _site_url(value: str, slug: str, local_ids: dict[str, str]) -> str:
    """Re-root one URL from the built page into the deck folder."""
    if not value or re.match(r"^(?:[a-z][a-z0-9+.-]*:|/|\.\./docs/html/)", value, re.I):
        return value
    if value.startswith("#"):
        # A reference to something on the slide stays local (under its new id);
        # anything else points back into the full page.
        target = value[1:]
        return "#" + local_ids[target] if target in local_ids else f"{SITE_PREFIX}{slug}.html{value}"
    return SITE_PREFIX + value


def reroot(markup: str, slug: str = "", local_ids: dict[str, str] | None = None) -> str:
    """Re-root every relative URL (attributes, srcset, inline CSS url()) for the deck."""
    local_ids = local_ids or {}
    markup = _URL_ATTR.sub(lambda m: m["lead"] + m["q"] + _site_url(m["v"], slug, local_ids) + m["q"], markup)
    markup = _SRCSET.sub(lambda m: m["lead"] + m["q"] + ", ".join(
        " ".join([_site_url(part.split()[0], slug, local_ids), *part.split()[1:]])
        for part in m["v"].split(",") if part.strip()) + m["q"], markup)
    return _CSS_URL.sub(lambda m: "url(" + m["q"] + _site_url(m["v"], slug, local_ids) + m["q"] + ")", markup)


def isolate_ids(markup: str, prefix: str) -> tuple[str, dict[str, str]]:
    """Prefix ids so faces from several pages can share one document (SVG
    gradients, clip paths, labels). Returns the markup and the old→new map."""
    ids = {value: prefix + value for _, _, value in _ID_ATTR.findall(markup) if value}
    markup = _ID_ATTR.sub(lambda m: m[1] + m[2] + ids.get(m[3], m[3]) + m[2], markup)
    return _ID_REFS.sub(lambda m: m[1] + m[2] + " ".join(ids.get(v, v) for v in m[3].split()) + m[2], markup), ids


def chapters(page: str) -> list[dict]:
    """Chapter sections in reading order, each with its id, title and face markup.

    Reader pages mark chapters with data-reader-chapter (or reader-adapted);
    pages without the reader use their outermost section.card elements."""
    nodes = list(_walk(Structure(page).roots))
    marked = [n for n in nodes if n.tag == "section"
              and ("data-reader-chapter" in n.attrs or "reader-adapted" in n.attrs.get("class", "").split())]
    if not marked:
        cards = [n for n in nodes if n.tag == "section" and "card" in n.attrs.get("class", "").split()]
        marked = [n for n in cards if not any(o is not n and o.start < n.start < o.end for o in cards)]
    found = []
    for node in marked:
        face = next((n for n in node.descendants() if "data-slide-face" in n.attrs), None)
        heading = next((n for n in node.descendants() if n.tag in {"h2", "h3"}
                        and not (face and face.start <= n.start < face.end)), None)
        identifier = node.attrs.get("id") or (heading.attrs.get("id", "") if heading else "")
        found.append({
            "id": identifier,
            "number": len(found) + 1,
            "title": label(page[heading.opening_end:heading.closing_start]) if heading else identifier,
            "face": page[face.start:face.end] if face else None,
        })
    return found


def _walk(roots):
    for root in roots:
        yield from root.descendants()


def parse_selection(values: list[str]) -> list[tuple[str, list[str] | None]]:
    out = []
    for value in values:
        slug, _, ids = value.partition("#")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug):
            raise ValueError(f"invalid page slug in --select: {value!r}")
        out.append((slug, [i for i in ids.split(",") if i] if ids else None))
    return out


def build_deck(selection, *, title: str) -> tuple[str, list[str]]:
    frames, sheets, body_classes, problems = [], [], [], []
    uses_math = False
    for slug, wanted in selection:
        path = OUTPUT_ROOT / "html" / f"{slug}.html"
        if not path.is_file():
            problems.append(f"{slug}: built page missing at {path}; build the site first")
            continue
        page = path.read_text()
        for sheet in _STYLESHEET.findall(page):
            if sheet not in sheets:
                sheets.append(sheet)
        match = _BODY_CLASS.search(page)
        if match:
            body_classes.extend(c for c in match[1].split() if c not in body_classes)
        found = chapters(page)
        by_id = {c["id"]: c for c in found}
        if wanted is None:
            picked = [c for c in found if c["face"]]
            if not picked:
                problems.append(f"{slug}: no chapter has a slide face")
        else:
            picked = []
            for chapter_id in wanted:
                chapter = by_id.get(chapter_id)
                if chapter is None:
                    problems.append(f"{slug}#{chapter_id}: no such chapter")
                elif not chapter["face"]:
                    problems.append(f"{slug}#{chapter_id}: chapter has no slide face")
                else:
                    picked.append(chapter)
        if _KATEX in page:
            uses_math = True
        for chapter in picked:
            number = f'{chapter["number"]:02d}'
            face = re.sub(r'(<p\b[^>]*\bclass="[^"]*\bslide-eyebrow\b[^"]*"[^>]*>)',
                          lambda m: m[1] + f'<span class="slide-number">{number} · </span>', chapter["face"], count=1)
            face, local_ids = isolate_ids(face, f"{slug}--{chapter['id']}--")
            face = reroot(face, slug, local_ids)
            source = f"{slug}.html#{chapter['id']}"
            frames.append(
                f'<section class="deck-frame" id="{html.escape(slug + "--" + chapter["id"], quote=True)}" '
                f'aria-label="{html.escape(number + " " + chapter["title"], quote=True)}">\n{face}\n'
                f'<a class="deck-source" href="{SITE_PREFIX}{html.escape(source, quote=True)}">{html.escape(chapter["title"])} · full chapter</a>\n</section>')
    if not any(sheet.partition("?")[0] == "assets/slide-face.css" for sheet in sheets):
        sheets.append("assets/slide-face.css")
    head = "".join(f'<link rel="stylesheet" href="{SITE_PREFIX}{html.escape(s, quote=True)}">\n' for s in sheets)
    deck_css = (KIT_SITE / "components" / "slide-deck.css").read_text()
    deck_js = (KIT_SITE / "components" / "slide-deck.js").read_text()
    document = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
        f"<title>{html.escape(title)}</title>\n{head}<style>\n{deck_css}</style>\n</head>\n"
        f'<body class="{html.escape(" ".join(["slide-deck-page", *body_classes]), quote=True)}">\n'
        f'<header class="deck-bar"><strong>{html.escape(title)}</strong>'
        f'<span class="deck-count" data-deck-count>{len(frames)} slides</span>'
        '<button type="button" data-deck-present>Present <kbd>P</kbd></button>'
        '<button type="button" data-deck-print>Print / PDF</button></header>\n'
        '<main class="slide-deck" data-slide-deck>\n' + "\n".join(frames) + "\n</main>\n"
        f"<script>\n{deck_js}</script>\n" + (math_scripts() if uses_math else "") + "</body>\n</html>\n")
    return document, problems


def math_scripts() -> str:
    """KaTeX for faces taken from math pages; the stylesheet arrives with the page's links."""
    return (f'<script defer src="{SITE_PREFIX}assets/katex/katex.min.js"></script>\n'
            f'<script defer src="{SITE_PREFIX}assets/katex/contrib/auto-render.min.js"></script>\n'
            "<script>\ndocument.addEventListener('DOMContentLoaded', function () {\n"
            "  renderMathInElement(document.querySelector('.slide-deck'), {\n"
            "    delimiters: [{left: '$$', right: '$$', display: true}, {left: '\\\\(', right: '\\\\)', display: false}],\n"
            "    ignoredTags: ['pre', 'code', 'script', 'style']\n  });\n});\n</script>\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--select", action="append", required=True, help="slug or slug#chapter,chapter (repeatable)")
    parser.add_argument("--out", required=True, help="deck file name without extension")
    parser.add_argument("--title", default="Slides")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", args.out):
        parser.error("--out must be a simple lowercase name")
    try:
        selection = parse_selection(args.select)
    except ValueError as problem:
        parser.error(str(problem))
    document, problems = build_deck(selection, title=args.title)
    if problems:
        for problem in problems:
            print("error: " + problem, file=sys.stderr)
        return 1
    DECK_ROOT.mkdir(parents=True, exist_ok=True)
    destination = DECK_ROOT / f"{args.out}.html"
    destination.write_text(document)
    count = document.count('class="deck-frame"')
    print(f"Wrote {count} slides to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
