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
  const {header, again, changed, tree, files} = JSON.parse(output);
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

  // A remembered key opens a later publish with the same passwords, not one after a change.
  assert.equal(again.kdf.salt, header.kdf.salt);
  assert.notEqual(again.id, header.id);
  const later = await lock.openSlots(both.wrapping, again);
  assert.equal(later.level, 2);
  assert.notDeepEqual(later.keys[2], both.keys[2], 'each publish draws new content keys');
  assert.equal((await lock.openSlots(opened.wrapping, again)).level, 1);
  assert.notEqual(changed.kdf.salt, header.kdf.salt);
  assert.equal(await lock.openSlots(both.wrapping, changed), null, 'a changed password locks the reference reader out too');
  assert.equal(await lock.openSlots(opened.wrapping, changed), null);

  // The sealed Reference tree opens with the reference password's level-2 key only.
  const sealedTree = /window\.docsLockedReferenceTree = "([A-Za-z0-9+\/=]+)";/.exec(tree)[1];
  assert.equal(header.pack, 'deflate', 'the key header says that files are compressed before they are sealed');
  const reference_tree = await lock.openTree(both.keys[2], sealedTree, true);
  assert.deepEqual(reference_tree, {entry: '    <a class="open-work" href="open.html">Open work</a>\n',
    section: '\n<div class="repo-tree"></div>', tree: '<ul class="repo-tree-list"></ul>'});
  assert.ok(lock.fromBase64(sealedTree).length >= 65536, 'the tree is padded');
  await assert.rejects(lock.openTree(both.keys[1], sealedTree, true), {name: 'OperationError'});
  // The offset counts UTF-8 bytes: 14 for the opening tag and 2 for "ä".
  const joined = lock.joinSection(new TextEncoder().encode('<div id="toc">ä\n  </div>'), 16,
    '\n<div class="repo-tree"></div>');
  assert.equal(joined, '<div id="toc">ä\n<div class="repo-tree"></div>\n  </div>');
  // The Open work entry goes back at its own offset; at the same offset it stands before the section.
  const menu = new TextEncoder().encode('<div id="toc">\nä\n  </div>');
  assert.equal(lock.joinSection(menu, 17, '\n<i></i>', 15, '<a></a>\n'), '<div id="toc">\n<a></a>\nä\n<i></i>\n  </div>');
  assert.equal(lock.joinSection(menu, 15, '\n<i></i>', 15, '<a></a>\n'), '<div id="toc">\n<a></a>\n\n<i></i>ä\n  </div>');
  assert.equal(lock.joinSection(menu, null, null, 15, '<a></a>\n'), '<div id="toc">\n<a></a>\nä\n  </div>');
  // A reader without the reference tree gets the page as it was sealed.
  assert.equal(lock.joinSection(menu, 17, null, 15, null), '<div id="toc">\nä\n  </div>');
  assert.deepEqual(lock.unpad(new Uint8Array([60, 0x80, 0, 0])), new Uint8Array([60]));
  assert.deepEqual(lock.unpad(new Uint8Array([0x80, 0x80])), new Uint8Array([0x80]));
  assert.throws(() => lock.unpad(new Uint8Array([60, 0, 0])), /Malformed page padding/);

  let checked = 0;
  for (const file of files) {
    const plain = lock.fromBase64(file.plain);
    let sealed;
    // Every file is compressed before it is sealed; pages are padded after that.
    let read = data => lock.unpack(data);
    if (file.envelope) {
      const envelope = lock.parseEnvelope(file.envelope);
      assert.equal(envelope.level, file.level);
      sealed = envelope.sealed;
    } else {
      sealed = lock.fromBase64(file.sealed);
      read = data => lock.unpack(lock.unpad(data));
    }
    if (file.level === 2 && !file.envelope) assert.equal(sealed.length, 8192 + 28, 'a padded page has its fixed size');
    assert.deepEqual(await read(await lock.openFile(both.keys[file.level], file.path, sealed)), plain, file.path);
    if (file.level === 1) assert.deepEqual(await read(await lock.openFile(opened.keys[1], file.path, sealed)), plain);
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
    + header.kdf.iterations + ' PBKDF2 iterations; wrong passwords, moved paths and changed bytes fail; '
    + 'a remembered key opens the next publish until a password changes; the padded tree opens at level 2 only.');
})().catch(error => { console.error(error); process.exitCode = 1; });
