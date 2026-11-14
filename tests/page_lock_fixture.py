"""Disposable project and vectors for the page-lock tests.

``make_project`` writes a starter project with both lock levels: a topic page
with the chapter reader, a page with tabs, plot toggles, a lightbox image and
an embedded HTML frame, a registered Reference page and an exported Markdown
file. Each carries a marker string that must never appear in a locked bundle.

Run as a script for the Node tests:

    python tests/page_lock_fixture.py publish <project> <out>   # passwords from the environment
    python tests/page_lock_fixture.py vectors                   # sealed vectors as JSON on stdout
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import subprocess
import sys

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / 'tooling'))

MARKERS = {
    'topic': 'TOPIC-MARKER-5e1f0c',
    'widgets': 'WIDGETS-MARKER-7d20b9',
    'frame': 'FRAME-MARKER-c41a83',
    'reference': 'REFERENCE-MARKER-a93d27',
    'markdown': 'MARKDOWN-MARKER-0b6e44',
}

GUIDE_CHAPTER = f'''
<section class="card" id="locked-detail">

## Locked detail

The topic marker {MARKERS['topic']} is in this chapter. Read [the rule](rule.html#rule-detail).

</section>
'''

WIDGETS = f'''+++
title = "Widgets after unlock"
toc = []
reader = false
components = ["toc", "nav", "tabs", "plot-toggles", "lightbox"]
page_only = "Fixture page for the page-lock browser test."
+++

# Widgets after unlock

The widgets marker {MARKERS['widgets']} is on this page. Open [the record](../../notes/record.md).

<svg class="inline-fig" viewBox="0 0 120 60" role="img" aria-label="Two lines">
<path id="tg-alpha--0" d="M0 15 L120 15" stroke="#f0883e" stroke-width="4"/>
<path id="tg-beta--0" d="M0 45 L120 45" stroke="#58a6ff" stroke-width="4"/>
</svg>

![A dot](../../media/dot.svg)

<iframe title="Embedded frame" src="../../media/frame.html" width="320" height="80"></iframe>

<!-- tab: First -->

First tab text.

<!-- tab: Second -->

## Second detail

Second tab text.

<div style="height:2400px"></div>

## Far heading

The far heading closes the page.
'''

RULE = f'''# Shared rule

The reference marker {MARKERS['reference']} is on this page.

## Rule detail

Read [the record](../notes/record.md).
'''

RECORD = f'''# Record

The Markdown marker {MARKERS['markdown']} is in this file.
'''

FRAME = f'<!doctype html><html lang="en"><meta charset="utf-8"><title>Frame</title><p>{MARKERS["frame"]}</p></html>\n'
DOT = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="160" height="160">'
       '<circle cx="20" cy="20" r="16" fill="#39d2c0"/></svg>\n')


def docsite(*args: object, env: dict | None = None) -> subprocess.CompletedProcess:
    # A CI run sets GITHUB_SHA, which pins source links; the fixture keeps branch links.
    environment = {name: value for name, value in (env or os.environ).items() if name != 'GITHUB_SHA'}
    return subprocess.run([sys.executable, str(KIT / 'docsite.py'), *map(str, args)],
                          capture_output=True, text=True, env=environment)


def make_project(root: Path, *, lock: bool | None = True) -> Path:
    """Write and track the fixture; ``lock=None`` leaves the key out of site.toml."""
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    created = docsite('init', root, '--title', 'Lock fixture', '--repository', '')
    if created.returncode:
        raise RuntimeError(created.stderr)

    def write(name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    guide = root / 'docs/topics/guide/index.md'
    guide.write_text(guide.read_text() + GUIDE_CHAPTER)
    write('docs/topics/widgets/index.md', WIDGETS)
    write('policy/rule.md', RULE)
    write('notes/record.md', RECORD)
    write('media/frame.html', FRAME)
    write('media/dot.svg', DOT)
    write('docs/site/public.json', json.dumps({'files': ['notes/record.md']}) + '\n')
    config = root / 'docs/site/site.toml'
    config.write_text(config.read_text() + '''
[[nav]]
label = "Widgets"
file = "widgets.html"
group = "guide"

[[source_pages]]
source = "policy/rule.md"
slug = "rule"
description = "A rule kept as Markdown."

[publication]
assets_manifest = "docs/site/public.json"
pages = ["index.html", "guide.html", "widgets.html", "rule.html"]
''' + ('' if lock is None else f'lock = {"true" if lock else "false"}\n'))
    subprocess.run(['git', 'add', '-A'], cwd=root, check=True)
    return root


def vectors() -> dict:
    """Sealed files and wrapped keys at the real iteration count, for the WebCrypto cross-check."""
    import page_lock
    passwords = page_lock.read_passwords(os.environ)
    keyring = page_lock.make_keyring(passwords)
    files = []
    for path, level, text in (('guide.html', 1, '<p>Topic ünïcode ✓</p>'), ('rule.html', 2, '<p>Reference</p>'),
                              ('notes/record.md', 2, RECORD)):
        data = text.encode('utf-8')
        entry = {'path': path, 'level': level, 'plain': base64.b64encode(data).decode()}
        if path.endswith('.md'):
            entry['envelope'] = page_lock.lock_text(path, level, data, keyring).decode()
        else:
            entry['sealed'] = base64.b64encode(page_lock.seal(keyring.content[level], data,
                                                              page_lock.file_context(path))).decode()
        files.append(entry)
    return {'header': keyring.header, 'files': files}


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'publish' and len(sys.argv) == 4:
        project = make_project(Path(sys.argv[2]))
        result = docsite('publish', '--project', project, '--out', sys.argv[3])
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    if command == 'vectors':
        json.dump(vectors(), sys.stdout)
        raise SystemExit(0)
    raise SystemExit(__doc__)
