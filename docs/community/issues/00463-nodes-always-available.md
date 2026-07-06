---
title: "#463 — Nodes always available"
source: https://github.com/gonka-ai/gonka/issues/463
issue_number: 463
synced_at: 2026-07-06T09:53:11Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #463](https://github.com/gonka-ai/gonka/issues/463) каждые 6 часов. 

# 🔴 Nodes always available

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-12-03 21:19 UTC · **Обновлено:** 2026-01-21 19:58 UTC

**Веха:** v0.2.6

---

## 📝 Описание

The defunal "INFERENCE" state for MLNode de-facto didn't work. 
it deployed model, but model was not in epoch state
=> validation would not go to this node => recovery is not possible 

take a look at this commit and test it https://github.com/gonka-ai/gonka/commit/21cb61ee61bace322de67265bcb971016e609cb3

goal: if MLNode is availabe and not in poc => it must be used for inference
