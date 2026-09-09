import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const project = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const upstream = path.resolve(process.argv[2] || '.research/archify');
const revision = '10722002bb8777ecb639d93c49586fae4adf3ae4';
const git = spawnSync('git', ['-C', upstream, 'rev-parse', 'HEAD'], { encoding: 'utf8' });
if (git.status !== 0 || git.stdout.trim() !== revision) throw new Error(`Use the pinned upstream revision: ${revision}`);
const web = path.join(project, 'web');
for (const dir of ['diagrams', 'specs', 'receipts', 'assets']) fs.mkdirSync(path.join(web, dir), { recursive: true });
const examples = [
  ['architecture', 'web-app.architecture.json', 'Web 应用架构'],
  ['workflow', 'agent-tool-call.workflow.json', 'Agent 工具调用流程'],
  ['sequence', 'cache-miss-request.sequence.json', '缓存未命中的请求时序'],
  ['dataflow', 'product-analytics.dataflow.json', '产品分析数据流'],
  ['lifecycle', 'agent-run.lifecycle.json', 'Agent 任务生命周期'],
];
const receiptPaths = [];
function run(args) {
  const r = spawnSync(process.execPath, [path.join(upstream, 'archify/bin/archify.mjs'), ...args], { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 });
  if (r.status !== 0) throw new Error(r.stdout + r.stderr);
  return JSON.parse(r.stdout);
}
function portable(value) {
  if (Array.isArray(value)) return value.map(portable);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k,v]) => [k,portable(v)]));
  if (typeof value === 'string') {
    const normalized = value.replaceAll('\\', '/');
    const base = project.replaceAll('\\', '/');
    if (normalized.startsWith(base + '/')) return normalized.slice(base.length + 1);
  }
  return value;
}
for (const [type, file, title] of examples) {
  const spec = JSON.parse(fs.readFileSync(path.join(upstream, 'archify/examples', file), 'utf8'));
  spec.meta.title = title;
  spec.meta.locale = 'zh-CN';
  spec.meta.animation = 'none';
  spec.meta.output = `${type}.html`;
  const input = path.join(web, 'specs', `${type}.json`);
  fs.writeFileSync(input, JSON.stringify(spec, null, 2) + '\n');
  const receipt = run(['deliver', type, input, path.join(web, 'diagrams', `${type}.html`), '--quality', 'showcase', '--json']);
  fs.writeFileSync(path.join(web, 'receipts', `${type}.json`), JSON.stringify(portable(receipt), null, 2) + '\n');
  receiptPaths.push(`${type}.json`);
  console.log(`${type}: delivered`);
}
for (const side of ['base','head']) {
  const spec = JSON.parse(fs.readFileSync(path.join(upstream, `archify/examples/checkout-platform.${side}.architecture.json`), 'utf8'));
  spec.meta.locale = 'zh-CN';
  fs.writeFileSync(path.join(web, 'specs', `delta-${side}.json`), JSON.stringify(spec, null, 2) + '\n');
}
const delta = run(['compare', 'architecture', path.join(web,'specs/delta-base.json'), path.join(web,'specs/delta-head.json'), path.join(web,'diagrams/delta.html'), '--receipt', path.join(web,'diagrams/delta.receipt.json'), '--quality','showcase','--json']);
fs.writeFileSync(path.join(web, 'receipts/delta.json'), JSON.stringify(portable(delta), null, 2) + '\n');
for (const [from,to] of [['LICENSE','LICENSE-Archify.txt'],['THIRD_PARTY_NOTICES.md','THIRD-PARTY-NOTICES.md'],['archify/assets/JetBrainsMono-OFL.txt','JetBrainsMono-OFL.txt']]) fs.copyFileSync(path.join(upstream,from),path.join(web,to));
const manifest = { upstream:'https://github.com/tt-a1i/archify', revision, version:'2.17.0-dev.1', modifications:'Chinese page titles and viewer locale; static by default. Original English example content and topology retained.', artifacts: [...examples.map(([type])=>type),'delta'].map(id=>{const b=fs.readFileSync(path.join(web,`diagrams/${id}.html`));return {id,bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')};}) };
fs.writeFileSync(path.join(web,'receipts/manifest.json'),JSON.stringify(manifest,null,2)+'\n');
console.log('delta: compared; licenses and provenance saved');
