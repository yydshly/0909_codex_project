# 009 · Hugging Face Agent 开发课程

Hugging Face 的 Agent 开发课程与示例集：通过模型决策、工具执行和反馈循环，结合检索增强与状态编排，讲解 smolagents、LlamaIndex、LangGraph 的实现；适合学习工具调用、构建知识问答与多步骤任务原型，并通过评估改进效果。

[在线研究页](https://yydshly.github.io/0909_codex_project/projects/009-agents-course/) · [上游仓库](https://github.com/huggingface/agents-course) · [返回研究室](../../README.md)

![Agent 课程能力与技术总览](web/assets/overview.svg)

## 我们对仓库的理解

这是一套 Agent 教学资料、示例代码与实践项目，提供理解机制、选择框架和开发原型的路径。运行能力由所选模型、工具和框架共同实现；下载课程不等于获得完整业务应用。

## 能力与技术词

### 01 · 理解任务

- **LLM**：理解需求，生成回答或动作。
- **Messages**：组织用户、模型与工具消息。
- **System Prompt**：说明目标、规则和工具用法。
- **Chat Template**：转换为模型所需的对话格式。
- **Special Tokens**：标识角色、消息及调用边界。

### 02 · 决策与执行

- **ReAct**：交替决策、行动并观察结果。
- **Tool / Function Calling**：生成工具名和参数，由程序调用。
- **Tools**：封装函数、搜索与外部 API。
- **Code Execution**：运行模型生成的代码。
- **Memory / Context**：保留执行记录和任务上下文。

### 03 · 检索知识

- **Chunking / Embedding**：文档分块，再转换为语义向量。
- **Index / Retriever**：建立索引，检索相关内容。
- **RAG**：将检索资料交给模型辅助回答。
- **Agentic RAG**：按任务选择检索和其他工具。
- **QueryEngine**：LlamaIndex 的查询与回答组件。

### 04 · 框架实现

- **smolagents**：CodeAgent：用 Python 表达动作。
- **ToolCallingAgent / @tool**：结构化调用 / 注册自定义工具。
- **LlamaIndex**：数据接入、索引、查询与工作流。
- **LangGraph**：State / Nodes / Edges：状态与流程。
- **Workflows**：组织步骤、事件和执行逻辑。

### 05 · 组合与实战

- **Multi-Agent Systems**：多个 Agent 分工并汇总结果。
- **VLM / Vision Agents**：理解图片和页面截图。
- **Browser Agents**：结合浏览器工具与网页交互。
- **Agentic RAG 实战**：综合资料检索与外部工具回答。
- **Pokémon Agent**：在回合制对战中选择行动。

### 06 · 观测与改进

- **Observability / Tracing**：查看调用过程、结果和错误。
- **OpenTelemetry**：采集和传递运行追踪数据。
- **Token Usage / Latency**：观察模型用量与执行耗时。
- **GAIA / LLM-as-a-judge**：基准任务评测 / 模型辅助评分。
- **LoRA**：用于工具调用微调的低秩适配。

## 技术原理

任务、工具说明和历史结果交给模型 → 模型生成工具名与参数或代码 → 框架解析并执行 → 结果写回上下文 → 继续调用或给出答案。执行环境负责真实动作，循环需要结束条件、步数上限与错误处理。

RAG 将外部资料检索后提供给模型；Agentic RAG 让检索成为可选工具。检索可以基于关键词或向量，并非所有检索都依赖向量数据库。LangGraph 使用状态、节点和边组织流程；LlamaIndex 提供数据与事件驱动工作流组件。三个框架不要求同时使用。

## 使用场景

- **知识问答**：检索产品手册与故障记录，解释问题并列出依据。 使用 RAG + 检索工具；实际业务还需接入资料、权限过滤、来源引用。
- **资料调研**：搜索网页，阅读多个来源并整理比较结果。 使用 搜索 + 网页读取 + 工具循环；实际业务还需来源核验、抓取适配、结果格式。
- **数据分析**：查询订单数据，计算指标并解释变化。 使用 数据工具 + CodeAgent；实际业务还需业务数据接口、计算校验、运行隔离。
- **客服与文档流程**：识别请求、查询记录、生成回复草稿并转交审核。 使用 状态编排 + 工具调用；实际业务还需业务规则、人工审核、失败恢复。

以上业务应用是根据课程能力推导的开发方向，不是仓库已经交付的产品。直接用途为学习、框架比较和技术验证。

## 学习与扩展

1. **理解循环（Unit 1）**：解释一次“模型 → 工具 → 反馈”完整过程。
2. **实现工具（Unit 2 · 先选一个框架）**：独立接入一个工具，验证参数和失败处理。
3. **接入资料（Unit 3）**：完成带来源的知识问答，检验检索是否命中。
4. **评估再扩展（Unit 4 + Bonus）**：固定一组真实任务，记录完成率、耗时和用量。

可按需要继续学习多 Agent、视觉与浏览器交互和微调；业务系统需进一步设计资料权限、长期记忆、任务恢复、评估数据与成本控制。这些属于扩展建议。

## 术语边界

- Memory / Context：这里指运行记录与任务上下文，不承诺长期记忆。
- GAIA：评测基准；课程最终项目使用其子集。
- OpenTelemetry：可观测性标准与工具生态，不是评分模型。
- LLM-as-a-judge：模型辅助评估方法，不能替代全部人工与业务校验。
- LoRA：微调方法；SFTTrainer：训练工具，二者不属于应用能力。

## 来源与验证范围

上游快照：[8c0832eae634ebb34541c65265caa6da4c5d2c57](https://github.com/huggingface/agents-course/tree/8c0832eae634ebb34541c65265caa6da4c5d2c57)，提交日期 2026-06-28；资料核对日期 2026-09-09。研究状态：已整理。

本次阅读官方课程和示例代码，验证研究网页、导航与静态构建；没有运行全部上游模型示例或 GAIA 实验。图为原创研究说明图，不是上游产品截图。

- [仓库目录与定位](https://github.com/huggingface/agents-course)
- [Agent 的决策—行动—观察循环](https://huggingface.co/learn/agents-course/en/unit1/agent-steps-and-structure)
- [smolagents 能力与模块](https://huggingface.co/learn/agents-course/en/unit2/smolagents/introduction)
- [CodeAgent 执行机制与代码](https://huggingface.co/learn/agents-course/en/unit2/smolagents/code_agents)
- [LlamaIndex 数据与检索组件](https://huggingface.co/learn/agents-course/en/unit2/llama-index/components)
- [LangGraph 状态与流程结构](https://huggingface.co/learn/agents-course/en/unit2/langgraph/building_blocks)
- [Agentic RAG 原理与实战](https://huggingface.co/learn/agents-course/en/unit3/agentic-rag/agentic-rag)
- [GAIA 子集最终项目](https://huggingface.co/learn/agents-course/en/unit4/introduction)
- [观测与评估](https://huggingface.co/learn/agents-course/bonus-unit2/introduction)
- [工具调用微调](https://huggingface.co/learn/agents-course/bonus-unit1/introduction)
- [Pokémon 游戏 Agent](https://huggingface.co/learn/agents-course/bonus-unit3/introduction)

## 页面维护

网页不依赖外部脚本或字体。修改 `experiments/build_page.py` 后执行该脚本可同步生成网页正文、SVG 总览和本研究记录；样式位于 `web/style.css`。
