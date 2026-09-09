# 归档验收记录

日期：2026-09-09。检查对象是本研究文档、静态网页和原创架构图，不是上游克隆功能。

## 已通过

| 检查项 | 结果 |
| --- | --- |
| 项目清单与 README 同步 | 项目 002 已登记为“已归档”，文档、网页和封面入口一致 |
| 静态构建 | 总站与项目子路径构建成功 |
| 既有仓库测试 | 5 项测试通过 |
| 桌面 / 平板 / 手机 | 1440、768、390px；页面无横向溢出，图片正常加载 |
| 步骤说明 | 六个步骤均可切换，内容与选中状态同步 |
| 键盘 | 方向键、Home/End；放大弹窗 Escape 关闭并返回焦点 |
| 原创导航示例 | 初始、滚动后、返回顶部状态切换正常 |
| 架构图 | SVG 文本未超出画布，已人工查看 PNG 排版；放大阅读正常 |
| 下载与本地链接 | 已检查页面中的内部非锚点链接，均可访问 |
| 减少动态效果 | reduced-motion 下示例过渡关闭 |
| 无 JavaScript | 核心正文、图、静态步骤说明和下载入口可用 |
| 浏览器错误 | 最终验证无页面错误、控制台错误或缺失链接 |
| 文件格式 | git diff --check 通过 |

浏览器自动检查详见 [browser-verification.json](browser-verification.json)。人工检查了[桌面首屏](../assets/desktop.png)、[处理思路区](../assets/process.png)、[手机首屏](../assets/mobile-top.png)及[架构 PNG](../web/assets/architecture.png)。截图为本归档网页真实渲染，非上游产品截图。

## 修复记录

- 首次检查发现 PNG 尚未进入站点构建；调整为先渲染 PNG，再构建与验收。
- SVG 旋转文字的局部坐标导致初版边界检查误判；改为检测实际屏幕边界，并人工确认。
- 增加页面图标，移除浏览器对不存在 favicon 的默认请求；图的独立渲染使用自包含页面。

## 可复现

运行环境：Python 3.10、Node.js、Playwright 和 Chrome。本地预览服务器从仓库根目录提供内容，默认 `http://127.0.0.1:8029`。

```sh
python projects/002-ai-website-cloner-template/experiments/build_archive.py
node projects/002-ai-website-cloner-template/experiments/verify_archive.cjs --render-only
python scripts/catalog.py sync
python scripts/catalog.py check
python scripts/catalog.py build
node projects/002-ai-website-cloner-template/experiments/verify_archive.cjs
python -m unittest discover -s tests -v
```

Playwright 需在 Node 模块路径中可用；本机使用桌面应用提供的依赖。网页自身无需 Node 或第三方前端依赖。`build_archive.py` 生成原创 SVG、便携文档并同步本项目元数据；PNG 由浏览器按 1440×1840 渲染。

## 未验证的上游事项

未安装上游、未调用模型、未执行实际网站克隆，未进行还原率、成本、耗时或不同模型质量对照。Git 提交与推送用于资料归档；清单中的 Pages 链接仍是预期发布路径，需单独部署才能上线。

## 核心目标修订

按用户确认，将“根据 URL 复刻网页并生成前端工程”放在资料首位；流程约束作为实现方法，能力边界作为结果限制。项目标题与摘要、网页首屏和输入输出条、文档、SVG/PNG 和下载副本同步更新。修订后重新执行构建、宽窄屏和交互验收，并更新实际截图。
