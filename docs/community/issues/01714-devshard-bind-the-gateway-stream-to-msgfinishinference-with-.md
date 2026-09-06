---
title: "#1714 — `devshard` bind the gateway stream to `MsgFinishInference` with a second hash"
source: https://github.com/gonka-ai/gonka/issues/1714
issue_number: 1714
synced_at: 2026-09-06T14:13:47Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    `devshard` bind the gateway stream to `MsgFinishInference` with a second hash
    <span class="issues-number">#1714</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-09-03 18:51 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-03 18:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Proposal: bind the gateway stream to `MsgFinishInference` with a second hash

**Status:** Design, not implemented
**Related:** [PR #1650](https://github.com/gonka-ai/gonka/pull/1650) (compress inference payloads),
[PR #1686](https://github.com/gonka-ai/gonka/pull/1686) (logprobs only to a gateway that asked),
[`docs/proposal/compressed-payloads.md`](../../../docs/proposal/compressed-payloads.md)

This is a security gap, not a size tweak. Payload stripping is a real network
win; the signed finish currently covers only the copy validators fetch, not
the copy the user was served.

---

## Problem

After [#1650](https://github.com/gonka-ai/gonka/pull/1650) the executor no
longer treats "the body I store" and "the body I stream to the gateway" as
the same bytes.

`ExecutorResponseProcessor.prepareBody` (`common/completionapi/responseprocessor.go`)
parses each chunk once and emits **two** JSON marshals:

| Copy | What is dropped | Who consumes it |
| --- | --- | --- |
| **Stored** | `token_ids`, `prompt_token_ids`, `prompt_logprobs`, plus redundant logprob fields (`bytes`, position `logprob`) | Payload store, `MsgFinishInference.response_hash`, validators |
| **Forwarded** | The same internals, and — when the gateway did not ask — `logprobs` entirely ([#1686](https://github.com/gonka-ai/gonka/pull/1686)) | SSE / JSON to `devshardctl` |

`MsgFinishInference` still has a single hash:

```protobuf
message MsgFinishInference {
  uint64 inference_id = 1;
  bytes  response_hash = 2;  // sha256 of the stored payload
  ...
  bytes  proposer_sig = 6;   // signs this message, including response_hash
}
```

That hash is `sha256` of `GetResponseBytes()` — for a stream, the
`SerializedStreamedResponse` envelope whose `events` are the **stored**
lines, not the forwarded ones (`execute.go` after `processor.GetResponse()`).

### What still works: validator ↔ executor

A sampled validator `GET`s the stored payload from the executor, checks the
executor's payload signature, then:

```
sha256(response_payload) == MsgFinishInference.response_hash
```

(`devshard/cmd/devshardd/inference/validate.go`). Mismatch is
`ErrHashMismatch`. The executor cannot finish one body and serve validators
another. Logprobs used for replay live on that stored copy, so validation of
the **original** (stored) message is intact.

### What does not work: gateway ↔ user

The gateway never fetches that payload on the hot path. It only sees:

1. The **forwarded** SSE/JSON (stripped).
2. `devshard_meta` carrying the signed `MsgFinishInference`.

`response_hash` is a hash of bytes the gateway does not have. Hashing the
stream it received cannot match. There is no second field to match against.
The gateway therefore **cannot** prove that the body it forwarded to the
client is the body the executor attested in Finish.

The gateway also strips again for the client (`internalStrippedFields`, and
`logprobs` unless the client asked — `devshardctl/stream_rewrite.go`). That
client-facing strip is not the gap: the user did not ask for a signed
OpenAI body. The gap is **host → gateway**: the only copy the gateway can
check is already a different document from `response_hash`.

### Attack

An executor can:

1. Store and hash a valid completion (logprobs intact enough to pass
   `CompareLogits` if sampled).
2. Sign `MsgFinishInference` over that hash.
3. Stream a **different** stripped body to the gateway — cheaper tokens,
   different text, truncated answer, ads, …

Validators who are sampled fetch (1) and vote valid. The user was served
(3). Nothing in Finish binds (3). Sampling does not close this: the
user-visible bytes are never what is hashed.

This is not theoretical divergence from JSON key order. The processor
**intentionally** marshals two documents and hashes only one.

---

## Goal

Keep the strip (network saving). Make the served body as binding as the
stored body.

- The gateway can hash what it received and check it against the signed
  Finish.
- A validator that fetched the original can apply the **same** strip and
  check that the served hash is a projection of that original — so the
  executor cannot attest two unrelated documents.
- `proposer_sig` covers both hashes. One signature, two views of one
  inference.

---

## Proposal: two hashes on Finish

Add a second hash on `MsgFinishInference`:

```protobuf
message MsgFinishInference {
  uint64 inference_id = 1;
  bytes  response_hash = 2;        // existing: sha256(stored payload)
  bytes  served_hash = 10;         // new: sha256(strip(stored payload))
  uint64 input_tokens = 3;
  uint64 output_tokens = 4;
  uint32 executor_slot = 5;
  bytes  proposer_sig = 6;
  string escrow_id = 7;
  uint64 observed_height = 8;
  bytes  observed_block_hash = 9;
}
```

Field number 10: 3–9 are already assigned. Name: `served_hash` (what left
the executor toward the gateway). `stripped_hash` is the same bytes if
`strip` is the function below.

`response_hash` is unchanged. Validators keep fetching the stored payload
and checking it. Replay and `CompareLogits` keep reading stored logprobs.

### Invariant

```
served_hash == sha256(StripForGateway(stored_payload))
```

`StripForGateway` is a **pure, deterministic** function of the stored
payload: drop `logprobs` (and any other field the executor is not allowed
to put on the host→gateway wire). It must be the same implementation on
executor, gateway, and validator — one package, one test corpus.

Then:

| Party | Check |
| --- | --- |
| **Executor** | Hashes stored bytes → `response_hash`. Strips, hashes → `served_hash`. Signs Finish over both. Forwards the stripped bytes (not a third marshal). |
| **Gateway** | Reconstructs the same document shape from the stream it received. `sha256(received) == served_hash`. `proposer_sig` verifies. Serve to the client only after this (or mark the attempt failed). |
| **Validator** | Existing: `sha256(fetched) == response_hash`. New: `sha256(StripForGateway(fetched)) == served_hash`. Failure means the executor signed a served view that is not a strip of the stored view. |

The gateway never needs the original payload. The validator never needs the
live stream. Anyone with the stored payload can re-derive `served_hash`.

### What `StripForGateway` is — and is not

It is **not** today's `prepareBody` forwarded marshal.

Today, when `forwardLogprobs` is true, the forwarded copy is taken **before**
`compressLogprobsIn`, so it still has `bytes` / position `logprob` that the
stored copy has already dropped. Strip(stored) cannot reproduce that
forwarded document: the information is gone. That is why a validator cannot
"strip the original and check the second hash" against the current wire
format.

The two-hash design only closes the gap if **the bytes on the wire are
exactly `StripForGateway(stored)`**. Concretely:

1. Slim and store as today (1650) — that remains `response_hash`.
2. `StripForGateway` = drop `logprobs` from that stored document (token_ids
   are already gone).
3. Forward **those** bytes. Hash **those** bytes as `served_hash`.

Gateway-side client logprobs (`reconstructChunkLogprobs`) then cannot be
filled from the host stream. That is the existing [#1686](https://github.com/gonka-ai/gonka/pull/1686)
trade: logprobs on the wire are for a gateway that asked, not for Finish
binding. Options, in order of preference:

- **A (recommended).** Host→gateway is always the stripped stored projection.
  A client that asked for logprobs gets them from the gateway's own policy
  (omit, or a later authenticated payload fetch). Finish binding is one
  shape. This is what [compressed-payloads.md](../../../docs/proposal/compressed-payloads.md)
  already proposed for the wire.
- **B.** Finish grows a flag (`served_includes_logprobs`) and two strip
  functions. Do not do this unless a measured product requirement says the
  gateway must reconstruct client logprobs from the live stream. Two
  projections double the test surface and let an executor pick the fatter
  path to hide divergence.

Do not hash a third ad-hoc marshal. The processor already has stored bytes;
strip those; forward the result.

### Document shape (stream vs JSON)

Stored streams are not raw SSE. They are:

```json
{"events": ["data: {…}", "data: {…}", "data: [DONE]"]}
```

(`SerializedStreamedResponse`, `GetBodyBytes`). `response_hash` is
`sha256` of that JSON as `json.Marshal` emitted it — **not**
`CanonicalizeJSON` (that helper is prompt-only).

`served_hash` must use the **same** envelope and the **same** hash
function, with each `data:` line replaced by its stripped marshal. The
gateway already buffers or can fold `data:` lines; wrapping them in
`events` and hashing is the check. Non-stream JSON is the stripped object
marshaled once, matching `GetForwardedJSONBytes` after the processor is
taught to forward `StripForGateway(stored)` instead of a parallel tree.

Whitespace and key order are whatever `json.Marshal` of `map[string]any`
produces after the shared strip. Executor and gateway must not re-parse
and re-marshal independently with different `UseNumber` / encoding flags.
The gateway should hash the **raw forwarded lines** it received (or the
raw JSON body), not a second decode. The executor should accumulate those
same forwarded strings while writing them, then envelope-hash — the same
pattern as `streamedResponse` today, but for the forwarded copy.

### Signature

`signProposer` already signs the Finish proto with `proposer_sig` cleared.
Adding `served_hash` automatically enters the signed payload. No new
signature scheme. Empty `served_hash` on a post-upgrade Finish is a
protocol error (fail closed), not "legacy skip", once the child version
that emits the field is required.

Pre-upgrade Finish messages have no field 10. Mixed estate:

| Executor | Gateway | Behaviour |
| --- | --- | --- |
| old | new | Field absent → gateway **cannot** bind the stream. Log and do not treat the body as Finish-authenticated. Do not fail the user response solely for this during rollout. |
| new | old | Extra field ignored. No worse than today. |
| new | new | Full check. |

Pin the cutover: once every executor in the group is new, gateways fail
closed on missing `served_hash`.

---

## What the gateway does with a mismatch

`sha256(received) != served_hash` (or signature fail) means the stream is
not the attested body. That is the same class of fault as an error envelope
with a Finish: do **not** silently serve it as a successful completion.

Recommended: treat as executor fault on that attempt (fail the stream to
the client with the existing host-error path, record, allow redundancy to
try another host). Do not accept the Finish as authenticating the bytes
just delivered. Exact mapping onto miss / timeout / invalidate is an
implementation plan item; the requirement is **fail closed for authenticity**,
not a new on-chain message.

---

## What this does not change

- Validation replay, `CompareLogits`, payload fetch, gzip/zstd.
- `response_hash` meaning or who computes it.
- Client-facing stripping in `devshardctl`.
- Error-miss: that path already binds `ResponseHash` of the **stored**
  error envelope. If the error is also stripped on the wire, `served_hash`
  applies the same way; verifiers keep using the stored hash.

---

## Tests (acceptance)

- **Projection.** For stored payloads in the 1650 corpus (JSON and streamed
  envelope), `sha256(StripForGateway(stored))` equals the executor's
  `served_hash`, and `StripForGateway` is idempotent.
- **Gateway bind.** A stubbed stream whose forwarded bytes match
  `served_hash` is accepted; flipping one `data:` line fails the check
  even when `response_hash` still matches the stored envelope.
- **Validator bind.** Fetched stored payload matches `response_hash`;
  strip of that payload matches `served_hash`. Mutating stored logprobs
  without changing the forwarded body fails the validator's second check
  if and only if strip sees the mutation (it should not: logprobs are
  stripped — so also assert the complementary case: mutating **content**
  in stored without matching served fails both).
- **Split-brain attack.** Processor stores completion A, forwards
  completion B. Finish cannot satisfy both hashes unless `B == strip(A)`.
- **Signature.** Changing `served_hash` after sign fails `proposer_sig`.
- **Legacy.** Absent field is distinguishable from present-and-wrong.
- Mutation-check the gateway check: delete it, the split-brain test
  fails.

---

## Sequencing

1. Extract `StripForGateway` next to `SlimStoredDocument` / `dropFields`.
   Unit-test it as a function of stored bytes only.
2. Processor: accumulate forwarded lines from that strip; expose
   `GetServedBytes()`; `execute.go` sets `served_hash`.
3. Proto field + sign (regenerate). State machine copies the field through
   apply like `ResponseHash`.
4. Gateway: after the stream (or on the JSON body), hash and compare
   before treating the attempt as a signed completion.
5. Validator: second hash check after the existing payload-hash check.
6. Fail-closed once the version is required; mixed-estate behaviour as in
   the table above.

Network cost of the extra field is 32 bytes on Finish. The wire body stays
the stripped copy — the 1650/1686 saving is kept, and it finally has a
verifier.

</div>

---

> 🔄 **Auto-synced** from [Issue #1714](https://github.com/gonka-ai/gonka/issues/1714) every hour.
