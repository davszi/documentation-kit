import unittest

from source_tree import TreeFile, tree_html


FILES = [TreeFile('docs/releases.md', 'releases.html', 'Release notes', None, False),
         TreeFile('rules/git.md', 'git.html', 'Git', None, False)]


class ListedRecordTest(unittest.TestCase):
    def test_record_listed_in_navigation_keeps_all_files_closed(self):
        listed = tree_html(FILES, 'releases.html', listed=True)
        self.assertIn('<details class="repo-tree-all">', listed)
        self.assertNotIn('aria-current', listed)
        self.assertIn('repo-tree-file current', listed)

    def test_unlisted_record_opens_all_files(self):
        self.assertIn('<details class="repo-tree-all" open>', tree_html(FILES, 'git.html'))


if __name__ == '__main__':
    unittest.main()
