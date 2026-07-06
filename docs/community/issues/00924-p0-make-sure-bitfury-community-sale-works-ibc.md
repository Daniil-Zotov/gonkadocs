---
title: "#924 — [P0] Make sure Bitfury community sale works: IBC"
source: https://github.com/gonka-ai/gonka/issues/924
issue_number: 924
synced_at: 2026-07-06T09:52:18Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #924](https://github.com/gonka-ai/gonka/issues/924) every 6 hours. 

# 🔴 [P0] Make sure Bitfury community sale works: IBC

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-03-20 23:20 UTC · **Updated:** 2026-04-11 04:34 UTC

**Labels:** `Priority: High`

**Веха:** v0.2.12

---

## 📝 Описание

*(empty)*

---

## 💬 Comments (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-03-20 23:21 UTC*

@maria-mitina said that Community Sale contract tested with IBC, worked well.
@GLiberman @0xgonka do we have other scenarios to try?

### Комментарий 2 — [@maria-mitina](https://github.com/maria-mitina)

*2026-03-25 09:11 UTC*

it will be great to confirm/decide whether bridge is needed for the Bitfury scenario.
If yes, we will work this scenario out and test.



### Комментарий 3 — [@maria-mitina](https://github.com/maria-mitina)

*2026-03-25 17:15 UTC*

@mtvnastya and I had a discussion about it, and bridge is needed for the Bitfury contract. We need to fix the hardcoded chainId and rebuild the binary. Happy to test after that 
@GLiberman - any chance you could update us on the bridge fix? 

FYI, @tcharchian 
