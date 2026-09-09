# 验证与交付记录

日期：2026-09-09。

## 已完成

- 建立 `013-firecrawl` 子项目，保留其他项目和已有未提交修改。
- 研究笔记整理了 URL / 搜索词等入口、HTML / 浏览器 / RSS / API 的区别、两层调度、开源与云服务边界、Agents Radar 对照；补充登录、X 平台防护和 Siftly 取数边界。
- 独立网页包含八种能力切换、四种获取方式切换、整体图、常见误解和真实服务调用示例下载。
- 将 Firecrawl 加入总索引，状态为“已整理”，生成总项目静态输出。

## 执行过的检查

- `python experiments/check_static.py`：23 处静态引用检查通过，页面锚点、SVG XML、Python 语法、下载副本一致性通过。
- `node --check web/app.js`：JavaScript 语法通过。
- `python experiments/firecrawl_example.py --help`：命令行入口正常。
- 根目录 `python scripts/catalog.py check`：13 个项目清单与索引一致。
- 根目录 `python scripts/catalog.py build`：13 个项目构建成功。构建脚本确认 `_site` 为工作区根目录内的输出路径后才重新生成。
- `git diff --check`：通过；已有文件的换行提示不属于本项目运行错误。
- 本地 HTTP 页面请求返回 200。预览入口：`http://127.0.0.1:8133/`。

## 实测边界

- 匿名调用官方 `POST /v2/scrape`，目标为 `https://example.com`，返回 HTTP 403。只观察到失败状态，不能判断具体拒绝原因。
- 没有配置 API Key，也没有运行完整 Firecrawl 自部署服务；没有获得抓取成功、性能或规模测试证据。
- 所有展示结果均为人工编写的教学示例；切换控件不触发网络采集，不构成真实数据回放。
- 未进行浏览器截图或交互自动化 QA；静态与语法检查不能替代视觉验收。

## 发布状态

首次交付为本地展示。用户随后明确要求提交 GitHub 并部署网页，因此本次使用总项目既有 GitHub Pages 流程发布。发布副本基于远端最新 main，只加入 Firecrawl 子项目、该项目清单条目和自动生成的总索引，避免混入共享目录的其他改动。

- 网页入口：[Firecrawl 能力展示](https://yydshly.github.io/0909_codex_project/projects/013-firecrawl/)。
- 源码与文档：[项目目录](https://github.com/yydshly/0909_codex_project/tree/main/projects/013-firecrawl)。
- 发布工作流：[Deploy GitHub Pages](https://github.com/yydshly/0909_codex_project/actions/workflows/pages.yml)。
- 工作流执行清单测试、索引校验和静态构建，再部署 Pages；部署结果以对应提交的成功运行记录为准。

网页发布的是研究和教学展示，不会启动 Firecrawl 服务端，不接受账号凭证，不自动采集任何登录网页。
