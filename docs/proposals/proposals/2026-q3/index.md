---
title: "2026-Q3 Proposals"
template: proposals-oview.html
hide:
  - toc
---

# 2026-Q3 Proposals

<div class="prop-oview-filter" markdown="1">

<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-passed" checked>
  <span class="prop-filter-label">Passed</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-rejected" checked>
  <span class="prop-filter-label">Rejected</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-voting" checked>
  <span class="prop-filter-label">Voting</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-funding">
  <span class="prop-filter-label">With Funding</span>
</label>
<span class="prop-filter-count"></span>

</div>

<div class="quarter-summary" markdown="1">

## 2026-Q3 Summary

<div class="qs-stats">
<div class="qs-stat total"><span class="qs-num">14</span><span class="qs-desc">Total Proposals</span></div>
<div class="qs-stat passed"><span class="qs-num">8</span><span class="qs-desc">Passed (57%)</span></div>
<div class="qs-stat rejected"><span class="qs-num">5</span><span class="qs-desc">Rejected (36%)</span></div>

</div>

<div class="qs-categories">
<div class="qs-row"><span class="qs-label">Governance Parameters</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:43%"></span></span><span class="qs-value">6</span></div>
<div class="qs-row"><span class="qs-label">Funding / Grants</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:36%"></span></span><span class="qs-value">5</span></div>
<div class="qs-row"><span class="qs-label">Software Upgrade</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:14%"></span></span><span class="qs-value">2</span></div>
<div class="qs-row"><span class="qs-label">GRC / Restitution</span><span class="qs-bar-wrap"><span class="qs-bar" style="width:7%"></span></span><span class="qs-value">1</span></div>
</div>

<div class="qs-funding-line">80,000 GNK · $88,000 · Community Pool</div>
<div class="qs-bounty-line">$90,075 USDT · Bounty Reward</div>


</div>

<div class="prop-quarter">
<h2>2026-Q3</h2>
<p>14 proposals</p>
<div class="prop-card" data-status="prop-voting" data-voting-end="2026-08-03T00:21:18.753587476Z">
  <div class="prop-card-header">
    <a href="93/" class="prop-card-title">#93 – Upgrade devshard v4 runtime to v4.0.1</a>
    <span class="prop-vote-countdown" data-deadline="2026-08-03T00:21:18.753587476Z"></span>
    <span class="prop-badge prop-voting">Voting</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-08-01</span>
    <span>Voting ends 2026-08-03</span>
  </div>
  <div class="prop-card-desc">Replace the existing devshard v4 runtime with v4.0.1. This performance and resource-management patch does not change protocol, inference, validation, or economic behavior. It removes per-block chain q…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 5,620 (100.0%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-veto-text">✗ Turnout 5,620 / 492,267 (1.1%) · Quorum 25% (123,066)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="92/" class="prop-card-title">#92 – Upgrade Proposal: v0.2.15</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-28</span>
    <span>Voting ends 2026-07-30</span>
  </div>
  <div class="prop-card-desc">Upgrade Proposal: v0.2.15</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 229,105 (100.0%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span><span class="prop-card-bounty">$39,825 USDT · Bounty Reward</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 229,105 / 410,505 (55.8%) · Quorum 25% (102,626)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="91/" class="prop-card-title">#91 – Temporarily update BLS signing parameters</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-23</span>
    <span>Voting ends 2026-07-24</span>
  </div>
  <div class="prop-card-desc">Set max_signing_attempts to 1 and signing_deadline_blocks to 60 epoch lengths (923460 blocks) to mitigate a theoretical risk identified in a security report. Historically, retries have never been need…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 243,165 (100.0%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 243,165 / 569,511 (42.7%) · Quorum 25% (142,377)</span></div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="90/" class="prop-card-title">#90 – Partnerships with Inference Resellers, B2C users acquisition and conversion funnels analytics setup</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-21</span>
    <span>Voting ends 2026-07-23</span>
  </div>
  <div class="prop-card-desc">Currently Gonka has a lot of marketing activities, but doesn't have analytics to measure the results of their work and doesn't have a vision which target audiences and how we need to attract and onboa…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 190,646 (57.3%)</span> · <span class="prop-tally-no-text">No 6,269 (1.9%)</span> · <span class="prop-tally-veto-text">Veto 133,354 (40.1%)</span> · <span class="prop-tally-abstain-text">Abstain 2,324 (0.7%)</span><span class="prop-card-funding prop-card-funding-rejected">240,000 GNK · $57,000 · Community Pool</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 332,593 / 569,511 (58.4%) · Quorum 25% (142,377)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="89/" class="prop-card-title">#89 – Upgrade Proposal: v0.2.14</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-21</span>
    <span>Voting ends 2026-07-23</span>
  </div>
  <div class="prop-card-desc">Upgrade Proposal: v0.2.14</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 296,240 (100.0%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 115 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span><span class="prop-card-bounty">$50,250 USDT · Bounty Reward</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 296,355 / 545,426 (54.3%) · Quorum 25% (136,356)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="88/" class="prop-card-title">#88 – Restore Kimi K2.6 and remove v1, v2</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-16</span>
    <span>Voting ends 2026-07-17</span>
  </div>
  <div class="prop-card-desc">Update current chain params to register moonshotai/Kimi-K2.6 in the governance model list and remove approved_versions v1, v2 from devshard_escrow_params (to reduce RAM usage).</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 272,063 (99.8%)</span> · <span class="prop-tally-no-text">No 543 (0.2%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 272,606 / 563,910 (48.3%) · Quorum 25% (140,977)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="87/" class="prop-card-title">#87 – Remove Kimi K2.6 model</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-16</span>
    <span>Voting ends 2026-07-16</span>
  </div>
  <div class="prop-card-desc">Remove moonshotai/Kimi-K2.6 from PoC params and delete it from the governance model list.</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 151,714 (100.0%)</span> · <span class="prop-tally-no-text">No 8 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 151,722 / 344,693 (44.0%) · Quorum 25% (86,173)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="86/" class="prop-card-title">#86 – Increase Kimi-K2.6 and GLM-5.2 weight_scale_factor by 5%</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-14</span>
    <span>Voting ends 2026-07-16</span>
  </div>
  <div class="prop-card-desc">Increase the weight_scale_factor for moonshotai/Kimi-K2.6 from 0.90 to 0.945 (+5%) and for zai-org/GLM-5.2-FP8 from 2.47 to 2.5935 (+5%). All other model and chain parameters remain unchanged.</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 299,231 (98.5%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 4,445 (1.5%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 303,676 / 564,299 (53.8%) · Quorum 25% (141,074)</span></div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="85/" class="prop-card-title">#85 – Internal Go-To-Market Team for 3 Month</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-10</span>
    <span>Voting ends 2026-07-12</span>
  </div>
  <div class="prop-card-desc">We will run hundreds of experiments across different target audience hypotheses and set up the basis: acquisition funnels, analytics, sharable target audience deep understanding. Our key performance m…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 41,668 (73.5%)</span> · <span class="prop-tally-no-text">No 8 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 14,932 (26.4%)</span> · <span class="prop-tally-abstain-text">Abstain 45 (0.1%)</span><span class="prop-card-funding prop-card-funding-rejected">600,000 GNK · $36,000 · Community Pool</span></div>
  <div class="prop-card-tally"><span class="prop-tally-veto-text">✗ Turnout 56,653 / 741,825 (7.6%) · Quorum 25% (185,456)</span></div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="84/" class="prop-card-title">#84 – Bringing $3M+ in New Capital to GONKA via Uniswap — Phase 1/6 ($50k USDT)</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-09</span>
    <span>Voting ends 2026-07-11</span>
  </div>
  <div class="prop-card-desc">My name is Andrey Orlovsky, and through this proposal I represent our team and an initiative to attract at least $3 million in new long-term capital to GONKA through Uniswap.  Below is a condensed ver…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 1,221 (0.4%)</span> · <span class="prop-tally-no-text">No 2,404 (0.8%)</span> · <span class="prop-tally-veto-text">Veto 290,022 (98.8%)</span> · <span class="prop-tally-abstain-text">Abstain 3 (0.0%)</span><span class="prop-card-funding prop-card-funding-rejected">20,000 GNK · $50,000 · Community Pool</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 293,650 / 741,825 (39.6%) · Quorum 25% (185,456)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="83/" class="prop-card-title">#83 – Approve devshard v3</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-09</span>
    <span>Voting ends 2026-07-11</span>
  </div>
  <div class="prop-card-desc">Update current chain params by adding v3 to devshard_escrow_params.approved_versions.</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 395,370 (100.0%)</span> · <span class="prop-tally-no-text">No 0 (0.0%)</span> · <span class="prop-tally-veto-text">Veto 0 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 395,370 / 741,825 (53.3%) · Quorum 25% (185,456)</span></div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="82/" class="prop-card-title">#82 – External Test Lab x Community DevNet</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-08</span>
    <span>Voting ends 2026-07-10</span>
  </div>
  <div class="prop-card-desc">4-month pilot of the External Test Lab & Community DevNet: a community-owned testing layer for Gonka. Full proposal and discussion: <a href="https://github.com/gonka-ai/gonka/discussions/1388" target="_blank">https://github.com/gonka-ai/gonka/discussions/1388</a>  The budget is he…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 368,084 (98.2%)</span> · <span class="prop-tally-no-text">No 468 (0.1%)</span> · <span class="prop-tally-veto-text">Veto 94 (0.0%)</span> · <span class="prop-tally-abstain-text">Abstain 6,141 (1.6%)</span><span class="prop-card-funding">80,000 GNK · $88,000 · Community Pool</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 374,787 / 741,825 (50.5%) · Quorum 25% (185,456)</span></div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="81/" class="prop-card-title">#81 – Kimi cPoC Restitution (epochs 306-309)</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-08</span>
    <span>Voting ends 2026-07-10</span>
  </div>
  <div class="prop-card-desc">Distribute restitution for Kimi operators affected by cPoC validation failure in epochs 306-309. The Kimi validation path failed starting in e306 causing confirmation_weight suppression for Kimi opera…</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 235,728 (56.2%)</span> · <span class="prop-tally-no-text">No 609 (0.1%)</span> · <span class="prop-tally-veto-text">Veto 183,094 (43.7%)</span> · <span class="prop-tally-abstain-text">Abstain 18 (0.0%)</span><span class="prop-card-funding prop-card-funding-rejected">175,082 GNK · Gov Module</span></div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">✓ Turnout 419,449 / 741,825 (56.5%) · Quorum 25% (185,456)</span></div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="80/" class="prop-card-title">#80 – GRC Proposal #3 - Restitution</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-05</span>
    <span>Voting ends 2026-07-07</span>
  </div>
  <div class="prop-card-desc">Restitution payout for confirmed GRC Proposal #3 cases, with Case 05 payments from proposal_id=67 deducted where the same address and epoch were already compensated, and positive victim outputs below …</div>
  <div class="prop-card-tally"><span class="prop-tally-yes-text">Yes 16,378 (10.4%)</span> · <span class="prop-tally-no-text">No 94,721 (60.4%)</span> · <span class="prop-tally-veto-text">Veto 39,454 (25.1%)</span> · <span class="prop-tally-abstain-text">Abstain 6,344 (4.0%)</span><span class="prop-card-funding prop-card-funding-rejected">47,850 GNK · Community Pool · 70,184 GNK · Gov Module</span></div>
  <div class="prop-card-tally"><span class="prop-tally-veto-text">✗ Turnout 156,897 / 741,825 (21.2%) · Quorum 25% (185,456)</span></div>
</div>

</div>

<p><a href="../"><em>← Back to all proposals</em></a></p>
