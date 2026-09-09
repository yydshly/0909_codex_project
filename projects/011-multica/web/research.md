# Multica：从任务看板到 Agent 执行编排

本文保留技术阅读基础；涵盖后续人工控制讨论、全部问题回顾与证据分级的版本见 [完整理解与回顾](review.md)。

研究日期：2026-09-09。源码基线：`9d3613653e310bbbed5ae294efd8f405e3b722aa`。本页是源码与官方文档研究，运行结果另见 verification.md。

## 1. 我们形成的共同理解

Multica 是已有 Agent 工具之上的任务协作与执行编排平台。它主要调度 Codex、Claude Code、Kimi 等完整 Agent 工具；Agent 再调用各自配置的模型进行推理，并操作文件、命令和外部工具。

调用关系：**Multica → Agent 工具 → 模型**。模型选项、推理强度等可以经 Multica 配置传给工具，但不等于 Multica 直接作为模型 API 网关或自动模型负载均衡器。

可以拆成三项核心能力：

1. **统一工具适配**：不同工具的启动、流式消息、取消、续接及用量，包装成统一执行接口。
2. **任务与执行管理**：任务记录、队列、运行节点路由、状态、故障恢复、结果追踪。
3. **多 Agent 协调**：组长决定分工，平台通过评论事件将决策转成新的执行任务。

## 2. 谁在调度？两种职责

| 角色 | 决定什么 | 实现方式 |
| --- | --- | --- |
| 人或组长 Agent | 做什么、交给谁、下一步是什么 | 人工操作或模型根据任务和成员能力作判断 |
| Multica 平台 | 任务如何入队、路由、领取、记录状态 | Go 服务、数据库队列、事件处理器 |
| 执行节点 Daemon | 准备目录和配置、启动工具、收集输出、处理进程生命周期 | 执行机器上的本地守护进程 |
| Agent 工具 | 读什么文件、调用什么工具、如何完成任务 | 自身的模型与工具执行循环 |

“按 Agent 关联的运行环境路由”不应直接称为自动选择最空闲机器或最便宜模型的负载均衡。

平台不是固定串行流水线：独立任务或成员可并行，有依赖的步骤等待结果，受 Agent/Daemon 并发配置、节点容量和目录锁约束。本次单成员交接展示的是依赖顺序，未单独做并行负载实验。平台按需启动或续接 Agent，工具内部可能多次调用模型；一次 Run 不等于一次模型调用。详见完整回顾第 4.1 节。

## 3. 整体架构

Web（Next.js）和 Desktop（Electron）共享业务组件；iOS 使用 Expo / React Native。Go 服务使用 Chi、sqlc 和 WebSocket。PostgreSQL 保存业务状态，Redis 为可选的跨实例实时通信等设施。

前端/API → Go 服务 → PostgreSQL 持久任务队列 → Daemon 领取 → Provider 适配层 → 本地 Agent 工具 → 模型及文件/命令工具。

执行进度、错误与结果沿反向链路回传。WebSocket 提供及时通知和 Daemon RPC，轮询路径帮助断线后继续获取工作。队列领取 SQL 使用 `FOR UPDATE SKIP LOCKED` 避免并发领取者争抢同一行。

**Issue 与 Run 分开**：Issue 是持续存在的目标、讨论和验收状态；Run 是一次执行，一个 Issue 可以对应多次 Run。Run completed 不是业务验收完成。

## 4. 组长与成员如何交互

1. 用户将 Issue 分配给 Squad，平台给 Leader 创建 Run。
2. 领取时注入组长协作协议、成员名单/角色/Skills，以及小队自定义指令。
3. 组长使用 CLI/API 在任务中发表委派评论。接收者采用 `[@Name](mention://agent/UUID)`，普通 `@名字` 不等价。
4. 服务端解析提及，检查权限及触发规则，为目标成员创建 Run。
5. 组长记录本轮决策后结束执行，不持续占着一次模型调用等待。
6. 成员独立执行，读取任务和相关讨论，将结果与产物位置写回任务。
7. 评论或其他符合规则的活动唤醒组长；组长再次评估，继续委派、请求人工介入或转入待评审。

共享的是任务与讨论记录，不是各模型的隐式推理或完整会话。代码文件也不会仅因发表评论自动同步到其他机器；跨工作目录或机器的交接需要分支、PR、附件等明确产物。

去重与自触发抑制减少重复执行，不能据此承诺任意复杂协作都不会循环。创建 Squad 不会自动同时启动所有成员，也不自动提高机器并发上限。

## 5. 已有能力与可扩展方向

已有：Issue/项目/成员管理，多种 Agent 工具，Skills，小队，聊天和提及触发，Autopilot 定时及 Webhook，运行历史、取消和重试，Git/消息渠道集成，自托管和插件机制。

插件示例已经包含自定义 Issue 面板、HTTP Hook、事件/定时触发、Agent 工具、外部 MCP 服务及 Skill。Skills 是复用工作方法；插件/MCP 是连接工具与业务；Provider 是接入新的执行工具。

以下是本研究的扩展建议，不是官方已完成清单：

| 扩展 | 可交付价值 |
| --- | --- |
| 业务系统连接 | 工单、CRM、内部数据库、发布平台形成具体场景 |
| 可执行验收 | 测试、证据、审批成为流程中的可检查条件 |
| 知识与经验积累 | 历史任务与评审可检索，形成可审核 Skills |
| 效果和成本路由 | 用成功率、返工率、耗时、费用指导分配 |
| 执行环境管理 | 临时容器/虚拟机、资源限额、限定凭证及网络 |

价值衡量应采用完成率、人工介入次数、返工率、耗时和成本。多 Agent 数量本身不是收益。

## 6. 边界

- Multica 的工程价值集中于工具适配与可靠协作，智能执行能力主要来自所接入的 Agent。
- 本地执行不等于数据全不出机器：执行记录会回平台，云模型工具可能将相关上下文发给模型服务。
- Daemon 的工作目录隔离不等于操作系统安全沙箱。默认运行权限取决于 Daemon 所属系统用户。
- 许可证为 Multica License（Apache 2.0 文本加额外条件）。内部使用与对第三方托管、商业嵌入、品牌变更的条件不同；商业路线需核对原文。

## 7. 源码阅读入口

基线链接均固定到本次 Commit：

- [统一 Backend 接口](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/pkg/agent/agent.go)
- [Daemon](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/internal/daemon/daemon.go)
- [任务创建](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/internal/service/task.go)
- [组长协议和上下文](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/internal/handler/squad_briefing.go)
- [评论事件路由](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/internal/handler/comment.go)
- [成员反馈唤醒组长测试](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/server/internal/handler/squad_worker_comment_wakes_leader_test.go)
- [官方架构](https://multica.ai/docs/developers/architecture) · [安全模型](https://multica.ai/docs/security-model)
- [插件示例](https://github.com/multica-ai/multica/tree/9d3613653e310bbbed5ae294efd8f405e3b722aa/examples/plugins) · [许可证](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/LICENSE)
