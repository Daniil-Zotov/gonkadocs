---
title: "#1821 — Cosmos SDK / fork security v0.2.18"
source: https://github.com/gonka-ai/gonka/issues/1821
issue_number: 1821
synced_at: 2026-09-25T07:57:21Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Cosmos SDK / fork security v0.2.18
    <span class="issues-number">#1821</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-09-22 02:35 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-24 21:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
Cosmos SDK fork security for v0.2.18. Nothing huge: targeted fork patches first, full rebase only if it stays in scope.

Chain-halt fixes can ship on the current `v0.53.3-ps19` fork without waiting for v0.53.8. The rebase is a second, state-breaking step and needs its own test pass.

Needs thorough testing before merge.

## Sub-issues

- #1708 chain-halt: `ValidatorByConsAddr` returns `ErrNoValidatorFound` (gonka-ai/cosmos-sdk#19)
- #1205 chain-halt: `markValidatorForDeletion` jailed-delete race (gonka-ai/cosmos-sdk#16)
- #1719 ECIES: restore curve validation, reject short ciphertexts (gonka-ai/cosmos-sdk#20)
- #1671 rebase fork onto upstream v0.53.8

## Related fork PRs  

- gonka-ai/cosmos-sdk#14 stale consensus-key conflicts
- gonka-ai/cosmos-sdk#17 skip tombstoned validators in epoch recompute
- gonka-ai/cosmos-sdk#10 snapshot chunk deletion during state sync (see also #632)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-09-24 21:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Local test pass over the fork PRs listed here, since the fork's own CI doesn't run them (every job on outside PRs sits <code>action_required</code>/cancelled, and most jobs were cancelled on #18 too). Environment: WSL, go1.24.2, <code>gonka-ai/cosmos-sdk</code> <code>release/v0.53.x</code> @ <code>c8229ef61</code> (= <code>v0.53.3-ps19-observability</code>, the tag inference-chain pins). Details are in each PR:</p>
<ul>
<li><strong>gonka-ai/cosmos-sdk#19</strong> (<code>ValidatorByConsAddr</code> → <code>(nil, nil)</code>): its tests fail on the base and pass on the PR. The evidence path is fixed. The slashing path still returns <code>ErrNoValidatorFound</code> one call earlier, via <code>IsValidatorJailed</code> in <code>HandleValidatorSignature</code> (integration test in the PR comment).</li>
<li><strong>gonka-ai/cosmos-sdk#16</strong> (<code>markValidatorForDeletion</code>): both tests fail on the base and pass on the PR. A multi-block run shows the removed validator stays resolvable for at least 5 EndBlocks, so there's no early deletion inside CometBFT's update lag.</li>
<li><strong>gonka-ai/cosmos-sdk#14</strong> (stale consensus keys): all 9 added tests pass. Per the simulation sweep in that thread, it should land with or after #19.</li>
<li><strong>gonka-ai/cosmos-sdk#17</strong> (tombstoned validators): its test passes. It's inert until the <code>SetTombstoneChecker(app.SlashingKeeper.IsTombstoned)</code> wiring lands in <code>inference-chain/app</code>.</li>
<li><strong>gonka-ai/cosmos-sdk#10</strong> (snapshot pruning): it protects a single in-flight chunk read, but not the gap between two chunk requests of one transfer, which is the #632 failure (probe test in the comment). It also needs a new <code>store/v1.1.2-psN</code> tag to reach inference-chain.</li>
</ul>
<p><strong>The chain-halt set composes:</strong> #14, #16, #17 and #19 merge cleanly together. On the combined branch, all of their own tests pass. The full root module (<code>x/...</code>, <code>baseapp</code>, <code>types</code>) plus <code>tests/integration/...</code> fails exactly the same tests as <code>release/v0.53.x</code> alone. The one extra failure in the first run, <code>x/distribution/simulation</code> <code>TestSimulateMsgWithdrawValidatorCommission</code>, flakes 2/5 on the base as well.</p>
<p><strong>One thing that limits "thorough testing" of anything in the fork:</strong> <code>release/v0.53.x</code> itself fails 69 top-level tests (72 subtests) across 18 packages:
- <code>x/{bank,distribution,gov,slashing,staking}</code> (keeper and simulation), <code>types</code>, <code>types/bech32/legacybech32</code>
- <code>tests/integration/{distribution,evidence,gov,slashing,staking}</code></p>
<p>The failures I traced are stock-SDK expectations of paths the fork disabled on purpose: <code>MsgDelegate</code>/<code>MsgUndelegate</code>/<code>MsgBeginRedelegate</code>/<code>MsgCancelUnbondingDelegation</code> return "is disabled", <code>RemoveValidatorTokensAndShares is disabled after genesis in Proof of Compute mode</code>, and the no-op bank keeper leaves balances untouched. I haven't classified all 69, and <code>types</code>/<code>legacybech32</code> in particular I didn't look into. In this state the unit suites can't flag a regression, because every package that matters is already red.</p>
<p>If it's useful, I can open a test-only PR against <code>release/v0.53.x</code> that marks the by-design divergences with <code>t.Skip</code> and a one-line reason each, and lists anything that doesn't fit that pattern for someone to look at. That would make a green baseline to test fork patches against. Happy to take a different approach if you'd rather delete those tests or keep them as they are.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1821](https://github.com/gonka-ai/gonka/issues/1821) every hour.
