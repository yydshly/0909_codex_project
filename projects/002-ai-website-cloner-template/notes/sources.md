# 来源、事实与解释边界

记录日期：2026-09-09。基于源码阅读和既有研究，未执行上游克隆任务。

| 来源 | 支持内容 |
| --- | --- |
| [README](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/README.md) | 核心目标：提供 URL，由代理重建为 Next.js 网页；模板、流程与场景 |
| [核心 Skill](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/.claude/skills/clone-website/SKILL.md) | 浏览器要求、采集示例、规格、拆分和默认范围 |
| [检查规范](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/docs/research/INSPECTION_GUIDE.md) | 视觉、组件、布局和行为维度 |
| [package.json](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/package.json) | Next.js/React/Tailwind 工程与命令 |
| [初始首页](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/src/app/page.tsx) | 占位页面，不是独立克隆工作台 |
| [同步脚本](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/scripts/sync-skills.mjs) | 多平台指令转换 |
| [CI](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/.github/workflows/ci.yml) | 同步、lint、类型与构建，无自动视觉门槛 |
| [MIT LICENSE](https://github.com/JCodesMore/ai-website-cloner-template/blob/92872bc40ced2c5edb4d5dc9fd3970d40c77f4ca/LICENSE) | 上游许可证 |
| [Screenshot-to-Code 提示词](https://github.com/abi/screenshot-to-code/blob/d026163f586dfa8c5c10d28c36edd59a9d3b0e88/backend/prompts/system_prompt.py) | 单 index.html 和预览要求 |
| [Screenshot-to-Code README](https://github.com/abi/screenshot-to-code/blob/d026163f586dfa8c5c10d28c36edd59a9d3b0e88/README.md) | 独立工作台与视觉输入 |
| [之前的研究](https://github.com/yydshly/0829_codex_project/tree/main/projects/screenshot-to-code-agent-study) | 2026-08-29 研究与采用判断 |
| [MDN 计算样式](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle) | 样式、伪元素、动画状态 |
| [MDN CSS 规则](https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleSheet/cssRules) | 样式规则读取 |
| [Playwright 环境模拟](https://playwright.dev/docs/emulation) | 视口、设备、主题 |
| [Playwright 视觉比较](https://playwright.dev/docs/test-snapshots) | 截图及环境一致性 |

## 边界

- 资料先表述“根据 URL 复刻网页”的目标，再解释流程约束的方法与可控性边界。
- “规范降低随意性”是架构理解，未量化收益。
- 结构化契约、置信度、状态图、失效追踪、自动门槛和有界重试是我们的扩展建议。
- 网页导航示例的数值是原创教学数据，不是实测结果。
- 架构图为原创；实线表示职责和流程要求，虚线表示扩展建议，实线不意味着程序强制执行。
- 未复制上游产品截图，未声称自研模型、恢复原工程或复制真实后端。
