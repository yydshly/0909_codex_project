"""Maintain the research catalog with Python's standard library only."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/yydshly/0909_codex_project"
STATUSES = {"待研究", "研究中", "已整理", "已归档"}


def key(project):
    return f"{project['id']:03d}-{project['slug']}"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_valid(value):
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return (parsed.scheme == "https" and parsed.netloc == "github.com"
            and re.fullmatch(r"/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?", parsed.path)
            and not parsed.query and not parsed.fragment)


def slug_valid(value):
    return isinstance(value, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value)


def inside(base, relative):
    require(isinstance(relative, str) and relative and "\\" not in relative,
            "路径必须是使用 / 的非空相对路径")
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
            f"路径不能越界：{relative}")
    target = base / relative
    require(target.resolve().is_relative_to(base.resolve()), f"路径不能越界：{relative}")
    require(not any(p.is_symlink() for p in [target, *target.parents]),
            f"不支持符号链接：{relative}")
    return target


def load_catalog():
    data = json.loads((ROOT / "registry/projects.json").read_text(encoding="utf-8"))
    require(isinstance(data, dict) and isinstance(data.get("projects"), list), "清单必须包含 projects 数组")
    require(type(data.get("nextId")) is int and data["nextId"] > 0, "nextId 必须是正整数")
    seen_ids, seen_orders, seen_slugs = set(), set(), set()
    for p in data["projects"]:
        require(isinstance(p, dict), "项目条目必须是对象")
        for field, seen in [("id", seen_ids), ("order", seen_orders)]:
            value = p.get(field)
            require(type(value) is int and value > 0 and value not in seen,
                    f"{field} 必须是唯一的正整数")
            seen.add(value)
        require(slug_valid(p.get("slug")) and p["slug"] not in seen_slugs, "slug 格式错误或重复")
        seen_slugs.add(p["slug"])
        for field in ("name", "summary"):
            value = p.get(field)
            require(isinstance(value, str) and value.strip() and not any(c in value for c in "\r\n"),
                    f"{key(p)} 的 {field} 必须是非空单行文本")
        require(source_valid(p.get("source")), f"{key(p)} 的 source 必须是 GitHub 仓库 HTTPS 链接")
        require(isinstance(p.get("status"), str) and p["status"] in STATUSES, "研究状态不合法")
        require(isinstance(p.get("tags"), list) and all(isinstance(t, str) and t.strip()
                and not any(c in t for c in "\r\n") for t in p["tags"]), "tags 必须是单行文本数组")
        require(type(p.get("demo")) is bool, "demo 必须是布尔值")
        require("cover" in p, "请设置 cover 为图片相对路径或 null")
        directory = inside(ROOT / "projects", key(p))
        require((directory / "README.md").is_file(), f"缺少研究页：{key(p)}/README.md")
        if p["cover"] is not None:
            cover = inside(directory, p["cover"])
            require(cover.is_file() and cover.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"},
                    f"封面不存在或格式不支持：{p['cover']}")
        if p["demo"]:
            web = inside(directory, "web")
            require((web / "index.html").is_file(), f"已启用演示但缺少 {key(p)}/web/index.html")
            require(not any(f.is_symlink() for f in web.rglob("*")), "演示目录不能包含符号链接")
    require(data["nextId"] > max(seen_ids, default=0), "nextId 必须大于所有已用编号")
    data["projects"].sort(key=lambda p: p["order"])
    return data


def markdown(value):
    value = escape(value, quote=False)
    for char in "\\`*_{}[]()#+!|":
        value = value.replace(char, "\\" + char)
    return value


def readme_content(projects):
    original = (ROOT / "README.md").read_text(encoding="utf-8")
    if not projects:
        index = "暂无研究项目。第一个项目将从 **001** 开始编号。"
        cards = "收录项目后，这里会自动展示摘要和已添加的封面图片。"
    else:
        rows = ["| 顺序 | 编号 | 项目 | 一句话摘要 | 状态 | Web |", "| --- | --- | --- | --- | --- | --- |"]
        blocks = []
        for rank, p in enumerate(projects, 1):
            folder = f"projects/{key(p)}"
            demo = f"https://yydshly.github.io/0909_codex_project/{folder}/"
            demo_link = f"[演示]({demo})" if p["demo"] else "—"
            rows.append(f"| {rank} | {p['id']:03d} | [{markdown(p['name'])}]({folder}/README.md) | "
                        f"{markdown(p['summary'])} | {p['status']} | {demo_link} |")
            block = f"### {p['id']:03d} · {markdown(p['name'])}\n\n{markdown(p['summary'])}\n\n"
            if p["cover"]:
                block += f"![{markdown(p['name'])} 封面]({folder}/{quote(p['cover'])})\n\n"
            block += f"[研究记录]({folder}/README.md) · [上游仓库]({p['source']})"
            if p["demo"]:
                block += f" · [Web 演示]({demo})"
            blocks.append(block)
        index, cards = "\n".join(rows), "\n\n".join(blocks)
    for section, content in [("INDEX", index), ("CARDS", cards)]:
        start, end = f"<!-- PROJECT_{section}:START -->", f"<!-- PROJECT_{section}:END -->"
        require(original.count(start) == original.count(end) == 1, f"README 的 {section} 标记缺失或重复")
        pattern = re.escape(start) + r".*?" + re.escape(end)
        require(re.search(pattern, original, flags=re.S), f"README 的 {section} 标记顺序错误")
        original = re.sub(pattern, lambda _: f"{start}\n{content}\n{end}", original, flags=re.S)
    return original


def sync(projects):
    (ROOT / "README.md").write_text(readme_content(projects), encoding="utf-8")


def build(projects):
    output = ROOT / "_site"
    require(not output.is_symlink() and output.resolve() == ROOT.resolve() / "_site",
            "拒绝清理不在仓库根目录内的构建目录")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    shutil.copyfile(ROOT / "site/style.css", output / "style.css")
    cards = []
    for p in projects:
        folder = key(p)
        picture = ""
        if p["cover"]:
            source = ROOT / "projects" / folder / p["cover"]
            target = output / "covers" / (folder + source.suffix.lower())
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(source, target)
            picture = f'<img src="./covers/{target.name}" alt="{escape(p["name"])} 封面" loading="lazy">'
        links = f'<a href="{REPO}/blob/main/projects/{folder}/README.md">研究记录 ↗</a>'
        links += f'<a href="{escape(p["source"])}">上游仓库 ↗</a>'
        if p["demo"]:
            shutil.copytree(ROOT / "projects" / folder / "web", output / "projects" / folder,
                            ignore=shutil.ignore_patterns(".gitkeep"))
            links += f'<a href="./projects/{folder}/">Web 演示 →</a>'
        tags = "".join(f"<li>{escape(t)}</li>" for t in p["tags"])
        cards.append(f'<article class="card">{picture}<div class="card-body">'
                     f'<div class="meta"><span>NO. {p["id"]:03d}</span><span>{p["status"]}</span></div>'
                     f'<h3>{escape(p["name"])}</h3><p>{escape(p["summary"])}</p>'
                     f'<ul class="tags">{tags}</ul><nav class="links" aria-label="{escape(p["name"])} 项目入口">'
                     f'{links}</nav></div></article>')
    content = "\n".join(cards) or ('<div class="empty"><h3>从第一个好项目开始。</h3>'
                                 '<p>研究室已就绪。收录后，这里将按顺序展示项目摘要、图片与演示入口。</p></div>')
    template = (ROOT / "site/index.html").read_text(encoding="utf-8")
    page = template.replace("{{COUNT}}", str(len(projects))).replace("{{CARDS}}", content)
    (output / "index.html").write_text(page, encoding="utf-8")
    (output / ".nojekyll").touch()


def create_project(args):
    data = load_catalog()
    require(slug_valid(args.slug), "slug 仅支持小写英文、数字和连字符")
    require(not any(p["slug"] == args.slug for p in data["projects"]), "slug 已被使用")
    require(source_valid(args.url), "请提供 GitHub 仓库 HTTPS 链接")
    for value in (args.name, args.summary):
        require(value.strip() and not any(c in value for c in "\r\n"), "名称和摘要必须是非空单行文本")
    # Validate generated regions before creating any files.
    readme_content(data["projects"])
    p = dict(id=data["nextId"], slug=args.slug,
             order=max((x["order"] for x in data["projects"]), default=0) + 10,
             name=args.name, source=args.url, summary=args.summary,
             status="待研究", tags=[], cover=None, demo=False)
    target = ROOT / "projects" / key(p)
    require(not target.exists(), f"目录已存在：{target.name}")
    shutil.copytree(ROOT / "templates/project", target)
    template = (target / "README.md").read_text(encoding="utf-8")
    values = {"ID": f"{p['id']:03d}", "NAME": markdown(p["name"]), "URL": p["source"],
              "SUMMARY": markdown(p["summary"]), "DATE": date.today().isoformat()}
    template = re.sub(r"\{\{(ID|NAME|URL|SUMMARY|DATE)\}\}", lambda m: values[m[1]], template)
    (target / "README.md").write_text(template, encoding="utf-8")
    data["projects"].append(p)
    data["nextId"] += 1
    (ROOT / "registry/projects.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync(data["projects"])
    print(f"Created projects/{key(p)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("sync", "check", "build"):
        sub.add_parser(command)
    new = sub.add_parser("new")
    new.add_argument("slug")
    new.add_argument("--name", required=True)
    new.add_argument("--url", required=True)
    new.add_argument("--summary", required=True)
    args = parser.parse_args()
    try:
        if args.command == "new":
            create_project(args)
        else:
            projects = load_catalog()["projects"]
            if args.command == "sync":
                sync(projects)
            elif args.command == "check":
                require((ROOT / "README.md").read_text(encoding="utf-8") == readme_content(projects),
                        "README 索引未同步，请先执行 python scripts/catalog.py sync")
            else:
                build(projects)
            print(f"{args.command}: OK ({len(projects)} projects)")
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
