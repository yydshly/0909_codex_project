"""Render the editable, dependency-free SVG overview used by this study."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1810" viewBox="0 0 1800 1810" role="img" aria-labelledby="title desc">
<title id="title">Multica 整体理解：人参与控制，平台编排，Agent 工具执行</title>
<desc id="desc">上方为人的派工、过程干预和评审；左侧展示平台到工具和模型的执行架构；右侧展示组长成员交接；下方总结边界、价值、扩展入口和实测证据。</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#718394"/></marker></defs>
<style>text{font-family:'Microsoft YaHei','Noto Sans SC',sans-serif;fill:#203143}.title{font-size:40px;font-weight:700}.h{font-size:27px;font-weight:700}.b{font-size:23px}.s{font-size:20px;fill:#526479}.tag{font-size:19px;font-weight:700;fill:#ac4836}.line{fill:none;stroke:#718394;stroke-width:2.5;marker-end:url(#arrow)}</style>
<rect width="1800" height="1810" rx="24" fill="#f5f7f8"/>''']

def rect(x,y,w,h,fill='white',stroke='#d7e0e7',r=14):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>')

def text(x,y,label,cls='b'):
    parts.append(f'<text x="{x}" y="{y}" class="{cls}">{escape(label)}</text>')

def lines(x,y,labels,cls='s',gap=30):
    for i,label in enumerate(labels): text(x,y+i*gap,label,cls)

def arrow(path, dashed=False):
    parts.append(f'<path class="line" d="{path}"'+(' stroke-dasharray="7 6"' if dashed else '')+'/>')

text(44,43,'011 / MULTICA · 完整理解总览 · 事件驱动与并发','tag')
text(44,97,'人参与控制，平台组织工作，Agent 工具调用模型执行','title')
text(44,133,'核心定位：已有 Agent 工具之上的协作与执行编排平台。看板是入口，任务、运行与事件构成工作闭环。','b')

rect(44,162,1712,142,'#fff0e8','#edcebe')
text(68,200,'人 / HUMAN IN THE LOOP','h')
lines(68,238,['开始：提目标、定验收标准、选负责人','可直派单 Agent，也可分配小队'])
lines(660,238,['过程：看日志与工具调用、评论纠偏','@指定执行者、停止 Run、调整分工'])
lines(1212,238,['结束：检查产物、评审与验收','通过 → 完成；不通过 → 评论返工'])
arrow('M565 304V363')
text(590,340,'Web / CLI / API；事件与定时也可触发','s')
arrow('M1690 376V313',True)
text(1390,341,'结果回到人；意见进入后续执行','s')

rect(44,376,1052,158,'#eaf1fa','#c6d8ea')
text(68,416,'① 平台执行调度 · Go 服务 + PostgreSQL','h')
lines(68,454,['Issue / Run / 身份与权限','目标与每次执行分别记录'])
lines(435,454,['事件路由 / 队列 / 并发约束','领取、去重、取消、重试与恢复'])
lines(828,454,['API / WebSocket','Redis 为可选设施'])
arrow('M570 534V577')
text(595,563,'持久队列 → 领取任务；进度与结果反向回传','s')

rect(44,586,1052,132,'#eaf5f0','#c5dfd3')
text(68,626,'② 执行机器 · Daemon 守护进程','h')
lines(68,665,['发现可用工具 → 领取任务 → 准备工作目录、指令和配置 → 启动进程','维护连接与执行生命周期，收集消息、工具事件、错误和结果'])
arrow('M570 718V747')

rect(44,756,1052,96,'#ffffff')
text(68,796,'③ Provider 适配 · 统一 Agent 工具执行接口','h')
text(68,828,'Execute → Session / 流式消息 / 结果；取消、续接、模型选项等支持因工具而异','s')
arrow('M570 852V886')

rect(44,895,455,109,'#ffffff')
text(68,934,'④ Agent 工具','h')
text(68,973,'Codex / Claude Code / 其他工具','b')
arrow('M499 950H562')
rect(571,895,525,109,'#ffffff')
text(595,934,'模型推理 ↔ 工具执行循环','h')
text(595,973,'文件、命令、MCP、外部业务系统','b')

rect(1124,376,632,628,'#fffdf9','#e3dccf')
text(1148,416,'小队协作 · 组长判断分工，平台落实','h')
steps = [
('1  分配 Issue 给小队','平台创建组长 Run，注入协议、名单与 Skills'),
('2  组长发布委派评论','结构化 @成员 ID + 自然语言工作要求'),
('3  平台安排成员 Run','成员排队/执行；组长结束本轮，不持续等待'),
('4  成员回写结果和产物位置','任务与评论是交接点；文件需分支/PR 等交接'),
('5  事件再次唤醒组长','读新反馈 → 继续委派 / 请求人处理 / 待评审'),
('6  人检查与反馈','验收通过，或 @组长 提出修改意见再执行'),
]
for i,(head,body) in enumerate(steps):
    y=443+i*91
    rect(1148,y,584,73,'#ffffff','#e6e1d8',9)
    text(1166,y+29,head,'b')
    text(1166,y+57,body,'s')
    if i<5: arrow(f'M1190 {y+73}V{y+87}')

rect(44,1030,1712,78,'#203143','#203143')
parts.append('<text x="68" y="1063" style="font-size:25px;font-weight:700;fill:white">共同工作记录：Issue 保存目标、讨论、负责人和验收状态；一个 Issue 可对应多次 Run。</text>')
parts.append('<text x="68" y="1093" style="font-size:22px;fill:#d8e4ee">Run 保存一次执行及日志。Agent 是配置好的角色，Runtime 是执行环境，Leader 是协调角色，模型提供推理。</text>')

rect(44,1134,838,242,'#fff0e8','#edcebe')
text(68,1174,'控制边界 · 回顾时不能混淆','h')
lines(68,1211,[
'评论 / 改状态 / 换负责人 ≠ 立即中断；停止要操作具体 Run。',
'Run completed ≠ 验收通过；待评审 ≠ 强制人工审批关卡。',
'默认面向无人值守；发布前必须审批，需要实际权限/流程约束。',
'取消 ≠ 回滚；共享评论 ≠ 共享模型会话或各机器文件。',
'目录隔离 ≠ 安全沙箱；本地执行 ≠ 数据全不出机器。',
],gap=31)

rect(908,1134,848,242,'#eef3f8','#d2deea')
text(932,1174,'价值与扩展 · 为业务闭环服务','h')
lines(932,1211,[
'价值：减少协调，让工作可分配、可追踪、可交接、可复查。',
'场景：研发、CI/故障、周期巡检、知识工作；需要业务工具与验收。',
'已有入口：Provider、Skills、插件/MCP、API/Hook、Autopilot。',
'扩展建议：强制审批、知识积累、效果/成本路由、隔离执行环境。',
'衡量收益：验收通过率、返工、人工介入、耗时与费用。',
],gap=31)

rect(44,1400,1712,126,'#eef3f8','#d2deea')
text(68,1440,'顺序与并行 · 依赖决定先后，资源约束并发','h')
lines(68,1477,['独立任务 / 独立成员可以并行；有依赖的步骤等待结果。','平台按需启动或续接 Agent；Agent 工具内部可多次调用模型。'])
lines(932,1477,['并发受 Agent / Daemon 设置、节点容量与目录锁约束。','本次单成员交接是顺序示例，未单独实测并行负载。'])

rect(44,1550,1712,150,'#eaf5f0','#c5dfd3')
text(68,1590,'本次实测 · 原版真实运行，证据与未验证范围分开','h')
lines(68,1628,['LAB-1：Claude Code 真实写文件并回传结果。','LAB-2：Codex 组长 → 成员 → 组长，三次 Run 完成。'])
lines(932,1628,['观察到排队，实际执行过人工停止；两任务保留待评审。','未实测完整人工返工、强制审批、多机规模及外部业务集成。'])
text(44,1741,'重要限定：适配 Agent 工具 ≠ 模型网关/自动负载均衡；人工改交 Claude 成功 ≠ 平台自动故障切换。','s')
text(44,1774,'依据：multica-ai/multica · 9d36136 · 2026-09-09｜Multica License 含额外条件｜完整细节见回顾文档｜研究资料发布版','s')
parts.append('</svg>')
(ROOT/'web/assets/architecture.svg').write_text('\n'.join(parts)+'\n',encoding='utf-8')
print('architecture.svg generated: 1800 × 1810')
