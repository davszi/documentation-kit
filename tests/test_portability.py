"""Exercise real Git consumer roots, source boundaries and portable commands."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]


def invoke(*args, cwd=KIT):
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          cwd=cwd, capture_output=True, text=True)


class Consumers(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='docs-kit-consumer-')
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        subprocess.run(['git', 'init', '-q', self.root], check=True)
        result = invoke('init', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def track(self):
        subprocess.run(['git', 'add', 'docs', 'AGENTS.md', 'CLAUDE.md'], cwd=self.root, check=True)

    def test_build_and_strict_lint_from_unrelated_working_directory(self):
        self.track()
        result = invoke('build', '--project', self.root, cwd=Path('/tmp'))
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('data-site-home-label="Docs"', page)
        self.assertIn('assets/build-sheet.css', page)
        self.assertIn('chapter-reader', page)
        self.assertNotIn('ADP docs', page)
        result = invoke('build', '--project', self.root, '--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_init_refuses_existing_files_before_writing_anything(self):
        source = self.root / 'docs/site/site.toml'
        source.write_text('keep this\n')
        result = invoke('init', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No files written', result.stderr)
        self.assertEqual(source.read_text(), 'keep this\n')

    def test_title_and_source_links_belong_to_the_consumer(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text().replace('Documentation kit', 'Second project').replace('home_label = "Docs"', 'home_label = "Second"'))
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        home = (self.root / '.build/docs/index.html').read_text()
        self.assertIn('<title>Second project</title>', home)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('data-site-home-label="Second"', page)

    def test_missing_required_resource_fails_instead_of_publishing_broken_media(self):
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text() + '\n<img src="../figures/missing.svg" alt="Missing">\n')
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)

    def test_undeclared_untracked_media_are_rejected(self):
        image = self.root / 'capture.png'
        image.write_bytes(b'not a real image, path admission only')
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text() + '\n<img src="../../capture.png" alt="Capture">\n')
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Untracked', result.stderr)

    def test_declared_evidence_mismatch_fails_lint(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('evidence_manifests = ["docs/project/evidence-locations.json"]\n' + config.read_text())
        frozen = self.root / 'docs/topics/example/evidence/original.md'
        frozen.parent.mkdir(parents=True)
        frozen.write_text('immutable\n')
        manifest = {'schema_version': 1, 'source_revision': 'a' * 40,
                    'documents': [{'original_path': 'docs/open/original.md',
                                   'path': str(frozen.relative_to(self.root)), 'bytes': 10,
                                   'sha256': hashlib.sha256(b'immutable\n').hexdigest()}]}
        (self.root / 'docs/project/evidence-locations.json').write_text(json.dumps(manifest))
        frozen.write_text('changed\n')
        self.track()
        result = invoke('lint', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Evidence identity mismatch', result.stderr)

    def test_local_css_cannot_replace_shared_theme(self):
        css = self.root / 'docs/site/assets/base.css'
        css.parent.mkdir(parents=True)
        css.write_text('body { color: red; }')
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text().replace('"build-sheet.css"', '"../site/assets/base.css"'))
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('would overwrite a shared asset', result.stderr)

    def test_untracked_css_include_and_extension_are_rejected(self):
        for kind in ('css', 'include', 'extension'):
            with self.subTest(kind=kind):
                guide = self.root / 'docs/topics/guide/index.md'
                original = guide.read_text()
                config = self.root / 'docs/site/site.toml'
                config_original = config.read_text()
                if kind == 'css':
                    local = self.root / 'docs/site/assets/untracked.css'
                    guide.write_text(original.replace('"build-sheet.css"', '"../site/assets/untracked.css"'))
                    content = 'body { color: red; }'
                elif kind == 'include':
                    local = self.root / 'docs/site/fragments/untracked.html'
                    guide.write_text(original + '\n<!-- include: fragments/untracked.html -->\n')
                    content = '<p>Untracked</p>'
                else:
                    local = self.root / 'docs/site/components/untracked.js'
                    config.write_text('extra_components = ["untracked"]\n' + config_original)
                    content = 'console.log("untracked")'
                self.track()
                local.parent.mkdir(parents=True, exist_ok=True)
                local.write_text(content)
                result = invoke('build', '--project', self.root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('must be tracked', result.stderr)
                local.unlink()
                guide.write_text(original)
                config.write_text(config_original)

    def test_svg_inlining_rejects_external_and_untracked_sources(self):
        self.track()
        guide = self.root / 'docs/topics/guide/index.md'
        original = guide.read_text()
        with tempfile.NamedTemporaryFile(suffix='.svg', mode='w') as outside:
            outside.write('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
            outside.flush()
            relative = os.path.relpath(outside.name, self.root / 'docs/figures')
            guide.write_text(original + f'\n<img src="../figures/{relative}" alt="External">\n')
            result = invoke('build', '--project', self.root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('escapes its root', result.stderr)
        local = self.root / 'docs/figures/untracked.svg'
        local.parent.mkdir()
        local.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        guide.write_text(original + '\n<img src="../figures/untracked.svg" alt="Untracked">\n')
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be tracked', result.stderr)

    def test_init_rejects_a_symlinked_destination_parent(self):
        project, external = self.root / 'second', self.root / 'elsewhere'
        project.mkdir()
        external.mkdir()
        (project / 'docs').symlink_to(external, target_is_directory=True)
        result = invoke('init', project)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No files written', result.stderr)
        self.assertEqual(list(external.iterdir()), [])

    def test_an_actual_git_submodule_builds_and_pins_its_commit(self):
        provider, consumer = self.root / 'provider', self.root / 'consumer'
        shutil.copytree(KIT, provider, ignore=shutil.ignore_patterns('.git', '.build', '__pycache__'))
        subprocess.run(['git', 'init', '-q', provider], check=True)
        subprocess.run(['git', 'add', '.'], cwd=provider, check=True)
        subprocess.run(['git', '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Shared kit fixture'], cwd=provider, check=True)
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=provider, text=True).strip()
        subprocess.run(['git', 'init', '-q', consumer], check=True)
        subprocess.run(['git', '-c', 'protocol.file.allow=always', 'submodule', 'add', '-q', str(provider), '.docs-kit'], cwd=consumer, check=True)
        command = [sys.executable, str(consumer / '.docs-kit/docsite.py')]
        subprocess.run([*command, 'init', str(consumer)], cwd=consumer, check=True, capture_output=True)
        subprocess.run(['git', 'add', 'docs', 'AGENTS.md', 'CLAUDE.md'], cwd=consumer, check=True)
        result = subprocess.run([*command, 'build', '--project', str(consumer)], cwd=consumer, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        index = subprocess.check_output(['git', 'ls-files', '--stage', '.docs-kit'], cwd=consumer, text=True)
        self.assertIn('160000 ' + revision, index)


if __name__ == '__main__':
    unittest.main()
