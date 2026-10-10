---
title: "#1939 — Route `StateSignatureContent` through `CanonicalSignedBytes`"
source: https://github.com/gonka-ai/gonka/issues/1939
issue_number: 1939
synced_at: 2026-10-10T00:59:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Route `StateSignatureContent` through `CanonicalSignedBytes`
    <span class="issues-number">#1939</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-07 14:51 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-07 14:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Route `StateSignatureContent` through `CanonicalSignedBytes`

**Status:** Follow-up, not blocking  
**Source:** [PR #1791 review](https://github.com/gonka-ai/gonka/pull/1791#pullrequestreview-5421014455) (kaileido)  
**Related:** [PR #1791](https://github.com/gonka-ai/gonka/pull/1791) — unify host signature identity

Pre-existing. Not introduced by the identity refactor. No divergence on current messages.

---

## Problem

`StateSignatureContent` is the secp256k1 preimage for a host state attestation (`state_root`, `escrow_id`, `nonce`). Signers and gossip verifiers build it with plain `proto.Marshal`. Settlement builds the same message with the deterministic marshal.

Those encodings are the same bytes today. The proto is three scalars (`bytes`, `string`, `uint64`) and has no map or other unordered field. `proto.Marshal` and `proto.MarshalOptions{Deterministic: true}` agree on that shape.

They stop agreeing if a map, or any field whose wire order is not fixed, is added later. The host would sign one encoding. `VerifySettlement` and the chain settlement keeper would recover against another. Nodes would reject honest state signatures.

`signProposer` already goes through `types.CanonicalSignedBytes`. `signState` does not.

## Call sites

| Role | Where | Encoding now |
|---|---|---|
| Sign | `Host.signState` | `proto.Marshal` |
| Gossip verify | `Host.AccumulateGossipSig` | `proto.Marshal` |
| Gossip verify | `Server.HandleGossipNonce` | `proto.Marshal` |
| User verify | `Session.verifyStateSignature` | `proto.Marshal` |
| Off-chain settlement | `state.VerifySettlement` | `deterministicMarshal` |
| On-chain settlement | `keeper` over `DevshardStateSignatureContent` | gogo `XXX_Marshal(..., deterministic=true)` |

Tests that forge the same preimage with `proto.Marshal` (`host`, `transport`, `user`, `state`, `protocol`) follow the signer they copy.

## Proposed change

Route every devshard signer and verifier of `StateSignatureContent` through `types.CanonicalSignedBytes`:

- `Host.signState`
- `Host.AccumulateGossipSig`
- `Server.HandleGossipNonce`
- `Session.verifyStateSignature`
- `state.VerifySettlement`

Update the tests that build this preimage by hand so they call the same helper.

`StateSignatureContent` stays in the empty domain of `signedPreimageDomain`. `CanonicalSignedBytes` then returns the deterministic proto body and nothing else. That matches `VerifySettlement` and the chain keeper on the message as it exists now, so existing signatures still verify. Do not add a domain tag in this change. A tag is a protocol break for every stored state signature, and the chain verifies the unprefixed deterministic encoding of `DevshardStateSignatureContent`.

Leave the chain type where it is. It is a separate gogo message with the same three fields. This change only makes the devshard side share one helper, so a later unordered field is encoded once.

## Out of scope

- A domain prefix on state signatures, finish, receipt, or user diffs.
- Replacing `DevshardStateSignatureContent` with the devshard proto.
- Sticky `WarmKeys` after bind / rotate / revoke.

## Acceptance

- `signState`, both gossip verifiers, `verifyStateSignature`, and `VerifySettlement` call `CanonicalSignedBytes`. No remaining `proto.Marshal` of `StateSignatureContent` in non-test production code.
- `CanonicalSignedBytes` of a populated `StateSignatureContent` equals `proto.Marshal` of the same message (scalar layout, empty domain). A test locks that equality so a domain tag or a non-deterministic field fails CI before it ships.
- Existing state signatures still verify in `VerifySettlement` and in the chain keeper. No new domain string.
- `go test ./host/ ./transport/ ./user/ ./state/ ./protocol/ ./types/`

</div>

---

> 🔄 **Auto-synced** from [Issue #1939](https://github.com/gonka-ai/gonka/issues/1939) every hour.
