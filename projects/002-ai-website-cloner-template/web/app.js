'use strict';
const stages = [
  ['观察页面','先确认实际看到了什么。','固定 URL、视口和主题，观察整体区域；滚动触发懒加载，并保存参考截图。','目标 URL、任务范围、可访问的页面。','页面拓扑、截图、未覆盖区域。','截图只有当前画面；DOM 也可能尚未包含未加载的内容。'],
  ['提取事实','把像素印象变成可追溯读数。','读取 DOM、计算样式、位置尺寸、伪元素和素材地址；按区域保存，避免只留下模型摘要。','浏览器中的元素与资源。','样式快照、文本、素材和采集条件。','当前 600px 宽度无法单独证明它来自固定值、百分比还是网格。'],
  ['归纳与推断','用多份证据寻找规则。','跨元素识别重复样式；多宽度比较布局；执行动作并记录前后变化。','多个元素、视口、状态的采集结果。','规范候选、响应式规则和状态转换。','直接读取、操作确认、推断和未知必须分开；行为变化不证明内部算法。'],
  ['形成规格','让实现与验收使用同一依据。','把结构、样式、素材、输入、事件、状态归属和验收条件写进组件规格。','已确认的事实与明确标注的假设。','组件规格和共享基础约定。','上游主要使用 Markdown；结构化必填校验、置信度和规格版本是扩展建议。'],
  ['拆分实现','先公共基础，再独立组件。','主代理维护主题与公共接口，按职责分派组件；依赖确定后并行，再合并页面。','规格、公共样式、真实素材。','Next.js 组件、路由及可运行页面。','worktree 只隔离工作，不自动解决状态、样式和接口冲突。'],
  ['验证与修复','沿差异回到问题发生的环节。','固定环境比较截图、布局与行为。采集错则重采集，规格错则改规格，实现错则修组件。','本地页面、原站证据、相同视口和状态。','差异、修复记录、验收结果与已知缺口。','构建通过不代表视觉一致；截图接近不代表后端业务相同。']
];
const stepButtons = [...document.querySelectorAll('[data-step]')];
const detail = document.getElementById('step-detail');
function showStage(index) {
  const [name,title,description,input,output,limit] = stages[index];
  stepButtons.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
  detail.replaceChildren();
  const label=document.createElement('p'); label.className='eyebrow'; label.textContent=`${String(index+1).padStart(2,'0')} / ${name}`;
  const heading=document.createElement('h3'); heading.textContent=title;
  const paragraph=document.createElement('p'); paragraph.textContent=description;
  const list=document.createElement('dl');
  [['输入',input],['产物',output],['注意',limit]].forEach(([term,text])=>{const dt=document.createElement('dt');dt.textContent=term;const dd=document.createElement('dd');dd.textContent=text;list.append(dt,dd);});
  detail.append(label,heading,paragraph,list);
}
stepButtons.forEach((button,index)=>{
  button.addEventListener('click',()=>showStage(index));
  button.addEventListener('keydown',event=>{
    let next;
    if(['ArrowDown','ArrowRight'].includes(event.key)) next=(index+1)%stepButtons.length;
    if(['ArrowUp','ArrowLeft'].includes(event.key)) next=(index+stepButtons.length-1)%stepButtons.length;
    if(event.key==='Home')next=0;if(event.key==='End')next=stepButtons.length-1;
    if(next!==undefined){event.preventDefault();stepButtons[next].focus();showStage(next);}
  });
});
const states={initial:['初始状态','示例读数：高度 88px；背景透明；无阴影。'],scrolled:['滚动后','示例读数：高度 64px；浅色背景；出现阴影。'],restored:['返回顶部','示例读数：恢复 88px；背景透明；阴影消失。']};
document.querySelectorAll('[data-state]').forEach(button=>button.addEventListener('click',()=>{
  const key=button.dataset.state;
  document.querySelectorAll('[data-state]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
  document.getElementById('mini-header').classList.toggle('scrolled',key==='scrolled');
  document.getElementById('example-state').textContent=states[key][0];
  document.getElementById('measurement').textContent=states[key][1];
}));
const diagram=document.getElementById('diagram-dialog');
if(typeof diagram.showModal==='function'){
  const opener=document.getElementById('open-diagram');opener.hidden=false;
  opener.addEventListener('click',()=>diagram.showModal());
  document.getElementById('close-diagram').addEventListener('click',()=>diagram.close());
}
