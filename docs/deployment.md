# Web 演示与部署

## 一个总览，多个项目路径

本仓库使用一个 GitHub Pages 站点，通过子路径容纳多个静态演示。预期发布地址：

```text
https://yydshly.github.io/0909_codex_project/
https://yydshly.github.io/0909_codex_project/projects/001-example-repo/
https://yydshly.github.io/0909_codex_project/projects/002-another-repo/
```

这些是地址规则示例，不代表演示已经上线。GitHub Pages 托管静态 HTML、CSS 和 JavaScript；需要服务器或数据库的项目应另行部署后在研究页记录入口。

## 接入子项目

1. 将可直接部署的静态文件放入 `projects/<编号>-<slug>/web/`，确保包含 `index.html`。
2. 在项目清单中将 `demo` 设为 `true`。
3. 运行 `python scripts/catalog.py build`，生成 `_site/`。
4. 运行 `python -m http.server 8000 --directory _site`，访问 `http://localhost:8000/` 检查总览和演示。

构建会清理并重新生成仓库根目录的 `_site/`，不要在该目录手写文件。需要 npm 等构建工具的子项目独立管理依赖，先自行构建，再把最终可发布产物放入 `web/`；总项目不自动执行子项目的构建命令。

静态资源优先使用 `./assets/...` 等相对链接。框架的部署基础路径应设为 `/0909_codex_project/projects/<编号>-<slug>/`。单页应用优先使用 hash 路由，避免直接访问深层路径时遇到 Pages 404。

## 首次启用 GitHub Pages

1. 将初始化文件推送到 GitHub 的 `main` 分支。
2. 在仓库 **Settings → Pages → Build and deployment** 中选择 **GitHub Actions**。
3. 在 **Actions → Deploy GitHub Pages → Run workflow** 中选择 `main` 手动运行。
4. 等待部署成功，再使用部署任务返回的实际站点地址。

发布工作流仅支持手动触发，且只允许从 `main` 发布。普通提交和拉取请求只校验项目清单、README 同步状态、脚本测试和静态构建。后续确实需要自动发布时，再给发布流程增加 `push` 触发器。

## 参考

- [GitHub Pages 的托管范围和站点限制](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [使用自定义工作流发布 Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
