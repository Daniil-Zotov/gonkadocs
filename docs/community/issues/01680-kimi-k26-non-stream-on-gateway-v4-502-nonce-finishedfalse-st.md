---
title: "#1680 — Kimi-K2.6 non-stream on gateway v4: 502 nonce_finished=false (stream OK)"
source: https://github.com/gonka-ai/gonka/issues/1680
issue_number: 1680
synced_at: 2026-09-04T20:50:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Kimi-K2.6 non-stream on gateway v4: 502 nonce_finished=false (stream OK)
    <span class="issues-number">#1680</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/paranjko">@paranjko</a> opened 2026-08-30 19:49 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-02 02:21 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
We ran into a Kimi-K2.6 issue on **gateway v4** (`mainnet-v0.2.15-v4`) and wanted to flag it.

**What we see.** `stream=true` is fine. `stream=false` with a tiny `max_tokens` (64) often returns JSON. Same prompt with `max_tokens` 256 / 1024 / 4096 comes back **502** after ~30–75s:

`inference: winner inference incomplete (nonce_finished=false)`

From the client it looks like a hang (no body until the 502). On the gateway the attempt already has a lot of upstream bytes (`aggregate_bytes` in the 100k+ range), then the request is failed with `winner_failed_after_content` / `race_completed winner=true finished=false content_source=delta.reasoning`.

**v3.** Same bodies, same night, **gateway v3** (`mainnet-v0.2.13-v3-post2`, `/devshard/v3`): all those non-stream cases return **200 JSON**. MiniMax-M2.7 non-stream on the same v4 is also 200. So this looks like a **v4 regression** on Kimi non-stream, not “Kimi hosts are down” and not “non-stream is dead on the gateway”.

**How we tested.** `POST /v1/chat/completions` straight at the gateway (not through a broker proxy). Unique `marker=` in the user text so the cache cannot hit. `temperature=0`. No host pin, no redundancy settings changed for the probes.

| # | model | stream | max_tokens | prompt | v3 | v4 |
|---|---|---|---:|---|---|---|
| 1 | Kimi-K2.6 | true | 64 | “Reply with exactly OK” | 200 SSE | 200 SSE |
| 2 | Kimi-K2.6 | false | 64 | same | 200 JSON | 200 JSON |
| 3 | Kimi-K2.6 | true | 1024 | same | 200 SSE | 200 SSE |
| 4 | Kimi-K2.6 | false | 1024 | same | **200 JSON** | **502** `nonce_finished=false` |
| 5 | Kimi-K2.6 | true | 256 | ~3 sentences | 200 SSE | 200 SSE |
| 6 | Kimi-K2.6 | false | 256 | same | **200 JSON** | **502** same |
| 7 | Kimi-K2.6 | false | 4096 | “Reply with exactly OK” | **200 JSON** | **502** same |
| 8 | MiniMax-M2.7 | false | 64 | short | — | 200 JSON |

**Repro**

```bash
curl -sS -m 120 "$GATEWAY/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "moonshotai/Kimi-K2.6",
    "messages": [{"role": "user", "content": "Reply with exactly OK. marker='"$RANDOM"'"}],
    "max_tokens": 1024,
    "temperature": 0,
    "stream": false
  }'
```

Same payload with `"stream": true` succeeds. On the v4 log, grep `request=` from `gateway_request_received` — for the failing case you should see `gateway_cache_miss stream=false` → `stream_forwarding_started` → `send_completed` with many chunks → `winner_failed_after_content` / `nonce_finished=false`.

[Gonka External TestLab](https://github.com/paranjko/external-test-lab)


</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-08-30 20:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Temporary fix is to disable force streaming:</p>
<pre><code class="language-sh">curl -N http://127.0.0.1:18080/v1/admin/settings \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;Authorization: Bearer $DEVSHARD_ADMIN_API_KEY&quot; \
  -d '{&quot;redundancy&quot;:{&quot;force_upstream_streaming&quot;:false}}'
</code></pre>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/paranjko">@paranjko</a></span>
    <span class="issues-meta-item">commented 2026-08-30 23:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Retested on mainnet-v0.2.15-v4.0.1. Same Kimi non-stream max_tokens=1024 case now returns 200 JSON. Stream still OK. 
Great work @qdanik !</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-09-02 02:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>fixed and merged into gateway-v4 branch</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1680](https://github.com/gonka-ai/gonka/issues/1680) every hour.
