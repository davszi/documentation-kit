"""Page-number notes: numbers on a page that none of its linked records state."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tooling'))
import lint  # noqa: E402
from page_numbers import page_number_notes, shown_numbers, stated_numbers  # noqa: E402

SITE = '''title = "Fixture"
page_number_notes = true

[[source_pages]]
source = "rules/timing.md"
slug = "timing"
'''

RECORD = '''# Timing

## Limits

A run takes 72 seconds on 1,036 cursors. The cap is `4096` rows and 0.5 of the budget.
'''


def page(body):
    return '+++\ntitle = "Page"\ntoc = []\n+++\n\n' + body


class PageNumberNotes(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-numbers-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.write('docs/site/site.toml', SITE)
        self.write('rules/timing.md', RECORD)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def notes(self):
        return page_number_notes(self.root, lint.slugify)

    def test_numbers_stated_in_a_linked_record_give_no_note(self):
        self.write('docs/topics/timing/index.md', page(
            '## Limits\n\nA run takes 72 seconds on 1036 cursors, within 0.5 of the budget and 4096 rows. '
            'See [limits](timing.html#limits).\n'))
        self.assertEqual(self.notes(), [])

    def test_a_number_no_linked_record_states_is_listed_with_its_chapter(self):
        self.write('docs/topics/timing/index.md', page(
            '## Limits\n\nA run takes 72 seconds. See [limits](timing.html#limits).\n\n'
            '## Scale\n\nIt holds for 250 cursors and 99% of runs; again 250.\n'))
        self.assertEqual(self.notes(), [
            'NOTE: docs/topics/timing/index.md shows numbers that none of its linked records state:\n'
            '        250, 99  (chapter: scale)\n'
            '      State each in its record, show it as code if it is a literal value, or take it off the page.'])

    def test_a_record_linked_by_path_below_the_page_end_counts(self):
        self.write('docs/topics/timing/timing.md', '# Timing topic\n\nThe window is 250 cursors.\n')
        self.write('docs/topics/timing/index.md', page(
            '## Scale\n\nIt holds for 250 cursors.\n\n<!-- page-end -->\n\nNotes: [record](timing.md), 777 drafts.\n'))
        self.assertEqual(self.notes(), [])

    def test_notes_are_off_unless_the_site_turns_them_on(self):
        self.write('docs/site/site.toml', SITE.replace('page_number_notes = true\n', ''))
        self.write('docs/topics/timing/index.md', page('## Scale\n\nIt holds for 250 cursors. See [limits](timing.html#limits).\n'))
        self.assertEqual(self.notes(), [])

    def test_a_long_list_is_cut_and_counted(self):
        numbers = ', '.join(str(1000 + n) for n in range(15))
        self.write('docs/topics/timing/index.md', page(f'## Scale\n\nValues {numbers}. See [limits](timing.html#limits).\n'))
        self.assertIn('1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011 and 3 more  (chapter: scale)',
                      self.notes()[0])

    def test_a_page_that_links_no_record_is_skipped(self):
        self.write('docs/topics/home/index.md', page('## Welcome\n\nThere are 31 reasons.\n'))
        self.assertEqual(self.notes(), [])

    def test_only_prose_quantities_are_read(self):
        text = page(
            '## Limits\n\n'
            'Literal `640` and <code>641</code> stay unchecked.\n\n'
            '```text\n642 rows\n```\n\n'
            '<svg viewBox="0 0 643 644"><text>645</text></svg>\n\n'
            '<p class="w-646" data-n="647">Figure 3 and Step 2 are labels; 01 is a label too.</p>\n\n'
            'Version 3.0.0, address 127.0.0.1, date 2026-11-10, ratio 16:9 and [a link](page-648.html) are not quantities.\n\n'
            '<!-- 649 in a comment -->\n\n'
            'Entity &#650; and id fig-651 and the name v652 are not numbers.\n\n'
            'Real quantities: 653 rows, 1,654 cursors, 0.655 share and 66%.\n')
        self.assertEqual([number for _, number in shown_numbers(text)], ['653', '1654', '0.655', '66'])

    def test_record_numbers_are_read_everywhere(self):
        self.assertTrue({'72', '1036', '4096', '0.5'} <= stated_numbers(RECORD))


if __name__ == '__main__':
    unittest.main()
