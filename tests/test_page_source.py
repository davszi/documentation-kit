"""`page_source`: a page's frontmatter and include-expanded body, equal to what the build inlines."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))

from page_source import INCLUDE_DEPTH, PageSourceError, expand_includes, page_source  # noqa: E402

PAGE = '+++\ntitle = "Guide"\ntoc = []\n+++\n'


def project(test) -> Path:
    folder = tempfile.TemporaryDirectory(prefix='docs-kit-page-source-')
    test.addCleanup(folder.cleanup)
    root = Path(folder.name).resolve()
    subprocess.run(['git', 'init', '-q', root], check=True)
    (root / 'docs/site/fragments').mkdir(parents=True)
    (root / 'docs/topics/guide').mkdir(parents=True)
    return root


def track(root: Path) -> None:
    subprocess.run(['git', 'add', '-A'], cwd=root, check=True)


class PageSource(unittest.TestCase):
    def setUp(self):
        self.root = project(self)
        self.page = self.root / 'docs/topics/guide/index.md'
        self.fragments = self.root / 'docs/site/fragments'

    def write(self, body, **fragments):
        self.page.write_text(PAGE + body)
        for name, text in fragments.items():
            (self.fragments / f'{name}.html').write_text(text)
        track(self.root)

    def problems(self, path=None):
        with self.assertRaises(PageSourceError) as caught:
            page_source(self.page if path is None else path, self.root)
        return caught.exception.problems

    def test_frontmatter_and_body_come_apart(self):
        self.page.write_text('+++\ntitle = "Guide"\ntoc = ["a"]\nmath = true\n+++\n# Body\n\n+++ stays\n')
        track(self.root)
        meta, body = page_source('docs/topics/guide/index.md', self.root)
        self.assertEqual(meta, {'title': 'Guide', 'toc': ['a'], 'math': True})
        self.assertEqual(body, '# Body\n\n+++ stays\n')
        self.assertEqual(page_source(self.page, self.root), (meta, body))  # absolute path, same result

    def test_frontmatter_keys_are_not_validated(self):
        self.page.write_text('+++\nnot_a_key = 1\n+++\ntext\n')
        track(self.root)
        self.assertEqual(page_source(self.page, self.root), ({'not_a_key': 1}, 'text\n'))

    def test_frontmatter_that_cannot_be_read_raises(self):
        for raw, part in (('# No fence\n', 'missing +++ frontmatter fence at top'),
                          ('+++\ntitle = "x"\n', 'unterminated +++ frontmatter'),
                          ('+++\ntitle = \n+++\nbody\n', 'frontmatter TOML error')):
            self.page.write_text(raw)
            track(self.root)
            problems = self.problems()
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(f'docs/topics/guide/index.md: {part}', problems[0])

    def test_nested_includes_are_expanded_in_place(self):
        self.write('before\n<!-- include: fragments/outer.html -->\nafter\n<!--include:fragments/inner.html-->\n',
                   outer='<p>outer</p>\n<!-- include: fragments/inner.html -->\n', inner='<p>inner</p>\n')
        _, body = page_source(self.page, self.root)
        self.assertEqual(body, 'before\n<p>outer</p>\n<p>inner</p>\n\n\nafter\n<p>inner</p>\n\n')

    def test_later_build_steps_are_not_applied(self):
        text = '<!-- site-map -->\n<!-- slide -->\n**bold**\n'
        self.write(text)
        self.assertEqual(page_source(self.page, self.root)[1], text)

    def test_a_cycle_raises(self):
        self.write('<!-- include: fragments/a.html -->\n', a='<p>a</p>\n<!-- include: fragments/b.html -->\n',
                   b='<p>b</p>\n<!-- include: fragments/a.html -->\n')
        problems = self.problems()
        self.assertEqual(len(problems), 1, problems)
        self.assertIn('include cycle: a.html -> b.html -> fragments/a.html', problems[0])

    def test_a_path_that_leaves_the_project_raises(self):
        outside = self.root.parent / f'{self.root.name}-outside.html'
        outside.write_text('<p>secret</p>\n')
        self.addCleanup(outside.unlink)
        for target in (f'../../../{outside.name}', str(outside)):
            # The problem after it is still named: one bad path does not hide the next.
            self.write(f'<!-- include: {target} -->\n<!-- include: fragments/missing.html -->\n')
            problems = self.problems()
            self.assertEqual(problems[0], 'docs/topics/guide/index.md: include paths must stay inside the theme or '
                                          f'project: {target}')
            self.assertIn('fragments/missing.html', problems[1])
            self.assertNotIn('secret', ' '.join(problems))
        (self.fragments / 'link.html').symlink_to(outside)
        self.write('<!-- include: fragments/link.html -->\n')
        self.assertIn('Project resource escapes its root', self.problems()[0])

    def test_text_below_the_page_end_marker_is_left_out_as_in_the_build(self):
        self.write('shown\n<!-- page-end -->\nnotes\n<!-- include: fragments/missing.html -->\n')
        self.assertEqual(page_source(self.page, self.root)[1], 'shown\n')

    def test_a_fragment_that_cannot_be_read_is_a_named_problem(self):
        (self.fragments / 'binary.html').write_bytes(b'\xff\xfe not text')
        (self.fragments / 'loop.html').symlink_to(self.fragments / 'loop.html')
        (self.fragments / 'folder.html').mkdir()
        (self.fragments / 'folder.html/keep.txt').write_text('x\n')
        self.write('<!-- include: fragments/binary.html -->\n<!-- include: fragments/loop.html -->\n'
                   '<!-- include: fragments/folder.html -->\n<!-- include: fragments/missing.html -->\n')
        problems = self.problems()
        self.assertEqual(len(problems), 4, problems)
        self.assertIn('include cannot be read as text: fragments/binary.html (UnicodeDecodeError)', problems[0])
        self.assertIn('fragments/loop.html', problems[1])
        self.assertIn('fragments/folder.html', problems[2])
        self.assertIn('fragments/missing.html', problems[3])

    @unittest.skipIf(os.geteuid() == 0, 'root reads every file')
    def test_a_fragment_without_read_permission_is_a_named_problem(self):
        self.write('<!-- include: fragments/closed.html -->\n', closed='<p>closed</p>\n')
        (self.fragments / 'closed.html').chmod(0)
        self.addCleanup((self.fragments / 'closed.html').chmod, 0o644)
        self.assertIn('include cannot be read as text: fragments/closed.html (PermissionError)', self.problems()[0])

    def test_a_tracked_file_whose_name_is_not_utf8_does_not_stop_other_pages(self):
        try:
            self.root.joinpath(os.fsdecode(b'odd-\xff.txt')).write_text('x\n')
        except OSError:
            self.skipTest('the file system refuses the name')
        self.write('<!-- include: fragments/part.html -->\n', part='<p>part</p>\n')
        self.assertEqual(page_source(self.page, self.root)[1], '<p>part</p>\n\n')

    def test_a_relative_project_and_a_real_theme_fragment(self):
        theme_file = next(path for path in sorted((KIT / 'theme/components').glob('*.html')))
        self.write(f'<!-- include: components/{theme_file.name} -->\n')
        before = os.getcwd()
        self.addCleanup(os.chdir, before)
        os.chdir(self.root.parent)
        _, body = page_source('docs/topics/guide/index.md', self.root.name)
        self.assertEqual(body, theme_file.read_text() + '\n')

    def test_a_missing_untracked_or_empty_include_raises(self):
        self.write('<!-- include: fragments/missing.html -->\n')
        self.assertIn('include not found or not tracked: fragments/missing.html', self.problems()[0])
        self.write('<!-- include: fragments/blank.html -->\n', blank=' \n')
        self.assertIn('include is empty: fragments/blank.html', self.problems()[0])
        (self.fragments / 'new.html').write_text('<p>new</p>\n')  # written after the last git add
        self.page.write_text(PAGE + '<!-- include: fragments/new.html -->\n')
        self.assertIn('must be tracked by the consumer Git repository', self.problems()[0])

    def test_depth_is_bounded(self):
        fragments = {f'n{level}': f'<p>n{level}</p>\n<!-- include: fragments/n{level + 1}.html -->\n'
                     for level in range(1, INCLUDE_DEPTH)}
        fragments[f'n{INCLUDE_DEPTH}'] = '<p>last</p>\n'
        self.write('<!-- include: fragments/n1.html -->\n', **fragments)
        self.assertIn('<p>last</p>', page_source(self.page, self.root)[1])
        fragments[f'n{INCLUDE_DEPTH}'] = f'<!-- include: fragments/n{INCLUDE_DEPTH + 1}.html -->\n'
        self.write('<!-- include: fragments/n1.html -->\n', **fragments, **{f'n{INCLUDE_DEPTH + 1}': '<p>too deep</p>\n'})
        self.assertIn(f'includes nest deeper than {INCLUDE_DEPTH} levels', self.problems()[0])

    def test_every_problem_of_a_page_is_named_at_once(self):
        self.page.write_text('+++\ntitle = \n+++\n<!-- include: fragments/one.html -->\n<!-- include: fragments/two.html -->\n')
        track(self.root)
        problems = self.problems()
        self.assertEqual(len(problems), 3, problems)
        self.assertIn('frontmatter TOML error', problems[0])
        self.assertIn('fragments/one.html', problems[1])
        self.assertIn('fragments/two.html', problems[2])
        self.assertIn('fragments/two.html', str(PageSourceError(list(problems))))

    def test_a_page_or_project_that_cannot_be_read_raises(self):
        self.assertIn('cannot read the page', self.problems(self.root / 'docs/topics/guide/none.md')[0])
        with tempfile.TemporaryDirectory() as plain:
            (Path(plain) / 'page.md').write_text(PAGE)
            with self.assertRaisesRegex(PageSourceError, 'not a Git repository'):
                page_source('page.md', plain)

    def test_a_theme_fragment_wins_over_a_project_one(self):
        with tempfile.TemporaryDirectory() as theme:
            (Path(theme) / 'fragments').mkdir()
            (Path(theme) / 'fragments/shared.html').write_text('<p>theme</p>\n')
            self.write('', shared='<p>project</p>\n')
            seen = []
            text = expand_includes('<!-- include: fragments/shared.html -->', 'page', site=self.root / 'docs/site',
                                   local=lambda path: self.fail('the project must not be asked'),
                                   problem=seen.append, kit_site=Path(theme).resolve())
            self.assertEqual((text, seen), ('<p>theme</p>\n', []))

    def test_importing_reads_no_environment_and_two_projects_stay_apart(self):
        other = project(self)
        (other / 'docs/topics/guide/index.md').write_text(PAGE + '<!-- include: fragments/part.html -->\n')
        (other / 'docs/site/fragments/part.html').write_text('<p>other</p>\n')
        track(other)
        self.write('<!-- include: fragments/part.html -->\n', part='<p>first</p>\n')
        self.assertEqual(page_source(self.page, self.root)[1], '<p>first</p>\n\n')
        self.assertEqual(page_source('docs/topics/guide/index.md', other)[1], '<p>other</p>\n\n')
        code = ('import os, sys; sys.path.insert(0, sys.argv[1]); import page_source; '
                'print(sorted(name for name in sys.modules if name in ("build", "site_paths")))')
        env = {name: value for name, value in os.environ.items() if name != 'DOCSITE_PROJECT_ROOT'}
        result = subprocess.run([sys.executable, '-c', code, str(KIT / 'tooling')], capture_output=True, text=True,
                                env=env, cwd=tempfile.gettempdir())
        self.assertEqual(result.stdout.strip(), '[]', result.stderr)


class EqualsTheBuild(unittest.TestCase):
    """One implementation: the helper returns what the build's own functions inline for the same page."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-page-source-build-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name).resolve()
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        init = subprocess.run([sys.executable, str(KIT / 'docsite.py'), 'init', str(self.root)], capture_output=True)
        self.assertEqual(init.returncode, 0)
        self.guide = self.root / 'docs/topics/guide/index.md'
        fragments = self.root / 'docs/site/fragments'
        fragments.mkdir(parents=True, exist_ok=True)
        (fragments / 'outer.html').write_text('<p id="outer-part">outer 4117</p>\n<!-- include: fragments/inner.html -->\n')
        (fragments / 'inner.html').write_text('<p id="inner-part">inner 9052</p>\n')
        self.guide.write_text(self.guide.read_text() + '\n<!-- include: fragments/outer.html -->\n'
                              '\n<!-- page-end -->\n\nNotes 7731, never rendered.\n<!-- include: fragments/none.html -->\n')
        track(self.root)

    def from_build(self):
        # The steps of build_page that shape the source: frontmatter, the page-end cut, the includes.
        code = ('import json, sys; sys.path.insert(0, sys.argv[1]); import build, page_source; from pathlib import Path; '
                'page = Path(sys.argv[2]); meta, body = build.parse_frontmatter(page.read_text(), "guide/index.md"); '
                'body = build.expand_includes(page_source.rendered_part(body), "guide/index.md"); '
                'print(json.dumps([meta, body, build._errors]))')
        result = subprocess.run([sys.executable, '-c', code, str(KIT / 'tooling'), str(self.guide)], capture_output=True,
                                text=True, cwd=self.root, env=dict(os.environ, DOCSITE_PROJECT_ROOT=str(self.root)))
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_helper_and_build_give_the_same_metadata_and_text(self):
        meta, body, errors = self.from_build()
        self.assertEqual(errors, [])
        self.assertEqual(page_source(self.guide, self.root), (meta, body))
        self.assertIn('inner 9052', body)
        self.assertNotIn('include:', body)
        built = subprocess.run([sys.executable, str(KIT / 'docsite.py'), 'build', '--project', str(self.root)],
                               capture_output=True, text=True)
        self.assertEqual(built.returncode, 0, built.stderr)
        html = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('<p id="outer-part">outer 4117</p>', html)
        self.assertIn('<p id="inner-part">inner 9052</p>', html)
        # The build renders nothing below the page-end marker, and the helper returns nothing from there.
        self.assertNotIn('7731', html)
        self.assertNotIn('7731', body)

    def test_helper_and_build_name_the_same_problems(self):
        text = self.guide.read_text()
        self.guide.write_text(text.replace('<!-- page-end -->', '<!-- include: fragments/missing.html -->\n'
                                           '<!-- include: /etc/hostname -->\n<!-- page-end -->'))
        _, _, errors = self.from_build()
        self.assertEqual(len(errors), 2, errors)
        with self.assertRaises(PageSourceError) as caught:
            page_source(self.guide, self.root)
        self.assertEqual([problem.replace('docs/topics/', '') for problem in caught.exception.problems], errors)

    def test_the_build_holds_no_copy(self):
        source = (KIT / 'tooling/build.py').read_text()
        self.assertNotIn('INCLUDE_RE.sub', source)
        self.assertNotIn('tomllib.loads(raw', source)
        self.assertIn('page_source.expand_includes(', source)
        self.assertIn('page_source.split_frontmatter(', source)
        self.assertNotIn('.split(PAGE_END', source)
        self.assertEqual(source.count('page_source.rendered_part('), 2)


if __name__ == '__main__':
    unittest.main()
