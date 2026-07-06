---
title: "#1398 — Gateway allowlist request: niro"
source: https://github.com/gonka-ai/gonka/issues/1398
issue_number: 1398
synced_at: 2026-07-06T09:51:37Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1398](https://github.com/gonka-ai/gonka/issues/1398) каждые 6 часов. 

# 🟢 Gateway allowlist request: niro

**Автор:** [@niro58](https://github.com/niro58) · **Состояние:** Open · **Создано:** 2026-07-04 20:09 UTC · **Обновлено:** 2026-07-04 20:11 UTC

---

## 📝 Описание

## Operator

Nichita R. — independent developer
Contact: GitHub @niro58

## Address

gonka142rw2k5qwh3rxm774z56uzcgfyqfnnclqewr36

## Models

- MiniMaxAI/MiniMax-M2.7
- moonshotai/Kimi-K2.6

## Use case

We run nine production apps (SaaS, content platform, mobile apps, AI tooling)
that route all text + tool-calling inference through Gonka via a community
broker. We'd like to move to a self-hosted devshard gateway to pay inference
from our own GNK.

Expected volume is tenths thousands of requests/day, around 100-300 mil tokens a day, growing with our user base.
Happy to share availability telemetry and benchmark results with the network.
