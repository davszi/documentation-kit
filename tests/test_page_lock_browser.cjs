// Real-browser check of the page lock on a published fixture with both levels.
// Publishes tests/page_lock_fixture.py's project with throwaway passwords,
// serves the bundle below a sub-path as GitHub Pages would (including
// extension-less page URLs) and drives Chromium through the reader's flow:
// the Reference tree per password, remembered readers across publishes,
// exported Markdown links with and without a source remote, and the reader's
// Presentation view after unlock. Run as one owned, serialized local job, like
// the other browser suites.
const {chromium} = require('../node_modules/playwright');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const {settle, activeChapter, assertHorizontalContainment, readerChecks} = require('../tooling/browser_checks.cjs');

const kit = path.resolve(__dirname, '..');
const python = process.env.DOCS_PYTHON || 'python3';
const output = path.join(kit, '.build/page-lock-review');
const MARKERS = {topic: 'TOPIC-MARKER-5e1f0c', widgets: 'WIDGETS-MARKER-7d20b9', frame: 'FRAME-MARKER-c41a83',
  reference: 'REFERENCE-MARKER-a93d27', markdown: 'MARKDOWN-MARKER-0b6e44', title: 'TITLE-MARKER-9f31aa',
  referenceFrame: 'REFFRAME-MARKER-3d7e52', notFound: 'NOT-FOUND-MARKER-81c0f4'};
// Addresses the server answers like GitHub Pages: a missing one gets 404.html,
// and moved.html serves guide.html's lock page at an address it was not sealed for.
const MISSING = 'no-such-page';
const throwaway = () => crypto.randomBytes(24).toString('base64url');
let general = throwaway();
const reference = throwaway();
const mime = {'.html': 'text/html; charset=utf-8', '.md': 'text/markdown; charset=utf-8', '.js': 'text/javascript',
  '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json'};

const work = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-kit-lock-browser-'));
// Served sub-paths; republishing points a sub-path at the new bundle.
const roots = {'/lock-fixture/': path.join(work, 'site-1'), '/lock-remote/': path.join(work, 'remote-site')};
const server = http.createServer((req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    const base = Object.keys(roots).find(prefix => pathname.startsWith(prefix));
    if (!base) { res.statusCode = pathname === '/favicon.ico' ? 204 : 404; res.end(); return; }
    const site = roots[base];
    let file = path.resolve(site, '.' + pathname.slice(base.length - 1));
    if (file !== site && !file.startsWith(site + path.sep)) throw Error('outside the bundle');
    if (file === path.join(site, 'moved.html')) file = path.join(site, 'guide.html');
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    // GitHub Pages serves page.html at /page as well, and 404.html at a missing address.
    if (!fs.existsSync(file) && fs.existsSync(file + '.html')) file += '.html';
    if (!fs.existsSync(file) && fs.existsSync(path.join(site, '404.html'))) {
      res.statusCode = 404;
      file = path.join(site, '404.html');
    }
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  } catch { res.statusCode = 404; res.end('Not found'); }
});

function publish(project, out, remote) {
  const printed = execFileSync(python, [path.join(kit, 'tests/page_lock_fixture.py'), 'publish',
    path.join(work, project), path.join(work, out), ...(remote ? [remote] : [])], {encoding: 'utf8',
    env: {...process.env, DOCSITE_GENERAL_PASSWORD: general, DOCSITE_REFERENCE_PASSWORD: reference}});
  assert.match(printed, /Page lock: the general password opens \d+ files/);
  assert.ok(!printed.includes(general) && !printed.includes(reference));
  return path.join(work, out);
}

async function unlockWith(page, password, {remember = false} = {}) {
  await page.locator('#page-lock-form').waitFor({state: 'visible'});
  await page.fill('#page-lock-password', password);
  if (remember) await page.check('#page-lock-remember');
  await page.click('#page-lock-form button[type=submit]');
}

async function waitUnlocked(page) {
  await page.waitForFunction(() => document.title !== 'Locked page' && !document.getElementById('page-lock'),
    null, {timeout: 20000});
  await page.waitForLoadState('load');
  await settle(page);
}

async function waitForm(page) {
  await page.locator('#page-lock-form').waitFor({state: 'visible', timeout: 20000});
}

// The sidebar's Reference section as a reader sees it, with the folder tree loaded.
async function referenceTree(page) {
  if (!(await page.locator('.toc .repo-tree').count())) return null;
  const all = page.locator('.toc details.repo-tree-all');
  if (!(await all.evaluate(node => node.open))) await all.locator(':scope > summary').click();
  await page.locator('.toc .repo-tree[data-repo-tree-ready]').waitFor({state: 'attached', timeout: 10000});
  return page.locator('.toc .repo-tree').evaluate(box => ({
    count: box.querySelector('.repo-tree-all > summary .repo-tree-count')?.textContent,
    files: [...box.querySelectorAll('a.repo-tree-file')].map(a => a.getAttribute('href')),
    current: [...box.querySelectorAll('a.repo-tree-file.current')].map(a => [a.getAttribute('href'), a.getAttribute('aria-current')]),
    text: box.textContent}));
}

(async () => {
  publish('project', 'site-1');
  publish('remote', 'remote-site', 'https://github.com/example/project');
  fs.mkdirSync(output, {recursive: true});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const url = (name, base = '/lock-fixture/') => origin + base + name;
  const browser = await chromium.launch({headless: true});
  const errors = [];
  const watch = page => {
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => {
      if (response.status() >= 400 && !response.url().includes(MISSING)) errors.push(response.url() + ': ' + response.status());
    });
    return page;
  };
  const results = {};
  try {
    // 1. A topic page: wrong password, then the general password; the reader works and no Reference shows.
    const context = await browser.newContext({viewport: {width: 1400, height: 900}, reducedMotion: 'reduce'});
    const page = watch(await context.newPage());
    await page.goto(url('guide.html'));
    await waitForm(page);
    assert.equal(await page.title(), 'Locked page');
    assert.equal(await page.getAttribute('meta[name=robots]', 'content'), 'noindex, nofollow, noarchive');
    assert.ok(!(await page.content()).includes(MARKERS.topic));
    await page.screenshot({path: path.join(output, '1400-lock.png')});
    await unlockWith(page, throwaway());
    await page.waitForFunction(() => /did not unlock/.test(document.getElementById('page-lock-status').textContent));
    const wrong = await page.textContent('#page-lock-status');
    assert.equal(wrong, 'That password did not unlock this site. Check it and try again.');
    await unlockWith(page, general);
    await waitUnlocked(page);
    let html = await page.content();
    assert.ok(html.includes(MARKERS.topic));
    for (const hidden of ['repo-tree', MARKERS.title, 'Browse by folder', 'notes.record.md.html', 'reference.index.html'])
      assert.ok(!html.includes(hidden), 'a general-password reader sees no Reference trace: ' + hidden);
    // The shared reader checks: chapters, next/previous, hash history, pair view and pinning.
    const reader = await readerChecks(page, {url: url('guide.html'), expectedChapters: 8});
    assert.ok(reader.checked.length >= 4, 'reader checks ran: ' + JSON.stringify(reader));
    const stored = await page.evaluate(() => JSON.stringify({session: {...sessionStorage}, local: {...localStorage}}));
    assert.ok(!stored.includes(general) && !stored.includes(reference), 'storage holds keys, never a password');
    assert.match(stored, /docsite-lock:\/lock-fixture\//);
    assert.ok(!/docsite-lock/.test(JSON.stringify(await page.evaluate(() => ({...localStorage})))),
      'nothing is remembered on the device without the choice');
    // Print shows every chapter of the unlocked page.
    await page.emulateMedia({media: 'print'});
    for (const id of ['pipeline', 'locked-detail']) assert.equal(await page.locator('#' + id).isVisible(), true, id + ' prints');
    await page.emulateMedia({media: 'screen'});
    results.topic = {chapters: reader.chapterIds.length, readerChecked: reader.checked, wrongPassword: wrong};

    // 2. Reference pages with the general password only: told plainly, automatic pages included.
    for (const name of ['rule.html', 'notes.record.md.html', 'reference.index.html']) {
      await page.goto(url(name));
      await waitForm(page);
      assert.match(await page.textContent('#page-lock-message'), /Reference section and needs the reference password/, name);
    }
    const lockedHtml = await page.content();
    assert.ok(!lockedHtml.includes(MARKERS.title) && !lockedHtml.includes(MARKERS.markdown));
    await page.goto(url('rule.html'));
    await waitForm(page);
    await page.screenshot({path: path.join(output, '1400-needs-reference.png')});
    // The general password again: the submit handler disables the button until the attempt ends.
    await unlockWith(page, general);
    await page.waitForFunction(() => !document.querySelector('#page-lock-form button').disabled
      && document.getElementById('page-lock-status').textContent === '');
    assert.match(await page.textContent('#page-lock-message'), /needs the reference password/);
    assert.ok(!(await page.content()).includes(MARKERS.reference));
    await unlockWith(page, reference);
    await waitUnlocked(page);
    assert.ok((await page.content()).includes(MARKERS.reference));
    // The reference password shows the whole tree with the current file marked.
    let tree = await referenceTree(page);
    assert.deepEqual(tree.current, [['rule.html', 'page']]);
    assert.ok(tree.files.includes('notes.record.md.html') && tree.text.includes(MARKERS.title), JSON.stringify(tree));
    assert.equal(Number(tree.count), tree.files.length);
    results.referenceTree = {files: tree.files.length, current: tree.current};

    // 3. The reference key opens the next page without asking; the tree is back on a general page;
    //    tabs, toggles, lightbox and frames work.
    await page.goto(url('widgets.html'));
    await waitUnlocked(page);
    assert.ok((await page.content()).includes(MARKERS.widgets));
    tree = await referenceTree(page);
    assert.ok(tree && tree.files.length === results.referenceTree.files && tree.current.length === 0, JSON.stringify(tree));
    await page.click('.ptab[data-ptab="1"]');
    assert.equal(await page.locator('.ptab-panel[data-ptab="1"]').isVisible(), true);
    assert.equal(await page.locator('.ptab-panel[data-ptab="0"]').isVisible(), false);
    const chips = page.locator('main .fig-chip');
    assert.equal(await chips.count(), 2, 'one chip per plot group');
    await chips.first().click();
    assert.equal(await page.locator('#tg-alpha--0').evaluate(el => el.style.display), 'none');
    await page.click('main img');
    await page.locator('.lb-overlay').waitFor({state: 'visible'});
    await page.keyboard.press('Escape');
    await page.locator('.lb-overlay').waitFor({state: 'detached'});
    const frame = page.frameLocator('iframe[title="Embedded frame"]');
    await frame.locator('p').waitFor({state: 'visible', timeout: 20000});
    assert.equal(await frame.locator('p').textContent(), MARKERS.frame);
    // Exported Markdown opens as text from a page without filelinks.js ...
    await page.click('main a[href$="record.md"]');
    await page.waitForURL(/^blob:/);
    assert.ok((await page.textContent('body')).includes(MARKERS.markdown));
    // ... and from the guide, which loads filelinks.js; without a remote its link stays local.
    await page.goto(url('guide.html#locked-detail'));
    await waitUnlocked(page);
    const local = page.locator('#locked-detail a', {hasText: 'the record source'});
    assert.equal(await local.getAttribute('href'), 'notes/record.md');
    await local.click();
    await page.waitForURL(/^blob:/);
    assert.ok((await page.textContent('body')).includes(MARKERS.markdown));
    results.widgets = {tabs: true, plotToggles: true, lightbox: true, frame: true, markdownWithAndWithoutFilelinks: true};
    await context.close();

    // 4. With a source remote, the exported Markdown link keeps its published address, as it does
    //    in the same page without the lock (the decrypted page is the plain page byte for byte):
    //    the exporter marks it data-repo-exported, so filelinks.js leaves it alone, and the lock
    //    tells this general-password reader that the Markdown needs the reference password.
    const remote = await browser.newContext({viewport: {width: 1400, height: 900}});
    const remotePage = watch(await remote.newPage());
    await remotePage.route('https://github.com/**', route => route.fulfill({contentType: 'text/plain', body: 'remote source'}));
    await remotePage.goto(url('guide.html#locked-detail', '/lock-remote/'));
    await unlockWith(remotePage, general);
    await waitUnlocked(remotePage);
    const remoteLink = remotePage.locator('#locked-detail a', {hasText: 'the record source'});
    const remoteHref = await remoteLink.getAttribute('href');
    assert.equal(remoteHref, 'notes/record.md');
    await remoteLink.click();
    await remotePage.locator('[role=alert]').waitFor({state: 'visible'});
    assert.match(await remotePage.textContent('[role=alert]'), /needs the reference password/);
    assert.ok(!remotePage.url().startsWith('https:'), remotePage.url());
    results.remoteMarkdownLink = remoteHref;
    await remote.close();

    // 5. Deep links with a fragment land on their target after unlock, also without the .html suffix,
    //    and a shared Presentation link opens its slide.
    const deep = await browser.newContext({viewport: {width: 1400, height: 900}, reducedMotion: 'reduce'});
    const deepPage = watch(await deep.newPage());
    await deepPage.goto(url('guide.html?view=present#evidence'));
    await unlockWith(deepPage, general);
    await waitUnlocked(deepPage);
    await deepPage.waitForFunction(() => document.querySelector('main.content')?.dataset.topicView === 'present'
      && document.querySelector('[data-reader-chapter].topic-active')?.id === 'evidence', null, {timeout: 10000});
    const present = await deepPage.evaluate(() => ({search: location.search, hash: location.hash,
      bar: !!document.querySelector('.present-bar:not([hidden])'),
      slide: !!document.querySelector('[data-reader-chapter].topic-active .present-slide')}));
    assert.deepEqual(present, {search: '?view=present', hash: '#evidence', bar: true, slide: true});
    await deepPage.keyboard.press('ArrowRight');
    await deepPage.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active')?.id === 'layers');
    // The same shared link on a new load opens without asking, from the tab's keys.
    await deepPage.goto(url('guide.html?view=present#slides'));
    await waitUnlocked(deepPage);
    await deepPage.waitForFunction(() => document.querySelector('main.content')?.dataset.topicView === 'present'
      && document.querySelector('[data-reader-chapter].topic-active')?.id === 'slides', null, {timeout: 10000});
    await deepPage.goto(url('guide.html#locked-detail'));
    await waitUnlocked(deepPage);
    await deepPage.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active')?.id === 'locked-detail');
    assert.equal(await activeChapter(deepPage), 'locked-detail');
    await deepPage.goto(url('widgets#far-heading'));
    await waitUnlocked(deepPage);
    // The browser scrolls to a fragment when the replaced document finishes loading.
    await deepPage.waitForFunction(() => {
      const box = document.getElementById('far-heading')?.getBoundingClientRect();
      return box && box.height > 0 && box.top >= 0 && box.top < innerHeight;
    }, null, {timeout: 10000}).catch(() => {});
    const far = await deepPage.locator('#far-heading').evaluate(el => {
      const box = el.getBoundingClientRect();
      return {top: Math.round(box.top), height: innerHeight, scrolled: Math.round(scrollY)};
    });
    assert.ok(far.scrolled > 1000 && far.top >= 0 && far.top < far.height, 'far heading in view: ' + JSON.stringify(far));
    await deepPage.goto(url('widgets.html#second-detail'));
    await waitUnlocked(deepPage);
    assert.equal(await deepPage.locator('.ptab-panel[data-ptab="1"]').isVisible(), true, 'the fragment opens its tab');
    // A level-1 reader is told that Markdown needs the reference password.
    await deepPage.goto(url('widgets.html'));
    await waitUnlocked(deepPage);
    await deepPage.click('main a[href$="record.md"]');
    await deepPage.locator('[role=alert]').waitFor({state: 'visible'});
    assert.match(await deepPage.textContent('[role=alert]'), /needs the reference password/);
    results.deepLinks = {present: 'evidence', reader: 'locked-detail', scroll: far, tab: 'second-detail'};
    await deep.close();

    // 6. Remember on this device: a new tab opens without asking, also after a new publish with the
    //    same passwords; a session-only tab asks again after that publish; a changed password locks
    //    the remembered reader out too.
    const device = await browser.newContext({viewport: {width: 1400, height: 900}});
    const tab = watch(await device.newPage());
    await tab.goto(url('rule.html'));
    await unlockWith(tab, reference, {remember: true});
    await waitUnlocked(tab);
    const remembered = await tab.evaluate(() => JSON.stringify({...localStorage}));
    assert.ok(/docsite-lock/.test(remembered) && !remembered.includes(reference) && !remembered.includes(general));
    const session = await browser.newContext({viewport: {width: 1400, height: 900}});
    const sessionTab = watch(await session.newPage());
    await sessionTab.goto(url('guide.html'));
    await unlockWith(sessionTab, general);
    await waitUnlocked(sessionTab);
    const next = watch(await device.newPage());
    await next.goto(url('index.html'));
    await waitUnlocked(next);
    assert.ok(await referenceTree(next), 'the remembered reference key brings the tree');
    // A frame that only a Reference page embeds opens for the reference password.
    await next.goto(url('framed.html'));
    await waitUnlocked(next);
    const referenceFrame = next.frameLocator('iframe[title="Reference frame"]');
    await referenceFrame.locator('p').waitFor({state: 'visible', timeout: 20000});
    assert.equal(await referenceFrame.locator('p').textContent(), MARKERS.referenceFrame);
    // The site's 404.html opens at a missing address; a page served at an address it was not
    // sealed for says so. Neither deletes the stored keys.
    const keysOf = tab => tab.evaluate(() => JSON.stringify({local: {...localStorage}, session: {...sessionStorage}}));
    const keysBefore = await keysOf(next);
    await next.goto(url(MISSING));
    await waitUnlocked(next);
    assert.ok((await next.content()).includes(MARKERS.notFound));
    await next.goto(url('moved.html'));
    await next.locator('#page-lock-message').waitFor({state: 'visible', timeout: 20000});
    assert.match(await next.textContent('#page-lock-message'), /This address does not match the page it holds/);
    assert.equal(await next.locator('#page-lock-form').isVisible(), false);
    assert.equal(await keysOf(next), keysBefore, 'a mismatched address keeps the keys');
    await next.goto(url('widgets.html'));
    await waitUnlocked(next);
    results.addresses = {notFound: 'opened', moved: 'told, keys kept', referenceFrame: 'opened at level 2'};
    roots['/lock-fixture/'] = publish('project', 'site-2');
    await next.goto(url('rule.html'));
    await waitUnlocked(next);
    await sessionTab.reload();
    await waitForm(sessionTab);
    general = throwaway();
    roots['/lock-fixture/'] = publish('project', 'site-3');
    const after = watch(await device.newPage());
    await after.goto(url('index.html'));
    await waitForm(after);
    assert.ok(!/docsite-lock/.test(await after.evaluate(() => JSON.stringify({...localStorage}))),
      'the stale remembered key is dropped');
    await unlockWith(after, general);
    await waitUnlocked(after);
    results.remember = {nextPublish: 'opened without asking', sessionOnly: 'asked again', passwordChanged: 'asked again'};
    await device.close();
    await session.close();

    // 7. Narrow lock page and the no-JavaScript fallback.
    const narrow = await browser.newContext({viewport: {width: 390, height: 844}});
    const narrowPage = watch(await narrow.newPage());
    await narrowPage.goto(url('rule.html'));
    await waitForm(narrowPage);
    await settle(narrowPage);
    await assertHorizontalContainment(narrowPage);
    await narrowPage.screenshot({path: path.join(output, '390-lock.png')});
    await narrow.close();
    const noScript = await browser.newContext({viewport: {width: 390, height: 844}, javaScriptEnabled: false});
    const plain = await noScript.newPage();
    await plain.goto(url('guide.html'));
    assert.match(await plain.evaluate(() => document.body.innerText), /Unlocking this page needs JavaScript/);
    assert.equal(await plain.locator('#page-lock-form').isVisible(), false);
    assert.ok(!(await plain.content()).includes(MARKERS.topic));
    await plain.screenshot({path: path.join(output, '390-no-javascript.png')});
    await noScript.close();

    assert.deepEqual(errors, []);
    console.log('Page lock browser flow passes: ' + JSON.stringify(results));
  } finally {
    await browser.close();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(work, {recursive: true, force: true});
  }
})().catch(error => { console.error(error); server.close(); process.exitCode = 1; });
