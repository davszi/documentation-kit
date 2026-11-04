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


if __name__=="__main__":
    unittest.main()
