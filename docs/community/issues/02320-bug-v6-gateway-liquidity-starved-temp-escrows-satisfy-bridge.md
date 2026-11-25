---
title: "#2320 — [BUG] v6 gateway: liquidity-starved temp escrows satisfy bridge count and prevent automatic refill"
source: https://github.com/gonka-ai/gonka/issues/2320
issue_number: 2320
synced_at: 2026-11-25T04:20:25Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] v6 gateway: liquidity-starved temp escrows satisfy bridge count and prevent automatic refill
    <span class="issues-number">#2320</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 2026-11-24 11:37 UTC</span>
    <span class="issues-meta-item">6 comments</span>
    <span class="issues-meta-item">Updated 2026-11-25 03:47 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

During the epoch bridge window, the deployed v6 gateway can keep the configured number of active temporary escrows while none has enough available balance to serve incoming requests. Rotation counts those records toward `temp_count`, and the normal funding planner disables creation inside the bridge window. The gateway consequently remains underfunded until an operator increases `temp_count` or another lifecycle event changes the pool.

This concerns the **epoch-transition escrow pool**, not the Ethereum bridge.

## Environment and scope

Observed on mainnet on 2026-11-24 using:

- Image: `ghcr.io/qdanik/gateway@sha256:ba1e4aa06c2b3f24d61cbf543b133f337dc8d0de28e73b0a62d1a5225b84e06d`
- Deployed v6 RC6 revision: [bfab9a226e2f1277d4da8d8e36254a44946953ea](https://github.com/qdanik/gonka/commit/bfab9a226e2f1277d4da8d8e36254a44946953ea)
- Rotation enabled; bridge window 1,000 blocks; per-model `max_unsettled=500`.
- MiniMax / DeepSeek / GLM initially had `temp_count=6/6/3`, with 0.5 GNK per newly created escrow.

The production observation and code diagnosis below apply to that gateway build; this is not a claim that every upstream v6 build has identical behavior.

## Impact and production evidence

At 10:53 UTC, the chain snapshot was healthy, the phase was Inference, requests were not globally blocked, and 462 blocks remained before the epoch switch:

- Active escrows were all temporary escrows for rotation epoch 468, with counts exactly 6/6/3.
- Funding diagnostics had reported `full=0`, `standby=0`, and zero pending creates for all three models.
- Remaining unsettled-budget headroom was 386/195/164 respectively, so the 500 limit was not exhausted.
- In the preceding two-minute sample, 3,709 of 3,951 finished request log records contained an insufficient-escrow-balance failure (93.9%). These are log records, not unique users or a direct HTTP 503 count.

This caused a sustained availability problem for this gateway's clients; we have not established network-wide impact.

## Code path

In [rotation.go:52–75](https://github.com/qdanik/gonka/blob/bfab9a226e2f1277d4da8d8e36254a44946953ea/devshard/cmd/gateway/escrow/rotation.go#L52), `createsWanted` uses:

```go
existing := countActive(devshards, model.ModelID, role, int64(label)) +
    countOpenCreates(commitments, model.ModelID, role, label)
if existing >= target {
    return 0, nil
}
```

`countActive` checks active/model/role/rotation epoch, without checking available liquidity. `prepareBridge` uses this count to fill the temporary pool.

Meanwhile, [funding/plan.go:265–267](https://github.com/qdanik/gonka/blob/bfab9a226e2f1277d4da8d8e36254a44946953ea/devshard/cmd/gateway/funding/plan.go#L265) explicitly excludes bridge-window creation:

```go
return !state.RequestsBlocked && !state.InEpochPoC &&
    state.EpochKnown && state.ServedByNetwork &&
    !state.BreakerGated && !state.InBridgeWindow
```

Together these paths explain why a count-complete but liquidity-starved temporary pool does not automatically refill in the observed state.

## Reproduction conditions

1. Enable rotation and enter the pre-switch bridge window with room below `max_unsettled` and sufficient wallet funding.
2. Let rotation fill the temporary pool to `temp_count`.
3. Run sustained traffic until available liquidity is insufficient, while temporary escrow records remain active.
4. Observe that the count target remains satisfied and no replacement/top-up creates are scheduled.
5. Increase `temp_count` by one: the newly missing slot permits creation, and the funded new escrow can serve requests.

The above is the production-derived reproduction sequence; no separate end-to-end lab reproduction is claimed.

## Mitigation verified

We initially raised counts to 7/7/4. Later, changing the amount for future escrows from 0.5 to 2 GNK alone created no new escrows because the count target was already met.

At 11:23 UTC, raising counts again to 8/8/5 created three 2 GNK escrows. All three were confirmed on-chain and subsequently logged real `served` requests, not just cache hits.

The router's eligible-request success rate rose to 56.7%, 64.5%, and 79.2% in the complete 11:24, 11:25, and 11:26 UTC minutes. No insufficient-escrow-balance errors occurred in those minutes, but timeouts/client aborts remained. This is partial operational recovery, not proof that all failures were caused by this issue or that the mitigation is durable.

## Comparison with v4.2.0

The [v4.2.0 release code](https://github.com/gonka-ai/gonka/blob/b88062c9529389a61d4ba15b8b5603716a50909e/devshard/cmd/devshardctl/gateway.go) has `replaceDepletedEscrow`: deactivate the old escrow first, choose the replacement role through `rotationPlacement` (temp in the bridge window), then create if below target.

Its [rotation count](https://github.com/gonka-ai/gonka/blob/b88062c9529389a61d4ba15b8b5603716a50909e/devshard/cmd/devshardctl/escrow_rotation_target.go#L33) excludes held escrows, and [escrow_hold.go](https://github.com/gonka-ai/gonka/blob/b88062c9529389a61d4ba15b8b5603716a50909e/devshard/cmd/devshardctl/escrow_hold.go) has a serving-pool top-up path.

This suggests a lifecycle behavior regression relative to v4.2.0, rather than just an undersized initial deposit. It does not establish that v4.2.0 never experienced insufficient-balance errors.

## Expected behavior / regression coverage

Bridge maintenance should restore usable temporary-pool liquidity when persistent escrow-level depletion leaves it unable to serve, even when active-record count meets `temp_count`.

Please retain safeguards for unsettled budget, pending creates, wallet balance, backoff and permitted chain phases. Distinguish spent funds from recoverable in-flight reservations, and do not treat one oversized request as proof that an escrow must be retired (related: #1800).

Suggested regression cases:

- Count target met, temporary pool persistently starved, budget available: bounded refill using temporary escrows.
- Funds only temporarily reserved: avoid repeated overfunding while reservations recover.
- Pending creates or budget exhaustion: no duplicate/unbounded creation.
- Healthy temporary pool: no extra creates.
- Newly funded temporary escrow remains eligible to serve through bridge reconciliation.

</div>

---

## 💬 Comments (6)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-24 11:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Submitted a fix in #2321 against <code>devshard/gateway/v6.0.0</code>.</p>
<p>It refills the current bridge's liquidity even when active temp count is already satisfied, while keeping existing temps and their in-flight work. Refill uses the existing funding shortfalls, create rate limit and budget checks, and accounts for returning funds and pending/unread escrows.</p>
<p>The new integrated regression reproduces the insufficient-balance failure without the patch and successfully serves from the funded temp with it. Full scenario tests and lint pass; the PR also documents one intermittent failure in an unchanged scheduler race test and its 20 passing reruns. This has not been deployed to production.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-11-24 12:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ghcr.io/gonka-ai/devshard-gateway:mainnet-v0.2.16-v6.0.1-latest</p>
<p>Could you please check this one? RC6 is already outdated. The issue is valid, but it can be fixed by amount value. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-24 12:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi thanks for answer, about the amount value and the temp_count of escrows, do you have any recommendations about this?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-11-24 13:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Target count 8, reserve count 1, temp count 4 and 2.5 GNK usually works good </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-24 13:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>got it thanks a lot!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-11-25 03:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Ryanchen911 https://github.com/gonka-ai/gonka/pull/2333 - please, review</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2320](https://github.com/gonka-ai/gonka/issues/2320) every hour.
