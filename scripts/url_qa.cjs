/* Exercise every legacy URL in a real browser, including query/anchor retention. */
const {chromium}=require('playwright');
const fs=require('fs');
const base=process.env.SITE_BASE || 'http://127.0.0.1:8765';
const aliases=JSON.parse(fs.readFileSync('static/data/url-redirects.json','utf8'));
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH});
 try {
  const page=await browser.newPage();
  for(const [old,target] of Object.entries(aliases)){
   await page.goto(base+old+'?source=url-check#main');
   const expected=new URL(target,base);expected.search='?source=url-check';expected.hash='#main';
   await page.waitForURL(expected.href);
   if(await page.locator('#site-header').count()!==1)throw Error('Missing canonical page after '+old);
  }
  await page.goto(base+'/connect/');await page.waitForURL(base+'/#connect');const contact=await page.locator('#connect a.primary').getAttribute('href');if(!contact.startsWith('mailto:sklegesi@gmail.com'))throw Error('Email contact recipient mismatch');
  const nojs=await browser.newContext({javaScriptEnabled:false});
  const fallback=await nojs.newPage();
  for(const old of ['/projects.html','/research/HS_Code/','/research/africa-affordable-housing-lab/calculator.html','/mtn-uganda-stock-coverage/valuation.html','/financial-literacy/emergency-fund/']){
   await fallback.goto(base+old);await fallback.waitForURL(base+aliases[old]);
  }
  await nojs.close();
  fs.mkdirSync('test-results',{recursive:true});
  fs.writeFileSync('test-results/url-qa.json',JSON.stringify({legacyForms:Object.keys(aliases).length,queryAndFragment:'passed',emailContact:'passed',noJavaScriptFallbacks:5},null,2));
  console.log('Passed '+Object.keys(aliases).length+' legacy redirects, query/anchor preservation and 5 no-JS fallbacks.');
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
