---
title: "#2217 — BUG: Severity Low: Non-initial model group cap compares N-1 post-collateral weight against pre-collateral contribution"
source: https://github.com/gonka-ai/gonka/issues/2217
issue_number: 2217
synced_at: 2026-11-14T10:41:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    BUG: Severity Low: Non-initial model group cap compares N-1 post-collateral weight against pre-collateral contribution
    <span class="issues-number">#2217</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-04 19:18 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 06:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span> <span class="issues-label" style="background-color: #c2e0c6; color: #24292f; border-color: #c2e0c6;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The group cap for non-initial models compares values in two different units. The cap budget is `cap_factor` × the previous epoch's **final** weight, which is after collateral adjustment, the 30% power cap and the confirmation discount. The value being capped is the group's **pre-collateral** contribution (`ConsensusKoeff × PoC weight`). Collateral adjustment then runs after the cap and reduces the group's weight a second time.

When participants are not fully collateralized, a non-initial model's weight share converges to about `cap_factor × base_weight_ratio`, no matter how much compute it contributes.

## Where

- [`ComputeGroupCap`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/delegation_weight_calculator.go#L279): `cap = CapFactor × TotalNetworkWeight`. `TotalNetworkWeight` is the sum of `ConsensusWeights`.
- `ConsensusWeights` come from [`buildPreviousConfirmedWeightCaps`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/previous_epoch_cap.go#L284). They are the N-1 confirmed effective weights, i.e. final `ActiveParticipant.Weight` after collateral and power capping, times the confirmation ratio.
- [`ComputeConsensusWeights`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/delegation_weight_calculator.go#L316) compares that cap against `rawTotal = Σ ConsensusKoeff × MemberPocWeights`, which is before collateral.
- [`runWeightPipeline`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/module.go#L705) in `module.go` then calls `AdjustWeightsByCollateral` ([L764](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/module.go#L764)) and `applyEpochPowerCapping` (L765) on the already-capped weights. The cap is applied at [L725](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/module.go#L725).

The calculator uses the name "consensus weight" for both the N-1 post-collateral value and the N pre-collateral value.

## Observed on testnet

The testnet runs v0.2.17-testnet-1 with DECODE PoC; the coefficient is 1 for both models.

- **Models:** Qwen3-4B is the initial model; Qwen2.5-7B is non-initial.
- **Params:** `cap_factor = 0.75`, `base_weight_ratio = 0.2`, grace period ended. Only one participant has collateral.
- **Raw PoC weight:** 7B ≈ 8,877, 4B ≈ 12,655, so 7B supplies about 41% of raw PoC weight.
- **One epoch:**
  - Cap = 0.75 × N-1 total 1,730 = 1,297, so 7B is scaled to 14.6% of its raw contribution.
  - Collateral (×0.2) then reduces 7B to about 259; the chain shows 257.
  - The 30% power cap trims the large 4B participants. The final total is 1,704.
- **Result:** 7B's weight share settles at 0.75 × 0.2 = 15%. Epochs 877–879 show 14.9%, 15.2% and 15.0%.
- **With the cap applied in post-collateral units,** a rough estimate puts 7B at about 33%.

This also moves the share closer to the eligibility threshold (`w_threshold = 0.1`). If it drops below that, the model gets weight 0 and cannot become eligible again. See "Related" below.

## Mainnet impact today

None at the moment. As of epoch 447:
- All 25 active participants are fully collateralized (lowest coverage 1.1×).
- No participant hits the 30% power cap.
- Neither non-initial model (DeepSeek-V4-Flash and GLM-5.3-Flash, at about 118k–659k and 173k–482k against a cap of about 1.07M) reaches the cap.

The issue becomes live on mainnet if a non-initial model grows enough for the cap to bind and, at the same time, weight is reduced by a slash or collateral withdrawal, or by the confirmation discount.

## Why the tests don't catch it

The `ComputeGroupCap` and `ComputeConsensusWeights` tests in `weight_calculator_test.go` set `TotalNetworkWeight` equal to the PoC weights, with no collateral or power cap, so the two units coincide.

## Design doc mismatch

`proposals/multi-model-poc/design-2.md` and `README.md` define the cap as `cap_factor * sum(member's prior-epoch consensus weight from other eligible groups)`, i.e. the group's own members. The code uses the whole network's N-1 weight. Under the doc's formula, hosts that only serve a non-initial model would always get a cap of 0. Either the doc or the code should be updated, and the units need to be defined explicitly.

## Possible fixes

1. Persist each participant's N-1 pre-collateral weight (the `ComputeConsensusWeights` output) and compute the cap against that.
2. Or apply the group cap after `AdjustWeightsByCollateral`, so both sides are in final-weight units.
3. Add a test with `base_weight_ratio < 1` and partial collateral, plus one where the power cap binds.

## Related

A non-initial group whose members all had zero N-1 weight, for example after every member dropped out for one epoch, fails both [`MeetsWeightThreshold`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/delegation_weight_calculator.go#L96) and the `v_min` established-member check in [`IsGroupEligible`](https://github.com/gonka-ai/gonka/blob/c4d441052f3362e48fb29d0dda297f73b14dc564/inference-chain/x/inference/module/delegation_weight_calculator.go#L176). It then stays at weight 0 permanently. On testnet the only way out was a governance change to `w_threshold`/`v_min` and back. This is worth a separate issue or a recovery path.

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-11-04 19:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@GLiberman, let's fix it in 0.2.18, please.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-04 19:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h3>Chain logs from testnet (epoch 881 formation)</h3>
<p>These are from <code>v0.2.17-testnet-1</code>, and the same pattern repeats in epochs 879, 880 and 882. Addresses are shortened.</p>
<pre><code>INF Collateral grace period has ended. Adjusting weights by collateral. current_epoch=881
INF Universal power capping applied to epoch powers originalTotalPower=6943 cappedTotalPower=1714 participantCount=7
INF weight_group epoch=881 model=Qwen/Qwen2.5-7B-Instruct    coeff=1 raw_total=8858  cap=1280 scale=0.144502144953714157
INF weight_group epoch=881 model=Qwen/Qwen3-4B-Instruct-2507 coeff=1 raw_total=12638 cap=-1   scale=1
INF weight_pipeline epoch=881 addr=…pcgs0y modes=7B:DIRECT,4B:NONE     consensus=492  before_collateral=492  final=98
INF weight_pipeline epoch=881 addr=…32vrcn modes=7B:DIRECT,4B:NONE     consensus=255  before_collateral=255  final=51
INF weight_pipeline epoch=881 addr=…q60cwt modes=7B:DIRECT,4B:NONE     consensus=265  before_collateral=265  final=53
INF weight_pipeline epoch=881 addr=…4sgtd5 modes=7B:DIRECT,4B:NONE     consensus=266  before_collateral=266  final=53
INF weight_pipeline epoch=881 addr=…u4txhy modes=7B:DELEGATE,4B:DIRECT consensus=5277 before_collateral=5277 final=514
INF weight_pipeline epoch=881 addr=…kyc325 modes=7B:NONE,4B:DIRECT     consensus=2159 before_collateral=2159 final=431
INF weight_pipeline epoch=881 addr=…2f3a2y modes=7B:DELEGATE,4B:DIRECT consensus=5202 before_collateral=5202 final=514
</code></pre>
<p>What the logs show:</p>
<ul>
<li><strong><code>weight_group</code>:</strong></li>
<li>The 7B cap of 1280 is <code>0.75 × 1707</code>, and 1707 is epoch 880's final total (<code>cappedTotalPower</code>).</li>
<li>It is compared against <code>raw_total=8858</code>, which is in pre-collateral units, so 7B is scaled to 14.45%.</li>
<li><strong><code>weight_pipeline</code>, 7B hosts:</strong> none of them have collateral. After the cap, collateral cuts each one again to 20%, e.g. pcgs0y 492 → 98.</li>
<li>The 7B final total is 255 of 1714, i.e. 14.9%, which matches <code>cap_factor × base_weight_ratio = 0.75 × 0.2</code>.</li>
<li><strong>Power capping:</strong> <code>originalTotalPower=6943 → cappedTotalPower=1714</code> combines collateral and the 30% power cap. That 1714 then becomes the next epoch's cap budget.</li>
<li><strong>Code comment:</strong> the one on <code>emitWeightPipelineLogs</code> says the gap between <code>before_collateral</code> and <code>final</code> is "collateral adjustment and power-cap (both rarely active)". Here both are active every epoch.</li>
</ul>
<p>The per-participant collateral breakdown (<code>Adjusted participant weight by collateral</code>) is logged at debug level, so it is not visible at the default log level. Raising it to info would make this issue easier to spot on mainnet.</p>
<h3>Simulated fix</h3>
<p>I fed epoch 881's per-node PoC weights through the chain's own <code>ComputeConsensusWeights</code> and <code>ApplyPowerCappingForWeights</code>. The current pipeline reproduces the on-chain finals exactly. With the cap computed in matching units, either by applying it after collateral or by comparing against N-1 pre-collateral weights:</p>
<table>
<thead>
<tr>
<th></th>
<th>7B final</th>
<th>4B final</th>
<th>7B share</th>
</tr>
</thead>
<tbody>
<tr>
<td>current (on chain)</td>
<td>255</td>
<td>1459</td>
<td>14.9%</td>
</tr>
<tr>
<td>fixed, first epoch (cap after collateral)</td>
<td>1278</td>
<td>2670</td>
<td>32.4%</td>
</tr>
<tr>
<td>fixed, steady state (both fixes)</td>
<td>1770</td>
<td>2881</td>
<td>38.1%</td>
</tr>
</tbody>
</table>
<p>At steady state the 7B cap no longer binds (1770 &lt; 0.75 × 4651).</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2217](https://github.com/gonka-ai/gonka/issues/2217) every hour.
