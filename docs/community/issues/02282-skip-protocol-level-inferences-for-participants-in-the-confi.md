---
title: "#2282 — Skip protocol-level inferences for participants in the confirmation PoC phase and revisit the discussion in https://github.com/gonka-ai/gonka/pull/1289"
source: https://github.com/gonka-ai/gonka/issues/2282
issue_number: 2282
synced_at: 2026-11-23T02:54:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Skip protocol-level inferences for participants in the confirmation PoC phase and revisit the discussion in https://github.com/gonka-ai/gonka/pull/1289
    <span class="issues-number">#2282</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-17 19:47 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-17 19:47 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
@0xMayoor 
> empty diffs are the lever

Actually empty diff is very undesirable by protocol and normally shouldn't appear. The another attack with empty diffs is skipping slots and send real work only to some choosen host in devshard.

There are still a lot of work on devshards to make it stable on protocol level. I don't think we need to push it right now, as devshard now is primarily used for gateway stabilisation.
But the intent is that every nonce should carry inference, so I think settlement solutions was done keeping this intent in mind, as anyway this host skipping attack should be prevented by protocol.

So the main thing here is that empty diff is not what target version of protocol expects, but current state is mostly experimental for gateway purposes, and every gateway currently is from white list and is trusted

Of course we can add real inference counting, but this should also be added to settlement message.

From one side of view we will be changing part of protocol to legitimate host-skip attack I've described. But we anyway need legal way to skip inferences for some hosts (for example during cPoC see https://github.com/a-kuprin/gonka/blob/devshard-testenv/devshard/docs/proposals/CPOC_PROTOCOL.md)

So adding real inference count to settlement message is what we should have, and is very easy to add

_Originally posted by @a-kuprin in https://github.com/gonka-ai/gonka/issues/1289#issuecomment-4701168965_
            
</div>

---

> 🔄 **Auto-synced** from [Issue #2282](https://github.com/gonka-ai/gonka/issues/2282) every hour.
