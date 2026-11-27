"""The sidebar's last line: the kit link with its version, and the build time kept in a file of its own."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from starter_project import KIT, StarterProject  # noqa: E402

VERSION = (KIT / "VERSION").read_text().strip()
LINK = f'<a href="https://davszi.github.io/documentation-kit/">Built with the documentation kit {VERSION}<span aria-hidden="true"> ↗</span></a>'


class KitLine(unittest.TestCase):
    def test_every_page_links_the_kit_with_its_version(self):
        project = StarterProject(self)
        project.build()
        for name in ("index", "guide"):
            self.assertIn(LINK, project.html(name), name)

    def test_a_project_can_leave_the_line_out(self):
        project = StarterProject(self)
        project.configure(first="kit_link = false\n")
        project.build()
        self.assertNotIn("kit-line", project.html("index"))
        self.assertNotIn("data-kit-built", project.html("guide"))
        # Without the line the site publishes no build time: the file is not written and not listed.
        self.assertFalse((project.root / ".build/docs/html/build-info.js").exists())
        self.assertNotIn("build-info.js", (project.root / ".build/docs/site-build.json").read_text())

    def test_turning_the_line_off_removes_an_earlier_build_time_file(self):
        project = StarterProject(self)
        project.build()
        info = project.root / ".build/docs/html/build-info.js"
        self.assertTrue(info.is_file())
        project.configure(first="kit_link = false\n")
        project.build()
        self.assertFalse(info.exists())

    def test_the_setting_takes_only_true_or_false(self):
        project = StarterProject(self)
        project.configure(first='kit_link = "no"\n')
        done = project.run("build")
        self.assertNotEqual(done.returncode, 0)
        self.assertEqual((done.stdout + done.stderr).count("kit_link must be true or false"), 1, "reported once, not per page")

    def test_the_build_time_does_not_make_a_fresh_site_stale(self):
        project = StarterProject(self)
        project.build()
        info = project.root / ".build/docs/html/build-info.js"
        self.assertRegex(info.read_text(), r'^window\.docsSiteBuilt = "\d{4}-\d\d-\d\dT\d\d:\d\dZ";\n$')
        # Another time in the file: the site is still fresh, and no page carries the time.
        info.write_text('window.docsSiteBuilt = "2001-01-01T00:00Z";\n')
        done = project.run("build", "--check")
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertNotIn("2001-01-01", project.html("index"))
        # A build that changes nothing keeps the time; one that changes a page moves it.
        project.build()
        self.assertIn("2001-01-01T00:00Z", info.read_text())
        project.page("notes", "# Notes\n\n## One\n\nText.\n", frontmatter="reader = false\n")
        project.build()
        self.assertNotIn("2001-01-01", info.read_text())

    def test_a_missing_build_time_file_is_written_again_and_is_no_stray_file(self):
        project = StarterProject(self)
        project.build()
        info = project.root / ".build/docs/html/build-info.js"
        info.unlink()
        self.assertEqual(project.run("build", "--check").returncode, 0)
        project.build()
        self.assertTrue(info.is_file())


if __name__ == "__main__":
    unittest.main()
