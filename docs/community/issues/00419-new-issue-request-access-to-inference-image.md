---
title: "#419 — New Issue → Request Access to Inference Image"
source: https://github.com/gonka-ai/gonka/issues/419
issue_number: 419
synced_at: 2026-07-06T09:53:36Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #419](https://github.com/gonka-ai/gonka/issues/419) every 6 hours. 

# 🔴 New Issue → Request Access to Inference Image

**Author:** [@rumirzayev-max](https://github.com/rumirzayev-max) · **State:** Closed · **Created:** 2025-11-06 12:53 UTC · **Updated:** 2025-11-17 21:52 UTC

---

## 📝 Описание

Hi, I need access to the GHCR image to run inferenced nodes.

My GitHub username: rumirzayev-max

Please add me to the gonka-ai organization and grant "read" access to:
  ghcr.io/gonka-ai/inferenced

Thanks!


---

## 💬 Comments (1)

### Комментарий 1 — [@DimaOrekhovPS](https://github.com/DimaOrekhovPS)

*2025-11-17 21:00 UTC*

The images are public for everyone. One possible cause for failing to pull an image is using stale GH credentials, try using `docker logout ghcr.io` to clear the credentials, then login again with `docker login ghcr.io` and retry
