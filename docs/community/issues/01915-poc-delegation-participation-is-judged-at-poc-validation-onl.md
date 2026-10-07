---
title: "#1915 — PoC delegation: participation is judged at PoC validation only, so a "bait" node switched off right after PoC still collects the 5% share (or escapes the 15% penalty) for the whole epoch"
source: https://github.com/gonka-ai/gonka/issues/1915
issue_number: 1915
synced_at: 2026-10-07T22:04:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    PoC delegation: participation is judged at PoC validation only, so a "bait" node switched off right after PoC still collects the 5% share (or escapes the 15% penalty) for the whole epoch
    <span class="issues-number">#1915</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Aktum1">@Aktum1</a> opened 2026-10-04 15:52 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-04 15:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Per-model participation (`DIRECT` / `DELEGATE` / `NONE`) is decided once, at the end of PoC validation: a host is `DIRECT` for a model iff it has an ML node with weight in that model's group, and a delegation is valid iff its target is such a member. From that moment the outcome is frozen for the epoch: the delegators' `delegation_share` (5%) is transferred to the receiver at settlement, and `DIRECT` hosts are exempt from `no_participation_penalty` (15%), no matter what happens to the node afterwards. Nothing checks that the node survived cPoC or served a single request.

Three consequences, one already observed on mainnet, two open incentives:

1. **Observed (epochs 412–414).** A receiver with a single DeepSeek node fails cPoC every epoch and ends the epoch `INACTIVE` with reward 0. Its delegators are still charged 5%; the transfer lands on a zero balance and burns. Delegators get no 15% penalty, the receiver gets nothing, nobody served DeepSeek for them.
2. **Ghost receiver.** A host can run the *smallest possible* node for a model only through PoC, switch it off, and keep 5% of every delegator's reward for that model for the whole epoch. The cPoC ratio and the missed-request test are computed per host across all models, so a bait node below 50% of the host's weight (`alpha_threshold` = 0.5) never deactivates the host, and a tiny node attracts few inference requests. The weaker the bait node, the safer the strategy. Delegators cannot see it: their delegation stays valid and penalty-free.
3. **Penalty escape.** The same trick works the other way round. A host that does not want to serve model M would normally delegate M (and give away 5%) or pay the 15% penalty. Instead it runs a minimal node for M through PoC only, becomes `DIRECT`, shuts the node down, and pays nothing to anyone. `AccumulateDelegationPenalties` skips `DIRECT` participants unconditionally.

Both incentives reward the same behaviour: bring the weakest node you can get away with to PoC, then turn it off.

## How it works today (code)

- `x/inference/module/delegation_weight_calculator.go`, `ResolveGroupParticipation`: `DIRECT` iff the host is in `g.Members`; `DELEGATE` iff the target is in `g.Members` and `participates(target)`. Computed once in `onEndOfPoCValidationStage` and frozen in the `DelegationRewardTransferSnapshot`.
- `x/inference/module/delegation_weight_adjustment.go`, `AccumulateDelegationPenalties`: `case ModeDirect: continue` — no penalty for a `DIRECT` host, regardless of what its node does during the epoch.
- `x/inference/keeper/bitcoin_rewards.go`, `applyDelegationRewardTransfers`: at settlement `amount = share × baseRewardable[from]` is always subtracted from the delegator; it is added to `to` iff `participantWeights[to] > 0`. No per-model condition on the receiver.
- `x/inference/module/confirmation_poc.go`, `foldEventReadings` / `computeRatio`: cPoC haircut and `ConfirmationPoCRatio` are per participant (sum over all its nodes and models); deactivation only below `alpha_threshold` (0.5 on mainnet).
- `x/inference/module/module.go`, `handleExpiredInferenceWithContext`: missed requests are per participant, and `HasNodeForModel` checks the epoch's cached `ActiveParticipants`, so a node that is physically gone still counts as present. The downtime test at settlement (`CheckAndPunishForDowntime`) is host-wide as well.

So the only thing a host has to do to be paid for a model (or to be excused from its penalty) is to have a node with weight in that model's group at PoC validation.

## Mainnet evidence (epoch 413 settlement, our network node log)

Receiver `gonka10thh6z0wvq9c05j4z3f9qtpxxedruqn5ae350k` (DeepSeek, 1 GPU, weight 2461 in epoch 413; 10 nodes / 47 GPUs registered, one producing PoC). Delegators for DeepSeek: `gonka1ajmhqgvkf76hss5xe35kcnntqqhs7r8jz8s939` (weight 33450), `gonka19wskgkz4xwwxa9s80nfx4q97w2ucmcyfezmhjk` (2800), `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` (1731), all three active and confirmed in that epoch.

```
04:10 INF Invalid/inactive participant found, will not receive rewards but counts in denominator fullWeight=2461 participant=gonka10thh6z…
04:10 INF Bitcoin Rewards: applied reward-only delegation transfer amount=86   from=gonka1830lqug5… modelId=deepseek-ai/DeepSeek-V4-Flash-0731 to=gonka10thh6z…
04:10 INF Bitcoin Rewards: applied reward-only delegation transfer amount=140  from=gonka19wskgkz4… modelId=deepseek-ai/DeepSeek-V4-Flash-0731 to=gonka10thh6z…
04:10 INF Bitcoin Rewards: applied reward-only delegation transfer amount=1672 from=gonka1ajmhqgvk… modelId=deepseek-ai/DeepSeek-V4-Flash-0731 to=gonka10thh6z…
04:10 INF Bitcoin Rewards: weights after delegation reward transfers … "gonka10thh6z…":0 …
09:51 WRN Participant deactivated for downtime address=gonka10thh6z… reason=failed_confirmation_poc stats="… confirmationPoCRatio:<exponent:-16 >"
```

1898 units of rewardable weight (≈ 620 GNK at that epoch's emission) were taken from the three delegators and credited to a participant with rewardable weight 0, i.e. burned. The same receiver was `DIRECT` for DeepSeek again in epoch 414 (`weight_pipeline … modes=…deepseek-ai/DeepSeek-V4-Flash-0731:DIRECT … final=1358`) and was deactivated again at the first cPoC. Over the last 12 epochs it had 0 epochs with a non-zero reward, 3 epochs absent and 8 epochs present-and-zeroed. Delegators keep paying.

### Explorer view

Receivers table for epoch 413 on https://ranking.gonkadb.com/delegations?epoch=413 ("Validated weight" is the host's last cPoC confirmation weight; "Share" is the delegators' 5% estimated from their weight and the epoch emission):

| Receiver | Runs | Weight | Validated weight | Delegators | Delegated weight | Share ≈ GNK / epoch | % of network reward |
|---|---|---|---|---|---|---|---|
| `gonka1gvrrhjmy4w…` | MiniMax, DeepSeek, GLM | 108,311 | 105,911 | 8 | 478,996 | 7,814 | 2.94% |
| `gonka1kx9mca3xm8…` | MiniMax, DeepSeek, GLM | 10,609 | 10,348 | 7 | 165,284 | 2,696 | 1.02% |
| `gonka1gvpv7vhk5g…` | DeepSeek | 2,850 | 2,599 | 6 | 118,298 | 1,930 | 0.73% |
| `gonka1gyk0aahvr3…` | MiniMax | 941 | 898 | 1 | 87,472 | 1,427 | 0.54% |
| `gonka16dgkvx7mh6…` | MiniMax, GLM | 47,591 | 47,482 | 4 | 55,269 | 902 | 0.34% |
| **`gonka10thh6z0wvq…`** | DeepSeek | 2,461 | **0 · deactivated** | 3 | 38,021 | **620** | 0.23% |
| `gonka168rtjfkszu…` | DeepSeek, GLM | 87,472 | 87,401 | 3 | 15,828 | 258 | 0.10% |
| `gonka1kvmerzu640…` | MiniMax | 45,865 | 45,392 | 1 | 2,850 | 46 | 0.02% |

The chain reports these three delegations as valid, so from the delegators' side nothing looks wrong.

This case is visible only because the bait node was the receiver's *whole* weight, so the host itself got deactivated. A host with a strong MiniMax fleet and one tiny DeepSeek node would show a normal validated weight, keep collecting the DeepSeek share, and be indistinguishable from an honest receiver with the data the chain exposes today (cPoC readings are published per host, not per model).

## Suggested fix (any of these closes the gap)

1. **Decide per-model participation at settlement, not at PoC validation.** Pay the share for model M (and grant the `DIRECT` exemption for M) only if the host's confirmation weight in M's subgroup after the last cPoC event is > 0, or its ML node for M is still in the epoch group and healthy. Otherwise treat the delegator as `NONE` for M (penalty applies, as if the receiver had never been there) — or at minimum do not charge the share — and apply `no_participation_penalty` to the host that dropped M.
2. **Pro-rate the share** by `confirmed_weight(receiver, M) / initial_weight(receiver, M)`, so a receiver that lost its node mid-epoch earns proportionally.
3. **Do not charge delegators when the receiver is `INACTIVE` / `INVALID` at settlement.** Today the amount is subtracted and burned (`participantWeights[to] == 0`), which penalises the delegator without benefiting anyone.
4. **Publish per-model cPoC results** (confirmation weight per model subgroup per host) and whether each transfer in `GetDelegationRewardTransfersForEpoch` will actually pay out, so explorers can warn delegators before the epoch settles.

Options 1 and 3 need no new state: the per-model `ValidationWeights[*].ConfirmationWeight` of the model subgroups and the participant status are already available in `SettleAccounts`.

## Environment

Mainnet, epochs 412–414 (2026-10-03/04). Network node `release/gateway/v4.1.2`. Chain params: `delegation_share` 0.05, `no_participation_penalty` 0.15, `confirmation_poc_params.alpha_threshold` 0.5, `expected_confirmations_per_epoch` 4, `maintenance_enabled` false.

---

If the project runs a bug bounty, I would be happy to receive a reward for this report in GNK.

</div>

---

> 🔄 **Auto-synced** from [Issue #1915](https://github.com/gonka-ai/gonka/issues/1915) every hour.
