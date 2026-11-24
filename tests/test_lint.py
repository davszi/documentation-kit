"""Public source anchors include authored HTML but exclude code and comments."""
from pathlib import Path
import subprocess
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

    def test_tabs_of_a_page_share_one_numbering(self):
        import os
        import re
        import subprocess
        import sys
        kit = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="docs-kit-tab-ids-") as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
            subprocess.run([sys.executable, str(kit / "docsite.py"), "init", str(root)], check=True, capture_output=True, env=env)
            page = root / "docs/topics/tabbed/index.md"
            page.parent.mkdir(parents=True)
            page.write_text('+++\ntoc = []\ntitle = "Tabbed"\npage_only = "a fixture"\n+++\n\n# Tabbed\n\n## Result\n\nBefore the tabs.\n\n'
                            '<!-- tab: One -->\n\n## Result\n\nIn one.\n\n<!-- tab: Two -->\n\n## Result\n\nIn two.\n')
            config = root / "docs/site/site.toml"
            config.write_text(config.read_text() + '\n[[nav]]\nlabel = "Tabbed"\nfile = "tabbed.html"\ngroup = "guide"\n')
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            built = subprocess.run([sys.executable, str(kit / "docsite.py"), "build", "--project", str(root)],
                                   capture_output=True, text=True, env=env)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            ids = re.findall(r'id="(result[^"]*)"', (root / ".build/docs/html/tabbed.html").read_text())
            self.assertEqual(sorted(ids), ["result", "result-1", "result-2"])
            self.assertEqual({"result", "result-1", "result-2"} - lint.md_anchors(page), set())

    def test_record_notes_number_the_same_way(self):
        import record_changes
        self.assertEqual([heading.anchor for heading in record_changes.headings(self.TEXT, lint.slugify)], self.IDS)
        chapters = [value for _, kind, value in record_changes._chapter_index(self.TEXT, lint.slugify) if kind == "heading"]
        self.assertEqual(chapters, ["result", "result-1", "result-1-1", "result-3", "", ""])


if __name__=="__main__":
    unittest.main()


class RecordRoots(unittest.TestCase):
    """`record_roots` adds a project's tracked Markdown outside docs/ to the checks that read records."""

    FILES = {
        "docs/guide.md": "# Guide\n",
        "studies/a/notes.md": "# Notes\n[guide](../../docs/guide.md#guide) [gone](missing.md) [bad](../../docs/guide.md#nowhere)\n",
        "studies/a/results/run.md": "[gone](missing.md)\n",
        "studies/b/results/deep/run.md": "[gone](missing.md)\n",
        "studies/b/plan.md": "# Plan\n",
        "CHANGELOG.md": "[gone](missing.md)\n",
        "other/readme.md": "[gone](missing.md)\n",
    }

    def run_links(self, site: str, *, untracked: dict[str, str] | None = None):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            for path, text in {**self.FILES, "docs/site/site.toml": site}.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(text)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            for path, text in (untracked or {}).items():
                (root / path).write_text(text)
            with mock.patch.object(lint, "REPO", root), mock.patch.object(lint, "DOCS", root / "docs"), \
                    mock.patch.object(lint, "errors", []), mock.patch.object(lint, "notices", []), \
                    mock.patch.object(lint, "_record_cache", {}), mock.patch.object(lint, "_entry_cache", {}):
                files = sorted(path.relative_to(root).as_posix() for path in lint.md_files())
                lint.check_md_links()
                lint.check_snippets()
                return files, list(lint.errors), list(lint.notices)

    def test_without_the_setting_only_docs_and_the_root_files_are_read(self):
        files, errors, notices = self.run_links("")
        self.assertEqual(files, ["docs/guide.md"])
        self.assertEqual((errors, notices), ([], []))

    def test_roots_join_the_link_check_and_excluded_folders_stay_out(self):
        files, errors, notices = self.run_links(
            'record_roots = ["studies/", "CHANGELOG.md"]\nrecord_roots_exclude = ["studies/*/results"]\n',
            untracked={"studies/a/draft.md": "[gone](missing.md)\n"})
        self.assertEqual(files, ["CHANGELOG.md", "docs/guide.md", "studies/a/notes.md", "studies/b/plan.md"])
        self.assertEqual(errors, ["CHANGELOG.md: dead link missing.md",
                                  "studies/a/notes.md: dead link missing.md",
                                  "studies/a/notes.md: anchor #nowhere not found in ../../docs/guide.md"])
        self.assertEqual(notices, [])

    def test_a_snippet_in_a_record_root_is_checked(self):
        site = 'record_roots = ["studies/b"]\n'
        with mock.patch.dict(self.FILES, {"studies/b/plan.md": "```python source=docs/guide.md#L1-L1\nnot there\n```\n"}):
            _, errors, _ = self.run_links(site)
        self.assertEqual(errors, ["studies/b/results/deep/run.md: dead link missing.md",
                                  "studies/b/plan.md: snippet body no longer appears in docs/guide.md"])

    def test_an_excluded_file_and_a_star_inside_a_name(self):
        files, _, notices = self.run_links(
            'record_roots = ["studies"]\nrecord_roots_exclude = ["studies/a/notes.md", "studies/*/res*"]\n')
        self.assertEqual(files, ["docs/guide.md", "studies/b/plan.md"])
        self.assertEqual(notices, [])

    def test_an_entry_that_selects_nothing_is_a_note(self):
        _, errors, notices = self.run_links('record_roots = ["docs/site", "studies"]\nrecord_roots_exclude = ["studies/results"]\n')
        self.assertEqual(notices, ["site.toml: record_roots entry 'docs/site' holds no tracked Markdown file",
                                   "site.toml: record_roots_exclude entry 'studies/results' leaves out no file under record_roots"])
        self.assertEqual(len(errors), 4)  # every dead link under studies/: the exclusion matches no folder

    def test_wrong_settings_are_errors(self):
        for site, message in (
                ('record_roots = "studies"\n', "site.toml: record_roots must be a list of paths inside the project"),
                ('record_roots = ["../elsewhere"]\n', "site.toml: record_roots entry '../elsewhere' must stay inside the project"),
                ('record_roots = ["/abs"]\n', "site.toml: record_roots entry '/abs' must stay inside the project"),
                ('record_roots = ["nowhere"]\n', "site.toml: record_roots entry 'nowhere' is not a folder or Markdown file of the project"),
                ('record_roots = ["docs/site/site.toml"]\n', "site.toml: record_roots entry 'docs/site/site.toml' is not a folder or Markdown file of the project"),
                ('record_roots = ["studies"]\nrecord_roots_exclude = [3]\n', "site.toml: record_roots_exclude must be a list of paths inside the project"),
                ('record_roots_exclude = ["studies/*/results"]\n', "site.toml: record_roots_exclude needs record_roots; alone it leaves nothing out")):
            with self.subTest(site=site):
                files, errors, _ = self.run_links(site)
                self.assertEqual(errors, [message])
                self.assertEqual(files, ["docs/guide.md"])


class RepeatedIds(unittest.TestCase):
    """An id carried twice by the elements of a built page is reported; text that only looks like one is not."""

    def test_elements_count_and_scripts_styles_comments_and_text_do_not(self):
        markup = """<h2 id="a">A</h2><p id='a'>again</p><svg><marker id="tip"/></svg><svg><marker id="tip"/></svg>
<section data-id="a" id = "b"></section><div id="c"></div>
<script>const s = '<div id="c"></div><i id="b"></i>';</script><style>/* <p id="c"> */</style>
<!-- <p id="c"></p> --><pre>&lt;p id=&quot;c&quot;&gt;</pre><p>the text id="b" is no element</p>"""
        self.assertEqual(lint.repeated_ids(markup), [("a", 2), ("tip", 2)])

    def test_the_kit_writes_no_repeated_id_for_repeated_headings(self):
        import build
        import mistune
        rendered = mistune.create_markdown(renderer=build.DocsRenderer(), plugins=["table", "math"])(RepeatedHeadings.TEXT)
        self.assertEqual(lint.repeated_ids(rendered), [])
