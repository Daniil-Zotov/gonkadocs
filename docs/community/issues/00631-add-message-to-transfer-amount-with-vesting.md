---
title: "#631 — Add message to transfer amount with vesting"
source: https://github.com/gonka-ai/gonka/issues/631
issue_number: 631
synced_at: 2026-07-06T09:52:51Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #631](https://github.com/gonka-ai/gonka/issues/631) every 6 hours. 

# 🔴 Add message to transfer amount with vesting

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-01-23 23:58 UTC · **Updated:** 2026-02-10 22:49 UTC

**Веха:** v0.2.10

---

## 📝 Описание

When the community distributes funds to miners, the transferred tokens should vest over a fixed 180-epoch period, rather than being fully available at the time of transfer.


---

## 💬 Comments (4)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-01-24 21:29 UTC*

Implemented in PR #641 - adds MsgTransferWithVesting message with 180 epoch default vesting, validation, CLI support, and unit tests.

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-01-29 23:47 UTC*

Hi @AlexeySamosadov can I kindly ask you to contact me on Discord? `tatianacharchian_07833`

### Комментарий 3 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-01-31 15:18 UTC*

<img width="554" height="402" alt="Image" src="https://github.com/user-attachments/assets/51108f38-eff7-45b9-8114-d9e71c754913" /> Hi @tcharchian i texted you in Discord :)

### Комментарий 4 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:14 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/641

Adds MsgTransferWithVesting for vesting transfers.
