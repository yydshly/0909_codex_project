// Optional raster export. Run from the research repository root after installing
// @resvg/resvg-js into .research/rnskill-svg-render (kept outside version control).
const fs = require('node:fs');
const path = require('node:path');
const { Resvg } = require(path.resolve(__dirname, '../../../.research/rnskill-svg-render/node_modules/@resvg/resvg-js'));
const assets = path.resolve(__dirname, '../web/assets');
const svg = fs.readFileSync(path.join(assets, 'module-guide.svg'), 'utf8');
const result = new Resvg(svg, { font: { loadSystemFonts: true, defaultFontFamily: 'Microsoft YaHei' }, fitTo: { mode: 'width', value: 2760 } }).render();
fs.writeFileSync(path.join(assets, 'module-guide.png'), result.asPng());
console.log(`Exported ${result.width} x ${result.height} PNG`);
