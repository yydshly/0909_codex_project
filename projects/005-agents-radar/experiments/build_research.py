"""Build the research page, source inventory and original one-page SVG from shared data."""
from pathlib import Path
from html import escape as E
import json

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
ASSETS = WEB / 'assets'
DOWNLOADS = WEB / 'downloads'
for folder in (ASSETS, DOWNLOADS, ROOT / 'notes'):
    folder.mkdir(parents=True, exist_ok=True)
COMMIT = 'dd2aaae700e2ebf62a7c80557c2bd64709be5e79'
UP = 'https://github.com/duanyytop/agents-radar'
def source(file): return f'{UP}/blob/{COMMIT}/{file}'

REPOS = [
 ('CLI 工具','Claude Code','anthropics/claude-code',''),
 ('CLI 工具','OpenAI Codex','openai/codex','Discussions'),
 ('CLI 工具','Gemini CLI','google-gemini/gemini-cli',''),
 ('CLI 工具','GitHub Copilot CLI','github/copilot-cli',''),
 ('CLI 工具','OpenCode','anomalyco/opencode',''),
 ('CLI 工具','Pi','earendil-works/pi','Discussions'),
 ('CLI 工具','Qwen Code','QwenLM/qwen-code',''),
 ('Agent 项目','OpenClaw','openclaw/openclaw','分页'),
 ('Agent 项目','Hermes Agent','nousresearch/hermes-agent',''),
 ('Agent 项目','IronClaw','nearai/ironclaw',''),
 ('Agent 项目','QwenPaw','agentscope-ai/QwenPaw',''),
 ('Agent 项目','ZeroClaw','zeroclaw-labs/zeroclaw',''),
 ('AI 基础设施','vLLM','vllm-project/vllm','分页'),
 ('AI 基础设施','SGLang','sgl-project/sglang','分页'),
 ('AI 基础设施','llama.cpp','ggml-org/llama.cpp','分页'),
 ('AI 基础设施','Ollama','ollama/ollama',''),
 ('AI 基础设施','LiteLLM','BerriAI/litellm','分页'),
 ('AI 基础设施','Unsloth','unslothai/unsloth','分页'),
 ('Skills','Claude Code Skills','anthropics/skills','独立热度采集'),
]
EXTERNAL = [
 ('公司官网','Anthropic','https://www.anthropic.com/sitemap.xml','Sitemap + HTML 正文','/news/、/research/、/engineering/、/learn/；比较已记录 URL 与 lastmod。','src/web.ts'),
 ('公司官网','OpenAI','https://openai.com/sitemap.xml','Sitemap 元数据','research、publication、release、company、engineering、milestone、learn-guides、safety、product 子 Sitemap；仅发现新 URL，当前不抓正文。','src/web.ts'),
 ('开源发现','GitHub Trending / Search','https://github.com/trending','HTML + REST API','日榜；搜索最近 7 天活跃且匹配 llm、ai-agent、rag、vector-database、large-language-model、machine-learning 的仓库。','src/trending.ts'),
 ('技术社区','Hacker News','https://news.ycombinator.com','官方 Firebase JSON API','读取 topstories，最多扫描前 500 个 ID，按标题和 URL 的 AI 关键词筛选，按榜单次序保留最多 30 条；当前代码没有 24 小时时间过滤。','src/hn.ts'),
 ('技术社区','Dev.to','https://dev.to/api/articles','Forem REST API','并行查询 ai、llm、machinelearning、openai、langchain 五个标签，按 ID 去重。','src/devto.ts'),
 ('技术社区','Lobste.rs','https://lobste.rs','标签 JSON API','https://lobste.rs/t/ai.json 和 /t/ml.json；筛选最近 7 天故事。','src/lobsters.ts'),
 ('学术论文','ArXiv','https://export.arxiv.org/api/query','API / Atom XML','cs.AI、cs.CL、cs.LG；最近 48 小时；最多 50 篇；模型输入为论文标题与摘要片段。','src/arxiv.ts'),
 ('模型平台','Hugging Face','https://huggingface.co/api/models','Hub REST API','按 likes7d 排序，最多 30 个模型；每周一采集并生成报告。','src/hf.ts'),
 ('产品发现','Product Hunt','https://api.producthunt.com/v2/api/graphql','GraphQL API','昨日产品按票数取候选，再按 AI 及相关主题过滤；主题也包括 developer-tools、open-source；需要 PRODUCTHUNT_TOKEN。','src/ph.ts'),
]
MODULES = [
 ('配置与编排','config.yml · src/config.ts · src/index.ts','读取关注仓库；并行采集各来源；安排摘要、翻译、比较、报告保存及发布。'),
 ('来源适配','github.ts · web.ts · trending.ts · hn.ts 等','各自处理 API、HTML 或 XML，返回对应类型的数据；新增平台仍需修改主流程。'),
 ('文本与提示词','prompts.ts · prompts-data.ts','时间与热度筛选多发生在采集器内；这里做 Top N 取样、字段排版、正文截取及分析指令构建。'),
 ('模型与可靠性','report.ts · providers/','统一模型接口、最多 5 路模型并发、连接和限流重试、失败统计、翻译回退。'),
 ('报告组织','report-builders.ts · report-savers.ts · i18n.ts','组装分项目报告与跨项目比较，保存中英双语 Markdown；按数据可用性跳过部分报告。'),
 ('索引与分发','generate-manifest.ts · notify.ts · feishu.ts','生成 manifest 与 RSS，推送 Telegram / 飞书，配合工作流提交文件和维护 Issues。'),
 ('网页与查询','index.html · mcp/src/index.ts','静态网页读取报告；Cloudflare Worker 提供 MCP 读取与关键词搜索接口。'),
]
OUTPUTS = [
 ('ai-cli','CLI 日报','跨工具比较、各工具更新、Skills 热点'),
 ('ai-agents','Agent 生态','OpenClaw 深入报告、同类项目比较'),
 ('ai-infra','基础设施','模型及硬件支持、性能、稳定性、破坏性变更'),
 ('ai-web','官网动态','新增官方内容；无新增则跳过'),
 ('ai-trending','开源趋势','热门仓库分类和趋势信号'),
 ('ai-hn','HN 社区','热点故事和社区观察'),
 ('ai-ph','产品发现','Product Hunt 产品；需 Token 且有可用数据'),
 ('ai-arxiv','论文速览','AI 相关分类的论文摘要'),
 ('ai-hf','模型周报','Hugging Face 模型榜；每周一'),
 ('ai-community','社区合刊','Dev.to 与 Lobste.rs 合并报告'),
]
LIMITS = [
 ('采样信息不等于全文研究','普通 GitHub 仓库单次采集 50 条；分页仓库每页 100 条、最多 5 页。提示词继续按评论数取 Top N，正文通常只保留 300 字符。ArXiv 也仅传入摘要片段。'),
 ('来源覆盖程度不同','Anthropic 正文最多取 1500 字符；OpenAI 为元数据模式，标题来自 URL。官网首次每站最多处理 25 条，并把已发现 URL 记入状态，不构成全站历史归档。'),
 ('趋势结论来自模型归纳','分项目摘要再汇总可能传递遗漏；热度和评论数不能直接代表质量。当前没有独立事实核验、语义去重或长期结构化趋势引擎。'),
 ('MCP 搜索有明确范围','默认搜索近期报告，最多 14 个已收录日期，跳过英文副本和汇总报告；采用字符串匹配，没有向量检索。类型说明中出现的 weekly/monthly 不能据此认定当前流水线会生成周月汇总。'),
 ('执行与发布存在边界','GitHub Actions 调度可能延迟；部分来源失败会降级或跳过。健康门限能减少全量模型故障时的错误产出，但并非所有渠道都具备事务性发布与完整幂等保障。'),
]
EXTENSIONS = [
 ('统一来源配置','把站点地址、查询条件、字段映射和调度频率移入统一配置；定义采集器注册接口。','让新增同类来源从改代码变为改配置。'),
 ('结构化事件与证据','保存原始响应、来源片段、采集时间和标准事件；区分 closed 与 merged 等状态。','为事实校验、去重和历史比较提供基础。'),
 ('个人订阅与告警','设置关注项目、主题与重要事件，增加重复事件抑制与变化检测。','将每日阅读变成只处理与用户相关的变化。'),
 ('长期趋势与语义检索','建立 7 / 30 / 90 天事件序列，加入全文和向量索引，扩展 MCP。','支持跨月比较、语义问答与有证据的趋势回溯。'),
 ('生产运行治理','采集成功率、覆盖率、模型成本、重试状态和发布记录可观测；失败任务可补跑。','让局部失败容易定位，并降低重跑带来的重复发布。'),
]

# One-page diagram. Native vector text, original drawing, no upstream art copied.
W,H=1920,1200
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
 '<title id="title">Agents Radar 一页能力与架构总览</title>',
 '<desc id="desc">左侧列出十九个真实 GitHub 仓库、两家官网及榜单社区论文模型产品来源；沿箭头经过采集适配、筛选与模型分析，最终生成双语报告并通过网页订阅通知和 MCP 分发。</desc>',
 '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#22756a"/></marker></defs>',
 '<style>text{font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif;fill:#18323a} .muted{fill:#587078} .mono{font-family:"Consolas","Microsoft YaHei",monospace} .eyebrow{fill:#22756a;font-weight:700}</style>',
 '<rect width="1920" height="1200" fill="#f4f2eb"/>']
def rect(x,y,w,h,fill='#ffffff',stroke='#d7dfd9',rx=12):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def text(x,y,s,size=20,weight=400,cls=''):
    svg.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" class="{cls}">{E(s)}</text>')
def lines(x,y,items,size=19,gap=29,cls=''):
    for i,s in enumerate(items):text(x,y+i*gap,s,size,cls=cls)
def line(x1,y1,x2,y2,arrow=False):
    svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#22756a" stroke-width="2"'+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
text(48,43,'研究室 005  /  AGENTS RADAR',18,700,'eyebrow')
text(48,100,'多源信息如何成为可订阅的 AI 生态报告',43,700)
text(48,133,'来源设置 → 采集适配 → 规则处理与模型分析 → 双语展示与分发',22,cls='muted')
for x,n,label in [(1320,'19','固定 GitHub 仓库'),(1540,'2','公司官网'),(1700,'6','外部平台')]:
    text(x,79,n,44,700);text(x,111,label,18,cls='muted')
rect(48,165,1824,76,'#e7eee7')
text(70,194,'配置',18,700,'eyebrow');text(132,194,'config.yml：仓库地址 / 分页 / Discussions',21)
text(132,222,'站点栏目、标签与关键词仍配置在各采集模块中',18,cls='muted')
text(740,194,'调度',18,700,'eyebrow');text(802,194,'GitHub Actions + src/index.ts',21)
text(802,222,'每日 06:37 北京时间触发；可手动运行',18,cls='muted')
text(1315,194,'模型',18,700,'eyebrow');text(1377,194,'6 种供应商适配',21)
text(1377,222,'当前工作流选择 Qwen；模型并发上限 5',18,cls='muted')
for x,num,label in [(48,'01','真实来源'),(820,'02','采集适配'),(1137,'03','清洗与分析'),(1509,'04','报告与服务')]:
    text(x,280,num,20,700,'eyebrow');text(x+42,280,label,26,700)
for x,w in [(48,740),(820,285),(1137,340),(1509,363)]:rect(x,301,w,674)
for a,b in [(788,820),(1105,1137),(1477,1509)]:line(a+4,620,b-5,620,True)
line(421,326,421,950)
y=338
for category,label in [('CLI 工具','GitHub CLI 工具 · 7'),('Agent 项目','GitHub Agent 项目 · 5'),('AI 基础设施','GitHub AI 基础设施 · 6'),('Skills','GitHub Skills · 1')]:
    text(70,y,label,20,700);y+=28
    for c,name,repo,flag in REPOS:
        if c==category:text(70,y,repo,18,cls='mono');y+=23
    y+=18
right_groups=[
 ('公司官网 · 2',['anthropic.com','Sitemap + 正文；指定 4 类栏目','openai.com','Sitemap 元数据；指定 9 类栏目']),
 ('GitHub 开源发现',['github.com/trending 日榜','Search API：6 个 AI Topic']),
 ('技术社区 · 3',['Hacker News：AI 相关热门故事','Dev.to：5 个 AI 相关标签','Lobste.rs：AI / ML 标签']),
 ('论文 · 模型 · 产品',['ArXiv：cs.AI / cs.CL / cs.LG','Hugging Face：likes7d 模型榜','Product Hunt：昨日产品票数榜']),
]
y=338
for title,items in right_groups:
    text(442,y,title,20,700);lines(442,y+32,items,18,27);y+=40+len(items)*27+24
text(442,934,'具体地址与筛选规则见详细清单',16,cls='muted')
blocks=[
 ('GitHub API',['REST：Issue / PR / Release','GraphQL：Discussions','Skills：独立热门条目']),
 ('HTML 与 Sitemap',['Trending 榜单页面解析','官网 URL 与 lastmod 状态','Anthropic 正文 / OpenAI 元数据']),
 ('各平台原生接口',['HN：官方 Firebase API','Dev.to / HF：REST API','Lobste.rs：JSON','ArXiv：Atom XML','Product Hunt：GraphQL']),
 ('模块内并行与容错',['按来源返回类型化数据','失败来源降级或跳过']),
]
y=341
for title,items in blocks:
    text(840,y,title,21,700);lines(840,y+33,items,17,28,cls='muted');y+=49+len(items)*28+23
blocks=[
 ('规则筛选',['时间窗口 / AI 关键词匹配','多查询去重 / 热度排序','Top N 抽样']),
 ('文本规整',['提取标题、状态、互动与链接','去标签、脚本和多余空白','GitHub 正文通常截取 300 字符','官网正文最多 1500 字符']),
 ('模型归纳',['分项目摘要 → 跨项目比较','功能变化 / 痛点 / 趋势信号','先英文生成 → 中文翻译','再提取通知亮点']),
 ('运行控制',['限流与连接重试 / 失败统计','翻译失败回退 / 健康门限']),
]
y=341
for title,items in blocks:
    text(1158,y,title,21,700);lines(1158,y+33,items,18,28,cls='muted');y+=48+len(items)*28+21
blocks=[
 ('10 类报告 · 中英双语',['CLI / Agent / 基础设施','官网 / Trending / HN / 产品','论文 / 模型 / 社区合刊','HF 每周一；部分来源按条件产出']),
 ('文件与历史',['按日期保存 Markdown','Git 归档 + 官网增量状态','manifest.json / feed.xml']),
 ('阅读与触达',['GitHub Pages / GitHub Issues','RSS：订阅报告','Telegram / 飞书：亮点与链接']),
 ('MCP 查询服务',['列出 / 最新 / 指定日期报告','近期关键词匹配，最多 14 个日期','Cloudflare Worker 读取静态报告']),
]
y=341
for title,items in blocks:
    text(1530,y,title,21,700);lines(1530,y+33,items,18,28,cls='muted');y+=47+len(items)*28+21
for x,title,items in [
 (48,'可复用的实现',['同类仓库统一适配；不同平台独立采集','后续报告生成、翻译与分发流程共用']),
 (664,'当前边界',['采样与元数据限制分析深度；MCP 为关键词搜索','没有通用来源配置中心、全文核验或长期趋势引擎']),
 (1280,'值得扩展的方向',['统一来源配置 → 结构化事件与证据','个性订阅与告警 → 长期趋势与语义检索']),
]:
    rect(x,1003,592,130,'#eaf0eb');text(x+22,1038,title,22,700);lines(x+22,1074,items,19,29)
text(48,1172,'代码核对版本 dd2aaae · 2026-09-09  |  github.com/duanyytop/agents-radar',17,cls='muted')
text(1270,1172,'HN 按源码使用 Firebase；RSS 是输出渠道',17,cls='muted')
svg.append('</svg>')
(ASSETS/'overview.svg').write_text('\n'.join(svg),encoding='utf-8')

def a(url,label):return f'<a href="{E(url,quote=True)}">{E(label)}</a>'
def table(headers,rows,cls=''):
    return '<div class="table-wrap"><table class="'+cls+'"><thead><tr>'+''.join('<th>'+E(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
repo_table=table(['分类','项目','真实仓库','额外配置'],[(E(c),E(n),a('https://github.com/'+r,r),E(f or '默认')) for c,n,r,f in REPOS])
external_table=table(['来源','采集方式','关注范围与规则'],[(f'<strong>{E(n)}</strong><small>{E(c)}</small>'+a(u,u),E(m),E(rule)+'<small>'+a(source(file),'查看实现')+'</small>') for c,n,u,m,rule,file in EXTERNAL])
external_table=external_table.replace('<table class="">','<table class="external-inventory">')
module_table=table(['模块','代码位置','职责'],[(E(n),f'<code>{E(f)}</code>',E(d)) for n,f,d in MODULES])
output_table=table(['报告标识','类型','内容与产出条件'],[(f'<code>{id}</code>',E(n),E(d)) for id,n,d in OUTPUTS])
extension_table=table(['方向','具体改造','价值'],[(E(n),E(d),E(v)) for n,d,v in EXTENSIONS])
refs=['config.yml','src/index.ts','src/github.ts','src/web.ts','src/trending.ts','src/hn.ts','src/devto.ts','src/lobsters.ts','src/arxiv.ts','src/hf.ts','src/ph.ts','src/prompts.ts','src/prompts-data.ts','src/report.ts','src/providers/index.ts','src/report-builders.ts','src/report-savers.ts','src/generate-manifest.ts','.github/workflows/daily-digest.yml','mcp/src/index.ts']
ref_html='<ol class="references">'+''.join(f'<li>{a(source(f),f)}</li>' for f in refs)+'</ol>'
overview_intro='agents-radar 是一个以 TypeScript 和 Node.js 实现的 AI 生态情报流水线。它定时采集开源项目、公司官网及社区平台的信息，通过规则筛选与大模型归纳生成中英双语报告，再以网页、订阅、通知和 MCP 服务提供给用户。最值得复用的是来源选择、平台适配、文本压缩和统一报告分发。'
architecture_text='GitHub Actions 负责调度，src/index.ts 负责固定流程编排。仓库配置由 config.yml 读取，站点与平台规则分散在各采集模块。采集器返回各自的数据类型，提示词模块将它们整理为模型输入，报告构建与保存模块负责双语内容及文件输出。各平台之间没有统一的动态插件注册机制。'
report_pages=[
 ('Agents Radar 架构与能力研究',f'<p class="lead">{overview_intro}</p><p>研究对象：{a(UP,"duanyytop/agents-radar")}　核对日期：2026-09-09<br/>固定版本：<code>{COMMIT}</code></p><img class="report-overview" src="../assets/overview.svg" alt="完整能力与架构总览"/><h2>核心架构</h2><p>{architecture_text}</p><h2>阅读这份报告</h2><p>先用一页图把握全链路，再查阅完整来源清单、处理与运行规则、报告服务，以及可以复用和扩展的部分。图中的 19 个仓库由 18 个项目仓库和 1 个 Skills 仓库组成；6 个外部平台不包含两家官网和 GitHub 自身。</p>'),
 ('指定 GitHub 来源',f'<p>下表为 config.yml 中的全部 19 个真实仓库。CLI、Agent、基础设施共 18 个项目；Skills 单独采集。仓库地址、显示名称、分页与 Discussions 开关集中配置。</p>{repo_table}<p>默认读取 Issues、PR 与 Release。Codex、Pi 额外读取 Discussions。分页仓库每页 100 条、最多 5 页，普通仓库请求 50 条；这属于采集上限，并非全量覆盖承诺。Skills 不按最近一天过滤，按社区热度获取条目。</p><p>依据：{a(source("config.yml"),"config.yml")} · {a(source("src/github.ts"),"src/github.ts")}</p>'),
 ('官网与外部平台来源',f'<p>站点、栏目、标签及查询条件配置在对应采集模块中。来源类型并不等同于独立站点数量：同一 GitHub 平台同时承担固定仓库跟踪、Skills 热度和新项目发现。</p>{external_table}<p><strong>源码与说明差异：</strong>README 仍描述 HN 使用 Algolia 查询最近 24 小时故事；当前 hn.ts 使用官方 Firebase 热门榜，并没有该时间窗口。本报告采用源码口径。</p>'),
 ('处理流程与模块职责',f'<p>{architecture_text}</p>{module_table}<h2>执行与成本控制</h2><p>当前工作流北京时间 06:37 触发，目标约 07:00 产出，GitHub 排队可能延迟。原始采集多路并行，模型请求并发上限为 5。英文先生成，中文再翻译，避免双语各自重复输入同一批原始材料。</p><p>模型供应商已适配 Anthropic、OpenAI、GitHub Copilot、OpenRouter、DeepSeek、Qwen；当前工作流指定 Qwen。report.ts 对限流与连接故障进行重试，翻译失败可回退英文；至少 5 次模型调用且失败比例达到 50% 时，健康检查会中止运行。</p><p>这是一条代码控制的固定流程。模型负责摘要和分析，未在主流程中自主规划、选择工具并反复执行任务。</p>'),
 ('报告与用户触达',f'{output_table}<p>每类报告生成中英文文件；英文文件使用 -en 后缀。支持一种报告不意味着每天都会产出：官网无新增、来源不可用、PH 未配置 Token、HF 不在周一时，可能跳过相应报告。</p><h2>存储与展示</h2><p>报告保存到 digests/YYYY-MM-DD/ 并提交 Git；web-state.json 保存官网 URL 状态。目录与 RSS 由 manifest.json 和 feed.xml 提供。GitHub Pages 用于历史阅读，GitHub Issues 发布分类日报，Telegram 与飞书推送亮点及报告链接。RSS 在这里主要是输出订阅渠道。</p><h2>MCP 查询</h2><p>Cloudflare Worker 读取静态报告，提供 list_reports、get_latest、get_report、search。搜索是关键词字符串匹配，最多扫描最近 14 个已收录日期，排除英文副本及汇总报告，不含语义索引。</p><h2>适用场景</h2><p>个人技术晨报、团队工具跟踪、产品需求与竞品观察、开源社区运营、内容选题，以及为其他助手提供近期信息。重大判断仍应回到原始来源核对。</p>'),
 ('能力边界与扩展建议',''.join(f'<h2>{E(n)}</h2><p>{E(d)}</p>' for n,d in LIMITS)+f'<h2>扩展优先级建议</h2>{extension_table}<p>本页扩展方向是研究建议，不属于仓库已经实现的功能。优先统一来源配置和保存结构化证据，再建设告警、趋势与语义查询。</p>'),
 ('源码依据与版本口径',f'<p>源码链接固定到提交 <code>{COMMIT}</code>，避免主分支后续更新导致对应关系变化。研究图与文字为本研究室原创整理，未复制上游图像。分析来自静态代码检查，没有运行上游采集、模型调用或外部消息发布。</p>{ref_html}<h2>来源统计口径</h2><p>仓库 README 将来源组织为 10 个采集类别：固定 GitHub 项目、Skills、GitHub Trending、HN、PH、ArXiv、HF、Dev.to、Lobste.rs、官方网页。本报告为了展示实现层次，将其归为仓库、官网、开源发现、社区、论文、模型和产品等类型，避免把“来源类别”“站点数量”和“报告种类”混为一谈。</p>'),
]

css='''
:root{--ink:#16333c;--muted:#5c7177;--paper:#f5f3ed;--card:#fffefa;--line:#dce3df;--accent:#226f65;--soft:#e8efea}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--paper);font:16px/1.7 "Microsoft YaHei","Segoe UI",sans-serif}a{color:var(--accent);text-underline-offset:4px}button,input{font:inherit}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #b56b28;outline-offset:4px}.shell{max-width:1440px;margin:auto;padding:0 40px}.top{border-bottom:1px solid var(--line)}.top .shell{display:flex;justify-content:space-between;align-items:center;gap:20px;padding-top:18px;padding-bottom:18px}.brand{font-weight:700;text-decoration:none}.top nav{display:flex;gap:24px}.top nav a{text-decoration:none;color:var(--muted);font-size:14px}.hero{padding:56px 0 28px;display:grid;grid-template-columns:1.3fr 1fr;gap:64px;align-items:end}.eyebrow{font-size:13px;letter-spacing:1.6px;font-weight:700;color:var(--accent);margin:0 0 16px}h1{font-size:clamp(32px,4vw,55px);line-height:1.17;letter-spacing:-1.5px;margin:0 0 20px}h2{font-size:28px;margin:0 0 18px;line-height:1.35}h3{font-size:19px;margin:0 0 12px}p{margin:0 0 16px}.lead{font-size:18px;color:var(--muted)}.hero-side{border-left:1px solid var(--line);padding-left:30px}.metrics{display:flex;gap:35px;margin-bottom:20px}.metrics strong{display:block;font-size:34px;line-height:1.3}.metrics span{font-size:13px;color:var(--muted)}.actions{display:flex;gap:10px;flex-wrap:wrap}.button{display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid #abc1b8;border-radius:7px;color:var(--accent);padding:9px 15px;text-decoration:none;cursor:pointer;font-size:14px}.button.primary{background:var(--ink);border-color:var(--ink);color:white}.section{padding:42px 0;border-top:1px solid var(--line);scroll-margin-top:20px}.section-head{display:flex;justify-content:space-between;gap:24px;align-items:start}.section-head p{max-width:760px;color:var(--muted)}.overview{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:10px}.figure-link{display:block}.caption{font-size:13px;color:var(--muted);margin-top:12px}.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:24px 0 18px}.toolbar input{padding:11px 15px;border:1px solid #aebeb8;border-radius:6px;background:var(--card);min-width:250px;flex:1}.filters{display:flex;gap:7px;flex-wrap:wrap}.filter{background:transparent;border:1px solid var(--line);border-radius:30px;padding:7px 13px;cursor:pointer;color:var(--ink)}.filter[aria-pressed=true]{background:var(--ink);color:white}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px;text-align:left}th{background:var(--soft);padding:12px 14px;font-weight:700;white-space:nowrap}td{border-bottom:1px solid var(--line);padding:13px 14px;vertical-align:top}td a{overflow-wrap:anywhere}small{display:block;color:var(--muted);font-size:12px;margin-top:4px}code{font:13px/1.6 Consolas,"Microsoft YaHei",monospace;overflow-wrap:anywhere}#source-table td:nth-child(3){min-width:245px}.count{font-size:13px;color:var(--muted)}.stack{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.step{padding:20px 0;border-top:3px solid var(--accent)}.step .number{font-size:13px;letter-spacing:1px;color:var(--accent)}.step p{color:var(--muted);font-size:15px}.source-block{margin-top:36px}.two-col{display:grid;grid-template-columns:1fr 1fr;gap:36px}.boundaries p{font-size:15px;color:var(--muted)}.references{columns:2;font-size:14px;padding-left:23px}.references li{padding:4px 0;break-inside:avoid}.foot{padding:28px 0 44px;font-size:13px;color:var(--muted)}.notice{font-size:14px;color:var(--muted);margin:16px 0 0}.report-overview{width:100%}.report-page{background:white;max-width:210mm;min-height:297mm;margin:24px auto;padding:16mm}.report-page h1{font-size:27px;color:#000;letter-spacing:0;margin:0 0 18px}.report-page h2{font-size:17px;color:#000;margin:18px 0 8px}.report-page p{font-size:13px;line-height:1.75}.report-page table{font-size:11px}.report-page th,.report-page td{padding:6px 8px}.report-page .references{font-size:11px}.report-page .page-label{font-size:11px;color:#555;margin-bottom:14px}.empty{padding:24px;text-align:center;color:var(--muted)}@media(max-width:800px){.shell{padding:0 20px}.hero{grid-template-columns:1fr;gap:24px;padding-top:34px}.hero-side{border-left:0;padding:0}.top nav{gap:13px;flex-wrap:wrap}.top .shell{align-items:start}.stack,.two-col{grid-template-columns:1fr}.section{padding:30px 0}.section-head{display:block}.references{columns:1}.metrics{gap:35px}th,td{padding:10px}#source-table td:nth-child(3){min-width:205px}.report-page{padding:20px;min-height:0;margin:0}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{@page{size:A4;margin:0}.report-page{margin:0;min-height:0;height:297mm;max-width:none;padding:14mm 16mm;break-after:page;overflow:hidden}.report-page:last-child{break-after:auto}body{background:white}.report-page a{color:#16333c;text-decoration:none}.report-page table{font-size:10.5px}.report-page p{font-size:12px}.report-page .table-wrap{overflow:visible}.report-page .references{font-size:11px}.report-page h2{margin-top:14px}.report-page td,.report-page th{padding:5px 7px}}
'''
css+='''
[hidden]{display:none!important}
@media(max-width:600px){#source-table .table-wrap{overflow:visible}#source-table table,#source-table tbody{display:block}#source-table thead{display:none}#source-table tr{display:grid;grid-template-columns:1fr 1fr;padding:14px 0;border-bottom:1px solid var(--line)}#source-table td{display:block;padding:3px 0;border:0;min-width:0!important}#source-table td:nth-child(1){color:var(--muted)}#source-table td:nth-child(2){font-weight:700;text-align:right}#source-table td:nth-child(3){grid-column:1/-1}#source-table td:nth-child(4){grid-column:1/-1;color:var(--muted);font-size:12px}#source-table td:nth-child(4):before{content:'采集设置：'}}
@media print{.report-page{width:210mm}.report-page p{font-size:14px}.report-page table{font-size:12px}.report-page td,.report-page th{padding:6px 7px}.report-page .references{font-size:12px}.report-page h2{font-size:18px}.report-page .lead{font-size:15px}.report-page .external-inventory th:first-child{width:22%}.report-page .external-inventory th:nth-child(2){width:20%}.report-page .external-inventory td:first-child>a{display:none}}
'''
(WEB/'style.css').write_text(css,encoding='utf-8')
sections=f'''
<section id="overview" class="section"><div class="section-head"><div><p class="eyebrow">01 / 一页看全</p><h2>从真实来源到最终触达</h2><p>一张图包含来源清单、配置位置、采集方式、清洗与模型处理、报告渠道，以及当前边界。点击图片可放大查看。</p></div><a class="button" href="./overview.html">独立一页视图 ↗</a></div><a class="figure-link" href="./assets/overview.svg" target="_blank" rel="noopener"><img class="overview" src="./assets/overview.svg" alt="Agents Radar 一页能力与架构总览，包含十九个仓库及全部外部来源"/></a><p class="caption">图为本研究室依据固定版本源码原创绘制。可下载 SVG、高清 PNG 或单页 PDF；单页 PDF 为横向版式。</p></section>
<section id="sources" class="section"><p class="eyebrow">02 / 来源清单</p><h2>关注谁，如何取得信息</h2><p>GitHub 固定仓库集中配置在 <code>config.yml</code>；官网及外部平台的规则写在对应采集模块。来源类别、真实站点数量与报告数量采用不同统计口径。</p><div class="toolbar"><input id="repo-search" type="search" aria-label="搜索仓库或项目" placeholder="搜索名称、仓库地址或配置…"/><div class="filters" role="group" aria-label="按仓库类别筛选">{''.join(f'<button type="button" class="filter" data-category="{E(c)}" aria-pressed="{str(c=="全部").lower()}">{E(c)}</button>' for c in ['全部','CLI 工具','Agent 项目','AI 基础设施','Skills'])}</div></div><p id="repo-count" class="count" aria-live="polite">显示 19 / 19 个仓库</p><div id="source-table">{repo_table}</div><p id="empty" class="empty" hidden>没有匹配的仓库。请更换关键词或分类。</p><p class="notice">Codex 与 Pi 开启 Discussions；标记“分页”的仓库允许读取更多条目。Skills 按社区热度独立处理。</p><div class="source-block"><h3>官网、榜单与外部平台</h3>{external_table}<p class="notice">已按源码纠正 HN：当前是官方 Firebase 热门榜，README 中的 Algolia 与 24 小时口径尚未同步。</p></div></section>
<section id="pipeline" class="section"><p class="eyebrow">03 / 模块架构</p><h2>各来源独立适配，报告流程集中组织</h2><div class="stack"><div class="step"><span class="number">采集</span><h3>固定流程并行取数</h3><p>按平台分别请求 REST、GraphQL、HTML 或 XML。保留各来源数据类型；新增平台需要加入主流程。</p></div><div class="step"><span class="number">处理</span><h3>规则筛选后交给模型</h3><p>先做去重、时间与主题筛选、排序和截取；再生成分项摘要、比较分析及中文翻译。</p></div><div class="step"><span class="number">交付</span><h3>报告成为可复用内容</h3><p>按日期保存到 Git，生成目录与 RSS，同时供网页阅读、群通知和 MCP 查询使用。</p></div></div>{module_table}<p class="notice">已有 6 种模型供应商适配，当前工作流选用 Qwen。模型最多并发 5 路，具备连接与限流重试、翻译回退和失败比例检查。</p></section>
<section id="outputs" class="section"><p class="eyebrow">04 / 最终能力</p><h2>10 类报告，多种使用入口</h2>{output_table}<div class="stack"><div class="step"><h3>阅读与归档</h3><p>中英双语 Markdown、Git 历史、GitHub Pages 与 GitHub Issues。</p></div><div class="step"><h3>订阅与通知</h3><p>RSS 订阅生成的报告；Telegram、飞书推送亮点与链接。</p></div><div class="step"><h3>提供给其他助手</h3><p>MCP 查询最新或指定报告；近期关键词搜索，最多 14 个已收录日期。</p></div></div></section>
<section id="boundaries" class="section"><p class="eyebrow">05 / 复用与边界</p><h2>先理解覆盖范围，再判断扩展价值</h2><div class="two-col boundaries">{''.join(f'<div><h3>{E(n)}</h3><p>{E(d)}</p></div>' for n,d in LIMITS)}</div><h3>建议的扩展顺序</h3>{extension_table}<p class="notice">以上扩展是研究建议，不属于当前已经实现的功能。适用场景包括个人晨报、团队选型跟踪、竞品需求观察、开源社区运营与内容选题。</p></section>
<section id="references" class="section"><p class="eyebrow">06 / 查阅与下载</p><h2>依据固定源码版本，可追溯</h2><p>核对版本 <code>{COMMIT}</code>。本页为架构研究，没有运行上游采集、模型调用或消息发布。</p><div class="actions"><a class="button primary" href="./downloads/agents-radar-research.pdf" download>研究文档 PDF</a><a class="button" href="./downloads/agents-radar-research.md" download>可编辑 Markdown</a><a class="button" href="./downloads/agents-radar-overview.pdf" download>一页图 PDF</a><a class="button" href="./assets/overview.png" download>高清 PNG</a><a class="button" href="./assets/overview.svg" download>矢量 SVG</a></div>{ref_html}</section>
'''
html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Agents Radar 多源情报架构 | 项目研究室 005</title><meta name="description" content="19 个 GitHub 仓库与全部站点来源清单，采集适配、清洗分析与报告分发，一页图与详细架构研究。"/><link rel="stylesheet" href="./style.css"/></head><body><header class="top"><div class="shell"><a class="brand" href="../../">项目研究室 / 005</a><nav aria-label="页面导航"><a href="#overview">一页总览</a><a href="#sources">真实来源</a><a href="#pipeline">架构</a><a href="#references">下载</a></nav></div></header><main class="shell"><div class="hero"><div><p class="eyebrow">开源项目研究 / 2026.09.09</p><h1>Agents Radar<br/>多源情报架构</h1><p class="lead">从关注的仓库、官网与社区，持续生成可阅读、可订阅、可查询的双语报告。</p></div><div class="hero-side"><div class="metrics"><div><strong>19</strong><span>固定 GitHub 仓库</span></div><div><strong>2</strong><span>公司官网</span></div><div><strong>6</strong><span>外部平台</span></div></div><p>重点拆解来源设置、抓取适配、规则处理与展示方式，帮助判断哪些实现可以复用。</p><div class="actions"><a class="button primary" href="#overview">查看一页图 ↓</a><a class="button" href="{UP}">上游仓库 ↗</a></div></div></div>{sections}</main><footer class="shell foot">项目研究室 005 · 原创研究与架构图 · 上游仓库采用 MIT 许可 · 来源以固定版本源码为准</footer><script src="./app.js"></script></body></html>'''
(WEB/'index.html').write_text(html,encoding='utf-8')
(WEB/'app.js').write_text('''const input=document.getElementById('repo-search');const buttons=[...document.querySelectorAll('[data-category]')];const rows=[...document.querySelectorAll('#source-table tbody tr')];let category='全部';function filter(){const q=input.value.trim().toLowerCase();let count=0;rows.forEach(row=>{const match=(category==='全部'||row.cells[0].textContent===category)&&row.textContent.toLowerCase().includes(q);row.hidden=!match;if(match)count++;});document.getElementById('repo-count').textContent=`显示 ${count} / ${rows.length} 个仓库`;document.getElementById('empty').hidden=count!==0;}input.addEventListener('input',filter);buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.category;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filter();}));''',encoding='utf-8')
overview_html='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Agents Radar 一页总览</title><style>*{box-sizing:border-box}body{margin:0;background:#f4f2eb;font-family:"Microsoft YaHei",sans-serif;color:#18323a}nav{display:flex;gap:24px;align-items:center;padding:16px 24px;flex-wrap:wrap}a{color:#226f65}img{display:block;width:100%;height:auto}main{max-width:1920px;margin:auto}@page{size:480mm 300mm;margin:0}@media print{nav{display:none}main{width:480mm;max-width:none}img{width:480mm;height:300mm}}</style></head><body><nav><a href="./index.html">← 详细研究</a><a href="./assets/overview.svg" target="_blank">放大矢量图</a><a href="./assets/overview.png" download>下载 PNG</a><a href="./downloads/agents-radar-overview.pdf" download>下载单页 PDF</a></nav><main><img src="./assets/overview.svg" alt="Agents Radar 全部来源、采集方式、处理流程、展示分发与架构边界"/></main></body></html>'''
(WEB/'overview.html').write_text(overview_html,encoding='utf-8')
report_html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"/><title>Agents Radar 架构与能力研究</title><link rel="stylesheet" href="../style.css"/></head><body>'+''.join(f'<section class="report-page"><div class="page-label">项目研究室 005　|　2026-09-09　|　{i+1} / {len(report_pages)}</div><h1>{E(title)}</h1>{body}</section>' for i,(title,body) in enumerate(report_pages))+'</body></html>'
(DOWNLOADS/'research-print.html').write_text(report_html,encoding='utf-8')

def md_table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(str(v).replace('|',' / ').replace('\n','<br/>') for v in row)+' |\n' for row in rows)
md=f'''# Agents Radar 架构与能力研究

{overview_intro}

| 项目资料 | 内容 |
| --- | --- |
| 上游仓库 | {UP} |
| 核对版本 | `{COMMIT}` |
| 核对日期 | 2026-09-09 |
| 研究状态 | 已整理 |
| 方法 | 静态源码检查；未运行上游采集、模型或消息发送 |

## 一页总览

![Agents Radar 一页能力与架构总览](web/assets/overview.svg)

[详细网页](web/index.html) · [独立一页视图](web/overview.html) · [研究 PDF](web/downloads/agents-radar-research.pdf) · [单页 PDF](web/downloads/agents-radar-overview.pdf) · [高清 PNG](web/assets/overview.png)

## 架构判断

{architecture_text}

这是代码控制的固定信息流水线。模型承担摘要、比较和翻译，主流程未实现模型自主规划与反复工具执行。最值得复用的是来源适配与后续报告处理的职责划分。

## 全部 GitHub 来源

18 个项目仓库加 1 个 Skills 仓库。以下为 config.yml 中的真实设置。

'''+md_table(['分类','名称','仓库','额外设置'],[(c,n,f'[{r}](https://github.com/{r})',f or '默认') for c,n,r,f in REPOS])+'''
普通仓库请求 50 条；分页仓库每页 100 条、最多 5 页。采集后还会按热度取样，不能据此宣称完整覆盖。Skills 独立按社区热度采集，不按最近一天过滤。

## 官网与其他平台

'''+md_table(['来源类型','真实源','方式','设置','实现'],[(c,f'[{n}]({u})',m,r,f'[{file}]({source(file)})') for c,n,u,m,r,file in EXTERNAL])+'''
HN 按当前源码使用官方 Firebase 热门榜；README 的 Algolia 与 24 小时说明未同步。本研究采用源码口径。RSS 在该项目中主要是生成报告后的输出订阅渠道。

## 模块职责

'''+md_table(['模块','代码','职责'],MODULES)+'''
## 处理和运行规则

1. Actions 定时触发，index.ts 读取配置并并行采集数据。当前计划北京时间 06:37 触发，预计约 07:00 产出，实际可能排队延迟。
2. 各采集模块进行时间、主题、ID 去重和排序等处理，规则依来源而异，并非所有来源都走相同清洗步骤。
3. prompts.ts 等做 Top N 抽样、字段排版与正文截取。GitHub 正文通常截取 300 字符，官网正文最多 1500 字符，ArXiv 输入摘要片段。
4. 按项目生成英文摘要，再生成跨项目比较；中文由英文翻译得到。最后提取通知亮点。
5. 按日期保存报告和状态，提交 Git，更新 manifest 与 RSS，发布 Issues 并发送通知。

模型已适配 Anthropic、OpenAI、GitHub Copilot、OpenRouter、DeepSeek、Qwen；当前工作流选择 Qwen。模型并发上限 5，支持连接和限流重试、翻译回退及失败统计。至少 5 次调用且失败比例达到 50% 时，健康检查中止运行。失败来源或报告可降级或跳过。

## 输出能力

'''+md_table(['标识','类型','内容或条件'],OUTPUTS)+'''
所有报告提供中文和英文文件，英文带 -en 后缀。支持一种报告不代表每天必然产出。

- **保存与阅读**：日期目录下的 Markdown、Git 历史归档、GitHub Pages、GitHub Issues。
- **订阅与通知**：RSS、Telegram、飞书。RSS 主要用于输出报告。
- **MCP**：Cloudflare Worker 读取静态报告，提供 list_reports、get_latest、get_report、search。

## 使用场景

个人技术晨报、团队工具选型跟踪、产品需求与竞品观察、开源社区运营、内容选题，以及为其他助手提供近期信息。它更适合作为进一步阅读的线索入口，重要判断应核对原始来源。

## 当前边界

'''+''.join(f'### {n}\n\n{d}\n\n' for n,d in LIMITS)+'''## 扩展建议

以下为研究建议，不是当前已实现功能。

'''+md_table(['方向','具体工作','价值'],EXTENSIONS)+'''
## 本地阅读与验证

研究室网页通过根目录 scripts/catalog.py build 构建到 _site。该项目为离线静态研究页，不会调用上游采集器或模型 API。下载包中提供 Markdown、PDF 和单页图。构建和浏览器检查记录见 notes/verification.md。

## 源码依据

'''+''.join(f'- [{file}]({source(file)})\n' for file in refs)+'''
本研究文字与图为原创整理，源码链接固定到已核对版本。仓库 README 以 10 个采集类别描述来源，本报告按实现类型重新组织，区分来源类别、站点数和报告数。上游许可为 MIT。
'''
(ROOT/'README.md').write_text(md,encoding='utf-8')
download_md=md.replace('(web/assets/', '(../assets/').replace('(web/downloads/','(./').replace('(web/index.html)','(../index.html)').replace('(web/overview.html)','(../overview.html)')
(DOWNLOADS/'agents-radar-research.md').write_text(download_md,encoding='utf-8')
(WEB/'data.json').write_text(json.dumps(dict(commit=COMMIT,repos=REPOS,sources=EXTERNAL,modules=MODULES,outputs=OUTPUTS,limitations=LIMITS,extensions=EXTENSIONS),ensure_ascii=False,indent=2),encoding='utf-8')
print('Built research Markdown, 7-page print document, website, source inventory and one-page SVG.')
