> 📋 Part of the **[TheSoul × Gonka proposal overview](https://github.com/ADME-CY-LTD/thesoul-gonka-proposals/issues/7)** — phasing, who we are, and how to vote.

**Gonka.AI · Phase 1 · Track A**

> The complete brand identity system — logo, color, typography, visual language, and templates. Everything that defines how Gonka looks and speaks, in one production-ready document.

**Payment:** 20,000 USDT — single tranche to TheSoul on proposal pass.
**Recipient:** `gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm`

## Approach — visual system as infrastructure

A brandbook isn't decoration. It's a production document that every visual decision depends on — the website, social media, merch, investor decks. It's built strictly on the positioning from 1.1 — the archetype, tone of voice, and brand idea. Without that foundation, the visual style will be arbitrary.

We develop the complete system: logo suite with usage variants, color system and typography, graphic language and patterns, photo style and layout principles, SMM and digital templates, merch direction. Every decision is strategically justified.

The process is iterative. Three rounds of alignment: concept directions → development of the chosen direction → finalization. Each round includes a presentation to the Gonka team with the rationale behind every decision.

## What we deliver

- **Logo System** — primary logo, monogram, light/dark variants, clear-space rules, and prohibited uses.
- **Color & Typography** — primary and extended palette, typographic scale, pairing principles, ready-to-use font files.
- **Graphic Language** — patterns, iconography, layout principles: Gonka's unique visual code, consistent across every surface.
- **SMM Templates** — ready-to-use template set for X, Telegram, and LinkedIn, adapted to all formats and placements.

## Final deliverable

Complete brandbook PDF plus all source files, signed off with the Gonka community at the final presentation. Unlocks all visual production in Phase 2+. No visual asset moves forward without this document.

## Terms

| | |
|---|---|
| Timeline | 4–6 weeks |
| Format | Fixed scope |
| Commitment | This phase only |
| Requires | Offer 1.1 |

## On-chain action

On pass, the gov authority calls the community USDT vault's `withdraw_ibc`, sending 20,000 USDT (IBC) to the recipient wallet:

```json
{
  "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
  "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
  "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
  "msg": { "withdraw_ibc": {
    "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
    "amount": "20000000000",
    "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm"
  } },
  "funds": []
}
```

USDT has 6 decimals: 20,000 × 10⁶ = 20,000,000,000.
