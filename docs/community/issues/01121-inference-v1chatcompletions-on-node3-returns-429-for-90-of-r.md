---
title: "#1121 — Inference /v1/chat/completions on node3 returns 429 for ~90% of requests — single live TA caps community gateways at ~10% pass-rate"
source: https://github.com/gonka-ai/gonka/issues/1121
issue_number: 1121
synced_at: 2026-08-05T14:39:32Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Inference /v1/chat/completions on node3 returns 429 for ~90% of requests — single live TA caps community gateways at ~10% pass-rate
    <span class="issues-number">#1121</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-04-26 22:40 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-05-21 21:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`POST /v1/chat/completions` on the only currently-reachable Transfer Agent
(`node3.gonka.ai`) returns `HTTP 429 "rate limit exceeded"` for ~90% of
requests, regardless of caller IP, key, or request shape. Other endpoints
on the same host (`/v1/identity`, `/v1/models`) work normally.

This caps every public community-run gateway at a global ~10% pass-rate.
On the gonka.pw monitor today this lines up roughly:

| Provider | 24h uptime | p50 TTFT |
|---|---:|---:|
| `proxy-gonka-gg` | 94.6% | 1064 ms |
| `andrey-panasenko-gateway` | 89.1% | 1124 ms |
| `mingles-gateway` | 82.4% | 1012 ms |
| `gonkagate` | 59.3% | 3596 ms |
| `gate-joingonka-ai` (mine) | **3.7%** | **19729 ms** |

The 19.7s p50 TTFT on our gateway is the giveaway: when a request *does*
succeed, it's the **second or third retry** that goes through. The first
attempt hangs for the SDK timeout (15s) before the next retry catches a
brief window where the limiter passes.

## State of `allowed_transfer_addresses`

```bash
$ curl -s "$NODE/chain-api/productscience/inference/inference/params" \
    | jq -r '.params.transfer_agent_access_params.allowed_transfer_addresses'
# 3 entries: node1, node2, node3
```

- `node1.gonka.ai:8000` — TCP timeout from anywhere we tried
- `node2.gonka.ai:8000` — TCP timeout from anywhere we tried
- `node3.gonka.ai` — `/v1/identity` and `/v1/models` answer in ~150ms; only
  `/v1/chat/completions` is rate-limited

So the network has effectively a **single live TA** for every public gateway,
and that TA is rate-limiting the inference endpoint hard.

## Reproduction

Anyone with `gonka-openai` SDK and any private key (signed transactions
work, just won't bill correctly with a fresh key) can reproduce:

```js
import { GonkaOpenAI } from 'gonka-openai';
import { randomBytes } from 'node:crypto';

const ep = {
  url: 'https://node3.gonka.ai/v1',
  transferAddress: 'gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5',
};

for (let i = 0; i < 10; i++) {
  const client = await GonkaOpenAI.create({
    gonkaPrivateKey: randomBytes(32).toString('hex'),
    endpoints: [ep],
    timeout: 25000,
    maxRetries: 0,
  });
  const t0 = Date.now();
  try {
    await client.chat.completions.create({
      model: 'Qwen/Qwen3-235B-A22B-Instruct-2507-FP8',
      messages: [{ role: 'user', content: 'hi' }],
      max_tokens: 3,
    });
    console.log(i, 'OK', Date.now() - t0, 'ms');
  } catch (e) {
    console.log(i, e.status, e.message?.slice(0, 50), Date.now() - t0, 'ms');
  }
  await new Promise(r => setTimeout(r, 100));
}
```

Result on a clean local machine right now (10/10 → 429 in ~35-150 ms):

```
0  429  rate limit exceeded  191ms
1  429  rate limit exceeded   39ms
2  429  rate limit exceeded   37ms
...
9  429  rate limit exceeded   33ms
```

A signed request with the same SDK but routed via a different participant's
URL (non-TA, signed with that TA's address) returns
`403 "Transfer Agent not allowed"`, which is expected.

## Things that don't fix it from the gateway side

We tried, on top of the standard `gonka-openai` flow:

- `httpAgent: { keepAlive: false }` (no effect — SDK goes through
  `globalThis.fetch`, not node-fetch)
- `setGlobalDispatcher(new undici.Agent({ keepAliveTimeout: 1 }))` — no effect
- Adaptive retry: many cheap attempts (12-20 × 100ms pause on 429,
  500ms on timeout) — uptime stays at 0% under burst load
- Fresh `GonkaOpenAI` client per retry attempt — same
- Reducing SDK `timeout` from 25s → 8s — only changes how fast the eventual
  502 comes back, success rate stays at 0%

We also wired up `fetchNodeIdentity` (`delegate_ta`) as a safety net so
that whenever a TA starts publishing delegates, our pool auto-expands.
Right now all 7 non-TA participants we probed return `delegate_ta: null`,
so the SDK delegate path is effectively unused.

## Asks for the protocol team

1. **Is `node3`'s `/v1/chat/completions` rate-limit configured globally
   (per endpoint), per-IP, or per Gonka address?** Knowing the policy lets
   community gateways tune retry/concurrency against real numbers instead
   of guessing.
2. **Can `node1` / `node2` be brought back, or `allowed_transfer_addresses`
   expanded?** With a single live TA the entire community-gateway layer
   has a hard ceiling well below what user demand needs.
3. **Is there a roadmap for participants to start publishing `delegate_ta`
   on `/v1/identity`?** That's the cleanest fan-out story (one TA-address
   for billing, many participant URLs for actual inference) and it's
   already supported by the SDK — needs the participant side to opt in.
4. **`proxy-gonka-gg` consistently sits at >90% uptime with 1s TTFT.** Is
   there a privileged path / private endpoint there that the rest of us
   can apply for? If yes, what's the process? If no — what does it do
   differently?

## Environment

- SDK: `gonka-openai@0.2.6` (latest on npm)
- Tested from: gateway VPS (Lithuania) and a residential connection in
  Russia — same behaviour
- Date: 2026-04-26 / 2026-04-27 UTC (ongoing for ~4 days, see incident #441
  on gonka.pw which started 2026-04-23T06:56Z)
- Public gateways' uptime numbers above are from `https://gonka.pw/providers`
  pulled at the time of writing

Happy to share full request/response logs, sample failing transactions
or any benchmark scripts on request.

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-04-30 09:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @unameisfine - this is the GonkaLabs team.</p>
<p>To address your question about proxy.gonka.gg consistently sitting above 90% uptime: no, we don't have any special privileges on the network. Here's what's actually under the hood:</p>
<p>Smart TA rotation - we hop between Transfer Agents instead of pinning to a single one, so a slow or rate-limited TA never blocks the pipeline.
A small upstream wallet pool (3 wallets) - purely for distributing signing load across multiple identities. It doesn't grant any special standing on the network; any user can do the same.
Configuration tuned via an autoresearch loop - we ran a Karpathy-style trial-and-error loop on the proxy's configuration, optimizing for a single metric: percentage of successful chat completions. Once you have a clean metric, almost any system can be improved by iterating on it.
So the answer is just: aggressive tuning, nothing more. Everything is open source at https://github.com/gonkalabs/opengnk — feel free to fork it and reproduce the same results.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-05-21 21:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@unameisfine Please note that the Developer Quickstart has been significantly updated: https://gonka.ai/docs/developer/quickstart/ If you still have any questions after reviewing it, please create a new issue.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1121](https://github.com/gonka-ai/gonka/issues/1121) every hour.
