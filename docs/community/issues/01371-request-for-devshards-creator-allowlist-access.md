---
title: "#1371 — Request for DevShards creator allowlist access"
source: https://github.com/gonka-ai/gonka/issues/1371
issue_number: 1371
synced_at: 2026-07-06T09:51:40Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1371](https://github.com/gonka-ai/gonka/issues/1371) каждые 6 часов. 

# 🔴 Request for DevShards creator allowlist access

**Автор:** [@GERAunits](https://github.com/GERAunits) · **Состояние:** Closed · **Создано:** 2026-06-28 11:40 UTC · **Обновлено:** 2026-07-03 00:13 UTC

---

## 📝 Описание

Request to add my address to devshard_escrow_params.allowed_creator_addresses for a self-hosted gateway.

Address: gonka1a02jacrjca02f0805v9kpx0h2axjdfxx4vmwls
Pubkey: A3X9+ooArJ8UyJX1WpvhnH7JFBcU6OrbaQtYtUF0lcDX
Registration tx: D398545C1EDB469490EC07D2BF83D9854C3E376F88122EED90FE5B45FAD6D850 (block 4796580)
Balance: above min_amount

Operator: Pavel Gerasimov
GitHub: @GERAunits
Contact: gerasape@gmail.com

Models: Kimi K2.6 for programming and text processing tasks. Also interested in other available models.

Use case: personal self-hosted gateway for AI-assisted programming, code review, documentation, and text work. Low volume, no public endpoint, no resale.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-07-03 00:13 UTC*

Hi @GERAunits! Additions to `devshard_escrow_params.allowed_creator_addresses` happen only through on-chain governance — a param-change proposal or inclusion in a governance-approved upgrade batch. No maintainer adds an address unilaterally, so filing this issue registers your intent, but inclusion and timing are governance-dependent and not guaranteed.

Given your use case — personal, low-volume, no public endpoint, no resale — it's worth asking what running your own gateway actually buys you here. It gives you two things: paying for inference with your own GNK directly, with no third party holding a balance for you, and no operator between you and the network (relevant if you don't want anyone else seeing your code and documents in transit). In exchange you take on escrow funding, rotation, and settlement, plus the governance wait before any of it works.

If what you need is simply an OpenAI-compatible endpoint for AI-assisted coding and text work, that exists today. Community brokers are listed in the developer quickstart, and OpenBroker (https://openbroker.gonka.gg, discussion #1363) is a GNK-native option with no markup — it deducts your balance 1-to-1 with actual escrow cost, no enrollment or approval wait, and Kimi K2.6 is served there alongside the other network models. The honest trade-off is that it's custodial: you deposit GNK to an address the operator controls, and access runs under their API key. If self-custody or keeping your request content away from any intermediary is the reason you want your own gateway, that doesn't replace this request — say so and it stands as-is for governance consideration. If not, a managed endpoint will get you working today, and the operator path stays open if you want it later. 
