---
title: "#1867 — Feature: Expose lightweight ParticipantWeight query to CosmWasm (AcceptedGrpcQueries)"
source: https://github.com/gonka-ai/gonka/issues/1867
issue_number: 1867
synced_at: 2026-09-30T13:53:00Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Feature: Expose lightweight ParticipantWeight query to CosmWasm (AcceptedGrpcQueries)
    <span class="issues-number">#1867</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/DmitriyVoronov00">@DmitriyVoronov00</a> opened 2026-09-28 11:12 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-28 16:55 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

I am working on an open-source compute weight swap and escrow mechanism for the Gonka network (GonkaWeightSwap), which allows node operators and capital providers to trustlessly agree on compute weight delivery in exchange for USDT, completely within the Gonka protocol (no external oracles or trusted off-chain relayers).

To enable CosmWasm contracts to verify performance on-chain, contracts need to read two core metrics:
1. The current / completed epoch number.
2. The weight achieved by a specific participant address in a given epoch.

To introduce the concept, the motivation, and how this expands the Gonka ecosystem, I have prepared a video pitch:
🎥 Video Pitch & Concept Overview: https://youtu.be/L3RNyd-STwo

---

### Motivation & Use Case

Currently, connecting hardware operators with outside capital relies heavily on off-chain trust, manual settlements, or complex legal agreements.

An on-chain escrow contract solves this by locking investor funds and releasing them dynamically as node operators deliver verified weight to the investor's designated address. However, CosmWasm currently cannot query the inference module's epoch/weight state directly.

---

### Why Not Just Allowlist EpochGroupData?

While `/inference.inference.Query/EpochGroupData` exists, having a CosmWasm contract query and deserialize the entire participant array has major drawbacks:
- O(N) Gas & Memory Overhead: As the network grows to hundreds or thousands of participants, passing the full array into the WASM runtime will exceed contract gas limits or cause out-of-memory errors.
- Contract Complexity: Parsing huge protobuf messages inside CosmWasm contracts creates unnecessary friction and gas waste for end users.

---

### Proposed Solution: Targeted O(1) Query

I propose adding a lightweight, gas-efficient endpoint to the inference query service and exposing it to CosmWasm:

1. New query method in x/inference:
   - Method: `rpc ParticipantWeight(QueryParticipantWeightRequest) returns (QueryParticipantWeightResponse);`
   - Request: `uint64 epoch`, `string participant`
   - Response: `uint64 weight`, `bool found`
   - Implementation detail: This directly looks up the participant in the epoch's KV store in O(1) time without serializing the rest of the network's participants.

2. Allowlist in x/wasm (AcceptedGrpcQueries):
   - `/inference.inference.Query/GetCurrentEpoch`
   - `/inference.inference.Query/ParticipantWeight`

---

### Benefits to Gonka

- Zero Security Risk: Both queries are strictly read-only against already finalized KV storage.
- Gas & Network Safe: Constant-time execution prevents block bloat and gas exhaustion attacks.
- Ecosystem Growth: Unlocks a decentralized market for compute rentals, attracts external capital into node operations, and encourages hardware competition.

---

### Next Steps

I would love to get your feedback on this approach!

I am happy to collaborate with the core team, share more details on the product mechanics, and discuss how this feature solves real liquidity and compute allocation challenges for Gonka participants.

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/DmitriyVoronov00">@DmitriyVoronov00</a></span>
    <span class="issues-meta-item">commented 2026-09-28 14:39 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Following up on this: I noticed that PR #1758, merged into <code>upgrade-v0.2.16</code>, already exposes <code>GetCurrentEpoch</code> and <code>EpochPerformanceSummaryByParticipant</code> to CosmWasm. This is a very important step for marketplace and escrow-style contracts.</p>
<p>Looking at the current protobuf definition, <code>EpochPerformanceSummary</code> already provides per-participant stats for a completed epoch, including inference counts, rewards, missed requests, and claim status. However, it does not currently include the participant's finalized compute <code>weight</code>.</p>
<p><strong>Proposed option</strong></p>
<p>Instead of introducing a completely new query endpoint, would it be feasible to extend the existing <code>EpochPerformanceSummary</code> with a weight field?</p>
<pre><code>uint64 weight = 11;
</code></pre>
<p>This would allow a CosmWasm contract to read, through the already exposed <code>EpochPerformanceSummaryByParticipant</code> query:</p>
<ul>
<li>the completed epoch;</li>
<li>the specific participant;</li>
<li>performance and reward-related statistics;</li>
<li>the participant's finalized compute weight for that epoch.</li>
</ul>
<p><strong>Why this may be the simplest approach</strong></p>
<ol>
<li><strong>No additional public query endpoint:</strong> the contract-facing query is already exposed in PR #1758.</li>
<li><strong>Low overhead:</strong> <code>EpochPerformanceSummaryByParticipant</code> is already a targeted per-participant, per-epoch lookup rather than a full-network participant list.</li>
<li><strong>Consistent settlement data:</strong> contracts can evaluate performance, reward status, and delivered compute weight from one authoritative epoch summary.</li>
<li><strong>Useful beyond one application:</strong> this could support escrow agreements, compute marketplaces, reward accounting, and other contracts based on completed epoch outcomes.</li>
</ol>
<p>For GonkaWeightSwap specifically, the contract needs the finalized weight of the configured reward-recipient address in order to determine whether the host met the agreed delivery conditions.</p>
<p>Would adding <code>weight</code> to <code>EpochPerformanceSummary</code> be feasible for an upcoming upgrade? I would be very interested in the view on whether this fits the intended meaning and lifecycle of this record.</p>
<p>cc @niktverd</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/niktverd">@niktverd</a></span>
    <span class="issues-meta-item">commented 2026-09-28 16:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ul>
<li>
<p>Yes, this looks feasible. The summary is created during epoch settlement, so it is a good place to store the final weight.</p>
</li>
<li>
<p>We can use the existing query. No new endpoint is needed.</p>
</li>
<li>
<ul>
<li>We already calculate ParticipantRewardWeight after caps, penalties, and delegation reward transfers. We should confirm if this is the weight GonkaWeightSwap needs.</li>
</ul>
</li>
<li>
<p>The query uses the participant address. A separate reward recipient does not get that participant’s summary.</p>
</li>
<li>
<p>We also need to handle old epochs: a missing weight must not be treated as a real zero.</p>
</li>
<li>For GonkaWeightSwap, do you need confirmed compute weight or the final weight used for rewards?</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/DmitriyVoronov00">@DmitriyVoronov00</a></span>
    <span class="issues-meta-item">commented 2026-09-28 16:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks so much for the quick and insightful feedback, @niktverd! This is super helpful.</p>
<p>Here are the specifics regarding our use case:</p>
<ol>
<li>
<p><strong>Weight type (<code>ParticipantRewardWeight</code> vs compute weight):</strong>
   <strong><code>ParticipantRewardWeight</code> (the final weight used for rewards) is exactly what GonkaWeightSwap needs.</strong>
   The core purpose of the escrow is to ensure the investor pays for actual, rewarded network contribution. If a node suffers penalties, slashing, or caps during the epoch, the escrow settlement should reflect the net rewarded weight rather than raw compute. Having <code>reward_weight</code> (and optionally raw compute weight if convenient) in <code>EpochPerformanceSummary</code> fits this perfectly.</p>
</li>
<li>
<p><strong>Participant address vs reward recipient:</strong>
   Thank you for highlighting this! Since the deal in the escrow contract tracks both parties (the host operator and the investor), the contract can directly query by the host's <code>participant</code> address to verify the epoch performance.</p>
</li>
<li>
<p><strong>Handling legacy epochs:</strong>
   Makes total sense. On the contract side, we will ensure that settlement only queries epochs from the agreement start onwards, and will treat unpopulated/legacy values as unsupported rather than an intentional zero.</p>
</li>
</ol>
<p>Would you prefer to include this field update directly in <code>upgrade-v0.2.16</code>, or would it help if I opened a PR against the upgrade branch?</p>
<p>Really appreciate your help and guidance on this!</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1867](https://github.com/gonka-ai/gonka/issues/1867) every hour.
