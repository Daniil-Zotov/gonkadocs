---
title: "#823 — Bridge: Weak Dealer Approval Enables Threshold Signing DoS"
source: https://github.com/gonka-ai/gonka/issues/823
issue_number: 823
synced_at: 2026-07-28T14:45:22Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Bridge: Weak Dealer Approval Enables Threshold Signing DoS
    <span class="issues-number">#823</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-27 22:24 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-04-02 23:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
**Locations:** 
- https://github.com/gonka-ai/gonka/blob/82c43a42c3c2f49b56ee8a32e6458480daf39ca9/inference-chain/x/bls/keeper/phase_transitions.go#L169-L169
- https://github.com/gonka-ai/gonka/blob/82c43a42c3c2f49b56ee8a32e6458480daf39ca9/inference-chain/x/bls/keeper/threshold_signing.go#L296-L302

**Categories:** 
- Logical-issue
- Denial-of-service

**Description**
Dealer validation uses an unweighted majority of submitted DealerValidity votes and does not verify per-recipient shares against commitments. A malicious dealer can send valid shares to ~50% of recipients and garbage to the rest.

The dealer (or a colluder) can vote “true,” giving itself a bare majority among submitters (>50%). The dealer is marked "valid" and included in the group key even though many recipients lack usable shares.

`inference-chain/x/bls/keeper/phase_transitions.go`
<img width="623" height="641" alt="Image" src="https://github.com/user-attachments/assets/8a28c807-c91a-4e05-93fe-8df8ade73b12" />

<img width="625" height="586" alt="Image" src="https://github.com/user-attachments/assets/47c5ec37-08e3-4941-a4b9-582b0ea3e2cc" />

Later, the dealer (or colluder) withholds its partial signature, pushing the usable signers below the >50% slot threshold. Threshold-signing requests then stall and expire—a sustained liveness/DoS risk, even with <50% malicious participants plus abstentions.

`inference-chain/x/bls/keeper/threshold_signing.go`

<img width="623" height="315" alt="Image" src="https://github.com/user-attachments/assets/f1e6e0eb-99c4-48fd-9e73-9b467b686d1c" />
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-28 13:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to help with this </p>
<h1>825 (WIP)</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-03-02 05:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 Can you please explain, how does proof work in your implementation?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-03-02 11:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>It's not finished yet but what I already made:
1. Proof for true votes - when a participant votes true for a dealer, they must sign a message using shares they got from that dealer. The chain checks this signature against the dealer's public commitments. If signature is invalid or missing, the vote is rejected. So you can't vote true without actually having valid shares
2. Slot-weighted quorum - dealer approval is now counted by slots, not by number of participants. The dealer also can't approve itself</p>
<p>Also added a description to the PR</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-03-02 16:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<ol>
<li>Proof for true votes - when a participant votes true for a dealer, they must sign a message using shares they got from that dealer. The chain checks this signature against the dealer's public commitments. If signature is invalid or missing, the vote is rejected. So you can't vote true without actually having valid shares</li>
</ol>
</blockquote>
<p>But the real problem in the issue is, that participant should prove that they have invalid share.A malicious dealer can send valid shares to ~50% of recipients and garbage to the rest. Malicious dealer doesn't need that participants with invalid shares vote true for him, it isn't key for the attack.</p>
<p>And participants can open invalid shares to chain (as they are invalid they could be shown as they are not the secret) to prove the dealer is the attacker.
So participants should check first the share against commitment, and if it doesn't match, they should send the invalid share to chain, if there is at least one invalid share, exclude the attacker (taking his collateral)</p>
<p>p.s.:
It seams the problem is already solved here:
https://github.com/gonka-ai/gonka/commit/6211d32109e89a913d2070d05e54d7bbb6fe8951#diff-89c99e1a367a5b8cc41a94e676865a63e9ed86554cdbf04000b4d5297381b8f9</p>
<p>But InvalidDealers should be tracked there to take collateral from them and exclude from the epoch</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #823](https://github.com/gonka-ai/gonka/issues/823) every hour.
