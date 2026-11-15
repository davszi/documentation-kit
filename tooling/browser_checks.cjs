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

// Slide faces, measured where they are shown: in a page at reader widths or in an extracted deck.
// One row per face in the page, or inside `within` (a selector such as '#chapter-id'). A face the
// page does not show (an inactive reader chapter, All chapters without the Slides switch) has
// `shown: false` and no measurements. For a shown face:
// - `compact`: the canvas is stacked (the face is narrower than 720 px);
// - `fits`: a 16:9 face holds its content (always true when compact);
// - `sideways`: px by which the canvas content is wider than the canvas, or the canvas wider than
//   the space its container or the window gives it;
// - `clipped`: text cut off by a box that hides its overflow, the canvas included;
// - `outside`: parts that stick out of the canvas, with the px they stick out;
// - `emptyBand`: height in px of the largest horizontal band of the canvas that holds nothing:
//   no text, image, figure, background or border. It is information only and never a problem.
// `problems` lists, in words, a 16:9 face that does not fit, sideways overflow, clipped text and
// parts outside the face; a face is in order when it is empty. Page styles can add space that the
// deck lacks, so check faces in their page as well as in the deck.
async function slideFaces(page, {within = null} = {}) {
  return page.evaluate(within => {
    const scope = within ? [...document.querySelectorAll(within)] : [document];
    const faces = [...new Set(scope.flatMap(root => [...(root.matches?.('[data-slide-face]') ? [root] : []),
      ...root.querySelectorAll('[data-slide-face]')]))];
    const name = node => node.tagName.toLowerCase() + (node.id ? '#' + node.id : '')
      + (typeof node.className === 'string' && node.className.trim() ? '.' + node.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
    const visible = node => {
      for (let current = node; current; current = current.parentElement) {
        const style = getComputedStyle(current);
        if (style.display === 'none' || style.visibility === 'hidden' || style.visibility === 'collapse'
            || Number(style.opacity) === 0) return false;
        if (current.matches('[data-slide-face]')) break;
      }
      return true;
    };
    const textRects = root => {
      const found = [];
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      for (let text = walker.nextNode(); text; text = walker.nextNode()) {
        if (!text.data.trim() || !visible(text.parentElement)) continue;
        const range = document.createRange();
        range.selectNodeContents(text);
        for (const rect of range.getClientRects()) if (rect.width > 0 && rect.height > 0) found.push({text, node: text.parentElement, rect});
      }
      return found;
    };
    return faces.map(face => {
      const canvas = face.querySelector(':scope > .slide-canvas') || face;
      const chapter = face.closest('[data-reader-chapter]')?.id || face.closest('section')?.id || '';
      const box = canvas.getBoundingClientRect();
      if (!face.getClientRects().length || box.width < 1 || box.height < 1 || !visible(canvas)) return {chapter, shown: false, problems: []};
      const main = canvas.querySelector('.slide-main');
      const compact = getComputedStyle(canvas).aspectRatio === 'auto';
      const fits = compact || !(canvas.scrollHeight > canvas.clientHeight + 1 || (!!main && main.scrollHeight > main.clientHeight + 1));
      // Sideways: content wider than the canvas, or the canvas reaching past the window or past the
      // nearest ancestor that cuts or scrolls its overflow. A face may bleed into its card's padding.
      let holder = null;
      for (let parent = face.parentElement; parent && parent !== document.documentElement; parent = parent.parentElement) {
        if (getComputedStyle(parent).overflowX !== 'visible') {
          const r = parent.getBoundingClientRect();
          holder = {left: r.left + parent.clientLeft, right: r.left + parent.clientLeft + parent.clientWidth};
          break;
        }
      }
      let sideways = Math.max(0, canvas.scrollWidth - canvas.clientWidth, box.right - innerWidth, -box.left,
        holder ? box.right - holder.right : 0, holder ? holder.left - box.left : 0);
      // Parts outside the canvas, and text cut off by a box that hides its overflow.
      const outside = [];
      const elements = [...canvas.querySelectorAll('*')].filter(node => visible(node));
      for (const node of elements) {
        const rect = node.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;
        let clippedBy = null;
        for (let parent = node.parentElement; parent && parent !== canvas.parentElement; parent = parent.parentElement) {
          const style = getComputedStyle(parent);
          if (/(hidden|clip|auto|scroll)/.test(style.overflowX + style.overflowY)) { clippedBy = parent; break; }
        }
        if (clippedBy) continue;  // its own clipping box decides what shows
        const out = Math.max(box.left - rect.left, rect.right - box.right, box.top - rect.top, rect.bottom - box.bottom);
        if (out > 1 && outside.length < 20) outside.push({part: name(node), by: Math.round(out)});
      }
      const cuts = new Map();  // one entry per text, with its deepest cut over all its lines
      for (const {text, node, rect} of textRects(canvas)) {
        for (let parent = node; parent && parent !== canvas.parentElement; parent = parent.parentElement) {
          const style = getComputedStyle(parent);
          const r = parent.getBoundingClientRect();
          // A scroll region keeps its text reachable; only a box that hides its overflow cuts text.
          // A glyph box reaches past the ink above capitals and below the baseline, so a vertical
          // cut counts only beyond a quarter of the line; a sideways cut beyond 2 px cuts letters.
          const across = /(hidden|clip)/.test(style.overflowX) ? Math.max(r.left - rect.left, rect.right - r.right) : 0;
          const down = /(hidden|clip)/.test(style.overflowY) ? Math.max(r.top - rect.top, rect.bottom - r.bottom) : 0;
          const cut = Math.max(across > 2 ? across : 0, down > Math.max(2, rect.height / 4) ? down : 0);
          if (cut > 0) {
            const known = cuts.get(text);
            if (!known || known.by < cut) cuts.set(text, {text: text.data.trim().replace(/\s+/g, ' ').slice(0, 60), in: name(parent), by: cut});
            break;
          }
        }
      }
      const clipped = [...cuts.values()].slice(0, 20).map(item => ({...item, by: Math.round(item.by)}));
      // Largest empty band: vertical extent of the canvas content box that nothing covers.
      const style = getComputedStyle(canvas);
      const top = box.top + parseFloat(style.borderTopWidth) + parseFloat(style.paddingTop);
      const bottom = box.bottom - parseFloat(style.borderBottomWidth) - parseFloat(style.paddingBottom);
      const covered = textRects(canvas).map(({rect}) => [rect.top, rect.bottom]);
      for (const node of elements) {
        const s = getComputedStyle(node), rect = node.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;
        const painted = /^(img|svg|video|canvas|picture|iframe|object|embed)$/i.test(node.tagName)
          || (s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') || s.backgroundImage !== 'none'
          || ['Top', 'Right', 'Bottom', 'Left'].some(side => parseFloat(s['border' + side + 'Width']) > 0 && s['border' + side + 'Style'] !== 'none');
        if (painted) covered.push([rect.top, rect.bottom]);
      }
      covered.sort((a, b) => a[0] - b[0]);
      let emptyBand = 0, reach = top;
      for (const [start, end] of covered) {
        if (end <= reach) continue;
        if (start > reach) emptyBand = Math.max(emptyBand, Math.min(start, bottom) - reach);
        reach = Math.max(reach, end);
        if (reach >= bottom) break;
      }
      emptyBand = Math.max(emptyBand, bottom - reach);
      sideways = Math.round(sideways);
      const problems = [];
      if (!fits) problems.push('the content does not fit the 16:9 canvas');
      if (sideways > 1) problems.push(`overflows sideways by ${sideways} px`);
      for (const item of clipped) problems.push(`clips text "${item.text}" in ${item.in} by ${item.by} px`);
      for (const item of outside) problems.push(`${item.part} sticks out of the face by ${item.by} px`);
      return {chapter, shown: true, width: canvas.clientWidth, height: canvas.clientHeight, compact, fits,
              sideways, clipped, outside, emptyBand: Math.max(0, Math.round(emptyBand)), problems,
              bridge: !!face.parentElement.querySelector(':scope > .slide-bridge, .slide-bridge')};
    });
  }, within);
}

// Fails with every problem of every shown face; returns the rows. `expectShown` guards against
// checking nothing, for example when the reader hides the chapter that holds the face.
async function assertSlideFaces(page, {within = null, expectShown = 1} = {}) {
  const faces = await slideFaces(page, {within});
  const shown = faces.filter(face => face.shown);
  assert.ok(shown.length >= expectShown, `Expected at least ${expectShown} shown slide face(s), found ${shown.length}`);
  const faults = shown.filter(face => face.problems.length)
    .map(face => `${face.chapter || '(no chapter)'} at ${face.width} px: ${face.problems.join('; ')}`);
  assert.deepEqual(faults, [], 'Slide face problems');
  return faces;
}

// Capture one element (a figure, a slide face, a chapter) for review. With `unclip`, the element and its
// ancestors lose height limits and clipping first, so a reader chapter is captured whole rather than at
// its stage height; `hide` selectors inside the element (for example '.slide-face') are hidden.
// The page is not restored: capture on a page or context opened for review.
async function captureElement(page, selector, file, {unclip = false, hide = []} = {}) {
  const element = page.locator(selector).first();
  await element.waitFor({state: 'attached'});
  if (unclip || hide.length) {
    await element.evaluate((node, {unclip, hide}) => {
      for (let current = unclip ? node : null; current; current = current.parentElement) {
        for (const [name, value] of [['height', 'auto'], ['max-height', 'none'], ['overflow', 'visible']])
          current.style.setProperty(name, value, 'important');
      }
      for (const inner of hide.flatMap(query => [...node.querySelectorAll(query)]))
        inner.style.setProperty('display', 'none', 'important');
    }, {unclip, hide});
  }
  await element.scrollIntoViewIfNeeded();
  await settle(page);
  const box = await element.boundingBox();
  await element.screenshot({path: file});
  return {width: Math.round(box?.width || 0), height: Math.round(box?.height || 0)};
}

module.exports = {slideFaces, assertSlideFaces, settle, visibleMedia, measureOverflow, assertHorizontalContainment,
  checkLayout, setView, activeChapter, waitActive, goHash, readerChecks, captureElement};
