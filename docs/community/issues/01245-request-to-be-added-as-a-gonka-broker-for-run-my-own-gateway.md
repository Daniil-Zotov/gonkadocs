---
title: "#1245 — Request to be added as a Gonka broker (for run my own gateway)"
source: https://github.com/gonka-ai/gonka/issues/1245
issue_number: 1245
synced_at: 2026-07-06T09:51:50Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1245](https://github.com/gonka-ai/gonka/issues/1245) каждые 6 часов. 

# 🔴 Request to be added as a Gonka broker (for run my own gateway)

**Автор:** [@Korolev-Oleg](https://github.com/Korolev-Oleg) · **Состояние:** Closed · **Создано:** 2026-05-25 13:27 UTC · **Обновлено:** 2026-06-23 23:17 UTC

---

## 📝 Описание

**Operator name and contact (email or Discord handle).**
1kor.oleg@gmail.com 
@unixverse_cli

**Public endpoint URL of your gateway.**
no public endpoints because its for run own gateway purpose

**Gonka address you intend to use for devshard creation (gonka1...).**
https://note2.gonka.ai:8000
https://node4.gonka.ai

**Supported models and any rate limits you plan to enforce.**
`Qwen/Qwen3-235B-A22B-Instruct-2507`
`moonshotai/Kimi-K2.6`

**A brief description of your billing model (USD / crypto / credits) and target audience.**
experimental, develop an application 
but in future maybe in $T / credits

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-23 23:17 UTC*

Hi @Korolev-Oleg! Before anything can move on the self-hosted gateway side, the address field in the request needs fixing: **Devshard creator address** needs to be a `gonka1…` account address that you control (the one your gateway will sign escrow transactions from).  

On the path itself: running your own devshard gateway means becoming an on-chain escrow operator, which requires your `gonka1…` creator address on the governance-controlled allowlist (`devshard_escrow_params.allowed_creator_addresses`). That path is open, but inclusion is an on-chain governance decision — no single operator or org adds an address unilaterally — so it goes through a governance request.

If the goal right now is to build and test against Gonka rather than to operate escrows, there are independent, managed gateways in the community that already run under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start immediately without your own allowlisting. One such community option is **OpenBroker** (run by Gonka Labs): https://github.com/gonka-ai/gonka/discussions/1363

OpenBroker is **independent third party**, not part of the core protocol  

Links: https://openbroker.gonka.gg · https://openbroker.gonka.gg/stats · https://gonkalabs.com
