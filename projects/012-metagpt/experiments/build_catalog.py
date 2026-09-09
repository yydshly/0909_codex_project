"""Read class definitions with AST; importing/starting agents is unnecessary."""
import ast
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "upstream"
COMMIT = subprocess.check_output(["git", "-C", str(UP), "rev-parse", "HEAD"], text=True).strip()
INFO = {
    "TeamLeader": ("团队负责人", "协调", "规划任务、选择成员、交接上下文并根据反馈推进计划。"),
    "ProductManager": ("产品经理", "软件开发", "需求分析、产品需求文档以及市场和竞品研究。"),
    "Architect": ("架构师", "软件开发", "设计系统结构、接口和技术方案。"),
    "Engineer2": ("新版工程师", "软件开发", "动态使用编辑器、终端、浏览器、审查和部署工具。"),
    "DataAnalyst": ("数据分析员", "数据研究", "通过工具与 Notebook 代码执行处理数据、检索及采集任务。"),
    "ProjectManager": ("项目经理", "软件开发", "将需求和设计拆解为开发任务，分析依赖关系。"),
    "Engineer": ("经典工程师", "软件开发", "以经典动作流程编写代码、审查与处理实现反馈。"),
    "QaEngineer": ("测试工程师", "软件开发", "主要围绕 Python 项目生成和运行测试，反馈调试信息。"),
    "SWEAgent": ("代码库修复员", "软件开发", "面向已有代码库的 Issue 和 Bug，使用终端及代码变更工具。"),
    "DataInterpreter": ("数据解释器", "数据研究", "先规划，再编写和执行分析代码，按结果重试与推进。"),
    "Researcher": ("研究员", "数据研究", "收集链接、浏览摘要、汇总生成 Markdown 研究报告。"),
    "Searcher": ("检索助手", "数据研究", "搜索信息并进行摘要问答。"),
    "Sales": ("导购助手", "业务助手", "基于知识库回答商品与零售咨询，不是销售指标分析员。"),
    "CustomerService": ("客服示例", "业务助手", "继承 Sales，按客服提示词与问答知识工作；未内置订单后台操作。"),
    "InvoiceOCRAssistant": ("发票识别助手", "业务助手", "识别发票内容、生成信息表，并对单份发票进行问答。"),
    "Teacher": ("教学计划助手", "内容", "按章节生成可配置语言的教学计划。"),
    "TutorialAssistant": ("教程助手", "内容", "从主题生成目录，再编写教程正文。"),
    "Assistant": ("技能助手", "通用", "管理对话记忆，选择技能、解析参数并调用技能。"),
    "AndroidAssistant": ("Android 助手", "场景扩展", "在专用环境中学习并执行手机应用操作。"),
    "Experimenter": ("机器学习实验员", "场景扩展", "SELA 的实验执行、计划变更、状态保存与评分。"),
    "STRole": ("虚拟居民", "场景扩展", "Stanford Town 中具有记忆和日程的社会模拟角色。"),
    "Moderator": ("狼人杀主持人", "场景扩展", "组织狼人杀游戏流程和结果判定。"),
    "Werewolf": ("狼人", "场景扩展", "狼人杀场景中的狼人角色。"),
    "Villager": ("村民", "场景扩展", "狼人杀场景中的村民角色。"),
    "Seer": ("预言家", "场景扩展", "狼人杀场景中的查验角色。"),
    "Witch": ("女巫", "场景扩展", "狼人杀场景中的女巫角色。"),
    "Guard": ("守卫", "场景扩展", "狼人杀场景中的守护角色。"),
}
entry = ast.parse((UP / "metagpt/software_company.py").read_text(encoding="utf-8"))
default = set()
for node in ast.walk(entry):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "hire":
        for item in node.args[0].elts:
            if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
                default.add(item.func.id)
rows = []
for folder in (UP / "metagpt/roles", UP / "metagpt/ext"):
    for path in sorted(folder.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in tree.body:
            if not isinstance(node, ast.ClassDef) or node.name not in INFO:
                continue
            fields = {}
            for child in node.body:
                if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name) and child.value is not None:
                    try: fields[child.target.id] = ast.literal_eval(child.value)
                    except (ValueError, TypeError): pass
            label, category, description = INFO[node.name]
            rel = path.relative_to(UP).as_posix()
            group = "default" if node.name in default else "extension" if "/ext/" in rel else "optional"
            rows.append({"class": node.name, "label": label, "category": category, "description": description,
                         "group": group, "base": ", ".join(ast.unparse(b) for b in node.bases),
                         "tools": fields.get("tools", []), "path": rel, "line": node.lineno,
                         "source": f"https://github.com/FoundationAgents/MetaGPT/blob/{COMMIT}/{rel}#L{node.lineno}",
                         "runtime_verified": False})
assert len(rows) == len(INFO) == 27, "Unexpected role inventory"
assert sum(r["group"] == "default" for r in rows) == 5
rows.sort(key=lambda r: ({"default": 0, "optional": 1, "extension": 2}[r["group"]], r["category"], r["class"]))
output = ROOT / "web/assets/agents.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({"commit": COMMIT, "scope": "角色类定义，不含基类和 examples 教学角色", "agents": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Verified {len(rows)} role definitions: 5 default, 13 optional, 9 extension.")
