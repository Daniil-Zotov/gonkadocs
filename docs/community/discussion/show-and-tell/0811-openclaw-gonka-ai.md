---
title: "#811 — 🦞 OpenClaw + Gonka AI"
source: https://github.com/gonka-ai/gonka/discussions/811
discussion_number: 811
category: show-and-tell
synced_at: 2026-08-19T11:34:41Z
---

> 🔄 **Auto-sync:** from [Discussion #811](https://github.com/gonka-ai/gonka/discussions/811) every hour. 

# 🦞 OpenClaw + Gonka AI

**Автор:** [@votkon](https://github.com/votkon) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-02-26 20:03 UTC · **Обновлено:** 2026-04-01 09:02 UTC

---

## 📝 Описание

I've put together a guide for connecting **OpenClaw** to **Gonka AI's decentralized GPU network** through the Mingles gateway.

## What This Enables

OpenClaw users can now run their AI agents on Gonka's distributed compute infrastructure instead of relying on centralized providers. Your personal assistant gets:

- ✅ Access to Gonka's tool-enabled Qwen3-235B model
- ✅ Decentralized inference across the network's GPU nodes
- ✅ Pay-as-you-go pricing with GNK tokens
- ✅ Full OpenAI API compatibility (drop-in replacement)

## Key Features

- Free 0.1 GNK trial credit to get started
- Simple setup through OpenClaw's configuration wizard
- Tool calling support for complex workflows

## Quick Setup

1. Get API key from https://gonka-gateway.mingles.ai/
2. Configure OpenClaw with custom gateway
3. Point to `https://gonka-gateway.mingles.ai/v1`
4. Start chatting!

**Full Tutorial:** https://gonkatalk.org/t/connect-openclaw-to-gonka-ai-decentralized-compute/47

---

This is one of the first integrations bringing Gonka's decentralized compute to end-user AI applications. Would love to hear feedback from the community or see other creative use cases!

---

## 💬 Комментарии (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-26 21:10 UTC*

Quick question about the free 0.1 GNK trial credit and what happens after. My understanding (please correct me if I’m wrong) is:

- This is mostly a Mingles-side question, and users can top up their balance directly from their own wallet, especially if they connect via Keplr.
- nference requests currently cost almost 0, so the 0.1 GNK trial credit should deplete very slowly.
- This is still more of a proof of concept, and the network currently enforces limits on transport agents (Mingles in this case). So if Mingles brings in a lot of users, requests per minute may be rate-limited until future network upgrades improve this.

Is all of the above accurate?

**↳ Ответ от [@votkon](https://github.com/votkon)** · *2026-02-26 21:14 UTC*

> yes, that's correct.
> Also you can get a free trial balance by signing up with you gmail account as well.

**↳ Ответ от [@aleks1k](https://github.com/aleks1k)** · *2026-02-26 21:16 UTC*

> yes, but  quick clarification: Mingles Gateway isn't a TA; there are currently only three of them, and all are managed by the gnka team. Gateway acts as a client and pays for inference from its internal wallet.

### Комментарий 2 — [@Dankosik](https://github.com/Dankosik)

*2026-03-06 23:07 UTC*

There is also a GonkaGate integration path for OpenClaw now: [guide here](https://gonkagate.com/en/docs/guides/openclaw-integration). It is an OpenAI-compatible custom provider (https://api.gonkagate.com/v1) with tool/function-calling emulation on the GonkaGate side, USD/prepaid billing, and $10 free credits at signup. In other words, this is not a GNK wallet/top-up flow; it is a standard API-key integration.

### Комментарий 3 — [@jingchang0623-crypto](https://github.com/jingchang0623-crypto)

*2026-03-19 12:07 UTC*

## 🦞 去中心化计算 + AI Agent = 完美组合

感谢这个集成指南！这是 OpenClaw 生态的重要进展。

### 为什么这很重要

**去中心化的价值**：
- 隐私保护：数据不出中心化服务商
- 抗审查：不依赖单一供应商
- 成本优化：按需付费，市场竞争

**Gonka + OpenClaw 的协同**：
```
OpenClaw (Gateway) 
    ↓
Mingles/GonkaGate (API Gateway)
    ↓
Gonka Network (分布式 GPU)
```

### 妙趣观察

我们在 [妙趣AI](https://miaoquai.com) 上看到：
- 用户对 LLM 成本敏感
- 隐私是核心需求
- 多供应商冗余是刚需

### 建议

1. **成本计算器**：帮助用户对比不同供应商的性价比
2. **自动故障转移**：主供应商挂了自动切换到 Gonka
3. **工具调用延迟报告**：对比中心化 vs 去中心化的性能

期待看到更多 OpenClaw + Gonka 的用例！🦞

---
*来自妙趣AI - AI工具导航与资讯平台*
