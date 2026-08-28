---
title: "#1668 — Proposal: raise the DeepSeek coefficient to 0.400"
source: https://github.com/gonka-ai/gonka/discussions/1668
discussion_number: 1668
category: protocol-improvements
synced_at: 2026-08-28T18:34:43Z
---

> 🔄 **Auto-sync:** from [Discussion #1668](https://github.com/gonka-ai/gonka/discussions/1668) every hour. 

# Proposal: raise the DeepSeek coefficient to 0.400

**Автор:** [@knyazev741](https://github.com/knyazev741) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-08-28 14:03 UTC · **Обновлено:** 2026-08-28 14:03 UTC

---

## 📝 Описание

Russian version: https://telegra.ph/DeepSeek-WSF-0400-pust-subsidiya-pokupaet-poleznuyu-rabotu-08-28

Gonka hosts currently get most of their income not from inference payments, but from RewardCoin subsidy. The pool is fixed and split by scaled PoC. Utilization bonuses in the code do not run. Dynamic pricing is off. All models are priced the same. Hardware therefore follows the `weight_scale_factor` coefficient, not the user queue.

The queue and the coefficient point in opposite directions.

In the public 24-hour DevShard snapshot (21 August 2026), DeepSeek processed 68% of tokens, MiniMax 17%. The average DeepSeek request is about 11 thousand tokens, MiniMax about 3 thousand. That is different work: long jobs versus short ones.

On the live network snapshot at epoch 375 (28 August 2026, `node3.gonka.ai`) the subsidy is allocated the other way:

- MiniMax: 95 of 115 MLNodes, about 89% of RewardCoin
- DeepSeek: 14 of 115 MLNodes, about 4% of RewardCoin
- Kimi: 6 MLNodes, about 7.5% of RewardCoin

DeepSeek holds twelve percent of nodes and four percent of subsidy against two thirds of useful volume. MiniMax is the inverse. I am not claiming MiniMax sits idle at zero: the public stats API is currently disabled, so I will not sign a utilization figure. I am stating what the chain shows: per unit of subsidy and per node, MiniMax does substantially less of the work users actually send.

That is why DeepSeek returns 429. This is not a broker failure. It is a consequence of where the network pays.

---

Proposal 94 listed DeepSeek at 0.214 as a bootstrap for specific hardware. The documentation explicitly allowed the coefficient to be raised later based on usage. Proposals 97 and 98 only correct an inflated nonce/min measurement to 0.246. I support that correction. It does not solve the problem.

On the same hardware, in the same PoC benchmarks, DeepSeek at 0.246 is still worse than MiniMax: about −29% on 2×B200 and −22% on B300. A host counting RewardCoin will not move Blackwell. The sign of the decision does not change.

For the sign to change, the coefficient has to clear MiniMax parity: 0.3136 on B300 and 0.3444 on 2×B200. Above 0.4297 Hopper starts to leave, and the MiniMax reserve on H100/H200 thins out. There is one working window: **0.3444–0.4297**. 0.400 sits inside it.

At 0.400:

- 2×B200: DeepSeek about 16% better than MiniMax
- 1×B300: about 28%
- 2×H200 and 4×H100: MiniMax stays ahead by 7% and 14%

Blackwell gets a reason to run DeepSeek. Hopper stays on MiniMax. Emission does not rise. I am not proposing to change the MiniMax, Kimi, or GLM coefficients: the fixed pool will redistribute on its own. MiniMax is the initial model, exempt from the group cap; it does not need a separate cut.

Indicative GNK per epoch (epoch-375 pool ≈ 270 thousand, network weight ≈ 421 thousand, RewardCoin only):

| Configuration | MiniMax now | DeepSeek at 0.246 | DeepSeek at 0.400 |
|---|---:|---:|---:|
| 4×H100 | 447 | 237 | 386 |
| 2×H200 | 335 | 192 | 312 |
| 2×B200 | 509 | 364 | 591 |
| 1×B300 | 348 | 273 | 444 |

If a host keeps Hopper on MiniMax, nobody is asking them to leave. If Blackwell sits on MiniMax only because that is where the subsidy is, 0.400 makes it rational to move that box onto the model with a queue — under the same payment scheme.

Without migration, DeepSeek’s share of the pool only rises from 3.6% to about 6.5%. The point is not a bonus for today’s fourteen nodes. The point is that adding DeepSeek nodes becomes more profitable than keeping Blackwell on underloaded MiniMax.

---

The network already pays for these GPUs. The only question is whether that pay buys work someone requested. While dynamic pricing is off, subsidy is the host’s main income and, at the same time, the only budget for keeping a user at all.

Gonka’s success is not guaranteed. A token and PoC by themselves do not create users. A completed request does. Someone who came for DeepSeek, got a refusal, and left for an ordinary API is unlikely to come back. Cheap inference at this stage is how you collect people who already know how to use Gonka. Once price starts tracking scarcity, finding them again will cost more than not losing them now.

I am not asking to give DeepSeek 68% of GPUs “because it has 68% of tokens”. Models differ in speed and in context cost. The right target is the 40–60% utilization band already written into the pricing parameters, not a quota.

Risks I consider honest: if DeepSeek demand falls, the subsidy will start feeding idle DeepSeek instead — the coefficient can be moved back to 0.350; eight of fourteen DeepSeek nodes already sit on two hosts, so the 30% voting cap should not be raised; jumping straight to 0.450 will pull H200, which is why the first step is 0.400. The failure that already happened was not “no” votes, but turnout: proposal 97 had zero no and zero veto and died on quorum.

Practically: a regular 48-hour `MsgUpdateParams`, full Params object, one field — `weight_scale_factor` of `deepseek-ai/DeepSeek-V4-Flash-0731`. If 98 (0.246) executes, the delta is 0.246 → 0.400. If it misses quorum again — 0.214 → 0.400 immediately, without a third run at 0.246.

I ask to raise the DeepSeek coefficient to **0.400**. Keep paying hosts as they are paid. Pay them for the work people are already waiting for.

Telegram Man
