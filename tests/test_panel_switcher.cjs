// Optional real-browser contract check; the legacy mode proves extraction parity.
const {chromium} = require(process.env.DOCS_PLAYWRIGHT || 'playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const kit = path.resolve(__dirname, '..');
const legacy = process.env.PANEL_SWITCHER_LEGACY === '1';
const source = process.env.PANEL_SWITCHER_SOURCE || path.join(kit, 'theme/components/panel-switcher.js');
const stylesheet = process.env.PANEL_SWITCHER_CSS || path.join(kit, 'theme/components/panel-switcher.css');
const output = process.env.PANEL_SWITCHER_RESULTS || path.join(kit, '.build/panel-switcher');
const rootAttribute = legacy ? 'data-width-lesson' : 'data-panel-switcher';
const choiceAttribute = legacy ? 'data-width-choice' : 'data-panel-choice';
const panelAttribute = legacy ? 'data-width-panel' : 'data-panel';
const defaultAttribute = legacy ? 'data-width-default' : 'data-panel-default';
const readyAttribute = legacy ? 'data-width-ready' : 'data-panel-ready';
const rootClass = legacy ? 'width-lesson' : 'panel-switcher';
const controlClass = legacy ? 'width-lesson-controls' : 'panel-switcher-controls';
const fixture = `<!doctype html><html lang="en"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local comparison controls</title><style>
:root{--border:#334051;--muted:#bac5d5;--bright:#fff;--adp:#39d2c0;--bg2:#19222d;}
body{margin:0;background:#101720;color:#dce5ef;font:16px/1.6 sans-serif;}
main{padding:24px;} section{padding:16px;margin-bottom:20px;border:1px solid var(--border);border-radius:12px;min-width:0;}
[${panelAttribute}]{padding:16px;border-left:3px solid var(--adp);background:var(--bg2);overflow-wrap:anywhere;}
</style><main><h1>Explore each comparison independently</h1>
${['left','right'].map(id => `<section id="${id}" class="${rootClass}" ${rootAttribute} ${defaultAttribute}="${id === 'left' ? 'first' : 'second'}">
<h2>${id === 'left' ? 'Source material' : 'Reading material'}</h2>
<div class="${controlClass}" role="group" aria-label="${id} comparison">
${['first','second'].map(value => `<button type="button" ${choiceAttribute}="${value}" aria-pressed="false" aria-controls="${id}-${value}">${value === 'first' ? 'Overview' : 'Supporting detail'}</button>`).join('')}
</div>
${['first','second'].map(value => `<div id="${id}-${value}" ${panelAttribute}="${value}"><h3 id="${id}-${value}-child">${value === 'first' ? 'Overview' : 'Supporting detail'}</h3><p>This is neutral sample content for the ${id} comparison.</p></div>`).join('')}
</section>`).join('')}
<section id="incomplete" class="${rootClass}" ${rootAttribute}><h2>Incomplete markup remains readable</h2>
<div class="${controlClass}"><button ${choiceAttribute}="first">Overview</button></div>
<div ${panelAttribute}="first">First incomplete panel.</div><div ${panelAttribute}="second">Second incomplete panel.</div></section>
</main></html>`;

(async () => {
  await fs.mkdir(output, {recursive:true});
  const css = await fs.readFile(stylesheet, 'utf8');
  const browser = await chromium.launch({headless:true, executablePath:process.env.DOCS_CHROMIUM || undefined});
  const results = [];
  try {
    for (const viewport of [{width:1600,height:1000},{width:390,height:844}]) {
      const context = await browser.newContext({viewport,reducedMotion:'reduce'});
      const page = await context.newPage();
      page.setDefaultTimeout(10000);
      page.setDefaultNavigationTimeout(10000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.setContent(fixture);
      await page.addStyleTag({content:css});
      assert.equal(await page.locator(`[${panelAttribute}]:visible`).count(), 6, 'All options visible before initialization');
      assert.equal(await page.locator(`.${controlClass}:visible`).count(), 0, 'No inactive controls');
      await page.addScriptTag({path:source});
      const first = page.locator('#left-first');
      const second = page.locator('#left-second');
      assert.equal(await first.isVisible(), true);
      assert.equal(await second.isVisible(), false);
      assert.equal(await page.locator('#right-second').isVisible(), true, 'Independent default');
      assert.equal(await page.locator(`#incomplete[${readyAttribute}]`).count(), 0);
      assert.equal(await page.locator(`#incomplete [${panelAttribute}]:visible`).count(), 2);
      const secondButton = page.locator(`#left [${choiceAttribute}="second"]`);
      await secondButton.click();
      assert.equal(await second.isVisible(), true);
      assert.equal(await first.isVisible(), false);
      assert.equal(await secondButton.getAttribute('aria-pressed'), 'true');
      assert.equal(await page.locator('#right-second').isVisible(), true, 'No cross-group switching');
      await page.locator(`#left [${choiceAttribute}="first"]`).focus();
      await page.keyboard.press('Enter');
      assert.equal(await first.isVisible(), true, 'Keyboard activation');
      await page.evaluate(() => {location.hash = 'left-second-child';});
      await page.waitForFunction(() => !document.getElementById('left-second').hidden);
      await page.evaluate(async () => {
        location.hash = '%E0%A4%A';
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      });
      assert.equal(await second.isVisible(), true, 'Malformed hash preserves selection');
      await page.screenshot({path:path.join(output, `${viewport.width}-selected.png`),fullPage:true});
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false, 'No viewport overflow');
      const target = await secondButton.boundingBox();
      assert.ok(target.width >= 44 && target.height >= 44, 'Touch target');
      await page.emulateMedia({media:'print'});
      await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
      assert.equal(await page.locator(`[${panelAttribute}]:visible`).count(), 6, 'Print shows every option');
      assert.equal(await page.locator(`.${controlClass}:visible`).count(), 0, 'Print hides controls');
      await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
      await page.emulateMedia({media:'screen'});
      assert.equal(await first.isVisible(), false, 'Print restores prior selection');
      assert.equal(await second.isVisible(), true);
      await page.goto('about:blank#right-first-child');
      await page.setContent(fixture);
      await page.addStyleTag({content:css});
      await page.addScriptTag({path:source});
      assert.equal(await page.locator('#right-first').isVisible(), true, 'Initial hash overrides default');
      assert.equal(await page.locator('#right-second').isVisible(), false);
      assert.deepEqual(errors, []);
      results.push({viewport,defaults:true,independentGroups:true,buttonsAndKeyboard:true,hashReveal:true,printRestore:true,invalidInputReadable:true,horizontalOverflow:false,pageErrors:errors});
      console.log(JSON.stringify({legacy,viewport,result:'pass'}));
      await context.close();
    }
    const fallback = await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:false});
    const page = await fallback.newPage();
    page.setDefaultTimeout(10000);
    await page.setContent(fixture.replace('</style>', css + '</style>'));
    assert.equal(await page.locator(`[${panelAttribute}]:visible`).count(), 6);
    assert.equal(await page.locator(`.${controlClass}:visible`).count(), 0);
    await page.screenshot({path:path.join(output,'390-no-javascript.png'),fullPage:true});
    await fallback.close();
    await fs.writeFile(path.join(output,'results.json'), JSON.stringify({legacy,source,results,noJavaScriptReadable:true},null,2)+'\n');
    console.log(JSON.stringify({legacy,viewports:results.length,noJavaScriptReadable:true,result:'pass'}));
  } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
