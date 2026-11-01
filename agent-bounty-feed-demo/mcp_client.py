#!/usr/bin/env python3
"""Read-only Streamable HTTP MCP client for Agent Bounty Feed. Python stdlib only."""
import argparse
import json
import sys
import uuid
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ENDPOINT = "https://agent-bounty-feed.dailydollar.workers.dev/mcp"
PROTOCOL = "2025-03-26"

def decode_response(raw, content_type):
    text = raw.decode("utf-8")
    if "text/event-stream" in content_type:
        events = []
        for line in text.splitlines():
            if line.startswith("data:"):
                try:
                    events.append(json.loads(line[5:].strip()))
                except json.JSONDecodeError:
                    continue
        if not events:
            raise ValueError("No JSON-RPC data events in SSE response")
        return events[-1]
    return json.loads(text) if text.strip() else {}

class MCPClient:
    def __init__(self, endpoint=ENDPOINT, opener=urlopen):
        self.endpoint, self.opener, self.session = endpoint, opener, None
    def request(self, method, params=None, notification=False):
        message = {"jsonrpc":"2.0", "method":method}
        if params is not None:
            message["params"] = params
        if not notification:
            message["id"] = str(uuid.uuid4())
        headers = {
            "Content-Type":"application/json",
            "Accept":"application/json, text/event-stream",
            "MCP-Protocol-Version":PROTOCOL,
            "User-Agent":"bounty-arcade-mcp-demo/1.0"
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = Request(self.endpoint, json.dumps(message).encode("utf-8"), headers=headers, method="POST")
        with self.opener(req, timeout=20) as response:
            self.session = response.headers.get("Mcp-Session-Id", self.session)
            result = decode_response(response.read(), response.headers.get("Content-Type", "application/json"))
        if isinstance(result, dict) and result.get("error"):
            raise ValueError("MCP error: " + str(result["error"]))
        return result
    def initialize(self):
        result = self.request("initialize", {
            "protocolVersion":PROTOCOL,
            "capabilities":{},
            "clientInfo":{"name":"bounty-arcade-example","version":"1.0"}
        })
        self.request("notifications/initialized", notification=True)
        return result
    def list(self):
        return self.request("tools/call", {"name":"list_bounties","arguments":{}})

def main():
    parser = argparse.ArgumentParser(description="List current bounties via the free MCP server")
    parser.add_argument("--endpoint", default=ENDPOINT, help="MCP Streamable HTTP URL")
    args = parser.parse_args()
    try:
        client = MCPClient(args.endpoint)
        client.initialize()
        result = client.list()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print("Request failed:", exc, file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
