---
title: "#1992 — v7 should account inferences, not nonces"
source: https://github.com/gonka-ai/gonka/issues/1992
issue_number: 1992
synced_at: 2026-10-15T00:36:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    v7 should account inferences, not nonces
    <span class="issues-number">#1992</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-13 18:11 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-13 19:30 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Issue: v7 should account inferences, not nonces

**Target:** v7  
**Related:** [PR #1991](https://github.com/gonka-ai/gonka/pull/1991) — `fix(devshard): default quiet settle to 5m; keep 5s in testenv`

## Problem

v6 charges `FeePerNonce` for every applied diff while the escrow is active. The nonce counter and the inference counter are the same number. A compose that does not open an inference still advances the nonce and pays the fee.

That includes the quiet-settle nonce. Quiet settle is the last-chat flush: the host has already finished, and the gateway is only publishing the queued ConfirmStart / receipt and Finish so the protocol can mark that inference finished and release the hold. It is not a new Start. It exists because heartbeat is off by default, and nothing else composes those txs when the escrow goes quiet.

[PR #1991](https://github.com/gonka-ai/gonka/pull/1991) does not change this. It lengthens the production quiet-settle wait from 5s to 5m so sparse traffic is more likely to fold the leftovers into the next Start. The trailing compose still advances the nonce and still pays `FeePerNonce`. A gap longer than five minutes still spends a nonce that is not an inference.

## What v7 should do

Count inferences, not nonces, on the fee and accounting surface that `FeePerNonce` covers today.

- An inference is a chat Start (the nonce that opens the request).
- The quiet-settle compose is settlement plumbing. It publishes receipt and Finish for an inference that already exists. It must not be counted as an inference, and it must not pay an inference fee.
- A later Start that absorbs those same leftovers is one inference. The absorbed receipt and Finish ride that Start; they do not add a second inference.

The flush itself stays. Lengthening the delay only reduces how often the extra nonce is composed. v7 has to stop treating that compose as an inference, including while heartbeat stays off and quiet settle is still the last-chat flush.

</div>

---

> 🔄 **Auto-synced** from [Issue #1992](https://github.com/gonka-ai/gonka/issues/1992) every hour.
