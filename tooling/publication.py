"""Copy an existing generated bundle into a consumer-owned publication tree.

This optional overlay does not build pages, discover repository resources or
choose source URLs. Consumers supply admitted public files, private-file policy
and the exact existing outputs that may be replaced. HTML changes use source
spans; scripts, JSON, labels and unrelated attributes remain opaque.
"""
from __future__ import annotations

import html
from pathlib import Path, PurePosixPath
import posixpath
import re
from collections.abc import Iterable, Mapping
from urllib.parse import unquote, urlsplit

from chapter_layout import Structure


# Applied only to an actual opening tag found by Structure, never page text.
_ATTRIBUTE = re.compile(
    r'''(?P<space>\s+)(?P<name>[^\s/>=]+)(?:\s*=\s*(?:"(?P<double>[^"]*)"|'(?P<single>[^']*)'|(?P<bare>[^\s>]+)))?'''
)
_MEDIA = frozenset({'img', 'iframe', 'video', 'audio', 'source'})


def _name(value: str) -> str:
    """Require an unambiguous, normalized bundle/repository relative path."""
    if (not isinstance(value, str) or not value or '\\' in value or '\x00' in value
            or '?' in value or '#' in value or PurePosixPath(value).is_absolute()
            or any(part in {'', '.', '..'} for part in value.split('/'))):
        raise ValueError(f'Invalid publication path: {value!r}')
    return value


def _contained(root: Path, name: str) -> Path:
    path = root
    for part in _name(name).split('/'):
        path /= part
        if path.is_symlink():
            raise ValueError(f'Publication path cannot follow a symlink: {name}')
    if not path.resolve().is_relative_to(root):
        raise ValueError(f'Publication path escapes its root: {name}')
    return path


def _relative(page: str, target: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(page) or '.')


def _opening(markup: str, node, changes: Mapping[str, str | None]) -> str:
    """Change whole attribute tokens without matching inside another value."""
    original = markup[node.start:node.opening_end]
    edits = []
    tag_end = re.match(r'<\s*[^\s/>]+', original).end()
    for match in _ATTRIBUTE.finditer(original, tag_end):
        name = match['name'].lower()
        if name not in changes:
            continue
        value = changes[name]
        if value is None:
            edits.append((match.start(), match.end(), ''))
            continue
        group = next((key for key in ('double', 'single', 'bare') if match[key] is not None), None)
        if group is None:
            continue
        escaped = html.escape(value, quote=True)
        # Retain the existing quote style; quote a bare replacement when needed.
        if group == 'bare' and re.search(r'''[\s"'`=<>]''', escaped):
            escaped = '"' + escaped + '"'
        edits.append((match.start(group), match.end(group), escaped))
    for start, end, replacement in reversed(edits):
        original = original[:start] + replacement + original[end:]
    return original


def _rewrite(markup: str, *, page: str, root: Path,
             tracked: set[str], public_files: set[str], private_suffixes: tuple[str, ...], private_prefixes: tuple[str, ...],
             local_notice: tuple[str, str]) -> str:
    edits = []
    structure = Structure(markup)
    for top in structure.roots:
        for node in top.descendants():
            changes = {}
            if node.tag in _MEDIA:
                for attr in ('src', 'poster'):
                    value = node.attrs.get(attr) or ''
                    url = urlsplit(value)
                    # SiteBundle emits root-relative-to-generated-page _media URLs.
                    if url.scheme or url.netloc or not url.path.startswith('_media/'):
                        continue
                    repository_path = unquote(url.path[len('_media/'):])
                    # Validated public files are tracked and available at this path.
                    if repository_path in public_files:
                        changes[attr] = _relative(page, repository_path) + value[len(url.path):]
            elif node.tag == 'a':
                repository_path = node.attrs.get('data-repo-path')
                if repository_path:
                    local = _contained(root, repository_path)
                    if repository_path not in tracked and not local.is_dir():
                        if node.end == node.opening_end:
                            raise ValueError('Local-evidence link is not a complete anchor')
                        css, title = local_notice
                        opening = ('<span class="' + html.escape(css, quote=True)
                                   + '" title="' + html.escape(title, quote=True) + '">')
                        edits.extend(((node.start, node.opening_end, opening),
                                      (node.closing_start, node.end, '</span>')))
                        continue
                    if (repository_path in public_files
                            and not repository_path.endswith(private_suffixes)
                            and not repository_path.startswith(private_prefixes)):
                        fragment = node.attrs.get('data-repo-fragment', '')
                        changes.update({'href': _relative(page, repository_path) + ('#' + fragment if fragment else ''),
                                        'data-repo-path': None, 'data-repo-fragment': None})
            if changes:
                updated = _opening(markup, node, changes)
                if updated != markup[node.start:node.opening_end]:
                    edits.append((node.start, node.opening_end, updated))
    for start, end, updated in sorted(edits, reverse=True):
        markup = markup[:start] + updated + markup[end:]
    return markup


def export_pages(generated_root: Path, destination: Path, *, root: Path,
                 tracked: Iterable[str], pages: Iterable[str],
                 public_files: Iterable[str], replace: Iterable[str] = (),
                 private_suffixes: tuple[str, ...] = (), private_prefixes: tuple[str, ...] = (),
                 local_notice: tuple[str, str] = ('local-evidence', 'Local evidence file; not published')) -> tuple[str, ...]:
    """Export generated files and rewrite only explicitly selected output pages.

    Every generated file is published under its generated path. ``pages`` names
    generated HTML files to rewrite. ``public_files`` names tracked repository
    paths that are published at the same path, either already in the destination
    or among the generated outputs. The exporter never copies source files or
    chooses source links. ``replace`` authorizes replacing existing destination
    files; byte-identical files need no authorization. Validation and rewriting
    finish before any destination file is written.
    """
    for directory in (generated_root, destination, root):
        directory = Path(directory).absolute()
        for component in (directory, *directory.parents):
            if component.is_symlink():
                raise ValueError(f'Publication root cannot follow a symlink: {directory}')
    generated_root, destination, root = (Path(path).resolve() for path in (generated_root, destination, root))
    if not generated_root.is_dir() or not root.is_dir():
        raise ValueError('Publication requires existing generated and repository directories')
    if generated_root.is_relative_to(destination) or destination.is_relative_to(generated_root):
        raise ValueError('Generated and publication directories must not overlap')
    tracked = {_name(name) for name in tracked}
    pages, replace = {_name(name) for name in pages}, {_name(name) for name in replace}
    public_files = {_name(name) for name in public_files}
    outputs = {}
    for path in sorted(generated_root.rglob('*')):
        name = path.relative_to(generated_root).as_posix()
        regular = _contained(generated_root, name)
        if regular.is_dir():
            continue
        if not regular.is_file():
            raise ValueError(f'Generated output is not a regular file: {name}')
        if name.startswith('_media/'):
            repository_path = name[len('_media/'):]
            if repository_path not in tracked or not _contained(root, repository_path).is_file():
                raise ValueError(f'Generated media is not a tracked repository file: {repository_path}')
        outputs[name] = regular.read_bytes()
    if pages - outputs.keys() or any(not name.endswith('.html') for name in pages):
        raise ValueError('Publication pages must name generated HTML outputs')
    if replace - outputs.keys():
        raise ValueError('Publication replacements must name generated outputs')

    for name in sorted(public_files):
        if (name not in tracked or not _contained(root, name).is_file()
                or not (name in outputs or _contained(destination, name).is_file())):
            raise ValueError(f'Public file must be a tracked, present repository resource: {name}')
    for page in pages:
        outputs[page] = _rewrite(outputs[page].decode('utf-8'), page=page, root=root,
                                 tracked=tracked, public_files=public_files,
                                 private_suffixes=tuple(private_suffixes), private_prefixes=tuple(private_prefixes),
                                 local_notice=local_notice).encode('utf-8')
    for name, data in outputs.items():
        target = _contained(destination, name)
        parent = PurePosixPath(name).parent
        while parent != PurePosixPath('.'):
            existing = _contained(destination, parent.as_posix())
            if existing.exists() and not existing.is_dir():
                raise ValueError(f'Publication file/directory collision: {name}')
            parent = parent.parent
        if target.exists() and (not target.is_file() or (name not in replace and target.read_bytes() != data)):
            raise ValueError(f'Publication would overwrite an existing output: {name}')
    for name, data in outputs.items():
        target = _contained(destination, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return tuple(outputs)
