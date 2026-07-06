---
title: "#804 — [P0?] Extend dev and TA signature payloads"
source: https://github.com/gonka-ai/gonka/issues/804
issue_number: 804
synced_at: 2026-07-06T09:52:02Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #804](https://github.com/gonka-ai/gonka/issues/804) каждые 6 часов. 

# 🔴 [P0?] Extend dev and TA signature payloads

**Автор:** [@DimaOrekhovPS](https://github.com/DimaOrekhovPS) · **Состояние:** Closed · **Создано:** 2026-02-25 20:49 UTC · **Обновлено:** 2026-05-21 21:05 UTC

---

## 📝 Описание

### Dev signature

Currently signs: `original_prompt_hash + timestamp + ta_address`.

Add `model` to prevent a TA or executor from redirecting the inference to a different model after the developer signed. The cross-message comparison catches model mismatches today, but the first message accepts any model without cryptographic proof of developer intent.

New payload: `original_prompt_hash + timestamp + ta_address + model`.

### TA signature

Currently signs: `prompt_hash + timestamp + ta_address + executor_address`.

Add `inferenceId` and `original_prompt_hash` to bind the TA signature to a specific inference request. Without these, an executor could replay a valid TA signature from one inference onto a different inference that shares the same `prompt_hash`, `timestamp`, and addresses.

New payload: `prompt_hash + timestamp + ta_address + executor_address + inferenceId + original_prompt_hash`.

### Changes required

- Update `getDevSignatureComponents` / `getFinishDevSignatureComponents`
- Update `getTASignatureComponents` / `getFinishTASignatureComponents`
- Update corresponding comparison functions
- Coordinate with off-chain signing code (TA and dev) to match new payload formats


---

## 💬 Комментарии (2)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-03-21 00:13 UTC*

Per discussion with @DimaOrekhovPS, this issue may become irrelevant after v0.2.12 and depends on whether we fully switch to the new inference system in the next upgrade or not, wdyt @0xgonka @gmorgachev?

### Комментарий 2 — [@0xgonka](https://github.com/0xgonka)

*2026-03-21 07:45 UTC*

security-wise it is important someone can't just use a dev signature from another inference. I am not sure what PR in 0.2.12 makes this irrelevant but would be happy to take a look if someone can point me in that direction
