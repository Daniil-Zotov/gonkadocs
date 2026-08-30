---
title: "#1668 — Proposal: raise the DeepSeek coefficient to 0.400"
source: https://github.com/gonka-ai/gonka/discussions/1668
discussion_number: 1668
category: protocol-improvements
synced_at: 2026-08-30T17:22:06Z
---

> 🔄 **Auto-sync:** from [Discussion #1668](https://github.com/gonka-ai/gonka/discussions/1668) every hour. 

# Proposal: raise the DeepSeek coefficient to 0.400

**Автор:** [@knyazev741](https://github.com/knyazev741) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-08-28 14:03 UTC · **Обновлено:** 2026-08-29 04:39 UTC

---

## 📝 Описание

Russian version: https://telegra.ph/DeepSeek-WSF-0400-pust-subsidiya-pokupaet-poleznuyu-rabotu-08-28

Gonka hosts currently get most of their income not from inference payments, but from RewardCoin subsidy. The pool is fixed and split by scaled PoC. Utilization bonuses in the code do not run. Dynamic pricing is off. All models are priced the same. Hardware therefore follows the `weight_scale_factor` coefficient, not the user queue.

The queue and the coefficient point in opposite directions.

The right unit is raw PoC **nonces per MLNode**, not `participant.weight`. Weight already includes the coefficient, caps, collateral, penalties and rounding. Figures below are epoch **375** (ranking.gonkadb.com snapshot, 28 August 2026). Nonces are that node’s PoC output. GNK is RewardCoin only: `nonces × k / 421,396 × 270,427`.

---

Useful volume versus hardware in this epoch:

| | Tokens | Share | GPUs | Subsidy |
|---|---:|---:|---:|---:|
| DeepSeek | 15.4B | **62%** | **26** | **3.6%** |
| MiniMax | 7.9B | 32% | **607** | **89%** |
| Kimi | 1.3B | 5% | 52 | 7.5% |

Per unit of subsidy DeepSeek does **45,142** tokens, MiniMax **939**. That is **48×**.

I am not claiming MiniMax sits idle at zero. I am stating what nonces and tokens show: the network already pays about the same per GPU (scaled nonce/GPU is already close: MiniMax 618, DeepSeek 580, Kimi 605), and it does not pay the same for the work people send. That is why DeepSeek returns 429. This is not a broker failure. It is a consequence of where the network pays.

A day earlier, in epoch 374, DeepSeek’s token share was 68.2% on the same 26 GPUs. Same picture.

---

Proposal 94 listed DeepSeek at 0.214 as a hardware bootstrap. The documentation allowed the coefficient to be raised later based on usage. Proposals 97 and 98 correct an inflated nonce/min measurement to 0.246. I support that correction. It does not solve the problem.

Parity is median nonce/GPU among nodes with nonzero PoC, inside one GPU class. That compares live boxes, not a lab stand and not a host’s total weight.

| | B300 | H200 | H100 |
|---|---:|---:|---:|
| MiniMax, nonce/GPU | 8742 | 3264 | 1385 |
| DeepSeek, nonce/GPU | 6347 | 1962 | 873 |
| k to match MiniMax | **0.417** | 0.503 | 0.480 |
| DeepSeek now | −49% | −57% | −55% |
| at 0.246 | −41% | −51% | −49% |
| at **0.400** | **−4%** | −21% | −17% |

No DeepSeek nodes on B200 in this epoch, so there is nothing to compare. Hopper stays on MiniMax.

0.246 is below parity on every class. **0.400 is live B300 parity** (minus 4% on the median). It is not a “+28% premium”. It equalizes the card DeepSeek already runs on.

Same count in RewardCoin on a typical live node, GNK per epoch:

| | MiniMax | DeepSeek now | DeepSeek at 0.400 |
|---|---:|---:|---:|
| 1×B300 | **1696** | 872 | **1629** |
| 4×H100 | **985** | 479 | 896 |

On 1×B300 after 0.400, DeepSeek gets 1629 GNK against MiniMax 1696. A B300 host no longer loses by a factor of two. On 4×H100 MiniMax stays ahead. Emission does not rise. I am not proposing to change MiniMax, Kimi or GLM coefficients: the fixed pool redistributes on its own. MiniMax is the initial model, exempt from the group cap.

Without migration, DeepSeek’s share of the pool only goes from 3.6% to 6.5% (6.2% at 0.379). The point is not a bonus for today’s 26 GPUs. The point is that the next B300 is not left on MiniMax only because of the coefficient.

---

The network already pays for these GPUs. The only question is whether that pay buys work someone requested. While dynamic pricing is off, subsidy is the host’s main income and the only budget for keeping a user.

Gonka’s success is not guaranteed. A token and PoC by themselves do not create users. A completed request does. Someone who came for DeepSeek, got a refusal, and left for an ordinary API is unlikely to come back. Cheap inference at this stage is how you collect people who already know how to use Gonka. Once price starts tracking scarcity, finding them again will cost more than not losing them now.

I am not asking to give DeepSeek 62% of GPUs “because it has 62% of tokens”. Models differ in speed and in context cost. The right target is the 40–60% utilization band already written into the pricing parameters, not a quota.

Risks I consider honest: if DeepSeek demand falls, the subsidy will start feeding idle DeepSeek instead — the coefficient can be moved back to 0.350; eight of fifteen DeepSeek nodes already sit on two hosts, so the 30% voting cap should not be raised; jumping straight to 0.45 will pull Hopper, which is why the first step is B300 parity, 0.400. The failure that already happened was not “no” votes, but turnout: proposal 97 had zero no and zero veto and died on quorum.

Practically: a regular 48-hour `MsgUpdateParams`, full Params object, one field — `weight_scale_factor` of `deepseek-ai/DeepSeek-V4-Flash-0731`. If 98 (0.246) executes, the delta is 0.246 → 0.400. If it misses quorum again — 0.214 → 0.400 immediately, without a third run at 0.246.

Source: [ranking.gonkadb.com, epoch 375](https://ranking.gonkadb.com/coefficients?epoch=375). Pool 270,427 GNK, claim weight 421,396.

I ask to raise the DeepSeek coefficient to **0.400**. Keep paying hosts as they are paid. Pay them for the work people are already waiting for.

Telegram Man
