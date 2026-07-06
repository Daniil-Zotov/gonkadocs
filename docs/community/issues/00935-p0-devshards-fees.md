---
title: "#935 — [P0] `devshards` fees"
source: https://github.com/gonka-ai/gonka/issues/935
issue_number: 935
synced_at: 2026-07-06T09:52:06Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #935](https://github.com/gonka-ai/gonka/issues/935) every 6 hours. 

# 🔴 [P0] `devshards` fees

**Author:** [@dcastro](https://github.com/dcastro) · **State:** Closed · **Created:** 2026-03-23 11:12 UTC · **Updated:** 2026-04-29 21:44 UTC

**Labels:** `Priority: High` `devshards`

**Веха:** v0.2.12

---

## 📝 Описание

Context: https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233

* Calculate and charge fee for `devshards`
    * Initial impl: create_fee + max_nonce * fee_per_nonce
        * Reasoning: charging per nonce acts as a mechanism to deter from spamming the network with small inference requests
    * Ensure escrow amount covers the fee
    * Ensure the escrow balance never goes below the fee
    * Charge the fee upon settlement



---

## 💬 Comments (1)

### Комментарий 1 — [@KKizilov](https://github.com/KKizilov)

*2026-03-26 15:06 UTC*

> Calculate and charge fee for subnets
 Will be done by March 29th.

All the remaining items will be done by April 5th

