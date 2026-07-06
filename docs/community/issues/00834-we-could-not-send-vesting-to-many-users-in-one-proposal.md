---
title: "#834 — We could not send vesting to many users in one proposal"
source: https://github.com/gonka-ai/gonka/issues/834
issue_number: 834
synced_at: 2026-07-06T09:52:39Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #834](https://github.com/gonka-ai/gonka/issues/834) каждые 6 часов. 

# 🔴 We could not send vesting to many users in one proposal

**Автор:** [@huxuxuya](https://github.com/huxuxuya) · **Состояние:** Closed · **Создано:** 2026-03-01 22:24 UTC · **Обновлено:** 2026-03-12 20:29 UTC

**Веха:** v0.2.11

---

## 📝 Описание

  **Problem**
  We had only single-recipient vesting transfer.
  So if we needed to vest tokens to many addresses, we had to add many separate messages
  into one governance proposal.

  **Main limitation**
  Governance proposals have practical size/count limits.
  With many recipients, the proposal became too large (too many messages), and
  distribution could not be done in one clean operation.

  **Why we solved it**
  We needed a simple way to send vesting to many addresses at once, in one proposal, to
  avoid splitting into multiple proposals and reduce operational risk.

  **Target result**
  Add one batch vesting message so one proposal can include many recipients and execute
  the distribution in a single run.

Assign this task to me plz.
