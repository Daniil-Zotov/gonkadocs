> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 2 · Digital infrastructure**

> A 360° playbook that brings every channel into a single coherent logic. The final deliverable of Phase 2 — and the key that unlocks Phase 3.

**Payment:** 100,000 GNK (≈ 25,000 USDT at 0.25 GNK/USDT) — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — plan before you scale

Before launching campaigns, content production, and PR — you need a clear plan: which channels, for which audience, with which message, at what volume. Without this document, Phase 3 activations will be fragmented and off-brand.

The 360° digital strategy ties everything together: social, site, influencer marketing, PR, and content into a single coherent logic. Channel matrix by audience, content types and volumes per month, a messaging guide by segment, social-media strategy (X, Telegram, LinkedIn), and brand-voice guidelines.

The document is built on data from 1.1 (personas), 1.3 (pilot results), and 2.2 (site analytics) — every decision grounded in real data that already exists by the time of writing.

## What we deliver

- **360° Strategy Document** — full digital playbook: channels, audiences, messages, formats, and volumes.
- **Channel Matrix** — which channel for which audience, with what KPI and budget logic.
- **Brand Voice Guidelines** — tone of voice by channel and segment: how Gonka sounds consistent everywhere.
- **Social Media Strategy** — X, Telegram, LinkedIn: formats, frequency, content types, and an influencer framework.

## Final deliverable

A signed-off 360° strategy document — the brief for all production and activations in Phase 3. Without it, no Phase 3 module can be scoped.

## Terms

| | |
|---|---|
| Timeline | 2–3 weeks |
| Requires | GA4 data (2.2) |
| Commitment | This phase only |
| Unlocks | Phase 3 |

## On-chain action

On pass, the gov authority spends from the community pool, sending 100,000 GNK to the recipient wallet:

```json
{
  "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
  "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm",
  "amount": [{ "denom": "ngonka", "amount": "100000000000000" }]
}
```

GNK has 9 decimals: 100,000 × 10⁹ = 100,000,000,000,000 ngonka (≈ 25,000 USDT at 0.25 GNK/USDT).
