// Optional real-browser review. Run as one owned, serialized local job.
const { chromium } = require(process.env.DOCS_PLAYWRIGHT || 'playwright');
const fs = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const assert = require('node:assert/strict');
const kit = path.resolve(__dirname, '..');
const root = path.join(kit, 'examples/starter/.build/docs');
const output = path.join(kit, '.build/visual-review');
const mime = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.woff2':'font/woff2'};
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

(async () => {
  await fs.mkdir(output,{recursive:true});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch({headless:true, executablePath:process.env.DOCS_CHROMIUM || undefined});
  const results=[];
  try {
    for(const viewport of [{width:1600,height:1000},{width:390,height:844}]) {
      const context = await browser.newContext({viewport,reducedMotion:'reduce'});
      const page = await context.newPage();
      const failures=[];
      page.on('pageerror',error=>failures.push(error.message));
      page.on('response',response=>{if(response.status()>=400) failures.push(response.url()+': '+response.status());});
      await page.goto(origin+'/html/guide.html',{waitUntil:'networkidle'});
      await page.evaluate(()=>document.fonts.ready);
      await page.waitForSelector('body.reader-enabled');
      const count=await page.locator('.chapter-body').count();
      for(let index=0;index<count;index++) {
        if(index) await page.keyboard.press('ArrowRight');
        await page.screenshot({path:path.join(output,`${viewport.width}-chapter-${index+1}.png`)});
        const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
        assert.equal(overflow,false,`page overflow at ${viewport.width}, chapter ${index+1}`);
        const broken=await page.locator('img').evaluateAll(images=>images.filter(i=>!i.complete||i.naturalWidth===0).length);
        assert.equal(broken,0,'broken image');
      }
      if(viewport.width>900) {
        await page.locator('[data-reader-view="pair"]').click();
        await page.screenshot({path:path.join(output,`${viewport.width}-comparison.png`)});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
      } else {
        const region=page.locator('.scroll[aria-label="Maintenance options; scroll horizontally"]');
        const metrics=await region.evaluate(el=>({scroll:el.scrollWidth,client:el.clientWidth,minWidth:getComputedStyle(el.querySelector('table')).minWidth}));
        assert.ok(metrics.scroll>metrics.client,'Mobile comparison must remain scrollable: '+JSON.stringify(metrics));
        await region.focus();
        await page.keyboard.press('ArrowRight');
        await region.evaluate(el=>{el.scrollLeft=el.scrollWidth;});
        await page.screenshot({path:path.join(output,'390-table-end.png')});
      }
      if(viewport.width<900) await page.locator('[data-reader-view-select]').selectOption('full');
      else await page.locator('[data-reader-view="full"]').click();
      await page.screenshot({path:path.join(output,`${viewport.width}-all.png`),fullPage:true});
      assert.deepEqual(failures,[]);
      await page.goto(origin+'/html/index.html',{waitUntil:'networkidle'});
      await page.screenshot({path:path.join(output,`${viewport.width}-home.png`),fullPage:true});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,'Home page overflow');
      results.push({viewport,chapters:count,consoleErrors:failures,horizontalOverflow:false});
      await context.close();
    }
    const fallback=await browser.newContext({viewport:{width:390,height:844},javaScriptEnabled:false});
    const page=await fallback.newPage();
    await page.goto(origin+'/html/guide.html');
    assert.ok((await page.textContent('main')).includes('Pin the tools, own the content'));
    await page.screenshot({path:path.join(output,'390-no-javascript.png'),fullPage:true});
    await fallback.close();
    await fs.writeFile(path.join(output,'results.json'),JSON.stringify(results,null,2)+'\n');
    console.log(JSON.stringify(results));
  } finally {await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
