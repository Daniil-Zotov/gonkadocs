> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 2 · Digital infrastructure**

> Every click has a source. Every conversion is tracked. This must be live before any traffic flows.

**Payment:** 28,000 GNK (≈ 7,000 USDT at 0.25 GNK/USDT) — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — measure from day one

Most companies set up analytics after they've already spent budget on traffic. We do the opposite: analytics and UTM tracking go live immediately after the site launches (2.1) — before any campaigns begin. Otherwise every dollar spent on promotion flies blind.

Full GA4 implementation: account setup, event tagging, conversion configuration per audience. A UTM taxonomy for all channels — organic, influencers, PR, paid — with a unique UTM tracker for every future creator.

The output isn't just "GA4 connected" — it's a working dashboard with per-segment funnels and an executive report the Gonka team can read without any technical knowledge.

## What we deliver

- **GA4 Setup** — full account, properties, data streams, and conversion events configured for all three audiences.
- **UTM Framework** — UTM parameter taxonomy for all channels and creators, with documentation and templates.
- **Event Tracking** — all key on-site actions tagged: CTA clicks, form fills, inter-landing navigation.
- **Dashboard & Reports** — live funnel dashboard per segment plus an executive report template for the Gonka team.

## Final deliverable

GA4 configured, live UTM tracking across all channels, and a reporting dashboard accessible to the Gonka team. From this point forward, every marketing activity is measured.

## Terms

| | |
|---|---|
| Timeline | 2–3 weeks |
| Requires | Live website (2.1) |
| Commitment | This phase only |
| Unlocks | Offer 2.3 |

## On-chain action

On pass, the gov authority spends from the community pool, sending 28,000 GNK to the recipient wallet:

```json
{
  "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
  "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm",
  "amount": [{ "denom": "ngonka", "amount": "28000000000000" }]
}
```

GNK has 9 decimals: 28,000 × 10⁹ = 28,000,000,000,000 ngonka (≈ 7,000 USDT at 0.25 GNK/USDT).
