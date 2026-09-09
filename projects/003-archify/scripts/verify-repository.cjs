const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const base=process.env.ARCHIFY_DEMO_URL||'http://127.0.0.1:8763/';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage({viewport:{width:1440,height:900}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(base+'diagrams/repository.html');await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.diagram-container > svg [data-node-id]').count(),11);
  await page.locator('.diagram-container').screenshot({path:path.join(root,'web/assets/repository-preview.png')});
  await page.locator('#node-build').click();
  const source=page.locator('a.semantic-passport-source').first();await source.waitFor();
  const href=await source.getAttribute('href');
  assert.equal(href,'https://github.com/yydshly/0909_codex_project/blob/855cde37272f0ab9912cfe8595ee0060ad531c9a/scripts/catalog.py#L133-L168');
  await page.screenshot({path:path.join(root,'web/assets/repository-source.png'),fullPage:true});
  await page.goto(base+'diagrams/repository.html#focus=build&reach=downstream');
  await page.locator('[data-reach-origin]').waitFor();
  const matched=await page.locator('.diagram-container > svg [data-node-id][data-reach-match]').evaluateAll(nodes=>nodes.map(n=>n.dataset.nodeId));
  assert.ok(matched.includes('site')&&matched.includes('pages')&&matched.includes('browser'));
  await page.goto(base+'examples.html#repository');await page.locator('#load-status').filter({hasText:'已载入'}).waitFor();
  assert.equal(await page.locator('#tab-repository').getAttribute('aria-selected'),'true');
  assert.equal(await page.locator('#source-link').getAttribute('href'),'./specs/repository.json');
  const sizes=[];
  for(const width of [1440,768,390]){
   await page.setViewportSize({width,height:1000});
   const bound=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(bound.scroll<=bound.width);sizes.push(bound);
   if(width!==768)await page.screenshot({path:path.join(root,`web/assets/repository-gallery-${width}.png`),fullPage:true});
  }
  await page.goto(base+'repository-notes.html');
  await page.locator('.case-image').evaluate(i=>i.decode());
  assert.equal(await page.locator('table tbody tr').count(),6);
  assert.equal(errors.length,0,JSON.stringify(errors));
  const receipt={ok:true,sourceHref:href,downstreamNodes:matched,viewports:sizes,errors,scope:'Real repository case: exact source link, authored downstream reach, gallery integration and notes page. Official visual-check receipt is separate.'};
  fs.writeFileSync(path.join(root,'web/receipts/repository-interactions.json'),JSON.stringify(receipt,null,2)+'\n');console.log(receipt);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});

