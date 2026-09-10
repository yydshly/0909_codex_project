"""Render the same architecture diagram to editable SVG and a shareable PNG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/assets'
W, H = 1800, 1420
im = Image.new('RGB', (W, H), '#f3f6f8')
draw = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">', '<title id="title">SurfSense 原有研究架构与后续扩展</title>', '<desc id="desc">左侧为 NotebookLM 式资料入库、混合检索、模型问答、引用和播客；右侧为平台实时数据、外部 MCP、自动化和对外工具服务。底部为共用的模型、存储、任务及界面基础设施。早期已经存在 Agent、连接器和 API，本图不是它们的首次上线时间表。</desc>', f'<rect width="{W}" height="{H}" fill="#f3f6f8"/>']
INK, MUTED, TEAL, PURPLE = '#173749', '#546d7c', '#006e78', '#6546a5'
FONT = Path('C:/Windows/Fonts/msyh.ttc')
BOLD = Path('C:/Windows/Fonts/msyhbd.ttc')

def rect(x,y,w,h,fill,stroke=None,r=12):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')

def text(x,y,value,size=20,fill=INK,bold=False):
    font=ImageFont.truetype(str(BOLD if bold else FONT),size)
    draw.text((x,y),value,font=font,fill=fill)
    # SVG y uses a baseline; Pillow uses font-top coordinates.
    ascent,_=font.getmetrics()
    svg.append(f'<text x="{x}" y="{y+ascent}" fill="{fill}" font-family="Microsoft YaHei,Segoe UI,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(value)}</text>')

def line(points,color=TEAL,arrow=True,dashed=False):
    draw.line(points,fill=color,width=3)
    svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="3"'+(' stroke-dasharray="8 6"' if dashed else '')+'/>')
    if arrow:
        x,y=points[-1];px,py=points[-2]
        if x>px: tri=[(x,y),(x-10,y-5),(x-10,y+5)]
        elif x<px: tri=[(x,y),(x+10,y-5),(x+10,y+5)]
        elif y>py: tri=[(x,y),(x-5,y-10),(x+5,y-10)]
        else: tri=[(x,y),(x-5,y+10),(x+5,y+10)]
        draw.polygon(tri,fill=color)
        svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in tri)+f'" fill="{color}"/>')

def node(x,y,w,h,title,lines,color=TEAL):
    rect(x,y,w,h,'#ffffff','#c8dce0' if color==TEAL else '#d6cbe8')
    rect(x+16,y+20,4,27,color,r=2)
    text(x+30,y+16,title,23,color,True)
    for i,body in enumerate(lines):text(x+20,y+60+i*29,body,18,MUTED)

text(45,30,'SURFSENSE / 能力与技术原理',19,TEAL,True)
text(45,74,'NotebookLM 式研究核心，向实时网络与 Agent 工具扩展',40,INK,True)
text(45,137,'先理解“能做什么”，再沿箭头看“如何实现”：资料准备 → 查询研究 → 成果交付。',23,MUTED)
rect(45,185,16,16,TEAL,r=4);text(73,178,'原有核心（早期版本已具备）',19,TEAL)
rect(525,185,16,16,PURPLE,r=4);text(553,178,'后续扩展 / 强化（共用原有核心）',19,PURPLE)
rect(40,230,1120,865,'#e9f4f3','#bedbd9',18)
rect(1190,230,570,865,'#f1edf8','#d6cce7',18)
text(68,251,'A · 围绕自己的资料学习与研究',28,TEAL,True)
text(68,297,'能力：导入资料 · 跨文档问答 · 总结对比 · 引用追溯 · 播客',22,INK)
text(1218,251,'B · 从资料研究走向实时研究',26,PURPLE,True)
text(1218,297,'能力：新鲜数据 · 工具连接 · 持续执行',21,INK)
text(70,341,'① 入库时：把资料变成可检索的知识',19,TEAL,True)
node(70,380,235,136,'接入资料',['文件 / 图片 / 音视频','网页保存 / 外部来源'])
node(335,380,235,136,'解析与切分',['提取文本 / 转写 / 识图','分块并保留来源信息'])
node(600,380,235,136,'Embedding 索引',['语义向量：表示内容含义','文档 / 片段索引与去重'])
node(865,380,235,136,'知识库',['PostgreSQL + pgvector','内容 / 向量 / 元数据'])
for x in (305,570,835):line([(x,448),(x+30,448)])
text(70,542,'早期已有层级索引、混合检索、重排序；当前实现按文档组织命中片段。',18,MUTED)
line([(980,516),(980,579),(717,579),(717,638)])
text(742,582,'读取候选证据',17,TEAL)
text(70,600,'② 提问时：先找到相关证据，再组织回答',19,TEAL,True)
node(70,640,235,142,'用户问题',['选择资料范围','携带会话上下文'])
node(335,640,235,142,'研究 Agent',['拆解问题 / 选择工具','管理多步骤研究状态'])
node(600,640,235,142,'检索与重排序',['语义 + 全文 → RRF','可选 reranker 精排'])
node(865,640,235,142,'模型生成答案',['问题 + 证据 → LLM','片段 ID 关联引用'])
for x in (305,570,835):line([(x,711),(x+30,711)])
text(70,803,'RAG：把证据交给模型回答',19,MUTED)
line([(980,782),(980,836)],arrow=False)
line([(980,864),(980,914)])
text(70,885,'③ 交付时：同一份研究，形成不同表达',19,TEAL,True)
rect(70,925,1030,137,'#ffffff','#bedbd9')
text(92,942,'问答 / 总结 / 对比',23,TEAL,True)
text(92,983,'模型结合证据组织文本',19,MUTED)
text(92,1014,'用户沿引用回到原始片段',19,MUTED)
text(420,942,'播客（早期已有）',23,TEAL,True)
text(420,983,'研究内容 → 对话脚本',19,MUTED)
text(420,1014,'→ TTS 语音合成 → 音频',19,MUTED)
text(759,942,'更多成果（后续强化）',22,PURPLE,True)
text(759,983,'报告 / 文档 / 表格 / 演示',19,MUTED)
text(759,1014,'视频等还需相应生成与渲染服务',17,MUTED)
node(1220,380,510,158,'平台实时数据连接器',['Reddit / YouTube / 社交 / 电商 / 地图等','专用采集与解析 → 结构化条目','按平台使用 HTTP、浏览器、代理与重试'],PURPLE)
line([(1220,453),(1100,453)],PURPLE)
text(1107,391,'解析后',16,PURPLE);text(1107,416,'索引入库',16,PURPLE)
node(1220,590,510,164,'外部 MCP 与更复杂的 Agent 编排',['连接已授权的第三方工具','计划 / 子 Agent / 工具调用 / 结果反馈','实时结果可直接用于研究，也可留存'],PURPLE)
line([(1220,674),(1177,674),(1177,850),(452,850),(452,782)],PURPLE,dashed=True)
rect(667,834,255,32,'#e9f4f3',r=3);text(677,836,'工具结果回到同一研究流程',17,PURPLE)
node(1220,787,510,118,'定时与事件触发',['触发器 → 运行 Agent → 摘要 / 写回'],PURPLE)
node(1220,938,510,124,'对外 REST API + MCP 服务',['外部程序 / Agent → SurfSense 工具','MCP 服务通过 REST 调用后端能力'],PURPLE)
text(48,1116,'共用基础设施 · 两部分并非两套独立系统',23,INK,True)
for x,title,body in [(45,'界面与服务','Next.js / React / FastAPI'),(480,'模型与语音','LiteLLM / Embedding / TTS'),(915,'存储与后台任务','PostgreSQL / pgvector / Celery / Redis'),(1350,'权限与部署','工作区授权 / 成员角色 / Docker')]:
    rect(x,1160,405,105,'#173749',r=12)
    text(x+20,1175,title,21,'#a2ece3',True)
    text(x+20,1217,body,16,'#ffffff')
text(48,1290,'演进说明：早期已经有 Agent、外部连接器与 API；紫色表示当前重点扩展，并非这些概念首次出现。',20,INK,True)
text(48,1330,'依据：2025-08-29 README（57d7c1c）与研究版本 README / 源码（3448772）。箭头为概念数据流，非逐行调用图。',18,MUTED)
text(48,1364,'2026-09-10 整理 · 独立架构解释 · 未运行原始服务或验证生成效果',17,MUTED)
svg.append('</svg>')
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'architecture.svg').write_text('\n'.join(svg),encoding='utf-8')
im.save(OUT/'architecture.png')
print('Rendered architecture.svg and architecture.png')
