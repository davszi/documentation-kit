"""Check that the chapter reader keeps every page's content.

Each topic page is rendered twice, with the chapter reader and without it. The
two results must hold the same words, links, media, tables, folds and SVG
figures, and the reader may not drop an anchor. `docsite.py build
--check-reader` runs this for a project and writes nothing.
"""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from typing import Callable

from chapter_layout import Structure


class Content(HTMLParser):
    """Words, links, media and ids of a page's <main>, without reader-made parts."""

    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.stack, self.words, self.links, self.media, self.ids = [], Counter(), Counter(), Counter(), Counter()
        body = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', page)[1]
        self.feed(body)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        ignored = bool(self.stack and self.stack[-1][1]) or tag in {'script', 'style'} or 'data-reader-generated' in attrs or attrs.get('id') == 'chapter-reader' or 'ptabs' in attrs.get('class', '').split()
        svg = tag == 'svg' or bool(self.stack and self.stack[-1][2])
        if not ignored and not svg:
            if attrs.get('id'):
                self.ids[attrs['id']] += 1
            if tag == 'a':
                self.links[attrs.get('href', '')] += 1
            if tag in {'img', 'video', 'audio', 'source', 'iframe'}:
                self.media[(tag, tuple(sorted(attrs.items())))] += 1
        if tag not in Structure.VOID:
            self.stack.append((tag, ignored, svg))

    def handle_startendtag(self, tag, pairs):
        self.handle_starttag(tag, pairs)
        if tag not in Structure.VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1][0] == tag, tag
        self.stack.pop()

    def handle_data(self, text):
        if not self.stack or not self.stack[-1][1]:
            self.words.update(text.split())


def svg_content(page):
    normalized = []
    for svg in re.findall(r'<svg\b[^>]*>[\s\S]*?</svg>', page):
        svg = re.sub(r'\bid="[^"]+"', 'id="local"', svg)
        svg = re.sub(r'url\(#[^)]*\)', 'url(#local)', svg)
        svg = re.sub(r'((?:xlink:)?href=")#[^"]+"', r'\1#local"', svg)
        normalized.append(re.sub(r'\s+', ' ', svg).strip())
    return Counter(normalized)


def unresolved_svg_references(page):
    identifiers = set(re.findall(r'\bid="([^"]+)"', page))
    references = {a or b for a, b in re.findall(r'url\(#([^)]*)\)|(?:xlink:)?href="#([^"]+)"', page)}
    return references - identifiers


def _has_no_reader(source: str) -> bool:
    """Forwarding pages, agent-record stubs and `reader = false` pages get no reader."""
    return ('data-page-redirect=' in source or 'data-agent-record=' in source
            or 'location.replace(' in source
            or bool(re.search(r'^reader\s*=\s*false\s*$', source, re.M)))


def _sample(counter: Counter) -> str:
    items = [str(item) for item in list(counter)[:5]]
    return ', '.join(items) + (' …' if len(counter) > 5 else '')


def page_problems(name: str, old: str, new: str, *, expects_reader: bool) -> list[str]:
    """Differences between a page rendered without (`old`) and with (`new`) the reader."""
    problems = []
    a, b = Content(old), Content(new)
    for label, before, after in (('text or code', a.words, b.words), ('links', a.links, b.links),
                                 ('figures or media', a.media, b.media)):
        if before != after:
            lost, added = before - after, after - before
            detail = '; '.join(part for part in ('lost ' + _sample(lost) if lost else '',
                                                 'added ' + _sample(added) if added else '') if part)
            problems.append(f'{name}: the chapter reader changes {label}: {detail}')
    dropped = sorted(set(a.ids) - set(b.ids))
    if dropped:
        problems.append(f'{name}: the chapter reader drops anchors: ' + ', '.join(dropped[:5]))
    if re.findall(r'<table\b[\s\S]*?</table>', old) != re.findall(r'<table\b[\s\S]*?</table>', new):
        problems.append(f'{name}: the chapter reader changes a table')
    if svg_content(old) != svg_content(new):
        problems.append(f'{name}: the chapter reader changes SVG figure geometry')
    broken = sorted(unresolved_svg_references(new) - unresolved_svg_references(old))
    if broken:
        problems.append(f'{name}: the chapter reader breaks figure references: ' + ', '.join(broken[:5]))
    folds = [[fold for fold in re.findall(r'<details\b[^>]*>', page) if 'topic-overview' not in fold]
             for page in (old, new)]
    if folds[0] != folds[1]:
        problems.append(f'{name}: the chapter reader changes folds')
    has_reader = 'assets/chapter-reader.js' in new
    if has_reader:
        if 'src="assets/toc.js"' in new or 'class="ptab-panel"' in new:
            problems.append(f'{name}: the reader page still carries the page-tab layout')
        if 'data-fold-controls="columns"' not in new:
            problems.append(f'{name}: the reader page has no fold controls')
        # Scripting is an enhancement: every chapter remains in source.
        if any(re.search(r'\shidden\b', card)
               for card in re.findall(r'<section class="card(?: reader-adapted)?"[^>]*>', new)):
            problems.append(f'{name}: the reader page hides a chapter without scripting')
    if has_reader != expects_reader:
        problems.append(f'{name}: ' + ('has no chapter reader' if expects_reader
                                       else 'has a chapter reader although it opts out or forwards'))
    return problems


def reader_content_problems(pages: list[Path], render: Callable[[Path, bool], str | None],
                            errors: list[str], *, root: Path | None = None) -> tuple[int, list[str]]:
    """Compare every page with and without the reader.

    `render(path, reader)` returns the page's HTML or None; `errors` is the
    builder's error list, read after each render. Returns the number of pages
    that carry the reader and the problems found.
    """
    problems, reader_pages = [], 0
    for path in pages:
        name = path.relative_to(root).as_posix() if root and path.is_relative_to(root) else path.name
        seen = len(errors)
        old, new = render(path, False), render(path, True)
        if old is None or new is None or len(errors) > seen:
            problems.append(f'{name}: does not build: ' + '; '.join(errors[seen:] or ['no output']))
            continue
        found = page_problems(name, old, new, expects_reader=not _has_no_reader(path.read_text()))
        problems.extend(found)
        reader_pages += 'assets/chapter-reader.js' in new
    return reader_pages, problems


def report(pages: list[Path], render: Callable[[Path, bool], str | None], errors: list[str],
           *, root: Path | None = None) -> int:
    """Print the result for the command line; the return value is the exit status."""
    reader_pages, problems = reader_content_problems(pages, render, errors, root=root)
    for problem in problems:
        print('ERROR: ' + problem, file=sys.stderr)
    if problems:
        return 1
    print(f'{reader_pages} reader pages preserve original text, code, links, media, public anchors, folds, tables and SVG geometry.')
    return 0
