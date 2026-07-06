---
title: "#744 — [P1] Don’t require developers to register as Participants to run inference"
source: https://github.com/gonka-ai/gonka/issues/744
issue_number: 744
synced_at: 2026-07-06T09:52:29Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #744](https://github.com/gonka-ai/gonka/issues/744) every 6 hours. 

# 🔴 [P1] Don’t require developers to register as Participants to run inference

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-02-13 01:16 UTC · **Updated:** 2026-03-30 23:52 UTC

**Веха:** v0.2.12

---

## 📝 Описание

Currently, the chain requires a Participant record not only to host, but also to send inference requests. There is no real reason for this, since the public key is available in the Account record after the first on-chain transaction signed by that account is executed. That should be sufficient.

- [ ] Remove the requirement to create a Participant record.
- [ ] Fix `/v1/participants/gonka...` to query Participant data, not just the Account (as it does now).
- [ ] Determine how to preserve per-developer statistics in this case.
- [ ] Update the documentation accordingly.

---

## 💬 Comments (4)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-13 01:19 UTC*

@x0152, would you like to work on this issue?

### Комментарий 2 — [@x0152](https://github.com/x0152)

*2026-02-13 06:15 UTC*

I'll take it

### Комментарий 3 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-11 20:03 UTC*

@tcharchian the PR itself is marked for milestone 0.2.11. what is valid?

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-03-11 20:23 UTC*

> [@tcharchian](https://github.com/tcharchian) the PR itself is marked for milestone 0.2.11. what is valid?

Per @patimen, let's move it to v0.2.12. https://github.com/gonka-ai/gonka/pull/750#issuecomment-3938311002
cc: @x0152  
