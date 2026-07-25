---
title: "#394 — [P0] Invalid participants in the `ActiveParticipant` list"
source: https://github.com/gonka-ai/gonka/issues/394
issue_number: 394
synced_at: 2026-07-25T17:28:41Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Invalid participants in the `ActiveParticipant` list
    <span class="issues-number">#394</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-10-16 00:22 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2025-12-02 20:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Proper removal (Check that we also jail => no voting power)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2025-10-21 18:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>Invalid Participant Exclusion – Feature Specification</h1>
<h2><strong>Overview</strong></h2>
<p>This feature refines, fixes and fully tests the mechanism for handling <strong>invalid participants</strong> in the Gonka network. Invalid participants are nodes that have misbehaved (e.g., submitted bad inferences, misconfigured models, attempted cheating, or failed other behavioral criteria). The goal is to ensure they are <strong>excluded from all network responsibilities and consensus mechanisms</strong>, without retroactively altering cryptographically signed data.</p>
<hr />
<h2><strong>Problem Statement</strong></h2>
<p>Currently, the list of <strong>active participants</strong> retrieved from the chain <strong>could include nodes that are technically invalid</strong> for the current epoch. This list is <strong>signed and committed cryptographically</strong> each epoch, making it immutable and essential for trust and traceability via Merkle proofs.</p>
<p>However, since some participants may be no longer trustworthy (due to detected invalid behavior during the epoch), relying solely on the active list is not sufficient for selecting endpoints to use.</p>
<p>Additionally, when a participant is marked as invalid, we need to ensure and test that they are excluded from:
* Task assignment (inference or validation)
* Voting weight calculation
* Consensus power allocation
* Inference routing via the decentralized API (DAPI)
* Model group membership logic (EpochGroup)
* Clients selecting transfer agents</p>
<hr />
<h2><strong>Proposed Solution</strong></h2>
<h3>1. <strong>Introduce a New Query and data structure: <code>InvalidatedParticipants</code></strong></h3>
<ul>
<li>A new chain query will return a list of <strong>invalidated participants for the current epoch</strong> only.</li>
<li>This query will include:<ul>
<li>Participant identifier</li>
<li>Epoch index for when they are invalidated</li>
<li>Reason for invalidation (e.g., bad inference, wrong model, configuration issue)</li>
</ul>
</li>
<li>No cryptographic proof is necessary (for now) as it's only relevant to the current epoch and used for filtering.</li>
<li>The list will be added to whenever a participant is marked invalid by the validation algorithms</li>
<li>There should be no need for specific pruning</li>
<li>There should be no write access to the list via queries or other endpoints.</li>
</ul>
<h3>2. <strong>Update DAPI Logic to Respect Invalid Participants</strong></h3>
<ul>
<li>
<p>When querying for active participants via the DAPI:</p>
<ul>
<li>Also query <code>InvalidatedParticipants</code></li>
<li>Add an "invalidated" field for the value.</li>
<li>We will rely on updated clients to exclude these now invalidated participants</li>
<li>(We cannot filter at this level as clients still need the cryptographically secured list)</li>
</ul>
</li>
</ul>
<h3>3. <strong>Recursive Removal from All Model Group Memberships</strong></h3>
<ul>
<li>An invalidated participant must be <strong>removed from all models they serve</strong>, not just the model they were invalidated for.</li>
<li>Treat invalidation as a <strong>global disqualification</strong> from participation for the epoch.</li>
</ul>
<h3>4. <strong>Ensure Invalid Participants Have No Voting or Consensus Power</strong></h3>
<ul>
<li>Remove consensus-related influence (this is already done, but not properly verified in tests)<ul>
<li>No voting rights in governance</li>
<li>No consensus power in Tendermint</li>
</ul>
</li>
</ul>
<hr />
<h2><strong>Testing &amp; Validation Plan</strong></h2>
<ul>
<li>
<p>The invalidation mechanism was previously disabled during development and was under tested. Now that the full behavior is enabled:</p>
<ul>
<li>Ensure that invalid participants are:<ul>
<li>Properly listed in the <code>InvalidatedParticipants</code> query</li>
<li>Excluded from all responsibilities</li>
<li>Not receiving rewards, work, or assignments</li>
<li>Removed from voting and consensus mechanisms</li>
</ul>
</li>
<li>Extend <strong>Testermint</strong> tests to cover these scenarios</li>
</ul>
</li>
</ul>
<hr />
<h2><strong>Client &amp; Consumer Requirements</strong></h2>
<ul>
<li>All example clients (and production consumers) must:<ul>
<li>Update to use the <strong>filter the list</strong> from DAPI to exclude invalid participants when selecting an endpoint</li>
</ul>
</li>
</ul>
<hr />
<h2><strong>Terminology Clarification</strong></h2>
<ul>
<li><strong>Invalidated Participant</strong>: A participant that has been deemed untrustworthy for the current epoch due to failed validations, model misalignment, or malicious behavior.</li>
<li><strong>Active Participant</strong>: A participant still cryptographically listed as active, but may need filtering at runtime if they're invalidated.</li>
</ul>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #394](https://github.com/gonka-ai/gonka/issues/394) every hour.
