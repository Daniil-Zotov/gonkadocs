---
title: "#1398 — Gateway allowlist request: niro"
source: https://github.com/gonka-ai/gonka/issues/1398
issue_number: 1398
synced_at: 2026-07-07T21:45:43Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request: niro
    <span class="issues-number">#1398</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@niro58](https://github.com/niro58) opened 2026-07-04 20:09 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-04 20:11 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator

Nichita R. — independent developer
Contact: GitHub @niro58

## Address

gonka142rw2k5qwh3rxm774z56uzcgfyqfnnclqewr36

## Models

- MiniMaxAI/MiniMax-M2.7
- moonshotai/Kimi-K2.6

## Use case

We run nine production apps (SaaS, content platform, mobile apps, AI tooling)
that route all text + tool-calling inference through Gonka via a community
broker. We'd like to move to a self-hosted devshard gateway to pay inference
from our own GNK.

Expected volume is tenths thousands of requests/day, around 100-300 mil tokens a day, growing with our user base.
Happy to share availability telemetry and benchmark results with the network.
</div>

---

> 🔄 **Auto-synced** from [Issue #1398](https://github.com/gonka-ai/gonka/issues/1398) every hour.
