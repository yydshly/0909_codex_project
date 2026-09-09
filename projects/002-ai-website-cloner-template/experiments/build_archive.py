"""Build the original architecture SVG and portable archive downloads."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'web' / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1840" viewBox="0 0 1440 1840" role="img" aria-labelledby="title desc">
<title id="title">URL 驱动的网页复刻：从目标地址到可运行的 Next.js 前端工程</title>
<desc id="desc">核心目标是输入 URL，复刻网页布局、样式、素材、响应式和可观察交互，输出前端工程。模型、工具与流程组织采集、分析、规格、实现和验证。共享证据保持一致，后台业务仍有边界。虚线框为额外工程建议。</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#236c62" stroke-width="1.5"/></marker><marker id="orange" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#a94528" stroke-width="1.5"/></marker></defs>
<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif;fill:#182e39}.tiny{font-size:17px;fill:#596b70}.body{font-size:21px;fill:#52676a}.head{font-size:27px;font-weight:700}.label{font-size:18px;fill:#236c62;font-weight:700;letter-spacing:1px}.line{fill:none;stroke:#236c62;stroke-width:2.5;marker-end:url(#arrow)}.feedback{fill:none;stroke:#a94528;stroke-width:2.5;marker-end:url(#orange)}</style>
<rect width="1440" height="1840" fill="#f6f3ec"/>
''']

def rect(x,y,w,h,fill='#fffefa',stroke='#c9d4ca',dash=False):
    d=' stroke-dasharray="8 6"' if dash else ''
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')

def text(x,y,s,cls='body',fill=None,size=None):
    extra=(f' style="fill:{fill}"' if fill else '')+(f' font-size="{size}"' if size else '')
    parts.append(f'<text x="{x}" y="{y}" class="{cls}"{extra}>{escape(s)}</text>')

def lines(x,y,values,cls='body',gap=31,fill=None):
    for i,s in enumerate(values):text(x,y+i*gap,s,cls,fill)

def path(d,orange=False):parts.append(f'<path d="{d}" class="{"feedback" if orange else "line"}"/>')

text(56,47,'研究室 / 002     ·     AI WEBSITE CLONER TEMPLATE','label')
parts.append('<text x="56" y="108" style="font-size:43px;font-weight:700">输入 URL，复刻为可运行的前端工程。</text>')
text(56,151,'目标：还原网页外观与可观察交互。方法：模型 + 工具 + 规格与验证流程。')
text(1120,47,'研究归档 2026.09.09','tiny')

for x,label,title,body in [
 (56,'能力来源 01','大模型',['理解截图与结构','归纳规则 · 生成代码 · 分析偏差']),
 (512,'能力来源 02','代理与工具环境',['浏览器采集与操作','文件编辑 · 终端运行 · 截图']),
 (968,'能力来源 03','本仓库的增量',['Skill / 检查规范 / 项目模板','任务拆分 · 输出约定 · 验收要求'])]:
    rect(x,187,416,151,'#e8eee5')
    text(x+23,219,label,'label');text(x+23,260,title,'head');lines(x+23,291,body,gap=28)

text(56,385,'起点：一个或多个目标 URL  /  打开网页，采集以下证据','label')
for x,title,body in [(56,'截图',['最终外观与区域关系','缺少隐藏状态和精确规则']),
                     (512,'DOM / CSS / 素材',['结构、样式、尺寸、文本与资源','不等于原始组件工程']),
                     (968,'操作记录',['点击、悬停、滚动、调整宽度','未观察到的行为仍然未知'])]:
    rect(x,406,416,118);text(x+23,443,title,'head');lines(x+23,475,body,gap=27)
path('M720 525 V557')
text(56,574,'主代理组织的处理循环  /  模型决定动作 → 工具执行 → 返回证据','label')

steps=[
 (56,599,'01','观察页面',['固定页面与环境，识别区域','滚动加载；保存参考截图']),
 (512,599,'02','提取事实',['读取结构、样式、尺寸和素材','多视口、多状态；标记遗漏']),
 (968,599,'03','归纳与推断',['识别重复规范、布局和交互','区分读取 / 确认 / 推断 / 未知']),
 (968,821,'04','写入组件规格',['结构、输入、行为、素材与样式','共享主题、接口及验收条件']),
 (512,821,'05','拆分与实现',['公共基础先行，独立任务并行','按职责分工，再组装页面']),
 (56,821,'06','对照与修复',['构建 + 视觉 + 交互检查','定位差异，修采集 / 规格 / 代码'])]
for x,y,num,title,body in steps:
    rect(x,y,416,163,'#fffefa' if num!='06' else '#e4ede0')
    text(x+24,y+33,num,'label');text(x+72,y+36,title,'head');lines(x+24,y+85,body,gap=32)
    text(x+24,y+141,{'01':'产物：页面拓扑与截图','02':'产物：原始数据与资源','03':'产物：规则和状态关系','04':'产物：可阅读的实现依据','05':'产物：Next.js 组件与路由','06':'产物：验收结果与已知缺口'}[num],'tiny')
path('M472 680 H506');path('M928 680 H962');path('M1176 762 V815');path('M968 904 H934');path('M512 904 H478')
path('M56 904 H28 V680 H50',True)
parts.append('<text transform="translate(20 850) rotate(-90)" class="tiny" style="fill:#a94528">差异反馈</text>')
text(996,799,'分析结果写入规格','tiny')

rect(56,1020,1328,106,'#e4ede0','#aec3b1')
text(82,1062,'验证后交付：可运行、可修改的 Next.js 前端工程','head')
text(82,1100,'页面 + 组件 + 路由 + 素材；复刻布局、样式、响应式与已观察到的交互。','body')
path('M264 985 V1014')
parts.append('<g transform="translate(0 130)">')
rect(56,1020,1328,130,'#182e39','#182e39')
text(82,1059,'贯穿全过程的共享依据','head','#f3f4e9')
text(82,1097,'真实素材 + 参考截图 + 组件规格 + 状态记录 + 输出路径','body','#d8e4dc')
text(82,1128,'事实有来源；推断有标记；未覆盖项保留。生成与验收始终对照同一份依据。','body','#b9cbc6')

text(56,1195,'怎样保持实现一致  /  并行只加速，不自动保证正确','label')
rect(56,1216,1328,128)
for x,title,body in [(80,'视觉与素材',['同一字体、主题、容器和资源']),
                     (520,'接口与状态',['明确输入、事件、布局与状态归属']),
                     (968,'修改与验收',['公共文件集中维护，固定条件对照'])]:
    text(x,1258,title,'head');lines(x,1294,body,cls='tiny')
text(80,1325,'流程约定需要实际执行；独立工作目录不能自动解决语义和接口冲突。','tiny')

rect(56,1372,1328,110,'#f1e8db','#d5c3a9')
text(80,1412,'能力边界','head','#8b492d')
text(278,1410,'构建通过 ≠ 视觉一致 ≠ 行为完整 ≠ 后端业务相同','body','#8b492d')
text(80,1450,'不能保证穷尽隐藏状态；Canvas / iframe 等需单独处理；认证、数据库、实时业务需要另外实现。','tiny')

rect(56,1510,1328,125,'#f8f5ed','#a17b43',True)
text(80,1550,'完整系统还需补充  /  我们的建议，非上游现成能力','head')
text(80,1585,'结构化契约与校验 → 任务状态与依赖 → 可重复验收 → 有界重试与断点恢复','body')
text(80,1614,'实现顺序：先采集准确、状态覆盖和局部修复，再扩展整站与更多并行。','tiny')
text(56,1675,'实线：职责与流程要求（不等于程序强制执行）    虚线：工程扩展建议','tiny')
text(1008,1675,'源码快照 92872bc · 克隆效果未实测','tiny')
parts.append('</g>')
parts.append('</svg>')
(ASSETS/'architecture.svg').write_text('\n'.join(parts),encoding='utf-8')

# Portable Markdown copies use absolute source links rather than broken relative links.
repo='https://github.com/yydshly/0909_codex_project/blob/main/projects/002-ai-website-cloner-template/'
for source,dest in [('README.md','understanding.md'),('notes/technical-understanding.md','technical-understanding.md'),('notes/sources.md','sources.md')]:
    content=(ROOT/source).read_text(encoding='utf-8')
    def link(match):
        target=match[1]
        if '://' in target or target.startswith('#'):return match[0]
        if target=='../../README.md':return '](https://github.com/yydshly/0909_codex_project)'
        return ']('+repo+target+')'
    content=re.sub(r'\]\(([^)]+)\)',link,content)
    (ASSETS/dest).write_text(content,encoding='utf-8')

catalog_path=ROOT.parents[1]/'registry/projects.json'
catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
for project in catalog['projects']:
    if project['slug']=='ai-website-cloner-template':
        project.update(name='URL 驱动的 AI 网页复刻',summary='输入一个或多个目标 URL，借助 AI 编程代理复刻网页布局、样式、素材和可观察交互，生成可修改的 Next.js 前端工程；以规格和验证流程减少执行遗漏。',status='已归档',tags=['URL 网页复刻','Agent 工作流','流程约束'],cover='web/assets/architecture.svg',demo=True)
catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Built architecture.svg, portable documents, and catalog entry.')
