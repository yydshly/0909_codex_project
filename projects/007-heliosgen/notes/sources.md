# HeliosGen 研究依据

核对日期：2026-09-09。上游固定提交：`fb011d6f3ad00510b4eface78e054c7eda329c54`。以下均指向本次实际阅读的版本。

| 研究结论 | 源码依据 |
| --- | --- |
| Tauri 桌面壳、内置 Node 服务、SQLite 和本地媒体 | [DESKTOP.md](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/DESKTOP.md) |
| 文本、助手、图片与视频输入、生成节点 | [nodeTypes.tsx](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/nodeTypes.tsx) |
| 模型能力、输入限制与参数映射 | [modelConfig.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/modelConfig.ts) |
| 供应商选择 | [providers.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/providers.ts) |
| 图片与视频节点分批、并行，按端口解析输入 | [executor.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/executor.ts)、[usePipelineRunner.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/usePipelineRunner.ts) |
| 通用 Kie 任务轮询、保存结果、更新状态 | [kieJobPoller.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/kieJobPoller.ts) |
| 本地参考素材上传到第三方临时文件服务 | [kieUpload.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/kieUpload.ts) |
| 图片调用中的 Azure 和 Codex CLI 路径 | [generate/route.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/app/api/generate/route.ts) |
| 提示词助手调用云端文本模型 | [assistant/route.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/app/api/assistant/route.ts) |
| 工作流结构与图片、视频打包 | [exportWorkflow.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/exportWorkflow.ts)、[importWorkflow.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/lib/importWorkflow.ts) |
| Veo 轮询未完成 | [generate-video/route.ts](https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/app/api/generate-video/route.ts) |

## 边界

- “本地”描述应用运行和数据存储；生成请求及必要参考素材仍可能发往云端。
- 模型配置存在不等于所有功能已经端到端验证，各模型能力和接口可用性可能变化。
- 自动执行主要覆盖图片、视频节点；整批等待和较简单的失败处理限制了无人值守生产能力。
- 文档注明大视频上传仍需完善，FFmpeg / FFprobe 和可选生成 CLI 没有随桌面应用打包。
- 编排、模型接入、任务处理是按代码职责归纳的逻辑模块，非独立微服务或完整插件框架。
- 本次研究未安装上游依赖、执行模型生成或处理真实用户素材。

## 图片来源

`web/assets/heliosgen-overview.png` 为本次研究使用内置图片生成工具制作的说明图，非上游截图。提示词保存在同目录的 `image-prompt.txt`。画面中的商品流程为能力示意，非实测产出。
