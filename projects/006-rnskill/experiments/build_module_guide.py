"""Generate one source-linked diagram with all reviewed skill entries."""
from pathlib import Path
from html import escape
import json
import csv

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
DATA = json.loads((WEB/'data/catalog.json').read_text(encoding='utf-8'))
GROUPS = {g['id']:g for g in DATA['categories']}
with (ROOT/'notes/capabilities.psv').open(encoding='utf-8',newline='') as rows:
    ORDER={row['key']:i for i,row in enumerate(csv.DictReader(rows,delimiter='|'))}
META = {
 'business': ('先把问题想清楚', '诊断业务、澄清目标，借不同视角推演选择。', '业务问题、目标、案例', '分析、判断与行动建议'),
 'plan': ('决定做什么、怎么开头', '记录灵感，规划选题、实测内容与标题。', '灵感、主题、观众', '选题卡、策划稿、标题候选'),
 'copy': ('把想法写成可以使用的内容', '改写与精修文稿，检查开头、结构和共鸣。', '草稿、逐字稿、受众信息', '新文稿、交接稿、诊断报告'),
 'media': ('获取并整理已有素材', '提取文章与视频内容，审核和剪辑口播。', '链接、文章、原始视频', '正文、逐字稿、粗剪、工程'),
 'voice': ('让内容被听见、被读懂', '生成配音与数字人，制作准确且可读的字幕。', '文稿、声音、最终音视频', '配音、数字人、字幕及质检'),
 'visual': ('把内容变成静态视觉', '制作插图、不同风格的封面与图文卡片。', '文章、标题、配图意图', '插图、封面、SVG / PNG'),
 'motion': ('把概念与画面变成动态', '编排动画，拆解参考，提取人体动作数据。', '主题、场景、授权参考视频', '动效工程、视频、关键点'),
 'ops': ('管理交接、质量与长期积累', '安排制作、验证结果，保存反馈与内容资产。', '交接稿、作品、指标、反馈', '成片归档、质检、知识与规则'),
 'agent': ('连接执行工具，整理工作入口', '调用 Grok Build，并统一不同 Agent 的规则。', '外部任务、现有项目规则', '工具结果、桥接文件与迁移记录'),
}
PARTS=[]
def add(text): PARTS.append(text)
def text(x,y,label,size=18,color='#354531',weight='400',extra=''):
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(label))}</text>')
def rect(x,y,w,h,fill='#fbfcf7',stroke='#d4ddc9',radius=10):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

def module(key,x,y,w,h,accent):
    g=GROUPS[key]; subtitle,intro,inputs,outputs=META[key]
    entries=sorted((s for s in DATA['skills'] if s['category']==key),key=lambda s:ORDER[s['key']])
    rect(x,y,w,h)
    rect(x,y,5,h,accent,accent,2)
    text(x+22,y+35,f'{g["number"]}  {g["name"]}',24,'#273723','650')
    text(x+w-22,y+34,f'{len(entries):02} 项',15,accent,'600','text-anchor="end"')
    text(x+22,y+64,subtitle,17,accent,'550')
    text(x+22,y+90,intro,14,'#6a775f')
    add(f'<path d="M{x+22} {y+106}H{x+w-22}" stroke="#e1e6d9"/>')
    for i,s in enumerate(entries):
        sy=y+134+i*23
        tag=' [别名]' if s['alias'] else ' [嵌套]' if s['nested'] else ''
        title=s['title']
        if s['key']=='孙割': title='孙割 → 孙宇晨'
        dot={'method':'#657f47','tools':'#64869b','workspace':'#b48452'}[s['reuse']]
        add(f'<a href="{escape(s["source"],quote=True)}" target="_blank" rel="noopener noreferrer" data-skill="{escape(s["key"],quote=True)}" aria-label="介绍：{escape(title,quote=True)}"><title>{escape(s["key"]+"："+s["summary"])}</title><rect class="hit" x="{x+16}" y="{sy-18}" width="{w-32}" height="23" rx="4" fill="transparent"/>')
        add(f'<circle cx="{x+27}" cy="{sy-6}" r="3.5" fill="{dot}"/>')
        text(x+40,sy,title+tag,16,'#3a4733')
        text(x+w-22,sy,'↗',12,'#87957c',extra='text-anchor="end"')
        add('</a>')
    if key=='agent':
        rect(x+22,y+192,w-44,97,'#edf1e5','#e0e7d5',6)
        text(x+40,y+219,'一个技能，通常把六件事说清楚',17,'#4e6740','600')
        text(x+40,y+247,'何时使用 → 输入材料 → 操作步骤 → 调用工具 → 产物 → 验收',16,'#627655')
        text(x+40,y+273,'执行时仍需宿主 Agent，以及可用的工具、账号与本地环境。',14,'#718367')
    fy=y+h-50
    add(f'<path d="M{x+22} {fy-17}H{x+w-22}" stroke="#e1e6d9"/>')
    text(x+22,fy+5,'输入  '+inputs,14,'#78856d')
    text(x+22,fy+30,'产物  '+outputs,14,'#526447','550')

def band(y,index,title,note,color):
    text(64,y,f'{index}  {title}',22,color,'650')
    text(1776,y,note,14,'#7b8971',extra='text-anchor="end"')
    add(f'<path d="M64 {y+15}H1776" stroke="#d4ddc9"/>')

def main():
    add('<svg xmlns="http://www.w3.org/2000/svg" width="1840" height="1840" viewBox="0 0 1840 1840" role="img" aria-labelledby="map-title map-description">')
    add('<title id="map-title">rnskill 全能力模块引导图</title><desc id="map-description">全部63个技能入口分成9个模块，按方向与内容、素材与制作、调度与支撑三层阅读。每个模块列出用途、技能、输入和产物。技能链接指向固定版本源码。</desc>')
    add('<style>a:hover .hit,a:focus .hit{fill:#e7eddc}a:focus{outline:none}text{pointer-events:none}</style>')
    rect(0,0,1840,1840,'#f3f5ed','#f3f5ed',0)
    add('<g font-family="Segoe UI,Microsoft YaHei,sans-serif">')
    text(64,48,'PROJECT LAB / 006  ·  MODULE GUIDE',14,'#7b8b6d',extra='letter-spacing="3"')
    text(64,104,'rnskill：把重复任务整理成可复用的工作方法',37,'#283b22','650')
    text(64,143,'先找到自己的任务，再选模块与技能。图中层次用于阅读引导，实际任务按需要组合，不要求依次跑完。',18,'#6c7e5f')
    text(1776,98,'9 模块 / 63 入口',24,'#54733f','600','text-anchor="end"')
    rect(64,170,1712,89,'#e4ebd8','#cfdcbd',8)
    text(88,203,'技能打包什么？',18,'#476236','650')
    text(88,235,'动作：重复操作     方法：判断与检查     流程：步骤与交接',19,'#4b613d')
    text(935,203,'运行时怎么做？',18,'#476236','650')
    text(935,235,'用户需求 → Agent 读取技能 → 调用工具 → 检查并交付',19,'#4b613d')
    band(303,'A','方向与内容：先想清楚，再写出来','三个模块可单独使用，也可组成策划与写作流程。','#587746')
    for key,x in [('business',64),('plan',640),('copy',1216)]:module(key,x,337,560,500,'#68864f')
    band(860,'B','素材与制作：按目标产物选择能力','以下为可组合的制作分支；配音、图片和动画并非每次都需要。','#587e91')
    for key,x in [('media',64),('voice',496),('visual',928),('motion',1360)]:module(key,x,894,416,384,'#688b9d')
    band(1310,'C','调度与支撑：贯穿执行，把结果留下来','制作前明确交接，制作后检查与归档，复盘结果回到下一次选题。','#9a754e')
    module('ops',64,1344,848,410,'#aa8358')
    module('agent',928,1344,848,410,'#aa8358')
    text(64,1798,'● 绿：方法可复用   ● 蓝：需工具配置   ● 棕：需工作台适配   ·   [嵌套] 5 项 / [别名] 1 项',13,'#6a7c5d')
    text(1776,1798,'58 顶层 + 5 嵌套 = 63 文件入口 · 含重叠能力 · 静态核对，未实测 · 7cbf47b / 2026-09-09',12,'#7d8a71',extra='text-anchor="end"')
    add('</g></svg>')
    svg='\n'.join(PARTS)
    assert svg.count('data-skill=')==DATA['total']
    (WEB/'assets/module-guide.svg').write_text(svg,encoding='utf-8')
    template=(ROOT/'experiments/module-guide-template.html').read_text(encoding='utf-8')
    (WEB/'guide.html').write_text(template.replace('<!-- MODULE_GUIDE -->',svg.replace('role="img"','role="group"',1)),encoding='utf-8')
    (WEB/'guide-print.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>rnskill 完整模块引导图</title><style>html,body{margin:0;width:1840px}svg{display:block}</style>'+svg+'</html>',encoding='utf-8')
    print('Generated single 1840 x 1840 diagram covering all 63 entries.')

if __name__=='__main__':main()
