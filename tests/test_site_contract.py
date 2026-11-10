"""Version 1.0 site contract: nested includes, strict navigation tables and site-map cards."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]


def invoke(*args):
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)], cwd=KIT, capture_output=True, text=True)


class SiteContract(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='docs-kit-contract-')
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        self.assertEqual(invoke('init', self.root).returncode, 0)
        self.guide = self.root / 'docs/topics/guide/index.md'
        self.fragments = self.root / 'docs/site/fragments'
        self.fragments.mkdir(parents=True, exist_ok=True)

    def build(self):
        subprocess.run(['git', 'add', 'docs', 'AGENTS.md', 'CLAUDE.md'], cwd=self.root, check=True)
        return invoke('build', '--project', self.root)

    def test_built_site_carries_the_kit_license_beside_vendor_licenses(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        assets = self.root / '.build/docs/html/assets'
        self.assertEqual((assets / 'documentation-kit/LICENSE').read_bytes(), (KIT / 'LICENSE').read_bytes())
        self.assertTrue((assets / 'katex/LICENSE').is_file())

    def test_project_asset_cannot_replace_the_kit_license(self):
        site = self.root / 'docs/site/site.toml'
        notice = self.root / 'docs/site/notice.txt'
        notice.write_text('other terms\n')
        site.write_text(site.read_text() + '\n[extra_assets]\n"documentation-kit/LICENSE" = "docs/site/notice.txt"\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('would overwrite a shared asset', result.stdout + result.stderr)

    def test_a_paragraph_after_a_fold_renders_as_markdown(self):
        self.guide.write_text(self.guide.read_text() + (
            '\n<!-- fold: code Fold before a paragraph -->\n\nInside the fold.\n\n<!-- /fold -->\n\n'
            'After the fold: [the guide](guide.html) and **bold**.\n'))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('Inside the fold.</p>', page)
        self.assertIn('After the fold: <a href="guide.html">the guide</a> and <strong>bold</strong>.', page)
        self.assertNotIn('[the guide](guide.html)', page)

    def test_a_paragraph_glued_to_a_closing_fold_renders_as_markdown(self):
        self.guide.write_text(self.guide.read_text() + (
            '\n<!-- fold: code Fold without a blank line after it -->\n\nInside.\n\n<!-- /fold -->\n'
            'Glued to the fold: [the guide](guide.html).\n'))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('Glued to the fold: <a href="guide.html">the guide</a>.', page)

    def test_lint_prints_page_number_notes_when_the_site_turns_them_on(self):
        site = self.root / 'docs/site/site.toml'
        text = site.read_text()
        self.assertEqual(self.build().returncode, 0)
        self.assertNotIn('shows numbers', invoke('lint', '--project', self.root).stdout)
        site.write_text(text.replace('[[nav]]', 'page_number_notes = true\n\n[[nav]]', 1))
        self.assertEqual(self.build().returncode, 0)
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertIn('shows numbers that none of its linked records state', result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        site.write_text(text.replace('[[nav]]', 'page_number_notes = "yes"\n\n[[nav]]', 1))
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('page_number_notes must be true or false', result.stdout + result.stderr)

    def test_included_fragments_may_include_others(self):
        (self.fragments / 'outer.html').write_text('<p id="outer-part">outer</p>\n<!-- include: fragments/inner.html -->\n')
        (self.fragments / 'inner.html').write_text('<p id="inner-part">inner</p>\n')
        self.guide.write_text(self.guide.read_text() + '\n<!-- include: fragments/outer.html -->\n')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('id="outer-part"', page)
        self.assertIn('id="inner-part"', page)
        self.assertNotIn('include: fragments/inner.html', page)

    def test_include_depth_is_bounded_and_errors_name_the_chain(self):
        for level in range(1, 11):
            (self.fragments / f'n{level}.html').write_text(f'<p>n{level}</p>\n<!-- include: fragments/n{level + 1}.html -->\n')
        (self.fragments / 'n8.html').write_text('<p>n8</p>\n')
        self.guide.write_text(self.guide.read_text() + '\n<!-- include: fragments/n1.html -->\n')
        self.assertEqual(self.build().returncode, 0, 'eight nested levels (n1 to n8) are allowed')
        (self.fragments / 'n8.html').write_text('<p>n8</p>\n<!-- include: fragments/n9.html -->\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('nest deeper than 8 levels', result.stdout + result.stderr)
        (self.fragments / 'n8.html').write_text('<p>n8</p>\n<!-- include: fragments/missing.html -->\n')
        result = self.build()
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('include not found or not tracked: n1.html -> n2.html', result.stdout + result.stderr)
        self.assertIn('n8.html -> fragments/missing.html', result.stdout + result.stderr)

    def test_include_cycle_fails(self):
        (self.fragments / 'a.html').write_text('<p>a</p>\n<!-- include: fragments/b.html -->\n')
        (self.fragments / 'b.html').write_text('<p>b</p>\n<!-- include: fragments/a.html -->\n')
        self.guide.write_text(self.guide.read_text() + '\n<!-- include: fragments/a.html -->\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('include cycle', result.stdout + result.stderr)

    def test_setting_written_below_a_nav_table_is_rejected(self):
        site = self.root / 'docs/site/site.toml'
        site.write_text(site.read_text() + '\nextra_components = ["viewer"]\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown keys ['extra_components']", result.stderr)
        self.assertIn('above the first [[nav]] table', result.stderr)

    def test_nav_must_be_typed_tables(self):
        site = self.root / 'docs/site/site.toml'
        original = site.read_text()
        site.write_text(original.replace('group = "guide"', 'group = "guide"\nhidden = "no"'))
        result = self.build()
        self.assertIn("wrong value types for ['hidden']", result.stderr)
        site.write_text(original.split('[[nav]]')[0] + 'nav = ["guide.html"]\n')
        result = self.build()
        self.assertIn('every nav entry must be a [[nav]] table', result.stderr)

    def test_remote_thumbnail_is_rejected(self):
        self.guide.write_text(self.guide.read_text().replace('+++\n', '+++\nthumbnail = "https://example.com/a.png"\n', 1))
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('thumbnail must be a local, tracked image', result.stdout + result.stderr)

    def test_site_map_cards_use_description_and_thumbnail(self):
        text = self.guide.read_text().replace('+++\n', '+++\ndescription = "How the reader is assembled"\n'
                                              'thumbnail = "../figures/guide-card.svg"\n', 1)
        self.guide.write_text(text)
        figures = self.root / 'docs/figures'
        figures.mkdir(exist_ok=True)
        (figures / 'guide-card.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 3"><rect width="4" height="3"/></svg>\n')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        home = (self.root / '.build/docs/html/index.html').read_text()
        # A local SVG thumbnail is inlined like any other local SVG figure.
        card = home[home.index('<a class="map-card" href="guide.html">'):]
        self.assertTrue(card.startswith('<a class="map-card" href="guide.html"><span class="map-thumb"><svg'), card[:120])
        self.assertIn('<rect width="4" height="3"/>', card[:400])
        self.assertIn('aria-hidden="true"', card[:300], 'the card names the page; its picture is decorative')
        self.assertNotIn('role="img"', card[:300])
        self.assertIn('<span>How the reader is assembled</span>', home)

    def test_empty_description_is_rejected(self):
        self.guide.write_text(self.guide.read_text().replace('+++\n', '+++\ndescription = " "\n', 1))
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('description must be a non-empty string', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
