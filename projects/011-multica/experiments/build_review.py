"""Build local review pages from the Markdown source documents."""
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
docs = [('review', ROOT/'notes/review.md'), ('research', ROOT/'notes/understanding.md'),
        ('verification', ROOT/'notes/verification.md'), ('setup', ROOT/'README.md')]
links = {
    '../web/assets/': 'assets/', 'web/assets/': 'assets/',
    'notes/review.md': 'review.md', 'notes/understanding.md': 'research.md',
    'notes/verification.md': 'verification.md', 'understanding.md': 'research.md',
    '../README.md': 'setup.md', '../../README.md': 'https://yydshly.github.io/0909_codex_project/',
}
for name, source in docs:
    content = source.read_text(encoding='utf-8')
    # Apply longer paths first so the parent README rewrite stays precise.
    for before, after in sorted(links.items(), key=lambda pair: -len(pair[0])):
        content = content.replace(']('+before, ']('+after)
    (WEB/f'{name}.md').write_text(content, encoding='utf-8')
    rendered = content
    for slug, _ in docs:
        rendered = rendered.replace(f']({slug}.md', f']({slug}.html')
    rendered = rendered.replace('](assets/architecture.svg)', '](diagram.html)')
    rendered = rendered.replace('research.html#7-源码阅读入口', 'research.html#7')
    parser = markdown.Markdown(extensions=['tables','fenced_code','toc'], extension_configs={'toc': {'toc_depth': 2}})
    body = parser.convert(rendered)
    title = content.splitlines()[0].removeprefix('# ')
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="review.css"></head><body>
<header><a href="index.html">← Multica 研究页</a><span>研究记录 · 2026-09-09</span><a href="diagram.html">整体架构图 ↗</a></header>
<main><aside><strong>阅读导航</strong>{parser.toc}<p><a href="{name}.md" download>下载 Markdown</a></p></aside><article>{body}</article></main></body></html>'''
    (WEB/f'{name}.html').write_text(page, encoding='utf-8')
print('Built review, research, verification and setup pages.')
