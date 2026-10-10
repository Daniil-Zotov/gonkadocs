---
title: "#1970 — Design question: who should be allowed to open a PoC challenge that waives devshard misses?"
source: https://github.com/gonka-ai/gonka/issues/1970
issue_number: 1970
synced_at: 2026-10-10T18:41:45Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Design question: who should be allowed to open a PoC challenge that waives devshard misses?
    <span class="issues-number">#1970</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-10-10 13:19 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-10 13:19 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Area

Branch `release/v0.2.16-post1`, module `x/inference` (PoC-challenge creation and the devshard miss waiver).

Relevant code:
- [`CreatePoCChallenge`](https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/x/inference/keeper/poc_challenge.go#L317) (who may open a challenge)
- [`WaiveDevshardMissesForActiveChallenge`](https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/x/inference/keeper/poc_challenge.go#L598) (the waiver)
- [`IsAllowedEscrowCreator`](https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/x/inference/keeper/params.go#L299) (the allowlist the gate reuses)
- [settlement call site](https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/x/inference/keeper/msg_server_settle_devshard_escrow.go#L227) (where the waiver runs, with the "waive only challenge-window misses" TODO)
- [`getInactiveStatus`](https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/x/inference/calculations/status.go#L90) (the downtime signal the waiver feeds)

## What the current rule allows

When a host is under an open challenge it must run PoC instead of serving inferences, so the waiver zeroes its missed-inference count at settlement so it is not marked INACTIVE for downtime it could not avoid. The intent is fine, but challenge creation is gated by the devshard escrow allowlist, whose default (empty) means anyone, and the only same-party check is `creator != target`, so under default params a funded account can open a challenge against a host it also controls. On mainnet today the escrow allowlist is set (18 addresses), so only those addresses can open a challenge; the gap is the default-open semantics and the coupling to the escrow list.

## Why it matters

The waiver suppresses the `MissedRequests` delta that drives the downtime SPRT, so a host that opens a challenge against itself can keep missing its queued inferences, stay ACTIVE, and keep its epoch reward without serving.

The design doc (`proposals/multi-model-poc/long-poc-challenge.md`) says a challenge is opened by "a governance-approved address", but the code's default lets anyone do it, so offline accounting and rewards can be wrong.

Note: this only suppresses the downtime signal. Completed/validated counts are unchanged, so it is not reward-count forgery.

## Options

1. Gate challenge creation to an explicit allowlist, empty means deny. Reuse the existing escrow allowlist field for the challenge path with inverted empty-semantics, so the feature is off until governance approves a challenger. Small, no proto change, no migration. Trade-off: couples escrow and challenge policy (approving a challenger also restricts escrow creation to that list), and an approved-but-malicious challenger could still self-challenge.

2. Dedicated `allowed_challenger_addresses` param on `PoCChallengeParams`, empty means deny. Same security outcome as option 1 but decoupled: escrow creation stays permissionless while challenge creation is gated on its own. Trade-off: needs a new proto field plus a (trivial, default-nil) migration.

3. Scope the waiver by assignment time (the TODO's "window" idea), keep creation permissionless. Waive only misses whose work was assigned after the challenge opened. Trade-off: this does not fix it and regresses honest challenges. New assignment already stops at the challenge start height, so every waivable miss comes from work assigned before the challenge opened, which means this would waive nothing and penalize honest challenged hosts for pre-challenge work.

## Recommended

Option 2 (dedicated challenger allowlist, default deny) as the clean fix. Option 1 is the minimal stopgap if a proto change is not wanted now.

## The question for the team

Should PoC-challenge creation have its own governance-gated allowlist that is closed by default, independent of the escrow allowlist? If yes, option 2; if coupling is acceptable for now, option 1.

A reproducing test and a draft fix exist and can be shared with maintainers on request.

</div>

---

> 🔄 **Auto-synced** from [Issue #1970](https://github.com/gonka-ai/gonka/issues/1970) every hour.
