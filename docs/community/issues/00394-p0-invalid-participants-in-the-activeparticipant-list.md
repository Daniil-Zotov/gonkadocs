---
title: "#394 — [P0] Invalid participants in the `ActiveParticipant` list"
source: https://github.com/gonka-ai/gonka/issues/394
issue_number: 394
synced_at: 2026-07-06T21:54:44Z
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
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2025-10-16 00:22 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2025-12-02 20:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content">
Proper removal (Check that we also jail => no voting power)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2025-10-21 18:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    # Invalid Participant Exclusion – Feature Specification

## **Overview**

This feature refines, fixes and fully tests the mechanism for handling **invalid participants** in the Gonka network. Invalid participants are nodes that have misbehaved (e.g., submitted bad inferences, misconfigured models, attempted cheating, or failed other behavioral criteria). The goal is to ensure they are **excluded from all network responsibilities and consensus mechanisms**, without retroactively altering cryptographically signed data.

---

## **Problem Statement**

Currently, the list of **active participants** retrieved from the chain **could include nodes that are technically invalid** for the current epoch. This list is **signed and committed cryptographically** each epoch, making it immutable and essential for trust and traceability via Merkle proofs.

However, since some participants may be no longer trustworthy (due to detected invalid behavior during the epoch), relying solely on the active list is not sufficient for selecting endpoints to use.

Additionally, when a participant is marked as invalid, we need to ensure and test that they are excluded from:
* Task assignment (inference or validation)
* Voting weight calculation
* Consensus power allocation
* Inference routing via the decentralized API (DAPI)
* Model group membership logic (EpochGroup)
* Clients selecting transfer agents

---

## **Proposed Solution**

### 1. **Introduce a New Query and data structure: `InvalidatedParticipants`**

* A new chain query will return a list of **invalidated participants for the current epoch** only.
* This query will include:
    * Participant identifier
    * Epoch index for when they are invalidated
    * Reason for invalidation (e.g., bad inference, wrong model, configuration issue)
* No cryptographic proof is necessary (for now) as it's only relevant to the current epoch and used for filtering.
* The list will be added to whenever a participant is marked invalid by the validation algorithms
* There should be no need for specific pruning
* There should be no write access to the list via queries or other endpoints.

### 2. **Update DAPI Logic to Respect Invalid Participants**

* When querying for active participants via the DAPI:

    * Also query `InvalidatedParticipants`
    * Add an "invalidated" field for the value.
    * We will rely on updated clients to exclude these now invalidated participants
    * (We cannot filter at this level as clients still need the cryptographically secured list)

### 3. **Recursive Removal from All Model Group Memberships**

* An invalidated participant must be **removed from all models they serve**, not just the model they were invalidated for.
* Treat invalidation as a **global disqualification** from participation for the epoch.

### 4. **Ensure Invalid Participants Have No Voting or Consensus Power**

* Remove consensus-related influence (this is already done, but not properly verified in tests)
    * No voting rights in governance
    * No consensus power in Tendermint

---

## **Testing & Validation Plan**

* The invalidation mechanism was previously disabled during development and was under tested. Now that the full behavior is enabled:

    * Ensure that invalid participants are:
        * Properly listed in the `InvalidatedParticipants` query
        * Excluded from all responsibilities
        * Not receiving rewards, work, or assignments
        * Removed from voting and consensus mechanisms
* Extend **Testermint** tests to cover these scenarios

---

## **Client & Consumer Requirements**

* All example clients (and production consumers) must:
    * Update to use the **filter the list** from DAPI to exclude invalid participants when selecting an endpoint

---

## **Terminology Clarification**

* **Invalidated Participant**: A participant that has been deemed untrustworthy for the current epoch due to failed validations, model misalignment, or malicious behavior.
* **Active Participant**: A participant still cryptographically listed as active, but may need filtering at runtime if they're invalidated.
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #394](https://github.com/gonka-ai/gonka/issues/394) every hour.
