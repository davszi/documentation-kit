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

    def test_long_text_is_rejected_once(self):
        site = {'title': 'X', 'brand_mark': 'TOOLONG'}
        build.brand_mark_html(site); build.brand_mark_html(site)
        self.assertEqual(len([e for e in build._errors if 'brand_mark' in e]), 1)


if __name__ == '__main__':
    unittest.main()
