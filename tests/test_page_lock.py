"""Page lock: key derivation, key wrapping, file sealing, passwords and the publish step.

Passwords are throwaway values generated at run time; no test stores one.
"""
import base64
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import page_lock
from page_lock import (ITERATIONS, PASSWORD_VARIABLES, PageLock, derive_key, derive_salt, file_context, lock_text,
                       lock_tree, make_keyring, named_references, open_keyring, open_slots, pad, prepare_lock,
                       read_passwords, reference_names, seal, split_reference, tree_markup, unpad, unseal)
import page_lock_fixture
from source_tree import TreeFile, tree_html, tree_script

try:
    from cryptography.exceptions import InvalidTag
except ImportError:  # the lock is optional; its dependency may be absent
    InvalidTag = None
needs_cryptography = unittest.skipIf(InvalidTag is None, 'cryptography is not installed; '
                                     'python -m pip install -r requirements-lock.txt')
FAST = 1_000  # iterations for checks of structure, not of cost


def throwaway() -> str:
    return secrets.token_urlsafe(24)  # 32 characters, 192 random bits


def environment(general=None, reference=None) -> dict:
    return {PASSWORD_VARIABLES[1]: throwaway() if general is None else general,
            PASSWORD_VARIABLES[2]: throwaway() if reference is None else reference}


class KeyDerivation(unittest.TestCase):
    def test_pbkdf2_matches_rfc_7914_vectors(self):
        # RFC 7914 section 11 lists PBKDF2-HMAC-SHA256 outputs; a 32-byte key is their first block.
        self.assertEqual(derive_key('passwd', b'salt', 1).hex(),
                         '55ac046e56e3089fec1691c22544b605f94185216dde0465e68b9d57c20dacbc')
        self.assertEqual(derive_key('Password', b'NaCl', 80000).hex(),
                         '4ddcd8f60b98be21830cee5ef22701f9641a4418d04c0414aeff08876b34ab56')

    def test_password_is_normalized_before_derivation(self):
        salt = os.urandom(16)
        composed, decomposed = 'café ' + throwaway(), 'café '
        self.assertEqual(derive_key(composed, salt, FAST), derive_key(decomposed + composed[5:], salt, FAST))
        self.assertNotEqual(derive_key(composed, salt, FAST), derive_key(composed, os.urandom(16), FAST))

    def test_iteration_count_meets_the_owasp_recommendation(self):
        self.assertGreaterEqual(ITERATIONS, 600_000)


@needs_cryptography
class Sealing(unittest.TestCase):
    def test_aes_256_gcm_known_answer(self):
        # GCM specification test case 14: zero key, zero nonce, one zero block, no associated data.
        sealed = seal(bytes(32), bytes(16), b'', nonce=bytes(12))
        self.assertEqual(sealed.hex(), '00' * 12 + 'cea7403d4d606b6e074ec5d3baf39d18'
                                                   'd0d1c8a799996bf0265b98b5d48ab919')

    def test_round_trip_uses_a_fresh_nonce(self):
        key, data = os.urandom(32), b'<p>locked text</p>'
        first, second = seal(key, data, file_context('a.html')), seal(key, data, file_context('a.html'))
        self.assertNotEqual(first[:12], second[:12])
        self.assertEqual(unseal(key, first, file_context('a.html')), data)
        self.assertEqual(unseal(key, second, file_context('a.html')), data)

    def test_changed_path_nonce_ciphertext_tag_or_key_fails(self):
        key, data = os.urandom(32), b'<p>locked text</p>'
        sealed = bytearray(seal(key, data, file_context('topic.html')))

        def flipped(index):
            changed = bytearray(sealed)
            changed[index] ^= 1
            return bytes(changed)

        cases = {'path': (key, bytes(sealed), file_context('other.html')),
                 'nonce': (key, flipped(0), file_context('topic.html')),
                 'ciphertext': (key, flipped(12), file_context('topic.html')),
                 'tag': (key, flipped(len(sealed) - 1), file_context('topic.html')),
                 'key': (os.urandom(32), bytes(sealed), file_context('topic.html'))}
        for name, (used_key, blob, context) in cases.items():
            with self.subTest(changed=name), self.assertRaises(InvalidTag):
                unseal(used_key, blob, context)


@needs_cryptography
class Wrapping(unittest.TestCase):
    def setUp(self):
        self.passwords = {1: throwaway(), 2: throwaway()}

    def test_general_password_opens_level_one_and_reference_opens_both(self):
        keyring = make_keyring(self.passwords, iterations=FAST)
        self.assertEqual(open_keyring(keyring.header, self.passwords[1]), (1, {1: keyring.content[1]}))
        self.assertEqual(open_keyring(keyring.header, self.passwords[2]), (2, keyring.content))
        self.assertIsNone(open_keyring(keyring.header, throwaway()))
        self.assertNotEqual(keyring.content[1], keyring.content[2])

    def test_header_holds_no_password_or_content_key(self):
        keyring = make_keyring(self.passwords, iterations=FAST)
        text = json.dumps(keyring.header)
        for secret in (*self.passwords.values(), *(base64.b64encode(k).decode() for k in keyring.content.values()),
                       *(k.hex() for k in keyring.content.values())):
            self.assertNotIn(secret, text)
        self.assertEqual(sorted(keyring.header), ['format', 'id', 'kdf', 'slots'])

    def test_every_publish_gets_a_fresh_id_and_content_keys_but_keeps_the_salt(self):
        # The salt once changed with every publish; it now changes only with a password,
        # so a remembered password key opens the next publish.
        first, second = (make_keyring(self.passwords, iterations=FAST) for _ in range(2))
        self.assertEqual(first.header['kdf']['salt'], second.header['kdf']['salt'])
        self.assertNotEqual(first.header['id'], second.header['id'])
        self.assertNotEqual(first.content, second.content)

    def test_salt_changes_when_either_password_changes(self):
        salt = derive_salt(self.passwords, FAST)
        self.assertEqual(len(salt), 16)
        self.assertEqual(salt, derive_salt(dict(self.passwords), FAST))
        self.assertNotEqual(salt, derive_salt({1: throwaway(), 2: self.passwords[2]}, FAST))
        self.assertNotEqual(salt, derive_salt({1: self.passwords[1], 2: throwaway()}, FAST))
        self.assertNotEqual(salt, derive_salt({1: self.passwords[2], 2: self.passwords[1]}, FAST))

    def test_remembered_key_opens_later_publishes_until_a_password_changes(self):
        first, later = (make_keyring(self.passwords, iterations=FAST) for _ in range(2))
        salt = base64.b64decode(first.header['kdf']['salt'])
        remembered = {level: derive_key(self.passwords[level], salt, FAST) for level in (1, 2)}
        self.assertEqual(open_slots(later.header, remembered[2]), (2, later.content))
        self.assertEqual(open_slots(later.header, remembered[1]), (1, {1: later.content[1]}))
        for changed in ({1: throwaway(), 2: self.passwords[2]}, {1: self.passwords[1], 2: throwaway()}):
            after = make_keyring(changed, iterations=FAST)
            for level in (1, 2):
                with self.subTest(changed=sorted(k for k in changed if changed[k] != self.passwords[k]), level=level):
                    self.assertIsNone(open_slots(after.header, remembered[level]))

    def test_slots_are_bound_to_their_publish(self):
        keyring = make_keyring(self.passwords, iterations=FAST)
        moved = dict(keyring.header, id=make_keyring(self.passwords, iterations=FAST).header['id'])
        self.assertIsNone(open_keyring(moved, self.passwords[2]))

    def test_default_iteration_count_is_written_and_used(self):
        keyring = make_keyring(self.passwords)
        self.assertEqual(keyring.header['kdf'], {'name': 'PBKDF2', 'hash': 'SHA-256', 'iterations': ITERATIONS,
                                                 'salt': keyring.header['kdf']['salt']})
        self.assertEqual(len(base64.b64decode(keyring.header['kdf']['salt'])), 16)
        self.assertEqual(open_keyring(keyring.header, self.passwords[2]), (2, keyring.content))


class Passwords(unittest.TestCase):
    def assertRejected(self, env, pattern):
        with self.assertRaisesRegex(ValueError, pattern) as caught:
            read_passwords(env)
        for value in env.values():
            if value.strip():
                self.assertNotIn(value.strip(), str(caught.exception))

    def test_missing_or_empty_password_names_its_variable(self):
        self.assertRejected({}, 'DOCSITE_GENERAL_PASSWORD is not set')
        self.assertRejected({PASSWORD_VARIABLES[1]: throwaway()}, 'DOCSITE_REFERENCE_PASSWORD is not set')
        self.assertRejected(environment(reference=''), 'DOCSITE_REFERENCE_PASSWORD is not set')

    def test_equal_passwords_fail(self):
        same = throwaway()
        self.assertRejected(environment(same, same), 'are equal')

    def test_no_rule_on_length_or_characters(self):
        for general in ('a', 'pw 1', 'ä€', throwaway()[:19]):
            env = environment(general=general)
            self.assertEqual(read_passwords(env)[1], general)

    def test_a_password_a_reader_may_not_type_gets_a_note_and_is_kept(self):
        for value, noted in ((throwaway() + '\n', True), (' ' + throwaway(), True),
                             (throwaway() + '\u200b' + throwaway(), True), ('short', False)):
            env, stderr = environment(reference=value), io.StringIO()
            with contextlib.redirect_stderr(stderr):
                self.assertEqual(read_passwords(env)[2], value)
            self.assertEqual('DOCSITE_REFERENCE_PASSWORD starts or ends with whitespace' in stderr.getvalue(), noted)
            self.assertNotIn(value.strip(), stderr.getvalue())

    def test_accepted_passwords_are_returned_by_level(self):
        env = environment()
        self.assertEqual(read_passwords(env), {1: env[PASSWORD_VARIABLES[1]], 2: env[PASSWORD_VARIABLES[2]]})

    def test_lock_is_off_unless_turned_on(self):
        self.assertIsNone(prepare_lock({}, {}))
        self.assertIsNone(prepare_lock({'lock': False}, {}))
        with self.assertRaisesRegex(ValueError, r'\[publication\] lock must be true or false'):
            prepare_lock({'lock': 'yes'}, {})

    def test_missing_dependency_fails_with_install_hint(self):
        with patch.dict(sys.modules, {'cryptography.hazmat.primitives.ciphers.aead': None}):
            with self.assertRaisesRegex(ValueError, 'needs the Python package cryptography.*requirements-lock.txt'):
                prepare_lock({'lock': True}, environment())

    @needs_cryptography
    def test_lock_object_never_shows_its_passwords(self):
        env = environment()
        lock = prepare_lock({'lock': True}, env)
        self.assertIsInstance(lock, PageLock)
        for value in env.values():
            self.assertNotIn(value, repr(lock))


def files(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(root.rglob('*')) if path.is_file()}


def sealed_page(data: bytes) -> bytes:
    return base64.b64decode(re.search(r'id="page-lock-data">([A-Za-z0-9+/=]+)<', data.decode())[1])


def opened(data: bytes, name: str, keys: dict[int, bytes]) -> tuple[int, bytes]:
    """Decrypt a locked page or text file as the browser would; pages are sealed padded."""
    text = data.decode()
    if name.endswith('.md'):
        level, sealed = re.search(r'^docsite-lock/1 level ([12])\n([A-Za-z0-9+/=]+)$', text, re.M).groups()
        return int(level), unseal(keys[int(level)], base64.b64decode(sealed), file_context(name))
    level = int(re.search(r'data-level="([12])"', text)[1])
    return level, unpad(unseal(keys[level], sealed_page(data), file_context(name)))


def opened_tree(data: bytes, keys: dict[int, bytes]) -> dict:
    sealed = re.search(r'window\.docsLockedReferenceTree = "([A-Za-z0-9+/=]+)";', data.decode())[1]
    return json.loads(unseal(keys[2], base64.b64decode(sealed), file_context('reference.tree.js')))


def joined(page: bytes, lock_page: bytes, section: str | None) -> bytes:
    """What the browser of a reference-password reader writes: the page with its Reference section back."""
    at = re.search(r'data-section-at="(\d+)"', lock_page.decode())
    return page if not at or section is None else page[:int(at[1])] + section.encode() + page[int(at[1]):]


TITLE = 'Listed TITLE-NAME-61be'
TREE_FILES = [TreeFile('policy/rule.md', 'rule.html', 'Shared rule', None, True),
              TreeFile('docs/listed.md', 'listed.html', TITLE, 'A listed record.', False)]


def kit_page(route: str, body_class: str = '', files=TREE_FILES) -> bytes:
    """A page shaped like the shared shell: sidebar list, Reference section, content."""
    section = tree_html(files, route, script='reference.tree.js?v=0123456789')
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<title>Page</title>\n</head>\n'
            f'<body{f" class={chr(34)}{body_class}{chr(34)}" if body_class else ""}>\n'
            '<nav class="sidebar" id="sidebar">\n  <a class="brand" href="index.html">B<small></small></a>\n'
            '  <div class="toc" id="toc">\n\n    <a class="xpage" href="guide.html">Guide</a>'
            + ('\n' + section if section else '') + '\n  </div>\n</nav>\n'
            f'<main class="content" id="top"><p>{route} text ✓</p><a href="rule.html#a">rule</a></main>\n'
            '</body>\n</html>\n').encode()


@needs_cryptography
class LockBundle(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-lock-')
        self.addCleanup(folder.cleanup)
        self.bundle = Path(folder.name)
        self.passwords = {1: throwaway(), 2: throwaway()}
        self.built = {'source_pages': {'rule.html': 'policy/rule.md', 'listed.html': 'docs/listed.md'},
                      'reference_tree': {'script': 'html/reference.tree.js', 'index': 'html/reference.index.html'}}
        self.original = {
            'index.html': kit_page('index.html'),
            'rule.html': kit_page('rule.html', 'source-page reference-page'),
            'listed.html': kit_page('listed.html'),
            'reference.index.html': kit_page('reference.index.html', 'reference-page reference-index-page'),
            'reference.tree.js': tree_script(TREE_FILES),
            '_media/media/frame.html': b'<p>frame text</p>',
            'notes/record.md': '# Record ✓\n'.encode(),
            'assets/base.css': b'body{color:white}',
            '_media/media/dot.svg': b'<svg/>',
            'data.json': b'{"value": 1}',
        }
        for name, data in self.original.items():
            path = self.bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def apply(self, built=None):
        return PageLock(self.passwords, iterations=FAST).apply(self.bundle, self.built if built is None else built)

    def test_pages_markdown_and_tree_are_locked_by_level_and_the_rest_stays(self):
        summary = self.apply()
        locked = files(self.bundle)
        header = json.loads(re.search(r'id="page-lock-keys">([^<]+)<', locked['index.html'].decode())[1])
        level, keys = open_keyring(header, self.passwords[2])
        self.assertEqual(level, 2)
        tree = opened_tree(locked['reference.tree.js'], keys)
        self.assertEqual(tree['tree'], tree_markup(self.original['reference.tree.js']))
        self.assertIn('data-repo-tree-src="reference.tree.js?v=0123456789"', tree['section'])
        levels = {}
        for name in ('index.html', 'rule.html', 'listed.html', 'reference.index.html', '_media/media/frame.html',
                     'notes/record.md'):
            levels[name], plain = opened(locked[name], name, keys)
            self.assertEqual(joined(plain, locked[name], tree['section']), self.original[name], name)
            self.assertNotIn(b'text \xe2\x9c\x93', locked[name])
        self.assertEqual(levels, {'index.html': 1, 'rule.html': 2, 'listed.html': 2, 'reference.index.html': 2,
                                  '_media/media/frame.html': 1, 'notes/record.md': 2})
        _, general = open_keyring(header, self.passwords[1])
        home = opened(locked['index.html'], 'index.html', general)[1]
        for hidden in (b'repo-tree', TITLE.encode(), b'Shared rule', b'listed.html', b'reference.tree.js'):
            self.assertNotIn(hidden, home)
        self.assertIn(b'data-section-at=', locked['index.html'])
        self.assertNotIn(b'data-section-at=', locked['_media/media/frame.html'])
        with self.assertRaises(KeyError):
            opened(locked['rule.html'], 'rule.html', general)
        with self.assertRaises(KeyError):
            opened_tree(locked['reference.tree.js'], general)
        for name in ('assets/base.css', '_media/media/dot.svg', 'data.json'):
            self.assertEqual(locked[name], self.original[name])
        self.assertIn('assets/page-lock.js', locked)
        self.assertIn('assets/page-lock.css', locked)
        self.assertEqual(header['tree'], hashlib.sha256(locked['reference.tree.js']).hexdigest()[:10])
        self.assertEqual(summary, 'Page lock: the general password opens 2 files (.html 2); only the reference '
                                  'password opens 5 more (.html 3, .js 1, .md 1).\nPage lock: 5 files stay readable '
                                  'without a password (.css 2, .js 1, .json 1, .svg 1).\nPage lock: pages the general '
                                  'password opens name 1 Reference file (links, source links or text); '
                                  'general-password readers see those names.')

    def reset(self, changes):
        """Write the bundle again from the originals, with ``changes``."""
        shutil.rmtree(self.bundle)
        for name, data in {**self.original, **changes}.items():
            path = self.bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def levels(self):
        return {name: int(re.search(rb'data-level="([12])"', data)[1])
                for name, data in files(self.bundle).items() if name.endswith('.html')}

    def test_pages_are_sealed_padded(self):
        self.assertEqual(unpad(pad(b'<p>x</p>')), b'<p>x</p>')
        self.assertEqual(len(pad(b'abc', 64)), 64)
        self.assertEqual(unpad(pad(b'\x80\x00', 9)), b'\x80\x00')
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            unpad(b'abc\x00')
        with self.assertRaisesRegex(ValueError, 'fewer bytes'):
            pad(b'abc', 3)

    def test_reference_index_is_padded_like_the_tree_file(self):
        # The index lists every Reference file; unpadded, its length showed the size of the tree.
        def sizes():
            locked = files(self.bundle)
            tree = re.search(r'"([A-Za-z0-9+/=]+)"', locked['reference.tree.js'].decode())[1]
            return len(sealed_page(locked['reference.index.html'])), len(base64.b64decode(tree))
        self.apply()
        self.assertEqual(sizes(), (65536 + 28, 65536 + 28))
        index = kit_page('reference.index.html', 'reference-page reference-index-page')
        self.reset({'reference.index.html': index.replace(b'</main>', b'x' * 70000 + b'</main>')})
        self.apply()
        self.assertEqual(sizes(), (131072 + 28, 131072 + 28))

    def test_frames_only_reference_pages_use_need_the_reference_password(self):
        rule = kit_page('rule.html', 'source-page reference-page').replace(
            b'</main>', b'<iframe src="_media/a/report.html"></iframe><iframe src="_media/b/both.html"></iframe>'
            b'<iframe src=_media/d/bare.html></iframe><object data="/project/_media/e/rooted.html"></object></main>')
        home = kit_page('index.html').replace(b'</main>', b'<iframe src="_media/b/both.html"></iframe></main>')
        self.reset({'rule.html': rule, 'index.html': home,
                    '_media/a/report.html': b'<p>report</p><iframe src="nested.html"></iframe>',
                    '_media/a/nested.html': b'<p>nested</p>', '_media/b/both.html': b'<p>both</p>',
                    '_media/c/alone.html': b'<p>alone</p>', '_media/d/bare.html': b'<p>bare</p>',
                    '_media/e/rooted.html': b'<p>rooted</p>'})
        self.apply()
        levels = self.levels()
        self.assertEqual({name: levels[name] for name in levels if name.startswith('_media/')},
                         {'_media/a/report.html': 2, '_media/a/nested.html': 2, '_media/b/both.html': 1,
                          '_media/d/bare.html': 2, '_media/e/rooted.html': 2,
                          '_media/c/alone.html': 1, '_media/media/frame.html': 1})

    def test_root_404_page_opens_at_any_address(self):
        self.reset({'404.html': b'<p>missing</p>', 'docs/404.html': b'<p>other</p>'})
        self.apply()
        locked = files(self.bundle)
        self.assertIn(b' data-not-found', locked['404.html'])
        self.assertNotIn(b'data-not-found', locked['docs/404.html'])
        self.assertNotIn(b'data-not-found', locked['index.html'])
        self.assertEqual(self.levels()['404.html'], 1)

    def test_xhtml_and_shtml_are_refused(self):
        for name in ('media/page.xhtml', 'media/page.XHT', 'ssi/page.shtml', 'ssi/page.shtm'):
            with self.subTest(name=name):
                self.reset({name: b'<p>x</p>'})
                with self.assertRaisesRegex(ValueError, f'cannot lock {re.escape(name)}: .*Rename it to .html'):
                    self.apply()

    def test_reference_markup_left_in_a_general_page_fails_closed(self):
        # With the sidebar's attributes in another order the cut finds nothing; the final check refuses.
        moved = kit_page('index.html').replace(b'<nav class="sidebar" id="sidebar">',
                                               b'<nav id="sidebar" class="sidebar">')
        self.reset({'index.html': moved})
        with self.assertRaisesRegex(ValueError, 'found Reference markup in index.html'):
            self.apply()
        self.assertEqual((self.bundle / 'index.html').read_bytes(), moved)
        # A loader attribute alone is Reference markup too; a route that merely contains the word is not.
        self.reset({'index.html': kit_page('index.html').replace(b'<main', b'<p data-repo-tree-src="x"></p><main')})
        with self.assertRaisesRegex(ValueError, 'found Reference markup in index.html'):
            self.apply()
        self.reset({'index.html': kit_page('index.html').replace(
            b'</main>', b'<a href="docs.repo-tree.md.html" title="repo-tree">repo-tree</a></main>')})
        self.apply()

    def test_summary_names_every_reference_file_a_general_page_points_at(self):
        built = {'source_pages': {'rule.html': 'policy/rule.md', 'listed.html': 'docs/listed.md',
                                  'notes.a.md.html': 'notes/a.md', 'notes.b.md.html': 'notes/b.md',
                                  'c.md.html': 'c.md', 'notes.d.md.html': 'notes/d.md'}}
        names = reference_names(built, {'notes/record.md'})
        page = ('<a href="rule.html#x">route</a>'
                '<a href="https://github.com/o/r/blob/main/docs/listed.md#L2">source host</a>'
                '<a data-repo-path="notes/a.md" href="#">today\'s marker</a>'
                '<a data-source-file="notes/b.md" href="#">any other marker</a>'
                '<a href="notes/record.md">exported Markdown</a>'
                '<p>Text that names c.md.</p>'
                '<a href="../../notes/d.md">logical source path</a>')
        self.assertEqual(named_references(page, 'index.html', names),
                         {'policy/rule.md', 'docs/listed.md', 'notes/a.md', 'notes/b.md', 'notes/record.md', 'c.md',
                          'notes/d.md'})
        self.assertEqual(named_references('<p>notes/ab.md xc.md rule.htm</p>', 'index.html', names), set())

    def test_site_without_reference_still_gets_a_sealed_tree_and_section_offsets(self):
        for name in ('rule.html', 'listed.html', 'reference.index.html', 'reference.tree.js'):
            (self.bundle / name).unlink()
        (self.bundle / 'index.html').write_bytes(kit_page('index.html', files=[]))
        self.apply({'source_pages': {}, 'reference_tree': None})
        locked = files(self.bundle)
        header = json.loads(re.search(r'id="page-lock-keys">([^<]+)<', locked['index.html'].decode())[1])
        _, keys = open_keyring(header, self.passwords[2])
        self.assertEqual(opened_tree(locked['reference.tree.js'], keys), {'section': None, 'tree': None})
        self.assertIn(b'data-section-at=', locked['index.html'])
        # Same length as the tree file of a site with a small Reference section.
        small = lock_tree(tree_markup(self.original['reference.tree.js']), 'section',
                          make_keyring(self.passwords, iterations=FAST))
        self.assertEqual(len(locked['reference.tree.js']), len(small))

    def test_sealed_tree_is_padded_to_a_power_of_two(self):
        keyring = make_keyring(self.passwords, iterations=FAST)
        sizes = {}
        for files_count in (0, 5, 500):
            listed = [TreeFile(f'notes/n{i}.md', f'n{i}.md.html', f'Note {i}', None, False) for i in range(files_count)]
            data = lock_tree(tree_html(listed, '') or None, None, keyring).decode()
            sizes[files_count] = len(base64.b64decode(re.search(r'"([A-Za-z0-9+/=]+)"', data)[1])) - 28
        self.assertEqual(sizes[0], sizes[5])
        self.assertEqual(sizes[0], 65536)
        self.assertEqual(sizes[500] & (sizes[500] - 1), 0)
        self.assertGreater(sizes[500], 65536)

    def test_reference_section_split_is_exact_and_strict(self):
        page = kit_page('index.html').decode()
        stripped, section, at = split_reference(page, 'index.html')
        self.assertEqual(stripped[:at] + section + stripped[at:], page)
        self.assertTrue(stripped[:at].endswith('Guide</a>'))
        bare = kit_page('index.html', files=[]).decode()
        # Without a section the offset is where one would go, so its presence says nothing.
        self.assertEqual(split_reference(bare, 'index.html'), (bare, None, bare.index('\n  </div>\n</nav>')))
        self.assertEqual(split_reference('<p>frame</p>', 'frame.html'), ('<p>frame</p>', None, None))
        with self.assertRaisesRegex(ValueError, 'at most one Reference section'):
            split_reference(page.replace('    <a class="xpage"', section + '\n    <a class="xpage"', 1), 'x.html')
        with self.assertRaisesRegex(ValueError, 'Reference markup remains'):
            split_reference(page.replace('<main class="content" id="top">',
                                         '<main class="content" id="top"><div class="repo-tree"></div>'), 'y.html')

    def test_lock_page_is_generic_and_finds_its_assets(self):
        self.apply()
        page = (self.bundle / '_media/media/frame.html').read_text()
        self.assertIn('<title>Locked page</title>', page)
        self.assertIn('<meta name="robots" content="noindex, nofollow, noarchive">', page)
        self.assertIn('data-root="../../"', page)
        version = hashlib.sha256((self.bundle / 'assets/page-lock.js').read_bytes()).hexdigest()[:10]
        self.assertIn(f'src="../../assets/page-lock.js?v={version}"', page)
        self.assertIn('href="../../assets/base.css?v=', page)
        self.assertIn('<noscript>', page)
        self.assertIn('data-root="./"', (self.bundle / 'index.html').read_text())

    def test_existing_lock_asset_or_non_utf8_text_fails(self):
        (self.bundle / 'assets/page-lock.js').write_text('project file')
        with self.assertRaisesRegex(ValueError, 'adds assets/page-lock.js'):
            self.apply()
        (self.bundle / 'assets/page-lock.js').unlink()
        with self.assertRaisesRegex(ValueError, 'writes reference.tree.js, which the bundle holds without the build'):
            self.apply(dict(self.built, reference_tree=None))
        (self.bundle / 'listed.html').write_bytes(b'<p>caf\xe9</p>')
        with self.assertRaisesRegex(ValueError, 'listed.html is not UTF-8'):
            self.apply()

    def test_text_envelope_starts_with_a_readable_notice(self):
        keyring = make_keyring(self.passwords, iterations=FAST)
        envelope = lock_text('notes/record.md', 2, b'# Record', keyring).decode()
        self.assertTrue(envelope.startswith('This file is locked.'))
        self.assertRegex(envelope, r'\ndocsite-lock/1 level 2\n[A-Za-z0-9+/=]+\n$')


@needs_cryptography
class PublishWithLock(unittest.TestCase):
    """The real publish command on a disposable project with both levels."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-lock-publish-')
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)

    def publish(self, *, lock, env=None, name='project'):
        project = page_lock_fixture.make_project(self.folder / name, lock=lock)
        out = self.folder / (name + '-site')
        result = page_lock_fixture.docsite('publish', '--project', project, '--out', out,
                                           env=dict(os.environ, **(env or {})))
        return result, out

    def plain_bundle(self, project: Path) -> Path:
        """The same project and build published without the lock step: what the lock layers over."""
        from publication import publish_project
        out = self.folder / 'plain-site'
        run = subprocess.run
        with patch('publication.prepare_lock', return_value=None), \
             patch('publication.subprocess.run', lambda *a, **k: run(*a, **{'stdout': subprocess.DEVNULL, **k})), \
             patch.dict(os.environ), contextlib.redirect_stdout(io.StringIO()):
            os.environ.pop('GITHUB_SHA', None)  # the fixture's own publish ignores it too
            publish_project(project, out, kit=page_lock_fixture.KIT)
        return out

    def test_locked_bundle_has_no_marker_or_password_and_unlocks_to_the_plain_bundle(self):
        env = environment()
        result, out = self.publish(lock=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        locked = files(out)
        for name, data in locked.items():
            for marker in page_lock_fixture.MARKERS.values():
                self.assertNotIn(marker.encode(), data, f'{marker} readable in {name}')
            for value in env.values():
                self.assertNotIn(value.encode(), data, f'a password is written into {name}')
        for value in env.values():
            self.assertNotIn(value, result.stdout + result.stderr)

        # Every tracked Markdown file of a listed folder is a Reference page, and a locked
        # build writes the tree once even for a few files. This test once expected
        # exactly two reference-level files: the registered page and the exported Markdown.
        project = self.folder / 'project'
        built = json.loads((project / '.build/docs/site-build.json').read_text())
        self.assertIn('notes.record.md.html', built['source_pages'])
        self.assertEqual(built['reference_tree'], {'script': 'html/reference.tree.js',
                                                   'index': 'html/reference.index.html'})
        # A frame that only a Reference page embeds needs the reference password too.
        reference_pages = set(built['source_pages']) | {'reference.index.html', '_media/policy/report.html'}
        self.assertIn(f'only the reference password opens {len(reference_pages) + 2} more '
                      f'(.html {len(reference_pages)}, .js 1, .md 1).', result.stdout)
        self.assertIn('files stay readable without a password', result.stdout)

        plain = files(self.plain_bundle(project))
        self.assertEqual(set(locked) - set(plain), {'assets/page-lock.js', 'assets/page-lock.css'})
        header = json.loads(re.search(r'id="page-lock-keys">([^<]+)<', locked['guide.html'].decode())[1])
        _, keys = open_keyring(header, env[PASSWORD_VARIABLES[2]])
        _, general = open_keyring(header, env[PASSWORD_VARIABLES[1]])
        tree = opened_tree(locked['reference.tree.js'], keys)
        self.assertEqual(tree['tree'], tree_markup(plain['reference.tree.js']))
        self.assertIn(page_lock_fixture.MARKERS['title'], tree['tree'])
        levels, named = {}, set()
        names = reference_names(built, {'notes/record.md'})
        for name, data in plain.items():
            if name == 'reference.tree.js':
                continue
            if name.endswith(('.html', '.md')):
                levels[name], page = opened(locked[name], name, keys)
                if levels[name] == 1:
                    # What a general-password reader decrypts holds no Reference tree.
                    self.assertEqual(opened(locked[name], name, general)[1], page)
                    for hidden in (b'repo-tree', page_lock_fixture.MARKERS['title'].encode(), b'reference.tree.js',
                                   b'notes.record.md.html', b'docs.worklog.md.html'):
                        self.assertNotIn(hidden, page, name)
                    named |= named_references(page.decode(), name, names)
                # Locking is a layer over the ordinary bundle; nothing else changes.
                self.assertEqual(joined(page, locked[name], tree['section']), data, name)
            else:
                self.assertEqual(locked[name], data, name)
        self.assertEqual({name for name, level in levels.items() if level == 2}, reference_pages | {'notes/record.md'})
        self.assertEqual({name for name, level in levels.items() if level == 1},
                         {'guide.html', 'index.html', 'widgets.html', '_media/media/frame.html', '404.html'})
        # General pages still name Reference files: a route, source links and an exported Markdown file.
        self.assertEqual(named, {'policy/rule.md', 'notes/record.md', 'docs/PROJECT_CONTEXT.md', 'docs/open/OPEN.md',
                                 'docs/topics/guide/guide.md'})
        self.assertIn(f'name {len(named)} Reference files (links, source links or text)', result.stdout)
        self.assertIn(b' data-not-found', locked['404.html'])
        index = sealed_page(locked['reference.index.html'])
        self.assertEqual(len(index), len(base64.b64decode(
            re.search(r'"([A-Za-z0-9+/=]+)"', locked['reference.tree.js'].decode())[1])))

    def test_lock_off_output_is_byte_identical(self):
        absent, absent_out = self.publish(lock=None, name='absent')
        off, off_out = self.publish(lock=False, name='off', env=environment())
        self.assertEqual((absent.returncode, off.returncode), (0, 0), absent.stderr + off.stderr)
        self.assertEqual(files(absent_out), files(off_out))
        self.assertNotIn('assets/page-lock.js', files(absent_out))
        self.assertNotIn('Page lock', absent.stdout + off.stdout)
        self.assertEqual(absent.stdout.replace('absent', 'off'), off.stdout)
        # Without the lock a small Reference tree stays inline in every page.
        built = json.loads((self.folder / 'off/.build/docs/site-build.json').read_text())
        self.assertIsNone(built['reference_tree'])
        self.assertIn(b'class="repo-tree"', files(off_out)['guide.html'])

    def test_unusable_passwords_fail_before_building_and_leave_no_output(self):
        same = throwaway()
        cases = {'not set': {PASSWORD_VARIABLES[1]: throwaway(), PASSWORD_VARIABLES[2]: ''},
                 'are equal': environment(same, same)}
        for index, (message, env) in enumerate(cases.items()):
            with self.subTest(message=message):
                result, out = self.publish(lock=True, env=env, name=f'failing-{index}')
                self.assertEqual(result.returncode, 1)
                self.assertIn('Publication failed: ', result.stderr)
                self.assertIn(message, result.stderr)
                for value in env.values():
                    if value:
                        self.assertNotIn(value, result.stdout + result.stderr)
                self.assertFalse(out.exists())
                self.assertFalse((self.folder / f'failing-{index}/.build/docs').exists())


if __name__ == '__main__':
    unittest.main()
