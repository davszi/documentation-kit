// Page lock: open a published page whose text the publish step encrypted.
// tooling/page_lock.py writes one lock page per HTML file, with the wrapped
// content keys and the sealed page inline. This script derives a key from the
// password (PBKDF2-HMAC-SHA-256), unwraps the content keys and decrypts the
// page (AES-256-GCM) through WebCrypto, then replaces the document so the
// kit's components start exactly as on a normal load. For a reader with the
// reference password it also opens the sealed Reference tree and puts the
// sidebar's Reference section back into pages that the general password opens.
// The tab keeps this publish's content keys in sessionStorage. A reader who
// asks to be remembered keeps the password's derived key in localStorage
// instead of the password; it opens later publishes until a password changes.
// Node's tests load the same functions.
(function () {
  'use strict';
  var FORMAT = 'docsite-lock/1';
  var NONCE = 12;
  var KEY = 32;
  var TREE = 'reference.tree.js';
  var LOCKED_TREE = 'docsLockedReferenceTree';
  var encoder = new TextEncoder();

  function fromBase64(text) {
    var binary = atob(String(text).replace(/\s+/g, ''));
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes;
  }

  function toBase64(bytes) {
    var binary = '';
    for (var i = 0; i < bytes.length; i += 0x8000) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    return btoa(binary);
  }

  function subtle() {
    var api = typeof crypto !== 'undefined' && crypto.subtle;
    if (!api) throw new Error('WebCrypto is unavailable');
    return api;
  }

  function isWrongKey(error) {
    return !!error && error.name === 'OperationError';
  }

  async function open(raw, sealed, context) {
    if (sealed.length < NONCE + 16) throw new Error('Sealed data is truncated');
    var key = await subtle().importKey('raw', raw, {name: 'AES-GCM'}, false, ['decrypt']);
    var plain = await subtle().decrypt({name: 'AES-GCM', iv: sealed.subarray(0, NONCE),
      additionalData: encoder.encode(context)}, key, sealed.subarray(NONCE));
    return new Uint8Array(plain);
  }

  async function deriveKey(password, kdf) {
    if (kdf.name !== 'PBKDF2' || kdf.hash !== 'SHA-256') throw new Error('Unsupported key derivation');
    var material = await subtle().importKey('raw', encoder.encode(password.normalize('NFC')),
      'PBKDF2', false, ['deriveBits']);
    var bits = await subtle().deriveBits({name: 'PBKDF2', hash: 'SHA-256', salt: fromBase64(kdf.salt),
      iterations: kdf.iterations}, material, KEY * 8);
    return new Uint8Array(bits);
  }

  // The level and content keys a password's derived key opens, or null.
  async function openSlots(wrapping, header) {
    if (!header || header.format !== FORMAT) throw new Error('Unsupported lock format');
    for (var i = 0; i < header.slots.length; i++) {
      var plain;
      try {
        plain = await open(wrapping, fromBase64(header.slots[i]), FORMAT + ' keys ' + header.id);
      } catch (error) {
        if (isWrongKey(error)) continue;
        throw error;
      }
      var level = plain[0];
      if ((level !== 1 && level !== 2) || plain.length !== 1 + level * KEY) throw new Error('Malformed key slot');
      var keys = {};
      for (var n = 1; n <= level; n++) keys[n] = plain.slice(1 + (n - 1) * KEY, 1 + n * KEY);
      return {level: level, keys: keys};
    }
    return null;
  }

  // The derived key, level and content keys this password opens, or null for a wrong one.
  async function unlock(password, header) {
    if (!header || header.format !== FORMAT) throw new Error('Unsupported lock format');
    var wrapping = await deriveKey(password, header.kdf);
    var result = await openSlots(wrapping, header);
    if (result) result.wrapping = wrapping;
    return result;
  }

  function fileContext(path) { return FORMAT + ' file ' + path; }

  function openFile(raw, path, sealed) { return open(raw, sealed, fileContext(path)); }

  // The sealed Reference tree and section, from the base64 that reference.tree.js sets.
  async function openTree(raw, sealedBase64) {
    var plain = await openFile(raw, TREE, fromBase64(sealedBase64));
    return JSON.parse(new TextDecoder('utf-8').decode(plain));
  }

  // A sealed page ends with one 0x80 byte and zero bytes of padding.
  function unpad(plain) {
    var end = plain.length;
    while (end > 0 && plain[end - 1] === 0) end--;
    if (end === 0 || plain[end - 1] !== 0x80) throw new Error('Malformed page padding');
    return plain.subarray(0, end - 1);
  }

  // A page as built: the publish step cut its Reference section out at byte `at`.
  function joinSection(plain, at, section) {
    var decoder = new TextDecoder('utf-8');
    if (at === null || typeof section !== 'string') return decoder.decode(plain);
    return decoder.decode(plain.subarray(0, at)) + section + decoder.decode(plain.subarray(at));
  }

  // Locked text files: a readable notice, a marker line, the sealed file in base64.
  function parseEnvelope(text) {
    var match = /^docsite-lock\/1 level ([12])\r?\n([A-Za-z0-9+\/=]+)\s*$/m.exec(text);
    return match ? {level: Number(match[1]), sealed: fromBase64(match[2])} : null;
  }

  var api = {FORMAT: FORMAT, unlock: unlock, openSlots: openSlots, openFile: openFile, openTree: openTree,
    unpad: unpad, joinSection: joinSection, parseEnvelope: parseEnvelope, fileContext: fileContext,
    fromBase64: fromBase64, toBase64: toBase64};
  if (typeof module === 'object' && module && module.exports) { module.exports = api; return; }
  if (typeof document === 'undefined') return;

  var shell = document.getElementById('page-lock');
  if (!shell) return;
  var header = JSON.parse(document.getElementById('page-lock-keys').textContent);
  var pageLevel = Number(shell.getAttribute('data-level'));
  var sectionAt = shell.hasAttribute('data-section-at') ? Number(shell.getAttribute('data-section-at')) : null;
  // The host serves the site's 404.html at every missing address.
  var notFound = shell.hasAttribute('data-not-found');
  var siteRoot = new URL(shell.getAttribute('data-root'), location.href);
  var storageKey = 'docsite-lock:' + siteRoot.pathname;
  var form = document.getElementById('page-lock-form');
  var input = document.getElementById('page-lock-password');
  var remember = document.getElementById('page-lock-remember');
  var message = document.getElementById('page-lock-message');
  var status = document.getElementById('page-lock-status');
  var submit = form.querySelector('button');

  function say(text) { status.textContent = text; }
  function explain(text) { message.textContent = text; message.hidden = !text; }

  // Bundle paths this URL may serve: static hosts also serve page.html at
  // /page and a folder's index.html at the folder's URL.
  function sitePaths(url) {
    if (url.protocol !== siteRoot.protocol || url.host !== siteRoot.host) return [];
    if (url.pathname.indexOf(siteRoot.pathname) !== 0) return [];
    var path;
    try { path = decodeURIComponent(url.pathname.slice(siteRoot.pathname.length)); } catch (error) { return []; }
    if (!path || path.charAt(path.length - 1) === '/') return [path + 'index.html'];
    return /\.[A-Za-z0-9]+$/.test(path) ? [path] : [path, path + '.html'];
  }

  function store(persistent) {
    try { return persistent ? localStorage : sessionStorage; } catch (error) { return null; }
  }

  function read(persistent) {
    var where = store(persistent);
    try { return where && JSON.parse(where.getItem(storageKey) || 'null'); } catch (error) { return null; }
  }

  function write(persistent, value) {
    var where = store(persistent);
    try { if (where) { if (value) where.setItem(storageKey, JSON.stringify(value)); else where.removeItem(storageKey); } }
    catch (error) { /* storage blocked */ }
  }

  function decodeKey(text) {
    var key = fromBase64(text);
    if (key.length !== KEY) throw new Error('malformed');
    return key;
  }

  // This publish's content keys, kept for the tab.
  function readSession() {
    var value = read(false);
    // Keys of another publish are ignored, not deleted: a page from a cache may be older than the keys.
    if (!value || value.id !== header.id) return null;
    try {
      if (value.level !== 1 && value.level !== 2) throw new Error('damaged');
      var keys = {};
      for (var n = 1; n <= value.level; n++) keys[n] = decodeKey(value.keys[n]);
      return {level: value.level, keys: keys};
    } catch (error) {
      write(false, null);
      return null;
    }
  }

  // A remembered password key; a new salt means a password changed.
  function readRemembered() {
    var value = read(true);
    if (!value) return null;
    try {
      if (value.salt !== header.kdf.salt) throw new Error('password changed');
      return decodeKey(value.wrapping);
    } catch (error) {
      write(true, null);
      return null;
    }
  }

  function keep(result, persistent) {
    var keys = {};
    for (var n = 1; n <= result.level; n++) keys[n] = toBase64(result.keys[n]);
    write(false, {id: header.id, level: result.level, keys: keys});
    if (persistent && result.wrapping) {
      write(true, {salt: header.kdf.salt, level: result.level, wrapping: toBase64(result.wrapping)});
    }
  }

  function showForm(text) {
    explain(text || '');
    form.hidden = false;
    submit.disabled = false;
    input.focus();
  }

  function needReference() {
    showForm('This page is in the Reference section and needs the reference password. ' +
      'The password you entered opens the other pages only.');
  }

  function notice(text) {
    var box = document.createElement('div');
    box.setAttribute('role', 'alert');
    box.style.cssText = 'position:fixed;left:16px;right:16px;bottom:16px;z-index:2000;max-width:36rem;margin:auto;' +
      'padding:12px 16px;border-radius:10px;background:#161b22;color:#e6edf3;border:1px solid #f0883e;' +
      'font:15px/1.5 system-ui,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.5)';
    box.textContent = text + ' ';
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = 'Close';
    close.addEventListener('click', function () { box.remove(); });
    box.appendChild(close);
    document.body.appendChild(box);
  }

  // Markdown files are locked too; open them from an unlocked page as text.
  function markdownLinks(keys) {
    return function (event) {
      if (event.defaultPrevented || event.button !== 0 || event.altKey) return;
      var link = event.target && event.target.closest ? event.target.closest('a[href]') : null;
      if (!link || link.hasAttribute('download')) return;
      var url = new URL(link.href, location.href);
      var paths = sitePaths(url);
      if (!paths.length || !/\.(?:md|markdown)$/i.test(paths[0])) return;
      event.preventDefault();
      var elsewhere = event.ctrlKey || event.metaKey || event.shiftKey || link.target === '_blank';
      var view = elsewhere ? window.open('', '_blank') : null;
      fetch(url.href).then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.text();
      }).then(function (text) {
        var envelope = parseEnvelope(text);
        if (!envelope) return url.href;
        if (!keys[envelope.level]) {
          notice('This file needs the reference password. Open a page in the Reference section to enter it.');
          return null;
        }
        return openFile(keys[envelope.level], paths[0], envelope.sealed).then(function (plain) {
          return URL.createObjectURL(new Blob([plain], {type: 'text/plain;charset=utf-8'})) + url.hash;
        });
      }).then(function (target) {
        if (!target) { if (view) view.close(); return; }
        if (view) view.location.href = target; else location.assign(target);
      }).catch(function () {
        if (view) view.close();
        location.assign(url.href);
      });
    };
  }

  // The sealed Reference tree, loaded through a <script> element, which works
  // from disk too; a missing or unreadable tree only leaves the section out.
  function loadTree(raw) {
    return new Promise(function (resolve) {
      if (typeof window[LOCKED_TREE] === 'string') { resolve(window[LOCKED_TREE]); return; }
      var script = document.createElement('script');
      script.src = new URL(TREE + '?v=' + encodeURIComponent(header.tree || ''), siteRoot).href;
      script.onload = function () { resolve(window[LOCKED_TREE]); };
      script.onerror = function () { resolve(null); };
      document.head.appendChild(script);
    }).then(function (sealed) {
      return typeof sealed === 'string' ? openTree(raw, sealed) : null;
    }).catch(function () { return null; });
  }

  // Keys that opened this publish's slots but not this page mean the page is
  // served at an address it was not sealed for: keep the keys and say so.
  function wrongAddress() {
    say('');
    explain('This address does not match the page it holds, so the page cannot be opened here.');
    var home = document.createElement('a');
    home.href = siteRoot.href;
    home.textContent = 'Open the home page';
    var line = document.createElement('p');
    line.className = 'page-lock-text';
    line.appendChild(home);
    message.insertAdjacentElement('afterend', line);
    form.hidden = true;
  }

  // True once the page is shown; false when this address does not match the page.
  async function reveal(keys) {
    var reference = keys[2] ? loadTree(keys[2]) : Promise.resolve(null);
    var sealed = fromBase64(document.getElementById('page-lock-data').textContent);
    var candidates = notFound ? ['404.html'] : sitePaths(new URL(location.href));
    var plain = null;
    for (var i = 0; i < candidates.length && !plain; i++) {
      try { plain = await openFile(keys[pageLevel], candidates[i], sealed); } catch (error) {
        if (!isWrongKey(error)) throw error;
      }
    }
    if (!plain) return false;
    plain = unpad(plain);
    var tree = await reference;
    // nav.js reads the folder tree from here before it would load reference.tree.js.
    if (tree && typeof tree.tree === 'string') window.docsReferenceTree = tree.tree;
    var markup = joinSection(plain, pageLevel === 1 ? sectionAt : null, tree && tree.section);
    // Replace the document: its scripts run and DOMContentLoaded fires again,
    // so every component starts as on a normal load of the page.
    document.open();
    document.addEventListener('click', markdownLinks(keys));
    window.addEventListener('load', function () {
      var id = location.hash.slice(1);
      if (!id || document.querySelector(':target')) return;
      var target;
      try { target = document.getElementById(decodeURIComponent(id)); } catch (error) { return; }
      if (target) target.scrollIntoView();
    });
    document.write(markup);
    document.close();
    return true;
  }

  async function start() {
    if (typeof crypto === 'undefined' || !crypto.subtle) {
      explain('This browser cannot unlock the page on this connection. Open the site over HTTPS.');
      return;
    }
    // Session keys belong to this publish (readSession checks its id), and a
    // remembered key has just opened its slots, so a page that still does not
    // open is at the wrong address; the keys stay.
    var session = readSession();
    if (session && session.keys[pageLevel]) {
      say('Unlocking…');
      if (!(await reveal(session.keys))) wrongAddress();
      return;
    }
    var wrapping = readRemembered();
    var remembered = wrapping && await openSlots(wrapping, header);
    if (wrapping && !remembered) write(true, null);
    if (remembered && (!session || remembered.level > session.level)) {
      keep(remembered, false);
      session = remembered;
      if (remembered.level >= pageLevel) {
        say('Unlocking…');
        if (!(await reveal(remembered.keys))) wrongAddress();
        return;
      }
    }
    if (session) needReference(); else showForm('Enter the password to read this page.');
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var password = input.value;
    if (!password) return;
    submit.disabled = true;
    say('Unlocking…');
    unlock(password, header).then(function (result) {
      input.value = '';
      if (!result) {
        submit.disabled = false;
        say('That password did not unlock this site. Check it and try again.');
        input.focus();
        return null;
      }
      keep(result, remember.checked);
      if (result.level < pageLevel) { say(''); needReference(); return null; }
      return reveal(result.keys).then(function (shown) {
        if (!shown) wrongAddress();
      });
    }).catch(function () {
      submit.disabled = false;
      say('This page could not be opened in this browser.');
    });
  });

  // What a page serves never deletes stored keys; only a new publish or a
  // changed password makes them stale, and readSession and readRemembered
  // drop those.
  function begin() {
    start().catch(function () {
      say('');
      showForm('This page could not be opened with the saved key. Enter the password again.');
    });
  }
  // Replace the lock page only after it has finished parsing.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', begin); else begin();
})();
