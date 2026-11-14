---
title: "#2219 — [BUG] decentralized-api: admin API cannot disable, enable or delete a node whose id contains "/""
source: https://github.com/gonka-ai/gonka/issues/2219
issue_number: 2219
synced_at: 2026-11-14T03:23:03Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] decentralized-api: admin API cannot disable, enable or delete a node whose id contains "/"
    <span class="issues-number">#2219</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/yaUrich">@yaUrich</a> opened 2026-11-05 10:40 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-06 06:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`POST /admin/v1/nodes` accepts a node id that contains `/`, for example `Qwen/Qwen3-4B-Instruct-2507:host--secondary`. After that, the node cannot be disabled, enabled or deleted through the admin API. Echo does not unescape path parameters, so the handlers look up `Qwen%2FQwen3-…` and do not find the node. `DELETE` still returns 200.

## Motivation

Node ids built from model names contain `/`. Such a node stays in the broker until the API is restarted with a changed configuration.

## Impact

- Who is affected: hosts whose node ids contain `/`.
- Limited to that node.
- Likelihood: edge case; the create endpoint accepts these ids.
- Affected components: `decentralized-api` admin API.

## Detailed description

The routes take `:id` from the raw path ([server.go#L70-L72](https://github.com/gonka-ai/gonka/blob/8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee/decentralized-api/internal/server/admin/server.go#L70-L72)). `deleteNode`, `enableNode` and `disableNode` pass `c.Param("id")` to the broker as is ([node_handlers.go#L25-L43](https://github.com/gonka-ai/gonka/blob/8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee/decentralized-api/internal/server/admin/node_handlers.go#L25-L43), [#L246-L247](https://github.com/gonka-ai/gonka/blob/8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee/decentralized-api/internal/server/admin/node_handlers.go#L246-L247), [#L273-L274](https://github.com/gonka-ai/gonka/blob/8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee/decentralized-api/internal/server/admin/node_handlers.go#L273-L274)). The MLNode callback already unescapes `model_id` ([post_generated_artifacts_v2_handler.go#L19-L28](https://github.com/gonka-ai/gonka/blob/8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee/decentralized-api/internal/server/mlnode/post_generated_artifacts_v2_handler.go#L19-L28)).

Reproduced with a test on `setupTestServer` (real broker, Echo v4.15.1), at `8af3f3f` and `release/v0.2.16-post1`. The id is passed through `url.PathEscape`.

| Step | Id with `/` | Id without `/` |
|---|---|---|
| `POST /admin/v1/nodes` | 200 | 200 |
| `POST …/nodes/<id>/disable` | 404 `node not found: Qwen%2FQwen3-…` | 200, `enabled=false` |
| `POST …/nodes/<id>/enable` | 404, same body | 200, `enabled=true` |
| `DELETE …/nodes/<id>` | 200, body `false` | 200, body `true` |
| `GET /admin/v1/nodes` | node still listed, `enabled=true` | `[]` |

The same 404 body came from a DevNet host on `v0.2.16-post1`.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/RyoKusnadi">@RyoKusnadi</a></span>
    <span class="issues-meta-item">commented 2026-11-05 15:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@GLiberman I opened #2220 for this. Could you please review it when you have a moment? Thank you!</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2219](https://github.com/gonka-ai/gonka/issues/2219) every hour.
