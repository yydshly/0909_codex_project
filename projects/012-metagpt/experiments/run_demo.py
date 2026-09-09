"""Run real MetaGPT scheduling with deterministic, explicitly non-LLM actions.

The two calculator implementations are authored fixtures. MetaGPT itself handles
role activation, message routing, memory, and the test/fix feedback cycle.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

PROJECT = Path(__file__).resolve().parents[1]
LOCAL = PROJECT / "runtime" / "local"
LOCAL.mkdir(parents=True, exist_ok=True)
(LOCAL / "config").mkdir(exist_ok=True)
(LOCAL / "config" / "config2.yaml").write_text(
    'llm:\n  api_type: openai\n  api_key: offline-not-a-secret\n'
    '  model: offline-no-model\n  base_url: http://127.0.0.1:9/v1\n',
    encoding="utf-8",
)
os.environ["METAGPT_PROJECT_ROOT"] = str(LOCAL)
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from metagpt.actions import Action, UserRequirement
from metagpt.config2 import Config
from metagpt.context import Context
from metagpt.environment import Environment
from metagpt.provider.base_llm import BaseLLM
from metagpt.roles.role import Role
from metagpt.schema import AIMessage
from metagpt.team import Team
from metagpt.logs import logger

logger.remove()
logger.add(sys.stderr, level="WARNING")


class NoModel(BaseLLM):
    """Fail closed if an action accidentally requests model inference."""
    calls = 0

    def __init__(self, config):
        self.config = config
        self.model = "offline-no-model"
        self.cost_manager = None

    async def aask(self, *args, **kwargs):
        self.calls += 1
        raise RuntimeError("离线演示禁止调用模型。")

    async def _achat_completion(self, *args, **kwargs):
        return await self.aask()

    async def acompletion(self, *args, **kwargs):
        return await self.aask()

    async def _achat_completion_stream(self, *args, **kwargs):
        return await self.aask()


RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:6]
RUN_DIR = LOCAL / "runs" / RUN_ID
EVENTS = []
START = time.monotonic()


def write(name: str, content: str):
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_DIR / name).write_text(content, encoding="utf-8")


def message(action, actor, title, text, artifacts=(), **extra):
    payload = {"actor": actor, "title": title, "text": text,
               "artifacts": list(artifacts), **extra}
    return AIMessage(content=json.dumps(payload, ensure_ascii=False),
                     sent_from=actor, cause_by=action, metadata={"demo": payload})


class TracedEnvironment(Environment):
    def publish_message(self, message, peekable=True):
        data = message.metadata.get("demo", {})
        EVENTS.append({"index": len(EVENTS), "elapsed_ms": round((time.monotonic()-START)*1000),
                       "actor": data.get("actor", "用户"),
                       "title": data.get("title", "提交任务"),
                       "text": data.get("text", message.content),
                       "cause_by": message.cause_by.rsplit(".", 1)[-1],
                       "send_to": sorted(message.send_to), **data})
        return super().publish_message(message, peekable)


class TestsFailed(Action):
    """Event type used to wake the developer after a failed test."""


class TestsPassed(Action):
    """Terminal event: no role watches this event."""


class DraftRequirement(Action):
    async def run(self, history):
        write("requirements.md", """# 优惠金额计算器：验收需求

输入原价 subtotal、优惠券 coupon 和折扣系数 rate。
先减优惠券，再打折；优惠券超出原价时结果为零。
金额采用十进制运算，保留两位小数并四舍五入。
拒绝负数、无穷大、NaN，以及不在 0 到 1 范围内的折扣。
提供可运行的 Python 命令行入口与自动化测试。

来源：本实验预先编写的固定需求，不是模型生成内容。
""")
        return message(type(self), "产品经理", "整理需求与验收标准",
                       "明确先减券再打折、最低为零、金额精度与非法输入规则。", ["requirements.md"])


class DesignSolution(Action):
    async def run(self, history):
        write("design.md", """# 技术设计

- payable(subtotal, coupon=0, rate=1) 返回两位小数的字符串。
- 使用 decimal.Decimal 避免二进制浮点误差。
- 命令行输入三个参数，输出 JSON。
- unittest 独立执行，结果以 JSON 返回给测试角色。
- 测试失败消息触发开发角色返修；成功消息终止交接。

来源：本实验预先编写的设计。
""")
        return message(type(self), "架构师", "确定接口与执行方案",
                       "采用 Decimal、单函数接口和独立测试进程，给下游明确输入输出。", ["design.md"])


class PlanWork(Action):
    async def run(self, history):
        tasks = [{"id": "implement", "assignee": "开发工程师", "depends_on": [], "output": "calculator.py"},
                 {"id": "test", "assignee": "测试工程师", "depends_on": ["implement"], "output": "tests-round-N.json"}]
        write("tasks.json", json.dumps(tasks, ensure_ascii=False, indent=2))
        return message(type(self), "项目经理", "拆分任务与交接关系",
                       "开发提交实现后触发测试；测试失败触发返修。这里的任务清单由固定动作产生。", ["tasks.json"])


CALCULATOR = '''"""Fixed demo fixture, delivered by a MetaGPT Action; not LLM-generated."""
from decimal import Decimal, ROUND_HALF_UP
import argparse
import json

def payable(subtotal, coupon=0, rate=1):
    subtotal, coupon, rate = map(lambda v: Decimal(str(v)), (subtotal, coupon, rate))
    if not all(v.is_finite() for v in (subtotal, coupon, rate)):
        raise ValueError("Inputs must be finite")
    if subtotal < 0 or coupon < 0 or not 0 <= rate <= 1:
        raise ValueError("Invalid amount or rate")
    amount = __FORMULA__
    return str(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subtotal")
    parser.add_argument("--coupon", default="0")
    parser.add_argument("--rate", default="1")
    args = parser.parse_args()
    print(json.dumps({"payable": payable(args.subtotal, args.coupon, args.rate)}))
'''

TESTS = '''import io
import json
import unittest
from calculator import payable

class CalculatorChecks(unittest.TestCase):
    def test_normal(self): self.assertEqual(payable(100), "100.00")
    def test_coupon(self): self.assertEqual(payable(100, 20), "80.00")
    def test_discount(self): self.assertEqual(payable(100, 0, "0.9"), "90.00")
    def test_coupon_before_discount(self): self.assertEqual(payable(100, 20, "0.9"), "72.00")
    def test_floor_zero(self): self.assertEqual(payable(10, 100, "0.9"), "0.00")
    def test_decimal_rounding(self): self.assertEqual(payable("0.05", 0, "0.5"), "0.03")
    def test_invalid(self):
        for values in [(-1, 0, 1), (1, -1, 1), (1, 0, 2), (1, 0, -1)]:
            with self.subTest(values=values), self.assertRaises(ValueError): payable(*values)
    def test_nonfinite(self):
        for value in ["NaN", "Infinity"]:
            with self.subTest(value=value), self.assertRaises(ValueError): payable(value)

if __name__ == "__main__":
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CalculatorChecks))
    print(json.dumps({"success": result.wasSuccessful(), "tests": result.testsRun,
                      "failures": len(result.failures), "errors": len(result.errors),
                      "output": stream.getvalue()}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
'''


class ImplementCalculator(Action):
    async def run(self, history):
        repair = any(m.cause_by.endswith("TestsFailed") for m in history)
        formula = 'max(Decimal("0"), subtotal - coupon) * rate' if repair else 'max(Decimal("0"), subtotal * rate - coupon)'
        code = CALCULATOR.replace("__FORMULA__", formula)
        write("calculator.py", code)
        write("calculator-v2.py" if repair else "calculator-v1.py", code)
        return message(type(self), "开发工程师", "依据失败测试交付修正版" if repair else "交付首版代码（故意植入顺序缺陷）",
                       "修正为先减优惠券、再计算折扣。修复规则是预先编写的，不是 AI 推断。" if repair else
                       "首版固定样例故意先打折再减券，用于观察真实的测试失败与消息返修链。",
                       ["calculator.py", "calculator-v2.py" if repair else "calculator-v1.py"], iteration=2 if repair else 1)


class RunChecks(Action):
    async def run(self, history):
        write("test_calculator.py", TESTS)
        iteration = sum(m.cause_by.endswith("ImplementCalculator") for m in history)
        proc = await asyncio.create_subprocess_exec(sys.executable, str(RUN_DIR / "test_calculator.py"),
                   cwd=str(RUN_DIR), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        if proc.returncode not in (0, 1):
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
        result = json.loads(stdout.decode("utf-8"))
        filename = f"tests-round-{iteration}.json"
        write(filename, json.dumps(result, ensure_ascii=False, indent=2))
        event = TestsPassed if result["success"] else TestsFailed
        return message(event, "测试工程师", "回归测试全部通过" if result["success"] else "测试发现缺陷，触发返修",
                       "8 项真实单元测试全部通过，协作链结束。" if result["success"] else
                       "组合优惠应为 72.00，首版实际为 70.00。TestsFailed 消息将唤醒开发角色。",
                       [filename, "test_calculator.py"], iteration=iteration, test_result=result)


async def main():
    config = Config.from_llm_config({"api_type": "openai", "api_key": "offline-not-a-secret",
                                    "base_url": "http://127.0.0.1:9/v1", "model": "offline-no-model"})
    context = Context(config=config)
    no_model = NoModel(config.llm)
    env = TracedEnvironment(context=context)
    team = Team(context=context, env=env, use_mgx=False)
    definitions = [("产品经理", DraftRequirement, [UserRequirement]),
                   ("架构师", DesignSolution, [DraftRequirement]),
                   ("项目经理", PlanWork, [DesignSolution]),
                   ("开发工程师", ImplementCalculator, [PlanWork, TestsFailed]),
                   ("测试工程师", RunChecks, [ImplementCalculator])]
    roles = [Role(name=name, profile=name, goal="演示固定软件交付流程",
                  actions=[action(context=context, llm=no_model)], watch=watch, context=context, llm=no_model)
             for name, action, watch in definitions]
    team.hire(roles)
    team.invest(1)
    await team.run(n_round=15, idea="交付一个先减优惠券再打折的金额计算器，并验证边界条件。", auto_archive=False)
    tests = [e["test_result"] for e in EVENTS if "test_result" in e]
    expected = ["UserRequirement", "DraftRequirement", "DesignSolution", "PlanWork",
                "ImplementCalculator", "TestsFailed", "ImplementCalculator", "TestsPassed"]
    actual = [e["cause_by"] for e in EVENTS]
    if actual != expected or len(tests) != 2 or tests[0]["success"] or not tests[-1]["success"]:
        raise RuntimeError(f"Unexpected real framework trace: {actual}")
    if not env.is_idle or no_model.calls:
        raise RuntimeError("The team did not become idle or unexpectedly requested a model.")
    commit = subprocess.check_output(["git", "-C", str(PROJECT / "upstream"), "rev-parse", "HEAD"], text=True).strip()
    artifacts = [{"name": p.name, "content": p.read_text(encoding="utf-8")}
                 for p in sorted(RUN_DIR.iterdir()) if p.is_file()]
    report = {"schema_version": 1, "run_id": RUN_ID, "mode": "fixed-actions-no-llm",
              "completed_at": datetime.now(timezone.utc).isoformat(), "commit": commit,
              "engine": "upstream MetaGPT Team / Environment / Role / Action", "model_calls": no_model.calls,
              "success": True, "team_idle": env.is_idle, "role_count": len(roles),
              "framework_seconds": round(time.monotonic()-START, 3), "events": EVENTS,
              "test_rounds": tests, "artifacts": artifacts,
              "scope": "真实框架调度、真实文件写入和测试进程；角色动作与代码为预编写样例，无模型推理。",
              "not_verified": ["内置 TeamLeader 的模型分派", "内置软件团队端到端生成", "LLM 代码生成", "LanceDB 检索接口"]}
    write("report.json", json.dumps(report, ensure_ascii=False, indent=2))
    target = PROJECT / "web" / "assets" / "run.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(".tmp")
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(target)
    (LOCAL / "latest-run.txt").write_text(str(RUN_DIR), encoding="utf-8")
    print(json.dumps({"success": True, "run_id": RUN_ID, "events": len(EVENTS), "tests": tests[-1]["tests"],
                      "model_calls": no_model.calls, "output": str(RUN_DIR)}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
