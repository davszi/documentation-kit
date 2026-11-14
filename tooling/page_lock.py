"""Opt-in page lock: store the text of a published bundle encrypted.

``publish`` calls ``prepare_lock`` before it builds, so a missing dependency or
an unusable password fails fast, and ``PageLock.apply`` on the finished bundle
before the bundle moves into place. A project turns the lock on with
``lock = true`` in the ``[publication]`` table of ``docs/site/site.toml``; the
two passwords come only from the environment variables in
``PASSWORD_VARIABLES``. Local ``build`` output is never locked.

Key layout, one set per publish:

- a random 16-byte salt and PBKDF2-HMAC-SHA-256 with ``ITERATIONS`` derive one
  key-encryption key from each password;
- level 1 (topic pages and every other page) and level 2 (Reference pages and
  exported Markdown) each get a random 256-bit content key;
- the general password's slot holds the level-1 key; the reference password's
  slot holds both keys, so it opens everything;
- every locked file is sealed with AES-256-GCM under its level's key, with a
  fresh random 96-bit nonce and its public bundle path as associated data.

The browser side is ``theme/components/page-lock.js``; it uses WebCrypto with
the same parameters. Passwords never enter output, logs or error messages.
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

FORMAT = 'docsite-lock/1'
# OWASP Password Storage Cheat Sheet: 600,000 iterations for PBKDF2-HMAC-SHA256.
ITERATIONS = 600_000
SALT_BYTES = 16
KEY_BYTES = 32
NONCE_BYTES = 12
# Length is the only property a check can see; it cannot measure randomness.
MIN_PASSWORD_LENGTH = 20
PASSWORD_VARIABLES = {1: 'DOCSITE_GENERAL_PASSWORD', 2: 'DOCSITE_REFERENCE_PASSWORD'}
HTML_SUFFIXES = ('.html', '.htm')
MARKDOWN_SUFFIXES = ('.md', '.markdown')
LOCK_ASSETS = {'assets/page-lock.js': 'page-lock.js', 'assets/page-lock.css': 'page-lock.css'}
INSTALL_HINT = ('python -m pip install -r .docs-kit/requirements-lock.txt '
                '(requirements-lock.txt in the kit itself)')
TEXT_NOTICE = ('This file is locked. Open it from a page of the documentation site '
               'after entering the password.')
_COMPONENTS = Path(__file__).resolve().parent.parent / 'theme/components'
_BODY = re.compile(rb'<body\b([^>]*)>', re.I)
_CLASS = re.compile(rb'''(?:^|\s)class\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))''', re.I)


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
    salt = secrets.token_bytes(SALT_BYTES)
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


def open_keyring(header: Mapping, password: str) -> tuple[int, dict[int, bytes]] | None:
    """What the browser does: the level and content keys a password opens, or None."""
    from cryptography.exceptions import InvalidTag
    kdf = header['kdf']
    key = derive_key(password, base64.b64decode(kdf['salt']), kdf['iterations'])
    for slot in header['slots']:
        try:
            plain = unseal(key, base64.b64decode(slot), slots_context(header['id']))
        except InvalidTag:
            continue
        level = plain[0]
        return level, {n: plain[1 + (n - 1) * KEY_BYTES:1 + n * KEY_BYTES] for n in range(1, level + 1)}
    return None


def is_source_page(markup: bytes) -> bool:
    """The build marks every Reference page's body with the class source-page."""
    body = _BODY.search(markup)
    if not body:
        return False
    match = _CLASS.search(body[1])
    return bool(match) and b'source-page' in next(group for group in match.groups() if group is not None).split()


def _utf8(name: str, data: bytes) -> None:
    try:
        data.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError(f'The page lock reads text as UTF-8, and {name} is not UTF-8') from None


def lock_text(name: str, level: int, data: bytes, keyring: Keyring) -> bytes:
    """A readable notice, a marker line and the sealed file in base64."""
    _utf8(name, data)
    sealed = seal(keyring.content[level], data, file_context(name))
    return f'{TEXT_NOTICE}\n{FORMAT} level {level}\n{_b64(sealed)}\n'.encode('ascii')


def lock_page(name: str, level: int, data: bytes, keyring: Keyring, versions: Mapping[str, str]) -> bytes:
    """The lock page served at ``name`` instead of the page itself."""
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
              '{{BASE_CSS}}': base, '{{LOCK_CSS}}': asset('assets/page-lock.css'),
              '{{LOCK_JS}}': asset('assets/page-lock.js'), '{{KEYS}}': header, '{{DATA}}': _b64(sealed)}
    text = (_COMPONENTS / 'page-lock.html').read_text()
    return re.sub(r'\{\{[A-Z_]+\}\}', lambda match: values[match[0]], text).encode('utf-8')


def _counts(counter: Counter) -> str:
    return ', '.join(f'{suffix} {count}' for suffix, count in sorted(counter.items())) or 'none'


@dataclass(frozen=True)
class PageLock:
    passwords: dict[int, str]
    iterations: int = ITERATIONS

    def __repr__(self) -> str:  # never show the passwords, even in a traceback
        return f'PageLock(iterations={self.iterations})'

    def apply(self, bundle: Path, reference_routes: Mapping[str, str] | set[str]) -> str:
        """Lock every HTML page and Markdown file of ``bundle`` in place; return the summary."""
        bundle = Path(bundle)
        for target in LOCK_ASSETS:
            if (bundle / target).exists():
                raise ValueError(f'The page lock adds {target}, which the bundle already holds')
        keyring = make_keyring(self.passwords, iterations=self.iterations)
        files = {path.relative_to(bundle).as_posix(): path for path in sorted(bundle.rglob('*'))
                 if path.is_file() or path.is_symlink()}
        assets = {target: (_COMPONENTS / source).read_bytes() for target, source in LOCK_ASSETS.items()}
        versions = {target: hashlib.sha256(data).hexdigest()[:10] for target, data in assets.items()}
        if 'assets/base.css' in files:
            versions['assets/base.css'] = hashlib.sha256(files['assets/base.css'].read_bytes()).hexdigest()[:10]
        locked = {1: Counter(), 2: Counter()}
        readable = Counter()
        for name, path in files.items():
            if path.is_symlink():
                raise ValueError(f'The page lock cannot follow a symlink: {name}')
            suffix = PurePath(name).suffix.lower() or '(no suffix)'
            data = path.read_bytes()
            if name.lower().endswith(HTML_SUFFIXES):
                level = 2 if name in reference_routes or is_source_page(data) else 1
                path.write_bytes(lock_page(name, level, data, keyring, versions))
                locked[level][suffix] += 1
            elif name.lower().endswith(MARKDOWN_SUFFIXES):
                path.write_bytes(lock_text(name, 2, data, keyring))
                locked[2][suffix] += 1
            else:
                readable[suffix] += 1
        for target, data in assets.items():
            (bundle / target).parent.mkdir(parents=True, exist_ok=True)
            (bundle / target).write_bytes(data)
            readable[PurePath(target).suffix] += 1
        return (f'Page lock: the general password opens {sum(locked[1].values())} files ({_counts(locked[1])}); '
                f'only the reference password opens {sum(locked[2].values())} more ({_counts(locked[2])}).\n'
                f'Page lock: {sum(readable.values())} files stay readable without a password '
                f'({_counts(readable)}).')


def prepare_lock(options: Mapping, environ: Mapping[str, str] | None = None) -> PageLock | None:
    """Return the lock for ``[publication]`` options, or None when it is off.

    Checks the dependency and both passwords before anything is built.
    """
    if not lock_requested(options):
        return None
    _aesgcm()
    return PageLock(read_passwords(os.environ if environ is None else environ))
