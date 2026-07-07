---
title: "#914 — [P0] `devshards` rewards (research)"
source: https://github.com/gonka-ai/gonka/issues/914
issue_number: 914
synced_at: 2026-07-07T04:29:08Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards` rewards (research)
    <span class="issues-number">#914</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@dcastro](https://github.com/dcastro) opened 2026-03-18 10:43 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-04-02 12:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
## Tasks

- [ ] Calculate what the fee on `devshards` should be for different `devshard` sizes
- [ ] Decide what we're going to implement
- [ ] Implement: (tentative plan)
    * Calculate and charge fee for `devshards`
        * Initial impl: create_fee + max_nonce * fee_per_nonce
            * Charging per nonce -> mechanism to deter from spamming the network with small inf requests
        * Ensure escrow amount covers the fee
        * Ensure the escrow balance never goes below the fee
        * Charge the fee upon settlement
    * Distribute `WorkCoins` at the end of the epoch, instead of upon settlement.
    * Take `devshard` stats into account when calculating punishments `WorkCoins`/`RewardCoins`


## Research

* [`devshards` - rewards and attack vectors](https://www.notion.so/serokell/Subnets-rewards-and-attack-vectors-3256c9c166b38058a312fa50ebfb102f)
* [`devshards` - security analysis](https://www.notion.so/serokell/Subnets-security-analysis-31b6c9c166b380d8b30ed73dfe28c0b2)
* [`devshards` - security analysis (Part 2: rewards)](https://www.notion.so/serokell/Subnets-security-analysis-Part-2-rewards-32c6c9c166b380bfb2b9dc0b7e32ad32)
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dcastro](https://github.com/dcastro)</span>
    <span class="issues-meta-item">commented 2026-03-19 14:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    ## Current situation

There are 2 kinds of rewards for inferences done on-chain (outside of `devshards`):
* `WorkCoins`: transferred from the user to hosts. It's a direct payment for work done running inferences.
* `RewardCoins`: mined coins distributed to hosts, proportional to their weight.
  * These do not increase/decrease with the number of inferences done.
* Above a certain threshold of `Missed` inferences, `RewardCoins` may be cut to 0.
  * See: `CheckAndPunishForDowntimeForParticipants`
* Additionally, if `Missed` inferences or `Invalidated` inferences are above certain threshold, the protocol will mark the host as `ParticipantStatus_INACTIVE` or `ParticipantStatus_INVALID`, and both their `WorkCoins` and `RewardCoins` will also be cut to 0.
  * See `status.go`: `ComputeStatus`, `getInvalidationStatus`, `getInvalidationStatus`

At the moment:
* `devshards` settlements distribute `WorkCoins` immediately after settlement
  * This distribution does not take `INACTIVE/INVALID` statuses into account
* `devshards` stats don't count towards `RewardCoins`

## Goals

We want to treat `devshards` settlements the same way as onchain inferences.
* The `devshards`'s stats (`Missed`/`Invalidated`) should count towards setting the host as `INACTIVE/INVALID`, and thus potentially cutting both their `WorkCoins` and `RewardCoins`
* `WorkCoins` should be distributed at the end of the epoch, rather than immediately

## Attack vectors


When a dishonest host hijacks a `devshards`, they can:
  * Manipulate their own `SubnetSettlementHostStats.Cost`.
    * They can exploit this to drain the user's escrow, without spending GPU power on running inferences
    * This profit is currently limited: the protocol checks that `Cost` cannot exceed the escrow amount. See: `VerifySubnetSettlement`
  * Manipulate other host's `SubnetSettlementHostStats.Invalid`
    * This damage is not currently limited, `SettleSubnetEscrow` does not perform any checks on this field.
  * Manipulate other host's `SubnetSettlementHostStats.Missed`
    * This damage is not currently limited, `SettleSubnetEscrow` does not perform any checks on this field.

They cannot:
  * Increase their `RewardCoins` for the epoch: these are tied to the host's weight.


There are two ways a dishonest actor can land in a `devshards` vulnerable to hijacking:
* By pure chance. This chance is higher when the host has higher weight / the `devshards` is smaller in size.
* By "grinding `devshards`". The actor acts as both Host and User, and repeatedly creates/settles `devshards`, without performing any inferences, until they land in a vulnerable `devshards`.
  * Note that, in this scenario, the actor cannot profit from the attack by manipulating `SubnetSettlementHostStats.Cost`, since they'd only be transferring tokens from their User account to their Host account.

## Solution

In order for `devshards`'s stats to be safely aggregated with epoch-level stats, we need to:
* When a host lands on a vulnerable `devshard` by chance, limit the damage they can do to other hosts' `Missed`/`Invalidated` inference count.
* Prevent dishonest actors from grinding `devshards` to augment damage done to other hosts.

### Limit `Missed` / `Invalidated`

These counters should be capped to their proportional share of the amount of inferences.

E.g. if, given the amount of tokens put into escrow, we infer that at most 500 inferences can be run, then a Host's `Missed+Invalidated` cannot be greater than (500 inferences / 128 slots * host's slot count).

If we cannot infer how many inferences can be run from a given escrow amount, then:
* The user can specify in `MsgCreateSubnetEscrow` how many inferences they plan on running. They can request inferences until either the escrow amount is depleted or the inference limit is reached, whichever happens first.

### `devshards` fee

Having a fee on creation/settlement of `devshards` would discourage dishonest actors from grinding `devshards` to damage other hosts.

Notes:
* The fee must be paid even if there are no inference requests, to prevent actors from repeatedly creating+closing `devshards`.
* The fee should not scale with the number of requests performed (to encourage users to create `devshards` with bigger escrow amounts instead of a lot of smaller ones)

A simple approach could be to pay `N` tokens per Host in the network, paid upon settlement.

**Question**: how should we quantify this fee?
In general, fees need to be greater than the theoretical profit in order to discourage a given behaviour.
However, this attack is not profit-driven.


  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dcastro](https://github.com/dcastro)</span>
    <span class="issues-meta-item">commented 2026-03-19 18:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    
Meeting Notes 2026/03/19

* Total RewardCoins for one whole epoch is 300k GNK, split by weight across all ACTIVE participants.
* Let's say the dishonest actor has to create 3k `devshards` to be able to exploit one (with 99% confidence)
* The total cost to create 3k `devshards` should be 300k GNK
    * It's a function of 300k and the `devshards` size
    * 300k is equal to the maximum damage the actor can do

* Limiting `Missed` / `Invalidated`: For now, let's say each `devshards` can run up to 2k inferences.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@KKizilov](https://github.com/KKizilov)</span>
    <span class="issues-meta-item">commented 2026-03-26 15:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    The research part will be in Progress, but doesn't block the implementation. 
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #914](https://github.com/gonka-ai/gonka/issues/914) every hour.
