'use strict';
const journeys = {
  search: {label:'搜索 / 内容请求', title:'搜索“做饭教程”', intro:'用户提交关键词，Invidious 从 YouTube 获取搜索结果，再转换成自己的页面或 JSON。',
    steps:[['提交关键词','浏览器访问搜索页，或 App 调用搜索 API。'],['请求 YouTube','主服务整理地区与过滤条件，请求内部搜索接口。'],['解析响应','提取标题、封面、作者和视频 ID 等字段。'],['返回结果','网页生成结果列表，API 返回结构化 JSON。']],
    takeaway:'全站搜索依赖 YouTube；在自己的订阅中搜索，可以查询实例数据库里的标题和作者。'},
  play: {label:'播放 / 信息与媒体分开', title:'点开一段视频', intro:'先取得可用的播放信息，再请求实际音视频数据。两段链路都成功，播放器才能正常工作。',
    steps:[['读取信息缓存','主服务读取视频信息，过期或缺失时重新获取。'],['调用 Companion','处理播放会话并获取响应；主服务整理播放格式与详情。'],['生成播放器','把可用格式、字幕和播放地址交给页面播放器。'],['请求媒体数据','浏览器直连或经代理取流；地址过期或上游拒绝会导致失败。']],
    takeaway:'能看到标题和封面，不代表视频能播。元数据缓存也不等于保存了整个视频文件。'},
  subscribe: {label:'订阅 / 实例自己的数据', title:'关注一个频道', intro:'Invidious 保存你的频道订阅关系，再由后台任务更新频道内容并整理个人订阅列表。',
    steps:[['保存订阅关系','登录实例账号，订阅的频道 ID 写入自己的数据库。'],['刷新频道内容','后台任务定期获取频道视频，失败时包含退避处理。'],['整理个人更新','维护订阅物化视图，相当于预先保存整理好的查询结果。'],['展示订阅列表','从实例数据库读取自己的更新流，也可通过相应接口使用。']],
    takeaway:'这里修改的是 Invidious 账号，不会自动修改 Google 账号。后台刷新仍消耗网络与数据库资源。'}
};
for (const button of document.querySelectorAll('[data-journey]')) {
  button.addEventListener('click', () => {
    const data = journeys[button.dataset.journey];
    for (const item of document.querySelectorAll('[data-journey]')) item.setAttribute('aria-pressed', String(item === button));
    document.getElementById('journey-label').textContent = data.label;
    document.getElementById('journey-title').textContent = data.title;
    document.getElementById('journey-intro').textContent = data.intro;
    const steps = data.steps.map(([title, description], index) => {
      const li = document.createElement('li');
      const number = document.createElement('span'); number.textContent = String(index + 1).padStart(2, '0');
      const heading = document.createElement('h4'); heading.textContent = title;
      const p = document.createElement('p'); p.textContent = description;
      li.append(number, heading, p); return li;
    });
    document.getElementById('journey-steps').replaceChildren(...steps);
    const label = document.createElement('strong'); label.textContent = '关键理解：';
    document.getElementById('journey-takeaway').replaceChildren(label, document.createTextNode(data.takeaway));
  });
}
const dialog = document.getElementById('map-dialog');
document.getElementById('zoom-map').addEventListener('click', () => dialog.showModal());
document.getElementById('close-map').addEventListener('click', () => dialog.close());
