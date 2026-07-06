---
title: "#1264 — logprobs, top_logprobs conditional stripping"
source: https://github.com/gonka-ai/gonka/issues/1264
issue_number: 1264
synced_at: 2026-07-06T09:51:41Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1264](https://github.com/gonka-ai/gonka/issues/1264) каждые 6 часов. 

# 🟢 logprobs, top_logprobs conditional stripping

**Автор:** [@a-kuprin](https://github.com/a-kuprin) · **Состояние:** Open · **Создано:** 2026-05-27 17:29 UTC · **Обновлено:** 2026-07-01 06:06 UTC

**Метки:** `enhancement`

**Веха:** v0.2.14-devshard3

---

## 📝 Описание

The gateway forces logprobs upstream for validation, but clients who never asked for logprobs should not see them in the response (OpenAI-compatible default).
Clients who explicitly set `logprobs: true` or `top_logprobs` should get them back.

Now we always strip them even if client asked this fields in request

Recommendation: Adopt conditional stripping for logprobs and top_logprobs on the client-facing proxy path. Keep unconditional stripping for token_ids, prompt_token_ids, and prompt_logprobs.
