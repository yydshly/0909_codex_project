(() => {
  'use strict';
  const data = window.RNSKILL_CATALOG;
  const $ = selector => document.querySelector(selector);
  const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const categories = new Map(data.categories.map(c => [c.id,c]));
  const byKey = new Map(data.skills.map(s => [s.key,s]));
  const featured = ['ra-选题','ra-人话','ra-video-production-director','tts-skill','ra-audio-to-subtitles','rn-cover-skill','xhs-article-to-images','rn-motion-replica','ra-local-talking-head-cut','ra-复盘','dbs-diagnosis','dbs-content-system'];
  const skills = [...data.skills].sort((a,b) => {
    const indexA=featured.indexOf(a.key), indexB=featured.indexOf(b.key);
    return (indexA<0?999:indexA)-(indexB<0?999:indexB);
  });
  let state = {category:'all', query:'', reuse:'all', type:'all', limit:12};
  $('#categories').innerHTML = data.categories.map(c=>`<button class="category" data-category="${c.id}" aria-pressed="false"><span><i>${c.number}</i>${c.name}</span><b>${c.count}</b></button>`).join('');
  const loadRow = document.createElement('div');
  loadRow.className='load-row';
  loadRow.innerHTML='<button class="load-more" id="load-more">查看更多能力 ↓</button>';
  $('#cards').after(loadRow);
  function reset() {
    state={category:'all',query:'',reuse:'all',type:'all',limit:12};
    $('#search').value=''; $('#reuse').value='all'; $('#entry-type').value='all'; render();
  }
  function render() {
    const terms=state.query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    const results=skills.filter(s => {
      const haystack=[s.title,s.key,s.name,s.summary,s.input,s.output,s.dependencies,categories.get(s.category).name].join(' ').toLocaleLowerCase();
      return (state.category==='all'||s.category===state.category) &&
        (state.reuse==='all'||s.reuse===state.reuse) &&
        (state.type==='all'||(state.type==='nested'&&s.nested)||(state.type==='top'&&!s.nested)||(state.type==='alias'&&s.alias)) &&
        terms.every(t=>haystack.includes(t));
    });
    const visible=results.slice(0,state.limit);
    const cat=state.category==='all'?'全部能力':categories.get(state.category).name;
    $('#title-count').textContent=results.length;
    $('#result-summary').textContent=`${cat} · 共 ${results.length} 个入口 · 当前显示 ${visible.length} 个`;
    $('#reset').hidden=state.category==='all'&&!state.query&&state.reuse==='all'&&state.type==='all';
    document.querySelectorAll('[data-category]').forEach(b=>{
      const active=b.dataset.category===state.category;
      b.classList.toggle('active',active); b.setAttribute('aria-pressed',String(active));
    });
    $('#cards').innerHTML=visible.map(s=>{
      const group=categories.get(s.category);
      return `<article class="capability-card"><div class="card-top"><span class="group-icon" aria-label="${group.name}">${group.number}</span><span class="badge ${s.reuse}">${data.reuseLabels[s.reuse]}</span></div><h3>${escape(s.title)}</h3><p class="skill-key">${escape(s.key)}</p><p class="card-description">${escape(s.summary)}</p><div class="card-output"><span>产物</span><p>${escape(s.output)}</p></div><div class="card-bottom"><span class="card-category">${group.name}${s.alias?' · 别名':s.nested?' · 嵌套':''}</span><button class="card-open" data-skill="${escape(s.key)}" aria-label="查看${escape(s.title)}详情">查看能力</button></div></article>`;
    }).join('');
    $('#empty').hidden=results.length!==0;
    loadRow.hidden=visible.length===results.length;
    $('#load-more').textContent=`查看更多能力 · 还有 ${results.length-visible.length} 个 ↓`;
  }
  document.querySelectorAll('[data-category]').forEach(button=>button.addEventListener('click',()=>{
    state.category=button.dataset.category;state.limit=12;render();
    $('#catalog').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  }));
  $('#search').addEventListener('input',e=>{state.query=e.target.value;state.limit=12;render()});
  $('#reuse').addEventListener('change',e=>{state.reuse=e.target.value;state.limit=12;render()});
  $('#entry-type').addEventListener('change',e=>{state.type=e.target.value;state.limit=12;render()});
  $('#reset').addEventListener('click',reset);$('#empty-reset').addEventListener('click',reset);
  $('#load-more').addEventListener('click',()=>{
    const previous=$('#cards').children.length;state.limit+=12;render();
    $('#cards').children[previous]?.querySelector('button')?.focus({preventScroll:true});
  });
  const dialog=$('#detail');
  function showDetail(key) {
    const s=byKey.get(key);if(!s)return;
    const group=categories.get(s.category);
    $('#detail-category').textContent=`${group.number} / ${group.name}${s.nested?' · 嵌套入口':''}${s.alias?' · 别名入口':''}`;
    $('#detail-content').innerHTML=`<div class="dialog-title-row"><h2 id="detail-title">${escape(s.title)}</h2><span class="badge ${s.reuse}">${data.reuseLabels[s.reuse]}</span></div><p class="skill-key">${escape(s.key)}</p><p class="summary">${escape(s.summary)}</p><dl class="detail-grid"><div><dt>给它什么</dt><dd>${escape(s.input)}</dd></div><div><dt>得到什么</dt><dd>${escape(s.output)}</dd></div><div><dt>需要准备</dt><dd>${escape(s.dependencies)}</dd></div><div><dt>实现线索</dt><dd>技能定义与参考资料${s.scripts.length?`；该目录下收录 ${s.scripts.length} 个脚本文件（包含嵌套目录）`:'；执行方式及外部工具以原文约定为准'}。</dd></div><div><dt>许可线索</dt><dd>${escape(s.license)}</dd></div></dl><div class="detail-actions"><a class="primary" href="${escape(s.source)}" target="_blank" rel="noopener noreferrer">查看原始技能 ↗</a><a href="./data/catalog.json" download="rnskill-capabilities.json">下载完整清单 ↓</a></div><p class="detail-evidence">${escape(s.evidence)} 复用条件为研究判断。</p><p class="detail-source">${escape(s.path)} · ${data.commit.slice(0,7)}</p>`;
    dialog.showModal();
  }
  document.addEventListener('click',e=>{const b=e.target.closest('[data-skill]');if(b)showDetail(b.dataset.skill)});
  $('#close-detail').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{
    const r=dialog.getBoundingClientRect();
    if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dialog.close();
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='/'&&!dialog.open&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)&&!document.activeElement.isContentEditable){e.preventDefault();$('#search').focus();}
  });
  const workflows=[
    {id:'article',name:'文章 → 图文',title:'把一篇长文变成可发布的图片组',input:'输入：已有 Markdown 文章与配图',note:'这是依据技能能力整理的组合路径。正文默认保持原文结构；可按需要先做表达精修。',steps:[
      ['整理表达','保留观点与事实，调整中文表达。',['ra-人话']],['选标题','按图文主题准备标题候选。',['dbs-xhs-title']],['拆页出图','选择皮肤，分配正文和配图。',['xhs-article-to-images']],['检查与交付','核对文字、图片、页码与卡片尺寸。',['xhs-article-to-images']]]},
    {id:'video',name:'脚本 → 视频',title:'从口播脚本到配音、字幕和成片',input:'输入：已确认脚本与制作要求',note:'制作导演负责贯穿各步的调度。需要先适配工作台；最终字幕须依据锁定音频生成，数字人路径另需试听确认。',steps:[
      ['制作交接','锁定比例、声音、视觉与交付位置。',['ra-video-production-director']],['生成配音','用已配置的无损声音参考生成旁白。',['tts-skill']],['对齐字幕','识别最终音频，再渲染字幕样式。',['ra-audio-to-subtitles','skill-captions']],['合成与质检','结合分镜和素材制作，检查并归档。',['rn-motion-director','ra-video-production-director']]]},
    {id:'cut',name:'口播 → 粗剪',title:'让录制素材进入可审核的剪辑流程',input:'输入：自己录制的口播或讲解视频',note:'默认粗剪与波形审核是不同工具路径。网页审核可选择 AI 剪口播；发布字幕应从最终合并后的媒体重新生成。',steps:[
      ['转写校对','识别语音，先检查术语与不确定内容。',['ra-local-talking-head-cut']],['审核删减','确认要删的口误、重复和停顿。',['ra-local-talking-head-cut']],['语义粗剪','按确认内容剪辑、处理停顿和响度。',['ra-local-talking-head-cut']],['最终字幕','后续定稿视频生成时间轴与字幕画面。',['ra-audio-to-subtitles','skill-captions']]]},
    {id:'review',name:'表现 → 经验',title:'把一次发布的结果留下来，下次继续用',input:'输入：作品、账号指标与历史记录',note:'复盘依赖真实数据、台账与配套脚本。将观察写成可检验的假设，单条作品表现不能证明普遍规律。',steps:[
      ['读取表现','定位作品，核对指标与历史基线。',['ra-复盘']],['分析内容','检查开头、结构与受众共鸣。',['dbs-hook','dbs-resonate']],['积累资产','保存案例、概念和可以再用的内容单元。',['dbs-content-system']],['回到选题','把本次观察用于下一轮选题。',['ra-选题']]]}
  ];
  $('#workflow-tabs').innerHTML=workflows.map((w,i)=>`<button id="tab-${w.id}" role="tab" aria-controls="workflow-panel" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-flow="${w.id}">${w.name}</button>`).join('');
  function selectFlow(id){
    const flow=workflows.find(w=>w.id===id);
    document.querySelectorAll('[data-flow]').forEach(b=>{const selected=b.dataset.flow===id;b.setAttribute('aria-selected',String(selected));b.tabIndex=selected?0:-1});
    $('#workflow-panel').setAttribute('aria-labelledby',`tab-${id}`);
    $('#workflow-panel').innerHTML=`<div class="flow-intro"><h3>${flow.title}</h3><p>${flow.input}</p></div><div class="flow-steps">${flow.steps.map((step,i)=>`<article class="flow-step"><b>0${i+1}</b><h4>${step[0]}</h4><p>${step[1]}</p>${step[2].map(key=>`<button data-skill="${key}">${key} ↗</button>`).join('')}</article>`).join('')}</div><p class="flow-note">${flow.note}</p>`;
  }
  $('#workflow-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-flow]');if(b)selectFlow(b.dataset.flow)});
  $('#workflow-tabs').addEventListener('keydown',e=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
    const buttons=[...document.querySelectorAll('[data-flow]')];let i=buttons.indexOf(document.activeElement);if(i<0)return;
    e.preventDefault();i=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(e.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;
    selectFlow(buttons[i].dataset.flow);buttons[i].focus();
  });
  selectFlow('article');render();
})();
