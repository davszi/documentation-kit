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
        self.public = {}

    def put(self, directory, name, content=b'content'):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode() if isinstance(content, str) else content)
        return path

    def resource(self, name, public=None, content=b'content'):
        self.put(self.root, name, content)
        self.tracked.add(name)
        if public is not None:
            self.put(self.destination, public, content)
            self.public[name] = public

    def export(self, **kwargs):
        options = dict(root=self.root, tracked=self.tracked, page_routes={'index.html': 'overview.html'},
                       pages=('overview.html',), public_files=self.public)
        options.update(kwargs)
        return export_pages(self.generated, self.destination, **options)

    def test_original_overlay_output_is_byte_exact(self):
        self.resource('docs/chart.svg', 'docs/chart.svg')
        self.resource('evidence/report.html', 'evidence/report.html')
        self.resource('notes.md', 'notes.md')
        self.resource('configs/run.json', 'configs/run.json')
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
        expected = (source.replace('href="index.html#top"', 'href="overview.html#top"')
                    .replace('src="_media/docs/chart.svg"', 'src="docs/chart.svg"')
                    .replace('href="https://example.test/blob/report" data-repo-path="evidence/report.html" data-repo-fragment="details"',
                             'href="evidence/report.html#details"')
                    .replace('<a href="https://example.test/blob/local" data-repo-path="results/local.html" data-repo-fragment="x"><b>Local label</b></a>',
                             '<span class="local-evidence" title="Local evidence file; not published"><b>Local label</b></span>'))
        exported = self.export(private_suffixes=('.md', '.py', '.toml'), private_prefixes=('configs/',))
        self.assertEqual((self.destination / 'overview.html').read_bytes(), expected.encode())
        self.assertEqual(set(exported), {'overview.html', '_media/docs/chart.svg'})
        self.assertEqual((self.destination / '_media/docs/chart.svg').read_bytes(), b'content')
        self.assertEqual((self.generated / 'index.html').read_bytes(), source.encode())

    def test_actual_attributes_only_with_mixed_quotes_queries_and_fragments(self):
        source = '''<html><body>
<a data-example='href="index.html#pretend"' href='index.html?mode=one&amp;x=2#part' id="same">Home</a>
<a href=index.html#bare>Bare</a>
<a href="https://example.test/index.html#remote">Remote</a>
<a href="//example.test/index.html">Protocol relative</a>
<a href="#index.html">Fragment</a>
<!-- <a href="index.html">comment</a> -->
<style>.x::after {content:'<a href="index.html">';}</style>
<script type='application/json'>{"text":"<a href='index.html'>JSON</a>"}</script>
<script>let literal = '<a href="index.html">script</a>';</script>
</body></html>'''
        self.put(self.generated, 'index.html', source)
        expected = source.replace("href='index.html?mode=one&amp;x=2#part'", "href='overview.html?mode=one&amp;x=2#part'")
        expected = expected.replace('href=index.html#bare', 'href=overview.html#bare')
        self.export()
        self.assertEqual((self.destination / 'overview.html').read_bytes(), expected.encode())

    def test_non_lf_separators_in_scripts_do_not_shift_later_edits(self):
        for separator in ('\u2028', '\r', '\f'):
            with self.subTest(separator=repr(separator)):
                opaque = ('<script>const value = "before' + separator + 'after";</script>'
                          '<script type="application/json">{"html":"before' + separator
                          + '<a href=\'index.html\'>opaque</a>"}</script>')
                source = '<main>' + opaque + '\n<a href="index.html#later">Later</a></main>'
                self.put(self.generated, 'index.html', source)
                self.export(replace=('overview.html',))
                expected = source.replace('href="index.html#later"', 'href="overview.html#later"')
                self.assertEqual((self.destination / 'overview.html').read_bytes(), expected.encode())

    def test_mixed_mapped_and_unmapped_generated_anchor_targets(self):
        source = ('<main><a href="about.html?view=all&amp;x=1#details">About</a>'
                  '<a href="./evidence/report.html#proof">Evidence</a>'
                  '<a href="assets/data.json?view=raw">Data</a>'
                  '<a href="index.html#intro">Start</a></main>')
        about = '<a href="./index.html?view=one#intro">Start</a>'
        evidence = '<a href="../about.html#details">About</a>'
        self.put(self.generated, 'index.html', source)
        self.put(self.generated, 'about.html', about)
        self.put(self.generated, 'evidence/report.html', evidence)
        self.put(self.generated, 'assets/data.json', b'{"opaque":"index.html"}')
        self.export(page_routes={'index.html': 'reader/start.html'},
                    pages=('reader/start.html', 'about.html', 'evidence/report.html'))
        expected = (source.replace('href="about.html?', 'href="../about.html?')
                    .replace('href="./evidence/report.html#', 'href="../evidence/report.html#')
                    .replace('href="assets/data.json?', 'href="../assets/data.json?')
                    .replace('href="index.html#', 'href="start.html#'))
        self.assertEqual((self.destination / 'reader/start.html').read_text(), expected)
        self.assertEqual((self.destination / 'about.html').read_text(),
                         '<a href="reader/start.html?view=one#intro">Start</a>')
        self.assertEqual((self.destination / 'evidence/report.html').read_text(), evidence)
        self.assertEqual((self.destination / 'assets/data.json').read_bytes(), b'{"opaque":"index.html"}')

    def test_unmoved_links_keep_original_spelling_and_entity_bytes(self):
        source = ('<main><a href="./about.html?x=1&#38;y=2#part">About</a>'
                  '<a href="evidence/../about.html#part">Normalized destination</a>'
                  '<a href="%61bout.html">Encoded destination</a>'
                  '<a href="index.html#intro">Home</a></main>')
        self.put(self.generated, 'index.html', source)
        self.put(self.generated, 'about.html', '<p>About</p>')
        self.export(page_routes={'index.html': 'overview.html', 'about.html': 'about.html'})
        expected = source.replace('href="index.html#intro"', 'href="overview.html#intro"')
        self.assertEqual((self.destination / 'overview.html').read_bytes(), expected.encode())

    def test_private_and_unpublished_links_and_media(self):
        self.resource('paper.md', 'paper.md')
        self.resource('data/hidden.json')
        self.resource('figures/public.svg', 'figures/public.svg')
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
        self.assertEqual((self.destination / 'overview.html').read_text(), expected)

    def test_neutral_consumer_nested_routes_and_public_html_evidence(self):
        self.resource('research/snapshot.html', 'evidence/2026/snapshot.html')
        source = ("<article id='original'><a href='../index.html?mode=two#intro'>Start</a>"
                  "<a href='https://source/snapshot' data-repo-path='research/snapshot.html' "
                  "data-repo-fragment='equation&amp;value'>Evidence</a></article>")
        self.put(self.generated, 'chapters/topic.html', source)
        self.put(self.generated, 'index.html', '<a href="chapters/topic.html#original">Topic</a>')
        self.put(self.generated, 'static/plain.json', b'{"href":"index.html"}\n')
        self.export(page_routes={'index.html': 'reader/start.html', 'chapters/topic.html': 'reader/deep/topic.html'},
                    pages=('reader/start.html', 'reader/deep/topic.html'))
        expected = (source.replace("href='../index.html?mode=two#intro'", "href='../start.html?mode=two#intro'")
                    .replace("href='https://source/snapshot' data-repo-path='research/snapshot.html' data-repo-fragment='equation&amp;value'",
                             "href='../../evidence/2026/snapshot.html#equation&amp;value'"))
        self.assertEqual((self.destination / 'reader/deep/topic.html').read_text(), expected)
        self.assertEqual((self.destination / 'reader/start.html').read_text(), '<a href="deep/topic.html#original">Topic</a>')
        self.assertEqual((self.destination / 'static/plain.json').read_bytes(), b'{"href":"index.html"}\n')

    def test_media_elements_restore_only_src_and_poster(self):
        self.resource('figures/frame.svg', 'published/frame.svg')
        source = ("<div><video poster='_media/figures/frame.svg' controls>"
                  "<source src='_media/figures/frame.svg'></video>"
                  "<audio src='_media/figures/frame.svg'></audio>"
                  "<iframe src='_media/figures/frame.svg'></iframe>"
                  "<a href='_media/figures/frame.svg'>Original link</a>"
                  "<script src='_media/figures/frame.svg'></script></div>")
        self.put(self.generated, 'index.html', source)
        self.export()
        expected = source.replace("poster='_media/figures/frame.svg'", "poster='published/frame.svg'")
        # Script and anchor references do not use the media restoration rule.
        expected = expected.replace("<source src='_media/figures/frame.svg'>", "<source src='published/frame.svg'>")
        expected = expected.replace("<audio src='_media/figures/frame.svg'>", "<audio src='published/frame.svg'>")
        expected = expected.replace("<iframe src='_media/figures/frame.svg'>", "<iframe src='published/frame.svg'>")
        self.assertEqual((self.destination / 'overview.html').read_text(), expected)

    def test_only_explicit_pages_are_rewritten(self):
        self.put(self.generated, 'index.html', '<a href="index.html">Active</a>')
        original = '<a href="index.html">Historical</a><script>"index.html"</script>'
        self.put(self.generated, 'evidence/nested.html', original)
        self.export()
        self.assertEqual((self.destination / 'evidence/nested.html').read_text(), original)

    def test_replacement_requires_explicit_permission(self):
        self.put(self.generated, 'index.html', '<p>New</p>')
        self.put(self.generated, 'asset.txt', 'New asset')
        self.put(self.destination, 'overview.html', '<p>Old</p>')
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            self.export()
        self.assertFalse((self.destination / 'asset.txt').exists())
        self.assertEqual((self.destination / 'overview.html').read_text(), '<p>Old</p>')
        self.export(replace=('overview.html',))
        # Identical reruns are safe without replacement permission.
        self.export()
        self.assertEqual((self.destination / 'overview.html').read_text(), '<p>New</p>')

    def test_invalid_paths_and_route_collisions_do_not_write(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        for target in ('../escape.html', '/escape.html', 'x/../escape.html', 'x//a.html', r'x\a.html', 'x.html?query'):
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, 'Invalid publication path'):
                self.export(page_routes={'index.html': target}, pages=(target,))
        self.put(self.generated, 'overview.html', '<p>Other page</p>')
        with self.assertRaisesRegex(ValueError, 'route collision'):
            self.export()
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_route_and_existing_parent_file_directory_collisions(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        self.put(self.generated, 'asset.txt', 'Other')
        with self.assertRaisesRegex(ValueError, 'file/directory collision'):
            self.export(page_routes={'index.html': 'reader', 'asset.txt': 'reader/file.txt'}, pages=())
        self.put(self.destination, 'reader', 'Existing file')
        with self.assertRaisesRegex(ValueError, 'file/directory collision'):
            self.export(page_routes={'index.html': 'reader/page.html'}, pages=('reader/page.html',))
        self.assertFalse((self.destination / 'asset.txt').exists())

    def test_invalid_page_and_missing_route_or_replacement(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        for options in ({'pages': ('absent.html',)}, {'pages': ('asset.json',)},
                        {'page_routes': {'missing.html': 'overview.html'}}, {'replace': ('absent.html',)}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.export(**options)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_public_file_mapping_requires_tracked_present_contained_files(self):
        self.put(self.generated, 'index.html', '<p>Page</p>')
        self.put(self.root, 'untracked.svg')
        self.put(self.destination, 'untracked.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files={'untracked.svg': 'untracked.svg'})
        self.tracked.add('missing.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files={'missing.svg': 'untracked.svg'})
        self.resource('tracked.svg')
        with self.assertRaisesRegex(ValueError, 'tracked, present'):
            self.export(public_files={'tracked.svg': 'absent.svg'})
        with self.assertRaisesRegex(ValueError, 'Invalid publication path'):
            self.export(public_files={'tracked.svg': '../outside.svg'})
        self.assertEqual(set(path.name for path in self.destination.iterdir()), {'untracked.svg'})

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
        (self.destination / 'overview.html').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(replace=('overview.html',))
        self.assertEqual(outside.read_text(), 'Do not overwrite')

    def test_directory_and_repository_symlinks_are_rejected(self):
        outside = self.base / 'outside'
        outside.mkdir()
        self.put(outside, 'asset.svg')
        self.put(self.generated, 'index.html', '<p>Page</p>')
        (self.destination / 'linked').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(page_routes={'index.html': 'linked/page.html'}, pages=('linked/page.html',))
        (self.root / 'assets').symlink_to(outside, target_is_directory=True)
        self.tracked.add('assets/asset.svg')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.export(public_files={'assets/asset.svg': 'linked/asset.svg'})
        alias = self.base / 'alias'
        alias.symlink_to(self.destination, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            export_pages(self.generated, alias / 'child', root=self.root, tracked=(), page_routes={}, pages=(), public_files={})

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
                         tracked=(), page_routes={}, pages=(), public_files={})


if __name__ == '__main__':
    unittest.main()
