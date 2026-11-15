"""Lint's slide-face checks: one face that opens each chapter, and no number only on a face."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import slide_face_checks as checks

KIT = Path(__file__).resolve().parents[1]


def face(inner: str) -> str:
    return f'<div class="slide-face" data-slide-face><div class="slide-canvas">\n{inner}\n</div></div>\n'


def chapter(identifier: str, body: str) -> str:
    return (f'<section class="card reader-adapted" id="{identifier}" data-reader-chapter="">\n'
            f'<section class="card">\n{body}</section>\n</section>\n')


def page(*chapters: str) -> str:
    return '<!doctype html><html><body><main>\n' + ''.join(chapters) + '</main></body></html>\n'


def run(*chapters: str):
    return checks.check_page(page(*chapters), 'docs/topics/demo/index.md (demo.html)')


def only_on_face(face_text: str, chapter_text: str) -> list[str]:
    """The warnings for one chapter whose face shows `face_text` and whose body shows `chapter_text`."""
    errors, warnings, _, _ = run(chapter('c', face(f'<p class="slide-title">{face_text}</p>')
                                         + f'<h2>Chapter</h2><p>{chapter_text}</p>'))
    assert errors == [], errors
    return warnings


class FacePlacement(unittest.TestCase):
    def test_one_face_that_opens_its_chapter_is_in_order(self):
        errors, warnings, notes, counts = run(chapter('a', face('<p>Face</p>') + '<h2>A</h2><p>Text.</p>'))
        self.assertEqual((errors, warnings, notes), ([], [], []))
        self.assertEqual(counts['faces'], 1)

    def test_two_faces_in_one_chapter_are_an_error_naming_page_and_chapter(self):
        errors, *_ = run(chapter('a', face('<p>One</p>') + face('<p>Two</p>') + '<h2>A</h2>'),
                         chapter('b', face('<p>Three</p>') + '<h2>B</h2>'))
        self.assertEqual(errors, ['docs/topics/demo/index.md (demo.html), chapter "a": 2 slide faces; '
                                  'a chapter opens with at most one'])

    def test_a_face_later_in_its_chapter_does_not_open_it(self):
        errors, *_ = run(chapter('a', '<h2>A</h2><p>Text first.</p>' + face('<p>Face</p>')))
        self.assertEqual(errors, ['docs/topics/demo/index.md (demo.html), chapter "a": the slide face does '
                                  "not open the chapter; write it at the chapter's start"])
        text_first, *_ = run(chapter('a', 'Loose words ' + face('<p>Face</p>')))
        self.assertEqual(len(text_first), 1)

    def test_wrappers_comments_and_a_generated_heading_may_come_first(self):
        body = ('<!-- a comment -->\n<div class="wrap">' + face('<p>Face</p>') + '</div><h2>A</h2>')
        self.assertEqual(run(chapter('a', body))[0], [])
        intro = '<h2 data-reader-generated="">Introduction</h2>\n' + face('<p>Face</p>') + '<p>Intro.</p>'
        self.assertEqual(run(chapter('reader-introduction', intro))[0], [])

    def test_a_face_outside_every_chapter_is_an_error(self):
        errors, *_ = checks.check_page(page(face('<p>Loose</p>'), chapter('a', '<h2>A</h2>')), 'x.html')
        self.assertEqual(errors, ['x.html: a slide face outside every chapter; a face opens a chapter'])

    def test_pages_without_the_reader_use_their_outermost_cards(self):
        markup = ('<main><section class="card" id="a">' + face('<p>One</p>') + face('<p>Two</p>')
                  + '<section class="card"><h3>Inner</h3></section></section></main>')
        errors, *_ = checks.check_page(markup, 'plain.html')
        self.assertEqual(errors, ['plain.html, chapter "a": 2 slide faces; a chapter opens with at most one'])


class NumbersOnlyOnAFace(unittest.TestCase):
    def test_a_number_the_chapter_lacks_is_a_warning_with_page_chapter_and_numbers(self):
        warnings = only_on_face('Error falls by 42% in 3 runs', 'Three runs, 3 in all.')
        self.assertEqual(warnings, ['docs/topics/demo/index.md (demo.html), chapter "c": numbers shown only on '
                                    'the slide face: 42%. State each in the chapter, or mark one shown on '
                                    'purpose with data-face-only="<reason>"'])

    def test_a_number_the_chapter_shows_anywhere_is_in_order(self):
        for chapter_text in ('<table><tr><td>42%</td></tr></table>', '<code>42%</code>',
                             '<svg><text>42%</text></svg>', '<img src="a.png" alt="error 42%">',
                             '<span aria-label="42%"></span>', '<abbr title="42%">most</abbr>',
                             '<noscript>42%</noscript>', '<div hidden>42%</div>'):
            with self.subTest(chapter_text):
                self.assertEqual(only_on_face('Error falls by 42%', chapter_text), [])

    def test_scripts_styles_and_templates_state_nothing_in_the_chapter(self):
        for chapter_text in ('<script>const v = "42%";</script>', '<style>/* 42% */</style>',
                             '<template><p>42%</p></template>'):
            with self.subTest(chapter_text):
                self.assertEqual(len(only_on_face('Error falls by 42%', chapter_text)), 1)

    def test_only_what_the_face_shows_is_read(self):
        hidden = ('<img src="a.png" alt="99 cases"><span aria-label="98 cases"></span><span hidden>97</span>'
                  '<svg><title>96</title><desc>95</desc><text>12</text></svg><script>94</script>'
                  '<style>.x{width:93px}</style><span class="slide-number">92 · </span>')
        self.assertEqual(only_on_face(hidden, '12'), [])
        self.assertEqual(len(only_on_face('<svg><text>12</text></svg>', '13')), 1)

    def test_text_is_split_at_every_element(self):
        self.assertEqual(only_on_face('Mean error<span>3,975</span>', 'a mean error of 3975'), [])
        self.assertEqual(only_on_face('<td>12</td><td>34</td>', '12 and 34'), [])


class Normalisation(unittest.TestCase):
    """Each pair is one number written two ways; each finding pair differs."""

    def test_same_number_written_differently(self):
        pairs = [
            ('1,036', '1036'), ('1036', '1,036'), ('1 036', '1036'), ('1 036', '1,036'),
            ('1 036', '1036'),                                           # thousands separators
            ('−0.5', '-0.5'), ('change −3', 'change -3'),               # Unicode minus
            ('0.500', '0.5'), ('3.0', '3'), ('2.50', '2.5000'), ('.5', '0.5'),   # trailing zeros, leading point
            ('−0.0', '0'),                                                   # negative zero is zero
            ('12 %', '12%'), ('12%', '12 %'), ('12<small>%</small>', '12%'),  # percent with or without space
            ('2026-11-15', 'on 2026-11-15'),                                      # a date is one number
        ]
        for shown, stated in pairs:
            with self.subTest(shown=shown, stated=stated):
                self.assertEqual(only_on_face(shown, stated), [])

    def test_different_numbers_stay_different(self):
        pairs = [('12%', '12'), ('12', '12%'), ('−3', '3'), ('-3', '3'), ('1.5', '15'),
                 ('0,5', '5'), ('2026-11-15', '2026'), ('30', '3'), ('3', '30')]
        for shown, stated in pairs:
            with self.subTest(shown=shown, stated=stated):
                self.assertEqual(len(only_on_face(shown, stated)), 1)

    def test_a_hyphen_between_numbers_is_no_sign(self):
        self.assertEqual(checks.numbers('pages 1-2, range 0.4–0.6, change -3, x−2'),
                         ['1', '2', '0.4', '0.6', '-3', '2'])

    def test_a_comma_separates_digit_groups_only_before_three_digits(self):
        self.assertEqual(checks.numbers('1,036 and (0,0) and 1,2345 and 12,345,678'),
                         ['1036', '0', '1', '12345678'])


class NotFacts(unittest.TestCase):
    def test_labels_and_names_are_not_counted(self):
        for decoration in ('01', '02 · 03', '<span>01</span><span>02</span>', 'Figure 3', 'see Fig. 2',
                           'Table 4', 'Chapter 5', 'Section 6', 'Appendix 1', 'version 1.2.3', 'H100 cards',
                           'v4 kit', 'file_2', 'name.5'):
            with self.subTest(decoration):
                self.assertEqual(only_on_face(decoration, 'nothing'), [])

    def test_a_step_count_is_a_fact(self):
        self.assertEqual(len(only_on_face('step 50 of 200', 'two hundred steps')), 1)

    def test_a_number_with_a_unit_after_it_is_a_number(self):
        self.assertEqual(only_on_face('2.5x faster, 16GB', '2.5 times, 16 GB'), [])
        self.assertEqual(len(only_on_face('16GB', '32 GB')), 1)


class AcceptedNumbers(unittest.TestCase):
    def accept(self, mark: str, chapter_text: str = 'nothing'):
        return run(chapter('c', face(f'<p>Rounded {mark} and 7</p>') + f'<h2>C</h2><p>{chapter_text} 7</p>'))

    def test_an_accepted_number_is_a_note_and_no_warning(self):
        errors, warnings, notes, counts = self.accept('<span data-face-only="rounded from 0.4712">0.47</span>')
        self.assertEqual((errors, warnings), ([], []))
        self.assertEqual(notes, ['docs/topics/demo/index.md (demo.html), chapter "c": 0.47 is shown only on '
                                 'the slide face, accepted: rounded from 0.4712'])
        self.assertEqual(counts['accepted'], 1)

    def test_the_acceptance_covers_only_the_marked_number(self):
        _, warnings, notes, _ = run(chapter('c', face('<p><b data-face-only="rounded">0.47</b> and 0.31</p>')
                                            + '<h2>C</h2>'))
        self.assertEqual(len(notes), 1)
        self.assertIn('numbers shown only on the slide face: 0.31.', warnings[0])

    def test_a_mark_needs_exactly_one_number(self):
        _, warnings, notes, _ = self.accept('<span data-face-only="two">0.47 and 0.48</span>')
        self.assertEqual(notes, [])
        self.assertIn('must hold exactly one number; it holds 2 (0.47, 0.48)', warnings[0])
        _, warnings, _, _ = self.accept('<span data-face-only="none">about half</span>')
        self.assertIn('must hold exactly one number; it holds 0', warnings[0])

    def test_a_mark_needs_a_reason(self):
        _, warnings, notes, _ = self.accept('<span data-face-only="">0.47</span>')
        self.assertEqual(notes, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn('the data-face-only mark on 0.47 gives no reason', warnings[0])

    def test_a_mark_whose_number_the_chapter_shows_is_no_longer_needed(self):
        _, warnings, notes, _ = self.accept('<span data-face-only="rounded">0.47</span>', 'now 0.470')
        self.assertEqual(notes, [])
        self.assertIn('the data-face-only mark on 0.47 is no longer needed; the chapter shows it', warnings[0])


class ProjectPages(unittest.TestCase):
    def test_pages_are_named_by_their_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'docs/topics/demo/index.md'
            source.parent.mkdir(parents=True)
            source.write_text('+++\ntitle = "Demo"\nslug = "shown"\n+++\n')
            built = root / '.build/docs/html'
            built.mkdir(parents=True)
            (built / 'shown.html').write_text(page(chapter('a', face('<p>1</p>') + face('<p>2</p>'))))
            (built / 'other.html').write_text(page(chapter('b', face('<p>5</p>') + '<p>4</p>')))
            errors, warnings, _, counts = checks.check(root)
            self.assertEqual(errors[0][:52], 'docs/topics/demo/index.md (shown.html), chapter "a":')
            self.assertTrue(warnings[0].startswith('.build/docs/html/other.html, chapter "b": numbers shown only'))
            self.assertEqual(counts, {'pages': 2, 'faces': 3, 'findings': 3, 'accepted': 0})


def git(root, *args):
    subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)


def invoke(*args):
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)], capture_output=True, text=True)


class LintCommand(unittest.TestCase):
    """End to end on the starter: two faces fail lint; a number only on a face fails --strict."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-slide-checks-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        git(self.root, 'init', '-q')
        self.assertEqual(invoke('init', self.root).returncode, 0)
        self.page = self.root / 'docs/topics/guide/index.md'
        self.text = self.page.read_text()
        self.assertIn('<p class="slide-title">Open a chapter with one slide, then read on</p>', self.text)

    def lint(self, text: str, *flags: str):
        self.page.write_text(text)
        git(self.root, 'add', '-A')
        built = invoke('build', '--project', self.root)
        self.assertEqual(built.returncode, 0, built.stderr)
        return invoke('lint', '--project', self.root, *flags)

    def test_the_starter_passes(self):
        result = self.lint(self.text, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_a_second_face_in_a_chapter_fails_lint(self):
        second = '<!-- slide -->\n<p class="slide-title">Another face</p>\n<!-- /slide -->\n'
        text = self.text.replace('<section class="card" id="slides">\n\n<!-- slide -->',
                                 '<section class="card" id="slides">\n\n' + second + '\n<!-- slide -->', 1)
        result = self.lint(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn('ERROR: docs/topics/guide/index.md (guide.html), chapter "slides": 2 slide faces; '
                      'a chapter opens with at most one', result.stderr)

    def test_a_number_only_on_a_face_fails_strict_until_it_is_accepted(self):
        title = '<p class="slide-title">Open a chapter with one slide, then read on</p>'
        text = self.text.replace(title, title.replace('one slide', 'one slide in 37 seconds'), 1)
        loose = self.lint(text)
        self.assertEqual(loose.returncode, 0, loose.stdout + loose.stderr)
        self.assertIn('WARN: docs/topics/guide/index.md (guide.html), chapter "slides": numbers shown only on '
                      'the slide face: 37.', loose.stdout)
        self.assertEqual(self.lint(text, '--strict').returncode, 1)
        accepted = text.replace('in 37 seconds', 'in <span data-face-only="an illustration">37</span> seconds')
        result = self.lint(accepted, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('NOTE: docs/topics/guide/index.md (guide.html), chapter "slides": 37 is shown only on '
                      'the slide face, accepted: an illustration', result.stdout)


if __name__ == '__main__':
    unittest.main()
