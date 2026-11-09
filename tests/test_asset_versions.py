import hashlib
import unittest

import build


class AssetVersionTest(unittest.TestCase):
    def test_shared_asset_links_carry_a_content_hash(self):
        css = b'body{color:red}'
        outputs = {
            'html/assets/base.css': css,
            'html/page.html': b'<link rel="stylesheet" href="assets/base.css">'
                              b'<script src="assets/missing.js"></script>'
                              b'<a href="other.html">x</a>',
        }
        build.version_asset_links(outputs)
        page = outputs['html/page.html'].decode()
        self.assertIn('href="assets/base.css?v=' + hashlib.sha256(css).hexdigest()[:10] + '"', page)
        self.assertIn('src="assets/missing.js"', page)
        self.assertIn('href="other.html"', page)

    def test_hash_changes_only_with_the_asset(self):
        page = b'<link rel="stylesheet" href="assets/base.css">'
        first = {'html/assets/base.css': b'a', 'html/p.html': page}
        same = {'html/assets/base.css': b'a', 'html/p.html': page}
        changed = {'html/assets/base.css': b'b', 'html/p.html': page}
        for outputs in (first, same, changed):
            build.version_asset_links(outputs)
        self.assertEqual(first['html/p.html'], same['html/p.html'])
        self.assertNotEqual(first['html/p.html'], changed['html/p.html'])


if __name__ == '__main__':
    unittest.main()
