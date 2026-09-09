"""Build static gallery metadata and contact sheets from the actual PNG files.

Requires Pillow only. Does not generate or retouch any illustration.
Run from any directory: python projects/004-ian-handdrawn-ppt/experiments/build_gallery.py
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / 'web'
UPSTREAM = 'https://github.com/helloianneo/ian-handdrawn-ppt'
COMMIT = 'b2cc5f303337e5470fd6ac2870d261a43b218439'
ORIGINALS = [
    ('cover', '能自动化 ≠ 该自动化', '自动化的边界', '封面隐喻', '用天平和分岔路，把“能做”与“该做”的差异变成一眼可见的选择。', '天平位于自动化机械臂与阅读书桌之间，表达自动化的边界。', 'cover-automation-boundary.png', 'a0a09040921cf632f5aba0843cb242b2bb4a6edb'),
    ('page-01', '阅读其实是两件事', '阅读的两件事', '左右对比', '左边是信息漏斗，右边是书本与罗盘。通过两组物体，区分摄入信息与训练判断。', '信息漏斗与阅读书本左右对比：摄入信息要结果，训练判断重过程。', 'page-01-reading-two-things.png', '9cfa198ea67f618a9a879becf4dfdaa174f57c4f'),
    ('page-02', '自动化该放哪里', '自动化放哪里', '流程与分工', '观察淡色标签、细箭头与物件如何组织工作步骤，并突出自动化的适用位置。', '原作者关于自动化在工作流程中应该放在哪里的手绘解释图。', 'page-02-where-to-automate.png', 'ee593a2f0731c9d8be1f19b00baac695280cd189'),
    ('page-03', '三问判断法', '三问判断法', '判断框架', '把抽象判断压缩成三个问题，保持短文字、克制标题和统一的手绘视觉。', '原作者用三个问题帮助读者判断是否应该自动化的手绘解释图。', 'page-03-three-question-method.png', '80a60970483511f2bf2b488ba8659010f5cd5eef'),
]


def info(path):
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        width, height = image.size
    content = path.read_bytes()
    return width, height, hashlib.sha256(content).hexdigest(), hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def contact_sheet(pages, target, title):
    width, height = 1600, 1094
    canvas = Image.new('RGB', (width, height), '#f2f5ee')
    draw = ImageDraw.Draw(canvas)
    font_file = Path('C:/Windows/Fonts/msyh.ttc')
    font = ImageFont.truetype(str(font_file), 23) if font_file.exists() else ImageFont.load_default()
    small = ImageFont.truetype(str(font_file), 19) if font_file.exists() else ImageFont.load_default()
    draw.text((40, 24), title, font=font, fill='#324b35')
    for i, page in enumerate(pages):
        x, y = 30 + (i % 2) * 790, 82 + (i // 2) * 500
        draw.rounded_rectangle((x, y, x + 760, y + 475), radius=9, fill='#ffffff', outline='#dce5d5')
        with Image.open(WEB / page['src']) as source:
            image = ImageOps.contain(source.convert('RGB'), (732, 411), Image.Resampling.LANCZOS)
            canvas.paste(image, (x + 14 + (732 - image.width) // 2, y + 12 + (411 - image.height) // 2))
        draw.text((x + 18, y + 436), page['title'], font=small, fill='#42543b')
    canvas.save(target, optimize=True)


def main():
    blueprint = json.loads((WEB / 'data/blueprint.json').read_text(encoding='utf-8'))
    originals, generated, manifest = [], [], []
    for asset_id, title, short, archetype, description, alt, upstream_name, expected_blob in ORIGINALS:
        path = WEB / 'assets/original' / f'{asset_id}.png'
        w, h, digest, blob = info(path)
        if blob != expected_blob:
            raise ValueError(f'Original differs from pinned upstream: {path}')
        originals.append(dict(id=asset_id, title=title, shortTitle=short, archetype=archetype, description=description, alt=alt, ratio='约 21:9' if asset_id == 'cover' else '16:9', width=w, height=h, src=f'./assets/original/{asset_id}.png'))
        manifest.append(dict(file=str(path.relative_to(PROJECT)).replace('\\', '/'), origin='Ian 原作，原文件未改动', source=f'{UPSTREAM}/blob/{COMMIT}/examples/images/{upstream_name}', width=w, height=h, sha256=digest, gitBlob=blob, matchesUpstream=True))
    for p in blueprint['pages']:
        path = WEB / 'assets/scenario' / f"{p['id']}.png"
        w, h, digest, blob = info(path)
        ratio = 21/9 if p['role'] == 'cover' else 16/9
        if abs(w / h / ratio - 1) > .035:
            raise ValueError(f'Unexpected aspect ratio: {path} {w}x{h}')
        generated.append(dict(id=p['id'], title=p['title'], archetype=p['archetype'], description=p['point'], alt=p['title'] + '。' + p['point'], ratio='约 ' + p['ratio'], width=w, height=h, src=f"./assets/scenario/{p['id']}.png"))
        manifest.append(dict(file=str(path.relative_to(PROJECT)).replace('\\', '/'), origin='本次实作：内置图像工具生成', width=w, height=h, sha256=digest, requiredText=p['texts'], promptRecord=f"web/data/blueprint.json → pages[{len(generated)-1}]", postprocessing='无；保留生成器返回的原生 PNG', styleReference='upstream/assets/reference-handdrawn-article-illustration-style.png'))
    payload = dict(original=originals, scenario=generated, blueprint=blueprint)
    (WEB / 'data/gallery.js').write_text('window.EXHIBITION = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    (WEB / 'data/verification.json').write_text(json.dumps(dict(date='2026-09-09', upstream=UPSTREAM, upstreamCommit=COMMIT, generation='内置 image_gen，附原库参考图，逐页独立提示词；模型版本不作额外推断', scenarioSources=blueprint['sourceFiles'], files=manifest, automatedChecks=['8 个 PNG 文件均可解码', '原作 Git blob 哈希与上游固定版本一致', '新图实际宽高比与页面角色接近，误差小于 3.5%'], visualReview='见项目 notes/verification.md，人工目视检查与自动检查分开记录'), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    contact_sheet(originals, WEB / 'assets/original/contact-sheet.png', '原作者示例 · Ian Handdrawn PPT')
    contact_sheet(generated, WEB / 'assets/scenario/contact-sheet.png', '真实场景实作 · GitHub 项目研究室')
    print('Built gallery: 4 original images + 4 generated images + 2 contact sheets.')
    for page in originals + generated:
        print(f"{page['src']} {page['width']}x{page['height']}")


if __name__ == '__main__':
    main()
