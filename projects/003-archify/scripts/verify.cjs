// Requires Playwright on NODE_PATH and a running local static server.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {createHash}=require('node:crypto');
const root=path.resolve(__dirname,'..');
const base=process.env.ARCHIFY_DEMO_URL||'http://127.0.0.1:8763/';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.ARCHIFY_BROWSER_CHANNEL||'chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const reports=[];
 try{
  await page.goto(base+'examples.html');await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
  for(const id of ['architecture','workflow','sequence','dataflow','lifecycle','delta']){
   await page.locator(`[data-scene="${id}"]`).click();
   await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
   await page.frameLocator('#diagram').locator('svg').first().waitFor();
   assert.equal(await page.locator(`[data-scene="${id}"]`).getAttribute('aria-selected'),'true');
   assert.match(await page.locator('#open-diagram').getAttribute('href'),new RegExp(`/diagrams/${id}.html`));
   const frame=page.frames().find(f=>f.url().includes(`/diagrams/${id}.html`));
   reports.push({id,svgCount:await frame.locator('svg').count(),title:await frame.title()});
  }
  await page.locator('[data-scene="architecture"]').click();
  await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
  await page.locator('[data-scene="architecture"]').focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('[data-scene="workflow"]').getAttribute('aria-selected'),'true');
  await page.locator('[data-jump="architecture"][data-fragment]').click();
  await page.waitForFunction(()=>document.querySelector('#diagram').contentDocument?.documentElement.dataset.focus==='api'||document.querySelector('#diagram').contentWindow?.location.hash.includes('focus=api'));
  await page.locator('[data-scene="architecture"]').click();
  // Reset the deep link by reloading the gallery before composition captures.
  await page.goto(base+'examples.html');await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
  await page.screenshot({path:path.join(root,'web/assets/showcase-desktop.png'),fullPage:true});
  for(const width of [390,768,1440]){
   await page.setViewportSize({width,height:1000});
   const bounds=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
   assert.ok(bounds.scrollWidth<=bounds.width,`gallery overflow at ${width}`);
   if(width===390)await page.screenshot({path:path.join(root,'web/assets/showcase-mobile.png'),fullPage:true});
   reports.push({galleryViewport:width,...bounds});
  }
  await page.setViewportSize({width:1440,height:1000});
  for(const id of ['architecture','workflow','sequence','dataflow','lifecycle','delta']){
   await page.goto(base+`diagrams/${id}.html`);await page.locator('svg').first().waitFor();await page.evaluate(()=>document.fonts.ready);
   const bytes=fs.readFileSync(path.join(root,`web/diagrams/${id}.html`));
   const bounds=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight}));
   await page.screenshot({path:path.join(root,`web/assets/${id}-desktop.png`),fullPage:true});
   await page.locator(id==='delta'?'svg':'.diagram-container').first().screenshot({path:path.join(root,`web/assets/${id}-preview.png`)});
   reports.push({diagram:id,...bounds,sha256:createHash('sha256').update(bytes).digest('hex')});
  }
  await page.goto(base+'diagrams/architecture.html');
  await page.locator('svg').first().waitFor();
  await page.locator('.diagram-container').screenshot({path:path.join(root,'web/assets/cover.png')});
  const theme=await page.locator('html').getAttribute('data-theme');
  await page.keyboard.press('t');
  assert.notEqual(await page.locator('html').getAttribute('data-theme'),theme);
  await page.keyboard.press('/');await page.locator('#node-finder-input').fill('API');
  assert.ok(await page.locator('.node-finder-result').count()>0);
  await page.keyboard.press('Escape');
  // Check a real PNG export, including the file signature.
  await page.keyboard.press('e');
  const exportOptions=await page.locator('[role=menuitem]').allTextContents();
  const downloadPromise=page.waitForEvent('download');
  await page.locator('button[data-format="png"]').click();
  const download=await downloadPromise;
  const png=fs.readFileSync(await download.path());
  assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  reports.push({themeToggle:true,nodeSearch:true,exportOptions,pngExport:{bytes:png.length,width:png.readUInt32BE(16),height:png.readUInt32BE(20),signatureVerified:true}});
  await page.goto(base+'examples.html');await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
  await page.setViewportSize({width:390,height:1000});
  await page.locator('#preview-image').evaluate(img=>img.decode());
  await page.screenshot({path:path.join(root,'web/assets/showcase-mobile.png'),fullPage:true});
  assert.equal(errors.length,0,JSON.stringify(errors));
  fs.writeFileSync(path.join(root,'web/receipts/browser.json'),JSON.stringify({testedAt:new Date().toISOString(),browser:'Chromium / Playwright',reports,errors,scope:'Six local artifacts, gallery navigation, deep-link handoff, keyboard tabs, mobile/tablet/desktop containment, theme, search, export menu. Screenshots require separate visual review.'},null,2)+'\n');
  console.log(JSON.stringify({ok:true,reports,errors},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

