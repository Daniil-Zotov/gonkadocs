---
title: "#2221 — [BUG] OpenBroker: request bodies above ~14 KiB are never read — no response, no error"
source: https://github.com/gonka-ai/gonka/issues/2221
issue_number: 2221
synced_at: 2026-11-05T18:49:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] OpenBroker: request bodies above ~14 KiB are never read — no response, no error
    <span class="issues-number">#2221</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/ludmilavasilievna3-cmd">@ludmilavasilievna3-cmd</a> opened 2026-11-05 16:05 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-05 16:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
`api.openbroker.gonka.gg` stops consuming the request body at roughly 14 KiB. Above that size the connection goes silent — no 413, no 400, no error body — and the client waits until its own timeout fires; below it the same endpoint answers in 0.2–0.3 s. The threshold is identical with a valid and with an invalid API key, so it is request intake, not inference or authentication.

## Motivation
Any tool-using client sends a prompt far above the cutoff, so the three models served by OpenBroker are effectively unreachable for real work: a normal Claude Code request (system prompt + tool definitions) is 30–200 KB. Small pings succeed, which hides the problem — the endpoint looks alive while every real request dies. The same symptom was already reported in discussion 1363 (2026-07) as "1780+ tokens hangs forever" and has no answer, so a reproducible measurement is needed to settle whether the cause is size in bytes, prompt tokens, or something else.

## Impact
- Who is affected: brokers and gateways that call the OpenBroker endpoint, and developers building agent/CLI clients against it. Validators and hosts are not affected.
- Scope: limited to the OpenBroker edge in front of 142.132.231.149. Direct network access and self-hosted gateways are unaffected — the same 80 KB payload to a different upstream returned 200 in 3.4 s.
- Likelihood: deterministic, not intermittent. Every request above ~14 KiB fails; below it, requests succeed reliably.
- Affected components: the OpenBroker request-intake/proxy layer. Not the models, not the devshard, not the chain.

## Detailed description

Reproduction (same model, same key, only body size differs):

1. Build two requests to `POST https://api.openbroker.gonka.gg/v1/chat/completions`, model `zai-org/GLM-5.3-Flash`, `max_tokens` 8, one user message padded with "x" so the JSON body is 14008 bytes, then 14408 bytes.
2. Send both with a 20 s client timeout.
3. 14008 bytes returns `401` (or `200` with a valid key) in ~0.3 s. 14408 bytes returns nothing — curl reports `(28) Operation timed out after 20s`.

Measured threshold: 13208 B → 401 in 0.28 s; 14008 B → 401 in 0.28 s (stable across repeats); 14408 B → stalls; 18711 B → stalls; 25000 B → stalls. Repeating the two boundary cases with `Bearer sk-invalid-test` gives the same split, so neither the key nor the model is involved.

It is the read side, not the completions handler:
- `POST /v1/nonexistent` with an 18 KB body → `405` in 0.23 s; the route rejects before reading, so it answers.
- `POST /health`, `/v1/models`, `/v1/chat/completions` with 18 KB → stall.
- `Expect: 100-continue` → server sends `100 Continue`, then stalls.
- `Transfer-Encoding: chunked`, no `Content-Length`, 20 KB → stalls. So it is not a `Content-Length` check and not a 413 policy.

Ruled out on our side: `ping 142.132.231.149` 57 ms avg with 0 % loss; TLS handshake 0.26 s; `GET /v1/models` 200 in 0.37 s; our gateway's nginx error log for the failing calls reads `upstream prematurely closed connection while reading response header from upstream` against `https://142.132.231.149:443/v1/chat/completions`, followed by 502 after 15.188 s; the same 80 KB payload to our own inference node returns 200 in 3.4 s.

Client-side consequence: the failure carries no error body, so callers can only report "timed out", and it is impossible to tell whether the hung request was billed — the open question from discussion 1363.

Evidence links:
- Discussion 1363 — OpenBroker announcement, with the earlier "1780+ tokens hangs" report: https://github.com/gonka-ai/gonka/discussions/1363
- OpenBroker knowledge base: https://openbroker.gonka.gg/docs

Request: confirm whether a ~14 KiB body limit or read buffer is intentional; if so, return 413 and document it; if not, the edge in front of 142.132.231.149 appears to stop draining the request body.

</div>

---

> 🔄 **Auto-synced** from [Issue #2221](https://github.com/gonka-ai/gonka/issues/2221) every hour.
