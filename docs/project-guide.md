# 项目收录约定

## 编号与展示顺序

每个研究项目采用 `001-example-repo` 这样的目录。`id` 是稳定身份，至少补齐三位；`slug` 使用小写英文、数字和连字符。创建后保留编号和目录名，避免破坏已有链接。清单的 `nextId` 保存下一可用编号，删除项目后也不要回退它或复用旧编号。

`order` 是独立的展示顺序，默认按 10、20、30 递增，方便插入新条目。README 的索引、摘要卡片和网页总览都按 `order` 升序排列。调整顺序只需修改此值，不需要重命名目录。

## 新增项目

```sh
python scripts/catalog.py new example-repo --name "项目名称" --url "https://github.com/owner/repo" --summary "项目用途和本次研究重点"
```

完成后填写 `projects/001-example-repo/README.md`，记录研究对应的上游版本或 Commit。实验代码放在 `experiments/`，演示放在 `web/`。默认仅保存本项目研究产物；如需引入上游源码，再为该项目选择克隆、子模块或摘录方式并保留许可信息。

## 清单字段

`registry/projects.json` 是总索引的唯一数据来源。

| 字段 | 用途 |
| --- | --- |
| `id` | 稳定的正整数编号 |
| `slug` | 目录名称后缀；编号与 slug 组合成项目目录 |
| `order` | 不重复的正整数，决定展示顺序 |
| `name` | 展示名称 |
| `source` | 上游 GitHub 仓库 HTTPS 链接 |
| `summary` | 一句话摘要，保持单行 |
| `status` | 待研究 / 研究中 / 已整理 / 已归档 |
| `tags` | 主题标签数组，可为空 |
| `cover` | 项目目录内的图片相对路径；未添加时为 `null` |
| `demo` | `true` 时发布 `web/`，必须包含 `web/index.html` |

创建脚本会生成完整条目，无需从零手写 JSON。修改清单后执行：

```sh
python scripts/catalog.py sync
python scripts/catalog.py check
```

README 中两组 `PROJECT_*` 标记之间的内容由脚本维护，其余内容可以直接编辑。项目状态在清单中修改后，也要更新对应研究页的资料表。

## 图片约定

图片放在子项目的 `assets/` 下，建议名称为 `cover.png`、`architecture.svg`、`demo-01.webp`。优先使用压缩后的 PNG、WebP 或 SVG；为 Markdown 图片添加描述性替代文本，并在研究页说明来源。

设置 `cover` 后，主 README 和网页总览自动显示封面。未设置封面时展示文本摘要，不使用虚构的截图占位。网页构建仅复制所选封面和启用的 `web/` 目录；研究文档仍链接到 GitHub。
