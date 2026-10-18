---
title: "#2039 — [BUG] devshardctl: an escrow the gateway cannot serve is never settled, and the chain splits its deposit after two epochs"
source: https://github.com/gonka-ai/gonka/issues/2039
issue_number: 2039
synced_at: 2026-10-18T14:40:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] devshardctl: an escrow the gateway cannot serve is never settled, and the chain splits its deposit after two epochs
    <span class="issues-number">#2039</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/snevolin">@snevolin</a> opened 2026-10-16 00:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-16 08:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary
An escrow that the gateway cannot serve is excluded from routing but is not settled. The gateway deactivates an escrow when its runtime build ends with a final reason (`ErrLocalStateUnrecoverable`, `ErrEscrowNotFound`, `ErrEscrowSettled`, missing private key); after #2035 it keeps retrying an escrow whose build fails for any other reason. In both cases nothing settles the escrow. If nobody settles it by hand before the next epoch ends, the chain distributes its whole deposit equally per slot, and the owner gets nothing back.

Split out of #2034, which now covers only the gateway start.

## Motivation
Pre-existing on `main`. v6 (#1792) raises the exposure: many escrows per gateway, and new recovery steps (validation-obs and sealed-index rebuild) that can leave an escrow unserviceable.

## Impact
- Who is affected: escrow owners (the deposit), hosts of the escrow (no host stats reach the epoch record), gateway operators.
- Money: an escrow that is not settled in its epoch or the next cannot be settled at all; two epochs later the chain splits the full deposit equally per slot (`devshard_pruning.go`, `distributeUnsettledEscrow`). The owner gets no remainder back, and hosts are paid as if the escrow was fully used.
- Affected components: `devshard/cmd/devshardctl` (deactivation and settlement paths), `devshard/user/recover.go`, and the host side if the settlement data has to come from the hosts.

## Detailed description
- A deactivated escrow (`SetDevshardActive(false)`) keeps its data and can be brought back by the admin endpoint, but nothing settles it automatically.
- For the four final reasons the gateway has nothing to settle with: the escrow is gone or already settled on chain, the signing key is missing, or the local journal is proven inconsistent. In the last case the data needed for settlement (last state root, host signatures, host stats) exists only on the hosts.
- An escrow whose build fails permanently for a reason outside the four (for example a group or version mismatch in `recover.go`) is retried and reported after #2035, but neither deactivated nor settled.
- The same loss happens when the gateway itself is down for two epochs: no settlement runs without it.

## Reproduce
1. Run a gateway with one active escrow that has served requests.
2. Damage the escrow's SQLite journal so that recovery reports `ErrLocalStateUnrecoverable`, and restart the gateway.
3. The escrow is deactivated and excluded from routing. Nothing settles it. Two epochs later the chain splits the deposit per slot.

Expected: an escrow that cannot be served is still settled before its settlement window closes, with the hosts' real stats.

</div>

---

> 🔄 **Auto-synced** from [Issue #2039](https://github.com/gonka-ai/gonka/issues/2039) every hour.
