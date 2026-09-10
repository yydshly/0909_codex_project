# SurfSense：从多格式资料到有依据的研究与生成

SurfSense 将多格式资料接入、内容解析、知识库检索和大模型生成组织成可自行部署的研究平台，提供 NotebookLM 式的资料问答、引用与内容生成体验，并扩展到实时网络数据、REST/MCP 工具接入和自动化研究。它的可复用价值，是把“资料如何进入系统、如何被找到、如何成为模型的回答依据”串成一条可检查、可改造的技术链路。

本研究围绕三个问题展开：**资料如何变得可检索？Embedding 与 RAG 分别负责什么？如何从资料问答进一步走向备考学习？**

![SurfSense 理解引导图：资料入库、检索生成与学习扩展](../web/assets/readme-guide.png)

[查看矢量图](../web/assets/readme-guide.svg) · [上游项目](https://github.com/MODSetter/SurfSense) · [详细研究记录](../README.md) · [本地教学页面](../web/index.html#architecture)

**引导图 V2 阅读顺序：**先看绿色入库链路及 A 原文、B 语义向量、C 全文词项三种用途，再看蓝色查询链路如何从 B/C 找出候选资料并回到 A 取证据。右侧解释核心概念与技术选项，底部说明数据更新、质量验证和备考扩展。图中“通用优化”和紫色部分为建议方案，不代表全部已由 SurfSense 实现。图已输出 2400 × 2680 PNG 与 SVG。

## 一条主线，两种执行时机

**入库阶段，在资料新增或更新时执行：**接入文件或外部资料，按格式提取内容，再切分为片段，生成 Embedding，并保存原文、向量和来源关联。解析与索引缓存、增量处理可以减少重复工作；初次处理仍需要承担解析和模型计算成本。

**查询阶段，在用户提出问题时执行：**限定资料范围，搜索候选内容，融合排名，按配置重排，再把相关原文与问题组织进模型上下文，由大模型生成回答、报告或其他内容，并关联引用。

这两条链路解释了为什么资料通常只需先入库，后续可以反复提问。这里的“入库”不等于把资料重新训练进大模型参数。

## Embedding、索引、RAG 的区别

| 概念 | 职责 | 产物或效果 |
| --- | --- | --- |
| 解析与 OCR / 转写 | 从文档、扫描页、音频等提取内容 | 可进一步处理的文本、表格或描述 |
| 切块 Chunking | 将长资料拆为可独立检索的单元，尽量保留语境 | 文本片段及其文档关联 |
| 元数据 Metadata | 记录文档、位置、版本、范围与权限等信息；字段依实现而定 | 过滤、更新与引用的依据 |
| Embedding | 将文本编码为语义向量 | 一组用于相似度比较的数字 |
| 索引 | 为内容建立查找结构 | 全文索引、向量索引等 |
| 混合检索 | 综合关键词与语义查找 | 多路候选资料 |
| RRF | 按各路排名融合结果 | 综合候选排序 |
| Reranker | 对问题与候选内容重新判断相关性 | 精选后的排序；需配置相应模型 |
| 上下文组装 | 组织资料原文、来源、问题与生成要求 | 大模型可接收的输入 |
| RAG | 检索增强生成：检索资料、组装上下文、基于资料生成 | 有外部资料支撑的回答 |

**Embedding 负责表示，索引负责查找，RAG 负责把检索与生成串起来。**

例如，用户问“植物如何利用阳光制造养分”，语义检索可以尝试找到写着“光合作用”的教材片段，即使措辞不完全相同。问题与资料需要使用兼容的向量编码方式；找到片段后，系统通常把对应原文交给生成模型，检索向量本身不充当教材原文。

向量相近只意味着可能相关，不保证资料正确或足以回答。RAG 也不限于向量搜索，可以使用全文搜索、数据库查询或多种检索方式结合。

## “召回”是什么意思？

召回是检索领域的术语，表示**从全部资料中先找出一批可能相关的候选内容**。引导图使用“初步检索：找出候选资料”表达这一环节。

例如，一份教材切成 1,000 个片段：先通过关键词和向量查找得到 30 个候选，再重排选出 5 个有用片段，最后把原文与问题交给生成模型。这些数量仅为示意，不是 SurfSense 的固定参数。

初步检索重点是少漏掉有用证据，重排重点是在候选中精选。关键资料若未进入候选集，后面的重排就没有机会选中它。“召回率”是另一种评估说法：在已标注的相关资料中，有多少被找回；它不等于答案正确率。

## SurfSense 已核对的实现与通用扩展

| 层次 | 本研究核对的 SurfSense 实现 | 可进一步研究的通用技术 |
| --- | --- | --- |
| 资料解析 | 类型分派、解析器适配；按配置使用 Docling 等服务、OCR、视觉描述与音频转写 | 针对扫描质量、公式与复杂表格的质量检查 |
| 知识入库 | 文本切分、Embedding、文档与片段存储、缓存及增量处理 | 父子块组织、按学科优化切分与元数据 |
| 检索 | PostgreSQL/pgvector 向量查询与 PostgreSQL 全文查询，RRF 融合，可选重排 | 查询拆解、同义词扩展、邻接片段补齐、召回评估 |
| 上层应用 | 引用问答、报告、播客、演示等生成；实时连接器、REST/MCP 与自动化 | 面向特定行业或学习任务的流程和交互 |

核对的混合检索代码使用 pgvector 余弦距离、PostgreSQL `ts_rank_cd` 全文排序与常数为 60 的 RRF。**不能把它写成 BM25 实现。**该路径使用 `english` 全文配置，中文资料的分词与召回效果需要单独验证。

HNSW、IVF 是常见的向量搜索加速技术；BM25 是常见的词项相关性排序方法。它们属于技术选项，本文不因使用 pgvector 或全文查询就推断某一种索引或算法已在当前部署启用。

## 产品定位与备考扩展

SurfSense 参考 NotebookLM 式的资料研究体验，通过可配置模型和可自行部署的系统实现相关能力；它不代表复现了 Google 未公开的内部算法。历史版本已经包含研究 Agent、外部来源、RAG API、混合检索、重排与播客，不能将这些全部归为后来才新增的能力。当前版本进一步强调实时平台数据、MCP 和自动化研究。

相关项目可以按职责选择：

| 项目 | 值得研究的部分 |
| --- | --- |
| [Open Notebook](https://github.com/lfnovo/open-notebook) | NotebookLM 类应用、多模型接入、资料问答与播客 |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 桌面知识库、文档问答与 Agent 工具 |
| [RAGFlow](https://github.com/infiniflow/ragflow) | 文档解析、可观察的切块与检索流程 |
| [Dify](https://github.com/langgenius/dify) | 知识库与自定义 AI 工作流 |
| [LlamaIndex](https://github.com/run-llama/llama_index) / [Docling](https://github.com/docling-project/docling) | 可嵌入应用的检索框架 / 文档解析组件 |
| [RemNote](https://www.remnote.com/) | 资料与笔记如何衔接记忆卡、测验和复习 |

对备考而言，“找到相关段落”并不保证“覆盖全部考点”。建议在通用 RAG 之上增加：

**考纲拆解 → 逐项对应资料与检查遗漏 → 分层讲解 → 出题与评分 → 错题反馈和复习安排。**

这是一条建议扩展路线，不是已在本子项目实现的学习系统。验证时应分别检查：正确资料是否被召回、关键证据是否进入上下文、回答是否忠于证据，以及考纲覆盖和学习效果。

## 研究范围与依据

研究基线：SurfSense `3448772bd3d5d439114f810ac5da8e5a86967917`；整理日期：2026-09-10。本文是源码与官方说明研究，未部署上游后端，也未进行真实模型质量或性能对比。本地教学页面使用预置资料与关键词匹配，不是真实向量检索服务。

自部署的实际成本与数据流向取决于模型、解析服务、连接器和服务器配置。主体 Apache 2.0 与指定目录的 BSL 1.1 应分别理解，不能将整个仓库概括为无附加限制的 Apache 2.0 项目。

- [上游 README：能力与定位](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/README.md)
- [历史 README：早期已有能力](https://github.com/MODSetter/SurfSense/blob/57d7c1c205fa9795bc8122a252a429c1d617528c/README.md)
- [混合检索源码](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/hybrid_search.py) / [可选重排](https://github.com/MODSetter/SurfSense/blob/3448772bd3d5d439114f810ac5da8e5a86967917/surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/reranking.py)
- [完整解析、索引、缓存与许可来源](sources.md)
- [RAG 概念](https://developers.llamaindex.ai/python/framework/understanding/rag/) / [切块策略](https://docs.langchain.com/oss/python/integrations/splitters/index)
- [向量搜索与索引](https://github.com/pgvector/pgvector) / [检索与重排模型分工](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
