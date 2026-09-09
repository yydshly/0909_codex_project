"use strict";
(() => {
  const base = "https://github.com/SegFault42/HeliosGen/blob/fb011d6f3ad00510b4eface78e054c7eda329c54/";
  const steps = [
    {title:"准备提示词与商品参考图",description:"在画布中放置参考图、图片生成和视频生成节点，设置提示词与模型。把图片输出连接到视频首帧输入，保存的是创作方案。",owner:"用户界面 · 工作流状态",data:"节点、连线、模型参数与本地素材引用",source:"lib/store.ts",states:["已准备","未开始","未开始"],classes:["done","",""]},
    {title:"解析输入，安排生成先后",description:"执行器读取端口与连线，解析上游素材。图片节点属于第一批，依赖图片结果的视频节点排在后续批次；同批无相互依赖的生成节点可并行。",owner:"输入解析 · 依赖执行器",data:"提示词、参考图地址、按依赖划分的节点批次",source:"lib/executor.ts",states:["可读取","准备执行","排队等待"],classes:["done","active",""]},
    {title:"转换参数，发起图片生成",description:"本地 API 读取模型配置，把应用参数映射为模型接口字段。需要时先上传本地参考图，再提交生成请求，取得用于跟踪的任务 ID。",owner:"本地 API · 模型适配 · 素材上传",data:"模型请求参数、参考图访问 URL、图片任务 ID",source:"app/api/generate/route.ts",states:["按需上传","已提交","排队等待"],classes:["done","active",""]},
    {title:"后台查询图片任务并保存结果",description:"通用 Kie 路径约每 3 秒查询状态，最长约 12 分钟。成功后下载主图，更新历史与任务状态，并把结果返回前端节点；这条示意路径假设任务成功。",owner:"后台轮询 · 本地存储 · 界面状态",data:"远程结果 URL → 本地图片文件与节点结果",source:"lib/kieJobPoller.ts",states:["已使用","结果已保存","等待本批结束"],classes:["done","done",""]},
    {title:"把主图作为视频首帧继续生成",description:"当前批次结束后，执行器触发下一批。视频节点读取主图，按所选模型要求准备首帧与提示词；必要时把主图上传，再创建视频任务。",owner:"工作流执行器 · 视频 API",data:"主图引用、视频参数、视频任务 ID",source:"app/api/generate-video/route.ts",states:["已使用","供下游读取","已提交 / 等待结果"],classes:["done","done","active"]},
    {title:"保存视频，沉淀可复用流程",description:"视频生成成功后写入本地文件和生成历史，界面显示结果。工作流可继续编辑，也可连同引用的素材打包分享；下次运行会产生新的生成任务。",owner:"任务结果处理 · 素材库 · 工作流导出",data:"视频文件、生成记录、可复用工作流和素材包",source:"lib/exportWorkflow.ts",states:["可复用","可复用","结果已保存"],classes:["done","done","done"]}
  ];
  const buttons = [...document.querySelectorAll("[data-step]")];
  const tasks = [...document.querySelectorAll("[data-task]")];
  let current = 0;
  function render(index, announce = true) {
    current = Math.max(0, Math.min(steps.length - 1, index));
    const step = steps[current];
    document.getElementById("step-count").textContent = "0" + (current + 1) + " / 06";
    document.getElementById("step-title").textContent = step.title;
    document.getElementById("step-description").textContent = step.description;
    document.getElementById("step-owner").textContent = step.owner;
    document.getElementById("step-data").textContent = step.data;
    document.getElementById("step-source").href = base + step.source;
    buttons.forEach((button, i) => button.setAttribute("aria-pressed", String(i === current)));
    tasks.forEach((node, i) => {
      node.classList.remove("active", "done");
      if (step.classes[i]) node.classList.add(step.classes[i]);
      node.querySelector("span").textContent = step.states[i];
    });
    document.getElementById("previous-step").disabled = current === 0;
    document.getElementById("next-step").disabled = current === steps.length - 1;
    if (announce) document.getElementById("step-announcement").textContent = "第 " + (current + 1) + " 步，共 6 步：" + step.title + "。" + step.description;
  }
  buttons.forEach((button, i) => button.addEventListener("click", () => render(i)));
  document.getElementById("previous-step").addEventListener("click", () => render(current - 1));
  document.getElementById("next-step").addEventListener("click", () => render(current + 1));
  render(0, false);
  document.getElementById("walkthrough").hidden = false;
  document.getElementById("execution-fallback").hidden = true;

  const dialog = document.getElementById("diagram-dialog");
  const opener = document.getElementById("open-diagram");
  const viewport = dialog.querySelector(".diagram-scroll");
  const large = document.getElementById("large-diagram");
  let zoom = 1;
  function setZoom(value) {
    zoom = Math.min(2, Math.max(.2, value));
    large.style.width = Math.round(1440 * zoom) + "px";
    document.getElementById("zoom-value").textContent = Math.round(zoom * 100) + "%";
    document.getElementById("zoom-out").disabled = zoom <= .2;
    document.getElementById("zoom-in").disabled = zoom >= 2;
  }
  if (typeof dialog.showModal === "function") {
    opener.hidden = false;
    opener.addEventListener("click", () => {
      dialog.showModal();
      document.body.classList.add("modal-open");
      setZoom(1);
      viewport.scrollTop = viewport.scrollLeft = 0;
      document.getElementById("close-diagram").focus();
    });
    document.getElementById("close-diagram").addEventListener("click", () => dialog.close());
    dialog.addEventListener("close", () => {
      document.body.classList.remove("modal-open");
      opener.focus();
    });
    document.getElementById("zoom-out").addEventListener("click", () => setZoom(zoom - .2));
    document.getElementById("zoom-in").addEventListener("click", () => setZoom(zoom + .2));
    document.getElementById("fit-diagram").addEventListener("click", () => setZoom((viewport.clientWidth - 4) / 1440));
  }

  const navLinks = [...document.querySelectorAll(".contents a")];
  const sections = navLinks.map(a => document.querySelector(a.getAttribute("href")));
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.filter(e => e.isIntersecting).forEach(entry => {
        navLinks.forEach(link => {
          if (link.getAttribute("href") === "#" + entry.target.id) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-10% 0px -70% 0px", threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }
})();
