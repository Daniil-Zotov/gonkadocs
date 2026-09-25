---
title: "#1800 — devshard gateway: request-specific insufficient balance deactivates and remints a usable escrow"
source: https://github.com/gonka-ai/gonka/issues/1800
issue_number: 1800
synced_at: 2026-09-25T01:37:04Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    devshard gateway: request-specific insufficient balance deactivates and remints a usable escrow
    <span class="issues-number">#1800</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 2026-09-18 02:49 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-20 04:16 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`ErrInsufficientBalance` means that the current escrow cannot reserve the cost of one particular request. The gateway currently interprets it as proof that the escrow has reached end-of-life, deactivates it, and mints a replacement.

A sufficiently large but otherwise valid request can therefore turn into an escrow mint/deactivate loop even when the escrow still has enough balance for ordinary requests.

## Production observation

On 2026-09-17, one request produced this sequence (unrelated concurrent lines omitted):

```text
request=req-1789648596464179072-1533588 stage=proxy_request_started escrow=80502 model=deepseek-ai/DeepSeek-V4-Flash-0731 stream=true input_tokens=926912
request=req-1789648596464179072-1533588 stage=runner_started escrow=80502 input_tokens=926912 model=deepseek-ai/DeepSeek-V4-Flash-0731
request=req-1789648596464179072-1533588 stage=runner_prepare_failed escrow=80502 error="prepare: local apply: mandatory start inference: insufficient escrow balance"
escrow_balance_exhausted escrow=80502
gateway_replacing_exhausted_escrow escrow=80502
request=req-1789648596464179072-1533588 stage=proxy_stream_failed escrow=80502 error="prepare: local apply: mandatory start inference: insufficient escrow balance"
escrow_depletion_deactivated escrow=80502 reason="balance_exhausted" deactivated_in_store=true settlement_due=false
escrow_rotation_created role=regular epoch=396 model="deepseek-ai/DeepSeek-V4-Flash-0731" escrow=80620 tx_hash=0232DAC22C5AC7C545BEAEDFFF36120234D3AD4C104976618B523A66F14EF7E1
escrow_depletion_replacement_created old_escrow=80502 new_escrow=80620 model="deepseek-ai/DeepSeek-V4-Flash-0731" reason="balance_exhausted" tx_hash=0232DAC22C5AC7C545BEAEDFFF36120234D3AD4C104976618B523A66F14EF7E1
```

The failure and the `escrow_balance_exhausted` event are 16 ms apart. The old escrow is persisted inactive immediately, and the replacement is created about four seconds later.

The same incident included a MiniMax mint peak: 29 epoch-396 regular escrows were created between 08:45:09Z and 10:06:13Z. The relevant Docker logs had already rotated out, so the database evidence alone cannot distinguish request-triggered depletion replacements from normal `target_count` reconciliation. The surviving DeepSeek sequence above does confirm the faulty path directly.

## Root cause

The state machine reserves the maximum cost of each request independently:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/state/machine.go#L944-L950

```go
reservedCost, err := tokenCost(msg.InputLength, msg.MaxTokens, sm.state.Config.TokenPrice)
if err != nil {
	return err
}
if sm.state.Balance < reservedCost {
	return types.ErrInsufficientBalance
}
```

This only proves:

```text
current balance < (this request's input_length + max_tokens) * token_price
```

It does not prove that the escrow cannot serve a smaller request.

`RunInference` nevertheless treats every occurrence of that error as terminal for the escrow:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L1724-L1730

```go
primary, err := e.prepareInflight(ctx, params, triedParticipants)
if err != nil {
	logRequestStage(ctx, "runner_prepare_failed", "escrow", e.devshardID, "error", err)
	if errors.Is(err, types.ErrInsufficientBalance) {
		e.fireBalanceExhausted()
	}
	return err
}
```

The callback then unconditionally deactivates the runtime or schedules a depletion replacement:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/gateway.go#L4031-L4038

```go
rt.proxy.redundancy.onBalanceExhausted = func() {
	if !g.escrowRotationEnabled() {
		g.deactivateDevshardByIDWithReason(escrowID, "escrow balance exhausted")
		g.retireRuntime(escrowID, "escrow balance exhausted")
		return
	}
	log.Printf("gateway_replacing_exhausted_escrow escrow=%s", escrowID)
	g.scheduleDepletedEscrowReplacement(escrowID, modelID, "balance_exhausted")
}
```

This bypasses the gateway's existing low-balance policy, which rotates only when the actual remaining balance is below `balanceMinimumThreshold`:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/gateway.go#L835-L864

## Why the observed request is expensive

The proxy stores `InputLength` as the byte length of the normalized JSON body:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/proxy.go#L233-L240

The host explicitly verifies the same byte-length convention:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/host/host.go#L1540-L1546

Consequently, the log field `input_tokens=926912` is actually 926,912 input bytes. With the default `max_tokens=3072`, the request tries to reserve:

```text
(926912 + 3072) * token_price = 929984 * token_price
```

For example, at `token_price=100`, the reservation is 92,998,400 units. An escrow with an 80,000,000 balance is healthy for many normal requests but cannot accept this one. The current code deactivates it anyway.

The pooled runtime selector also does not consider whether a candidate can afford the incoming request. It filters by lifecycle/nonce state and then chooses by active load and capacity weight:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/gateway.go#L1859-L1880

This lets a large request land on a lower-balance escrow even when another matching escrow could cover it.

## Expected behavior

- Failure to reserve one request must not by itself deactivate or replace the escrow.
- If another matching escrow can cover the reservation, the pooled route should select or retry that escrow.
- If no escrow can cover it, fail that request with a clear request/capacity error while keeping otherwise usable escrows active.
- Depletion replacement should run only after checking an escrow-level end-of-life condition, such as the existing low-balance threshold or a defined minimum viable reservation.

## Suggested change

1. Stop calling `fireBalanceExhausted()` solely because `prepareInflight` returned `ErrInsufficientBalance`.
2. Pass the required reservation and current balance through a typed error, or read the current balance in the callback, and distinguish `request_unaffordable` from `escrow_depleted`.
3. Before dispatch, calculate the exact reservation for each candidate using the normalized body byte length, `max_tokens`, and that escrow's `token_price`; exclude candidates that cannot cover it. Account for concurrent reservations so simultaneous requests cannot all select the same remaining balance.
4. Keep `checkBalances()` as the escrow lifecycle authority, or share one explicit depletion predicate between the periodic check and the request path.
5. Improve the failure log with `balance`, `required_reservation`, `input_bytes`, `max_tokens`, and `token_price`. Rename the proxy's `input_tokens` field to `input_bytes` (or log both) because it currently reports bytes.

## Regression tests

Add a test with a balance that is:

- below the reservation required by a large request;
- above `balanceMinimumThreshold`; and
- sufficient for a subsequent small request.

Assert that:

1. The large request returns an insufficient-capacity error.
2. No depletion callback, deactivation, settlement, or replacement mint occurs.
3. The same escrow remains active and successfully prepares the smaller request.

For pooled routing, add two same-model escrows with different balances and assert that a request which fits only the richer escrow is routed there without deactivating the poorer one.

Current tests call `onBalanceExhausted()` directly and verify that it deactivates an already-classified exhausted escrow. They do not cover whether a request-specific `ErrInsufficientBalance` was classified correctly before that callback.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-09-20 04:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>fixed in gateway v4.1.2</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1800](https://github.com/gonka-ai/gonka/issues/1800) every hour.
