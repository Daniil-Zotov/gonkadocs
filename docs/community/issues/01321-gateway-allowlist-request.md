---
title: "#1321 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1321
issue_number: 1321
synced_at: 2026-07-06T09:51:50Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1321](https://github.com/gonka-ai/gonka/issues/1321) каждые 6 часов. 

# 🔴 Gateway allowlist request

**Автор:** [@bruev](https://github.com/bruev) · **Состояние:** Closed · **Создано:** 2026-06-08 14:26 UTC · **Обновлено:** 2026-06-23 23:03 UTC

---

## 📝 Описание

name: Andrei
company: Lunaro
project: Lunaro Gonka Gateway
github: @bruev
Gonka address: gonka1yfr6fcatj5hvx25ucy7uswwsdzdw7aql4uhug3
Models: Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
Purpose: Self-hosted devshard gateway on the linux server




---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-23 23:03 UTC*

Hi @bruev!

To set expectations on the self-hosted path you asked for: running your own devshard gateway means becoming an on-chain escrow operator. Your `gonka1…` creator address has to be on the governance-controlled allowlist (`devshard_escrow_params.allowed_creator_addresses`) before it can open escrows, and you take on the operator side yourself — funding, rotating, and settling escrows, handling v1/v2 state roots, etc. That path stays fully open: inclusion is an on-chain governance decision (no single operator adds an address), so the way to pursue it is to request consideration via governance.  

If you'd rather not wait on a governance vote, there are independent, managed gateways in the community that already operate under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start now without your own allowlisting or enrollment. One such community option is **OpenBroker** (run by Gonka Labs) https://github.com/gonka-ai/gonka/discussions/1363

OpenBroker is **independent third party**, not part of the core protocol. 
