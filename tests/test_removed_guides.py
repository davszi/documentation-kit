"""A project's link to a migration guide the kit removed is a note, so the project still passes lint."""
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from starter_project import KIT, StarterProject  # noqa: E402


class RemovedGuides(unittest.TestCase):
    def linked(self, name):
        """A starter whose guide record links `name` in the kit's former folder of migration guides."""
        project = StarterProject(self)
        record = project.root / "docs/topics/guide/guide.md"
        target = os.path.relpath(KIT / "docs/topics/releases/migrations" / name, record.parent)
        record.write_text(record.read_text() + f"\nSee the [older guide]({target}).\n")
        project.run("build")   # lint reads the built site; the build's own result is not the subject here
        return project.run("lint", "--strict")

    def test_a_link_to_a_removed_guide_is_a_note_and_lint_passes(self):
        done = self.linked("5.0.0.md")
        said = done.stdout + done.stderr
        self.assertEqual(done.returncode, 0, said)
        self.assertIn("link to a migration guide the kit removed", said)
        self.assertIn("docs/topics/releases/migration.md", said)
        self.assertIn("v5.9.0", said)

    def test_any_other_missing_file_there_is_still_a_dead_link(self):
        done = self.linked("notes.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("dead link", done.stdout + done.stderr)


if __name__ == "__main__":
    unittest.main()
