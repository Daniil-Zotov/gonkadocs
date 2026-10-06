---
title: "#1881 — The Gateway That Never Forgets"
source: https://github.com/gonka-ai/gonka/issues/1881
issue_number: 1881
synced_at: 2026-10-06T21:42:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    The Gateway That Never Forgets
    <span class="issues-number">#1881</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/paranjko">@paranjko</a> opened 2026-09-29 23:35 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-06 05:16 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

A devshard gateway writes one SQLite session file per escrow, `$DEVSHARD_STORAGE_DIR/escrow-<id>/epoch_<N>.db` (template path `/root/.devshardctl`),

These files are never deleted. Each epoch adds several gigabytes.
 `DEVSHARD_STATS_RETENTION_EPOCHS` only prunes rows in `accounting.db`.

## Motivation

A full disk stops the gateway from opening new session files.
On a production gateway the session files from epoch 403 through the epoch 409 occupied **37.8 GB**.  

| Epoch | Directories | `epoch_N.db` |
|---:|---:|---:|
| 403 | 393 | 4.4 GB |
| 404 | 427 | 7.3 GB |
| 405 | 340 | 6.3 GB |
| 406 | 298 | 6.4 GB |
| 407 | 387 | 6.6 GB |
| 408 | 273 | 5.2 GB |
| 409 | 131 | 1.6 GB, epoch still running |
| **Total** | | **37.8 GB** |

A completed epoch typically leaves behind around 5–7 GB.
Given enough epochs, the ending is predictable: the disk fills up. 

## Impact

- Who is affected: gateway operators.
- Effect: each gateway's local disk.
- Likelihood: common over time.
- Severity: high.
- Affected components: `devshardctl` gateway storage (`devshard/cmd/devshardctl/gateway.go`, `devshard/storage`).

## Expected behavior

On epoch change, the gateway removes session directories older than the host horizon (current + two previous), with the same skip for anything still live.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/danielhubersstorm">@danielhubersstorm</a></span>
    <span class="issues-meta-item">commented 2026-10-05 02:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi, I’d like to work on this issue. Is it still available, and does the work in #1905 overlap with the session-file cleanup?</p>
<p>My proposed approach is to clean up expired session storage on epoch changes, retaining the current epoch and two previous epochs while protecting live sessions and any state still needed for settlement or recovery. I would include regression tests for retention boundaries, active-session protection, and repeated cleanup.</p>
<p>Could you confirm the preferred target branch and any additional acceptance criteria?</p>
<p>Also, is this task eligible for a contributor reward? If so, I’d appreciate clarification on the proposed amount, payment currency, and approval process before starting substantial implementation.</p>
<p>Thanks!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-10-06 05:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @danielhubersstorm, it seems like @qdanik has already fixed this issue in #1905. But if you are open to contributing to Gonka, please read https://gonka.ai/docs/bounty-program/, and I hope you will find something interesting. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1881](https://github.com/gonka-ai/gonka/issues/1881) every hour.
