// Logic checks for the shared chapter reader and fold controls, without a
// browser. Runs theme/components/chapter-reader.js and fold-controls.js in a
// small fake DOM (tests/reader_harness.cjs) on a synthetic page; the reader
// toolbar comes from the real chapter-reader.html. Covered: navigation, pins,
// scroll restore, history, deep links, fold wrapping and key ownership,
// dialogs, per-column layers and fold caches, presets and their storage,
// legacy migration, the navigation drawer, print, reduced motion, page
// identities, redirects, jump groups and the fold-controls opt-in.
// Ported from ADP's experiments/track_geometry/test_road_review_topics.cjs at
// commit e21c2e84. Its layout and stylesheet-value checks were not ported:
// widths here are fixture input that selects code paths, not layout claims.
const assert = require('node:assert/strict');
const {CHAPTERS, SITE_PAGES, FIXTURE, FakeElement, rect, readComponent, bootReader, runFoldControls} =
  require('./reader_harness.cjs');

const N = CHAPTERS.length;
const ids = indices => indices.map(index => CHAPTERS[index].id);
const WIDTHS = [{width: 304, gap: 12}, {width: 744, gap: 16}, {width: 1200, gap: 16}];
const deepLink = page => {
  const link = new FakeElement('a', page.document);
  link.href = new URL('#' + FIXTURE.deepTarget, page.location).href;
  return link;
};

function checkNavigationAndPins() {
  // Without JavaScript the toolbar stays hidden and the page reads as source.
  const scriptless = bootReader('', {runReader: false});
  assert.equal(scriptless.nav.hidden, true, 'chapter-reader.html keeps the toolbar hidden until the script runs');
  assert.equal(scriptless.nav.dataset.foldControls, 'columns', 'chapter-reader.html opts out of the global fold bar');
  for (const layout of WIDTHS) {
    const at = `width ${layout.width}`;
    const page = bootReader('', layout);
    assert.equal(page.nav.hidden, false, 'The reader reveals its hidden toolbar');
    assert.equal(page.history.scrollRestoration, 'manual', 'Deck view takes over scroll restoration');
    assert.ok(page.control('prev').disabled, 'Previous is disabled on the first chapter');
    assert.equal(page.content.style.getPropertyValue('--topic-scroll-offset'), FIXTURE.navHeight + 12 + 'px',
      'The scroll offset clears the toolbar height');
    page.assertCentred(0, `${at}, first chapter`);
    for (let index = 1; index < N; index++) {
      page.bodies[index - 1].scrollTop = (index - 1) * 137 + 50;
      page.chapterKey('ArrowRight');
      page.assertCentred(index, `${at}, ArrowRight to chapter ${index + 1}`);
      assert.equal(page.location.hash, '#' + CHAPTERS[index].id, 'ArrowRight writes the chapter to the URL');
      assert.equal(page.control('count').textContent, `Chapter ${index + 1} of ${N}`, 'The status names the position');
      assert.equal(page.links[index].getAttribute('aria-current'), 'step', 'The active chapter link is marked current');
      assert.equal(page.document.activeElement, page.sections[index], 'Focus follows the active chapter');
      assert.ok(page.strip.classes.has('topic-animate'), 'Keyboard moves animate the strip');
    }
    assert.ok(page.control('next').disabled, 'Next is disabled on the last chapter');
    page.back();
    assert.equal(page.bodies[N - 2].scrollTop, (N - 2) * 137 + 50, 'Back restores the reading position');
    for (let index = N - 3; index >= 0; index--) {
      page.chapterKey('ArrowLeft');
      assert.equal(page.bodies[index].scrollTop, index * 137 + 50, 'Each chapter resumes where it was left');
    }

    page.bodies[0].scrollTop = 610;
    page.click(page.control('pair'));
    page.assertPair(0, 1, `${at}, pair view`);
    page.bodies[1].scrollTop = 830;
    page.pin(0);
    page.chapterKey('ArrowRight');
    page.assertPair(0, 2, 'A pinned left column stays while the right moves');
    assert.equal(page.bodies[0].scrollTop, 610, 'The pinned column keeps its position');
    page.bodies[2].scrollTop = 450;
    page.chapterKey('ArrowLeft');
    page.assertPair(0, 1, 'The unpinned column moves back');
    assert.equal(page.bodies[1].scrollTop, 830, 'The returning column resumes its position');
    page.chapterKey('ArrowRight');
    page.assertPair(0, 2);
    page.pin(2);
    page.chapterKey('ArrowRight');
    page.assertPair(1, 2, 'Pinning the right column moves the left one instead');
    page.chapterKey('ArrowRight');
    page.assertPair(3, 2, 'The moving column skips the pinned chapter');
    assert.equal(page.bodies[2].scrollTop, 450, 'The pinned right column keeps its position');
    assert.equal(page.sections.filter(node => node.classes.has('topic-pinned')).length, 1, 'Only one chapter is pinned');
    page.back();
    page.assertPair(1, 2, 'Back restores the previous pair');
    assert.equal(page.history.state.chapterReader.pinned, 1, 'History keeps which column is pinned');
    page.pin(2);
    page.chapterKey('ArrowRight');
    page.assertPair(2, 3, 'Unpinning lets both columns move together');
  }
  return 'navigation, scroll restore, history and both pins at three viewport widths';
}

function checkFoldsKeysAndDrawer() {
  const page = bootReader('#notation');
  page.bodies[1].scrollTop = 860;
  for (const section of page.sections) {
    for (const fold of section.querySelectorAll('details.fold')) {
      assert.equal(fold.querySelector('summary .fold-title').textContent, 'Details', 'The fold summary keeps its title');
      assert.ok(fold.querySelector('.fold-content'), 'Every typed fold receives its reading panel');
      assert.ok(fold.querySelector('.fold-content p').textContent.includes('Layer content'),
        'The original fold content stays inside its fold');
    }
  }
  const equation = page.document.getElementById('display-equation');
  const table = page.document.getElementById('depth-table');
  assert.equal(equation.textContent, '$$x^2 + y^2 = r^2$$', 'Display equations keep their text');
  assert.ok(equation.classes.has('fold-equation'), 'Display equations are marked as horizontal regions');
  assert.equal(equation.tabIndex, 0, 'Display equations are focusable for keyboard scrolling');
  assert.equal(table.textContent, '123 preserved', 'Tables keep their content');
  assert.equal(table.parentElement.tabIndex, 0, 'Tables are wrapped in a focusable scroller');
  assert.ok(!page.key('ArrowRight', {target: equation}).defaultPrevented, 'Equation scrolling owns its arrow keys');
  assert.ok(!page.key('ArrowRight', {target: table}).defaultPrevented, 'Table scrolling owns its arrow keys');

  const deep = FIXTURE.deepChapter;
  assert.ok(page.click(deepLink(page)).defaultPrevented, 'A link into a fold is routed by the reader');
  assert.deepEqual(page.visible(), ids([deep]), 'A deep link shows the chapter that holds its target');
  assert.equal(page.bodies[deep].scrollTop, FIXTURE.layerOffset - 12, 'A deep link scrolls its target to the body top');
  assert.equal(page.folds(deep)[0].open, true, 'A deep link opens the fold around its target');
  // Widgets keep state on their own nodes; the reader must move, not clone.
  page.sections[deep].widgetChoice = {scenario: 'B'};
  page.chapterKey('ArrowRight');
  page.bodies[deep + 1].scrollTop = 425;
  page.chapterKey('ArrowLeft');
  assert.equal(page.bodies[deep].scrollTop, FIXTURE.layerOffset - 12, 'The deep-linked chapter resumes its position');
  assert.deepEqual(page.sections[deep].widgetChoice, {scenario: 'B'}, 'Chapters are moved, not cloned');

  for (const tag of ['input', 'select', 'textarea', 'button', 'a', 'summary', 'svg', 'canvas', 'video', 'audio', 'iframe']) {
    const target = new FakeElement(tag, page.document);
    assert.ok(!page.key('ArrowRight', {target}).defaultPrevented, `A focused ${tag} keeps its arrow keys`);
  }
  for (const flag of ['defaultPrevented', 'repeat', 'altKey', 'ctrlKey', 'metaKey', 'shiftKey']) {
    page.chapterKey('ArrowRight', {[flag]: true});
    assert.deepEqual(page.visible(), ids([deep]), `An arrow key with ${flag} does not change chapter`);
  }
  const overlay = page.document.createElement('div');
  overlay.className = 'lb-overlay';
  page.document.body.appendChild(overlay);
  assert.ok(!page.chapterKey('ArrowRight').defaultPrevented, 'An open lightbox keeps the arrow keys');
  overlay.parentNode.removeChild(overlay);

  page.click(page.control('drawer'));
  assert.equal(page.sidebar.inert, false, 'The opened drawer is interactive');
  assert.equal(page.content.inert, true, 'An overlay drawer makes the page inert');
  assert.ok(!page.chapterKey('ArrowRight').defaultPrevented, 'An overlay drawer keeps the arrow keys');
  assert.equal(page.bodies[deep].scrollTop, FIXTURE.layerOffset - 12, 'Opening the drawer keeps the position');
  page.key('Escape');
  assert.equal(page.content.inert, false, 'Escape closes the drawer');
  assert.equal(page.sidebar.inert, true, 'A closed drawer is inert');
  assert.equal(page.document.activeElement, page.control('drawer'), 'Closing the drawer returns focus to its button');
  page.click(page.control('drawer'));
  page.click(page.links[1]);
  assert.deepEqual(page.visible(), ids([1]), 'A drawer link opens its chapter');
  assert.equal(page.bodies[1].scrollTop, 860, 'A drawer link resumes the chapter position');
  assert.equal(page.content.inert, false, 'An overlay drawer closes after choosing a chapter');
  assert.equal(page.sidebar.querySelector('.reader-home').textContent, FIXTURE.brandMark + FIXTURE.brandName,
    'The drawer header repeats the sidebar brand');

  const external = new FakeElement('a', page.document);
  external.href = 'https://example.com/#notation';
  assert.ok(!page.click(external).defaultPrevented, 'Links to other sites are left to the browser');
  assert.ok(!page.click(page.links[1], {ctrlKey: true}).defaultPrevented, 'Modifier-key clicks are left to the browser');

  const about = page.document.querySelector('.reader-about');
  const help = page.document.querySelector('.reader-help');
  page.click(page.control('about'));
  assert.ok(about.open, 'The about button opens its dialog');
  assert.ok(!page.chapterKey('ArrowRight').defaultPrevented, 'An open dialog keeps the arrow keys');
  page.click(about.querySelector('.reader-text-button'));
  assert.ok(help.open && !about.open, 'The about dialog hands over to the help dialog');
  help.emit('cancel');
  assert.equal(page.document.activeElement, page.control('about'), 'Closing help returns focus to its trigger');

  const row = page.read(1);
  assert.equal(row.querySelectorAll('button').length, 6, 'Each chapter has Story, four layers and All inline');
  assert.equal(page.document.querySelector('.reader-popover'), null, 'Layers stay inline instead of opening a menu');
  assert.ok(!page.key('ArrowRight', {target: row.querySelector('button')}).defaultPrevented,
    'Layer buttons keep their arrow keys');
  return 'fold wrapping, equation and table key ownership, deep links, external and modifier links, '
    + 'drawer, dialogs and inline layers';
}

// Layers follow the column, including a pinned chapter. Manual folds are cached
// per chapter and column; explicit choices replace that column's old defaults.
function checkColumnLayers() {
  const page = bootReader('#notation');
  page.click(page.control('pair'));
  page.assertPair(1, 2);
  page.read(1); page.layers(['math', 'experiment']);
  assert.deepEqual(page.states(1), [true, true, false, false], 'Left layers open the left chapter folds');
  assert.deepEqual(page.states(2), [false, false, false, false], 'Left layers leave the right column closed');
  page.read(2); page.layers(['code', 'dead-end']);
  assert.deepEqual(page.states(1), [true, true, false, false], 'Right layers leave the left column alone');
  assert.deepEqual(page.states(2), [false, false, true, true], 'Right layers open the right chapter folds');
  page.pin(1);
  page.chapterKey('ArrowRight');
  page.assertPair(1, 3);
  assert.deepEqual(page.states(1), [true, true, false, false], 'The pinned chapter keeps its layers');
  assert.deepEqual(page.states(3), [false, false, true, true], 'A chapter entering a column takes that column\'s layers');
  page.folds(3)[0].open = true;
  page.folds(3)[3].open = false;
  page.chapterKey('ArrowRight');
  page.chapterKey('ArrowLeft');
  assert.deepEqual(page.states(3), [true, false, true, false], 'Manual folds resume on return');
  page.read(1); page.layers(['experiment']);
  assert.deepEqual(page.states(3), [true, false, true, false], 'Changing the pinned column leaves the other column alone');
  page.read(3); page.layers(['math']);
  page.chapterKey('ArrowRight');
  page.chapterKey('ArrowLeft');
  assert.deepEqual(page.states(3), [true, false, false, false], 'Explicit layers replace earlier manual folds');
  page.read(3);
  page.click(page.sections[3].querySelector('[data-reader-preset="all"]'));
  assert.deepEqual(page.states(3), [true, true, true, true], 'The All preset opens every layer');
  page.click(page.sections[3].querySelector('[data-reader-preset="story"]'));
  assert.deepEqual(page.states(3), [false, false, false, false], 'The Story preset closes every layer');
  const profileKey = 'foldcolumns:' + page.location.pathname;
  assert.ok(page.storage.has(profileKey), 'Column layer choices are stored under the page-scoped foldcolumns key');
  assert.deepEqual(JSON.parse(page.storage.get(profileKey)), [['experiment'], []],
    'Column layer choices are stored under the page-scoped foldcolumns key');

  page.read(3); page.layers(['code']);
  page.chapterKey('ArrowRight');
  page.read(4); page.layers(['math', 'experiment']);
  page.back();
  page.assertPair(1, 3, 'Back restores the pair');
  assert.deepEqual(page.states(3), [true, true, false, false], 'Back restores the arrangement, not old layer choices');
  assert.equal(page.history.state.chapterReader.activeColumn, 1, 'History keeps the active column');
  page.click(page.control('single'));
  assert.deepEqual(page.visible(), ids([3]), 'Single view keeps the active right chapter');
  page.read(3); page.layers(['dead-end']);
  page.click(page.control('pair'));
  page.assertPair(2, 3, 'Pair view from a right-column chapter keeps it on the right');
  assert.deepEqual(page.states(2), [false, true, false, false], 'The left column restores its own layers');
  assert.deepEqual(page.states(3), [false, false, false, true], 'The right column restores its own layers');

  // Move a manually edited chapter to the opposite column, then back.
  page.folds(3)[0].open = true;
  page.sections[2].emit('pointerdown');
  page.click(page.links[4]);
  page.assertPair(4, 3);
  page.click(page.links[5]);
  page.sections[3].emit('pointerdown');
  page.click(page.links[6]);
  page.sections[5].emit('pointerdown');
  page.click(page.links[3]);
  page.assertPair(3, 6);
  assert.deepEqual(page.states(3), [false, true, false, false], 'The same chapter has a separate left-column fold cache');
  page.click(page.links[5]);
  page.sections[6].emit('pointerdown');
  page.click(page.links[3]);
  page.assertPair(5, 3);
  assert.deepEqual(page.states(3), [true, false, false, true], 'Returning to the right restores its manual fold');
  return 'per-column layers, manual fold cache per chapter and column, Story/All presets, foldcolumns storage and back/forward';
}

function checkStoredProfiles() {
  const pathname = bootReader('', {runReader: false}).location.pathname;
  const legacyKey = 'foldmode:' + pathname;
  const profileKey = 'foldcolumns:' + pathname;
  for (const mode of ['all', 'math', 'experiment', 'code', 'dead-end', 'none']) {
    const page = bootReader('', {stored: {[legacyKey]: mode}});
    page.click(page.control('pair'));
    const expected = ['math', 'experiment', 'code', 'dead-end'].map(kind => mode === 'all' || mode === kind);
    assert.deepEqual(page.states(0), expected, `A legacy foldmode "${mode}" migrates to the left column`);
    assert.deepEqual(page.states(1), expected, `A legacy foldmode "${mode}" migrates to the right column`);
  }
  const saved = bootReader('', {stored: {[profileKey]: JSON.stringify([['math'], ['experiment', 'code']]), [legacyKey]: 'all'}});
  saved.click(saved.control('pair'));
  assert.deepEqual(saved.states(0), [true, false, false, false], 'A stored column profile wins over the legacy mode (left)');
  assert.deepEqual(saved.states(1), [false, true, true, false], 'A stored column profile wins over the legacy mode (right)');
  const corrupt = bootReader('', {stored: {[profileKey]: 'broken JSON', [legacyKey]: 'math'}});
  assert.deepEqual(corrupt.states(0), [true, false, false, false], 'A corrupt stored profile falls back to the legacy mode');

  const page = bootReader('');
  page.click(page.control('pair'));
  const kinds = ['math', 'experiment', 'code', 'dead-end'];
  for (const side of [0, 1]) {
    for (let mask = 0; mask < 16; mask++) {
      const other = page.states(1 - side);
      const chosen = kinds.filter((_, bit) => mask & (1 << bit));
      page.read(side); page.layers(chosen);
      assert.deepEqual(page.states(side), kinds.map(kind => chosen.includes(kind)),
        `Layers [${chosen}] open exactly those folds`);
      assert.deepEqual(page.states(1 - side), other, 'Every layer combination leaves the other column untouched');
    }
  }
  return 'legacy foldmode migration, stored and corrupt column profiles, all 16 layer combinations per column';
}

function checkDrawerFocusAndSelection() {
  const drawer = bootReader('');
  drawer.click(drawer.control('drawer'));
  const first = drawer.sidebar.querySelector('.reader-home');
  const last = drawer.sidebar.querySelectorAll('.toc a.xpage').at(-1);
  last.focus({preventScroll: true});
  assert.ok(drawer.key('Tab').defaultPrevented, 'Tab from the last drawer link is trapped');
  assert.equal(drawer.document.activeElement, first, 'Tab wraps to the first drawer control');
  assert.ok(drawer.key('Tab', {shiftKey: true}).defaultPrevented, 'Shift-Tab from the first drawer control is trapped');
  assert.equal(drawer.document.activeElement, last, 'Shift-Tab wraps to the last drawer link');
  assert.equal(drawer.sidebar.querySelectorAll('[role="tab"]').length, 0, 'Site pages and chapters share one tree, without tabs');
  assert.ok(!drawer.key('ArrowRight', {target: last}).defaultPrevented, 'Site links keep their arrow keys');
  assert.equal(drawer.sidebar.querySelector('#reader-chapter-list').hidden, false, 'The chapter list is shown in the drawer');
  drawer.backdrop.emit('click');
  assert.equal(drawer.sidebar.inert, true, 'A backdrop click closes the drawer');
  assert.equal(drawer.document.activeElement, drawer.control('drawer'), 'A backdrop close returns focus to the menu button');

  const page = bootReader('#notation');
  page.click(page.control('pair'));
  page.sections[2].emit('pointerdown');
  page.bodies[2].scrollTop = 630;
  assert.equal(page.history.state.chapterReader.activeColumn, 1, 'Selecting a column is recorded in history');
  page.chapterKey('ArrowRight');
  page.back();
  page.assertPair(1, 2);
  assert.ok(page.sections[2].classes.has('topic-active'), 'The restored right column stays active');
  page.read(2); page.layers(['code']);
  page.click(page.control('single'));
  assert.deepEqual(page.visible(), ids([2]), 'Back keeps the selected right column even when the URL names the left');
  assert.equal(page.bodies[2].scrollTop, 630, 'The selected column keeps its position');
  return 'drawer Tab trap, backdrop close and focus return, active column kept through history';
}

// Layer changes keep the paragraph being read in place, or bring the summary
// of a closing fold into view.
function checkViewportAnchor() {
  const page = bootReader('');
  const body = page.bodies[0];
  const below = offset => FIXTURE.bodyTop + offset - body.scrollTop; // viewport top of a body offset
  const paragraph = page.document.getElementById('story-0');
  const math = page.folds(0)[0];
  page.read(0); page.layers(['math']);
  // The paragraph sits below the Math fold, further down while it is open.
  paragraph.rectFn = () => rect(below(math.open ? 400 : 200), 0, 200, 100);
  body.scrollTop = 388;
  const originalTop = paragraph.getBoundingClientRect().top;
  page.read(0); page.layers([]);
  assert.equal(paragraph.getBoundingClientRect().top, originalTop, 'Closing a fold above the paragraph keeps it in place');
  paragraph.rectFn = () => rect(below(230), 0, 200, 100);
  page.flush();
  assert.equal(paragraph.getBoundingClientRect().top, originalTop, 'A late figure reflow keeps that anchor too');

  paragraph.rectFn = () => rect(0, 0, 0, 0);
  const inside = math.querySelector('p');
  const summary = math.querySelector('summary');
  page.read(0); page.layers(['math']);
  summary.rectFn = () => rect(below(200), 0, 200, 44);
  inside.rectFn = () => rect(below(270), 0, 200, 200);
  body.scrollTop = 300;
  page.read(0); page.layers([]);
  const top = summary.getBoundingClientRect().top;
  assert.ok(top >= FIXTURE.bodyTop && top < FIXTURE.bodyTop + 620, 'Closing the fold being read keeps its summary in view');
  return 'viewport anchor kept on layer change and late reflow';
}

function checkFullPagePrintAndBoot() {
  const page = bootReader('#notation');
  page.click(page.control('pair'));
  page.sections[2].emit('pointerdown');
  page.read(2); page.layers(['code']);
  page.bodies[1].scrollTop = 860;
  page.bodies[2].scrollTop = 420;
  page.click(page.control('full'));
  assert.equal(page.visible().length, N, 'Full page shows every chapter');
  assert.equal(page.history.scrollRestoration, 'auto', 'Full page returns scroll restoration to the browser');
  assert.ok(page.sections.every((_, index) => JSON.stringify(page.states(index)) === '[false,false,true,false]'),
    'Full page applies the active column layers to every chapter');
  assert.ok(!page.chapterKey('ArrowRight').defaultPrevented, 'Full page leaves arrow keys to the browser');
  page.bodies.forEach(body => { body.scrollTop = 0; });
  page.sections.forEach((section, index) => { section.top = index <= 4 ? -500 : 1000; });
  page.window.emit('scroll');
  page.click(page.control('pair'));
  page.assertPair(1, 4, 'Leaving full page puts the scrolled-to chapter in the active column');
  assert.equal(page.history.state.chapterReader.activeColumn, 1, 'Full page returns the active chapter to its side');
  assert.equal(page.bodies[1].scrollTop, 860, 'Leaving full page restores the left position');
  assert.equal(page.bodies[2].scrollTop, 420, 'Leaving full page restores the right position');
  page.click(page.control('single'));
  page.assertCentred(4);
  page.click(page.control('pair'));
  page.assertPair(3, 4);

  const beforePrint = page.sections.map((_, index) => page.states(index));
  page.window.emit('beforeprint');
  assert.equal(page.overview.parentElement, page.content, 'Print puts the page introduction back in the page');
  assert.ok(page.sections.every((_, index) => page.states(index).every(Boolean)), 'Print opens every layer in every chapter');
  page.window.emit('afterprint');
  page.flush();
  assert.equal(page.overview.parentElement, page.document.querySelector('.reader-about'),
    'After print the introduction returns to About');
  assert.deepEqual(page.sections.map((_, index) => page.states(index)), beforePrint, 'After print every fold choice is restored');
  page.pin(3);
  page.click(page.control('full'));
  page.click(page.links[6]);
  page.click(page.control('pair'));
  page.assertPair(3, 6);
  assert.ok(page.sections[3].classes.has('topic-pinned'), 'Returning from full page does not move a pinned chapter');

  for (const hash of ['#unknown', '#%E0%A4%A', '#chapter-reader']) {
    assert.deepEqual(bootReader(hash).visible(), ids([0]), `The bad hash ${hash} opens the first chapter`);
  }
  const deep = bootReader('#' + FIXTURE.deepTarget);
  assert.deepEqual(deep.visible(), ids([FIXTURE.deepChapter]), 'A deep link at load shows its chapter');
  assert.ok(deep.folds(FIXTURE.deepChapter)[0].open, 'A deep link at load opens its fold');
  for (const layout of WIDTHS) {
    const page = bootReader('#legacy-formula', {...layout,
      subsections: [{id: 'legacy-formula', label: 'Legacy formula', chapter: 6, fold: 0}]});
    assert.deepEqual(page.visible(), ids([6]), 'A subsection link at load shows its chapter');
    assert.ok(page.folds(6)[0].open, 'A subsection link at load opens the fold around it');
  }
  const still = bootReader('#notation', {reducedMotion: true});
  still.chapterKey('ArrowRight');
  assert.ok(!still.strip.classes.has('topic-animate'), 'Reduced motion turns off the strip animation');
  const end = bootReader('#' + CHAPTERS[N - 1].id);
  end.click(end.control('pair'));
  end.assertPair(N - 2, N - 1, 'Pair view at the last chapter pairs it with the one before');
  assert.ok(end.control('next').disabled, 'Next is disabled at the last pair');
  return 'full-page mode and return, print open and restore, bad hashes, deep links at load, reduced motion, last pair';
}

function checkDockedNavigation() {
  const sidebarKey = 'reader-nav-pin:' + FIXTURE.siteHomeLabel;
  const docked = page => page.document.body.classes.has('reader-nav-docked');
  const page = bootReader('#notation', {width: 1200});
  page.bodies[1].scrollTop = 610;
  assert.ok(docked(page), 'Wide screens start with docked navigation');
  page.click(page.control('drawer'));
  assert.equal(page.storage.get(sidebarKey), 'false', 'Hiding docked navigation is remembered site-wide');
  page.click(page.control('drawer'));
  assert.equal(page.content.inert, false, 'Docked navigation leaves the page interactive');
  assert.ok(docked(page), 'The menu button docks navigation again on wide screens');
  assert.equal(page.storage.get(sidebarKey), 'true', 'Docking again is remembered');
  page.assertCentred(1, 'After docking');
  assert.equal(page.bodies[1].scrollTop, 610, 'Docking does not reset the chapter');
  assert.ok(page.chapterKey('ArrowRight').defaultPrevented, 'Docked navigation leaves chapter keys available');
  page.click(page.links[1]);
  assert.ok(page.document.body.classes.has('reader-nav-open'), 'Chapter links keep docked navigation open');
  assert.equal(page.bodies[1].scrollTop, 610, 'Chapter links keep the reading position');
  page.window.innerWidth = 768;
  page.window.emit('resize');
  assert.ok(!docked(page), 'Narrow windows undock navigation');
  assert.equal(page.content.inert, true, 'Undocked open navigation covers the page');
  page.click(page.links[2]);
  assert.equal(page.content.inert, false, 'A chapter link closes overlay navigation');
  assert.equal(page.storage.get(sidebarKey), 'true', 'Closing overlay navigation by a link keeps the dock choice');
  page.window.innerWidth = 1224;
  page.click(page.control('drawer'));
  page.assertCentred(2, 'Re-docked');
  page.click(page.sidebar.querySelector('.reader-drawer-close'));
  assert.equal(page.storage.get(sidebarKey), 'false', 'The close button records the hidden choice');
  assert.equal(page.sidebar.inert, true, 'The close button closes navigation');
  page.assertCentred(2, 'After closing navigation');

  const savedDock = bootReader('', {width: 1200, stored: {[sidebarKey]: 'true'}});
  assert.ok(docked(savedDock), 'A saved dock choice docks on wide screens');
  assert.equal(savedDock.content.inert, false, 'Saved docking leaves the page interactive');
  savedDock.assertCentred(0, 'Saved docking');
  const savedHidden = bootReader('', {width: 1200, stored: {[sidebarKey]: 'false'}});
  assert.ok(!docked(savedHidden) && savedHidden.sidebar.inert, 'A saved hidden choice keeps wide navigation closed');
  const savedNarrow = bootReader('', {width: 296, stored: {[sidebarKey]: 'true'}});
  assert.equal(savedNarrow.sidebar.inert, true, 'Phones start with navigation closed even when docking is saved');

  const previews = bootReader('#notation');
  previews.bodies[1].scrollTop = 360;
  const neighbour = previews.stage.querySelector('.topic-peek-next');
  assert.equal(neighbour.textContent, '', 'The neighbour peek has no edge arrow');
  neighbour.emit('pointerenter');
  assert.ok(previews.sections[2].classes.has('topic-preview-hover'), 'Hovering the peek highlights the next chapter');
  neighbour.emit('pointerleave');
  assert.ok(!previews.sections[2].classes.has('topic-preview-hover'), 'Leaving the peek removes the highlight');
  previews.click(neighbour);
  previews.assertCentred(2, 'Clicking the next peek');
  previews.click(previews.stage.querySelector('.topic-peek-prev'));
  assert.equal(previews.bodies[1].scrollTop, 360, 'The previous peek returns to the saved position');
  return 'docked navigation threshold and reader-nav-pin persistence, neighbour peek hover and click';
}

// Pages with different titles, units, chapter counts and groups each get their
// own identity and page-scoped storage.
function checkPageIdentities() {
  const pages = [
    {pageName: 'reader-check', title: 'Reader check', unit: 'chapter', chapters: CHAPTERS.slice(0, 5),
      groups: {overview: 'Basics', model: 'Method'}},
    {pageName: 'second-guide', title: 'Second guide — a longer title', unit: 'section', chapters: CHAPTERS.slice(2, 5),
      groups: {model: 'Only group'}},
    {pageName: 'appendix', title: 'Appendix', unit: 'chapter', chapters: CHAPTERS, groups: {}},
  ];
  const storageKeys = new Set();
  for (const {pageName, title, unit, chapters, groups} of pages) {
    for (const {width} of WIDTHS) {
      const page = bootReader('', {width, pageName, title, unit, chapters, groups});
      page.assertCentred(0, `${pageName} at width ${width}`);
      assert.equal(page.nav.querySelector('.reader-title strong').textContent, title, 'The toolbar shows the page title');
      assert.equal(page.nav.getAttribute('aria-label'), `${title} ${unit} reader`, 'The toolbar names the page and unit');
      assert.equal(page.stage.getAttribute('aria-label'), `${title} ${unit}s`, 'The stage names the page and unit');
      assert.deepEqual(page.document.querySelectorAll('.reader-nav-group').map(node => node.textContent), Object.values(groups),
        'The drawer shows the page\'s chapter groups in order');
      const tree = page.sidebar.querySelector('.toc');
      for (const {href} of SITE_PAGES) {
        assert.ok(tree.querySelectorAll('a.xpage').some(link => link.getAttribute('href') === href),
          `The site page ${href} stays in the tree`);
      }
      const current = tree.querySelector('a.xpage.current');
      assert.equal(current.getAttribute('href'), pageName + '.html', 'The current page is marked in the tree');
      assert.equal(tree.children[tree.children.indexOf(current) + 1].id, 'reader-chapter-list',
        'Chapters follow their own page entry');
      const plural = unit[0].toUpperCase() + unit.slice(1) + 's';
      assert.equal(page.sidebar.querySelector('#reader-chapter-list').getAttribute('aria-label'), `${plural} of this page`,
        'The chapter list is named by unit');
      page.bodies[0].scrollTop = 375;
      page.click(page.control('pair'));
      page.assertPair(0, 1);
      page.read(1); page.layers(['math', 'experiment']);
      assert.deepEqual(page.states(0), [false, false, false, false], 'Right-column layers leave the left closed');
      assert.deepEqual(page.states(1), [true, true, false, false], 'Right-column layers open the right chapter');
      page.pin(0);
      page.chapterKey('ArrowRight');
      page.assertPair(0, 2);
      assert.equal(page.bodies[0].scrollTop, 375, 'The pinned chapter keeps its position');
      page.click(page.control('full'));
      assert.equal(page.visible().length, chapters.length, 'Full page shows every chapter of this page');
      page.click(page.control('single'));
      page.assertCentred(2);
      const key = 'foldcolumns:/fixture-site/' + pageName + '.html';
      assert.ok(page.storage.has(key), `Layer choices are stored under ${key}`);
      storageKeys.add([...page.storage.keys()].find(name => name.startsWith('foldcolumns:')));
    }
  }
  assert.equal(storageKeys.size, pages.length, 'Each page stores layer choices under its own key');

  const sections = bootReader('', {unit: 'section', title: 'Sectioned page',
    groups: {overview: 'Construct', solver: 'Control', results: 'Compare', limits: 'Check'},
    foldKinds: [['math'], ['math', 'experiment'], ['experiment', 'code'], ['experiment'], ['math', 'dead-end'],
      ['code'], ['math', 'experiment'], ['dead-end']],
    subsections: [{id: 'legacy-formula', label: 'Legacy formula', chapter: 6, fold: 0}]});
  assert.equal(sections.sidebar.querySelector('#reader-chapter-list').getAttribute('aria-label'), 'Sections of this page',
    'A section page names its list by sections');
  assert.equal(sections.control('drawer').getAttribute('aria-label'), 'Open sections', 'The menu button names sections');
  assert.equal(sections.control('count').textContent, `Section 1 of ${N}`, 'The status names sections');
  assert.ok(!sections.document.querySelector('.reader-help').textContent.includes('chapter'), 'Help text speaks of sections');
  assert.deepEqual(sections.document.querySelectorAll('.reader-nav-group').map(node => node.textContent),
    ['Construct', 'Control', 'Compare', 'Check'], 'Section groups appear in order');
  const [left, right] = [3, 4];
  for (const index of [left, right]) {
    sections.click(sections.links[index]);
    assert.deepEqual(sections.visible(), ids([index]), 'A section link shows that section');
    assert.ok(sections.states(index).every(open => !open), 'A visited section opens no fold by default');
  }
  sections.click(sections.links[left]);
  sections.bodies[left].scrollTop = 325;
  sections.click(sections.control('pair'));
  sections.assertPair(left, right);
  sections.pin(left);
  sections.chapterKey('ArrowRight');
  sections.assertPair(left, right + 1);
  assert.equal(sections.bodies[left].scrollTop, 325, 'The pinned section keeps its position');
  sections.chapterKey('ArrowLeft');
  sections.assertPair(left, right);
  sections.pin(right);
  sections.chapterKey('ArrowLeft');
  sections.assertPair(left - 1, right, 'Pinning the right section moves the left one');
  const legacy = sections.document.querySelectorAll('.reader-chapter-list a')
    .find(link => link.getAttribute('href') === '#legacy-formula');
  assert.ok(legacy, 'A subsection link stays under its section in the drawer');
  sections.click(legacy);
  sections.assertPair(6, right, 'A subsection link moves the unpinned column to its section');
  assert.ok(sections.folds(6)[0].open, 'A subsection link opens the fold around it');
  assert.ok(sections.states(right).every(open => !open), 'The pinned section keeps its layer state');
  return 'page titles, units, groups, site tree, page-scoped foldcolumns keys; section wording, pins and subsection links';
}

function checkSmallPagesAndRedirects() {
  const two = bootReader('', {chapters: CHAPTERS.slice(0, 2), title: 'Two chapters'});
  two.click(two.control('pair'));
  two.assertPair(0, 1, 'A two-chapter page pairs both');
  assert.ok(two.control('next').disabled && two.control('prev').disabled, 'A two-chapter pair cannot move');
  const one = bootReader('', {chapters: CHAPTERS.slice(0, 1), title: 'One chapter'});
  assert.equal(one.control('pair').disabled, true, 'Pair view is disabled with one chapter');
  one.click(one.control('pair'));
  one.assertCentred(0, 'One-chapter page after choosing pair');

  const redirects = {'moved-away': 'second-guide.html#moved-away'};
  const moved = bootReader('#moved-away', {redirects});
  assert.equal(moved.redirected.length, 1, 'A hash naming a moved chapter redirects once');
  assert.ok(moved.redirected[0].endsWith('second-guide.html#moved-away'), 'The redirect goes to the moved chapter');
  assert.equal(moved.content.querySelector('.topic-stage'), null, 'A redirecting page does not build the reader');
  const later = bootReader('', {redirects});
  later.location.hash = '#moved-away';
  later.window.emit('hashchange');
  assert.deepEqual(later.redirected.map(href => href.replace(/^.*\//, '')), ['second-guide.html#moved-away'],
    'A later hash change to a moved chapter redirects');
  return 'two-chapter and one-chapter pages, data-reader-redirect at load and on hash change';
}

// Pages adapted by the build: chapters are marked sections with h2 headers,
// nested cards stay subsections, chapters without folds hide their layer row.
function checkAdaptedPages() {
  const chapters = CHAPTERS.slice(0, 4);
  const foldKinds = [[], ['math'], [], ['code', 'math']];
  const subsections = [
    {id: 'nested-card', label: 'Nested card', chapter: 1, card: true},
    {id: 'late-heading', label: 'Late heading', chapter: 3},
  ];
  for (const {width} of WIDTHS) {
    const page = bootReader('#top', {width, chapters, adapted: true, headingTag: 'h2', foldKinds, subsections});
    page.assertCentred(0, `Adapted page at width ${width}`);
    assert.equal(page.strip.children.length, chapters.length, 'Nested cards are not extra chapters');
    page.sections.forEach((section, index) => {
      assert.equal(section.getAttribute('aria-labelledby'), 'heading-' + index, 'An h2 header labels its chapter');
      assert.equal(section.querySelector('.chapter-layers').hidden, !foldKinds[index].length,
        'Only chapters with folds show layer buttons');
    });
    page.bodies[0].scrollTop = 315;
    page.click(page.control('pair'));
    page.assertPair(0, 1);
    page.pin(0);
    page.chapterKey('ArrowRight');
    page.assertPair(0, 2);
    assert.equal(page.bodies[0].scrollTop, 315, 'The pinned chapter keeps its position');
    for (const {id} of subsections) {
      const link = page.document.querySelectorAll('.reader-chapter-list a').find(node => node.getAttribute('href') === '#' + id);
      assert.ok(link, `The subsection ${id} stays in the chapter list`);
    }
    const lastLink = page.document.querySelectorAll('a').find(node => node.getAttribute('href') === '#late-heading');
    page.click(lastLink);
    assert.ok(page.visible().includes(chapters[3].id), 'A subsection link shows its chapter');
    page.click(page.control('full'));
    assert.equal(page.visible().length, chapters.length, 'Full page shows every adapted chapter');
    page.window.emit('beforeprint');
    page.window.emit('afterprint');
    page.flush();
  }
  return 'h2 headers, nested cards, empty layer rows, pins, subsection links, full page and print';
}

// Subsection links are labelled jumps within a parent, not extra chapters.
function checkJumpGroups() {
  const chapters = [{id: 'intro', label: 'Introduction'}, {id: 'queries', label: 'Projection and containment'}];
  const subsections = [
    {id: 'intro-assumptions', label: 'Example assumptions', chapter: 0},
    {id: 'query-formulas', label: 'Constant-width query formulas', chapter: 1, fold: 0},
  ];
  for (const {width} of WIDTHS) {
    for (const unit of ['section', 'chapter']) {
      const page = bootReader('#query-formulas', {width, unit, chapters, subsections, pageName: 'navigation-check'});
      const groups = page.document.querySelectorAll('.reader-chapter-jumps');
      assert.equal(groups.length, 2, 'Only parents with destinations get a jump group');
      const group = groups.find(node => node.dataset.readerShortcutsFor === 'queries');
      const link = group.querySelector('a');
      assert.equal(group.querySelector('summary').textContent, 'Jump within this ' + unit, 'The jump group names the unit');
      assert.ok(group.open, 'A deep-linked parent shows its jump destinations');
      assert.equal(link.querySelector('.reader-jump-kind').textContent, 'Math', 'A jump into a fold carries its layer badge');
      assert.equal(link.dataset.readerJumpKind, 'math', 'A jump into a fold records its layer');
      const intro = groups.find(node => node.dataset.readerShortcutsFor === 'intro');
      assert.equal(intro.querySelector('.reader-jump-kind'), null, 'A jump to visible story has no layer badge');
      assert.match(link.getAttribute('aria-label'),
        /Jump to Constant-width query formulas in Projection and containment; opens Math details/, 'The jump says where it goes');
      assert.equal(link.getAttribute('aria-current'), 'location', 'The deep-linked jump is marked current');
      assert.ok(page.folds(1)[0].open, 'The jump destination reveals its fold');
      page.click(page.links[0]);
      assert.ok(!group.open, 'Inactive parents close their jump group');
      assert.equal(link.getAttribute('aria-current'), null, 'Visiting another parent clears the jump highlight');
      page.click(page.links[1]);
      assert.ok(group.open, 'Visiting the parent shows its jumps');
      page.click(link);
      assert.equal(link.getAttribute('aria-current'), 'location', 'Following a jump marks it current');
      page.click(page.control('full'));
      assert.ok(groups.every(node => node.open), 'Full page shows every jump group');
    }
  }
  const single = bootReader('', {chapters: [{id: 'only', label: 'Only section'}], pageName: 'navigation-empty'});
  assert.equal(single.document.querySelectorAll('.reader-chapter-jumps').length, 0, 'No empty jump groups');

  // The page is the last site page, so its jump disclosure ends the drawer.
  const keyboard = bootReader('', {chapters: [{id: 'first', label: 'First section'}, {id: 'last', label: 'Last section'}],
    subsections: [{id: 'last-detail', label: 'Last detail', chapter: 1}],
    pageName: SITE_PAGES.at(-1).href.slice(0, -'.html'.length)});
  keyboard.click(keyboard.control('drawer'));
  const disclosure = keyboard.document.querySelector('.reader-chapter-jumps summary');
  disclosure.focus({preventScroll: true});
  assert.ok(keyboard.key('Tab').defaultPrevented, 'Tab from the last disclosure wraps within the drawer');
  assert.notEqual(keyboard.document.activeElement, disclosure, 'Tab leaves the last disclosure');
  assert.ok(keyboard.key('Tab', {shiftKey: true}).defaultPrevented, 'Shift-Tab from the first control wraps');
  assert.equal(keyboard.document.activeElement, disclosure, 'Shift-Tab reaches the last disclosure');
  return 'jump groups, Math badges, aria-current, deep-link folds, full page, no empty groups, '
    + 'Tab loop through the last disclosure';
}

function checkFoldControls() {
  // Reader pages opt in with data-fold-controls="columns": styling only.
  const reader = bootReader('#notation');
  const before = reader.states(1);
  const hashHandlers = reader.window.listenerCount('hashchange');
  runFoldControls(reader, {getItem: () => 'all', setItem() {}});
  assert.deepEqual(reader.states(1), before, 'The reader opt-in leaves fold states to the reader');
  assert.equal(reader.document.querySelector('.fold-bar'), null, 'The reader opt-in installs no global fold bar');
  assert.equal(reader.window.listenerCount('hashchange'), hashHandlers, 'The reader opt-in adds no hashchange handler');
  assert.equal(reader.document.head.querySelectorAll('style').length, 1, 'The reader opt-in keeps the fold styling');

  // Other pages get the global bar with six presets.
  const page = bootReader('', {runReader: false});
  page.nav.dataset.foldControls = 'default';
  const legacyKey = 'foldmode:' + page.location.pathname;
  const storage = new Map([[legacyKey, 'math']]);
  runFoldControls(page, {getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value)});
  const states = index => page.sections[index].querySelectorAll('details.fold').map(fold => fold.open);
  const bar = page.document.querySelector('.fold-bar');
  assert.ok(bar, 'Pages without the reader get the global fold bar');
  const buttons = bar.querySelectorAll('button');
  assert.equal(buttons.length, 6, 'The fold bar offers six presets');
  assert.deepEqual(states(0), [true, false, false, false], 'The saved foldmode opens its kind at load');
  buttons[5].emit('click');
  assert.deepEqual(states(0), [true, true, true, true], 'The last preset opens every fold');
  assert.equal(storage.get(legacyKey), 'all', 'A preset choice is saved under the foldmode key');
  buttons[0].emit('click');
  assert.deepEqual(states(0), [false, false, false, false], 'The story preset closes every fold');
  assert.equal(storage.get(legacyKey), 'none', 'The story preset is saved');
  page.location.hash = '#' + FIXTURE.deepTarget;
  page.window.emit('hashchange');
  assert.equal(page.sections[FIXTURE.deepChapter].querySelectorAll('details.fold')[0].open, true,
    'A hash change opens the fold around its target');
  return 'reader opt-in installs no bar or hash handler; default bar has six presets, foldmode persistence and hash deep links';
}

function checkSourceRules() {
  const source = readComponent('chapter-reader.js');
  assert.ok(!/\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(/.test(source), 'chapter-reader.js makes no network request');
  assert.ok(!source.includes('section.hidden'), 'chapter-reader.js never hides a source section');
  return 'chapter-reader.js makes no network request and never hides a source section';
}

const checks = [
  ['Reader navigation', checkNavigationAndPins],
  ['Reader folds, keys and dialogs', checkFoldsKeysAndDrawer],
  ['Reader column layers', checkColumnLayers],
  ['Reader stored profiles', checkStoredProfiles],
  ['Reader drawer focus', checkDrawerFocusAndSelection],
  ['Reader viewport anchor', checkViewportAnchor],
  ['Reader full page and print', checkFullPagePrintAndBoot],
  ['Reader docked navigation', checkDockedNavigation],
  ['Reader page identities', checkPageIdentities],
  ['Reader small pages', checkSmallPagesAndRedirects],
  ['Reader adapted pages', checkAdaptedPages],
  ['Reader jump groups', checkJumpGroups],
  ['Fold controls', checkFoldControls],
  ['Reader source rules', checkSourceRules],
];
for (const [name, check] of checks) console.log(`${name} checks pass: ${check()}.`);
