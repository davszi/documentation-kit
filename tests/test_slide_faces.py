"""Slide-face markers, chapter extraction and deck export."""
from pathlib import Path
import unittest

import build
import slides


FACE = ('<!-- slide -->\n<p class="slide-eyebrow">Topic</p>\n<p class="slide-title">A finding</p>\n'
        '<div class="slide-main"><img src="../figures/plot.svg" alt=""></div>\n<!-- /slide -->\n')


class SlideMarkers(unittest.TestCase):
    def setUp(self):
        build._errors.clear()

    def tearDown(self):
        build._errors.clear()

    def test_markers_become_one_face_element(self):
        html = build.slides_to_html(FACE, "page.md")
        self.assertEqual(html.count('<div class="slide-face" data-slide-face><div class="slide-canvas">'), 1)
        self.assertEqual(html.count("</div>\n"), 2)
        self.assertNotIn("<!--", html)
        self.assertEqual(build._errors, [])

    def test_unbalanced_or_nested_markers_are_errors_and_left_untouched(self):
        for broken in (FACE.replace("<!-- /slide -->", ""), "<!-- slide -->\n<!-- slide -->\n<!-- /slide -->\n<!-- /slide -->\n",
                       "<!-- /slide -->\n<!-- slide -->\n"):
            build._errors.clear()
            self.assertEqual(build.slides_to_html(broken, "page.md"), broken)
            self.assertEqual(len(build._errors), 1)

    def test_marker_text_inside_a_line_is_not_a_marker(self):
        text = "Write `<!-- slide -->` at the start of a chapter.\n"
        self.assertEqual(build.slides_to_html(text, "page.md"), text)
        self.assertEqual(build._errors, [])


PAGE = """<!doctype html><html><head><link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/page.css"></head><body class="scoped">
<main><section class="card" data-reader-chapter id="first"><h2>First chapter</h2><p>Text.</p></section>
<section class="card" data-reader-chapter id="second"><div class="slide-face" data-slide-face><p class="slide-eyebrow">Topic</p>
<p class="slide-title">Second finding</p><img src="figures/a.svg" alt=""><a href="#first">jump</a><a href="https://example.org/x">out</a></div>
<div class="intro"><h2 id="second-title">Second chapter</h2></div></section></main></body></html>"""


class MarkdownAndFlatPages(unittest.TestCase):
    def setUp(self):
        build._errors.clear()

    def test_marker_examples_in_code_blocks_are_not_converted(self):
        import mistune
        source = "```html\n<!-- slide -->\n```\n\n    <!-- /slide -->\n"
        rendered = build.slides_to_html(mistune.create_markdown()(source), "page.md")
        self.assertNotIn("data-slide-face", rendered)
        self.assertIn("&lt;!-- slide --&gt;", rendered)
        self.assertEqual(build._errors, [])

    def test_face_before_a_flat_heading_opens_that_chapter(self):
        from chapter_layout import adapt_sections
        content = ('<div class="slide-face" data-slide-face><div class="slide-canvas"><p class="slide-title">F1</p></div></div>\n'
                   '<h2 id="a">First</h2><p>one</p>\n'
                   '<div class="slide-face" data-slide-face><div class="slide-canvas"><p class="slide-title">F2</p></div></div>\n'
                   '<h2 id="b">Second</h2><p>two</p>\n')
        markup, entries, _ = adapt_sections(content, [])
        self.assertEqual(entries, [["First", "#a"], ["Second", "#b"]])
        self.assertNotIn("reader-introduction", markup)
        first, second = markup.split('id="b"')
        self.assertIn("F1", first)
        self.assertNotIn("F2", first)
        self.assertIn("F2", second)

    def test_slide_headings_never_name_a_chapter(self):
        from chapter_layout import adapt_sections
        content = ('<section class="card" id="c"><div class="slide-face" data-slide-face><div class="slide-canvas">'
                   '<h3>Slide heading</h3></div></div><h2>Real title</h2></section>')
        _, entries, _ = adapt_sections(content, [])
        self.assertEqual(entries, [["Real title", "#c"]])


class DeckExport(unittest.TestCase):
    def test_chapters_number_in_reader_order_and_skip_face_headings(self):
        found = slides.chapters(PAGE)
        self.assertEqual([c["id"] for c in found], ["first", "second"])
        self.assertEqual([c["number"] for c in found], [1, 2])
        self.assertEqual(found[1]["title"], "Second chapter")
        self.assertIsNone(found[0]["face"])
        self.assertTrue(found[1]["face"].startswith('<div class="slide-face" data-slide-face>'))
        self.assertTrue(found[1]["face"].endswith("</div>"))

    def test_reroot_changes_only_relative_site_urls(self):
        out = slides.reroot('<img src="figures/a.svg"><a href="#first"></a><a href="https://example.org/x"></a>'
                            '<a href="../docs/html/x.html"></a><img data-gif="anim.gif">', "page")
        self.assertIn('src="../docs/html/figures/a.svg"', out)
        self.assertIn('href="../docs/html/page.html#first"', out)
        self.assertIn('href="https://example.org/x"', out)
        self.assertIn('href="../docs/html/x.html"', out)
        self.assertNotIn("../docs/html/../docs", out)
        self.assertIn('data-gif="../docs/html/anim.gif"', out)

    def test_reroot_covers_srcset_css_urls_svg_references_and_objects(self):
        out = slides.reroot('<img srcset="a.png 1x, b.png 2x" style="background:url(\'c.png\')">'
                            '<svg><use xlink:href="#g"/><rect fill="url(#g)"/></svg><object data="d.svg"></object>',
                            "page", {"g": "page--x--g"})
        self.assertIn('srcset="../docs/html/a.png 1x, ../docs/html/b.png 2x"', out)
        self.assertIn("url('../docs/html/c.png')", out)
        self.assertIn('xlink:href="#page--x--g"', out)
        self.assertIn('fill="url(#page--x--g)"', out)
        self.assertIn('data="../docs/html/d.svg"', out)

    def test_ids_are_prefixed_with_their_references(self):
        out, ids = slides.isolate_ids('<linearGradient id="g"/><p id="t"></p><button aria-controls="t other">', "p--")
        self.assertEqual(ids, {"g": "p--g", "t": "p--t"})
        self.assertIn('id="p--g"', out)
        self.assertIn('aria-controls="p--t other"', out)

    def test_pages_without_the_reader_use_outermost_cards(self):
        page = ('<main><section class="card" id="one"><h2>One</h2><section class="card" id="inner"></section></section>'
                '<section class="card" id="two"><div class="slide-face" data-slide-face><div class="slide-canvas">'
                '<p class="slide-eyebrow extra">E</p></div></div><h2>Two</h2></section></main>')
        found = slides.chapters(page)
        self.assertEqual([(c["id"], c["number"]) for c in found], [("one", 1), ("two", 2)])
        self.assertIsNotNone(found[1]["face"])

    def test_selection_parsing(self):
        self.assertEqual(slides.parse_selection(["page", "other#b,a"]), [("page", None), ("other", ["b", "a"])])
        with self.assertRaises(ValueError):
            slides.parse_selection(["../escape"])

    def test_deck_from_built_page(self):
        html_dir = slides.OUTPUT_ROOT / "html"
        page = html_dir / "slide-test-page.html"
        html_dir.mkdir(parents=True, exist_ok=True)
        page.write_text(PAGE)
        try:
            deck, problems = slides.build_deck([("slide-test-page", None)], title="Deck")
            self.assertEqual(problems, [])
            self.assertEqual(deck.count('class="deck-frame"'), 1)
            self.assertIn('<span class="slide-number">02 · </span>Topic', deck)
            self.assertIn('href="../docs/html/assets/page.css"', deck)
            self.assertIn('href="../docs/html/assets/slide-face.css"', deck)
            self.assertIn('class="slide-deck-page scoped"', deck)
            self.assertIn('href="../docs/html/slide-test-page.html#second"', deck)
            _, problems = slides.build_deck([("slide-test-page", ["first", "missing"])], title="Deck")
            self.assertEqual(problems, ["slide-test-page#first: chapter has no slide face",
                                        "slide-test-page#missing: no such chapter"])
            _, problems = slides.build_deck([("absent-page", None)], title="Deck")
            self.assertEqual(len(problems), 1)
        finally:
            page.unlink()

    def test_starter_guide_faces_survive_the_build(self):
        built = (slides.OUTPUT_ROOT / "html" / "guide.html").read_text()
        found = [c for c in slides.chapters(built) if c["face"]]
        self.assertEqual([c["id"] for c in found], ["pipeline", "slides"])
        self.assertRegex(built, r'href="assets/slide-face\.css\?v=[0-9a-f]{10}"')
        self.assertRegex(built, r'src="assets/slide-face\.js\?v=[0-9a-f]{10}"')


if __name__ == "__main__":
    unittest.main()
