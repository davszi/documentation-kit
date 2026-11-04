"""Optional exact-byte evidence collections declared by a consumer project.

Site configuration may name evidence_manifests = ["docs/project/evidence-locations.json"].
No platform-specific collection is required by the shared kit.
"""
import hashlib
import os
from pathlib import Path
import re
import tomllib

ROOT = Path(os.environ.get('DOCSITE_PROJECT_ROOT', Path.cwd())).resolve()
_config = ROOT / 'docs/site/site.toml'
MANIFESTS = tuple(tomllib.loads(_config.read_text()).get('evidence_manifests', [])) if _config.is_file() else ()


def safe_path(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError(f'Invalid evidence path: {value!r}')
    path = root / value
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError(f'Evidence path escapes the project: {value}')
    return path


def manifest_documents(root=ROOT, *, require_all_manifests=False):
    import json
    root = Path(root).resolve()
    entries, revisions, original_paths, destinations = [], {}, set(), set()
    for relative in MANIFESTS:
        path = safe_path(root, relative)
        if not path.is_file():
            if require_all_manifests:
                raise ValueError(f'Missing declared evidence manifest: {relative}')
            continue
        manifest = json.loads(path.read_text())
        revision = manifest.get('source_revision', '')
        if manifest.get('schema_version') != 1 or not re.fullmatch(r'[0-9a-f]{40}', revision):
            raise ValueError(f'Invalid evidence manifest: {relative}')
        documents = manifest.get('documents')
        if not isinstance(documents, list) or not documents:
            raise ValueError(f'Evidence manifest has no documents: {relative}')
        revisions[relative] = revision
        for item in documents:
            if not isinstance(item, dict):
                raise ValueError(f'Invalid evidence item: {relative}')
            for field in ('path', 'original_path'):
                safe_path(root, item.get(field))
            effective = item.get('source_revision', revision)
            if not re.fullmatch(r'[0-9a-f]{40}', effective):
                raise ValueError('Invalid evidence source revision')
            if item['original_path'] in original_paths or item['path'] in destinations:
                raise ValueError('Duplicate evidence original or destination')
            original_paths.add(item['original_path'])
            destinations.add(item['path'])
            entries.append(dict(item, source_revision=effective))
    return entries, revisions


def verify(root=ROOT, *, require_all_manifests=False):
    root = Path(root).resolve()
    rows, revisions = manifest_documents(root, require_all_manifests=require_all_manifests)
    for row in rows:
        path = safe_path(root, row['path'])
        data = path.read_bytes()
        if type(row.get('bytes')) is not int or row['bytes'] != len(data) or row.get('sha256') != hashlib.sha256(data).hexdigest():
            raise ValueError(f'Evidence identity mismatch: {row["path"]}')
    return rows, revisions
