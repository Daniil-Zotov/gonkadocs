---
title: "#2015 — [BUG] cPoC rotation can shrink the final challenge segment below the punishable minimum"
source: https://github.com/gonka-ai/gonka/issues/2015
issue_number: 2015
synced_at: 2026-10-15T23:07:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] cPoC rotation can shrink the final challenge segment below the punishable minimum
    <span class="issues-number">#2015</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:54 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-15 21:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

**How it is supposed to work**

When a challenge is created, the chain checks that enough blocks remain until the safety window:

`safetyHeight − startHeight ≥ min_punishable_segment_blocks`
This guarantees the target has at least min_punishable_segment_blocks blocks (100 on testnet‑4, 300 on mainnet) to generate PoC before the segment is evaluated. The segment runs from startHeight to finish = safetyHeight.

**What actually happens when a confirmation PoC fires**

A confirmation PoC (cPoC) can be triggered at any block of the Inference phase. When it does, the open challenge is handled like this:

1. The current challenge segment is cut short: its finish becomes the cPoC exchange end + 1 (ChallengeFinish), and that shortened segment is evaluated.
2. When the cPoC completes, the challenge is restarted with a new segment (RotateChallengeSegment): startHeight becomes the current height, finish stays at the original safetyHeight.

The check "finish − start ≥ min" is **only performed at creation time**. It is not repeated at rotation. So the new segment can be arbitrarily short — it is simply whatever is left between the cPoC's end and the safety window.


**What I observed (testnet‑4, epoch 52)**
_min_punishable_segment_blocks was 100_. Both segments were below it, so neither was ever evaluated (see #2013), and the challenge defaulted to PASSED: the challenger's locked payment was paid to a target that had produced zero commits.

**Why it matters on mainnet too**

With mainnet params (safety window 500, cPoC cycle 35+0+5+240+120 = 400 blocks, min 300), any cPoC triggered in roughly the last ~200 blocks of the cPoC trigger window leaves a final segment shorter than 300 blocks. With ~4 random cPoC triggers per epoch, that is a few percent of epochs with an open challenge.

Combined with [issue 2013](https://github.com/gonka-ai/gonka/issues/2013) that converts a valid challenge into a free payout. The rotation should either guarantee finish − newStart ≥ min (else abort+refund), or the final decision should evaluate across all segments of the epoch.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-10-15 11:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>There is a chance of this happening on mainnet:
module/confirmation_poc.go:139-147 and the rotation rule (new start = cPoC validation end + 1):</p>
<p>cPoC trigger window ends at nextPoC − 2 − (35+0+5+240+120+500) = nextPoC − 902.
A cPoC triggered at height T starts generating ~20 blocks later and finishes validation at T + 20 + 34 + 5 + 239 ≈ T + 298; the challenge segment restarts at ≈ T + 299.
Safety (= challenge finish) is nextPoC − 500, so the final segment is nextPoC − 500 − (T + 299). It is &lt; 300 whenever T &gt; nextPoC − 1099, i.e. for any cPoC triggered in the last ~197 blocks of the trigger window. Latest possible trigger gives a final segment of ≈ 103 blocks.</p>
<p>Mainnet does 4 cPoCs per epoch at effectively random heights across a ~14 090‑block trigger window, so per epoch ≈ 1 − (1 − 197/14090)^4 ≈ 5–6 % chance that the last cPoC lands in that zone.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/24a4204de78cefbe14d3e1dda2784ab4fbebc65d</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2015](https://github.com/gonka-ai/gonka/issues/2015) every hour.
