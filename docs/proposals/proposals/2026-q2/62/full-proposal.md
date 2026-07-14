> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 1 · Track B**

> Fixed budget, fixed timeline — a live performance signal before we talk about scaling.

**Payment:** 50,000 USDT — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — data, not promises

Before committing serious budget to influencer marketing, we need to know what actually works for Gonka. The pilot answers that with hard constraints: fixed spend, a 4-week window, measurable output. No deck of hypotheses — a real performance signal.

Which creators drive qualified traffic. Which messages land with crypto investors. What a cost-efficient placement looks like for this product. That's the output — and it feeds directly into how we scale in Phase 3.

Eight primary creators across X, YouTube, and niche newsletters — crypto audience, western markets — each matched to a specific audience segment (institutional investors, the DeFi community, crypto-native developers), with five backups on standby. All outreach, briefing, and content sign-off handled by TheSoul; UTM tracking per creator, live from day one. Individual creator rates are finalized during outreach and negotiation; Gonka picks the preferred mix within the budget. The pilot is sized for **~180K estimated views at a ~$283 blended CPM, with 2,100–4,200 estimated clicks**.

## What we deliver

- **Creator Selection & Outreach** — 8 primary creators + 5 backups, vetted by audience quality and past crypto performance.
- **Brief & Approval** — creative briefs per creator, message alignment with the Gonka team, content review and sign-off.
- **UTM Tracking** — unique UTM links per creator from day one, real-time click and conversion tracking across all placements.
- **Performance Report** — full report at close: reach, clicks, CTR, and scaling recommendations for Phase 3.

## Final deliverable

A live campaign with selected creators, a full performance report at close, and strategic scaling recommendations for Phase 3 — all based on real data.

## Terms

| | |
|---|---|
| Timeline | 3 months |
| Platforms | X · YouTube · Newsletters |
| Market | Western, English-speaking |
| Unlocks | Phase 3 scaling |

## On-chain action

On pass, the gov authority calls the community USDT vault's `withdraw_ibc`, sending 50,000 USDT (IBC) to the recipient wallet:

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
  "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
  "msg": { "withdraw_ibc": {
    "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
    "amount": "50000000000",
    "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm"
  } },
  "funds": []
}
```

USDT has 6 decimals: 50,000 × 10⁶ = 50,000,000,000.
