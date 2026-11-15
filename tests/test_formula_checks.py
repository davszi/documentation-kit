"""Lint's formula check: every formula on a built page compiles with the kit's KaTeX."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from formula_checks import check, find_node, page_formulas, split_at_delimiters

KIT = Path(__file__).resolve().parents[1]
RENDERER = '<script defer src="assets/katex/contrib/auto-render.min.js"></script>'


def page(body: str, renderer: bool = True) -> str:
    return (f'<html><head>{RENDERER if renderer else ""}</head><body>'
            f'<nav>\\(outside\\)</nav><main class="content" id="top">{body}</main>'
            f'<footer>\\(also outside</footer></body></html>')


def node_or_skip(test: unittest.TestCase) -> str:
    try:
        node = find_node()
    except ValueError as problem:
        test.fail(str(problem))
    if node is None:
        test.skipTest('Node.js is not installed; the compile step needs it')
    return node


class Delimiters(unittest.TestCase):
    def test_display_and_inline_formulas_in_one_run(self):
        self.assertEqual(split_at_delimiters('a $$x^2$$ b \\(y\\) c'),
                         ([('x^2', True), ('y', False)], None))

    def test_braces_keep_a_closing_delimiter_inside_the_formula(self):
        self.assertEqual(split_at_delimiters('\\(\\text{\\)}\\)'), ([('\\text{\\)}', False)], None))

    def test_an_unclosed_opening_is_returned_with_the_rest(self):
        self.assertEqual(split_at_delimiters('a \\(x+1 and more'), ([], '\\(x+1 and more'))

    def test_single_dollars_are_text(self):
        self.assertEqual(split_at_delimiters('Costs $10 and $20.'), ([], None))


class PageFormulas(unittest.TestCase):
    def test_reads_the_content_element_outside_code_like_the_renderer(self):
        formulas, split, unclosed = page_formulas(page(
            '<p><span class="math-inline">\\(a^2\\)</span> and raw \\(b &lt; c\\)</p>'
            '<div class="math">$$\\frac{1}{2}$$</div>'
            '<pre><code>$$not a formula$$ \\(neither</code></pre><code>\\(literal</code>'
            '<script>var s = "\\\\(";</script><p>$5 and $10</p>'))
        self.assertEqual(formulas, [('a^2', False), ('b < c', False), ('\\frac{1}{2}', True)])
        self.assertEqual((split, unclosed), ([], []))

    def test_a_formula_split_by_markdown_is_reported_once(self):
        # ADP's guard: markup inside the build's formula wrapper means Markdown split it.
        formulas, split, unclosed = page_formulas(page(
            '<p><span class="math-inline">\\(a<em>b</em>c\\)</span></p>'))
        self.assertEqual((formulas, split, unclosed), ([], ['\\(a<em>b</em>c\\)'], []))

    def test_a_wrapper_with_markup_and_no_open_delimiter_is_not_split(self):
        formulas, split, unclosed = page_formulas(page(
            '<div class="math"><span>a project\'s own wrapper</span> \\(x\\)</div>'))
        self.assertEqual((formulas, split, unclosed), ([('x', False)], [], []))

    def test_a_delimiter_that_never_closes_is_reported(self):
        formulas, split, unclosed = page_formulas(page(
            '<p>raw \\(x <b>bold</b> y\\)</p><span class="math-inline">\\(a{\\)</span>'))
        self.assertEqual((formulas, split), ([], []))
        self.assertEqual(unclosed, ['\\(x ', '\\(a{\\)'])


class Check(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-formulas-')
        self.addCleanup(folder.cleanup)
        self.html = Path(folder.name)
        self.names = {'guide.html': 'docs/topics/guide/index.md'}

    def write(self, name: str, markup: str) -> None:
        (self.html / name).write_text(markup)

    def test_a_formula_that_does_not_compile_is_an_error_with_page_and_formula(self):
        node = node_or_skip(self)
        self.write('guide.html', page('<span class="math-inline">\\(\\frac{a}{2}\\)</span>'
                                      '<div class="math">$$\\undefinedmacro{x}$$</div>'))
        errors, notes, summary = check(KIT, {}, self.html, self.names, find=lambda: node)
        self.assertEqual(len(errors), 1, errors)
        self.assertTrue(errors[0].startswith(
            'docs/topics/guide/index.md (guide.html): formula does not compile: $$\\undefinedmacro{x}$$ — '), errors[0])
        self.assertIn('Undefined control sequence', errors[0])
        self.assertEqual(notes, [])
        self.assertRegex(summary, r'^formula check: 1 of 2 formula\(s\) on 1 page\(s\) compile with KaTeX \d')

    def test_valid_formulas_pass_and_pages_without_the_renderer_are_skipped(self):
        node = node_or_skip(self)
        self.write('guide.html', page('<div class="math">$$R = P \\cup S$$</div>'))
        self.write('other.html', page('<div class="math">$$\\broken{$$</div>', renderer=False))
        errors, notes, summary = check(KIT, {}, self.html, self.names, find=lambda: node)
        self.assertEqual((errors, notes), ([], []))
        self.assertIn('1 of 1 formula(s) on 1 page(s)', summary)

    def test_split_and_unclosed_formulas_are_errors(self):
        self.write('guide.html', page('<span class="math-inline">\\(a<em>b</em>\\)</span><p>\\(open</p>'))
        errors, _, _ = check(KIT, {}, self.html, self.names, find=lambda: None)
        self.assertEqual(errors, [
            'docs/topics/guide/index.md (guide.html): formula split by Markdown: \\(a<em>b</em>\\)',
            'docs/topics/guide/index.md (guide.html): formula not closed in the same text: \\(open'])

    def test_without_node_the_check_is_a_note_unless_the_project_requires_it(self):
        self.write('guide.html', page('<div class="math">$$x$$</div>'))
        errors, notes, summary = check(KIT, {}, self.html, self.names, find=lambda: None)
        self.assertEqual((errors, summary), ([], None))
        self.assertEqual(notes, ['formula check skipped: Node.js was not found (set DOCS_NODE or put node on PATH); '
                                 '1 formula(s) on 1 page(s) were not compiled'])
        errors, notes, _ = check(KIT, {'formula_check_required': True}, self.html, self.names, find=lambda: None)
        self.assertEqual(notes, [])
        self.assertEqual(len(errors), 1)
        self.assertIn('formula_check_required = true', errors[0])

    def test_a_node_that_cannot_run_the_compiler_is_a_note_unless_required(self):
        self.write('guide.html', page('<div class="math">$$x$$</div>'))
        errors, notes, _ = check(KIT, {}, self.html, self.names, find=lambda: 'false')
        self.assertEqual(errors, [])
        self.assertEqual(len(notes), 1)
        self.assertIn('formula check could not run', notes[0])
        errors, notes, _ = check(KIT, {'formula_check_required': True}, self.html, self.names, find=lambda: 'false')
        self.assertEqual((len(errors), notes), (1, []))

    def test_lint_refuses_a_setting_that_is_not_a_boolean(self):
        self.write('guide.html', page('<div class="math">$$x$$</div>'))
        self.assertEqual(check(KIT, {'formula_check_required': 'yes'}, self.html, self.names, find=lambda: None),
                         (['site.toml: formula_check_required must be true or false'], [], None))

    def test_a_docs_node_that_names_nothing_is_an_error(self):
        self.write('guide.html', page('<div class="math">$$x$$</div>'))
        with mock.patch.dict(os.environ, {'DOCS_NODE': '/nonexistent/docs-kit-node'}):
            errors, notes, _ = check(KIT, {}, self.html, self.names)
        self.assertEqual(notes, [])
        self.assertEqual(errors, ['formula check could not run: DOCS_NODE names no executable: /nonexistent/docs-kit-node'])

    def test_a_site_without_math_pages_has_nothing_to_check(self):
        self.write('guide.html', page('<p>No formulas.</p>', renderer=False))
        self.assertEqual(check(KIT, {'formula_check_required': True}, self.html, self.names, find=lambda: None),
                         ([], [], None))


class LintCommand(unittest.TestCase):
    """The check runs inside `docsite.py lint` on a project the starter made."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-formula-lint-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        self.run_kit('init', self.root)

    def run_kit(self, *args, env=None):
        return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)], cwd=KIT,
                              capture_output=True, text=True, env=env)

    def test_a_broken_formula_fails_lint_with_its_page(self):
        node_or_skip(self)
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text().replace('R = P \\cup S', 'R = P \\cupp S'))
        subprocess.run(['git', 'add', 'docs', 'AGENTS.md', 'CLAUDE.md'], cwd=self.root, check=True)
        self.assertEqual(self.run_kit('build', '--project', self.root).returncode, 0)
        result = self.run_kit('lint', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ERROR: docs/topics/guide/index.md (guide.html): formula does not compile: $$', result.stderr)
        self.assertIn('R = P \\cupp S', result.stderr)

    def test_the_setting_must_be_a_boolean(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('formula_check_required = "yes"\n' + config.read_text())
        subprocess.run(['git', 'add', 'docs', 'AGENTS.md', 'CLAUDE.md'], cwd=self.root, check=True)
        result = self.run_kit('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('site.toml: formula_check_required must be true or false', result.stderr)


if __name__ == '__main__':
    unittest.main()
