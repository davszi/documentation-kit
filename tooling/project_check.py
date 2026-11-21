"""Run a project's documentation checks in order and stop at the first failure.

`docsite.py check --project .` is what the kit's pre-push hook calls, so that a
push is stopped by the same checks that would fail in the project's workflow:

1. `build`, because lint compares the built site with its sources;
2. `lint --strict`;
3. a trial `publish` into a temporary folder, when `docs/site/site.toml` has a
   `[publication]` table; skipped with a note when the page lock is on and its
   passwords are not in the environment;
4. each command the project declares, in the order written:

       [[checks]]
       name = "public paths"
       command = ["{python}", "-m", "unittest", "docs/site/checks/test_public_paths.py"]

`command` is an argument list, run from the project root without a shell; an
element that is exactly `{python}` becomes the interpreter that runs the check.
The checks read the working tree, not a commit.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

CHECK_KEYS = {"name", "command"}
PLACEHOLDER = "{python}"
EXAMPLE = '[[checks]] with name = "tests" and command = ["{python}", "-m", "unittest"]'


def declared(site: dict) -> list[tuple[str, list[str]]]:
    """The project's own checks from `[[checks]]`, validated; ValueError says what is wrong."""
    tables = site.get("checks", [])
    if not isinstance(tables, list) or any(not isinstance(table, dict) for table in tables):
        raise ValueError(f"site.toml: checks must be a list of tables, such as {EXAMPLE}")
    found = []
    for number, table in enumerate(tables, 1):
        unknown = sorted(set(table) - CHECK_KEYS)
        if unknown:
            raise ValueError(f"site.toml: [[checks]] entry {number} has the unknown key {unknown[0]!r}; "
                             "it takes name and command")
        command = table.get("command")
        if (not isinstance(command, list) or not command
                or any(not isinstance(part, str) or not part for part in command)):
            raise ValueError(f"site.toml: [[checks]] entry {number} needs command as a list of non-empty strings, "
                             f"such as {EXAMPLE}")
        name = table.get("name", " ".join(command))
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"site.toml: [[checks]] entry {number} has a name that is not text")
        found.append((name.strip(), command))
    return found


def _publish_note(site: dict, environ) -> str | None:
    """Why the trial publish cannot run, or None when it can."""
    from page_lock import PASSWORD_VARIABLES
    options = site.get("publication")
    if not isinstance(options, dict) or options.get("lock") is not True:
        return None
    missing = [name for name in PASSWORD_VARIABLES.values() if not environ.get(name)]
    if missing:
        return f"the page lock is on and {' and '.join(missing)} {'is' if len(missing) == 1 else 'are'} not set"
    return None


def run(project: Path, kit: Path, environ=None) -> int:
    """Run every step for `project`; return 0, or the exit status of the step that failed."""
    environ = os.environ if environ is None else environ
    python = sys.executable
    docsite = [python, str(kit / "docsite.py")]
    try:
        site = tomllib.loads((project / "docs/site/site.toml").read_text())
        own = declared(site)
    except (ValueError, tomllib.TOMLDecodeError) as problem:
        print(f"check: {problem}", file=sys.stderr)
        return 2
    steps: list[tuple[str, list[str] | None]] = [
        ("build", [*docsite, "build", "--project", str(project)]),
        ("lint --strict", [*docsite, "lint", "--project", str(project), "--strict"]),
    ]
    skipped = None
    if "publication" in site:
        skipped = _publish_note(site, environ)
        steps.append(("publish, into a temporary folder", None))
    steps += [(name, [python if part == PLACEHOLDER else part for part in command]) for name, command in own]
    for number, (name, command) in enumerate(steps, 1):
        print(f"check {number}/{len(steps)}: {name}", flush=True)
        if command is None and skipped:
            print(f"  skipped: {skipped}", flush=True)
            continue
        try:
            if command is None:
                with tempfile.TemporaryDirectory(prefix="docsite-check-") as folder:
                    status = subprocess.run([*docsite, "publish", "--project", str(project),
                                             "--out", str(Path(folder) / "site")],
                                            cwd=project, stdout=subprocess.DEVNULL).returncode
            else:
                status = subprocess.run(command, cwd=project).returncode
        except OSError as problem:
            print(f"check failed at step {number}, {name}: cannot run {command[0]}: {problem.strerror}", file=sys.stderr)
            return 127
        if status:
            print(f"check failed at step {number}: {name}", file=sys.stderr)
            return status
    print(f"check passed: {len(steps)} step(s)" + (", the trial publish skipped" if skipped else ""))
    return 0
