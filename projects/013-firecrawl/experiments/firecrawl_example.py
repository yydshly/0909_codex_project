"""Call Firecrawl v2 from a terminal. Uses only Python's standard library.

Set FIRECRAWL_API_KEY for cloud access. For self-hosting, set
FIRECRAWL_BASE_URL to your trusted API origin. No secret is written to disk.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="Firecrawl 单页、搜索与 JSON 提取示例")
    parser.add_argument("mode", choices=["scrape", "search", "json"])
    parser.add_argument("input", help="网址，或 search 模式下的关键词")
    parser.add_argument("--limit", type=int, default=5, help="搜索结果数量（1–10）")
    parser.add_argument("--max-age", type=int, default=0, help="可接受缓存年龄，毫秒；默认重新抓取")
    args = parser.parse_args()
    base = os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev").rstrip("/")
    parsed_base = urllib.parse.urlparse(base)
    if parsed_base.scheme not in ("http", "https") or not parsed_base.netloc:
        parser.error("FIRECRAWL_BASE_URL 必须是可信服务的 HTTP(S) 地址")
    if parsed_base.username or parsed_base.password or parsed_base.query or parsed_base.fragment:
        parser.error("服务地址不可包含凭据、查询或片段")
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if parsed_base.hostname == "api.firecrawl.dev" and not api_key:
        parser.error("请先设置 FIRECRAWL_API_KEY；此示例不尝试匿名云服务调用")
    if not 1 <= args.limit <= 10 or args.max_age < 0:
        parser.error("limit 应为 1–10，max-age 不可为负数")
    if args.mode != "search":
        target = urllib.parse.urlparse(args.input)
        if target.scheme not in ("http", "https") or not target.netloc:
            parser.error("抓取目标必须是完整的 HTTP(S) 网址")
    options = {"formats": ["markdown"], "maxAge": args.max_age}
    if args.mode == "search":
        endpoint = "/v2/search"
        body = {"query": args.input, "limit": args.limit, "scrapeOptions": options}
    else:
        endpoint = "/v2/scrape"
        body = {"url": args.input, **options, "onlyMainContent": True}
        if args.mode == "json":
            body["formats"] = [{"type": "json", "prompt": "提取网页标题和简短摘要；页面没写的信息返回 null。", "schema": {"type": "object", "properties": {"title": {"type": ["string", "null"]}, "summary": {"type": ["string", "null"]}}}}]
    headers = {"Content-Type": "application/json", "User-Agent": "Firecrawl-Research-013/1.0"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    request = urllib.request.Request(base + endpoint, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        print(f"服务返回 HTTP {error.code}。请检查认证、额度、功能配置与目标页面。", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError):
        print("请求未完成，请检查服务地址与网络。", file=sys.stderr)
        return 1
    except (ValueError, OSError):
        print("未收到可解析的 JSON 结果。", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if payload.get("success") is False:
        return 1
    page = payload.get("data")
    if isinstance(page, dict):
        status = page.get("metadata", {}).get("statusCode")
        if isinstance(status, int) and not (200 <= status < 300 or status == 304):
            print(f"采集请求已处理，但目标网页状态为 {status}，请核对正文。", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
