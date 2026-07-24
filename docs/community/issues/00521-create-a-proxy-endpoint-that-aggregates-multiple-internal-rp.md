---
title: "#521 — Create a proxy endpoint that aggregates multiple internal RPC nodes behind a single public-facing address (for crypto wallets)"
source: https://github.com/gonka-ai/gonka/issues/521
issue_number: 521
synced_at: 2026-07-24T15:49:22Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Create a proxy endpoint that aggregates multiple internal RPC nodes behind a single public-facing address (for crypto wallets)
    <span class="issues-number">#521</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-06 00:34 UTC</span>
    <span class="issues-meta-item">7 comments</span>
    <span class="issues-meta-item">Updated 2026-06-04 19:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
@GLiberman @gmorgachev please evaluate how viable this solution would be.

Current issue with wallet connections:
At the moment, wallets can be configured to use only a single address. If that address becomes unavailable, the wallet stops working.

For example, this happened when 6block shut down their node 3, and Keplr was no longer able to connect.

Proposed idea:
Introduce a proxy endpoint that sits in front of all available HTTPS endpoints (6block, Hyperfusion, PS, etc). This way, if individual nodes go offline, wallets would still be able to operate without interruption.

Wdyt?

CC @kotelnikova 
</div>

---

## 💬 Comments (7)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-23 19:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@kotelnikova, could you please share the technical requirements?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-03 02:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'll take it, thank you! @tcharchian </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-06-03 22:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi!</p>
<p>Just to add some context from our side: https://rpc.gonka.gg acts as a routing layer in front of multiple RPC upstreams. It routes traffic between our own RPC nodes (we have multiple own feather rpc nodes) and node1.gonka.ai-node3.gonka.ai, periodically health-checks each upstream, and automatically fails over when one of them becomes unavailable.</p>
<p>The routing priority is set to prefer our own Feather RPC nodes first, so we do not put unnecessary load on the core gonka.ai RPC infrastructure. The upstream pool can be extended if needed to almost any size.</p>
<p>At the moment, we are processing several million RPC requests per day through our rpc layer, which is roughly 20% of the current capacity. Capacity is mostly limited by server resources, so we can scale it up if traffic grows.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-03 22:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@gonkalabs thanks, this makes sense. Would it be possible to extend the upstream pool with for example 6block and Hyperfusion, as fallback upstreams as well?</p>
<p>Do your health checks only verify availability, or do they also check whether the upstream is lagging behind? For wallet reliability, it would be important to fail over not only when a node is down, but also when it is stale.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-06-03 23:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian Yes, we can extend the upstream pool with more members: hyperfusion, 6block - no problem! </p>
<p>Yes, we test chain-tip lag of upstreams as well as latency and general up/down status, so stale detection is one of the criteria when service selects the upstream for a request</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-03 23:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@gonkalabs thanks, please let me know once you add more members</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-06-04 18:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@gonkalabs we added Hyperfusion and 6block rpc to the upstream list! </p>
<p>Bellow is a diagram of routing. All nodes are latency, tip-tested.</p>
<p>Also, we significantly encreased rpc throughput, and made service completely work without any api keys and without any limits! So anyone can use this routing layer to access the combined stability of many upstreams!</p>
<p><img width="1449" height="583" alt="Image" src="https://github.com/user-attachments/assets/adc87e0c-f661-429f-9a42-07540faac3f8" /></p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #521](https://github.com/gonka-ai/gonka/issues/521) every hour.
