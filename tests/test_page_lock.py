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
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import page_lock
from page_lock import (ITERATIONS, PASSWORD_VARIABLES, PageLock, derive_key, file_context, lock_text,
                       make_keyring, open_keyring, prepare_lock, read_passwords, seal, unseal)
import page_lock_fixture

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

    def test_every_publish_gets_a_fresh_salt_id_and_keys(self):
        first, second = (make_keyring(self.passwords, iterations=FAST) for _ in range(2))
        self.assertNotEqual(first.header['kdf']['salt'], second.header['kdf']['salt'])
        self.assertNotEqual(first.header['id'], second.header['id'])
        self.assertNotEqual(first.content, second.content)

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

    def test_short_equal_or_untypable_passwords_fail(self):
        self.assertRejected(environment(general=throwaway()[:19]), 'DOCSITE_GENERAL_PASSWORD is shorter than 20')
        same = throwaway()
        self.assertRejected(environment(same, same), 'are equal')
        self.assertRejected(environment(reference=throwaway() + '\n'), 'DOCSITE_REFERENCE_PASSWORD starts or ends')
        self.assertRejected(environment(general=' ' + throwaway()), 'DOCSITE_GENERAL_PASSWORD starts or ends')
        self.assertRejected(environment(general=throwaway() + '​' + throwaway()), 'invisible')

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


def opened(data: bytes, name: str, keys: dict[int, bytes]) -> tuple[int, bytes]:
    """Decrypt a locked page or text file as the browser would."""
    text = data.decode()
    if name.endswith('.md'):
        level, sealed = re.search(r'^docsite-lock/1 level ([12])\n([A-Za-z0-9+/=]+)$', text, re.M).groups()
    else:
        level = re.search(r'data-level="([12])"', text)[1]
        sealed = re.search(r'id="page-lock-data">([A-Za-z0-9+/=]+)<', text)[1]
    return int(level), unseal(keys[int(level)], base64.b64decode(sealed), file_context(name))


@needs_cryptography
class LockBundle(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='docs-kit-lock-')
        self.addCleanup(folder.cleanup)
        self.bundle = Path(folder.name)
        self.passwords = {1: throwaway(), 2: throwaway()}
        self.original = {
            'index.html': b'<!doctype html><html><head><title>Home</title></head><body><p>home text</p></body></html>',
            'rule.html': b'<html><body class="source-page reference-page" data-x="1"><p>rule text</p></body></html>',
            'listed.html': b'<html><body><p>listed only in the build manifest</p></body></html>',
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

    def apply(self):
        return PageLock(self.passwords, iterations=FAST).apply(self.bundle, {'listed.html': 'docs/listed.md'})

    def test_pages_and_markdown_are_locked_by_level_and_the_rest_stays(self):
        summary = self.apply()
        locked = files(self.bundle)
        header = json.loads(re.search(r'id="page-lock-keys">([^<]+)<', locked['index.html'].decode())[1])
        level, keys = open_keyring(header, self.passwords[2])
        self.assertEqual(level, 2)
        levels = {}
        for name in ('index.html', 'rule.html', 'listed.html', '_media/media/frame.html', 'notes/record.md'):
            levels[name], plain = opened(locked[name], name, keys)
            self.assertEqual(plain, self.original[name])
            self.assertNotIn(self.original[name], locked[name])
        self.assertEqual(levels, {'index.html': 1, 'rule.html': 2, 'listed.html': 2,
                                  '_media/media/frame.html': 1, 'notes/record.md': 2})
        _, general = open_keyring(header, self.passwords[1])
        self.assertEqual(opened(locked['index.html'], 'index.html', general)[1], self.original['index.html'])
        with self.assertRaises(KeyError):
            opened(locked['rule.html'], 'rule.html', general)
        for name in ('assets/base.css', '_media/media/dot.svg', 'data.json'):
            self.assertEqual(locked[name], self.original[name])
        self.assertIn('assets/page-lock.js', locked)
        self.assertIn('assets/page-lock.css', locked)
        self.assertEqual(summary, 'Page lock: the general password opens 2 files (.html 2); only the reference '
                                  'password opens 3 more (.html 2, .md 1).\nPage lock: 5 files stay readable '
                                  'without a password (.css 2, .js 1, .json 1, .svg 1).')

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
        self.assertRegex(result.stdout, r'Page lock: the general password opens \d+ files \(\.html \d+\); '
                                        r'only the reference password opens 2 more \(\.html 1, \.md 1\)\.')
        self.assertIn('files stay readable without a password', result.stdout)

        plain_result, plain = self.publish(lock=False, name='plain')
        self.assertEqual(plain_result.returncode, 0, plain_result.stderr)
        expected = files(plain)
        self.assertEqual(set(locked) - set(expected), {'assets/page-lock.js', 'assets/page-lock.css'})
        header = json.loads(re.search(r'id="page-lock-keys">([^<]+)<', locked['guide.html'].decode())[1])
        _, keys = open_keyring(header, env[PASSWORD_VARIABLES[2]])
        levels = {}
        for name, data in expected.items():
            if name.endswith(('.html', '.md')):
                levels[name], plain_bytes = opened(locked[name], name, keys)
                # Locking is a layer over the ordinary bundle; nothing else changes.
                self.assertEqual(plain_bytes, data, name)
            else:
                self.assertEqual(locked[name], data, name)
        self.assertEqual({name for name, level in levels.items() if level == 2}, {'rule.html', 'notes/record.md'})
        self.assertIn('guide.html', levels)
        self.assertIn('widgets.html', levels)
        self.assertIn('_media/media/frame.html', levels)

    def test_lock_off_output_is_byte_identical(self):
        absent, absent_out = self.publish(lock=None, name='absent')
        off, off_out = self.publish(lock=False, name='off', env=environment())
        self.assertEqual((absent.returncode, off.returncode), (0, 0), absent.stderr + off.stderr)
        self.assertEqual(files(absent_out), files(off_out))
        self.assertNotIn('assets/page-lock.js', files(absent_out))
        self.assertNotIn('Page lock', absent.stdout + off.stdout)
        self.assertEqual(absent.stdout.replace('absent', 'off'), off.stdout)

    def test_unusable_passwords_fail_before_building_and_leave_no_output(self):
        same = throwaway()
        cases = {'not set': {PASSWORD_VARIABLES[1]: throwaway(), PASSWORD_VARIABLES[2]: ''},
                 'are equal': environment(same, same),
                 'shorter than 20': environment(reference=throwaway()[:12])}
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
