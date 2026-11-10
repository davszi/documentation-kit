"""Record-change reminders and the topic structure check, on temporary projects."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import lint
from record_changes import changed_lines, record_change_notes
from topic_structure import topic_structure_problems

KIT = Path(__file__).resolve().parents[1]

RECORD = """Intro above the first heading.

# Code practices

## Refactoring over compatibility

Remove the old form once the owner decides.

### Nested detail

Detail text.

## Logging

Log text.

```text
## Not a heading
```

Tail of the logging section.
"""

PRACTICE_PAGE = """+++
title = "Practice"
toc = []
+++

<section class="card" id="compatibility">

## Refactor fully

See [the rule](../../rules/code.md#refactoring-over-compatibility).

</section>

## Logging and output

Read <a href="code-practices.html#logging">the logging rule</a>.
"""

OVERVIEW_PAGE = """+++
title = "Overview"
toc = []
+++

## Overview

All of [the code guide](code-practices.html).
"""

FENCED_PAGE = """+++
title = "Fenced"
toc = []
+++

## Example

```markdown
[only an example](../../rules/code.md#logging)
```

`[inline example](../../rules/code.md#logging)`
"""

SITE = """title = "Fixture"

[[source_pages]]
source = "rules/code.md"
slug = "code-practices"
"""


def git(cwd, *args):
    return subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                           *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def note(title, *readers):
    lines = [f'NOTE: {title} changed.', '      Pages that explain it — reread them:']
    lines += [f'        {reader}' for reader in readers]
    return '\n'.join(lines)


PRACTICE = 'docs/topics/practice/index.md  (chapter: compatibility)'
PRACTICE_LOGGING = 'docs/topics/practice/index.md  (chapter: logging-and-output)'
OVERVIEW = 'docs/topics/overview/index.md  (chapter: overview)'


class RecordChangeNotes(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-notes-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        git(self.root, 'init', '-q')
        self.write('docs/site/site.toml', SITE)
        self.write('rules/code.md', RECORD)
        self.write('docs/topics/practice/index.md', PRACTICE_PAGE)
        self.write('docs/topics/overview/index.md', OVERVIEW_PAGE)
        self.write('docs/topics/fenced/index.md', FENCED_PAGE)
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'Fixture')

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def edit(self, old, new, relative='rules/code.md'):
        path = self.root / relative
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def test_a_record_whose_name_contains_a_space_is_found(self):
        self.write('rules/my rule.md', '# My rule\n\n## Limits\n\nOld.\n')
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'Add a rule with a space')
        self.write('rules/my rule.md', '# My rule\n\n## Limits\n\nNew.\n')
        self.assertEqual(set(changed_lines(self.root)), {'rules/my rule.md'})

    def test_a_content_line_that_looks_like_a_diff_header_is_content(self):
        self.write('rules/code.md', RECORD.replace('Remove the old form once the owner decides.',
                                                   '++ a line that starts like a header').replace('Log text.', 'Log text, changed.'))
        changes = changed_lines(self.root)
        self.assertEqual(set(changes), {'rules/code.md'})
        self.assertEqual(len(changes['rules/code.md']), 2)

    def notes(self, since=None):
        return record_change_notes(self.root, lint.slugify, since)

    def test_changed_section_names_linking_pages_and_chapters(self):
        self.edit('Remove the old form', 'Remove every old form')
        self.assertEqual(self.notes(), [note('rules/code.md › Refactoring over compatibility',
                                             PRACTICE)])

    def test_subsection_change_reaches_links_to_its_enclosing_section(self):
        self.edit('Detail text.', 'Changed detail.')
        self.assertEqual(self.notes(), [note('rules/code.md › Nested detail', PRACTICE)])

    def test_link_through_built_route(self):
        self.edit('Log text.', 'Log to stderr.')
        self.assertEqual(self.notes(), [note('rules/code.md › Logging', PRACTICE_LOGGING)])

    def test_change_above_first_heading_reaches_only_links_without_fragment(self):
        self.edit('Intro above', 'Opening above')
        self.assertEqual(self.notes(), [note('rules/code.md', OVERVIEW)])

    def test_deleted_line_maps_to_heading_at_its_new_position(self):
        self.edit('Log text.\n', '')
        self.assertEqual(self.notes(), [note('rules/code.md › Logging', PRACTICE_LOGGING)])

    def test_headings_and_links_in_fenced_code_are_ignored(self):
        self.edit('Tail of the logging section.', 'Changed tail.')
        notes = self.notes()
        self.assertEqual(notes, [note('rules/code.md › Logging', PRACTICE_LOGGING)])
        self.assertNotIn('fenced', notes[0])

    def test_staged_changes_and_several_sections_are_grouped_in_order(self):
        self.edit('Log text.', 'Log to stderr.')
        self.edit('Intro above', 'Opening above')
        self.edit('Remove the old form', 'Remove every old form')
        git(self.root, 'add', 'rules/code.md')
        self.assertEqual(self.notes(), [
            note('rules/code.md', OVERVIEW),
            note('rules/code.md › Refactoring over compatibility', PRACTICE),
            note('rules/code.md › Logging', PRACTICE_LOGGING),
        ])

    def test_page_changes_and_unlinked_records_give_no_notes(self):
        self.edit('## Overview', '## Overview of practice', 'docs/topics/overview/index.md')
        self.write('rules/other.md', '# Other\n\nText.\n')
        git(self.root, 'add', 'rules/other.md')
        self.assertEqual(self.notes(), [])

    def test_clean_tree_and_projects_without_history_give_nothing(self):
        self.assertEqual(self.notes(), [])
        with tempfile.TemporaryDirectory() as folder:
            bare = Path(folder)
            (bare / 'rules').mkdir()
            (bare / 'rules/code.md').write_text(RECORD)
            self.assertEqual(record_change_notes(bare, lint.slugify), [])  # not a repository
            git(bare, 'init', '-q')
            git(bare, 'add', '-A')
            self.assertEqual(record_change_notes(bare, lint.slugify), [])  # no HEAD yet

    def test_since_compares_with_another_revision(self):
        self.edit('Log text.', 'Log to stderr.')
        git(self.root, 'commit', '-q', '-am', 'Change logging')
        self.assertEqual(self.notes(), [])
        self.assertEqual(self.notes('HEAD~1'),
                         [note('rules/code.md › Logging', PRACTICE_LOGGING)])
        with self.assertRaisesRegex(ValueError, '--since no-such-rev: not a commit'):
            self.notes('no-such-rev')


def invoke(*args):
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True)


class LintCommand(unittest.TestCase):
    """End to end on the starter: notes never fail --strict; page warnings do."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-lint-notes-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        git(self.root, 'init', '-q')
        self.assertEqual(invoke('init', self.root).returncode, 0)
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'Starter')

    def build(self):
        git(self.root, 'add', '-A')
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_notes_print_without_failing_strict(self):
        record = self.root / 'docs/topics/guide/guide.md'
        text = record.read_text()
        head, marker, rest = text.partition('## Acceptance checklist\n')
        self.assertTrue(marker)
        record.write_text(head + marker + '\nOne more acceptance condition.\n' + rest)
        self.build()
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('NOTE: docs/topics/guide/guide.md › Acceptance checklist changed.\n'
                      '      Pages that explain it — reread them:\n'
                      '        docs/topics/guide/index.md', result.stdout)
        self.assertIn('lint clean (0 warning(s))', result.stdout)
        git(self.root, 'commit', '-q', '-am', 'Extend the checklist')
        quiet = invoke('lint', '--project', self.root, '--strict')
        self.assertNotIn('NOTE:', quiet.stdout)
        since = invoke('lint', '--project', self.root, '--strict', '--since', 'HEAD~1')
        self.assertEqual(since.returncode, 0, since.stdout + since.stderr)
        self.assertIn('› Acceptance checklist changed.', since.stdout)
        unknown = invoke('lint', '--project', self.root, '--since', 'no-such-rev')
        self.assertEqual(unknown.returncode, 1)
        self.assertIn('--since no-such-rev: not a commit', unknown.stderr)

    def test_page_without_record_fails_strict_and_page_only_is_accepted(self):
        page = self.root / 'docs/topics/lonely/index.md'
        page.parent.mkdir(parents=True)
        page.write_text('+++\ntitle = "Lonely"\ntoc = []\n+++\n\n# Lonely\n\nA page.\n')
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '\n[[nav]]\nlabel = "Lonely"\nfile = "lonely.html"\n')
        self.build()
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 1)
        self.assertIn('WARN: docs/topics/lonely: page without a record; add '
                      'docs/topics/lonely/lonely.md or declare page_only = "<reason>" '
                      'in its frontmatter', result.stdout)
        self.assertNotIn('ERROR', result.stderr)
        page.write_text(page.read_text().replace('toc = []', 'toc = []\npage_only = "Explains the guide."'))
        self.build()
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TopicStructure(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-topics-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)

    def page(self, topic, *extra):
        path = self.root / 'docs/topics' / topic / 'index.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('+++\n' + '\n'.join(('title = "T"', 'toc = []', *extra)) + '\n+++\n\n# T\n')

    def record(self, relative):
        path = self.root / 'docs/topics' / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# Record\n')

    def test_page_without_record_warns(self):
        self.page('alone')
        self.assertEqual(topic_structure_problems(self.root), ([], [
            'docs/topics/alone: page without a record; add docs/topics/alone/alone.md '
            'or declare page_only = "<reason>" in its frontmatter']))

    def test_records_anywhere_in_the_folder_except_evidence_count(self):
        self.page('paired')
        self.record('paired/paired.md')
        self.page('nested')
        self.record('nested/notes/design.md')
        self.page('evidence-only')
        self.record('evidence-only/evidence/run.md')
        errors, warnings = topic_structure_problems(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, ['docs/topics/evidence-only: page without a record; add '
                                    'docs/topics/evidence-only/evidence-only.md or declare '
                                    'page_only = "<reason>" in its frontmatter'])

    def test_page_only_reason_is_accepted(self):
        self.page('overview', 'page_only = "Explains the shared rules, which are the records."')
        self.assertEqual(topic_structure_problems(self.root), ([], []))

    def test_empty_or_non_string_page_only_is_an_error(self):
        self.page('empty', 'page_only = "  "')
        self.page('flag', 'page_only = true')
        errors, warnings = topic_structure_problems(self.root)
        self.assertEqual(errors, [
            'docs/topics/empty/index.md: page_only must be a non-empty reason string',
            'docs/topics/flag/index.md: page_only must be a non-empty reason string'])
        self.assertEqual(warnings, [])

    def test_redundant_page_only_warns(self):
        self.page('paired', 'page_only = "Not needed."')
        self.record('paired/paired.md')
        self.assertEqual(topic_structure_problems(self.root), ([], [
            'docs/topics/paired: page_only is unnecessary; the folder holds the record '
            'docs/topics/paired/paired.md']))

    def test_home_page_is_exempt(self):
        self.page('home', 'slug = "index"')
        self.assertEqual(topic_structure_problems(self.root), ([], []))


if __name__ == '__main__':
    unittest.main()
