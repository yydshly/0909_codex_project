'use strict';
const scenes = {
  repository:{kicker:'REAL REPOSITORY / 中文源码实战',title:'我们的研究库，怎样把项目变成网页？',description:'真实分析对象是 0909_codex_project：从模板创建子项目、登记清单、同步索引，到组合静态网页并手动发布。图中 11 个节点对应真实职责，14 处来源绑定固定版本。',reading:'先看顶部收录与索引，再看中部站点构建，最后看右下方网页发布。箭头表示文件和数据的流向，不是全部函数调用的时序。',try:'点选“静态站点构建”，在详情中打开“来源”链接，查看 catalog.py 的真实代码；也可切换上方三个中文章节逐步阅读。'},
  architecture:{kicker:'ARCHITECTURE / 系统全貌',title:'一个 Web 应用，从入口到数据库',description:'沿 Users → CloudFront → Load Balancer → API Server → PostgreSQL 阅读主链路，再看缓存与异步任务分支。',reading:'实线主链路说明同步访问；下方消息队列和 Worker 展示异步工作；区域和安全组框说明部署边界。',try:'点选 API Server 查看关联节点；按 / 搜索；在工具栏切换主题、视觉风格，或导出 SVG / PNG。'},
  workflow:{kicker:'WORKFLOW / 任务协作',title:'Agent 怎样完成一次工具调用',description:'用户提出任务，Agent 规划并选择工具，经过审批后执行，最后回传答案；泳道把不同参与方分开。',reading:'横向看执行顺序，纵向看责任归属。Policy & Recovery 展示审批、阻止和重试分支；底部单独呈现工具与证据。',try:'点选 Approval Gate 观察关联关系；搜索 Tool Call；在完整交互图中切换风格，观察泳道与路径保持稳定。'},
  sequence:{kicker:'SEQUENCE / 一次请求',title:'缓存没有命中，然后发生什么？',description:'从打开页面到认证、读取 Redis、回退数据库、写入缓存和返回响应，按时间从上到下阅读。',reading:'竖线代表参与方，箭头代表消息；返回调用的样式更轻，异步 Trace 与用户响应分开，便于解释一次请求的完整过程。',try:'使用上方章节切换至 Cache fallback；点选 Redis 看节点详情；在完整图中按 P 播放当前章节。'},
  dataflow:{kicker:'DATA FLOW / 数据去向',title:'产品事件如何变成指标与特征',description:'Web 和移动端事件经过采集、策略检查、事件流与仓库，最终进入指标看板和机器学习特征。',reading:'从左至右看 Sources、Ingest、Process、Store、Consume。安全色路径单独标出身份与敏感数据，虚线表示次要批处理路径。',try:'点选 Warehouse 查看关联关系；用上游追踪观察数据来源，用下游追踪查看看板与特征消费者。'},
  lifecycle:{kicker:'LIFECYCLE / 状态变化',title:'一个任务，从排队到结束',description:'主阶段由 Queued、Planning、Executing、Reviewing、Completed 构成；等待、恢复和终止分布在不同泳道。',reading:'Needs Approval 与 Blocked 表示暂停；Failed 有恢复路径；Cancelled 与 Expired 是终止出口。它表达状态转换，不表示真实任务正在运行。',try:'点选 Executing，观察等待和失败分支；用 Recovery and terminal exits 章节区分可恢复错误与终止状态。'},
  delta:{kicker:'ARCHITECTURE DELTA / 版本对照',title:'结算平台改造，到底改变了什么？',description:'同一组稳定身份的组件在 Before、Delta、After 中对照，展示组件新增与删除、属性变化、位置移动和关系改道。',reading:'切换改造前、差异和改造后三个视图，再展开下方具体变更条目。差异来自两份图规格，不会自动推断风险、故障影响或合并安全。',try:'选择一个变更条目定位对应对象，或使用 Review 播放有限次变更讲解。差异页的控件与普通图形查看器不同。'}
};
const frame=document.getElementById('diagram');
const tabs=[...document.querySelectorAll('[role=tab]')];
let current='';
let timer;
function selectScene(id,fragment='',updateHash=true){
  if(!scenes[id])id='repository';
  const s=scenes[id];
  tabs.forEach(b=>{const active=b.dataset.scene===id;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});
  document.getElementById('scene').setAttribute('aria-labelledby',`tab-${id}`);
  for(const [el,key] of [['scene-kicker','kicker'],['scene-title','title'],['scene-description','description'],['reading-note','reading'],['try-note','try']])document.getElementById(el).textContent=s[key];
  const url=`./diagrams/${id}.html${fragment?'#'+fragment:''}`;
  document.getElementById('open-diagram').href=url;
  document.getElementById('mobile-preview').href=url;
  document.getElementById('preview-image').src=`./assets/${id}-preview.png`;
  document.getElementById('preview-image').alt=s.title+' · 完整图形预览';
  const source=document.getElementById('source-link');
  source.href=`./specs/${id==='delta'?'delta-head':id}.json`;
  source.textContent=id==='delta'?'查看改造后 JSON ↗':'查看图规格 JSON ↗';
  document.getElementById('receipt-link').href=`./receipts/${id}.json`;
  frame.title=s.title+' · Archify 原生交互演示';
  if(frame.getAttribute('src')!==url||!current){
    document.getElementById('load-status').textContent='正在载入图形…';
    frame.src=url;current=id;
    clearTimeout(timer);timer=setTimeout(()=>{document.getElementById('load-status').textContent='若未显示，请打开完整交互图 ↗';},12000);
  }
  if(updateHash)history.replaceState(null,'',`#${id}`);
}
frame.addEventListener('load',()=>{clearTimeout(timer);document.getElementById('load-status').textContent='已载入 · 点击图内探索';});
tabs.forEach((b,index)=>{
  b.addEventListener('click',()=>selectScene(b.dataset.scene));
  b.addEventListener('keydown',event=>{let next=index;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;event.preventDefault();tabs[next].focus();selectScene(tabs[next].dataset.scene);});
});
document.querySelectorAll('[data-jump]').forEach(b=>b.addEventListener('click',()=>{selectScene(b.dataset.jump,b.dataset.fragment||'');document.getElementById('explore').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});}));
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(scenes[id])selectScene(id,'',false);});
selectScene(location.hash.slice(1)||'repository','',false);
