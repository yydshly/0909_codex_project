window.EXHIBITION = {
  "original": [
    {
      "id": "cover",
      "title": "能自动化 ≠ 该自动化",
      "shortTitle": "自动化的边界",
      "archetype": "封面隐喻",
      "description": "用天平和分岔路，把“能做”与“该做”的差异变成一眼可见的选择。",
      "alt": "天平位于自动化机械臂与阅读书桌之间，表达自动化的边界。",
      "ratio": "约 21:9",
      "width": 1928,
      "height": 816,
      "src": "./assets/original/cover.png"
    },
    {
      "id": "page-01",
      "title": "阅读其实是两件事",
      "shortTitle": "阅读的两件事",
      "archetype": "左右对比",
      "description": "左边是信息漏斗，右边是书本与罗盘。通过两组物体，区分摄入信息与训练判断。",
      "alt": "信息漏斗与阅读书本左右对比：摄入信息要结果，训练判断重过程。",
      "ratio": "16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/original/page-01.png"
    },
    {
      "id": "page-02",
      "title": "自动化该放哪里",
      "shortTitle": "自动化放哪里",
      "archetype": "流程与分工",
      "description": "观察淡色标签、细箭头与物件如何组织工作步骤，并突出自动化的适用位置。",
      "alt": "原作者关于自动化在工作流程中应该放在哪里的手绘解释图。",
      "ratio": "16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/original/page-02.png"
    },
    {
      "id": "page-03",
      "title": "三问判断法",
      "shortTitle": "三问判断法",
      "archetype": "判断框架",
      "description": "把抽象判断压缩成三个问题，保持短文字、克制标题和统一的手绘视觉。",
      "alt": "原作者用三个问题帮助读者判断是否应该自动化的手绘解释图。",
      "ratio": "16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/original/page-03.png"
    }
  ],
  "scenario": [
    {
      "id": "cover",
      "title": "让开源项目成为知识",
      "archetype": "封面隐喻",
      "description": "把开源项目的原始资料，整理成有出处、可演示、可复用的知识。",
      "alt": "让开源项目成为知识。把开源项目的原始资料，整理成有出处、可演示、可复用的知识。",
      "ratio": "约 21:9",
      "width": 1916,
      "height": 821,
      "src": "./assets/scenario/cover.png"
    },
    {
      "id": "page-01",
      "title": "先把项目收录清楚",
      "archetype": "分类图",
      "description": "每个项目都有独立目录，保存来源、版本、许可与一句话摘要。",
      "alt": "先把项目收录清楚。每个项目都有独立目录，保存来源、版本、许可与一句话摘要。",
      "ratio": "约 16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/scenario/page-01.png"
    },
    {
      "id": "page-02",
      "title": "从读懂到亲手验证",
      "archetype": "横向流程",
      "description": "研究记录、结构图和实际演示共同支持对项目能力的理解。",
      "alt": "从读懂到亲手验证。研究记录、结构图和实际演示共同支持对项目能力的理解。",
      "ratio": "约 16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/scenario/page-02.png"
    },
    {
      "id": "page-03",
      "title": "保存与上线分两步",
      "archetype": "阶段区分",
      "description": "资料推送触发检查，网站上线还需要手动运行发布流程。",
      "alt": "保存与上线分两步。资料推送触发检查，网站上线还需要手动运行发布流程。",
      "ratio": "约 16:9",
      "width": 1672,
      "height": 941,
      "src": "./assets/scenario/page-03.png"
    }
  ],
  "blueprint": {
    "name": "GitHub 项目研究室：从收录到复用",
    "deckType": "工作流程解释",
    "generatedWith": "内置 image_gen 工具；按 Ian Handdrawn PPT 规则执行",
    "styleReference": "upstream/assets/reference-handdrawn-article-illustration-style.png",
    "styleLock": "Refined Chinese handdrawn technical article illustration. Very light near-white paper #FBFAF5 with extremely subtle grain, no full-page border. Centered restrained hard-pen Chinese title and one pale blue handdrawn underline, small subtitle below. Fine black ink and pencil linework with delicate hatching; stable slightly irregular lines. Pale blue #D9E8F6, sage green #DCEAD6, peach #F5DEB8 and lavender #E4DCF4 used only in small marker labels. Faint grey grid/dot construction marks in upper-right and lower-left corners. Generous negative space. Small refined object-based diagrams, no people. Body titles optically identical in scale, medium and restrained. Props blank or simple line marks unless listed in Required text only. No yellow paper, beige paper, giant fonts, dense bullets, corporate cards, shadows, gradients, neon, logos, watermark, filler text or fake writing.",
    "sourceFiles": [
      "README.md",
      "docs/project-guide.md",
      "docs/deployment.md"
    ],
    "assumptions": [
      "面向初次加入研究室的协作者",
      "将工作流程压缩为一张封面和三张解释图",
      "收录和发布规则来自本仓库现有文档，不包含虚构客户或效果数据"
    ],
    "pages": [
      {
        "id": "cover",
        "title": "让开源项目成为知识",
        "role": "cover",
        "archetype": "封面隐喻",
        "ratio": "21:9",
        "point": "把开源项目的原始资料，整理成有出处、可演示、可复用的知识。",
        "texts": [
          "让开源项目成为知识",
          "收录 · 研究 · 复用",
          "开源项目",
          "研究工作台",
          "知识资料"
        ],
        "composition": "Ultra-wide 21:9, preferred 2520x1080. No page number. A compact meticulous pencil drawing across the center: left small stack of repository folders with blank paper and tiny node diagrams, label 开源项目; middle a magnifying glass over an open notebook with a small pencil, label 研究工作台; right neatly indexed document folders and a small display stand showing a simple flow diagram, label 知识资料. Thin arrows connect left to middle to right. Overall metaphor about 55% canvas width with very wide empty margins. Title centered near top, subtitle below. Use the attached image only as a style reference, replace its content entirely.",
        "prompt": "Use case: productivity-visual.\nCreate one final PNG page, fully composed Chinese text baked into image, not a mockup photograph.\nPage role: cover.\nArchetype: 封面隐喻.\nMain point: 把开源项目的原始资料，整理成有出处、可演示、可复用的知识。\nDeck style lock: Refined Chinese handdrawn technical article illustration. Very light near-white paper #FBFAF5 with extremely subtle grain, no full-page border. Centered restrained hard-pen Chinese title and one pale blue handdrawn underline, small subtitle below. Fine black ink and pencil linework with delicate hatching; stable slightly irregular lines. Pale blue #D9E8F6, sage green #DCEAD6, peach #F5DEB8 and lavender #E4DCF4 used only in small marker labels. Faint grey grid/dot construction marks in upper-right and lower-left corners. Generous negative space. Small refined object-based diagrams, no people. Body titles optically identical in scale, medium and restrained. Props blank or simple line marks unless listed in Required text only. No yellow paper, beige paper, giant fonts, dense bullets, corporate cards, shadows, gradients, neon, logos, watermark, filler text or fake writing.\nTitle exactly: 让开源项目成为知识\nComposition: Ultra-wide 21:9, preferred 2520x1080. No page number. A compact meticulous pencil drawing across the center: left small stack of repository folders with blank paper and tiny node diagrams, label 开源项目; middle a magnifying glass over an open notebook with a small pencil, label 研究工作台; right neatly indexed document folders and a small display stand showing a simple flow diagram, label 知识资料. Thin arrows connect left to middle to right. Overall metaphor about 55% canvas width with very wide empty margins. Title centered near top, subtitle below. Use the attached image only as a style reference, replace its content entirely.\nRequired text only (render every item once, exact Simplified Chinese):\n- 让开源项目成为知识\n- 收录 · 研究 · 复用\n- 开源项目\n- 研究工作台\n- 知识资料\nNo other visible text. Match the reference line quality and near-white background. Keep labels clean and legible."
      },
      {
        "id": "page-01",
        "title": "先把项目收录清楚",
        "role": "body",
        "archetype": "分类图",
        "ratio": "16:9",
        "point": "每个项目都有独立目录，保存来源、版本、许可与一句话摘要。",
        "texts": [
          "01 / 03",
          "先把项目收录清楚",
          "一个项目 · 一份档案",
          "来源",
          "版本",
          "许可",
          "摘要"
        ],
        "composition": "Landscape 16:9, preferred 1920x1080. Small upper-left page number 01 / 03. A central carefully drawn open archival folder with four slim paper tabs branching toward four small object illustrations: a chain link above-left labeled 来源, a small version-history timeline above-right labeled 版本, a paper certificate with simple nontext marks below-left labeled 许可, a compact index card below-right labeled 摘要. Exactly four labels, no invented writing. The entire diagram occupies 55% width and 40% height. This is a classification map, not a process. Same top centered title position as other body pages, title approximate 4.5% canvas height. Use attached image only for matching its style.",
        "prompt": "Use case: productivity-visual.\nCreate one final PNG page, fully composed Chinese text baked into image, not a mockup photograph.\nPage role: body.\nArchetype: 分类图.\nMain point: 每个项目都有独立目录，保存来源、版本、许可与一句话摘要。\nDeck style lock: Refined Chinese handdrawn technical article illustration. Very light near-white paper #FBFAF5 with extremely subtle grain, no full-page border. Centered restrained hard-pen Chinese title and one pale blue handdrawn underline, small subtitle below. Fine black ink and pencil linework with delicate hatching; stable slightly irregular lines. Pale blue #D9E8F6, sage green #DCEAD6, peach #F5DEB8 and lavender #E4DCF4 used only in small marker labels. Faint grey grid/dot construction marks in upper-right and lower-left corners. Generous negative space. Small refined object-based diagrams, no people. Body titles optically identical in scale, medium and restrained. Props blank or simple line marks unless listed in Required text only. No yellow paper, beige paper, giant fonts, dense bullets, corporate cards, shadows, gradients, neon, logos, watermark, filler text or fake writing.\nTitle exactly: 先把项目收录清楚\nComposition: Landscape 16:9, preferred 1920x1080. Small upper-left page number 01 / 03. A central carefully drawn open archival folder with four slim paper tabs branching toward four small object illustrations: a chain link above-left labeled 来源, a small version-history timeline above-right labeled 版本, a paper certificate with simple nontext marks below-left labeled 许可, a compact index card below-right labeled 摘要. Exactly four labels, no invented writing. The entire diagram occupies 55% width and 40% height. This is a classification map, not a process. Same top centered title position as other body pages, title approximate 4.5% canvas height. Use attached image only for matching its style.\nRequired text only (render every item once, exact Simplified Chinese):\n- 01 / 03\n- 先把项目收录清楚\n- 一个项目 · 一份档案\n- 来源\n- 版本\n- 许可\n- 摘要\nNo other visible text. Match the reference line quality and near-white background. Keep labels clean and legible."
      },
      {
        "id": "page-02",
        "title": "从读懂到亲手验证",
        "role": "body",
        "archetype": "横向流程",
        "ratio": "16:9",
        "point": "研究记录、结构图和实际演示共同支持对项目能力的理解。",
        "texts": [
          "02 / 03",
          "从读懂到亲手验证",
          "阅读 · 拆解 · 验证",
          "读材料",
          "画结构",
          "做演示",
          "用途与限制",
          "模块与流程",
          "操作与结果"
        ],
        "composition": "Landscape 16:9, preferred 1920x1080. Small upper-left page number 02 / 03. Three calm stations across the middle with thin unambiguous arrows going left to right. Left a small open technical notebook with magnifier, pale blue label 读材料 above, caption 用途与限制 below. Middle a detailed miniature board holding a simple connected-box system diagram with no text inside boxes, pale sage label 画结构 above, caption 模块与流程 below. Right a laptop with a small cursor arrow and a simple visual flow on screen (no screen writing), peach label 做演示 above, caption 操作与结果 below. Group occupies 58% width and 40% height; ample blank margins. Same top centered title position as other body pages, title approximate 4.5% canvas height. Attached image is style reference only.",
        "prompt": "Use case: productivity-visual.\nCreate one final PNG page, fully composed Chinese text baked into image, not a mockup photograph.\nPage role: body.\nArchetype: 横向流程.\nMain point: 研究记录、结构图和实际演示共同支持对项目能力的理解。\nDeck style lock: Refined Chinese handdrawn technical article illustration. Very light near-white paper #FBFAF5 with extremely subtle grain, no full-page border. Centered restrained hard-pen Chinese title and one pale blue handdrawn underline, small subtitle below. Fine black ink and pencil linework with delicate hatching; stable slightly irregular lines. Pale blue #D9E8F6, sage green #DCEAD6, peach #F5DEB8 and lavender #E4DCF4 used only in small marker labels. Faint grey grid/dot construction marks in upper-right and lower-left corners. Generous negative space. Small refined object-based diagrams, no people. Body titles optically identical in scale, medium and restrained. Props blank or simple line marks unless listed in Required text only. No yellow paper, beige paper, giant fonts, dense bullets, corporate cards, shadows, gradients, neon, logos, watermark, filler text or fake writing.\nTitle exactly: 从读懂到亲手验证\nComposition: Landscape 16:9, preferred 1920x1080. Small upper-left page number 02 / 03. Three calm stations across the middle with thin unambiguous arrows going left to right. Left a small open technical notebook with magnifier, pale blue label 读材料 above, caption 用途与限制 below. Middle a detailed miniature board holding a simple connected-box system diagram with no text inside boxes, pale sage label 画结构 above, caption 模块与流程 below. Right a laptop with a small cursor arrow and a simple visual flow on screen (no screen writing), peach label 做演示 above, caption 操作与结果 below. Group occupies 58% width and 40% height; ample blank margins. Same top centered title position as other body pages, title approximate 4.5% canvas height. Attached image is style reference only.\nRequired text only (render every item once, exact Simplified Chinese):\n- 02 / 03\n- 从读懂到亲手验证\n- 阅读 · 拆解 · 验证\n- 读材料\n- 画结构\n- 做演示\n- 用途与限制\n- 模块与流程\n- 操作与结果\nNo other visible text. Match the reference line quality and near-white background. Keep labels clean and legible."
      },
      {
        "id": "page-03",
        "title": "保存与上线分两步",
        "role": "body",
        "archetype": "阶段区分",
        "ratio": "16:9",
        "point": "资料推送触发检查，网站上线还需要手动运行发布流程。",
        "texts": [
          "03 / 03",
          "保存与上线分两步",
          "资料更新 · 网站发布",
          "推送资料",
          "自动检查",
          "手动发布",
          "网站更新"
        ],
        "composition": "Landscape 16:9, preferred 1920x1080. Small upper-left page number 03 / 03. Two compact pairs across the central zone. Left pair: a small file tray labeled 推送资料 with a thin arrow to a magnifier and check-mark checklist labeled 自动检查. Right pair: a small hand-operated lever labeled 手动发布 with a thin arrow to a desktop browser display on a pedestal labeled 网站更新. A faint vertical dashed divider and wide gap between pairs; NO arrow from automatic checking to manual release, since manual release is a separate action. Four small detailed pencil object illustrations, no people or fake writing. Blue small marker labels on left pair, sage on right. Group occupies 60% width and 38% height. Same centered title position as other body pages, title approximate 4.5% canvas height. Reference is style only.",
        "prompt": "Use case: productivity-visual.\nCreate one final PNG page, fully composed Chinese text baked into image, not a mockup photograph.\nPage role: body.\nArchetype: 阶段区分.\nMain point: 资料推送触发检查，网站上线还需要手动运行发布流程。\nDeck style lock: Refined Chinese handdrawn technical article illustration. Very light near-white paper #FBFAF5 with extremely subtle grain, no full-page border. Centered restrained hard-pen Chinese title and one pale blue handdrawn underline, small subtitle below. Fine black ink and pencil linework with delicate hatching; stable slightly irregular lines. Pale blue #D9E8F6, sage green #DCEAD6, peach #F5DEB8 and lavender #E4DCF4 used only in small marker labels. Faint grey grid/dot construction marks in upper-right and lower-left corners. Generous negative space. Small refined object-based diagrams, no people. Body titles optically identical in scale, medium and restrained. Props blank or simple line marks unless listed in Required text only. No yellow paper, beige paper, giant fonts, dense bullets, corporate cards, shadows, gradients, neon, logos, watermark, filler text or fake writing.\nTitle exactly: 保存与上线分两步\nComposition: Landscape 16:9, preferred 1920x1080. Small upper-left page number 03 / 03. Two compact pairs across the central zone. Left pair: a small file tray labeled 推送资料 with a thin arrow to a magnifier and check-mark checklist labeled 自动检查. Right pair: a small hand-operated lever labeled 手动发布 with a thin arrow to a desktop browser display on a pedestal labeled 网站更新. A faint vertical dashed divider and wide gap between pairs; NO arrow from automatic checking to manual release, since manual release is a separate action. Four small detailed pencil object illustrations, no people or fake writing. Blue small marker labels on left pair, sage on right. Group occupies 60% width and 38% height. Same centered title position as other body pages, title approximate 4.5% canvas height. Reference is style only.\nRequired text only (render every item once, exact Simplified Chinese):\n- 03 / 03\n- 保存与上线分两步\n- 资料更新 · 网站发布\n- 推送资料\n- 自动检查\n- 手动发布\n- 网站更新\nNo other visible text. Match the reference line quality and near-white background. Keep labels clean and legible."
      }
    ]
  }
};
