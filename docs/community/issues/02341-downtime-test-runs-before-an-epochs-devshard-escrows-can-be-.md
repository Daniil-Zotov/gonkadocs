---
title: "#2341 — Downtime test runs before an epoch's devshard escrows can be settled: in epochs 455–468 it saw 11% of requests, and 5 of its 12 penalties hit hosts below the threshold"
source: https://github.com/gonka-ai/gonka/issues/2341
issue_number: 2341
synced_at: 2026-11-27T02:16:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Downtime test runs before an epoch's devshard escrows can be settled: in epochs 455–468 it saw 11% of requests, and 5 of its 12 penalties hit hosts below the threshold
    <span class="issues-number">#2341</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/gafrustam">@gafrustam</a> opened 2026-11-26 07:10 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-26 07:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
#1069 made devshard settlements feed `CurrentEpochStats`, because without it devshard work did not reach the stats "which are critical for accurate network performance tracking, rewards, and voting power". On mainnet this path almost never works: the downtime test of an epoch runs before that epoch's escrows can be settled. In epochs 455–468 the test saw 11.4% of devshard requests. It still issued 12 penalties, and 5 of them hit hosts that pass the test on all of the epoch's escrows.

### Why the test cannot see most escrows

- `SettleAccounts(N)` runs at the next PoC start + 280. Epoch N ends at + 399 (`epoch_group_data/N` → `last_block_height`). So the test of epoch N runs about 11 minutes before epoch N ends. This holds for every epoch from 455 to 468.
- Escrows of epoch N keep serving until the end of the epoch. The gateway treats the PoC as epoch N (`deriveEffectiveEpochIndex`). The chain also keeps creating epoch-N escrows during the next PoC, 59–203 per epoch in 458–468, and some are created after `SettleAccounts(N)`: escrow 184433 (epoch 466) was created at 7199284 and served 760 nonces, while `SettleAccounts(466)` ran at 7199232.
- The gateways settle these escrows when the epoch ends. That is what was planned: in #1000 akup wrote "we should force finalization of a `devshard` when epoch ends", and the gateway's previous-epoch mode settles an escrow "only once its chain epoch E is over, never in E itself" (`devshard/cmd/gateway/docs/escrows.md` on `devshard/v7`). Since epoch 458 the first settlement comes 2–5 blocks after the epoch ends. In epoch 466 no escrow was settled between 7199232 and 7199351, and the first settlement came at 7199355.
- By then `treatAsCurrentEpochSettle` is false, either because the escrow is from the previous epoch or because the epoch summary already exists. The misses then go only to `DevshardHostEpochStatsMap`, and no reward or penalty rule reads it.

So the test of epoch N sees only the escrows a gateway happened to close in the middle of the epoch. In every epoch these came from one or two gateways.

### Mainnet, epochs 455–468

I rebuilt per-host totals from every `MsgSettleDevshardEscrow` (`nonce`, `host_stats`) and the escrow's slots, using `devshardAssignedUpperBoundForSlot`. The part settled before `SettleAccounts` matches `epoch_performance_summary` exactly for every host in all 14 epochs. The total misses agree with `devshard_host_epoch_stats` to within one miss per host, once misses waived during PoC challenges (epochs 456 and 463) are taken out. "All escrows" below means every settled escrow of the epoch, run through the same test (`getDynamicP0` and `MissedStatTest`).

| epoch | requests the test saw | penalties | of them pass on all escrows | fail on all escrows, full reward |
|---|---|---|---|---|
| 455 | 12.5% | 2 | 0 | 0 |
| 456 | 0 | 0 | – | 3 |
| 457 | 29.3% | 1 | 1 | 0 |
| 458 | 21.1% | 1 | 0 | 0 |
| 459 | 0.2% | 2 | 1 | 2 |
| 460 | 23.9% | 3 | 0 | 0 |
| 461 | 67.4% | 0 | – | 0 |
| 462 | 21.3% | 0 | – | 0 |
| 463 | 0 | 0 | – | 1 |
| 464 | 0.9% | 0 | – | 0 |
| 465 | 0 | 0 | – | 0 |
| 466 | 5.7% | 3 | 3 | 1 |
| 467 | 0 | 0 | – | 1 |
| 468 | 0 | 0 | – | 1 |
| **all** | **11.4%** | **12** | **5** | **9** |

The last column leaves out hosts whose reward was 0 for other reasons. It also leaves out one host with a weight under 200, which fails in 7 epochs for 7–20 GNK each time.

The five penalties that hit hosts below the threshold:

| epoch | host | what the test used | all escrows of the epoch |
|---|---|---|---|
| 457 | …j4vh7v62 | 15.1% of 58,053, all from gateway …vsewfflt | 8.1% of 233,199 |
| 459 | …sh8rvmw4 | 18.5% of 189, from 8 escrows of …s35lat8n | 2.8% of 117,773 |
| 466 | …c9rcu3rp | 16.8% of 43,949, all from …vsewfflt | 5.5% of 315,061 |
| 466 | …mkxkvu25 | 15.2% of 45,534, all from …vsewfflt | 6.3% of 317,112 |
| 466 | …mh4v49fm | 14.3% of 36,004, all from …vsewfflt | 4.5% of 325,945 |

Each of them lost the whole epoch reward. Together that is about 52k GNK, estimated as weight times the epoch's median reward per unit of weight. Failing the test also zeroes the host's previous confirmed weight (`zeroFailedMissRateWeights`). Because of that, …sh8rvmw4 had no voting power for all of epoch 460, although it was in the epoch with weight 78,674. The three hosts from 466 had none for all of 467, and in 466 they held 7.5% of the voting power. They came back in 468.

In 466 these three missed 15–19% of requests in …vsewfflt's escrows and about 2% in …p6demv90's, which sent each of them about 200k requests. The test used only the 64 escrows that …vsewfflt settled in one batch in the middle of the epoch. In the same epoch …twex0gz9 missed 10.4% of 287,926 requests (8–16% at every gateway that sent it more than 5,000) and got its full reward. It was over the threshold in 467 (15.2%) and 468 (11.6%) as well, and it got its full reward each time.

### How this differs from #1087, #1000 and #1078

- #1087 keeps escrows of a previous epoch out of the current epoch's stats. That is right, and it is a different case. Here an epoch's own escrows cannot reach that epoch's test.
- #1000 ("we anyway cannot punish for previous epoch") is about epochs whose rewards are already paid. Here epoch N is tested on its own data, but only on a remnant.
- In #1078 a host with no requests passes the test. Here the hosts had hundreds of thousands of requests.

There are two possibilities, and today's behaviour fits neither. If devshard misses are meant to count, the test misses 90% of them and punishes on the rest. If they are not meant to count yet, the 12 penalties should not have happened. As it is, which hosts get tested depends on which escrows a gateway settles before `SettleAccounts`, not on how the hosts served.

The code involved (`msg_server_settle_devshard_escrow.go`, `accountsettle.go`, `bitcoin_rewards.go`, `devshard_host_stats.go`) is the same on `upgrade-v0.2.17`, `upgrade-v0.2.18-sdk`, `devshard/v7`, `testnet/main` and `main`.

### Possible fixes

1. Decide epoch N's downtime at `SettleAccounts(N+1)` from `DevshardHostEpochStats(N)`. The chain accepts a settlement only in the escrow's epoch and the next one, so by then every epoch-N escrow that will ever settle has settled. On mainnet all of them did. This needs an assigned count per host in `DevshardHostEpochStats`, which `devshardAssignedUpperBoundForSlot` already gives. The penalty would then apply to the N+1 reward and weight.
2. Until then, do not run the test on a remnant: skip the devshard part when most of the epoch's escrows are still unsettled at `SettleAccounts`.

I can open a PR for either once you pick one.

### How to check

- `epoch_group_data/466` → `last_block_height` 7199351. `epoch_performance_summary/466/gonka12jurnq3mlwgnfd7ssrmr9p9nl3dltfc9rcu3rp` with header `x-cosmos-block-height: 7199231` → not found. With 7199232 → `inference_count` 36560, `missed_requests` 7389, `rewarded_coins` 0.
- `tx_search "message.action='/inference.inference.MsgSettleDevshardEscrow' AND tx.height>=7199232 AND tx.height<=7199351"` → 0 results. The first settlement after that is at 7199355.
- `tx_search "devshard_escrow_created.escrow_id='184433'"` → height 7199284, `epoch_index` 466.
- `devshard_host_epoch_stats/466/gonka12jurnq3mlwgnfd7ssrmr9p9nl3dltfc9rcu3rp` with `x-cosmos-block-height: 7214342` → `missed` 17279. All escrows of the epoch give this host 315,061 assigned requests.
- CometBFT `/validators?height=7207000` (epoch 467) has no validator for …c9rcu3rp, …mkxkvu25 or …mh4v49fm. `height=7192000` (466) and `height=7222000` (468) have all three.

</div>

---

> 🔄 **Auto-synced** from [Issue #2341](https://github.com/gonka-ai/gonka/issues/2341) every hour.
