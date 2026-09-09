/* Static exhibition: all outputs are saved assets, no simulated generation. */
(() => {
  'use strict';
  const data = window.EXHIBITION;
  if (!data) return;
  const dialog = document.getElementById('lightbox');
  let activeGallery = null;
  let restoreFocus = null;
  const el = (tag, className, text) => { const node = document.createElement(tag); if (className) node.className = className; if (text !== undefined) node.textContent = text; return node; };

  function makeGallery(id, pages, origin) {
    const container = document.getElementById(id);
    const state = { index: 0, pages, origin, container };
    const stage = el('div', 'gallery-stage');
    const imageStage = el('div', 'image-stage');
    const open = el('button', 'image-open');
    const img = el('img'); img.decoding = 'async';
    open.append(img); imageStage.append(open, el('span', 'zoom-hint', '点击放大 ↗'));
    const caption = el('div', 'image-caption'); caption.setAttribute('aria-live', 'polite');
    const captionTop = el('div', 'caption-top');
    const type = el('span', 'slide-type'); const count = el('span', 'slide-counter'); captionTop.append(type, count);
    const title = el('h3'); const desc = el('p', 'caption-desc');
    const detail = el('dl');
    const actions = el('div', 'caption-actions');
    const download = el('a', 'download', '下载 PNG ↓');
    const arrows = el('div', 'slide-arrows');
    const prev = el('button', '', '←'); prev.setAttribute('aria-label', origin + '上一张');
    const next = el('button', '', '→'); next.setAttribute('aria-label', origin + '下一张');
    arrows.append(prev, next); actions.append(download, arrows); caption.append(captionTop, title, desc, detail, actions); stage.append(imageStage, caption);
    const thumbs = el('div', 'thumbnails'); thumbs.setAttribute('aria-label', origin + '页面选择');
    const thumbButtons = pages.map((page, i) => {
      const button = el('button', 'thumb'); button.setAttribute('aria-label', '查看' + page.title); button.setAttribute('aria-pressed', 'false');
      const thumb = el('img'); thumb.src = page.src; thumb.alt = ''; thumb.loading = 'lazy'; thumb.decoding = 'async';
      const label = el('span'); label.append(el('small', '', i === 0 ? 'COVER / 封面' : `0${i} / 正文`), document.createTextNode(page.shortTitle || page.title));
      button.append(thumb, label); button.addEventListener('click', () => update(i)); thumbs.append(button); return button;
    });
    container.append(stage, thumbs);
    function update(index) {
      state.index = (index + pages.length) % pages.length;
      const p = pages[state.index];
      img.src = p.src; img.alt = p.alt; img.width = p.width; img.height = p.height;
      open.setAttribute('aria-label', '放大：' + p.title);
      type.textContent = p.archetype; count.textContent = `${String(state.index + 1).padStart(2, '0')} / ${String(pages.length).padStart(2, '0')}`;
      title.textContent = p.title; desc.textContent = p.description;
      detail.replaceChildren(el('dt', '', '画幅'), el('dd', '', p.ratio), el('dt', '', '尺寸'), el('dd', '', `${p.width} × ${p.height}`));
      download.href = p.src; download.download = p.src.split('/').pop();
      thumbButtons.forEach((b, i) => b.setAttribute('aria-pressed', String(i === state.index)));
      if (dialog.open && activeGallery === state) renderLightbox();
    }
    state.update = update;
    prev.addEventListener('click', () => update(state.index - 1)); next.addEventListener('click', () => update(state.index + 1));
    open.addEventListener('click', () => { activeGallery = state; restoreFocus = open; renderLightbox(); dialog.showModal(); document.getElementById('lightbox-close').focus(); });
    container.addEventListener('keydown', event => { if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); update(state.index + (event.key === 'ArrowRight' ? 1 : -1)); } });
    update(0); return state;
  }

  function renderLightbox() {
    const page = activeGallery.pages[activeGallery.index];
    const image = document.getElementById('lightbox-image'); image.src = page.src; image.alt = page.alt;
    document.getElementById('lightbox-title').textContent = `${activeGallery.origin} · ${page.title}`;
    document.getElementById('lightbox-count').textContent = `${activeGallery.index + 1} / ${activeGallery.pages.length}`;
  }
  makeGallery('original-gallery', data.original, '原作者示例');
  makeGallery('scenario-gallery', data.scenario, '本次实作');
  document.getElementById('lightbox-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => restoreFocus?.focus());
  dialog.addEventListener('click', e => { if (e.target === dialog) { const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); } });
  document.getElementById('lightbox-prev').addEventListener('click', () => activeGallery.update(activeGallery.index - 1));
  document.getElementById('lightbox-next').addEventListener('click', () => activeGallery.update(activeGallery.index + 1));
  dialog.addEventListener('keydown', e => { if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); activeGallery.update(activeGallery.index + (e.key === 'ArrowRight' ? 1 : -1)); } });

  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function selectTab(tab) { tabs.forEach(t => { const selected = t === tab; t.setAttribute('aria-selected', String(selected)); t.tabIndex = selected ? 0 : -1; document.getElementById(t.dataset.panel).hidden = !selected; }); }
  tabs.forEach((tab, i) => { tab.addEventListener('click', () => selectTab(tab)); tab.addEventListener('keydown', e => { let next; if (e.key === 'ArrowRight') next = (i + 1) % tabs.length; if (e.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length; if (e.key === 'Home') next = 0; if (e.key === 'End') next = tabs.length - 1; if (next !== undefined) { e.preventDefault(); selectTab(tabs[next]); tabs[next].focus(); } }); });
  const list = document.getElementById('blueprint-list');
  const select = document.getElementById('prompt-page');
  data.blueprint.pages.forEach((p, i) => {
    const row = el('div', 'blueprint-row'); row.append(el('span', '', String(i).padStart(2, '0')), el('strong', '', p.title), el('em', '', p.archetype), el('p', '', p.point)); list.append(row);
    const option = el('option', '', (i === 0 ? '封面' : `第 ${i} 页`) + ' · ' + p.title); option.value = i; select.append(option);
  });
  const promptText = document.getElementById('prompt-text');
  const showPrompt = () => { promptText.textContent = data.blueprint.pages[Number(select.value)].prompt; document.getElementById('copy-status').textContent = ''; };
  select.addEventListener('change', showPrompt); showPrompt();
  document.getElementById('copy-prompt').addEventListener('click', async () => {
    const status = document.getElementById('copy-status');
    try { await navigator.clipboard.writeText(promptText.textContent); status.textContent = '已复制当前页面的完整提示词。'; }
    catch { const range = document.createRange(); range.selectNodeContents(promptText); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); status.textContent = '浏览器未允许自动复制，已选中文本，请按 Ctrl+C（Mac 使用 ⌘C）。'; }
  });
})();
