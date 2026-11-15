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
async function reviewPresentation(page, origin, viewport, failures) {
  const url = `${origin}/html/${PRESENT_PAGE}.html`;
  const checked = [];
  const select = viewport.width < 900, narrow = viewport.width < 720;
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
  assert.ok(state.bar && state.toolbar === 'none' && state.sidebar === 'none', 'only the presentation controls show: ' + JSON.stringify(state));
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
    assert.ok(state.toolbar !== 'none' && !state.bar, 'the reader toolbar returns');
  }
  checked.push('exit restores Two chapters and All chapters');

  // From start begins at the first chapter; focus returns to the starting control.
  await setView(page, 'single');
  await page.waitForFunction(() => document.querySelector('[data-reader-chapter].topic-active')?.id === 'the-reader');
  if (select) await page.selectOption('[data-reader-view-select]', 'present-start');
  else await page.click('[data-reader-present-start]');
  state = await waitPresent(page, FACE_CHAPTER);
  assert.equal(state.scroll, 0, 'From start opens the first slide');
  await page.keyboard.press('Shift+Tab');
  const close = await page.evaluate(() => ({inBar: !!document.activeElement?.closest('.present-bar'),
    outline: getComputedStyle(document.activeElement).outlineStyle}));
  assert.ok(close.inBar && close.outline !== 'none', 'Shift+Tab reaches the visible presentation controls: ' + JSON.stringify(close));
  await page.keyboard.press('Escape');
  state = await waitPresent(page, FACE_CHAPTER, 'single');
  const returned = await page.evaluate(select => {
    const node = document.activeElement;
    return select ? !!node?.closest('[data-reader-view-select], [data-reader-chapter].topic-active') : !!node?.matches('[data-reader-present-start]');
  }, select);
  assert.ok(returned, 'focus returns to the starting control, or to the chapter when the menu started it');
  checked.push('From start', 'focus on enter and exit');

  // The controls fade when idle and return on pointer movement; fullscreen is optional.
  if (!select) {
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
  await page.click('[data-reader-slides]');
  shown = await faces();
  assert.deepEqual([shown.face !== 'none', shown.bridge !== 'none', shown.pressed], [true, true, 'true'], 'the switch shows slides');
  await page.emulateMedia({media: 'print'});
  assert.notEqual((await faces()).face, 'none', 'print follows the switch (on)');
  await page.emulateMedia({media: 'screen'});
  await page.reload({waitUntil: 'networkidle'});
  await setView(page, 'full');
  shown = await faces();
  assert.deepEqual([shown.face !== 'none', shown.pressed], [true, 'true'], 'the switch is remembered for the page');
  await page.click('[data-reader-slides]');
  assert.equal((await faces()).face, 'none', 'the switch hides slides again');
  checked.push('Slides switch off by default, on after the click, remembered, print');

  // A page without slide faces offers neither Presentation nor Slides.
  await page.goto(`${origin}/html/experiments.html?view=present`, {waitUntil: 'networkidle'});
  await setView(page, 'full');
  const plain = await page.evaluate(() => ({controls: [...document.querySelectorAll('[data-reader-view="present"], [data-reader-present-start], [data-reader-slides]')].filter(node => node.getClientRects().length).length,
    options: document.querySelectorAll('[data-reader-view-select] option[value^="present"]').length, view: document.querySelector('main.content').dataset.topicView,
    bar: document.querySelectorAll('.present-bar').length, search: location.search}));
  assert.deepEqual(plain, {controls: 0, options: 0, view: 'single', bar: 0, search: ''}, 'no Presentation without slide faces');
  checked.push('pages without faces');
  assert.deepEqual(failures, [], 'browser errors during presentation checks at ' + viewport.width);
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
      const releaseRoutes = ['releases.html', 'migrate-5-1-0.html', 'migrate-5-0-0.html', 'migrate-4-0-0.html', 'migrate-3-2-0.html', 'migrate-3-1-0.html', 'migrate-3-0-0.html', 'migrate-2-0-0.html', 'migrate-1-1-0.html'];
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
  console.log(`Own site: ${results.pages} pages contained with visible media at 1600 and 390; slide faces fit at 1600 and stack cleanly at 390; deep links, panel hash, keyboard paths, reader chapters, sidebar repository tree, views, docking, pinning and carousel, Presentation and the Slides switch, narrow menu/tree/table scrolling, print and no-JavaScript reading pass.`);
})().catch(error => { console.error(error); process.exitCode = 1; server.close(); });
