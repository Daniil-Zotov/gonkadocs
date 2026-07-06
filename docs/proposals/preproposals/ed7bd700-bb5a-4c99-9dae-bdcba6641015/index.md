---
title: "Gonka Integration Grant for AI Startups and Products (GNK Rewards)"
template: proposals-main.html
---

# Gonka Integration Grant for AI Startups and Products (GNK Rewards)

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🟢 Active</div>

**Author:** Evgenii Maksimenkov
**Created:** 2026-04-25 06:46 UTC
**Closes:** 2026-07-24 06:45 UTC
**Language:** EN
**Votes:** 3
**Avg. Bid:** 50.0K GNK

</div>

Grant program in GNK for AI startups that integrate Gonka inference into their production product. Fixed grant tiers, milestone-based payouts, mandatory technical and visibility requirements.

---

## Full Proposal

Context

Gonka offers an OpenAI-compatible decentralized inference API (currently serving Qwen3-235B-A22B-Instruct-2507-FP8) at competitive cost vs. centralized providers. To accelerate Developer adoption, this grant program rewards **AI startups and products that integrate Gonka as a production inference backend** with grants paid in **GNK tokens**.

This is a **non-dilutive grant** — Gonka takes no equity, no revenue share, no IP rights. The only obligations are technical integration and agreed visibility requirements.

## 2. Who Can Apply

Eligible applicants are companies or teams that:

1. Operate an AI-powered product (live or in active development) that uses LLM inference as a core component.
2. Have a **working product or functional MVP** at time of application — concept-only pitches are NOT eligible.
3. Have a registered legal entity (any jurisdiction permitted by Gonka compliance).
4. Pass basic KYB (Know-Your-Business) checks.

**Examples of eligible products**: AI chat apps, agent frameworks, RAG products, AI coding tools, AI customer-support platforms, AI content tools, vertical AI SaaS (legal/medical/finance), AI infrastructure tools.

**NOT eligible**: pure research projects without product, hobby projects without users, products that resell raw inference, pump-and-dump token projects, projects competing directly with Gonka (other decentralized inference networks).

## 3. Grant Tiers

| Tier | Grant Amount (GNK equivalent in USD) | For |
|---|---|---|
| **Starter** | $5,000 | Pre-revenue products, <1K MAU, integration of Gonka as one of multiple backends |
| **Growth** | $25,000 | Revenue-generating or >5K MAU, Gonka as primary backend for ≥30% of inference traffic |
| **Scale** | $100,000 | $500K+ ARR or >50K MAU, Gonka as primary backend for ≥70% of inference traffic |
| **Strategic** | $100,000+ (negotiated) | Category-defining integrations, custom case-by-case |

GNK is paid at the 7-day TWAP at the date of each milestone payout. Recipients are responsible for their own tax treatment.

## 4. Team Requirements

Applicants MUST demonstrate:

1. **Technical capability**: at least 1 founder or core team member with verifiable engineering background (GitHub profile, prior shipped product, or equivalent). LinkedIn alone is not sufficient.
2. **Working product**: live URL, app store listing, or demo video showing the product in actual use. Mockups and Figma files are not accepted.
3. **Real users or pilot customers**: minimum 50 active users OR 1 paying customer OR 3 signed LOIs at time of application.
4. **No anonymous teams** for Growth tier and above. Starter tier permits pseudonymous teams with established crypto reputation.
5. **Clean track record**: no prior fraud, rug pulls, or unresolved legal issues against the team or company.
6. **English communication**: at least one team member able to communicate fluently in English for technical and reporting purposes.

## 5. Technical Integration Requirements

To qualify for grant payout, the integration MUST meet ALL of the following:

### 5.1. Production Integration

- Gonka MUST be wired into the **production codepath** of the product, not a sandbox or feature-flagged demo.
- Integration MUST use the OpenAI-compatible `/v1/chat/completions` endpoint (or other supported Gonka APIs) with proper ECDSA request signing as specified in the Gonka Developer Docs.
- Production traffic share served by Gonka MUST meet the tier minimum (see §3) and be verifiable via on-chain inference records.

### 5.2. Reliability and Fallback

- Implementation MUST handle Gonka network errors gracefully (retries with exponential backoff, optional fallback to a secondary provider).
- Implementation MUST NOT route only failed/degraded requests to Gonka. Routing logic MUST be either deterministic (e.g., percentage split) or unbiased.

### 5.3. Code Quality

- Integration code MUST be reviewable. For closed-source products, the relevant integration module MUST be shared privately with the Gonka grants team for verification.
- Open-source integrations are encouraged and MAY receive a 10% bonus on the grant amount.

### 5.4. Telemetry

- Recipient MUST share basic usage telemetry with Gonka monthly: total inference calls routed to Gonka, total tokens, error rate, p95 latency observed. Aggregate numbers only — no end-user data required.

## 6. Visibility Requirements

To qualify for grant payout, the recipient MUST complete ALL of the following:

### 6.1. Website

- "Powered by Gonka" badge displayed on the product website (footer or about/tech page acceptable). Badge assets provided by Gonka.
- One sentence in the product's stack/technology section naming Gonka as the inference provider, linked to gonka.ai.

### 6.2. Public Announcement

- One public announcement post on the recipient's primary channel (X, blog, or LinkedIn) announcing the integration. Minimum reach: the recipient's actual organic following — no requirement to buy reach.
- Post MUST tag @gonka_ai (or current official handle) and MUST be coordinated with the Gonka marketing team for timing (not content approval — recipient retains editorial control).

### 6.3. Case Study Cooperation

- Recipient agrees to participate in **one** case study (written interview, 60–90 min total time commitment) within 6 months of grant completion. Gonka produces and publishes the case study; recipient reviews for accuracy before publication.

### 6.4. Logo Use

- Recipient grants Gonka the right to use the recipient's name and logo in:
  - Gonka's website (Developers / Customers section)
  - Gonka's pitch decks and marketing materials
  - Gonka's social channels in the context of this integration
- This right is non-exclusive, royalty-free, and revocable on 30 days' notice if the integration is discontinued.

### 6.5. Optional (Bonus)

- Conference talk, podcast appearance, or YouTube video featuring the integration: **+5% grant bonus**.
- Open-source release of the integration (with permissive license): **+10% grant bonus** (already mentioned in §5.3).
- Maximum cumulative bonus: 20%.

## 7. Milestone-Based Payout Structure

Grants are paid in **3 milestones**, NOT upfront:

| Milestone | % of Grant | Trigger |
|---|---|---|
| **M1: Integration Live** | 30% | Production integration deployed, Gonka traffic share verified on-chain at tier minimum, "Powered by Gonka" badge visible on website |
| **M2: 60-Day Sustained Usage** | 40% | Tier-minimum traffic share maintained for 60 consecutive days, monthly telemetry submitted, public announcement post published |
| **M3: 6-Month Retention + Case Study** | 30% | Tier-minimum traffic share maintained at month 6, case study completed |

If a recipient drops below the tier minimum:
- For >14 days: M2 or M3 payout is paused until restored.
- For >60 days: remaining unpaid milestones are forfeited (already-paid milestones are NOT clawed back unless fraud is detected).

## 8. Fraud Prevention

- Synthetic traffic, bot-generated inference calls, or any artificial inflation of usage metrics triggers immediate forfeiture and clawback of all paid milestones.
- Gonka reserves the right to audit on-chain inference patterns and request reasonable verification (e.g., correlation with public product usage metrics).
- Multiple grant applications from related entities (same team, same product under different names) are not permitted.

## 9. Application Requirements

Applicants MUST submit:

1. **Company info**: legal entity, jurisdiction, founding date, team size.
2. **Product info**: live URL, current MAU/ARR (if applicable), inference volume estimate (calls/month, tokens/month).
3. **Team info**: founders' names, GitHub/LinkedIn, prior products shipped.
4. **Integration plan**: which Gonka model(s) will be used, expected traffic share, integration timeline, fallback strategy.
5. **Tier requested** with justification.
6. **Visibility commitment**: confirmation of §6 obligations.
7. **Wallet address** (Gonka-compatible bech32) for grant payout.

## 10. Out of Scope

- Equity investment, SAFE, token warrants — this is a non-dilutive grant only.
- Co-marketing budget beyond the case study and announcement (separate marketing partnerships handled outside this program).
- Custom model deployment on Gonka network (separate process).
- Free inference credits beyond what the grant amount can purchase at standard rates.

---

## Votes (3)

| Voter | Amount | Date |
| :----- | :----- | :--- |
| `gonka1gm...gzg6ry` | 50.0K GNK | 2026-04-25 06:46 |
| `gonka109...wdesy6` | 50.0K GNK | 2026-05-03 14:36 |
| `gonka1rw...dftj3l` | 50.0K GNK | 2026-04-25 15:53 |

---

## Comments (1)

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 20:48* · 👍 1 · 👎 0

Нужно установить требования еще по количеству инференса, который они будут использовать.

А то я уже использую инференс Гонка для своих проектов. 
Но при этом я не думаю, что мне за это нужно платить ))

---


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/ed7bd700-bb5a-4c99-9dae-bdcba6641015)

</div>
