---
title: "#1648 — Running our own devshard gateway — plan, economics, and what hosts want to see for allowlisting"
source: https://github.com/gonka-ai/gonka/discussions/1648
discussion_number: 1648
category: ecosystem
synced_at: 2026-08-25T15:54:06Z
---

> 🔄 **Auto-sync:** from [Discussion #1648](https://github.com/gonka-ai/gonka/discussions/1648) every hour. 

# Running our own devshard gateway — plan, economics, and what hosts want to see for allowlisting

**Автор:** [@theaungmyatmoe](https://github.com/theaungmyatmoe) · **Категория:** :jigsaw: Ecosystem · **Создано:** 2026-08-25 12:18 UTC · **Обновлено:** 2026-08-25 12:18 UTC

---

## 📝 Описание

# Running our own devshard gateway — plan, economics, and the one thing we need from hosts

**Who:** Fusion AI Gateway (`api.fusioncode.app`) — a production broker already serving DeepSeek V4 Flash, MiniMax M2.7, and Kimi K2.6 through the network (currently via OpenBroker).

## Why we want our own gateway

1. **Direct GNK settlement & self-custody** — we have a committed multi-billion-token/day pipeline and need escrow pooling/rotation/settlement under our own control.
2. **The price gap** — the network's on-chain rate is **1 ngonka/token (0.001 GNK/M)**; a broker layer currently marks this up ~15x. Running our own `devshardctl` gateway removes that layer entirely.
3. **Capacity & cache affinity** — broker-side concurrency limits and global load-balancing have surfaced under sustained load; escrow-bound sessions give us better control (and eventually host affinity for prefix reuse).

## What we've done so far

- **Allowlist request filed:** #1637 — dedicated escrow creator address, generated + kept unfunded until membership is confirmed (per the gateway guide).
- **Staged deployment plan:** gateway-only container on an existing VPS, public node endpoints, single escrow → functional checks → concurrency ramp (1→3→10→25→50→100→200) → multi-escrow pooling + rotation → production cutover.
- **Contribution plan:** we'll publish anonymized capacity/TTFT/settlement results back to the community.

## The one thing we need from hosts

Per the process for #1479, allowlist inclusion is an **on-chain governance decision**, and the strongest signal is **support from active hosts**. So we're asking directly:

**What evidence, operational commitments, or safeguards would you want to see from a broker before supporting its creator address in the next allowlist batch?**

- Load-test results against the current network?
- Settlement/refund transparency commitments?
- A cap on concurrent escrows or requests?
- Anything else that de-risks it for hosts?

## Related

- Allowlist request: https://github.com/gonka-ai/gonka/issues/1637
- Cache-served token pricing proposal: https://github.com/gonka-ai/gonka/discussions/1636
- Cache telemetry PR (prerequisite for cache pricing): https://github.com/gonka-ai/gonka/pull/1633

Happy to answer any questions here or in `#dev-chat`.

