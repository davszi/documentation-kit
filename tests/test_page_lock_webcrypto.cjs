// The browser side of the page lock (theme/components/page-lock.js, through
// Node's WebCrypto) must open what the build side (tooling/page_lock.py)
// sealed, at the real iteration count. Passwords are generated here, passed to
// Python through the environment and never written to disk.
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const crypto = require('node:crypto');
const path = require('node:path');

const kit = path.resolve(__dirname, '..');
const lock = require('../theme/components/page-lock.js');
const python = process.env.DOCS_PYTHON || 'python3';
const throwaway = () => crypto.randomBytes(24).toString('base64url');
const general = throwaway();
const reference = throwaway();

(async () => {
  const output = execFileSync(python, [path.join(kit, 'tests/page_lock_fixture.py'), 'vectors'], {
    env: {...process.env, DOCSITE_GENERAL_PASSWORD: general, DOCSITE_REFERENCE_PASSWORD: reference},
    encoding: 'utf8'});
  assert.ok(!output.includes(general) && !output.includes(reference), 'vectors must not carry a password');
  const {header, files} = JSON.parse(output);
  assert.equal(header.kdf.iterations, 600000);

  const opened = await lock.unlock(general, header);
  const both = await lock.unlock(reference, header);
  assert.equal(opened.level, 1);
  assert.deepEqual(Object.keys(opened.keys), ['1']);
  assert.equal(both.level, 2);
  assert.deepEqual(Object.keys(both.keys), ['1', '2']);
  assert.deepEqual(both.keys[1], opened.keys[1]);
  assert.equal(await lock.unlock(throwaway(), header), null);
  assert.equal(await lock.unlock(general.slice(0, -1), header), null);

  let checked = 0;
  for (const file of files) {
    const plain = lock.fromBase64(file.plain);
    let sealed;
    if (file.envelope) {
      const envelope = lock.parseEnvelope(file.envelope);
      assert.equal(envelope.level, file.level);
      sealed = envelope.sealed;
    } else {
      sealed = lock.fromBase64(file.sealed);
    }
    assert.deepEqual(await lock.openFile(both.keys[file.level], file.path, sealed), plain, file.path);
    if (file.level === 1) assert.deepEqual(await lock.openFile(opened.keys[1], file.path, sealed), plain);
    else assert.equal(opened.keys[file.level], undefined);
    // Associated data binds the path; any changed byte fails authentication.
    await assert.rejects(lock.openFile(both.keys[file.level], 'moved/' + file.path, sealed), {name: 'OperationError'});
    for (const index of [0, 12, sealed.length - 1]) {
      const changed = sealed.slice();
      changed[index] ^= 1;
      await assert.rejects(lock.openFile(both.keys[file.level], file.path, changed), {name: 'OperationError'});
    }
    await assert.rejects(lock.openFile(both.keys[3 - file.level], file.path, sealed), {name: 'OperationError'});
    checked++;
  }
  assert.equal(checked, 3);
  assert.equal(lock.toBase64(lock.fromBase64('AAECAwQ=')), 'AAECAwQ=');
  console.log('Page lock WebCrypto cross-check passes: Node decrypts what Python sealed for both levels at '
    + header.kdf.iterations + ' PBKDF2 iterations; wrong passwords, moved paths and changed bytes fail.');
})().catch(error => { console.error(error); process.exitCode = 1; });
