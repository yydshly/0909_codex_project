# 发布与重建

## 公开入口

- [完整研究网页](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/)
- [独立一页总览](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/overview.html)
- [七页研究 PDF](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/downloads/agents-radar-research.pdf)
- [单页总览 PDF](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/downloads/agents-radar-overview.pdf)
- [高清 PNG](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/assets/overview.png)
- [可编辑 SVG](https://yydshly.github.io/0909_codex_project/projects/005-agents-radar/assets/overview.svg)

## 站点发布

项目已接入 `registry/projects.json`，网页文件位于 `web/`，封面为 `web/assets/overview.svg`。推送 `main` 后，运行仓库的 `Deploy GitHub Pages` 工作流（`pages.yml`）。工作流执行测试、清单校验和静态构建后发布 `_site/`。实际发布状态以 [GitHub Actions](https://github.com/yydshly/0909_codex_project/actions/workflows/pages.yml) 为准。

网页及文档全部为静态研究资料，不会调用上游采集器、模型接口或消息推送。页面无运行时外部依赖，浏览器可直接打开 `web/index.html`；以 HTTP 方式预览可同时使用返回研究室入口。

## 重新生成研究产物

1. 使用 Python 3 运行 `experiments/build_research.py`，生成 Markdown、HTML、数据清单与 SVG。
2. 使用 Node.js 与 Playwright、Sharp 运行 `experiments/render_check.cjs`，生成 PNG、两份 PDF，并检查交互及排版。Playwright 需要已安装的 Chromium。
3. 默认使用 Node.js 常规包解析；如果依赖位于独立目录，可通过 `RADAR_NODE_MODULES` 指定该目录。
4. 在研究室根目录运行 `python scripts/catalog.py sync`、`check`、`build`。

已生成的网页和下载文件直接入库；GitHub Pages 部署不需要安装 Playwright、Sharp，也不会重新生成研究 PDF。逐页 PNG 与浏览器截图为本地排版检查中间件，不纳入发布提交；机器检查记录保留于 `notes/qa/checks.json`。
