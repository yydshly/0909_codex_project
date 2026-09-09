# GitHub 项目研究室

持续研究遇到的优秀开源项目，记录它们解决的问题、实现思路、运行方法和可复用的经验。每个项目独立整理研究笔记、截图和可选的 Web 演示，这里只保留摘要与入口。

**阅读路线：** 浏览下方有序索引 → 进入项目研究页 → 查看图片、复现步骤与演示。

## 项目索引

<!-- PROJECT_INDEX:START -->
暂无研究项目。第一个项目将从 **001** 开始编号。
<!-- PROJECT_INDEX:END -->

## 项目速览

<!-- PROJECT_CARDS:START -->
收录项目后，这里会自动展示摘要和已添加的封面图片。
<!-- PROJECT_CARDS:END -->

## 仓库结构

```text
projects/                 各子项目：研究页、图片、实验代码、可选 Web
registry/projects.json    项目清单：稳定编号、展示顺序、摘要和状态
templates/project/        新项目模板
site/                     总览网页模板与样式
scripts/catalog.py        创建项目、同步索引、生成静态站点
docs/                     收录约定与部署指南
.github/workflows/        校验流程与手动发布流程
```

## 开始收录

需要 Python 3.10 或更新版本，无需安装第三方依赖。在仓库根目录执行：

```sh
python scripts/catalog.py new example-repo --name "项目名称" --url "https://github.com/owner/repo" --summary "一句话描述项目与研究重点"
python scripts/catalog.py check
python scripts/catalog.py build
python -m http.server 8000 --directory _site
```

`example-repo` 是命令用法示例，尚未收录为真实项目。创建命令会分配编号、生成研究目录，并同步本页索引。随后填写项目研究页，将截图放入 `assets/`；需要封面时，在清单中设置 `cover`，例如 `assets/cover.png`。

编辑项目清单后运行 `python scripts/catalog.py sync` 更新本页。展示顺序由 `order` 决定；编号与目录保持稳定。

## 维护与发布

- [项目收录、编号与图片约定](docs/project-guide.md)
- [Web 演示与 GitHub Pages 部署](docs/deployment.md)
- [项目元数据清单](registry/projects.json)

当前已准备静态网站生成与手动发布流程；是否上线以仓库 Pages 设置和实际部署结果为准。上游项目的代码与素材应注明来源及原有许可。
