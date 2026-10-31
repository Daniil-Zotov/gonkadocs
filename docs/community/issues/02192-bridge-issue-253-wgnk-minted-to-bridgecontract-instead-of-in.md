---
title: "#2192 — Bridge issue: 253 WGNK minted to BridgeContract instead of intended wallet"
source: https://github.com/gonka-ai/gonka/issues/2192
issue_number: 2192
synced_at: 2026-10-31T07:04:52Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge issue: 253 WGNK minted to BridgeContract instead of intended wallet
    <span class="issues-number">#2192</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/AkSwiss573">@AkSwiss573</a> opened 2026-10-31 05:07 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-31 05:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">

Problem

I accidentally received 253 WGNK at the BridgeContract address instead of my intended Ethereum wallet address during a GNK-to-WGNK bridge operation.

Transaction details

- Transaction hash: "0xffcf0eec7058b01597ccf0ffb0d513ec1915fca04216d092e2a6779c437458ee"
- Amount: 253 WGNK
- Incorrect recipient (BridgeContract): "0x972a7A92D92796a98801A8818bcF91f1648f2F68"
- Intended recipient (my wallet): "0xd0A76F94f432Ec4Fba3B701127bB0D47EEf00254"

Actual result

The transaction logs show that 253 WGNK were minted directly to the BridgeContract address.

Expected result

The 253 WGNK should have been minted to my intended Ethereum wallet address.

Request

Could the Gonka bridge developers please investigate whether the original transaction can be corrected or the 253 WGNK recovered through an authorized contract-level intervention?

Please escalate this issue to the developers responsible for the bridge smart contract.

I am not requesting a duplicate mint. I am requesting assistance with the original transaction.

Thank you.
</div>

---

> 🔄 **Auto-synced** from [Issue #2192](https://github.com/gonka-ai/gonka/issues/2192) every hour.
