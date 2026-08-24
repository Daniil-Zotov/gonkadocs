---
title: "#1637 — Gateway allowlist request: Fusion AI Gateway — production wholesale broker (DeepSeek Flash / MiniMax / Kimi)"
source: https://github.com/gonka-ai/gonka/issues/1637
issue_number: 1637
synced_at: 2026-08-24T19:04:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request: Fusion AI Gateway — production wholesale broker (DeepSeek Flash / MiniMax / Kimi)
    <span class="issues-number">#1637</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/theaungmyatmoe">@theaungmyatmoe</a> opened 2026-08-24 17:15 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-24 17:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator

- **Name:** Aung Myat Moe
- **GitHub:** [@theaungmyatmoe](https://github.com/theaungmyatmoe)
- **Project:** Fusion AI Gateway (`https://api.fusioncode.app`) — production OpenAI-compatible wholesale gateway
- **Contact:** via this GitHub issue

## Requested creator address

```text
gonka10x8h2drma75gvk5pj8tnf4q5tj3zws9n3r7839
```

Public key (compressed secp256k1, hex):

```text
02D25E3E9DD03C5AFC55F9C081473E6B5C86C7012D4AEAFF57A703E484B0038B66
```

Please consider adding this address to `devshard_escrow_params.allowed_creator_addresses`.

The key is dedicated exclusively to devshard escrow creation. Per the self-hosted gateway guide, the creator will be funded only after allowlist membership is confirmed.

## Models

- `deepseek-ai/DeepSeek-V4-Flash-0731` — primary (cache-heavy agent workload)
- `MiniMaxAI/MiniMax-M2.7` — secondary
- `moonshotai/Kimi-K2.6` — secondary / evaluation

## Use case

We operate a production wholesale gateway already serving real OpenAI-compatible traffic at `api.fusioncode.app`. We broker DeepSeek V4 Flash, MiniMax M2.7, and Kimi K2.6 to downstream clients (agent infrastructure, high-volume background processing).

We currently route through OpenBroker, but need the native devshard creator path because:

- we require **direct GNK settlement and self-custody** for a committed wholesale volume (multi-billion tokens/day pipeline);
- we need **control over escrow pooling, rotation, settlement, and capacity-aware routing** for a sustained 60–100 RPS baseline with burst support;
- we need the **network per-token price** rather than a broker layer between us and the chain;
- broker-side concurrency limits have surfaced under sustained load.

This request is for a **production self-hosted gateway**, not a broker-directory listing.

## Initial deployment plan

- Gateway-only deployment (`libermans/gonka-devshard-proxy`) on an existing Linux VPS
- Public node endpoints (no full chain node), `GATEWAY_MAX_CONCURRENT_REQUESTS=512`
- Multiple devshards pooled for throughput and epoch rotation; capacity-aware limits enabled
- Reverse proxy in front; creator key dedicated and not reused
- Staged concurrency ramp, settlement/refund verification, then production cutover

## Validation and contribution plan

1. One manually managed escrow + deterministic functional checks.
2. Concurrency ramp: 1 / 3 / 10 / 25 / 50 / 100 / 200.
3. Measure success rate, HTTP error distribution, TTFT, p50/p95/p99 latency, output throughput, settlement/refund behavior.
4. Enable multi-escrow pooling + rotation only after single-escrow verification.
5. Share anonymized capacity and reliability results with the Gonka community.

## Governance and operations commitments

- We understand allowlist inclusion is an **on-chain governance decision** and is not guaranteed.
- We will respond to maintainer and host questions promptly.
- We will not fund or open escrows until the address is confirmed on the allowlist.
- We will start with staged private traffic, not an immediate public endpoint.
- We will publish operational findings and adjust limits if governance or operators request it.

## Related

- Open discussion of gateway economics and cache-served token pricing: https://github.com/gonka-ai/gonka/discussions/1636
- Telemetry PR (cache metadata passthrough): https://github.com/gonka-ai/gonka/pull/1633
- Precedent request: #1479 (Knyazev AI)
</div>

---

> 🔄 **Auto-synced** from [Issue #1637](https://github.com/gonka-ai/gonka/issues/1637) every hour.
