"""Build the reviewed, static catalog from inventory and editorial annotations."""
from pathlib import Path
import csv
import json
from collections import Counter
from html import escape

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ('plan','选题与策划','从灵感走到可制作的选题','01'),
    ('copy','写作与表达','把内容写清楚，再检查表达','02'),
    ('media','素材与剪辑','获取素材、转写与编辑视频','03'),
    ('voice','声音与字幕','配音、数字人和字幕时间轴','04'),
    ('visual','封面与图文','把文字转成可发布的视觉内容','05'),
    ('motion','动画与动效','设计运动、重建参考与提取动作','06'),
    ('ops','调度与沉淀','制作交接、质检和内容资产管理','07'),
    ('business','商业与思考','诊断问题、比较视角与规划行动','08'),
    ('agent','Agent 工具','连接其他工具与整理工作台','09'),
]
REUSE = {'method':'方法可复用','tools':'需工具配置','workspace':'需工作台适配'}

def main():
    inventory = json.loads((ROOT/'web/data/inventory.json').read_text(encoding='utf-8'))
    with (ROOT/'notes/capabilities.psv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='|'))
    annotations = {r['key']:r for r in rows}
    assert len(annotations) == len(rows), 'Duplicate editorial keys'
    skills = []
    used = set()
    for source in inventory['skills']:
        key = source['name'] if source['nested'] else source['path'].split('/')[1]
        assert key in annotations, f'Missing review: {key}'
        row = annotations[key]
        assert row['category'] in {g[0] for g in GROUPS}
        assert row['reuse'] in REUSE and all(row.values())
        used.add(key)
        item = {**source, **row, 'id': f'skill-{len(skills)+1:02}', 'alias': key == '孙割'}
        item['evidence'] = '已读技能定义；部分代表脚本已静态核对。未执行上游功能。'
        item['license'] = ('CC BY-NC 4.0（dbs 工具箱）' if key.startswith('dbs') else
            'AGPL-3.0（该模块声明）' if key == 'ai-jian-koubo' else
            'MIT（该模块声明）' if key in ['video-use','ian-xiaohei-illustrations'] else
            '目录内许可优先；仓库默认 CC BY-NC 4.0，嵌套和改编内容另核上游许可')
        skills.append(item)
    assert used == set(annotations), f'Unexpected rows: {set(annotations)-used}'
    count = Counter(s['category'] for s in skills)
    categories = [dict(id=a, name=b, description=c, number=d, count=count[a]) for a,b,c,d in GROUPS]
    result = {**{k:v for k,v in inventory.items() if k!='skills'}, 'categories':categories,
              'reuseLabels':REUSE,'reuseCounts':dict(Counter(s['reuse'] for s in skills)),
              'skills':skills,'scopeNote':'按固定提交的 SKILL.md 文件统计：58 个顶层入口、5 个嵌套入口，其中孙割为别名。文件数不等于互不重复的能力数。上游 README 标注 57，本页采用目录核对口径。'}
    encoded = json.dumps(result,ensure_ascii=False,indent=2)
    (ROOT/'web/data/catalog.json').write_text(encoded+'\n',encoding='utf-8')
    (ROOT/'web/data/catalog.js').write_text('window.RNSKILL_CATALOG = '+encoded+';\n',encoding='utf-8')
    lines = ['# rnskill 完整能力清单','',f"核对版本：`{inventory['commit']}` · 日期：{inventory['checked']}",
             '',result['scopeNote'],'','复用分类是静态研究判断；未验证工具已安装、账号可用或上游功能运行成功。','']
    for group in categories:
        lines += [f"## {group['number']} · {group['name']}（{group['count']} 个入口）",'',
                  '| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |','| --- | --- | --- | --- | --- |']
        for s in skills:
            if s['category'] == group['id']:
                lines.append(f"| [{s['key']}]({s['source']}) | **{s['title']}**：{s['summary']} | {s['input']} → {s['output']} | {s['dependencies']} | {REUSE[s['reuse']]} |")
        lines.append('')
    (ROOT/'notes/capability-catalog.md').write_text('\n'.join(lines),encoding='utf-8')
    assets=ROOT/'web/assets'
    assets.mkdir(exist_ok=True)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="740" viewBox="0 0 1200 740" role="img" aria-labelledby="title desc">',
         '<title id="title">rnskill 九类能力总览</title><desc id="desc">63 个技能文件入口，包括 58 个顶层和 5 个嵌套入口。按九类工作能力整理。</desc>',
         '<rect width="1200" height="740" fill="#f4f5ed"/>',
         '<g font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#293422">',
         '<text x="48" y="48" font-size="13" letter-spacing="3" fill="#738261">PROJECT LAB / RESEARCH 006</text>',
         '<text x="48" y="111" font-size="42" font-weight="650">rnskill · 个人能力工作台</text>',
         '<text x="48" y="150" font-size="17" fill="#78846b">工作方法 × 工具调用 × 生产流程</text>',
         '<rect x="890" y="58" width="260" height="100" rx="8" fill="#dfe8ce"/>',
         '<text x="912" y="105" font-size="30" font-weight="600">63 个入口 · 9 类</text>',
         '<text x="912" y="134" font-size="13" fill="#657950">58 顶层 + 5 嵌套（含别名）</text>']
    for i,g in enumerate(categories):
        x=48+(i%3)*377;y=195+(i//3)*151
        svg += [f'<rect x="{x}" y="{y}" width="350" height="128" rx="7" fill="#fdfdf9" stroke="#d8dfcc"/>',
                f'<text x="{x+20}" y="{y+29}" font-size="12" fill="#82916e">{g["number"]} / CAPABILITY</text>',
                f'<text x="{x+20}" y="{y+65}" font-size="23" font-weight="600">{escape(g["name"])}</text>',
                f'<text x="{x+312}" y="{y+64}" font-size="24" text-anchor="end" fill="#82916e">{g["count"]:02}</text>',
                f'<text x="{x+20}" y="{y+99}" font-size="13" fill="#7a856d">{escape(g["description"])}</text>']
    svg += ['<path d="M48 675H1150" stroke="#d8dfcc"/>',
            '<text x="48" y="708" font-size="12" fill="#7a856d">文件数量不等于独立能力数量 · 能力定义已整理，上游运行效果未实测</text>',
            '<text x="1150" y="708" font-size="12" text-anchor="end" fill="#7a856d">7cbf47b / 2026.09.09</text></g></svg>']
    (assets/'overview.svg').write_text('\n'.join(svg),encoding='utf-8')
    print(f"Reviewed {len(skills)} entries in {len(categories)} categories; {dict(count)}")

if __name__ == '__main__':
    main()
