// Verify retrieval scope and safe rendering helpers without a browser or backend.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../web/app.js',import.meta.url),'utf8');
const definitions=source.slice(0,source.indexOf('let scenario ='));
const ranking=source.slice(source.indexOf('function rankDocuments('),source.indexOf('function showSample('));
const context=vm.createContext({});
vm.runInContext(definitions+'\n'+ranking+'\nglobalThis.testApi={scenarios,rankDocuments,escapeHtml};',context);
const {scenarios,rankDocuments,escapeHtml}=context.testApi;
assert.equal(scenarios.length,3);
for(const scenario of scenarios){
  assert.equal(rankDocuments(scenario.question,scenario.docs).length,3,`${scenario.id}: default query should retrieve all relevant samples`);
  assert.equal(rankDocuments('zzzzzzzz',scenario.docs).length,0,'Unrelated queries must not fabricate results');
  assert.equal(rankDocuments(scenario.question,[]).length,0,'Empty source scope must stay empty');
}
const product=scenarios[0];
assert.equal(rankDocuments('离线',product.docs)[0].doc.id,'P03');
assert.equal(rankDocuments('离线',product.docs.filter(d=>d.id!=='P03')).length,0,'Excluded document must never leak into citations');
assert.equal(rankDocuments('导出',product.docs).length,2);
assert.equal(escapeHtml('<img onerror="alert(1)">&'), '&lt;img onerror=&quot;alert(1)&quot;&gt;&amp;');
assert.equal(new Set(scenarios.flatMap(s=>s.docs.map(d=>d.id))).size,9);
console.log('PASS: 3 scenario queries, empty/unmatched scope, source exclusion, topic matching, unique citations, HTML escaping.');
