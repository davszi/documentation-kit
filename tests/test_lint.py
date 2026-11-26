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

    def run_links(self, site: str, *, untracked: dict | None = None, deleted: tuple | list = ()):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            for path, text in {**self.FILES, "docs/site/site.toml": site}.items():
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_text(text)
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            for path, text in (untracked or {}).items():
                (root / path).write_bytes(text) if isinstance(text, bytes) else (root / path).write_text(text)
            for path in deleted:
                (root / path).unlink()
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

    def test_a_tracked_record_that_is_gone_from_disk_is_not_read(self):
        files, errors, _ = self.run_links('record_roots = ["studies/b"]\n', deleted=["studies/b/plan.md"])
        self.assertEqual(files, ["docs/guide.md", "studies/b/results/deep/run.md"])
        self.assertEqual(errors, ["studies/b/results/deep/run.md: dead link missing.md"])

    def test_a_record_that_is_not_utf8_is_an_error_and_is_left_out(self):
        files, errors, _ = self.run_links('record_roots = ["studies/b"]\nrecord_roots_exclude = ["studies/b/results"]\n',
                                          untracked={"studies/b/plan.md": b"\xff\xfe caf\xe9"})
        self.assertEqual(files, ["docs/guide.md"])
        self.assertEqual(errors, ["studies/b/plan.md: lint cannot read this record under record_roots (UnicodeDecodeError); "
                                  "make it UTF-8 text or name it in record_roots_exclude"])

    def test_overlapping_roots_read_a_file_once(self):
        files, errors, _ = self.run_links('record_roots = ["studies", "studies/b", "studies/b/plan.md", "."]\n'
                                          'record_roots_exclude = ["studies/*/results", "other", "CHANGELOG.md", "docs"]\n')
        self.assertEqual(files, ["docs/guide.md", "studies/a/notes.md", "studies/b/plan.md"])
        self.assertEqual(len(errors), 2)

    def test_wrong_settings_are_errors(self):
        for site, message in (
                ('record_roots = "studies"\n', "site.toml: record_roots must be a list of paths inside the project"),
                ('record_roots = ["../elsewhere"]\n', "site.toml: record_roots entry '../elsewhere' must stay inside the project"),
                ('record_roots = ["/abs"]\n', "site.toml: record_roots entry '/abs' must stay inside the project"),
                ('record_roots = ["nowhere"]\n', "site.toml: record_roots entry 'nowhere' is not a folder or Markdown file of the project"),
                ('record_roots = ["docs/site/site.toml"]\n', "site.toml: record_roots entry 'docs/site/site.toml' is not a folder or Markdown file of the project"),
                ('record_roots = ["studies"]\nrecord_roots_exclude = [3]\n', "site.toml: record_roots_exclude must be a list of paths inside the project"),
                ('record_roots = ["studies"]\nrecord_roots_exclude = ["."]\n', "site.toml: record_roots_exclude entry '.' would leave out every record; name a folder or a file"),
                ('record_roots_exclude = ["studies/*/results"]\n', "site.toml: record_roots_exclude needs record_roots; alone it leaves nothing out")):
            with self.subTest(site=site):
                files, errors, _ = self.run_links(site)
                self.assertEqual(errors, [message])
                self.assertEqual(files, ["docs/guide.md"])


class RepeatedIds(unittest.TestCase):
    """An id carried twice by the elements of a built page is reported; text that only looks like one is not."""

    def test_elements_count_and_scripts_styles_comments_and_text_do_not(self):
        markup = """<h2 id="a">A</h2><p id='a'>again</p><svg><marker id="tip"/></svg><svg><marker id="tip"/></svg>
<section data-id="a" id = "b"></section><div id="c"></div><a title=" id='c' " href="#c">c</a>
<script>const s = '<div id="c"></div><i id="b"></i>';</script><style>/* <p id="c"> */</style>
<!-- <p id="c"></p> --><pre>&lt;p id=&quot;c&quot;&gt;</pre><p>the text id="b" is no element</p>
<template><p id="c"></p></template><textarea><p id="c"></p></textarea><noscript><p id="c"></p></noscript>
<style-box id="box"></style-box><p id="after-the-box"></p><p id="after-the-box"></p>
<p ID=upper></p><p id=upper></p><p id="x&amp;y"></p><p id="x&y"></p><p data-x="a > b" id="late"></p><p id="late"></p>"""
        self.assertEqual(lint.repeated_ids(markup),
                         [("a", 2), ("tip", 2), ("after-the-box", 2), ("upper", 2), ("x&y", 2), ("late", 2)])

    def test_a_heading_that_takes_an_id_of_the_page_shell_is_found(self):
        self.assertEqual(lint.repeated_ids('<nav id="sidebar"></nav><main><h2 id="sidebar">Sidebar</h2></main>'),
                         [("sidebar", 2)])

    def test_a_topic_page_gets_a_warning_and_a_listed_page_a_note(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            built = root / ".build/docs/html"
            built.mkdir(parents=True)
            for name in ("topic.html", "listed.md.html", "clean.html"):
                (built / name).write_text('<p id="one"></p>' + ('<p id="one"></p>' if name != "clean.html" else ""))
            sources = ({"topic.html": "docs/topics/topic/index.md", "listed.md.html": "docs/listed.md"}, set(), {"docs/listed.md"})
            with mock.patch.object(lint, "REPO", root), mock.patch.object(lint, "DOCS", root / "docs"), \
                    mock.patch.object(lint, "built_page_sources", return_value=sources), \
                    mock.patch.object(lint, "warnings", []), mock.patch.object(lint, "notices", []), mock.patch.object(lint, "errors", []):
                lint.check_html()
                message = "{}: 1 id(s) appear more than once, so a link reaches only the first element: one (2x)"
                self.assertEqual(lint.warnings, [message.format(".build/docs/html/topic.html")])
                self.assertEqual(lint.notices, [message.format(".build/docs/html/listed.md.html")])
                self.assertEqual(lint.errors, [])

    def test_the_kit_writes_no_repeated_id_for_repeated_headings(self):
        import build
        import mistune
        rendered = mistune.create_markdown(renderer=build.DocsRenderer(), plugins=["table", "math"])(RepeatedHeadings.TEXT)
        self.assertEqual(lint.repeated_ids(rendered), [])


class ShellIds(unittest.TestCase):
    """A heading never takes an id of the shell around the page, so a link can reach it."""

    HEADINGS = "## Top\n\nText.\n\n## Menu\n\nText.\n\n## Menu\n\nText.\n\n## Sidebar\n\nText.\n\n## TOC\n\nText.\n\n" \
               "## Backdrop\n\nText.\n\n## Repo tree label\n\nText.\n\n## Chapter reader\n\nText.\n"

    def render(self, **taken):
        import build
        import mistune
        import page_source
        renderer = build.DocsRenderer()
        if taken:
            renderer.seen_ids = page_source.taken_ids(**taken)
        mistune.create_markdown(renderer=renderer)(self.HEADINGS)
        return renderer.heading_ids

    def test_the_build_numbers_a_heading_past_the_shell(self):
        self.assertEqual(self.render(), ["top-1", "menu-1", "menu-2", "sidebar-1", "toc-1", "backdrop-1", "repo-tree-label",
                                         "chapter-reader"])
        # An id is taken only where the page holds its element: without a Reference tree or the reader's
        # bar, a heading keeps the id, and a link to it keeps working.
        self.assertEqual(self.render(reader=True, tree=True)[-2:], ["repo-tree-label-1", "chapter-reader-1"])
        import page_source
        self.assertEqual(set(page_source.taken_ids(plot_labels=True)) - set(page_source.taken_ids()), {"plot-toggle-labels"})

    def test_the_record_notes_name_the_chapter_as_the_page_has_it(self):
        import record_changes
        chapters = [value for _, kind, value in record_changes._chapter_index("## Menu\n\n## Chapter reader\n", lint.slugify)
                    if kind == "heading"]
        self.assertEqual(chapters, ["menu-1", "chapter-reader-1"])

    def test_lint_reads_the_file_as_github_shows_it(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.md"
            source.write_text(self.HEADINGS)
            self.assertEqual(lint.md_anchors(source), {"top", "menu", "menu-1", "sidebar", "toc", "backdrop", "repo-tree-label",
                                                       "chapter-reader"})

    def test_the_lists_name_the_ids_the_shell_writes(self):
        import re
        import page_source
        import source_pages
        import source_tree
        components = Path(__file__).resolve().parents[1] / "theme/components"
        written = lambda name: set(re.findall(r'\bid="([^"{]+)"', (components / name).read_text()))
        self.assertEqual(set(page_source.SHELL_IDS), written("shell.html"))
        self.assertEqual(set(page_source.TREE_IDS), {source_tree.TREE_LABEL_ID})
        self.assertEqual(set(page_source.READER_IDS), written("chapter-reader.html"))
        self.assertIn(f'id="{page_source.PLOT_LABEL_IDS[0]}"', (components.parents[1] / "tooling/build.py").read_text())
        self.assertLessEqual(set(page_source.taken_ids(reader=True, tree=True, plot_labels=True)), source_pages.KIT_IDS)

    def test_built_pages_carry_no_id_twice(self):
        import os
        import re
        import subprocess
        import sys
        kit = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="docs-kit-shell-ids-") as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
            subprocess.run([sys.executable, str(kit / "docsite.py"), "init", str(root)], check=True, capture_output=True, env=env)
            for slug, extra in (("shellids", ""), ("plainids", "reader = false\n")):
                page = root / f"docs/topics/{slug}/index.md"
                page.parent.mkdir(parents=True)
                page.write_text(f'+++\ntoc = []\ntitle = "Shell ids"\npage_only = "a fixture"\n{extra}+++\n\n# Shell ids\n\n' + self.HEADINGS)
            (root / "docs/listed.md").write_text("# Listed\n\n" + self.HEADINGS)
            (root / "docs/registered.md").write_text("# Registered\n\n" + self.HEADINGS)
            config = root / "docs/site/site.toml"
            config.write_text(config.read_text()
                              + '\n[[nav]]\nlabel = "Shell ids"\nfile = "shellids.html"\ngroup = "guide"\n'
                              + '\n[[nav]]\nlabel = "Plain ids"\nfile = "plainids.html"\ngroup = "guide"\n'
                              + '\n[[source_pages]]\nsource = "docs/registered.md"\nslug = "registered"\ntitle = "Registered"\n')
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            built = subprocess.run([sys.executable, str(kit / "docsite.py"), "build", "--project", str(root)],
                                   capture_output=True, text=True, env=env)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            for name in ("shellids.html", "plainids.html", "docs.listed.md.html", "registered.html"):
                with self.subTest(page=name):
                    markup = (root / ".build/docs/html" / name).read_text()
                    self.assertEqual(lint.repeated_ids(markup), [])
                    self.assertIn('id="menu-2"', markup)
                    self.assertEqual(len(re.findall(r'\bid="top"', markup)), 1)
            # The reader's bar is part of a reader page only, so only there the heading gives way to it.
            self.assertRegex((root / ".build/docs/html/shellids.html").read_text(), r'<section\b[^>]*\bid="chapter-reader-1"')
            self.assertIn('<h2 id="chapter-reader">', (root / ".build/docs/html/plainids.html").read_text())

    def test_the_readers_id_is_taken_only_where_the_page_places_the_bar(self):
        import build
        bar = "<!-- include: components/chapter-reader.html -->"
        self.assertTrue(build.places_reader_bar("## Chapter reader\n\n" + bar + "\n"))
        self.assertTrue(build.places_reader_bar('<nav id="chapter-reader"></nav>\n'))
        self.assertFalse(build.places_reader_bar("## Chapter reader\n\nA [link](#chapter-reader).\n"))
        self.assertFalse(build.places_reader_bar("<!-- include: fragments/chapter-reader.html -->\n"))

    def test_a_page_that_lists_the_reader_without_its_bar_keeps_the_heading(self):
        import os
        import subprocess
        import sys
        kit = Path(__file__).resolve().parents[1]
        bar = "\n<!-- include: components/chapter-reader.html -->\n"
        text = "## Chapter reader\n\nA [link](#chapter-reader) to the heading.\n"
        with tempfile.TemporaryDirectory(prefix="docs-kit-reader-id-") as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
            subprocess.run([sys.executable, str(kit / "docsite.py"), "init", str(root)], check=True, capture_output=True, env=env)
            config = root / "docs/site/site.toml"
            added = ""
            for slug, body in (("listsreader", text), ("placesbar", text + bar)):
                page = root / f"docs/topics/{slug}/index.md"
                page.parent.mkdir(parents=True)
                page.write_text(f'+++\ntoc = []\ntitle = "Reader id"\npage_only = "a fixture"\nreader = false\n'
                                f'components = ["chapter-reader", "nav"]\n+++\n\n# Reader id\n\n' + body)
                added += f'\n[[nav]]\nlabel = "{slug}"\nfile = "{slug}.html"\ngroup = "guide"\n'
            config.write_text("reference_listing = false\n" + config.read_text() + added)
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            for command in ("build", "lint"):
                done = subprocess.run([sys.executable, str(kit / "docsite.py"), command, "--project", str(root)],
                                      capture_output=True, text=True, env=env)
                self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            # Without the bar the heading keeps the id and the link reaches it, as on 5.5.1.
            listed = (root / ".build/docs/html/listsreader.html").read_text()
            self.assertIn('<h2 id="chapter-reader">', listed)
            self.assertEqual(lint.repeated_ids(listed), [])
            # With the bar the heading gives way to it.
            placed = (root / ".build/docs/html/placesbar.html").read_text()
            self.assertIn('<h2 id="chapter-reader-1">', placed)
            self.assertEqual(lint.repeated_ids(placed), [])

    def test_without_a_reference_tree_a_heading_keeps_the_tree_labels_id(self):
        import os
        import subprocess
        import sys
        kit = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="docs-kit-no-tree-") as folder:
            root = Path(folder).resolve()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
            subprocess.run([sys.executable, str(kit / "docsite.py"), "init", str(root)], check=True, capture_output=True, env=env)
            page = root / "docs/topics/notree/index.md"
            page.parent.mkdir(parents=True)
            page.write_text('+++\ntoc = []\ntitle = "No tree"\npage_only = "a fixture"\nreader = false\n+++\n\n# No tree\n\n'
                            '## Repo tree label\n\nA [link](#repo-tree-label) to the heading.\n\n## Menu\n\nText.\n')
            config = root / "docs/site/site.toml"
            config.write_text("reference_listing = false\n" + config.read_text()
                              + '\n[[nav]]\nlabel = "No tree"\nfile = "notree.html"\ngroup = "guide"\n')
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            built = subprocess.run([sys.executable, str(kit / "docsite.py"), "build", "--project", str(root)],
                                   capture_output=True, text=True, env=env)
            self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
            markup = (root / ".build/docs/html/notree.html").read_text()
            self.assertEqual(markup.count('id="repo-tree-label"'), 1)
            self.assertIn('<h2 id="repo-tree-label">', markup)
            self.assertIn('<h2 id="menu-1">', markup)



class InlinedFigureIds(unittest.TestCase):
    """SVG figures inlined into one page keep their ids apart, with the chapter reader and without it."""

    SVG = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 10 10">'
           '<style>#mark, g #clip rect { stroke: #abc }</style>'
           '<defs><clipPath id="clip"><rect width="10" height="10"/></clipPath><path id="mark" d="M0 0h2"/></defs>'
           '<g id="tg-series--a" clip-path="url(#clip)"><use xlink:href="#mark"/></g><g id="tg-solo"/></svg>\n')
    BODY = ('<img src="../figures/one.svg" alt="one">\n\n<img src="../figures/two.svg" alt="two">\n\n'
            '<img src="../figures/one.svg" alt="one again">\n')

    def built(self):
        import os
        import subprocess
        import sys
        kit = Path(__file__).resolve().parents[1]
        folder = tempfile.TemporaryDirectory(prefix="docs-kit-figure-ids-")
        self.addCleanup(folder.cleanup)
        root = Path(folder.name).resolve()
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
        subprocess.run([sys.executable, str(kit / "docsite.py"), "init", str(root)], check=True, capture_output=True, env=env)
        (root / "docs/figures").mkdir(exist_ok=True)
        for name in ("one.svg", "two.svg"):
            (root / "docs/figures" / name).write_text(self.SVG)
        added = ""
        for slug, extra in (("plainfigures", "reader = false\n"), ("readerfigures", "")):
            page = root / f"docs/topics/{slug}/index.md"
            page.parent.mkdir(parents=True)
            page.write_text(f'+++\ntoc = []\ntitle = "Figures"\npage_only = "a fixture"\n{extra}+++\n\n# Figures\n\n## Three figures\n\n' + self.BODY)
            added += f'\n[[nav]]\nlabel = "{slug}"\nfile = "{slug}.html"\ngroup = "guide"\n'
        config = root / "docs/site/site.toml"
        config.write_text(config.read_text() + added)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        done = subprocess.run([sys.executable, str(kit / "docsite.py"), "build", "--project", str(root)], capture_output=True, text=True, env=env)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        return {slug: (root / f".build/docs/html/{slug}.html").read_text() for slug in ("plainfigures", "readerfigures")}

    def figures(self, markup):
        import re
        return re.findall(r'<svg\b[^>]*class="inline-fig".*?</svg>', markup, flags=re.S)

    def test_a_page_without_the_reader_repeats_no_figure_id(self):
        import re
        markup = self.built()["plainfigures"]
        self.assertEqual(lint.repeated_ids(markup), [])
        figures = self.figures(markup)
        self.assertEqual(len(figures), 3)
        # The first figure keeps its ids, so a link that reached one before still reaches it.
        self.assertEqual(set(re.findall(r'\bid="([^"]+)"', figures[0])), {"clip", "mark", "tg-series--a", "tg-solo"})
        for figure in figures:
            with self.subTest(figure=figures.index(figure)):
                ids = set(re.findall(r'\bid="([^"]+)"', figure))
                # Every reference stays inside its own figure, and the toggle group keeps its "tg-<group>--" start.
                self.assertLessEqual(set(re.findall(r'url\(#([^)]+)\)', figure)) | set(re.findall(r'href="#([^"]+)"', figure)), ids)
                self.assertEqual(len([value for value in ids if value.startswith("tg-series--")]), 1)
                self.assertEqual(len([value for value in ids if value == "tg-solo" or value.startswith("tg-solo--")]), 1)
                # A style rule of the figure still selects the figure's own elements, and its colour is untouched.
                style = re.search(r'<style>(.*?)</style>', figure, flags=re.S).group(1)
                self.assertLessEqual(set(re.findall(r'#([A-Za-z_][\w-]*)(?=[^{};]*\{)', style)), ids)
                self.assertIn("stroke: #abc", style)

    def test_a_reader_page_names_every_figure_id_as_before(self):
        import re
        markup = self.built()["readerfigures"]
        self.assertEqual(lint.repeated_ids(markup), [])
        ids = set(re.findall(r'\bid="([^"]+)"', self.figures(markup)[0]))
        self.assertEqual(ids, {"figure-one-1-clip", "figure-one-1-mark", "tg-series--figure-one-1-a", "figure-one-1-tg-solo"})

if __name__ == "__main__":
    unittest.main()
