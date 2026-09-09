(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  let report = null, agents = [], group = 'default', step = 0, timer = null, local = false;
  const setText = (id, value) => { $(id).textContent = value; };
  function stop() { if (timer) clearInterval(timer); timer = null; setText('play', '播放回放 ▷'); }
  function renderReport(data) {
    if (!data || !Array.isArray(data.events) || !Array.isArray(data.artifacts)) throw new Error('运行记录格式无效。');
    report = data; stop(); step = 0;
    setText('hero-status', data.success ? '已验证 · 真实框架运行 / 0 次模型调用' : '运行尚未通过验证');
    $('run-meta').replaceChildren(...[
      `${data.role_count} 个角色`, `${data.events.length} 条事件`,
      `${data.test_rounds.length} 轮测试`, `${data.test_rounds.at(-1).tests} 项测试通过`,
      '无模型调用', `运行 ${data.run_id}`
    ].map(text => { const span = document.createElement('span'); span.textContent = text; return span; }));
    $('timeline').replaceChildren(...data.events.map((event, i) => {
      const button = document.createElement('button');
      button.type = 'button'; button.dataset.step = i;
      if (event.cause_by === 'TestsFailed') button.classList.add('failure');
      const number = document.createElement('span'); number.className = 'number'; number.textContent = String(i + 1).padStart(2, '0');
      const block = document.createElement('span'), title = document.createElement('span'), actor = document.createElement('span');
      title.className = 'event-name'; title.textContent = event.title;
      actor.className = 'event-owner'; actor.textContent = event.actor;
      block.append(title, actor); button.append(number, block);
      button.addEventListener('click', () => { stop(); showStep(i); });
      return button;
    }));
    $('artifact-select').replaceChildren(...data.artifacts.map(a => {
      const option = document.createElement('option'); option.value = a.name; option.textContent = a.name; return option;
    }));
    $('download-artifact').disabled = false;
    selectArtifact('calculator.py'); showStep(0);
    $('play').disabled = false;
    setText('run-notice', `记录时间：${new Date(data.completed_at).toLocaleString('zh-CN')}。步骤按钮播放已完成的记录；“重新运行协作”会重新执行框架。`);
  }
  function showStep(index) {
    if (!report) return;
    step = Math.max(0, Math.min(index, report.events.length - 1));
    const event = report.events[step];
    document.querySelectorAll('[data-step]').forEach(button => {
      const active = Number(button.dataset.step) === step;
      button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
    });
    document.querySelectorAll('[data-actor]').forEach(node => node.classList.toggle('active', node.dataset.actor === event.actor));
    setText('event-actor', event.actor); setText('event-index', `${String(step + 1).padStart(2, '0')} / ${report.events.length}`);
    setText('event-title', event.title); setText('event-text', event.text); setText('event-type', event.cause_by);
    const tests = $('test-result'); tests.replaceChildren(); tests.hidden = !event.test_result;
    if (event.test_result) {
      const result = event.test_result, summary = document.createElement('div'), score = document.createElement('strong'), label = document.createElement('span');
      summary.className = `test-summary${result.success ? '' : ' failed'}`;
      score.textContent = `${result.tests-result.failures-result.errors} / ${result.tests}`;
      label.textContent = result.success ? '全部通过 · 实际 Python 测试' : `${result.failures} 项失败 · 进入返修`;
      summary.append(score, label); tests.append(summary);
      const details = document.createElement('details'), title = document.createElement('summary'), pre = document.createElement('pre');
      title.textContent = '查看真实测试输出'; pre.className = 'test-log'; pre.textContent = result.output;
      details.append(title, pre); tests.append(details);
    }
    $('event-artifacts').replaceChildren(...(event.artifacts || []).map(name => {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = name;
      button.addEventListener('click', () => { selectArtifact(name); $('artifact-select').scrollIntoView({behavior:'smooth',block:'center'}); });
      return button;
    }));
    $('previous').disabled = step === 0; $('next').disabled = step === report.events.length - 1;
  }
  function selectArtifact(name) {
    if (!report) return;
    const artifact = report.artifacts.find(a => a.name === name) || report.artifacts[0];
    if (!artifact) return;
    $('artifact-select').value = artifact.name; setText('artifact-content', artifact.content);
  }
  function renderAgents() {
    const list = agents.filter(a => a.group === group);
    $('agent-list').replaceChildren(...list.map(agent => {
      const button = document.createElement('button'); button.type = 'button'; button.dataset.agent = agent.class;
      const title = document.createElement('strong'), code = document.createElement('code');
      title.textContent = agent.label; code.textContent = agent.class; button.append(title, code);
      button.addEventListener('click', () => showAgent(agent)); return button;
    }));
    if (list.length) showAgent(list[0]);
  }
  function showAgent(agent) {
    document.querySelectorAll('[data-agent]').forEach(button => {
      const active = button.dataset.agent === agent.class; button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active));
    });
    setText('agent-category', agent.category); setText('agent-name', agent.label); setText('agent-class', agent.class);
    setText('agent-description', agent.description); setText('agent-base', agent.base);
    setText('agent-tools', agent.tools.length ? agent.tools.join(' · ') : '此角色主要绑定 Action 或采用专用执行流程，详见源码。');
    $('agent-source').href = agent.source;
  }
  $('previous').addEventListener('click', () => { stop(); showStep(step - 1); });
  $('next').addEventListener('click', () => { stop(); showStep(step + 1); });
  $('play').addEventListener('click', () => {
    if (timer) return stop();
    if (step === report.events.length - 1) showStep(0);
    setText('play', '暂停回放 Ⅱ');
    timer = setInterval(() => { if (step >= report.events.length - 1) return stop(); showStep(step + 1); }, 2200);
  });
  $('artifact-select').addEventListener('change', event => selectArtifact(event.target.value));
  $('download-artifact').addEventListener('click', () => {
    const artifact = report.artifacts.find(a => a.name === $('artifact-select').value);
    const url = URL.createObjectURL(new Blob([artifact.content], {type:'text/plain;charset=utf-8'}));
    const link = document.createElement('a'); link.href = url; link.download = artifact.name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  document.querySelectorAll('[data-group]').forEach(button => button.addEventListener('click', () => {
    group = button.dataset.group;
    document.querySelectorAll('[data-group]').forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button)); });
    renderAgents();
  }));
  $('run-button').addEventListener('click', async () => {
    if (!local) return;
    stop(); $('run-button').disabled = true; setText('run-button', '协作运行中…');
    setText('run-notice', '正在启动本机 MetaGPT：需求、设计、开发、测试与返修。下方保留上一轮记录，完成后更新。');
    try {
      const response = await fetch('/api/run', {method:'POST',headers:{'Content-Type':'application/json','X-MetaGPT-Demo':'local'},body:'{}'});
      const data = await response.json(); if (!response.ok) throw new Error(data.error);
      renderReport(data); showStep(data.events.length - 1);
      setText('run-notice', `新一轮实际运行已完成：${data.run_id}。8 项测试通过，模型调用为零。`);
    } catch (error) { setText('run-notice', `运行未完成：${error.message}。下方记录未更新。`); }
    finally { $('run-button').disabled = !local; setText('run-button', '重新运行协作 ↻'); }
  });
  $('calculator').addEventListener('submit', async event => {
    event.preventDefault(); if (!local) return;
    $('calculate-button').disabled = true; $('calculation').classList.remove('error'); setText('calculation', '运行 Python 产物…');
    try {
      const response = await fetch('/api/calculate', {method:'POST',headers:{'Content-Type':'application/json','X-MetaGPT-Demo':'local'},body:JSON.stringify(Object.fromEntries(new FormData(event.target)))});
      const data = await response.json(); if (!response.ok) throw new Error(data.error);
      setText('calculation', `应付金额 ¥ ${data.payable}`); setText('calculation-source', `实际执行 calculator.py · ${data.run_id}`);
    } catch (error) { $('calculation').classList.add('error'); setText('calculation', error.message); setText('calculation-source', ''); }
    finally { $('calculate-button').disabled = !local; }
  });
  async function init() {
    await Promise.allSettled([
      fetch('assets/run.json', {cache:'no-store'}).then(r => {if(!r.ok) throw new Error('尚无运行记录'); return r.json();}).then(renderReport).catch(error => {setText('hero-status','尚无已验证运行记录');setText('run-notice',error.message);}),
      fetch('assets/agents.json').then(r => r.json()).then(data => {agents = data.agents; renderAgents();}),
      (async () => {
        if (!['127.0.0.1','localhost'].includes(location.hostname)) { setText('connection','静态回放 · 本机运行按钮不可用'); return; }
        try { const r = await fetch('/api/health', {signal:AbortSignal.timeout(3000)}); const data = await r.json(); local = data.service === 'metagpt-lab'; }
        catch { local = false; }
        setText('connection', local ? '● 本机运行服务已连接' : '静态回放 · 未连接本机服务');
        $('connection').classList.toggle('connected',local); $('run-button').disabled = !local; $('calculate-button').disabled = !local;
        if (local) setText('calculation','等待输入 · 100 − 20，再 × 0.9');
      })()
    ]);
  }
  init();
})();
