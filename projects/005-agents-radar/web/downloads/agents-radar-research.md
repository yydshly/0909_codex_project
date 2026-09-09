# Agents Radar 架构与能力研究

agents-radar 是一个以 TypeScript 和 Node.js 实现的 AI 生态情报流水线。它定时采集开源项目、公司官网及社区平台的信息，通过规则筛选与大模型归纳生成中英双语报告，再以网页、订阅、通知和 MCP 服务提供给用户。最值得复用的是来源选择、平台适配、文本压缩和统一报告分发。

| 项目资料 | 内容 |
| --- | --- |
| 上游仓库 | https://github.com/duanyytop/agents-radar |
| 核对版本 | `dd2aaae700e2ebf62a7c80557c2bd64709be5e79` |
| 核对日期 | 2026-09-09 |
| 研究状态 | 已整理 |
| 方法 | 静态源码检查；未运行上游采集、模型或消息发送 |

## 一页总览

![Agents Radar 一页能力与架构总览](../assets/overview.svg)

[详细网页](../index.html) · [独立一页视图](../overview.html) · [研究 PDF](./agents-radar-research.pdf) · [单页 PDF](./agents-radar-overview.pdf) · [高清 PNG](../assets/overview.png)

## 架构判断

GitHub Actions 负责调度，src/index.ts 负责固定流程编排。仓库配置由 config.yml 读取，站点与平台规则分散在各采集模块。采集器返回各自的数据类型，提示词模块将它们整理为模型输入，报告构建与保存模块负责双语内容及文件输出。各平台之间没有统一的动态插件注册机制。

这是代码控制的固定信息流水线。模型承担摘要、比较和翻译，主流程未实现模型自主规划与反复工具执行。最值得复用的是来源适配与后续报告处理的职责划分。

## 全部 GitHub 来源

18 个项目仓库加 1 个 Skills 仓库。以下为 config.yml 中的真实设置。

| 分类 | 名称 | 仓库 | 额外设置 |
| --- | --- | --- | --- |
| CLI 工具 | Claude Code | [anthropics/claude-code](https://github.com/anthropics/claude-code) | 默认 |
| CLI 工具 | OpenAI Codex | [openai/codex](https://github.com/openai/codex) | Discussions |
| CLI 工具 | Gemini CLI | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 默认 |
| CLI 工具 | GitHub Copilot CLI | [github/copilot-cli](https://github.com/github/copilot-cli) | 默认 |
| CLI 工具 | OpenCode | [anomalyco/opencode](https://github.com/anomalyco/opencode) | 默认 |
| CLI 工具 | Pi | [earendil-works/pi](https://github.com/earendil-works/pi) | Discussions |
| CLI 工具 | Qwen Code | [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | 默认 |
| Agent 项目 | OpenClaw | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 分页 |
| Agent 项目 | Hermes Agent | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) | 默认 |
| Agent 项目 | IronClaw | [nearai/ironclaw](https://github.com/nearai/ironclaw) | 默认 |
| Agent 项目 | QwenPaw | [agentscope-ai/QwenPaw](https://github.com/agentscope-ai/QwenPaw) | 默认 |
| Agent 项目 | ZeroClaw | [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) | 默认 |
| AI 基础设施 | vLLM | [vllm-project/vllm](https://github.com/vllm-project/vllm) | 分页 |
| AI 基础设施 | SGLang | [sgl-project/sglang](https://github.com/sgl-project/sglang) | 分页 |
| AI 基础设施 | llama.cpp | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 分页 |
| AI 基础设施 | Ollama | [ollama/ollama](https://github.com/ollama/ollama) | 默认 |
| AI 基础设施 | LiteLLM | [BerriAI/litellm](https://github.com/BerriAI/litellm) | 分页 |
| AI 基础设施 | Unsloth | [unslothai/unsloth](https://github.com/unslothai/unsloth) | 分页 |
| Skills | Claude Code Skills | [anthropics/skills](https://github.com/anthropics/skills) | 独立热度采集 |

普通仓库请求 50 条；分页仓库每页 100 条、最多 5 页。采集后还会按热度取样，不能据此宣称完整覆盖。Skills 独立按社区热度采集，不按最近一天过滤。

## 官网与其他平台

| 来源类型 | 真实源 | 方式 | 设置 | 实现 |
| --- | --- | --- | --- | --- |
| 公司官网 | [Anthropic](https://www.anthropic.com/sitemap.xml) | Sitemap + HTML 正文 | /news/、/research/、/engineering/、/learn/；比较已记录 URL 与 lastmod。 | [src/web.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/web.ts) |
| 公司官网 | [OpenAI](https://openai.com/sitemap.xml) | Sitemap 元数据 | research、publication、release、company、engineering、milestone、learn-guides、safety、product 子 Sitemap；仅发现新 URL，当前不抓正文。 | [src/web.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/web.ts) |
| 开源发现 | [GitHub Trending / Search](https://github.com/trending) | HTML + REST API | 日榜；搜索最近 7 天活跃且匹配 llm、ai-agent、rag、vector-database、large-language-model、machine-learning 的仓库。 | [src/trending.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/trending.ts) |
| 技术社区 | [Hacker News](https://news.ycombinator.com) | 官方 Firebase JSON API | 读取 topstories，最多扫描前 500 个 ID，按标题和 URL 的 AI 关键词筛选，按榜单次序保留最多 30 条；当前代码没有 24 小时时间过滤。 | [src/hn.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/hn.ts) |
| 技术社区 | [Dev.to](https://dev.to/api/articles) | Forem REST API | 并行查询 ai、llm、machinelearning、openai、langchain 五个标签，按 ID 去重。 | [src/devto.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/devto.ts) |
| 技术社区 | [Lobste.rs](https://lobste.rs) | 标签 JSON API | https://lobste.rs/t/ai.json 和 /t/ml.json；筛选最近 7 天故事。 | [src/lobsters.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/lobsters.ts) |
| 学术论文 | [ArXiv](https://export.arxiv.org/api/query) | API / Atom XML | cs.AI、cs.CL、cs.LG；最近 48 小时；最多 50 篇；模型输入为论文标题与摘要片段。 | [src/arxiv.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/arxiv.ts) |
| 模型平台 | [Hugging Face](https://huggingface.co/api/models) | Hub REST API | 按 likes7d 排序，最多 30 个模型；每周一采集并生成报告。 | [src/hf.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/hf.ts) |
| 产品发现 | [Product Hunt](https://api.producthunt.com/v2/api/graphql) | GraphQL API | 昨日产品按票数取候选，再按 AI 及相关主题过滤；主题也包括 developer-tools、open-source；需要 PRODUCTHUNT_TOKEN。 | [src/ph.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/ph.ts) |

HN 按当前源码使用官方 Firebase 热门榜；README 的 Algolia 与 24 小时说明未同步。本研究采用源码口径。RSS 在该项目中主要是生成报告后的输出订阅渠道。

## 模块职责

| 模块 | 代码 | 职责 |
| --- | --- | --- |
| 配置与编排 | config.yml · src/config.ts · src/index.ts | 读取关注仓库；并行采集各来源；安排摘要、翻译、比较、报告保存及发布。 |
| 来源适配 | github.ts · web.ts · trending.ts · hn.ts 等 | 各自处理 API、HTML 或 XML，返回对应类型的数据；新增平台仍需修改主流程。 |
| 文本与提示词 | prompts.ts · prompts-data.ts | 时间与热度筛选多发生在采集器内；这里做 Top N 取样、字段排版、正文截取及分析指令构建。 |
| 模型与可靠性 | report.ts · providers/ | 统一模型接口、最多 5 路模型并发、连接和限流重试、失败统计、翻译回退。 |
| 报告组织 | report-builders.ts · report-savers.ts · i18n.ts | 组装分项目报告与跨项目比较，保存中英双语 Markdown；按数据可用性跳过部分报告。 |
| 索引与分发 | generate-manifest.ts · notify.ts · feishu.ts | 生成 manifest 与 RSS，推送 Telegram / 飞书，配合工作流提交文件和维护 Issues。 |
| 网页与查询 | index.html · mcp/src/index.ts | 静态网页读取报告；Cloudflare Worker 提供 MCP 读取与关键词搜索接口。 |

## 处理和运行规则

1. Actions 定时触发，index.ts 读取配置并并行采集数据。当前计划北京时间 06:37 触发，预计约 07:00 产出，实际可能排队延迟。
2. 各采集模块进行时间、主题、ID 去重和排序等处理，规则依来源而异，并非所有来源都走相同清洗步骤。
3. prompts.ts 等做 Top N 抽样、字段排版与正文截取。GitHub 正文通常截取 300 字符，官网正文最多 1500 字符，ArXiv 输入摘要片段。
4. 按项目生成英文摘要，再生成跨项目比较；中文由英文翻译得到。最后提取通知亮点。
5. 按日期保存报告和状态，提交 Git，更新 manifest 与 RSS，发布 Issues 并发送通知。

模型已适配 Anthropic、OpenAI、GitHub Copilot、OpenRouter、DeepSeek、Qwen；当前工作流选择 Qwen。模型并发上限 5，支持连接和限流重试、翻译回退及失败统计。至少 5 次调用且失败比例达到 50% 时，健康检查中止运行。失败来源或报告可降级或跳过。

## 输出能力

| 标识 | 类型 | 内容或条件 |
| --- | --- | --- |
| ai-cli | CLI 日报 | 跨工具比较、各工具更新、Skills 热点 |
| ai-agents | Agent 生态 | OpenClaw 深入报告、同类项目比较 |
| ai-infra | 基础设施 | 模型及硬件支持、性能、稳定性、破坏性变更 |
| ai-web | 官网动态 | 新增官方内容；无新增则跳过 |
| ai-trending | 开源趋势 | 热门仓库分类和趋势信号 |
| ai-hn | HN 社区 | 热点故事和社区观察 |
| ai-ph | 产品发现 | Product Hunt 产品；需 Token 且有可用数据 |
| ai-arxiv | 论文速览 | AI 相关分类的论文摘要 |
| ai-hf | 模型周报 | Hugging Face 模型榜；每周一 |
| ai-community | 社区合刊 | Dev.to 与 Lobste.rs 合并报告 |

所有报告提供中文和英文文件，英文带 -en 后缀。支持一种报告不代表每天必然产出。

- **保存与阅读**：日期目录下的 Markdown、Git 历史归档、GitHub Pages、GitHub Issues。
- **订阅与通知**：RSS、Telegram、飞书。RSS 主要用于输出报告。
- **MCP**：Cloudflare Worker 读取静态报告，提供 list_reports、get_latest、get_report、search。

## 使用场景

个人技术晨报、团队工具选型跟踪、产品需求与竞品观察、开源社区运营、内容选题，以及为其他助手提供近期信息。它更适合作为进一步阅读的线索入口，重要判断应核对原始来源。

## 当前边界

### 采样信息不等于全文研究

普通 GitHub 仓库单次采集 50 条；分页仓库每页 100 条、最多 5 页。提示词继续按评论数取 Top N，正文通常只保留 300 字符。ArXiv 也仅传入摘要片段。

### 来源覆盖程度不同

Anthropic 正文最多取 1500 字符；OpenAI 为元数据模式，标题来自 URL。官网首次每站最多处理 25 条，并把已发现 URL 记入状态，不构成全站历史归档。

### 趋势结论来自模型归纳

分项目摘要再汇总可能传递遗漏；热度和评论数不能直接代表质量。当前没有独立事实核验、语义去重或长期结构化趋势引擎。

### MCP 搜索有明确范围

默认搜索近期报告，最多 14 个已收录日期，跳过英文副本和汇总报告；采用字符串匹配，没有向量检索。类型说明中出现的 weekly/monthly 不能据此认定当前流水线会生成周月汇总。

### 执行与发布存在边界

GitHub Actions 调度可能延迟；部分来源失败会降级或跳过。健康门限能减少全量模型故障时的错误产出，但并非所有渠道都具备事务性发布与完整幂等保障。

## 扩展建议

以下为研究建议，不是当前已实现功能。

| 方向 | 具体工作 | 价值 |
| --- | --- | --- |
| 统一来源配置 | 把站点地址、查询条件、字段映射和调度频率移入统一配置；定义采集器注册接口。 | 让新增同类来源从改代码变为改配置。 |
| 结构化事件与证据 | 保存原始响应、来源片段、采集时间和标准事件；区分 closed 与 merged 等状态。 | 为事实校验、去重和历史比较提供基础。 |
| 个人订阅与告警 | 设置关注项目、主题与重要事件，增加重复事件抑制与变化检测。 | 将每日阅读变成只处理与用户相关的变化。 |
| 长期趋势与语义检索 | 建立 7 / 30 / 90 天事件序列，加入全文和向量索引，扩展 MCP。 | 支持跨月比较、语义问答与有证据的趋势回溯。 |
| 生产运行治理 | 采集成功率、覆盖率、模型成本、重试状态和发布记录可观测；失败任务可补跑。 | 让局部失败容易定位，并降低重跑带来的重复发布。 |

## 本地阅读与验证

研究室网页通过根目录 scripts/catalog.py build 构建到 _site。该项目为离线静态研究页，不会调用上游采集器或模型 API。下载包中提供 Markdown、PDF 和单页图。构建和浏览器检查记录见 notes/verification.md。

## 源码依据

- [config.yml](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/config.yml)
- [src/index.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/index.ts)
- [src/github.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/github.ts)
- [src/web.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/web.ts)
- [src/trending.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/trending.ts)
- [src/hn.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/hn.ts)
- [src/devto.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/devto.ts)
- [src/lobsters.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/lobsters.ts)
- [src/arxiv.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/arxiv.ts)
- [src/hf.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/hf.ts)
- [src/ph.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/ph.ts)
- [src/prompts.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/prompts.ts)
- [src/prompts-data.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/prompts-data.ts)
- [src/report.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/report.ts)
- [src/providers/index.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/providers/index.ts)
- [src/report-builders.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/report-builders.ts)
- [src/report-savers.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/report-savers.ts)
- [src/generate-manifest.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/src/generate-manifest.ts)
- [.github/workflows/daily-digest.yml](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/.github/workflows/daily-digest.yml)
- [mcp/src/index.ts](https://github.com/duanyytop/agents-radar/blob/dd2aaae700e2ebf62a7c80557c2bd64709be5e79/mcp/src/index.ts)

本研究文字与图为原创整理，源码链接固定到已核对版本。仓库 README 以 10 个采集类别描述来源，本报告按实现类型重新组织，区分来源类别、站点数和报告数。上游许可为 MIT。
