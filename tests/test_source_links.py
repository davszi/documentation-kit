"""Lint checks links to repository files written as HTML, with the build's resolution."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]

PAGE = '''+++
title = "Links"
toc = []
page_only = "link fixture"
+++

# Links

<p>Read <a href="../../notes/record.md#kept">the kept part</a> and
<a href="../../tools/run.py">the script</a>.</p>

<!-- include: fragments/links.html -->
'''

RECORD = '# Record\n\n## Kept\n'


def invoke(*args):
    env = {name: value for name, value in os.environ.items() if name != 'GITHUB_SHA'}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True, env=env)


class HtmlSourceLinks(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-source-links-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        self.assertEqual(invoke('init', self.root).returncode, 0)
        self.config = self.root / 'docs/site/site.toml'
        # notes/ is no page, so its links stay source links; policy/ holds a registered page.
        self.config.write_text(self.config.read_text().replace(
            'reference_exclude = ["CLAUDE.md"]', 'reference_exclude = ["CLAUDE.md", "notes/"]')
            + '\n[[nav]]\nlabel = "Links"\nfile = "links.html"\n'
            + '\n[[source_pages]]\nsource = "policy/rule.md"\nslug = "rule"\n')
        self.write('docs/topics/links/index.md', PAGE)
        self.write('docs/site/fragments/links.html', '<p><a href="../../notes/record.md">The record</a></p>\n')
        self.write('notes/record.md', RECORD)
        self.write('tools/run.py', 'print("run")\n')
        self.write('policy/rule.md', '# Rule\n\n<p><a href="../notes/record.md#kept">Kept</a></p>\n')

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def lint(self):
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        built = invoke('build', '--project', self.root)
        self.assertEqual(built.returncode, 0, built.stderr)
        return invoke('lint', '--project', self.root, '--strict')

    def assertLintFails(self, *messages):
        result = self.lint()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        for message in messages:
            self.assertEqual(result.stderr.count(message), 1, result.stderr)
        return result

    def test_resolving_links_pass(self):
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dead_target_in_a_page_body(self):
        self.write('docs/topics/links/index.md', PAGE.replace('../../tools/run.py', '../../tools/gone.py'))
        self.assertLintFails('docs/topics/links/index.md (links.html): dead link to repository file tools/gone.py')

    def test_missing_anchor_in_a_page_body(self):
        self.write('docs/topics/links/index.md', PAGE.replace('record.md#kept', 'record.md#lost'))
        self.assertLintFails('docs/topics/links/index.md (links.html): anchor #lost not found in notes/record.md')

    def test_dead_target_in_an_included_fragment(self):
        self.write('docs/site/fragments/links.html', '<p><a href="../../notes/old.md">Old</a></p>\n')
        self.assertLintFails('docs/topics/links/index.md (links.html): dead link to repository file notes/old.md')

    def test_missing_anchor_in_a_registered_page(self):
        self.write('policy/rule.md', '# Rule\n\n<p><a href="../notes/record.md#lost">Lost</a></p>\n')
        self.assertLintFails('policy/rule.md (rule.html): anchor #lost not found in notes/record.md')

    def test_without_a_source_remote_each_link_is_reported_once(self):
        self.config.write_text(self.config.read_text().replace(
            'gh_repo = "https://github.com/example/project"', 'gh_repo = ""'))
        self.write('docs/topics/links/index.md', PAGE.replace('../../tools/run.py', '../../tools/gone.py')
                   + '\nAnd [as Markdown](../../tools/also-gone.py).\n')
        result = self.assertLintFails('dead link to repository file tools/gone.py',
                                      'docs/topics/links/index.md: dead link ../../tools/also-gone.py')
        self.assertNotIn('dead relative href', result.stderr)
        self.assertNotIn('repository file tools/also-gone.py', result.stderr)

    def test_automatically_listed_page_gets_a_note(self):
        self.write('drafts/draft.md', '# Draft\n\n<p><a href="../notes/record.md#lost">Lost</a></p>\n')
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('NOTE: drafts/draft.md (drafts.draft.md.html): anchor #lost not found in notes/record.md',
                      result.stdout)

    def test_old_worklog_entries_are_not_checked(self):
        # Top-level settings go above the first [[nav]]; the guide page quotes the first lines.
        self.config.write_text(self.config.read_text().replace(
            '\n[[nav]]', '\nworklog_links_checked_from = "2026-01-02"\n\n[[nav]]', 1)
            + '\n[[source_pages]]\nsource = "docs/worklog.md"\nslug = "worklog"\n')
        worklog = self.root / 'docs/worklog.md'
        entry = '\n## {date} — Entry\n\n<p><a href="../notes/record.md#{anchor}">Record</a></p>\n'
        head, _, rest = worklog.read_text().partition('\n## ')
        worklog.write_text(head + entry.format(date='2026-01-03', anchor='kept')
                           + entry.format(date='2026-01-01', anchor='lost') + ('\n## ' + rest if rest else ''))
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        worklog.write_text(worklog.read_text().replace('2026-01-01 — Entry', '2026-01-02 — Entry'))
        self.assertLintFails('docs/worklog.md (worklog.html): anchor #lost not found in notes/record.md')


if __name__ == '__main__':
    unittest.main()
