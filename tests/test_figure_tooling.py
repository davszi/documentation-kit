"""Generator tooling: SVG figure helpers."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling"))
import svg_figures  # noqa: E402


def drawing(title="Rates and draws", desc="Two bars."):
    parts = svg_figures.svg_open(100, 40, title, desc)
    parts.append(svg_figures.text(4, 20, "rate 0.1", fill="var(--accent,#39d2c0)"))
    return "\n".join(parts + ["</svg>"])


class SvgFigures(unittest.TestCase):
    def test_figure_numbers_caption_and_labels_once(self):
        out = svg_figures.figure("rates", "R1", drawing(title="Rates' draws"), "Caption with <a href=\"#x\">a link</a>.")
        self.assertIn('<figure class="network-plate" id="rates">', out)
        self.assertIn('aria-label="Rates&#x27; draws"', out)
        self.assertNotIn("&amp;#x27;", out)
        self.assertIn('<figcaption><b>Figure R1.</b> Caption with <a href="#x">a link</a>.</figcaption>', out)
        self.assertNotIn("{id}", out)

    def test_slide_has_no_ids_and_standalone_resolves_variables(self):
        slide = svg_figures.slide_svg(drawing())
        self.assertNotIn(" id=", slide)
        self.assertIn('aria-label="Two bars."', slide)
        image = svg_figures.standalone(drawing())
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', image)
        self.assertNotIn("var(--", image)
        self.assertIn('fill="#39d2c0"', image)


class SvgEdges(unittest.TestCase):
    def test_standalone_after_a_comment_and_slide_after_figure_ids(self):
        header = svg_figures.generated_header("make.py", ["data.json"])
        image = svg_figures.standalone(header + '<svg\n viewBox="0 0 4 4" xmlns="http://www.w3.org/2000/svg"><rect/></svg>')
        self.assertEqual(image.count("xmlns="), 1)
        plain = svg_figures.standalone(header + '<svg viewBox="0 0 4 4"><rect/></svg>')
        self.assertEqual(plain.count('xmlns="http://www.w3.org/2000/svg"'), 1)
        named = drawing(desc='Quote " and <tag>').replace("{id}", "fig")
        slide = svg_figures.slide_svg(named)
        self.assertNotIn("aria-labelledby", slide)
        self.assertIn('aria-label="Quote &quot; and &lt;tag&gt;"', slide)


if __name__ == "__main__":
    unittest.main()
