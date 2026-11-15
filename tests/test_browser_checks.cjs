/* Optional real-browser regression for the shared review helpers.
 * Run as one owned, serialized job; requires the same Playwright/Chromium
 * environment as visual_review.cjs. No site build or application runtime. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const {chromium} = require('../node_modules/playwright');
const {visibleMedia, measureOverflow, assertHorizontalContainment, checkLayout, readerChecks, captureElement,
  settle, slideFaces, assertSlideFaces} = require('../tooling/browser_checks.cjs');

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

// Slide faces with the real slide-face stylesheet: a stacked face at 390 px that overflows
// sideways, clips text or lets a part stick out is reported; a sound face reports nothing; the
// empty band is information only; a face the page does not show is not measured.
async function reviewSlideFaces(browser) {
  const css = await fs.readFile(path.join(__dirname, '../theme/components/slide-face.css'), 'utf8');
  const face = (id, main, extra = '') => `<section id="${id}"${extra}><div class="slide-face" data-slide-face><div class="slide-canvas">
    <p class="slide-eyebrow">Subject</p><p class="slide-title">A finding stated as a sentence</p>
    <div class="slide-main">${main}</div><p class="slide-scope">What the numbers cover</p></div></div></section>`;
  const sound = '<div class="slide-split"><div class="slide-tile"><b>One</b><p>Short text.</p></div>'
    + '<div class="slide-tile"><b>Two</b><p>Short text.</p></div></div>';
  const page = await browser.newPage({viewport:{width:390, height:844}});
  try {
    await page.setContent(`<!doctype html><style>body{margin:0;background:#101720;color:#dce5ef}main{padding:0 16px}${css}
      /* A page style the deck does not have: it pushes images on faces sideways. */
      #page-style img{margin-left:120px}</style><main>
      ${face('sound', sound)}
      ${face('wide', sound + '<div style="width:600px;height:20px;background:#335"></div>')}
      ${face('clipped', '<p style="height:14px;overflow:hidden;font-size:14px;line-height:20px">' + 'A long line of text that wraps. '.repeat(6) + '</p>')}
      ${face('outside', sound + '<div style="position:relative;left:-30px;width:40px;height:20px;background:#a33"></div>')}
      ${face('page-style', '<img alt="" style="display:block;width:300px;height:80px;background:#345" src="data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="80"/>') + '">', ' class="in-page"')}
      ${face('hidden', sound, ' style="display:none"')}
    </main>`);
    await settle(page);
    const rows = Object.fromEntries((await slideFaces(page)).map(row => [row.chapter, row]));
    assert.deepEqual(Object.keys(rows), ['sound', 'wide', 'clipped', 'outside', 'page-style', 'hidden']);
    assert.equal(rows.sound.shown, true);
    assert.equal(rows.sound.compact, true, 'A face narrower than 720 px stacks');
    assert.deepEqual(rows.sound.problems, [], 'A sound stacked face reports nothing: ' + JSON.stringify(rows.sound));
    assert.ok(rows.wide.sideways > 200 && rows.wide.problems.some(item => /overflows sideways/.test(item)),
      'Sideways overflow is reported: ' + JSON.stringify(rows.wide));
    assert.ok(rows.clipped.clipped.length === 1 && rows.clipped.problems.some(item => /^clips text "A long line/.test(item)),
      'Clipped text is reported: ' + JSON.stringify(rows.clipped));
    assert.ok(rows.outside.outside.some(item => item.part === 'div' && item.by >= 10),
      'A part outside the face is reported: ' + JSON.stringify(rows.outside));
    assert.ok(rows['page-style'].problems.length > 0, 'A page style that pushes a part out of the face is reported in the page: '
      + JSON.stringify(rows['page-style']));
    assert.deepEqual(rows.hidden, {chapter:'hidden', shown:false, problems:[]}, 'A face the page does not show is not measured');
    // `within` limits the rows; the assertion fails with every problem and passes on a sound face.
    assert.deepEqual((await slideFaces(page, {within:'#sound'})).map(row => row.chapter), ['sound']);
    await assertSlideFaces(page, {within:'#sound'});
    await assert.rejects(() => assertSlideFaces(page, {within:'#wide'}), /wide at \d+ px: overflows sideways/);
    await assert.rejects(() => assertSlideFaces(page, {within:'#hidden'}), /Expected at least 1 shown slide face/);

    // At a wide window the face keeps 16:9; the largest empty band is reported and fails nothing.
    await page.setViewportSize({width:1600, height:1000});
    await settle(page);
    const wide = Object.fromEntries((await slideFaces(page)).map(row => [row.chapter, row]));
    assert.equal(wide.sound.compact, false);
    assert.equal(wide.sound.fits, true);
    assert.ok(wide.sound.emptyBand > 150 && wide.sound.problems.length === 0,
      'A face with little on it reports a large empty band and no problem: ' + JSON.stringify(wide.sound));
    await page.evaluate(() => {
      document.querySelector('#sound .slide-main').insertAdjacentHTML('beforeend',
        '<div style="height:360px;background:#234"></div>');
    });
    const filled = (await slideFaces(page, {within:'#sound'}))[0];
    assert.ok(filled.emptyBand < wide.sound.emptyBand, 'Filling the canvas shrinks the empty band: ' + JSON.stringify(filled));
    return {stacked:Object.keys(rows).length, emptyBand:[wide.sound.emptyBand, filled.emptyBand]};
  } finally {await page.close();}
}

(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    await reviewSlideFaces(browser);
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
    await page.setContent(`<!doctype html><style>body{margin:0}#stage{height:120px;overflow:hidden}
      #chapter{height:100px;overflow:hidden}#chapter p{height:300px;margin:0}</style>
      <div id="stage"><section id="chapter"><div class="slide-face">face</div><p>long chapter</p></section></div>`);
    const shot = path.join(require('node:os').tmpdir(), `kit-capture-${process.pid}.png`);
    assert.equal((await captureElement(page, '#chapter', shot)).height, 100);
    const whole = await captureElement(page, '#chapter', shot, {unclip:true, hide:['.slide-face']});
    assert.equal(whole.height, 300, 'An unclipped capture shows the whole chapter without its hidden face');
    await fs.rm(shot, {force:true});
    await page.close();
    await reviewSmallReaders(browser);
    console.log('Verified shared browser helpers: stacked slide faces at 390 px (sideways overflow, clipped text, parts outside, page styles) and the empty band at 1600 px, one/two/three-chapter scope, clipped/inactive lazy media, visible broken media, contained scrolling, root overflow, element capture.');
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode = 1;});
