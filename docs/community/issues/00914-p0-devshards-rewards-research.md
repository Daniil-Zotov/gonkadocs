---
title: "#914 — [P0] `devshards` rewards (research)"
source: https://github.com/gonka-ai/gonka/issues/914
issue_number: 914
synced_at: 2026-08-05T14:40:01Z
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
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-18 10:43 UTC</span>
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
    <span><a href="https://github.com/dcastro">@dcastro</a></span>
    <span class="issues-meta-item">commented 2026-03-19 14:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Current situation</h2>
<p>There are 2 kinds of rewards for inferences done on-chain (outside of <code>devshards</code>):
* <code>WorkCoins</code>: transferred from the user to hosts. It's a direct payment for work done running inferences.
* <code>RewardCoins</code>: mined coins distributed to hosts, proportional to their weight.
  * These do not increase/decrease with the number of inferences done.
* Above a certain threshold of <code>Missed</code> inferences, <code>RewardCoins</code> may be cut to 0.
  * See: <code>CheckAndPunishForDowntimeForParticipants</code>
* Additionally, if <code>Missed</code> inferences or <code>Invalidated</code> inferences are above certain threshold, the protocol will mark the host as <code>ParticipantStatus_INACTIVE</code> or <code>ParticipantStatus_INVALID</code>, and both their <code>WorkCoins</code> and <code>RewardCoins</code> will also be cut to 0.
  * See <code>status.go</code>: <code>ComputeStatus</code>, <code>getInvalidationStatus</code>, <code>getInvalidationStatus</code></p>
<p>At the moment:
* <code>devshards</code> settlements distribute <code>WorkCoins</code> immediately after settlement
  * This distribution does not take <code>INACTIVE/INVALID</code> statuses into account
* <code>devshards</code> stats don't count towards <code>RewardCoins</code></p>
<h2>Goals</h2>
<p>We want to treat <code>devshards</code> settlements the same way as onchain inferences.
* The <code>devshards</code>'s stats (<code>Missed</code>/<code>Invalidated</code>) should count towards setting the host as <code>INACTIVE/INVALID</code>, and thus potentially cutting both their <code>WorkCoins</code> and <code>RewardCoins</code>
* <code>WorkCoins</code> should be distributed at the end of the epoch, rather than immediately</p>
<h2>Attack vectors</h2>
<p>When a dishonest host hijacks a <code>devshards</code>, they can:
  * Manipulate their own <code>SubnetSettlementHostStats.Cost</code>.
    * They can exploit this to drain the user's escrow, without spending GPU power on running inferences
    * This profit is currently limited: the protocol checks that <code>Cost</code> cannot exceed the escrow amount. See: <code>VerifySubnetSettlement</code>
  * Manipulate other host's <code>SubnetSettlementHostStats.Invalid</code>
    * This damage is not currently limited, <code>SettleSubnetEscrow</code> does not perform any checks on this field.
  * Manipulate other host's <code>SubnetSettlementHostStats.Missed</code>
    * This damage is not currently limited, <code>SettleSubnetEscrow</code> does not perform any checks on this field.</p>
<p>They cannot:
  * Increase their <code>RewardCoins</code> for the epoch: these are tied to the host's weight.</p>
<p>There are two ways a dishonest actor can land in a <code>devshards</code> vulnerable to hijacking:
* By pure chance. This chance is higher when the host has higher weight / the <code>devshards</code> is smaller in size.
* By "grinding <code>devshards</code>". The actor acts as both Host and User, and repeatedly creates/settles <code>devshards</code>, without performing any inferences, until they land in a vulnerable <code>devshards</code>.
  * Note that, in this scenario, the actor cannot profit from the attack by manipulating <code>SubnetSettlementHostStats.Cost</code>, since they'd only be transferring tokens from their User account to their Host account.</p>
<h2>Solution</h2>
<p>In order for <code>devshards</code>'s stats to be safely aggregated with epoch-level stats, we need to:
* When a host lands on a vulnerable <code>devshard</code> by chance, limit the damage they can do to other hosts' <code>Missed</code>/<code>Invalidated</code> inference count.
* Prevent dishonest actors from grinding <code>devshards</code> to augment damage done to other hosts.</p>
<h3>Limit <code>Missed</code> / <code>Invalidated</code></h3>
<p>These counters should be capped to their proportional share of the amount of inferences.</p>
<p>E.g. if, given the amount of tokens put into escrow, we infer that at most 500 inferences can be run, then a Host's <code>Missed+Invalidated</code> cannot be greater than (500 inferences / 128 slots * host's slot count).</p>
<p>If we cannot infer how many inferences can be run from a given escrow amount, then:
* The user can specify in <code>MsgCreateSubnetEscrow</code> how many inferences they plan on running. They can request inferences until either the escrow amount is depleted or the inference limit is reached, whichever happens first.</p>
<h3><code>devshards</code> fee</h3>
<p>Having a fee on creation/settlement of <code>devshards</code> would discourage dishonest actors from grinding <code>devshards</code> to damage other hosts.</p>
<p>Notes:
* The fee must be paid even if there are no inference requests, to prevent actors from repeatedly creating+closing <code>devshards</code>.
* The fee should not scale with the number of requests performed (to encourage users to create <code>devshards</code> with bigger escrow amounts instead of a lot of smaller ones)</p>
<p>A simple approach could be to pay <code>N</code> tokens per Host in the network, paid upon settlement.</p>
<p><strong>Question</strong>: how should we quantify this fee?
In general, fees need to be greater than the theoretical profit in order to discourage a given behaviour.
However, this attack is not profit-driven.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/dcastro">@dcastro</a></span>
    <span class="issues-meta-item">commented 2026-03-19 18:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Meeting Notes 2026/03/19</p>
<ul>
<li>Total RewardCoins for one whole epoch is 300k GNK, split by weight across all ACTIVE participants.</li>
<li>Let's say the dishonest actor has to create 3k <code>devshards</code> to be able to exploit one (with 99% confidence)</li>
<li>
<p>The total cost to create 3k <code>devshards</code> should be 300k GNK</p>
<ul>
<li>It's a function of 300k and the <code>devshards</code> size</li>
<li>300k is equal to the maximum damage the actor can do</li>
</ul>
</li>
<li>
<p>Limiting <code>Missed</code> / <code>Invalidated</code>: For now, let's say each <code>devshards</code> can run up to 2k inferences.</p>
</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The research part will be in Progress, but doesn't block the implementation. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #914](https://github.com/gonka-ai/gonka/issues/914) every hour.
