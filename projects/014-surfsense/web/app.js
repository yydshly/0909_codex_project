'use strict';
const COMMIT = '3448772bd3d5d439114f810ac5da8e5a86967917';
const REPO = `https://github.com/MODSetter/SurfSense/blob/${COMMIT}/`;
const $ = selector => document.querySelector(selector);
const escapeHtml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const scenarios = [
  {id:'product',name:'竞品与用户反馈',question:'用户对知识工具最关注哪些问题？下一版应该优先改进什么？',title:'优先解决导出与协作的摩擦',description:'把内部规划与外部反馈放在一起，寻找产品改进的证据。',output:'反馈摘要、证据清单与改进建议',docs:[
    {id:'P01',type:'PDF',title:'产品访谈摘要',meta:'内部资料 · 虚构样本',text:'受访用户希望一键导出 Markdown，并保留引用链接。跨文档查找比单篇摘要更有价值。用户担心分享资料后无法控制访问权限。',tags:['导出','引用','用户','资料','知识','问题','产品'],insight:'导出时保留引用，可以让研究结果继续用于笔记和后续写作。'},
    {id:'P02',type:'Reddit',title:'社区反馈摘录',meta:'外部反馈 · 虚构样本',text:'几位用户反馈：知识工具的团队协作权限不够直观，检索结果偶尔缺少上下文。比起新增生成模板，他们更希望找到结果后能直接定位原文。',tags:['协作','权限','反馈','用户','知识','问题','原文'],insight:'协作权限和原文定位在反馈中反复出现，值得纳入下一轮需求验证。'},
    {id:'P03',type:'DOCX',title:'下一版功能规划',meta:'内部资料 · 虚构样本',text:'下一版候选功能包括 Markdown 导出、协作权限说明、离线浏览与播客模板。团队计划先验证导出和协作需求，再评估离线支持的实施成本。',tags:['下一版','改进','规划','导出','协作','离线','播客','模板'],insight:'现有规划已包含导出与协作改进，可先验证需求，再决定离线能力的投入。'}]},
  {id:'learning',name:'论文与学习资料',question:'检索增强与模型微调有什么区别？资料经常变化时应该如何选择？',title:'资料常变时，先评估检索增强',description:'对照多份笔记理解技术选择，并保留每项判断的出处。',output:'方法对照、学习摘要与引用笔记',docs:[
    {id:'L01',type:'PDF',title:'RAG 课程笔记',meta:'课程资料 · 教学样本',text:'检索增强在回答时读取外部资料。资料更新后重新索引，不必为每次内容更新修改模型参数。回答质量受到检索覆盖率、片段质量和生成模型影响。',tags:['检索','增强','资料','更新','变化','rag','选择'],insight:'检索增强适合读取可更新的外部知识，但应验证相关证据是否被召回。'},
    {id:'L02',type:'MD',title:'微调实验摘要',meta:'学习笔记 · 教学样本',text:'模型微调通过训练更新参数，可用于调整任务行为和输出风格。微调不自动提供外部事实的引用，也不等于能可靠记忆所有训练资料。',tags:['微调','训练','模型','区别','风格','引用'],insight:'微调主要改变模型行为与参数；如果目标是实时事实和可追溯引用，仍需考虑检索。'},
    {id:'L03',type:'DOCX',title:'技术选型讨论',meta:'讨论记录 · 教学样本',text:'资料频繁变化且需要引用时，先建立检索增强基线；任务格式稳定但模型经常不遵循时，可以评估微调。两者可以组合，最终用实际任务集比较质量、成本和延迟。',tags:['资料','变化','选择','区别','微调','检索','评估','成本'],insight:'先根据任务建立可评估的基线，两种方法可以组合，而非必须二选一。'}]},
  {id:'team',name:'团队知识与入职',question:'新同事如何申请项目访问权限，遇到阻塞应该找谁？',title:'按角色申请，按问题寻找负责人',description:'从团队手册、会议纪要和常见问题中定位工作所需的信息。',output:'入职指南、会议准备与问答清单',docs:[
    {id:'T01',type:'PDF',title:'团队入职手册',meta:'内部手册 · 虚构样本',text:'新同事先提交项目名称与职责，由项目负责人确认访问范围。阅读资料默认申请 Viewer，需要维护内容时再申请 Editor。不要直接共享他人账号。',tags:['新同事','入职','权限','申请','项目','访问','角色'],insight:'先说明项目和职责，按最小需要申请阅读或编辑权限。'},
    {id:'T02',type:'MD',title:'协作常见问题',meta:'知识库条目 · 虚构样本',text:'访问申请被阻塞时，先联系项目负责人确认成员关系，再由工作区管理员检查角色配置。资料打不开时应记录文档链接与报错信息。',tags:['阻塞','权限','谁','访问','管理员','资料','申请'],insight:'项目负责人确认业务范围，工作区管理员处理成员与角色配置。'},
    {id:'T03',type:'DOCX',title:'本周交接纪要',meta:'会议纪要 · 虚构样本',text:'本周入职资料已更新。交接人负责讲解项目背景，管理员负责完成权限配置，新同事应在首次协作前确认能打开目标文件。',tags:['新同事','入职','权限','协作','项目','交接'],insight:'首次协作前核验目标文件是否可访问，并向交接人补齐业务背景。'}]}
];
const connectors = [
  {id:'reddit',name:'Reddit',icon:'R',desc:'帖子、评论与社区内容',input:'搜索词 / 社区 / 帖子网址',sample:{demo:true,kind:'post',title:'希望知识工具支持导出与引用',community:'example_community',comments:[{text:'团队权限需要更直观。'}]},principle:'专用采集器负责分页和解析。核对的实现会先用浏览器建立会话，再通过 HTTP 复用会话读取 JSON，并处理代理、限流与失败。',path:'surfsense_backend/app/proprietary/platforms/reddit/fetch.py'},
  {id:'youtube',name:'YouTube',icon:'Y',desc:'视频资料、字幕与评论',input:'视频网址 / 搜索目标',sample:{demo:true,title:'知识管理方法介绍（示例）',transcript:'先收集资料，再建立检索与引用。',comments:[{text:'希望补充团队使用流程。'}]},principle:'上游提供视频数据、字幕和评论等平台工具；不同数据类型走相应的采集与解析路径。可取得内容受源站可见性和部署配置影响。',path:'surfsense_backend/app/proprietary/platforms/youtube/scraper.py'},
  {id:'google',name:'Google Search',icon:'G',desc:'搜索结果与页面线索',input:'搜索词',sample:{demo:true,query:'知识库 工具 对比',results:[{title:'示例资料：团队知识管理',url:'https://example.com/research',snippet:'关于引用、检索和协作的讨论。'}]},principle:'返回搜索结果线索；搜索结果摘要与页面完整正文是不同内容，研究任务可以继续抓取相关页面。',path:'surfsense_backend/app/proprietary/platforms/google_search/scraper.py'},
  {id:'maps',name:'Google Maps',icon:'M',desc:'地点、评分与公开评价',input:'地点 / 搜索目标',sample:{demo:true,name:'示例咖啡店',reviews:[{text:'工作日环境安静，周末等待较久。'}]},principle:'将地点和评价整理为可分析的条目，适用于本地商业研究；样本覆盖和排序会影响研究结论。',path:'surfsense_backend/app/proprietary/platforms/google_maps/scraper.py'},
  {id:'social',name:'Instagram / TikTok',icon:'@',desc:'公开内容、账号与互动',input:'公开内容或账号目标',sample:{demo:true,platform:'social',profile:'example_creator',posts:[{caption:'知识工具使用体验',topic:'工作效率'}]},principle:'针对平台的公开数据设计工具。各平台支持字段不同，不能将一个连接器的能力泛化到全部平台。',path:'surfsense_mcp/README.md'},
  {id:'commerce',name:'Amazon / Walmart',icon:'A',desc:'商品、报价与评价资料',input:'商品网址 / 商品目标',sample:{demo:true,product:'示例产品',offers:[{currency:'USD',price:49}],note:'虚构金额；非实时报价'},principle:'提供商品相关结构化数据；Walmart 还有评价工具。字段和可见数据依平台工具而异，不应假设都能读取完整历史。',path:'surfsense_mcp/README.md'},
  {id:'indeed',name:'Indeed',icon:'i',desc:'公开职位与职位描述',input:'职位搜索词 / 公司目标',sample:{demo:true,jobTitle:'知识管理专员',company:'Example Company',description:'维护团队资料与研究流程。'},principle:'将公开招聘信息转换成结构化条目，便于招聘需求研究。实际结果取决于目标与可访问内容。',path:'surfsense_backend/app/proprietary/platforms/indeed_jobs/scraper.py'},
  {id:'web',name:'Web / 外部 MCP',icon:'↗',desc:'通用网页与扩展工具',input:'网页 URL / 外部 MCP 配置',sample:{demo:true,url:'https://example.com/docs',markdown:'# 示例文档\n这是教学内容。'},principle:'通用网页采集用于读取页面；外部 MCP 是另一种扩展机制，将第三方服务工具接入 Agent，需要对应授权和配置。',path:'surfsense_mcp/README.md'}
];
const steps = [
  {name:'接入资料',tag:'INPUT',intro:'把分散的信息引入工作区。',input:'文件、网盘同步内容、网页资料',action:'上传和连接器负责接收资料并记录来源。后台任务推进处理状态。',output:'待处理文档与来源元数据',path:'surfsense_backend/app/tasks/document_processors/file_processors.py'},
  {name:'解析与切分',tag:'EXTRACT',intro:'把不同格式转换成可检索片段。',input:'PDF、Office、图片、音频等',action:'统一提取流程转换内容；按配置使用视觉理解或音频转写。切分逻辑专门处理 Markdown 表格完整性。',output:'文本片段、顺序及位置',path:'surfsense_backend/app/indexing_pipeline/document_chunker.py'},
  {name:'向量化与去重',tag:'INDEX',intro:'为后续查询建立语义索引。',input:'文档文本及分块',action:'计算内容标识，处理重复与更新，调用 Embedding 模型生成向量，并使用缓存减少重复计算。',output:'可索引文档、片段及向量',path:'surfsense_backend/app/indexing_pipeline/indexing_pipeline_service.py'},
  {name:'知识存储',tag:'STORE',intro:'将证据与检索数据关联保存。',input:'内容、向量、工作区与来源信息',action:'PostgreSQL 保存文档和片段，pgvector 支持相似度查询；检索按工作区等条件限定范围。',output:'后续可搜索的知识库',path:'docker/docker-compose.yml'},
  {name:'Agent 规划',tag:'PLAN',intro:'根据问题选择合适的工具。',input:'用户问题、可用工具与会话上下文',action:'组织模型、系统指令、工具、中间件和子 Agent；可调用知识库、实时连接器及外部 MCP。',output:'工具调用及中间研究结果',path:'surfsense_backend/app/agents/chat/multi_agent_chat/main_agent/runtime/factory.py'},
  {name:'混合检索',tag:'RETRIEVE',intro:'结合语义相似与关键词匹配。',input:'问题文本、Embedding 与搜索范围',action:'语义和全文查询分别产生排名，以 RRF 合并：1/(60+语义排名) + 1/(60+关键词排名)。缺失一侧时该项为 0。',output:'按文档组织的命中片段',path:'surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/hybrid_search.py'},
  {name:'重排序',tag:'RERANK',intro:'可选地再评估候选资料相关性。',input:'问题与候选文档的命中片段',action:'配置了 reranker 时，按片段内容重新排列文档；未配置则保留原顺序。',output:'重新排序的检索结果',path:'surfsense_backend/app/agents/chat/multi_agent_chat/shared/retrieval/reranking.py'},
  {name:'生成与引用',tag:'ANSWER',intro:'结合证据组织回答与成果。',input:'检索内容、片段 ID 与工具结果',action:'模型结合相关材料生成回答，以片段标识关联引用。资料可用于报告、文档、演示或其他生成任务。',output:'可核查的回答或研究成果',path:'surfsense_backend/app/retriever/chunks_hybrid_search.py'}
];
let scenario = scenarios[0], selected = new Set(scenario.docs.map(d=>d.id)), lastResult = null, busy = false;
const configText = JSON.stringify({mcpServers:{surfsense:{url:'https://mcp.surfsense.com/mcp',headers:{Authorization:'Bearer YOUR_SURFSENSE_API_KEY'}}}},null,2);
function navigate(){const requested=location.hash.slice(1);const view=['research','connectors','architecture','scenarios','boundaries'].includes(requested)?requested:'architecture';document.querySelectorAll('.view').forEach(el=>el.hidden=el.id!==view);document.querySelectorAll('[data-view]').forEach(a=>{a.classList.toggle('active',a.dataset.view===view);if(a.dataset.view===view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});}
function chooseScenario(id){if(busy)return false;const next=scenarios.find(s=>s.id===id);if(!next)throw new Error('未知研究场景');scenario=next;selected=new Set(scenario.docs.map(d=>d.id));lastResult=null;renderScenario();showSample();return true;}
function renderScenario(){
  $('#scenario-buttons').innerHTML=scenarios.map(s=>`<button type="button" data-scenario="${s.id}" class="${s.id===scenario.id?'active':''}" aria-pressed="${s.id===scenario.id}">${s.name}</button>`).join('');
  $('#question').value=scenario.question;
  $('#source-list').innerHTML=scenario.docs.map(d=>`<label class="source-row"><input type="checkbox" value="${d.id}" checked><span><span class="source-type">${d.type}</span><strong>${d.title}</strong><small>${d.meta}</small></span></label>`).join('');
  $('#source-count').textContent=`${selected.size} / ${scenario.docs.length}`;
  document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>chooseScenario(b.dataset.scenario)));
  $('#source-list').querySelectorAll('input').forEach(input=>input.addEventListener('change',()=>{input.checked?selected.add(input.value):selected.delete(input.value);$('#source-count').textContent=`${selected.size} / ${scenario.docs.length}`;lastResult=null;$('#result').innerHTML='<div class="empty-state"><h3>资料范围已更新</h3><p>点击“运行演示”，重新查找所选资料中的证据。</p></div>';renderEvidence([]);markSteps(-1);}));
  markSteps(-1);
}
function rankDocuments(query,docs){const q=query.toLowerCase();const explicit=['导出','协作','离线','播客','引用','检索','微调','训练','rag','管理员','阻塞','权限'].filter(t=>q.includes(t));const tokens=q.match(/[a-z0-9]+|[\u3400-\u9fff]{2}/g)||[];return docs.map(d=>({doc:d,score:explicit.length?explicit.reduce((n,t)=>n+((d.text+' '+d.tags.join(' ')).toLowerCase().includes(t)?3:0),0):d.tags.reduce((n,t)=>n+(q.includes(t.toLowerCase())?2:0),0)+tokens.reduce((n,t)=>n+(d.text.toLowerCase().includes(t)?1:0),0)})).filter(d=>d.score>0).sort((a,b)=>b.score-a.score);}
function showSample(){const hits=scenario.docs.map(doc=>({doc,score:null}));renderResult(hits,scenario.question,true);}
function markSteps(index){document.querySelectorAll('#run-steps li').forEach((li,i)=>{li.classList.toggle('done',i<index);li.classList.toggle('current',i===index);});}
function renderResult(hits,query,sample=false){
  const docs=hits.map(h=>h.doc);lastResult={query,docs,sample,scenario:scenario.name};
  if(!docs.length){$('#result').innerHTML='<div class="empty-state"><h3>没有找到匹配的证据</h3><p>尝试资料中的关键词，例如“导出”“微调”或“权限”，或切换研究场景。此演示不理解任意自然语言，也不会编造答案。</p></div>';renderEvidence([]);return;}
  const curated=query===scenario.question;
  $('#result').innerHTML=`<div class="result-label"><strong>${sample?'预置研究样例':'检索完成 · 教学演示'}</strong><span>${docs.length} 份资料</span></div><h3 class="answer-title">${curated&&docs.length===scenario.docs.length?scenario.title:curated?'基于所选资料的研究线索':'与你的问题匹配的资料原文'}</h3>${docs.map((d,i)=>`<p class="answer-paragraph">${escapeHtml(curated?d.insight:d.text)} <button class="citation" data-cite="${d.id}" aria-label="查看引用 ${i+1}：${d.title}">${i+1}</button></p>`).join('')}<p class="result-note">${curated?'以上为预先编写的教学归纳，展示证据与结论的关联。':'以上是本地关键词匹配的原文摘录，不是大模型生成的答案。'} 真实系统使用混合检索与模型推理。</p><button class="text-button" id="export-result">下载本次证据笔记 ↓</button>`;
  $('#export-result').addEventListener('click',exportResult);bindCitations($('#result'));renderEvidence(docs);
}
function renderEvidence(docs){$('#evidence-count').textContent=String(docs.length);$('#evidence-list').innerHTML=docs.length?docs.map((d,i)=>`<button class="evidence-card" data-cite="${d.id}"><span class="evidence-id">[${i+1}] ${d.type} · ${d.id}</span><strong>${d.title}</strong><p>${d.text}</p></button>`).join(''):'<p class="muted">运行演示后，匹配的资料会出现在这里。</p>';bindCitations($('#evidence-list'));}
function bindCitations(root){root.querySelectorAll('[data-cite]').forEach(b=>b.addEventListener('click',()=>openCitation(b.dataset.cite)));}
function openCitation(id){const doc=scenario.docs.find(d=>d.id===id);if(!doc)return;$('#citation-content').innerHTML=`<h2>${doc.title}</h2><p>${doc.type} · ${doc.id} · ${doc.meta}</p><blockquote>${doc.text}</blockquote><p>这段内容是内置教学资料，未从平台实时采集。真实 SurfSense 保留文档与片段标识，供回答引用。</p>`;$('#citation-dialog').showModal();}
async function runResearch(query){
  if(busy)throw new Error('演示正在运行');const q=String(query).trim();if(!q){toast('请输入一个研究问题');return {status:'empty_query'};}if(q.length>500)throw new Error('问题最多 500 字');
  if(!selected.size){$('#result').innerHTML='<div class="empty-state"><h3>请先选择资料</h3><p>至少勾选一份资料，才能进行本地检索。</p></div>';renderEvidence([]);lastResult=null;return {status:'no_sources'};}
  busy=true;$('#run-button').disabled=true;$('#run-button').textContent='演示运行中…';$('#question').disabled=true;document.querySelectorAll('[data-scenario],#source-list input').forEach(el=>el.disabled=true);
  $('#result').innerHTML='<div class="empty-state"><h3>正在整理所选资料…</h3><p>流程动画用于解释步骤，不代表真实 API 调用。</p></div>';renderEvidence([]);
  try{for(let i=0;i<4;i++){markSteps(i);await new Promise(resolve=>setTimeout(resolve,matchMedia('(prefers-reduced-motion: reduce)').matches?0:300));}const hits=rankDocuments(q,scenario.docs.filter(d=>selected.has(d.id)));markSteps(4);renderResult(hits,q);return {status:'complete',demo:true,matched_documents:hits.map(h=>h.doc.id)};}
  finally{busy=false;$('#run-button').disabled=false;$('#run-button').innerHTML='运行演示 <span>↗</span>';$('#question').disabled=false;document.querySelectorAll('[data-scenario],#source-list input').forEach(el=>el.disabled=false);}
}
function exportResult(){if(!lastResult)return;const body=`# SurfSense 教学证据笔记\n\n场景：${lastResult.scenario}\n\n问题：${lastResult.query}\n\n> 内置教学资料；非实时数据，未调用上游服务或大模型。\n\n${lastResult.docs.map((d,i)=>`## [${i+1}] ${d.title}\n\n来源类型：${d.type} · 文档标识：${d.id}\n\n${d.text}\n`).join('\n')}\n上游：https://github.com/MODSetter/SurfSense\n研究提交：${COMMIT}\n`;const url=URL.createObjectURL(new Blob([body],{type:'text/markdown;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='surfsense-evidence-note.md';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('证据笔记已下载');}
function selectConnector(id){const c=connectors.find(c=>c.id===id);if(!c)return;document.querySelectorAll('[data-connector]').forEach(b=>{b.classList.toggle('active',b.dataset.connector===id);b.setAttribute('aria-pressed',String(b.dataset.connector===id));});$('#connector-detail').innerHTML=`<p class="eyebrow">CONNECTOR EXPLORER</p><h2>${c.name}</h2><p>${c.desc}</p><h3>提供什么</h3><p>${c.input}</p><h3>结构化内容示意 · 非接口字段契约</h3><pre>${escapeHtml(JSON.stringify(c.sample,null,2))}</pre><h3>实际如何工作</h3><p>${c.principle}</p><a href="${REPO+c.path}" target="_blank" rel="noopener noreferrer">查看上游依据 ↗</a>`;}
function selectStep(index){const s=steps[index];if(!s)return;document.querySelectorAll('[data-step]').forEach(b=>{b.classList.toggle('active',Number(b.dataset.step)===index);b.setAttribute('aria-pressed',String(Number(b.dataset.step)===index));});$('#step-detail').innerHTML=`<div><span class="tiny-label">${s.tag} · ${String(index+1).padStart(2,'0')}</span><h2>${s.name}</h2><p>${s.intro}</p><a target="_blank" rel="noopener noreferrer" href="${REPO+s.path}">阅读对应源码 ↗</a></div><dl><dt>输入</dt><dd>${s.input}</dd><dt>处理</dt><dd>${s.action}</dd><dt>输出</dt><dd>${s.output}</dd></dl>`;}
let toastTimer;function toast(message){clearTimeout(toastTimer);$('#toast').textContent=message;$('#toast').hidden=false;toastTimer=setTimeout(()=>$('#toast').hidden=true,3000);}
window.addEventListener('hashchange',navigate);
$('#question-form').addEventListener('submit',event=>{event.preventDefault();runResearch($('#question').value).catch(()=>toast('演示未完成，请重新尝试。'));});
$('#question').addEventListener('input',()=>{if(lastResult){lastResult=null;$('#result').innerHTML='<div class="empty-state"><h3>问题已修改</h3><p>运行演示，查找与新问题匹配的资料。</p></div>';renderEvidence([]);markSteps(-1);}});
$('#close-dialog').addEventListener('click',()=>$('#citation-dialog').close());
$('#citation-dialog').addEventListener('click',event=>{if(event.target===$('#citation-dialog')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();}});
$('#connector-grid').innerHTML=connectors.map(c=>`<button class="connector-card" data-connector="${c.id}"><span class="letter-icon">${c.icon}</span><strong>${c.name}</strong><p>${c.desc}</p></button>`).join('');
document.querySelectorAll('[data-connector]').forEach(b=>b.addEventListener('click',()=>selectConnector(b.dataset.connector)));
steps.forEach((s,i)=>{$(i<4?'#ingestion-flow':'#query-flow').insertAdjacentHTML('beforeend',`<button class="flow-node" data-step="${i}"><span>${String(i+1).padStart(2,'0')} / ${s.tag}</span><strong>${s.name}</strong></button>`);});
document.querySelectorAll('[data-step]').forEach(b=>b.addEventListener('click',()=>selectStep(Number(b.dataset.step))));
$('#use-case-grid').innerHTML=scenarios.map((s,i)=>`<article class="use-case"><span class="case-number">0${i+1}</span><h2>${s.name}</h2><p>${s.description}</p><div class="case-question">“${s.question}”</div><p><strong>可形成的成果</strong><br>${s.output}</p><button class="text-button" data-start="${s.id}">体验这个场景 →</button></article>`).join('');
document.querySelectorAll('[data-start]').forEach(b=>b.addEventListener('click',()=>{if(chooseScenario(b.dataset.start)){location.hash='research';window.scrollTo({top:0});}else toast('请等待当前演示完成');}));
$('#mcp-config').textContent=configText;$('#copy-config').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(configText);toast('配置已复制；请替换示例 Key');}catch{const range=document.createRange();range.selectNodeContents($('#mcp-config'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('请复制已选中的配置文本');}});
$('#source-links').innerHTML=[['项目说明','README.md'],['混合检索',steps[5].path],['Agent 编排',steps[4].path],['MCP 工具','surfsense_mcp/README.md'],['部署配置','docker/docker-compose.yml'],['主体许可','LICENSE'],['BSL 许可','surfsense_backend/app/proprietary/LICENSE']].map(([label,path])=>`<a href="${REPO+path}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`).join('');
renderScenario();showSample();selectConnector('reddit');selectStep(5);navigate();

// Optional agent access uses the same demonstration actions as the visible UI.
if(document.modelContext?.registerTool){
  const lifecycle=new AbortController();
  window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
  try{Promise.resolve(document.modelContext.registerTool({
    name:'run_surfsense_teaching_demo',title:'运行 SurfSense 教学检索',
    description:'切换教学场景并在全部内置样本中执行本地关键词检索。仅更新当前展示页，不调用真实 SurfSense 或任何外部服务。',
    inputSchema:{type:'object',properties:{scenario:{type:'string',enum:['product','learning','team']},query:{type:'string',minLength:1,maxLength:500}},required:['scenario','query'],additionalProperties:false},
    annotations:{readOnlyHint:false,untrustedContentHint:false},
    async execute(input){
      if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).some(k=>!['scenario','query'].includes(k))||!scenarios.some(s=>s.id===input.scenario)||typeof input.query!=='string'||!input.query.trim()||input.query.length>500)throw new Error('请提供有效场景和 1–500 字的问题');
      if(busy)throw new Error('当前演示正在运行，请稍后重试');
      chooseScenario(input.scenario);$('#question').value=input.query;location.hash='research';navigate();return await runResearch(input.query);
    }
  },{signal:lifecycle.signal})).catch(()=>{});}catch{/* Unsupported registries do not affect the page. */}
}
