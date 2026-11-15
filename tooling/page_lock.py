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
back where the section was. The browser side is
``theme/components/page-lock.js``; it uses WebCrypto with the same parameters.
Passwords never enter output, logs or error messages.
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
MIN_PASSWORD_LENGTH = 20
PASSWORD_VARIABLES = {1: 'DOCSITE_GENERAL_PASSWORD', 2: 'DOCSITE_REFERENCE_PASSWORD'}
HTML_SUFFIXES = ('.html', '.htm')
MARKDOWN_SUFFIXES = ('.md', '.markdown')
LOCK_ASSETS = {'assets/page-lock.js': 'page-lock.js', 'assets/page-lock.css': 'page-lock.css'}
# Body classes of pages that only the reference password opens.
REFERENCE_CLASSES = {b'source-page', b'reference-index-page'}
LOCKED_TREE_GLOBAL = 'docsLockedReferenceTree'
# The sealed tree is padded to a power of two of at least this size, so its
# length shows little about how many files the Reference section holds.
TREE_PADDING = 1 << 16
INSTALL_HINT = ('python -m pip install -r .docs-kit/requirements-lock.txt '
                '(requirements-lock.txt in the kit itself)')
TEXT_NOTICE = ('This file is locked. Open it from a page of the documentation site '
               'after entering the password.')
_COMPONENTS = Path(__file__).resolve().parent.parent / 'theme/components'
_BODY = re.compile(rb'<body\b([^>]*)>', re.I)
_CLASS = re.compile(rb'''(?:^|\s)class\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.I)
_HREF = re.compile(r'''\shref\s*=\s*(?:"([^"]*)"|'([^']*)')''', re.I)
# The shared shell opens the sidebar with this element; build.py fills it.
_SIDEBAR = '<nav class="sidebar" id="sidebar">'


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
        if value != value.strip() or not value.isprintable():
            raise ValueError(f'{name} starts or ends with whitespace or holds a control or invisible '
                             'character; readers could not type it reliably.')
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(f'{name} is shorter than {MIN_PASSWORD_LENGTH} characters. '
                             'Use a long random passphrase: anyone can test guesses offline.')
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


def lock_tree(tree: str | None, section: str | None, keyring: Keyring) -> bytes:
    """``TREE_SCRIPT`` as a script that hands the sealed, padded tree and section to page-lock.js."""
    data = json.dumps({'section': section, 'tree': tree}, sort_keys=True, separators=(',', ':')).encode('utf-8')
    size = max(TREE_PADDING, 1 << (len(data) - 1).bit_length())
    sealed = seal(keyring.content[2], data + b' ' * (size - len(data)), file_context(TREE_SCRIPT))
    return (f'// Locked: only the reference password opens this file.\n'
            f'window.{LOCKED_TREE_GLOBAL} = "{_b64(sealed)}";\n').encode('ascii')


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
              section_at: int | None = None) -> bytes:
    """The lock page served at ``name`` instead of the page itself.

    ``section_at`` is the byte offset in ``data`` where a reference-password
    reader's browser puts the sidebar's Reference section back.
    """
    _utf8(name, data)
    sealed = seal(keyring.content[level], data, file_context(name))
    up = posixpath.relpath('.', posixpath.dirname(name) or '.')
    prefix = '' if up == '.' else up + '/'

    def asset(target):
        return html.escape(prefix + target + ('?v=' + versions[target] if target in versions else ''), quote=True)

    base = (f'<link rel="stylesheet" href="{asset("assets/base.css")}">\n'
            if 'assets/base.css' in versions else '')
    header = json.dumps(keyring.header, sort_keys=True, separators=(',', ':')).replace('<', '\\u003c')
    values = {'{{ROOT}}': html.escape(prefix or './', quote=True), '{{LEVEL}}': str(level),
              '{{SECTION_AT}}': '' if section_at is None else f' data-section-at="{section_at}"',
              '{{BASE_CSS}}': base, '{{LOCK_CSS}}': asset('assets/page-lock.css'),
              '{{LOCK_JS}}': asset('assets/page-lock.js'), '{{KEYS}}': header, '{{DATA}}': _b64(sealed)}
    text = (_COMPONENTS / 'page-lock.html').read_text()
    return re.sub(r'\{\{[A-Z_]+\}\}', lambda match: values[match[0]], text).encode('utf-8')


def _linked(markup: str, name: str, routes: set[str]) -> set[str]:
    """Reference routes that a page links by address."""
    found = set()
    for match in _HREF.finditer(markup):
        url = urlsplit(html.unescape(match[1] if match[1] is not None else match[2]))
        if url.scheme or url.netloc or not url.path:
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
        if target in routes:
            found.add(target)
    return found


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
        reference = set(built.get('source_pages', {})) | {shared.get('index', '').removeprefix('html/')} - {''}
        keyring = make_keyring(self.passwords, iterations=self.iterations)
        files = {path.relative_to(bundle).as_posix(): path for path in sorted(bundle.rglob('*'))
                 if path.is_file() or path.is_symlink()}
        assets = {target: (_COMPONENTS / source).read_bytes() for target, source in LOCK_ASSETS.items()}
        versions = {target: hashlib.sha256(data).hexdigest()[:10] for target, data in assets.items()}
        if 'assets/base.css' in files:
            versions['assets/base.css'] = hashlib.sha256(files['assets/base.css'].read_bytes()).hexdigest()[:10]

        pages: dict[str, tuple[int, bytes, int | None]] = {}
        sections, linked = set(), set()
        for name, path in files.items():
            if path.is_symlink():
                raise ValueError(f'The page lock cannot follow a symlink: {name}')
            if not name.lower().endswith(HTML_SUFFIXES):
                continue
            data = path.read_bytes()
            text = _utf8(name, data)
            if name in reference or is_reference_page(data):
                pages[name] = (2, data, None)
                continue
            stripped, section, at = split_reference(text, name)
            if section is not None:
                sections.add(section)
            linked |= _linked(stripped, name, reference)
            pages[name] = (1, stripped.encode('utf-8'), None if at is None else len(stripped[:at].encode('utf-8')))
        if len(sections) > 1:
            raise ValueError('The page lock found different Reference sections on pages outside the Reference')
        tree = tree_markup(files[TREE_SCRIPT].read_bytes()) if script else None
        envelope = lock_tree(tree, next(iter(sections), None), keyring)
        keyring.header['tree'] = hashlib.sha256(envelope).hexdigest()[:10]

        locked = {1: Counter(), 2: Counter()}
        readable = Counter()
        for name, path in files.items():
            suffix = PurePath(name).suffix.lower() or '(no suffix)'
            if name in pages:
                level, data, at = pages[name]
                path.write_bytes(lock_page(name, level, data, keyring, versions, at))
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
        if linked:
            lines.append(f'Page lock: pages the general password opens link to {len(linked)} Reference '
                         f'page{"" if len(linked) == 1 else "s"} by address (navigation, site map or text); '
                         'general-password readers see those links.')
        return '\n'.join(lines)


def prepare_lock(options: Mapping, environ: Mapping[str, str] | None = None) -> PageLock | None:
    """Return the lock for ``[publication]`` options, or None when it is off.

    Checks the dependency and both passwords before anything is built.
    """
    if not lock_requested(options):
        return None
    _aesgcm()
    return PageLock(read_passwords(os.environ if environ is None else environ))
