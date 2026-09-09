"""Loopback-only viewer and fixed-demo runner. No secrets or arbitrary commands."""
from __future__ import annotations
import argparse
from decimal import Decimal, InvalidOperation
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import threading
from urllib.parse import urlparse

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "web"
LOCK = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    def reply(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/api/health":
            self.reply({"service": "metagpt-lab", "fixed_demo": True, "live_model_configured": False})
        else:
            super().do_GET()

    def do_POST(self):
        host = self.headers.get("Host", "")
        origin = self.headers.get("Origin")
        if (host not in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
                or (origin and origin not in {f"http://{host}"})
                or self.headers.get("X-MetaGPT-Demo") != "local"):
            return self.reply({"error": "仅接受本机演示页面请求。"}, 403)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 <= size <= 2048:
                return self.reply({"error": "请求过大。"}, 413)
            data = json.loads(self.rfile.read(size) or b"{}")
            if not isinstance(data, dict):
                raise ValueError("请求必须是对象。")
            route = urlparse(self.path).path
            if route == "/api/run":
                if not LOCK.acquire(blocking=False):
                    return self.reply({"error": "已有演示运行中，请稍后再试。"}, 409)
                try:
                    result = subprocess.run([sys.executable, str(PROJECT / "experiments/run_demo.py")],
                                            cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
                                            errors="replace", timeout=240)
                    if result.returncode:
                        self.save_error(result)
                        return self.reply({"error": "框架运行失败，请查看 runtime/local/last-error.txt。"}, 500)
                    report = json.loads((WEB / "assets/run.json").read_text(encoding="utf-8"))
                    return self.reply(report)
                finally:
                    LOCK.release()
            if route == "/api/calculate":
                values = [str(data.get(key, default)) for key, default in [("subtotal", "100"), ("coupon", "20"), ("rate", "0.9")]]
                if any(len(v) > 24 for v in values):
                    raise ValueError("输入数值过长。")
                decimals = [Decimal(v) for v in values]
                if not all(v.is_finite() and 0 <= v <= 1000000000 for v in decimals) or decimals[2] > 1:
                    raise ValueError("金额应为非负有限数，折扣系数应在 0 到 1 之间。")
                latest = PROJECT / "runtime/local/latest-run.txt"
                if not latest.exists():
                    return self.reply({"error": "请先运行协作演示。"}, 409)
                run = Path(latest.read_text(encoding="utf-8")).resolve()
                if not run.is_relative_to((PROJECT / "runtime/local/runs").resolve()):
                    raise ValueError("产物路径无效。")
                result = subprocess.run([sys.executable, str(run / "calculator.py"), values[0], "--coupon", values[1], "--rate", values[2]],
                                        cwd=run, capture_output=True, text=True, timeout=10)
                if result.returncode:
                    raise ValueError("计算器拒绝了这组输入。")
                return self.reply({**json.loads(result.stdout), "run_id": run.name, "execution": "generated-python-artifact"})
            return self.reply({"error": "未知接口。"}, 404)
        except (ValueError, InvalidOperation):
            return self.reply({"error": "输入无效，请检查金额、折扣或请求格式。"}, 400)
        except subprocess.TimeoutExpired:
            return self.reply({"error": "运行超时，请在本机检查运行日志。"}, 504)

    def save_error(self, result):
        target = PROJECT / "runtime/local/last-error.txt"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result.stderr + "\n" + result.stdout, encoding="utf-8")
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8122)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(WEB)))
    print(f"MetaGPT Lab http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()
