---
title: "#2016 — devshard: GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE is ignored after the gateway's first start"
source: https://github.com/gonka-ai/gonka/issues/2016
issue_number: 2016
synced_at: 2026-10-23T18:28:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE is ignored after the gateway's first start
    <span class="issues-number">#2016</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/yaUrich">@yaUrich</a> opened 2026-10-15 10:51 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-15 20:36 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">

## Summary

`GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE` takes effect only on the gateway's first start. After that the gateway reads the setting from its DB, so a new value in the env is ignored on restart. The admin API (`POST /v1/admin/settings` with `logprobs_optimization`) works at runtime and is not affected.

## Why

An operator who changes the env and restarts the gateway keeps the old value. A small follow-up could make the env apply on restart too.

## Details

- The env is read into `bootstrapSettings` ([`main.go#L254`](https://github.com/gonka-ai/gonka/blob/d1b9df2413062a3bd3ea009a5745aff8b4d7f90e/devshard/cmd/devshardctl/main.go#L254)).
- `Initialize` writes them only when the settings row is missing ([Postgres](https://github.com/gonka-ai/gonka/blob/d1b9df2413062a3bd3ea009a5745aff8b4d7f90e/devshard/cmd/devshardctl/gateway_store_postgres.go#L329), [SQLite](https://github.com/gonka-ai/gonka/blob/d1b9df2413062a3bd3ea009a5745aff8b4d7f90e/devshard/cmd/devshardctl/gateway_store_sqlite.go#L352)).

Reproduced on testenv at `d1b9df2`:

1. Set `{"logprobs_optimization":{"enabled":false}}` through the admin API, then restart the gateway. Result: `false`.
2. Recreate the gateway with `GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE=true`. Result: still `false`.
3. Start a second gateway on an empty DB with the env set to `false`. Result: `false`, so the env is applied.

Found while testing the v6 logprobs switch: paranjko/external-test-lab#246.

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-10-15 13:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Taking this one: a small change in <code>mustBootstrapGatewayState</code> that re-applies an explicitly set <code>GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE</code> after <code>Initialize</code>, with a test on both store backends. PR follows in a minute.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-10-15 20:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Follow-up: the PR for this (#2024) was closed as working by design. Once the gateway state exists, the stored value has priority over <code>GATEWAY_LOGPROBS_OPTIMIZATION_OVERRIDE</code>, so the env var only seeds the first bootstrap and a changed value on restart is ignored on purpose.</p>
<p>To change the setting on a running gateway, use the admin endpoint documented in <code>docs/proposal/compressed-payloads.md</code> (it persists through <code>store.UpdateSettings</code>):</p>
<pre><code>POST /v1/admin/settings  {&quot;logprobs_optimization&quot;: {&quot;enabled&quot;: false}}
POST /v1/admin/settings  {&quot;logprobs_optimization&quot;: {}}   # clear, defer to the hosts again
</code></pre>
<p>So this is at most a documentation gap (the env var table in that document does not say the variable is bootstrap-only), not a code change.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2016](https://github.com/gonka-ai/gonka/issues/2016) every hour.
