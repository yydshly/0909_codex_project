"""Build the original Chinese study page and its SVG overview; stdlib only."""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
WEB.mkdir(exist_ok=True)
(WEB / 'assets').mkdir(exist_ok=True)
SUMMARY = 'Hugging Face 的 Agent 开发课程与示例集：通过模型决策、工具执行和反馈循环，结合检索增强与状态编排，讲解 smolagents、LlamaIndex、LangGraph 的实现；适合学习工具调用、构建知识问答与多步骤任务原型，并通过评估改进效果。'
PANELS = [
 ('01', '理解任务', '模型与输入', [
  ('LLM', '理解需求，生成回答或动作'), ('Messages', '组织用户、模型与工具消息'),
  ('System Prompt', '说明目标、规则和工具用法'), ('Chat Template', '转换为模型所需的对话格式'), ('Special Tokens', '标识角色、消息及调用边界')]),
 ('02', '决策与执行', 'Agent 核心循环', [
  ('ReAct', '交替决策、行动并观察结果'), ('Tool / Function Calling', '生成工具名和参数，由程序调用'),
  ('Tools', '封装函数、搜索与外部 API'), ('Code Execution', '运行模型生成的代码'), ('Memory / Context', '保留执行记录和任务上下文')]),
 ('03', '检索知识', '外部资料与回答', [
  ('Chunking / Embedding', '文档分块，再转换为语义向量'), ('Index / Retriever', '建立索引，检索相关内容'),
  ('RAG', '将检索资料交给模型辅助回答'), ('Agentic RAG', '按任务选择检索和其他工具'), ('QueryEngine', 'LlamaIndex 的查询与回答组件')]),
 ('04', '框架实现', '三条可选开发路径', [
  ('smolagents', 'CodeAgent：用 Python 表达动作'), ('ToolCallingAgent / @tool', '结构化调用 / 注册自定义工具'),
  ('LlamaIndex', '数据接入、索引、查询与工作流'), ('LangGraph', 'State / Nodes / Edges：状态与流程'), ('Workflows', '组织步骤、事件和执行逻辑')]),
 ('05', '组合与实战', '课程展示的应用方向', [
  ('Multi-Agent Systems', '多个 Agent 分工并汇总结果'), ('VLM / Vision Agents', '理解图片和页面截图'),
  ('Browser Agents', '结合浏览器工具与网页交互'), ('Agentic RAG 实战', '综合资料检索与外部工具回答'), ('Pokémon Agent', '在回合制对战中选择行动')]),
 ('06', '观测与改进', '运行评估与可选训练', [
  ('Observability / Tracing', '查看调用过程、结果和错误'), ('OpenTelemetry', '采集和传递运行追踪数据'),
  ('Token Usage / Latency', '观察模型用量与执行耗时'), ('GAIA / LLM-as-a-judge', '基准任务评测 / 模型辅助评分'), ('LoRA', '用于工具调用微调的低秩适配')]),
]
SOURCES = [
 ('仓库目录与定位', 'https://github.com/huggingface/agents-course'),
 ('Agent 的决策—行动—观察循环', 'https://huggingface.co/learn/agents-course/en/unit1/agent-steps-and-structure'),
 ('smolagents 能力与模块', 'https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction'),
 ('CodeAgent 执行机制与代码', 'https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents'),
 ('LlamaIndex 数据与检索组件', 'https://huggingface.co/learn/agents-course/en/unit2/llama-index/components'),
 ('LangGraph 状态与流程结构', 'https://huggingface.co/learn/agents-course/en/unit2/langgraph/building_blocks'),
 ('Agentic RAG 原理与实战', 'https://huggingface.co/learn/agents-course/en/unit3/agentic-rag/agentic-rag'),
 ('GAIA 子集最终项目', 'https://huggingface.co/learn/agents-course/en/unit4/introduction'),
 ('观测与评估', 'https://huggingface.co/learn/agents-course/bonus-unit2/introduction'),
 ('工具调用微调', 'https://huggingface.co/learn/agents-course/bonus-unit1/introduction'),
 ('Pokémon 游戏 Agent', 'https://huggingface.co/learn/agents-course/bonus-unit3/introduction'),
]
SCENARIOS = [
 ('知识问答', '检索产品手册与故障记录，解释问题并列出依据。', 'RAG + 检索工具', '接入资料、权限过滤、来源引用'),
 ('资料调研', '搜索网页，阅读多个来源并整理比较结果。', '搜索 + 网页读取 + 工具循环', '来源核验、抓取适配、结果格式'),
 ('数据分析', '查询订单数据，计算指标并解释变化。', '数据工具 + CodeAgent', '业务数据接口、计算校验、运行隔离'),
 ('客服与文档流程', '识别请求、查询记录、生成回复草稿并转交审核。', '状态编排 + 工具调用', '业务规则、人工审核、失败恢复'),
]
LEARNING = [
 ('1', '理解循环', 'Unit 1', '解释一次“模型 → 工具 → 反馈”完整过程。'),
 ('2', '实现工具', 'Unit 2 · 先选一个框架', '独立接入一个工具，验证参数和失败处理。'),
 ('3', '接入资料', 'Unit 3', '完成带来源的知识问答，检验检索是否命中。'),
 ('4', '评估再扩展', 'Unit 4 + Bonus', '固定一组真实任务，记录完成率、耗时和用量。'),
]
cards = ''.join('<article class="map-card"><div class="card-top"><span class="number">'+n+'</span><h3>'+title+'</h3><span class="kind">'+kind+'</span></div><dl>'+''.join('<div><dt>'+e(term)+'</dt><dd>'+e(desc)+'</dd></div>' for term,desc in rows)+'</dl></article>' for n,title,kind,rows in PANELS)
source_links = ''.join('<li><a href="'+url+'">'+title+' ↗</a></li>' for title,url in SOURCES)
page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="'''+SUMMARY+'''">
<title>Agents Course · 能力、原理与应用 | 项目研究室</title><link rel="stylesheet" href="./style.css"></head>
<body><header class="topbar"><a href="../../">项目研究室 <span>/ 009</span></a><nav aria-label="页内导航"><a href="#overview">一页总览</a><a href="#principle">技术原理</a><a href="#scenarios">使用场景</a><a href="#learning">学习路径</a><a href="https://github.com/huggingface/agents-course">源库 ↗</a></nav></header>
<main><section class="hero"><p class="eyebrow">HUGGING FACE / AGENTS COURSE</p><h1>从理解 Agent，到构建任务原型。</h1><p class="intro">'''+SUMMARY+'''</p></section>
<section id="overview" class="overview" aria-labelledby="map-title"><div class="section-head"><div><h2 id="map-title">一页看懂技术能力</h2><p>上排：运行机制与数据基础　／　下排：开发路径、应用与改进</p></div><div class="actions"><a href="./assets/overview.svg" download>下载总览图</a><button id="print" type="button">打印总览</button></div></div>
<div class="map-grid">'''+cards+'''</div><div class="map-note"><strong>定位：</strong>课程与示例集合。三个框架按需选用；Memory 指任务上下文，长期记忆需另行设计；微调属于可选进阶。</div></section>
<section id="principle" class="detail"><div class="section-head"><h2>技术原理：模型决策，程序执行，反馈驱动下一步</h2><span>Unit 1–3</span></div>
<div class="cycle" aria-label="Agent 执行循环"><span>用户任务</span><i>→</i><span>模型选择动作</span><i>→</i><span>程序执行工具或代码</span><i>→</i><span>结果写入上下文</span><i>↩</i></div>
<p>模型读取任务、工具说明和历史结果，输出调用请求或代码。框架解析并执行，将结果或错误交还给模型；模型据此继续行动或输出答案。循环还需要结束条件、步数上限与错误处理。循环本身不保证任务正确完成。</p>
<div class="explain-grid"><article><h3>资料怎样进入回答？</h3><p>RAG 把外部内容检索出来作为上下文。课程介绍文档分块、向量化、索引与查询；具体示例也可使用关键词检索。Agentic RAG 将检索封装成可选择的工具，因此并非每次回答都必须检索。</p></article><article><h3>复杂流程怎样控制？</h3><p>LangGraph 用 State 保存任务信息，以 Nodes 执行操作，以 Edges 决定路径；LlamaIndex Workflows 通过事件组织步骤。固定规则可以控制分支，模型只在需要判断的环节参与。</p></article><article><h3>三个框架怎么选？</h3><p>smolagents 适合先理解代码与工具执行；LlamaIndex 侧重围绕数据构建应用；LangGraph 侧重显式控制流程。能力有重叠，先根据一个任务选一个框架，再做比较。</p></article></div>
<p class="source-inline">原理来源：<a href="'''+SOURCES[1][1]+'''">Agent 循环</a> · <a href="'''+SOURCES[4][1]+'''">检索组件</a> · <a href="'''+SOURCES[5][1]+'''">状态编排</a></p></section>
<section id="scenarios" class="detail"><div class="section-head"><h2>使用场景：从课程能力推导的落地方向</h2><span>需接入自己的数据与工具</span></div><div class="scenario-grid">'''+''.join('<article><h3>'+title+'</h3><p>'+task+'</p><dl><dt>技术组合</dt><dd>'+tech+'</dd><dt>落地补充</dt><dd>'+extra+'</dd></dl></article>' for title,task,tech,extra in SCENARIOS)+'''</div><p class="note">这些是可以基于课程构建的业务原型，并非仓库开箱即用的产品。最直接的用途是学习、框架比较与技术验证；步骤固定的任务可以先采用普通程序或固定工作流。</p></section>
<section id="learning" class="detail"><div class="section-head"><h2>学习路径：用一个小项目贯穿练习</h2><span>示例目标：带来源的资料问答助手</span></div><ol class="learning">'''+''.join('<li><span>'+n+'</span><div><h3>'+title+'</h3><small>'+unit+'</small><p>'+outcome+'</p></div></li>' for n,title,unit,outcome in LEARNING)+'''</ol><p class="note">再按需求扩展多 Agent、视觉与浏览器操作、跨会话记忆、混合检索和任务恢复。上述工程扩展属于建议；完成基础应用不要求先微调模型。</p></section>
<section id="sources" class="detail sources"><h2>来源与理解边界</h2><p>基于仓库 README、官方课程与页面内示例代码整理。上游快照：<a href="https://github.com/huggingface/agents-course/tree/8c0832eae634ebb34541c65265caa6da4c5d2c57">8c0832e · 2026-06-28</a>；核对日期：2026-09-09。本次验证的是研究网页与发布构建，未运行上游全部模型示例，也未以 GAIA 实测 Agent 能力。</p><ul>'''+source_links+'''</ul><p>GAIA 是评测基准（最终项目使用其子集）；LLM-as-a-judge 是辅助评估方法；OpenTelemetry 属于可观测性标准与工具生态；LoRA 是微调方法，SFTTrainer 是训练实现工具。名称相邻不表示能力等价。</p></section>
</main><footer>原创中文研究整理 · 上游资料归原作者所有 · <a href="https://github.com/yydshly/0909_codex_project/tree/main/projects/009-agents-course">研究记录与网页源码 ↗</a></footer><script>document.getElementById('print').addEventListener('click',()=>window.print());</script></body></html>'''
(WEB / 'index.html').write_text(page, encoding='utf-8')

# Original vector overview: explicit text, no embedded HTML or external renderer.
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="880" viewBox="0 0 1440 880" role="img" aria-labelledby="title desc"><title id="title">Agents Course 技术能力总览</title><desc id="desc">模型基础、Agent 执行、检索知识、框架实现、组合实战、观测与改进六个板块。</desc><rect width="1440" height="880" fill="#f5f7f8"/><g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" fill="#183339">']
def text(x,y,value,size=18,weight='400',color='#183339'):
    svg.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{e(value)}</text>')
text(40,48,'HUGGING FACE / AGENTS COURSE',17,'600','#526d71')
text(40,94,'Agent 开发课程：能力、原理与应用',34,'600')
text(40,128,'通过模型决策、工具执行与反馈循环，学习构建知识问答和多步骤任务原型。',20)
for i,(num,title,kind,rows) in enumerate(PANELS):
    x=40+(i%3)*458; y=158+(i//3)*318
    svg.append(f'<rect x="{x}" y="{y}" width="444" height="302" rx="12" fill="#ffffff" stroke="#cfdddf"/>')
    text(x+18,y+35,num+'  '+title,23,'600')
    text(x+18,y+60,kind,16,'400','#526d71')
    for j,(term,desc) in enumerate(rows):
        text(x+18,y+92+j*41,term,18,'600')
        text(x+18,y+112+j*41,desc,17)
text(40,827,'定位：课程与示例集合；框架按需选用；Memory 指任务上下文；微调为可选进阶。',18)
text(40,856,'来源：github.com/huggingface/agents-course · 官方课程与示例 · 核对日期 2026-09-09',16,'400','#526d71')
svg.append('</g></svg>')
(WEB / 'assets/overview.svg').write_text(''.join(svg),encoding='utf-8')

readme = '# 009 · Hugging Face Agent 开发课程\n\n'+SUMMARY+'\n\n[在线研究页](https://yydshly.github.io/0909_codex_project/projects/009-agents-course/) · [上游仓库](https://github.com/huggingface/agents-course) · [返回研究室](../../README.md)\n\n![Agent 课程能力与技术总览](web/assets/overview.svg)\n\n## 我们对仓库的理解\n\n这是一套 Agent 教学资料、示例代码与实践项目，提供理解机制、选择框架和开发原型的路径。运行能力由所选模型、工具和框架共同实现；下载课程不等于获得完整业务应用。\n\n## 能力与技术词\n\n'
for n,title,kind,rows in PANELS:
    readme += '### '+n+' · '+title+'\n\n'+'\n'.join('- **'+term+'**：'+desc+'。' for term,desc in rows)+'\n\n'
readme += '## 技术原理\n\n任务、工具说明和历史结果交给模型 → 模型生成工具名与参数或代码 → 框架解析并执行 → 结果写回上下文 → 继续调用或给出答案。执行环境负责真实动作，循环需要结束条件、步数上限与错误处理。\n\nRAG 将外部资料检索后提供给模型；Agentic RAG 让检索成为可选工具。检索可以基于关键词或向量，并非所有检索都依赖向量数据库。LangGraph 使用状态、节点和边组织流程；LlamaIndex 提供数据与事件驱动工作流组件。三个框架不要求同时使用。\n\n## 使用场景\n\n'
for title,task,tech,extra in SCENARIOS:
    readme += '- **'+title+'**：'+task+' 使用 '+tech+'；实际业务还需'+extra+'。\n'
readme += '\n以上业务应用是根据课程能力推导的开发方向，不是仓库已经交付的产品。直接用途为学习、框架比较和技术验证。\n\n## 学习与扩展\n\n'
for n,title,unit,outcome in LEARNING:
    readme += n+'. **'+title+'（'+unit+'）**：'+outcome+'\n'
readme += '\n可按需要继续学习多 Agent、视觉与浏览器交互和微调；业务系统需进一步设计资料权限、长期记忆、任务恢复、评估数据与成本控制。这些属于扩展建议。\n\n## 术语边界\n\n- Memory / Context：这里指运行记录与任务上下文，不承诺长期记忆。\n- GAIA：评测基准；课程最终项目使用其子集。\n- OpenTelemetry：可观测性标准与工具生态，不是评分模型。\n- LLM-as-a-judge：模型辅助评估方法，不能替代全部人工与业务校验。\n- LoRA：微调方法；SFTTrainer：训练工具，二者不属于应用能力。\n\n## 来源与验证范围\n\n上游快照：[8c0832eae634ebb34541c65265caa6da4c5d2c57](https://github.com/huggingface/agents-course/tree/8c0832eae634ebb34541c65265caa6da4c5d2c57)，提交日期 2026-06-28；资料核对日期 2026-09-09。研究状态：已整理。\n\n本次阅读官方课程和示例代码，验证研究网页、导航与静态构建；没有运行全部上游模型示例或 GAIA 实验。图为原创研究说明图，不是上游产品截图。\n\n'+'\n'.join('- ['+title+']('+url+')' for title,url in SOURCES)+'\n\n## 页面维护\n\n网页不依赖外部脚本或字体。修改 `experiments/build_page.py` 后执行该脚本可同步生成网页正文、SVG 总览和本研究记录；样式位于 `web/style.css`。\n'
(ROOT / 'README.md').write_text(readme,encoding='utf-8')
catalog_path=ROOT.parents[1] / 'registry/projects.json'
catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
record=dict(id=9,slug='agents-course',order=90,name='Hugging Face Agent 开发课程',source=SOURCES[0][1],summary=SUMMARY,status='已整理',tags=['Agent 教程','工具调用','检索增强','工作流编排'],cover='web/assets/overview.svg',demo=True)
existing=[p for p in catalog['projects'] if p['id']==9 or p['slug']=='agents-course']
assert not existing or (len(existing)==1 and existing[0]['slug']=='agents-course')
catalog['projects']=[p for p in catalog['projects'] if p['slug']!='agents-course']+[record]
catalog['nextId']=max(catalog['nextId'],10)
catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Generated study page, overview, README and registry entry.')
