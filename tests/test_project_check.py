"""`docsite.py check` and the pre-push hook: the steps, their order, and where each stops."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))

from project_check import declared  # noqa: E402

HOOK = KIT / 'hooks/pre-push'


def clean_env(**extra):
    drop = {'GITHUB_SHA', 'DOCSITE_PROJECT_ROOT', 'DOCS_PYTHON', 'DOCSITE_GENERAL_PASSWORD', 'DOCSITE_REFERENCE_PASSWORD'}
    return {**{name: value for name, value in os.environ.items() if name not in drop}, **extra}


class Declared(unittest.TestCase):
    def test_none_and_valid(self):
        self.assertEqual(declared({}), [])
        self.assertEqual(declared({'checks': [{'name': ' tests ', 'command': ['{python}', '-m', 'unittest']},
                                              {'command': ['node', 'check.cjs']}]}),
                         [('tests', ['{python}', '-m', 'unittest']), ('node check.cjs', ['node', 'check.cjs'])])

    def test_invalid_entries_are_named(self):
        for site, part in (({'checks': 'pytest'}, 'checks must be a list of tables'),
                           ({'checks': [{'command': 'pytest -q'}]}, 'entry 1 needs command as a list'),
                           ({'checks': [{'command': []}]}, 'entry 1 needs command as a list'),
                           ({'checks': [{'command': ['a'], 'shell': True}]}, "entry 1 has the unknown key 'shell'"),
                           ({'checks': [{'command': ['a']}, {'command': ['b'], 'name': 3}]}, 'entry 2 has a name')):
            with self.assertRaisesRegex(ValueError, part, msg=site):
                declared(site)


class Check(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-check-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.git('init', '-q')
        self.assertEqual(self.docsite('init', self.root).returncode, 0)
        self.config = self.root / 'docs/site/site.toml'
        self.git('add', '-A')

    def git(self, *args):
        subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)

    def docsite(self, *args, **env):
        return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                              capture_output=True, text=True, env=clean_env(**env))

    def check(self, **env):
        return self.docsite('check', '--project', self.root, **env)

    def declare(self, text):
        self.config.write_text(self.config.read_text() + text)
        self.git('add', '-A')

    def test_a_starter_project_passes_without_a_built_site(self):
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('check 1/2: build', result.stdout)
        self.assertIn('check 2/2: lint --strict', result.stdout)
        self.assertIn('check passed: 2 step(s)', result.stdout)

    def test_declared_checks_run_in_order_and_stop_at_the_first_failure(self):
        mark = self.root / 'ran.txt'
        self.declare('\n[[checks]]\nname = "first"\ncommand = ["{python}", "-c", "open(\'ran.txt\', \'a\').write(\'1\')"]\n'
                     '\n[[checks]]\nname = "second"\ncommand = ["{python}", "-c", "import sys; sys.exit(7)"]\n'
                     '\n[[checks]]\nname = "third"\ncommand = ["{python}", "-c", "open(\'ran.txt\', \'a\').write(\'3\')"]\n')
        result = self.check()
        self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
        self.assertEqual(mark.read_text(), '1')
        self.assertIn('check 4/5: second', result.stdout)
        self.assertNotIn('check 5/5', result.stdout)
        self.assertIn('check failed at step 4: second', result.stderr)

    def test_a_lint_failure_stops_before_the_declared_checks(self):
        self.declare('\n[[checks]]\nname = "never"\ncommand = ["{python}", "-c", "open(\'ran.txt\', \'w\')"]\n')
        (self.root / 'docs/worklog.md').write_text('# Worklog\n\nSee [the plan](missing.md).\n')
        self.git('add', '-A')
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('check failed at step 2: lint --strict', result.stderr)
        self.assertFalse((self.root / 'ran.txt').exists())

    def test_a_command_that_is_not_installed_is_named(self):
        self.declare('\n[[checks]]\ncommand = ["no-such-program-of-the-kit", "--version"]\n')
        result = self.check()
        self.assertEqual(result.returncode, 127)
        self.assertIn('cannot run no-such-program-of-the-kit', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_wrong_configuration_fails_before_anything_runs(self):
        self.declare('\n[[checks]]\ncommand = "pytest -q"\n')
        result = self.check()
        self.assertEqual(result.returncode, 2)
        self.assertIn('site.toml: [[checks]] entry 1 needs command as a list', result.stderr)
        self.assertNotIn('check 1/', result.stdout)

    def test_a_configured_publication_is_tried_and_leaves_nothing_behind(self):
        self.declare('\n[publication]\npages = ["guide.html"]\n')
        before = sorted(path.name for path in self.root.iterdir())
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('check 3/3: publish, into a temporary folder', result.stdout)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), sorted({*before, '.build'}))

    def test_a_publication_that_fails_stops_the_check(self):
        self.declare('\n[publication]\npages = ["no-such-page.html"]\n')
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('check failed at step 3: publish', result.stderr)

    def test_the_trial_publish_is_skipped_when_the_lock_has_no_passwords(self):
        self.declare('\n[publication]\npages = ["guide.html"]\nlock = true\n')
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('skipped: the page lock is on and DOCSITE_GENERAL_PASSWORD and DOCSITE_REFERENCE_PASSWORD '
                      'are not set', result.stdout)
        self.assertIn('check passed: 3 step(s), the trial publish skipped', result.stdout)


class Hook(unittest.TestCase):
    """The hook finds an interpreter and hands over to `docsite.py check`; a stub stands in for the kit."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-hook-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name).resolve()
        subprocess.run(['git', 'init', '-q'], cwd=self.root, check=True)
        (self.root / '.docs-kit').mkdir()
        (self.root / '.docs-kit/docsite.py').write_text('import sys\nprint("ARGS", *sys.argv[1:])\nsys.exit(5)\n')
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', 'commit', '-q', '-m', 'Start'],
                       cwd=self.root, check=True)

    def push(self, **env):
        return subprocess.run(['sh', str(HOOK)], cwd=self.root, capture_output=True, text=True, env=clean_env(**env))

    def test_it_is_executable_and_runs_the_check_with_the_named_interpreter(self):
        self.assertTrue(os.access(HOOK, os.X_OK))
        result = self.push(DOCS_PYTHON=sys.executable)
        self.assertEqual(result.returncode, 5, result.stderr)
        self.assertEqual(result.stdout.strip(), f'ARGS check --project {self.root}')
        self.assertEqual(result.stderr, '')

    def test_it_uses_the_projects_environment_and_says_when_the_tree_is_dirty(self):
        env_bin = self.root / '.build/docs-env/bin'
        env_bin.mkdir(parents=True)
        (env_bin / 'python').symlink_to(sys.executable)
        result = self.push()
        self.assertEqual(result.returncode, 5, result.stderr)
        self.assertIn('ARGS check --project', result.stdout)
        self.assertIn('the working tree has uncommitted changes', result.stderr)  # .build is not ignored here

    def test_it_stops_without_an_interpreter(self):
        result = self.push()
        self.assertEqual(result.returncode, 1)
        self.assertIn('no documentation interpreter', result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
