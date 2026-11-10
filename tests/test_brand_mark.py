import unittest

import build


class BrandMarkTest(unittest.TestCase):
    def setUp(self):
        build._BRAND_MARKS.clear()
        build._errors.clear()

    def test_initials_without_setting(self):
        self.assertIn('>DK</span>', build.brand_mark_html({'title': 'Documentation kit'}))

    def test_short_text_mark(self):
        self.assertIn('>∿</span>', build.brand_mark_html({'title': 'ADP', 'brand_mark': '∿'}))

    def test_svg_mark_with_an_editor_prolog_is_accepted(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory(dir=build.REPO) as folder:
            mark = Path(folder) / 'mark.svg'
            mark.write_text('<?xml version="1.0"?>\n<!-- exported -->\n<svg viewBox="0 0 4 4"><rect/></svg>\n')
            original = build.local_resource
            build.local_resource = lambda path: Path(path)
            try:
                html = build.brand_mark_html({'title': 'X', 'brand_mark': mark.relative_to(build.REPO).as_posix()})
            finally:
                build.local_resource = original
        self.assertIn('brand-mark-svg" aria-hidden="true"><svg viewBox="0 0 4 4">', html)
        self.assertEqual([e for e in build._errors if 'brand_mark' in e], [])

    def test_long_text_is_rejected_once(self):
        site = {'title': 'X', 'brand_mark': 'TOOLONG'}
        build.brand_mark_html(site); build.brand_mark_html(site)
        self.assertEqual(len([e for e in build._errors if 'brand_mark' in e]), 1)


if __name__ == '__main__':
    unittest.main()
