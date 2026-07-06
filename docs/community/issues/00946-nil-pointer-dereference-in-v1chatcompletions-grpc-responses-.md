---
title: "#946 — Nil pointer dereference in /v1/chat/completions — gRPC responses not nil-checked"
source: https://github.com/gonka-ai/gonka/issues/946
issue_number: 946
synced_at: 2026-07-06T09:52:31Z
---

> 🔄 **Авто-синхронизация:** из [Issue #946](https://github.com/gonka-ai/gonka/issues/946) каждые 6 часов. 

# 🔴 Nil pointer dereference in /v1/chat/completions — gRPC responses not nil-checked

**Автор:** [@unameisfine](https://github.com/unameisfine) · **Состояние:** Closed · **Создано:** 2026-03-25 15:52 UTC · **Обновлено:** 2026-03-25 16:04 UTC

---

## 📝 Описание

Related to #876.

Three gRPC response accesses in `post_chat_handler.go` lack nil guards, causing runtime panics when chain RPC is slow or partially responsive:

1. **`enforceDeveloperAccessGate`** (line 250): `paramsResp.Params.DeveloperAccessParams` — panics if `paramsResp` is nil. Called for ALL requests (both transfer and executor paths).

2. **`handleTransferRequest`** (line 294): raw gRPC error returned without `echo.NewHTTPError` wrapping — error handler middleware receives an unexpected error type.

3. **`validateRequester`** (line 1000): `priceResponse.Found` — panics if `priceResponse` is nil after `GetModelPerTokenPrice` query.

All three are in the common request path, which explains why all documented transfer-agent endpoints fail simultaneously under the same conditions.

The pattern used elsewhere in the codebase (e.g. `enforceDeveloperAccessGate` already nil-checks `p` on line 251) should be applied consistently to all gRPC responses.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-03-25 16:04 UTC*

Closing in favor of #876 — this is the same issue. Posted analysis there instead.
