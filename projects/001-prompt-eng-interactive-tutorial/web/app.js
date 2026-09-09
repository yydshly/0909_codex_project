"use strict";

const upstream = "https://github.com/anthropics/prompt-eng-interactive-tutorial";
const revision = "0d277542e927652da25b0014c9b346723af55881";
const notebook = (name) => `${upstream}/blob/${revision}/Anthropic%201P/${encodeURIComponent(name)}.ipynb`;
const sources = {
  readme: `${upstream}/blob/${revision}/README.md`,
  commit: `${upstream}/commit/${revision}`,
  setup: notebook("00_Tutorial_How-To"),
  basic: notebook("01_Basic_Prompt_Structure"),
  clear: notebook("02_Being_Clear_and_Direct"),
  role: notebook("03_Assigning_Roles_Role_Prompting"),
  separate: notebook("04_Separating_Data_and_Instructions"),
  format: notebook("05_Formatting_Output_and_Speaking_for_Claude"),
  reasoning: notebook("06_Precognition_Thinking_Step_by_Step"),
  examples: notebook("07_Using_Examples_Few-Shot_Prompting"),
  evidence: notebook("08_Avoiding_Hallucinations"),
  complex: notebook("09_Complex_Prompts_from_Scratch"),
  chain: notebook("10.1_Appendix_Chaining Prompts"),
  tools: notebook("10.2_Appendix_Tool Use"),
  rag: notebook("10.3_Appendix_Search & Retrieval"),
  eval: `${upstream}/blob/${revision}/AmazonBedrock/anthropic/10_3_Appendix_Empirical_Performance_Evaluations.ipynb`,
  license: `${upstream}/blob/${revision}/AmazonBedrock/LICENSE`,
  current: "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices",
  thinking: "https://platform.claude.com/docs/en/docs/build-with-claude/extended-thinking"
};

const techniques = [
  {id:"clear",name:"清晰指令与任务约束",en:"Clear & direct instructions",group:"input",chapter:"第 1–2 章",status:"课程与练习",source:"clear",brief:"把目标、范围和完成标准说清楚。",explain:"用具体的动词、条件和输出要求定义任务，减少模型自行猜测的空间。系统提示词可以承载持续的行为要求，用户消息提供当前任务。",mechanism:"模型根据上下文生成回答；越明确的任务信息，越容易让生成方向与需求一致。这里改变输入，不训练模型。",example:"将这段会议记录整理为 3 条行动项。每条包含负责人和截止日期；未提及的信息填写“未说明”。",boundary:"指令再清晰也不能补出缺失事实；相互冲突的要求需要先解决。",value:"优先学习：目标、边界与验收标准仍有长期价值。"},
  {id:"role",name:"角色提示",en:"Role prompting",group:"input",chapter:"第 3 章",status:"课程与练习",source:"role",brief:"设定回答视角、语气和专业范围。",explain:"告诉模型以什么身份、面向谁完成任务。角色是组织行为要求的一种方式，适合约束表达视角和交流方式。",mechanism:"角色描述为模型提供相关的语言和任务模式，再结合明确要求引导回答。",example:"你是一名面向 Python 初学者的代码导师。解释错误原因，给出最小修改，并说明如何验证。",boundary:"“世界顶级专家”之类的头衔不是能力保证；专业结论仍需要依据。",value:"按需使用：具体职责和受众通常比夸张身份更有用。"},
  {id:"separate",name:"模板变量与数据分隔",en:"Prompt templates · XML delimiters",group:"input",chapter:"第 4 章",status:"课程与练习",source:"separate",brief:"分开固定规则和每次变化的材料。",explain:"将固定指令写成模板，把邮件、文档或问题作为变量填入。使用 XML 标签标出材料的开始和结束。",mechanism:"Python 的 f-string 或 format() 完成文本替换；标签帮助模型识别语义边界，并不会让模型变成严格的 XML 解析器。",example:"请改写 <email>{邮件正文}</email> 中的邮件，使语气更礼貌。保留原有事实，不添加承诺。",boundary:"分隔符能减少混淆，但不是抵御恶意指令的安全隔离机制。",value:"优先学习：适合重复任务、长文档和业务模板。"},
  {id:"examples",name:"少样本提示",en:"Few-shot prompting",group:"input",chapter:"第 7 章",status:"课程与练习",source:"examples",brief:"用少量正确例子展示分类或输出规则。",explain:"在提示词里提供几组输入和期望输出，让模型按示例中的模式处理新数据。“Few-shot”就是少量示例。",mechanism:"模型从当前上下文中的示例归纳任务模式，称为上下文学习；不会永久更新模型权重。",example:"输入：收到的杯子裂了。\n输出：售后\n\n输入：这款有蓝色吗？\n输出：售前\n\n输入：{新邮件}\n输出：",boundary:"错误、单一或不具代表性的示例会带偏结果；测试集应与示例分开。",value:"优先学习：适合业务标签、特殊格式和难以口述的风格。"},
  {id:"format",name:"输出格式与预填充",en:"Output formatting · Assistant prefill",group:"output",chapter:"第 5 章",status:"课程与练习",source:"format",brief:"指定输出结构，或提供回答的开头。",explain:"要求回答使用 JSON、XML 或固定标签。原教程还演示预填充：先给 assistant 消息写入一个开头，让模型从那里续写。",mechanism:"格式指令引导输出形状；预填充通过已有前缀影响后续生成。例如先写“{”，再让模型续写 JSON 内容。",example:"仅输出 JSON，包含 category、evidence 两个字段。category 只能是“售前”“售后”“其他”。",boundary:"提示词要求不等于格式强约束；程序仍需解析和校验。当前部分新模型不支持末轮 assistant 预填充。",value:"保留输出规范；预填充需查目标模型文档，可按接口能力改用结构化输出。",extra:"current"},
  {id:"reasoning",name:"分步骤处理",en:"Step-by-step prompting",group:"output",chapter:"第 6 章",status:"课程与练习",source:"reasoning",brief:"把复杂任务拆成可检查的处理步骤。",explain:"对复杂判断说明处理顺序，例如先提取信息，再对照标准，最后给结论。教程用显式步骤演示这种方法。",mechanism:"在逐步生成中，中间结果成为后续生成的上下文，可能帮助减少遗漏；步骤本身也可能出错。",example:"先列出需求中的限制，再检查方案是否逐项满足，最后给出结论和可以验证的依据。",boundary:"长篇推理不保证正确。教程“必须输出思考文字才算思考”的表述不能推广到具备独立推理机制的新模型。",value:"保留任务分解和可验证依据；按目标模型的推理接口调整提示方式。",extra:"thinking"},
  {id:"evidence",name:"证据约束与拒绝猜测",en:"Grounding · Abstention",group:"output",chapter:"第 8 章",status:"课程与练习",source:"evidence",brief:"先找材料依据，不足时明确说明。",explain:"让模型先寻找相关原文，再基于证据回答；明确允许“资料不足，无法判断”，减少为了完成任务而编造。",mechanism:"把回答与给定材料关联，并提供不作结论的有效出口。证据优先是回答策略，不是额外的事实数据库。",example:"仅依据所附文档回答退款期限。引用支持结论的原句；若未说明期限，回答“资料未提供退款期限”。",boundary:"仍需核验引用是否真实、是否支持结论；降低 temperature 也不能保证事实正确。",value:"优先学习：适合资料问答、信息提取和报告分析。"},
  {id:"complex",name:"复杂提示词组合",en:"Complex prompt composition",group:"input",chapter:"第 9 章",status:"行业案例与练习",source:"complex",brief:"将角色、材料、规则和格式组合成任务。",explain:"把前面学到的方法组合起来，形成可重复使用的业务提示词。教程提供职业教练、法律材料问答、税务分析及代码教学案例。",mechanism:"用变量和字符串拼接组织提示词组件；本质仍是一次模型请求中的上下文设计。",example:"角色：代码导师\n材料：<code>{代码}</code>\n规则：先解释错误，再给最小修改\n输出：问题、修改建议、验证步骤",boundary:"不必把所有组件都塞进每个任务；冗余要求可能增加成本或产生冲突。",value:"适合业务原型：从完整要求起步，再依据测试精简。"},
  {id:"chain",name:"提示词链",en:"Prompt chaining",group:"extend",chapter:"附录 10.1",status:"可运行示例",source:"chain",brief:"把前一次调用的结果传给下一次调用。",explain:"将复杂任务拆成多次模型调用。例如先生成草稿，再检查问题，最后按检查结果修改。",mechanism:"程序保存前一次响应，将其放进新的提示词或对话历史。不同步骤可以使用不同规则和输出要求。",example:"第 1 次：提取文档里的行动项。\n第 2 次：对照原文检查是否遗漏或编造。\n第 3 次：根据检查结果输出最终列表。",boundary:"增加延迟与费用；自我检查也可能把正确答案改错，需要独立依据。",value:"按任务使用：当步骤能单独验证时更值得拆分。"},
  {id:"tools",name:"工具调用",en:"Tool use · Function calling",group:"extend",chapter:"附录 10.2",status:"可运行示例",source:"tools",brief:"让模型提出调用，由程序执行外部函数。",explain:"在上下文里描述工具名称、用途和参数。模型选择工具并给出参数，程序完成计算或数据操作，再把结果返回模型。",mechanism:"原教程用 <function_calls> 文本、stop_sequences 和 Python 参数解析完成调用回路，包含计算器和字典模拟数据库练习。",example:"用户：计算 1984135 × 9343116。\n模型：提出 calculator 调用及两个操作数。\n程序：完成乘法并返回数值。\n模型：据此回答。",boundary:"模型不能只靠说“调用工具”就执行操作。生产使用还需接口适配、参数校验、权限和异常处理。",value:"值得理解原理：扩展模型能力的关键模式，旧协议需要更新。"},
  {id:"eval",name:"效果评估",en:"Code · Human · Model grading",group:"output",chapter:"主课练习 / Bedrock 附录",status:"判分代码与评估教学",source:"eval",brief:"用规则、人或模型检查输出质量。",explain:"客观结果可用代码核对；难以自动判断的质量可以人工评分，也可让另一个模型按明确标准评分。",mechanism:"基础练习使用关键词、正则等判分。Bedrock 附录进一步介绍代码评分、人工评分及模型评分。",example:"分类：核对预测标签与人工标注。\n格式：尝试解析 JSON 并校验字段。\n摘要：按信息覆盖和事实一致性评分。",boundary:"关键词命中不代表语义正确；模型评分也有偏差。本仓库不提供完整生产评测平台。",value:"建议重点扩展：加入真实测试集、独立验证集和版本对比。"},
  {id:"rag",name:"检索增强生成",en:"Retrieval-Augmented Generation · RAG",group:"extend",chapter:"搜索与检索附录",status:"延伸阅读入口",source:"rag",brief:"先检索相关资料，再交给模型回答。",explain:"RAG 先从外部资料中找出与问题相关的内容，再把这些内容放入模型上下文，辅助生成有依据的回答。",mechanism:"典型流程为文档处理 → 检索相关片段 → 组装上下文 → 生成答案。向量检索是可选实现之一，并非所有 RAG 都必须使用向量数据库。",example:"问：产品的退款条件是什么？\n先从产品文档检索退款条款，再要求模型依据条款回答并标明出处。",boundary:"本仓库该附录主要提供 Cookbook 和资料链接，没有实现完整 RAG 系统；检索不到正确资料时仍可能答错。",value:"可扩展方向：补充文档接入、检索评测与引用校验。"}
];

const scenarios = [
  {id:"email",label:"邮件分类",title:"把邮件送到正确队列",description:"用清晰的业务标签和少量示例减少分类歧义。",techniques:"清晰指令 · 模板分隔 · Few-shot · 输出格式",gap:"真实标注集、边界案例、格式校验。",task:"将以下客户邮件分类为“售前”“售后”或“其他”。",context:"<email>昨天收到的杯子有裂痕，可以换一个吗？</email>",rules:"分类标准：购买咨询归为售前；已购商品的质量、退换问题归为售后；无法归类时选其他。仅依据邮件，不补充未提供的订单信息。",example:"示例：\n“这款有蓝色吗？” → 售前\n“收到的杯子裂了。” → 售后",output:"仅输出 JSON，包含 category 和 evidence 两个字段。evidence 必须是邮件中的原文片段。"},
  {id:"document",label:"文档问答",title:"先找依据，再回答",description:"使用给定资料回答问题，并让缺失信息保持缺失。",techniques:"模板分隔 · 证据约束 · 拒绝猜测",gap:"文档接入、长文档检索、引用真实性检查。",task:"回答客户的问题：退款到账需要多久？",context:"<document>用户可在签收后 7 天内申请退货。商品需保持完好。运费由责任方承担。</document>",rules:"仅依据文档。先查找支持答案的原句；区分“申请退货期限”和“退款到账时间”。资料没有说明时明确回答资料不足。",example:"示例：\n问题：可以换成其他颜色吗？\n文档未涉及换色 → “资料未说明是否可以换色。”",output:"输出两项：结论、原文依据。若没有依据，写“无相关依据”，不要猜测天数。"},
  {id:"coding",label:"AI 辅助开发",title:"让开发任务可以验收",description:"把项目要求与验证条件交给 AI，减少它猜测实现范围。",techniques:"清晰指令 · 上下文组织 · 任务分解 · 效果验证",gap:"代码仓库访问、实际运行与测试工具；教程并不提供开发代理。",task:"为现有应用实现登录页面。",context:"<project>项目已有表单和按钮组件；登录接口由现有 auth 服务提供；具体字段与错误码以仓库定义为准。</project>",rules:"先阅读现有组件和认证实现，再按已有风格开发。覆盖密码错误、网络失败和提交中状态。若缺少接口定义，明确指出缺口。",example:"验收示例：错误密码应展示接口对应的错误提示，并允许修改后重试，不应跳转到已登录页面。",output:"交付代码修改与验证记录。检查成功登录、失败提示、重复提交和退出流程；区分已实际执行的检查与尚未验证的项目。"}
];

document.querySelectorAll("a[data-source]").forEach((link) => {
  link.href = sources[link.dataset.source];
  link.target = "_blank";
  link.rel = "noopener noreferrer";
});

const escapeHTML = (text) => text.replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
let activeTechnique = "clear";
let activeFilter = "all";
const searchInput = document.querySelector("#search");

function renderDetail(technique) {
  const panel = document.querySelector("#tech-detail");
  if (!technique) {
    panel.innerHTML = '<h3>没有匹配的技术</h3><p class="detail-intro">试试“示例”“工具”或“评估”，也可以清空搜索后选择其他分类。</p>';
    return;
  }
  panel.innerHTML = `<div class="detail-top"><span class="pill ${technique.id === "rag" ? "amber" : ""}">${escapeHTML(technique.status)}</span><span class="chapter">${escapeHTML(technique.chapter)}</span></div>
    <h3>${escapeHTML(technique.name)}</h3><p class="english">${escapeHTML(technique.en)}</p><p class="detail-intro">${escapeHTML(technique.explain)}</p>
    <div class="detail-block"><h4>技术原理 / 简单解释</h4><p>${escapeHTML(technique.mechanism)}</p></div>
    <div class="detail-block"><h4>一个简单例子 · 本页编写</h4><pre>${escapeHTML(technique.example)}</pre></div>
    <div class="detail-block"><h4>适用边界</h4><p>${escapeHTML(technique.boundary)}</p></div>
    <div class="detail-block"><h4>今天怎么看</h4><p>${escapeHTML(technique.value)}</p></div>
    <div class="detail-links"><a href="${sources[technique.source]}" target="_blank" rel="noopener noreferrer">查看对应源码 ↗</a>${technique.extra ? `<a href="${sources[technique.extra]}" target="_blank" rel="noopener noreferrer">当前官方说明 ↗</a>` : ""}</div>`;
}

function renderTechniques() {
  const query = searchInput.value.trim().toLocaleLowerCase();
  const visible = techniques.filter((t) => (activeFilter === "all" || t.group === activeFilter) && `${t.name} ${t.en} ${t.brief} ${t.explain} ${t.mechanism} ${t.chapter}`.toLocaleLowerCase().includes(query));
  if (!visible.some((t) => t.id === activeTechnique)) activeTechnique = visible[0]?.id ?? null;
  document.querySelector("#result-count").textContent = `显示 ${visible.length} / ${techniques.length} 项技术 · 按教学内容归纳，含评估与检索扩展`;
  const list = document.querySelector("#tech-list");
  list.innerHTML = visible.length ? visible.map((t) => `<button class="tech-button ${t.id === activeTechnique ? "selected" : ""}" data-technique="${t.id}" aria-pressed="${t.id === activeTechnique}" aria-controls="tech-detail"><span class="tech-number">${String(techniques.indexOf(t) + 1).padStart(2,"0")}</span><span><strong>${escapeHTML(t.name)}</strong><small>${escapeHTML(t.brief)}</small></span><span class="tech-arrow" aria-hidden="true">↗</span></button>`).join("") : '<p class="empty">未找到匹配项。<br>请调整关键词或分类。</p>';
  list.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
    activeTechnique = button.dataset.technique;
    list.querySelectorAll("button").forEach((item) => {
      const selected = item === button;
      item.classList.toggle("selected", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    renderDetail(techniques.find((t) => t.id === activeTechnique));
  }));
  renderDetail(visible.find((t) => t.id === activeTechnique));
}
document.querySelectorAll("[data-filter]").forEach((button) => button.addEventListener("click", () => {
  activeFilter = button.dataset.filter;
  document.querySelectorAll("[data-filter]").forEach((item) => {
    item.classList.toggle("selected", item === button);
    item.setAttribute("aria-pressed", String(item === button));
  });
  renderTechniques();
}));
searchInput.addEventListener("input", renderTechniques);
renderTechniques();

let activeScenario = scenarios[0];
const scenarioTabs = document.querySelector("#scenario-tabs");
scenarioTabs.innerHTML = scenarios.map((s) => `<button data-scenario="${s.id}" aria-pressed="${s.id === activeScenario.id}" class="${s.id === activeScenario.id ? "selected" : ""}">${s.label}</button>`).join("");

function renderPrompt() {
  const parts = [activeScenario.task];
  document.querySelectorAll("[data-part]").forEach((input) => {
    if (input.checked) parts.push(activeScenario[input.dataset.part]);
  });
  document.querySelector("#prompt-preview").textContent = parts.join("\n\n");
  document.querySelector("#copy-status").textContent = "仅组合示例文本，无 API 请求或密钥配置。";
}
function renderScenario() {
  document.querySelector("#scenario-title").textContent = activeScenario.title;
  document.querySelector("#scenario-description").textContent = activeScenario.description;
  document.querySelector("#scenario-techniques").textContent = activeScenario.techniques;
  document.querySelector("#scenario-gap").textContent = activeScenario.gap;
  scenarioTabs.querySelectorAll("button").forEach((button) => {
    const selected = button.dataset.scenario === activeScenario.id;
    button.classList.toggle("selected", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
  renderPrompt();
}
scenarioTabs.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
  activeScenario = scenarios.find((s) => s.id === button.dataset.scenario);
  renderScenario();
}));
document.querySelectorAll("[data-part]").forEach((input) => input.addEventListener("change", renderPrompt));
document.querySelector("#copy-prompt").addEventListener("click", async () => {
  const text = document.querySelector("#prompt-preview").textContent;
  const status = document.querySelector("#copy-status");
  try {
    await navigator.clipboard.writeText(text);
    status.textContent = "已复制当前提示词。可粘贴到你使用的 AI 工具中。";
  } catch {
    const range = document.createRange();
    range.selectNodeContents(document.querySelector("#prompt-preview"));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    document.querySelector("#prompt-preview").focus();
    status.textContent = "浏览器未允许自动复制，已选中文本，请按 Ctrl+C（Mac 使用 ⌘C）。";
  }
});
renderScenario();

const navLinks = [...document.querySelectorAll(".sidebar nav a")];
const sections = navLinks.map((link) => document.querySelector(link.getAttribute("href")));
let scrollScheduled = false;
function updateNavigation() {
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 160) current = section;
  }
  navLinks.forEach((link) => {
    const active = link.getAttribute("href") === `#${current.id}`;
    link.classList.toggle("active", active);
    if (active) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
  scrollScheduled = false;
}
window.addEventListener("scroll", () => {
  if (!scrollScheduled) {
    scrollScheduled = true;
    window.requestAnimationFrame(updateNavigation);
  }
}, {passive:true});
updateNavigation();
