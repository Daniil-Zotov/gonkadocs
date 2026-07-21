---
title: "11. Team GonkaGate Grant Request"
template: proposals-main.html
---

# 11. Team GonkaGate Grant Request

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🔴 Expired</div>

**Author:** Slava MyGonka
**Created:** 2026-06-11 05:51 UTC
**Closes:** 2026-07-11 05:51 UTC
**Language:** EN
**Votes:** 0
**Avg. Bid:** 0.00 GNK

</div>

Team GonkaGate built a public Gonka API gateway and plans to scale infrastructure, payments, analytics, plugins, docs, and developer adoption tools.

---

## Full Proposal

What does your team plan to build or deliver for Gonka over the next three months?

Over the next three months, Team GonkaGate plans to develop GonkaGate into a stronger reliability and developer adoption layer for the Gonka Network.

The main deliverables include:

* Improve fault-tolerant infrastructure, routing, failure handling, observability, accounting, and load behavior.
* Continue scaling GonkaGate toward thousands and later tens of thousands of requests per second.
* Expand one-command setup tools for AI agents and developer tools.
* Continue work on planned integrations, including:

  * Codex setup:
    https://github.com/GonkaGate/codex-setup
  * OpenHuman setup:
    https://github.com/GonkaGate/openhuman-setup
* Finish the model performance analytics layer on model pages, including metrics such as throughput, latency, end-to-end latency, tool-call error rate, structured-output error rate, and reliability data.
* Add payment and balance top-up flows so developers can continue using Gonka after free trial credits.
* Implement USD top-ups by credit card.
* Add crypto top-ups through NOWPayments with support for multiple currencies.
* Improve billing flows, credit accounting, usage tracking, and spend reporting.
* Continue improving the dashboard as an operations panel for Gonka developers.
* Expand plugins and developer features, including search, file handling, structured output reliability, privacy controls, and practical tools for agents and applications.
* Grow real developer usage through open-source tooling, documentation, examples, integrations, and targeted outreach.

The goal is to make Gonka easier to adopt, easier to trust, and easier to use in production.

## What contributions or products has your team already developed for Gonka (with links pls)?

Team GonkaGate has built **GonkaGate**, a public developer gateway and control panel for the Gonka Network:
https://gonkagate.com

The main contribution is a practical path from “I want to try Gonka” to “my product or agent is already sending requests.” GonkaGate helps developers with API access, account setup, API keys, usage tracking, agent configuration, documentation, examples, and additional features around model calls.

The team treats GonkaGate as infrastructure, not just a demo app. The system is being built around reliability, request routing, observability, accounting, and load handling.

### OpenAI-compatible Gonka API

Team GonkaGate launched a public API gateway for Gonka:

https://gonkagate.com/en/gonka-api
https://gonkagate.com/en/docs/quickstart
https://gonkagate.com/en/docs/api/reference/overview

Developers can use a familiar OpenAI-compatible flow with chat completions, streaming, model discovery, and API-key authentication.

### Developer dashboard

The team built a dashboard where users can manage API keys, see request history, track token usage, inspect model usage, and understand spending in USD.

### Free developer onboarding

Every registered user currently receives **$10 in free credits**, allowing developers to test Gonka models, agents, plugins, and integrations without a payment step.

### Open-source setup tools for agents

The team published open-source installers and guides that make Gonka easier to connect to coding agents and developer tools:

https://github.com/GonkaGate/hermes-agent-setup
https://github.com/GonkaGate/claude-code-setup
https://github.com/GonkaGate/openclaw-setup
https://github.com/GonkaGate/opencode-setup
https://github.com/GonkaGate/kilo-setup
https://github.com/GonkaGate/gonkagate-doctor
https://github.com/GonkaGate/gonkagate-examples
https://github.com/GonkaGate/awesome-gonkagate

Guides:

https://gonkagate.com/en/docs/guides/coding-agents/hermes-agent
https://gonkagate.com/en/docs/guides/coding-agents/claude-code
https://gonkagate.com/en/docs/guides/coding-agents/openclaw
https://gonkagate.com/en/docs/guides/coding-agents/opencode
https://gonkagate.com/en/docs/guides/coding-agents/kilo-code
https://gonkagate.com/en/docs/guides/coding-agents/cursor

### n8n integration

The team built an n8n community package so automation builders can use Gonka inside workflows:

https://github.com/GonkaGate/n8n-nodes-gonkagate
https://gonkagate.com/en/docs/guides/community/n8n

### Plugins and application features

Team GonkaGate added features around Gonka that developers need in real products, including:

* Web Search plugin.
* PDF input and file parsing support.
* Response Healing for malformed structured outputs.
* Privacy Sanitization for safer handling of sensitive data.
* Structured Outputs.
* Tool Calling.
* Presets for reusable model and request settings.

Docs:

https://gonkagate.com/en/docs/guides/features/plugins/overview
https://gonkagate.com/en/docs/guides/features/plugins/pdf-inputs
https://gonkagate.com/en/docs/guides/features/plugins/response-healing
https://gonkagate.com/en/docs/guides/features/plugins/privacy-sanitization
https://gonkagate.com/en/docs/guides/features/structured-outputs
https://gonkagate.com/en/docs/guides/features/tool-calling
https://gonkagate.com/en/docs/guides/features/presets

### Public docs, model pages, pricing, and status

The team also built public developer-facing pages:

https://gonkagate.com/en/models
https://gonkagate.com/en/pricing
https://status.gonkagate.com

## GNK Wallet Address

gonka1lv55k52lvxz074yhr7kcne86srf7dse9pvyfhm

## Your Discord ID for Contact Purposes

279952435668320256

## Email Address

[daniil.koryto@gmail.com](mailto:daniil.koryto@gmail.com)

---

## Comments (1)

### 💬 Slava MyGonka
*2026-06-11 07:59* · 👍 0 · 👎 0

Привет! 
Пользуюсь вашим Гейтом. Очень доволен.
Особенно радует наличие классной документации.
И то, что ее можно "скормить" Агенту.

Вот тут похожее предложение от ваших конкурентов: https://vote.gonka.vip/tenders/f021bdb3-59f4-4906-bfaa-7b90b72019b1

Свое мнение по этому поводу я там высказал.
Кратно: Поддержав один Gonka Брокер мы ставим в проигрышное положение других.
Но есть идея по компенсации затрат.

1. Скажи, сколько инференса уже потрачено через твой Gate и сколько GNK ты за это заплатил?
Вот это точно можно просить вернуть.
Думаю, комьюнити одобрит.

2. Можно ли как-то подтвердить эти траты?

3. Скажи, а ты мог бы помочь с созданием документации для Хостов?
Чтобы так же, как у тебя на сервисе было, через md или как там сделано? Через Контейнер?
Т.е. чтобы можно было просто установить в бота и все. А дальше бот уже поставит.

И хорошо бы, чтобы этот бот был на Gonka.

Спасибо за классный сервис!

---


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/d2f317f0-541a-4d9f-bbac-d2d394906bf2)

</div>
