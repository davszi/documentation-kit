"""A project's own site colours: the [theme_colors] table, its stylesheet, its contrast checks and its figures."""
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

import figure_themes  # noqa: E402
import theme_colors  # noqa: E402
from test_figure_themes import distance  # noqa: E402

HAS_CRYPTOGRAPHY = importlib.util.find_spec('cryptography') is not None
# A warm dark brown, the palette a consuming project asked for.
BROWN = {'bg': '#2b211b', 'bg2': '#30251e', 'panel': '#3a2c23', 'panel2': '#44342a', 'border': '#59493a',
         'text': '#e6dccd', 'bright': '#f2e9dc', 'muted': '#b3a593'}
BROWN_TOML = '\n[theme_colors]\n' + ''.join(f'{key} = "{value}"\n' for key, value in BROWN.items())
THEME_CSS = [*sorted((KIT / 'theme/components').glob('*.css')), *sorted((KIT / 'theme/assets').glob('*.css'))]


def root_properties() -> dict[str, str]:
    """The custom properties base.css defines on :root."""
    block = re.search(r':root\{(.*?)\n\}', (KIT / 'theme/components/base.css').read_text(), re.S)[1]
    block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
    return {name: value.strip() for name, value in re.findall(r'--([\w-]+):([^;]+);', block)}


def outside_print(css: str) -> str:
    """The stylesheet without its @media print blocks, which keep their own colours."""
    while (start := css.find('@media print')) >= 0:
        depth, i = 0, css.index('{', start)
        while True:
            depth += {'{': 1, '}': -1}.get(css[i], 0)
            i += 1
            if depth == 0:
                break
        css = css[:start] + css[i:]
    return css


class Table(unittest.TestCase):
    def test_known_keys_and_hex_colours_pass(self):
        self.assertEqual(theme_colors.problems(BROWN), [])
        self.assertEqual(theme_colors.problems({'accent': '#3cb'}), [])
        self.assertEqual(theme_colors.problems({}), [])

    def test_an_unknown_key_names_the_supported_ones(self):
        found = theme_colors.problems({'background': '#000000'})
        self.assertEqual(len(found), 1)
        self.assertIn("theme_colors sets 'background', which is not a theme colour", found[0])
        self.assertIn('bg, bg2, panel, panel2, border, text, bright, muted, accent, secondary, blue, link, '
                      'orange, red, green', found[0])
        # A derived colour is not set directly: it follows the base colours it mixes.
        self.assertIn("'sidebar-bg', which is not a theme colour", theme_colors.problems({'sidebar-bg': '#000'})[0])

    def test_a_value_must_be_an_opaque_hex_colour(self):
        for value in ('red', '#12345', '#11223344', '#fff;}body{display:none', 3, '#ggg'):
            found = theme_colors.problems({'bg': value})
            self.assertEqual(len(found), 1, value)
            self.assertIn(f"theme_colors gives 'bg' the value {value!r}; use a 3 or 6 digit hex colour", found[0])

    def test_a_value_that_is_not_a_table_is_refused(self):
        self.assertIn('theme_colors must be a [theme_colors] table', theme_colors.problems('#2b211b')[0])


class Colours(unittest.TestCase):
    def test_base_css_holds_the_kit_values_of_every_colour(self):
        props = root_properties()
        for name, value in theme_colors.BASE.items():
            self.assertEqual(props[name], value, name)
        for name, (kit, *_) in theme_colors.DERIVED.items():
            self.assertEqual(props[name], kit, name)
        colors = theme_colors.resolve()
        for name in theme_colors.CHANNELS:
            channels = ','.join(str(int(colors[name][i:i + 2], 16)) for i in (1, 3, 5))
            self.assertEqual(props[name + '-rgb'], channels, name)

    def test_without_a_table_every_colour_is_the_kit_value(self):
        colors = theme_colors.resolve()
        self.assertEqual({name: colors[name] for name in theme_colors.BASE}, theme_colors.BASE)
        self.assertEqual({name: colors[name] for name in theme_colors.DERIVED},
                         {name: kit for name, (kit, *_) in theme_colors.DERIVED.items()})

    def test_each_mix_of_the_kit_colours_stays_close_to_the_kit_value(self):
        # The mixes recolour a project's site in the kit's steps. Each was fitted to the kit's
        # value; the line tint alone is neutral on purpose, where the kit's is blue.
        anchors = {**theme_colors.BASE, 'black': '#000000', 'white': '#ffffff'}
        for name, (kit, first, share, second) in theme_colors.DERIVED.items():
            mixed = theme_colors.mix(anchors[first], share, anchors[second])
            # A group tone is a lighter step of a hue in another direction than the hue itself.
            limit = 5.0 if name == 'rule' else 7.0 if name in theme_colors.HUE_DERIVED else 2.5
            self.assertLess(distance(mixed, kit), limit, f'{name}: {mixed} for {kit}')

    def test_mix_is_srgb_color_mix(self):
        self.assertEqual(theme_colors.mix('#ffffff', 50, '#000000'), '#808080')
        self.assertEqual(theme_colors.mix('#2b211b', 100, '#000000'), '#2b211b')
        self.assertEqual(theme_colors.mix('#2b211b', 72, '#000000'), '#1f1813')

    def test_a_derived_colour_follows_only_the_base_colours_it_mixes(self):
        colors = theme_colors.resolve({'accent': '#ff8800'})
        self.assertEqual(colors['accent'], '#ff8800')
        self.assertEqual(colors['sidebar-bg'], '#080c13')
        colors = theme_colors.resolve({'bg': '#2b211b'})
        self.assertEqual(colors['sidebar-bg'], '#1f1813')
        self.assertEqual(colors['figure-bg'], '#2b211b')
        self.assertEqual(colors['nav-text'], '#dbe2ea')   # text and bright are the kit's

    def test_the_stylesheet_sets_only_what_the_table_changes(self):
        css = theme_colors.stylesheet({'accent': '#FF8800'}).decode()
        # The accent and the first group tone, a lighter step of it, and nothing else.
        self.assertEqual(css, '/* Generated from [theme_colors] in docs/site/site.toml. */\n'
                              ':root{\n  --accent:#ff8800;\n  --accent-rgb:255,136,0;\n'
                              '  --group-tone-1:#ffac4d;\n  --group-tone-1-rgb:255,172,77;\n}\n')
        css = theme_colors.stylesheet(BROWN).decode()
        self.assertIn('  --bg:#2b211b;\n  --bg-rgb:43,33,27;\n', css)
        self.assertIn('  --sidebar-bg:#1f1813;\n  --sidebar-bg-rgb:31,24,19;\n', css)
        self.assertIn('  --figure-bg:#2b211b;\n', css)
        self.assertNotIn('--accent', css)
        self.assertEqual(css.count('{'), 1)  # one :root rule and nothing else

    def test_the_theme_reads_no_property_the_kit_does_not_define(self):
        props = set(root_properties())
        defined = set()
        for path in THEME_CSS:
            defined |= set(re.findall(r'(--[\w-]+)\s*:', path.read_text()))
        for path in sorted((KIT / 'theme/components').glob('*.js')):
            defined |= set(re.findall(r"setProperty\(['\"](--[\w-]+)", path.read_text()))
        for path in THEME_CSS:
            for name in re.findall(r'var\((--[\w-]+)', path.read_text()):
                self.assertTrue(name[2:] in props or name in defined, f'{path.name} reads {name}')

    def test_no_navy_or_grey_literal_is_left_outside_print(self):
        # Hues with a meaning of their own (syntax colours, fold types, the tinted diagram box
        # edges), the light backdrop of site-map pictures and white and black stay literal;
        # every neutral and every group tone reads a property.
        kept = {'#000', '#000000', '#fff', '#ffffff',
                '#a99df0', '#5dcaa5', '#85b7eb', '#f0997b', '#e3b341', '#ff7b9d', '#7ee787', '#56d4dd',
                '#2f7f76', '#7c5cad', '#a35d5d', '#f7f8fa'}
        kit_values = {*theme_colors.BASE.values(), *(kit for kit, *_ in theme_colors.DERIVED.values())}
        for path in THEME_CSS:
            css = outside_print(path.read_text())
            css = re.sub(r':root\{.*?\n\}', '', css, flags=re.S)
            css = re.sub(r'var\(--[\w-]+,\s*#[0-9a-fA-F]+\)', '', css)  # fallbacks of a property
            for literal in re.findall(r'#[0-9a-fA-F]{3,8}\b', css):
                self.assertIn(literal.lower(), kept, f'{path.name} writes {literal}')
                self.assertNotIn(literal.lower(), kit_values, f'{path.name} writes {literal}')
            for channels in re.findall(r'rgba?\((\d+\s*,\s*\d+\s*,\s*\d+)', css):
                self.assertIn(channels.replace(' ', ''), {'0,0,0', '255,255,255'}, f'{path.name} writes rgba({channels})')

    def test_scripts_draw_their_controls_in_theme_colours(self):
        # Styles that scripts inject read the same properties, with the kit's value as fallback.
        # The reader's own scripts are left for the reader branch; fold-controls.js stays literal.
        reserved = {'chapter-reader.js', 'fold-controls.js', 'slide-face.js'}
        for path in sorted((KIT / 'theme/components').glob('*.js')):
            if path.name in reserved:
                continue
            text = re.sub(r'var\(--[\w-]+,\s*[^()]*\)', '', path.read_text())  # a property with its fallback
            literals = re.findall(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b(?![\w-])', text)
            self.assertEqual([c for c in literals if c.lower() not in {'#fff', '#000'}], [], path.name)
            for channels in re.findall(r'rgba?\((\d+\s*,\s*\d+\s*,\s*\d+)', text):
                self.assertIn(re.sub(r'\s', '', channels), {'0,0,0', '255,255,255'}, f'{path.name} writes rgba({channels})')


class Contrast(unittest.TestCase):
    def test_the_kit_colours_and_the_brown_palette_pass(self):
        self.assertEqual(theme_colors.contrast_problems(), [])
        self.assertEqual(theme_colors.contrast_problems(BROWN), [])
        self.assertEqual(figure_themes.problems(figure_themes.project_dark(BROWN)), [])

    def test_a_failing_pair_is_named_with_its_colours_and_ratio(self):
        found = theme_colors.contrast_problems({'muted': '#3a3a3a'})
        self.assertIn('theme_colors: text colour muted #3a3a3a on bg #0d1117 has contrast', found[0])
        self.assertIn('text needs at least 4.5:1', found[0])
        # A light page would make the kit's hues and white sidebar text unreadable.
        found = '\n'.join(theme_colors.contrast_problems({'bg': '#ffffff'}))
        self.assertIn('text colour bright #e6edf3 on bg #ffffff', found)
        self.assertIn('text colour accent #39d2c0 on bg #ffffff', found)

    def test_code_comments_keep_their_contrast(self):
        self.assertIn(('faint', 'bg2'), theme_colors.TEXT_PAIRS)
        found = '\n'.join(theme_colors.contrast_problems({'bg2': '#4a4f55'}))
        self.assertIn('text colour faint #768390 on bg2 #4a4f55', found)

    def test_a_ratio_just_below_the_floor_never_reads_as_passing(self):
        self.assertEqual(theme_colors.shown_ratio(4.4995), '4.49')
        self.assertEqual(theme_colors.shown_ratio(4.5), '4.50')
        self.assertEqual(theme_colors.shown_ratio(12.268), '12.26')

    def test_the_slide_tones_keep_their_contrast(self):
        # is-held is a dashed outline on the slide; is-alert is red text and outline on a tile.
        found = '\n'.join(theme_colors.contrast_problems({'panel2': '#5a5a5a', 'muted': '#5a5a5a'}))
        self.assertIn('mark colour figure-held', found)
        found = '\n'.join(theme_colors.contrast_problems({'red': '#5a1a1a'}))
        self.assertIn('text colour red #5a1a1a on figure-panel', found)
        self.assertIn('mark colour red #5a1a1a on figure-panel', found)

    def test_figure_marks_are_checked_on_the_project_surfaces(self):
        found = figure_themes.problems(figure_themes.project_dark({'bg': '#3a9a8a', 'panel2': '#3a9a8a'}))
        self.assertTrue(any(line.startswith('dark figures: mark accent #39d2c0 on bg #3a9a8a') for line in found),
                        found)


class Figures(unittest.TestCase):
    def project(self, table: str) -> Path:
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-theme-figures-')
        self.addCleanup(folder.cleanup)
        root = Path(folder.name)
        (root / 'docs/site').mkdir(parents=True)
        (root / 'docs/site/site.toml').write_text('title = "Figures"\n' + table)
        return root

    def test_without_a_table_the_dark_palette_is_the_kit_one(self):
        self.assertEqual(figure_themes.palette('dark', root=self.project('')), figure_themes.DARK)

    def test_the_dark_palette_takes_the_project_surfaces(self):
        dark = figure_themes.palette('dark', root=self.project(BROWN_TOML))
        colors = theme_colors.resolve(BROWN)
        self.assertEqual((dark.bg, dark.panel, dark.line, dark.ink, dark.sub, dark.dim),
                         (BROWN['bg'], colors['figure-panel'], colors['figure-line'], BROWN['bright'],
                          colors['figure-sub'], colors['figure-dim']))
        # Series and alert stay the kit's, so a project's figures keep their colour meanings.
        self.assertEqual(dark.series, figure_themes.DARK.series)
        self.assertEqual(dark.alert, figure_themes.DARK.alert)
        self.assertEqual(figure_themes.palette('light', root=self.project(BROWN_TOML)), figure_themes.LIGHT)

    def test_write_both_draws_on_the_project_background_from_the_project_root(self):
        root = self.project(BROWN_TOML)
        old = os.environ.get('DOCSITE_PROJECT_ROOT')
        os.environ['DOCSITE_PROJECT_ROOT'] = str(root)
        self.addCleanup(lambda: os.environ.pop('DOCSITE_PROJECT_ROOT') if old is None
                        else os.environ.__setitem__('DOCSITE_PROJECT_ROOT', old))
        written = figure_themes.write_both(root / 'box.svg', lambda c: f'<svg><rect fill="{c.bg}"/></svg>')
        self.assertEqual(written[0].read_text(), f'<svg><rect fill="{BROWN["bg"]}"/></svg>\n')
        self.assertEqual(written[1].read_text(), f'<svg><rect fill="{figure_themes.LIGHT.bg}"/></svg>\n')

    def test_a_palette_that_fails_its_checks_writes_no_figure(self):
        root = self.project('\n[theme_colors]\nbg = "#39d2c0"\n')
        with self.assertRaisesRegex(ValueError, r'\[theme_colors\] makes the dark figure palette hard to read: '
                                                r'dark figures: text ink'):
            figure_themes.palette('dark', root=root)
        os.environ['DOCSITE_PROJECT_ROOT'] = str(root)
        self.addCleanup(os.environ.pop, 'DOCSITE_PROJECT_ROOT')
        with self.assertRaises(ValueError):
            figure_themes.write_both(root / 'box.svg', lambda c: '<svg/>')
        self.assertFalse((root / 'box.svg').exists())

    def test_an_invalid_table_is_named(self):
        with self.assertRaisesRegex(ValueError, "theme_colors sets 'page'"):
            figure_themes.palette('dark', root=self.project('\n[theme_colors]\npage = "#000000"\n'))


def docsite(*args, env=None):
    environment = {name: value for name, value in (env or os.environ).items()
                   if name not in ('GITHUB_SHA', 'DOCSITE_PROJECT_ROOT')}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)], cwd=KIT,
                          capture_output=True, text=True, env=environment)


def stylesheets(page: str) -> list[str]:
    return re.findall(r'<link rel="stylesheet" href="(?:\.\./)*(?:docs/html/)?assets/([^"?]+)', page)


class Site(unittest.TestCase):
    """The table in a real project: the stylesheet, its link on every page kind and the checks."""

    def setUp(self):
        import page_lock_fixture
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-theme-colors-')
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        # The lock fixture has topic and reader-free pages, registered and listed Reference
        # pages, a Reference index (the lock writes it) and a page lock for `publish`.
        self.root = page_lock_fixture.make_project(self.folder / 'project', lock=True)
        self.site = self.root / 'docs/site/site.toml'
        self.text = self.site.read_text()
        self.html = self.root / '.build/docs/html'

    def build(self, extra=''):
        self.site.write_text(self.text + extra)
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        return docsite('build', '--project', self.root)

    def outputs(self) -> dict[str, bytes]:
        out = self.root / '.build/docs'
        return {path.relative_to(out).as_posix(): path.read_bytes() for path in sorted(out.rglob('*')) if path.is_file()}

    def test_without_the_table_nothing_is_written_or_linked_and_output_is_unchanged(self):
        self.assertEqual(self.build().returncode, 0)
        before = self.outputs()
        self.assertNotIn('html/assets/theme-colors.css', before)
        self.assertFalse(any(b'theme-colors' in data for data in before.values()))
        # An empty table changes nothing, and a table that comes and goes leaves no trace.
        self.assertEqual(self.build('\n[theme_colors]\n').returncode, 0)
        self.assertEqual(self.outputs(), before)
        self.assertEqual(self.build(BROWN_TOML).returncode, 0)
        self.assertNotEqual(self.outputs(), before)
        self.assertEqual(self.build().returncode, 0)
        self.assertEqual(self.outputs(), before)

    def test_every_page_links_the_stylesheet_right_after_base_css(self):
        result = self.build(BROWN_TOML)
        self.assertEqual(result.returncode, 0, result.stderr)
        css = (self.html / 'assets/theme-colors.css').read_bytes()
        self.assertEqual(css, theme_colors.stylesheet(BROWN))
        pages = sorted(self.html.glob('*.html'))
        names = {page.name for page in pages}
        # Topic page with the reader, a reader-free page, the home page, a registered record page,
        # automatically listed pages and the Reference index.
        self.assertLessEqual({'guide.html', 'widgets.html', 'index.html', 'rule.html', 'notes.record.md.html',
                              'docs.project_context.md.html', 'reference.index.html'}, names)
        for page in pages:
            self.assertEqual(stylesheets(page.read_text())[:2], ['base.css', 'theme-colors.css'], page.name)
        lint = docsite('lint', '--project', self.root, '--strict')
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_slide_decks_link_the_stylesheet(self):
        self.site.write_text(self.text + BROWN_TOML)
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        result = docsite('slides', '--project', self.root, '--select', 'guide', '--out', 'deck')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        deck = (self.root / '.build/slides/deck.html').read_text()
        self.assertEqual(stylesheets(deck)[:2], ['base.css', 'theme-colors.css'])

    @unittest.skipUnless(HAS_CRYPTOGRAPHY, 'cryptography is not installed; pip install -r requirements-lock.txt')
    def test_the_lock_page_links_the_stylesheet(self):
        self.site.write_text(self.text + BROWN_TOML)
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        out = self.folder / 'site'
        env = dict(os.environ, DOCSITE_GENERAL_PASSWORD='general secret', DOCSITE_REFERENCE_PASSWORD='reference secret')
        result = docsite('publish', '--project', self.root, '--out', out, env=env)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((out / 'assets/theme-colors.css').read_bytes(), theme_colors.stylesheet(BROWN))
        for name in ('guide.html', 'rule.html'):
            page = (out / name).read_text()
            self.assertIn('id="page-lock-data"', page, name)
            self.assertEqual(stylesheets(page), ['base.css', 'theme-colors.css', 'page-lock.css'], name)

    def test_every_bad_key_is_named_in_one_error(self):
        result = self.build('\n[theme_colors]\npage = "#000000"\nbg = "navy"\n')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr.count('error:'), 1, result.stderr)
        self.assertIn("theme_colors sets 'page', which is not a theme colour", result.stderr)
        self.assertIn("theme_colors gives 'bg' the value 'navy'", result.stderr)

    def test_a_bad_table_stops_the_build_and_lint_with_the_reason(self):
        for table, message in (
                ('page = "#000000"', "theme_colors sets 'page', which is not a theme colour"),
                ('bg = "navy"', "theme_colors gives 'bg' the value 'navy'"),
                ('muted = "#30251e"', 'text colour muted #30251e on bg #0d1117 has contrast'),
                ('bg = "#39d2c0"', 'dark figures: text ink #e6edf3 on bg #39d2c0')):
            result = self.build('\n[theme_colors]\n' + table + '\n')
            self.assertEqual(result.returncode, 2, table)
            self.assertIn(message, result.stderr, table)
            lint = docsite('lint', '--project', self.root)
            self.assertNotEqual(lint.returncode, 0, table)
            self.assertIn(message, lint.stdout + lint.stderr, table)


if __name__ == '__main__':
    unittest.main()
