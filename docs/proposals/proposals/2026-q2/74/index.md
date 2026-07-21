---
title: "#74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones"
description: "Full proposal: https://gonkalabs.com/proposal

This proposal funds the next six months of work for the Gonka ecosystem.

The focus is production-grade infrastructure and high-use products: Gonka.gg V2"
template: proposals-proposals-main.html
---

# #74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `74`

**Type:** Execute Contract, Transfer With Vesting

**Submit:** 2026-06-10 20:42 UTC

**Voting:** 2026-06-10 20:42 UTC → 2026-06-12 20:42 UTC

**Proposer:** [`gonka1e3pepqllu89t8l2acw86fgp5jjkw8m7kcl47nk`](https://gonka.gg/address/gonka1e3pepqllu89t8l2acw86fgp5jjkw8m7kcl47nk){:target="_blank"}

**Metadata:** [https://gonkalabs.com/proposal](https://gonkalabs.com/proposal)

<div class="prop-funding-line">$70,000 · Community Pool · 330,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/74){:target="_blank"}

</div>

Full proposal: <https://gonkalabs.com/proposal>

This proposal funds the next six months of work for the Gonka ecosystem.

The focus is production-grade infrastructure and high-use products: Gonka.gg V2 as the default explorer and data hub, rpc.gonka.gg as reliable public RPC, proxy.gonka.gg for business inference access and API-key management, a mobile Gonka app based on GG Wallet, governance tooling through Gonkavote, and a public open-source Marketing Transparency Dashboard. Existing tools such as Gonkablocks, meter.gonka.gg, and other Gonka Labs projects will continue to receive maintenance, fixes, and support.

Gonka Labs products will remain non-commercial: no ads, paid placements, PR slots, or profit markups. Any fees are intended only to cover infrastructure and operating costs.

Accountability commitments include monthly public progress and spending reports, an 80%+ open-source code commitment, and on-chain transparency for both the USDT payment and GNK vesting.

Budget: 70,000 USDT paid immediately to cover six months of server infrastructure, monitoring, operations, and guaranteed stablecoin compensation; plus 330,000 GNK vested to the core team over 180 Gonka vesting epochs, aligning the team with long-term network growth.

Full proposal: <https://gonkalabs.com/proposal>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:79.6%"></div>
    <div class="prop-tally-no" style="width:1.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:19.4%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 305,163 (79.6%)</span>
    <span class="prop-tally-no-text">No 3,791 (1.0%)</span>
    <span class="prop-tally-veto-text">Veto 15 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 74,304 (19.4%)</span>
    <span class="prop-tally-total-text">Total 383,273 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 2 | `/inference.streamvesting.MsgTransferWithVesting` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "70000000000",
        "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh"
      }
    },
    "funds": []
  },
  {
    "@type": "/inference.streamvesting.MsgTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "330000000000000"
      }
    ],
    "vesting_epochs": "180"
  }
]
```

</details>

---

## Отчёты

### Report #1 — 2026-07-18

<details class="prop-contracts" markdown="1">
<summary markdown="1">Gonka Labs — Monthly Report No.1</summary>

[Открыть отдельной страницей](report1.md) · [Обсуждение на GitHub](https://github.com/gonka-ai/gonka/discussions/1477)

---

Hey! Gonka Labs here.

On June 12th the community passed [Proposal #74](https://gonka.gg/network/proposals/74). That vote funded the next stretch of work — infra, ops, and shipping products for the ecosystem.

This is the first public progress report we promised in the proposal (monthly updates on GitHub Discussions). Short version of what landed so far:

1. **OpenBroker** — new product, live
2. **Pulse** — new product, live
3. **gonka.gg** — ~240 QA bugs closed + big product updates (devshards / inference, network analytics, mobile)
4. **proxy.gonka.gg** — B2B inference proxy scaled hard + public status/analytics + DevShards v3
5. **Infra move** — Whole infra migrated (explorer + indexer stack, all dbs, all backend, new frontend and analytics stack) onto the new production setup.

---

### 1. OpenBroker

We already announced the launch here: [OpenBroker — broker for brokers or Devshards as a service](https://github.com/gonka-ai/gonka/discussions/1363) (Jun 23).

Quick recap: OpenBroker is managed DevShards-as-a-service. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at `https://api.openbroker.gonka.gg/v1` (UI at [openbroker.gonka.gg](https://openbroker.gonka.gg)). No wallet whitelist dance, no running your own escrow rotation. GNK billing with no markup. Public stats at [openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats).

#### Since launch (numbers as of Jul 18)

- **33 active brokers** — 48 registered orgs
- **~3.2 GNK deposited** into broker ledgers
- **~15M requests logged** in usage
- **~11.8B tokens served** across MiniMax, Kimi, GLM, Qwen
- Peak observed throughput around **~100 req/s**
- **DevShards v3 live** on both production gateways
- Real brokers / relays already pointing parts or all traffic at OpenBroker

#### Ops + product work after launch

- Moved production off the early Railway pilot onto a **dedicated server**
- Dual-gateway HA with live traffic drain/switch
- Broker dashboard: per-request usage, participant breakdown, cost reconciliation
- New broker APIs: `GET /v1/usage` and `GET /v1/usage/{id}`
- Hardening under real load

Links:
- Product: [https://openbroker.gonka.gg](https://openbroker.gonka.gg)
- API: [https://api.openbroker.gonka.gg/v1](https://api.openbroker.gonka.gg/v1)
- Register: [https://openbroker.gonka.gg/register](https://openbroker.gonka.gg/register)
- Stats: [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats)

---

### 2. Pulse

Pulse is the live media + sentiment dashboard for Gonka. It pulls public Gonka coverage from X, Instagram, YouTube, and the web into one place, scores tone via Gonka LLMs (`proxy.gonka.gg`), and shows activity / reach / engagement next to GNK market data.

Live: [https://pulse.gonka.gg](https://pulse.gonka.gg)

#### What shipped

- Full Pulse app on Railway (API + web + Postgres), collectors on a ~2h cadence
- Sources: X, Instagram, YouTube, curated web / press
- Dashboard: last-24h activity / reach / engagement charts, sentiment gauge + 14-day tone chart, GNK market data, Fear & Greed, top creators, content feed, EN + RU translations
- Sentiment analysis runs on LLMs in the Gonka network
- Embedded on the gonka.gg homepage
- Public read API for stats / market / feed / news / creators

#### Numbers (as of Jul 18)

- **~2,600 posts indexed**
- **~11.9M total reach** and **~149K engagement**
- Sentiment: **100% of indexed items analyzed** (mid-50s / Neutral)

---

### 3. gonka.gg — bugs + product work

#### QA bug smash (~240)

- Mobile layouts and basic UX reorganizations
- Charts, maps, tooltips escaping viewport on touch
- Table, card alignments, restructuring
- Status badges, filters, i18n gaps
- Reward / weight tooltips and incomplete-epoch edge cases
- Block / tx / wallet polish
- Updated indexers (28k less load on the network)
- Devshards V3 flow alignment for inference data ingestion

#### Product / data updates

- Built `devshard-poller` that ingests off-chain session diffs into ClickHouse
- `/network/inference` driven from that pipeline
- **Model Weight Share** on `/network` — weight distribution across AI models per epoch
- GPU / reward-per-weight chart polish
- Proper Frontend serving with low TTFB, API with horizontal auto-scaling

Links:
- Explorer: [https://gonka.gg](https://gonka.gg)
- Inference: [https://gonka.gg/network/inference](https://gonka.gg/network/inference)
- Network: [https://gonka.gg/network](https://gonka.gg/network)

---

### 4. proxy.gonka.gg — B2B inference + public status

[proxy.gonka.gg](https://proxy.gonka.gg) is our OpenAI-compatible inference proxy on top of Gonka DevShards — API keys, balances, usage, docs, chat playground. Public API at [api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1).

#### Numbers (as of Jul 18)

- **~29.0B tokens** served (~5.2M requests, ~96.8% OK)
- **~23.6B tokens in the last 7 days** (~3.5M requests)
- **~7.3B tokens in the last 24 hours** (~1.1M requests)
- Peak recent days ~**4.8-5.0B tokens / day**
- Model mix: MiniMax-M2.7 ~25.6B, Kimi-K2.6 ~3.4B
- Accounts: +10-30 new accounts daily

#### What shipped since the vote

- **Dedicated production box** for the API — moved off the flaky VPS / Railway onto a tuned server
- **Own DevShard gateway ops** — escrow rotation, capacity-aware concurrency limits, admin tooling
- Gateway now on **DevShards v3** ahead of the network v0.2.14 deadline
- **Public status / analytics page** at [proxy.gonka.gg/status](https://proxy.gonka.gg/status)
- Product surface: models page, docs, partner paths, top-up flows, password reset

Links:
- Product: [https://proxy.gonka.gg](https://proxy.gonka.gg)
- API: [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1)
- Status: [https://proxy.gonka.gg/status](https://proxy.gonka.gg/status)

---

We are still heads-down on the rest of the Proposal #74 checklist — hardening infra under real load, polishing what already shipped, and building the next products on the list. More updates as they land. Stay tuned.

---

**Links:** [Gonka Labs](https://gonkalabs.com) · [Explorer](https://gonka.gg) · [OpenBroker](https://openbroker.gonka.gg) · [Pulse](https://pulse.gonka.gg) · [Proxy](https://proxy.gonka.gg) · [RPC](https://rpc.gonka.gg) · [GitHub](https://github.com/gonkalabs)

</details>

