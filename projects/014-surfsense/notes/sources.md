# 来源、设计与验证记录

核对日期：2026-09-09。研究基线：`3448772bd3d5d439114f810ac5da8e5a86967917`。

## 一手依据

| 依据 | 对应结论 |
| --- | --- |
| [README](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/README.md) | 研究工作台、实时网络数据、成果生成、自动化、协作与当前成熟度声明 |
| [文件处理](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/tasks/document_processors/file_processors.py) | 内容提取、文件分类、视觉处理选择、后台处理与索引交接 |
| [切分器](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/indexing_pipeline/document_chunker.py) | 表格完整性、片段文本与行位置 |
| [索引流程](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/indexing_pipeline/indexing_pipeline_service.py) | 文档统一入库、内容标识、缓存与更新 |
| [混合检索](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/hybrid_search.py) | 语义和英文全文查询、RRF 常数 60、工作区过滤、片段按文档组织 |
| [重排序](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/reranking.py) | 重排序可选，未配置则保持结果 |
| [Agent 构建](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/agents/chat/multi_agent_chat/main_agent/runtime/factory.py) | 工具、子 Agent、模型和 MCP 依赖组装 |
| [Reddit 请求实现](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/proprietary/platforms/reddit/fetch.py) | 浏览器建立会话、HTTP 复用、代理和限流失败处理 |
| [MCP 服务](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_mcp/README.md) | 工具目录、托管与自托管模式、通过 REST 访问后端 |
| [部署配置](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/docker/docker-compose.yml) | PostgreSQL/pgvector、Redis、后台任务等组件 |
| [主体许可证](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/LICENSE) | 主体 Apache 2.0 与指定目录例外 |
| [BSL 许可证](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/proprietary/LICENSE) | 附加使用授权、商业服务限制及变更许可规则 |

## 展示实现

- 原创静态 HTML / CSS / JavaScript；无需第三方前端库、网络字体或远程图片。
- 深蓝侧栏与青色流程状态，五个 hash 导航视图，适配窄屏与减少动态效果偏好。
- 3 个场景、9 份教学资料；非来自实际公司、论文或社区的抓取样本。
- 8 组连接器示意，JSON 明确包含 `demo: true`；字段用于解释形状，并非保证与真实接口 schema 一致。
- 本地检索按问题中的显式主题词或资料标签与词段匹配。不生成真实语义向量，不伪造检索性能指标。
- 只有问题未更改时使用预先编写的教学归纳；自定义问题返回匹配原文。
- 资料或问题改变会清空旧结果，运行时锁定影响当前任务的控件，避免证据与结果错配。
- 引用弹窗使用原生 dialog，支持关闭按钮与 Escape；动态用户文本经过 HTML 转义。
- Markdown 下载保留教学性质与研究基线。

## 验证边界

本地 HTTP 返回、脚本语法、资源路径与项目清单/构建采用实际检查。未进行浏览器截图或点击测试，未部署原始 SurfSense，未进行模型调用、真实采集、负载测试或权限审计。

远程发布：当前会话没有可调用的 Sites 托管工具；展示保留在现有 GitHub Pages 项目结构，未将本地地址声称为远程部署成功。

## 本次检查结果

- 项目清单、README 同步与全站静态构建通过，包含 14 个子项目。
- JavaScript 语法、3 个预设问题、未知问题无匹配、空范围、排除资料、主题匹配、引用 ID 唯一性与 HTML 转义检查通过。
- HTML ID 与导航锚点、本地文件引用、架构图 SVG XML 和 4 个本地 HTTP 资源检查通过。
- 页面提供可选的 WebMCP 教学检索入口；当前没有可用的 WebMCP 浏览器验证上下文，未声称其注册和运行契约已验证。不支持的浏览器会忽略此入口。

## 2026-09-10 · 原有架构与后续强化

补充历史基线：[2025-08-29 README / 57d7c1c](https://github.com/MODSetter/SurfSense/blob/57d7c1c205fa9795bc8122a252a429c1d617528c/README.md)。该版本已经明确列出私人 NotebookLM/Perplexity 研究体验、研究 Agent、外部来源、RAG API、层级与混合检索、重排序及播客。由此修正“Agent、连接器、API 都是后来才加入”的错误划分。

- 总图左侧呈现原有能力主线，右侧呈现研究版本重点强化的实时平台、MCP、自动化等能力，底部为共用技术。
- 后续强化根据两个版本的能力描述对照，不主张每一项功能的精确首次发布日期。
- 图中具体处理组件与函数语义按研究版本源码整理，不声称现有实现全部存在于旧版本。
- 原理图同步输出 SVG 和 PNG，基于同一绘制脚本；PNG 已目视检查文字与连线布局。
- 首页改为架构图，新增能力—技术对照和历史依据；保留原有教学交互。

## 技术实现总图

新增 `technical-architecture.svg` 和同内容 PNG，展示：类型分派与解析器适配、统一返回接口、文本切分与向量化、文档/片段存储、混合检索与生成、Agent 控制、双向 MCP、缓存和增量计算。图中的文档字段为概念摘录，不是完整数据库 schema。

补充源码依据（固定研究版本）：

- [EtlPipelineService](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/etl_pipeline/etl_pipeline_service.py)：类型分派与解析服务路由。
- [直接转换器](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/tasks/document_processors/_direct_converters.py)：csv 与 markdownify。
- [EtlResult](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/etl_pipeline/etl_document.py)：Pydantic 统一接口。
- [Docling 封装](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/services/docling_service.py)：OCR、表格结构、Markdown 导出。
- [图片描述](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/etl_pipeline/picture_describer.py)：提取图片和插回描述。
- [音频转写](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/etl_pipeline/parsers/audio.py)：本地服务或 LiteLLM 转写。
- [解析缓存](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/etl_pipeline/cache/cached_extraction.py)、[向量缓存](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/indexing_pipeline/cache/cached_indexing.py)、[增量对比](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/indexing_pipeline/chunk_reconciler.py)：复用结果和片段。

技术图由独立绘图脚本生成，同源输出 SVG / PNG，已检查 PNG 的文字和图形布局。未进行上游运行或性能基准验证。

## 2026-09-10 · 对外理解汇总与引导图定稿

- 已将确认稿整理为 `notes/understanding.md`，正式引导图为 `web/assets/readme-guide.png` 和 `.svg`，生成源为 `experiments/draw-readme-guide.py`。
- 图文使用“初步检索：找出候选资料”解释“召回”，区分候选查找、重排和生成；数量示例不是实际默认参数。
- 总项目摘要与封面、子项目 README 已接入正式材料；保留组件架构与能力演进图供深入阅读。
- 已有实现与通用优化、备考建议分别标注；原始审阅草稿留在本地，不作为正式发布文件。
- 本次提交不表示已部署上游或完成真实模型测试，也不触发远程推送或发布。
