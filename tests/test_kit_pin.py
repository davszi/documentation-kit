from pathlib import Path
import subprocess
import tempfile
import unittest

from kit_pin import unpublished_pin


def git(cwd, *args):
    subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                    '-c', 'init.defaultBranch=main', '-c', 'protocol.file.allow=always', *args],
                   cwd=cwd, check=True, capture_output=True)


class KitPinTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.upstream, self.project = base / 'kit.git', base / 'project'
        source = base / 'source'
        git(base, 'init', '--bare', str(self.upstream))
        git(base, 'init', str(source))
        (source / 'VERSION').write_text('1\n')
        git(source, 'add', 'VERSION')
        git(source, 'commit', '-m', 'Start the kit')
        git(source, 'push', str(self.upstream), 'HEAD:main')
        self.project.mkdir()
        self.kit = self.project / '.docs-kit'
        git(base, 'clone', str(self.upstream), str(self.kit))

    def tearDown(self):
        self.tmp.cleanup()

    def test_pushed_pin_passes(self):
        self.assertIsNone(unpublished_pin(self.kit, self.project))

    def test_local_only_commit_fails(self):
        (self.kit / 'VERSION').write_text('2\n')
        git(self.kit, 'commit', '-am', 'Change the kit inside the project')
        problem = unpublished_pin(self.kit, self.project)
        self.assertIn('on no remote branch', problem)
        self.assertIn('.docs-kit', problem)
        git(self.kit, 'push', 'origin', 'HEAD:main')
        git(self.kit, 'fetch', 'origin')
        self.assertIsNone(unpublished_pin(self.kit, self.project))

    def test_local_tag_does_not_count_as_published(self):
        (self.kit / 'VERSION').write_text('2\n')
        git(self.kit, 'commit', '-am', 'Change the kit inside the project')
        git(self.kit, 'tag', 'v2')
        self.assertIsNotNone(unpublished_pin(self.kit, self.project))

    def test_skipped_outside_project_for_own_repository_and_shallow_checkout(self):
        (self.kit / 'VERSION').write_text('2\n')
        git(self.kit, 'commit', '-am', 'Unpushed kit work')
        self.assertIsNone(unpublished_pin(self.kit, self.kit))
        self.assertIsNone(unpublished_pin(self.kit, Path(self.tmp.name) / 'elsewhere'))
        shallow = self.project / 'shallow-kit'
        git(self.project, 'clone', '--depth', '1', f'file://{self.upstream}', str(shallow))
        self.assertIsNone(unpublished_pin(shallow, self.project))

    def test_copy_without_git_metadata_is_skipped(self):
        copy = self.project / 'vendored'
        copy.mkdir()
        (copy / 'VERSION').write_text('1\n')
        # The project itself is not a Git repository, so the copy has no toplevel.
        self.assertIsNone(unpublished_pin(copy, self.project))


if __name__ == '__main__':
    unittest.main()
