"""Configured publication preserves boundaries and atomic failure behavior."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from publication import publish_project


class ProjectPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'project'
        self.generated = self.root / '.build/docs/html'
        self.generated.mkdir(parents=True)
        (self.generated.parent / 'site-build.json').write_text('{"resource_origins": {}}')
        self.output = self.root / '_site'
        self.kit = Path(__file__).resolve().parents[1]
        self.tracked = []
        self.put('docs/site/site.toml', '''title = "Example"
[publication]
assets_manifest = "docs/site/assets.json"
pages = ["overview.html"]
private_suffixes = [".md", ".py", ".toml"]
private_prefixes = ["configs/"]
''')
        self.put('docs/site/assets.json', json.dumps({'files': ['evidence/result.json']}))
        self.put('evidence/result.json', '{"value": 42}')
        (self.generated / 'overview.html').write_text(
            '<script>{"literal":"overview.html"}</script><a href="overview.html#result">Read</a>'
            '<img src="_media/evidence/result.json">')
        (self.generated / 'assets').mkdir()
        (self.generated / 'assets/base.css').write_text('body {color: white}')

    def put(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        if name not in self.tracked:
            self.tracked.append(name)
        return path

    def publish(self):
        with patch('publication.subprocess.check_output', return_value='\0'.join(self.tracked) + '\0'), \
             patch('publication.subprocess.run') as build, contextlib.redirect_stdout(io.StringIO()):
            publish_project(self.root, self.output, kit=self.kit)
            build.assert_called_once()

    def test_pages_resources_and_opaque_scripts(self):
        self.publish()
        page = (self.output / 'overview.html').read_text()
        self.assertIn('href="overview.html#result"', page)
        self.assertIn('<script>{"literal":"overview.html"}</script>', page)
        self.assertIn('src="evidence/result.json"', page)
        self.assertEqual((self.output / 'evidence/result.json').read_bytes(),
                         (self.root / 'evidence/result.json').read_bytes())
        self.assertEqual((self.output / 'assets/base.css').read_text(), 'body {color: white}')
        self.assertFalse((self.output / 'docs').exists())
        self.assertEqual(list(self.root.glob('.docsite-publish-*')), [])

    def test_unsupported_publication_keys_are_rejected_before_building(self):
        for extra in ('[publication.page_routes]\n"index.html" = "overview.html"\n',
                      '[publication.files]\n"docs/site/entry.html" = "index.html"\n',
                      'retired_routes = "docs/site/retired.json"\n'):
            with self.subTest(extra=extra):
                config = self.root / 'docs/site/site.toml'
                original = config.read_text()
                # Keys before a subtable stay in [publication]; subtables close it.
                config.write_text(original.replace('pages = ', extra + 'pages = ', 1)
                                  if not extra.startswith('[') else original + extra)
                with patch('publication.subprocess.run') as build:
                    with self.assertRaisesRegex(ValueError, 'Unsupported \\[publication\\] keys: '
                                                '(page_routes|files|retired_routes); supported keys: '
                                                'assets_manifest, pages, private_suffixes, private_prefixes'):
                        publish_project(self.root, self.output, kit=self.kit)
                    build.assert_not_called()
                self.assertFalse(self.output.exists())
                config.write_text(original)

    def test_missing_publication_table_is_rejected(self):
        self.put('docs/site/site.toml', 'title = "Example"\n')
        with self.assertRaisesRegex(ValueError, 'Configure \\[publication\\]'):
            self.publish()
        self.assertFalse(self.output.exists())

    def test_existing_output_is_never_overwritten(self):
        self.output.mkdir()
        marker = self.output / 'keep'
        marker.write_text('owned by another build')
        with self.assertRaisesRegex(ValueError, 'must be fresh'):
            self.publish()
        self.assertEqual(marker.read_text(), 'owned by another build')

    def test_untracked_missing_private_and_duplicate_assets_leave_no_output(self):
        for names in (['missing.json'], ['untracked.json'], ['notes.md'], ['configs/run.json'],
                      ['evidence/result.json', 'evidence/result.json'], ['../outside.json']):
            with self.subTest(names=names):
                self.put('docs/site/assets.json', json.dumps({'files': names}))
                self.put('notes.md', 'private')
                self.put('configs/run.json', '{}')
                (self.root / 'untracked.json').write_text('{}')
                with self.assertRaises(ValueError):
                    self.publish()
                self.assertFalse(self.output.exists())

    def test_failed_export_leaves_no_output(self):
        self.put('docs/site/site.toml', (self.root / 'docs/site/site.toml').read_text()
                 .replace('pages = ["overview.html"]', 'pages = ["missing.html"]'))
        with self.assertRaisesRegex(ValueError, 'generated HTML'):
            self.publish()
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.docsite-publish-*')), [])

    def test_source_and_destination_symlinks_are_rejected(self):
        (self.root / 'evidence/result.json').unlink()
        (self.root / 'evidence/result.json').symlink_to(self.root / 'docs/site/assets.json')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.publish()
        self.assertFalse(self.output.exists())
        self.output.symlink_to(self.root / 'elsewhere')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.publish()

    def test_private_generated_assets_and_media_cannot_bypass_manifest_policy(self):
        for name in ('assets/private.md', '_media/configs/run.json'):
            with self.subTest(name=name):
                path = self.generated / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('private')
                with self.assertRaisesRegex(ValueError, 'Private source'):
                    self.publish()
                self.assertFalse(self.output.exists())
                path.unlink()

    def test_generated_source_alias_cannot_disguise_private_configuration(self):
        config = self.root / 'docs/site/site.toml'
        config.write_text('[extra_assets]\n"data.json" = "configs/run.json"\n' + config.read_text())
        with self.assertRaisesRegex(ValueError, 'Private source'):
            self.publish()
        self.assertFalse(self.output.exists())

    def test_resource_origin_cannot_disguise_private_stylesheet(self):
        (self.generated.parent / 'site-build.json').write_text(json.dumps({
            'resource_origins': {'html/assets/policy.css': 'configs/policy.css'}}))
        with self.assertRaisesRegex(ValueError, 'Private source'):
            self.publish()
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
