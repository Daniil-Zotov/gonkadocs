---
title: "#926 — [P1] Seed for POC fix"
source: https://github.com/gonka-ai/gonka/issues/926
issue_number: 926
synced_at: 2026-07-06T09:52:18Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #926](https://github.com/gonka-ai/gonka/issues/926) каждые 6 часов. 

# 🔴 [P1] Seed for POC fix

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-03-20 23:33 UTC · **Обновлено:** 2026-04-11 04:28 UTC

**Метки:** `Priority: Medium`

**Веха:** v0.2.12

---

## 📝 Описание

- [x] on-chain params to choose option 
- [x] MLNode support
- [x] way to monitor it

---

## 💬 Комментарии (1)

### Комментарий 1 — [@IgnatovFedor](https://github.com/IgnatovFedor)

*2026-03-31 17:54 UTC*

# Proposal: Concatenated Murmur (concat_murmur)

## The problem

`_seed_from_string` computes sha256(seed_string) but discards 224 of the 256 bits:

```python
return int(h[:8], 16)  # only 32 bits used
```

With a 32-bit seed space, an attacker running Node A can find a nonce that produces the same seed as Node B's target
nonce in ~2^32 SHA256 evaluations. They then run the model once (as Node A) and submit that output as
Node A's and B's proof just with different nonces. The validator accepts it.

## Proposal

SHA256 produces 256 bits. Split them into 8 × 32-bit words (s0, s1, ..., s7). Use each word as a murmur3 seed to
generate an independent segment of the output:

sha256(block_hash + public_key + nonce) → [s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7]

output = [ murmur(s0, n/8) | murmur(s1, n/8) | ... | murmur(s7, n/8) ]

All 256 bits of SHA256 are consumed. The output is still N(0,1) — same murmur3 → Box-Muller pipeline,
just chunked into 8 segments that are concatenated.

##  Why it solves the problem

The attacker submits one nonce nonce_X. The verifier computes:

sha256(block_hash + key_B + nonce_X)  →  s0_X, s1_X, ..., s7_X

All 8 sub-seeds are locked to that single hash call. For the forged proof to pass, the attacker needs:

sha256(key_B + nonce_X) == sha256(key_A + nonce_Y)   [all 256 bits]

That is a SHA256 collision — 2^128 work by birthday attack. The attacker cannot attack the 8 segments independently
because changing nonce_X changes all 8 sub-seeds simultaneously through SHA256.

The "attack segments one by one" idea would require submitting 8 different nonces — one per segment — which the protocol
does not allow. One nonce → one hash → all 8 seeds determined at once.

# On-chain part
## MLNode Version

Add software_version field to HardwareNode proto message. The broker fetches the version from mlnode at node registration/update time and includes it in the on-chain tx. This makes the running mlnode/vllm version visible on-chain per node for auditing.

## PoC Stronger RNG (poc_stronger_rng_enabled)
Add poc_stronger_rng_enabled bool to PocParams. When enabled via governance vote, switches PoC input vector generation from the legacy single 32-bit murmur3 seed to concatenated murmur3 using the full 256-bit SHA256 output.
