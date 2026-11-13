---
title: "#2244 — [Discussion] Tx fees: enable the remaining groups?"
source: https://github.com/gonka-ai/gonka/issues/2244
issue_number: 2244
synced_at: 2026-11-13T08:08:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [Discussion] Tx fees: enable the remaining groups?
    <span class="issues-number">#2244</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 23:16 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-11 14:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zpoken">@zpoken</a></span>
    <span class="issues-meta-item">commented 2026-11-11 14:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd enable <code>ibc</code> together with <code>wasm</code> in v0.2.17, do <code>onboarding</code>/<code>devshard</code>/<code>governance</code> at 1, and hold off on <code>bridge</code>. <code>bls</code> doesn't matter.</p>
<p>Revenue isn't really the point. One epoch I sampled had ~8k txs, most blocks outside PoC/DKG windows were empty, and there were no ibc or onboarding txs at all. Even at 1000 ngonka/gas all the free groups together would bring in maybe ~1.4k GNK/day. Also <code>AllocateTokens</code> is a no-op in SDK fork, so whatever we collect just piles up in <code>fee_collector</code> (~288 GNK now). Probably worth deciding what that's for at some point.</p>
<p>Per group:</p>
<ul>
<li><code>ibc</code>: with #2218 as is it gets the 100M cap but no price, so zero-fee 100M-gas txs can eat the IBC block budget and fill the mempool (maksimenkoff's repro in #2218). I'd price it at 1000 like wasm. At 1, 5k of those txs only need ~500 GNK of balance. Heads up that adding it to <code>enabled_fee_groups</code> isn't enough: the v0.2.17 handler creates the row with <code>min_gas_price = 0</code>, so that has to be set too.</li>
<li><code>onboarding</code>: fine at 1, as in #2218.</li>
<li><code>devshard</code>: only Create and SetRequestsEnabled would pay, Settle is a duty. Keep it at 1. <code>devshardctl</code> sends a hardcoded 1M ngonka fee and the gateway declares ~700k gas, so 2 would already underpay.</li>
<li><code>governance</code>: only external SubmitProposal/Vote/Deposit pay; anything executed by a passed proposal skips ante. Harmless at 1, low priority.</li>
<li><code>bridge</code>: this one would make hosts pay for <code>MsgBridgeExchange</code> (the bridge votes) out of the cold feegrant. The cost is tiny, but bridge voting would then depend on the grant not running out, and <code>epoch-fee-budget</code> doesn't count it. I'd make it a duty with a signer check first.</li>
<li><code>bls</code>: all 5 msgs are compiled duties, so enabling it changes nothing. #2252 is the actual fix.</li>
</ul>
<p>Some things pricing won't fix:</p>
<ul>
<li>Duty bypass is type-only with no signer check (#1539, #1576, #2252).</li>
<li><code>MsgTransferOwnership</code> has no group and isn't a duty, so it's free whatever we enable.</li>
<li>DAPI always sets the cold feegranter, and the SDK calls <code>UseGrantedFees</code> even for a zero fee. If a host's grant expires or gets removed, even its free PoC/BLS txs fail. Grants also aren't uniform: 10 GNK by default, while the v0.2.12 migration gave 100 GNK with a 1-year expiry.</li>
<li>Simulate skips <code>txFeeChecker</code>, so it skips the group gas cap too. The comment in <code>group_gas.go</code> says otherwise.</li>
<li><code>FeeParams.Validate</code> doesn't require the wasm/ibc rows but <code>CappedGroups</code> does. A full inference <code>MsgUpdateParams</code> carrying the old tree would stop direct wasm/ibc txs, so fee proposals need to start from current params.</li>
<li><code>ensureGroupGasCeilings</code> only fills defaults on nil. A non-nil empty tree makes the v0.2.17 upgrade fail with "epoch fee group missing". Not an issue for mainnet right now, but cheap to fix.</li>
</ul>
<p>Keplr's Gonka config uses gas price 1/1.5/2 and chain-registry has 0. Direct wasm txs (e.g. wrapped-token withdrawals) from wallets using those defaults will get rejected, and simulate won't catch it since it skips the fee check. Worth checking what the dashboard sets for those calls before wasm goes to 1000.</p>
<p>Minor: the #2218 description still mentions <code>block.max_gas = 200M</code>, and <code>docs/tokenomics.md</code> still says there are no gas fees.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2244](https://github.com/gonka-ai/gonka/issues/2244) every hour.
