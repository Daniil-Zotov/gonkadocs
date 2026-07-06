---
title: "#985 — [P0] Bug: unsupported OpenAI type input for the inference requests"
source: https://github.com/gonka-ai/gonka/issues/985
issue_number: 985
synced_at: 2026-07-06T09:52:25Z
---

> 🔄 **Авто-синхронизация:** из [Issue #985](https://github.com/gonka-ai/gonka/issues/985) каждые 6 часов. 

# 🔴 [P0] Bug: unsupported OpenAI type input for the inference requests

**Автор:** [@tamazgadaev](https://github.com/tamazgadaev) · **Состояние:** Closed · **Создано:** 2026-03-31 15:15 UTC · **Обновлено:** 2026-04-03 22:36 UTC

**Веха:** v0.2.12

---

## 📝 Описание

decentralized-api rejects valid Cursor/OpenAI chat requests where messages[].content is an array of text parts instead of a plain string. The request fails during request parsing on TA/executor because Message.Content is typed as string, producing 500 {"error":"json: cannot unmarshal array into Go struct field ... content of type string"} even though the payload is valid modern chat-completions format.

---

## 💬 Комментарии (4)

### Комментарий 1 — [@tamazgadaev](https://github.com/tamazgadaev)

*2026-03-31 15:16 UTC*

Check David's thoughts on this in the branch: https://github.com/gonka-ai/gonka/compare/main...codex/dl/diagnose-multimodal-content-parsing

### Комментарий 2 — [@tamazgadaev](https://github.com/tamazgadaev)

*2026-03-31 15:16 UTC*

@tcharchian FYI
@patimen @DimaOrekhovPS Can you take a look? 

### Комментарий 3 — [@x0152](https://github.com/x0152)

*2026-03-31 16:31 UTC*

Hey! If we're talking about the current /v1/chat/completions endpoint then #614 covers this

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-04-01 03:09 UTC*

@x0152 thanks! @DimaOrekhovPS will be working on merging David's changes first. And then will ask you @x0152  to merge them in David's branch. Hope that works for you
