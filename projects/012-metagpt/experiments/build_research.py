"""Render the checked-in research document using the installed markdown-it-py."""
from pathlib import Path
from markdown_it import MarkdownIt

WEB = Path(__file__).resolve().parents[1] / "web"
body = MarkdownIt("commonmark", {"html": False}).enable("table").render(
    (WEB / "research.md").read_text(encoding="utf-8")
)
page = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MetaGPT · 完整理解与运行依据</title><link rel="stylesheet" href="style.css">
<style>.research{max-width:980px;padding-top:44px;padding-bottom:70px}.research h1{font-size:36px;letter-spacing:-1px}.research h2{font-size:25px;border-top:1px solid var(--line);padding-top:30px;margin-top:38px}.research h3{margin-top:24px}.research p,.research ul,.research ol{margin:16px 0}.research p{color:var(--ink)}.research a{color:var(--green);text-decoration:underline;text-underline-offset:3px}.research pre{padding:20px;background:var(--green-soft);border-radius:8px}.research table{display:block;overflow-x:auto;border-collapse:collapse;margin:20px 0;width:100%;font-size:14px}.research th,.research td{text-align:left;vertical-align:top;padding:12px;border:1px solid var(--line);min-width:130px}.research th{background:var(--green-soft)}.research code{overflow-wrap:anywhere}.research img{max-width:100%}</style></head>
<body><header class="topbar"><a class="brand" href="index.html">MetaGPT <span>/ 012</span></a><a class="button" href="index.html">返回协作演示</a></header><main class="research">'''+body+'''</main></body></html>'''
(WEB / "research.html").write_text(page, encoding="utf-8")
print("Rendered web/research.html")
