# Siftly 来源与核查记录

研究版本固定为 `b25daa45b858f4be096b5c368671c34db4407d8e`，核对日期为 2026-09-09。本文区分源码事实、由事实推导的用途和尚未验证的运行效果。

## 能力依据

| 主题 | 源码 | 核查结论 |
| --- | --- | --- |
| 浏览器采集 | [app/import/page.tsx](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/import/page.tsx) | 书签按钮和控制台脚本都捕获后续 fetch / XHR JSON 响应；自动滚动与无新增超时判断不能证明历史收藏完整 |
| 文件导入 | [import route](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/import/route.ts)、[parser](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/parser.ts) | 解析支持的 JSON 格式，按 tweetId 去重，保存导入数据；支持 bookmark / like 来源标记，不等于全部点赞获取路径均可用 |
| Cookie 接口 | [twitter-api](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/twitter-api.ts)、[x-sync](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/x-sync.ts) | 内部 GraphQL 查询 ID 固定；分页最多 50 页；进程内定时器 1 / 4 / 8 / 24 小时；主要新增和去重 |
| 官方 API | [callback](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/import/x-oauth/callback/route.ts)、[fetch](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/import/x-oauth/fetch/route.ts) | 已有 PKCE 授权、令牌保存 / 刷新及用户 ID 获取；收藏请求仍用 /2/users/me/bookmarks，默认 5 页、最多 20 页 |
| 官方接口要求 | [X Bookmarks Lookup](https://docs.x.com/x-api/posts/bookmarks/quickstart/bookmarks-lookup) | 文档要求先获取用户 ID，再请求 /2/users/{id}/bookmarks；可用性、授权和计费需按当前平台确认 |
| 数据存储 | [schema.prisma](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/prisma/schema.prisma) | Bookmark / MediaItem / Category / BookmarkCategory / ImportJob / Setting，SQLite 存储；媒体存在 URL、缩略图等字段 |
| 图片理解 | [vision-analyzer](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/vision-analyzer.ts) | SDK 读取图片后 Base64 编码传给模型；CLI 备用路径仅提示 URL；要求 OCR、物体、场景、情绪等 JSON；视频主要取缩略图 |
| 模型适配 | [ai-client](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/ai-client.ts) | Anthropic / OpenAI / MiniMax 适配不保证每个模型都支持视觉或取得同等效果 |
| 实体与分类 | [rawjson-extractor](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/rawjson-extractor.ts)、[categorizer](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/categorizer.ts) | 规则提取实体，LLM 根据内容和分类说明赋类；分数来自模型，不应当作经过校准的概率 |
| 搜索 | [fts](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/fts.ts)、[AI search](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/search/ai/route.ts) | FTS5 召回 + 分类规则 + LLM 重排；回退文本匹配；候选不足补近期资料；未见向量检索 |
| 中文缺陷 | [search-utils](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/search-utils.ts) | 非 a-z / 数字 / 空白字符被替换，中文关键词会丢失，影响候选召回 |
| 分类图 | [mindmap](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/mindmap/route.ts) | 根节点到分类，再到书签；每分类最多返回 66 个推文节点，不是所有收藏都一定同时显示 |
| CLI | [cli/siftly.ts](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/cli/siftly.ts) | 列表、详情、分类、统计与全文 / 文本搜索；JSON 输出；没有 AI 重排 |
| 导出 | [exporter](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/exporter.ts)、[export route](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/app/api/export/route.ts) | CSV / JSON 非完整备份；分类 ZIP 尝试下载媒体，失败会跳过；全量 ZIP 仅含 JSON |
| Obsidian | [obsidian-exporter](https://github.com/viperrcrypto/Siftly/blob/b25daa45b858f4be096b5c368671c34db4407d8e/lib/obsidian-exporter.ts) | 生成笔记、分类和作者索引；图片仍引用 URL；标签清洗也可能去除中文 |

## 对前期说明的修订

- 将接入方式、内容数据、凭证和后续操作分开，避免把 X 登录状态当作业务数据。
- 将书签按钮和控制台归为同一采集原理的两个入口。
- 将“同步”限定为代码实现的周期导入与去重，避免暗示双向一致性。
- 图片理解限定为视觉模型生成描述；不暗示独立 OCR 引擎、以图搜图、完整视频理解或全模型视觉兼容。
- 搜索结果限定为候选收藏；说明召回限制和中文问题；补充 CLI 与 AI 搜索差异。
- 区分分类 ZIP、全量 ZIP、JSON / CSV、Obsidian，避免把导出叫作完整备份。

## 验证边界

完成核心源码静态核查和说明图视觉检查。用途与优化方向为研究推导；未用真实 X 账号测试收藏覆盖，没有运行上游服务或调用模型。本仓库仅发布静态研究内容，不对上游功能缺陷做修复。采集凭证和私有数据未进入研究文件。
