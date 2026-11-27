---
title: "#2234 — Maintenance window: Review & activation"
source: https://github.com/gonka-ai/gonka/issues/2234
issue_number: 2234
synced_at: 2026-11-27T02:17:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Maintenance window: Review & activation
    <span class="issues-number">#2234</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 06:14 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-11-17 07:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #c2e0c6; color: #24292f; border-color: #c2e0c6;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-11-06 22:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>1850 is relevant here. With current params the confirmation PoC trigger comes 281 blocks before evaluation, and the schedule lead is only 100 blocks, so a host that sees the trigger can still put a 1-block window on the evaluation block and be skipped by it. The PR rejects any window that covers an in-progress evaluation.</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maksimenkoff">@maksimenkoff</a></span>
    <span class="issues-meta-item">commented 2026-11-06 22:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>One thing to fix first, in ClaimRewards: a window touching an epoch at all (a single block at its end is enough) currently skips the missed-validation check for the entire epoch. Once claim_validation_enabled is on as well, default credit params let a host validate in just 1 epoch out of 21. My PR #2212 limits the waiver to inferences created inside the window.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-16 11:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Reviewed the spec against <code>upgrade-v0.2.17</code> (aa3c763ab) and current mainnet params. Besides #1850 and #2212, three things look worth settling before <code>maintenance_enabled</code> is turned on, plus two notes.</p>
<p><strong>1. The confirmation PoC exemption never reaches a host that was down for generation.</strong>
<code>evaluateConfirmation</code> skips hosts that are in an ACTIVE window at the evaluation block. On mainnet generation is T+2…T+36 and evaluation is T+281, 245 blocks later, while <code>maintenance_max_window_blocks</code> is 200. A window that covers evaluation starts at T+82 or later, so its host was online for generation. A window that overlaps generation ends by T+235 and is evaluated as usual with little or nothing measured: confirmation weight drops to the preserved part, and below <code>alpha_threshold</code> the host goes INACTIVE and is slashed (#2208).</p>
<p>With 4 expected events over a 14,090-block trigger range, a trigger falls inside a 200-block window with probability 5.5%. That is about 1 in 18 full windows for an honest host.</p>
<p>Suggestion: decide the exemption by overlap with the event, i.e. the reservation was ACTIVE at some block of <code>[GenerationStart, ValidationEnd]</code>. With the scheduling check from #1850 such a reservation predates the trigger (apart from the same-block case noted there), and a window placed on the evaluation block alone no longer exempts. The index from #2212 gives the lookup.</p>
<p><strong>2. DKG is not protected.</strong> The spec forbids overlap with DKG. <code>checkEpochPhaseOverlap</code> rejects PoC, PoC validation and the single <code>SetNewValidators</code> block. DKG starts at <code>EndOfPoCValidation</code> (P+280) and runs 5+3+3 blocks. A window P+281…P+399 is accepted and covers dealing and verification. Suggestion: reject the whole <code>[EndOfPoCValidation, SetNewValidators]</code> range (120 blocks, 0.8% of the epoch).</p>
<p><strong>3. The 10% power cap excludes the largest hosts.</strong> <code>checkConcurrencyLimits</code> counts the applicant's own power. Validator sets at 30 heights one epoch apart (6,620,015…7,066,354):</p>
<table>
<thead>
<tr>
<th>share of consensus power</th>
<th>validators</th>
<th>their power together</th>
</tr>
</thead>
<tbody>
<tr>
<td>above 10%: can never schedule</td>
<td>1–6, median 2.5</td>
<td>15–77%, median 35%</td>
</tr>
<tr>
<td>5–10%: cannot overlap with each other</td>
<td>1–8, median 6</td>
<td>median 49%</td>
</tr>
</tbody>
</table>
<p>So about a third of the power has no maintenance path, and <code>max_concurrent_validators = 3</code> is reachable only by small hosts. Is that intended? If not, one option is to let a reservation that is alone in its interval pass up to a higher single-validator limit.</p>
<p><strong>Notes</strong>
- With <code>signed_blocks_window = 100</code> and <code>min_signed_per_window = 0.5</code>, an outage of up to 50 blocks never jails. A window starts to help above 50 blocks, which is 3 epochs of credit; a full 200-block window (18.7 min) takes 10 epochs. Worth stating in the host docs.
- Devshard does not know about maintenance: escrow slots are drawn for hosts in a window, and settlement misses are waived only for PoC challenges. <code>GetRandomExecutor</code> and the expiry waiver cover the classic path only. The cost today is small: 200 blocks is 1.3% of an epoch against the 10% reward test, and the median host miss rate in epoch 457 was 1.2%. Still, the gateway could skip hosts in an active window.</p>
<p>Params and validator sets are from public mainnet RPC; I can share the two scripts. Code was read, not run.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-17 05:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I implemented the original maintenance windows in #998. I'll take the DKG overlap fix first, then a separate follow-up for the confirmation PoC exemption, coordinating with #1850 and #2212.</p>
<p>The DKG PR will cover the full critical interval, boundary and cross-epoch cases, and agreement between the schedulability query and the transaction. The CPoC follow-up will cover maintenance overlapping the event but completed before evaluation, with protection against reactive scheduling and the same-trigger-block case.</p>
<p>I'll also add activation regressions for preserved weight/collateral during covered downtime and normal duties and penalties after the window ends.</p>
<p>Update: the DKG fix is in #2275 and the CPoC fix is in #2276. The activation regression also exposed a separate existing slashing-wiring omission: dependency injection copies the keeper into the module before the maintenance checker is attached, so ACTIVE maintenance still accumulates missed signatures. #2278 fixes that application wiring and carries the downtime/recovery regression; the registered-module test reproduces the failure before the fix and passes afterward.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2234](https://github.com/gonka-ai/gonka/issues/2234) every hour.
