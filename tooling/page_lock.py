"""Opt-in page lock: store the text of a published bundle encrypted.

``publish`` calls ``prepare_lock`` before it builds, so a missing dependency or
an unusable password fails fast, and ``PageLock.apply`` on the finished bundle
before the bundle moves into place. A project turns the lock on with
``lock = true`` in the ``[publication]`` table of ``docs/site/site.toml``; the
two passwords come only from the environment variables in
``PASSWORD_VARIABLES``. Local ``build`` output is never encrypted.

Key layout:

- the salt is PBKDF2-HMAC-SHA-256 of both passwords, so it stays the same from
  publish to publish and changes when either password changes;
- PBKDF2-HMAC-SHA-256 with ``ITERATIONS`` and that salt derives one
  key-encryption key from each password; a reader who asks to be remembered
  keeps that key, which therefore opens later publishes until a password
  changes;
- every publish draws a random 256-bit content key for level 1 (topic pages
  and every other page) and for level 2 (Reference pages, the Reference tree
  and exported Markdown); the general password's slot holds the level-1 key,
  the reference password's slot holds both;
- every locked file is sealed with AES-256-GCM under its level's key, with a
  fresh random 96-bit nonce and its public bundle path as associated data.

Level-1 pages lose their sidebar Reference section before they are sealed.
The section and the folder tree go into ``reference.tree.js``, sealed at level
2 and padded, which the browser loads for a reference-password reader and puts
back where the section was. The Reference index page is padded to the same
size. HTML without the kit's sidebar that only Reference pages embed or link
is level 2 as well. Every page is sealed with ``pad``; the root ``404.html``
opens at any address. The browser side is ``theme/components/page-lock.js``;
it uses WebCrypto with the same parameters. Passwords never enter output,
logs or error messages.
"""
from __future__ import annotations

import base64
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import html
import json
import os
from pathlib import Path, PurePath
import posixpath
import re
import secrets
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from chapter_layout import Structure
from source_tree import TREE_GLOBAL, TREE_SCRIPT

FORMAT = 'docsite-lock/1'
# OWASP Password Storage Cheat Sheet: 600,000 iterations for PBKDF2-HMAC-SHA256.
ITERATIONS = 600_000
SALT_BYTES = 16
SALT_CONTEXT = f'{FORMAT} salt'.encode('ascii')
KEY_BYTES = 32
NONCE_BYTES = 12
# Length is the only property a check can see; it cannot measure randomness.
PASSWORD_VARIABLES = {1: 'DOCSITE_GENERAL_PASSWORD', 2: 'DOCSITE_REFERENCE_PASSWORD'}
HTML_SUFFIXES = ('.html', '.htm')
# The unlock writes the page with document.write, which an XML document does
# not have, and a server-side-include page may not be served as HTML.
REFUSED_SUFFIXES = ('.xhtml', '.xht', '.shtml', '.shtm')
MARKDOWN_SUFFIXES = ('.md', '.markdown')
LOCK_ASSETS = {'assets/page-lock.js': 'page-lock.js', 'assets/page-lock.css': 'page-lock.css'}
# Body classes of pages that only the reference password opens.
REFERENCE_CLASSES = {b'source-page', b'reference-index-page'}
LOCKED_TREE_GLOBAL = 'docsLockedReferenceTree'
# The sealed tree and the Reference index page are padded to the same power
# of two of at least this size, so their lengths show little about how many
# files the Reference section holds.
TREE_PADDING = 1 << 16
# GitHub Pages serves this page at every missing address.
NOT_FOUND = '404.html'
INSTALL_HINT = ('python -m pip install -r .docs-kit/requirements-lock.txt '
                '(requirements-lock.txt in the kit itself)')
TEXT_NOTICE = ('This file is locked. Open it from a page of the documentation site '
               'after entering the password.')
_COMPONENTS = Path(__file__).resolve().parent.parent / 'theme/components'
_BODY = re.compile(rb'<body\b([^>]*)>', re.I)
_CLASS = re.compile(rb'''(?:^|\s)class\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.I)
# Addresses a page embeds or links: frames, objects, embeds, images and links.
_TARGET = re.compile(r'''\s(?:src|href|data)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.I)
# Anything in a page that may be an address or a path, in attributes or text.
_TOKEN = re.compile(r'''[^\s"'<>()\[\]{}|\\^`]+''')
_SOURCE_HOST_PATH = re.compile(r'/(?:blob|tree)/[^/]+/(.+)$')
# Any tag that still carries Reference markup, whatever the attribute order: a
# repo-tree class or id, or a data-repo-tree attribute.
_TREE_TAG = re.compile(r'''<[A-Za-z][^>]*(?:\b(?:class|id)\s*=\s*["']?[^"'>]*\brepo-tree|\bdata-repo-tree)''')
# The shared shell opens the sidebar with this element; build.py fills it.
_SIDEBAR = '<nav class="sidebar" id="sidebar">'
_KIT_PAGE = 'id="sidebar"'


def _aesgcm():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        raise ValueError('The page lock needs the Python package cryptography, which is not installed. '
                         'Install the pinned version: ' + INSTALL_HINT) from None
    return AESGCM


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')


def lock_requested(options: Mapping) -> bool:
    value = options.get('lock', False)
    if not isinstance(value, bool):
        raise ValueError('[publication] lock must be true or false')
    return value


def read_passwords(environ: Mapping[str, str]) -> dict[int, str]:
    """Return the NFC-normalized passwords by level; never echo a value."""
    passwords = {}
    for level, name in PASSWORD_VARIABLES.items():
        value = environ.get(name, '')
        if not value:
            raise ValueError(f'The page lock is on ([publication] lock = true), but {name} is not set. '
                             'Set it from a secret in the environment that runs publish.')
        value = unicodedata.normalize('NFC', value)
        # No rule on length or characters: the owner chooses the password. A stray
        # newline from a secret would lock every reader out, so that case gets a note.
        if value != value.strip() or not value.isprintable():
            print(f'note: {name} starts or ends with whitespace or holds a control or invisible character; '
                  'a reader may be unable to type it.', file=sys.stderr)
        passwords[level] = value
    if passwords[1] == passwords[2]:
        raise ValueError(f'{PASSWORD_VARIABLES[1]} and {PASSWORD_VARIABLES[2]} are equal; '
                         'the reference password must differ from the general password.')
    return passwords


def derive_key(password: str, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    """PBKDF2-HMAC-SHA-256 over the NFC-normalized UTF-8 password; WebCrypto derives the same bits."""
    return hashlib.pbkdf2_hmac('sha256', unicodedata.normalize('NFC', password).encode('utf-8'),
                               salt, iterations, KEY_BYTES)


def derive_salt(passwords: Mapping[int, str], iterations: int = ITERATIONS) -> bytes:
    """The salt of both password keys: unchanged while both passwords stay, new when either changes.

    It is a PBKDF2 value of the two passwords, so it is as slow to test a guess
    against as a key slot, and it lets a remembered key open later publishes.
    """
    joined = '\n'.join(unicodedata.normalize('NFC', passwords[level]) for level in (1, 2))
    return hashlib.pbkdf2_hmac('sha256', joined.encode('utf-8'), SALT_CONTEXT, iterations, SALT_BYTES)


def seal(key: bytes, plaintext: bytes, associated: bytes, *, nonce: bytes | None = None) -> bytes:
    """AES-256-GCM: nonce, then ciphertext with its 16-byte tag."""
    nonce = secrets.token_bytes(NONCE_BYTES) if nonce is None else nonce
    if len(key) != KEY_BYTES or len(nonce) != NONCE_BYTES:
        raise ValueError('The page lock needs a 256-bit key and a 96-bit nonce')
    return nonce + _aesgcm()(key).encrypt(nonce, plaintext, associated)


def unseal(key: bytes, sealed: bytes, associated: bytes) -> bytes:
    """Reverse ``seal``; raises ``cryptography.exceptions.InvalidTag`` on any change."""
    return _aesgcm()(key).decrypt(sealed[:NONCE_BYTES], sealed[NONCE_BYTES:], associated)


def file_context(path: str) -> bytes:
    return f'{FORMAT} file {path}'.encode('utf-8')


def slots_context(lock_id: str) -> bytes:
    return f'{FORMAT} keys {lock_id}'.encode('utf-8')


@dataclass(frozen=True)
class Keyring:
    content: dict[int, bytes]   # level -> content key; secret
    header: dict                # public: format, id, KDF parameters, wrapped keys


def make_keyring(passwords: Mapping[int, str], *, iterations: int = ITERATIONS) -> Keyring:
    salt = derive_salt(passwords, iterations)
    lock_id = base64.urlsafe_b64encode(secrets.token_bytes(12)).decode('ascii')
    content = {1: secrets.token_bytes(KEY_BYTES), 2: secrets.token_bytes(KEY_BYTES)}
    context = slots_context(lock_id)
    # A slot opens with one password and holds its level byte and every key it may use.
    slots = [_b64(seal(derive_key(passwords[1], salt, iterations), bytes([1]) + content[1], context)),
             _b64(seal(derive_key(passwords[2], salt, iterations), bytes([2]) + content[1] + content[2], context))]
    header = {'format': FORMAT, 'id': lock_id,
              'kdf': {'name': 'PBKDF2', 'hash': 'SHA-256', 'iterations': iterations, 'salt': _b64(salt)},
              'slots': slots}
    return Keyring(content, header)


def open_slots(header: Mapping, wrapping: bytes) -> tuple[int, dict[int, bytes]] | None:
    """The level and content keys a password key opens, or None; a remembered key takes this path."""
    from cryptography.exceptions import InvalidTag
    for slot in header['slots']:
        try:
            plain = unseal(wrapping, base64.b64decode(slot), slots_context(header['id']))
        except InvalidTag:
            continue
        level = plain[0]
        return level, {n: plain[1 + (n - 1) * KEY_BYTES:1 + n * KEY_BYTES] for n in range(1, level + 1)}
    return None


def open_keyring(header: Mapping, password: str) -> tuple[int, dict[int, bytes]] | None:
    """What the browser does: the level and content keys a password opens, or None."""
    kdf = header['kdf']
    return open_slots(header, derive_key(password, base64.b64decode(kdf['salt']), kdf['iterations']))


def is_reference_page(markup: bytes) -> bool:
    """The build marks Reference pages and the Reference index by their body class."""
    body = _BODY.search(markup)
    if not body:
        return False
    match = _CLASS.search(body[1])
    classes = next(group for group in match.groups() if group is not None).split() if match else []
    return bool(REFERENCE_CLASSES.intersection(classes))


def split_reference(markup: str, name: str) -> tuple[str, str | None, int | None]:
    """Remove the sidebar's Reference section from a page.

    Returns the page without it, the section with its leading line break, and
    the offset where it was; ``stripped[:at] + section + stripped[at:]`` is the
    page. A page without a section still gets the offset where one would go,
    so the offset says nothing about the Reference section. A page without the
    shared sidebar returns no offset.
    """
    start = markup.find(_SIDEBAR)
    if start < 0:
        return markup, None, None
    end = markup.find('</nav>', start)
    if end < 0:
        raise ValueError(f'The page lock cannot find the end of the sidebar in {name}')
    try:
        nodes = [node for top in Structure(markup[start:end + len('</nav>')]).roots for node in top.descendants()]
    except ValueError as problem:
        raise ValueError(f'The page lock cannot read the sidebar of {name}: {problem}') from None
    toc = next((node for node in nodes if node.tag == 'div' and node.attrs.get('id') == 'toc'), None)
    trees = [node for node in nodes if node.tag == 'div' and 'repo-tree' in (node.attrs.get('class') or '').split()]
    if toc is None or len(trees) > 1:
        raise ValueError(f'The page lock expects one sidebar list and at most one Reference section in {name}')
    if not trees:
        at = start + toc.closing_start
        while markup[at - 1] in ' \t\n':
            at -= 1
        return markup, None, at
    # The section starts on its own indented line: cut from the line break before it.
    at, until = start + trees[0].start, start + trees[0].end
    while markup[at - 1] == ' ':
        at -= 1
    at -= 1
    if markup[at] != '\n':
        raise ValueError(f'The page lock cannot cut the Reference section out of {name}')
    stripped = markup[:at] + markup[until:]
    if 'class="repo-tree' in stripped:
        raise ValueError(f'Reference markup remains in {name} outside the sidebar section')
    return stripped, markup[at:until], at


def tree_markup(data: bytes) -> str:
    """The folder tree that build.py wrote into ``TREE_SCRIPT``."""
    prefix, suffix = f'window.{TREE_GLOBAL} = ', ';\n'
    text = data.decode('utf-8')
    if not (text.startswith(prefix) and text.endswith(suffix)):
        raise ValueError(f'The page lock cannot read {TREE_SCRIPT}')
    markup = json.loads(text[len(prefix):-len(suffix)])
    if not isinstance(markup, str):
        raise ValueError(f'The page lock cannot read {TREE_SCRIPT}')
    return markup


def padded_size(length: int) -> int:
    """The smallest power of two of at least ``TREE_PADDING`` that holds ``length`` bytes."""
    return max(TREE_PADDING, 1 << (length - 1).bit_length())


def tree_payload(tree: str | None, section: str | None) -> bytes:
    return json.dumps({'section': section, 'tree': tree}, sort_keys=True, separators=(',', ':')).encode('utf-8')


def lock_tree(tree: str | None, section: str | None, keyring: Keyring, size: int | None = None) -> bytes:
    """``TREE_SCRIPT`` as a script that hands the sealed, padded tree and section to page-lock.js.

    JSON ignores the trailing spaces that pad it to ``size`` bytes.
    """
    data = tree_payload(tree, section)
    size = padded_size(len(data)) if size is None else size
    if size < len(data):
        raise ValueError(f'The page lock cannot pad {TREE_SCRIPT} to {size} bytes')
    sealed = seal(keyring.content[2], data + b' ' * (size - len(data)), file_context(TREE_SCRIPT))
    return (f'// Locked: only the reference password opens this file.\n'
            f'window.{LOCKED_TREE_GLOBAL} = "{_b64(sealed)}";\n').encode('ascii')


def pad(data: bytes, size: int | None = None) -> bytes:
    """A page sealed as itself, one 0x80 byte and zero bytes up to ``size``; ``unpad`` removes them."""
    size = len(data) + 1 if size is None else size
    if size <= len(data):
        raise ValueError('The page lock cannot pad a page into fewer bytes than it has')
    return data + b'\x80' + bytes(size - len(data) - 1)


def unpad(data: bytes) -> bytes:
    end = len(data.rstrip(b'\x00'))
    if not end or data[end - 1] != 0x80:
        raise ValueError('Malformed page padding')
    return data[:end - 1]


def _utf8(name: str, data: bytes) -> str:
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError(f'The page lock reads text as UTF-8, and {name} is not UTF-8') from None


def lock_text(name: str, level: int, data: bytes, keyring: Keyring) -> bytes:
    """A readable notice, a marker line and the sealed file in base64."""
    _utf8(name, data)
    sealed = seal(keyring.content[level], data, file_context(name))
    return f'{TEXT_NOTICE}\n{FORMAT} level {level}\n{_b64(sealed)}\n'.encode('ascii')


def lock_page(name: str, level: int, data: bytes, keyring: Keyring, versions: Mapping[str, str],
              section_at: int | None = None, *, size: int | None = None) -> bytes:
    """The lock page served at ``name`` instead of the page itself.

    ``section_at`` is the byte offset in ``data`` where a reference-password
    reader's browser puts the sidebar's Reference section back. The page is
    sealed padded (``pad``), to ``size`` bytes when given. The site's root
    ``404.html`` opens at any address, because the host serves it at every
    missing one.
    """
    _utf8(name, data)
    sealed = seal(keyring.content[level], pad(data, size), file_context(name))
    up = posixpath.relpath('.', posixpath.dirname(name) or '.')
    prefix = '' if up == '.' else up + '/'

    def asset(target):
        return html.escape(prefix + target + ('?v=' + versions[target] if target in versions else ''), quote=True)

    base = (f'<link rel="stylesheet" href="{asset("assets/base.css")}">\n'
            if 'assets/base.css' in versions else '')
    header = json.dumps(keyring.header, sort_keys=True, separators=(',', ':')).replace('<', '\\u003c')
    values = {'{{ROOT}}': html.escape(prefix or './', quote=True), '{{LEVEL}}': str(level),
              '{{ATTRIBUTES}}': ('' if section_at is None else f' data-section-at="{section_at}"')
                                + (' data-not-found' if name == NOT_FOUND else ''),
              '{{BASE_CSS}}': base, '{{LOCK_CSS}}': asset('assets/page-lock.css'),
              '{{LOCK_JS}}': asset('assets/page-lock.js'), '{{KEYS}}': header, '{{DATA}}': _b64(sealed)}
    text = (_COMPONENTS / 'page-lock.html').read_text()
    return re.sub(r'\{\{[A-Z_]+\}\}', lambda match: values[match[0]], text).encode('utf-8')


def _addresses(markup: str, name: str) -> set[str]:
    """Bundle paths a page embeds or links through its src, href or data attributes.

    Values may be quoted or not. A root-relative path counts from the bundle's
    root and, for a site served below a folder, also without its first folder.
    """
    found = set()
    for match in _TARGET.finditer(markup):
        try:
            url = urlsplit(html.unescape(next(value for value in match.groups() if value is not None)))
        except ValueError:
            continue
        if url.scheme or url.netloc or not url.path:
            continue
        path = unquote(url.path)
        if path.startswith('/'):
            rooted = posixpath.normpath(path.lstrip('/'))
            found.update({rooted, rooted.partition('/')[2]} - {''})
        else:
            found.add(posixpath.normpath(posixpath.join(posixpath.dirname(name), path)))
    return found


def reference_names(built: Mapping, markdown: set[str]) -> dict[str, str]:
    """Each name a page can use for a Reference file, mapped to the file's repository path.

    A Reference page has its route and its repository path; a locked Markdown
    file has its bundle path, which is its repository path.
    """
    names = {}
    for route, source in built.get('source_pages', {}).items():
        names[route] = names[source] = source
    for path in markdown:
        names[path] = path
    return names


def named_references(markup: str, name: str, names: Mapping[str, str]) -> set[str]:
    """The Reference files a page names anywhere: in any attribute or in its text.

    Every token that may be an address or a path is decoded and compared with
    every name: as written, resolved from the page's folder, resolved from the
    site root, and, on a source host, the repository path after
    ``/blob/<ref>/`` or ``/tree/<ref>/``. No attribute name is relied on, so a
    source link counts whatever marks it.
    """
    found = set()
    for token in _TOKEN.findall(html.unescape(markup)):
        try:
            url = urlsplit(token)
        except ValueError:
            continue
        path = unquote(url.path).rstrip('.,;:!')
        if url.netloc:
            match = _SOURCE_HOST_PATH.search(path)
            candidates = [match[1]] if match else []
        else:
            joined = posixpath.normpath(posixpath.join(posixpath.dirname(name), path)) if path else ''
            candidates = [path, joined, re.sub(r'^(?:\.\./)+', '', joined)]
        found.update(names[candidate] for candidate in candidates if candidate in names)
    return found


def html_levels(texts: Mapping[str, str], reference: set[str]) -> dict[str, int]:
    """The level of each HTML file.

    Reference pages (``reference``, or a Reference body class) need the
    reference password. HTML without the kit's sidebar, such as a frame or an
    exported HTML file, needs it too when only such pages embed or link it;
    one that a general page uses, or that no page uses, opens with the general
    password, like every other page.
    """
    levels = {name: 2 if name in reference or is_reference_page(text.encode('utf-8')) else 1
              for name, text in texts.items()}
    others = {name for name, text in texts.items() if levels[name] == 1 and _KIT_PAGE not in text}
    users = {name: set() for name in others}
    for name, text in texts.items():
        for target in _addresses(text, name) & others - {name}:
            users[target].add(name)
    for name in others:
        if users[name]:
            levels[name] = 2
    changed = True
    while changed:
        changed = False
        for name in others:
            if levels[name] == 2 and any(levels[user] == 1 for user in users[name]):
                levels[name], changed = 1, True
    return levels


def _counts(counter: Counter) -> str:
    return ', '.join(f'{suffix} {count}' for suffix, count in sorted(counter.items())) or 'none'


@dataclass(frozen=True)
class PageLock:
    passwords: dict[int, str]
    iterations: int = ITERATIONS

    def __repr__(self) -> str:  # never show the passwords, even in a traceback
        return f'PageLock(iterations={self.iterations})'

    def apply(self, bundle: Path, built: Mapping) -> str:
        """Lock every HTML page, Markdown file and the Reference tree of ``bundle`` in place.

        ``built`` is the build's ``site-build.json``: its ``source_pages`` and
        ``reference_tree`` name what only the reference password opens.
        Returns the summary.
        """
        bundle = Path(bundle)
        for target in LOCK_ASSETS:
            if (bundle / target).exists():
                raise ValueError(f'The page lock adds {target}, which the bundle already holds')
        shared = built.get('reference_tree') or {}
        script = shared.get('script', '').removeprefix('html/') or None
        if (bundle / TREE_SCRIPT).exists() != (script == TREE_SCRIPT):
            raise ValueError(f'The page lock writes {TREE_SCRIPT}, which the bundle holds without the build')
        index = shared.get('index', '').removeprefix('html/')
        reference = set(built.get('source_pages', {})) | {index} - {''}
        keyring = make_keyring(self.passwords, iterations=self.iterations)
        files = {path.relative_to(bundle).as_posix(): path for path in sorted(bundle.rglob('*'))
                 if path.is_file() or path.is_symlink()}
        assets = {target: (_COMPONENTS / source).read_bytes() for target, source in LOCK_ASSETS.items()}
        versions = {target: hashlib.sha256(data).hexdigest()[:10] for target, data in assets.items()}
        if 'assets/base.css' in files:
            versions['assets/base.css'] = hashlib.sha256(files['assets/base.css'].read_bytes()).hexdigest()[:10]

        texts = {}
        for name, path in files.items():
            if path.is_symlink():
                raise ValueError(f'The page lock cannot follow a symlink: {name}')
            if name.lower().endswith(REFUSED_SUFFIXES):
                raise ValueError(f'The page lock cannot lock {name}: it unlocks pages that browsers read as HTML. '
                                 'Rename it to .html or leave it out of the bundle.')
            if name.lower().endswith(HTML_SUFFIXES):
                texts[name] = _utf8(name, path.read_bytes())
        levels = html_levels(texts, reference)
        markdown = {name for name in files if name.lower().endswith(MARKDOWN_SUFFIXES)}
        names = reference_names(built, markdown)
        pages: dict[str, tuple[int, bytes, int | None]] = {}
        sections, named = set(), set()
        for name, text in texts.items():
            if levels[name] == 2:
                pages[name] = (2, text.encode('utf-8'), None)
                continue
            stripped, section, at = split_reference(text, name)
            # Fail closed: a changed shell must not leave the tree in a general page.
            if _TREE_TAG.search(stripped):
                raise ValueError(f'The page lock found Reference markup in {name}, which the general password opens')
            if section is not None:
                sections.add(section)
            named |= named_references(stripped, name, names)
            pages[name] = (1, stripped.encode('utf-8'), None if at is None else len(stripped[:at].encode('utf-8')))
        if len(sections) > 1:
            raise ValueError('The page lock found different Reference sections on pages outside the Reference')
        tree = tree_markup(files[TREE_SCRIPT].read_bytes()) if script else None
        section = next(iter(sections), None)
        # The Reference index lists the whole tree: it gets the tree file's padded size.
        size = padded_size(max(len(tree_payload(tree, section)), len(pages[index][1]) + 1 if index in pages else 0))
        envelope = lock_tree(tree, section, keyring, size)
        keyring.header['tree'] = hashlib.sha256(envelope).hexdigest()[:10]

        locked = {1: Counter(), 2: Counter()}
        readable = Counter()
        for name, path in files.items():
            suffix = PurePath(name).suffix.lower() or '(no suffix)'
            if name in pages:
                level, data, at = pages[name]
                path.write_bytes(lock_page(name, level, data, keyring, versions, at,
                                           size=size if name == index else None))
                locked[level][suffix] += 1
            elif name.lower().endswith(MARKDOWN_SUFFIXES):
                path.write_bytes(lock_text(name, 2, path.read_bytes(), keyring))
                locked[2][suffix] += 1
            elif name != TREE_SCRIPT:
                readable[suffix] += 1
        (bundle / TREE_SCRIPT).write_bytes(envelope)
        locked[2]['.js'] += 1
        for target, data in assets.items():
            (bundle / target).parent.mkdir(parents=True, exist_ok=True)
            (bundle / target).write_bytes(data)
            readable[PurePath(target).suffix] += 1
        lines = [f'Page lock: the general password opens {sum(locked[1].values())} files ({_counts(locked[1])}); '
                 f'only the reference password opens {sum(locked[2].values())} more ({_counts(locked[2])}).',
                 f'Page lock: {sum(readable.values())} files stay readable without a password '
                 f'({_counts(readable)}).']
        if named:
            lines.append(f'Page lock: pages the general password opens name {len(named)} Reference '
                         f'file{"" if len(named) == 1 else "s"} (links, source links or text); '
                         'general-password readers see those names.')
        return '\n'.join(lines)


def prepare_lock(options: Mapping, environ: Mapping[str, str] | None = None) -> PageLock | None:
    """Return the lock for ``[publication]`` options, or None when it is off.

    Checks the dependency and both passwords before anything is built.
    """
    if not lock_requested(options):
        return None
    _aesgcm()
    return PageLock(read_passwords(os.environ if environ is None else environ))
