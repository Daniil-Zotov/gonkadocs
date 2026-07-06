---
title: "#818 — Slow nodes investigation"
source: https://github.com/gonka-ai/gonka/issues/818
issue_number: 818
synced_at: 2026-07-06T09:52:36Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #818](https://github.com/gonka-ai/gonka/issues/818) каждые 6 часов. 

# 🟢 Slow nodes investigation

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-02-27 21:07 UTC · **Обновлено:** 2026-03-18 14:23 UTC

**Метки:** `help wanted` `up-for-grabs` `Priority: High`

---

## 📝 Описание


### Discussed in https://github.com/gonka-ai/gonka/discussions/817

<div type='discussions-op-text'>

<sup>Originally posted by **tcharchian** February 27, 2026</sup>

Task: Multiple hosts reported node slowdowns in the last days. Need to identify common patterns and mitigate.


---

## 💬 Комментарии (7)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-03-03 10:33 UTC*

PR: https://github.com/gonka-ai/gonka/pull/844

### Комментарий 2 — [@sysmanalex](https://github.com/sysmanalex)

*2026-03-03 18:20 UTC*

- Imho for bottleneck location and deep diagnostics - we need some profiling, debug, logs and metrics here.
also imho cosmos-SDK, IAVLX (SDK v0.54+), write operation and some gRPC I mention upper should help.
(doesn't solve totally more postpone bottlenecks will appear later, but they will still appear under heavy load on a larger network.)

### Комментарий 3 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-04 09:16 UTC*

> * Imho for bottleneck location and deep diagnostics - we need some profiling, debug, logs and metrics here.
>   also imho cosmos-SDK, IAVLX (SDK v0.54+), write operation and some gRPC I mention upper should help.
>   (doesn't solve totally more postpone bottlenecks will appear later, but they will still appear under heavy load on a larger network.)


https://gonka.gg/public-api/



### Комментарий 4 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-06 14:21 UTC*

L8 (latency consistency) axis in GiP #860 measures this directly.

Live measurement (proxy.gonka.gg, Qwen3-235B, 16 requests, Mar 6 2026):
  mean:  1280ms
  σ:     876ms
  CV:    0.68  ← primary signal
  p95:   2621ms
  min:   553ms / max: 2621ms

CV=0.68 means the slowest node delivers the same request in ~4× the time of
the fastest. Current GetRandomExecutor routes to both equally — the slow node
gets the same traffic share as the fast one.

Phase 4 of GiP #860 (GetQualityWeightedExecutor) routes traffic proportional
to L8 score (1 − CV per epoch). Nodes with high latency variance get less
traffic automatically, without manual investigation per node.

Projection from routing simulation: mean latency ↓15%, σ ↓40% as
high-CV nodes are progressively deprioritized.

Data + design: docs/specs/inference-quality-protocol.md in PR #859 branch.
Discussion: #860

### Комментарий 5 — [@sysmanalex](https://github.com/sysmanalex)

*2026-03-06 22:33 UTC*

My imho - 16 requests is too small measurement.
- I see several logical errors, risks, and unobvious long-term consequences here
1) The measurements were taken on a MiniLM-L6-v2 (384 dimensions, without a GPU). 
GPUs behave differently and have high latencies write/read shared mem, especially for large requests, up to seconds!
 For a large model, if there's a large request or response, it's sent in chunks. The spread will be large.
(node can be alive, but may still serve perv request - without alv capacity.)
2) a) When the network load is 50-75-90%, routing toward the fastest node will automatically load it, which will cause it to lag, and latency will increase. (network should know capacity and load.)
b) A node that's delay by 1000 reasons, including network/tcp delay/miss/dissorder 
-  may return with in a second back.
seems here is two layers network and gpu/llm models. for network more logical use ping-beacons.
for llm models - router should try again later always, otherwise this will lead to exclude for long time - any delayed node, this will lead to low LLM/model/GPU network inefficiency/idle hw, waste or resources.
b) at simple cases, some nodes/areas can just lag/ddos/net-split for 2-5-90 sec - will statistically lead to high_weight for alive and down_weight for lagged - with huge distance. 
router cache - should have **expire_time** & fail_attempts always, smarter logics.
(seems lose to typical HA High availability clusters.)
p.s. **p2p mesh network** is always meaning - different travel time/vary_latency/re-route/splits/re-orgs.
only dedicated core with multi-leg low latency can compensate this.
p2p mesh for btc is ok, for Gonka imho different way.

### Комментарий 6 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-18 14:20 UTC*

>RE

My calculations for splitting results between participants for efficiency are supported by current pull requests, but the instance is initialized with Docker and doesn't use the GPU. While the bridge idea is relevant and is reflected in the metrics from your point 2, it's worth addressing separately.

I'm currently testing this in the development paradigm and current solutions: one-shot minimum GPU computations using goroutine threads within instances.

It turns out that even alpha testing shows the absolute effectiveness of the semantic cache in terms of CPU time before using the GPU. This depends on the developer's performance and the number of currently closed pull requests. The next few weeks should reveal the developer's effectiveness.

How this might impact the protocol, hosts, and a separate pull request.

### Комментарий 7 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-18 14:23 UTC*

> * Imho for bottleneck location and deep diagnostics - we need some profiling, debug, logs and metrics here.
>   also imho cosmos-SDK, IAVLX (SDK v0.54+), write operation and some gRPC I mention upper should help.
>   (doesn't solve totally more postpone bottlenecks will appear later, but they will still appear under heavy load on a larger network.)

I just thought about providing the node starter pack with this comprehensive solution.
