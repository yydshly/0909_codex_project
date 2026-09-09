// Browser verification for the archive only; never calls an AI model or clones a target.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname,'..');
const base = process.env.ARCHIVE_BASE_URL || 'http://127.0.0.1:8029';
const pagePath = '/_site/projects/002-ai-website-cloner-template/';
async function main(){
  const browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1840},deviceScaleFactor:1});
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('console',msg=>{if(msg.type()==='error')errors.push(msg.text());});
  const report={checkedAt:new Date().toISOString(),viewports:[],interactions:[],missingLinks:[],svgOverflow:[],errors};
  try{
    await page.setContent('<!doctype html><html><head><link rel="icon" href="data:,"></head><body style="margin:0">'+fs.readFileSync(path.join(root,'web/assets/architecture.svg'),'utf8')+'</body></html>');
    await page.evaluate(()=>document.fonts.ready);
    report.svgOverflow=await page.locator('svg text').evaluateAll(nodes=>nodes.flatMap(node=>{const b=node.getBoundingClientRect();return b.x<0||b.right>1440||b.y<0||b.bottom>1840?[{text:node.textContent,bounds:{x:b.x,width:b.width,y:b.y,height:b.height}}]:[]}));
    await page.screenshot({path:path.join(root,'web/assets/architecture.png')});
    if(process.argv.includes('--render-only')){if(report.svgOverflow.length)throw Error('SVG overflow');console.log('Rendered architecture.png');return;}
    for(const [width,height,name] of [[1440,1000,'desktop'],[768,1000,'tablet'],[390,844,'mobile']]){
      await page.setViewportSize({width,height});
      await page.goto(base+pagePath);
      await page.evaluate(()=>document.fonts.ready);
      const layout=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].filter(i=>!i.closest('dialog')).every(i=>i.complete&&i.naturalWidth>0)}));
      report.viewports.push({name,...layout});
      if(width===1440)await page.screenshot({path:path.join(root,'assets/desktop.png')});
      if(width===390)await page.screenshot({path:path.join(root,'assets/mobile.png'),fullPage:true});
    }
    for(let index=0;index<6;index++){
      await page.locator(`[data-step="${index}"]`).click();
      if(await page.locator(`[data-step="${index}"]`).getAttribute('aria-pressed')!=='true')throw Error('Step selection failed');
      if(!(await page.locator('#step-detail h3').textContent()))throw Error('Step detail missing');
    }
    report.interactions.push('Six process steps update their content and selection');
    await page.locator('[data-step="0"]').focus();await page.keyboard.press('End');
    if(await page.locator('[data-step="5"]').getAttribute('aria-pressed')!=='true')throw Error('Keyboard navigation failed');
    report.interactions.push('Keyboard End selects and focuses final step');
    await page.locator('[data-state="scrolled"]').click();
    if(!(await page.locator('#mini-header').getAttribute('class')).includes('scrolled'))throw Error('Scrolled example failed');
    await page.locator('[data-state="restored"]').click();
    if((await page.locator('#mini-header').getAttribute('class')).includes('scrolled'))throw Error('Restore example failed');
    report.interactions.push('Navigation example changes and restores state');
    await page.locator('#open-diagram').click();
    if(!await page.locator('#diagram-dialog').evaluate(el=>el.open))throw Error('Diagram did not open');
    await page.keyboard.press('Escape');
    if(await page.locator('#diagram-dialog').evaluate(el=>el.open))throw Error('Escape did not close diagram');
    if(!await page.locator('#open-diagram').evaluate(el=>el===document.activeElement))throw Error('Dialog focus was not restored');
    report.interactions.push('Diagram dialog opens, closes with Escape, and restores focus');
    await page.emulateMedia({reducedMotion:'reduce'});
    report.reducedMotion=await page.locator('#mini-header').evaluate(el=>getComputedStyle(el).transitionDuration==='0s');
    const internal=await page.locator('a[href]').evaluateAll(nodes=>[...new Set(nodes.map(n=>n.getAttribute('href')).filter(h=>!h.startsWith('http')&&!h.startsWith('#')))]);
    for(const href of internal){const response=await page.request.get(new URL(href,base+pagePath).href);if(!response.ok())report.missingLinks.push({href,status:response.status()});}
    report.jsDisabled=await (async()=>{const noJs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const p=await noJs.newPage();await p.goto(base+pagePath);const result=await p.locator('h1').isVisible()&&await p.locator('noscript').isVisible();await noJs.close();return result;})();
    if(report.svgOverflow.length||report.viewports.some(v=>v.scrollWidth>v.width||!v.images)||report.missingLinks.length||errors.length||!report.reducedMotion||!report.jsDisabled)throw Error('Archive verification failed: '+JSON.stringify(report));
    report.result='passed';
  }finally{
    fs.mkdirSync(path.join(root,'notes'),{recursive:true});
    fs.writeFileSync(path.join(root,'notes/browser-verification.json'),JSON.stringify(report,null,2)+'\n');
    await browser.close();
  }
  console.log(JSON.stringify(report,null,2));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
