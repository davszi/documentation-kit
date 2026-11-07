"""Registered source pages: origins, links, anchors, media, containment and collisions."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]

RULE = """# Shared rule

Read [the other rule](other.md#second-part) and [its top](other.md).
See [the record](../notes/record.md#kept) and [this section](#first-part).

![Diagram](media/diagram.png)

## First part

<!-- include: missing.html -->

<!-- fold: math Kept literal -->

| Key | Meaning |
|---|---|
| a | b |
"""

OTHER = """# Other rule

## Second part

Back to [the shared rule](rule.md#first-part).
"""


def invoke(*args):
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True)


class SourcePages(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-sources-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        self.assertEqual(invoke('init', self.root).returncode, 0)
        self.write('policy/rule.md', RULE)
        self.write('policy/other.md', OTHER)
        self.write('notes/record.md', '# Record\n\n## Kept\n')
        (self.root / 'policy/media').mkdir()
        (self.root / 'policy/media/diagram.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
        self.register('policy/rule.md', 'shared-rule', description='A shared rule.')
        self.register('policy/other.md', 'other-rule')

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def register(self, source, slug, *, nav=True, **extra):
        config = self.root / 'docs/site/site.toml'
        text = config.read_text()
        if nav:
            text += f'\n[[nav]]\nlabel = "{slug}"\nfile = "{slug}.html"\ngroup = "rules"\n'
        text += f'\n[[source_pages]]\nsource = "{source}"\nslug = "{slug}"\n'
        text += ''.join(f'{key} = {json.dumps(value)}\n' for key, value in extra.items())
        config.write_text(text)

    def build(self, *options):
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        return invoke('build', '--project', self.root, *options)

    def page(self, slug):
        return (self.root / '.build/docs/html' / (slug + '.html')).read_text()

    def assertFails(self, message):
        result = self.build()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def test_source_origin_routes_media_and_literal_markers(self):
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = self.page('shared-rule')
        # Origin: canonical path, hosted source link and edit link.
        self.assertIn('data-source-page="policy/rule.md"', page)
        self.assertIn('href="https://github.com/example/project/blob/main/policy/rule.md"', page)
        self.assertIn('href="https://github.com/example/project/edit/main/policy/rule.md"', page)
        self.assertIn('class="source-page reference-page"', page)
        self.assertIn('<title>Shared rule</title>', page)
        # Registered targets become routes; other repository files stay source links.
        self.assertIn('href="other-rule.html#second-part"', page)
        self.assertIn('href="other-rule.html"', page)
        self.assertIn('href="https://github.com/example/project/blob/main/notes/record.md#kept"', page)
        self.assertIn('data-repo-path="notes/record.md"', page)
        self.assertIn('href="#first-part"', page)
        # Media resolve from the source folder and are packaged.
        self.assertIn('src="_media/policy/media/diagram.png"', page)
        self.assertTrue((self.root / '.build/docs/html/_media/policy/media/diagram.png').is_file())
        # Topic-page markers stay literal; tables get a labelled scroll region.
        self.assertIn('<!-- include: missing.html -->', page)
        self.assertIn('<!-- fold: math Kept literal -->', page)
        self.assertIn('aria-label="Table: Key, Meaning"', page)
        # Sidebar lists headings; navigation and manifest know the route.
        self.assertIn('href="#first-part">First part</a>', page)
        self.assertIn('class="xpage current" aria-current="page"', page)
        manifest = json.loads((self.root / '.build/docs/site-build.json').read_text())
        self.assertEqual(manifest['source_pages'], {'other-rule.html': 'policy/other.md',
                                                   'shared-rule.html': 'policy/rule.md'})
        self.assertIn('href="shared-rule.html#first-part"', self.page('other-rule'))
        self.assertEqual(self.build('--check').returncode, 0)
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_site_map_lists_source_pages(self):
        home = self.root / 'docs/topics/home/index.md'
        self.assertIn('<!-- site-map -->', home.read_text())
        self.assertEqual(self.build().returncode, 0)
        self.assertIn('href="shared-rule.html"', self.page('index'))
        self.assertIn('A shared rule.', self.page('index'))

    def test_missing_cross_page_anchor_fails(self):
        self.write('policy/other.md', OTHER.replace('rule.md#first-part', 'rule.md#no-such-part'))
        self.assertFails('other-rule.html: anchor #no-such-part not found in shared-rule.html')

    def test_topic_page_link_into_source_page_is_anchor_checked(self):
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text() + '\n[Rule](shared-rule.html#gone)\n')
        self.assertFails('guide.html: anchor #gone not found in shared-rule.html')

    def test_missing_same_page_anchor_fails(self):
        self.write('policy/rule.md', RULE.replace('(#first-part)', '(#absent)'))
        self.assertFails('shared-rule.html: anchor #absent not found in shared-rule.html')

    def test_missing_link_target_fails(self):
        self.write('policy/rule.md', RULE + '\n[Gone](gone.md)\n')
        self.assertFails('policy/rule.md: link target not found: gone.md')

    def test_untracked_media_fails(self):
        self.write('policy/rule.md', RULE + '\n![Local](media/untracked.png)\n')
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        (self.root / 'policy/media/untracked.png').write_bytes(b'png')
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Untracked website media', result.stderr)

    def test_links_that_leave_the_project_fail(self):
        self.write('policy/rule.md', RULE + '\n[Out](../../outside.md) [Root](/etc/passwd)\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('link escapes the repository: ../../outside.md', result.stderr)
        self.assertIn('absolute link /etc/passwd', result.stderr)

    def test_source_containment(self):
        outside = tempfile.TemporaryDirectory(prefix='docs-kit-outside-')
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / 'secret.md').write_text('# Secret\n')
        (self.root / 'policy/linked.md').symlink_to(Path(outside.name) / 'secret.md')
        self.register('policy/linked.md', 'linked')
        self.register('../escape.md', 'escape')
        self.register('policy/untracked.md', 'untracked')
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        self.write('policy/untracked.md', '# Untracked\n')
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('policy/linked.md: source escapes the project through a symlink', result.stderr)
        self.assertIn('../escape.md: source must be a contained relative .md path', result.stderr)
        self.assertIn('policy/untracked.md: source must be a tracked file', result.stderr)

    def test_route_collisions_and_registry_errors(self):
        self.register('policy/other.md', 'again', nav=False)
        self.register('notes/record.md', 'guide', nav=False)
        self.register('docs/topics/guide/index.md', 'guide-copy')
        self.register('notes/record.md', 'Bad Slug', nav=False)
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '\n[[source_pages]]\nsource = "notes/record.md"\nslug = "x"\nlayout = "wide"\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('policy/other.md: registered twice (other-rule, again)', result.stderr)
        self.assertIn('route collision: guide.html is produced by more than one page (notes/record.md)', result.stderr)
        self.assertIn('topic entry pages render through their own frontmatter', result.stderr)
        self.assertIn('slug must be a lowercase filename stem', result.stderr)
        self.assertIn("unknown keys ['layout']", result.stderr)

    def test_route_needs_navigation_entry(self):
        self.register('notes/record.md', 'record', nav=False)
        self.assertFails('notes/record.md: record.html missing from site.toml [[nav]] registry')

    def test_lint_checks_registered_source_links(self):
        self.write('policy/rule.md', RULE.replace('../notes/record.md#kept', '../notes/record.md#not-kept'))
        self.assertEqual(self.build().returncode, 0)
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertNotEqual(lint.returncode, 0)
        self.assertIn('policy/rule.md: anchor #not-kept not found in ../notes/record.md', lint.stderr)

    def test_edit_link_keeps_branch_when_built_for_a_commit(self):
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        env = dict(os.environ, GITHUB_SHA='a' * 40)
        result = subprocess.run([sys.executable, str(KIT / 'docsite.py'), 'build', '--project', self.root],
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = self.page('shared-rule')
        self.assertIn('/blob/' + 'a' * 40 + '/policy/rule.md"', page)
        self.assertIn('/edit/main/policy/rule.md"', page)


    def test_nested_navigation_folds_groups_and_nests_sections(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('nested_nav = true\n' + config.read_text())
        self.assertEqual(self.build().returncode, 0)
        page = self.page('shared-rule')
        self.assertNotIn('<details class="nav-fold" data-group="rules" open data-nav-default>', self.page('guide'))
        self.assertIn('<details class="nav-fold" data-group="rules" open data-nav-default>', page)
        current = page.index('class="xpage current"')
        sections = page.index('<div class="nav-sections" aria-label="On this page">')
        self.assertLess(current, sections)
        self.assertLess(sections, page.index('href="#first-part">First part</a>'))
        self.assertIn('<span class="nav-group-label">rules</span>', page)
        # The home page has no current group: the first group opens.
        home = self.page('index')
        self.assertEqual(home.count(' open data-nav-default>'), 1)

    def test_flat_navigation_stays_the_default(self):
        self.assertEqual(self.build().returncode, 0)
        page = self.page('shared-rule')
        self.assertNotIn('nav-fold', page)
        self.assertIn('<span class="nav-group" data-group="rules">rules</span>', page)

    def test_reference_entry_page_tables_scroll_in_place(self):
        table = '| Before… | Read… |\n|---|---|\n| Quoting | evidence |\n'
        self.write('docs/topics/ref/index.md', '+++\ntitle = "Ref"\nbody_class = "reference-page"\ntoc = []\n+++\n\n# Ref\n\n' + table)
        self.write('docs/topics/plain/index.md', '+++\ntitle = "Plain"\ntoc = []\n+++\n\n# Plain\n\n' + table)
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + ''.join(
            f'\n[[nav]]\nlabel = "{slug}"\nfile = "{slug}.html"\n' for slug in ('ref', 'plain')))
        self.assertEqual(self.build().returncode, 0)
        self.assertIn('<div class="scroll" role="region" tabindex="0" data-reader-horizontal aria-label="Table: Before…, Read…"><table>',
                      self.page('ref'))
        self.assertNotIn('class="scroll"', self.page('plain'))

    def test_reader_merges_a_short_opening_into_the_first_chapter(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text().replace(
            'slug = "shared-rule"\n', 'slug = "shared-rule"\nreader = true\n'))
        self.write('policy/rule.md', '# Shared rule\n\nA short opening.\n\n## First part\n\nBody.\n')
        self.assertEqual(self.build().returncode, 0)
        page = self.page('shared-rule')
        self.assertNotIn('reader-introduction', page)
        chapter = page.index('id="first-part"')
        self.assertLess(chapter, page.index('class="source-origin"'))
        self.assertLess(chapter, page.index('A short opening.'))
        self.write('policy/rule.md', '# Shared rule\n\n' + 'A long opening sentence. ' * 40 + '\n\n## First part\n\nBody.\n')
        self.assertEqual(self.build().returncode, 0)
        self.assertIn('id="reader-introduction"', self.page('shared-rule'))

    def test_nested_navigation_must_be_boolean(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('nested_nav = "yes"\n' + config.read_text())
        self.assertFails('nested_nav must be true or false')


if __name__ == '__main__':
    unittest.main()
