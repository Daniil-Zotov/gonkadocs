---
title: "#1028 — `devshards` `SessionConfig` setting by governmant"
source: https://github.com/gonka-ai/gonka/issues/1028
issue_number: 1028
synced_at: 2026-07-06T09:51:45Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1028](https://github.com/gonka-ai/gonka/issues/1028) каждые 6 часов. 

# 🔴 `devshards` `SessionConfig` setting by governmant

**Автор:** [@akup](https://github.com/akup) · **Состояние:** Closed · **Создано:** 2026-04-07 18:44 UTC · **Обновлено:** 2026-06-26 22:40 UTC

**Метки:** `Priority: Low`

**Веха:** v0.2.13-devshard2

---

## 📝 Описание

Currently devshard `SessionConfig` has a lot of hardcoded values. They should be settable on new escrow start from mainnet, and should be configurable by governance.

For example https://github.com/gonka-ai/gonka/pull/1005 introduces `MaxInferencesPerSubnet` that is also used for checking at `‎inference-chain/x/inference/keeper/subnet_settlement.go` that is breaking single source of truth rule

---

## 💬 Комментарии (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-04-20 16:35 UTC*

Starting work on this. PR to follow — threading RefusalTimeout, ExecutionTimeout, and ValidationRate through SubnetEscrowParams -> SubnetEscrow -> subnet SessionConfig, same pattern as TokenPrice. ETA: done.
