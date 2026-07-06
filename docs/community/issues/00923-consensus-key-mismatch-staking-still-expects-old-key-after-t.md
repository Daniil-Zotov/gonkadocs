---
title: "#923 — Consensus key mismatch: staking still expects old key after TMKMS key loss"
source: https://github.com/gonka-ai/gonka/issues/923
issue_number: 923
synced_at: 2026-07-06T09:52:09Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #923](https://github.com/gonka-ai/gonka/issues/923) every 6 hours. 

# 🔴 Consensus key mismatch: staking still expects old key after TMKMS key loss

**Author:** [@krizis-sila](https://github.com/krizis-sila) · **State:** Closed · **Created:** 2026-03-20 20:36 UTC · **Updated:** 2026-04-28 20:53 UTC

---

## 📝 Описание

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

---

## 💬 Comments (1)

### Комментарий 1 — [@0xgonka](https://github.com/0xgonka)

*2026-04-28 20:53 UTC*

this is likely stale by now. We can re-open if there are subsequent reports but looks like it might have been a fluke


