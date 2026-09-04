---
title: "#1677 — [BUG] Gateway/mlnode: agent-sized prefill hangs or fails with no usable error"
source: https://github.com/gonka-ai/gonka/issues/1677
issue_number: 1677
synced_at: 2026-09-04T00:09:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] Gateway/mlnode: agent-sized prefill hangs or fails with no usable error
    <span class="issues-number">#1677</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/paranjko">@paranjko</a> opened 2026-08-29 20:39 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-29 21:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Chat completions whose **total prefill is on the order of ≥ ~8K tokens** (typical agent/RAG system prompts; not a single-message format bug) often **never produce a first token**: client sees a hang with 0 bytes, a write timeout, or a generic upstream failure. Small prompts on the same model/path return HTTP 200 in ~1s. Probaly a **gateway → host/vLLM prefill** problem. 

Split out of https://github.com/gonka-ai/gonka/issues/1628.

## Motivation

The network advertises 200K–400K context. Agent clients in `docs/chat-api/agents.md` routinely send tens of thousands of input tokens. If that class of request hangs or takes the host down, the advertised developer use case does not work. Repeated fails also feed host quarantine.

## What to reproduce

1. Same model, same router: `messages=[{user: "ping"}]`, `max_tokens=5`, `stream=true` → HTTP 200, first token &lt; 2s.
2. Same call with **total input ~8K–40K tokens** (one message or split across many — #1628 showed chunking does not help) → hang &gt; tens of seconds with **0 bytes**, client abort, or opaque 5xx.
3. Confirm it is **prefill volume**, not JSON shape.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/paranjko">@paranjko</a></span>
    <span class="issues-meta-item">commented 2026-08-29 21:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Could not reproduce a 0-byte hang on our <a href="https://inference.dahl.global">gateway</a> (DeepSeek-V4-Flash-0731 and MiniMax-M2.7, unique ~12k / ~63k <code>prompt_tokens</code>). <code>stream=true</code> and <code>stream=false</code>: HTTP 200. Stream: first token ~1–6s. Non-stream: full JSON in ~2–15s (DeepSeek ~63k was 14.5s). <code>max_tokens=5</code> completes as 64. Engine stayed up.</p>
<p>A ~75k-in / 4096-out MiniMax non-stream on another path finished in ~53s (<code>outcome=served</code>) a bit slow, not stuck.</p>
<p>Asked the topic starters on #1628 for the large-prompt <code>curl</code>.</p>
<p>Probably not a network-wide ≥8K 0-byte hang. Closing here.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1677](https://github.com/gonka-ai/gonka/issues/1677) every hour.
