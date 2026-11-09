"""Source-bound checks for the optional publication overlay; no site build."""
from pathlib import Path
import tempfile
import unittest

from publication import export_pages


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / 'project'
        self.generated = self.base / 'generated'
        self.destination = self.base / 'published'
        for directory in (self.root, self.generated, self.destination):
            directory.mkdir()
        self.tracked = set()
        self.public = set()

    def put(self, directory, name, content=b'content'):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode() if isinstance(content, str) else content)
        return path

    def resource(self, name, public=False, content=b'content'):
        self.put(self.root, name, content)
        self.tracked.add(name)
        if public:
            self.put(self.destination, name, content)
            self.public.add(name)

    def export(self, **kwargs):
        options = dict(root=self.root, tracked=self.tracked, pages=('index.html',), public_files=self.public)
        options.update(kwargs)
        return export_pages(self.generated, self.destination, **options)

    def test_original_overlay_output_is_byte_exact(self):
        self.resource('docs/chart.svg', public=True)
        self.resource('evidence/report.html', public=True)
        self.resource('notes.md', public=True)
        self.resource('configs/run.json', public=True)
        # This admitted directory remains a source link, even when not tracked.
        (self.root / 'reports').mkdir()
        opaque = '''<script type="application/json">{"html":"<a href='index.html'>opaque</a>","x":"_media/docs/chart.svg"}</script>
<script>const x = '<a href="index.html">opaque</a>'; const y = `href="_media/docs/chart.svg"`;</script>'''
        source = ('<!doctype html>\r\n<html><head>' + opaque + '</head><body id="keep">\n'
                  '<a id="home" href="index.html#top">Home</a>\n'
                  '<img id="chart" src="_media/docs/chart.svg" alt="same">\n'
                  '<a class="source" href="https://example.test/blob/report" data-repo-path="evidence/report.html" data-repo-fragment="details">Report <em>label</em></a>\n'
                  '<a href="https://example.test/blob/note" data-repo-path="notes.md" data-repo-fragment="x">Notes</a>\n'
                  '<a href="https://example.test/blob/config" data-repo-path="configs/run.json" data-repo-fragment="">Config</a>\n'
                  '<a href="https://example.test/blob/local" data-repo-path="results/local.html" data-repo-fragment="x"><b>Local label</b></a>\n'
                  '<a href="https://example.test/tree/reports" data-repo-path="reports">Directory</a>\n'
                  '</body></html>')
        self.put(self.generated, 'index.html', source)
        self.put(self.generated, '_media/docs/chart.svg')
        expected = (source.replace('src="_media/docs/chart.svg"', 'src="docs/chart.svg"')
                    .replace('href="https://example.test/blob/report" data-repo-path="evidence/report.html" data-repo-fragment="details"',
                             'href="evidence/report.html#details"')
                    .replace('<a href="https://example.test/blob/local" data-repo-path="results/local.html" data-repo-fragment="x"><b>Local label</b></a>',
                             '<span class="local-evidence" title="Local evidence file; not published"><b>Local label</b></span>'))
        exported = self.export(private_suffixes=('.md', '.py', '.toml'), private_prefixes=('configs/',))
        self.assertEqual((self.destination / 'index.html').read_bytes(), expected.encode())
        self.assertEqual(set(exported), {'index.html', '_media/docs/chart.svg'})
        self.assertEqual((self.destination / '_media/docs/chart.svg').read_bytes(), b'content')
        self.assertEqual((self.generated / 'index.html').read_bytes(), source.encode())

    def test_generated_outputs_keep_their_names_and_relative_links(self):
        source = ('<main><a href="./about.html?x=1&#38;y=2#part">About</a>'
                  '<a href="evidence/../about.html#part">Normalized destination</a>'
                  '<a href="%61bout.html">Encoded destination</a>'
                  '<a href="evidence/report.html#proof">Evidence</a>'
                  '<a href="index.html#intro">Home</a></main>')
        evidence = '<a href="../index.html?view=one#intro">Start</a>'
        self.put(self.generated, 'index.html', source)
        self.put(self.generated, 'about.html', '<p>About</p>')
        self.put(self.generated, 'evidence/report.html', evidence)
        self.put(self.generated, 'assets/data.json', b'{"opaque":"index.html"}')
        exported = self.export(pages=('index.html', 'evidence/report.html'))
        self.assertEqual(set(exported), {'index.html', 'about.html', 'evidence/report.html', 'assets/data.json'})
        self.assertEqual({path.relative_to(self.destination).as_posix()
                          for path in self.destination.rglob('*') if path.is_file()}, set(exported))
        self.assertEqual((self.destination / 'index.html').read_bytes(), source.encode())
        self.assertEqual((self.destination / 'evidence/report.html').read_text(), evidence)
        self.assertEqual((self.destination / 'assets/data.json').read_bytes(), b'{"opaque":"index.html"}')

    def test_actual_attributes_only_with_mixed_quotes_queries_and_fragments(self):
        self.resource('fig.svg', public=True)
        self.resource('paper.html', public=True)
        source = '''<html><body>
<img data-example='src="_media/fig.svg"' src='_media/fig.svg?mode=one&amp;x=2#part' id="same">
<img src=_media/fig.svg#bare>
<img src="https://example.test/_media/fig.svg#remote">
<img src="//example.test/_media/fig.svg">
<a data-example="data-repo-path='paper.html'" href='https://source/paper' data-repo-path='paper.html' data-repo-fragment='a&amp;b'>Paper</a>
<!-- <img src="_media/fig.svg"> -->
<style>.x::after {content:'<img src="_media/fig.svg">';}</style>
<script type='application/json'>{"text":"<img src='_media/fig.svg'>"}</script>
<script>let literal = '<a data-repo-path="paper.html">script</a>';</script>
</body></html>'''
        self.put(self.generated, 'index.html', source)
        expected = source.replace("src='_media/fig.svg?mode=one&amp;x=2#part'", "src='fig.svg?mode=one&amp;x=2#part'")
        expected = expected.replace('src=_media/fig.svg#bare', 'src=fig.svg#bare')
        expected = expected.replace("href='https://source/paper' data-repo-path='paper.html' data-repo-fragment='a&amp;b'",
                                    "href='paper.html#a&amp;b'")
        self.export()
        self.assertEqual((self.destination / 'index.html').read_bytes(), expected.encode())

    def test_non_lf_separators_in_scripts_do_not_shift_later_edits(self):
        self.resource('fig.svg', public=True)
        for separator in (' ', '\r', '\f'):
            with self.subTest(separator=repr(separator)):
                opaque = ('<script>const value = "before' + separator + 'after";</script>'
                          '<script type="application/json">{"html":"before' + separator
                          + '<img src=\'_media/fig.svg\'>"}</script>')
                source = '<main>' + opaque + '\n<img src="_media/fig.svg#later"></main>'
                self.put(self.generated, 'index.html', source)
                self.export(replace=('index.html',))
                expected = source.replace('src="_media/fig.svg#later"', 'src="fig.svg#later"')
                self.assertEqual((self.destination / 'index.html').read_bytes(), expected.encode())

    def test_private_and_unpublished_links_and_media(self):
        self.resource('paper.md', public=True)
        self.resource('data/hidden.json')
        self.resource('figures/public.svg', public=True)
        self.resource('figures/private.svg')
        self.put(self.generated, 'index.html', '''<main>
<a href='https://source/paper' data-repo-path='paper.md' data-repo-fragment='method'>Paper</a>
<a href='https://source/hidden' data-repo-path='data/hidden.json' data-repo-fragment=''>Hidden</a>
<a href='https://source/local' data-repo-path='local/untracked.html'>Keep <em>all labels</em></a>
<img src='_media/figures/public.svg?scale=2&amp;n=3#point' data-other="a &amp; b">
<img src='_media/figures/private.svg'>
<img src='_media/figures/untracked.svg'>
</main>''')
        original = (self.generated / 'index.html').read_text()
        self.export(private_suffixes=('.md',), local_notice=('local-note', 'Kept locally & omitted'))
        expected = original.replace("<a href='https://source/local' data-repo-path='local/untracked.html'>Keep <em>all labels</em></a>",
                                    '<span class="local-note" title="Kept locally &amp; omitted">Keep <em>all labels</em></span>')
        expected = expected.replace("src='_media/figures/public.svg?scale=2&amp;n=3#point'", "src='figures/public.svg?scale=2&amp;n=3#point'")
        self.assertEqual((self.destination / 'index.html').read_text(), expected)

    def test_nested_page_links_public_files_relative_to_itself(self):
        self.resource('research/snapshot.html', public=True)
        self.resource('figures/plot.svg', public=True)
        source = ("<article id='original'><a href='../index.html?mode=two#intro'>Start</a>"
                  "<img src='../_media/figures/plot.svg'>"
                  "<a href='https://source/snapshot' data-repo-path='research/snapshot.html' "
                  "data-repo-fragment='equation&amp;value'>Evidence</a></article>")
        self.put(self.generated, 'chapters/topic.html', source)
        self.put(self.generated, 'index.html', '<a href="chapters/topic.html#original">Topic</a>')
        self.put(self.generated, 'static/plain.json', b'{"href":"index.html"}\n')
        self.export(pages=('index.html', 'chapters/topic.html'))
        expected = source.replace("href='https://source/snapshot' data-repo-path='research/snapshot.html' data-repo-fragment='equation&amp;value'",
                                  "href='../research/snapshot.html#equation&amp;value'")
        self.assertEqual((self.destination / 'chapters/topic.html').read_text(), expected)
        self.assertEqual((self.destination / 'index.html').read_text(), '<a href="chapters/topic.html#original">Topic</a>')
        self.assertEqual((self.destination / 'static/plain.json').read_bytes(), b'{"href":"index.html"}\n')

    def test_media_elements_restore_only_src_and_poster(self):
        self.resource('figures/frame.svg', public=True)
        source = ("<div><video poster='_media/figures/frame.svg' controls>"
                  "<source src='_media/figures/frame.svg'></video>"
                  "<audio src='_media/figures/frame.svg'></audio>"
                  "<iframe src='_media/figures/frame.svg'></iframe>"
                  "<a href='_media/figures/frame.svg'>Original link</a>"
                  "<script src='_media/figures/frame.svg'></script></div>")
        self.put(self.generated, 'index.html', source)
        self.export()
        expected = source.replace("poster='_media/figures/frame.svg'", "poster='figures/frame.svg'")
        # Script and anchor references do not use the media restoration rule.
        expected = expected.replace("<source src='_media/figures/frame.svg'>", "<source src='figures/frame.svg'>")
        expected = expected.replace("<audio src='_media/figures/frame.svg'>", "<audio src='figures/frame.svg'>")
        expected = expected.replace("<iframe src='_media/figures/frame.svg'>", "<iframe src='figures/frame.svg'>")
        self.assertEqual((self.destination / 'index.html').read_text(), expected)

    def test_public_file_may_be_a_generated_output(self):
        self.resource('evidence/report.html')
        self.public.add('evidence/report.html')
        self.put(self.generated, 'evidence/report.html', '<p>Report</p>')
        self.put(self.generated, 'index.html',
                 '<a href="https://source/report" data-repo-path="evidence/report.html">Report</a>')
        self.export()
        self.assertEqual((self.destination / 'index.html').read_text(), '<a href="evidence/report.html">Report</a>')
        self.assertEqual((self.destination / 'evidence/report.html').read_text(), '<p>Report</p>')

    def test_only_explicit_pages_are_rewritten(self):
        self.resource('fig.svg', public=True)
        self.put(self.generated, 'index.html', '<img src="_media/fig.svg">')
        original = '<img src="../_media/fig.svg"><script>"_media/fig.svg"</script>'
        self.put(self.generated, 'evidence/nested.html', original)
        self.export()
        self.assertEqual((self.destination / 'index.html').read_text(), '<img src="fig.svg">')
        self.assertEqual((self.destination / 'evidence/nested.html').read_text(), original)

    def test_replacement_requires_explicit_permission(self):
        self.put(self.generated, 'index.html', '<p>New</p>')
        self.put(self.generated, 'asset.txt', 'New asset')
        self.put(self.destination, 'index.html', '<p>Old</p>')
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            self.export()
        self.assertFalse((self.destination / 'asset.txt').exists())
        self.assertEqual((self.destination / 'index.html').read_text(), '<p>Old</p>')
        self.export(replace=('index.html',))
        # Identical reruns are safe without replacement permission.
        self.export()
        self.assertEqual((self.destination / 'index.html').read_text(), '<p>New</p>')

    def test_invalid_paths_do_not_write(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        for name in ('../escape.html', '/escape.html', 'x/../escape.html', 'x//a.html', r'x\a.html', 'x.html?query'):
            for option in ('pages', 'replace', 'public_files', 'tracked'):
                with self.subTest(name=name, option=option), self.assertRaisesRegex(ValueError, 'Invalid publication path'):
                    self.export(**{option: (name,)})
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_existing_parent_file_directory_collision(self):
        self.put(self.generated, 'reader/page.html', '<p>Page</p>')
        self.put(self.generated, 'asset.txt', 'Other')
        self.put(self.destination, 'reader', 'Existing file')
        with self.assertRaisesRegex(ValueError, 'file/directory collision'):
            self.export(pages=('reader/page.html',))
        self.assertFalse((self.destination / 'asset.txt').exists())
        self.assertEqual((self.destination / 'reader').read_text(), 'Existing file')

    def test_invalid_page_or_replacement(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        self.put(self.generated, 'asset.json', '{}')
        for options in ({'pages': ('absent.html',)}, {'pages': ('asset.json',)}, {'replace': ('absent.html',)}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.export(**options)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_public_files_require_tracked_present_available_files(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        self.put(self.root, 'untracked.svg')
        self.put(self.destination, 'untracked.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files=('untracked.svg',))
        self.tracked.add('missing.svg')
        self.put(self.destination, 'missing.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files=('missing.svg',))
        self.resource('unpublished.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files=('unpublished.svg',))
        with self.assertRaisesRegex(ValueError, 'Invalid publication path'):
            self.export(public_files=('../outside.svg',))
        self.assertEqual(set(path.name for path in self.destination.iterdir()), {'untracked.svg', 'missing.svg'})

    def test_generated_media_requires_tracked_repository_file(self):
        self.put(self.generated, 'index.html', '<img src="_media/private.svg">')
        self.put(self.generated, '_media/private.svg')
        self.put(self.root, 'private.svg')
        with self.assertRaisesRegex(ValueError, 'not a tracked repository file'):
            self.export()
        self.tracked.add('private.svg')
        (self.root / 'private.svg').unlink()
        with self.assertRaisesRegex(ValueError, 'not a tracked repository file'):
            self.export()
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_generated_and_destination_symlinks_are_rejected(self):
        outside = self.put(self.base, 'outside.txt', 'Do not overwrite')
        self.put(self.generated, 'index.html', '<p>Page</p>')
        (self.generated / 'asset.txt').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export()
        (self.generated / 'asset.txt').unlink()
        (self.destination / 'index.html').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(replace=('index.html',))
        self.assertEqual(outside.read_text(), 'Do not overwrite')

    def test_directory_and_repository_symlinks_are_rejected(self):
        outside = self.base / 'outside'
        outside.mkdir()
        self.put(outside, 'asset.svg')
        self.put(self.generated, 'linked/page.html', '<p>Page</p>')
        (self.destination / 'linked').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(pages=('linked/page.html',))
        (self.generated / 'linked/page.html').unlink()
        (self.generated / 'linked').rmdir()
        self.put(self.generated, 'index.html', '<p>Page</p>')
        (self.root / 'assets').symlink_to(outside, target_is_directory=True)
        self.tracked.add('assets/asset.svg')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(public_files=('assets/asset.svg',))
        alias = self.base / 'alias'
        alias.symlink_to(self.destination, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            export_pages(self.generated, alias / 'child', root=self.root, tracked=(), pages=(), public_files=())
        self.assertFalse((outside / 'page.html').exists())

    def test_escaping_repository_metadata_is_rejected(self):
        self.put(self.generated, 'index.html', '<a href="https://source" data-repo-path="../outside">Label</a>')
        with self.assertRaisesRegex(ValueError, 'Invalid publication path'):
            self.export()
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_incomplete_local_anchor_is_rejected(self):
        self.put(self.generated, 'index.html', '<a href="https://source" data-repo-path="local.html"/>')
        with self.assertRaisesRegex(ValueError, 'complete anchor'):
            self.export()
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_overlapping_roots_are_rejected(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        with self.assertRaisesRegex(ValueError, 'must not overlap'):
            export_pages(self.generated, self.generated / 'nested', root=self.root,
                         tracked=(), pages=(), public_files=())


if __name__ == '__main__':
    unittest.main()
