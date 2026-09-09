(() => {
  'use strict';
  const data=window.RNSKILL_CATALOG;
  const skills=new Map(data.skills.map(s=>[s.key,s]));
  const groups=new Map(data.categories.map(g=>[g.id,g]));
  const $=s=>document.querySelector(s);
  const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let scale=100;
  const svg=$('#map-viewport>svg'),dialog=$('#skill-detail');
  function zoom(value){scale=Math.max(100,Math.min(200,value));svg.style.width=scale+'%';$('#zoom-level').textContent=scale+'%';$('#zoom-out').disabled=scale===100;$('#zoom-in').disabled=scale===200;}
  $('#zoom-in').addEventListener('click',()=>zoom(scale+25));
  $('#zoom-out').addEventListener('click',()=>zoom(scale-25));
  $('#zoom-reset').addEventListener('click',()=>{zoom(100);$('#map-viewport').scrollLeft=0});
  function show(key){const s=skills.get(key);if(!s)return;
    $('#skill-group').textContent=groups.get(s.category).name+' / '+data.reuseLabels[s.reuse]+(s.nested?' / 嵌套入口':'')+(s.alias?' / 别名入口':'');
    $('#skill-body').innerHTML=`<h2 id="skill-title">${esc(s.title)}</h2><p class="skill-key">${esc(s.key)}</p><p class="skill-summary">${esc(s.summary)}</p><dl><div><dt>何时使用</dt><dd>当你需要${esc(s.title.replace(' · 别名',''))}，且已准备好下面的输入材料时。</dd></div><div><dt>输入材料</dt><dd>${esc(s.input)}</dd></div><div><dt>得到什么</dt><dd>${esc(s.output)}</dd></div><div><dt>准备条件</dt><dd>${esc(s.dependencies)}</dd></div><div><dt>许可线索</dt><dd>${esc(s.license)}</dd></div></dl><a class="source-link" href="${esc(s.source)}" target="_blank" rel="noopener noreferrer">查看原始技能定义 ↗</a><p class="evidence">来源：${esc(s.path)}<br>固定版本 ${data.commit.slice(0,7)} · 静态核对，未实测运行。</p>`;
    dialog.showModal();
  }
  svg.addEventListener('click',e=>{const link=e.target.closest('[data-skill]');if(link){e.preventDefault();show(link.dataset.skill)}});
  $('#close-skill').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dialog.close()});
  zoom(100);
})();
