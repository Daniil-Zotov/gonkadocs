---
title: "#1247 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1247
issue_number: 1247
synced_at: 2026-07-06T09:51:50Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1247](https://github.com/gonka-ai/gonka/issues/1247) каждые 6 часов. 

# 🔴 Request to be added as a Gonka broker

**Автор:** [@olkwwuah](https://github.com/olkwwuah) · **Состояние:** Closed · **Создано:** 2026-05-26 07:27 UTC · **Обновлено:** 2026-06-23 23:10 UTC

---

## 📝 Описание

Hi Gonka team & community,

I'm requesting inclusion as a Gonka broker and inclusion of our address in the devshard creator allow-list.

Operator: Daniel
Contact: Discord @labdalab, Telegram @That_metalhead
Public URL: https://gonkadalab.com

About us:
We are a team building infrastructure around Gonka. We aim to help expand the ecosystem, attract new users, and provide practical tools and services that make Gonka easier to access and use.

Devshard creator address:
gonka15uuzwv36ln8mlsmu7ccg6rr3ntj9mh7t9x6n8u

Supported models:
Qwen/Qwen3-235B-A22B-Instruct-2507
moonshotai/Kimi-K2.6

Initial rate limits:
60 RPM per API key

Billing:
Crypto / GNK

Thanks,
Daniel

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-23 23:10 UTC*

Hi @olkwwuah!

Two parts to your ask — broker listing and allowlisting your devshard creator address — so a quick note on how each works:

**Allowlisting `gonka15uuzwv36ln8mlsmu7ccg6rr3ntj9mh7t9x6n8u`.** Operating your own devshard gateway means becoming an on-chain escrow operator, which requires your creator address on the governance-controlled allowlist (`devshard_escrow_params.allowed_creator_addresses`). That path is open, but inclusion is an on-chain governance decision — no single operator or org adds an address unilaterally — so it goes through a governance request. On top of the allowlist, you'd own the escrow lifecycle yourself: funding, rotation, v1/v2 state roots, and settlement.

**Broker listing.** The community broker directory is a curated, non-exhaustive set from the early rollout and isn't being actively expanded.

If you'd rather not wait on a governance vote, there are independent, managed gateways in the community that already operate under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start serving inference now without your own allowlisting. One such community option is **OpenBroker** (run by Gonka Labs): https://github.com/gonka-ai/gonka/discussions/1363

OpenBroker is **independent third party**, not part of the core protocol  
