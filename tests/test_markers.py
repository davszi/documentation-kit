"""Marked statements: cards outside code, text inside code, and what lint lists."""
import html
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]

PAGE = '''+++
title = "Markers"
toc = []
page_only = "marker fixture"
+++

# Markers

**INVARIANT:** a real constraint.

```markdown
**INVARIANT:** shown in a backtick fence
**DON'T-REDO:** also shown
```

~~~~
**DON'T-REDO:** shown in a tilde fence
```
**INVARIANT:** still inside: a shorter fence of the other kind does not close it
~~~~

**DON'T-REDO:** a settled decision that runs straight into a fence
```text
**INVARIANT:** the fence after the card
```

- **INVARIANT:** inside a list item

The rule names `INVARIANT` and `DON'T-REDO` in code spans on a line with **bold** text.

```
**INVARIANT:** in a fence left open to the end
'''


def invoke(*args):
    env = {name: value for name, value in os.environ.items() if name != 'GITHUB_SHA'}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True, env=env)


class MarkersInCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-markers-')
        cls.addClassCleanup(folder.cleanup)
        cls.root = Path(folder.name)
        subprocess.run(['git', 'init', '-q', cls.root], check=True)
        assert invoke('init', cls.root).returncode == 0
        page = cls.root / 'docs/topics/markers/index.md'
        page.parent.mkdir(parents=True)
        page.write_text(PAGE)
        config = cls.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '\n[[nav]]\nlabel = "Markers"\nfile = "markers.html"\n')
        subprocess.run(['git', 'add', '-A'], cwd=cls.root, check=True)
        cls.result = invoke('build', '--project', cls.root)
        built = cls.root / '.build/docs/html/markers.html'
        cls.page = built.read_text() if built.is_file() else ''

    def test_build_passes(self):
        self.assertEqual(self.result.returncode, 0, self.result.stderr)

    def test_only_unindented_paragraphs_outside_code_become_cards(self):
        cards = re.findall(r'<div class="callout (inv|redo)">\s*<p>(.*?)</p>', self.page, re.S)
        self.assertEqual(cards, [('inv', 'a real constraint.'),
                                 ('redo', 'a settled decision that runs straight into a fence')])

    def test_markers_inside_fences_stay_code(self):
        blocks = re.findall(r'<pre><code[^>]*>(.*?)</code></pre>', self.page, re.S)
        text = [html.unescape(re.sub(r'<[^>]+>', '', block)) for block in blocks]
        self.assertEqual(len(text), 4, text)
        self.assertIn("**INVARIANT:** shown in a backtick fence\n**DON'T-REDO:** also shown", text[0])
        self.assertIn('still inside: a shorter fence of the other kind does not close it', text[1])
        self.assertIn('**INVARIANT:** the fence after the card', text[2])
        self.assertIn('**INVARIANT:** in a fence left open to the end', text[3])
        for block in text:
            self.assertNotIn('callout', block)

    def test_indented_marker_keeps_its_label(self):
        # The rule leaves a marker in a list item as text: a card is a block of its own.
        self.assertRegex(self.page, r'<li><strong>INVARIANT:</strong> inside a list item</li>')

    def test_registry_lists_no_marker_in_code(self):
        result = invoke('lint', '--project', self.root, '--registry')
        self.assertEqual(result.returncode, 0, result.stderr)
        listed = [line for line in result.stdout.splitlines() if line.startswith('docs/')]
        self.assertEqual([line.split(': ', 1)[1] for line in listed],
                         ['**INVARIANT:** a real constraint.',
                          "**DON'T-REDO:** a settled decision that runs straight into a fence",
                          '- **INVARIANT:** inside a list item'])

    def test_code_span_mention_is_not_a_malformed_marker(self):
        result = invoke('lint', '--project', self.root)
        self.assertNotIn('marker-ish line', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
