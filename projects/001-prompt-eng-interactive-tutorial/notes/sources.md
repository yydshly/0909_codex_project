# 来源与研究范围

核对日期：2026-09-09。固定研究版本：`0d277542e927652da25b0014c9b346723af55881`，提交于 2024-04-08。网页所有仓库源码链接固定到此版本。

## 结论与源码对应

以下文件均位于[固定版本仓库](https://github.com/anthropics/prompt-eng-interactive-tutorial/tree/0d277542e927652da25b0014c9b346723af55881)。直接 API 课程所在目录为 [Anthropic 1P](https://github.com/anthropics/prompt-eng-interactive-tutorial/tree/0d277542e927652da25b0014c9b346723af55881/Anthropic%201P)。

| 来源文件 | 支持的内容 |
| --- | --- |
| `README.md` | 9 章课程、练习与实验区、总体教学定位 |
| `Anthropic 1P/00_Tutorial_How-To.ipynb` | API 凭据、Anthropic SDK、默认 Claude 3 Haiku |
| `Anthropic 1P/01_Basic_Prompt_Structure.ipynb` | system、messages、get_completion、调用参数、正则判分 |
| `Anthropic 1P/02_Being_Clear_and_Direct.ipynb` | 明确要求，减少歧义 |
| `Anthropic 1P/03_Assigning_Roles_Role_Prompting.ipynb` | 角色与任务视角 |
| `Anthropic 1P/04_Separating_Data_and_Instructions.ipynb` | 模板变量、f-string、XML 分隔 |
| `Anthropic 1P/05_Formatting_Output_and_Speaking_for_Claude.ipynb` | JSON/XML 与 assistant 预填充 |
| `Anthropic 1P/06_Precognition_Thinking_Step_by_Step.ipynb` | 显式步骤教学，不将旧表述推广到现代模型 |
| `Anthropic 1P/07_Using_Examples_Few-Shot_Prompting.ipynb` | 用示例指导格式和行为 |
| `Anthropic 1P/08_Avoiding_Hallucinations.ipynb` | 允许不知道、先找证据、温度控制 |
| `Anthropic 1P/09_Complex_Prompts_from_Scratch.ipynb` | 组件组合、职业教练、法律、税务与代码教学 |
| `Anthropic 1P/10.1_Appendix_Chaining Prompts.ipynb` | 多次调用、检查与改写，自检也会引入错误 |
| `Anthropic 1P/10.2_Appendix_Tool Use.ipynb` | 文本协议、停止序列、Python 解析、计算器与字典数据库 |
| `Anthropic 1P/10.3_Appendix_Search & Retrieval.ipynb` | 主要为外部 Cookbook 和资料入口 |
| `AmazonBedrock/anthropic/10_3_Appendix_Empirical_Performance_Evaluations.ipynb` | 代码评分、人工评分、模型评分 |
| `AmazonBedrock/requirements.txt` | 较早且固定的 SDK 依赖 |
| `AmazonBedrock/LICENSE` | MIT No Attribution，不推定为全库统一许可证 |

## 当前适用性来源

- [Anthropic 官方提示词实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)：部分新模型不再支持末轮 assistant 预填充，迁移需核对具体模型。
- [Anthropic 扩展思考文档](https://platform.claude.com/docs/en/docs/build-with-claude/extended-thinking)：现代推理机制不能由教程关于显式步骤的说法概括。

在线文档可能更新，不与仓库旧 Commit 混为同一时间版本。

## 事实、分析与演示的区分

- **仓库事实：** 章节、文件结构、调用方法、判分与工具代码、RAG 附录的实际范围。
- **本研究分析：** 学习优先级、生产落地需要补充的能力、四条扩展路线。
- **原创教学示例：** 图谱例子与三组场景提示词，展示信息组织方式，不是上游模型输出或效果评测。
- **未执行：** 付费模型调用、Notebook 全量复现、跨模型对比、业务质量基准测试。

根目录未发现统一许可文件，仅按实际发现记录子目录许可。展示页及研究文档以原创摘要、例子和来源链接为主，没有复制完整课程。
