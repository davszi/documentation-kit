"""The snapshot of the owner's global agent instructions: no personal details, and the routes to it hold."""
import re
import unittest
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
SNAPSHOT = KIT / 'examples/global-agent-context.md'
SECTION = "Optional: the owner's global agent instructions"


class Snapshot(unittest.TestCase):
    def test_it_holds_no_address_or_home_path(self):
        text = SNAPSHOT.read_text()
        self.assertIsNone(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text), 'an e-mail address')
        self.assertIsNone(re.search(r'/home/|/Users/|[A-Z]:\\Users', text), 'a home folder path')

    def test_its_first_line_marks_it_and_names_the_readme_section(self):
        text = SNAPSHOT.read_text()
        self.assertTrue(text.startswith("> Snapshot of the kit owner's global agent instructions, taken on "))
        self.assertIn(SECTION.split(': ')[1], ' '.join(text.split('\n\n')[0].replace('> ', '').split()))
        self.assertIn(f'\n## {SECTION}\n', (KIT / 'README.md').read_text())

    def test_the_starter_and_the_readme_name_the_file(self):
        for path in ('examples/starter/AGENTS.md.tmpl', 'README.md', 'docs/topics/releases/migrations/5.10.0.md'):
            self.assertIn('examples/global-agent-context.md', ' '.join((KIT / path).read_text().split()), path)


if __name__ == '__main__':
    unittest.main()
