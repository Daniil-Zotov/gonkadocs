---
title: "#361 — [P0] Threshold + Params for big model. Part 2."
source: https://github.com/gonka-ai/gonka/issues/361
issue_number: 361
synced_at: 2026-07-06T09:53:35Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #361](https://github.com/gonka-ai/gonka/issues/361) every 6 hours. 

# 🔴 [P0] Threshold + Params for big model. Part 2.

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2025-09-16 22:31 UTC · **Updated:** 2025-12-05 22:18 UTC

---

## 📝 Описание

1. Threshold + Params for big model; 
2. Scripts to compute, re-check for existing; 
3. New Models 

- [ ] `gpt-oss-120b`
- [x] `DeepSeek-R1-0528`
- [x] `gemma-3-27b-it`
- [x] `Qwen3-30B-A3B-Instruct-2507`
- [ ] `gpt-oss-20b`
- [x] `Qwen3-235B`

4. Instruction to do it
5. Inference Validation finetuning;
6. Fine-tuning Qwen 235 

---

## 💬 Comments (2)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2025-12-05 22:16 UTC*

GPT-OSS can be implemented after the vLLM update. Right now, it is being handled by community contributors from the bounty program  https://discord.com/channels/1336477374442770503/1425189436748206171/1446142256900997152


### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2025-12-05 22:18 UTC*

The threshold-calculation task is completed for the models listed above (except GTP-OSS). They haven’t deployed it to the chain yet. They will most likely be deployed after the vLLM update  
