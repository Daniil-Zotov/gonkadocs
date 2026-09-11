---
title: "#1726 — x/inference: CollateralParams.DowntimeMissedPercentageThreshold is governance-settable but read by nothing, and SlashForDowntime's comment describes a check it does not perform"
source: https://github.com/gonka-ai/gonka/issues/1726
issue_number: 1726
synced_at: 2026-09-11T00:14:37Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: CollateralParams.DowntimeMissedPercentageThreshold is governance-settable but read by nothing, and SlashForDowntime's comment describes a check it does not perform
    <span class="issues-number">#1726</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-09-07 14:23 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-07 14:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
`CollateralParams.DowntimeMissedPercentageThreshold` is declared, defaulted, validated, registered as a governance-settable param and live on chain at `0.05` — and no code reads it. A governance vote to tune it would pass, store the new value, and change nothing.

## Evidence

Every non-generated, non-test reference in the tree is declaration or plumbing, all in one file:

| location | what it is |
|---|---|
| `x/inference/types/params.go:17` | `KeyDowntimeMissedPercentageThreshold` |
| `x/inference/types/params.go:338` | default `DecimalFromFloat(0.05)` |
| `x/inference/types/params.go:581` | entry in the params string listing |
| `x/inference/types/params.go:636` | `NewParamSetPair` registration |
| `x/inference/types/params.go:982` | `validatePercentage` call |

Its four siblings under `CollateralParams` all have the same plumbing **plus** a consumer in `x/inference/keeper/collateral.go`:

| parameter | consumed at |
|---|---|
| `SlashFractionInvalid` | `collateral.go:170` |
| `SlashFractionDowntime` | `collateral.go:198` |
| `CollateralPerWeightUnit` | `collateral.go:51, 108, 115` |
| `BaseWeightRatio` | `collateral.go:46, 93, 103` |
| `DowntimeMissedPercentageThreshold` | **nowhere** |

## Why this looks like residue rather than a bug

`proposals/tokenomics-v2/collateral-todo.md` specifies the consumer that would have read it: "calculates a participant's missed request percentage for the epoch and compares it to the `DowntimeMissedPercentageThreshold` parameter."

What shipped instead is a sequential probability ratio test. `getInactiveStatus` in `x/inference/calculations/status.go:90` decides the INACTIVE transition from `DowntimeGoodPercentage`, `DowntimeBadPercentage` and `DowntimeHThreshold` — all `ValidationParams` — accumulating an `InactiveLLR` across epochs rather than comparing one epoch's ratio to a fixed cut-off.

That is a better test than the one the design doc described, and downtime slashing does work: `deactiveParticipant` (`participant_status.go:75`) calls `SlashForDowntime` on the transition into INACTIVE. So this is a parameter left behind when its mechanism was replaced, not a missing feature.

## The part that actively misleads

`SlashForDowntime`'s doc comment still describes the superseded design:

```go
// inference-chain/x/inference/keeper/collateral.go:195
// SlashForDowntime checks a participant's performance for the completed epoch and
// slashes their collateral if their missed request percentage exceeds the threshold.
func (k Keeper) SlashForDowntime(ctx context.Context, participant *types.Participant, params types.Params) {
```

The function performs no such comparison — it reads `SlashFractionDowntime` and slashes. The threshold decision happened upstream, in the SPRT, against different parameters. A reader auditing the slashing path is pointed at a check that does not exist there, and `proposals/tokenomics-v2/collateral.md` still documents the parameter as "the epoch performance threshold that triggers a downtime slash".

## Suggested fix

Either remove the parameter, or wire it. Removal is a state-breaking params change and so wants an upgrade handler, which may not be worth it on its own — in which case the cheap and useful half is documentation: correct the `SlashForDowntime` comment to say the INACTIVE transition already made the decision, and mark the parameter deprecated where it is declared and in `proposals/tokenomics-v2/collateral.md`, so nobody proposes a vote on a value with no effect.

## Scope

Read from `main` at `379bebced6`. I searched open issues and pull requests for `DowntimeMissedPercentageThreshold` and found nothing covering this. The reference counts above come from grepping the tree at that commit, excluding `*.pb.go`, `*.pulsar.go` and `_test.go`; I checked the four siblings as a control precisely because an initial search that found no consumer for any of them would have proved only that my search was wrong.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a></span>
    <span class="issues-meta-item">commented 2026-09-07 14:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Correcting my own framing above, having since read the live parameters rather than the code defaults. The core claim is unaffected — <code>DowntimeMissedPercentageThreshold</code> is still read by nothing — but the section headed "Why this looks like residue rather than a bug" describes the SPRT as what shipped in its place, and on mainnet that test cannot currently fire.</p>
<p>Live <code>validation_params</code>, epoch 386:</p>
<table>
<thead>
<tr>
<th>parameter</th>
<th>code default</th>
<th>live</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>downtime_good_percentage</code></td>
<td>0.10</td>
<td><strong>0.99</strong></td>
</tr>
<tr>
<td><code>downtime_bad_percentage</code></td>
<td>0.20</td>
<td><strong>0.99</strong></td>
</tr>
<tr>
<td><code>downtime_h_threshold</code></td>
<td>4</td>
<td><strong>1000000000</strong></td>
</tr>
</tbody>
</table>
<p>With <code>P0 == P1</code>, both increments in <code>SPRT.UpdateCounts</code> are exactly zero — <code>logFail = ln(P1/P0) = ln(1) = 0</code> and <code>logPass = ln((1-P1)/(1-P0)) = ln(1) = 0</code> — so the LLR cannot move from zero regardless of the observation sequence, and <code>Decision()</code> returns <code>Undetermined</code> for every possible input. The <code>1e9</code> threshold makes it unreachable a second time over. <code>getInactiveStatus</code> therefore never returns <code>Fail</code>, so <code>ParticipantStatus_INACTIVE</code> with reason <code>Downtime</code> is unreachable through the statistical path.</p>
<p>That reads as deliberate rather than accidental, and the same params object carries its own control: the <strong>invalidation</strong> SPRT beside it is live and well formed — <code>false_positive_rate</code> 0.05, <code>bad_participant_invalidation_rate</code> 0.18, <code>invalidation_h_threshold</code> 40, giving <code>logFail = +1.2809</code> and <code>logPass = -0.1472</code>, so 32 consecutive failures condemn and 272 consecutive passes clear. One test is parameterised to work and the other to do nothing.</p>
<p>Worth noting what <code>H</code> means here, since the implementation uses a symmetric <code>±H</code> rather than Wald's asymmetric boundaries. Symmetric bounds force <code>alpha = beta</code>, and <code>A = ln((1-beta)/alpha) = H</code> then gives <code>alpha = 1/(1+e^H)</code>. So the live invalidation threshold of 40 encodes a false-invalidation rate of about <code>4.2e-18</code>, against roughly <code>1.8e-2</code> at the code default of 4 — the on-chain value is not a tweak of the default, it is a different regime.</p>
<p>Downtime slashing itself is still reachable, so the doc-comment problem this issue raises remains live rather than moot: <code>getConfirmationPoCStatus</code> also returns <code>INACTIVE</code> (reason <code>FailedConfirmationPoC</code>), <code>confirmation_poc_params.alpha_threshold</code> is <code>0.5</code> on chain, and that transition runs the same <code>deactiveParticipant</code> -&gt; <code>SlashForDowntime</code> path. So a participant can still be slashed for downtime — just never via the missed-request statistics that <code>SlashForDowntime</code>'s comment describes, which makes the stale comment more misleading in production than it looked from the code alone.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1726](https://github.com/gonka-ai/gonka/issues/1726) every hour.
