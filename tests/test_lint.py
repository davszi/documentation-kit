"""Public source anchors include authored HTML but exclude code and comments."""
from pathlib import Path
import tempfile
from types import SimpleNamespace
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
    def test_adapter_origin_and_unregistered_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, origin = root / "snapshot.md", root / "docs/original.md"
            resolver = mock.Mock(return_value=origin)
            with mock.patch.object(lint, "REPO", root), mock.patch.object(
                    lint, "_evidence", SimpleNamespace(document_origin=resolver)):
                self.assertEqual(lint.markdown_origin(source), origin)
                resolver.assert_called_once_with(source, root=root)
                resolver.return_value = None
                with mock.patch.object(lint, "evidence_document_locations", return_value={origin: source}):
                    self.assertEqual(lint.markdown_origin(source), origin)
                with mock.patch.object(lint, "evidence_document_locations", return_value={}):
                    self.assertEqual(lint.markdown_origin(source), source)

    def test_adapter_cannot_return_outside_paths_or_symlink_origins(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "linked").symlink_to(root, target_is_directory=True)
            for value in (root.parent / "outside.md", "../outside.md", root / "linked/source.md", 42):
                with self.subTest(value=value), mock.patch.object(lint, "REPO", root), mock.patch.object(
                        lint, "_evidence", SimpleNamespace(document_origin=lambda path, *, root: value)):
                    with self.assertRaisesRegex(ValueError, "document_origin"):
                        lint.markdown_origin(root / "snapshot.md")


if __name__=="__main__":
    unittest.main()
