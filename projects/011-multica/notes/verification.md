# 本地运行验证 · 2026-09-09

## 结论

已启动 Multica 原版 Web、Go API、专用 PostgreSQL 与真实 Daemon；检测到本机 Codex 和 Claude Code。完成了一个真实文件生成任务，以及一个组长/成员通过评论事件协调的最小闭环。

这不是模拟 API、重绘界面或人工伪造的 Agent 结果。研究页中的逐步交互是讲解；本页列出的执行结果和截图来自原版实例。

## 已验证范围

| 项目 | 实际结果与证据 |
| --- | --- |
| 源码获取 | 完整 Git checkout 位于 upstream/，基线 9d36136 |
| 数据库 | 独立 PostgreSQL 18.1，5511 端口；执行上游迁移至 456 |
| 后端 | Go 1.26.6 构建，/health 返回 ok，监听 127.0.0.1:8111 |
| 前端 | 原版 Next.js 16.2.6，开发模式 localhost:3111；中文登录、看板、运行节点与任务页可用 |
| Daemon | 本机研究节点在线；自动发现 Claude 与 Codex 两种运行时 |
| 任务与取消 | LAB-1 保留失败、取消和换 Agent 后完成的三次运行记录 |
| 真实工具执行 | Claude Code 生成 hello-multica.txt，运行命令读回，发表评论并转待评审 |
| 小队协调 | LAB-2 中组长委派一次，成员回复，组长再次执行核对并转待评审 |
| 排队 | 执行员并发限制为 1；小队成员任务在其前一任务未结束时进入 queued |

## LAB-1：真实文件生成

第一次运行继承本机配置中的 gpt-6-astra，Codex CLI 0.152.1 返回“该模型需要更新版本 Codex”。平台记录为 failed / api_invalid_request。

将演示 Agent 配置为 gpt-5.5、low 后重试。任务能够读取 Issue、更新状态并开始文件修改，但停在 patch_apply，没有产出文件。约 5 分钟后由本次验证操作者主动取消。**此处仅确认本机该配置下的现象，尚未定位根因，不能泛化为所有 Codex 文件操作都不可用。**

随后手动把同一 Issue 改派给独立的 Claude 文件执行员，更新要求中的 Agent 名称，并创建新 Run。Claude Code 在约 36 秒内完成文件生成、命令读回、结果评论和待评审状态更新。平台没有自行决定切换供应商；改派是本次验证操作者的操作。

真实产物内容：

```text
Multica demo
Agent: Claude Code
17 * 23 = 391
```

产物位于 `runtime/local/workspaces/multica-lab-b22e1975b5c9/lab-1-643efbe91dc4/workdir/hello-multica.txt`，已另存一份到 `web/hello-multica.txt` 供查看。

SHA-256：`ef5035ad989940248089b257fcffe44c146acd6bd1dcb3dd96f6bc36a8c0f8bd`。

成功 Run：`01a0855f-3faa-73ec-97e2-643efbe91dc4`。

## LAB-2：组长与成员的真实交互

组长和成员都使用 Codex / gpt-5.5 / low。下面三条评论由 Agent 自己通过 Multica CLI/API 写入：

1. **16:48:38，组长委派**：带 `mention://agent/b470cedc-a355-41de-bd4b-d0771f71580f` 的结构化提及，请执行员计算 17×23 并给出分解过程。
2. **16:53:20，成员回复**：`17×(20+3) = 340 + 51 = 391`。
3. **16:54:03，组长收尾**：核对结果与过程，将任务转为待评审。

这三步对应三个不同的 Run：

| 执行 | Run ID | 结果 |
| --- | --- | --- |
| 组长首次委派 | 01a08559-d7e3-7dda-8bdc-b831b4cddcfc | completed |
| 成员执行 | 01a0855a-d6f4-7c4f-9b01-5a2fbb0a0941 | completed |
| 组长接收反馈后再运行 | 01a0855f-2596-7cce-bb34-96bf94635adf | completed |

成员任务在 16:48:38 入队，到 16:52:34 开始执行；中间在等待同一执行员的前一运行结束。组长收尾 Run 在 16:54:15 完成。时间为本地 Asia/Shanghai，仅用于说明本次时序，不是性能基准。

## 截图

- [运行节点](../web/assets/runtime-original.png)：一台机器内的 Claude 与 Codex 均在线。
- [文件产物](../web/assets/result-original.png)：原版任务评论里的读回内容及待评审状态变化。
- [小队交接](../web/assets/squad-original.png)：组长、成员、组长三段真实评论。

截图由浏览器直接获取，未重绘产品界面，保留原版标识。只包含本地演示身份与合成任务。

## 未验证或不作保证的范围

- 没有验证全部 26 种 Agent 工具，也没有进行大规模、多机或长时间稳定性测试。
- 没有实际接入 GitHub/飞书/Slack，没有创建 PR、推送代码或对外发消息。
- 没有验证定时 Autopilot、Webhook、插件、MCP 及企业权限边界；这些只做源码/文档说明。
- 本次使用开发模式；首次访问页面会进行编译，启动等待不等于生产页面响应速度。
- PostgreSQL 18.1 通过本次最小流程，但上游主要文档使用 17，不将此结果扩展为全部版本兼容性结论。
- Run completed 与 Issue 的人工验收分开。两项演示停在 in_review，保留给用户查看。

## 复现与本地变更

参考项目 README、start.ps1、stop.ps1。原版服务唯一代码补丁为支持 HOST 绑定，目的是将本机 API 限制在 127.0.0.1，补丁保存在 runtime/localhost-bind.patch。

未新增长期 PAT，Daemon 使用本地演示账户已有会话。环境配置、会话凭据、原始日志、数据库和 Agent 工作目录在忽略路径中；研究页不包含凭据，也未发布公共托管实例。
