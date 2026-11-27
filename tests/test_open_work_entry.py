"""The menu's first line: the project's open work as a page, with the number of open lines."""
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from starter_project import StarterProject  # noqa: E402

ENTRY = re.compile(r'<a class="open-work( current)?" href="([^"]+)"( aria-current="page")?>'
                   r'<span class="open-work-label">Open work</span>(?:<span class="open-work-count"[^>]*>(\d+)</span>)?</a>')


class OpenWorkEntry(unittest.TestCase):
    def entry(self, project, page):
        found = ENTRY.search(project.html(page))
        self.assertIsNotNone(found, f"{page} has no Open work entry")
        return found

    def test_every_page_starts_its_menu_with_the_open_work_and_its_count(self):
        project = StarterProject(self)
        lines = sum(1 for line in (project.root / "docs/open/OPEN.md").read_text().splitlines() if line.startswith("- "))
        self.assertGreater(lines, 0)
        project.build()
        for name in ("index", "guide"):
            found = self.entry(project, name)
            self.assertEqual(found.group(4), str(lines), name)
            self.assertIsNone(found.group(1), "not current on another page")
            markup = project.html(name)
            self.assertLess(markup.index('class="open-work'), markup.index('class="nav-section'), "it is the menu's first line")
        route = self.entry(project, "index").group(2)
        self.assertTrue((project.root / ".build/docs/html" / route).is_file(), "the entry's page is built")
        opened = self.entry(project, route)
        self.assertEqual((opened.group(1), opened.group(3)), (" current", ' aria-current="page"'))

    def test_the_count_follows_the_list_and_an_empty_list_shows_none(self):
        project = StarterProject(self)
        project.write("docs/open/OPEN.md", "# Open work\n\nRoutes only.\n")
        project.build()
        self.assertIsNone(self.entry(project, "index").group(4))

    def test_a_list_the_site_does_not_show_gets_no_entry_and_no_page(self):
        # The entry never publishes a file by itself: with the Reference listing off and the list
        # not registered, the site has no page for it, so the menu has no entry.
        project = StarterProject(self)
        project.configure(first="reference_listing = false\n")
        project.build()
        self.assertNotIn('class="open-work', project.html("index"))
        self.assertEqual([path.name for path in (project.root / ".build/docs/html").glob("*open*")], [])

    def test_a_registered_list_is_linked_at_its_own_address(self):
        project = StarterProject(self)
        project.configure(first="reference_listing = false\n",
                          last='\n[[source_pages]]\nsource = "docs/open/OPEN.md"\nslug = "owed"\n')
        project.build()
        self.assertEqual(self.entry(project, "index").group(2), "owed.html")

    def test_a_project_can_leave_the_entry_out(self):
        project = StarterProject(self)
        project.configure(first="open_work_entry = false\n")
        project.build()
        self.assertNotIn('class="open-work', project.html("index"))

    def test_a_locked_site_shows_the_entry_only_when_the_project_asks(self):
        # Pages a general password opens would show that the list exists and how long it is.
        lock = '\n[publication]\npages = ["guide.html"]\nlock = true\n'
        project = StarterProject(self)
        project.configure(last=lock)
        project.build()
        self.assertNotIn('class="open-work', project.html("guide"))
        asked = StarterProject(self)
        asked.configure(first="open_work_entry = true\n", last=lock)
        asked.build()
        self.assertIsNotNone(ENTRY.search(asked.html("guide")))

    def test_the_list_is_found_however_its_path_is_written(self):
        project = StarterProject(self)
        project.configure(first='open_work = "./docs/open/OPEN.md"\n')
        project.build()
        self.assertIsNotNone(ENTRY.search(project.html("index")))

    def test_the_setting_takes_only_true_or_false(self):
        project = StarterProject(self)
        project.configure(first='open_work_entry = "no"\n')
        done = project.run("build")
        self.assertNotEqual(done.returncode, 0)
        self.assertEqual((done.stdout + done.stderr).count("open_work_entry must be true or false"), 1)


if __name__ == "__main__":
    unittest.main()
