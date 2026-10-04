---
title: "#1886 — Proposal: a consistent integer-overflow policy for Gonka (#1222)"
source: https://github.com/gonka-ai/gonka/discussions/1886
discussion_number: 1886
category: protocol-improvements
synced_at: 2026-10-04T22:18:06Z
---

> 🔄 **Auto-sync:** from [Discussion #1886](https://github.com/gonka-ai/gonka/discussions/1886) every hour. 

# Proposal: a consistent integer-overflow policy for Gonka (#1222)

**Автор:** [@zpoken](https://github.com/zpoken) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-10-01 10:37 UTC · **Обновлено:** 2026-10-01 10:37 UTC

---

## 📝 Описание

We prepared proposal describing a standard way to handle integer overflow, applied consistently across the codebase, with an automated check.

**Full proposal:** https://github.com/zpoken/gonka/blob/zpoken/int-overflow-proposal/int-overflow-proposal.md

## What we propose

1. Rules by execution context.  What happens on overflow depends on where the code runs. 
2.  Implement and use one shared package.
3. Add a CI check. gosec G115 and `nolintlint` run in all four Go modules on new lines only, so the existing backlog does not block anyone. 

## Why

- Overflow fixes keep landing one PR at a time with different semantics. Today's helpers disagree: the keeper's `checkedMul` returns `true` on overflow, while devshard's `safeMul` returns `true` on success.
- Three of the four Go modules have no lint check in CI.
- We found 379 G115 diagnostics, 712 arithmetic candidates and 50 SDK/decimal narrowing calls. These still need site-by-site classification, and there is currently no shared way to record which sites are safe and why.
- Some failures are silent: decimal `IntPart()` wraps, and the v0.2.15 decimal-exponent fix shows how library semantics can reach consensus.

Feedback is welcome, especially on the block-hook rule and the CI scope. 
