// Real-browser check of a Reference tree above the inline limit, opened from
// disk (file://): nav.js loads reference.tree.js when "Browse by folder" opens,
// or at load on a listed page, and marks the current file as the inline tree
// does. Without JavaScript the disclosure links the Reference index page.
// REFERENCE_TREE_CAPTURES=<folder> also saves screenshots of a listed page.
const {chromium} = require('../node_modules/playwright');
const {execFileSync} = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const assert = require('node:assert/strict');

const kit = path.resolve(__dirname, '..');
const python = process.env.DOCS_PYTHON || 'python3';
const captures = process.env.REFERENCE_TREE_CAPTURES || '';
const FILES = 70;  // above source_tree.INLINE_TREE_LIMIT (60)

function run(command, args, cwd) {
  const env = {...process.env};
  delete env.DOCSITE_PROJECT_ROOT;
  delete env.GITHUB_SHA;
  return execFileSync(command, args, {cwd, env, stdio: ['ignore', 'pipe', 'pipe']}).toString();
}

function buildFixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'docs-kit-reference-tree-'));
  run('git', ['init', '-q'], root);
  run(python, [path.join(kit, 'docsite.py'), 'init', root], kit);
  for (let index = 0; index < FILES; index++) {
    const file = path.join(root, 'many', `group${index % 5}`, `file${String(index).padStart(3, '0')}.md`);
    fs.mkdirSync(path.dirname(file), {recursive: true});
    fs.writeFileSync(file, `# File ${index}\n\nSome text.\n`);
  }
  run('git', ['add', '-A'], root);
  run(python, [path.join(kit, 'docsite.py'), 'build', '--project', root], kit);
  return root;
}

// The folder counts and the marking the inline tree would carry for `current`.
async function treeFacts(page, current) {
  return page.evaluate(route => {
    const all = document.querySelector('.toc .repo-tree details.repo-tree-all');
    const files = [...all.querySelectorAll('a.repo-tree-file')];
    const folders = [...all.querySelectorAll('li.repo-tree-folder')];
    const counts = folders.every(folder => {
      const shown = Number(folder.querySelector(':scope > details > summary .repo-tree-count').textContent);
      return shown === folder.querySelectorAll('a.repo-tree-file').length;
    });
    const here = files.filter(a => a.classList.contains('current'));
    const holding = folders.filter(folder => route && folder.querySelector(`a.repo-tree-file[href="${route}"]`));
    return {
      files: files.length,
      counts,
      current: here.map(a => a.getAttribute('href')),
      ariaCurrent: here.map(a => a.getAttribute('aria-current')),
      foldersMarked: folders.filter(f => f.classList.contains('has-current')).length,
      foldersOpen: folders.filter(f => f.querySelector(':scope > details').open).length,
      holding: holding.length,
      holdingMarkedOpen: holding.every(f => f.classList.contains('has-current') && f.querySelector(':scope > details').open),
      disclosureOpen: all.open,
      ready: document.querySelector('.toc .repo-tree').hasAttribute('data-repo-tree-ready'),
    };
  }, current);
}

(async () => {
  const root = buildFixture();
  const html = path.join(root, '.build/docs/html');
  const listed = Object.keys(JSON.parse(fs.readFileSync(path.join(root, '.build/docs/site-build.json'), 'utf8')).source_pages);
  assert.ok(listed.length > 60, 'the fixture is above the inline limit');
  const url = name => pathToFileURL(path.join(html, name)).href;
  const browser = await chromium.launch({headless: true});
  const results = [];
  try {
    for (const viewport of [{width: 1600, height: 1000}, {width: 390, height: 844}]) {
      const context = await browser.newContext({viewport, reducedMotion: 'reduce'});
      const page = await context.newPage();
      page.setDefaultTimeout(10000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
      const narrow = viewport.width < 768;
      // Reader pages open navigation from the reader bar; reference pages from the shell menu.
      const openMenu = async () => {
        if (!narrow) return;
        await page.click(await page.locator('#menu').isVisible() ? '#menu' : '.reader-mobile-menu');
        await page.waitForFunction(() => {
          const r = document.getElementById('sidebar').getBoundingClientRect();
          return r.right > 100 && r.left >= -1;
        });
      };

      // A page for people: nothing loads until the disclosure opens, by keyboard.
      await page.goto(url('guide.html'));
      assert.equal(await page.evaluate(() => typeof window.docsReferenceTree), 'undefined');
      let facts = await treeFacts(page, '');
      assert.equal(facts.files, 0);
      assert.equal(facts.disclosureOpen, false);
      await openMenu();
      await page.focus('.toc .repo-tree details.repo-tree-all > summary');
      await page.keyboard.press('Enter');
      await page.waitForSelector('.toc .repo-tree[data-repo-tree-ready]');
      facts = await treeFacts(page, '');
      assert.equal(facts.files, listed.length, 'every listed file appears');
      assert.ok(facts.counts, 'folder counts match their files');
      assert.deepEqual(facts.current, []);
      assert.equal(facts.foldersOpen, 0);
      // Folders open and close by keyboard as in the inline tree.
      await page.focus('.toc .repo-tree-all li.repo-tree-folder > details > summary');
      await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(() => document.querySelector('.toc .repo-tree-all li.repo-tree-folder > details').open), true);

      // A listed page: the tree loads at once and unfolds to the current file.
      const target = 'many.group3.file013.md.html';
      await page.goto(url(target));
      await page.waitForSelector('.toc .repo-tree[data-repo-tree-ready]');
      facts = await treeFacts(page, target);
      assert.equal(facts.files, listed.length);
      assert.ok(facts.counts);
      assert.deepEqual(facts.current, [target]);
      assert.deepEqual(facts.ariaCurrent, ['page']);
      assert.equal(facts.holding, 2, 'many/ and group3/ hold the file');
      assert.ok(facts.holdingMarkedOpen);
      assert.equal(facts.foldersMarked, 2);
      assert.equal(facts.foldersOpen, 2);
      assert.ok(facts.disclosureOpen);
      await openMenu();
      const inView = await page.evaluate(route => {
        const link = document.querySelector(`.toc a.repo-tree-file[href="${route}"]`);
        const bar = link.closest('.sidebar').getBoundingClientRect(), box = link.getBoundingClientRect();
        return box.height > 0 && box.top >= bar.top && box.bottom <= bar.bottom;
      }, target);
      assert.ok(inView, 'the current file is scrolled into view');
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
      assert.equal(overflow, false, 'no horizontal overflow');
      if (captures) {
        fs.mkdirSync(captures, {recursive: true});
        await page.screenshot({path: path.join(captures, `fixture-listed-${viewport.width}.png`)});
      }
      assert.deepEqual(errors, []);
      await context.close();

      results.push({viewport, files: listed.length, result: 'pass'});
      // Without JavaScript the disclosure links the index page, which holds the whole tree.
      // The narrow menu itself needs JavaScript, so this runs at the wide width.
      if (narrow) continue;
      const plain = await browser.newContext({viewport, javaScriptEnabled: false});
      const still = await plain.newPage();
      still.setDefaultTimeout(10000);
      await still.goto(url('guide.html'));
      await still.click('.toc .repo-tree details.repo-tree-all > summary');
      const link = still.locator('.toc .repo-tree-index a');
      assert.equal(await link.getAttribute('href'), 'reference.index.html');
      await link.click();
      await still.waitForURL(/reference\.index\.html$/);
      assert.equal(await still.locator('.reference-index a.repo-tree-file').count(), listed.length);
      await still.goto(url(target));
      assert.equal(await still.locator('.toc .repo-tree-all a.repo-tree-file').count(), 1, 'only the current file, in its folders');
      assert.equal(await still.locator('.toc .repo-tree-all a.repo-tree-file.current[aria-current="page"]').count(), 1);
      await plain.close();
      results.push({viewport, javaScript: false, result: 'pass'});
    }
  } finally {
    await browser.close();
    fs.rmSync(root, {recursive: true, force: true});
  }
  console.log(JSON.stringify(results));
  console.log(`Reference tree: ${FILES}+ files load from file:// on opening and on a listed page, keep counts, marking and keyboard folders, and link the index without JavaScript.`);
})().catch(error => { console.error(error); process.exit(1); });
