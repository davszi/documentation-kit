// Page lock: open a published page whose text the publish step encrypted.
// tooling/page_lock.py writes one lock page per HTML file, with the wrapped
// content keys and the sealed page inline. This script derives a key from the
// password (PBKDF2-HMAC-SHA-256), unwraps the content keys and decrypts the
// page (AES-256-GCM) through WebCrypto, then replaces the document so the
// kit's components start exactly as on a normal load. Content keys, never the
// password, stay in sessionStorage, or in localStorage when the reader asks
// to be remembered on this device. Node's tests load the same functions.
(function () {
  'use strict';
  var FORMAT = 'docsite-lock/1';
  var NONCE = 12;
  var KEY = 32;
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

  // The level and content keys this password opens, or null for a wrong one.
  async function unlock(password, header) {
    if (!header || header.format !== FORMAT) throw new Error('Unsupported lock format');
    var wrapping = await deriveKey(password, header.kdf);
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

  function fileContext(path) { return FORMAT + ' file ' + path; }

  function openFile(raw, path, sealed) { return open(raw, sealed, fileContext(path)); }

  // Locked text files: a readable notice, a marker line, the sealed file in base64.
  function parseEnvelope(text) {
    var match = /^docsite-lock\/1 level ([12])\r?\n([A-Za-z0-9+\/=]+)\s*$/m.exec(text);
    return match ? {level: Number(match[1]), sealed: fromBase64(match[2])} : null;
  }

  var api = {FORMAT: FORMAT, unlock: unlock, openFile: openFile, parseEnvelope: parseEnvelope,
    fileContext: fileContext, fromBase64: fromBase64, toBase64: toBase64};
  if (typeof module === 'object' && module && module.exports) { module.exports = api; return; }
  if (typeof document === 'undefined') return;

  var shell = document.getElementById('page-lock');
  if (!shell) return;
  var header = JSON.parse(document.getElementById('page-lock-keys').textContent);
  var pageLevel = Number(shell.getAttribute('data-level'));
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

  function stores(persistent) {
    var list = [];
    try { list.push(sessionStorage); } catch (error) { /* storage blocked */ }
    if (persistent) { try { list.push(localStorage); } catch (error) { /* storage blocked */ } }
    return list;
  }

  function forget() {
    stores(true).forEach(function (store) { try { store.removeItem(storageKey); } catch (error) { /* blocked */ } });
  }

  function readStored() {
    var found = null;
    stores(true).forEach(function (store) {
      var value;
      try { value = JSON.parse(store.getItem(storageKey) || 'null'); } catch (error) { value = null; }
      if (!value) return;
      var keys = {};
      try {
        if (value.id !== header.id || (value.level !== 1 && value.level !== 2)) throw new Error('stale');
        for (var n = 1; n <= value.level; n++) {
          keys[n] = fromBase64(value.keys[n]);
          if (keys[n].length !== KEY) throw new Error('malformed');
        }
      } catch (error) {
        // A key from an earlier publish, or damaged: drop it and ask again.
        try { store.removeItem(storageKey); } catch (blocked) { /* blocked */ }
        return;
      }
      if (!found || value.level > found.level) found = {level: value.level, keys: keys};
    });
    return found;
  }

  function keep(result, persistent) {
    var keys = {};
    for (var n = 1; n <= result.level; n++) keys[n] = toBase64(result.keys[n]);
    var value = JSON.stringify({id: header.id, level: result.level, keys: keys});
    stores(persistent).forEach(function (store) { try { store.setItem(storageKey, value); } catch (error) { /* blocked */ } });
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

  async function reveal(keys) {
    var sealed = fromBase64(document.getElementById('page-lock-data').textContent);
    var candidates = sitePaths(new URL(location.href));
    var plain = null;
    for (var i = 0; i < candidates.length && !plain; i++) {
      try { plain = await openFile(keys[pageLevel], candidates[i], sealed); } catch (error) {
        if (!isWrongKey(error)) throw error;
      }
    }
    if (!plain) return false;
    var markup = new TextDecoder('utf-8').decode(plain);
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
    var stored = readStored();
    if (stored && stored.keys[pageLevel]) {
      say('Unlocking…');
      if (await reveal(stored.keys)) return;
      forget();
      say('');
      showForm('The saved key no longer opens this page. Enter the password again.');
      return;
    }
    if (stored) needReference(); else showForm('Enter the password to read this page.');
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
        if (!shown) { submit.disabled = false; say('This page could not be opened. Reload it and try again.'); }
      });
    }).catch(function () {
      submit.disabled = false;
      say('This page could not be opened in this browser.');
    });
  });

  function begin() {
    start().catch(function () {
      forget();
      say('');
      showForm('This page could not be opened with the saved key. Enter the password again.');
    });
  }
  // Replace the lock page only after it has finished parsing.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', begin); else begin();
})();
