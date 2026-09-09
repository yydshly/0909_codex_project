# 010 · Invidious 能力与架构分析

> 自建 YouTube 观看入口与数据 API：获取并整理 YouTube 内容，以独立界面播放，管理自己的账号、订阅和历史。

| 项目资料 | 内容 |
| --- | --- |
| 上游仓库 | [iv-org/invidious](https://github.com/iv-org/invidious) |
| 研究状态 | 已整理（源码分析，未运行验证） |
| 主仓库 Commit | `049d591d294e2a43cb32b97a0bb018c2093e5beb` |
| 声明版本 | `2.20260804.1-dev` |
| 上游许可证 | `shard.yml` 声明 AGPL-3.0-only |
| 分析日期 | 2026-09-09 |
| Companion 依据 | 当日官方 master 源码，未固定到与主服务共同验证的版本 |

[← 返回总索引](../../README.md)

## 一图理解能力与架构

![Invidious 能力与架构理解图：内容来自 YouTube，主服务组织网页和 API，数据库保存用户状态，Companion 处理播放](web/assets/overview.png)

[查看矢量原图](web/assets/overview.svg) · [下载 PNG](web/assets/overview.png) · [网页源码](web/index.html)

读图顺序：上排看五组能力；中间看浏览器、主服务和 YouTube 的分工；下排看数据库与 Companion。实线表示服务请求和数据读写，虚线概括媒体直连或经代理的传输路径。多个主服务模块不是多个独立部署单元。

这是根据源码原创绘制的理解图，不是运行截图。网页提供搜索、播放、订阅三个可切换的说明流程，不会请求真实 YouTube 内容。网页与图在本地完成检查，尚未发布到线上。

## 我们最终澄清的六个问题

| 问题 | 理解结论 |
| --- | --- |
| 是通过 YouTube 接口封装后展示吗？ | 是，还包含独立用户数据、缓存、后台刷新以及 Companion 播放链路。 |
| 内部接口意味着内部员工开发的吗？ | 不是。它指客户端使用的接口，可以观察请求并分析协议。 |
| 我们能查到 API 吗？ | Invidious 有公开 API 文档；项目源码也公开了对 YouTube 的调用实现。 |
| 视频源能随意设置吗？ | 没有通用视频源开关，当前围绕 YouTube 实现。 |
| 自己部署就有了自己的视频库吗？ | 有自己的入口和账号数据，视频内容仍来自 YouTube；不是上传托管与全量归档。 |
| 能搜索就一定能播放吗？ | 不能。搜索、播放信息获取、媒体传输是不同链路，可能分别失败。 |

## 1. 它是什么

Invidious 是一套可部署的 Web 应用，也对外提供 HTTP API。用户打开实例网站，搜索、观看和订阅 YouTube 内容；开发者可以调用实例的 API，在自己的应用中展示内容。

它的能力可以概括为：YouTube 内容获取和解析 + 自己的网页与播放器 + 独立用户数据 + 对外 API + 播放适配和代理。

“内部接口”指 YouTube 网页或 App 使用的接口，不代表开发者具有内部员工身份。协议可以通过客户端行为分析了解，项目公开了自己的调用实现。它没有使用官方面向第三方的 YouTube Data API，因此通常不需要使用者申请该 API 的 Key；仍受 YouTube 服务行为和访问限制影响。

## 2. 能力及数据归属

| 能力 | 实际内容 | 来源或存储位置 |
| --- | --- | --- |
| 搜索 | 视频、频道、播放列表及过滤条件 | 全站搜索主要请求 YouTube；订阅内搜索查询实例数据库 |
| 频道浏览 | 视频、Shorts、直播、播放列表、社区等入口 | YouTube；可用程度取决于上游响应 |
| 视频信息 | 标题、作者、描述、时长、封面、播放格式等 | YouTube，部分信息缓存到 PostgreSQL |
| 播放 | 普通视频、音频模式、DASH、直播相关路径 | 视频仍来自 YouTube；主服务与 Companion 配合 |
| 字幕与评论 | 字幕、文字稿、YouTube 评论，另有 Reddit 评论来源 | 依赖外部服务；不自带语音识别或 AI 总结 |
| 下载和嵌入 | 视频嵌入页面及下载入口 | 当前 Companion 配置下下载走 Companion；管理员可以禁用 |
| 用户账号 | 登录、偏好、历史、订阅、本地播放列表 | Invidious 实例数据库 |
| 更新聚合 | 频道刷新、订阅更新、RSS、可选通知 | 外部更新信息与实例用户订阅关系组合 |
| 数据迁移 | 导入/导出订阅、历史和用户数据 | 用户文件与实例；不是自动同步 Google 账号 |
| 开发者 API | 内容读取及认证后的用户数据管理 | 由 Invidious 自己提供 |

基础使用可不依赖 JavaScript，但增强播放器和 DASH 播放依赖 JavaScript。项目提供无广告界面；不能扩大理解为自动删除创作者剪进视频中的商业内容。

项目没有通用视频源配置、上传托管或全站视频存档系统。代码与 YouTube 的视频 ID、频道结构、播放器响应和视频服务器耦合。增加其他平台需要开发内容适配与播放逻辑。

依据：[路由清单](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/routing.cr)、[项目功能](https://github.com/iv-org/invidious)、[API](https://docs.invidious.io/api/)。

## 3. 系统组成

组件关系见上方同一张总览图；以下按运行职责展开。

图中网页路由、JSON API、业务逻辑、后台任务是同一个主服务中的模块，通常不分别部署。基础组合是主服务 + Companion + PostgreSQL；反向代理是可选部署组件。

| 组件 | 技术 | 职责 |
| --- | --- | --- |
| 主服务 | Crystal、Kemal | HTTP 请求、页面渲染、API、用户功能、内容解析 |
| 网页 | ECR 模板、HTML/CSS、JavaScript、Video.js | 服务端输出页面，浏览器展示并播放 |
| 数据库 | PostgreSQL | 用户状态、视频信息缓存、频道列表、订阅聚合 |
| Companion | TypeScript、Deno、Hono、YouTube.js | 播放信息、会话、相关令牌与视频流处理 |
| 后台任务 | 主服务内的 Crystal fibers | 周期刷新、通知、缓存清理 |

网页与 JSON API 共用内部业务代码，网页不必先请求一遍自己的公开 API。主仓库还有 `api_only` 编译分支，但不意味着无需数据库或播放配套组件。

依据：[启动入口](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious.cr)、[依赖](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/shard.yml)、[Companion 依赖](https://github.com/iv-org/invidious-companion/blob/master/deno.jsonc)。

## 4. 搜索一次视频经过什么

以用户输入“做饭”为例：

1. 浏览器请求实例的 `/search?q=做饭`；外部程序可请求 `/api/v1/search?q=做饭`。
2. 主服务解析关键词、地区、排序和过滤条件。
3. 常规搜索调用 `Search::Processors.regular`，构造 YouTube 查询参数。
4. `YoutubeAPI.search` 请求 YouTube `/youtubei/v1/search`，携带客户端名称、版本和地区等上下文。
5. `extract_items` 从复杂响应中提取视频、频道、播放列表对象。
6. 网页路由渲染结果页；API 路由将对象序列化为 JSON。

这是“请求内容 → 解释和整理 → 以自己的格式输出”。源码也有页面访问与初始数据提取路径，不能把所有功能简化成调用同一个 JSON 接口。

订阅内搜索是另一路径：使用 PostgreSQL 文本检索搜索已聚合视频的标题和作者。它不是 YouTube 全站全文索引，也不是视频字幕语义搜索。

依据：[搜索处理](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/search/processors.cr)、[上游请求](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/yt_backend/youtube_api.cr)。

## 5. 播放一次视频经过什么

1. 浏览器访问 `/watch?v=视频ID`。
2. 主服务读取偏好并调用 `get_video`，尝试读取数据库中的视频信息缓存。
3. 需要刷新时，`fetch_video` 调用解析器，经 `YoutubeAPI.player` 向 Companion 请求播放信息。
4. Companion 使用 YouTube.js 和配置的会话机制获取播放响应。源码含会话刷新及 PO Token 相关处理，启用方式受配置控制。
5. 主服务按可用状态继续或报错，并在适用时追加 YouTube `next` 响应，合并详情与相关视频等数据。
6. 解析普通媒体格式、音视频分离格式、字幕和播放状态等信息；页面模板生成播放器资源。
7. 浏览器开始请求真正的音视频数据。部分路径可直连，另一些经主服务/Companion 或其公开入口代理；DASH 路径包含为处理跨域而进行的代理处理。

元数据请求和媒体传输是两件事。视频 API 返回 JSON 不等于把整段视频装在 JSON 中；媒体地址通常有有效期，播放器还要请求后续数据。

所以可能出现：首页可打开但搜索失败；搜索有结果但 Companion 会话尚未就绪；视频信息存在但媒体地址过期、上游拒绝或转发失败，导致不能播放。

Companion 的健康检查通过也不等于某个视频一定能播。验收应分别检查网页、搜索、详情、字幕与实际视频流。

依据：[视频读取与缓存](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/videos.cr#L303)、[解析器](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/videos/parser.cr)、[播放器模板](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/views/components/player.ecr)、[Companion 入口](https://github.com/iv-org/invidious-companion/blob/master/src/main.ts)、[视频代理](https://github.com/iv-org/invidious-companion/blob/master/src/routes/videoPlaybackProxy.ts)。

## 6. 缓存、订阅与后台任务

`videos` 表保存视频 ID、信息和更新时间，主要缓存元数据，不是把整个视频文件存进数据库。`get_video` 包含超过约 10 分钟刷新、结构版本变化刷新及强制刷新等条件；带地区参数或数据库错误时可能走不同路径，不能理解为所有内容统一缓存十分钟。

订阅保存在实例自己的用户数据中。后台任务刷新频道视频，再维护按用户生成的订阅物化视图。物化视图相当于预先整理并保存查询结果，方便快速显示订阅内容；刷新也产生网络和数据库开销。

后台任务运行在主服务内，包含并发控制和失败退避，并非预置分布式任务集群。部署更多副本需要考虑重复刷新与共享数据库负担。

连接池复用 HTTP 连接。Companion 配置可列出多个地址供连接池选择，但不等于完整的按健康状态调度和无缝切换体系。

依据：[频道任务](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/jobs/refresh_channels_job.cr)、[订阅任务](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/jobs/refresh_feeds_job.cr)、[连接池](https://github.com/iv-org/invidious/blob/049d591d294e2a43cb32b97a0bb018c2093e5beb/src/invidious/yt_backend/connection_pool.cr)。

## 7. 开发者接口与扩展位置

| 接口示例 | 作用 |
| --- | --- |
| `GET /api/v1/search?q=关键词` | 搜索内容 |
| `GET /api/v1/videos/:id` | 获取详情与可用格式等信息 |
| `GET /api/v1/captions/:id` | 字幕列表，按参数获取字幕内容 |
| `GET /api/v1/comments/:id` | 获取评论 |
| `GET /api/v1/channels/:ucid/videos` | 获取频道视频 |
| `GET /api/v1/playlists/:plid` | 获取播放列表 |
| `POST /api/v1/auth/subscriptions/:ucid` | 修改 Invidious 账号的订阅，需认证 |

应区分 YouTube 官方开放 API、YouTube 客户端内部接口、Invidious 对外 API。开发应用通常对接第三种，Invidious 负责第二种。认证接口有令牌、权限范围和有效期校验；服务间 Companion Key 也不是 YouTube 官方 API Key。

以下是架构推导出的建议，不是已有内置功能：

- 自定义手机、电视或学习界面：复用 HTTP API，业务数据独立存储。
- AI 摘要和知识库：获取已有字幕 → 分段 → 模型处理 → 带时间戳引用；缺字幕时另接语音识别。
- 频道更新摘要：利用频道数据或 RSS，增加调度、去重和通知。
- 跨实例同步：开发身份验证、用户数据同步与冲突处理。
- 其他平台视频源：需要适配层、统一内容模型和新播放逻辑，工作量明显大于修改界面。

源码入口：`routing.cr` 看功能入口，`search/` 看查询处理，`yt_backend/` 看上游协议，`videos/` 看解析，`jsonify/` 看输出格式，`views/` 与 `assets/` 看界面，`database/` 与 `jobs/` 看状态与更新。

## 8. 适用范围与限制

适合个人自建入口、独立订阅、专用客户端和学习工具原型。要求稳定服务承诺的商业应用需要评估上游变化、限流、代理带宽、运维和许可证。

它不提供自有视频上传托管、任意平台即插即用、全量视频镜像、内置 AI 总结或自动同步 Google 账号。它不能承诺任何私有、付费、地区或年龄受限的视频都可播放。

隐私取决于数据路径与运营方式。浏览器直连视频服务仍会发送连接信息；代理改变请求出口，运营者仍可能记录访问。自建意味着掌握更多配置，不等于自动匿名。

路由存在只证明有对应实现入口，不证明当前所有视频都正常；源码错误处理不能消除上游不可用的问题。

## 9. 本地状态与验证范围

- 按用户要求暂停安装部署，仅完成源码和文档分析。
- 此前新增 Docker、Compose 及同次依赖已卸载；未拉取镜像，未启动 Invidious。
- 此前未完成、未验证的部署草稿仅保留在本地，未纳入本次提交。后续安装环境须先获得用户确认。
- 本报告没有真实 YouTube 搜索、字幕获取或视频播放成功率数据，也没有上游应用运行截图。网页和理解图仅用于说明源码机制。
- 主源码在仓库忽略的 `.research/invidious/`，未将完整上游源码纳入研究项目。

补充资料：[安装文档](https://docs.invidious.io/installation/)、[FAQ](https://docs.invidious.io/faq/)、[认证 API](https://docs.invidious.io/api/authenticated-endpoints/)、[上游错误说明](https://docs.invidious.io/youtube-errors-explained/)。
