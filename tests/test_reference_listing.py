"""Automatic Reference listing: the named folders and files, its settings and tolerance."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))

from source_pages import automatic_pages, automatic_route_base, reference_settings  # noqa: E402
from source_tree import INLINE_TREE_LIMIT, TREE_INDEX, TREE_SCRIPT  # noqa: E402

GONE = '<span class="link-gone" title="The target of this link no longer exists.">'


def invoke(*args):
    env = {name: value for name, value in os.environ.items() if name not in {'GITHUB_SHA', 'DOCSITE_PROJECT_ROOT'}}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True, env=env)


def git(root, *args):
    subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', *args],
                   cwd=root, check=True, capture_output=True)


class Settings(unittest.TestCase):
    def test_defaults_and_validation(self):
        self.assertEqual(reference_settings({}), (True, ('docs',)))
        self.assertEqual(reference_settings({'reference_listing': False, 'reference_roots': ['docs/', 'a/b', 'README.md']}),
                         (False, ('docs', 'a/b', 'README.md')))
        self.assertEqual(reference_settings({'reference_roots': []}), (True, ()))
        for site in ({'reference_listing': 'no'}, {'reference_roots': 'docs'}, {'reference_roots': ['a', 'a/']},
                     {'reference_roots': [1]}, {'reference_roots': ['/abs']}, {'reference_roots': ['../up']},
                     {'reference_roots': ['a\\b']}, {'reference_roots': ['']}, {'reference_roots': ['.']},
                     {'reference_roots': ['notes/**']}, {'reference_roots': ['notes/[a-z].md']}):
            with self.assertRaises(ValueError, msg=site):
                reference_settings(site)

    def test_the_removed_exclude_setting_fails_and_names_its_replacement(self):
        with self.assertRaises(ValueError) as raised:
            reference_settings({'reference_exclude': []})
        for part in ('reference_exclude was removed in kit 5.1.0', 'reference_roots', 'private_prefixes',
                     'migrations/5.1.0.md'):
            self.assertIn(part, str(raised.exception))

    def test_route_base_is_path_shaped(self):
        self.assertEqual(automatic_route_base('README.md'), ('readme.md', False))
        self.assertEqual(automatic_route_base('docs/topics/guide/guide.md'), ('docs.topics.guide.guide.md', True))
        self.assertEqual(automatic_route_base('docs/Design Notes/API v1.2.md'),
                         ('docs.design-notes.api-v1-2.md', False))
        self.assertEqual(automatic_route_base('docs/KIT_WORKLOG.md'), ('docs.kit_worklog.md', False))


class Project(unittest.TestCase):
    """A starter project with a few Markdown files outside its topic pages.

    The fixture names its folders and root files in `reference_roots`; a test
    of the default removes that line.
    """

    ROOTS = 'reference_roots = ["docs", "notes", "drafts", "README.md", "AGENTS.md"]'

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-reference-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        git(self.root, 'init', '-q')
        self.assertEqual(invoke('init', self.root).returncode, 0)
        self.config = self.root / 'docs/site/site.toml'
        self.write('README.md', '# Project\n\nSee [the notes](notes/plan.md#steps).\n')
        self.write('notes/plan.md', '# Plan\n\n## Steps\n\nBack to [the project](../README.md).\n')
        self.write('notes/deep/inner.md', '# Inner\n')
        self.write('drafts/idea.md', '# Idea\n')
        self.write('docs/topics/guide/extra.md', '# Extra record\n')
        self.write('docs/framed.md', '+++\ntitle = "Framed"\n+++\n\n# Framed\n')
        self.settings(self.ROOTS)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def settings(self, text):
        """Top-level settings go above the first [[nav]] table; a key set again replaces the starter's line."""
        key = text.split('=')[0].strip()
        lines = [line for line in self.config.read_text().splitlines(keepends=True) if not line.startswith(key + ' =')]
        self.config.write_text(''.join(lines).replace('[[nav]]', text + '\n\n[[nav]]', 1) if text.split('=', 1)[1].strip()
                               else ''.join(lines))

    def build(self, *options):
        git(self.root, 'add', '-A')
        return invoke('build', '--project', self.root, *options)

    def routes(self):
        manifest = json.loads((self.root / '.build/docs/site-build.json').read_text())
        return manifest['source_pages']

    def page(self, route):
        return (self.root / '.build/docs/html' / route).read_text()


class ReferenceListing(Project):
    def test_named_roots_list_their_tracked_markdown_files(self):
        self.write('untracked.md', '# Untracked\n')
        nested = self.root / 'vendor/lib'
        nested.mkdir(parents=True)
        git(nested, 'init', '-q')
        (nested / 'inside.md').write_text('# Inside a submodule\n')
        git(nested, 'add', '-A')
        git(nested, 'commit', '-q', '-m', 'Nested')
        git(self.root, 'add', 'README.md', 'notes', 'drafts', 'docs', 'AGENTS.md', 'CLAUDE.md', 'vendor/lib')
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        routes = self.routes()
        self.assertEqual(routes, {
            'agents.md.html': 'AGENTS.md',
            'docs.capability_map.md.html': 'docs/CAPABILITY_MAP.md',
            'docs.index.md.html': 'docs/index.md',
            'docs.open.open.md.html': 'docs/open/OPEN.md',
            'docs.project_context.md.html': 'docs/PROJECT_CONTEXT.md',
            'docs.topics.guide.extra.md.html': 'docs/topics/guide/extra.md',
            'docs.topics.guide.guide.md.html': 'docs/topics/guide/guide.md',
            'docs.worklog.md.html': 'docs/worklog.md',
            'drafts.idea.md.html': 'drafts/idea.md',
            'notes.deep.inner.md.html': 'notes/deep/inner.md',
            'notes.plan.md.html': 'notes/plan.md',
            'readme.md.html': 'README.md',
        })  # CLAUDE.md is in no root; frontmatter, topic, untracked and submodule files are skipped
        readme = self.page('readme.md.html')
        self.assertIn('href="notes.plan.md.html#steps"', readme)
        self.assertIn('<span class="repo-tree-label" id="repo-tree-label">Reference</span>', readme)
        self.assertIn('href="readme.md.html"', self.page('guide.html'))
        self.assertIn('href="readme.md.html"', self.page('notes.plan.md.html'))
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertNotIn('NOTE: reference page', lint.stdout)

    def test_default_lists_only_docs(self):
        self.settings('reference_roots =')  # no line: the default
        self.assertNotIn('reference_roots =', self.config.read_text().replace('# reference_roots =', ''))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(self.routes().values()), [
            'docs/CAPABILITY_MAP.md', 'docs/PROJECT_CONTEXT.md', 'docs/index.md', 'docs/open/OPEN.md',
            'docs/topics/guide/extra.md', 'docs/topics/guide/guide.md', 'docs/worklog.md'])
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertNotIn('NOTE: reference page', lint.stdout)

    def test_a_file_outside_the_roots_is_not_listed(self):
        self.settings('reference_roots = ["docs/topics", "notes/deep/", "README.md"]')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sorted(self.routes().values()), [
            'README.md', 'docs/topics/guide/extra.md', 'docs/topics/guide/guide.md', 'notes/deep/inner.md'])
        # A link to a file that is not listed stays a source link.
        self.assertIn('data-repo-path="notes/plan.md"', self.page('readme.md.html'))

    def test_a_root_is_a_whole_path_segment(self):
        self.write('notes-old/kept.md', '# Old\n')
        self.write('README.md.bak/inner.md', '# Inner\n')
        self.settings('reference_roots = ["notes", "README.md"]')
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(sorted(self.routes().values()), ['README.md', 'notes/deep/inner.md', 'notes/plan.md'])

    def test_a_root_that_lists_nothing_gets_a_note(self):
        self.settings('reference_roots = ["docs", "experiments", ".github"]')
        self.write('.github/template.md', '# Template\n')
        self.assertEqual(self.build().returncode, 0)
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        for entry in ('experiments', '.github'):
            self.assertIn(f"NOTE: reference page site.toml: reference_roots entry '{entry}' holds no tracked "
                          'Markdown file that can be listed', lint.stdout)
        self.assertNotIn("entry 'docs'", lint.stdout)

    def test_a_root_whose_only_file_is_registered_gets_no_note(self):
        self.settings('reference_roots = ["docs", "drafts"]')
        self.config.write_text(self.config.read_text() + '\n[[source_pages]]\nsource = "drafts/idea.md"\nslug = "idea"\n')
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(self.routes()['idea.html'], 'drafts/idea.md')
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertNotIn('reference_roots entry', lint.stdout)

    def test_invalid_settings_fail_with_a_clear_message(self):
        self.settings('reference_listing = "yes"')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('site.toml: reference_listing must be true or false', result.stderr)
        self.config.write_text(self.config.read_text().replace('reference_listing = "yes"\n', ''))
        self.settings('reference_roots = ["/notes"]')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("site.toml: reference_roots entry '/notes' must be a folder or Markdown file inside the project",
                      result.stderr)
        self.settings('reference_roots = ["docs"]')
        self.settings('reference_exclude = ["CLAUDE.md"]')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('site.toml: reference_exclude was removed in kit 5.1.0', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        lint = invoke('lint', '--project', self.root)
        self.assertNotEqual(lint.returncode, 0)
        self.assertIn('reference_exclude was removed in kit 5.1.0', lint.stdout + lint.stderr)

    def test_reference_listing_false_equals_the_explicit_registry_alone(self):
        self.settings('reference_listing = false')
        self.config.write_text(self.config.read_text() + '\n[[source_pages]]\nsource = "notes/plan.md"\nslug = "plan"\n')
        self.assertEqual(self.build().returncode, 0)
        listed = {path.relative_to(self.root).as_posix(): path.read_bytes()
                  for path in (self.root / '.build/docs').rglob('*') if path.is_file()}
        self.assertEqual(self.routes(), {'plan.html': 'notes/plan.md'})
        # The same site without any other Markdown file builds the same bytes.
        for relative in ('notes/deep/inner.md', 'drafts/idea.md', 'docs/topics/guide/extra.md'):
            git(self.root, 'rm', '-q', '--cached', relative)
            (self.root / relative).unlink()
        git(self.root, 'add', '-A')
        self.assertEqual(invoke('build', '--project', self.root).returncode, 0)
        rebuilt = {path.relative_to(self.root).as_posix(): path.read_bytes()
                   for path in (self.root / '.build/docs').rglob('*') if path.is_file()}
        self.assertEqual(listed.keys(), rebuilt.keys())
        self.assertEqual({name for name in listed if listed[name] != rebuilt[name]}, set())

    def test_explicit_table_overrides_and_registers_a_file_outside_the_roots(self):
        self.settings('reference_roots = ["docs", "README.md"]')
        self.config.write_text(self.config.read_text() + '\n[[source_pages]]\nsource = "notes/plan.md"\n'
                               'slug = "plan"\ntitle = "The plan"\npinned = true\n')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        routes = self.routes()
        self.assertEqual(routes['plan.html'], 'notes/plan.md')
        self.assertNotIn('notes.plan.md.html', routes)
        self.assertNotIn('notes/deep/inner.md', routes.values())
        readme = self.page('readme.md.html')
        self.assertIn('href="plan.html#steps"', readme)
        self.assertIn('<a class="repo-tree-pin" href="plan.html" title="notes/plan.md">The plan</a>', readme)

    def test_route_collisions_take_a_path_hash_and_never_fail(self):
        self.write('notes/My Plan.md', '# Spaced plan\n')
        self.write('notes/my-plan.md', '# Dashed plan\n')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        routes = self.routes()

        def hashed(stem, source):
            return stem + '-' + hashlib.sha256(source.encode()).hexdigest()[:8] + '.md.html'
        self.assertEqual(routes['notes.my-plan.md.html'], 'notes/my-plan.md')  # the lossless path keeps it
        self.assertEqual(routes[hashed('notes.my-plan', 'notes/My Plan.md')], 'notes/My Plan.md')
        # A route a topic or registered page already has (the build itself
        # refuses topic folders named *.md, so only the listing can show it).
        tracked = frozenset(self.root / name for name in ('README.md', 'notes/plan.md'))
        pages, notes = automatic_pages({'reference_roots': ['README.md', 'notes']}, self.root, tracked, [],
                                       {'readme.md.html'})
        self.assertEqual([page.route for page in pages], [hashed('readme', 'README.md'), 'notes.plan.md.html'])
        self.assertIn('README.md: route readme.md.html is also claimed by a topic or registered page', notes[0])
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertIn('NOTE: reference page notes/My Plan.md: route notes.my-plan.md.html is also claimed by '
                      'notes/my-plan.md', lint.stdout)
        # Routes are stable across builds.
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(self.routes(), routes)

    def test_problems_in_automatic_pages_are_notes(self):
        (self.root / 'notes/media').mkdir()
        (self.root / 'notes/media/kept.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
        (self.root / 'notes/media/ignored.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
        (self.root / '.gitignore').write_text('notes/media/ignored.png\n')
        self.write('notes/messy.md', '\n'.join([
            'No heading here. A [dead link](missing.md#x), an [absolute one](/etc/passwd),',
            'one [outside](../../outside.md), a [phone](tel:123), an [unknown anchor](#nowhere),',
            'a [bad fragment](plan.md#no-such-part) and [a good one](plan.md#steps).',
            '',
            '![missing](gone.png) ![untracked](media/ignored.png) ![kept](media/kept.png)',
            '![remote](https://example.com/x.png)',
            '',
            '<script src="https://example.com/x.js"></script>',
            '<div style="background: url(https://example.com/bg.png)">styled</div>',
            '',
            'Prose with url(https://example.com/a) and href="nowhere.html".',
            '',
            '```css',
            'body { background: url(https://example.com/b.png); }',
            '```',
            '',
            '<!-- an unclosed comment',
        ]) + '\n')
        (self.root / 'notes/latin1.md').write_bytes('# Caf\xe9 notes\n'.encode('latin-1'))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('problem(s) in automatically listed reference pages were tolerated', result.stdout)
        page = self.page('notes.messy.md.html')
        self.assertIn(' · messy</title>', page)
        self.assertIn(GONE + 'dead link</span>', page)
        self.assertIn(GONE + 'absolute one</span>', page)
        self.assertIn(GONE + 'outside</span>', page)
        self.assertIn(GONE + 'phone</span>', page)
        self.assertIn(GONE + 'unknown anchor</span>', page)
        self.assertIn(GONE + 'missing</span>', page)
        self.assertIn(GONE + 'untracked</span>', page)
        self.assertIn('src="_media/notes/media/kept.png"', page)
        self.assertIn('<a href="https://example.com/x.png">remote</a>', page)
        self.assertIn('&lt;script src=', page)
        self.assertNotIn('<script src="https://example.com', page)
        self.assertNotIn('url(https://', page)
        self.assertIn('href="notes.plan.md.html#no-such-part"', page)
        self.assertIn('Caf� notes', self.page('notes.latin1.md.html'))
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertIn('lint clean (0 warning(s))', lint.stdout)
        for expected in ('notes/messy.md: no level-one heading; the title is the file name',
                         'notes/messy.md: link target not found: missing.md#x',
                         'notes/messy.md: absolute link /etc/passwd',
                         'notes/messy.md: link escapes the repository: ../../outside.md',
                         'notes/messy.md: link scheme tel: is not served',
                         'notes/messy.md: link target not found: media/ignored.png',
                         'notes/messy.md: external media is not loaded; shown as a link',
                         'notes/messy.md: unclosed HTML comment shown as text',
                         'notes/messy.md: anchor #nowhere not found on its own page',
                         'notes.messy.md.html: anchor #no-such-part not found in notes.plan.md.html',
                         'notes/latin1.md: not valid UTF-8'):
            self.assertIn(expected, lint.stdout)

    def test_registered_pages_keep_their_strictness(self):
        self.write('notes/strict.md', '# Strict\n\n[dead](missing.md)\n')
        self.config.write_text(self.config.read_text() + '\n[[source_pages]]\nsource = "notes/strict.md"\nslug = "strict"\n')
        result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('notes/strict.md: link target not found: missing.md', result.stderr)

    def test_publication_carries_automatic_pages_and_their_media(self):
        (self.root / 'notes/media').mkdir()
        (self.root / 'notes/media/kept.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
        self.write('notes/plan.md', '# Plan\n\n## Steps\n\n![kept](media/kept.png) and ![secret](../configs/s.png)\n')
        (self.root / 'configs').mkdir()
        (self.root / 'configs/s.png').write_bytes(b'\x89PNG\r\n\x1a\nsecret')
        self.write('configs/notes.md', '# Private notes\n')
        self.settings(self.ROOTS.replace('"README.md"', '"configs", "README.md"'))  # named, and still private
        self.config.write_text(self.config.read_text() + '\n[publication]\npages = ["readme.md.html"]\n'
                               'private_suffixes = [".toml"]\nprivate_prefixes = ["configs/"]\n')
        self.assertEqual(self.build().returncode, 0)
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertIn('notes/plan.md: media file is not packaged (untracked, private or symlinked): ../configs/s.png',
                      lint.stdout)
        git(self.root, 'add', '-A')
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        published = {path.relative_to(destination).as_posix() for path in destination.rglob('*') if path.is_file()}
        for route in ('readme.md.html', 'notes.plan.md.html', 'notes.deep.inner.md.html', 'docs.worklog.md.html',
                      '_media/notes/media/kept.png'):
            self.assertIn(route, published)
        self.assertNotIn('configs.notes.md.html', published)  # private prefixes are never listed
        self.assertNotIn('_media/configs/s.png', published)
        self.assertIn(GONE + 'secret</span>', (destination / 'notes.plan.md.html').read_text())
        # Every Reference link in the published bundle opens a published page.
        sidebar = (destination / 'guide.html').read_text()
        for route in json.loads((self.root / '.build/docs/site-build.json').read_text())['source_pages']:
            self.assertIn(f'href="{route}"', sidebar)
            self.assertIn(route, published)

    def test_no_remote_builds_without_github_source_lines(self):
        self.config.write_text(self.config.read_text().replace(
            'gh_repo = "https://github.com/example/project"', 'gh_repo = ""'))
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        page = self.page('notes.plan.md.html')
        self.assertIn('class="source-origin"', page)
        self.assertNotIn('github.com', page[page.index('class="source-origin"'):].split('</p>')[0])
        self.assertNotIn('source-origin-edit', page)


class ReleaseReview(Project):
    """Defects the 4.x release review found in the automatic listing."""

    def publication(self, suffixes, prefixes=()):
        self.config.write_text(self.config.read_text() + '\n[publication]\npages = ["guide.html"]\n'
                               f'private_suffixes = {json.dumps(list(suffixes))}\n'
                               f'private_prefixes = {json.dumps(list(prefixes))}\n')

    def test_private_suffixes_are_never_listed(self):
        self.write('notes/plan.private.md', '# Private plan\n')
        self.publication(['.private.md'])
        self.assertEqual(self.build().returncode, 0)
        self.assertNotIn('notes/plan.private.md', self.routes().values())
        self.assertIn('notes/plan.md', self.routes().values())
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any('private' in path.name for path in destination.rglob('*.html')))

    def test_the_example_publication_config_lists_no_markdown(self):
        # rules/site/publication.md: private_suffixes = [".md", ".py", ".toml"].
        self.publication(['.md', '.py', '.toml'], ['configs/'])
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(self.routes(), {})
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(sorted(path.name for path in destination.rglob('*.md.html')), [])

    def test_publish_refuses_a_registered_page_from_a_private_file(self):
        self.publication(['.md'])
        self.config.write_text(self.config.read_text().replace(
            '\n[publication]', '\n[[source_pages]]\nsource = "notes/plan.md"\nslug = "plan"\n\n[publication]', 1))
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(self.routes(), {'plan.html': 'notes/plan.md'})
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Private source cannot be published as a page: notes/plan.md (plan.html)', result.stderr)
        self.assertFalse(destination.exists())

    def test_symlinked_markdown_is_not_listed(self):
        outside = tempfile.TemporaryDirectory(prefix='docs-kit-outside-')
        self.addCleanup(outside.cleanup)
        (Path(outside.name) / 'secret.md').write_text('# Outside the project\n')
        (self.root / 'notes/inside-link.md').symlink_to('plan.md')
        (self.root / 'notes/outside-link.md').symlink_to(Path(outside.name) / 'secret.md')
        (self.root / 'linked').symlink_to('notes', target_is_directory=True)
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        tracked = subprocess.run(['git', 'ls-files', '-s', 'notes/inside-link.md', 'notes/outside-link.md', 'linked'],
                                 cwd=self.root, capture_output=True, text=True, check=True).stdout
        self.assertEqual(tracked.count('120000'), 3, tracked)  # Git tracks all three as symlinks
        listed = set(self.routes().values())
        self.assertIn('notes/plan.md', listed)
        for source in ('notes/inside-link.md', 'notes/outside-link.md'):
            self.assertNotIn(source, listed)
        self.assertFalse(any('Outside the project' in path.read_text()
                             for path in (self.root / '.build/docs/html').glob('*.html')))

    def test_dot_folders_are_not_listed_but_can_be_registered(self):
        self.write('.github/pull_request_template.md', '# Pull request\n')
        self.write('.claude/agents/helper.md', '# Helper\n')
        self.write('docs/.draft.md', '# Draft\n')
        self.config.write_text(self.config.read_text()
                               + '\n[[source_pages]]\nsource = ".github/pull_request_template.md"\nslug = "pr-template"\n')
        result = self.build()
        self.assertEqual(result.returncode, 0, result.stderr)
        routes = self.routes()
        self.assertEqual(routes['pr-template.html'], '.github/pull_request_template.md')
        for source in ('.claude/agents/helper.md', 'docs/.draft.md'):
            self.assertNotIn(source, routes.values())
        self.assertFalse(any(route.startswith('-') for route in routes))

    def test_no_remote_publish_points_every_page_at_admitted_sources(self):
        self.config.write_text(self.config.read_text().replace(
            'gh_repo = "https://github.com/example/project"', 'gh_repo = ""')
            + '\n[publication]\npages = ["guide.html"]\nassets_manifest = "docs/site/public.json"\n')
        self.write('docs/site/public.json', json.dumps({'files': ['notes/plan.md']}))
        git(self.root, 'add', '-A')
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        page = (destination / 'notes.plan.md.html').read_text()  # not named in pages
        self.assertIn('class="source-origin-path" href="notes/plan.md"', page)
        self.assertNotIn('href="../../notes/plan.md"', page)
        self.assertTrue((destination / 'notes/plan.md').is_file())


class TreeSize(Project):
    """The Reference tree is inlined up to INLINE_TREE_LIMIT files and written once above it."""

    ROOTS = Project.ROOTS.replace('"drafts"', '"drafts", "many"')

    def files(self, count):
        for index in range(count):
            self.write(f'many/group{index % 5}/file{index:03d}.md', f'# File {index}\n')

    def test_small_tree_stays_inline(self):
        self.files(INLINE_TREE_LIMIT - 20)  # plus the fixture's and the starter's files
        self.assertEqual(self.build().returncode, 0)
        listed = len(self.routes())
        self.assertLessEqual(listed, INLINE_TREE_LIMIT)
        guide = self.page('guide.html')
        self.assertNotIn('data-repo-tree-src', guide)
        self.assertNotIn(TREE_INDEX, guide)
        for route in self.routes():
            self.assertIn(f'href="{route}"', guide)
        self.assertFalse((self.root / '.build/docs/html' / TREE_SCRIPT).exists())
        manifest = json.loads((self.root / '.build/docs/site-build.json').read_text())
        self.assertIsNone(manifest['reference_tree'])

    def test_large_tree_is_written_once(self):
        self.files(INLINE_TREE_LIMIT + 10)
        self.assertEqual(self.build().returncode, 0)
        routes = self.routes()
        self.assertGreater(len(routes), INLINE_TREE_LIMIT)
        html_root = self.root / '.build/docs/html'
        script = (html_root / TREE_SCRIPT).read_text()
        self.assertTrue(script.startswith('window.docsReferenceTree = "'))
        index = (html_root / TREE_INDEX).read_text()
        for route in routes:
            self.assertIn(route, script)
            self.assertIn(f'href="{route}"', index)
        manifest = json.loads((self.root / '.build/docs/site-build.json').read_text())
        self.assertEqual(manifest['reference_tree'], {'script': 'html/' + TREE_SCRIPT, 'index': 'html/' + TREE_INDEX})
        self.assertIn('html/' + TREE_SCRIPT, manifest['files'])

        # A page for people: pinned files, the closed disclosure and the index link only.
        guide = self.page('guide.html')
        digest = hashlib.sha256((html_root / TREE_SCRIPT).read_bytes()).hexdigest()[:10]
        self.assertIn(f'data-repo-tree-src="{TREE_SCRIPT}?v={digest}"', guide)
        self.assertNotIn('data-repo-tree-current', guide)
        self.assertIn('<details class="repo-tree-all"><summary><span class="repo-tree-name">Browse by folder</span>'
                      f'<span class="repo-tree-count" title="{len(routes)} files">{len(routes)}</span></summary>', guide)
        self.assertIn(f'<p class="repo-tree-index"><a href="{TREE_INDEX}">All {len(routes)} files on one page</a></p>',
                      guide)
        self.assertNotIn('many.group0.file000.md.html', guide)

        # A listed page: the open disclosure holds the folders leading to it, with full counts.
        page = self.page('many.group2.file007.md.html')
        self.assertIn('data-repo-tree-current="many.group2.file007.md.html" data-repo-tree-mark', page)
        self.assertIn('<details class="repo-tree-all" open>', page)
        self.assertIn('<li class="repo-tree-folder has-current"><details open><summary><span class="repo-tree-name">'
                      'many/</span><span class="repo-tree-count" title="70 files">70</span>', page)
        self.assertIn('<span class="repo-tree-name">group2/</span><span class="repo-tree-count" title="14 files">14',
                      page)
        self.assertIn('<a class="repo-tree-file current" aria-current="page" href="many.group2.file007.md.html"', page)
        self.assertNotIn('href="many.group2.file002.md.html"', page)
        self.assertNotIn('group1/', page)
        self.assertLess(len(page.encode()), len(index.encode()) + 4000)
        lint = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

        # A topic page that sets its own components still gets the loader.
        guide_source = self.root / 'docs/topics/guide/index.md'
        text = guide_source.read_text()
        self.assertIn('components = ["toc", "nav",', text)
        guide_source.write_text(text.replace('components = ["toc", "nav",', 'components = ["toc",'))
        self.assertEqual(self.build().returncode, 0)
        self.assertIn('assets/nav.js', self.page('guide.html'))

        # Publication carries the tree script and the index page.
        destination = self.root / '_site'
        self.config.write_text(self.config.read_text() + '\n[publication]\npages = ["guide.html"]\n')
        git(self.root, 'add', '-A')
        published = invoke('publish', '--project', self.root, '--out', destination)
        self.assertEqual(published.returncode, 0, published.stdout + published.stderr)
        self.assertTrue((destination / TREE_SCRIPT).is_file())
        self.assertTrue((destination / TREE_INDEX).is_file())


if __name__ == '__main__':
    unittest.main()
