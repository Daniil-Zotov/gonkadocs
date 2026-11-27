---
title: "#2300 — Gas simulation misses ~24k gas on paid MsgVote; --gas-adjustment 1.5 votes fail on v0.2.18"
source: https://github.com/gonka-ai/gonka/issues/2300
issue_number: 2300
synced_at: 2026-11-27T02:17:04Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gas simulation misses ~24k gas on paid MsgVote; --gas-adjustment 1.5 votes fail on v0.2.18
    <span class="issues-number">#2300</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-20 09:41 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-20 09:42 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`--gas auto` underestimates a paid `MsgVote` by a fixed ~24,072 gas. With `--gas-adjustment 1.5`, votes passed only by a 0.07% margin before v0.2.18. v0.2.18 lowered the vote's base cost by 1,973 gas, so the same 24,072 now exceeds the 1.5× headroom and votes fail with out of gas. CheckTx still returns `code=0`, so the failure is silent for the sender.

## Evidence (gonka-testnet-4, same voters, same harness, identical votes)

| Votes | Simulated | Used | Used − simulated | Used / simulated | Result at 1.5× |
|---|---:|---:|---:|---:|---|
| Proposals 6–10, v0.2.17 (heights 109575–153892) | 48,236 | 72,308 | 24,072 | 1.499 | pass (49–97 gas spare) |
| Proposal 12, v0.2.18 (height 155071) | 46,263 | 70,335 | 24,072 | 1.520 | `code=11` |

```
out of gas in location: WritePerByte; gasWanted: 69547, gasUsed: 70437: out of gas
```

- The gap is identical before and after the upgrade. v0.2.18 only moved both values down by 1,973.
- Re-voting with `--gas-adjustment 2.0` works: 92,730 wanted, 70,437 used.
- PoC messages are unaffected. Paid ones (`MsgPoCV2StoreCommit`, `MsgSubmitHardwareDiff`) are simulated to within ~5% (wanted/used = 1.43 at 1.5×). Fee-exempt ones use fixed gas limits.

## Likely cause (not confirmed)

Simulation runs with a zero fee, but the real tx pays `fee = gas_wanted × 1ngonka`. So the fee deduction (a bank transfer to the fee collector, which costs `WritePerByte`) is charged only on execution. Supporting clue: fee-0 votes on the same chain use ~50.7k gas, against ~72.4k for paid votes.

## Impact

Any script, guide or wallet that votes, or sends other small paid txs, with `--gas-adjustment 1.5` now fails silently on v0.2.18.

## Suggested fix

- Include the fee deduction in the simulation (simulate with a non-zero fee), or add a fixed fee-deduction margin to the estimate.
- Until then, document `--gas-adjustment 2.0` as the minimum for votes.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-20 09:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian fyi, minor</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2300](https://github.com/gonka-ai/gonka/issues/2300) every hour.
