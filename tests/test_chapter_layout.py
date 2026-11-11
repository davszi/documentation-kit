"""Site-wide preservation checks for adapting documents to the chapter reader."""
from pathlib import Path
import tempfile
import unittest

import build
from chapter_layout import Structure, reader_page
from reader_content import page_problems, reader_content_problems


class ChapterLayoutTests(unittest.TestCase):
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
