"""Public source anchors include authored HTML but exclude code and comments."""
from pathlib import Path
import tempfile
import unittest

import lint


class Anchors(unittest.TestCase):
    def test_source_anchor_kinds_and_quoted_html(self):
        text='''# Intro
## Heading {#named}
### Check `friction_coefficient`
<a id="retained-sliding"></a>
<section class="card" id='near-rest-force-budget'>
```
<a id="example-only"></a>
# Example heading
```
`<a id="inline-example"></a>`
<!-- <a id="comment-only"></a> -->
'''
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/"source.md";source.write_text(text)
            self.assertEqual(lint.md_anchors(source),{"intro","named","check-friction_coefficient","retained-sliding","near-rest-force-budget"})


class RepeatedHeadings(unittest.TestCase):
    """A heading id is unique on its page: a repeated heading is numbered as GitHub numbers it."""

    TEXT = '''# Runs
## Result
Text.
## Result
### Result
## Result 1
## Named {#result}
## !!!
## ???
'''
    IDS = ["runs", "result", "result-1", "result-2", "result-1-1", "result-3", "", ""]

    def test_numbering_follows_document_order(self):
        seen = {}
        self.assertEqual([lint.unique_heading_id(hid, seen) for hid in ["a", "a", "a-1", "a", ""]],
                         ["a", "a-1", "a-1-1", "a-2", ""])

    def test_lint_knows_the_numbered_anchors(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.md"
            source.write_text(self.TEXT)
            self.assertEqual(lint.md_anchors(source), set(self.IDS))

    def test_build_writes_the_same_ids_once_each(self):
        import re
        import build
        import mistune
        rendered = mistune.create_markdown(renderer=build.DocsRenderer(), plugins=["table", "math"])(self.TEXT)
        ids = re.findall(r'<h[1-6] id="([^"]*)"', rendered)
        self.assertEqual(ids, self.IDS)
        named = [hid for hid in ids if hid]
        self.assertEqual(len(named), len(set(named)))

    def test_record_notes_number_the_same_way(self):
        import record_changes
        self.assertEqual([heading.anchor for heading in record_changes.headings(self.TEXT, lint.slugify)], self.IDS)
        chapters = [value for _, kind, value in record_changes._chapter_index(self.TEXT, lint.slugify) if kind == "heading"]
        self.assertEqual(chapters, ["result", "result-1", "result-1-1", "result-3", "", ""])


if __name__=="__main__":
    unittest.main()
