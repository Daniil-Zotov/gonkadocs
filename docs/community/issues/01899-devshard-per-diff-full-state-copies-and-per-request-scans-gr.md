---
title: "#1899 — devshard: per-diff full-state copies and per-request scans grow with the escrow's live set under load"
source: https://github.com/gonka-ai/gonka/issues/1899
issue_number: 1899
synced_at: 2026-10-05T07:11:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: per-diff full-state copies and per-request scans grow with the escrow's live set under load
    <span class="issues-number">#1899</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/cyberdelamain">@cyberdelamain</a> opened 2026-10-02 04:10 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-02 05:27 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Following the v5.0.2 OOM (#1896): with the response cache gone, the next memory and CPU drivers on a busy escrow are copies and scans whose size is the escrow's live set or history rather than the request. All of the below is present on devshard-0.2.x-v6 (0581a7c91), v5.0.2 and the v5.1.0 release head (120604fe9); line numbers are v6. Note that v6 still has the uncapped `completedResponses` cache that #1896 removes (`host/host.go:1159`), so the #1896 fix needs a forward-port too.

**1. Full state copies on every diff, under the escrow lock**
`ValidateDiff` takes `snapshotMutable()` three times per diff (`state/machine.go:326`, `:338`, and inside `applyCore` at `:717`); `PreviewLocalBestEffort` (gateway compose) three times as well (`:396`, inside `localBestEffortLocked` at `:490`, `:409`). Each copy contains all live inferences, `committedEntries` and every `sealedNonces` entry the escrow has ever had (never pruned). The root is then recomputed over all live records. A finished inference stays live until `InferenceSealGraceSeconds + ExecutionTimeout` (3600 + 1920 s on mainnet, ~92 min), so the live set grows with request rate.
Throwaway benchmark of one gateway compose (M1, 16 slots, measured on 120604fe9; v6 within 4%):

| live inferences | time | allocated |
|---|---|---|
| 1 000 | 1.32 ms | 2.72 MB |
| 10 000 | 13.1 ms | 27.7 MB |
| 19 800 | 27.9 ms | 54.8 MB |

On the host side, summing the measured parts (three snapshots, two root computations, plus the per-request `SnapshotState`) at 20k live / 200k sealed gives roughly 58 ms of CPU and 100 MB of garbage per request. At ~20k live this caps one escrow at roughly 15–20 nonces/s per host (~35/s on the gateway side), and every host in the group pays it for every diff. An undo journal instead of full copies, sharing `committedEntries`, and an incremental live hash would remove most of it.

**2. Validation job collection is O(live × mempool)**
`collectValidationJobs` (`host/host.go:1192`) calls `hasMempoolValidationOrVote` (`:1358`) for each Finished/Challenged candidate, and that copies and scans the whole mempool (`h.mempool.Txs()`). An index by inference id built once per call fixes it.

**3. The mempool has no TTL or cap**
Gossiped txs that arrive after their diff was applied are never removed, and the whole mempool rides in every inference response (`host/host.go:628`, SSE `devshard_meta` at `transport/server.go:527`) (cf. `docs/attacks.md:60`).

**4. Auto-seal diagnostic logs every live candidate at Info**
`state/seal.go:420` logs the JSON of all candidates every 150 nonces: ~3.6 MB per line at 20k live. Debug level or a count instead of the list.

Happy to send PRs for 2 and 4 (small).

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-02 05:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Related: #1900 removes one more full-state copy of the same kind, outside the list above: on the gateway side, the pooled <code>GET /v1/status</code> in devshardctl (two or more escrow runtimes) called <code>SnapshotState()</code> for every runtime on every request just to read two scalars (unauthenticated endpoint; per runtime at 20k live: 2.93 ms / 5.55 MB → 90 ns / 0 B).</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1899](https://github.com/gonka-ai/gonka/issues/1899) every hour.
