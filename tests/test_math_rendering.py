"""Regression checks for Markdown formulas, escaping and math-page opt-in."""
import unittest

import mistune

from build import DocsRenderer, katex_scripts


def render(text, enabled=True):
    return mistune.create_markdown(renderer=DocsRenderer(math_enabled=enabled),
                                  plugins=['math', 'table'])(text)


class MathRendering(unittest.TestCase):
    def test_inline_expression_keeps_tex_intact_and_uses_inline_delimiters(self):
        text = render("Limit $10^{-9}$. Edge $(1-l(s)\\kappa(s))\\mathbf{t}(s)+l'(s)\\mathbf{n}(s)$.")
        self.assertIn('<span class="math-inline">\\(10^{-9}\\)</span>', text)
        self.assertIn("\\mathbf{t}(s)+l&#x27;(s)\\mathbf{n}(s)\\)</span>", text)
        self.assertNotIn('$10^{-9}$', text)

    def test_math_is_not_reparsed_as_markdown_or_html(self):
        text = render(r'$r_c < r_R$ and $x^2+y^2$.')
        self.assertIn(r'\(r_c &lt; r_R\)', text)
        self.assertNotIn('<em>', text)

    def test_display_equations_and_ignored_code_keep_their_existing_form(self):
        text = render('$$\nx^2+y^2\n$$\n\n`$kappa$`\n\n```python\ncost = "$10"\n```')
        self.assertIn('<div class="math">$$x^2+y^2$$</div>', text)
        self.assertIn('<code>$kappa$</code>', text)
        self.assertEqual(text.count('math-inline'), 0)

    def test_literal_dollars_and_non_math_pages_are_preserved(self):
        self.assertNotIn('math-inline', render(r'Costs \$10 and \$20.'))
        self.assertEqual(render('Value $x$ here.', False), '<p>Value $x$ here.</p>\n')

    def test_inline_and_display_delimiters_are_both_registered(self):
        script = katex_scripts()
        self.assertIn('left: "$$", right: "$$", display: true', script)
        self.assertIn('left: "\\\\(", right: "\\\\)", display: false', script)
        self.assertIn('ignoredTags: ["pre", "code", "script", "style"]', script)
        self.assertNotIn('left: "$"', script)


if __name__ == '__main__':
    unittest.main()
