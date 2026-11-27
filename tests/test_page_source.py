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


class MarkdownHeadings(unittest.TestCase):
    """One heading reader with each caller's rule as a keyword; these inputs show where the rules differ."""

    @staticmethod
    def anchors(text, **rules):
        from page_source import markdown_headings
        return [heading.anchor for heading in markdown_headings(text, **rules)]

    @staticmethod
    def texts(text, **rules):
        from page_source import markdown_headings
        return [heading.text for heading in markdown_headings(text, **rules)]

    def test_heading_fields(self):
        from page_source import Heading, markdown_headings
        self.assertEqual(markdown_headings('Intro\n\n## Result {#runs}\n## Result\n'),
                         [Heading(3, 7, 2, 'Result', 'runs'), Heading(4, 25, 2, 'Result', 'result')])

    def test_fences(self):
        # Lint and the record sections: a fence line may be indented, and either character closes it.
        self.assertEqual(self.anchors(' ```\n# In\n```\n# Out\n'), ['out'])
        self.assertEqual(self.anchors('```\n## A\n~~~\n## B\n'), ['b'])
        # A source page's title: only a fence line in the first column counts.
        self.assertEqual(self.anchors(' ```\n# In\n```\n', fences='column0'), ['in'])
        # The chapter index reads masked text and skips nothing itself.
        self.assertEqual(self.anchors('```\n## A\n```\n', fences=None), ['a'])
        # The worklog entries skip the blocks that fenced_spans finds: a fence closes only with its own kind.
        from worklog_entries import fenced_spans
        text = '````\n## A\n```\n## B\n````\n## C\n'
        self.assertEqual(self.anchors(text), ['b'])
        self.assertEqual(self.anchors(text, fences=None, skip=fenced_spans(text), line_breaks='newline'), ['c'])

    def test_line_breaks(self):
        # str.splitlines also breaks at a form feed, a lone carriage return and other Unicode breaks.
        self.assertEqual(self.anchors('a\x0c## B\n'), ['b'])
        self.assertEqual(self.anchors('a\x0c## B\n', line_breaks='newline'), [])
        self.assertEqual(self.anchors('a\r## B\n', line_breaks='newline'), [])
        with self.assertRaises(ValueError):
            self.anchors('', line_breaks='crlf')

    def test_syntax(self):
        from page_source import ATX_HEADING_WITH_TEXT, ENTRY_HEADING, TITLE_HEADING
        # Any white space separates in lint's reading; the chapter index wants a space or tab and some text.
        self.assertEqual(self.anchors('##\xa0x\n## \n'), ['x', ''])
        self.assertEqual(self.anchors('##\xa0x\n## \n##  \n', syntax=ATX_HEADING_WITH_TEXT), [''])
        # A source page's title is `# ` at level one; a worklog entry is `## ` at level two.
        self.assertEqual(self.texts('#\tTab\n## Two\n#  Title\n', syntax=TITLE_HEADING), ['Title'])
        self.assertEqual(self.texts('##\tTab\n### Three\n##  Entry\n', syntax=ENTRY_HEADING), ['Entry'])

    def test_frontmatter(self):
        self.assertEqual(self.anchors('+++\n# k\n+++\n# T\n'), ['k', 't'])
        self.assertEqual(self.anchors('+++\n# k\n+++\n# T\n', frontmatter=True), ['t'])
        self.assertEqual(self.anchors('+++\n# k\n', frontmatter=True), ['k'])  # never closed: read as text

    def test_id_suffix(self):
        from page_source import LAST_ID_SUFFIX
        text = '# A {#x} b {#y}\n'
        self.assertEqual(self.texts(text), ['A'])
        self.assertEqual(self.texts(text, id_suffix=LAST_ID_SUFFIX), ['A {#x} b'])
        self.assertEqual(self.texts(text, id_suffix=None), ['A {#x} b {#y}'])
        self.assertEqual(self.anchors(text), ['y'])
        self.assertEqual(self.anchors('# A {#x}}\n'), ['a'])  # no explicit id, the end is still cut off

    def test_seen_starts_the_numbering(self):
        from page_source import taken_ids
        self.assertEqual(self.anchors('## Menu\n## Menu\n', seen=taken_ids(reader=True)), ['menu-1', 'menu-2'])
        self.assertEqual(self.anchors('## Menu\n## Menu\n'), ['menu', 'menu-1'])

    def test_slugify_of_source_and_of_rendered_text(self):
        import html
        from page_source import slugify
        self.assertEqual(slugify('Results: a <em>b</em>  c'), 'results-a-b--c')
        # The build decodes character references in the rendered text first; the source text keeps them.
        self.assertEqual(slugify(html.unescape('a &amp; b')), 'a--b')
        self.assertEqual(slugify('a &amp; b'), 'a-amp-b')
        self.assertEqual(slugify(html.unescape('&lt;b&gt;x')), 'x')
        self.assertEqual(slugify('Straße İ'), 'straße-i')  # İ lowers to i and a combining dot, which is dropped

    def test_where_the_build_gives_another_id(self):
        # Present behaviour, not a contract: the build slugifies rendered text and allows only ASCII in `{#id}`.
        import re
        import build
        import mistune
        for text, source_id, built_id in [('## [L](u.md)\n', 'lumd', 'l'), ('## a &amp; b\n', 'a-amp-b', 'a--b'),
                                          ('## T {#título}\n', 'título', 't-título')]:
            with self.subTest(text=text):
                rendered = mistune.create_markdown(renderer=build.DocsRenderer(), plugins=['table', 'math'])(text)
                self.assertEqual(self.anchors(text), [source_id])
                self.assertEqual(re.findall(r'<h2 id="([^"]*)"', rendered), [built_id])


if __name__ == '__main__':
    unittest.main()
