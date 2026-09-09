"""Validate publishable local references without controlling a browser."""
import ast
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

project = Path(__file__).resolve().parents[1]
web = project / "web"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.buttons = {"task": [], "route": []}

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "Duplicate HTML id"
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.refs.append(attrs[key])
        if tag == "button":
            assert attrs.get("type") == "button"
            for kind in self.buttons:
                if "data-" + kind in attrs:
                    self.buttons[kind].append(attrs["data-" + kind])

page = Page()
page.feed((web / "index.html").read_text(encoding="utf-8"))
for ref in page.refs:
    parsed = urlparse(ref)
    if parsed.scheme or parsed.netloc:
        continue
    if parsed.path:
        target = (web / unquote(parsed.path)).resolve()
        assert target.is_relative_to(web.resolve()) and target.is_file(), f"Broken local reference: {ref}"
    elif parsed.fragment:
        assert parsed.fragment in page.ids, f"Broken section link: {ref}"
assert len(page.buttons["task"]) == 8 and len(set(page.buttons["task"])) == 8
assert len(page.buttons["route"]) == 7 and len(set(page.buttons["route"])) == 7
ElementTree.parse(web / "assets" / "architecture.svg")
for file in [project / "experiments" / "firecrawl_example.py", web / "downloads" / "firecrawl_example.py"]:
    ast.parse(file.read_text(encoding="utf-8"))
assert (web / "downloads" / "firecrawl_example.py").read_bytes() == (project / "experiments" / "firecrawl_example.py").read_bytes()
print(f"Local references, anchors, SVG and Python examples: OK ({len(page.refs)} references)")
