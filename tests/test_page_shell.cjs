// Real-browser check of the shared shell on pages without the reader, opened
// from disk (file://), and of printing with motion left on:
// - below 900 px the closed drawer takes no keyboard focus; the menu button
//   states aria-expanded, opening moves focus into the drawer, Escape closes it
//   and returns focus to the button;
// - the source links and code chips of a Reference page are at least 24 px tall;
// - a long address in Reference prose, and a formula far right in a scrolling
//   table, do not widen the page;
// - printing shows no fold mid-fade.
// The other browser suites run with reduced motion, which hides a running fade.
// PAGE_SHELL_CAPTURES=<folder> also saves screenshots.
const {chromium} = require('../node_modules/playwright');
const {execFileSync} = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const assert = require('node:assert/strict');
const {assertHorizontalContainment} = require('../tooling/browser_checks.cjs');

const kit = path.resolve(__dirname, '..');
const python = process.env.DOCS_PYTHON || 'python3';
const captures = process.env.PAGE_SHELL_CAPTURES || '';
const ADDRESS = 'https://example.org/' + 'a-long-address-without-a-break/'.repeat(6) + '0123456789abcdef'.repeat(4);

function run(command, args, cwd) {
  const env = {...process.env};
  delete env.DOCSITE_PROJECT_ROOT;
  delete env.GITHUB_SHA;
  return execFileSync(command, args, {cwd, env, stdio: ['ignore', 'pipe', 'pipe']}).toString();
}

function buildFixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-kit-page-shell-'));
  run('git', ['init', '-q'], root);
  run(python, [path.join(kit, 'docsite.py'), 'init', root], kit);
  fs.mkdirSync(path.join(root, 'notes'));
  fs.writeFileSync(path.join(root, 'notes/long.md'), [
    '# Long note', '', `Prose with a bare address ${ADDRESS} in a sentence.`, '',
    `A linked address: [${ADDRESS}](${ADDRESS}).`, '', '```python', 'print("a code block")', '```', '',
  ].join('\n'));
  fs.writeFileSync(path.join(root, 'notes/math.md'), [
    '# Math note', '',
    '| Quantity | Meaning | Where the method uses it | Unit | Symbol |', '|---|---|---|---|---|',
    '| Lateral acceleration of the body | measured at the centre of gravity | steady-state comparison | m/s² | $a_y$ |',
    '| Yaw rate of the body | measured by the inertial unit | transient response comparison | rad/s | $\\dot\\psi$ |', '',
  ].join('\n'));
  const config = path.join(root, 'docs/site/site.toml');
  fs.writeFileSync(config, fs.readFileSync(config, 'utf8').replace(
    '# reference_roots = ["docs"]', 'reference_roots = ["docs", "notes"]')
    + '\n[[source_pages]]\nsource = "notes/math.md"\nslug = "math-note"\ntitle = "Math note"\nmath = true\n');
  run('git', ['add', '-A'], root);
  run(python, [path.join(kit, 'docsite.py'), 'build', '--project', root], kit);
  return root;
}

const drawer = page => page.evaluate(() => {
  const bar = document.getElementById('sidebar'), menu = document.getElementById('menu'), active = document.activeElement;
  return {open: document.body.classList.contains('nav-open'), expanded: menu.getAttribute('aria-expanded'),
    controls: menu.getAttribute('aria-controls'), inert: bar.inert, contentInert: document.querySelector('main.content').inert,
    focusInDrawer: !!active.closest('#sidebar'), focusOnMenu: active === menu};
});

(async () => {
  const root = buildFixture();
  const html = path.join(root, '.build/docs/html');
  const url = name => pathToFileURL(path.join(html, name)).href;
  if (captures) fs.mkdirSync(captures, {recursive: true});
  const browser = await chromium.launch({headless: true});
  const checked = [];
  try {
    // Motion stays on in every context of this suite.
    const context = await browser.newContext({viewport: {width: 390, height: 844}});
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });

    for (const name of ['index.html', 'notes.long.md.html']) {
      await page.goto(url(name));
      assert.equal(await page.evaluate(() => document.body.classList.contains('reader-enabled')), false, name + ' has no reader');
      let state = await drawer(page);
      assert.deepEqual({open: state.open, expanded: state.expanded, controls: state.controls, inert: state.inert, contentInert: state.contentInert},
        {open: false, expanded: 'false', controls: 'sidebar', inert: true, contentInert: false}, name + ': closed drawer');
      // The closed drawer is off screen; no Tab stop may land in it.
      const links = await page.locator('#sidebar a[href], #sidebar summary').count();
      assert.ok(links > 3, name + ': the drawer holds links');
      for (let stop = 0; stop < 12; stop++) {
        await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(() => !!document.activeElement.closest('#sidebar')), false,
          `${name}: Tab stop ${stop + 1} lands in the closed drawer`);
      }
      await page.focus('#menu');
      await page.keyboard.press('Enter');
      state = await drawer(page);
      assert.deepEqual({open: state.open, expanded: state.expanded, inert: state.inert, contentInert: state.contentInert, focusInDrawer: state.focusInDrawer},
        {open: true, expanded: 'true', inert: false, contentInert: true, focusInDrawer: true}, name + ': open drawer');
      if (captures) { await page.waitForTimeout(250); await page.screenshot({path: path.join(captures, `390-drawer-${name}.png`)}); }
      await page.keyboard.press('Escape');
      state = await drawer(page);
      assert.deepEqual({open: state.open, expanded: state.expanded, inert: state.inert, contentInert: state.contentInert, focusOnMenu: state.focusOnMenu},
        {open: false, expanded: 'false', inert: true, contentInert: false, focusOnMenu: true}, name + ': Escape closes the drawer');
      // The backdrop closes it too, and a class another script sets is followed.
      await page.click('#menu');
      await page.mouse.click(370, 600);
      assert.equal((await drawer(page)).open, false, name + ': the backdrop closes the drawer');
      await page.evaluate(() => document.body.classList.add('nav-open'));
      await page.waitForFunction(() => !document.getElementById('sidebar').inert);
      await page.evaluate(() => document.body.classList.remove('nav-open'));
      await page.waitForFunction(() => document.getElementById('sidebar').inert && !document.querySelector('main.content').inert);
    }
    checked.push('drawer: no focus while closed, aria-expanded, focus moves in, Escape and backdrop close');

    // A wide window shows the sidebar beside the page: never inert, whatever the class says.
    await page.setViewportSize({width: 1600, height: 1000});
    await page.goto(url('notes.long.md.html'));
    assert.equal((await drawer(page)).inert, false, 'wide: the sidebar takes focus');
    await page.evaluate(() => document.body.classList.add('nav-open'));
    await page.waitForTimeout(100);
    assert.deepEqual(await page.evaluate(() => [document.getElementById('sidebar').inert, document.querySelector('main.content').inert]),
      [false, false], 'wide: nothing is inert with the class set');
    if (captures) await page.screenshot({path: path.join(captures, '1600-reference.png')});
    await page.setViewportSize({width: 390, height: 844});
    checked.push('wide window: sidebar and page stay reachable');

    // Reference page: target sizes and no sideways scroll.
    await page.goto(url('notes.long.md.html'));
    await page.hover('.codeblock');
    const sizes = await page.evaluate(() => Object.fromEntries(['.source-origin a', '.cb-chips .cb-copy'].map(selector =>
      [selector, Math.min(...[...document.querySelectorAll(selector)].map(node => node.getBoundingClientRect().height))])));
    for (const [selector, height] of Object.entries(sizes)) assert.ok(height >= 24, `${selector} is ${height} px tall, below 24 px`);
    await assertHorizontalContainment(page);
    if (captures) await page.screenshot({path: path.join(captures, '390-reference.png'), fullPage: true});
    checked.push('Reference page: 24 px targets, long address wraps');

    await page.goto(url('math-note.html'));
    await page.waitForSelector('td .katex');
    const table = await page.evaluate(() => {
      const box = document.querySelector('td .katex').closest('.scroll');
      return {scrolls: box.scrollWidth > box.clientWidth, formulaLeft: document.querySelector('td .katex').getBoundingClientRect().left, width: innerWidth};
    });
    assert.ok(table.scrolls && table.formulaLeft > table.width, 'the fixture formula lies right of the window: ' + JSON.stringify(table));
    await assertHorizontalContainment(page);
    checked.push('formula in a scrolling table does not widen the page');

    // Print with motion on: the reader opens every fold; none may still fade.
    await page.setViewportSize({width: 1280, height: 900});
    await page.goto(url('guide.html'));
    await page.waitForSelector('body.reader-enabled');
    await page.emulateMedia({media: 'print'});
    const print = await page.evaluate(() => {
      window.dispatchEvent(new Event('beforeprint'));
      const folds = [...document.querySelectorAll('details.fold[open] > .fold-content')];
      return {folds: folds.length, fading: folds.filter(node => node.getAnimations().some(a => a.playState === 'running')).length,
        pale: folds.filter(node => Number(getComputedStyle(node).opacity) < 1).length};
    });
    assert.ok(print.folds > 0, 'printing opens the folds');
    assert.deepEqual({fading: print.fading, pale: print.pale}, {fading: 0, pale: 0}, 'print shows no fold mid-fade: ' + JSON.stringify(print));
    await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
    await page.emulateMedia({media: 'screen'});
    checked.push(`print: ${print.folds} folds open, none fading`);

    assert.deepEqual(errors, []);
    await context.close();
    console.log(JSON.stringify({checked, result: 'pass'}));
  } finally {
    await browser.close();
    fs.rmSync(root, {recursive: true, force: true});
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
