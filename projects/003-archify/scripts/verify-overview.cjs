const {chromium}=require('playwright');const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');
const web=path.resolve(__dirname,'../web');const base=process.env.ARCHIFY_DEMO_URL||'http://127.0.0.1:8763/';
(async()=>{const browser=await chromium.launch({headless:true,channel:'chrome'});const p=await browser.newPage({viewport:{width:1800,height:1200},deviceScaleFactor:2});const errors=[];p.on('pageerror',e=>errors.push(e.message));const result={viewports:[],errors};try{
await p.goto(base+'assets/understanding.svg');await p.evaluate(()=>document.fonts.ready);
result.textBounds=await p.locator('svg text').evaluateAll(es=>es.map(e=>{const b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height}}));
result.outside=result.textBounds.filter(b=>b.x<0||b.x+b.w>1800||b.y<0||b.y+b.h>3180);
result.overlaps=[];for(let i=0;i<result.textBounds.length;i++)for(let j=i+1;j<result.textBounds.length;j++){const a=result.textBounds[i],b=result.textBounds[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>3&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>3)result.overlaps.push([a.text,b.text]);}
console.log('text geometry',JSON.stringify({outside:result.outside,overlaps:result.overlaps}));
await p.locator('svg').screenshot({path:path.join(web,'assets/understanding.png')});
await p.setViewportSize({width:1200,height:630});await p.evaluate(()=>{document.documentElement.style.width='1200px';document.documentElement.style.height='auto';});await p.screenshot({path:path.join(web,'assets/understanding-preview.png')});
assert.equal(result.outside.length,0);assert.equal(result.overlaps.length,0,JSON.stringify(result.overlaps));
await p.goto(base);await p.locator('#map svg').waitFor();assert.equal(await p.locator('#map svg a').count(),9);await p.locator('#more').click();assert.equal(await p.locator('#scale').textContent(),'125%');await p.locator('#less').click();assert.equal(await p.locator('#scale').textContent(),'100%');await p.locator('#fit').click();
for(const width of [1440,768,390]){await p.setViewportSize({width,height:1000});const s=await p.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(s.scroll<=s.width);result.viewports.push(s);if(width!==768)await p.screenshot({path:path.join(web,'assets/overview-'+width+'.png'),fullPage:true});}
await p.locator('#more').click();assert.ok(await p.locator('#map-scroll').evaluate(e=>e.scrollWidth>e.clientWidth));assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.locator('#fit').click();
const paths=new Set(['assets/understanding.svg','assets/understanding.png','assets/understanding-preview.png']);for(const file of ['index.html','research.html','self.html','examples.html']){await p.goto(base+file);if(file==='index.html')await p.locator('#map svg').waitFor();const urls=await p.locator('a[href],img[src],script[src],link[href],source[src]').evaluateAll(es=>es.map(e=>e.getAttribute('href')||e.getAttribute('src')).filter(s=>s&&!/^(https?:|#|mailto:)/.test(s)));for(const url of urls)paths.add(url);assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
for(const file of paths){const response=await p.request.get(new URL(file,base).href);assert.equal(response.status(),200,file);}result.resourcesChecked=paths.size;
assert.equal(errors.length,0,JSON.stringify(errors));delete result.textBounds;result.ok=true;fs.writeFileSync(path.join(web,'receipts/overview-browser.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});

