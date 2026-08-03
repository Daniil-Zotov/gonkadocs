---
title: "#923 — Consensus key mismatch: staking still expects old key after TMKMS key loss"
source: https://github.com/gonka-ai/gonka/issues/923
issue_number: 923
synced_at: 2026-08-03T17:23:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Consensus key mismatch: staking still expects old key after TMKMS key loss
    <span class="issues-number">#923</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/krizis-sila">@krizis-sila</a> opened 2026-03-20 20:36 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-28 20:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hello,

I need help with a validator consensus key mismatch on Gonka mainnet.

Participant:
gonka1dll7aqkqleqt8s363fx2s3versn3r3c0zt3vj0

Current situation:
- staking still expects old consensus key: YMsTg8SKXFYJf5g5sfRsWHE8MPUeg23ImLkoFl6ZZyc=
- current TMKMS key is different: 3fbo8+SH2OBHRParBPxU7OAic0+lNNPHNa5emBKEbqc=
- validator is jailed / unbonding
- inference is still active
- submit-new-participant updated the inference-side participant record, but staking still keeps the old key

What happened:
- during migration to /ephemeral, the active TMKMS directory was wiped
- shell history shows:
  - sudo rm -rf /ephemeral/gonka-data/tmkms/*
  - sudo find /ephemeral/gonka-data/tmkms/ -mindepth 1 -delete
- after that, TMKMS generated a new consensus key
- I do not have a backup of the old TMKMS validator key

What I already confirmed:
- current active TMKMS path is /ephemeral/gonka-data/tmkms
- current TMKMS secrets:
  - /ephemeral/gonka-data/tmkms/secrets/priv_validator_key.softsign
  - /ephemeral/gonka-data/tmkms/secrets/kms-identity.key
- staking-side key did not realign automatically
- I was advised not to unjail until staking matches the active TMKMS key

Questions:
1. What is the exact recovery path if the old TMKMS consensus key is lost?
2. Is there any manual way to update the staking-side consensus key?
3. Can this be done by me via CLI, or does it require team intervention?
4. Should I keep the validator jailed until the staking-side key is updated?

Related tx:
36826F73D7B2BB31D5D506C4463E53DE632AC072F1B2A50E68A06D3C8BB48205

Thank you.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/0xgonka">@0xgonka</a></span>
    <span class="issues-meta-item">commented 2026-04-28 20:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>this is likely stale by now. We can re-open if there are subsequent reports but looks like it might have been a fluke</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #923](https://github.com/gonka-ai/gonka/issues/923) every hour.
