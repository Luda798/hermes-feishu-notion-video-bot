#!/usr/bin/env python3
"""Verify Notion API connectivity and search for a database by name.

Usage:
    python3 scripts/verify_notion_connection.py "我的知识库"
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

NOTION_VERSION = os.environ.get("NOTION_VERSION", "2025-09-03")
DEFAULT_API_BASE = "https://api.notion.com"


def load_notion_env_if_needed() -> None:
    if os.environ.get("NOTION_API_KEY"):
        return
    env_path = Path.home() / ".hermes" / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "NOTION_API_KEY":
            os.environ["NOTION_API_KEY"] = value.strip().strip('"').strip("'")
            return


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


def notion_post(endpoint: str, payload: dict, api_base: str) -> dict:
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        raise SystemExit("Missing NOTION_API_KEY")
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(api_base + endpoint, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Notion-Version", os.environ.get("NOTION_VERSION", NOTION_VERSION))
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def title_of(item: dict) -> str:
    title = item.get("title") or []
    if title and isinstance(title, list):
        return "".join(part.get("plain_text", "") for part in title)
    return item.get("name") or ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("database_name")
    parser.add_argument("--allow-custom-api-base", action="store_true")
    parser.add_argument("--show-ids", action="store_true", help="Print Notion IDs; useful for debugging but avoid sharing publicly")
    args = parser.parse_args()

    load_notion_env_if_needed()
    api_base = validate_api_base(os.environ.get("NOTION_API_BASE", DEFAULT_API_BASE), args.allow_custom_api_base)
    result = notion_post("/v1/search", {"query": args.database_name, "page_size": 10}, api_base)
    matches = []
    for item in result.get("results", []):
        obj = item.get("object")
        name = title_of(item)
        if args.database_name in name or name in args.database_name:
            entry = {"object": obj, "name": name, "url": item.get("url")}
            if args.show_ids:
                entry["id"] = item.get("id")
            matches.append(entry)
    print(json.dumps({"ok": True, "query": args.database_name, "matches": matches}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
