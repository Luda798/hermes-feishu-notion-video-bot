#!/usr/bin/env python3
"""Apply a JSON payload to the Notion API.

Usage:
    python3 scripts/notion_apply_payload.py POST /v1/pages payload.json
    python3 scripts/notion_apply_payload.py PATCH /v1/blocks/<page_id>/children payload.json
    python3 scripts/notion_apply_payload.py GET /v1/pages/<page_id>

Reads NOTION_API_KEY from the environment or ~/.hermes/.env. By default this
script prints only a compact summary to avoid leaking Notion content into chat
logs. Full output requires an explicit double-confirmation flag.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

NOTION_VERSION = os.environ.get("NOTION_VERSION", "2025-09-03")
DEFAULT_API_BASE = "https://api.notion.com"


def load_notion_env_if_needed() -> None:
    """Best-effort load of only Notion-related vars from ~/.hermes/.env."""
    env_path = Path.home() / ".hermes" / ".env"
    if not env_path.exists():
        return
    wanted = {"NOTION_API_KEY", "NOTION_VERSION"}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in wanted or key in os.environ:
            continue
        os.environ[key] = value.strip().strip('"').strip("'")


def validate_api_base(api_base: str, allow_custom: bool) -> str:
    parsed = urllib.parse.urlparse(api_base)
    if not allow_custom and (parsed.scheme, parsed.netloc) != ("https", "api.notion.com"):
        raise SystemExit(
            "Refusing to send Notion token to custom NOTION_API_BASE. "
            "Use --allow-custom-api-base only if you fully trust the endpoint."
        )
    if parsed.scheme != "https":
        raise SystemExit("Notion API base must use https")
    return api_base.rstrip("/")


def request(method: str, endpoint: str, payload_path: str | None, api_base: str) -> dict:
    load_notion_env_if_needed()
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        raise SystemExit("Missing NOTION_API_KEY. Set it in environment or ~/.hermes/.env")

    data = None
    if payload_path:
        data = Path(payload_path).read_bytes()
        # Validate JSON early so malformed payloads fail locally.
        json.loads(data.decode("utf-8"))

    url = api_base + endpoint
    req = urllib.request.Request(url, data=data, method=method.upper())
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", os.environ.get("NOTION_VERSION", NOTION_VERSION))
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {"ok": True}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(json.dumps({"ok": False, "status": exc.code, "error": body}, ensure_ascii=False))


def summarize(obj: dict) -> dict:
    return {
        "ok": "object" in obj or obj.get("ok") is True,
        "object": obj.get("object"),
        "id": obj.get("id"),
        "url": obj.get("url"),
        "archived": obj.get("archived"),
        "has_more": obj.get("has_more"),
        "results_count": len(obj.get("results", [])) if isinstance(obj.get("results"), list) else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("method", help="HTTP method, e.g. GET, POST, PATCH")
    parser.add_argument("endpoint", help="Notion API endpoint, e.g. /v1/pages")
    parser.add_argument("payload", nargs="?", help="Path to JSON payload file")
    parser.add_argument("--full", action="store_true", help="Print full response; may include private Notion content")
    parser.add_argument("--i-understand-this-may-print-private-data", action="store_true")
    parser.add_argument("--allow-custom-api-base", action="store_true", help="Allow NOTION_API_BASE other than https://api.notion.com")
    args = parser.parse_args()

    if args.full and not args.i_understand_this_may_print_private_data:
        raise SystemExit("--full may print private Notion content; add --i-understand-this-may-print-private-data to continue")

    api_base = validate_api_base(os.environ.get("NOTION_API_BASE", DEFAULT_API_BASE), args.allow_custom_api_base)
    obj = request(args.method, args.endpoint, args.payload, api_base)
    print(json.dumps(obj if args.full else summarize(obj), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
