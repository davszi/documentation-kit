"""The capability map check, on temporary Git projects and on the kit itself."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / "tooling"))

import capability_map  # noqa: E402
import lint  # noqa: E402

SITE = {"tooling_roots": ["tools/"], "experiment_roots": ["experiments/"]}

MAP = """# Capability map

| Need | Code | State | Imported by |
|---|---|---|---|
| Record what a native run did | [run_record/](../tools/run_record/) | exists | {record} |
| Judge a finished run against its criteria | [judge.py](../tools/judge.py) | partly | {judge} |
| Replay a recorded run | — | missing | — |

## Seen but not built

- Compare two recorded runs. Decision (owner, 2026-11-15): do not build.
"""


def project(files: dict[str, str], *, track: bool = True) -> tempfile.TemporaryDirectory:
    folder = tempfile.TemporaryDirectory()
    root = Path(folder.name)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text)
    if track:
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    return folder


def base_files(record="`experiments/attended/`, `tools/judge.py`", judge="no Python imports") -> dict[str, str]:
    return {
        "tools/run_record/__init__.py": "",
        "tools/run_record/writer.py": "def write(): pass\n",
        "tools/judge.py": "from run_record.writer import write\n",
        "experiments/attended/run.py": "import tools.run_record.writer\n",
        "docs/CAPABILITY_MAP.md": MAP.format(record=record, judge=judge),
    }


class Settings(unittest.TestCase):
    def test_missing_setting_fails(self):
        # The map is required: a project that does not set tooling_roots fails lint.
        with project({"tools/harness.py": ""}) as folder:
            errors, _ = capability_map.check(Path(folder), {})
            self.assertEqual(len(errors), 1)
            self.assertIn("tooling_roots is missing; every project sets it", errors[0])

    def test_empty_list_states_no_tooling(self):
        # No map and an experiment import: with no tooling folder nothing else is checked.
        files = {"tools/harness.py": "import experiments.a.run\n", "experiments/a/run.py": ""}
        with project(files) as folder:
            self.assertEqual(capability_map.check(Path(folder), {"tooling_roots": []}), ([], []))
            self.assertIsNone(capability_map.settings({"tooling_roots": []}))

    def test_wrong_settings_are_refused(self):
        for site in ({"capability_map": "docs/MAP.md"}, {"experiment_roots": ["experiments/"]},
                     {"tooling_roots": [], "capability_map": "docs/MAP.md"}, {"tooling_roots": "tools/"}, {"tooling_roots": ["../tools"]},
                     {"tooling_roots": ["/abs"]}, {"tooling_roots": ["tools", "tools/"]},
                     {"tooling_roots": ["tools/"], "experiment_roots": ["tools/exp/"]},
                     {"tooling_roots": ["tools/"], "capability_map": "docs/map.txt"}):
            with self.subTest(site=site), self.assertRaises(ValueError):
                capability_map.settings(site)

    def test_default_and_named_map_path(self):
        self.assertEqual(capability_map.settings({"tooling_roots": ["tools/"]})["map"], "docs/CAPABILITY_MAP.md")
        self.assertEqual(capability_map.settings({"tooling_roots": ["tools"], "capability_map": "tools/MAP.md"})["map"],
                         "tools/MAP.md")


class Check(unittest.TestCase):
    def test_listed_tooling_and_fresh_column_pass(self):
        with project(base_files()) as folder:
            errors, warnings = capability_map.check(Path(folder), SITE)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_missing_map_fails(self):
        files = base_files()
        del files["docs/CAPABILITY_MAP.md"]
        with project(files) as folder:
            errors, _ = capability_map.check(Path(folder), SITE)
            self.assertEqual(len(errors), 1)
            self.assertIn("docs/CAPABILITY_MAP.md is missing", errors[0])

    def test_untracked_map_fails(self):
        with project(base_files()) as folder:
            subprocess.run(["git", "rm", "-q", "--cached", "docs/CAPABILITY_MAP.md"], cwd=folder, check=True)
            errors, _ = capability_map.check(Path(folder), SITE)
            self.assertIn("capability map docs/CAPABILITY_MAP.md is not tracked by Git", errors)

    def test_unlisted_folder_and_module_fail(self):
        files = base_files()
        files["tools/supervisor.py"] = ""
        files["tools/journal/entry.py"] = ""
        files["tools/notes.txt"] = "a tracked file is an entry too\n"
        files["tools/.gitignore"] = "*.tmp\n"
        with project(files) as folder:
            errors, _ = capability_map.check(Path(folder), SITE)
            unlisted = sorted(e for e in errors if "no row links it" in e)
            self.assertEqual(len(unlisted), 3, errors)
            self.assertIn("tools/journal is under the tooling root tools/", unlisted[0])
            self.assertIn("tools/notes.txt", unlisted[1])
            self.assertIn("tools/supervisor.py", unlisted[2])
            # The table's own rows stay fresh; only the three entries fail.
            self.assertEqual(len(errors), 3, errors)

    def test_untracked_tooling_warns_before_the_commit_that_fails(self):
        with project(base_files()) as folder:
            root = Path(folder)
            (root / "tools/scratch.py").write_text("")
            (root / "tools/run_record/extra.py").write_text("")  # inside a folder a row already links
            (root / "tools/.gitignore").write_text("*.tmp\n")
            (root / "tools/ignored.tmp").write_text("")
            subprocess.run(["git", "add", "tools/.gitignore"], cwd=root, check=True)
            errors, warnings = capability_map.check(root, SITE)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, ["docs/CAPABILITY_MAP.md: tools/scratch.py is under the tooling root tools/ "
                                        "and not tracked yet; no row links it, so lint fails once it is committed"])
            # An untracked file that imports a tool announces the stale column too.
            (root / "experiments/attended/later.py").write_text("import tools.judge\n")
            errors, warnings = capability_map.check(root, SITE)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 2, warnings)
            self.assertIn("Imported by for 'Judge a finished run against its criteria' changes once the untracked "
                          "files are committed", warnings[1])
            (root / "experiments/attended/later.py").unlink()
            # The commit turns the same file into the error the warning announced.
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            errors, warnings = capability_map.check(root, SITE)
            self.assertEqual(warnings, [])
            self.assertEqual([e for e in errors if "no row links it" in e],
                             ["docs/CAPABILITY_MAP.md: tools/scratch.py is under the tooling root tools/ "
                              "but no row links it"])

    def test_untracked_files_get_the_warnings_their_commit_would_bring(self):
        with project(base_files()) as folder:
            root = Path(folder)
            (root / "tools/__pycache__").mkdir()
            (root / "tools/__pycache__/judge.cpython-312.pyc").write_bytes(b"cache")
            (root / "tools/run_record/reuse.py").write_text("from experiments.attended.run import x\n")
            (root / "tools/run_record/broken.py").write_text("def (:\n")
            (root / b"tools/run_record/caf\xe9.txt".decode("utf-8", "surrogateescape")).write_text("")
            errors, warnings = capability_map.check(root, SITE)
            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 2, warnings)
            self.assertIn("cannot read the imports of tools/run_record/broken.py", warnings[0])
            self.assertIn("tools/run_record/reuse.py:1 imports experiments/attended/run.py from the experiment folder",
                          warnings[1])

    def test_stale_column_fails_and_the_command_rewrites_it(self):
        with project(base_files(record="`tools/judge.py`")) as folder:
            root = Path(folder)
            errors, _ = capability_map.check(root, SITE)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("Imported by is out of date for 'Record what a native run did'", errors[0])
            self.assertIn("expected: `experiments/attended/`, `tools/judge.py`", errors[0])
            (root / "docs/site").mkdir(parents=True)
            (root / "docs/site/site.toml").write_text('tooling_roots = ["tools/"]\nexperiment_roots = ["experiments/"]\n')
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            self.assertEqual(capability_map.write(root), 1)
            self.assertEqual(capability_map.check(root)[0], [])
            text = (root / "docs/CAPABILITY_MAP.md").read_text()
            self.assertIn("| Judge a finished run against its criteria | [judge.py](../tools/judge.py) | partly | "
                          "no Python imports |", text)
            self.assertIn("- Compare two recorded runs. Decision (owner, 2026-11-15): do not build.", text)
            self.assertEqual(capability_map.write(root), 0)

    def test_state_must_match_the_code_column(self):
        files = base_files()
        files["docs/CAPABILITY_MAP.md"] = files["docs/CAPABILITY_MAP.md"].replace("| partly |", "| planned |").replace(
            "| — | missing | — |", "| [judge.py](../tools/judge.py) | missing | no Python imports |")
        with project(files) as folder:
            errors, _ = capability_map.check(Path(folder), SITE)
            self.assertTrue(any("state 'planned' is not exists, partly or missing" in e for e in errors), errors)
            self.assertTrue(any("a missing need links no code" in e for e in errors), errors)

    def test_tool_importing_from_an_experiment_warns(self):
        files = base_files()
        files["experiments/attended/harness.py"] = "def run(): pass\n"
        files["tools/judge.py"] += "from experiments.attended.harness import run\n"
        with project(files) as folder:
            errors, warnings = capability_map.check(Path(folder), SITE)
            self.assertEqual(len(warnings), 1, warnings)
            self.assertIn("tools/judge.py:2 imports experiments/attended/harness.py from the experiment folder "
                          "experiments/attended/", warnings[0])
            # An experiment importing a tool is the intended direction and is not reported.
            self.assertFalse(any("experiments/attended/run.py" in w for w in warnings))

    def test_relative_and_function_level_imports_count(self):
        files = base_files(record="`experiments/attended/`, `tools/judge.py`, `tools/report/`")
        files["tools/report/__init__.py"] = ""
        files["tools/report/summary.py"] = "def f():\n    from ..run_record import writer\n"
        files["docs/CAPABILITY_MAP.md"] = files["docs/CAPABILITY_MAP.md"].replace(
            "| Replay a recorded run |",
            "| Summarise recorded runs | [report/](../tools/report/) | exists | no Python imports |\n| Replay a recorded run |")
        with project(files) as folder:
            self.assertEqual(capability_map.check(Path(folder), SITE), ([], []))

    def test_unparsable_python_warns_only_under_the_roots(self):
        files = base_files()
        files["tests/fixtures/broken.py"] = "print 'python 2'\n"
        files["experiments/attended/broken.py"] = "def (:\n"
        with project(files) as folder:
            _, warnings = capability_map.check(Path(folder), SITE)
            self.assertEqual(warnings, ["capability map: cannot read the imports of "
                                        "experiments/attended/broken.py: SyntaxError"])

    def test_links_with_a_title_or_an_encoded_space_are_read(self):
        files = base_files()
        files["tools/my tool.py"] = ""
        files["docs/CAPABILITY_MAP.md"] = files["docs/CAPABILITY_MAP.md"].replace(
            "[judge.py](../tools/judge.py)", '[judge.py](../tools/judge.py "the judge"), [t](../tools/my%20tool.py)')
        with project(files) as folder:
            self.assertEqual(capability_map.check(Path(folder), SITE), ([], []))

    def test_stdlib_name_is_not_credited_to_a_namespace_folder(self):
        files = base_files()
        files["logging/notes.txt"] = "no Python here\n"
        files["queue/worker.py"] = ""
        files["tools/judge.py"] += "import logging\nimport queue\n"
        with project(files) as folder:
            imports = capability_map.ImportIndex(Path(folder), capability_map.tracked_files(Path(folder)),
                                                 ("tools",)).imports["tools/judge.py"]
            self.assertEqual([t for _, t in imports], ["tools/run_record/writer.py"])

    def test_the_command_keeps_crlf_line_endings(self):
        files = base_files(record="`tools/judge.py`")
        files["docs/CAPABILITY_MAP.md"] = files["docs/CAPABILITY_MAP.md"].replace("\n", "\r\n")
        files["docs/site/site.toml"] = 'tooling_roots = ["tools/"]\nexperiment_roots = ["experiments/"]\n'
        with project(files) as folder:
            root = Path(folder)
            (root / "docs/CAPABILITY_MAP.md").write_bytes(files["docs/CAPABILITY_MAP.md"].encode())
            self.assertEqual(capability_map.write(root), 1)
            data = (root / "docs/CAPABILITY_MAP.md").read_bytes()
            self.assertEqual(data.count(b"\n"), data.count(b"\r\n"))


class KitLint(unittest.TestCase):
    def test_the_kits_own_map_passes(self):
        errors, warnings = capability_map.check(KIT)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(capability_map.site_settings(KIT)["map"], "docs/KIT_CAPABILITY_MAP.md")

    def test_lint_checks_the_links_of_a_map_outside_docs(self):
        files = base_files()
        files["tools/CAPABILITIES.md"] = files.pop("docs/CAPABILITY_MAP.md").replace("../tools/", "")
        files["docs/site/site.toml"] = 'tooling_roots = ["tools/"]\ncapability_map = "tools/CAPABILITIES.md"\n'
        with project(files) as folder:
            root = Path(folder)
            with mock.patch.object(lint, "REPO", root), mock.patch.object(lint, "DOCS", root / "docs"):
                self.assertIn(root / "tools/CAPABILITIES.md", lint.md_files())


if __name__ == "__main__":
    unittest.main()
