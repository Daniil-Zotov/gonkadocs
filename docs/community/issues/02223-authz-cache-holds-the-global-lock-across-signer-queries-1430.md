---
title: "#2223 — authz cache holds the global lock across signer queries (#1430 fix never landed)"
source: https://github.com/gonka-ai/gonka/issues/2223
issue_number: 2223
synced_at: 2026-11-12T11:29:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    authz cache holds the global lock across signer queries (#1430 fix never landed)
    <span class="issues-number">#2223</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-05 20:48 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 13:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
`AuthzCache.getSigners` takes the process-wide write lock and holds it across `GranteesByMessageType` and `AccountByAddress`. A failed lookup is not cached, so the next request for the same granter takes the lock and queries again. One slow or failing granter stalls every other signer lookup on that dapi, including an honest `POST /v1/poc/proofs`.

Documented and patched in #1430 (item 2). That PR was closed unmerged on 2026-09-26; the commits are on no branch. The same code is still on main and the current release line.

The HackerOne report that shows this via an unsigned proof request and a granter whose grant scan exceeds the default 10M query gas limit was closed Informative: the lock was already public in #1430. Not a hotfix. Nice-to-have for a future upgrade.

Candidate fix already sits on unmerged #1855 (`42fd0f4c9`, `9f397f07e`): query outside the lock, cache failures for a few seconds, do not store a canceled caller, NotFound, or an address that does not parse. The chain-side grant cap in that same PR is a separate change and does not by itself release the lock.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zpoken">@zpoken</a></span>
    <span class="issues-meta-item">commented 2026-11-06 09:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I will pick this up.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zpoken">@zpoken</a></span>
    <span class="issues-meta-item">commented 2026-11-06 13:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ol>
<li>
<h1>2006 already covers VerifyWarmKey's path, and it notes that each outsider Attach costs one chain query per group validator.</h1>
</li>
<li>Re-reviewed #1855. </li>
<li>https://github.com/gonka-ai/gonka/pull/2236</li>
<li>https://github.com/gonka-ai/gonka/pull/2237</li>
</ol>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2223](https://github.com/gonka-ai/gonka/issues/2223) every hour.
