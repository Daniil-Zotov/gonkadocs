---
title: "#1628 — [BUG] Public routers hang/timeout on prompts ≥ ~7.5K tokens (prefill); 502 `all_providers_failed`; DeepSeek missing from /v1/models"
source: https://github.com/gonka-ai/gonka/issues/1628
issue_number: 1628
synced_at: 2026-08-25T22:48:32Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Public routers hang/timeout on prompts ≥ ~7.5K tokens (prefill); 502 `all_providers_failed`; DeepSeek missing from /v1/models
    <span class="issues-number">#1628</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/inecro1">@inecro1</a> opened 2026-08-23 12:28 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-23 17:02 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Public Gonka routers hang or fail on any request whose total prefill is ≥ ~7.5K tokens: tested 2026-08-23 across `api.opengonka.com`, `node.gonka.lat`, `gate.joingonka.ai`, `openbroker.gonka.gg` (and partially `proxy.gonka.gg`). Small prompts (5 tokens) return HTTP 200 in ~1 s; prompts at ~40K tokens hang >90 s with zero bytes, or fail immediately with HTTP 500/502 (`all_providers_failed`). The same failure reproduces when the same total volume is split across 10 messages — it is a prefill-volume problem, not a single-message size/format problem. Separately, the `/v1/models` catalog is inaccurate: active `deepseek-ai/DeepSeek-V4-Flash-0731` answers direct requests but is absent from the catalog, while retired `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` is listed and always fails.

## Motivation

The network advertises 200K–400K context models (DeepSeek-V4-Flash-0731: 380–400K per node-config, proposal 94). LLM agents (e.g. Hermes Agent, which is in the official compatibility matrix in `docs/chat-api/agents.md`) routinely send system prompts of tens of thousands of tokens. At the current prefill threshold the network is unusable for its advertised primary use case (agent workloads), not just for adversarial large inputs. The catalog inaccuracy compounds this by making the active PoC model unselectable from web UIs while retired models mislead clients into guaranteed failures.

## Impact

- Who is affected (hosts, developers, validators):
  - **End users / developers** via public routers (`api.opengonka.com`, `node.gonka.lat`, `gate.joingonka.ai`, `openbroker.gonka.gg`, `proxy.gonka.gg`): any agent/RAG client with a large system prompt cannot complete a single request.
  - **Gateway operators**: repeated `all_providers_failed` paths trigger mass host quarantine cycles (see #1506), degrading health scoring for honest hosts.
  - **Web chat users**: 502/429/402 storms on simple questions (observed on opengonka web chat and browser/network logs).
- Is effect network-wide or limited: **Network-wide pattern** — reproduced independently on 4 public routers (including the official `gate.joingonka.ai`), not a single-host fault. Matches documented vLLM OOM behavior (#1171) rather than one operator's config.
- Likelihood (common, intermittent, edge case, or intentional attack): **Common** — deterministic at ≥ ~7.5K prefill tokens on the tested routers; not an edge case.
- Severity [Impact x Likelihood]: **High** — common × network-wide impact for the advertised agent/developer use case (see risk matrix in FAQ).
- Affected components: public gateway/router layer (proxy → gateway → mlnode/vLLM prefill), `/v1/models` catalog serving, gateway host-health/quarantine logic (#1506 interplay).

## Detailed description

### Reproduction (all tests 2026-08-23)

Environment: OpenAI-compatible client (curl and Hermes Agent `custom_providers` + `model_aliases`, `api_mode: openai`); API key issued by opengonka.com (`gnk-sk-…`); account balance sufficient (10M test tokens + 77 GNK — failures are NOT client billing).

Small prompt — works, ~1 s:

```bash
curl -N -sS https://api.opengonka.com/v1/chat/completions \
  -H "Authorization: Bearer $GONKA_ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-ai/DeepSeek-V4-Flash-0731","messages":[{"role":"user","content":"ping"}],"max_tokens":5,"stream":true}'
# → HTTP 200, first token < 2 s
```

Large prompt (~40K tokens) — fails on every router:

| Router | Result |
|---|---|
| `https://api.opengonka.com/v1` | timeout >90 s, 0 bytes (client `--max-time 90` aborted) |
| `https://node.gonka.lat/v1` | HTTP 502 `{"error":{"message":"All providers failed to respond","type":"upstream_error","code":"all_providers_failed"}}` |
| `https://gate.joingonka.ai/v1` | write timeout (client-side, stream never opened) |
| `https://openbroker.gonka.gg/v1` | 404 on `/v1/models` (broker path unavailable) |

Chunking does not help: the same ~40K token total split into 10 messages still hangs (>90 s, 0 bytes). The trigger is total prefill volume, not single-message size or message format.

Threshold: failure is deterministic at ~7.5K prefill tokens and above. This is consistent with the documented vLLM v1 OOM at ~6K+ tokens with forced logprobs (issue #1171: EngineDeadError → HTTP 500, engine down 6–12 min) and with the gateway forcing `logprobs=true, top_logprobs=5, return_token_ids=true` for observability (`docs/chat-api/README.md`).

### Catalog inaccuracy

- `GET /v1/models` (api.opengonka.com, node.gonka.lat, gate.joingonka.ai): `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` (retired by proposal 78) is listed; every request to it returns `502 all_providers_failed`.
- `deepseek-ai/DeepSeek-V4-Flash-0731` (active PoC model, epoch 360, proposal 94) answers direct requests with HTTP 200 but is **absent** from `/v1/models` — web UIs cannot select it.

### Notes on evidence and logs

- Server-side router/gateway logs are not accessible to the client; the client-side evidence is exact HTTP codes, timing, and request behavior above. We can provide `x-request-id` values from `api.opengonka.com` responses on request (the router returns `x-request-id` and `X-Provider` headers on every response).
- Prompt caching is NOT available: `cache_key` / `prompt_cache_key` are silently stripped by the gateway (docs/chat-api troubleshooting), so every large request is a cold prefill.
- Related open issues: #1171 (vLLM OOM on ~6K+ prompts), #1550 (DRAFT session affinity / KV-cache reuse), #1591 (request continues after client timeout), #1506 (mass quarantine → no winners), #1121 (429 storms, p50 TTFT 19.7 s on gate.joingonka.ai), #1579/#1574 (always-stream upstream), #424 (reliability math).

### Suggested actions

1. Publish an accurate `/v1/models`: remove retired `Qwen3-235B`, add active `deepseek-ai/DeepSeek-V4-Flash-0731` (and any other active models).
2. Fix prefill/OOM on long prompts: memory handling in mlnode/vLLM, stop forcing logprobs on every request, KV-cache reuse (see #1550).
3. Make gateway timeouts surface server-side errors instead of silent 0-byte hangs or `all_providers_failed` (correlate with #1591/#1593).
4. Stabilize public routers against 429/502 storms (#1121, #1506).
5. Consider surfacing real-time router health (gonka.pw-style) in the official quickstart so users can pick a healthy gateway.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a></span>
    <span class="issues-meta-item">commented 2026-08-23 17:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>It's the widely occurred bug it need attention </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1628](https://github.com/gonka-ai/gonka/issues/1628) every hour.
