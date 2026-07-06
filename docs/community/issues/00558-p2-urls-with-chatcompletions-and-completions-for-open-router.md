---
title: "#558 — [P2] URLs with `/chat/completions` and `/completions` for Open Router"
source: https://github.com/gonka-ai/gonka/issues/558
issue_number: 558
synced_at: 2026-07-06T09:52:23Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #558](https://github.com/gonka-ai/gonka/issues/558) каждые 6 часов. 

# 🔴 [P2] URLs with `/chat/completions` and `/completions` for Open Router

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-01-14 20:40 UTC · **Обновлено:** 2026-04-08 16:51 UTC

**Веха:** v0.2.12

---

## 📝 Описание

Provide a minimal but verifiable example that demonstrates Gonka’s inference capability via standard OpenAI-compatible endpoints, suitable for validation and review by openrouter.ai. We need to run a simple inference and provide publicly accessible URLs for the following endpoints:
- `/completions`
- `/chat/completions`

These endpoints are required for listing Gonka as an inference vendor on openrouter.ai.

Requirements
- The inference should be very simple (e.g. a basic prompt like asking about the weather).
- The URLs must return real inference results, not mock data.

Inference logs for the provided URLs must:
- Be readable
- Remain accessible for a reasonably long period of time
- Just a minimal, clear demonstration of how to query the API

**Must be openAI-compliant and return usage for both stream and non-stream**

+ include pricing models endpoint

Before implementation, please review OpenRouter documentation and any relevant provider integration requirements.
This will help ensure full compatibility and avoid iteration during validation.

---

## 💬 Комментарии (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-23 01:14 UTC*

@x0152 feel free to ask @kotelnikova any questions here as well 

### Комментарий 2 — [@libermans](https://github.com/libermans)

*2026-02-18 01:17 UTC*

Should it work with no "request signing" needed? With "api key" requests? Do we have requirements from them? @kotelnikova @tcharchian 

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-02-19 03:20 UTC*

After review https://github.com/gonka-ai/gonka/pull/614, the merge is temporarily paused. A community broker must be identified to serve as an intermediary between OpenRouter and Gonka. Once that structure is defined, the required adjustments on the integration side will become clearer.

In particular, this will determine whether separate endpoints (for example, with /openrouter in the address) are necessary, or whether a different architectural approach would be more appropriate.

Further feedback and next steps will be shared once the broker setup is clarified.

cc: @libermans @kotelnikova @x0152 
