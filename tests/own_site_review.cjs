// Optional real-browser review of the kit's own reference website (.build/docs).
// Build it first: python docsite.py build --project .
// Run as one owned, serialized local job; screenshots go to .build/visual-review/own-site/.
const { chromium } = require(process.env.DOCS_PLAYWRIGHT || 'playwright');
const fs = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const assert = require('node:assert/strict');
const {settle, checkLayout} = require('../tooling/browser_checks.cjs');
const kit = path.resolve(__dirname, '..');
const root = path.join(kit, '.build/docs');
const output = path.join(kit, '.build/visual-review/own-site');
const mime = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml',
  '.woff2':'font/woff2','.png':'image/png','.json':'application/json'};
const server = http.createServer(async (req,res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    if(pathname==='/favicon.ico') {res.statusCode=204;res.end();return;}
    const file = path.resolve(root,'.'+pathname);
    if (!file.startsWith(root+path.sep)) throw Error('outside output');
    res.setHeader('Content-Type', mime[path.extname(file)] || 'application/octet-stream');
    res.end(await fs.readFile(file));
  } catch {res.statusCode=404;res.end('Not found');}
});
const SHOTS = ['index', 'getting-started', 'commands', 'site-toolkit', 'git', 'releases', 'readme'];

(async () => {
  await fs.mkdir(output,{recursive:true});
  const manifest = JSON.parse(await fs.readFile(path.join(root,'site-build.json'),'utf8'));
  const pages = manifest.public_pages.filter(name => /^html\/[^/]+\.html$/.test(name)).map(name => name.slice(5, -5));
  for (const required of ['git', 'documentation-system', 'authoring', 'reader', 'panel-switcher', 'releases', 'migrate-1-1-0'])
    assert.ok(pages.includes(required), 'missing required page ' + required);
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({headless:true, executablePath:process.env.DOCS_CHROMIUM || undefined});
  const results = {pages: pages.length, viewports: {}};
  try {
    for (const viewport of [{width:1600,height:1000},{width:390,height:844}]) {
      const context = await browser.newContext({viewport, reducedMotion:'reduce'});
      const page = await context.newPage();
      const failures = [];
      page.on('pageerror', error => failures.push(error.message));
      page.on('console', message => { if (message.type() === 'error') failures.push(message.text()); });
      page.on('response', response => { if (response.status() >= 400) failures.push(response.url() + ': ' + response.status()); });
      let images = 0;
      for (const slug of pages) {
        await page.goto(`${origin}/html/${slug}.html`, {waitUntil:'networkidle'});
        const layout = await checkLayout(page);
        images += layout.images.length || 0;
        if (SHOTS.includes(slug)) await page.screenshot({path: path.join(output, `${viewport.width}-${slug}.png`), fullPage: slug === 'index'});
      }
      assert.deepEqual(failures, [], 'browser errors at ' + viewport.width);

      // Deep links into rendered Markdown anchors land on their heading.
      await page.goto(`${origin}/html/releases.html#100--first-stable-version`, {waitUntil:'networkidle'});
      await settle(page);
      // Fonts can shift layout after the first fragment scroll; the browser re-anchors.
      const landed = await page.waitForFunction(() => {
        const top = document.getElementById('100--first-stable-version').getBoundingClientRect().top;
        return top >= -2 && top < 200 ? top : false;
      }, null, {timeout: 5000}).then(handle => handle.jsonValue(), () => null);
      assert.ok(landed !== null, 'deep link target near top: ' +
        await page.evaluate(() => document.getElementById('100--first-stable-version').getBoundingClientRect().top));

      // A hash into an adoption route reveals that panel.
      await page.goto(`${origin}/html/getting-started.html#route-existing`, {waitUntil:'networkidle'});
      await settle(page);
      assert.equal(await page.locator('#route-existing').isVisible(), true);
      assert.equal(await page.locator('#route-new').isVisible(), false);

      // Keyboard: the home paths are reachable by Tab and show focus.
      await page.goto(`${origin}/html/index.html`, {waitUntil:'networkidle'});
      let reached = null;
      for (let step = 0; step < 80 && !reached; step++) {
        await page.keyboard.press('Tab');
        reached = await page.evaluate(() => document.activeElement?.classList.contains('now-card')
          ? {href: document.activeElement.getAttribute('href'), outline: getComputedStyle(document.activeElement).outlineStyle,
             shadow: getComputedStyle(document.activeElement).boxShadow} : null);
      }
      assert.ok(reached, 'a home path card is reachable by keyboard');
      assert.ok(reached.outline !== 'none' || reached.shadow !== 'none', 'focused path card is visibly marked');

      // Pages for people use the chapter reader; rendered records are plain reference pages.
      const peoplePages = ['getting-started', 'reader-tour', 'commands', 'engineering-practices',
                           'writing-practices', 'experiments', 'site-toolkit'];
      for (const slug of pages.filter(slug => slug !== 'index')) {
        await page.goto(`${origin}/html/${slug}.html`, {waitUntil:'networkidle'});
        const chapters = await page.locator('section.card[data-reader-chapter]').count();
        if (peoplePages.includes(slug)) assert.ok(chapters > 0, slug + ' has reader chapters');
        else {
          assert.equal(chapters, 0, slug + ' is a plain reference page');
          assert.equal(await page.locator('.source-origin').first().isVisible(), true, slug + ' shows its source line');
        }
      }
      await page.goto(`${origin}/html/site-toolkit.html`, {waitUntil:'networkidle'});
      if (viewport.width >= 900) {
        // The reader stage uses the content width; no line-length cap leaves the right side blank.
        const stage = await page.evaluate(() => ({card: document.querySelector('section.card[data-reader-chapter]').getBoundingClientRect().width,
                                                  main: document.querySelector('main.content').getBoundingClientRect().width}));
        assert.ok(stage.card > 0.8 * stage.main, 'reader card fills the stage: ' + JSON.stringify(stage));
        await page.click('button[data-reader-view="pair"]');
        assert.equal(await page.getAttribute('button[data-reader-view="pair"]', 'aria-pressed'), 'true', 'two-chapter view selectable');
        await page.click('button[data-reader-view="single"]');

        // Reader tour: docking, pinning and the carousel work as the tour describes.
        await page.goto(`${origin}/html/reader-tour.html#move-through-chapters`, {waitUntil:'networkidle'});
        const docked = () => page.evaluate(() => document.body.classList.contains('reader-nav-docked'));
        assert.equal(await docked(), true, 'navigation starts docked on wide screens');
        await page.click('.reader-drawer-close');
        assert.equal(await docked(), false, 'hiding undocks the navigation');
        await page.click('.reader-mobile-menu');
        assert.equal(await docked(), true, 'reopening docks it again');
        await page.click('button[data-reader-view="pair"]');
        await page.locator('section.card[data-reader-chapter] .chapter-pin').first().click();
        const inView = () => page.$$eval('section.card[data-reader-chapter]', cards => cards.filter(card => {
          const r = card.getBoundingClientRect(); return r.width > 0 && r.left >= 0 && r.right <= innerWidth + 1; }).map(card => card.id));
        await page.keyboard.press('ArrowRight');
        await page.keyboard.press('ArrowRight');
        await page.waitForFunction(() => document.getElementById('reading-layers')?.getBoundingClientRect().right > innerWidth
          || document.getElementById('figures')?.getBoundingClientRect().left >= 0, null, {timeout: 3000}).catch(() => {});
        await page.waitForTimeout(400);
        const shown = await inView();
        assert.ok(shown.includes('move-through-chapters') && !shown.includes('dock-and-pin'), 'pinned chapter holds while the other column moves: ' + shown);
        await page.click('button[data-reader-view="single"]');
        await page.goto(`${origin}/html/reader-tour.html#figures`, {waitUntil:'networkidle'});
        const slides = await page.$$eval('#figures .fig-carousel > img', imgs => imgs.filter(img => getComputedStyle(img).display !== 'none').length);
        assert.equal(slides, 1, 'carousel shows one capture at a time');
      }

      if (viewport.width < 900) {
        // The menu opens navigation over content; tables scroll inside their region.
        // Reader pages open navigation from the reader bar; reference pages from the shell menu.
        await page.goto(`${origin}/html/site-toolkit.html`, {waitUntil:'networkidle'});
        await page.click('.reader-mobile-menu');
        await page.waitForFunction(() => {
          const r = document.getElementById('sidebar').getBoundingClientRect();
          return r.right > 100 && r.left >= -1;
        });
        await page.goto(`${origin}/html/git.html`, {waitUntil:'networkidle'});
        await page.click('#menu');
        await page.waitForFunction(() => {
          const r = document.getElementById('sidebar').getBoundingClientRect();
          return r.right > 100 && r.left >= -1;
        });
        await page.goto(`${origin}/html/releases.html`, {waitUntil:'networkidle'});
        const region = page.locator('.scroll[role="region"]').first();
        const metrics = await region.evaluate(el => ({scroll: el.scrollWidth, client: el.clientWidth}));
        assert.ok(metrics.scroll > metrics.client, 'narrow release table scrolls in place: ' + JSON.stringify(metrics));
        await region.focus();
        await page.keyboard.press('ArrowRight');
        await page.waitForFunction(() => document.querySelector('.scroll[role="region"]').scrollLeft > 0);
      }

      // Print: every adoption route is visible and edit controls are hidden.
      await page.emulateMedia({media:'print'});
      await page.goto(`${origin}/html/getting-started.html`, {waitUntil:'networkidle'});
      for (const id of ['route-new', 'route-existing', 'route-practices'])
        assert.equal(await page.locator('#' + id).isVisible(), true, id + ' prints');
      await page.goto(`${origin}/html/git.html`, {waitUntil:'networkidle'});
      assert.equal(await page.locator('.source-origin-edit').isVisible(), false, 'edit link hidden in print');
      await page.emulateMedia({media:'screen'});
      results.viewports[viewport.width] = {pages: pages.length, visibleImages: images, keyboard: reached.href};
      await context.close();
    }

    // Without JavaScript: content, every adoption route and the source line stay readable.
    const context = await browser.newContext({viewport:{width:390,height:844}, javaScriptEnabled:false});
    const page = await context.newPage();
    await page.goto(`${origin}/html/getting-started.html`, {waitUntil:'load'});
    for (const id of ['route-new', 'route-existing', 'route-practices'])
      assert.equal(await page.locator('#' + id).isVisible(), true, id + ' readable without JavaScript');
    await page.goto(`${origin}/html/git.html`, {waitUntil:'load'});
    assert.equal(await page.locator('.source-origin').isVisible(), true);
    assert.ok((await page.locator('main').textContent()).includes('Commit messages'));
    const width = await page.evaluate(() => document.documentElement.scrollWidth);
    assert.ok(width <= 391, 'no horizontal page scroll without JavaScript: ' + width);
    await page.screenshot({path: path.join(output, '390-no-javascript-git.png')});
    await context.close();
    results.noJavaScript = 'passed';
  } finally {
    await browser.close();
    server.close();
  }
  await fs.writeFile(path.join(output, 'results.json'), JSON.stringify(results, null, 2) + '\n');
  console.log(`Own site: ${results.pages} pages contained with visible media at 1600 and 390; deep links, panel hash, keyboard paths, reader chapters, views, docking, pinning and carousel, narrow menu/table scrolling, print and no-JavaScript reading pass.`);
})().catch(error => { console.error(error); process.exitCode = 1; server.close(); });
