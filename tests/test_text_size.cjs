// Real-browser check that no text of the kit's theme renders below 11 px
// (rules/writing/pages.md): every page of the kit's own site (.build/docs) at a
// wide and a phone width, and one fixture with the theme's labels that the
// kit's pages do not use. Build first: python docsite.py build --project .
const {chromium} = require('../node_modules/playwright');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const assert = require('node:assert/strict');
const {smallText, setView, settle} = require('../tooling/browser_checks.cjs');

const kit = path.resolve(__dirname, '..');
const root = path.join(kit, '.build/docs');
const mime = {'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.png': 'image/png', '.json': 'application/json'};
const server = http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
  const file = path.resolve(root, '.' + pathname);
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    response.statusCode = 404; response.end('Not found'); return;
  }
  response.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
  response.end(fs.readFileSync(file));
});

// Labels of the theme that no page of the kit's site shows, put into a page that runs the reader:
// `BODY` goes into its open chapter and `NAV` into its sidebar.
const BODY = `<span class="badge">new</span><div class="owns"><span class="k">owns</span></div>
  <div class="callout inv">An invariant.</div><div class="callout redo">A settled point.</div>
  <table><tr><th>Head <code>code</code></th></tr></table><p><small>Small <code>code</code></small></p>
  <svg width="300" height="60" viewBox="0 0 300 60"><text class="s" x="20" y="20">s</text><text class="lab" x="60" y="20">lab</text>
    <text class="d-note" x="100" y="20">note</text><text class="d-lab" x="150" y="20">d-lab</text>
    <text class="dimt" x="200" y="20">dimt</text><text class="axt" x="250" y="20">axt</text></svg>`;
const NAV = `<details class="nav-section nav-section-fold" open><summary class="nav-group">Group</summary></details><div class="reader-chapter-list"><span class="reader-nav-group" data-part="1">Part</span>
  <a class="top" href="#a">Chapter</a><a class="reader-chapter-sub" href="#b"><span class="reader-jump-kind">figure</span></a></div>`;
const HOST = 'build-a-site.html';

(async () => {
  assert.ok(fs.existsSync(path.join(root, 'html/index.html')), 'Build the kit site first: python docsite.py build --project .');
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const names = fs.readdirSync(path.join(root, 'html')).filter(name => name.endsWith('.html')).sort();
  const browser = await chromium.launch({headless: true});
  try {
    const readerPages = new Set(), titleCards = [];
    for (const width of [1440, 390]) {
      const context = await browser.newContext({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      const page = await context.newPage();
      for (const name of names) {
        await page.goto(`${origin}/html/${name}`, {waitUntil: 'load'});
        // A drawing counts only while it is rendered: show every chapter and open every fold.
        if (await page.locator('[data-reader-view="full"]').count()) {
          await setView(page, 'full');
          readerPages.add(name);
        }
        await page.evaluate(() => { for (const fold of document.querySelectorAll('details')) fold.open = true; });
        const small = await smallText(page);
        assert.deepEqual(small.map(item => `${item.px} px, ${item.count}x in ${item.where}: "${item.text}"`), [],
          `Text below 11 px on ${name} at ${width} px`);
      }
      await page.goto(`${origin}/html/${HOST}`, {waitUntil: 'load'});
      await page.evaluate(([body, nav]) => {
        document.querySelector('[data-reader-chapter].topic-active .chapter-body').insertAdjacentHTML('beforeend', body);
        document.querySelector('#sidebar .toc').insertAdjacentHTML('beforeend', nav);
      }, [BODY, NAV]);
      const added = await page.evaluate(() => document.querySelectorAll('.badge, .owns .k, .callout, svg .dimt, .toc .reader-jump-kind').length);
      assert.ok(added >= 6, `The label fixture is on the page: ${added}`);
      const small = await smallText(page);
      assert.deepEqual(small, [], `Theme labels below 11 px at ${width} px: ${JSON.stringify(small)}`);
      // Inline code stops at 11 px in small text and keeps scaling on a slide face.
      await page.evaluate(() => document.querySelector('[data-reader-chapter].topic-active .chapter-body').insertAdjacentHTML('beforeend',
        '<p style="font-size:9px" data-probe="text">small <code>code</code></p>'
        + '<div data-slide-face><div class="slide-canvas" style="font-size:8px!important"><code data-probe="face">code</code></div></div>'));
      const sizes = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll('[data-probe] code, code[data-probe]')]
        .map(node => [node.closest('[data-probe]').dataset.probe, parseFloat(getComputedStyle(node).fontSize)])));
      assert.equal(sizes.text, 11, 'Inline code in 9 px text stops at 11 px');
      assert.ok(Math.abs(sizes.face - 0.88 * 8) < 0.01, `Inline code on a slide face keeps 0.88 em: ${sizes.face}`);
      // The title card of the Presentation view, which the reader builds only in that view.
      await setView(page, 'present');
      await settle(page);
      const card = await page.evaluate(() => { const node = document.querySelector('.present-title-eyebrow');
        return node && parseFloat(getComputedStyle(node).fontSize); });
      if (card !== null) assert.ok(card >= 10.95, `Presentation title eyebrow at ${width} px: ${card} px`);
      titleCards.push(card);
      await context.close();
    }
    // Between 720 and 916 px the card's 1.2cqi eyebrow would be below 11 px without its floor.
    const middle = await browser.newPage({viewport: {width: 800, height: 600}, reducedMotion: 'reduce'});
    await middle.goto(`${origin}/html/${HOST}`, {waitUntil: 'load'});
    await setView(middle, 'present');
    await settle(middle);
    const eyebrow = await middle.evaluate(() => parseFloat(getComputedStyle(document.querySelector('.present-title-eyebrow')).fontSize));
    assert.ok(eyebrow >= 10.95, `Presentation title eyebrow at 800 px: ${eyebrow} px`);
    titleCards.push(eyebrow);
    await middle.close();
    assert.ok(readerPages.size >= 5, `Reader pages were shown with all chapters: ${readerPages.size}`);
    console.log(`Verified text size: no text below 11 px on ${names.length} pages of the kit's site, ${readerPages.size} of them reader pages `
      + `shown with all chapters and every fold open, and in the theme's label fixture, at 1440 and 390 px; inline code stops at 11 px `
      + `and scales on a slide face; Presentation title eyebrow ${JSON.stringify(titleCards)} px at 1440, 390 and 800 px`);
  } finally {
    await browser.close();
    server.close();
  }
})().catch(error => { console.error(error); process.exit(1); });
