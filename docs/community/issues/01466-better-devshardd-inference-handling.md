---
title: "#1466 — Better devshardd inference handling"
source: https://github.com/gonka-ai/gonka/issues/1466
issue_number: 1466
synced_at: 2026-08-02T19:38:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Better devshardd inference handling
    <span class="issues-number">#1466</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-07-17 09:59 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-23 21:22 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
While reviewing this PR: https://github.com/gonka-ai/gonka/pull/1460 I have found couple of problems/tasks, and listed them at PR comment https://github.com/gonka-ai/gonka/pull/1460#issuecomment-5001774184

1. Unify accept/execute paths (should be targeted by https://github.com/gonka-ai/gonka/pull/1460 PR)

Problem: User SSE (signReceipt) and timeout challenge (challengeReceiptLocked) both do verify → sign receipt → dedup → maybe execute, but as duplicated logic that already diverges (ConfirmStart, cache replay, soft-fail semantics). Challenge also blocks the receipt RPC on full ML, unlike SSE.

Task: Extract one shared “accept as executor” helper; thin SSE vs challenge wrappers; challenge returns receipt without waiting on ML.

2. Gateway disconnect must not kill executor proof

Problem: Today, if the host→client (or gateway→host) stream dies in a way that cancels host→ML, generation can abort. Then the executor may never publish a clean MsgFinishInference, so the work isn’t accountable/validatable even though the host had accepted it. A drop by devshardctl/user must not be a reason the executor fails to produce execution proof.

Task: Decouple ML execution lifetime from the outbound user/gateway stream. After receipt/accept, run inference to completion (or controlled failure) under a host-owned context; always try to land MsgFinishInference (+ cache body) even if the client has gone. Treat stream write failure as delivery loss, not work cancellation.

3. Same-nonce reconnect for devshardctl

Problem: Host can re-serve receipt / CachedResponseBody on the same StartInference, but devshardctl never resends the same nonce—it opens new attempts. After an accidental drop, the user side can’t reattach to in-flight or finished work on that nonce.

Task: On disconnect/retry, allow devshardctl to resend the same nonce with the same payload/params (reject mismatch via prompt/params hash). Host validates equality, skips re-execute if already running/done, and returns receipt + live/cached stream (CachedResponseBody when complete).

4. HA / fault-tolerance across devshardd instances

Problem: In-flight inference state (payload, execution progress, cached response) lives in process memory. If a connection drops mid-serve, or devshardd reboots/fails over, another instance can’t resume: no durable payload, no way to reattach to an ML job still running, no disk CachedResponseBody. Work is lost or must be blindly restarted without shared proof.

Task: Persist, until the inference is finished/settled: payload + parameters (for same-hash reconnect), execution/receipt metadata, and CachedResponseBody (on disk). On another devshardd: if ML still running, reconnect to that job; else recreate from stored payload; serve reconnecting clients the live stream or cached body. Goal: drop/reboot/failover doesn’t erase the path to a validatable MsgFinishInference.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-07-23 14:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>When working with this ussue PR https://github.com/gonka-ai/gonka/pull/1496 should be taken into account, that implements HA redesign</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1466](https://github.com/gonka-ai/gonka/issues/1466) every hour.
