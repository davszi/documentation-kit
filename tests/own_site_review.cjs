// Optional real-browser review of the kit's own reference website (.build/docs).
// Build it first: python docsite.py build --project .
// Run as one owned, serialized local job; screenshots go to .build/visual-review/own-site/.
const { chromium } = require('../node_modules/playwright');
const fs = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const assert = require('node:assert/strict');
const {settle, checkLayout, setView, goHash, assertSlideFaces} = require('../tooling/browser_checks.cjs');
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
const SHOTS = ['index', 'getting-started', 'build-a-site', 'git', 'releases', 'readme'];

// Presentation view and the All chapters Slides switch on build-a-site, whose
// first chapter opens with a slide face and whose other chapters have none.
const PRESENT_PAGE = 'build-a-site';
const FACE_CHAPTER = 'how-a-build-works';
const PLAIN_CHAPTERS = ['write-a-topic-page', 'the-reader', 'figures-and-slides', 'existing-markdown'];
async function presentState(page) {
  return page.evaluate(() => {
    const card = document.querySelector('[data-reader-chapter].topic-active');
    const body = card?.querySelector('.chapter-body'), slide = card?.querySelector('.present-slide');
    const box = slide?.getBoundingClientRect(), titleCard = card?.querySelector('.present-title-card');
    return {cardShown: !!titleCard?.getClientRects().length, headingTop: card?.querySelector('.chapter-headline')?.getBoundingClientRect().top,view: document.querySelector('main.content').dataset.topicView, active: card?.id, scroll: body?.scrollTop,
      search: location.search, hash: location.hash, bar: !!document.querySelector('.present-bar:not([hidden])'),
      toolbar: getComputedStyle(document.getElementById('chapter-reader')).display,
      island: getComputedStyle(document.querySelector('.reader-island')).display,
      sidebar: getComputedStyle(document.getElementById('sidebar')).display,
      snap: body && [getComputedStyle(body).scrollSnapType, slide && getComputedStyle(slide).scrollSnapAlign],
      slide: box && {face: slide.hasAttribute('data-slide-face'), titleCard: slide.classList.contains('present-title-card'),
        top: box.top, left: box.left, width: box.width, height: box.height, compact: box.width < 720},
      focus: document.activeElement?.id || document.activeElement?.getAttribute('data-reader-view') || document.activeElement?.className || ''};
  });
}
async function waitPresent(page, id, view = 'present') {
  await page.waitForFunction(([id, view]) => document.querySelector('main.content')?.dataset.topicView === view
    && document.querySelector('[data-reader-chapter].topic-active')?.id === id, [id, view], {timeout: 5000});
  await page.waitForTimeout(50);
  return presentState(page);
}
// The slide fills the window at 16:9, letterboxed and centred; below 720 px it stacks at the top.
function assertSlideFills(state, viewport, what) {
  const {slide} = state;
  assert.ok(slide, what + ': the chapter shows a slide');
  if (slide.compact) {
    assert.ok(Math.abs(slide.top) < 1 && Math.abs(slide.width - viewport.width) < 1, what + ': stacked slide at the top ' + JSON.stringify(slide));
    return;
  }
  assert.ok(Math.abs(slide.width / slide.height - 16 / 9) < 0.01, what + ': slide keeps 16:9 ' + JSON.stringify(slide));
  assert.ok(Math.abs(slide.width - viewport.width) < 1 || Math.abs(slide.height - viewport.height) < 1, what + ': slide fills one window axis');
  assert.ok(Math.abs(slide.top - (viewport.height - slide.height) / 2) < 1 && Math.abs(slide.left - (viewport.width - slide.width) / 2) < 1,
    what + ': slide is letterboxed in the centre ' + JSON.stringify(slide));
}
// Clicks a control of the navigation; a closed overlay navigation is opened first.
async function clickInNavigation(page, selector) {
  const control = page.locator(selector);
  if (!await control.isVisible()) {
    await page.click('.reader-mobile-menu');
    await control.waitFor({state: 'visible', timeout: 5000});
  }
  await control.click();
}
async function reviewPresentation(page, origin, viewport, failures) {
  const url = `${origin}/html/${PRESENT_PAGE}.html`;
  const checked = [];
  const overlay = viewport.width <= 900, narrow = viewport.width < 720;
  const built = await fs.readFile(path.join(root, `html/${PRESENT_PAGE}.html`), 'utf8');
  assert.ok(!built.includes('present-title-card') && !built.includes('present-slide'), 'title cards exist only at run time');

  // From the current chapter: the view opens on that chapter's slide.
  await page.goto(`${url}#${PLAIN_CHAPTERS[0]}`, {waitUntil: 'networkidle'});
  await settle(page);
  await page.locator('[data-reader-chapter].topic-active .chapter-body').evaluate(node => { node.scrollTop = 400; });
  await setView(page, 'present');
  let state = await waitPresent(page, PLAIN_CHAPTERS[0]);
  assert.equal(state.scroll, 0, 'Presentation opens the chapter on its slide');
  assert.equal(state.search, '?view=present', 'the address names the view');
  assert.equal(state.hash, '#' + PLAIN_CHAPTERS[0], 'the address names the chapter');
  assert.ok(state.bar && state.toolbar === 'none' && state.island === 'none' && state.sidebar === 'none', 'only the presentation controls show: ' + JSON.stringify(state));
  assert.equal(state.focus, PLAIN_CHAPTERS[0], 'focus moves to the presented chapter');
  // Proximity is the initial strictness, so the computed value may serialize as plain "y".
  assert.ok(/^y( proximity)?$/.test(state.snap[0]) && state.snap[1] === 'start', 'the chapter snaps back to its slide near the top: ' + state.snap);
  // At 720 px and wider a chapter without a face shows a run-time title card
  // from its headline and lead. Narrower, slides stack and the card would
  // repeat the heading the chapter starts with, so the chapter starts there.
  if (narrow) {
    assert.equal(state.cardShown, false, 'a narrow chapter without a face shows no title card');
    assert.ok(state.headingTop >= 0 && state.headingTop < 60, 'a narrow chapter without a face starts at its heading: ' + state.headingTop);
  } else {
    assert.ok(state.cardShown && state.slide.titleCard && !state.slide.face, 'a chapter without a face shows a title card');
    const card = await page.locator('[data-reader-chapter].topic-active .present-title-card').evaluate(node => ({
      face: node.matches('[data-slide-face]') || !!node.querySelector('[data-slide-face]'), hidden: node.getAttribute('aria-hidden'),
      heading: node.querySelector('.present-title-heading').textContent, lead: node.querySelector('.present-title-lead')?.textContent,
      expected: [node.closest('[data-reader-chapter]').querySelector('.chapter-headline').textContent.trim(),
        node.closest('[data-reader-chapter]').querySelector('.bs-lead').textContent]}));
    assert.equal(card.face, false, 'the title card is not a slide face');
    assert.equal(card.hidden, 'true', 'the title card repeats the chapter for sight only');
    assert.deepEqual([card.heading, card.lead], card.expected, 'the title card carries the chapter headline and lead');
    assertSlideFills(state, viewport, 'title card');
  }
  assert.equal(await page.locator('[data-slide-face]').count(), 1, 'title cards add no slide face');
  checked.push('enter from the current chapter', 'title card');

  // Key navigation always lands on the slide; scrolling stays in the chapter.
  await page.mouse.move(viewport.width / 2, viewport.height / 3);
  await page.mouse.wheel(0, 900);
  await page.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active .chapter-body').scrollTop > 0);
  await page.keyboard.press('ArrowDown');
  await page.keyboard.press('Space');
  await page.waitForTimeout(150);
  state = await presentState(page);
  assert.equal(state.active, PLAIN_CHAPTERS[0], 'wheel, ArrowDown and Space never change the chapter');
  assert.ok(state.scroll > 0, 'scrolling reaches the full chapter below the slide');
  for (const [key, id] of [['ArrowRight', PLAIN_CHAPTERS[1]], ['PageDown', PLAIN_CHAPTERS[2]], ['PageUp', PLAIN_CHAPTERS[1]], ['ArrowLeft', PLAIN_CHAPTERS[0]]]) {
    await page.locator('[data-reader-chapter].topic-active .chapter-body').evaluate(node => { node.scrollTop = 300; });
    await page.keyboard.press(key);
    state = await waitPresent(page, id);
    assert.equal(state.scroll, 0, key + ' lands at the top of ' + id);
    assert.equal(state.hash, '#' + id, key + ' writes the chapter to the address');
  }
  await page.keyboard.press('Home');
  state = await waitPresent(page, FACE_CHAPTER);
  assert.ok(state.slide.face && !state.slide.titleCard, 'a chapter with a face presents its face');
  assertSlideFills(state, viewport, 'slide face');
  await page.keyboard.press('End');
  await waitPresent(page, 'reference-guides');
  await page.keyboard.press('Home');
  await waitPresent(page, FACE_CHAPTER);
  checked.push('arrow, page and Home/End keys land on the slide', 'scrolling keeps the chapter');

  // Controls inside a chapter keep their keys; the lightbox keeps its own.
  await page.locator('.present-bar .present-next').click();
  await waitPresent(page, PLAIN_CHAPTERS[0]);
  for (let step = 1; step < 4; step++) await page.keyboard.press('ArrowRight');
  await waitPresent(page, 'existing-markdown');
  await page.locator('[data-reader-chapter].topic-active [data-panel-choice="page"]').click();
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(150);
  assert.equal((await presentState(page)).active, 'existing-markdown', 'a focused panel control keeps ArrowRight');
  assert.equal(await page.locator('#view-page').isVisible(), true, 'the panel switcher still switches');
  await page.keyboard.press('Home');
  await page.waitForTimeout(150);
  assert.equal((await presentState(page)).active, 'existing-markdown', 'a focused panel control keeps Home');
  await page.locator('.present-bar .present-restart').click();
  await waitPresent(page, FACE_CHAPTER);
  // The slide is still the chapter's focus target after a control kept the focus.
  await page.locator('[data-reader-chapter].topic-active').focus();
  // A face may swap a wide drawing for an upright one below 720 px; click the drawing that is shown.
  await page.locator('[data-reader-chapter].topic-active .present-slide svg.inline-fig:visible').first().click();
  await page.waitForSelector('.lb-overlay');
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('Escape');
  await page.waitForSelector('.lb-overlay', {state: 'detached'});
  state = await presentState(page);
  assert.deepEqual([state.view, state.active], ['present', FACE_CHAPTER], 'keys in the lightbox change neither chapter nor view');
  checked.push('interactive parts keep their keys');

  // Reload and a shared link reopen the same slide in the same view.
  await page.keyboard.press('ArrowRight');
  await waitPresent(page, PLAIN_CHAPTERS[0]);
  await page.reload({waitUntil: 'networkidle'});
  state = await waitPresent(page, PLAIN_CHAPTERS[0]);
  assert.equal(state.scroll, 0, 'reload reopens the slide');
  await page.goto(`${url}?view=present#the-reader`, {waitUntil: 'networkidle'});
  state = await waitPresent(page, 'the-reader');
  assert.ok(state.bar && state.cardShown === !narrow, 'a shared link opens Presentation on its chapter');
  checked.push('reload and shared link');

  // Escape and the close control return to the previous view and chapter.
  await page.keyboard.press('Escape');
  state = await waitPresent(page, 'the-reader', 'single');
  assert.equal(state.search, '', 'leaving removes the view from the address');
  for (const view of ['pair', 'full']) {
    await setView(page, view);
    await page.waitForFunction(view => view === 'full' ? document.querySelector('main.content').dataset.topicLayout === 'full'
      : document.querySelector('main.content').dataset.topicView === view, view);
    const before = await page.evaluate(() => document.querySelector('[data-reader-chapter].topic-active').id);
    await setView(page, 'present');
    await waitPresent(page, before);
    await page.locator('.present-bar .present-close').click();
    await page.waitForFunction(view => view === 'full' ? document.querySelector('main.content').dataset.topicLayout === 'full'
      : document.querySelector('main.content').dataset.topicView === view, view);
    state = await presentState(page);
    assert.equal(state.active, before, `leaving returns to ${view} on the presented chapter`);
    assert.ok(state.island !== 'none' && !state.bar, 'the reader stepper returns');
  }
  checked.push('exit restores Two chapters and All chapters');

  // Changed behaviour: "From start" is gone; Presentation starts at the current chapter.
  // Focus returns to the Presentation icon, or to the chapter where the overlay navigation closed.
  await setView(page, 'single');
  await page.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active')?.id === 'the-reader');
  assert.equal(await page.locator('[data-reader-present-start], [data-reader-view-select]').count(), 0, 'no From start control or view menu');
  await setView(page, 'present');
  state = await waitPresent(page, 'the-reader');
  assert.equal(state.scroll, 0, 'Presentation opens the current chapter on its slide');
  await page.keyboard.press('Shift+Tab');
  const close = await page.evaluate(() => ({inBar: !!document.activeElement?.closest('.present-bar'),
    outline: getComputedStyle(document.activeElement).outlineStyle}));
  assert.ok(close.inBar && close.outline !== 'none', 'Shift+Tab reaches the visible presentation controls: ' + JSON.stringify(close));
  await page.keyboard.press('Escape');
  state = await waitPresent(page, 'the-reader', 'single');
  const returned = await page.evaluate(overlay => {
    const node = document.activeElement;
    return overlay ? !!node?.closest('[data-reader-chapter].topic-active') : !!node?.matches('[data-reader-view="present"]');
  }, overlay);
  assert.ok(returned, 'focus returns to the Presentation icon, or to the chapter when the overlay navigation started it');
  checked.push('Presentation at the current chapter', 'focus on enter and exit');

  // The controls fade when idle and return on pointer movement; fullscreen is optional.
  if (!overlay) {
    await page.goto(`${url}#${FACE_CHAPTER}`, {waitUntil: 'networkidle'});
    await setView(page, 'present');
    await waitPresent(page, FACE_CHAPTER);
    await page.mouse.move(20, 20);
    await page.waitForFunction(() => document.body.classList.contains('present-idle'), null, {timeout: 6000});
    await page.mouse.move(60, 60);
    assert.equal(await page.evaluate(() => document.body.classList.contains('present-idle')), false, 'pointer movement brings the controls back');
    if (await page.evaluate(() => document.fullscreenEnabled)) {
      await page.keyboard.press('f');
      await page.waitForFunction(() => !!document.fullscreenElement, null, {timeout: 3000});
      assert.equal(await page.getAttribute('.present-bar .present-button[aria-pressed]', 'aria-label'), 'Leave fullscreen');
      await page.keyboard.press('Escape');
      await page.waitForTimeout(150);
      assert.equal((await presentState(page)).view, 'present', 'Escape in fullscreen does not leave the view');
      if (await page.evaluate(() => !!document.fullscreenElement)) await page.keyboard.press('f');
      await page.waitForFunction(() => !document.fullscreenElement, null, {timeout: 3000});
      await page.waitForTimeout(600);
      checked.push('fullscreen');
    }
    await page.keyboard.press('Escape');
    await waitPresent(page, FACE_CHAPTER, 'single');
    checked.push('idle fade');
  }

  // All chapters: slide faces are hidden until the Slides switch shows them; the choice is remembered.
  const faces = () => page.evaluate(() => ({face: getComputedStyle(document.querySelector('[data-slide-face]')).display,
    bridge: getComputedStyle(document.querySelector('.slide-bridge')).display,
    pressed: document.querySelector('[data-reader-slides]').getAttribute('aria-pressed'),
    visible: !!document.querySelector('[data-reader-slides]').getClientRects().length}));
  let shown = await faces();
  assert.ok(shown.face !== 'none' && !shown.visible, 'One chapter always shows the face; the switch belongs to All chapters');
  await setView(page, 'full');
  shown = await faces();
  assert.deepEqual(shown, {face: 'none', bridge: 'none', pressed: 'false', visible: true}, 'All chapters hides slides by default');
  await page.emulateMedia({media: 'print'});
  assert.equal((await faces()).face, 'none', 'print follows the switch (off)');
  await page.emulateMedia({media: 'screen'});
  await clickInNavigation(page, '[data-reader-slides]');
  shown = await faces();
  assert.deepEqual([shown.face !== 'none', shown.bridge !== 'none', shown.pressed], [true, true, 'true'], 'the switch shows slides');
  await page.emulateMedia({media: 'print'});
  assert.notEqual((await faces()).face, 'none', 'print follows the switch (on)');
  await page.emulateMedia({media: 'screen'});
  await page.reload({waitUntil: 'networkidle'});
  await setView(page, 'full');
  shown = await faces();
  assert.deepEqual([shown.face !== 'none', shown.pressed], [true, 'true'], 'the switch is remembered for the page');
  await clickInNavigation(page, '[data-reader-slides]');
  assert.equal((await faces()).face, 'none', 'the switch hides slides again');
  checked.push('Slides switch off by default, on after the click, remembered, print');

  // A page without slide faces offers neither Presentation nor Slides.
  await page.goto(`${origin}/html/experiments.html?view=present`, {waitUntil: 'networkidle'});
  await setView(page, 'full');
  const plain = await page.evaluate(() => ({controls: [...document.querySelectorAll('[data-reader-view="present"], [data-reader-slides]')].filter(node => node.getClientRects().length).length,
    view: document.querySelector('main.content').dataset.topicView,
    bar: document.querySelectorAll('.present-bar').length, search: location.search}));
  assert.deepEqual(plain, {controls: 0, view: 'single', bar: 0, search: ''}, 'no Presentation without slide faces');
  checked.push('pages without faces');
  assert.deepEqual(failures, [], 'browser errors during presentation checks at ' + viewport.width);
  return checked;
}

// The reader's frame on build-a-site, whose first chapter opens with a slide face.
// Wide: no top bar, the icon row under the site name, the stepper island at the
// bottom centre over a fade, the "Full chapter" row docked on the island's line at
// three window heights and gone once the chapter scrolls, click zones equal to the
// visible strips of the neighbours. Narrow: the bar with menu and page name, the
// row and options inside the drawer, "Continue reading" above the island, swipe.
async function frameState(page) {
  return page.evaluate(() => {
    const box = node => { if (!node) return null; const r = node.getBoundingClientRect(); return {left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height}; };
    const card = document.querySelector('[data-reader-chapter].topic-active'), row = card.querySelector('.slide-bridge[data-slide-bridge-lead]');
    const style = node => node && getComputedStyle(node);
    return {active: card.id, card: box(card), stage: box(document.querySelector('.topic-stage')), island: box(document.querySelector('.reader-island')),
      place: document.querySelector('.reader-place').textContent, away: document.querySelector('.reader-island').classList.contains('reader-island-away'),
      bar: style(document.getElementById('chapter-reader')).display, scroll: card.querySelector('.chapter-body').scrollTop,
      row: row && {box: box(row), shown: style(row).visibility !== 'hidden' && Number(style(row).opacity) > 0, pill: box(row.querySelector('.slide-bridge-pill')),
        pillShown: style(row.querySelector('.slide-bridge-pill')).display !== 'none', meta: style(row.querySelector('.slide-bridge-meta')).display !== 'none',
        button: box(row.querySelector('.slide-bridge-button')), text: row.querySelector('.slide-bridge-button').textContent.trim()},
      fade: style(card, '::after') && getComputedStyle(card, '::after').backgroundImage,
      header: style(card.querySelector('.chapter-header')).display, headline: parseFloat(style(card.querySelector('.chapter-headline')).fontSize)};
  });
}
async function reviewFrame(browser, origin) {
  const url = `${origin}/html/${PRESENT_PAGE}.html#${FACE_CHAPTER}`;
  const checked = [];
  const context = await browser.newContext({viewport: {width: 1600, height: 900}, reducedMotion: 'reduce'});
  const page = await context.newPage();
  await page.goto(url, {waitUntil: 'networkidle'});
  await settle(page);
  let state = await frameState(page);
  assert.equal(state.bar, 'none', 'wide windows with docked navigation have no top bar');
  const sidebar = await page.evaluate(() => {
    const box = node => node.getBoundingClientRect();
    const head = box(document.querySelector('#sidebar .reader-drawer-head')), row = box(document.querySelector('#sidebar .reader-tools')), toc = box(document.getElementById('toc'));
    const icons = [...document.querySelectorAll('#sidebar .reader-tools button')].filter(node => node.getClientRects().length).map(node => {
      const r = box(node); return {name: node.getAttribute('aria-label'), tip: node.title, width: r.width, height: r.height}; });
    return {gapToList: toc.top - row.bottom, underHead: row.top >= head.bottom - 1, rowWidth: row.width, sidebar: box(document.getElementById('sidebar')).width, icons};
  });
  assert.ok(sidebar.underHead && Math.abs(sidebar.gapToList - 4) <= 1, 'the icon row sits under the site name, 4 px above the page list: ' + JSON.stringify(sidebar));
  assert.deepEqual(sidebar.icons.map(icon => icon.name), ['One chapter', 'Two chapters', 'All chapters', 'Presentation', 'About this page', 'Reader help'],
    'six named icons in one row');
  assert.ok(sidebar.icons.every(icon => icon.tip === icon.name && icon.height >= 44 && icon.width >= 43.5 && Math.abs(icon.width - sidebar.icons[0].width) < 1),
    'each icon has a tooltip, a 44 px target and an equal share of the row: ' + JSON.stringify(sidebar.icons));
  assert.ok(Math.abs((state.island.left + state.island.right) / 2 - (state.stage.left + state.stage.right) / 2) <= 1
    && state.island.bottom <= state.stage.bottom && state.stage.bottom - state.island.bottom < 40, 'the island sits at the bottom centre of the stage: ' + JSON.stringify(state.island));
  const chapters = await page.locator('[data-reader-chapter]').count();
  assert.equal(state.place, `1 of ${chapters}`, 'the island says where the reader is');
  assert.ok(/gradient/.test(state.fade), 'a fade layer lies under the bottom line: ' + state.fade);
  assert.equal(state.header, 'none', 'One chapter shows no chapter strip');
  assert.ok(state.headline >= 32 && state.headline <= 50, 'the chapter name is the large headline: ' + state.headline);
  checked.push('no bar', 'icon row', 'island at the bottom centre', 'fade', 'headline');

  // Review finding: a hidden click zone shows nothing and takes no click, at the first and
  // the last chapter and in All chapters.
  const zonesShown = () => page.evaluate(() => [...document.querySelectorAll('.topic-peek')]
    .map(node => `${node.className.split('-').pop()}:${node.hidden ? 'hidden' : 'on'}:${getComputedStyle(node).display === 'none' ? 'none' : 'shown'}`));
  assert.deepEqual(await zonesShown(), ['prev:hidden:none', 'next:on:shown'], 'the first chapter has no previous zone');
  await page.goto(`${origin}/html/${PRESENT_PAGE}.html#reference-guides`, {waitUntil: 'networkidle'});
  await settle(page);
  assert.deepEqual(await zonesShown(), ['prev:on:shown', 'next:hidden:none'], 'the last chapter has no next zone');
  await setView(page, 'full');
  await settle(page);
  assert.deepEqual(await zonesShown(), ['prev:hidden:none', 'next:hidden:none'], 'All chapters has no click zones');
  const edge = await page.evaluate(() => {
    const line = [...document.querySelectorAll('[data-reader-chapter] .chapter-body p')].find(node => { const r = node.getBoundingClientRect(); return r.top > 80 && r.bottom < innerHeight - 120; });
    const r = line.getBoundingClientRect();
    return document.elementFromPoint(r.left + 3, r.top + 6)?.closest('.topic-peek') ? 'zone' : 'text';
  });
  assert.equal(edge, 'text', 'in All chapters the start of a line is text, not a click zone');
  await setView(page, 'single');
  await page.goto(url, {waitUntil: 'networkidle'});
  await settle(page);
  checked.push('no hidden click zone at the first and last chapter or in All chapters');

  // Review finding: the docked row never runs under the island at narrower wide windows:
  // the reading time goes first, then the label.
  for (const width of [1000, 1200]) {
    await page.setViewportSize({width, height: 900});
    await settle(page);
    await page.waitForFunction(() => !document.querySelector('.reader-island').classList.contains('reader-island-away'), null, {timeout: 3000});
    const fit = await page.evaluate(() => {
      const row = document.querySelector('[data-reader-chapter].topic-active [data-slide-bridge-lead]');
      const island = document.querySelector('.reader-island').getBoundingClientRect();
      const shown = [...row.querySelectorAll('.slide-bridge-pill, .slide-bridge-meta')].filter(node => getComputedStyle(node).display !== 'none');
      return {docked: document.body.classList.contains('reader-nav-docked'), parts: shown.map(node => node.className),
        labelRight: Math.max(0, ...shown.map(node => node.getBoundingClientRect().right)), islandLeft: island.left, islandRight: island.right,
        buttonLeft: row.querySelector('.slide-bridge-button').getBoundingClientRect().left};
    });
    assert.ok(fit.docked && fit.labelRight < fit.islandLeft - 4 && fit.buttonLeft > fit.islandRight + 4,
      `at ${width} px the row stays clear of the island: ` + JSON.stringify(fit));
  }
  await page.setViewportSize({width: 1600, height: 900});
  await settle(page);
  checked.push('the row clears the island at 1000 and 1200 px');

  // The "Full chapter" row at three window heights: inside the window, docked on the island's line,
  // its label at the far left and "Continue reading" at the far right; gone after a scroll.
  for (const height of [900, 680, 560]) {
    await page.setViewportSize({width: 1600, height});
    await settle(page);
    await page.waitForFunction(() => !document.querySelector('.reader-island').classList.contains('reader-island-away'), null, {timeout: 3000});
    state = await frameState(page);
    const {row, island, card} = state;
    assert.ok(row && row.shown && row.box.top >= 0 && row.box.bottom <= height, `the row shows inside the window at ${height} px: ` + JSON.stringify(row));
    assert.ok(Math.abs((row.box.top + row.box.bottom) / 2 - (island.top + island.bottom) / 2) <= 4, `the row is on the island's line at ${height} px`);
    assert.ok(row.pill.left - card.left < 40 && card.right - row.button.right < 40 && row.pill.right < island.left && row.button.left > island.right,
      `label at the far left, Continue reading at the far right at ${height} px: ` + JSON.stringify(state));
    await page.locator('[data-reader-chapter].topic-active .chapter-body').evaluate(node => { node.scrollTop = 200; });
    await page.waitForFunction(() => !!document.querySelector('[data-reader-chapter].topic-active.topic-scrolled'));
    state = await frameState(page);
    assert.equal(state.row.shown, false, `the row leaves once the chapter scrolls at ${height} px`);
    assert.ok(state.away, 'the island steps back while the chapter scrolls');
    await page.waitForFunction(() => !document.querySelector('.reader-island').classList.contains('reader-island-away'), null, {timeout: 3000});
    await page.locator('[data-reader-chapter].topic-active .chapter-body').evaluate(node => { node.scrollTop = 0; });
    await page.waitForFunction(() => !document.querySelector('[data-reader-chapter].topic-active.topic-scrolled'));
    await page.waitForFunction(() => !document.querySelector('.reader-island').classList.contains('reader-island-away'), null, {timeout: 3000});
  }
  await page.setViewportSize({width: 1600, height: 900});
  await settle(page);
  // Review finding: activated by keyboard, the docked button hands focus to its chapter before it hides.
  await page.focus('[data-reader-chapter].topic-active .slide-bridge-button');
  await page.keyboard.press('Enter');
  await page.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active .chapter-body').scrollTop > 100);
  assert.ok(await page.evaluate(() => document.activeElement.matches('[data-reader-chapter].topic-active')),
    'after Continue reading by keyboard the focus is on the chapter, not on the hidden button');
  const landed = await page.evaluate(() => {
    const card = document.querySelector('[data-reader-chapter].topic-active');
    return card.querySelector('.chapter-headline').getBoundingClientRect().top - card.querySelector('.chapter-body').getBoundingClientRect().top;
  });
  assert.ok(landed > -40 && landed < 120, 'Continue reading brings the full chapter to the top: ' + landed);
  checked.push('Full chapter row at 900, 680 and 560 px', 'row leaves after a scroll', 'island steps back', 'Continue reading');

  // Click zones: each covers exactly the strip of its neighbour that shows.
  await page.goto(`${origin}/html/${PRESENT_PAGE}.html#${PLAIN_CHAPTERS[1]}`, {waitUntil: 'networkidle'});
  await settle(page);
  const zones = await page.evaluate(() => {
    const stage = document.querySelector('.topic-stage').getBoundingClientRect(), active = document.querySelector('[data-reader-chapter].topic-active');
    return ['prev', 'next'].map(side => {
      const zone = document.querySelector('.topic-peek-' + side).getBoundingClientRect();
      const card = (side === 'prev' ? active.previousElementSibling : active.nextElementSibling).getBoundingClientRect();
      const strip = {left: Math.max(card.left, stage.left), right: Math.min(card.right, stage.right), top: card.top, bottom: card.bottom};
      return {side, offBy: Math.max(...['left', 'right', 'top', 'bottom'].map(edge => Math.abs(zone[edge] - strip[edge]))), zone: [zone.left, zone.right, zone.top, zone.bottom], strip};
    });
  });
  assert.ok(zones.every(zone => zone.offBy <= 1.5), 'each click zone covers exactly its visible strip: ' + JSON.stringify(zones));
  await page.locator('.topic-peek-next').hover();
  const lit = await page.evaluate(() => document.querySelector('[data-reader-chapter].topic-active').nextElementSibling.classList.contains('topic-preview-hover'));
  assert.ok(lit, 'the neighbour brightens under the pointer');
  await page.click('.topic-peek-next');
  await waitPresent(page, PLAIN_CHAPTERS[2], 'single');
  await page.click('.topic-peek-prev');
  await waitPresent(page, PLAIN_CHAPTERS[1], 'single');
  await page.click('.reader-island [data-topic-next]');
  await waitPresent(page, PLAIN_CHAPTERS[2], 'single');
  assert.equal((await frameState(page)).place, `4 of ${chapters}`, 'the island counts the step');
  await page.click('.reader-island [data-topic-prev]');
  await waitPresent(page, PLAIN_CHAPTERS[1], 'single');
  checked.push('click zones equal the visible strips', 'neighbour hover', 'island arrows');
  await context.close();

  // Narrow, with touch.
  const phone = await browser.newContext({viewport: {width: 390, height: 844}, reducedMotion: 'reduce', hasTouch: true, isMobile: true});
  const narrow = await phone.newPage();
  await narrow.goto(url, {waitUntil: 'networkidle'});
  await settle(narrow);
  state = await frameState(narrow);
  const bar = await narrow.evaluate(() => [...document.getElementById('chapter-reader').children]
    .filter(node => node.getClientRects().length).map(node => node.className));
  assert.deepEqual(bar, ['reader-icon reader-mobile-menu', 'reader-title'], 'the narrow bar holds the menu button and the page name');
  assert.ok(Math.abs((state.island.left + state.island.right) / 2 - 195) <= 2, 'the island is at the bottom centre: ' + JSON.stringify(state.island));
  assert.ok(state.row.shown && !state.row.pillShown && !state.row.meta, 'narrow: the label and reading time are not shown');
  assert.ok(state.row.button.bottom <= state.island.top && state.island.top - state.row.button.bottom < 24,
    '"Continue reading" sits just above the island: ' + JSON.stringify([state.row.button, state.island]));
  // A drag starts on a line of text, or on a drawing, which keeps its own drags.
  const swipe = (from, to, on = 'p') => narrow.evaluate(([from, to, on]) => {
    const target = [...document.querySelectorAll(`[data-reader-chapter].topic-active .chapter-body ${on}`)]
      .find(node => !node.parentElement.closest('svg, a, button, summary, [data-reader-horizontal]') && node.getBoundingClientRect().height > 0);
    const touch = x => new Touch({identifier: 1, target, clientX: x, clientY: 420});
    target.dispatchEvent(new TouchEvent('touchstart', {bubbles: true, touches: [touch(from)], changedTouches: [touch(from)]}));
    target.dispatchEvent(new TouchEvent('touchend', {bubbles: true, touches: [], changedTouches: [touch(to)]}));
  }, [from, to, on]);
  await swipe(300, 120, 'svg');
  await narrow.waitForTimeout(300);
  assert.equal((await frameState(narrow)).active, FACE_CHAPTER, 'a drag that starts on a drawing does not turn the chapter');
  await swipe(300, 120);
  await waitPresent(narrow, PLAIN_CHAPTERS[0], 'single');
  await swipe(120, 160);
  await narrow.waitForTimeout(300);
  assert.equal((await frameState(narrow)).active, PLAIN_CHAPTERS[0], 'a drag under 70 px does not turn the chapter');
  await swipe(100, 300);
  await waitPresent(narrow, FACE_CHAPTER, 'single');
  checked.push('narrow bar', 'Continue reading above the island', 'swipe');
  await narrow.click('.reader-mobile-menu');
  await narrow.locator('#sidebar .reader-tools').waitFor({state: 'visible'});
  const drawer = await narrow.evaluate(() => ['.reader-tools', '.reader-layers'].map(selector => {
    const node = document.querySelector('#sidebar ' + selector); if (!node || node.hidden) return {selector, absent: true};
    const r = node.getBoundingClientRect(); return {selector, inView: r.left >= 0 && r.right <= innerWidth && r.top >= 0 && r.bottom <= innerHeight && r.width > 0};
  }));
  assert.ok(drawer.every(item => item.inView || item.absent) && !drawer[0].absent, 'the icon row and the options are inside the open drawer: ' + JSON.stringify(drawer));
  await narrow.screenshot({path: path.join(output, '390-drawer.png')});
  await narrow.click('#sidebar [data-reader-view="pair"]');
  await narrow.waitForFunction(() => document.querySelector('main.content').dataset.topicView === 'pair' && !document.body.classList.contains('reader-nav-open'));
  checked.push('controls inside the drawer at 390 px', 'a view choice closes the drawer');
  await phone.close();
  return checked;
}

// The other arrangements and the cross-cutting behaviour of the new controls.
// Two chapters keeps its strip (the pin lives there), both columns and the
// stepper; All chapters reads as one document with the options and Slides
// under Also show; the options and a reader's own fold click survive a reload;
// keyboard order, names, help text, print and reduced motion.
async function reviewArrangements(browser, origin) {
  const url = `${origin}/html/${PRESENT_PAGE}.html`;
  const checked = [];
  const context = await browser.newContext({viewport: {width: 1600, height: 900}, reducedMotion: 'reduce'});
  const page = await context.newPage();
  await page.goto(`${url}#${PLAIN_CHAPTERS[1]}`, {waitUntil: 'networkidle'});
  await settle(page);
  const chapters = await page.locator('[data-reader-chapter]').count();

  await setView(page, 'pair');
  await settle(page);
  const pair = await page.evaluate(() => [...document.querySelectorAll('[data-reader-chapter].topic-visible')].map(card => ({
    id: card.id, header: getComputedStyle(card.querySelector('.chapter-header')).display,
    pin: card.querySelector('.chapter-pin').getClientRects().length > 0, fade: /gradient/.test(getComputedStyle(card, '::after').backgroundImage)})));
  assert.ok(pair.length === 2 && pair.every(card => card.header !== 'none' && card.pin && card.fade),
    'Two chapters keeps the chapter strip with its pin, and both columns fade under the stepper: ' + JSON.stringify(pair));
  assert.equal(await page.locator('.reader-place').textContent(), `3–4 of ${chapters}`, 'the stepper names both columns');
  await page.locator('[data-reader-chapter].topic-visible .chapter-pin').first().click();
  await page.click('.reader-island [data-topic-next]');
  await page.waitForFunction(() => [...document.querySelectorAll('[data-reader-chapter].topic-visible')].map(card => card.id).join() === 'the-reader,existing-markdown');
  assert.equal(await page.locator('[data-reader-chapter].topic-pinned').getAttribute('id'), PLAIN_CHAPTERS[1], 'the pinned column holds while the stepper moves the other');
  checked.push('Two chapters: strip, pin, both columns, stepper, fade');

  // All chapters: the options act on every chapter; the Slides switch is under Also show.
  await setView(page, 'full');
  await settle(page);
  const panel = await page.evaluate(() => [...document.querySelectorAll('#sidebar .reader-layers button')].filter(node => node.getClientRects().length).map(node => node.textContent.trim()));
  assert.deepEqual(panel, ['All', 'Math', 'Code', 'Alternatives', 'Slides'], 'Also show offers the kinds present, All and, in All chapters, Slides');
  const island = await page.evaluate(() => { const r = document.querySelector('.reader-island').getBoundingClientRect(); return r.bottom <= innerHeight && r.top > innerHeight / 2; });
  assert.ok(island, 'in All chapters the stepper rides the bottom of the window');
  const code = () => page.evaluate(() => [...document.querySelectorAll('details.fold[data-fold="code"]')].map(fold => fold.open));
  assert.ok((await code()).every(open => !open), 'code folds start closed');
  await page.click('#sidebar .reader-layer[data-reader-layer="code"]');
  const opened = await code();
  assert.ok(opened.length >= 3 && opened.every(Boolean), 'Code opens every code fold in every chapter: ' + opened);
  await page.locator('details.fold[data-fold="code"] > summary').first().click();
  assert.equal((await code())[0], false, 'a fold click closes that fold');
  await page.goto(`${url}#${PLAIN_CHAPTERS[1]}`, {waitUntil: 'networkidle'});
  await page.reload({waitUntil: 'networkidle'});
  await setView(page, 'full');
  await settle(page);
  const after = await code();
  assert.equal(await page.getAttribute('#sidebar .reader-layer[data-reader-layer="code"]', 'aria-pressed'), 'true', 'the options are remembered for the page');
  assert.ok(after[0] === false && after.slice(1).every(Boolean), 'after a reload the clicked fold stays closed and the others open: ' + after);
  await page.click('#sidebar .reader-layer-all');
  await page.click('#sidebar .reader-layer-all');
  assert.ok((await page.evaluate(() => [...document.querySelectorAll('details.fold')].every(fold => !fold.open))), 'All on then off closes every fold');
  checked.push('All chapters: options on every chapter, Slides under Also show, stepper', 'options and a fold click survive a reload', 'All switch');

  // Keyboard: the row follows the hide button, then the page list; the stepper follows the chapter.
  await setView(page, 'single');
  await settle(page);
  await page.focus('#sidebar .reader-drawer-close');
  const order = [];
  for (let step = 0; step < 7; step++) {
    await page.keyboard.press('Tab');
    order.push(await page.evaluate(() => document.activeElement.getAttribute('aria-label') || document.activeElement.textContent.trim().slice(0, 30)));
  }
  assert.deepEqual(order.slice(0, 6), ['One chapter', 'Two chapters', 'All chapters', 'Presentation', 'About this page', 'Reader help'],
    'Tab reaches every icon in order after the hide button: ' + order);
  assert.ok(await page.evaluate(() => !!document.activeElement.closest('#toc')), 'then the page list');
  // Review finding: Tab never leaves the focus under the fade and the stepper at the bottom.
  await page.goto(`${url}#the-reader`, {waitUntil: 'networkidle'});
  await settle(page);
  await page.focus('[data-reader-chapter].topic-active');
  const covered = [];
  let inside = 0;
  for (let step = 0; step < 60; step++) {
    await page.keyboard.press('Tab');
    const place = await page.evaluate(() => {
      const node = document.activeElement, card = node.closest('[data-reader-chapter].topic-active');
      if (!card) return null;
      const box = node.getBoundingClientRect(), bottom = card.getBoundingClientRect().bottom;
      return {what: node.tagName + ' ' + node.textContent.trim().slice(0, 24), clear: Math.round(bottom - box.bottom), height: Math.round(box.height)};
    });
    if (place) inside += 1;
    if (place && place.height < 300 && place.clear < 70) covered.push(place);
  }
  assert.ok(inside >= 4, 'Tab walks through the chapter: ' + inside);
  assert.deepEqual(covered, [], 'every element Tab reaches in a chapter sits clear of the fade');
  await page.focus('.topic-peek-next');
  await page.keyboard.press('Tab');
  assert.ok(await page.evaluate(() => !!document.activeElement.closest('.reader-island')), 'Tab after the chapter reaches the stepper');
  await page.focus('[data-reader-chapter].topic-active');
  await page.keyboard.press('ArrowRight');
  await waitPresent(page, PLAIN_CHAPTERS[2], 'single');
  await page.keyboard.press('ArrowLeft');
  await waitPresent(page, PLAIN_CHAPTERS[1], 'single');
  await page.click('#sidebar [data-reader-help]');
  const help = await page.locator('.reader-help').textContent();
  assert.ok(/Also show/.test(help) && /row of icons/.test(help) && /stepper/.test(help) && /swipe/.test(help) && !/From start|layer buttons/.test(help),
    'the help describes the reader as it now is');
  await page.keyboard.press('Escape');
  assert.equal(await page.evaluate(() => document.activeElement.getAttribute('data-reader-help') !== null), true, 'closing help returns focus to its icon');
  checked.push('keyboard order and arrow keys', 'help text');

  // Print hides the new controls; reduced motion stops every new transition.
  await page.emulateMedia({media: 'print'});
  const printed = await page.evaluate(() => ['.reader-island', '.reader-tools', '.reader-layers'].map(selector => getComputedStyle(document.querySelector(selector)).display));
  assert.deepEqual(printed, ['none', 'none', 'none'], 'print shows none of the new controls');
  await page.emulateMedia({media: 'screen'});
  const motion = () => page.evaluate(() => [document.querySelector('.reader-island'), document.querySelector('.reader-tool'), document.querySelector('.reader-switch'),
    document.querySelector('[data-reader-chapter].topic-active').nextElementSibling].map(node => getComputedStyle(node).transitionDuration)
    .concat(getComputedStyle(document.querySelector('.reader-switch'), '::after').transitionDuration, getComputedStyle(document.querySelector('.topic-peek-next'), '::after').transitionDuration));
  assert.ok((await motion()).every(value => /^0s(, 0s)*$/.test(value)), 'reduced motion stops the new transitions: ' + await motion());
  await page.emulateMedia({reducedMotion: 'no-preference'});
  assert.ok((await motion()).every(value => !/^0s(, 0s)*$/.test(value)), 'without that preference they move: ' + await motion());
  checked.push('print', 'reduced motion');
  await context.close();
  return checked;
}

(async () => {
  await fs.mkdir(output,{recursive:true});
  const manifest = JSON.parse(await fs.readFile(path.join(root,'site-build.json'),'utf8'));
  const pages = manifest.public_pages.filter(name => /^html\/[^/]+\.html$/.test(name)).map(name => name.slice(5, -5));
  for (const required of ['git', 'documentation-system', 'authoring', 'reader', 'panel-switcher', 'releases', 'migrate-1-1-0'])
    assert.ok(pages.includes(required), 'missing required page ' + required);
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({headless:true});
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
      const faces = [];
      for (const slug of pages) {
        await page.goto(`${origin}/html/${slug}.html`, {waitUntil:'networkidle'});
        const layout = await checkLayout(page);
        images += layout.images.length || 0;
        if (SHOTS.includes(slug)) await page.screenshot({path: path.join(output, `${viewport.width}-${slug}.png`), fullPage: slug === 'index'});
        // Every slide face, in its page and its reader chapter: at 390 px a stacked face must not
        // overflow sideways, clip text or let a part stick out; at 1600 px it must fit 16:9.
        const faceChapters = await page.$$eval('[data-reader-chapter]', nodes => nodes
          .filter(node => node.querySelector('[data-slide-face]')).map(node => node.id));
        for (const id of faceChapters) {
          await goHash(page, `${origin}/html/${slug}.html`, id);
          for (const face of await assertSlideFaces(page, {within: '#' + id}))
            faces.push({page: slug, chapter: id, compact: face.compact, emptyBand: face.emptyBand});
        }
      }
      assert.ok(faces.length >= 2, 'the kit site shows its slide faces: ' + JSON.stringify(faces));
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

      // A hash into a panel-switcher option reveals that panel; adoption routes are all visible.
      await page.goto(`${origin}/html/build-a-site.html#view-page`, {waitUntil:'networkidle'});
      await settle(page);
      assert.equal(await page.locator('#view-page').isVisible(), true);
      assert.equal(await page.locator('#view-markdown').isVisible(), false);
      await page.goto(`${origin}/html/getting-started.html#choose-how-to-adopt-it`, {waitUntil:'networkidle'});
      await settle(page);
      for (const id of ['route-new', 'route-existing', 'route-practices'])
        assert.equal(await page.locator('#' + id).isVisible(), true, id + ' shown side by side');

      // Keyboard: the home paths are reachable by Tab and show focus.
      await page.goto(`${origin}/html/index.html`, {waitUntil:'networkidle'});
      let reached = null;
      for (let step = 0; step < 80 && !reached; step++) {
        await page.keyboard.press('Tab');
        reached = await page.evaluate(() => document.activeElement?.classList.contains('map-card')
          ? {href: document.activeElement.getAttribute('href'), outline: getComputedStyle(document.activeElement).outlineStyle,
             shadow: getComputedStyle(document.activeElement).boxShadow} : null);
      }
      assert.ok(reached, 'a home page card is reachable by keyboard');
      assert.ok(reached.outline !== 'none' || reached.shadow !== 'none', 'focused page card is visibly marked');

      // Pages for people use the chapter reader; rendered records are plain reference pages.
      const peoplePages = ['getting-started', 'build-a-site', 'engineering-practices',
                           'writing-practices', 'experiments', 'approval-failed-open'];
      for (const slug of pages.filter(slug => slug !== 'index')) {
        await page.goto(`${origin}/html/${slug}.html`, {waitUntil:'networkidle'});
        const chapters = await page.locator('section.card[data-reader-chapter]').count();
        if (peoplePages.includes(slug)) assert.ok(chapters > 0, slug + ' has reader chapters');
        else {
          assert.equal(chapters, 0, slug + ' is a plain reference page');
          assert.equal(await page.locator('.source-origin').first().isVisible(), true, slug + ' shows its source line');
        }
      }
      // Sidebar: navigation holds pages for people and the release records. The
      // repository section lists pinned records first, then every record in one
      // "Browse by folder" disclosure, closed on pages for people and pinned records,
      // open to an unpinned record.
      const pinnedRoutes = ['readme.html'];
      const releaseRoutes = ['releases.html', 'migrate-5-8-0.html', 'migrate-5-5-0.html', 'migrate-5-2-0.html', 'migrate-5-1-0.html', 'migrate-5-0-0.html', 'migrate-4-0-0.html', 'migrate-3-2-0.html', 'migrate-3-1-0.html', 'migrate-3-0-0.html', 'migrate-2-0-0.html', 'migrate-1-1-0.html'];
      for (const [slug, open, folders] of [['index', false, []], ['getting-started', false, []],
                                           ['releases', false, ['docs/', 'topics/', 'releases/']],
                                           ['git', true, ['rules/', 'engineering/']]]) {
        await page.goto(`${origin}/html/${slug}.html`, {waitUntil:'networkidle'});
        const tree = await page.evaluate(() => ({
          nav: [...document.querySelectorAll('.toc a.xpage')].map(a => a.getAttribute('href')),
          pinned: [...document.querySelectorAll('.repo-tree-pinned a')].map(a => a.getAttribute('href')),
          current: [...document.querySelectorAll('.repo-tree [aria-current="page"]')].map(a => a.getAttribute('href')),
          open: document.querySelector('.repo-tree details.repo-tree-all').open,
          folders: [...document.querySelectorAll('.repo-tree-folder > details[open] > summary .repo-tree-name')].map(n => n.textContent),
          files: [...document.querySelectorAll('.repo-tree a.repo-tree-file')].map(a => a.getAttribute('href'))}));
        assert.ok(tree.nav.every(href => peoplePages.includes(href.slice(0, -5)) || releaseRoutes.includes(href)), 'navigation lists pages for people and release records: ' + tree.nav);
        assert.deepEqual(tree.nav.filter(href => releaseRoutes.includes(href)), releaseRoutes, 'release records listed in the navigation');
        assert.deepEqual(tree.pinned, pinnedRoutes, 'pinned records in declared order');
        assert.deepEqual(tree.files.sort(), Object.keys(manifest.source_pages).sort(), 'the tree lists exactly the registered records');
        assert.deepEqual(tree.current, peoplePages.includes(slug) || slug === 'index' || releaseRoutes.includes(slug + '.html') ? [] : [slug + '.html'], slug + ' current mark');
        assert.equal(tree.open, open, slug + ' Browse by folder disclosure ' + (open ? 'open' : 'closed'));
        assert.deepEqual(tree.folders, folders, slug + ' unfolds only the folders to its own file');
      }
      // Carousel: the arrows stay on the picture shown and cover no dot, however many rows the dots take.
      await page.goto(`${origin}/html/build-a-site.html#figures-and-slides`, {waitUntil:'networkidle'});
      const arrows = await page.evaluate(() => {
        const box = document.querySelector('#figures-and-slides .fig-carousel');
        const shown = box.querySelector(':scope > img.fc-active').getBoundingClientRect();
        const buttons = [...box.querySelectorAll('.fc-btn')].map(button => button.getBoundingClientRect());
        const dots = [...box.querySelectorAll('.fc-dot')].map(dot => dot.getBoundingClientRect());
        const overlap = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
        return {offset: buttons.map(button => Math.round(button.top + button.height / 2 - shown.top - shown.height / 2)),
          covered: dots.filter(dot => buttons.some(button => overlap(dot, button))).length,
          rows: new Set(dots.map(dot => Math.round(dot.top))).size, slides: dots.length, height: Math.round(shown.height)};
      });
      assert.ok(arrows.height > 0 && arrows.offset.length === 2 && arrows.offset.every(value => Math.abs(value) <= 1) && arrows.covered === 0,
        'carousel arrows sit on the picture and cover no dot: ' + JSON.stringify(arrows));
      await page.goto(`${origin}/html/build-a-site.html`, {waitUntil:'networkidle'});
      if (viewport.width >= 900) {
        // The reader stage uses the content width; no line-length cap leaves the right side blank.
        const stage = await page.evaluate(() => ({card: document.querySelector('section.card[data-reader-chapter]').getBoundingClientRect().width,
                                                  main: document.querySelector('main.content').getBoundingClientRect().width}));
        assert.ok(stage.card > 0.8 * stage.main, 'reader card fills the stage: ' + JSON.stringify(stage));
        await page.click('button[data-reader-view="pair"]');
        assert.equal(await page.getAttribute('button[data-reader-view="pair"]', 'aria-pressed'), 'true', 'two-chapter view selectable');
        await page.click('button[data-reader-view="single"]');

        // Reader tour: docking, pinning and the carousel work as the tour describes.
        await page.goto(`${origin}/html/build-a-site.html#how-a-build-works`, {waitUntil:'networkidle'});
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
        assert.ok(shown.includes('how-a-build-works') && !shown.includes('write-a-topic-page'), 'pinned chapter holds while the other column moves: ' + shown);
        await page.click('button[data-reader-view="single"]');
        await page.goto(`${origin}/html/build-a-site.html#figures-and-slides`, {waitUntil:'networkidle'});
        const slides = await page.$$eval('#figures-and-slides .fig-carousel > img', imgs => imgs.filter(img => getComputedStyle(img).display !== 'none').length);
        assert.equal(slides, 1, 'carousel shows one capture at a time');
      }

      if (viewport.width < 900) {
        // The menu opens navigation over content; tables scroll inside their region.
        // Reader pages open navigation from the reader bar; reference pages from the shell menu.
        await page.goto(`${origin}/html/build-a-site.html`, {waitUntil:'networkidle'});
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
        const treeFile = page.locator('.repo-tree a[aria-current="page"]');
        await treeFile.scrollIntoViewIfNeeded();
        assert.equal(await treeFile.isVisible(), true, 'narrow menu reaches the current file in the repository tree');
        const folder = page.locator('.repo-tree summary', {hasText: 'writing/'});
        await folder.click();
        assert.equal(await folder.evaluate(node => node.parentElement.open), true, 'a closed folder opens from the narrow menu');
        await page.goto(`${origin}/html/releases.html`, {waitUntil:'networkidle'});
        const region = page.locator('.scroll[role="region"]').first();
        const metrics = await region.evaluate(el => ({scroll: el.scrollWidth, client: el.clientWidth}));
        assert.ok(metrics.scroll > metrics.client, 'narrow release table scrolls in place: ' + JSON.stringify(metrics));
        await region.focus();
        await page.keyboard.press('ArrowRight');
        await page.waitForFunction(() => document.querySelector('.scroll[role="region"]').scrollLeft > 0);
      }

      results.viewports[viewport.width] = {presentation: await reviewPresentation(page, origin, viewport, failures)};

      // Print: every adoption route is visible and edit controls are hidden.
      await page.emulateMedia({media:'print'});
      await page.goto(`${origin}/html/getting-started.html`, {waitUntil:'networkidle'});
      for (const id of ['route-new', 'route-existing', 'route-practices'])
        assert.equal(await page.locator('#' + id).isVisible(), true, id + ' prints');
      await page.goto(`${origin}/html/git.html`, {waitUntil:'networkidle'});
      assert.equal(await page.locator('.source-origin-edit').isVisible(), false, 'edit link hidden in print');
      await page.emulateMedia({media:'screen'});
      Object.assign(results.viewports[viewport.width], {pages: pages.length, visibleImages: images, keyboard: reached.href, slideFaces: faces});
      await context.close();
    }

    results.frame = await reviewFrame(browser, origin);
    results.arrangements = await reviewArrangements(browser, origin);

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
  console.log(`Own site: ${results.pages} pages contained with visible media at 1600 and 390; slide faces fit at 1600 and stack cleanly at 390; deep links, panel hash, keyboard paths, reader chapters, sidebar repository tree, views, docking, pinning and carousel, Presentation and the Slides switch, the reader frame (icon row, island, Full chapter row at three heights, click zones, swipe, drawer at 390), Two and All chapters, options and fold clicks across a reload, keyboard order, help text, print and reduced motion of the new controls, narrow menu/tree/table scrolling, print and no-JavaScript reading pass.`);
})().catch(error => { console.error(error); process.exitCode = 1; server.close(); });
