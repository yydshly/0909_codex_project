"""Refresh downloadable copies and the existing research catalog entry."""
import json
from pathlib import Path

project = Path(__file__).resolve().parents[1]
root = project.parents[1]
downloads = project / "web" / "downloads"
downloads.mkdir(parents=True, exist_ok=True)
note = (project / "README.md").read_text(encoding="utf-8")
note = note.replace("(web/assets/architecture.svg)", "(../assets/architecture.svg)")
note = note.replace("(web/index.html)", "(../index.html)")
note = note.replace("(notes/verification.md)", "(https://github.com/yydshly/0909_codex_project/blob/main/projects/013-firecrawl/notes/verification.md)")
(downloads / "understanding.md").write_text(note, encoding="utf-8")
(downloads / "firecrawl_example.py").write_bytes((project / "experiments" / "firecrawl_example.py").read_bytes())
catalog_path = root / "registry" / "projects.json"
catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
entry = next(p for p in catalog["projects"] if p["slug"] == "firecrawl")
entry.update(summary="Firecrawl 是网页数据获取服务，以 API/SDK 接收网址、搜索词与任务，通过 HTTP 请求、浏览器渲染、队列调度和内容转换输出 Markdown/JSON；支持搜索、抓取、爬站及云端交互，可用于新闻补全文与知识库，扩展持续更新、行业字段与质量校验，并明确登录和平台封号边界。", status="已整理", tags=["网页获取", "浏览器与 API", "登录与平台限制", "能力与扩展"], cover="web/assets/architecture.svg", demo=True)
catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Refreshed downloadable artifacts and Firecrawl catalog entry.")
