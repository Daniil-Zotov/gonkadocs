---
title: "#343 — BUG-3: Removing models from inference/model_list is not supported"
source: https://github.com/gonka-ai/gonka/issues/343
issue_number: 343
synced_at: 2026-07-06T09:53:05Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #343](https://github.com/gonka-ai/gonka/issues/343) every 6 hours. 

# 🔴 BUG-3: Removing models from inference/model_list is not supported

**Author:** [@gmorgachev](https://github.com/gmorgachev) · **State:** Closed · **Created:** 2025-09-05 07:31 UTC · **Updated:** 2026-01-28 22:26 UTC

---

## 📝 Описание

Fix the bug in network inference API where sending a request with an unsupported model name incorrectly returns the error 402 Insufficient balance.
