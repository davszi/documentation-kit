"""Site-wide preservation checks for adapting documents to the chapter reader."""
from pathlib import Path
import tempfile
import unittest

import build
from chapter_layout import Structure, reader_page
from reader_content import page_problems, reader_content_problems


class ChapterLayoutTests(unittest.TestCase):
    def test_fold_marker_can_start_open(self):
        source = ('<!-- fold: math (open) Derivation of the bound -->\nProof.\n<!-- /fold -->\n\n'
                  '<!-- fold: code Listing -->\nx = 1\n<!-- /fold -->\n')
        markup = build.folds_to_html(source, 'fixture')
        self.assertIn('<details class="fold fold-math" data-fold="math" open>\n'
                      '<summary><span class="fold-tag">math</span> Derivation of the bound</summary>', markup)
        self.assertIn('<details class="fold fold-code" data-fold="code">\n', markup)
        self.assertNotIn('(open)', markup)

    def test_fold_without_a_kind_has_no_badge(self):
        source = ('<!-- fold: detail Math of the old layout -->\nText.\n<!-- /fold -->\n\n'
                  '<!-- fold: detail (open) Notes -->\nMore.\n<!-- /fold -->\n')
        errors = len(build._errors)
        markup = build.folds_to_html(source, 'fixture')
        self.assertEqual(len(build._errors), errors)
        # A title that starts with a kind's name stays the title.
        self.assertIn('<details class="fold fold-detail" data-fold="detail">\n'
                      '<summary>Math of the old layout</summary>', markup)
        self.assertIn('<details class="fold fold-detail" data-fold="detail" open>\n<summary>Notes</summary>', markup)
        self.assertNotIn('fold-tag', markup)

    def test_unknown_fold_kind_is_an_error(self):
        errors = len(build._errors)
        try:
            build.folds_to_html('<!-- fold: note Aside -->\nText.\n<!-- /fold -->\n', 'fixture')
            self.assertEqual(build._errors[errors:], ['fixture: unbalanced fold markers (0 open, 1 close)'])
        finally:
            del build._errors[errors:]

    def test_source_offsets_count_only_lf_inside_opaque_scripts(self):
        for separator in ('\u2028', '\r', '\f'):
            with self.subTest(separator=repr(separator)):
                opaque = ('<script>const text = "before' + separator + 'after";</script>'
                          '<script type="application/json">{"text":"before' + separator + 'after"}</script>')
                opening = '<a id="later" href="index.html#part">'
                source = '<div>' + opaque + '\n' + opening + 'Label</a></div>'
                nodes = [node for root in Structure(source).roots for node in root.descendants()]
                anchor = next(node for node in nodes if node.tag == 'a')
                self.assertEqual(anchor.start, source.index(opening))
                self.assertEqual(source[anchor.start:anchor.opening_end], opening)
                self.assertEqual(source[anchor.closing_start:anchor.end], '</a>')
                scripts = [node for node in nodes if node.tag == 'script']
                self.assertEqual(''.join(source[node.start:node.end] for node in scripts), opaque)

    def test_public_anchors_and_original_content(self):
        text = '<h1 id="name">A guide</h1><p>Original introduction.</p><h2 id="first">First</h2><p>1.25 m</p><h3 id="sub">Detail</h3><pre>keep(x)</pre><h2 id="last">Last</h2><p>Done.</p>'
        markup, toc = reader_page([(None, text)], [['Overview', '#top'], ['First', '#first'], ['-Detail', '#sub'], ['Last', '#last']], 'Guide', '')
        ids = [node.attrs['id'] for root in Structure(markup).roots for node in root.descendants() if 'id' in node.attrs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({'name', 'first', 'sub', 'last'} <= set(ids))
        # Changed in 5.8.0: the text before the first chapter is no chapter of its own. It opens the first
        # chapter, after that chapter's heading, and keeps the id an Introduction chapter had.
        self.assertEqual([href for _, href in toc], ['#first', '#last', '#sub'])
        self.assertNotIn('Introduction</h2>', markup)
        first = markup[markup.index('id="first"'):markup.index('id="last"')]
        self.assertLess(first.index('<h2>First</h2>'), first.index('class="reader-opening" id="reader-introduction"'))
        self.assertLess(first.index('Original introduction.'), first.index('1.25 m'))
        self.assertIn('data-reader-opening="2"', first)
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
        # Changed in 5.8.0: each group's opening joins its first chapter, so two entries, not four.
        self.assertEqual(len(toc), 2)
        self.assertTrue({'first', 'second', 'reader-introduction', 'reader-introduction-intro'} <= set(ids))

    def test_an_opening_is_marked_for_lint_unless_kept_or_a_record(self):
        text = '<h1>A guide</h1><p>Three words here.</p><section class="card" id="one"><h2>One</h2><p>Body.</p></section>'
        toc = [['One', '#one']]
        warned, _ = reader_page([(None, text)], toc, 'Guide', '')
        self.assertIn('data-reader-opening="3"', warned)
        kept, _ = reader_page([(None, text)], toc, 'Guide', '', opening='keep')
        self.assertIn('data-reader-opening-kept=""', kept)
        self.assertNotIn('data-reader-opening="', kept)
        record, _ = reader_page([(None, text)], toc, 'Guide', '', opening='record')
        self.assertIn('class="reader-opening"', record)
        self.assertNotIn('data-reader-opening', record)
        # Inside a card the opening follows the card's heading; the card keeps its own markup.
        self.assertLess(warned.index('<h2>One</h2>'), warned.index('Three words here.'))
        self.assertLess(warned.index('Three words here.'), warned.index('<p>Body.</p>'))
        # Only a style block or a comment before the first chapter is not text: nothing to decide.
        silent, _ = reader_page([(None, '<style>.x{}</style><!-- note --><h2 id="a">A</h2><p>B</p>')], [['A', '#a']], 'Guide', '')
        self.assertNotIn('data-reader-opening', silent)

    def test_an_opening_with_a_slide_face_stays_a_chapter(self):
        # Joined, the face would no longer open a chapter and lint would report an error that 5.7.0 did not.
        face = '<div class="slide-face" data-slide-face=""><p>Face</p></div>'
        text = '<h1>T</h1>' + face + '<p>Opening words.</p><h2 id="first">First</h2><p>Body.</p>'
        markup, toc = reader_page([(None, text)], [['First', '#first']], 'Guide', '')
        self.assertEqual([href for _, href in toc], ['#reader-introduction', '#first'])
        self.assertNotIn('reader-opening', markup)
        intro = markup[markup.index('id="reader-introduction"'):markup.index('id="first"')]
        self.assertIn('data-slide-face', intro)

    def test_a_styling_host_page_passes_the_decision_on(self):
        text = '<div class="host"><h1>T</h1><p>Four words stand here.</p><h2 id="a">A</h2><p>B</p></div>'
        kept, _ = reader_page([(None, text)], [['A', '#a']], 'Guide', '', opening='keep')
        self.assertIn('data-reader-opening-kept=""', kept)
        self.assertNotIn('data-reader-opening="', kept)
        record, _ = reader_page([(None, text)], [['A', '#a']], 'Guide', '', opening='record')
        self.assertNotIn('data-reader-opening', record)

    def test_the_opening_never_lands_inside_a_fold_or_a_column(self):
        for holder, inner in (('<details>', '<details><summary>s</summary><h3>Deep</h3><p>x</p></details><p>After.</p>'),
                              ('bs-grid', '<div class="bs-grid g2"><div><h3>Left</h3><p>x</p></div><div><p>y</p></div></div>')):
            with self.subTest(holder=holder):
                text = '<h1>T</h1><p>Opening words.</p><section class="card" id="a">' + inner + '</section>'
                markup, _ = reader_page([(None, text)], [['A', '#a']], 'Guide', '')
                card = markup[markup.index('<section class="card">'):]
                # At the start of the card, before the block that holds the deep heading.
                self.assertLess(card.index('Opening words.'), card.index(holder))
        # A card nested at the start of the chapter still counts: the opening follows its heading.
        nested = '<h1>T</h1><p>Opening words.</p><section class="card" id="a"><section class="card"><h2>A</h2><p>B</p></section></section>'
        markup, _ = reader_page([(None, nested)], [['A', '#a']], 'Guide', '')
        self.assertLess(markup.index('<h2>A</h2>'), markup.index('Opening words.'))
        self.assertLess(markup.index('Opening words.'), markup.index('<p>B</p>'))

    def test_a_page_without_chapters_keeps_its_text_as_one_chapter(self):
        markup, toc = reader_page([(None, '<h1>A guide</h1><p>Only text.</p>')], [['Overview', '#top']], 'Guide', '')
        self.assertEqual([href for _, href in toc], ['#reader-introduction'])
        self.assertNotIn('reader-opening', markup)

    def test_every_live_page_preserves_evidence(self):
        site = build.tomllib.loads((build.SRC / 'site.toml').read_text())
        shell = (build.COMPONENTS / 'shell.html').read_text()

        def render(path, reader):
            page = build.build_page(path, site if reader else dict(site, chapter_reader=False), shell)
            return page and page[1]

        # The same comparison a project runs with `docsite.py build --check-reader`.
        reader_pages, problems = reader_content_problems(build.topic_pages(), render, build._errors, root=build.REPO)
        self.assertEqual(problems, [])
        self.assertFalse(build._errors, build._errors)
        self.assertGreater(reader_pages, 0)
        print(f'{reader_pages} reader pages preserve original text, code, links, media, public anchors, folds, tables and SVG geometry.')

    def test_reader_content_check_names_what_a_page_lost(self):
        plain = ('<main><h2 id="first">First</h2><p>Measured 1.25 m.</p><a href="report.html">report</a>'
                 '<img src="plot.png"><table><tr><td>1</td></tr></table><details class="fold"></details></main>')
        reader = ('<main><script src="assets/chapter-reader.js"></script><div data-fold-controls="columns"></div>'
                  '<section class="card" id="first"><h2>First</h2><p>Measured 1.25 m.</p><a href="report.html">report</a>'
                  '<img src="plot.png"><table><tr><td>1</td></tr></table><details class="fold"></details></section></main>')
        self.assertEqual(page_problems('guide', plain, reader, expects_reader=True), [])
        damaged = reader.replace('1.25 m.', 'm.').replace('<a href="report.html">report</a>', 'report').replace(' id="first"', '')
        problems = page_problems('guide', plain, damaged, expects_reader=True)
        self.assertIn('guide: the chapter reader changes text or code: lost 1.25', problems)
        self.assertIn('guide: the chapter reader changes links: lost report.html', problems)
        self.assertIn('guide: the chapter reader drops anchors: first', problems)
        self.assertEqual(page_problems('guide', plain, plain, expects_reader=True), ['guide: has no chapter reader'])
        self.assertEqual(page_problems('guide', plain, plain, expects_reader=False), [])
        # A page that does not build is reported by name with the builder's error.
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'index.md'
            source.write_text('text')
            errors = []

            def failing(path, with_reader):
                errors.append('index.md: bad frontmatter')
                return None

            self.assertEqual(reader_content_problems([source], failing, errors, root=Path(folder)),
                             (0, ['index.md: does not build: index.md: bad frontmatter; index.md: bad frontmatter']))


if __name__ == '__main__':
    unittest.main()
