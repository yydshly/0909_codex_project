# 011 · Multica Agent 协作与执行平台

> 调度 Codex、Claude Code 等 Agent 工具，以任务队列与事件反馈组织人机协作。

| 项目资料 | 内容 |
| --- | --- |
| 上游仓库 | [multica-ai/multica](https://github.com/multica-ai/multica) |
| 研究状态 | 已整理 |
| 研究版本 | `9d3613653e310bbbed5ae294efd8f405e3b722aa`（2026-09-09） |
| 上游许可 | Multica License，Apache 2.0 文本及额外条件 |
| 研究方式 | 源码分析、原版前后端本地启动、真实 Agent 最小任务验证 |

[← 总索引](../../README.md) · [完整理解回顾](notes/review.md) · [技术阅读补充](notes/understanding.md) · [运行验证](notes/verification.md) · [线上研究页](https://yydshly.github.io/0909_codex_project/projects/011-multica/)

本轮已补齐人工介入、评论触发、停止与重跑、评审与强制审批、顺序依赖与并行执行的区别，并将已有机制、实测证据和扩展建议分别标明。经用户确认，研究资料发布到 GitHub Pages；原版应用在本机运行。

## 整体介绍

**Multica → Agent 工具 → 模型。** Multica 的核心是统一工具适配、任务与执行管理、多 Agent 协调，以及人的派工、反馈和评审。组长决定“做什么、交给谁”，平台代码负责“入队、路由、领取、跟踪”，执行机器上的 Daemon 实际启动 Agent 工具。人工评审状态不等于底层强制审批关卡。

它支持事件触发和并发执行：独立任务可以并行，有依赖的步骤等待前序结果；并发受配置与执行资源约束。平台按需启动或续接 Agent，工具内部可多次调用模型，一次 Run 不等于一次模型请求。

![Multica 整体架构与小队交接](web/assets/architecture.svg)

[打开架构图](web/assets/architecture.svg) · [可缩放架构图](http://127.0.0.1:8011/diagram.html) · [完整回顾阅读页](http://127.0.0.1:8011/review.html) · [本机原版应用](http://localhost:3111/multica-lab/issues)

## 阅读与展示

1. 从整体图理解人的控制、平台执行架构、小队交接、价值与关键边界。
2. 在研究页点击“组长与成员交接”步骤，查看消息与事件流。
3. 打开原版应用，查看运行时、Agent、小队以及 LAB-1、LAB-2 的执行记录。
4. 阅读运行验证，区分已真实跑通的能力与仅经文档确认的功能。

图文源文件：`notes/review.md` 是完整回顾，`experiments/build_architecture.py` 生成 SVG；`experiments/build_review.py` 使用 Python Markdown 生成便于浏览的阅读页。本地执行这两个脚本只更新静态文件，不提交或部署。

研究页中的交互步骤是机制讲解；原版应用与截图来自本机运行实例。静态研究页不提供公共 Multica 服务。

## 本机启动与停止

```powershell
# 在本目录执行。环境已安装时，重复启动会跳过本项目已运行的进程。
.\start.ps1 -WithAgent

# 停止本项目服务，保留文件和数据库。
.\stop.ps1 -IncludeDatabase
```

| 服务 | 本地入口 |
| --- | --- |
| 研究页 | http://127.0.0.1:8011 |
| 原版 Web | http://localhost:3111 |
| 原版 API | http://127.0.0.1:8111/health |
| 专用 PostgreSQL | 127.0.0.1:5511，数据库 multica_demo |

演示用户为 `demo@multica.test`。这是本机合成测试身份，不会向真实邮箱发送邮件。若浏览器会话失效，输入邮箱后，使用本地 `runtime/local/config.json` 中的开发验证码登录。开发登录方式仅用于本地实例。

Daemon 使用独立配置名 `multica-research-011`，其配置位于用户目录下 `.multica/profiles/multica-research-011/`。使用已创建的本地会话凭据，不新增长期 PAT；过期后需重新登录并更新该演示配置。任务工作目录限定在 `runtime/local/workspaces/`，这不是操作系统沙箱。

## 获取源码与重新搭建

完整 Git 源码已保存在本机 `upstream/`（目录被外层 Git 忽略，避免复制巨大依赖及嵌套仓库）。重新获取时：

```powershell
git clone https://github.com/multica-ai/multica.git upstream
git -C upstream checkout 9d3613653e310bbbed5ae294efd8f405e3b722aa
git -C upstream apply ../runtime/localhost-bind.patch
```

本次采用本机安装的 Node 22.15.0、PostgreSQL 18.1、项目内 Go 1.26.6，以及 pnpm 10.28.2。上游主要文档和 CI 使用 PostgreSQL 17；本次 18.1 环境的最小验证不等于全部兼容性认证。

构建顺序：安装 Web 工作区依赖 → 构建 `server/cmd/server`、`server/cmd/multica`、`server/cmd/migrate` → 初始化专用 PostgreSQL → 在 `upstream/server/` 目录运行迁移 → 启动后端及 Next.js → 创建本地工作区并连接 Daemon。

```powershell
# upstream 目录内
npx --yes pnpm@10.28.2 --filter @multica/web... install --frozen-lockfile

# upstream/server 目录内（需要 Go 1.26.6）
go build -o ../../runtime/bin/multica-server.exe ./cmd/server
go build -o ../../runtime/bin/multica.exe ./cmd/multica
go build -o ../../runtime/bin/migrate.exe ./cmd/migrate
# 配好 DATABASE_URL 后，在此目录执行 ../../runtime/bin/migrate.exe up
```

`runtime/.env.example` 说明配置字段，启动器从本地未跟踪的 `runtime/local/config.json` 读取环境变量。真实配置、构建二进制、数据库和完整执行日志不进入研究页或外层 Git。

唯一上游代码改动：让后端通过 `HOST` 环境变量选择监听地址，本次设为 127.0.0.1。不设置 HOST 时保持上游原行为。补丁保存在 `runtime/localhost-bind.patch`；上游品牌及许可信息保持原样。

## 扩展价值与边界

- Skills：复用工作方法、参考资料及脚本。
- 插件、HTTP Hook、MCP：接入具体业务工具与界面。
- Provider：接入新的 Agent 执行工具。
- 进一步价值：围绕真实业务形成触发、执行、验收和反馈闭环，而非仅增加 Agent 数量。

本地执行不代表数据完全不出机器；云模型工具可能发送相关上下文。对第三方托管、商业嵌入及品牌修改需核对上游许可证。此次只启动本机实例，没有发布托管服务。

## 来源

[源码与能力依据](notes/understanding.md#7-源码阅读入口) · [上游自托管指南](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/SELF_HOSTING.md) · [许可证](https://github.com/multica-ai/multica/blob/9d3613653e310bbbed5ae294efd8f405e3b722aa/LICENSE)
