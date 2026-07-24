---
title: "#1222 — [P1] Int overflow"
source: https://github.com/gonka-ai/gonka/issues/1222
issue_number: 1222
synced_at: 2026-07-24T11:57:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P1] Int overflow
    <span class="issues-number">#1222</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-21 22:30 UTC</span>
    <span class="issues-meta-item">6 comments</span>
    <span class="issues-meta-item">Updated 2026-07-22 05:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">nice-to-have</span></div>
</div>

<div class="issues-content" markdown="1">
The goal of this is to have in place after this a standard way of handling possible overflows, have it implemented consistently across the entire codebase and to have a check (preferably a static check, an AI persona if necessary as a backup) that flags anything that doesn't use the established pattern
</div>

---

## 💬 Comments (6)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/olegsuhoparov">@olegsuhoparov</a></span>
    <span class="issues-meta-item">commented 2026-06-30 13:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Opened a surgical first PR against main: #1379.</p>
<p>It ports the already-accepted #1100/#1101 overflow fixes to main and adds two small guards for payout uint64-&gt;int64 conversion and validation totalWeight accumulation.</p>
<p>I intentionally left broad static analysis and #1017 supply-cap semantics out of scope so this remains reviewable.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-07-07 10:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @olegsuhoparov </p>
<p>Wanted to flag that #1017 (Bitcoin reward supply-cap overflow guards) has been aligned with the overflow-handling direction from this meta-issue.</p>
<p>Changes on branch <code>fix/bitcoin-rewards-supply-cap-overflow</code> (commit <code>9e4ebf74e</code>):</p>
<ul>
<li>Added a reusable <code>checkedAddUint64</code> helper in <code>inference-chain/x/inference/keeper/bitcoin_rewards.go</code>, placed next to the <code>checkedAddInt64</code> pattern introduced in #1379
  .</li>
<li>Replaced the inline <code>math.MaxUint64</code> overflow checks in the supply-cap reduction loop and in <code>CalculateParticipantBitcoinRewards</code> with the new helper.</li>
<li>Upgraded the overflow guard logs from <code>Warn</code> to <code>Error</code>.</li>
<li>Added explicit unit tests for the overflow path:<ul>
<li><code>TestCheckedAddUint64</code></li>
<li><code>TestGetBitcoinSettleAmounts_SupplyCapReductionNoWrap</code></li>
</ul>
</li>
</ul>
<p>Since #1379 explicitly left the #1017 supply-cap semantics out of scope, #1017 adopts the same helper/logging/test pattern independently rather than conflicting with #1379.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/olegsuhoparov">@olegsuhoparov</a></span>
    <span class="issues-meta-item">commented 2026-07-08 08:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for aligning #1017 with the overflow-handling direction from #1379.</p>
<p>That split makes sense to me: #1379 intentionally stays focused on settlement/claim/validation overflow paths and leaves the Bitcoin supply-cap semantics to a separate PR.</p>
<p>One thing to keep in mind is merge order: #1379 changes the <code>CalculateParticipantBitcoinRewards</code> fallback from <code>MaxUint64</code> to <code>MaxInt64</code>, so if #1379 lands first, #1017 will likely need a small rebase/adaptation around the fallback-path rationale and tests.</p>
<p>I would also double-check that the new #1017 tests assert the overflow guard path directly, not only the final <code>totalRewarded &lt;= remainingSupply</code> invariant. That would make the defense-in-depth coverage clearer for reviewers.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-07-08 09:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>re  </p>
</blockquote>
<p>Have a good time, Oleg! Direct overflow guard test - added in the latest commit <code>76d0ab6d0</code> on <code>fix/bitcoin-rewards-supply-cap-overflow</code>:
  - <code>TestApplyProportionalSupplyCapReduction_OverflowGuard</code> feeds <code>RewardCoins = MaxUint64</code> for two participants and asserts the guard fires, <code>total Distributed</code> saturates
  at <code>MaxUint64</code>, and remaining rewards are zeroed. The log shows the <code>Error</code>-level guard trigger.  Merge order — agreed. If #1379 lands first, I'll rebase #1017 and align the <code>CalculateParticipantBitcoinRewards</code> fallback path with the <code>MaxInt64</code> cap introduced there.</p>
<p>I'll keep waiting maintainers reaction and proto lifecycle move.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-20 22:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>First, prepare a detailed proposal outlining what is planned, why it should be done, the expected outcomes, and the rationale behind the proposed approach. Share the proposal with the community and obtain validation before proceeding with implementation.</p>
<p>@everyone @Mayveskii @olegsuhoparov </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-07-22 05:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>re</p>
</blockquote>
<p>Got it. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1222](https://github.com/gonka-ai/gonka/issues/1222) every hour.
