> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 1 · Track A**

> Before scaling — you need to know who you are, who you're for, and what makes you credibly different. This is step one.

**Payment:** 25,000 USDT — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — where we start

Positioning isn't a tagline. It's the foundational document that everything else depends on — how the brand looks, how it sounds, who it speaks to, and how it explains its value to different audiences. Without it, a brandbook is just pretty colors, and campaigns are noise without an address.

We begin with a deep dive into Gonka: the product, the technology, and how it's currently perceived. In parallel, we map the competitive landscape across AI infrastructure and DePIN to find the territory Gonka can own credibly and long-term. The output is a concrete document with a brand idea, values, archetype, tone of voice, and audience personas for three key groups.

The process is iterative. We run stakeholder sessions with the Gonka team, gather feedback, and align direction before finalizing.

## What we deliver

- **Competitive Map** — positioning of key players in AI infrastructure and DePIN: where the gaps are, where it's oversaturated.
- **Brand Idea & Values** — core brand concept, 3–5 values, mission and brand promise, aligned with the team.
- **Archetype & Tone of Voice** — brand archetype and tone/voice guidelines (v1), the foundation for all copy and communications.
- **Audience Personas** — 3 detailed profiles (miner, inference buyer, investor): motivations, barriers, and key messages.

## Final deliverable

A positioning and audience-strategy document, signed off with Gonka stakeholders at the final presentation. Unlocks Brandbook development (1.2) and serves as the strategic foundation for every subsequent phase.

## Terms

| | |
|---|---|
| Timeline | 3–4 weeks |
| Format | Fixed scope |
| Commitment | This phase only |
| Unlocks | Offer 1.2 |

## On-chain action

On pass, the gov authority calls the community USDT vault's `withdraw_ibc`, sending 25,000 USDT (IBC) to the recipient wallet:

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
  "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
  "msg": { "withdraw_ibc": {
    "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
    "amount": "25000000000",
    "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm"
  } },
  "funds": []
}
```

USDT has 6 decimals: 25,000 × 10⁶ = 25,000,000,000.
