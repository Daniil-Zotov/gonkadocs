---
title: "#2210 — x/inference: validation_sample_size is not bounded; values above 500 make honest PoC validation fail"
source: https://github.com/gonka-ai/gonka/issues/2210
issue_number: 2210
synced_at: 2026-11-13T16:32:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: validation_sample_size is not bounded; values above 500 make honest PoC validation fail
    <span class="issues-number">#2210</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-11-03 17:47 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-05 03:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

`poc_params.validation_sample_size` has no bound in param validation, while the proof endpoint every participant serves accepts at most 500 leaf indices per request. A governance update to a value above 500 or below 0 passes validation and makes honest participants fail PoC validation.

- `PocParams.Validate` checks `validation_vote_threshold_bps` and the PoC schemes, but not `validation_sample_size` ([types/params.go:1035-1045](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/x/inference/types/params.go#L1035-L1045)). The field is an `int32` ([params.proto:262](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/proto/inference/inference/params.proto#L262)).
- The validator reads it as is and replaces only 0 with 200 ([poc/validator.go:317-320](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/validator.go#L317-L320), same in [poc/challenge_validate.go:31-34](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/challenge_validate.go#L31-L34)).
- `sampleLeafIndices` returns `min(sampleSize, count)` indices, and nil for a negative size ([poc/validator.go:1033-1046](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/validator.go#L1033-L1046)). `FetchAndVerifyProofs` sends all of them in one request ([poc/proof_client.go:128-180](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/proof_client.go#L128-L180)).
- The proof handler answers 400 for an empty list or more than `maxLeafIndicesPerRequest = 500` ([server/public/poc_handler.go:23](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/internal/server/public/poc_handler.go#L23), [:166-171](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/internal/server/public/poc_handler.go#L166-L171)).

So with `validation_sample_size = 501`, every validator's proof request to a participant whose commit count is above 500 gets a 400. The validator classifies a non-200 answer as `validateFailRetry` ([poc/validator.go:861-873](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/validator.go#L861-L873)), and every retry fails the same way, so it votes -1 once attempts run out ([poc/validator.go:105](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/decentralized-api/poc/validator.go#L105)). With a negative value the request is empty and fails the same way for every participant. The current mainnet value is 200, so nothing is affected today. `upgrade-v0.2.18` and `main` have the same code.

## Expected

A param value that passes `Params.Validate` should not make honest participants fail validation.

## Suggested fix

In `PocParams.Validate`, reject `validation_sample_size < 0 || > 500`, with 500 taken from one constant shared with the DAPI handler. This is a chain change and ships with an upgrade. The DAPI can also clamp the sample size to `[1, 500]` in both readers, which needs no chain upgrade.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/EazyHood">@EazyHood</a></span>
    <span class="issues-meta-item">commented 2026-11-05 03:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@kaileido are you planning to send the fix for this yourself? If not, and it's open for contributors, I'd like to take it: reject validation_sample_size below 0 or above 500 in PocParams.Validate, with the 500 in one constant shared with the proof handler, and clamp it to [1, 500] in the two DAPI readers (0 still means the default of 200). Tests for -1, 0, 500 and 501. ETA 2-3 days.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2210](https://github.com/gonka-ai/gonka/issues/2210) every hour.
