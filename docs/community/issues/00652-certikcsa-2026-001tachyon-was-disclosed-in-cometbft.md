---
title: "#652 — Certik(CSA-2026-001:Tachyon, was disclosed in CometBFT)"
source: https://github.com/gonka-ai/gonka/issues/652
issue_number: 652
synced_at: 2026-07-06T09:52:41Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #652](https://github.com/gonka-ai/gonka/issues/652) every 6 hours. 

# 🔴 Certik(CSA-2026-001:Tachyon, was disclosed in CometBFT)

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-01-27 19:04 UTC · **Updated:** 2026-03-12 18:29 UTC

**Веха:** v0.2.11

---

## 📝 Описание

A critical vulnerability — CSA-2026-001: Tachyon — was disclosed in CometBFT (Advisory: https://github.com/cometbft/cometbft/security/advisories/GHSA-c32p-wcqj-j677).

According to the disclosure, all versions of CometBFT are affected. The issue has been addressed in CometBFT versions v0.38.21 and v0.37.18.

As Gonka is a Cosmos-based project that uses CometBFT, Certik kindly recommends upgrading to a patched version as soon as possible to mitigate potential risks.

---

## 💬 Comments (1)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:14 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/675

Updates CometBFT to v0.38.21 to fix the Tachyon vulnerability (CSA-2026-001).
