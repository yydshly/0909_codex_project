"""Original technical component diagram, rendered to SVG and PNG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'web/assets'
W, H = 2080, 1740
im = Image.new('RGB', (W,H), '#f4f7f9')
draw = ImageDraw.Draw(im)
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">', '<title id="title">SurfSense 技术实现架构：解析、模型、数据、检索与工具</title>', '<desc id="desc">左侧展示多格式分派、解析器适配、EtlResult 统一接口、片段索引、pgvector 混合检索和 LLM 生成。右侧展示 Agent 控制、平台采集与双向 MCP 接入，以及缓存和增量处理。不同颜色区分程序与数据库、模型推理和工具扩展。</desc>',f'<rect width="{W}" height="{H}" fill="#f4f7f9"/>']
INK='#173749'; MUTED='#506c7c'; TEAL='#006e78'; BLUE='#2358a1'; PURPLE='#6947a3'

def rect(x,y,w,h,fill,stroke=None,r=12):
    draw.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')

def text(x,y,value,size=22,color=INK,bold=False):
    font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if bold else 'C:/Windows/Fonts/msyh.ttc',size)
    draw.text((x,y),value,font=font,fill=color)
    parts.append(f'<text x="{x}" y="{y+font.getmetrics()[0]}" fill="{color}" font-family="Microsoft YaHei,Segoe UI,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(value)}</text>')

def arrow(points,color=TEAL):
    draw.line(points,fill=color,width=3)
    parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="3"/>')
    x,y=points[-1]; px,py=points[-2]
    tri=([(x,y),(x-11,y-5),(x-11,y+5)] if x>px else [(x,y),(x+11,y-5),(x+11,y+5)] if x<px else [(x,y),(x-5,y-11),(x+5,y-11)] if y>py else [(x,y),(x-5,y+11),(x+5,y+11)])
    draw.polygon(tri,fill=color)
    parts.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in tri)+f'" fill="{color}"/>')

def label(x,y,w,title,color=TEAL):
    rect(x,y,5,29,color,r=2)
    text(x+18,y-3,title,26,color,True)

def node(x,y,w,h,title,lines,color=TEAL):
    rect(x,y,w,h,'#ffffff','#cbdce5')
    text(x+20,y+15,title,25,color,True)
    for i,line in enumerate(lines):text(x+20,y+62+i*34,line,21,MUTED)

text(45,28,'SURFSENSE / TECHNICAL ARCHITECTURE',20,TEAL,True)
text(45,73,'一张图看懂：多格式资料如何变成可查询、可生成的知识',44,INK,True)
text(45,140,'技术分工：程序处理格式与数据，专用模型识别和编码，大模型生成内容，Agent 组织工具调用。',24,MUTED)
for x,c,t in [(45,TEAL,'程序 / 数据库'),(350,BLUE,'模型推理'),(625,PURPLE,'工具与后续扩展')]:
    rect(x,192,17,17,c,r=4);text(x+29,185,t,20,c)
text(1450,185,'按代码组件整理 · 非接口调用时序图',20,MUTED)

# A. Parser adapters and their actual implementation seams.
rect(40,237,1320,456,'#eaf3f4','#c6dce0',18)
label(65,257,1260,'A / 多格式能力 = 类型分派 + 解析器适配 + 统一返回接口')
rect(65,310,1270,55,'#d7e9ec',r=8)
text(85,321,'输入：TXT / Markdown / CSV / HTML / PDF / Office / 图片 / 音频等（支持范围依解析配置）',22)
node(65,395,320,265,'类型分派 · 普通程序',[
    'classify_file(filename)',
    'EtlPipelineService.extract()',
    '按文件类别和 ETL_SERVICE',
    '选择处理函数与解析后端',
    '检查不支持格式 / 处理失败'
])
node(420,395,565,265,'解析器适配 · 专用能力',[
    'TXT → 文本读取；CSV → Python csv',
    'HTML → markdownify',
    'PDF / Office → Docling 等解析服务',
    '扫描文字 → OCR；图形含义 → 视觉模型',
    '音频 → 本地 STT / LiteLLM atranscription'
])
node(1020,395,315,265,'统一对象 · EtlResult',[
    'markdown_content',
    'etl_service',
    'actual_pages / content_type',
    'Pydantic 定义返回结构',
    '下游统一消费文本内容'
])
arrow([(385,518),(420,518)]);arrow([(985,518),(1020,518)])

# B. Materialized representation used for retrieval.
arrow([(1170,660),(1170,726),(228,726),(228,759)])
rect(440,707,515,34,'#f4f7f9',r=3)
text(452,710,'可选视觉增强：图片 → 描述 → 插回正文',20,BLUE)
rect(40,759,1320,249,'#eaf3f4','#c6dce0',18)
label(65,779,1260,'B / 知识库能力 = 文本切分 + 向量编码 + 关联存储')
node(65,826,320,151,'Chunker · 普通程序',[
    '切分片段 / 保留顺序与来源',
    'Markdown 表格做完整性处理'
])
node(420,826,345,151,'Embedding · 编码模型',[
    '输入文本 → 输出数值向量',
    '表达语义相似性，不写答案'
],BLUE)
node(800,826,535,151,'PostgreSQL + pgvector',[
    'Document：标题 / 来源 / workspace',
    'Chunk：正文 / document_id / 位置 / 向量'
])
arrow([(385,900),(420,900)]);arrow([(765,900),(800,900)])

# C. Query-time algorithms and grounded generation.
rect(40,1064,1320,413,'#edf3fa','#c7d7e8',18)
label(65,1084,1260,'C / 问答与生成能力 = 查询计算 + 证据上下文 + 生成模型',BLUE)
node(65,1138,240,190,'研究问题',[
    '问题文本',
    '资料范围 / 工作区',
    '会话上下文'
])
node(340,1138,485,190,'混合检索 + 可选重排序',[
    '问题 → Embedding → 向量相似度',
    '关键词 → PostgreSQL 全文查询',
    'RRF 融合排名 → 可选 reranker'
])
node(860,1138,475,190,'LLM · 生成模型',[
    '指令 + 问题 + 检索证据 → 回答',
    '根据证据解释、归纳、比较',
    '保留片段 ID，用于关联引用'
],BLUE)
arrow([(305,1230),(340,1230)]);arrow([(825,1230),(860,1230)],BLUE)
arrow([(1070,977),(1070,1040),(580,1040),(580,1064)])
rect(714,1023,210,32,'#f4f7f9',r=3);text(725,1025,'按权限与范围查库',19,TEAL)
arrow([(1100,1328),(1100,1376)],BLUE)
rect(65,1385,1270,66,'#ffffff','#c7d7e8',8)
text(85,1404,'输出：带引用的问答 / 讲义 / 报告；播客 = 内容 → 对话脚本 → TTS；其他成果需相应生成与渲染',20,INK)

# Control and extension plane, distinct from data transformation.
rect(1405,237,635,366,'#173749',r=18)
text(1435,261,'控制层 / Agent 如何组织能力',28,'#a2ece3',True)
text(1435,316,'LangChain / LangGraph / Deep Agents 组件',22,'#ffffff')
text(1435,362,'模型：选择工具并生成调用参数',23,'#ffffff',True)
text(1435,404,'程序：执行解析、检索或外部请求',23,'#ffffff',True)
text(1435,446,'结果：返回模型，决定下一步或完成回答',23,'#ffffff',True)
text(1435,501,'维护指令、会话状态、工具与子 Agent',21,'#b8d0dc')
text(1435,538,'调用左侧能力；并非每一步都需要大模型',21,'#b8d0dc')
rect(1405,633,635,375,'#f0ecf8','#d5cbe6',18)
label(1435,655,565,'扩展层 / 实时数据与双向 MCP',PURPLE)
text(1435,712,'平台采集器',24,PURPLE,True)
text(1435,750,'按平台使用 HTTP / 浏览器 / 代理 / 分页重试',21,MUTED)
text(1435,784,'→ 结构化结果：可直接供研究，或解析索引后入库',21,MUTED)
text(1435,833,'外部 MCP → 把第三方工具接入 SurfSense',22,PURPLE,True)
text(1435,875,'SurfSense MCP → 经 REST 向其他 Agent 提供能力',21,PURPLE,True)
text(1435,930,'定时 / 事件 → 触发 Agent → 摘要或授权写回',21,MUTED)
text(1435,965,'早期已有 Agent、连接器和 API，后来持续强化。',20,MUTED)
rect(1405,1038,635,439,'#ffffff','#cbdce5',18)
label(1435,1058,565,'性能层 / 为什么能复用，哪里仍会慢')
text(1435,1115,'解析缓存',24,TEAL,True)
text(1435,1152,'文件哈希 + 解析配置 → 复用已提取内容',21,MUTED)
text(1435,1194,'向量缓存与增量索引',24,TEAL,True)
text(1435,1231,'内容 / 模型 / 切分配置匹配 → 复用向量',21,MUTED)
text(1435,1265,'新旧片段对比 → 只为新增内容计算向量',21,MUTED)
text(1435,1310,'首次处理仍要付出计算成本',24,BLUE,True)
text(1435,1347,'OCR、逐图视觉推理、长文本生成与语音合成',21,MUTED)
text(1435,1398,'RAG 负责找证据；考点覆盖与教学质量需另行验证。',20,MUTED)

rect(40,1510,2000,120,'#173749',r=16)
for x,t,b in [(65,'交互与服务','Next.js / React / FastAPI'),(570,'模型适配','LiteLLM / 本地与远程模型'),(1075,'数据与后台任务','PostgreSQL / Celery / Redis'),(1580,'访问与部署','工作区授权 / 角色 / Docker')]:
    text(x,1530,t,23,'#a2ece3',True);text(x,1574,b,21,'#ffffff')
text(45,1654,'技术要点：解析器解决格式差异；Embedding 解决语义表示；数据库解决检索；LLM 解决内容生成；Agent 解决工具编排。',22,INK,True)
text(45,1700,'基于 MODSetter/SurfSense 3448772bd3d5 的源码阅读 · 2026-09-10 · 独立技术归纳，省略非核心字段；未运行上游服务。',18,MUTED)
parts.append('</svg>')
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'technical-architecture.svg').write_text('\n'.join(parts),encoding='utf-8')
im.save(OUT/'technical-architecture.png')
print('Rendered technical-architecture.svg and technical-architecture.png')
