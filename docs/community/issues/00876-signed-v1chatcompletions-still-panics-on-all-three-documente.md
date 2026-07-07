---
title: "#876 — Signed /v1/chat/completions still panics on all three documented mainnet transfer-agent endpoints"
source: https://github.com/gonka-ai/gonka/issues/876
issue_number: 876
synced_at: 2026-07-07T04:28:20Z
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
    <span class="issues-meta-item">[@junior2wnw](https://github.com/junior2wnw) opened 2026-03-10 20:30 UTC</span>
    <span class="issues-meta-item">13 comments</span>
    <span class="issues-meta-item">Updated 2026-06-03 06:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content">
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
    <span>[@junior2wnw](https://github.com/junior2wnw)</span>
    <span class="issues-meta-item">commented 2026-03-10 20:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Adding a fresh spot-check here to reduce maintainer validation time.

## Fresh reproduction (UTC)

I repeated the signed-path test after opening this issue, using the same signing shape described in the report.

- `2026-03-10T20:34:12.215Z` -> `node1` -> `500` -> `runtime error: invalid memory address or nil pointer dereference: panic`
- `2026-03-10T20:34:12.431Z` -> `node2` -> `500` -> `runtime error: invalid memory address or nil pointer dereference: panic`
- `2026-03-10T20:34:12.628Z` -> `node3` -> `500` -> `runtime error: invalid memory address or nil pointer dereference: panic`

Control check:

- `2026-03-10T20:34:45.512Z` -> unsigned `POST http://node2.gonka.ai:8000/v1/chat/completions` -> `401` -> `Authorization is required`

Fallback surface check:

- `2026-03-10T20:34:38.205Z` -> `GET https://node4.gonka.ai/v1/identity` -> `502 Bad Gateway`

That does not prove the exact panic site, but it does further narrow the failure mode:

- the documented route is live
- the unauthenticated case is handled normally
- the signed request gets past the initial missing-auth stage
- the public signed path then fails with the same internal panic on all three documented endpoints

## Maintainer validation shortcut

If I were debugging this from your side, I would check in this order:

1. Confirm whether the currently deployed public transfer agents are all actually running a build that includes the `#643` nil-guard path.
2. Re-run the signed `/v1/chat/completions` path on a funded account against `node1/node2/node3`.
3. If the same `500 panic` persists, inspect the remaining nil / empty-result boundaries in the public inference path, especially:
   - requester lookup
   - executor selection
   - executor forwarding
4. Add a regression test asserting that the signed public handler path must never surface a panic-shaped failure.
5. Optionally add recover middleware on the public API server as defense-in-depth, even if the primary bug is elsewhere.

<details>
<summary>Minimal sanitized Node.js repro shape</summary>

```ts
import { secp256k1 } from '@noble/curves/secp256k1.js';
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
    'X-Requester-Address': '<funded gonka1... address>',
    'X-Timestamp': timestamp.toString(),
    Authorization: buildAuthorization(body, timestamp, endpoint.transferAddress, <privateKeyBytes>),
  };

  const response = await fetch(endpoint.url, {
    method: 'POST',
    headers,
    body,
  });

  console.log(endpoint.name, response.status, await response.text());
}
```

This is intentionally sanitized. I can provide the exact reproduction script and exact headers privately if useful.
</details>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@junior2wnw](https://github.com/junior2wnw)</span>
    <span class="issues-meta-item">commented 2026-03-10 21:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Downstream note from a live client.

This issue currently blocks the Gonka-backed chat path in `Klava`:
- repo: https://github.com/junior2wnw/klava-bot
- provider implementation: https://github.com/junior2wnw/klava-bot/blob/main/packages/runtime/src/gonka-service.ts
- public status note: https://github.com/junior2wnw/klava-bot/blob/main/README.md

`Klava` already implements onboarding, balance and model checks, strongest-model resolution, and signed `POST /v1/chat/completions` requests against the documented public flow.

The client now reports this as a provider-side failure because the signed request passes the unauthenticated stage and then fails inside the transfer-agent path.

That is why the downstream response is to wait for provider stabilization here rather than redesign the client path. If the public mainnet transfer-agent panic is fixed on the Gonka side, the existing Gonka-backed path in `Klava` should work again without a different request model.

If bounty attribution metadata is useful later, my Gonka address is:
`gonka1glph4syjlx347ptv2n7qfz67sryrhk983j5f8a`
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@junior2wnw](https://github.com/junior2wnw)</span>
    <span class="issues-meta-item">commented 2026-03-11 20:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    One more downstream signal from the live client side.

I kept the current Gonka integration path intact and documented the current client boundary here:
- https://github.com/junior2wnw/klava-bot/blob/main/GONKA_STATUS.md

Current downstream status on my side is still:

- onboarding / validation works
- requester address derivation works
- balance lookup works
- model discovery / strongest-model selection works
- signed `/v1/chat/completions` is the blocked path

So from the client side this still looks isolated to the signed transfer-agent completion path rather than to the broader Gonka onboarding or account surfaces.

That is why I have not redesigned the client around a different request model yet. If the provider-side panic is fixed here, the existing downstream path should become usable again without changing the surrounding client architecture.

If a maintainer wants a freshly minimized reproduction bundle again, I can post one.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-03-25 16:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Found three nil-unguarded gRPC response accesses in `post_chat_handler.go` that can cause the panic described here:

1. **`enforceDeveloperAccessGate`** (line 250): `paramsResp.Params.DeveloperAccessParams` — panics if `paramsResp` is nil. Called for ALL requests.

2. **`handleTransferRequest`** (line 294): raw gRPC error returned without `echo.NewHTTPError` wrapping — error handler middleware receives an unexpected error type.

3. **`validateRequester`** (line 1000): `priceResponse.Found` — panics if `priceResponse` is nil after `GetModelPerTokenPrice` query.

All three are in the common request path, which explains why all documented endpoints fail simultaneously.

Fix in PR #947 — adds nil guards to all three locations (3 lines changed).
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@x0152](https://github.com/x0152)</span>
    <span class="issues-meta-item">commented 2026-03-26 14:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    @junior2wnw Hi
Tried your script - buildAuthorization double-hashes the message, so the server returns 401 "invalid signature". Fix: pass raw bytes to secp256k1.sign(message, ...) instead of secp256k1.sign(sha256(message), ...). After that, inference returns 200

```js
function buildAuthorization(body, timestamp, transferAddress, privateKeyBytes) {
  const payloadHashHex = Buffer.from(sha256(Buffer.from(body))).toString('hex').toLowerCase();
  const message = Buffer.from(`${payloadHashHex}${timestamp.toString()}${transferAddress}`);
  const sig = secp256k1.sign(message, privateKeyBytes, { lowS: true, format: 'compact' });
  const bytes = sig instanceof Uint8Array ? sig : sig.toCompactRawBytes();
  return Buffer.from(bytes).toString('base64');
}
```

Could you rerun with this fix and check if the 500 panic still reproduces? It's possible it was already fixed in a recent update
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@zhaog100](https://github.com/zhaog100)</span>
    <span class="issues-meta-item">commented 2026-03-26 15:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    /attempt
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@zhaog100](https://github.com/zhaog100)</span>
    <span class="issues-meta-item">commented 2026-03-26 15:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    /attempt
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@zhaog100](https://github.com/zhaog100)</span>
    <span class="issues-meta-item">commented 2026-03-26 16:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    /attempt
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-03-28 20:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Found the same InjectParamsIntoContext pattern in two more handlers — StartInference and FinishInference silently continue with broken context when params store is corrupted.

This is the same bug fixed for Validation in #968, but in the other two critical message handlers.

Without fix: handler logs warning, continues → GetDeveloperAccessParams and GetTransferAgentAccessParams fail silently → access gates bypassed.

Fix in PR (link below) — regression tests confirm FAIL without fix, PASS with fix.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@junior2wnw](https://github.com/junior2wnw)</span>
    <span class="issues-meta-item">commented 2026-03-30 20:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks - I reran this on March 31, 2026 against the currently documented public mainnet transfer-agent endpoints using a funded external requester account, and I tested both signing variants:

1. the current public `gonka-openai` SDK style
   (`payload hash -> signature input -> sha256(signature input) -> sign`)
2. the raw-message variant suggested above
   (`payload hash -> signature input -> sign`)

At least on the currently documented public mainnet endpoints, changing the signature that way did not restore a successful public inference response on my side.

What I observed on the March 31 rerun:

- `node1.gonka.ai`
  - SDK-style signing: `429 rate limit exceeded`
  - raw-message signing: `429 rate limit exceeded`
  - no successful `200` from either variant

- `node2.gonka.ai`
  - I still could not get a successful `200`
  - during retesting it remained unstable and alternated between `429 rate limit exceeded` and the same internal panic shape reported in this issue:
    `runtime error: invalid memory address or nil pointer dereference: panic`

- `node3.gonka.ai`
  - unstable / timed out during the rerun, so I could not complete a clean public A/B check there

So as of March 31, 2026, I cannot confirm that the extra hash is the root cause of the current public mainnet failure path.

Another reason I am hesitant to treat this as the main fix is that the current public `gonka-openai` TypeScript SDK still hashes the signature input before signing, so our client-side implementation was matching the published SDK behavior rather than inventing its own scheme:
https://github.com/gonka-ai/gonka-openai/blob/main/typescript/src/utils.ts

I also rechecked the wallet side during the same run:

- the requester account derives correctly on the standard path
- the account exists on mainnet
- the account is funded
- transfer-agent allowlist data is present on-chain for the currently documented public transfer-agent addresses

So at least from the March 31 retest, this does not currently look like a missing-wallet-registration issue on my side.

One more concrete observation: on one of today's direct checks, `node2` was not even a clean oracle for signature validity, because a deliberately invalid `Authorization` value could still fall into the same server-side failure path instead of returning a clean `401`. That makes it hard to conclude from current public-node behavior alone that raw-message signing is the canonical fix.

My current read is:

- the signing observation may still be valid in some environment, deployment, or server revision
- but on the currently documented public mainnet endpoints, the blocking issue still appears to be endpoint-side instability rather than a clean, reproducible client-side signature mismatch
- in particular, the nil-response / nil-pointer handler issue discussed in `#946` and `#947` still looks highly relevant to the public failure path

The fastest path to resolution seems to be:

1. Confirm the canonical signature contract at the server boundary and make the SDK, docs, and server-side verification test all agree on the same rule.
2. Re-run an end-to-end signed `POST /v1/chat/completions` test against the documented public endpoints using a funded external account.
3. Land `#947` or equivalent hardening if the public chat handler can still panic under partial / nil chain-RPC responses.
4. If raw-message signing is now the intended behavior, update the public SDK and docs accordingly, because the currently published SDK still implements the hashed-input signing flow.

If useful, I can also post a fresh March 31 endpoint matrix with exact status/body pairs from the rerun.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@junior2wnw](https://github.com/junior2wnw)</span>
    <span class="issues-meta-item">commented 2026-04-27 13:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Hi, quick follow-up on #876.

I noticed #947 explored a possible fix path and added an integration test for the signed `/v1/chat/completions` flow, but it was later closed unmerged. Since this issue is still in Triage/New, let me know if a fresh retest against the public endpoints or the private reproduction details from the report would help.

Happy to validate a patched deployment if useful.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-05-29 16:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ### Fresh repro 2026-05-29 — distinct 401 variant: per-model "requires an API key" (not signature/panic)

Following up ~1 month after the last activity here — the documented public mainnet inference flow is still not usable for an external developer, but I hit a **different failure mode** than the panic/`invalid signature`/`429` already in this thread, so flagging it in case it is a separate access-control layer worth its own issue.

**Setup**
- Funded mainnet account (`gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt`, ~295 GNK).
- `publish-pubkey` via `inferenced` v0.2.12 succeeded (`code: 0`, txhash returned).
- Account is **not** a `Participant` (`query inference show-participant <addr>` -> `NotFound`).
- Client: `gonka-openai==0.2.6` (Python), `api_key="mock-api-key"` set explicitly.

**Request the SDK actually sent** (captured by patching `httpx.Client.send`):

```
POST https://node4.gonka.ai/v1/chat/completions
authorization:        <present, len=88, secp256k1 compact base64>
x-requester-address:  gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
x-timestamp:          1780067501484655306
content-type:         application/json
```

So all three documented signing headers are present — this is past the unsigned (`Authorization is required`) stage.

**Response**

```
401 {"error":{"message":"model \"Qwen/Qwen3-235B-A22B-Instruct-2507-FP8\" requires an API key"}}
```

**Why this looks distinct from the existing reports here**
- Not `Authorization is required` (unsigned case).
- Not `invalid signature` (the SDK double-hash issue @x0152 raised).
- Not the `500` nil-pointer panic / `429` rate-limit in the original report.
- The rejection is **model-specific** (`model "X" requires an API key`), which reads like a per-model access gate (cf. #1213, #1226) applied *after* signature validation — possibly the broker/allowlist registration several others are requesting (#1245, #1247, #1257).

**Question for maintainers**: is mainnet inference now gated behind a per-model API key / broker-allowlist on top of `publish-pubkey` + signing? If so, the public Developer Quickstart does not mention it, and a funded account following the documented flow lands on this 401 with no obvious next step. Happy to file this as a separate issue if you consider it distinct from the signed-completion panic tracked here.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-03 06:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Hi @dufok, the Developer Quickstart has been updated. If you have any other questions, please open a new issue
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #876](https://github.com/gonka-ai/gonka/issues/876) every hour.
