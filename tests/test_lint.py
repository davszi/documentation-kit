"""Public source anchors include authored HTML but exclude code and comments."""
from pathlib import Path
import tempfile
import unittest
from unittest import mock

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


class DocumentOrigins(unittest.TestCase):
    def test_relocated_document_resolves_from_its_original_path(self):
        # A declared evidence collection still relocates documents; no project
        # adapter takes part since 5.0.0.
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, origin = root / "snapshot.md", root / "docs/original.md"
            with mock.patch.object(lint, "REPO", root):
                with mock.patch.object(lint, "evidence_document_locations", return_value={origin: source}):
                    self.assertEqual(lint.markdown_origin(source), origin)
                with mock.patch.object(lint, "evidence_document_locations", return_value={}):
                    self.assertEqual(lint.markdown_origin(source), source)


if __name__=="__main__":
    unittest.main()
