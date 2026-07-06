---
title: "#1342 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1342
issue_number: 1342
synced_at: 2026-07-06T09:51:51Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1342](https://github.com/gonka-ai/gonka/issues/1342) каждые 6 часов. 

# 🔴 Gateway allowlist request

**Автор:** [@appgencore](https://github.com/appgencore) · **Состояние:** Closed · **Создано:** 2026-06-13 07:39 UTC · **Обновлено:** 2026-06-23 22:52 UTC

---

## 📝 Описание

Hi Gonka team,

Requesting to join the Gateway allowlist.
We are a bootstrapped startup studio building AI agents and automation tools. We are exploring decentralized AI infrastructure and would like to run inference directly on Gonka via a self-hosted gateway, paying GNK on-chain per request, rather than going through a third-party broker.

Operator: Den
Contact Discord: gendevik
GitHub: appgencore

Gonka creator address:
gonka1cavsfewz9jrgqxeh5u55y37qxevyueglddtl63

Models planned:
moonshotai/Kimi-K2.6
Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
MiniMaxAI/MiniMax-M2.7

Purpose:
Initial usage will be low-volume and private/internal only. Our goal is to understand the protocol, test the developer experience, and evaluate what products could be built on top of Gonka.
We want to validate the full self-hosted flow end to end: devshard escrow creation, OpenAI-compatible API calls, inference reliability, settlement, and direct on-chain GNK payments.

If local validation works well, we may later submit a separate public broker request with a final project name, public endpoint, rate limits, billing model, and rollout plan.

Thanks!

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-23 22:52 UTC*

Hi! At the moment, the public broker list is not being actively expanded through governance. Inclusion in that list should be handled through the governance process and discussed in the community.

As a practical alternative, there is now a community-operated option for teams that want to start operating as brokers without waiting for direct access https://github.com/gonka-ai/gonka/discussions/1363.

OpenBroker provides access to Gonka inference through devshards v1 and v2 under an already whitelisted escrow-operating wallet. It is intended for teams that want to build or test broker-side products without handling escrow enrollment, escrow funding and rotation, v1/v2 state-root differences, or node4 access.

You can register here:
https://openbroker.gonka.gg/register

Endpoint:
https://openbroker.gonka.gg/v1

Stats:
https://openbroker.gonka.gg/stats

This should let you start while the governance discussion around inclusion/white-listing continues separately.
