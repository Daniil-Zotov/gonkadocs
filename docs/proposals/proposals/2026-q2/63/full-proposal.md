> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 2 · Digital infrastructure**

> From placeholder to a conversion-ready brand site. Three dedicated landing pages — one per audience, each with its own CTAs and messaging.

**Payment:** 10,000 USDT — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — the website as a conversion tool

Most early-stage crypto projects launch a website that says almost nothing — and converts nobody. This offer builds something different: a working acquisition tool structured around the 3 core audience segments defined in 1.1. Each group arrives with different questions, and those answers belong on separate pages with their own CTA architecture.

Design is built strictly on the brandbook from 1.2 — no deviations from the visual system. The site becomes the first production application of the brandbook: positioning and visual identity from Phase 1 don't just inform the site, they are the site.

The tech stack is confirmed with the Gonka team at kickoff. Mobile optimization is mandatory.

## What we deliver

- **Website Redesign** — full redesign built on the brandbook: identity, navigation, hero, and information architecture.
- **3 Core Audience Landing Pages** — one page per segment defined in 1.1, each with its own messaging and CTA.
- **CTA Architecture** — conversion paths per audience: from landing page to target action.
- **Mobile Optimization** — full responsiveness, Core Web Vitals, tracking-ready infrastructure for 2.2.

## Final deliverable

A live website plus 3 landing pages — fully responsive, with infrastructure ready for tracking (2.2) and UTM attribution. The first public application of the Gonka brandbook.

## Terms

| | |
|---|---|
| Timeline | 4–6 weeks |
| Requires | Positioning (1.1) + Brandbook (1.2) |
| Commitment | This phase only |
| Unlocks | Offer 2.2 |

## On-chain action

On pass, the gov authority calls the community USDT vault's `withdraw_ibc`, sending 10,000 USDT (IBC) to the recipient wallet:

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
  "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
  "msg": { "withdraw_ibc": {
    "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
    "amount": "10000000000",
    "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm"
  } },
  "funds": []
}
```

USDT has 6 decimals: 10,000 × 10⁶ = 10,000,000,000.
