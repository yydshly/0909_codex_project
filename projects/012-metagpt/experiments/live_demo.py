"""Opt-in original DataInterpreter demo; requires a local model config.

Generated code is executed by upstream MetaGPT in a local notebook kernel.
The sample data is synthetic. This is not used by the offline webpage runner.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


async def run(config_file):
    import yaml
    path = Path(config_file).expanduser().resolve()
    if not path.is_file():
        raise SystemExit("找不到模型配置文件。请复制 runtime/model.example.yaml 并填写本机配置。")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    llm = data.get("llm", {}) if isinstance(data, dict) else {}
    if not llm.get("model") or llm.get("api_key") in (None, "", "YOUR_API_KEY"):
        raise SystemExit("配置需要 llm.model 和 llm.api_key。本机 Ollama 可用非空占位值。")
    local = PROJECT / "runtime/local/live"
    (local / "config").mkdir(parents=True, exist_ok=True)
    # Config remains in ignored local storage; it is never sent to the viewer.
    (local / "config/config2.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    os.environ["METAGPT_PROJECT_ROOT"] = str(local)
    os.chdir(local)
    from metagpt.config2 import Config
    from metagpt.roles.di.data_interpreter import DataInterpreter
    sample = local / "sales.csv"
    sample.write_text("product,month,amount\nA,2026-07,100\nA,2026-08,130\nB,2026-07,200\nB,2026-08,180\n", encoding="utf-8")
    cfg = Config.from_llm_config(llm)
    role = DataInterpreter(config=cfg, max_react_loop=8, auto_run=True)
    task = (f"使用 Python 分析虚构销售数据 {sample.as_posix()}。按产品计算两个月合计销售额与环比。"
            f"输出中文 Markdown 报告到 {(local / 'analysis.md').as_posix()}，以及对比图到 {(local / 'sales.png').as_posix()}。"
            "仅使用这些样本数据，不进行网络检索。完成后核验数值与输出文件。")
    await asyncio.wait_for(role.run(task), timeout=600)
    print(json.dumps({"mode": "live-DataInterpreter", "output_directory": str(local),
                      "report_exists": (local / "analysis.md").exists(), "chart_exists": (local / "sales.png").exists()}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="本机模型配置文件路径，勿提交密钥")
    args = parser.parse_args()
    asyncio.run(run(args.config))
