---
title: "#1480 — Gateway allowlist request: Ancapex"
source: https://github.com/gonka-ai/gonka/issues/1480
issue_number: 1480
synced_at: 2026-07-19T22:12:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request: Ancapex
    <span class="issues-number">#1480</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/alancapex">@alancapex</a> opened 2026-07-19 21:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-19 21:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Operator**

Ancapex — mining platform for Gonka (https://ancapex.ai/)
Contact: <GitHub @alancapex / al@ancapex.ai>
About Ancapex

Ancapex is a platform for mining on the Gonka Network. Launched as a public pool in December 2025, it gives anyone the ability to participate in Gonka mining without running their own node or managing server infrastructure.

Since launch, the platform has attracted over 1,500 deposits with a total volume exceeding $350,000. The team continuously ships new features - most recently, in-platform governance voting, which allows Ancapex users to participate in Gonka Network proposals directly through the platform, with each user's vote counted individually and proportionally to their mining share.

**Address**

gonka1fnnjn8nr978tzrjknum3kqwdm24gc9sernrpae

**Models**

Any

**Use case**

We're building a platform designed to serve both our clients and autonomous agents. This is custom development at the gateway level, which a shared gateway with fixed behavior can't accommodate:


Custom custody schemes — different client types require different custody and payment arrangements; some must settle non-custodially, with no intermediary holding client funds, which a broker ledger can't provide.
Agentic payments — agents paying for inference programmatically from accounts they control, with our entities as on-chain payer-of-record where required.
Execution lifecycle control — our own management of session/escrow lifecycle, timeouts, retries, and rotation cadence, tuned to agent workloads (we understand routing and per-token pricing are protocol-defined and expect no performance advantage from self-hosting — this is about gateway behavior, not the network).
Operator-side protocol work — we'll run our own devshardd v1/v2 integration and keep feeding operator-side issues and fixes back here, which isn't possible from behind a proxy.


Once our development stabilizes, we'll contribute the generalized schemes back to open source, as we've done with our previous work. 
</div>

---

> 🔄 **Auto-synced** from [Issue #1480](https://github.com/gonka-ai/gonka/issues/1480) every hour.
