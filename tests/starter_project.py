"""A throwaway project for tests: what `docsite.py init` writes, in a temporary Git repository.

    project = StarterProject(self)                 # removed when the test ends
    project.page("notes", "# Notes\\n\\n## One\\n\\nText.\\n", frontmatter="reader = false\\n")
    project.build()                                # fails the test with the build's output
    markup = project.html("notes")
    done = project.run("lint", "--strict")         # any docsite.py command; the caller reads the result

A page needs a `[[nav]]` entry and the build reads only tracked files; `page`
adds the entry and every command stages the tree first, so a test states only
what it is about. The environment of the test run is passed on without
`DOCSITE_PROJECT_ROOT` and `GITHUB_SHA`, which would point a command at
another project or change the links it writes.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]


class StarterProject:
    def __init__(self, test: unittest.TestCase, *, prefix: str = "docs-kit-test-"):
        folder = tempfile.TemporaryDirectory(prefix=prefix)
        test.addCleanup(folder.cleanup)
        self.test = test
        self.root = Path(folder.name).resolve()
        self.env = {key: value for key, value in os.environ.items() if key not in {"DOCSITE_PROJECT_ROOT", "GITHUB_SHA"}}
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run([sys.executable, str(KIT / "docsite.py"), "init", str(self.root)],
                       check=True, capture_output=True, env=self.env)
        self.config = self.root / "docs/site/site.toml"

    def write(self, relative: str, text: str) -> Path:
        """Write a file of the project, with the folders it needs."""
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def configure(self, *, first: str = "", last: str = "") -> None:
        """Add to `site.toml`: `first` before what is there, for top-level keys, `last` after it, for tables."""
        self.config.write_text(first + self.config.read_text() + last)

    def page(self, slug: str, body: str, *, title: str | None = None, frontmatter: str = "",
             label: str | None = None) -> Path:
        """A topic page at `docs/topics/<slug>/index.md` with its navigation entry; returns its source file."""
        title = title or slug
        self.configure(last=f'\n[[nav]]\nlabel = "{label or title}"\nfile = "{slug}.html"\ngroup = "guide"\n')
        return self.write(f"docs/topics/{slug}/index.md",
                          f'+++\ntoc = []\ntitle = "{title}"\npage_only = "a fixture"\n{frontmatter}+++\n\n' + body)

    def run(self, *command: str) -> subprocess.CompletedProcess:
        """Stage the tree and run one `docsite.py` command on the project."""
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        return subprocess.run([sys.executable, str(KIT / "docsite.py"), *command, "--project", str(self.root)],
                              capture_output=True, text=True, env=self.env)

    def build(self) -> subprocess.CompletedProcess:
        """Build the site; a failing build fails the test and shows what the build said."""
        done = self.run("build")
        self.test.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        return done

    def html(self, name: str) -> str:
        """The built page `name`, with or without `.html`."""
        return (self.root / ".build/docs/html" / (name if name.endswith(".html") else name + ".html")).read_text()
