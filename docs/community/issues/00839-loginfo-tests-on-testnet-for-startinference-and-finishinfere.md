---
title: "#839 — LogInfo tests on testnet for StartInference and FinishInference"
source: https://github.com/gonka-ai/gonka/issues/839
issue_number: 839
synced_at: 2026-07-06T09:52:35Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #839](https://github.com/gonka-ai/gonka/issues/839) every 6 hours. 

# 🔴 LogInfo tests on testnet for StartInference and FinishInference

**Author:** [@maria-mitina](https://github.com/maria-mitina) · **State:** Closed · **Created:** 2026-03-02 15:50 UTC · **Updated:** 2026-03-19 06:35 UTC

**Веха:** v0.2.11

---

## 📝 Описание

To investigate the impact of log_format = "json" vs log_format = "plain" on node performance, a [number of experiments were executed on Testnet](https://docs.google.com/spreadsheets/d/1GkV6tn5tgQ3eL7VgAF4JaBWerqsN-fGHc6KEKNigFog/edit?pli=1&gid=586520582#gid=586520582). This is not compared to [mainnet performance](https://github.com/gonka-ai/gonka/issues/780#issuecomment-3972000833), however in isolation supports the same conclusion.  
We could achieve around 3x improvement under inference to performance of LogInfo, when switching to log_format = "json".



<img width="1237" height="470" alt="Image" src="https://github.com/user-attachments/assets/dc9b7e25-3562-4f70-b058-2c6fe8ed52ac" />

---

## 💬 Comments (3)

### Комментарий 1 — [@maria-mitina](https://github.com/maria-mitina)

*2026-03-02 15:51 UTC*

Should we continue with the log_level=info and log_level=error?

### Комментарий 2 — [@hleb-albau](https://github.com/hleb-albau)

*2026-03-02 16:34 UTC*

x3 for start/finish inference, or x3 for logging?

### Комментарий 3 — [@maria-mitina](https://github.com/maria-mitina)

*2026-03-03 08:44 UTC*

@hleb-albau 3x improvement under inference to performance of LogInfo
