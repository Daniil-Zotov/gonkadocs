---
title: "#521 — Create a proxy endpoint that aggregates multiple internal RPC nodes behind a single public-facing address (for crypto wallets)"
source: https://github.com/gonka-ai/gonka/issues/521
issue_number: 521
synced_at: 2026-07-06T09:51:54Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #521](https://github.com/gonka-ai/gonka/issues/521) every 6 hours. 

# 🔴 Create a proxy endpoint that aggregates multiple internal RPC nodes behind a single public-facing address (for crypto wallets)

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-01-06 00:34 UTC · **Updated:** 2026-06-04 19:10 UTC

**Веха:** v0.2.14

---

## 📝 Описание

@GLiberman @gmorgachev please evaluate how viable this solution would be.

Current issue with wallet connections:
At the moment, wallets can be configured to use only a single address. If that address becomes unavailable, the wallet stops working.

For example, this happened when 6block shut down their node 3, and Keplr was no longer able to connect.

Proposed idea:
Introduce a proxy endpoint that sits in front of all available HTTPS endpoints (6block, Hyperfusion, PS, etc). This way, if individual nodes go offline, wallets would still be able to operate without interruption.

Wdyt?

CC @kotelnikova 

---

## 💬 Comments (7)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-23 19:23 UTC*

@kotelnikova, could you please share the technical requirements?

### Комментарий 2 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-06-03 02:19 UTC*

I'll take it, thank you! @tcharchian 

### Комментарий 3 — [@gonkalabs](https://github.com/gonkalabs)

*2026-06-03 22:32 UTC*

Hi!

Just to add some context from our side: https://rpc.gonka.gg acts as a routing layer in front of multiple RPC upstreams. It routes traffic between our own RPC nodes (we have multiple own feather rpc nodes) and node1.gonka.ai-node3.gonka.ai, periodically health-checks each upstream, and automatically fails over when one of them becomes unavailable.

The routing priority is set to prefer our own Feather RPC nodes first, so we do not put unnecessary load on the core gonka.ai RPC infrastructure. The upstream pool can be extended if needed to almost any size.

At the moment, we are processing several million RPC requests per day through our rpc layer, which is roughly 20% of the current capacity. Capacity is mostly limited by server resources, so we can scale it up if traffic grows.

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-06-03 22:47 UTC*

@gonkalabs thanks, this makes sense. Would it be possible to extend the upstream pool with for example 6block and Hyperfusion, as fallback upstreams as well?

Do your health checks only verify availability, or do they also check whether the upstream is lagging behind? For wallet reliability, it would be important to fail over not only when a node is down, but also when it is stale.

### Комментарий 5 — [@gonkalabs](https://github.com/gonkalabs)

*2026-06-03 23:09 UTC*

@tcharchian Yes, we can extend the upstream pool with more members: hyperfusion, 6block - no problem! 

Yes, we test chain-tip lag of upstreams as well as latency and general up/down status, so stale detection is one of the criteria when service selects the upstream for a request

### Комментарий 6 — [@tcharchian](https://github.com/tcharchian)

*2026-06-03 23:26 UTC*

@gonkalabs thanks, please let me know once you add more members

### Комментарий 7 — [@gonkalabs](https://github.com/gonkalabs)

*2026-06-04 18:51 UTC*

@gonkalabs we added Hyperfusion and 6block rpc to the upstream list! 

Bellow is a diagram of routing. All nodes are latency, tip-tested.

Also, we significantly encreased rpc throughput, and made service completely work without any api keys and without any limits! So anyone can use this routing layer to access the combined stability of many upstreams!

<img width="1449" height="583" alt="Image" src="https://github.com/user-attachments/assets/adc87e0c-f661-429f-9a42-07540faac3f8" />
