"""Site-wide preservation checks for adapting documents to the chapter reader."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

import build
from chapter_layout import Structure, reader_page


class Content(HTMLParser):
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


class ChapterLayoutTests(unittest.TestCase):
    def test_public_anchors_and_original_content(self):
        text = '<h1 id="name">A guide</h1><p>Original introduction.</p><h2 id="first">First</h2><p>1.25 m</p><h3 id="sub">Detail</h3><pre>keep(x)</pre><h2 id="last">Last</h2><p>Done.</p>'
        markup, toc = reader_page([(None, text)], [['Overview', '#top'], ['First', '#first'], ['-Detail', '#sub'], ['Last', '#last']], 'Guide', '')
        ids = [node.attrs['id'] for root in Structure(markup).roots for node in root.descendants() if 'id' in node.attrs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({'name', 'first', 'sub', 'last'} <= set(ids))
        self.assertEqual([href for _, href in toc], ['#reader-introduction', '#first', '#last', '#sub'])
        self.assertIn('<pre>keep(x)</pre>', markup)
        self.assertIn('<h2>First</h2>', markup)

    def test_styling_host_and_local_tabs_remain(self):
        text = '<div class="contract-review"><h1>Guide</h1><p>Intro</p><section class="card" id="one"><h2>One</h2><button role="tab">Local</button><div role="tabpanel">Evidence</div></section></div>'
        markup, _ = reader_page([(None, text)], [['One', '#one']], 'Guide', '')
        self.assertIn('class="contract-review" data-reader-host', markup)
        self.assertIn('<button role="tab">Local</button>', markup)
        self.assertIn('<div role="tabpanel">Evidence</div>', markup)

    def test_multiple_group_introductions_and_duplicate_heading_aliases(self):
        chunks = [('A', '<p>First intro.</p><section class="card" id="first"><h2 id="first">First</h2></section>'),
                  ('B', '<p>Second intro.</p><h2 id="second">Second</h2>')]
        markup, toc = reader_page(chunks, [['First', '#first'], ['Second', '#second']], 'Guide', '')
        ids = [node.attrs['id'] for root in Structure(markup).roots for node in root.descendants() if 'id' in node.attrs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(toc), 4)
        self.assertTrue({'first', 'second'} <= set(ids))

    def test_every_live_page_preserves_evidence(self):
        site = build.tomllib.loads((build.SRC / 'site.toml').read_text())
        shell = (build.COMPONENTS / 'shell.html').read_text()
        reader_pages = set()
        topic_paths = build.topic_pages()
        # Every content page is covered; explicit forwarding pages, stubs of
        # pages converted to agent records and pages that opt out with
        # `reader = false` (the home page) have no chapter reader. New topics
        # must join this proof without a magic count.
        content_pages = {path for path in topic_paths
                         if 'data-page-redirect=' not in path.read_text()
                         and 'data-agent-record=' not in path.read_text()
                         and not re.search(r'^reader\s*=\s*false\s*$', path.read_text(), re.M)
                         and 'location.replace(' not in path.read_text()}
        for path in topic_paths:
            legacy = build.build_page(path, dict(site, chapter_reader=False), shell)
            current = build.build_page(path, site, shell)
            self.assertIsNotNone(legacy, path.name)
            self.assertIsNotNone(current, path.name)
            old, new = legacy[1], current[1]
            a, b = Content(old), Content(new)
            self.assertEqual(a.words, b.words, path.name + ': complete original text and code')
            self.assertEqual(a.links, b.links, path.name + ': report and cross-page links')
            self.assertEqual(a.media, b.media, path.name + ': figures and recording paths')
            self.assertFalse(set(a.ids) - set(b.ids), path.name + ': public anchors')
            self.assertEqual(re.findall(r'<table\b[\s\S]*?</table>', old), re.findall(r'<table\b[\s\S]*?</table>', new), path.name + ': all measurement tables')
            self.assertEqual(svg_content(old), svg_content(new), path.name + ': unchanged figure geometry')
            self.assertFalse(unresolved_svg_references(new) - unresolved_svg_references(old), path.name + ': no new broken figure references')
            old_folds = re.findall(r'<details\b[^>]*>', old)
            new_folds = re.findall(r'<details\b[^>]*>', new)
            self.assertEqual([fold for fold in old_folds if 'topic-overview' not in fold], [fold for fold in new_folds if 'topic-overview' not in fold], path.name + ': native/manual folds')
            if 'assets/chapter-reader.js' in new:
                reader_pages.add(path)
                self.assertNotIn('src="assets/toc.js"', new)
                self.assertNotIn('class="ptab-panel"', new)
                self.assertIn('data-fold-controls="columns"', new)
                # Scripting is an enhancement: every chapter remains in source.
                for card in re.findall(r'<section class="card(?: reader-adapted)?"[^>]*>', new):
                    self.assertNotRegex(card, r'\shidden\b')
        self.assertEqual(reader_pages, content_pages)
        self.assertFalse(build._errors, build._errors)
        print(f'{len(reader_pages)} reader pages preserve original text, code, links, media, public anchors, folds, tables and SVG geometry.')


if __name__ == '__main__':
    unittest.main()
