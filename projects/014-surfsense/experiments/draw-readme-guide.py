"""Detailed SVG/PNG architecture guide for review."""
from pathlib import Path
from html import escape
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parents[1]/'web/assets'
W,H=2400,2680
BG,INK,MUTED='#f4f7fb','#163449','#526a7a'
TEAL,BLUE,PURPLE,AMBER='#087b76','#295fbd','#7851ac','#9a651d'
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">','<title id="title">SurfSense 资料、索引与 RAG 技术全景</title>','<desc id="desc">入库时解析、切块并保存原文、向量和全文表示；查询时混合召回、融合、可选重排，取回原文组装上下文并生成。侧栏解释概念与通用扩展，底部说明维护、验证和备考建议。</desc>',f'<rect width="{W}" height="{H}" fill="{BG}"/>']
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc' if b else 'C:/Windows/Fonts/msyh.ttc',n)
def box(x,y,w,h,fill='#ffffff',stroke='#cfdee8',r=17):
    d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def txt(x,y,s,n=26,c=INK,b=False):
    f=font(n,b);assert x+d.textlength(s,font=f)<=W-40,(s,'page width')
    d.text((x,y),s,font=f,fill=c)
    svg.append(f'<text x="{x}" y="{y+f.getmetrics()[0]}" fill="{c}" font-family="Microsoft YaHei,Segoe UI,sans-serif" font-size="{n}" font-weight="{700 if b else 400}">{escape(s)}</text>')
def wrap(s,width,n=25):
    lines=[];line=''
    for ch in s:
        if d.textlength(line+ch,font=font(n))>width:lines.append(line);line=ch
        else:line+=ch
    if line:lines.append(line)
    return lines
def card(x,y,w,h,title,lines,c=TEAL,fill='#ffffff'):
    box(x,y,w,h,fill);assert d.textlength(title,font=font(29,True))<=w-40,title
    txt(x+20,y+18,title,29,c,True);yy=y+70
    for s in lines:
        for line in wrap(s,w-40):
            assert yy+35<=y+h,(title,line,'height')
            txt(x+20,yy,line,25,MUTED);yy+=37
def arrow(points,c=TEAL):
    d.line(points,fill=c,width=3)
    svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" stroke="{c}" stroke-width="3" fill="none"/>')
    x,y=points[-1];px,py=points[-2]
    tri=[(x,y),(x-11,y-6),(x-11,y+6)] if x>px else [(x,y),(x+11,y-6),(x+11,y+6)] if x<px else [(x,y),(x-6,y-11),(x+6,y-11)] if y>py else [(x,y),(x-6,y+11),(x+6,y+11)]
    d.polygon(tri,fill=c);svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in tri)+f'" fill="{c}"/>')
def section(y,n,title,sub,c=TEAL):
    txt(65,y,n,31,c,True);txt(128,y,title,31,c,True);txt(65,y+48,sub,24,MUTED)

txt(60,30,'SURFSENSE  /  TECHNICAL READING MAP  /  V2',22,TEAL,True)
txt(60,80,'从多格式资料，到可检索知识，再到有依据的生成',49,INK,True)
txt(60,152,'核心问题：资料如何变成模型能用的证据？关键是保留内容、建立查找能力、按问题组织上下文。',27,MUTED)
for x,c,s in [(60,TEAL,'绿色：资料入库'),(450,BLUE,'蓝色：检索与生成'),(900,PURPLE,'紫色：通用方案 / 建议扩展')]:
    box(x,215,16,16,c,c,4);txt(x+28,207,s,23,c,True)
txt(1630,207,'主流程按已核对代码概括；不是完整调用时序',23,MUTED)
section(285,'01','资料入库 · 新增或更新时执行','解析和切分后的片段，同时服务于语义查找、全文查找和原文回取。')
xs=[65,490,915,1340]
items=[('来源与采集',['文件 / 网盘 / 本地资料','网页与平台连接器','PDF、Office、图片、音频','来源与支持范围依配置']),('按格式解析',['文本：直接读取或转换','文档：Docling 等适配器','扫描文字：OCR','音频：STT；图片可加描述']),('统一内容与结构',['输出 Markdown 等文本','保留可提取的标题与表格','携带文档及来源信息','复杂内容需检查解析质量']),('切块 · Chunking',['长文拆为可检索片段','保留文档关联与文本顺序','处理 Markdown 表格完整性','切太小缺语境，太大有噪声'])]
for x,(t,ls) in zip(xs,items):card(x,380,380,235,t,ls)
for x in xs[:-1]:arrow([(x+380,495),(x+425,495)])
arrow([(1530,615),(1530,648),(340,648),(340,705)])
arrow([(890,648),(890,705)]);arrow([(1440,648),(1440,705)])
txt(65,660,'同一片段，三种用途',24,TEAL,True)
card(65,705,530,205,'A  内容存储：保留证据',['保存片段原文 + 文档 / 片段 ID','通过来源关联支持回溯与引用','示意：{ id, text, document_id, position }'])
card(625,705,530,205,'B  Embedding：语义表示',['片段文本 → 编码模型 → 数值向量','向量与片段关联，存入 pgvector','示意：[0.12, -0.38, …]，不是原文编码表'])
card(1185,705,535,205,'C  全文查询：词项表示',['文本 → 分词 / 规范化 → tsvector','问题词项与内容词项进行匹配','PostgreSQL 排序：ts_rank_cd'])
txt(65,933,'缓存与增量：复用未变化的解析 / 向量结果；更换编码模型时，需要相应重建或迁移语义索引。',24,MUTED)
section(997,'02','检索与生成 · 每次提问时执行','候选 ID / 分数用于选择资料；进入生成模型的主要是筛选后的原文与来源。',BLUE)
card(65,1090,380,245,'问题与范围',['输入问题文本','限定工作区及所选资料','问题用兼容的模型编码','得到问题向量和全文查询'],BLUE)
box(490,1090,805,245);txt(510,1108,'双路初步检索 · 找出候选资料',29,BLUE,True)
for yy,s in [(1170,'语义路：问题向量与片段向量（对应 B）'),(1208,'pgvector 余弦距离，找到含义相近的候选'),(1254,'全文路：问题词项与内容词项（对应 C）'),(1292,'PostgreSQL 全文排序，补充字面匹配')]:txt(510,yy,s,25,MUTED)
card(1340,1090,380,245,'融合 · RRF',['按各路名次融合候选','Σ 1 / (60 + rank)','不直接相加不同尺度分数','保留命中片段与文档关联'],BLUE)
arrow([(445,1210),(490,1210)],BLUE);arrow([(1295,1210),(1340,1210)],BLUE)
arrow([(1530,1335),(1530,1370),(255,1370),(255,1410)],BLUE)
card(65,1410,380,245,'可选重排 · Reranker',['问题 + 候选内容 → 分数','重新判断能否帮助回答','未配置时保持检索结果','首轮漏掉的证据无法凭空补回'],BLUE)
card(490,1410,805,245,'取回原文 → 组装模型上下文',['从内容存储 A 取回原文，附上可追溯的来源标识','输入：任务要求 + 问题 + 相关原文 + 引用标识','通用优化：去重、补齐相邻语境、控制 Token 预算','Token 是输入长度单位，要为历史与输出预留空间'],BLUE)
card(1340,1410,380,245,'生成大模型 · LLM',['阅读问题与证据原文','进行解释、比较和归纳','生成回答并关联引用','有引用仍需核对事实与归纳'],BLUE)
arrow([(445,1530),(490,1530)],BLUE);arrow([(1295,1530),(1340,1530)],BLUE)
txt(65,1678,'RAG = 检索 → 上下文组装 → 基于资料生成；不限于向量检索，也不等于把资料训练进模型参数。',24,BLUE,True)
section(1745,'03','成果与 Agent · 模型生成，工具执行','研究内容可以呈现为多种形式；Agent、API 与 MCP 组织外部能力的调用。',BLUE)
card(65,1840,805,215,'内容生成与呈现',['引用问答 / 报告 / 文档 / 表格 / 演示等研究成果','播客：资料与要求 → 脚本 → TTS 配音 → 音频','不同成果走不同生成路径，不是一次问答的固定后处理'],BLUE)
card(915,1840,805,215,'研究控制与接入',['Agent 按任务调用检索、平台连接器或其他工具','REST / MCP 对外提供能力，也可接入外部 MCP 工具','定时或事件触发研究；权限与服务配置决定可用范围'],BLUE)

card(1790,285,550,220,'Embedding · 表示内容',['输入：片段 / 问题文本','输出：数值向量，帮助比较语义','不是答案，也不能可靠还原原文','编码空间必须兼容；语言与领域影响效果'])
card(1790,530,550,220,'索引 · 加速查找',['原文之外的查找结构','倒排索引：词 → 出现位置 / 片段','向量索引：加速查找相近向量','数据库负责保存、过滤和查询'])
card(1790,765,550,220,'RAG · 使用外部证据',['Retrieve：检索相关资料','Augment：资料加入模型上下文','Generate：模型据此生成','通常不修改生成模型的参数'],BLUE)
card(1790,1000,550,330,'常见扩展 · 不推断已启用',['BM25：词项相关性排序','HNSW / IVF：向量搜索加速','查询改写 / 拆解：改善问题表达','父子块：小块定位，大块补语境','这里是技术选项，不是部署清单','SurfSense 路径用 ts_rank_cd，不能直接称为 BM25'],PURPLE,'#f8f5fc')
card(1790,1350,550,265,'例子 · 措辞不同也能查找',['问题：“植物如何用阳光制造养分？”','教材：“光合作用利用光能……”','Embedding 帮助判断语义相关','检索取回教材原文；LLM 再作解释','向量相近 ≠ 内容正确或证据充分'],BLUE)
card(1790,1640,550,255,'实现与数据边界',['核对的全文路径使用 english 配置','中文分词与检索效果需实际验证','来源定位取决于解析与关联信息','不保证任何格式都无损保留','自部署的数据流向取决于服务配置'],AMBER,'#fffbf3')
card(1790,1905,550,150,'图的阅读范围',['绿色 / 蓝色按代码概括主链路','紫色及“通用优化”为建议方案'],MUTED)
section(2110,'04','更新与验证 · 让结果可持续使用','已有缓存 / 增量机制可以复用计算；下列评估方式建议使用真实资料执行。',PURPLE)
card(65,2200,710,200,'数据维护',['源内容变化 → 识别变化 → 更新片段与向量','内容删除 / 权限变化 → 验证检索结果同步变化','索引版本应与解析、切分、编码配置对应'],PURPLE,'#f8f5fc')
card(810,2200,710,200,'三段质量检查',['初步检索：正确证据是否进入候选集？','上下文：证据是否保留、条件是否完整？','生成：结论是否忠于证据，引用是否对应？'],PURPLE,'#f8f5fc')
card(1555,2200,785,200,'速度与成本',['初次入库：OCR / 视觉 / 转写 / Embedding','每次提问：初步检索 / 可选重排 / LLM 生成','分别观察耗时、调用成本与覆盖率，避免只换模型'],PURPLE,'#f8f5fc')
box(65,2430,2275,150,'#eee8f7','#d6c8e8')
txt(88,2447,'备考应用 · 建议扩展，尚未实现',28,PURPLE,True)
txt(88,2495,'考纲拆解 → 逐项匹配资料与查漏 → 分层讲解 → 出题评分 → 错题反馈 → 复习安排',31,INK,True)
txt(88,2540,'相关性检索不等于全量覆盖；备考系统还需要学习进度、题目质量与掌握程度的验证。',24,MUTED)
txt(65,2603,'研究基线：SurfSense 3448772 · 2026-09-10 · 来源与解释见 notes/understanding.md',21,MUTED)
txt(65,2640,'本地展示未运行上游后端；本图是原理与能力分工说明，未声称已完成质量、速度或权限实测。',21,MUTED)
svg.append('</svg>');(OUT/'readme-guide.svg').write_text('\n'.join(svg),encoding='utf-8');im.save(OUT/'readme-guide.png')
print(f'Generated {W} x {H} PNG and SVG')
