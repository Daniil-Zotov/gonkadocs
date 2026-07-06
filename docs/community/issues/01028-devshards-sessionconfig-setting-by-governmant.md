---
title: "#1028 — `devshards` `SessionConfig` setting by governmant"
source: https://github.com/gonka-ai/gonka/issues/1028
issue_number: 1028
synced_at: 2026-07-06T09:51:45Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #1028](https://github.com/gonka-ai/gonka/issues/1028) every 6 hours. 

# 🔴 `devshards` `SessionConfig` setting by governmant

**Author:** [@akup](https://github.com/akup) · **State:** Closed · **Created:** 2026-04-07 18:44 UTC · **Updated:** 2026-06-26 22:40 UTC

**Labels:** `Priority: Low`

**Веха:** v0.2.13-devshard2

---

## 📝 Описание

Currently devshard `SessionConfig` has a lot of hardcoded values. They should be settable on new escrow start from mainnet, and should be configurable by governance.

For example https://github.com/gonka-ai/gonka/pull/1005 introduces `MaxInferencesPerSubnet` that is also used for checking at `‎inference-chain/x/inference/keeper/subnet_settlement.go` that is breaking single source of truth rule

---

## 💬 Comments (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-04-20 16:35 UTC*

Starting work on this. PR to follow — threading RefusalTimeout, ExecutionTimeout, and ValidationRate through SubnetEscrowParams -> SubnetEscrow -> subnet SessionConfig, same pattern as TokenPrice. ETA: done.
