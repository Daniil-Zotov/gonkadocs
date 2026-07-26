---
title: "#797 — New nodes can't join from snapshots with error"
source: https://github.com/gonka-ai/gonka/issues/797
issue_number: 797
synced_at: 2026-07-26T07:08:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    New nodes can't join from snapshots with error
    <span class="issues-number">#797</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-24 19:35 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-02-25 17:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
**This is an urgent, open issue, and many contributors are working on it in parallel.**

There is a quite weird issue today - new nodes can't join from snapshots with error like that:
```
5:49AM ERR error in proxyAppConn.FinalizeBlock err="no validator signing info found" module=consensus
```
[no-validator-signing.log](https://github.com/user-attachments/files/25529057/no-validator-signing.log)

Seems like there is no signing info in snapshot. But that issue happens with different set of peers for state sync (pex=false) and seems reproducable in most cases 

Experiment was done to ignore this issue in cosmos-sdk and them it fails like the state doesn't have slashing params also 

Seems like active nodes had all this data at the state at this height 

How to reproduce it - to start new node, it is likely you get it (it passes with some snapshots, which makes everything even stranger)

main hypothesis that something is with producing snapshots, it's cosmo-sdk level

There is also a hypothesis that it is somehow connected to slashing, as it started to happen when collateral was activated. But we are not sure.

it happens the same block the validator list usually updated.

Also, collateral needs to be checked. 
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/hleb-albau">@hleb-albau</a></span>
    <span class="issues-meta-item">commented 2026-02-24 19:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>As a workaround(before fix), it is possible to just compress data folder(except some filers) and distribute it as is archive. Quite popular in cosmos world. See https://snapshots.osmosis.zone/index.html as example</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-24 20:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@hleb-albau thanks, that makes sense and it’s a well-known approach in the Cosmos ecosystem. You are right, it’s more of an operational workaround than a real fix (it doesn’t address the underlying issue we’re trying to solve)</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/blizko">@blizko</a></span>
    <span class="issues-meta-item">commented 2026-02-24 21:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Additional feedback:
The issue was observed before collateral slashing was activated. During epoch 179 have been observing same error.
Known failed attempt time around Feb 21st 01:47 UTC</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-24 23:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The issue is in <a href="https://github.com/cosmos/iavl/tree/v1.2.4">cosmos/iavl v1.2.4</a></p>
<p>After snapshot restore, IAVL rebuilds a "fast node" index by iterating the tree. If the iterator hits an error mid-way, it silently stops - the error is never stored (<a href="https://github.com/cosmos/iavl/blob/v1.2.4/iterator.go#L230-L235">iterator.go:230-235</a>). The fast index ends up incomplete, but IAVL marks it as ready</p>
<p>Then when the node starts processing blocks, <code>Get()</code> checks the fast index, doesn't find the key, and assumes it doesn't exist - without checking the actual tree (<a href="https://github.com/cosmos/iavl/blob/v1.2.4/immutable_tree.go#L192-L198">immutable_tree.go:192-198</a>). The data is in the tree, but the code never reaches it</p>
<p>That's why slashing module gets <code>nil</code> -&gt; <code>no validator signing info found</code> -&gt; crash</p>
<p>The exact error that triggers the iterator failure is still unknown - since IAVL swallows it, there's no way to see it without patching the code</p>
<p><strong>Workaround (was found by @gmorgachev):</strong> setting <code>iavl-disable-fastnode = true</code> on the same snapshot - works immediately. This skips the fast index and reads the tree directly</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-25 17:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://gonka.ai/FAQ/#how-do-i-fix-errno-validator-signing-info-found-when-starting-from-a-state-sync-snapshot</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #797](https://github.com/gonka-ai/gonka/issues/797) every hour.
