---
title: "#2307 — Proposal from Ancapex: Alternative Tokenomics"
source: https://github.com/gonka-ai/gonka/discussions/2307
discussion_number: 2307
category: protocol-improvements
synced_at: 2026-11-26T23:44:44Z
---

> 🔄 **Auto-sync:** from [Discussion #2307](https://github.com/gonka-ai/gonka/discussions/2307) every hour. 

# Proposal from Ancapex: Alternative Tokenomics

**Автор:** [@alancapex](https://github.com/alancapex) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-23 13:03 UTC · **Обновлено:** 2026-11-26 19:55 UTC

---

## 📝 Описание

Bitfury has put forward a tokenomics proposal so that hosts' main income comes from inference. We support it as the starting mechanism, and in parallel we want to develop an alternative that is a better fit for a DePIN/DeVIN network.

The main idea: GNK is the currency used to pay for work in the network, not a share in a company. So emission should depend on how much work the network actually does, and not only on the calendar.

Part of every payment is burned, emission is tied to the work done, and pricing covers training as well as inference.

**Full draft:** https://github.com/alancapex/gonka/blob/proposal/depin-tokenomics-mechanism/proposals/depin-tokenomics-mechanism/README.md

Questions and feedback are welcome.


---

## 💬 Комментарии (2)

### Комментарий 1 — [@alancapex](https://github.com/alancapex)

*2026-11-26 17:43 UTC*

This proposal is now on-chain as **#122**. Voting is open until 28 November, 17:39 UTC.

### Комментарий 2 — [@akamitch](https://github.com/akamitch)

*2026-11-26 19:55 UTC*

I agree that something in the tokenomics should change.
However, I wasn't impressed by your vision on this, so I'm against this proposal.

Burning during the primary emission stage, which is now and the next several years, will have absolutely no effect on anything.

Pricing inference in USD with a "market price" oracle is a terrible idea strategically. The market should discover the price of inference right here, in GNK, as a balance between those who want to buy inference here and the network's capacity to deliver it.
We should simply make the inference price in GNK adjust dynamically depending on network load, as was originally planned (and is still in the plans).

Tests of protection against fake work: PoC is already being reworked for the third time, and it isn't really part of tokenomics anyway.

Network model and stress tests: this simply won't work. You can't predict the behavior of people deciding whether to mine or not, whether to buy the coin or sell it, whether to buy inference here or not.
Nobody can, and that's normal.

What's really worth changing, if we do want more GPUs in the network, is the number of vesting days.
A VERY simple experiment.
We set the vesting period to 7 days, just by a vote.
We see the number of GPUs grow almost immediately (if I'm right).
