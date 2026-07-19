---
title: "#946 — Nil pointer dereference in /v1/chat/completions — gRPC responses not nil-checked"
source: https://github.com/gonka-ai/gonka/issues/946
issue_number: 946
synced_at: 2026-07-19T19:38:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Nil pointer dereference in /v1/chat/completions — gRPC responses not nil-checked
    <span class="issues-number">#946</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-03-25 15:52 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-25 16:04 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Related to #876.

Three gRPC response accesses in `post_chat_handler.go` lack nil guards, causing runtime panics when chain RPC is slow or partially responsive:

1. **`enforceDeveloperAccessGate`** (line 250): `paramsResp.Params.DeveloperAccessParams` — panics if `paramsResp` is nil. Called for ALL requests (both transfer and executor paths).

2. **`handleTransferRequest`** (line 294): raw gRPC error returned without `echo.NewHTTPError` wrapping — error handler middleware receives an unexpected error type.

3. **`validateRequester`** (line 1000): `priceResponse.Found` — panics if `priceResponse` is nil after `GetModelPerTokenPrice` query.

All three are in the common request path, which explains why all documented transfer-agent endpoints fail simultaneously under the same conditions.

The pattern used elsewhere in the codebase (e.g. `enforceDeveloperAccessGate` already nil-checks `p` on line 251) should be applied consistently to all gRPC responses.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-03-25 16:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing in favor of #876 — this is the same issue. Posted analysis there instead.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #946](https://github.com/gonka-ai/gonka/issues/946) every hour.
