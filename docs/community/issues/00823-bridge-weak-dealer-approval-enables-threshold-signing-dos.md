---
title: "#823 — Bridge: Weak Dealer Approval Enables Threshold Signing DoS"
source: https://github.com/gonka-ai/gonka/issues/823
issue_number: 823
synced_at: 2026-07-06T09:52:26Z
---

> 🔄 **Авто-синхронизация:** из [Issue #823](https://github.com/gonka-ai/gonka/issues/823) каждые 6 часов. 

# 🔴 Bridge: Weak Dealer Approval Enables Threshold Signing DoS

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-02-27 22:24 UTC · **Обновлено:** 2026-04-02 23:28 UTC

**Метки:** `Priority: High`

**Веха:** v0.2.12

---

## 📝 Описание

**Locations:** 
- https://github.com/gonka-ai/gonka/blob/82c43a42c3c2f49b56ee8a32e6458480daf39ca9/inference-chain/x/bls/keeper/phase_transitions.go#L169-L169
- https://github.com/gonka-ai/gonka/blob/82c43a42c3c2f49b56ee8a32e6458480daf39ca9/inference-chain/x/bls/keeper/threshold_signing.go#L296-L302

**Categories:** 
- Logical-issue
- Denial-of-service

**Description**
Dealer validation uses an unweighted majority of submitted DealerValidity votes and does not verify per-recipient shares against commitments. A malicious dealer can send valid shares to ~50% of recipients and garbage to the rest.

The dealer (or a colluder) can vote “true,” giving itself a bare majority among submitters (>50%). The dealer is marked "valid" and included in the group key even though many recipients lack usable shares.

`inference-chain/x/bls/keeper/phase_transitions.go`
<img width="623" height="641" alt="Image" src="https://github.com/user-attachments/assets/8a28c807-c91a-4e05-93fe-8df8ade73b12" />

<img width="625" height="586" alt="Image" src="https://github.com/user-attachments/assets/47c5ec37-08e3-4941-a4b9-582b0ea3e2cc" />

Later, the dealer (or colluder) withholds its partial signature, pushing the usable signers below the >50% slot threshold. Threshold-signing requests then stall and expire—a sustained liveness/DoS risk, even with <50% malicious participants plus abstentions.

`inference-chain/x/bls/keeper/threshold_signing.go`

<img width="623" height="315" alt="Image" src="https://github.com/user-attachments/assets/f1e6e0eb-99c4-48fd-9e73-9b467b686d1c" />

---

## 💬 Комментарии (4)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-02-28 13:19 UTC*

I'd like to help with this 
#825 (WIP)

### Комментарий 2 — [@libermans](https://github.com/libermans)

*2026-03-02 05:10 UTC*

@x0152 Can you please explain, how does proof work in your implementation?

### Комментарий 3 — [@x0152](https://github.com/x0152)

*2026-03-02 11:52 UTC*

It's not finished yet but what I already made:
1. Proof for true votes - when a participant votes true for a dealer, they must sign a message using shares they got from that dealer. The chain checks this signature against the dealer's public commitments. If signature is invalid or missing, the vote is rejected. So you can't vote true without actually having valid shares
2. Slot-weighted quorum - dealer approval is now counted by slots, not by number of participants. The dealer also can't approve itself

Also added a description to the PR

### Комментарий 4 — [@akup](https://github.com/akup)

*2026-03-02 16:19 UTC*

> 1. Proof for true votes - when a participant votes true for a dealer, they must sign a message using shares they got from that dealer. The chain checks this signature against the dealer's public commitments. If signature is invalid or missing, the vote is rejected. So you can't vote true without actually having valid shares

But the real problem in the issue is, that participant should prove that they have invalid share.A malicious dealer can send valid shares to ~50% of recipients and garbage to the rest. Malicious dealer doesn't need that participants with invalid shares vote true for him, it isn't key for the attack.

And participants can open invalid shares to chain (as they are invalid they could be shown as they are not the secret) to prove the dealer is the attacker.
So participants should check first the share against commitment, and if it doesn't match, they should send the invalid share to chain, if there is at least one invalid share, exclude the attacker (taking his collateral)

p.s.:
It seams the problem is already solved here:
https://github.com/gonka-ai/gonka/commit/6211d32109e89a913d2070d05e54d7bbb6fe8951#diff-89c99e1a367a5b8cc41a94e676865a63e9ed86554cdbf04000b4d5297381b8f9

But InvalidDealers should be tracked there to take collateral from them and exclude from the epoch
