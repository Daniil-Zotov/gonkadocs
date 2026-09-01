---
title: "#1636 — Proposal: Cache-Served Token Pricing"
source: https://github.com/gonka-ai/gonka/discussions/1636
discussion_number: 1636
category: protocol-improvements
synced_at: 2026-09-01T14:46:06Z
---

> 🔄 **Auto-sync:** from [Discussion #1636](https://github.com/gonka-ai/gonka/discussions/1636) every hour. 

# Proposal: Cache-Served Token Pricing

**Автор:** [@theaungmyatmoe](https://github.com/theaungmyatmoe) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-08-24 16:27 UTC · **Обновлено:** 2026-08-24 17:14 UTC

---

## 📝 Описание

# Proposal: Cache-Served Token Pricing

**Author:** Aung Myat Moe — operator of the Fusion gateway (`api.fusioncode.app`), a broker serving `deepseek-ai/DeepSeek-V4-Flash-0731`, `MiniMaxAI/MiniMax-M2.7`, and `moonshotai/Kimi-K2.6` through the Gonka network.

## Summary

The network already performs real per-host KV prefix caching, but GNK is billed flat per token — cached tokens cost the same as fresh ones. This proposal makes **cache-served tokens bill at a reduced rate** (proposed 10% of fresh input), so the network's actual hardware savings flow to brokers and their clients, and the network wins more cache-heavy workloads (agents, long stable system prompts) that currently go to centralized providers with native cache discounts (e.g. DeepSeek's ~90% cached-input price).

## Motivation (measured)

Live measurement on 2026-08-24 against `api.openbroker.gonka.gg` (`deepseek-ai/DeepSeek-V4-Flash-0731`, 52k-token prompt):

| Request | Latency | `prompt_tokens_details` |
|---|---|---|
| Cold prefix | 12–31 s | `null` |
| Changed suffix (same host) | ~5 s | `null` |
| Exact replay (same host) | 23–41 ms | `null` |

The latency collapse proves vLLM is reusing the GPU KV cache per host. Yet GNK billing is flat: **15 nGNK per token for every token**, cached or not (verified from the OpenBroker usage API and ledger). Downstream brokers therefore cannot offer cache-based pricing, so the network is structurally uncompetitive for cache-heavy traffic — the exact traffic DeepSeek's own API discounts ~90%.

## Why hosts still profit

Host cost is dominated by **prefill** — attention over every token. A KV-cache hit means the prefill was already computed: the host spends ~0 compute on cached tokens and only generates the new completion. A discounted cached rate still pays the host *more than idle GPU time* and increases utilization — the discount is a utilization incentive, not a loss.

## Proposed pricing model

```
cost = input_rate × fresh_input_tokens
     + cached_rate × cached_tokens
     + output_rate × completion_tokens
```

- `cached_rate = input_rate × DISCOUNT` (proposed default `DISCOUNT = 0.10`; negotiable per model)
- Exact-response replays deduplicated at the gateway already cost zero upstream and are unaffected
- Only provider-reported `prompt_tokens_details.cached_tokens` counts are credited — never locally estimated values

With today's flat 15 nGNK/token and `DISCOUNT = 0.10`, a request with 50k cached + 2k fresh input + 16 output tokens drops from `780,240` nGNK to `82,740` nGNK — an ~89% reduction, matching the real hardware savings.

## Implementation options

- **Option A — Gateway-level (fast, no chain change):** the gateway already receives `prompt_tokens_details.cached_tokens` once telemetry lands (PR #1633); it applies the discount when computing GNK deduction. Ships in days. Con: policy lives in gateway code, less auditable.
- **Option B — On-chain (structural):** extend the Finish/validation payloads with a `cached_tokens` count; `inference-chain` billing (see `x/inference/epochgroup/unit_of_compute_price.go`) computes the discounted cost. Single source of truth, validated, per-model factors via epoch params. Con: requires chain upgrade + validation changes.
- **Recommended:** Option A now to capture the economics, then Option B as the durable protocol rule.

## Prerequisite

PR #1633 (telemetry): `--enable-prefix-caching` + `--enable-prompt-tokens-details` so vLLM emits `usage.prompt_tokens_details.cached_tokens`. Full proposal doc in PR #1635 (`proposals/cache-served-token-pricing/proposal.md`).

## Open questions

1. **Trust** — cached counts are host-reported (like token counts today, see #1474). Should validation re-check cache claims (reject `cached_tokens` when the validator saw no shared prefix)?
2. **Discount factor** — fixed 0.10 or per-model via epoch params?
3. **Minimum cacheable prefix** — avoid tiny-prefix gaming?
4. **Host payout floor** — per-request minimum so cached-only requests never cost hosts money?
5. **Interplay with tokenomics-v2 dynamic pricing** — per-model utilization-based pricing?

## Impact

- **Who is affected:** brokers and developers using the OpenBroker/Gonka API; hosts (per-token payout); downstream billing systems.
- **Network-wide or limited:** network-wide — applies to every request.
- **Likelihood:** common — cache hits already occur today (verified per-host).
- **Severity:** Medium-High — affects host revenue and broker cost, but is a pure pricing change with no service risk.
- **Affected components:** `x/inference` tokenomics, gateway/broker billing, `common/validation`, mlnode vLLM flags (PR #1633).


---

## 💬 Комментарии (1)

### Комментарий 1 — [@qdanik](https://github.com/qdanik)

*2026-08-24 16:37 UTC*

#1550 still in draft, it should be first step to make it possible 

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-24 17:14 UTC*

> okay good 

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-24 17:14 UTC*

> as argument in telegram they are not planning to do it yet 
