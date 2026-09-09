# rnskill 完整能力清单

核对版本：`7cbf47b57cbae0596d46c10c4a1445cbb27904b3` · 日期：2026-09-09

按固定提交的 SKILL.md 文件统计：58 个顶层入口、5 个嵌套入口，其中孙割为别名。文件数不等于互不重复的能力数。上游 README 标注 57，本页采用目录核对口径。

复用分类是静态研究判断；未验证工具已安装、账号可用或上游功能运行成功。

## 01 · 选题与策划（5 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [dbs-xhs-title](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-xhs-title/SKILL.md) | **小红书标题公式**：从内置标题公式中选择适合图文主题的表达方式。 | 小红书图文主题、文案 → 标题方案、公式选择理由 | 宿主 Agent、技能内标题公式 | 方法可复用 |
| [ra-hook](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-hook/SKILL.md) | **短视频开头选型**：根据场景从七类开头中选型，提供句型与容易出错的地方。 | 选题、观众、核心观点 → 开头类型、钩子草稿 | 宿主 Agent、技能内方法说明 | 方法可复用 |
| [ra-video-title](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-title/SKILL.md) | **视频标题候选**：先锁定视频主题，再参考对标规律生成两段式标题候选。 | 主题、文稿、可选对标标题 → 8–12 个标题候选、Top 3 推荐 | 宿主 Agent；写入成片目录时需路径约定 | 方法可复用 |
| [ra-实操策划](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E5%AE%9E%E6%93%8D%E7%AD%96%E5%88%92/SKILL.md) | **实操长片策划**：把工具实测主题拆成可照着录制的讲解与操作步骤。 | 实测主题、产品、录制目标 → 测试题组、时间轴、口播稿、录屏清单 | 工作台策划模板、状态约定、录制素材 | 需工作台适配 |
| [ra-选题](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E9%80%89%E9%A2%98/SKILL.md) | **选题全生命周期**：记录灵感、深化角度，并把同一选题分发为视频、文章或图文项目。 | 灵感、链接、目标内容形态 → 选题卡、立项链接、发布状态 | 个人定位、选题模板、工作台目录；推荐环节还需云端监测与去重脚本 | 需工作台适配 |

## 02 · 写作与表达（8 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [dbs-ai-check](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-ai-check/SKILL.md) | **文案风格诊断**：按二十二类表达特征扫描文稿，默认输出诊断而不直接改写。 | 待检查文稿 → 逐处问题报告 | 宿主 Agent、表达规则；结果属于编辑判断 | 方法可复用 |
| [dbs-content](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-content/SKILL.md) | **内容创作诊断**：在选题确定后分析内容结构、论据和表达方式。 | 选题、文稿、内容目标 → 创作建议、问题清单 | 宿主 Agent、配套知识材料 | 方法可复用 |
| [dbs-hook](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-hook/SKILL.md) | **开头诊断与优化**：检查已有开头是否交代利益、抓住注意力并形成继续观看的理由。 | 已有视频开头 → 问题定位、优化方案 | 宿主 Agent、开头与正文语境 | 方法可复用 |
| [dbs-resonate](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-resonate/SKILL.md) | **文稿共鸣诊断**：从受众情绪与传播心理分析文稿中的表达问题。 | 完整文稿、受众信息 → 共鸣分析、修改建议 | 宿主 Agent；结论需真实发布数据检验 | 方法可复用 |
| [dbs-spread](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-spread/SKILL.md) | **传播心理分析**：从传播理论解释内容中的情绪、立场和讨论空间。 | 文章、视频文稿或内容片段 → 传播机制分析、讨论方向 | 宿主 Agent、传播理论参考 | 方法可复用 |
| [ra-video-wash-pipeline](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-wash-pipeline/SKILL.md) | **视频到脚本流水线**：串联来源获取、转写、改写与入队，默认在待制作阶段交接。 | 视频链接或本地视频、改写目标 → 新脚本、标题候选、待制作交接稿 | 转写及改写技能、下载工具、工作台、缺失的去重脚本 | 需工作台适配 |
| [ra-人话](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E4%BA%BA%E8%AF%9D/SKILL.md) | **中文表达精修**：检查模板腔、空泛总结与机械对比，保留作者判断和事实。 | 中文草稿、作者表达偏好 → 精修文稿、具体修改 | 宿主 Agent、原稿与事实材料 | 方法可复用 |
| [ra-洗稿](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E6%B4%97%E7%A8%BF/SKILL.md) | **口播脚本改写**：组合表达精修、开头和共鸣检查，生成脚本与制作交接。 | 已有逐字稿、口播草稿、主题笔记 → 新脚本、检查结果、交接稿 | 多个下游技能、工作台模板、去重台账 | 需工作台适配 |

## 03 · 素材与剪辑（8 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [ai-jian-koubo](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ai-jian-koubo/SKILL.md) | **AI 剪口播审核**：转录口播、识别口误，在网页中审核删除范围并导出剪辑工程。 | 口播视频 → 波形审核页、删除清单、FCPXML | Node.js、Python、火山 ASR、FFmpeg、浏览器 | 需工具配置 |
| [chengfeng-videocut-skills:剪口播](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/chengfeng-videocut-skills/%E5%89%AA%E5%8F%A3%E6%92%AD/SKILL.md) | **乘风 · 口播素材粗剪**：转写并识别口误，审核后剪出基础视频并重做字幕。 | 原始口播视频 → source_cut.mp4、subtitles.srt、审核页 | Node.js、Shell、ASR、FFmpeg、浏览器 | 需工具配置 |
| [chengfeng-videocut-skills:口播成片](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/chengfeng-videocut-skills/%E5%8F%A3%E6%92%AD%E6%88%90%E7%89%87/SKILL.md) | **乘风 · 口播成片**：将剪后视频、文稿和插图组织为分镜、时间线和成片。 | 口播稿、SRT、剪后视频、图片 → 分镜稿、时间线预览、最终 MP4 | 用户配置、HTML 动画、视频合成工具 | 需工具配置 |
| [ra-local-talking-head-cut](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-local-talking-head-cut/SKILL.md) | **本地口播粗剪**：先校对术语和不确定内容，再按语义剪辑、处理停顿与响度。 | 自录口播或讲解录屏 → 粗剪 MP4、剪辑与质检资料 | ASR 服务、FFmpeg、本地脚本；剪前内容需要审核 | 需工具配置 |
| [ra-video-download](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-download/SKILL.md) | **多平台视频下载**：通过下载器和平台服务把来源保存为可核验的本地媒体。 | 公开视频或音频链接 → 本地视频、音频、来源信息 | yt-dlp、TikHub、FFmpeg；按平台配置访问条件 | 需工具配置 |
| [ra-公众号提取](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E5%85%AC%E4%BC%97%E5%8F%B7%E6%8F%90%E5%8F%96/SKILL.md) | **公众号文章提取**：以特定浏览器标识请求公开文章，提取正文供后续处理。 | 公开微信公众号文章链接 → 正文文本 | Python 标准库、网络访问；平台页面变动会影响提取 | 需工具配置 |
| [ra-逐字稿提取skill](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E9%80%90%E5%AD%97%E7%A8%BF%E6%8F%90%E5%8F%96skill/SKILL.md) | **视频逐字稿提取**：下载来源并调用语音识别获取口播文本，供阅读或改写。 | 抖音、小红书链接 → 逐字稿文本 | qushuiyin、Paraformer ASR、配套转写环境 | 需工具配置 |
| [video-use](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/video-use/SKILL.md) | **对话式视频编辑**：按对话计划完成转写、剪辑、调色、字幕及动画叠加。 | 视频素材、编辑要求 → 处理后视频、项目文件 | 视频工具链、转写能力；具体依赖随编辑路径变化 | 需工具配置 |

## 04 · 声音与字幕（4 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [heygen-digital-avatar](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/heygen-digital-avatar/SKILL.md) | **HeyGen 数字人**：将经过试听确认的配音交给数字人服务，再按布局合成视频。 | 已确认音频、数字人身份、布局 → 数字人视频、合成成片 | HeyGen CLI OAuth、订阅、Digital Twin、个人声音与布局资产 | 需工作台适配 |
| [ra-audio-to-subtitles](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-audio-to-subtitles/SKILL.md) | **真实时间戳字幕**：识别最终音频，再将原稿匹配到时间轴，分句并检查可读性。 | 最终音频或视频、准确文稿 → SRT、VTT、JSON 时间轴、字幕质检 | 火山 Doubao ASR API Key、Python、FFmpeg | 需工具配置 |
| [skill-captions](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/skill-captions/SKILL.md) | **字幕样式与烧录**：将已通过检查的时间轴渲染为统一外观，并验证最终画面。 | 字幕 JSON、视频、选定样式 → 带字幕视频、预览、渲染质检 | 已通过检查的字幕时间轴、渲染及合成工具 | 需工具配置 |
| [tts-skill](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/tts-skill/SKILL.md) | **本地克隆配音**：使用固定无损参考声音生成旁白，并记录声音来源与参数。 | 分段文稿、声音参考 → WAV 配音、voice_manifest.json | IndexTTS2 模型与 CLI、FFmpeg、作者声音配置；配置未随库提供 | 需工作台适配 |

## 05 · 封面与图文（6 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [editorial-dot-cover](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/editorial-dot-cover/SKILL.md) | **点阵编辑风封面**：用程序构建大标题、留白和点阵矢量图标的封面。 | 标题、图标主题 → SVG、PNG | Python、字体、SVG 渲染环境 | 需工具配置 |
| [ian-xiaohei-illustrations](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ian-xiaohei-illustrations/SKILL.md) | **小黑正文插图**：把文章中的流程、判断与隐喻表现为白底手绘插图。 | 文章、观点、配图意图 → 正文插图、配图计划 | 宿主生图能力、风格参考 | 需工具配置 |
| [rn-cover-skill](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-cover-skill/SKILL.md) | **RN 编辑图解封面**：生图模型画概念图，程序控制暖白背景、中文标题与网格。 | 标题、概念、可选副标题 → 5:2 SVG 与 PNG | 生图能力、抠图脚本、Python、字体与浏览器渲染 | 需工具配置 |
| [rn-niulai-style-image](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-niulai-style-image/SKILL.md) | **粗粝 3D 风格图像**：从照片或场景描述生成粗粝低模、充气人偶质感的风格图。 | 照片、电影画面或场景描述 → 风格化图片、对照资料 | 生图能力、授权参考图像 | 需工具配置 |
| [skill-cover](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/skill-cover/SKILL.md) | **注册风格封面**：按已有风格、人物与比例资产生成或修改系列封面。 | 主题、注册风格、人物或参考封面 → 3:4 与 4:3 等指定封面 | 个人注册资产系统、人物素材、生图能力 | 需工作台适配 |
| [xhs-article-to-images](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/xhs-article-to-images/SKILL.md) | **长文转图文卡片**：把 Markdown 按原文结构拆页，填入既定版式并逐张渲染。 | Markdown 文章、配图、皮肤偏好 → 3:4 PNG 图片组、HTML/CSS 工程 | Node.js、Playwright、浏览器、字体与图片素材 | 需工具配置 |

## 06 · 动画与动效（8 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [ian-xiaohei-svg-motion](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/chengfeng-videocut-skills/%E5%8F%A3%E6%92%AD%E6%88%90%E7%89%87/%E5%8A%A8%E7%94%BB/ian-xiaohei-svg-motion/SKILL.md) | **小黑 SVG 动画**：把概念和工作流表现为可控制的分层 SVG 与 HTML 动画。 | 文稿、分镜、概念说明 → HTML、SVG、GSAP 动画工程 | HTML/SVG、GSAP、配套图标与模板 | 需工具配置 |
| [editorial-collage-motion](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/editorial-collage-motion/SKILL.md) | **纸张拼贴动效**：生成静帧与透明图层，再编排逐件进入和组装的动画。 | 参考图或视觉简报 → 拼贴静帧、图层、动态视频 | 生图能力、FFmpeg 或 HyperFrames | 需工具配置 |
| [rn-bw-text-opener](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-bw-text-opener/SKILL.md) | **黑白文字开场**：规划文字逐字出现、字体变化和声音节奏，生成短开场。 | 开场文案、时长、节奏 → 文字开场视频、时序方案 | Python 时序脚本、动画渲染工具、可选音效 | 需工具配置 |
| [rn-dark-saas-video](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-dark-saas-video/SKILL.md) | **暗色产品宣传动效**：用预设场景蓝图组合产品界面、文字、按钮和转场。 | 产品卖点、界面素材、时长 → 暗色 SaaS 产品视频、工程 | HyperFrames、字体、产品素材、渲染环境 | 需工具配置 |
| [rn-human-motion-extractor](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-human-motion-extractor/SKILL.md) | **人体与手部动作提取**：逐帧提取人体和双手关键点，生成骨架预览及置信度报告。 | 获授权的真人参考视频 → 关键点数据、匿名骨架视频、质检 | Python、MediaPipe、OpenCV、NumPy、FFmpeg | 需工具配置 |
| [rn-motion-director](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-motion-director/SKILL.md) | **动效创作导演**：从主题规划视觉隐喻、运动节奏和场景，并组织视频制作。 | 主题、文章、脚本或简报 → 动效概念、分镜、动画工程与视频 | 下游制作技能、HyperFrames 或 Remotion、生图及渲染能力 | 需工具配置 |
| [rn-motion-replica](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-motion-replica/SKILL.md) | **参考动效拆解与重建**：提取参考片段的布局和时序，用新文案与素材搭建动画。 | 获授权的参考片段、目标效果 → 分镜、可编辑工程、MP4、质检画面 | FFmpeg、HyperFrames、参考分析脚本 | 需工具配置 |
| [manim-video](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/video-use/skills/manim-video/SKILL.md) | **数学与技术动画**：用程序表达公式推导、算法过程、几何关系和技术概念。 | 概念、公式、算法讲解要求 → Manim 场景、解释视频 | Python、Manim Community、FFmpeg；公式按需配置 LaTeX | 需工具配置 |

## 07 · 调度与沉淀（9 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [chengfeng-videocut-skills:自进化](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/chengfeng-videocut-skills/%E8%87%AA%E8%BF%9B%E5%8C%96/SKILL.md) | **剪辑规则反馈更新**：把用户反馈写入规则和方法说明，供下一次剪辑使用。 | 用户反馈、已有规则 → 更新后的规则文档 | 本地技能文件写入权限；属于规则维护 | 方法可复用 |
| [dbs-content-system](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-content-system/SKILL.md) | **内容资产结构化**：审计本地文稿，再抽取内容单元、建立主题地图与选题装配稿。 | 本地文稿、案例、选题、课程资料 → 内容单元库、主题地图、装配稿 | Node.js、配套模板与工具、本地文件访问 | 需工具配置 |
| [dbs-decision](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-decision/SKILL.md) | **长期决策记录**：以来源、快照和概念库组织需要长期跟踪的个人议题。 | 领域问题、历史材料、后续结果 → 本地知识工程、决策记录、状态画像 | 宿主 Agent、本地文件访问、领域资料 | 方法可复用 |
| [dbs-report](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-report/SKILL.md) | **诊断报告汇编**：将多次保存的诊断状态合并为可分享的报告。 | 多个诊断快照 → Markdown 报告 | 已有诊断快照、宿主 Agent | 方法可复用 |
| [dbs-restore](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-restore/SKILL.md) | **诊断状态续读**：读取已保存的诊断记录，为后续讨论恢复上下文。 | 已有诊断快照 → 恢复后的诊断上下文 | dbs-save 产物、本地读取权限 | 方法可复用 |
| [dbs-save](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-save/SKILL.md) | **诊断状态存档**：将当前诊断中的关键判断与未解决事项保存到本地。 | 当前诊断对话 → 本地状态快照 | 宿主 Agent、本地写入权限 | 方法可复用 |
| [ra-video-production-director](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-video-production-director/SKILL.md) | **制作总导演**：读取交接要求，选择制作路径，管理状态、质量检查与归档。 | 交接稿、文稿、制作需求 → 成片、质检资料、工程归档 | 个人工作台、多个下游技能与工具；部分交付脚本未入库 | 需工作台适配 |
| [ra-复盘](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/ra-%E5%A4%8D%E7%9B%98/SKILL.md) | **内容表现复盘**：结合指标和内容分析表现，并把有效表达、案例与结论回写。 | 作品、账号指标、历史数据 → 分级分析、素材库条目、选题卡回写 | 个人台账、指标快照、分级标准、云端监测脚本 | 需工作台适配 |
| [rn-replica-qc](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/rn-replica-qc/SKILL.md) | **动效复刻质检**：区分复刻精度级别，检查素材、运行时和最终视频的帧级证据。 | 参考视频、复刻工程、最终 MP4 → 比对证据、质检结论、问题清单 | FFmpeg、视频分析脚本、可复现渲染环境 | 需工具配置 |

## 08 · 商业与思考（13 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [dbs-action](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-action/SKILL.md) | **行动阻力分析**：按作者采用的心理学框架探讨行动迟滞的可能原因。 | 目标、行动过程、阻碍描述 → 行动阻力分析、反思问题 | 宿主 Agent；属于自我反思工具 | 方法可复用 |
| [dbs-benchmark](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-benchmark/SKILL.md) | **对标对象分析**：按过滤框架识别可学习的案例与不适用的模仿对象。 | 业务目标、候选对标、案例信息 → 对标分析、筛选理由 | 宿主 Agent、对标资料、配套知识材料 | 方法可复用 |
| [dbs-chatroom-austrian](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-chatroom-austrian/SKILL.md) | **奥派经济学讨论**：以奥派经济学相关视角组织多角色模拟交流。 | 经济或商业议题 → 模拟讨论、视角比较 | 宿主 Agent；不代表相关人物真实发言 | 方法可复用 |
| [dbs-chatroom](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-chatroom/SKILL.md) | **多视角模拟讨论**：按主题推荐讨论角色，模拟不同视角的交流。 | 话题、可选讨论角色 → 多角色模拟对话 | 宿主 Agent；模拟观点需与真实言论区分 | 方法可复用 |
| [dbs-deconstruct](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-deconstruct/SKILL.md) | **商业概念拆解**：澄清概念的指代、条件和关系，减少抽象词造成的歧义。 | 模糊商业词语或判断 → 概念解释、关系拆解 | 宿主 Agent、配套知识材料 | 方法可复用 |
| [dbs-diagnosis](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-diagnosis/SKILL.md) | **商业模式诊断**：通过问题澄清与模式拆解，帮助梳理业务逻辑。 | 业务描述、商业问题、已有证据 → 问题分析、商业模式诊断 | 宿主 Agent、配套知识材料、真实业务事实 | 方法可复用 |
| [dbs-goal](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-goal/SKILL.md) | **目标清晰化**：把含混愿望转成能检查、能交付的目标描述。 | 模糊目标、约束条件 → 目标定义、可检查交付物 | 宿主 Agent、真实目标背景 | 方法可复用 |
| [dbs-good-question](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-good-question/SKILL.md) | **问题说明书**：把含混提问拆成可推理、可批评、可验证的任务。 | 模糊问题、已有资料 → 问题说明书、自动化适用性判断 | 宿主 Agent、任务背景与可用证据 | 方法可复用 |
| [dbs-learning](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-learning/SKILL.md) | **反馈式连续学习**：围绕课题连续组织学习材料，按反馈调整下一次内容。 | 课题、当前水平、阅读反馈 → 连续学习文章、后续学习安排 | 宿主 Agent、学习反馈 | 方法可复用 |
| [dbs-slowisfast](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-slowisfast/SKILL.md) | **长期积累路径分析**：分析短期效率与长期资产之间的取舍。 | 当前做法、目标、资源约束 → 替代路径、积累建议 | 宿主 Agent、真实业务背景 | 方法可复用 |
| [dbs](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs/SKILL.md) | **商业问题导航**：在任务前选择合适的诊断技能，在完成后提示下一步。 | 商业问题、当前进度 → 技能路由、后续行动建议 | 宿主 Agent、对应 dbs 技能 | 方法可复用 |
| [孙割](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/%E5%AD%99%E5%89%B2/SKILL.md) | **决策模式分析 · 别名**：转到孙宇晨技能读取同一套规则，不提供独立能力。 | 同主技能的决策问题 → 主技能分析结果 | 依赖同目录体系中的孙宇晨技能 | 方法可复用 |
| [孙宇晨](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/%E5%AD%99%E5%AE%87%E6%99%A8/SKILL.md) | **公开决策模式分析**：借公开案例中的注意力、叙事与身份运用方式进行决策推演。 | 选题、发布、公关或危机问题 → 模式分析、情境推演 | 宿主 Agent、公开案例；非真人扮演 | 方法可复用 |

## 09 · Agent 工具（2 个入口）

| 技能 / 来源 | 能力 | 输入 → 输出 | 依赖 | 复用条件 |
| --- | --- | --- | --- | --- |
| [dbs-agent-migration](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/dbs-agent-migration/SKILL.md) | **Agent 工作台整理**：审计不同宿主的规则入口，整理真源与桥接文件。 | 已有项目、规则和技能目录 → 统一规则入口、桥接文件、迁移记录 | 本地项目读写权限、目标宿主约定 | 方法可复用 |
| [grok-build-cli](https://github.com/Pluviobyte/rnskill/blob/7cbf47b57cbae0596d46c10c4a1445cbb27904b3/skills/grok-build-cli/SKILL.md) | **调用 Grok Build**：检查登录与模型，执行单轮或 Agentic 任务并跟踪结果。 | 交给 Grok 的问题或任务 → Grok 返回内容、任务结果 | 本地 Grok Build CLI、登录状态、网络 | 需工具配置 |
