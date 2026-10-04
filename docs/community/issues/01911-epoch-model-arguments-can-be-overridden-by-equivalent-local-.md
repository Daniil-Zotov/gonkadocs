---
title: "#1911 — Epoch model arguments can be overridden by equivalent local CLI spellings"
source: https://github.com/gonka-ai/gonka/issues/1911
issue_number: 1911
synced_at: 2026-10-04T00:44:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Epoch model arguments can be overridden by equivalent local CLI spellings
    <span class="issues-number">#1911</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-10-03 11:58 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-03 11:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

`MergeModelArgs` compares raw CLI tokens when it gives epoch model arguments precedence over a host's local arguments. These spellings name the same vLLM option but both survive today:

```text
epoch: ["--max-model-len", "240000"]
local: ["--max-model-len=8192"]
merged: ["--max-model-len", "240000", "--max-model-len=8192"]
```

vLLM uses the later scalar value. The same mismatch exists when the epoch uses `=` and the local setting uses a space, underscores, or an accepted long abbreviation such as `--max-model`. Short aliases take a different path: the broker silently drops them. This affects other model options as well as the context limit. It also becomes relevant to #1763, which bases the inference reservation cap on the epoch snapshot's context limit.

## How do you know this is a real problem?

The raw-string comparison is in `decentralized-api/broker/broker.go`. A broker regression test using the argument list above fails on the head of #1763 because the local option remains in the deployment arguments. This is a source-level reproduction; I have not launched the pinned vLLM image with these arguments.

The issue predates #1763. That PR changes the reservation path but does not change `MergeModelArgs`.

## Expected behavior

When epoch and local arguments refer to the same vLLM option, the epoch value should control the deployment. Unrelated local options should retain their order. MLNode's own parsing of TP/PP and context arguments should agree with the values it passes to vLLM. A deployment whose effective arguments change may need to restart, so the fix should document that impact.

</div>

---

> 🔄 **Auto-synced** from [Issue #1911](https://github.com/gonka-ai/gonka/issues/1911) every hour.
