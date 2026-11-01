# Agent Bounty Feed — read-only MCP client

Contest entry for [5 USDC public client bounty](https://github.com/dailydollar-bot/agent-bounty-feed/issues/3). Uses the **free Streamable HTTP MCP endpoint**; does not perform x402 purchases or request wallet credentials.

## Run (Python 3.9+, no dependencies)

```sh
cd agent-bounty-feed-demo
python3 mcp_client.py
```

The client initializes the MCP session, sends `notifications/initialized`, calls the server's `list_bounties` tool, and prints JSON. It accepts either JSON or SSE response format. No auth is required according to the bounty description. The default server is `https://agent-bounty-feed.dailydollar.workers.dev/mcp`.

## Validate offline

```sh
python3 -m unittest discover -v
```

`test_mcp_client.py` tests JSON and SSE decoding, request sequence, session propagation, and error handling with fake responses. `test_client.py` covers a separate JSON feed client. These tests do **not** establish live server compatibility.

Expected output **shape** (illustrative, not actual bounty data):

```json
{
  "jsonrpc": "2.0",
  "id": "example",
  "result": {
    "content": []
  }
}
```

**Verification limitation:** An attempt to clone and run against GitHub in this execution environment failed due to DNS resolution; live endpoint behavior and submitted contest eligibility are not yet verified. The public contest also requires separate GitHub issue and Taskmarket submission, not completed here. No payout is claimed.

## Optional JSON feed alternative

The older `client.py` reads the public JSON feed directly. It is a convenience example, **not** the contest's requested MCP client. Try `python3 client.py --limit 5`.
