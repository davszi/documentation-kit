"""Assemble the generated website from explicit repository inputs.

Page bodies keep their public docs/html URL layout. Repository source links go
through GitHub (and retain local editor metadata); published media are copied,
while explicitly local evidence stays local. No repository tree is mirrored.
"""
from __future__ import annotations

import html
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import quote, unquote, urlsplit

from site_paths import REPO, DOCS, resolve_legacy_path

ATTR = re.compile(r'(?<![\w-])(href|src|poster)="([^"]*)"')
TAG = re.compile(r'<(a|img|video|audio|source|iframe)\b[^>]*>', re.I)
RESOURCE_SUFFIXES = {'.html', '.json', '.js', '.css', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.glb'}


class SiteBundle:
    def __init__(self, site: dict, root: Path = REPO):
        self.root = root
        self.repository = site['gh_repo'].rstrip('/')
        self.ref = site.get('gh_ref', 'main')
        result = subprocess.run(['git', 'ls-files', '-z'], cwd=root, capture_output=True, check=True)
        self.tracked = {resolve_legacy_path(root / path, root=root)
                        for path in result.stdout.decode().split('\0') if path}
        self.resources: dict[str, bytes] = {}
        self.local_media: set[str] = set()
        self.declared_local = set(site.get('local_media', []))
        import json
        local_manifest = root / 'docs/project/local-artifacts.json'
        if local_manifest.is_file():
            self.declared_local.update(json.loads(local_manifest.read_text())['omitted_files'])

    def _copy(self, source: Path, name: str):
        if source.is_symlink() or not source.resolve().is_relative_to(self.root):
            raise ValueError(f'Website resource must be a regular repository file: {source}')
        if source not in self.tracked or not source.is_file():
            raise ValueError(f'Website resource is not a tracked file: {source}')
        self.resources[name] = source.read_bytes()

    def source_url(self, path: Path, fragment: str = '') -> str:
        relative = path.relative_to(self.root).as_posix()
        kind = 'tree' if path.is_dir() else 'blob'
        return (self.repository + '/' + kind + '/' + quote(self.ref, safe='') + '/'
                + quote(relative, safe='/') + ('#' + quote(fragment, safe='-_.~') if fragment else ''))

    def rewrite_page(self, markup: str) -> str:
        def add_attributes(tag, attributes):
            return re.sub(r'(\s*/?>)$', lambda m: ' ' + attributes + m[1], tag)

        def locate(raw):
            url = urlsplit(html.unescape(raw))
            if not url.path or url.scheme or url.netloc:
                return None
            logical = self.root / posixpath.normpath('docs/html/' + unquote(url.path))
            dest = resolve_legacy_path(logical, root=self.root)
            if not dest.is_relative_to(self.root):
                raise ValueError('Website link escapes the repository: ' + raw)
            public = (logical.is_relative_to(self.root / 'docs/html')
                      or dest.is_relative_to(self.root / 'docs/figures')
                      or (dest.is_relative_to(self.root / 'docs/site/fragments')
                          and dest.suffix in RESOURCE_SUFFIXES))
            return url, dest, public

        def tag_replace(match):
            tag, original = match[1].lower(), match[0]
            attributes = dict(ATTR.findall(original))
            if tag == 'a':
                raw = attributes.get('href', '')
                located = locate(raw)
                if located is None or located[2]:
                    return original
                url, dest, _ = located
                relative = dest.relative_to(self.root).as_posix()
                href = html.escape(self.source_url(dest, url.fragment), quote=True)
                updated = original.replace('href="' + raw + '"', 'href="' + href + '"', 1)
                return add_attributes(updated, 'data-repo-path="' + html.escape(relative, quote=True)
                                      + '" data-repo-fragment="' + html.escape(url.fragment, quote=True) + '"')
            updated = original
            for resource_attr in ('src', 'poster'):
                raw = attributes.get(resource_attr)
                if not raw:
                    continue
                located = locate(raw)
                if located is None or located[2]:
                    continue
                _, source, _ = located
                relative = source.relative_to(self.root).as_posix()
                if source in self.tracked:
                    self._copy(source, 'html/_media/' + relative)
                    updated = updated.replace(resource_attr + '="' + raw + '"', resource_attr + '="_media/' + html.escape(relative, quote=True) + '"', 1)
                elif relative in self.declared_local:
                    self.local_media.add(relative)
                    updated = re.sub(r'(?<![\w-])' + resource_attr + '="' + re.escape(raw) + '"', '', updated, count=1)
                    updated = add_attributes(updated, 'data-local-' + resource_attr + '="' + html.escape(relative, quote=True) + '"')
                else:
                    raise ValueError('Untracked website media are not registered as local evidence: ' + relative)
            return updated
        rendered = TAG.sub(tag_replace, markup)
        note = '<span class="local-evidence-note">Capture retained in the local evidence collection.</span>'
        # Put notices outside playable elements; fallback children are hidden by
        # browsers that support video/audio, including nested <source> layouts.
        rendered = re.sub(r'<(video|audio)\b[^>]*>[\s\S]*?</\1>',
                          lambda m: m[0] + (note if 'data-local-' in m[0] else ''), rendered)
        return re.sub(r'<img\b[^>]*data-local-[^>]*>', lambda m: m[0] + note, rendered)

    def gather(self) -> dict[str, bytes]:
        for source in sorted(self.tracked):
            if source.is_relative_to(self.root / 'docs/figures'):
                self._copy(source, source.relative_to(self.root / 'docs').as_posix())
            elif source.is_relative_to(self.root / 'docs/site/fragments') and source.suffix in RESOURCE_SUFFIXES:
                relative = source.relative_to(self.root / 'docs/site/fragments').as_posix()
                self._copy(source, 'site/fragments/' + relative)
                # Old published fragment URLs remain available as generated aliases.
                data = self.resources['site/fragments/' + relative]
                if source.suffix == '.html':
                    data = data.replace(b'../figures/', b'../../figures/')
                    self.resources['site/fragments/' + relative] = data
                self.resources['src/fragments/' + relative] = data
        return self.resources


def validate_resources(outputs: dict[str, bytes]) -> list[str]:
    """Check physical resource closure without treating source links as assets."""
    errors = []
    for name, data in outputs.items():
        if not name.startswith('html/') or not name.endswith('.html'):
            continue
        for tag in re.finditer(r'<(img|video|audio|source|iframe|script|link)\b[^>]*>', data.decode(), re.I):
            for attr, target in ATTR.findall(tag[0]):
                if attr == 'href' and tag[1].lower() != 'link':
                    continue
                target = html.unescape(target)
                url = urlsplit(target)
                if not url.path or url.scheme or url.netloc:
                    continue
                resource = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
                if resource not in outputs:
                    errors.append(name + ': missing packaged resource ' + target)
    return errors
