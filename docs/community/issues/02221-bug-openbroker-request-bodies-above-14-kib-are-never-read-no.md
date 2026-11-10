---
title: "#2221 — [BUG] OpenBroker: request bodies above ~14 KiB are never read — no response, no error"
source: https://github.com/gonka-ai/gonka/issues/2221
issue_number: 2221
synced_at: 2026-11-10T02:16:20Z
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
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-05 22:32 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-11-05 22:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hello, @ludmilavasilievna3-cmd </p>
<p>We could not reproduce a body-size cutoff on <code>POST https://api.openbroker.gonka.gg/v1/chat/completions</code>.</p>
<p>There is no ~14 KB read limit. The same request shape from the report (<code>zai-org/GLM-5.3-Flash</code>, <code>max_tokens</code> 8, one user message padded with <code>x</code>, 20 s client timeout) was sent at the two exact sizes, over both HTTP/2 and HTTP/1.1.</p>
<p>With an invalid key (<code>Bearer sk-invalid-test</code>):</p>
<table>
<thead>
<tr>
<th>Body</th>
<th>Result</th>
<th>Time</th>
<th>Bytes uploaded</th>
</tr>
</thead>
<tbody>
<tr>
<td>14008</td>
<td>401</td>
<td>0.21–0.29 s</td>
<td>14008</td>
</tr>
<tr>
<td>14408</td>
<td>401</td>
<td>0.24–0.31 s</td>
<td>14408</td>
</tr>
</tbody>
</table>
<p>The 401 is the bad key. It is returned before the body is used. Curl did not time out, and the full body was uploaded.</p>
<p>With a valid OpenBroker key, same model and <code>max_tokens</code> 8:</p>
<table>
<thead>
<tr>
<th>Body</th>
<th>Result</th>
<th>Time</th>
<th>Bytes uploaded</th>
</tr>
</thead>
<tbody>
<tr>
<td>14008</td>
<td>200</td>
<td>1.5 s</td>
<td>14008</td>
</tr>
<tr>
<td>14408</td>
<td>200</td>
<td>9.8 s</td>
<td>14408</td>
</tr>
<tr>
<td>80008</td>
<td>200</td>
<td>2.4 s</td>
<td>80008</td>
</tr>
<tr>
<td>200008</td>
<td>200</td>
<td>3.5 s</td>
<td>200008</td>
</tr>
</tbody>
</table>
<p>Each 200 was a real completion (<code>finish_reason: length</code>). <code>POST /health</code> with an 18 KB body returns 405 in about 0.3 s. Nothing in this range is dropped, and a request rejected for a bad key is not billed.</p>
<p>If you still see <code>curl (28)</code> only above ~14 KB, that is on the client-code side of the connection. A proxy that keeps uploading after the server has already answered, and does not read the response until the upload finishes, will block once its buffer fills and then report a timeout with no body. From this API those sizes get a normal status line.</p>
<p>Also, we attached the test script that can be ran with a valid OBK api key.
<code>OPENBROKER_API_KEY='obk-...' python3 openbroker_body_size_check.py</code></p>
<p>Test report:</p>
<pre><code>&gt; POST https://api.openbroker.gonka.gg/v1/chat/completions
&gt; timeout 20 s
&gt; ok    invalid 14008 h2              http 401      0.012130s  uploaded 14008    source openbroker    expect 401
&gt; ok    invalid 14008 h1              http 401      0.009832s  uploaded 14008    source openbroker    expect 401
&gt; ok    invalid 14408 h2              http 401      0.010042s  uploaded 14408    source openbroker    expect 401
&gt; ok    invalid 14408 h1              http 401      0.010590s  uploaded 14408    source openbroker    expect 401
&gt; ok    extra /health 18000           http 405      0.010419s  uploaded 18000    source -             expect 405
&gt; ok    extra /v1/models 18000        http 405      0.017727s  uploaded 18000    source -             expect 405
&gt; ok    extra /v1/nonexistent 18000   http 405      0.014436s  uploaded 18000    source -             expect 405
&gt; valid key prefix obk-c030b3c378
&gt; ok    valid 14008 h2                http 200      1.228530s  uploaded 14008    source -             expect 200
&gt; ok    valid 14408 h2                http 200      0.105048s  uploaded 14408    source -             expect 200
&gt; ok    valid 80008 h2                http 200      0.149533s  uploaded 80008    source -             expect 200
&gt; ok    valid 200008 h2               http 200      19.904983s  uploaded 200008   source -             expect 200
&gt; pass
</code></pre>
<p>The 200008 byte completion finished in 19.9 seconds, just inside the 20 second limit, and still returned 200.</p>
<p>Looking forward to investigate further if the issue is not cleared,
Gonka Labs team.</p>
<p><a href="https://github.com/user-attachments/files/34451284/openbroker_body_size_check.py">openbroker_body_size_check.py</a></p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2221](https://github.com/gonka-ai/gonka/issues/2221) every hour.
