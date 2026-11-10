"""Exercise real Git consumer roots, source boundaries and portable commands."""
import re
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
        self.assertIn(f'data-site-home-label="{self.root.name}"', page)
        self.assertIn('assets/build-sheet.css', page)
        self.assertIn('chapter-reader', page)
        self.assertNotIn('ADP docs', page)
        result = invoke('build', '--project', self.root, '--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_init_writes_entry_templates_under_their_real_names(self):
        # Entry files live in the kit only as *.tmpl, so none is active inside .docs-kit/.
        starter = KIT / 'examples/starter'
        for name in ('AGENTS.md', 'CLAUDE.md', 'docs/PROJECT_CONTEXT.md', 'docs/index.md',
                     'docs/worklog.md', 'docs/open/OPEN.md', 'docs/site/site.toml'):
            self.assertFalse((starter / name).exists(), name + ' is live inside the kit')
            self.assertTrue((self.root / name).is_file(), name + ' was not written')
        self.assertEqual(list(self.root.rglob('*.tmpl')), [])
        config = (self.root / 'docs/site/site.toml').read_text()
        self.assertIn(f'title = "{self.root.name}"', config)
        self.assertNotIn('{{', config)
        other = Path(tempfile.mkdtemp(prefix='docs-kit-titled-'))
        self.addCleanup(shutil.rmtree, other)
        result = invoke('init', other, '--title', 'Say "hi"', '--repository', 'https://example.org/team/repo')
        self.assertEqual(result.returncode, 0, result.stderr)
        config = (other / 'docs/site/site.toml').read_text()
        self.assertIn('title = "Say \\"hi\\""', config)
        self.assertIn('gh_repo = "https://example.org/team/repo"', config)

    def test_init_refuses_existing_files_before_writing_anything(self):
        source = self.root / 'docs/site/site.toml'
        source.write_text('keep this\n')
        result = invoke('init', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No files written', result.stderr)
        self.assertEqual(source.read_text(), 'keep this\n')

    def test_configured_publication_cli_from_unrelated_working_directory(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '''
[publication]
assets_manifest = "docs/site/public-assets.json"
pages = ["index.html", "guide.html"]
private_suffixes = [".md", ".py", ".toml"]
''')
        (self.root / 'docs/site/public-assets.json').write_text('{"files": ["docs/site/result.json"]}')
        (self.root / 'docs/site/result.json').write_text('{"value": 42}')
        self.track()
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination, cwd=Path('/tmp'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((destination / 'index.html').is_file())
        self.assertTrue((destination / 'guide.html').is_file())
        self.assertEqual((destination / 'docs/site/result.json').read_text(), '{"value": 42}')
        self.assertEqual(list(destination.rglob('*.md')), [])
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be fresh', result.stderr)

    def test_publication_rejects_removed_keys(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '''
[publication]
pages = ["index.html"]
[publication.page_routes]
"home.html" = "index.html"
''')
        self.track()
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Unsupported [publication] keys: page_routes', result.stderr)
        self.assertFalse(destination.exists())
        self.assertFalse((self.root / '.build').exists())

    def test_publication_rejects_private_stylesheet_source_alias(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(config.read_text() + '''
[publication]
pages = ["index.html", "guide.html"]
private_prefixes = ["configs/"]
''')
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text().replace('page_css = ["build-sheet.css"]',
                                                  'page_css = ["build-sheet.css", "../../configs/policy.css"]'))
        private = self.root / 'configs/policy.css'
        private.parent.mkdir()
        private.write_text('/* private configuration */')
        self.track()
        subprocess.run(['git', 'add', 'configs'], cwd=self.root, check=True)
        destination = self.root / '_site'
        result = invoke('publish', '--project', self.root, '--out', destination)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Private source cannot be published: configs/policy.css', result.stderr)
        self.assertFalse(destination.exists())

    def test_shared_panel_switcher_needs_no_local_extension(self):
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text().replace('components = ["toc",', 'components = ["panel-switcher", "toc",'))
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / '.build/docs/html'
        page = (output / 'guide.html').read_text()
        self.assertRegex(page, r'href="assets/panel-switcher\.css\?v=[0-9a-f]{10}"')
        self.assertRegex(page, r'src="assets/panel-switcher\.js\?v=[0-9a-f]{10}"')
        for extension in ('js', 'css'):
            name = 'panel-switcher.' + extension
            self.assertEqual((output / 'assets' / name).read_bytes(), (KIT / 'theme/components' / name).read_bytes())
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_path_and_evidence_adapters_are_used(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('path_resolver = "adapter.py"\nevidence_validator = "evidence.py"\n' + config.read_text())
        (self.root / 'adapter.py').write_text('''from pathlib import Path
import os
def resolve_legacy_path(path, root, *, recorded_roots=()):
    path = Path(path)
    path = Path(os.path.abspath(path if path.is_absolute() else root / path))
    old = root / "docs/html"
    return root / ".build/docs/html" / path.relative_to(old) if path.is_relative_to(old) else path
''')
        (self.root / 'evidence.py').write_text('''MANIFESTS = ()
def manifest_documents(root, *, require_all_manifests=False): return [], {}
def verify(root, *, require_all_manifests=False): raise ValueError("project evidence gate exercised")
''')
        self.track()
        subprocess.run(['git', 'add', 'adapter.py', 'evidence.py'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = invoke('lint', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('project evidence gate exercised', result.stdout + result.stderr)

    def test_untracked_adapter_is_rejected_before_execution(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('path_resolver = "adapter.py"\n' + config.read_text())
        (self.root / 'adapter.py').write_text('raise RuntimeError("must never execute")\n')
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must be tracked', result.stderr)
        self.assertNotIn('RuntimeError: must never execute', result.stderr)

    def test_shared_reader_include_needs_no_local_copy(self):
        guide = self.root / 'docs/topics/guide/index.md'
        guide.write_text(guide.read_text().replace('toc = []', 'toc = []\nreader = false').replace('components = ["toc",', 'components = ["chapter-reader", "toc",') + '\n<!-- include: components/chapter-reader.html -->\n')
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'docs/site/components/chapter-reader.html').exists())
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('id="chapter-reader"', page)
        self.assertIn('assets/chapter-reader.js', page)

    def test_adapter_symlink_is_rejected_before_execution(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('path_resolver = "adapter.py"\n' + config.read_text())
        (self.root / 'real.py').write_text('raise RuntimeError("must never execute")\n')
        (self.root / 'adapter.py').symlink_to('real.py')
        self.track()
        subprocess.run(['git', 'add', 'adapter.py', 'real.py'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cannot use symlinks', result.stderr)
        self.assertNotIn('RuntimeError: must never execute', result.stderr)

    def test_project_content_transform_uses_shared_renderer(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('content_transform = "transformer.py"\n' + config.read_text())
        (self.root / 'transformer.py').write_text('''def transform(body, *, metadata, source, root):
    metadata['title'] = 'Imported project content'
    metadata['body_class'] = 'project-reader scientific-content'
    return body.replace('Pin the tools, own the content', 'Imported source remains project-owned')
''')
        self.track()
        subprocess.run(['git', 'add', 'transformer.py'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('<body class="project-reader scientific-content"', page)
        self.assertIn('Imported source remains project-owned', page)
        self.assertIn('<title>Imported project content</title>', page)
        self.assertIn('assets/chapter-reader.js', page)

    def test_transformed_metadata_is_validated_before_output(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('content_transform = "transformer.py"\n' + config.read_text())
        (self.root / 'transformer.py').write_text('''def transform(body, *, metadata, source, root):
    metadata['body_class'] = 'reader" onload="bad()'
    return body
''')
        self.track()
        subprocess.run(['git', 'add', 'transformer.py'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('body_class must contain plain', result.stderr)

    def test_content_transform_cannot_change_registered_page_identity(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('content_transform = "transformer.py"\n' + config.read_text())
        (self.root / 'transformer.py').write_text('''def transform(body, *, metadata, source, root):
    metadata['slug'] = 'unexpected-page'
    return body
''')
        self.track()
        subprocess.run(['git', 'add', 'transformer.py'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('must keep slug and page_css', result.stderr)

    def test_title_and_source_links_belong_to_the_consumer(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text(re.sub(r'^title = ".*"$', 'title = "Second project"\nhome_label = "Second"', config.read_text(), flags=re.M))
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        home = (self.root / '.build/docs/index.html').read_text()
        self.assertIn('<title>Second project</title>', home)
        page = (self.root / '.build/docs/html/guide.html').read_text()
        self.assertIn('data-site-home-label="Second"', page)

    def test_existing_project_can_keep_its_canonical_worklog(self):
        config = self.root / 'docs/site/site.toml'
        lines = config.read_text().splitlines(keepends=True)
        lines.insert(5, 'worklog = "docs/development/worklog.md"\n')
        config.write_text(''.join(lines))
        destination = self.root / 'docs/development/worklog.md'
        destination.parent.mkdir(parents=True)
        (self.root / 'docs/worklog.md').rename(destination)
        for relative in ('docs/PROJECT_CONTEXT.md', 'docs/index.md'):
            index = self.root / relative
            index.write_text(index.read_text().replace('(worklog.md)', '(development/worklog.md)'))
        self.track()
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = invoke('lint', '--project', self.root, '--strict')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_declared_project_assets_are_packaged_without_shared_overwrite(self):
        config = self.root / 'docs/site/site.toml'
        original = config.read_text()
        dependency = self.root / 'renderer.js'
        dependency.write_text('// local renderer dependency\n')
        config.write_text(original + '\n[extra_assets]\n"viewer/renderer.js" = "renderer.js"\n')
        self.track()
        subprocess.run(['git', 'add', 'renderer.js'], cwd=self.root, check=True)
        result = invoke('build', '--project', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / '.build/docs/html/assets/viewer/renderer.js').read_bytes(), dependency.read_bytes())
        config.write_text(original + '\n[extra_assets]\n"base.css" = "renderer.js"\n')
        result = invoke('build', '--project', self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('overwrite a shared asset', result.stderr)
        for name in ('./base.css', 'other/../base.css', '..\\base.css'):
            with self.subTest(name=name):
                config.write_text(original + '\n[extra_assets]\n' + json.dumps(name) + ' = "renderer.js"\n')
                result = invoke('build', '--project', self.root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('contained relative paths', result.stderr)

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
        config.write_text('evidence_manifests = ["docs/evidence/locations.json"]\n' + config.read_text())
        frozen = self.root / 'docs/topics/example/evidence/original.md'
        frozen.parent.mkdir(parents=True)
        frozen.write_text('immutable\n')
        manifest = {'schema_version': 1, 'source_revision': 'a' * 40,
                    'documents': [{'original_path': 'docs/open/original.md',
                                   'path': str(frozen.relative_to(self.root)), 'bytes': 10,
                                   'sha256': hashlib.sha256(b'immutable\n').hexdigest()}]}
        manifest_path = self.root / 'docs/evidence/locations.json'
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest))
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


class LocalArtifactsManifestTest(unittest.TestCase):
    def test_old_project_location_is_not_used(self):
        sys.path.insert(0, str(KIT / 'tooling'))
        import site_paths
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = root / 'docs/project/local-artifacts.json'
            old.parent.mkdir(parents=True)
            old.write_text('{}')
            self.assertIsNone(site_paths.local_artifacts_manifest(root, site={}))
            current = root / 'docs/evidence/local-artifacts.json'
            current.parent.mkdir(parents=True)
            current.write_text('{}')
            self.assertEqual(site_paths.local_artifacts_manifest(root, site={}), current.resolve())


if __name__ == '__main__':
    unittest.main()
