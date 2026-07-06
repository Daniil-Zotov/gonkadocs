---
title: "10. Team Alexander Kuprin Grant Request"
template: proposals-main.html
---

# 10. Team Alexander Kuprin Grant Request

<div class="preproposal-header">

<div class="preproposal-status">🟢 Active</div>

**Author:** Slava MSE!
**Created:** 2026-06-11 05:50 UTC
**Closes:** 2026-09-09 05:50 UTC
**Language:** EN
**Votes:** 0
**Avg. Bid:** 0.00 GNK

</div>

Team Alexander Kuprin plans to build an observability layer to detect, trace, and analyze Gonka network issues faster.

---

## Full Proposal

What does your team plan to build or deliver for Gonka over the next three months?

The planned work is related to **Track 0: Core stability and reliability** of the Gonka Community Roadmap:
https://github.com/gonka-ai/gonka/blob/main/proposals/gonka-network-development-roadmap.md

The team plans to build an **observability technical layer** for the Gonka network.

The current problem is that the network experiences issues that are difficult to test, detect, and analyze. At the moment, when a problem is reported, logs often need to be collected manually by contacting hosts individually. Even when some hosts provide logs, this may still not give a complete picture of the issue and its context.

The proposed observability layer should help collect network-wide data, identify problems faster, and support quicker decisions on improvements.

The planned functionality includes:

* Detecting and logging inferences that fail, are missed, or are wrongly invalidated.
* Tracing requests using the **OTEL** protocol.
* Measuring execution context, including API node load, ML node load, and network-layer data for detecting possible attacks.
* Authenticating collected data with Gonka key signatures, so data is accepted only from active epoch participants. This should help prevent spam or flooding and make it easier to localize problems.

The hardware for storing gathered data is outside the scope of the current work. The data could be stored on multiple community servers that can be added to the list. The code will be open, tested, and provided so such servers can be deployed by the community.

The current work is planned to be done in collaboration with other contributors, and the grant reward will be shared.

## What contributions or products has your team already developed for Gonka (with links pls)?

Alexander Kuprin has personally contributed to Gonka through bug bounty work, protocol improvements, release management, and governance-related proposals.

Bug bounty and protocol-related work for address:
gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56

Relevant upgrade files:

https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_8/upgrades.go

https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_10/upgrades.go

https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_11/upgrades.go

https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_12/upgrades.go

Release-related contribution:

https://github.com/gonka-ai/gonka/pull/1289

## GNK Wallet Address

gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56

## Your Discord ID for Contact Purposes

alexanderkuprin_

## Email Address

[kuprin.alexander@gmail.com](mailto:kuprin.alexander@gmail.com)

---

## Comments (1)

### 💬 Slava MSE!
*2026-06-11 07:52* · 👍 0 · 👎 0

Привет!
Это предложение выходит за рамки моего понимания.

Но вопросы я все-таки задам ))
1. Какие серверы нужны и сколько они стоят?
2. Кого ты планируешь привлечь в Контрибьюторы? Они об этом знают?
3. Сколько средств нужно на реализацию этого проекта? Т.е. сколько ты запрашиваешь?
4. Будут ли хосты делиться информацией? Как их мотивировать это делать?


Здорово, что есть такая инициатива!
Чем больше инфы о работе сети, тем лучше!

---


---

<div class="preproposal-link">

[View on gonka.vote](https://gonka.vote/proposal/59175b49-b83f-4aa6-98f5-b27fffb23cd8)

</div>
