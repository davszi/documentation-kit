"""The figure palettes: readable text, visible marks, series that stay apart, and the two-file naming."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))

import figure_themes  # noqa: E402
import svg_figures  # noqa: E402
from figure_themes import DARK, LIGHT, matplotlib_rc, palette, variant_path, write_both  # noqa: E402

HAS_MATPLOTLIB = importlib.util.find_spec('matplotlib') is not None
TEXT_CONTRAST, MARK_CONTRAST = 4.5, 3.0  # WCAG ratios: body text, and graphical marks
APART, APART_DEFICIENT = 15.0, 8.0       # OKLab distance x100 between neighbours in the series order

# Machado, Oliveira and Fernandes (2009), severity 1.0, applied to linear RGB.
PROTAN = ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998))
DEUTAN = ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881))


def linear(color: str) -> tuple[float, float, float]:
    channels = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)


def contrast(first: str, second: str) -> float:
    lum = sorted((0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in (linear(first), linear(second))), reverse=True)
    return (lum[0] + 0.05) / (lum[1] + 0.05)


def oklab(rgb) -> tuple[float, float, float]:
    r, g, b = (min(max(c, 0.0), 1.0) for c in rgb)
    l, m, s = (v ** (1 / 3) for v in (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
                                      0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
                                      0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def distance(first: str, second: str, seen=None) -> float:
    def see(color):
        rgb = linear(color)
        return rgb if seen is None else tuple(sum(k * c for k, c in zip(row, rgb)) for row in seen)
    return 100 * sum((a - b) ** 2 for a, b in zip(oklab(see(first)), oklab(see(second)))) ** 0.5


class Palettes(unittest.TestCase):
    def test_text_reads_on_both_surfaces(self):
        for p in (DARK, LIGHT):
            for role in ('ink', 'sub', 'dim'):
                for surface in ('bg', 'panel'):
                    ratio = contrast(getattr(p, role), getattr(p, surface))
                    self.assertGreaterEqual(ratio, TEXT_CONTRAST, f'{p.name}: {role} on {surface} is {ratio:.2f}:1')

    def test_marks_show_on_both_surfaces(self):
        for p in (DARK, LIGHT):
            for color in (*p.series, p.alert):
                for surface in (p.bg, p.panel):
                    ratio = contrast(color, surface)
                    self.assertGreaterEqual(ratio, MARK_CONTRAST, f'{p.name}: {color} on {surface} is {ratio:.2f}:1')

    def test_neighbours_in_the_series_order_stay_apart(self):
        for p in (DARK, LIGHT):
            order = (*p.series, p.alert)
            for first, second in zip(order, order[1:]):
                self.assertGreaterEqual(distance(first, second), APART, f'{p.name}: {first} and {second}')
                for name, seen in (('protan', PROTAN), ('deutan', DEUTAN)):
                    self.assertGreaterEqual(distance(first, second, seen), APART_DEFICIENT,
                                            f'{p.name}: {first} and {second} for {name}')

    def test_the_order_matters_for_the_dark_palette(self):
        # Violet next to blue is the pair the fixed order keeps apart.
        self.assertLess(distance(DARK.violet, DARK.blue, DEUTAN), APART_DEFICIENT)
        self.assertNotIn((DARK.violet, DARK.blue), list(zip(DARK.series, DARK.series[1:])))
        self.assertNotIn((DARK.blue, DARK.violet), list(zip(DARK.series, DARK.series[1:])))

    def test_the_svg_helpers_use_the_dark_palette(self):
        for name in ('ink', 'sub', 'dim', 'line', 'panel', 'bg', 'accent', 'warm', 'violet', 'blue', 'alert'):
            self.assertEqual(getattr(svg_figures, name.upper()), getattr(DARK, name))

    def test_unknown_theme_is_refused(self):
        with self.assertRaisesRegex(ValueError, "figure theme 'sepia' is not one of: dark, light"):
            palette('sepia')


class Files(unittest.TestCase):
    def test_the_light_file_lies_beside_the_dark_one(self):
        self.assertEqual(variant_path('docs/figures/speed.svg'), Path('docs/figures/speed.svg'))
        self.assertEqual(variant_path('docs/figures/speed.svg', 'light'), Path('docs/figures/speed.light.svg'))
        self.assertEqual(variant_path('a/run.v2.png', 'light'), Path('a/run.v2.light.png'))

    def test_svg_text_is_written_in_both_themes(self):
        with tempfile.TemporaryDirectory() as folder:
            written = write_both(Path(folder) / 'box.svg', lambda c: f'<svg><rect fill="{c.bg}" stroke="{c.accent}"/></svg>')
            self.assertEqual([path.name for path in written], ['box.svg', 'box.light.svg'])
            self.assertEqual(written[0].read_text(), f'<svg><rect fill="{DARK.bg}" stroke="{DARK.accent}"/></svg>\n')
            self.assertEqual(written[1].read_text(), f'<svg><rect fill="{LIGHT.bg}" stroke="{LIGHT.accent}"/></svg>\n')

    def test_anything_else_is_refused(self):
        with tempfile.TemporaryDirectory() as folder, self.assertRaisesRegex(TypeError, 'SVG text or a matplotlib figure'):
            write_both(Path(folder) / 'box.svg', lambda c: 3)


@unittest.skipUnless(HAS_MATPLOTLIB, 'matplotlib is not installed')
class Matplotlib(unittest.TestCase):
    @staticmethod
    def draw(colors):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 3))
        for offset in range(3):
            ax.plot([0, 1, 2], [offset, offset + 1, offset + 3], label=f'series {offset}')
        ax.set_title('Title')
        ax.set_xlabel('x')
        ax.grid(True)
        ax.legend()
        return fig

    def test_the_settings_are_valid_and_colour_the_figure(self):
        import matplotlib
        for p in (DARK, LIGHT):
            with matplotlib.rc_context(matplotlib_rc(p.name)):
                cycle = [entry['color'] for entry in matplotlib.rcParams['axes.prop_cycle']]
                self.assertEqual(cycle, list(p.series))
                fig = self.draw(p)
                ax = fig.axes[0]
                same = matplotlib.colors.same_color
                self.assertTrue(same(fig.get_facecolor(), p.bg))
                self.assertTrue(same(ax.get_facecolor(), p.bg))
                self.assertTrue(same(ax.title.get_color(), p.ink))
                self.assertTrue(same(ax.lines[1].get_color(), p.series[1]))
                matplotlib.pyplot.close(fig)

    def test_both_files_are_written_and_stay_the_same_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'plot.svg'
            first = [path.read_bytes() for path in write_both(target, self.draw)]
            second = [path.read_bytes() for path in write_both(target, self.draw)]
            self.assertEqual(first, second)
            dark, light = (data.decode() for data in first)
            self.assertIn(DARK.bg, dark)
            self.assertNotIn(DARK.bg, light)
            self.assertIn(LIGHT.accent, light)
            self.assertNotIn('<dc:date>', dark)
            png = write_both(Path(folder) / 'plot.png', self.draw, dpi=60)
            self.assertEqual([path.name for path in png], ['plot.png', 'plot.light.png'])
            self.assertTrue(all(path.read_bytes().startswith(b'\x89PNG') for path in png))


if __name__ == '__main__':
    unittest.main()
