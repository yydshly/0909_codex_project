"""Build the public, source-linked one-page research map without remote assets."""
from pathlib import Path
from html import escape
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
BASE = 'https://yydshly.github.io/0909_codex_project/projects/003-archify/'
REV = '10722002bb8777ecb639d93c49586fae4adf3ae4'
UP = 'https://github.com/tt-a1i/archify/tree/' + REV
W, H = 1800, 3180
out = []
def add(s): out.append(s)
def text(x, y, s, size=22, color='#263d38', weight=400):
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>')
def wrapped(x, y, s, width, size=21, leading=31, color='#50645d', weight=400):
    # CJK characters occupy one em; Latin uses a conservative 0.6 em.
    lines=[]; line=''; units=0
    for c in s:
        amount=1 if unicodedata.east_asian_width(c) in ('F','W') else .6
        if c=='\n' or units+amount>width/size:
            lines.append(line);line='';units=0
            if c=='\n':continue
        line+=c;units+=amount
    if line:lines.append(line)
    for i,l in enumerate(lines):text(x,y+i*leading,l,size,color,weight)
    return y+(len(lines)-1)*leading
def box(x,y,w,h,fill='#fffefa',stroke='#d4ded5',radius=15):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')
def link_start(href):add(f'<a href="{escape(href,quote=True)}" target="_blank" rel="noopener">')
def link_end():add('</a>')
def section(n,title,y,note=''):
    text(56,y,n,21,'#67806b',700);text(104,y,title,30,'#193c32',700)
    if note:text(1744-len(note)*17,y,note,17,'#687d72')
def card(x,y,w,h,kicker,title,body,footer='',href=None,fill='#fffefa'):
    if href:link_start(href)
    box(x,y,w,h,fill)
    text(x+24,y+29,kicker,15,'#667e6d',700)
    text(x+24,y+67,title,27,'#234d3d',700)
    wrapped(x+24,y+105,body,w-48,21,31)
    if footer:text(x+24,y+h-20,footer,17,'#3c7660',600)
    if href:link_end()

add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">')
add('<title id="title">Archify 理解全景：能力、原理、设计体系与扩展路线</title><desc id="desc">一页中文研究图。涵盖五类技术图和架构差异、外部作者到结构化规格的生成链、UML 与 4+1 及 C4 的区别、八个项目分析维度、三层扩展路线和真实实验依据。带链接的卡片可进入详细演示或官方来源。</desc>')
add('<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,1 L8,5 L0,9" fill="none" stroke="#668773" stroke-width="1.6"/></marker></defs>')
add('<style>text{font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif}a{cursor:pointer}a:hover>rect{stroke:#3c7660;stroke-width:2}a:focus>rect{stroke:#b88225;stroke-width:3}</style>')
box(0,0,W,H,'#f3f5ef','#f3f5ef',0)
text(56,51,'003  /  OPEN-SOURCE RESEARCH MAP',17,'#5d7865',700)
text(56,114,'Archify：从技术表达，到可交付的项目图谱',48,'#163f32',700)
text(56,158,'能力是什么 · 信息从哪里来 · 如何组织设计 · 还能向哪里扩展',24,'#62776a')
text(1396,48,'研究快照 / 2026.09.09',17,'#607567')
text(1396,76,'v2.17.0-dev.1 · 1072200',17,'#607567')

card(56,194,546,179,'定位 / OUR INTERPRETATION','面向 Agent 的技术图表达与交付','Skill 指导表达；结构化规格驱动绘图。\n用于源码讲解、设计评审、文档与变更沟通。',fill='#e8efe3')
card(626,194,546,179,'价值 / WHY IT MATTERS','把理解沉淀为可复查的图','图规格可修改、版本化；产物可离线阅读。\n确定布局与校验规则，减少随意拼图。')
card(1196,194,548,179,'边界 / WHAT IT DOES NOT DO','代码理解来自外部','没有通用源码关系抽取器；不会独立理解仓库。\n不等于完整 UML、拖拽编辑或托管协作平台。',fill='#f9f0df')

section('01','从输入到成品：谁负责理解，谁负责绘制？',425)
steps=[('外部信息与作者','源码 · 描述 · Mermaid','用户或 Agent 分析并取舍内容。\n这些信息需先转为图规格。','#edf0eb'),('有类型的 JSON 规格','Archify 程序直接读取的输入','声明节点、关系、布局与说明。\n五类 Schema 约束各自结构。','#e8efe3'),('校验、布局与渲染','专用渲染器 + 共享模块','检查字段、引用、布局约束。\n生成 SVG，装入 HTML 模板。','#e8efe3'),('检查与原子交付','deliver 的受控生成链','冻结快照 → 验收候选 → 哈希。\n通过后才替换最终文件。','#e8efe3'),('浏览器阅读与导出','已生成页面不需要模型服务','搜索、聚焦、路径、章节与风格。\n导出图片、矢量和动态视频。','#e8efe3')]
for i,(title,sub,body,fill) in enumerate(steps):
    x=56+i*342;box(x,460,320,166,fill)
    text(x+18,496,title,24,'#24513d',700);wrapped(x+18,529,sub,285,17,25)
    wrapped(x+18,567,body,285,18,28)
    if i<4:add(f'<path d="M{x+322},545 L{x+338},545" stroke="#668773" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
box(56,644,1688,64,'#e9eee7',radius=8)
text(76,671,'可选源码证据：架构图可核验固定 Git 提交、文件与行范围；不证明关系语义正确。',20)
text(76,696,'实现要点：开发阶段用 AJV 编译校验器；共享模板承载交互。preview 监控输入，失败保留上次验证通过的产物。',18,'#607568')

section('02','已支持的表达能力：五类基础图 + 架构差异视图',760,'点击卡片 → 中文源码实战')
native=[('01 / ARCHITECTURE','架构图：系统由什么组成？','组件、关系、区域、分组与边界。\n案例：作者 → 规格 → 渲染交付 → 查看器。','节点可附固定版本源码引用','architecture'),('02 / WORKFLOW','工作流：谁先做什么？','步骤、职责泳道、阶段、分支与异常。\n案例：生成、验收、交付及外部修复重试。','表达控制流与责任交接','workflow'),('03 / SEQUENCE','时序图：调用如何往返？','参与者、生命线、消息、返回与活动区间。\n案例：主进程与两个子进程的调用顺序。','时间顺序 ≠ 实际耗时','sequence'),('04 / DATAFLOW','数据流：输入变成什么？','数据来源、处理阶段、存储、流向与标签。\n案例：JSON → 已校验规格 → SVG / HTML。','IR 是图规格，不是源码 AST','dataflow'),('05 / LIFECYCLE','生命周期：怎样完成或失败？','阶段、活动、等待、决策、成功与失败。\n案例：候选产物通过验收后成为最终文件。','本次阶段名由源码分析后整理','lifecycle'),('06 / ARCHITECTURE DELTA','架构差异：前后改变了什么？','比较两份架构规格：新增、删除、修改、\n移动与改道；切换 Before / Delta / After。','真实案例：在线字体 → 内嵌字体','delta')]
for i,(k,t,b,f,id) in enumerate(native):card(56+(i%3)*570,796+(i//3)*218,546,198,k,t,b,f,BASE+'self.html#'+id)
box(56,1248,1688,82,'#dfeadd',radius=10)
text(78,1278,'通用查看器能力',22,'#24523d',700)
text(280,1278,'搜索与聚焦 · 上下游与有向路径 · 章节讲解 · 动画与演示 · 四种风格 × 深浅主题',20)
text(78,1310,'交付与导出：独立 HTML、PNG、JPEG、WebP、SVG、WebM、整图 / 路径 / 范围分享卡片。不同视图支持的操作有区别。',19)

section('03','设计体系：组织视角、定义语义、保存设计理由',1381)
box(56,1416,832,208)
text(80,1453,'4+1 / 检查哪些架构关注点',27,'#24523d',700)
for i,s in enumerate(['逻辑：职责与关键抽象    开发：源码组织与依赖','进程：并发、通信与同步    物理：软件与运行节点','＋1：关键场景贯穿并验证四个视图；不只是多画一张图。','一个视图可以包含多张图；进程视图不是普通流程图。']):text(80,1492+i*31,s,21 if i<2 else 19,'#50645d')
box(912,1416,832,208)
text(936,1453,'C4 / 从系统全景逐层展开到代码',27,'#24523d',700)
for i,s in enumerate(['系统上下文 → 容器 → 组件 → 代码','用户与外部系统 → 应用 / 服务 / 存储 → 内部组件 → 实现','Container 不专指 Docker；按需要选择层级。','补充动态与部署视图，帮助从总览进入关键细节。']):text(936,1492+i*31,s,23 if i==0 else 19,'#50645d')
box(56,1644,1688,137)
text(80,1680,'UML / 规定模型元素、关系与行为的表达语义',26,'#24523d',700)
text(80,1719,'结构类：类图、对象图、包图、组件图、组合结构图、部署图、轮廓图。',21)
text(80,1753,'行为类：用例图、活动图、状态机图；交互类属于行为类，包括顺序图、通信图、交互概览图、定时图。',21)
box(56,1801,1688,117,'#eef0e9')
text(80,1835,'arc42：记录目标、约束、结构、运行、部署、决策、质量与风险。BPMN：业务流程。SysML：软硬件系统工程。',20)
text(80,1868,'ArchiMate：企业业务—应用—技术的建模语言。TOGAF：企业架构方法与治理框架。',20)
text(80,1897,'关系：C4 组织层级，4+1 检查关注点，UML 等定义表达，arc42 组织文档；分层、微服务、六边形架构属于设计风格。',18,'#607568')

section('04','按系统整理：完整项目还值得展示哪些图？',1970,'可复用 ≠ 已有专用语义支持')
box(56,2000,1688,527,'#fffefa',radius=10)
add('<path d="M56,2050 H1744" stroke="#d4ded5"/>')
cols=[80,308,948,1432]
for x,s in zip(cols,['分析维度','建议图谱与要回答的问题','信息来源','与 Archify 的关系']):text(x,2033,s,20,'#315943',700)
rows=[('业务与目标','上下文图、用例图、BPMN：谁用、做什么、跨谁协作？','需求、角色、业务规则','复用架构 / 新图型'),('结构与部署','C4 分层、组件与部署图：拆成什么，运行在哪里？','模块设计、部署配置','细化架构图'),('代码与接口','包依赖、调用图、类 / 接口图：如何组织、调用、扩展？','引用解析、静态分析、追踪','关系图复用 / 类图新增'),('数据与契约','ER、规格结构、数据血缘：字段如何关联、转换和派生？','数据库、Schema、转换逻辑','细化数据流 / ER 新增'),('运行与异常','时序、完整状态机、并发图：如何响应、等待和恢复？','控制逻辑、事件、运行日志','复用时序 / 深化状态'),('安全与验证','信任边界、权限、需求—实现—测试：谁能做，如何证明？','权限配置、需求和测试关联','边界复用 / 关联模型新增'),('性能与变化','热点 / 火焰图、版本差异：哪里慢，哪些结构改变？','性能测量、前后模型','性能新增 / 架构差异已有'),('项目与演进','功能树、路线图、甘特图：范围是什么，怎样逐步实现？','功能清单、计划和决策','树图、时间轴等新增')]
for i,row in enumerate(rows):
    y=2050+i*59
    if i%2==0:box(57,y+1,1686,58,'#f3f6ee','#f3f6ee',0)
    for j,(x,s) in enumerate(zip(cols,row)):text(x,y+37,s,19 if j in (1,2) else 18,'#304c3e' if j==0 else '#566b5e',600 if j==0 else 400)

section('05','扩展路线：补上信息来源、模型语义与阅读层级',2580,'以下均为建议，未声称已实现')
card(56,2614,546,218,'第一层 / DATA','从“有人写规格”到“有证据提取”','接入源码引用、调用关系、数据库结构、\n部署配置、OpenAPI 与运行追踪。\n保留来源、版本、未知项与分析置信度。','绘图类型增加，不会自动带来数据来源',fill='#f9f0df')
card(626,2614,546,218,'第二层 / MODEL','从通用节点到专用语义模型','新增类图、ER、完整状态机等 Schema。\n定义接口、关系数量、触发条件与约束；\n配套布局、诊断、测试和图间一致性。','先定义含义，再设计外观',fill='#f9f0df')
card(1196,2614,548,218,'第三层 / READING','从多张图到可逐层浏览的图谱','稳定 ID、全景到模块的跳转与跨图引用。\n关联设计理由、质量指标、变更与测试；\n支持按角色、场景和分析层级阅读。','推荐：C4 层级 + 4+1 视角 + 必要细节图',fill='#f9f0df')
box(56,2842,1688,92,'#e8efe3',radius=10)
text(78,2874,'对 Archify 自身的优先补充',23,'#24523d',700)
text(78,2909,'模块依赖图 → 关键函数调用图 → 五类规格结构图 → 预览状态机 → 新图型接入图。增加分析深度，避免多张图重复同一条主线。',20)

section('06','可复查的实战与阅读边界',2980)
text(56,3017,'已验证：五类中文图各 9/9 检查通过；八组风格、八份原生导出；预览错误期间旧文件哈希不变，修复后才更新。',20)
text(56,3050,'注意：路径只遍历已声明关系；Delta 比较两份模型，不自动理解 Git diff。本次范围分享菜单有交互问题，成品通过原生接口导出。',18,'#66796c')
link_start(BASE+'self.html');text(56,3090,'查看全部原生实战 ↗',20,'#28704e',700);link_end()
link_start(BASE+'research.html');text(376,3090,'查看完整文字整理与来源 ↗',20,'#28704e',700);link_end()
link_start(UP);text(804,3090,'核对上游固定版本源码 ↗',20,'#28704e',700);link_end()
text(56,3133,'本页为研究整理的信息总览，不是 Archify 自动生成的代码分析结果。示例与导出保留上游 MIT 及字体 OFL 许可。',17,'#748577')
add('</svg>')
(WEB/'assets/understanding.svg').write_text('\n'.join(out),encoding='utf-8')
print('understanding.svg: 1800 × 3180, source-linked one-page map')

