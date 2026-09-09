import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("catalog", SOURCE / "scripts/catalog.py")
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.previous_root = catalog.ROOT
        catalog.ROOT = self.root
        for folder in ("templates", "site"):
            shutil.copytree(SOURCE / folder, self.root / folder)
        (self.root / "registry").mkdir()
        shutil.copyfile(SOURCE / "README.md", self.root / "README.md")
        self.save({"nextId": 1, "projects": []})
        catalog.sync([])

    def tearDown(self):
        catalog.ROOT = self.previous_root
        self.temp.cleanup()

    def save(self, data):
        (self.root / "registry/projects.json").write_text(json.dumps(data), encoding="utf-8")

    def create(self, slug="example"):
        catalog.create_project(argparse.Namespace(slug=slug, name=f"研究 {slug}",
                               url=f"https://github.com/owner/{slug}", summary="功能 | <script>alert(1)</script>"))

    def test_empty_catalog_builds_honest_empty_state(self):
        catalog.build(catalog.load_catalog()["projects"])
        page = (self.root / "_site/index.html").read_text(encoding="utf-8")
        self.assertIn("0 个项目", page)
        self.assertNotIn("{{CARDS}}", page)
        self.assertFalse((self.root / "_site/projects").exists())

    def test_order_can_change_without_changing_ids_or_paths(self):
        self.create("first")
        self.create("second")
        data = catalog.load_catalog()
        data["projects"][1]["order"] = 5
        self.save(data)
        projects = catalog.load_catalog()["projects"]
        self.assertEqual([p["id"] for p in projects], [2, 1])
        catalog.sync(projects)
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertLess(readme.index("002-second"), readme.index("001-first"))
        self.assertTrue((self.root / "projects/001-first/README.md").is_file())
        catalog.build(projects)
        page = (self.root / "_site/index.html").read_text(encoding="utf-8")
        self.assertLess(page.index("NO. 002"), page.index("NO. 001"))
        self.assertNotIn("<script>", page)

    def test_duplicate_order_and_missing_demo_are_rejected(self):
        self.create("first")
        self.create("second")
        data = catalog.load_catalog()
        data["projects"][1]["order"] = 10
        self.save(data)
        with self.assertRaisesRegex(ValueError, "order"):
            catalog.load_catalog()
        data["projects"][1]["order"] = 20
        data["projects"][0]["demo"] = True
        self.save(data)
        with self.assertRaisesRegex(ValueError, "index.html"):
            catalog.load_catalog()

    def test_cover_and_demo_publish_to_distinct_paths(self):
        self.create("first")
        self.create("second")
        data = catalog.load_catalog()
        for p in data["projects"]:
            directory = self.root / "projects" / catalog.key(p)
            (directory / "web/index.html").write_text(p["slug"], encoding="utf-8")
            (directory / "assets/cover.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
            p.update(demo=True, cover="assets/cover.svg")
        self.save(data)
        catalog.build(catalog.load_catalog()["projects"])
        for p in data["projects"]:
            self.assertEqual((self.root / "_site/projects" / catalog.key(p) / "index.html").read_text(), p["slug"])
            self.assertTrue((self.root / "_site/covers" / (catalog.key(p) + ".svg")).is_file())
        data["projects"][0]["demo"] = False
        self.save(data)
        catalog.build(catalog.load_catalog()["projects"])
        self.assertFalse((self.root / "_site/projects/001-first").exists())

    def test_path_traversal_and_reused_ids_are_rejected(self):
        self.create()
        data = catalog.load_catalog()
        data["projects"][0]["cover"] = "../../README.md"
        self.save(data)
        with self.assertRaisesRegex(ValueError, "越界"):
            catalog.load_catalog()
        data["projects"][0]["cover"] = None
        data["nextId"] = 1
        self.save(data)
        with self.assertRaisesRegex(ValueError, "nextId"):
            catalog.load_catalog()


if __name__ == "__main__":
    unittest.main()
