---
title: "#1632 — OpenBroker strips provider prompt-cache metadata (prompt_tokens_details is always null)"
source: https://github.com/gonka-ai/gonka/issues/1632
issue_number: 1632
synced_at: 2026-08-25T08:02:08Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    OpenBroker strips provider prompt-cache metadata (prompt_tokens_details is always null)
    <span class="issues-number">#1632</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a> opened 2026-08-24 06:38 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-24 06:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
# OpenBroker strips provider prompt-cache metadata (`prompt_tokens_details` is always `null`)

## Summary

OpenBroker performs prompt/prefix caching — latency collapses from 12–31 s on a cold 52k-token prompt to ~5 s on a changed-suffix reuse and 23–41 ms on a byte-identical replay — but every `/v1/chat/completions` response returns `"prompt_tokens_details": null`. The gateway normalizes away the underlying provider's cache token counts, making prefix caching invisible and unbillable to downstream consumers.

## Motivation

DeepSeek's API reports cache-served tokens (`prompt_cache_hit_tokens`) and prices cached input ~90% cheaper than fresh input — that discount is the core economics of reselling `deepseek-ai/DeepSeek-V4-Flash-0731`. Because OpenBroker strips the metadata, downstream OpenAI-compatible gateways cannot apply cached-input billing and cannot audit cache reuse. This blocks a real, measurable cost optimization for every API consumer and forces either overcharging (bill all as fresh) or undercharging (bill all as cached).

## Impact

- Who is affected (hosts, developers, validators): all developers and gateway operators using the OpenBroker API; downstream billing/analytics systems; hosts paying for cold inference when prefix reuse is not credited.
- Is effect network-wide or limited: **network-wide** — every response from the gateway carries no cache metadata, regardless of model or node.
- Likelihood: **common** — observed on 100% of requests across multiple runs and models (cold, changed-suffix, and exact-replay responses all return `null`).
- Severity [Impact x Likelihood]: **Medium** — high impact (billing correctness + pricing feasibility) x common likelihood, but no data loss or service failure.
- Affected components: OpenBroker gateway response normalization (`usage` object on `POST /v1/chat/completions`); upstream provider telemetry passthrough.

## Detailed description

Reproduce with a 3-request sequence against `https://api.openbroker.gonka.gg/v1/chat/completions` (model `deepseek-ai/DeepSeek-V4-Flash-0731`, a fixed 2,000-line system prefix ~52k prompt tokens, `max_tokens: 16`, `temperature: 0`):

1. **REQ 1 — cold prefix** (suffix A)
2. **REQ 2 — same prefix, changed suffix** (suffix B)
3. **REQ 3 — byte-identical replay of REQ 2** (suffix B again)

### Evidence — latency and cache metadata per run (direct to api.openbroker.gonka.gg, 2026-08-24)

| Run | REQ 1 — cold prefix | REQ 2 — changed suffix | REQ 3 — exact replay | `prompt_tokens_details` |
|---|---|---|---|---|
| Run 1 | 200 · 13,028 ms | 200 · 5,231 ms | 200 · 41 ms | `null` |
| Run 2 | 200 · 11,996 ms | 429 (rate limited) | 429 (rate limited) | `null` |
| Run 3 | 200 · 31,196 ms | 200 · 5,054 ms | 200 · 23 ms | `null` |

Request IDs (sample): `req-1787552573073481834-7795508`, `req-1787552586020653004-2215078`, `req-1787552591250553152-2215178`.

### Evidence — response usage object (identical shape on all requests)

| Field | Value |
|---|---|
| `prompt_tokens` | 52,027 |
| `completion_tokens` | 16 |
| `total_tokens` | 52,043 |
| `prompt_tokens_details` | `null` |

The latency signature proves caching is active (cold 12–31 s → changed-suffix ~5 s → replay tens of ms), yet no response carries the cached-token count.

Requested behavior — pass through the provider's cache metadata, e.g.:

```json
"usage": {
  "prompt_tokens": 52027,
  "prompt_tokens_details": { "cached_tokens": 48003, "uncached_tokens": 4024 }
}
```

and/or `usage.prompt_cache_hit_tokens`, and optionally `x-openbroker-prefix-cache: hit|miss` + `x-openbroker-cached-tokens: N` response headers.

Links to evidence: full dual-side test results are available on request; measurements taken on 2026-08-24 from an external host.
</div>

---

> 🔄 **Auto-synced** from [Issue #1632](https://github.com/gonka-ai/gonka/issues/1632) every hour.
