"""Browser-tab titles: the site's title first, then the page's short name."""
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))
sys.path.insert(0, str(KIT / 'tests'))

import page_lock_fixture  # noqa: E402
from page_lock import lock_title  # noqa: E402

HAS_CRYPTOGRAPHY = importlib.util.find_spec('cryptography') is not None


def docsite(*args, env=None):
    environment = {name: value for name, value in (env or os.environ).items()
                   if name not in ('GITHUB_SHA', 'DOCSITE_PROJECT_ROOT')}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)], cwd=KIT,
                          capture_output=True, text=True, env=environment)


def tab(page: str) -> str:
    return re.search(r'<title>(.*?)</title>', page, re.S)[1]


class TabTitles(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-tab-titles-')
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        # Topic pages, registered and listed Reference pages, and the Reference index the lock writes.
        self.root = page_lock_fixture.make_project(self.folder / 'project', lock=True)
        self.site = self.root / 'docs/site/site.toml'
        self.text = self.site.read_text()
        self.html = self.root / '.build/docs/html'

    def build(self, text):
        self.site.write_text(text)
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        result = docsite('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def page(self, name):
        return (self.html / name).read_text()

    def test_each_page_kind_names_the_site_then_the_page(self):
        self.assertIn('title = "Lock fixture"', self.text)
        self.build(self.text)
        # The home page names the site alone: its [[nav]] label would only repeat that it is the start.
        self.assertEqual(tab(self.page('index.html')), 'Lock fixture')
        # A topic page with the reader and one without: their [[nav]] labels.
        self.assertEqual(tab(self.page('guide.html')), 'Lock fixture · Guide')
        self.assertEqual(tab(self.page('widgets.html')), 'Lock fixture · Widgets')
        # A registered record page, an automatically listed file and the Reference index: their titles.
        self.assertEqual(tab(self.page('rule.html')), 'Lock fixture · Shared rule')
        self.assertEqual(tab(self.page('notes.record.md.html')),
                         f'Lock fixture · Record {page_lock_fixture.MARKERS["title"]}')
        self.assertEqual(tab(self.page('reference.index.html')), 'Lock fixture · Reference')

    def test_the_visible_titles_stay_the_page_titles(self):
        self.build(self.text)
        page = self.page('widgets.html')
        self.assertIn('<span class="t">Widgets after unlock</span>', page)
        self.assertIn('<h1 id="widgets-after-unlock">Widgets after unlock</h1>', page)

    def test_a_label_differs_from_the_title_and_everything_is_escaped(self):
        text = self.text.replace('title = "Lock fixture"', 'title = "Fish & <Chips> \\"Co\\""', 1)
        text = text.replace('label = "Widgets"', 'label = "Wid<gets> & co"', 1)
        self.build(text)
        self.assertEqual(tab(self.page('widgets.html')), 'Fish &amp; &lt;Chips&gt; &quot;Co&quot; · Wid&lt;gets&gt; &amp; co')
        self.assertEqual(tab(self.page('index.html')), 'Fish &amp; &lt;Chips&gt; &quot;Co&quot;')

    def test_a_site_without_a_title_keeps_the_page_title_alone(self):
        self.build(self.text.replace('title = "Lock fixture"\n', '', 1))
        self.assertEqual(tab(self.page('widgets.html')), 'Widgets after unlock')
        self.assertEqual(tab(self.page('rule.html')), 'Shared rule')

    def test_a_deck_names_the_site_then_the_deck(self):
        self.site.write_text(self.text)
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        result = docsite('slides', '--project', self.root, '--select', 'guide', '--out', 'deck', '--title', 'Talk & demo')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        deck = (self.root / '.build/slides/deck.html').read_text()
        self.assertEqual(tab(deck), 'Lock fixture · Talk &amp; demo')
        self.assertIn('<strong>Talk &amp; demo</strong>', deck)

    def test_the_lock_title(self):
        self.assertEqual(lock_title('Lock fixture'), 'Lock fixture · Locked')
        self.assertEqual(lock_title(''), 'Locked page')
        self.assertEqual(lock_title('  '), 'Locked page')

    @unittest.skipUnless(HAS_CRYPTOGRAPHY, 'cryptography is not installed; pip install -r requirements-lock.txt')
    def test_a_lock_page_names_the_site_and_no_page(self):
        out = self.folder / 'site'
        env = dict(os.environ, DOCSITE_GENERAL_PASSWORD='general secret', DOCSITE_REFERENCE_PASSWORD='reference secret')
        result = docsite('publish', '--project', self.root, '--out', out, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for name in ('index.html', 'guide.html', 'rule.html', 'reference.index.html'):
            page = (out / name).read_text()
            self.assertIn('id="page-lock-data"', page, name)
            self.assertEqual(tab(page), 'Lock fixture · Locked', name)
            for leak in ('Guide', 'Shared rule', 'Widgets', 'Reference', *page_lock_fixture.MARKERS.values()):
                self.assertNotIn(leak, page.replace('id="page-lock', ''), f'{leak} in {name}')


if __name__ == '__main__':
    unittest.main()
