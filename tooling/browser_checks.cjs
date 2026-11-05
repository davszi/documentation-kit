/* Reusable Playwright checks. Callers own serving, routes, evidence and domain
 * assertions. No browser is imported or launched by this module. */
'use strict';
const assert = require('node:assert/strict');

async function settle(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
}

// Runs in the browser. Test actual viewport intersection after every clipping
// ancestor, rather than treating every loaded or inactive chapter as visible.
function visibleImageState({readyOnly, sampleLimit}) {
  const images = [...document.images].filter(image => {
    if (image.closest('[hidden], [inert]')) return false;
    const rect = image.getBoundingClientRect();
    let left = Math.max(0, rect.left), right = Math.min(innerWidth, rect.right);
    let top = Math.max(0, rect.top), bottom = Math.min(innerHeight, rect.bottom);
    for (let node = image; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden' || style.visibility === 'collapse'
          || Number(style.opacity) === 0) return false;
      if (node === image) continue;
      const box = node.getBoundingClientRect();
      if (/(auto|scroll|hidden|clip)/.test(style.overflowX)) {
        left = Math.max(left, box.left); right = Math.min(right, box.right);
      }
      if (/(auto|scroll|hidden|clip)/.test(style.overflowY)) {
        top = Math.max(top, box.top); bottom = Math.min(bottom, box.bottom);
      }
    }
    return right > left && bottom > top;
  });
  if (readyOnly) return images.every(image => image.complete && image.naturalWidth > 0);
  return images.slice(0, sampleLimit).map(image => ({id:image.id, src:image.getAttribute('src'),
    complete:image.complete, naturalWidth:image.naturalWidth}));
}

async function visibleMedia(page, {timeout = 10000, sampleLimit = 25} = {}) {
  // Do not eagerly load inactive/clipped lazy images to make this check pass.
  await page.waitForFunction(visibleImageState, {readyOnly:true, sampleLimit}, {timeout});
  return page.evaluate(visibleImageState, {readyOnly:false, sampleLimit});
}

async function measureOverflow(page) {
  return page.evaluate(() => {
    const viewport = innerWidth;
    const offenders = [];
    for (const element of document.querySelectorAll('body *')) {
      if (element.closest('[inert], [hidden]')) continue;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      if (!rect.width || !rect.height || style.visibility === 'hidden' || style.display === 'none') continue;
      if (rect.bottom <= 0 || rect.top >= innerHeight || rect.right <= 0 || rect.left >= viewport) continue;
      if (rect.left >= -2 && rect.right <= viewport + 2) continue;
      let contained = false;
      for (let parent = element.parentElement; parent && parent !== document.body; parent = parent.parentElement) {
        const box = parent.getBoundingClientRect(), parentStyle = getComputedStyle(parent);
        if (/(auto|scroll|hidden|clip)/.test(parentStyle.overflowX)
            && box.left >= -2 && box.right <= viewport + 2) { contained = true; break; }
      }
      if (contained) continue;
      if (offenders.length < 20) offenders.push({tag:element.tagName.toLowerCase(), id:element.id,
        classes:typeof element.className === 'string' ? element.className.slice(0,120) : '',
        left:Math.round(rect.left), right:Math.round(rect.right), width:Math.round(rect.width),
        scrollWidth:element.scrollWidth, clientWidth:element.clientWidth});
    }
    return {viewport, documentWidth:document.documentElement.scrollWidth,
      bodyWidth:document.body.scrollWidth, rootOverflow:document.documentElement.scrollWidth > viewport + 2,
      offenders};
  });
}

async function assertHorizontalContainment(page) {
  const measurement = await measureOverflow(page);
  assert.equal(measurement.rootOverflow, false, `Root overflow: ${JSON.stringify(measurement)}`);
  assert.equal(measurement.offenders.length, 0, `Visible overflow: ${JSON.stringify(measurement.offenders)}`);
  return measurement;
}

async function checkLayout(page) {
  await settle(page);
  const images = await visibleMedia(page);
  const overflow = await assertHorizontalContainment(page);
  return {images, overflow};
}

async function setView(page, view) {
  const button = page.locator(`[data-reader-view="${view}"]`);
  if (await button.isVisible()) { await button.click(); return 'button'; }
  const select = page.locator('[data-reader-view-select]');
  assert.equal(await select.isVisible(), true, `No visible ${view} arrangement control`);
  await select.selectOption(view);
  return 'select';
}
async function activeChapter(page) {
  return page.locator('[data-reader-chapter].topic-active').getAttribute('id');
}
async function waitActive(page, id) {
  await page.waitForFunction(id => document.querySelector('[data-reader-chapter].topic-active')?.id === id,
    id, {timeout:10000});
  await settle(page);
}
async function goHash(page, url, id) {
  await page.goto(`${url.split("#")[0]}#${encodeURIComponent(id)}`, {waitUntil:'domcontentloaded'});
  await page.waitForFunction(id => {
    const node = document.getElementById(id), chapter = node?.closest('[data-reader-chapter]');
    return !!node && !!chapter && chapter.classList.contains('topic-active') && !chapter.inert;
  }, id, {timeout:10000});
  await settle(page);
}
// Optional check(label, run) records failures and returns whether run succeeded.
// Without that callback a failed assertion throws. onPair captures caller-owned
// screenshots/layout evidence while the pin interaction is still displayed.
// Returns {chapterIds, checked, skipped}; impossible interactions are never
// passed to check() as successful checks.
async function readerChecks(page, {url, expectedChapters, check = async (_label, run) => {
  await run(); return true;
}, onPair = async () => {}}) {
  let chapterIds = [];
  const scope = {chapterIds, checked:[], skipped:[]};
  async function runCheck(label, run) {
    const passed = await check(label, run);
    if (passed) scope.checked.push(label);
    return passed;
  }
  const ready = await runCheck('shared reader initializes the expected chapters', async () => {
    await page.waitForSelector('body.reader-enabled');
    chapterIds = await page.locator('[data-reader-chapter]').evaluateAll(nodes => nodes.map(node => node.id));
    scope.chapterIds = chapterIds;
    assert.equal(chapterIds.length, expectedChapters);
    assert.equal(new Set(chapterIds).size, expectedChapters);
    assert.equal(await page.locator('#chapter-reader').isVisible(), true);
    assert.equal(await page.locator('.topic-stage').count(), 1);
    return {chapterIds, countText:await page.locator('[data-topic-count]').innerText()};
  });
  if (!ready) return scope;
  if (chapterIds.length === 1) {
    await runCheck('hash navigation reveals the only chapter', async () => {
      await goHash(page, url, chapterIds[0]);
      return {target:chapterIds[0]};
    });
    for (const label of ['click next and previous chapter controls',
      'hash navigation and browser back/forward restore chapters',
      'two chapter arrangement and pinning preserve the held chapter']) {
      scope.skipped.push({label, reason:'Only one chapter; no distinct chapter or pair is available'});
    }
    return scope;
  }
  await runCheck('click next and previous chapter controls', async () => {
    assert.equal(await activeChapter(page), chapterIds[0]);
    await page.locator('.topic-peek-next').click();
    await waitActive(page, chapterIds[1]);
    await page.locator('.topic-peek-prev').click();
    await waitActive(page, chapterIds[0]);
    return {next:chapterIds[1], previous:chapterIds[0]};
  });
  // Keep the original third/fourth targets on larger consumers; smaller
  // readers use the last two available chapters.
  const [backId, forwardId] = chapterIds.slice(Math.min(2, chapterIds.length - 2), Math.min(4, chapterIds.length));
  await runCheck('hash navigation and browser back/forward restore chapters', async () => {
    await goHash(page, url, backId);
    await goHash(page, url, forwardId);
    await page.goBack({waitUntil:'domcontentloaded'});
    await waitActive(page, backId);
    await page.goForward({waitUntil:'domcontentloaded'});
    await waitActive(page, forwardId);
    assert.equal(new URL(page.url()).hash, '#' + forwardId);
    return {back:backId, forward:forwardId};
  });
  await runCheck('two chapter arrangement and pinning preserve the held chapter', async () => {
    await goHash(page, url, chapterIds[0]);
    const control = await setView(page, 'pair');
    await page.waitForFunction(() => document.querySelector('.content')?.dataset.topicView === 'pair');
    assert.equal(await page.locator('[data-reader-chapter].topic-visible').count(), 2);
    const pin = page.locator('[data-reader-chapter].topic-visible .chapter-pin').first();
    assert.equal(await pin.isVisible(), true, 'Pair arrangement must offer its chapter pin');
    await pin.click();
    const pinnedId = await page.locator('[data-reader-chapter].topic-pinned').getAttribute('id');
    const before = await page.locator('[data-reader-chapter].topic-visible:not(.topic-pinned)').getAttribute('id');
    if (chapterIds.length > 2) {
      await page.locator('[data-topic-next]').click();
      await page.waitForFunction(before => document.querySelector('[data-reader-chapter].topic-visible:not(.topic-pinned)')?.id !== before,
        before, {timeout:10000});
      scope.checked.push('pinned chapter navigation');
    } else {
      assert.equal(await page.locator('[data-topic-prev]').isDisabled(), true);
      assert.equal(await page.locator('[data-topic-next]').isDisabled(), true);
      scope.checked.push('two chapter pinned navigation boundaries');
      scope.skipped.push({label:'pinned chapter navigation',
        reason:'Both chapters occupy the pair; no third chapter can replace the unpinned chapter'});
    }
    assert.equal(await page.locator('[data-reader-chapter].topic-pinned').getAttribute('id'), pinnedId);
    const widths = await page.locator('[data-reader-chapter].topic-visible').evaluateAll(nodes => nodes.map(node => Math.round(node.getBoundingClientRect().width)));
    assert.ok(Math.abs(widths[0] - widths[1]) <= 2, `Unequal pair columns: ${widths}`);
    await onPair();
    await setView(page, 'single');
    return {control, pinnedId, before, after:await activeChapter(page), widths};
  });
  // Restore a known single arrangement even if a prior interaction failed.
  await runCheck('restore single chapter arrangement', async () => {
    await setView(page, 'single');
    await page.waitForFunction(() => document.querySelector('.content')?.dataset.topicView === 'single');
  });
  return scope;
}

// Slide faces: every face at or above the compact width must fit its 16:9 canvas.
// Returns one row per face; callers assert on `fits` for rendered (non-compact) faces.
async function slideFaces(page) {
  return page.evaluate(() => [...document.querySelectorAll('[data-slide-face]')].map(face => {
    const canvas = face.querySelector(':scope > .slide-canvas') || face;
    const main = canvas.querySelector('.slide-main');
    const compact = getComputedStyle(canvas).aspectRatio === 'auto';
    const overflow = !compact && (canvas.scrollHeight > canvas.clientHeight + 1 || (!!main && main.scrollHeight > main.clientHeight + 1));
    const chapter = face.closest('[data-reader-chapter]')?.id || face.closest('section')?.id || '';
    return {chapter, width: canvas.clientWidth, height: canvas.clientHeight, compact, fits: !overflow,
            bridge: !!face.parentElement.querySelector(':scope > .slide-bridge, .slide-bridge')};
  }));
}

module.exports = {slideFaces, settle, visibleMedia, measureOverflow, assertHorizontalContainment,
  checkLayout, setView, activeChapter, waitActive, goHash, readerChecks};
