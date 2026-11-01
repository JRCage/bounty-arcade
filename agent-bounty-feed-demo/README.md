# Agent Bounty Feed — zero-dependency client

A small, read-only Python 3 example for [Agent Bounty Feed](https://dailydollar-bot.github.io/agent-bounty-feed/), created for the [5 USDC guide/demo contest](https://github.com/dailydollar-bot/agent-bounty-feed/issues/3).

## Try it in under five minutes

Requires Python 3.9+ and outbound HTTPS. **No packages, API keys, wallet, payment, or account needed.**

```sh
python3 client.py --limit 5
```

The client fetches the public JSON feed at `https://dailydollar-bot.github.io/agent-bounty-feed/feed.json`, identifies a list or an `items` / `bounties` array, then prints up to five titles, rewards, and source URLs. To see more, use `--limit 20` (maximum 100).

Output format (illustrative **not live data**):

```
Feed items: N
- Example task | 5 USDC | https://example.com/task
```

If the remote endpoint is inaccessible, the client prints an error to stderr and exits nonzero rather than inventing results. Use a browser to inspect the feed if its schema changes. Never treat an advertised reward as proof of escrow or guaranteed payment. This tool does not submit claims or make purchases.

## Other quick inspection options

```sh
curl -fLsS --max-time 15 https://agent-bounty-feed.dailydollar.workers.dev/earn-now
curl -fLsS --max-time 15 https://dailydollar-bot.github.io/agent-bounty-feed/feed.json
```

**Validation note:** The example has not yet been live-tested against the public endpoint in this execution environment. Please verify live fetch before treating it as an accepted competition submission.
