---
title: "#876 — Signed /v1/chat/completions still panics on all three documented mainnet transfer-agent endpoints"
source: https://github.com/gonka-ai/gonka/issues/876
issue_number: 876
synced_at: 2026-08-09T04:41:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Signed /v1/chat/completions still panics on all three documented mainnet transfer-agent endpoints
    <span class="issues-number">#876</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/junior2wnw">@junior2wnw</a> opened 2026-03-10 20:30 UTC</span>
    <span class="issues-meta-item">13 comments</span>
    <span class="issues-meta-item">Updated 2026-06-03 06:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Around **2026-03-10 20:28 UTC**, I followed the public Developer Quickstart flow on mainnet using a funded account and observed that inference requests signed using the public Gonka SDK semantics failed on **all three documented active transfer-agent endpoints** with the same internal server panic.

I then checked whether a practical public fallback existed and did not find a usable one during the same test window.

This report makes a narrow claim:

- I am **not** claiming global network unavailability.
- I am **not** claiming that every possible internal or private route was unavailable.
- I am **not** claiming that the participant prerequisite is necessarily a protocol bug by itself.

The narrower claim is:

> For an external developer following the publicly documented inference flow, the same internal server failure was reproducible on all three documented active transfer-agent endpoints, and no usable public fallback was found during the same test window.

## Related context

This appears externally similar to **#499** (`Chat Completions aren't working`), which was closed by **#643** (`fix: guard nil participants in executor selection`).

Because the current public symptom is still reproducible on the documented mainnet endpoints, I cannot tell from the outside whether this is:

- a regression of the nil-participant path addressed in `#643`,
- a different nil/empty-path bug with the same public symptom,
- or a deployment/version mismatch where the documented public transfer agents are not all running the code expected after `#643`.

I am intentionally **not** claiming which of those is true. I am only claiming that the documented public mainnet developer path still reproduces the same failure pattern.

## Documented endpoints tested

Per the public Developer Quickstart, the documented active transfer-agent endpoints are:

- `http://node1.gonka.ai:8000/v1/chat/completions`
- `http://node2.gonka.ai:8000/v1/chat/completions`
- `https://node3.gonka.ai/v1/chat/completions`

Additional fallback-related surfaces checked during the same window:

- `https://node4.gonka.ai`
- non-allowlisted participant endpoints discovered from active participant data

## Reproduction matrix

| Endpoint | Request | Result |
|---|---|---|
| `node1.gonka.ai` | signed `POST /v1/chat/completions` | `500` -> `runtime error: invalid memory address or nil pointer dereference: panic` |
| `node2.gonka.ai` | signed `POST /v1/chat/completions` | `500` -> `runtime error: invalid memory address or nil pointer dereference: panic` |
| `node3.gonka.ai` | signed `POST /v1/chat/completions` | `500` -> `runtime error: invalid memory address or nil pointer dereference: panic` |
| `node4.gonka.ai` | fallback check | `502 Bad Gateway` or timeout |
| non-allowlisted participant endpoints | signed inference request | `403` -> `Transfer Agent not allowed` |

## Steps to reproduce

1. Use a funded Gonka mainnet account.
2. Build a standard OpenAI-compatible `POST /v1/chat/completions` request.
3. Sign the request using the public Gonka SDK semantics.
4. Send the signed request to each documented active transfer-agent endpoint:
   - `http://node1.gonka.ai:8000/v1/chat/completions`
   - `http://node2.gonka.ai:8000/v1/chat/completions`
   - `https://node3.gonka.ai/v1/chat/completions`
5. Observe the response.

## Expected result

A normal inference response, or at minimum a structured application-level error without a server panic.

## Actual result

All three documented active transfer-agent endpoints returned the same internal panic:

```text
rpc error: code = Unknown desc = runtime error: invalid memory address or nil pointer dereference: panic
```

## Controls performed

To reduce the chance of a client-side false positive, I also checked the following:

- unsigned `POST /v1/chat/completions` requests returned `401 Authorization is required`
- signed requests progressed past the unauthenticated stage and then failed with `500`
- `GET /v1/identity` was reachable on the documented nodes
- `GET /v1/models` was reachable
- chain status endpoints were reachable
- the test account existed on mainnet and was funded
- the signing flow was implemented to match the public Gonka SDK semantics

These controls do not prove that every aspect of the request was perfect, but they strongly suggest that this was not just a dead route or a missing-auth condition.

## Impact during testing

From the perspective of an external developer following the documented public flow, this presented as an effective outage during the tested window:

- all three documented active transfer-agent endpoints returned the same internal panic on signed inference requests
- no usable public fallback was found during the same test window
- ordinary participant nodes did not serve as fallback because they returned `403 Transfer Agent not allowed`

## Additional note: chain-level path appears unavailable to funded non-Participant accounts

After the HTTP inference path failed, I checked whether the chain-level inference path could serve as fallback.

What I found:

- the funded account used for testing existed as a normal account and had balance
- that account did not resolve as a `Participant`
- in the `StartInference` path, `requested_by` appears to be resolved through participant lookup

This is also a narrow claim:

> The chain-level path appears unavailable to accounts that are funded but not already present as `Participant` records, and this prerequisite does not appear to be clearly disclosed in the Developer Quickstart.

I am not presenting that point as a standalone protocol flaw. I am including it because it materially limited recovery options for the documented developer flow during testing.

## Code pointers worth checking

The goal of this section is to reduce investigation time, not to overclaim the exact root cause.

Potentially relevant areas:

- `inference-chain/x/inference/epochgroup/random.go`
  - `#643` added nil-member sanitization in executor selection.
- `inference-chain/x/inference/keeper/query_get_random_executor.go`
  - current executor selection path on the chain side.
- `decentralized-api/internal/server/public/post_chat_handler.go`
  - transfer request validation, requester lookup, executor selection, and forwarding.
- `decentralized-api/internal/server/public/post_chat_handler_test.go`
  - natural place for a signed request regression test.
- `decentralized-api/internal/server/public/server.go`
  - public API server setup; this appears to have no `echo` recover middleware, so any remaining panic path becomes a public-facing failure mode.

## Suggested minimal fix path

I do not want to overstate root cause without internal logs, so this is intentionally framed as a minimal hardening / validation path rather than a claim about the exact panic site.

1. **Verify that the documented public transfer-agent deployment actually includes the `#643` nil-guard path (or equivalent).**
   - If the current deployment does not, this may be a deployment/version mismatch rather than a fresh logic bug.

2. **Add a regression test for signed `POST /v1/chat/completions` on the documented public handler path.**
   - The key assertion should be: this path must not produce a panic-shaped failure.
   - If an internal dependency returns an invalid or empty result, the handler should return a structured HTTP error.

3. **Add explicit nil/empty guards at the public inference boundary where missing chain/query results can still leak into handler logic.**
   - In particular around requester lookup, executor selection, and forwarding.

4. **Optionally add recover middleware on the public API server as defense-in-depth.**
   - This is not a substitute for fixing the panic source.
   - It would still reduce blast radius for any remaining panic path.

5. **If `requested_by` must already exist as a `Participant`, document that explicitly in the Developer Quickstart.**
   - If that is not intended, the chain-level path should fail earlier and more clearly, or the prerequisite should be relaxed.

## Why this report should be easy to validate

I can provide privately if needed:

- exact UTC timestamps
- sanitized request bodies
- signed header set
- exact response bodies
- minimal reproduction script
- fallback-check requests and results
- the specific participant / transfer-agent queries used during testing

If useful, I can also retest against a patched environment and confirm whether the issue is resolved.

## Reporter details

GitHub: `@junior2wnw`
Wallet (if bounty attribution is relevant): `gonka1glph4syjlx347ptv2n7qfz67sryrhk983j5f8a`
</div>

---

## 💬 Comments (13)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/junior2wnw">@junior2wnw</a></span>
    <span class="issues-meta-item">commented 2026-03-10 20:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Adding a fresh spot-check here to reduce maintainer validation time.</p>
<h2>Fresh reproduction (UTC)</h2>
<p>I repeated the signed-path test after opening this issue, using the same signing shape described in the report.</p>
<ul>
<li><code>2026-03-10T20:34:12.215Z</code> -&gt; <code>node1</code> -&gt; <code>500</code> -&gt; <code>runtime error: invalid memory address or nil pointer dereference: panic</code></li>
<li><code>2026-03-10T20:34:12.431Z</code> -&gt; <code>node2</code> -&gt; <code>500</code> -&gt; <code>runtime error: invalid memory address or nil pointer dereference: panic</code></li>
<li><code>2026-03-10T20:34:12.628Z</code> -&gt; <code>node3</code> -&gt; <code>500</code> -&gt; <code>runtime error: invalid memory address or nil pointer dereference: panic</code></li>
</ul>
<p>Control check:</p>
<ul>
<li><code>2026-03-10T20:34:45.512Z</code> -&gt; unsigned <code>POST http://node2.gonka.ai:8000/v1/chat/completions</code> -&gt; <code>401</code> -&gt; <code>Authorization is required</code></li>
</ul>
<p>Fallback surface check:</p>
<ul>
<li><code>2026-03-10T20:34:38.205Z</code> -&gt; <code>GET https://node4.gonka.ai/v1/identity</code> -&gt; <code>502 Bad Gateway</code></li>
</ul>
<p>That does not prove the exact panic site, but it does further narrow the failure mode:</p>
<ul>
<li>the documented route is live</li>
<li>the unauthenticated case is handled normally</li>
<li>the signed request gets past the initial missing-auth stage</li>
<li>the public signed path then fails with the same internal panic on all three documented endpoints</li>
</ul>
<h2>Maintainer validation shortcut</h2>
<p>If I were debugging this from your side, I would check in this order:</p>
<ol>
<li>Confirm whether the currently deployed public transfer agents are all actually running a build that includes the <code>#643</code> nil-guard path.</li>
<li>Re-run the signed <code>/v1/chat/completions</code> path on a funded account against <code>node1/node2/node3</code>.</li>
<li>If the same <code>500 panic</code> persists, inspect the remaining nil / empty-result boundaries in the public inference path, especially:</li>
<li>requester lookup</li>
<li>executor selection</li>
<li>executor forwarding</li>
<li>Add a regression test asserting that the signed public handler path must never surface a panic-shaped failure.</li>
<li>Optionally add recover middleware on the public API server as defense-in-depth, even if the primary bug is elsewhere.</li>
</ol>
<details>
<summary>Minimal sanitized Node.js repro shape</summary>


<pre><code class="language-ts">import { secp256k1 } from '@noble/curves/secp256k1.js';
import { sha256 } from '@noble/hashes/sha2.js';

const body = JSON.stringify({
  model: 'Qwen/Qwen3-235B-A22B-Instruct-2507-FP8',
  messages: [{ role: 'user', content: 'ping' }],
  max_tokens: 16,
});

const endpoints = [
  {
    name: 'node1',
    url: 'http://node1.gonka.ai:8000/v1/chat/completions',
    transferAddress: 'gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le',
  },
  {
    name: 'node2',
    url: 'http://node2.gonka.ai:8000/v1/chat/completions',
    transferAddress: 'gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp',
  },
  {
    name: 'node3',
    url: 'https://node3.gonka.ai/v1/chat/completions',
    transferAddress: 'gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5',
  },
];

function nanoTimestamp() {
  const millisSinceEpoch = BigInt(Date.now()) * 1_000_000n;
  const subMillisecondNanos = process.hrtime.bigint() % 1_000_000n;
  return millisSinceEpoch + subMillisecondNanos;
}

function buildAuthorization(body, timestamp, transferAddress, privateKeyBytes) {
  const payloadHashHex = Buffer.from(sha256(Buffer.from(body))).toString('hex').toLowerCase();
  const message = Buffer.from(`${payloadHashHex}${timestamp.toString()}${transferAddress}`);
  const sig = secp256k1.sign(sha256(message), privateKeyBytes, { lowS: true, format: 'compact' });
  const bytes = sig instanceof Uint8Array ? sig : sig.toCompactRawBytes();
  return Buffer.from(bytes).toString('base64');
}

for (const endpoint of endpoints) {
  const timestamp = nanoTimestamp();
  const headers = {
    'Content-Type': 'application/json',
    'X-Requester-Address': '&lt;funded gonka1... address&gt;',
    'X-Timestamp': timestamp.toString(),
    Authorization: buildAuthorization(body, timestamp, endpoint.transferAddress, &lt;privateKeyBytes&gt;),
  };

  const response = await fetch(endpoint.url, {
    method: 'POST',
    headers,
    body,
  });

  console.log(endpoint.name, response.status, await response.text());
}
</code></pre>


This is intentionally sanitized. I can provide the exact reproduction script and exact headers privately if useful.
</details>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/junior2wnw">@junior2wnw</a></span>
    <span class="issues-meta-item">commented 2026-03-10 21:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Downstream note from a live client.</p>
<p>This issue currently blocks the Gonka-backed chat path in <code>Klava</code>:
- repo: https://github.com/junior2wnw/klava-bot
- provider implementation: https://github.com/junior2wnw/klava-bot/blob/main/packages/runtime/src/gonka-service.ts
- public status note: https://github.com/junior2wnw/klava-bot/blob/main/README.md</p>
<p><code>Klava</code> already implements onboarding, balance and model checks, strongest-model resolution, and signed <code>POST /v1/chat/completions</code> requests against the documented public flow.</p>
<p>The client now reports this as a provider-side failure because the signed request passes the unauthenticated stage and then fails inside the transfer-agent path.</p>
<p>That is why the downstream response is to wait for provider stabilization here rather than redesign the client path. If the public mainnet transfer-agent panic is fixed on the Gonka side, the existing Gonka-backed path in <code>Klava</code> should work again without a different request model.</p>
<p>If bounty attribution metadata is useful later, my Gonka address is:
<code>gonka1glph4syjlx347ptv2n7qfz67sryrhk983j5f8a</code></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/junior2wnw">@junior2wnw</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>One more downstream signal from the live client side.</p>
<p>I kept the current Gonka integration path intact and documented the current client boundary here:
- https://github.com/junior2wnw/klava-bot/blob/main/GONKA_STATUS.md</p>
<p>Current downstream status on my side is still:</p>
<ul>
<li>onboarding / validation works</li>
<li>requester address derivation works</li>
<li>balance lookup works</li>
<li>model discovery / strongest-model selection works</li>
<li>signed <code>/v1/chat/completions</code> is the blocked path</li>
</ul>
<p>So from the client side this still looks isolated to the signed transfer-agent completion path rather than to the broader Gonka onboarding or account surfaces.</p>
<p>That is why I have not redesigned the client around a different request model yet. If the provider-side panic is fixed here, the existing downstream path should become usable again without changing the surrounding client architecture.</p>
<p>If a maintainer wants a freshly minimized reproduction bundle again, I can post one.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-03-25 16:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Found three nil-unguarded gRPC response accesses in <code>post_chat_handler.go</code> that can cause the panic described here:</p>
<ol>
<li>
<p><strong><code>enforceDeveloperAccessGate</code></strong> (line 250): <code>paramsResp.Params.DeveloperAccessParams</code> — panics if <code>paramsResp</code> is nil. Called for ALL requests.</p>
</li>
<li>
<p><strong><code>handleTransferRequest</code></strong> (line 294): raw gRPC error returned without <code>echo.NewHTTPError</code> wrapping — error handler middleware receives an unexpected error type.</p>
</li>
<li>
<p><strong><code>validateRequester</code></strong> (line 1000): <code>priceResponse.Found</code> — panics if <code>priceResponse</code> is nil after <code>GetModelPerTokenPrice</code> query.</p>
</li>
</ol>
<p>All three are in the common request path, which explains why all documented endpoints fail simultaneously.</p>
<p>Fix in PR #947 — adds nil guards to all three locations (3 lines changed).</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-03-26 14:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@junior2wnw Hi
Tried your script - buildAuthorization double-hashes the message, so the server returns 401 "invalid signature". Fix: pass raw bytes to secp256k1.sign(message, ...) instead of secp256k1.sign(sha256(message), ...). After that, inference returns 200</p>
<pre><code class="language-js">function buildAuthorization(body, timestamp, transferAddress, privateKeyBytes) {
  const payloadHashHex = Buffer.from(sha256(Buffer.from(body))).toString('hex').toLowerCase();
  const message = Buffer.from(`${payloadHashHex}${timestamp.toString()}${transferAddress}`);
  const sig = secp256k1.sign(message, privateKeyBytes, { lowS: true, format: 'compact' });
  const bytes = sig instanceof Uint8Array ? sig : sig.toCompactRawBytes();
  return Buffer.from(bytes).toString('base64');
}
</code></pre>
<p>Could you rerun with this fix and check if the 500 panic still reproduces? It's possible it was already fixed in a recent update</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zhaog100">@zhaog100</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>/attempt</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zhaog100">@zhaog100</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>/attempt</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zhaog100">@zhaog100</a></span>
    <span class="issues-meta-item">commented 2026-03-26 16:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>/attempt</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-03-28 20:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Found the same InjectParamsIntoContext pattern in two more handlers — StartInference and FinishInference silently continue with broken context when params store is corrupted.</p>
<p>This is the same bug fixed for Validation in #968, but in the other two critical message handlers.</p>
<p>Without fix: handler logs warning, continues → GetDeveloperAccessParams and GetTransferAgentAccessParams fail silently → access gates bypassed.</p>
<p>Fix in PR (link below) — regression tests confirm FAIL without fix, PASS with fix.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/junior2wnw">@junior2wnw</a></span>
    <span class="issues-meta-item">commented 2026-03-30 20:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks - I reran this on March 31, 2026 against the currently documented public mainnet transfer-agent endpoints using a funded external requester account, and I tested both signing variants:</p>
<ol>
<li>the current public <code>gonka-openai</code> SDK style
   (<code>payload hash -&gt; signature input -&gt; sha256(signature input) -&gt; sign</code>)</li>
<li>the raw-message variant suggested above
   (<code>payload hash -&gt; signature input -&gt; sign</code>)</li>
</ol>
<p>At least on the currently documented public mainnet endpoints, changing the signature that way did not restore a successful public inference response on my side.</p>
<p>What I observed on the March 31 rerun:</p>
<ul>
<li><code>node1.gonka.ai</code></li>
<li>SDK-style signing: <code>429 rate limit exceeded</code></li>
<li>raw-message signing: <code>429 rate limit exceeded</code></li>
<li>
<p>no successful <code>200</code> from either variant</p>
</li>
<li>
<p><code>node2.gonka.ai</code></p>
</li>
<li>I still could not get a successful <code>200</code></li>
<li>
<p>during retesting it remained unstable and alternated between <code>429 rate limit exceeded</code> and the same internal panic shape reported in this issue:
    <code>runtime error: invalid memory address or nil pointer dereference: panic</code></p>
</li>
<li>
<p><code>node3.gonka.ai</code></p>
</li>
<li>unstable / timed out during the rerun, so I could not complete a clean public A/B check there</li>
</ul>
<p>So as of March 31, 2026, I cannot confirm that the extra hash is the root cause of the current public mainnet failure path.</p>
<p>Another reason I am hesitant to treat this as the main fix is that the current public <code>gonka-openai</code> TypeScript SDK still hashes the signature input before signing, so our client-side implementation was matching the published SDK behavior rather than inventing its own scheme:
https://github.com/gonka-ai/gonka-openai/blob/main/typescript/src/utils.ts</p>
<p>I also rechecked the wallet side during the same run:</p>
<ul>
<li>the requester account derives correctly on the standard path</li>
<li>the account exists on mainnet</li>
<li>the account is funded</li>
<li>transfer-agent allowlist data is present on-chain for the currently documented public transfer-agent addresses</li>
</ul>
<p>So at least from the March 31 retest, this does not currently look like a missing-wallet-registration issue on my side.</p>
<p>One more concrete observation: on one of today's direct checks, <code>node2</code> was not even a clean oracle for signature validity, because a deliberately invalid <code>Authorization</code> value could still fall into the same server-side failure path instead of returning a clean <code>401</code>. That makes it hard to conclude from current public-node behavior alone that raw-message signing is the canonical fix.</p>
<p>My current read is:</p>
<ul>
<li>the signing observation may still be valid in some environment, deployment, or server revision</li>
<li>but on the currently documented public mainnet endpoints, the blocking issue still appears to be endpoint-side instability rather than a clean, reproducible client-side signature mismatch</li>
<li>in particular, the nil-response / nil-pointer handler issue discussed in <code>#946</code> and <code>#947</code> still looks highly relevant to the public failure path</li>
</ul>
<p>The fastest path to resolution seems to be:</p>
<ol>
<li>Confirm the canonical signature contract at the server boundary and make the SDK, docs, and server-side verification test all agree on the same rule.</li>
<li>Re-run an end-to-end signed <code>POST /v1/chat/completions</code> test against the documented public endpoints using a funded external account.</li>
<li>Land <code>#947</code> or equivalent hardening if the public chat handler can still panic under partial / nil chain-RPC responses.</li>
<li>If raw-message signing is now the intended behavior, update the public SDK and docs accordingly, because the currently published SDK still implements the hashed-input signing flow.</li>
</ol>
<p>If useful, I can also post a fresh March 31 endpoint matrix with exact status/body pairs from the rerun.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/junior2wnw">@junior2wnw</a></span>
    <span class="issues-meta-item">commented 2026-04-27 13:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi, quick follow-up on #876.</p>
<p>I noticed #947 explored a possible fix path and added an integration test for the signed <code>/v1/chat/completions</code> flow, but it was later closed unmerged. Since this issue is still in Triage/New, let me know if a fresh retest against the public endpoints or the private reproduction details from the report would help.</p>
<p>Happy to validate a patched deployment if useful.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/dufok">@dufok</a></span>
    <span class="issues-meta-item">commented 2026-05-29 16:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h3>Fresh repro 2026-05-29 — distinct 401 variant: per-model "requires an API key" (not signature/panic)</h3>
<p>Following up ~1 month after the last activity here — the documented public mainnet inference flow is still not usable for an external developer, but I hit a <strong>different failure mode</strong> than the panic/<code>invalid signature</code>/<code>429</code> already in this thread, so flagging it in case it is a separate access-control layer worth its own issue.</p>
<p><strong>Setup</strong>
- Funded mainnet account (<code>gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt</code>, ~295 GNK).
- <code>publish-pubkey</code> via <code>inferenced</code> v0.2.12 succeeded (<code>code: 0</code>, txhash returned).
- Account is <strong>not</strong> a <code>Participant</code> (<code>query inference show-participant &lt;addr&gt;</code> -&gt; <code>NotFound</code>).
- Client: <code>gonka-openai==0.2.6</code> (Python), <code>api_key="mock-api-key"</code> set explicitly.</p>
<p><strong>Request the SDK actually sent</strong> (captured by patching <code>httpx.Client.send</code>):</p>
<pre><code>POST https://node4.gonka.ai/v1/chat/completions
authorization:        &lt;present, len=88, secp256k1 compact base64&gt;
x-requester-address:  gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
x-timestamp:          1780067501484655306
content-type:         application/json
</code></pre>
<p>So all three documented signing headers are present — this is past the unsigned (<code>Authorization is required</code>) stage.</p>
<p><strong>Response</strong></p>
<pre><code>401 {&quot;error&quot;:{&quot;message&quot;:&quot;model \&quot;Qwen/Qwen3-235B-A22B-Instruct-2507-FP8\&quot; requires an API key&quot;}}
</code></pre>
<p><strong>Why this looks distinct from the existing reports here</strong>
- Not <code>Authorization is required</code> (unsigned case).
- Not <code>invalid signature</code> (the SDK double-hash issue @x0152 raised).
- Not the <code>500</code> nil-pointer panic / <code>429</code> rate-limit in the original report.
- The rejection is <strong>model-specific</strong> (<code>model "X" requires an API key</code>), which reads like a per-model access gate (cf. #1213, #1226) applied <em>after</em> signature validation — possibly the broker/allowlist registration several others are requesting (#1245, #1247, #1257).</p>
<p><strong>Question for maintainers</strong>: is mainnet inference now gated behind a per-model API key / broker-allowlist on top of <code>publish-pubkey</code> + signing? If so, the public Developer Quickstart does not mention it, and a funded account following the documented flow lands on this 401 with no obvious next step. Happy to file this as a separate issue if you consider it distinct from the signed-completion panic tracked here.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-03 06:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @dufok, the Developer Quickstart has been updated. If you have any other questions, please open a new issue</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #876](https://github.com/gonka-ai/gonka/issues/876) every hour.
