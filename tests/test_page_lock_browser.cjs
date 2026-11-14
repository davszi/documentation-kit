// Real-browser check of the page lock on a published fixture with both levels.
// Publishes tests/page_lock_fixture.py's project with throwaway passwords,
// serves the bundle below a sub-path as GitHub Pages would (including
// extension-less page URLs) and drives Chromium through the reader's flow.
// Run as one owned, serialized local job, like the other browser suites.
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
  reference: 'REFERENCE-MARKER-a93d27', markdown: 'MARKDOWN-MARKER-0b6e44'};
const throwaway = () => crypto.randomBytes(24).toString('base64url');
const general = throwaway();
const reference = throwaway();
const BASE = '/lock-fixture/';
const mime = {'.html': 'text/html; charset=utf-8', '.md': 'text/markdown; charset=utf-8', '.js': 'text/javascript',
  '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json'};

const work = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-kit-lock-browser-'));
const site = path.join(work, 'site');
const server = http.createServer((req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (!pathname.startsWith(BASE)) { res.statusCode = pathname === '/favicon.ico' ? 204 : 404; res.end(); return; }
    let file = path.resolve(site, '.' + pathname.slice(BASE.length - 1));
    if (file !== site && !file.startsWith(site + path.sep)) throw Error('outside the bundle');
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    // GitHub Pages serves page.html at /page as well.
    if (!fs.existsSync(file) && fs.existsSync(file + '.html')) file += '.html';
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    res.end(fs.readFileSync(file));
  } catch { res.statusCode = 404; res.end('Not found'); }
});

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

async function shellText(page) {
  return page.evaluate(() => document.body.innerText);
}

(async () => {
  const published = execFileSync(python, [path.join(kit, 'tests/page_lock_fixture.py'), 'publish',
    path.join(work, 'project'), site], {encoding: 'utf8',
    env: {...process.env, DOCSITE_GENERAL_PASSWORD: general, DOCSITE_REFERENCE_PASSWORD: reference}});
  assert.match(published, /Page lock: the general password opens \d+ files/);
  assert.ok(!published.includes(general) && !published.includes(reference));
  fs.mkdirSync(output, {recursive: true});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const url = name => origin + BASE + name;
  const browser = await chromium.launch({headless: true});
  const errors = [];
  const watch = page => {
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => { if (response.status() >= 400) errors.push(response.url() + ': ' + response.status()); });
    return page;
  };
  const results = {};
  try {
    // 1. A topic page: wrong password, then the general password; the reader works.
    const context = await browser.newContext({viewport: {width: 1400, height: 900}, reducedMotion: 'reduce'});
    const page = watch(await context.newPage());
    await page.goto(url('guide.html'));
    await page.locator('#page-lock-form').waitFor({state: 'visible'});
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
    assert.ok((await page.content()).includes(MARKERS.topic));
    assert.ok(!(await page.title()).includes('Locked'));
    // The shared reader checks: chapters, next/previous, hash history, pair view and pinning.
    const reader = await readerChecks(page, {url: url('guide.html'), expectedChapters: 8});
    const chapters = reader.chapterIds.length;
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
    results.topic = {chapters, readerChecked: reader.checked, readerSkipped: reader.skipped, wrongPassword: wrong};

    // 2. A Reference page with the general password only: told plainly, then the reference password.
    await page.goto(url('rule.html'));
    await page.locator('#page-lock-form').waitFor({state: 'visible'});
    const needs = await page.textContent('#page-lock-message');
    assert.match(needs, /Reference section and needs the reference password/);
    assert.ok(!(await page.content()).includes(MARKERS.reference));
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

    // 3. The reference key opens the next page without asking; tabs, toggles, lightbox and frames work.
    await page.goto(url('widgets.html'));
    await waitUnlocked(page);
    assert.ok((await page.content()).includes(MARKERS.widgets));
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
    // Exported Markdown opens as text from an unlocked page.
    await page.click('a[href$="record.md"]');
    await page.waitForURL(/^blob:/);
    assert.ok((await page.textContent('body')).includes(MARKERS.markdown));
    results.widgets = {tabs: true, plotToggles: true, lightbox: true, frame: true, markdown: true};
    await context.close();

    // 4. Deep links with a fragment land on their target after unlock, also without the .html suffix.
    const deep = await browser.newContext({viewport: {width: 1400, height: 900}, reducedMotion: 'reduce'});
    const deepPage = watch(await deep.newPage());
    await deepPage.goto(url('guide.html#locked-detail'));
    await unlockWith(deepPage, general);
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
    await deepPage.click('a[href$="record.md"]');
    await deepPage.locator('[role=alert]').waitFor({state: 'visible'});
    assert.match(await deepPage.textContent('[role=alert]'), /needs the reference password/);
    results.deepLinks = {reader: 'locked-detail', scroll: far, tab: 'second-detail'};
    await deep.close();

    // 5. Remember on this device: a new tab opens without asking; without the choice it asks again.
    for (const remember of [true, false]) {
      const device = await browser.newContext({viewport: {width: 1400, height: 900}});
      const tab = watch(await device.newPage());
      await tab.goto(url('guide.html'));
      await unlockWith(tab, general, {remember});
      await waitUnlocked(tab);
      const local = await tab.evaluate(() => JSON.stringify({...localStorage}));
      assert.equal(/docsite-lock/.test(local), remember);
      assert.ok(!local.includes(general));
      const next = watch(await device.newPage());
      await next.goto(url('index.html'));
      if (remember) {
        await waitUnlocked(next);
      } else {
        await next.locator('#page-lock-form').waitFor({state: 'visible'});
      }
      results['remember' + remember] = true;
      await device.close();
    }

    // 6. Narrow lock page and the no-JavaScript fallback.
    const narrow = await browser.newContext({viewport: {width: 390, height: 844}});
    const narrowPage = watch(await narrow.newPage());
    await narrowPage.goto(url('rule.html'));
    await narrowPage.locator('#page-lock-form').waitFor({state: 'visible'});
    await settle(narrowPage);
    await assertHorizontalContainment(narrowPage);
    await narrowPage.screenshot({path: path.join(output, '390-lock.png')});
    await narrow.close();
    const noScript = await browser.newContext({viewport: {width: 390, height: 844}, javaScriptEnabled: false});
    const plain = await noScript.newPage();
    await plain.goto(url('guide.html'));
    assert.match(await shellText(plain), /Unlocking this page needs JavaScript/);
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
