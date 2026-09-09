# MetaGPT：源码、运行证据与扩展方式

研究版本：`11cdf466d042aece04fc6cfd13b28e1a70341b1f`，2026-09-09。上游源码完整克隆在子项目 `upstream/`，未改动。[返回演示](index.html)

## 库的实际能力

MetaGPT 提供把任务分给多个角色、交换消息和执行工具的基础。软件开发是主要场景，库中也有数据分析、研究、教学、客服等专用角色。框架负责组织执行；规划和内容生成通常需要模型，文件、浏览器或终端等操作需要相应工具和运行环境。

## 我们形成的核心理解

**MetaGPT 是组织多个 Agent 协作的框架。提示词定义工作方式，工具提供实际操作，框架负责消息投递和执行。**

| 层面 | 负责什么 | 不能由它单独保证什么 |
| --- | --- | --- |
| 大模型 | 理解、推理、生成内容或工具调用参数 | 不能仅靠生成文字完成文件修改、测试或部署 |
| 提示词与上下文 | 角色职责、工作方法、约束、输入资料 | 不会凭空增加模型能力，也不等于重新训练模型 |
| Action / 工具 | 读写文件、运行代码、检索、操作外部服务 | 工具可调用不等于调用正确或业务结果合格 |
| Role / 记忆 | 保存角色状态、观察消息、选择动作并保留结果 | 角色名称不代表它已具备对应岗位的完整能力 |
| Team / Environment | 组队、循环、路由和异步执行 | 不自动保证任务被合理拆分或软件交付成功 |
| 验收机制 | 用实际测试和业务标准判断产物 | 不能只凭 Agent 自报“已完成”认定成功 |

同一个模型可以服务多个角色，角色之间主要通过提示词、上下文、记忆、动作和工具配置形成差异。一个 Agent 通常是有状态的程序对象，不必对应一条独立线程，也不必对应一个不同的模型。

## 两种协作方式如何调度

### 固定交接：程序预先规定触发关系

`用户需求 → 产品 → 架构 → 项目管理 → 开发 → 测试 → 失败返修 / 通过结束`

基础环境先依据消息的 `send_to` 投递到收件箱，角色再通过 `_watch` 与消息的 `cause_by` 判断是否关注。地址路由与事件关注是两个步骤。例如本实验开发角色监听 `PlanWork` 和 `TestsFailed`，分别意味着初次开发和返修。一次交接不需要负责人模型决定接收人。

环境每轮遍历当前非空闲角色，收集 `role.run()` 协程并通过 `asyncio.gather()` 运行。新消息让后续角色具备执行条件；具体交接受运行轮次和消息可见时机影响。这是异步协作机制，不是为每个岗位常驻创建线程。

### 动态分派：负责人借助模型选择执行人

`用户目标 → TeamLeader 读取成员职责与进度 → 模型选择成员和任务 → 工具发送消息 → 成员执行 → 反馈负责人`

负责人提供真实方法 `publish_team_message(content, send_to)`。模型给出要交接的内容和成员名，程序调用方法，环境完成投递。模型决定“工作交给谁、做什么”，程序执行“如何投递、何时运行”。[TeamLeader 源码](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/roles/di/team_leader.py)

任务计划中的负责人、依赖和完成状态帮助组织工作，但这些数据本身不会启动线程，也不能替代消息投递与业务验收。角色也不必每一步都调用模型：单一固定动作可以直接运行，需要推理时才发起模型请求。

## 谁调度谁

1. `Team` 装配成员、注入用户任务并驱动环境循环。
2. `Environment` 根据消息接收地址分发消息，再异步运行角色。它不是为每个角色分配一条常驻操作系统线程。
3. 基础 `Role` 读取自己的消息队列，以 `_watch` 关注的动作类型筛选消息，保存记忆，选择并执行动作，发布结果。
4. 固定流程可以让每个角色只绑定一个动作；也可以让角色从多个动作中选择。`RoleZero` 提供更通用的工具选择和执行循环。
5. 当前默认 MGX 软件团队使用 `MGXEnv` 和 `TeamLeader` 协调成员。负责人判断任务与交接对象，底层程序仍负责投递和实际运行。

架构依据：[Team](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/team.py)、[Environment](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/environment/base_env.py)、[Role](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/roles/role.py)、[MGXEnv](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/environment/mgx/mgx_env.py)、[RoleZero](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/roles/di/role_zero.py)。

## 怎样定制专用 Agent

一个专用 Agent 需要确定职责、输入、动作、触发方式和交付标准。提示词只覆盖其中的职责和推理约束，不能替代工具实现及验收。

本项目的开发角色是一个具体例子：

| 配置项 | 实验内容 |
| --- | --- |
| 职责 | 交付优惠金额计算器 |
| 输入 | 任务拆分结果或测试失败消息 |
| 触发 | 监听 `PlanWork` 与 `TestsFailed` |
| 执行 | `ImplementCalculator.run()` 写入代码文件 |
| 交付 | 代码路径与 `ImplementCalculator` 消息 |
| 验收 | 测试角色启动真实 Python 子进程，运行 8 个测试 |
| 返修 | 失败消息重新激活开发角色；修复规则为本实验预编写 |

改造为真实智能开发角色，需要把固定代码交付换成模型生成/修改，将仓库上下文和测试错误提供给模型，同时保留实际工具执行与验收。增加 Agent 数量不会自动提高成功率，分工与输入输出契约同样重要。

## 内置角色目录

目录来自本版本源码的 AST 提取。统计范围是 `metagpt/roles` 与 `metagpt/ext` 下的 27 个具体角色实现，排除 `Role`、`RoleZero`、`BasePlayer` 等基类及示例目录；不同目录有不同用途，不能视为一支默认团队。[机器可读目录及逐项源码链接](assets/agents.json)

| 分组 | 角色 |
| --- | --- |
| 默认软件团队 5 个 | TeamLeader、ProductManager、Architect、Engineer2、DataAnalyst |
| 可选角色 13 个 | ProjectManager、Engineer、QaEngineer、SWEAgent、DataInterpreter、Researcher、Searcher、Sales、CustomerService、InvoiceOCRAssistant、Teacher、TutorialAssistant、Assistant |
| 场景扩展 9 个 | AndroidAssistant、Experimenter、STRole、Moderator、Werewolf、Villager、Seer、Witch、Guard |

默认团队依据：[software_company.py](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/metagpt/software_company.py)。角色目录表示源码存在，不代表全部配置完成或已在本机验证。

## 本次实际验证

实验使用原版 `Team(use_mgx=False)`、`Environment`、`Role`、`Action` 和消息记忆机制。自定义 5 个基础角色绑定固定动作。没有调用内置软件团队；没有模型推理。

- 实际产生 8 条事件：需求、需求文档、设计、任务拆分、首版代码、测试失败、修正版代码、测试通过。
- 首版缺陷预设为“先打折再减券”，组合优惠测试失败，得到 70.00 而非 72.00。
- `TestsFailed` 消息被开发角色观察到，执行预编写修复，回归 8/8 通过。
- 框架进入空闲状态；禁止模型调用的适配器记录为 0 次。事件顺序与测试结果都有程序断言。
- 已通过网页点击重新执行，产生新的运行编号；计算功能实际执行最新产物，并得到 72.00。

[原始运行记录、测试输出和文件内容](assets/run.json)。网页播放用于回看这份记录；本机“重新运行协作”启动新的 Python 框架进程。

尚未验证：默认 MGX 团队的模型分派、内置开发角色自动生成、真实项目交付质量、LanceDB 检索。故本实验不能作为“AI 自动完成软件研发”的成功率证据。

## 复现

在 `projects/012-metagpt` 目录使用 PowerShell：

```powershell
./runtime/setup.ps1
.venv/Scripts/python.exe -X utf8 experiments/serve.py
```

访问 `http://127.0.0.1:8122`。安装脚本需要 Git 和 uv，使用 Python 3.10、固定源码提交与依赖快照。上游锁定的 LanceDB 0.4.0 缺少 Windows wheel，安装覆盖为 0.14.0；上游源码不变，相关检索 API 未测试。依赖检查也会报告这一个明确的版本偏离。完整环境较大，首次下载和安装需要时间。

单独运行框架：

```powershell
.venv/Scripts/python.exe -X utf8 experiments/run_demo.py
```

接入模型运行库内置的数据分析角色，先在本机填写配置模板：

```powershell
Copy-Item runtime/model.example.yaml runtime/config2.yaml
.venv/Scripts/python.exe -X utf8 experiments/live_demo.py --config runtime/config2.yaml
```

该入口准备了虚构销售数据，请求原版 DataInterpreter 生成分析报告和图表。目前没有可用模型配置，尚未实际执行。配置与结果在被忽略的本机目录中，网页不接收密钥。此模式会调用模型并执行模型生成的代码。

## 向上扩展的产品方向

以下是基于源码能力的产品推演，不是库开箱即用的功能清单。

| 目标产品 | 可复用基础 | 还需要补齐 |
| --- | --- | --- |
| 需求到原型工作台 | 产品、架构、开发角色 | 页面预览、项目模板、验收、部署与版本管理 |
| 研发任务协作助手 | TeamLeader、工程师、测试角色 | 现有仓库接入、代码审查、CI、权限和失败恢复 |
| 自动测试与修复服务 | 消息闭环、代码执行、测试角色 | 真实问题复现、稳定测试、变更风险控制 |
| 数据分析交付工具 | DataInterpreter、DataAnalyst | 数据连接器、指标定义、报告模板、数据权限 |
| 行业流程助手 | 角色、动作、消息与工具扩展 | 领域数据、操作接口、审核节点和质量评价 |

本实验适合作为可观察的任务协作工作台起点：先让输入、交接、产物和验收可检查，再逐步替换固定动作、接入模型。

## MetaGPT 与 Atoms 的关系

固定版本的 MetaGPT README 宣布了自然语言编程产品 MGX（MetaGPT X）。Atoms 当前官网展示 AI 团队、应用构建、托管等面向用户的产品功能，同时列出 MetaGPT 研究与团队开源项目。它们存在团队与技术路线上的关联；不能据此推断 Atoms 的全部线上功能、部署设施或最新内部实现都包含在这个开源提交中。[上游产品公告](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/README.md)、[Atoms 官网，核对于 2026-09-09](https://atoms.dev/zh)

使用 MetaGPT 库意味着自行配置模型、角色、工具、环境和产品界面；使用 Atoms 则是在使用已封装的在线产品。本实验没有验证 Atoms 的内部调度实现，不能把官网产品描述当作开源运行证据。

## 线上与本机边界

发布入口：[MetaGPT 软件团队实验室](https://yydshly.github.io/0909_codex_project/projects/012-metagpt/)。GitHub Pages 提供架构、完整理解、27 个角色目录、运行记录回放和产物下载。线上不会启动 Python 或访问本机配置，重新运行与试算按钮会明确禁用。本机访问 `http://127.0.0.1:8122` 可以执行协作与计算。

## 来源与许可

上游：[MetaGPT](https://github.com/FoundationAgents/MetaGPT)，[MIT 许可证](https://github.com/FoundationAgents/MetaGPT/blob/11cdf466d042aece04fc6cfd13b28e1a70341b1f/LICENSE)，Copyright 2024 Chenglin Wu。图示、网页、固定动作实验与文字说明为本子项目制作。产品方向为本项目推演。
