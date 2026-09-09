# 验证记录

日期：2026-09-09。上游版本：`dd2aaae700e2ebf62a7c80557c2bd64709be5e79`。

## 内容核对

- 按 `config.yml` 核对全部 19 个 GitHub 仓库，包括 7 个 CLI、5 个 Agent、6 个基础设施和 1 个 Skills 仓库。
- 按采集模块核对 Anthropic、OpenAI、GitHub Trending/Search、HN、Dev.to、Lobste.rs、ArXiv、HF、Product Hunt 的实际接口与过滤条件。
- HN 以当前 `hn.ts` 的 Firebase 实现为准，明确区分 README 中尚未同步的 Algolia 和 24 小时口径。
- 明确区分已实现功能和扩展建议。没有运行上游采集、模型调用或外部消息发布。

## 成品检查

- 浏览器检查 1440 像素桌面布局及 390 像素手机布局。页面无横向整体溢出，手机仓库清单按记录展示。
- 类别筛选得到 Agent 项目 5 / 19；结合搜索 Hermes 得到 1 / 19；空结果提示和恢复全部均通过。
- 网页下载入口所指文件均存在；浏览器无脚本异常。
- 原创 SVG 中的文字均处于 1920 × 1200 画布范围内。PNG 为 3840 × 2400。
- 研究 PDF 确认为 7 页；独立总览 PDF 确认为 1 页。已逐页渲染并目视检查研究 PDF，没有截断、重叠或缺字。
- 总览图、桌面页面、手机页面均已查看。机器检查结果保存于 `qa/checks.json`。

## 构建与预览

本项目采用离线静态页面。研究室使用 `scripts/catalog.py` 同步目录、检查清单并构建 `_site/`。GitHub Pages 的发布入口、公开链接与重建说明见 [deployment.md](deployment.md)。

## 文件职责

- `experiments/build_research.py`：共享数据、Markdown、网页、打印文档与原创 SVG 的构建逻辑。
- `experiments/render_check.cjs`：生成 PNG 与 PDF，验证布局和筛选行为。
- `web/assets/overview.svg`：可编辑矢量总览图。
- `web/downloads/`：最终研究 Markdown、PDF 和单页 PDF。
