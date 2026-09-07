---
title: "#1628 — [BUG] Public routers hang/timeout on prompts ≥ ~7.5K tokens (prefill); 502 `all_providers_failed`; DeepSeek missing from /v1/models"
source: https://github.com/gonka-ai/gonka/issues/1628
issue_number: 1628
synced_at: 2026-09-07T00:01:32Z
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
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-09-06 09:40 UTC</span>
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

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a></span>
    <span class="issues-meta-item">commented 2026-08-23 17:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>It's the widely occurred bug it need attention </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/paranjko">@paranjko</a></span>
    <span class="issues-meta-item">commented 2026-08-29 21:39 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Tried several times the ping-vs-large-prefill contrast from this thread on our <a href="https://inference.dahl.global">gateway</a>: DeepSeek-V4-Flash-0731 and MiniMax-M2.7, <code>stream=true</code>, unique padding.</p>
<p>Both models: HTTP 200, first token in ~1–6s at ~12k and ~63k <code>prompt_tokens</code>. <code>max_tokens=5</code> completes as <strong>64</strong> (gateway floor). No 0-byte hang; engine not left dead.</p>
<p>A ~75k-in / 4096-out MiniMax <strong>non-stream</strong> on another path finished in ~53s (<code>outcome=served</code>) a bit slow, not stuck.</p>
<p>The <code>curl</code> in the post is the <code>ping</code>. To replay the hang, please paste the same kind of command with the large prompt (~7.5K or ~40K) that timed out for you (URL + body + <code>--max-time</code>).</p>
<p>Happy to re-run if we have that.
Gonka <a href="https://github.com/paranjko/external-test-lab">External TestLab</a></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/inecro1">@inecro1</a></span>
    <span class="issues-meta-item">commented 2026-08-30 10:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the detailed test! One clarification: our report is specifically about the <strong>public routers</strong> (<code>api.opengonka.com</code>, <code>node.gonka.lat</code>, <code>gate.joingonka.ai</code>, <code>openbroker.gonka.gg</code>) — your gateway is a separate deployment, so a clean pass there doesn't contradict the report.</p>
<p>Here's the exact repro we use (large-prefill non-stream request to <code>api.opengonka.com</code>, ~160K chars ≈ 40K tokens system prompt; redact the key):</p>
<pre><code class="language-bash">python3 - &lt;&lt;'EOF'
import json, urllib.request, time
body = json.dumps({
  &quot;model&quot;: &quot;deepseek-ai/DeepSeek-V4-Flash-0731&quot;,
  &quot;messages&quot;: [
    {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;x&quot; * 160_000},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;ok&quot;}
  ],
  &quot;max_tokens&quot;: 5,
  &quot;stream&quot;: False,
}).encode()
req = urllib.request.Request(&quot;https://api.opengonka.com/v1/chat/completions&quot;, data=body, method=&quot;POST&quot;)
req.add_header(&quot;Authorization&quot;, &quot;Bearer &lt;API_KEY&gt;&quot;)
req.add_header(&quot;Content-Type&quot;, &quot;application/json&quot;)
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=100) as r:
        print(&quot;OK&quot;, round(time.time()-t0, 1), &quot;s&quot;, r.read()[:200])
except Exception as e:
    print(type(e).__name__, round(time.time()-t0, 1), &quot;s&quot;, str(e)[:200])
EOF
</code></pre>
<p>Latest probe results against <code>api.opengonka.com</code> (2026-08-30):
- <code>GET /v1/models</code> -&gt; 200 in ~0.5s
- small prompt (~5 tokens) -&gt; 200 in 1.2-3.4s
- same large-prefill request as above -&gt; <strong>timeout after 100s, zero bytes</strong> (reproducible on every probe since 2026-08-23, latest at 13:14 today)</p>
<p>We also reproduced the failure across <code>node.gonka.lat</code>, <code>gate.joingonka.ai</code>, <code>openbroker.gonka.gg</code>, and with stream=true (first chunk never arrives). If it works on your gateway, great — the question is why the public routers still hang at the same prefill volume. Happy to run a side-by-side test against your gateway if that helps.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-09-03 22:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @inecro1 - thanks for the clarification and the exact repro.</p>
<p>There are two claims in the issue: (1) <code>/v1/models</code> is wrong, and (2) public routers hang or return <code>all_providers_failed</code> on prefill ≥ ~7.5K.</p>
<p>We operate <strong>proxy.gonka.gg</strong> and <strong>OpenBroker</strong> and response will be only around them <em>(also: we can not answer on behalf of brokers that are operating using OpenBroker as a gateway because we can not be sure on how request/response transformation flow might happen there)</em></p>
<p>After your 2026-08-30 note we re-checked both of our live paths. <strong>We do not see that hang signature.</strong></p>
<h3>proxy.gonka.gg</h3>
<p><strong>Catalog.</strong> This is the opposite of “retired Qwen listed, DeepSeek hidden.” Live <code>GET /v1/models</code> on both <code>https://api.proxy.gonka.gg/v1/models</code> and <code>https://proxy.gonka.gg/v1/models</code> returns:</p>
<ul>
<li><code>deepseek-ai/DeepSeek-V4-Flash-0731</code></li>
<li><code>MiniMaxAI/MiniMax-M2.7</code></li>
<li><code>moonshotai/Kimi-K2.6</code></li>
</ul>
<p>Qwen is not in the catalog. Old clients that still send Qwen get <strong>404 not available</strong>, not a fake “it’s up” 502.</p>
<p>Preferred base URL: <code>https://api.proxy.gonka.gg/v1</code> (<a href="https://proxy.gonka.gg/docs">docs</a>). The apex host also serves <code>/v1</code> today, but clients should follow the docs as proxy.gonka.gg/v1 is a frontend-re-resolved route, not direct production api path (it is reserved for reverse-compatibility for old clients, but it is limited according to frontend operation traffic rules).</p>
<p><strong>Large prefill /</strong> <strong><code>all_providers_failed</code></strong> <strong>all_providers_failed.</strong> We do not see “≥ ~7.5K and the engine dies / 0-byte hang” on the current proxy path. Large agent-sized prefills complete, including DeepSeek prompts well above 40K. We have <strong>zero</strong> <code>all_providers_failed</code> rows on this router.</p>
<p>What we <em>do</em> see is the other half of this thread: <strong>capacity</strong>, not a hard prefill cliff - 429 (too many concurrent), 503 (hosts / queue full), 502 (no host left / deadline). That is the #1121 / #1506 family. It is network state, not “large prompts never work,” and not broker-specific.</p>
<p>If proxy looked “partially” affected on Aug 23, that specific 0-byte / <code>all_providers_failed</code> prefill cliff is <strong>not</strong> <strong>what we see on the current path now</strong>.</p>
<h3>OpenBroker</h3>
<p><strong><code>/v1/models</code></strong> <strong>/v1/models.</strong> Your original table already has this right: <code>https://openbroker.gonka.gg/v1</code> → <strong>404</strong>. That host is the website, not the API.</p>
<p>The API is <code>https://api.openbroker.gonka.gg/v1</code>. <code>GET /v1/models</code> returns the same three live models (no Qwen). It is documented at <a href="https://openbroker.gonka.gg/docs">openbroker.gonka.gg/docs</a> (<code>GET /models</code>) and only this api path shall be used.</p>
<p><strong>Large prefill.</strong> We ran <strong>your exact script</strong> (DeepSeek, <code>"x" * 160_000</code>, <code>max_tokens=5</code>, 100s timeout) against <code>https://api.openbroker.gonka.gg</code> at <strong>2026-09-03 22:27 UTC</strong>:</p>
<table>
<thead>
<tr>
<th>Probe</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>small prompt</td>
<td><strong>200</strong> in 0.3s</td>
</tr>
<tr>
<td>your large non-stream body</td>
<td><strong>200</strong> in 0.9s (~20k prompt tokens - repeated <code>x</code> compresses; not ~40k)</td>
</tr>
<tr>
<td>same body, <code>stream=true</code></td>
<td><strong>200</strong> in 1.8s, first chunk arrived</td>
</tr>
<tr>
<td>same calls on <code>openbroker.gonka.gg</code></td>
<td><strong>404</strong> immediately (website / frontend resolved path and it is expected. Api path is api.openbroker.gonka.gg as per the docs).</td>
</tr>
</tbody>
</table>
<p>Last 24h on OpenBroker: <strong>130k+</strong> requests with prompt ≥ 7.5K and <strong>14.5k+</strong> with ≥ 40K, all HTTP <strong>200</strong>. Max logged prompt <strong>~227K</strong>. <strong>Zero</strong> <code>all_providers_failed</code> (that error is from other routers). We do not force <code>logprobs</code> on chat.</p>
<p>Failed rows often have <code>prompt_tokens=0</code>, so a true silent hang would not land in the ≥7.5K bucket. What we can say is: agent-sized prefills are completing here <strong>now</strong>, and the OpenBroker line in the issue is mostly the website host 404 / wrong base URL, not the 0-byte hang.</p>
<p>Our 502s here are mostly client cancel (if code that calls our api from client side does have a very short timeout value) and “no host left” (capacity), not a prefill OOM.</p>
<p>If you still see a hang, please re-run that script against <code>https://api.openbroker.gonka.gg/v1/chat/completions</code> and <code>https://api.proxy.gonka.gg/v1/chat/completions</code>, and send UTC time + <code>x-request-id</code>. Happy to do a side-by-side (same applied for proxy.gonka.gg issues with correct api.proxy.gonka.gg path as per docs).</p>
<p><em>Thank You for the report,</em></p>
<p><strong>Gonka Labs team</strong></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/inecro1">@inecro1</a></span>
    <span class="issues-meta-item">commented 2026-09-06 09:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @gonkalabs — follow-up from our side after your 2026-09-03 reply. We ran a side-by-side probe on 2026-09-06 09:14 UTC (same key, same model <code>deepseek-ai/DeepSeek-V4-Flash-0731</code>, <code>stream=true</code>/<code>false</code> as applicable) against all three paths.</p>
<h3>api.opengonka.com/v1 (the router our key is issued for)</h3>
<ul>
<li><code>GET /v1/models</code> -&gt; <strong>200</strong> (~0.6s). Catalog now: <code>MiniMaxAI/MiniMax-M2.7</code>, <code>deepseek-ai/DeepSeek-V4-Flash-0731</code>, <code>moonshotai/Kimi-K2.6</code>, <code>zai-org/GLM-5.2-FP8</code>. Qwen is gone and DeepSeek is listed — the catalog part of the issue appears resolved on this router. ✅</li>
<li>small prompt (stream) -&gt; <strong>200</strong> in 2.2s</li>
<li>~7.7K prefill (stream) -&gt; <strong>timeout after 60s, zero bytes</strong> (no <code>x-request-id</code> in headers — they never arrived)</li>
<li>~40K prefill (<code>"x"*160_000</code> system, non-stream, <code>max_tokens=5</code>, your exact repro) -&gt; <strong>timeout after 110s</strong> (<code>read operation timed out</code>)</li>
<li>~40K prefill (stream) -&gt; <strong>timeout after 110s</strong></li>
</ul>
<p>So the ≥~7.5K prefill hang is still 100% reproducible on <code>api.opengonka.com</code> as of today.</p>
<h3>api.proxy.gonka.gg/v1 and api.openbroker.gonka.gg/v1 (your paths)</h3>
<ul>
<li><code>GET /v1/models</code> -&gt; <strong>200</strong> on both (~0.4s; catalog on both: DeepSeek-V4-Flash-0731 + MiniMax-M2.7)</li>
<li>chat/completions with our opengonka-issued <code>gnk-sk-…</code> key -&gt; <strong>401 Unauthorized</strong> (~0.2s) — the key is not accepted on your paths</li>
<li>~7.7K and ~40K prefills with the same key -&gt; <strong>do NOT return 401 quickly</strong>: they hang 60–110s (<code>read</code>/<code>write operation timed out</code>) before any auth response</li>
</ul>
<h3>What this means / request</h3>
<p>We cannot verify your "no hang on our paths" claim from this account: the routers use separate billing/key systems, and our key gets 401 on <code>proxy.gonka.gg</code> / <code>OpenBroker</code>. Two questions:
1. Where do we obtain a key for <code>api.proxy.gonka.gg</code> / <code>api.openbroker.gonka.gg</code> (registration hub / docs page)? We'd like to run the exact repro with valid auth on your paths and close this out.
2. Is the pre-auth hang on large bodies (60–110s instead of a fast 401) expected behavior on your gateways — i.e. is the full request body read/processed before authentication? If so, that still looks like a prefill-path problem worth a look.</p>
<p>Happy to provide UTC times and full request bodies for any specific run you want to inspect.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1628](https://github.com/gonka-ai/gonka/issues/1628) every hour.
