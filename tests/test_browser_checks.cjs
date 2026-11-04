/* Optional real-browser regression for the shared review helpers.
 * Run as one owned, serialized job; requires the same Playwright/Chromium
 * environment as visual_review.cjs. No site build or application runtime. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {chromium} = require(process.env.DOCS_PLAYWRIGHT || 'playwright');
const {visibleMedia, measureOverflow, assertHorizontalContainment, checkLayout, readerChecks} =
  require('../tooling/browser_checks.cjs');

const image = 'data:image/svg+xml,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect width="40" height="40" fill="blue"/></svg>');
const broken = 'data:image/png;base64,broken';

// Use the real reader source and controls, with one, two and three authored
// chapters. These fixtures check helper scope and boundary behavior without a
// site build or a mocked navigation implementation.
async function reviewSmallReaders(browser) {
  const components = path.join(__dirname, '../theme/components');
  const [controls, css, script] = await Promise.all(['chapter-reader.html',
    'chapter-reader.css', 'chapter-reader.js'].map(file => fs.readFile(path.join(components, file), 'utf8')));
  for (const count of [1, 2, 3]) {
    const context = await browser.newContext({viewport:{width:1600,height:1000}, reducedMotion:'reduce'});
    try {
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const url = `http://reader-fixture.test/reader-${count}.html`;
      const ids = Array.from({length:count}, (_, index) => `chapter-${index + 1}`);
      await page.route(url, route => route.fulfill({contentType:'text/html', body:`<!doctype html>
        <style>:root{--bg:#101720;--bg2:#19222d;--border:#334051;--text:#dce5ef;--muted:#bac5d5;--bright:#fff;--mono:monospace}
        *{box-sizing:border-box}body{margin:0}.layout{display:grid}.content{min-width:0}.card{padding:20px}
        ${css}</style><div id="backdrop" class="backdrop"></div><div class="layout">
        <aside id="sidebar" class="sidebar"><nav id="toc" class="toc">${ids.map(id => `<a href="#${id}">${id}</a>`).join('')}</nav></aside>
        <main class="content"><span data-reader-title="Small reader" data-reader-adapted hidden></span>${controls}
        ${ids.map(id => `<section class="card" id="${id}" data-reader-chapter><h2>${id}</h2><p>Readable chapter content.</p></section>`).join('')}
        </main></div><script>${script}</script>`}));
      await page.goto(url, {waitUntil:'load'});
      const scope = await readerChecks(page, {url, expectedChapters:count});
      assert.deepEqual(scope.chapterIds, ids);
      if (count === 1) {
        assert.equal(scope.skipped.length, 3, 'Impossible single-chapter interactions must be reported as skipped');
        assert.ok(scope.checked.includes('hash navigation reveals the only chapter'));
        assert.equal(scope.checked.includes('click next and previous chapter controls'), false);
      } else {
        assert.ok(scope.checked.includes('click next and previous chapter controls'));
        assert.ok(scope.checked.includes('hash navigation and browser back/forward restore chapters'));
        assert.ok(scope.checked.includes('two chapter arrangement and pinning preserve the held chapter'));
        if (count === 2) {
          assert.ok(scope.checked.includes('two chapter pinned navigation boundaries'));
          assert.equal(scope.skipped[0]?.label, 'pinned chapter navigation');
        } else {
          assert.ok(scope.checked.includes('pinned chapter navigation'));
          assert.deepEqual(scope.skipped, []);
        }
      }
      assert.deepEqual(errors, []);
    } finally {await context.close();}
  }
}

(async () => {
  const browser = await chromium.launch({headless:true,
    executablePath:process.env.DOCS_CHROMIUM || undefined});
  try {
    const page = await browser.newPage({viewport:{width:480,height:320}});
    await page.setContent(`<!doctype html><style>
      body {margin:0} img {width:40px;height:40px;position:absolute;left:0}
      #clip {position:absolute;left:10px;top:20px;width:300px;height:110px;overflow:auto}
      #inside {position:relative;width:900px;height:280px}
      #visible {top:0} #clipped {top:200px}
      #inactive {position:absolute;top:140px} #below {top:800px}
    </style><div id="clip"><div id="inside">
      <img id="visible" src="${image}" alt="Visible fixture">
      <img id="clipped" loading="lazy" src="${broken}" alt="Clipped broken fixture">
    </div></div>
    <div id="inactive" inert><img id="inactive-image" loading="lazy" src="${broken}" alt="Inactive fixture"></div>
    <img id="below" loading="lazy" src="${broken}" alt="Below viewport fixture">`);
    const initial = await checkLayout(page);
    assert.deepEqual(initial.images.map(item => item.id), ['visible'],
      'Inactive, below-viewport and fully clipped lazy images must not fail visible media');
    assert.equal(initial.overflow.rootOverflow, false,
      'Wide content belongs inside the local scroll region');

    // Bring the same broken lazy image into its clipping ancestor's visible
    // area. A check that uses only viewport rectangles would miss this change.
    await page.locator('#clip').evaluate(node => {node.scrollTop = 160;});
    await assert.rejects(() => visibleMedia(page, {timeout:300}),
      /Timeout|timeout/, 'A visible broken image must fail the media gate');
    await page.locator('#clipped').evaluate((node, source) => {node.src = source;}, image);
    assert.deepEqual((await visibleMedia(page)).map(item => item.id), ['clipped']);

    // A real root-level escape must fail; the intentional scroll region above
    // remains allowed. Keep this element vertically in the viewport.
    await page.evaluate(() => {
      const escape = document.createElement('div');
      escape.id = 'escape';
      escape.style.cssText = 'position:absolute;left:10px;top:180px;width:700px;height:40px';
      document.body.append(escape);
    });
    const overflow = await measureOverflow(page);
    assert.equal(overflow.rootOverflow, true);
    assert.ok(overflow.offenders.some(item => item.id === 'escape'));
    await assert.rejects(() => assertHorizontalContainment(page), /Root overflow/);
    await page.close();
    await reviewSmallReaders(browser);
    console.log('Verified shared browser helpers: one/two/three-chapter scope, clipped/inactive lazy media, visible broken media, contained scrolling, root overflow.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode = 1;});
