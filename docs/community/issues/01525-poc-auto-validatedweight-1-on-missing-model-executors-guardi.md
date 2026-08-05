---
title: "#1525 — PoC auto ValidatedWeight:-1 on missing model executors + guardian tiebreaker can wipe model weight (v0.2.14)"
source: https://github.com/gonka-ai/gonka/issues/1525
issue_number: 1525
synced_at: 2026-08-05T03:39:47Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    PoC auto ValidatedWeight:-1 on missing model executors + guardian tiebreaker can wipe model weight (v0.2.14)
    <span class="issues-number">#1525</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-07-30 08:59 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-30 10:45 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

On Gonka **testnet**, PoC stage **98080** (epoch **273→274**), we reproduced the **v0.2.14** PoC path where a host assigned to validate a model it cannot execute eventually submits `ValidatedWeight: -1`. That same path, run by the testnet **genesis guardian** (a **4B-only** host), caused **all** `Qwen/Qwen2.5-7B-Instruct` PoC weight to be **rejected** for the next epoch—despite honest 7B store commits and peer `+20` validations. **4B weight was unaffected.**

This is **not** “bad 7B proofs.” It is:
1. **auto `-1`** from missing validation executors, plus
2. **majority math** that cannot clear **>50% of total network weight** for a small model, so
3. the decision falls to the **guardian tiebreaker**, which counts **raw** guardian votes even when the guardian has **no voting power for that model**.

Related background (mainnet / Kimi): after the v0.2.14 upgrade, nodes that previously **abstained** when they lacked a model started submitting **negative** PoC validations. Claims that “`-1` from hosts with no model weight cannot affect results” are **only true for the majority tally**. They are **false for the guardian path**, which we proved on testnet.

---

## Setup / experiment steps

### DAPI path (`decentralized-api/poc/validator.go`)

1. Host assigned to validate model `M`
2. `filterValidationNodesForModel(M)` empty → `"no validation executors for model"`
3. Returns `validateFailRetry`
4. Retries with backoff `3s × 1.5^n` (cap **45s**), **`MaxRetries=25`** (~**14–15 min** to exhaust)
5. On exhaustion → `reportInvalidParticipant` → submit **`ValidatedWeight: -1`**

Note: this submit path was effectively enabled in v0.2.14; previously missing-model cases often produced **no** validation tx (abstain).

### Why a short validate window hides the bug

Default testnet `poc_validation_duration=40` (~4 min) ends before 25 retries complete → `validation complete … failed=0` → **no `-1` tx**.

### What we changed to reproduce on-chain `-1`

1. Gov proposal **#19**: set **`poc_validation_duration=160`** (~16 min validate window)
2. Left **18132** `node7-18213` (**7B**) **disabled** for PoC stage **`98080`** so 18132 would be assigned 7B validation without a local executor
3. Other hosts continued to generate/commit 7B normally

### Reproduction evidence (stage `98080`)

**18132 logs:**
- `no validation executors for model` for 7B targets (18133 / 18134 / 18218)
- `max retries exceeded` (`attempts=25`)
- `reported participant as invalid`
- `validation complete … successful=6 failed=3`

**On-chain:** 18132 (`gonka1lhys…`) submitted `-1` for `Qwen/Qwen2.5-7B-Instruct` against those three committers.

**Also organic (same path):** 4B-only hosts **`.79` (guardian)**, **`.250`**, **`18216`** also submitted 7B `-1`s (no intentional disable).

---

## What happened at weight calculation

For **each** of 18133 / 18134 / 18218 on 7B:

| Vote | Who | Notes |
|------|-----|--------|
| `+20` × 3 | Peer 7B hosts among {18133, 18134, 18218} | Real validation; had 7B VP |
| `-1` × 4 | 18132 (experiment), `.79` (guardian), `.250`, `18216` | No 7B executor → auto `-1` |

### Majority path (`chainvalidation.go`)

- Majority only counts validators with **that model’s voting power** (`getParticipantValidations` filters).
- So 4B-only / no-7B-VP `-1`s are **dropped** from majority.
- Majority effectively saw **3× `+`** from 7B hosts.

But params were:
- `validation_slots=0`
- `validation_vote_threshold_bps=5000` → need **strictly >50% of `TotalNetworkWeight`** (whole network), **not** model-local.

Epoch 273 total ≈ **191 594** → bar ≈ **95 798**.  
Three 7B voters’ combined VP ≈ **≤66k** → **cannot** clear valid majority.  
Invalid side also **0** in majority (all `-1`s filtered) → **inconclusive** → guardian.

### Guardian path (`guardianProtection`)

Guardian votes are read from the **raw (unfiltered)** validation list (explicit comment in code: guardian may have no model VP and must still count).

Guardian `.79` is **4B-only** → same auto-`-1` path →:

```text
Guardian tiebreaker - unanimous invalid. Rejecting. (guardianInvalidCount=1)
```

**Result:** all 7B PoC weight **rejected**. 4B **accepted**.

### Downstream impact

- Dual hosts (18132/33/34) survived into epoch **274** on **4B** weight.
- **18218** (7B-only) **dropped** from the active set (no accepted weight left).
- 7B re-entered via **bootstrap** after a later successful PoC (epoch **275**, 7 members, 18218 back). One successful PoC is enough; not two.

---

## Why the background “no impact” claim is wrong

| Layer | Do no-model-VP `-1`s matter? |
|-------|------------------------------|
| Majority tally | **No** — filtered out when voter lacks model VP |
| Guardian tiebreaker | **Yes** — raw list; guardian without model can cast invalid and wipe the model when majority is inconclusive |

On small models / networks where model VP ≪ half of `TotalNetworkWeight`, majority is often inconclusive, so **guardian path is the real decision**—and auto-`-1` from a guardian who cannot run the model is catastrophic.

---

## Code pointers

- DAPI retries → `-1`: `decentralized-api/poc/validator.go` (`filterValidationNodesForModel`, `validateFailRetry`, `MaxRetries=25`, `reportInvalidParticipant`)
- Majority filter vs guardian raw list: `inference-chain/x/inference/module/chainvalidation.go` (`getParticipantValidations`, `pocValidated`, `guardianProtection`)

---

## Suggested fix directions

1. **Do not submit `-1` for “no validation executors”** — abstain / skip (restore pre-v0.2.14 behavior for this case), **and/or**
2. **Guardian tiebreaker:** guardians without capability / model VP must not cast **invalid** for that model (or must be excluded from raw tiebreaker for that model), **and/or**
3. **Majority threshold:** when `validation_slots=0`, use a **model-local** denominator (or otherwise make small-model majorities reachable without always falling to guardian).

---

## Verification status

### Done (testnet)

- [x] Missing executor → retries → on-chain `-1` (stage `98080`, validate duration 160)
- [x] Impact via guardian wipe of all 7B weight despite honest commits + peer `+20`
- [x] Correction: “no weight ⇒ no impact” is false for guardian path
- [x] Recovery via bootstrap observed (epoch 275)

### Still open

- [ ] Mainnet / Kimi halt forensics (which `-1` voters; were any guardians; was majority inconclusive; halt height / restart)
- [ ] Product fix + retest (same 18132 disable experiment should **not** wipe model / should **not** emit `-1` for missing executors)

### Out of scope for “bug is real”

- Reproducing a full **chain halt** on testnet
- Kimi-specific model id (7B is the same path)

---

## Environment

- Chain: `gonka-testnet` (`http://89.169.111.79:8000`)
- Binary / behavior: **v0.2.14** PoC validation submit path
- PoC stage: **98080** (epoch 273→274)
- Model wiped: `Qwen/Qwen2.5-7B-Instruct`
- Guardian: `.79` (`gonka17cpc…` / `gonkavaloper17cpc…`), 4B-only
</div>

---

> 🔄 **Auto-synced** from [Issue #1525](https://github.com/gonka-ai/gonka/issues/1525) every hour.
