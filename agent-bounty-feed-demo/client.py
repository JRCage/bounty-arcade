#!/usr/bin/env python3
"""No-dependency, read-only client for Agent Bounty Feed's public JSON endpoint."""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

URL = "https://dailydollar-bot.github.io/agent-bounty-feed/feed.json"

def load_feed(url=URL, opener=urlopen):
    req = Request(url, headers={"User-Agent": "agent-bounty-feed-example/1.0", "Accept": "application/json"})
    with opener(req, timeout=15) as response:
        data = json.load(response)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for name in ("items", "bounties"):
            if isinstance(data.get(name), list):
                return data[name]
    raise ValueError("Unexpected feed structure (expected list or items/bounties array)")

def main():
    parser = argparse.ArgumentParser(description="Read public Agent Bounty Feed; no wallet, auth, or payment")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1 or args.limit > 100:
        parser.error("--limit must be between 1 and 100")
    try:
        items = load_feed()
        print(f"Feed items: {len(items)}")
        for item in items[:args.limit]:
            if not isinstance(item, dict):
                print("  - [unrecognized item]")
                continue
            title = item.get("title") or item.get("name") or item.get("id") or "(untitled)"
            reward = item.get("reward", "?")
            currency = item.get("currency", "")
            url = item.get("url", "")
            print(f"- {title} | {reward} {currency} | {url}")
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"Feed unavailable or invalid: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
