# 源码证据与研究说明

核对日期：2026-09-09。固定提交：`7cbf47b57cbae0596d46c10c4a1445cbb27904b3`。

## 来源与方法

- [完整文件树 API](https://api.github.com/repos/Pluviobyte/rnskill/git/trees/7cbf47b57cbae0596d46c10c4a1445cbb27904b3?recursive=1)：统计所有 SKILL.md、保存 blob SHA、检查所引用的四个工作台依赖是否入库。
- [README](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/README.md)：仓库定位、能力分类、第三方来源和许可声明。
- [清单数据](../web/data/inventory.json)：63 个入口的文件路径、来源链接、blob SHA、目录下脚本列表。脚本数量包含嵌套目录，不用于衡量能力强弱。
- [完整能力目录](capability-catalog.md)：逐项归纳的输入、输出、依赖和复用条件，每条附固定版本源文件链接。

采集后阅读全部入口定义，并静态查看配音、字幕、封面等代表性脚本。未安装或调用上游技能，未运行模型、媒体制作或第三方收费服务。页面中的四条流程属于研究者基于技能定义整理的组合路径，并非经过端到端运行的自动化管线。

## 代表性实现证据

| 结论 | 源文件 |
| --- | --- |
| 制作导演用交接稿与目录状态指导下游技能 | [ra-video-production-director/SKILL.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-production-director/SKILL.md) |
| 视频改写默认停在待制作队列 | [ra-video-wash-pipeline/SKILL.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-wash-pipeline/SKILL.md) |
| 配音强依赖声音配置与作者工作台根目录 | [generate_indextts2_narration.py](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/tts-skill/scripts/generate_indextts2_narration.py) |
| 字幕调用火山 ASR，使用 SequenceMatcher 对齐原稿，含局部时间推算 | [generate_subtitles.py](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-audio-to-subtitles/scripts/generate_subtitles.py) |
| 封面文字与背景由 SVG 控制，生成插图作为位图嵌入 | [compose_cover.py](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-cover-skill/scripts/compose_cover.py) |
| 图文由 Agent 拆页填 HTML、Playwright 渲染为 PNG | [xhs-article-to-images/SKILL.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/xhs-article-to-images/SKILL.md) |
| 人体动作提取依赖 MediaPipe、OpenCV、NumPy 和 FFmpeg | [extract_motion.py](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-human-motion-extractor/scripts/extract_motion.py) |
| 复盘取数依赖台账、快照和云端脚本 | [ra-复盘/SKILL.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-复盘/SKILL.md) |
| 孙割只是跳转到同一套决策分析定义 | [孙割/SKILL.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/孙割/SKILL.md) |

## 统计说明

README 声称 57 个技能；当前固定版本文件树包含 63 个 SKILL.md，其中顶层 58、嵌套 5。展示采用文件清单口径，保留一个明确别名，不把文件数量写成独立能力数量。九类分类和复用条件是本研究的整理，不冒充上游官方分类或运行认证。

## 许可与素材

[仓库默认许可证](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/LICENSE)为 CC BY-NC 4.0。第三方组件包含 MIT、Apache-2.0、AGPL-3.0 等不同声明，不能整体视为统一许可。详细来源以 [CREDITS.md](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/CREDITS.md) 和对应模块目录为准。

本子项目的界面、能力关系图和分类总览图为研究室自行制作，没有复制上游示例封面、人物图像或视频。保存的页面截图仅展示本子项目界面。
