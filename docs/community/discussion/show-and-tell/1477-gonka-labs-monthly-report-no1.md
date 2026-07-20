---
title: "#1477 — Gonka Labs - Monthly Report No.1"
source: https://github.com/gonka-ai/gonka/discussions/1477
discussion_number: 1477
category: show-and-tell
synced_at: 2026-07-20T19:03:04Z
---

> 🔄 **Auto-sync:** from [Discussion #1477](https://github.com/gonka-ai/gonka/discussions/1477) every hour. 

# Gonka Labs - Monthly Report No.1

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-07-18 18:31 UTC · **Обновлено:** 2026-07-18 18:31 UTC

---

## 📝 Описание

# 

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/ZarQaYSqnMMS69H.png)

Hey! Gonka Labs here.

On June 12th the community passed [Proposal #74](https://gonka.gg/network/proposals/74). That vote funded the next stretch of work - infra, ops, and shipping products for the ecosystem.

This is the first public progress report we promised in the proposal (monthly updates on GitHub Discussions). Short version of what landed so far:

1. **OpenBroker** - new product, live
2. **Pulse** - new product, live
3. **gonka.gg** - ~240 QA bugs closed + big product updates (devshards / inference, network analytics, mobile)
4. **proxy.gonka.gg** - B2B inference proxy scaled hard + public status/analytics + DevShards v3
5. **Infra move** - Whole infra migrated (explorer + indexer stack, all dbs, all backend, new frontend and analytics stack) onto the new production setup.

***

## 1. OpenBroker

We already announced the launch here: [OpenBroker - broker for brokers or Devshards as a service](https://github.com/gonka-ai/gonka/discussions/1363) (Jun 23).

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/GUY7yidIzteGuy9.png)

Quick recap: OpenBroker is managed DevShards-as-a-service. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at `https://api.openbroker.gonka.gg/v1` (UI at [https://openbroker.gonka.gg](https://openbroker.gonka.gg)). No wallet whitelist dance, no running your own escrow rotation. GNK billing with no markup. Public stats at [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats).

### Since launch (numbers as of Jul 18)

- **33 active brokers** - 48 registered orgs

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/Fdbf8HKI2CJLyQf.png)

- **~3.2GNK deposited** into broker ledgers
- **~15M requests logged** in usage (~15M lifetime hits through the dual-gateway router)
- **~11.8B tokens served** (8.5 logged since migration) across MiniMax, Kimi, GLM, Qwen (usage window since early July; launch load test already pushed past **1B tokens in ~1 hour**)
- Peak observed throughput around **~100 req/s** (busiest minutes ~5.7k req/min; busiest day ~1.06M requests)
- **DevShards v3 live** on both production gateways - image `mainnet-v0.2.13-v3-post1`, route prefix `/devshard/v3`, 50/50 sticky split behind the router. OpenBroker was already on the v1/v2 path at launch; we completed the network-mandated v3 cutover ahead of the v0.2.14 deadline so brokers do not fall off when classic `/v1/devshard` goes away
- Real brokers / relays already pointing parts or all traffic at OpenBroker (public org names): **gonkarelay.com**, **Gonka24.com**, **Gonka-API.org**, **gate.joingonka.ai**,**Vitarum, etc**, plus several private / internal accounts.

### Ops + product work after launch

- Moved production off the early Railway pilot (where we landed after Qupra DC issues in end of June) onto a **dedicated server**. Same public domains, more headroom under load
- Dual-gateway HA with live traffic drain/switch (used for the v3 migrate - one gateway at a time, verify, then the other)
- Broker dashboard: per-request usage, participant / redundancy attempt breakdown, cost reconciliation
- New broker APIs: `GET /v1/usage` and `GET /v1/usage/{id}` so integrators can pull request-level cost/token data without scraping the UI
- Hardening under real load (connection pooling to the gateway router, escrow rotation / capacity ops, model-aware capacity after governance model changes)

### Feedback thread (git discussions)

Thanks for the sharp measurements. Where we landed so far:

- **Billing / hung requests** - usage logging + `GET /v1/usage/{id}` so you can see whether a request settled, what tokens/cost we recorded, and the FinalCost snapshot when the gateway returns it
- **`/v1/models`** **/v1/models** **/v1/models** - still on the polish list (model ids are also in docs / 400 text); not blocking chat completions
- **~10s fixed overhead** - largely protocol / escrow path (block times), not OpenBroker markup. Dual gateways + v3 cutover keep us on the current network path; further shaving depends on protocol-side escrow UX
- **Large-prompt hang band** - treated as a gateway/host-path issue; we keep feeding failure modes back to core while brokers route production traffic through us

OpenBroker is also doing what the launch post promised: shake out new DevShard versions at production scale. v3 on our gateways was exactly that - migrate, smoke `/devshard/v3`, keep MiniMax brokers online through the cutover.

Links:

- Product: [https://openbroker.gonka.gg](https://openbroker.gonka.gg)
- API: [https://api.openbroker.gonka.gg/v1](https://api.openbroker.gonka.gg/v1)
- Register: [https://openbroker.gonka.gg/register](https://openbroker.gonka.gg/register)
- Stats: [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats)
- Launch post: [https://github.com/gonka-ai/gonka/discussions/1363](https://github.com/gonka-ai/gonka/discussions/1363)

***

## 2. Pulse

Pulse is the live media + sentiment dashboard for Gonka (see it as a backbone and a part of proposal item named MTD / Marketing Transparency Dashboard - we shipped essential part that does data gathering first). It pulls public Gonka coverage from X, Instagram, YouTube, and the web into one place, scores tone via Gonka LLMs (`proxy.gonka.gg`), and shows activity / reach / engagement next to GNK market data. Built so anyone can see what the ecosystem is saying without opening ten tabs.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/rj4gBndPAI6mlw5.png)

Live: [https://pulse.gonka.gg](https://pulse.gonka.gg)

### What shipped

- Full Pulse app on Railway (API + web + Postgres), collectors on a ~2h cadence
- Sources: X, Instagram, YouTube, curated web / press
- Dashboard: last-24h activity / reach / engagement charts, general sentiment gauge + 14-day tone chart, GNK market (Uniswap v3 + HEX OTC), market Fear & Greed, top creators, content feed, EN + RU ui translations
- Sentiment analysis runs on LLMs running in Gonka (same network we all are building for) - not a closed SaaS LLM
- Embedded on the gonka.gg homepage (sentiment, Fear & Greed, latest news, link out to Pulse)
- Public read API for stats / market / feed / news / creators so gonka.gg and others can reuse the data. Some dashboards are already ingesting it alongside basic network info.

### Numbers (as of Jul 18)

- **~2,600 posts indexed**
- **~11.9M total reach** and **~149K engagement** across indexed content
- Sentiment: **100% of indexed items analyzed** (latest daily reading in the mid-50s / Neutral)
- Last 24h snapshot (volatile): **~43 new posts**, **~784K reach gained**, **~4.5K engagement gained**



### Why this matters

Proposal #74 called out demand activation and making Gonka easier to follow for non-technical users. Pulse is a part of that "transparency layer" - a public pulse of coverage, tone, and creators, wired into gonka.gg and backed by Networks collective inference stack.

***

## 3. gonka.gg - bugs + product work

Explorer side of the proposal was "gonka.gg V2.0" - faster engine, better UI, mobile, accurate GPU/inference metrics. We are not done with that part of roadmap yet, but a lot of the painful day-to-day stuff is already fixed and several new surfaces shipped.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/rqIXpMRSJzuXQfe.png)

### QA bug smash (~240)

We ran a dedicated desktop + mobile QA pass with an external unbiased audit, and closed on the order of **~240 tracker bugs** (desktop tracker version into the 170s, mobile into the 60s - still an ongoing flow since we ship new features that are getting QA tested as well).

Rough shape of what that covered:

- Mobile layouts and basic UX reorganizations
- charts, maps, tooltips escaping the viewport on touch
- table, card alignments, repositionings, restructuring
- status badges, filters, i18n gaps
- reward / weight tooltips and incomplete-epoch edge cases
- block / tx / wallet polish
- Updated indexers (28k less load on the network)
- Devshards V3 flow alignment for inference data ingestion
- A lot of backend work to make page load time go down

Shipped across a long streak of QA PRs and multiple levels of sanity checks. Not glamorous, but this is the difference between "works for some people" and "works for 70% of 10k+ people a day on phones".

### Product / data updates on gonka.gg (since the vote)

**Inference after DevShards (v0.2.12+)**

- Built and run a dedicated `devshard-poller` that ingests off-chain session diffs into ClickHouse (the chain no longer emits per-inference txs the old way) and is properly aligned with V3 flow, and is optimized to not make heavy load for the network (overall produced load caused by data ingestion went down X27k).
- `/network/inference` (Inference tab) is driven from that pipeline - 24h stats, gateway traffic, timelines.
- Added **DevShards v3** support in the poller (v2 and v3 coexist on hosts during migration; we probe `/devshard/v3` and union live shard inventories so traffic does not silently drop when gateways switch).

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/SOejlg1EImWiYAz.png)

**Network analytics**

- **Model Weight Share** on `/network` - weight distribution across AI models per epoch, with an all-epochs view (Redis-cached so it stays fast).
- GPU / reward-per-weight chart polish for in-progress epochs.
- Live Devshard flow tightened to recent epochs so the UI stays honest under load.

**Token holders**

- Supply fetch fallbacks when LCD nodes flake.
- Prune stale holder rows so rankings do not keep wallets that dropped under the qualification threshold.

**Infra behind the explorer** (also see section 4)

- Proper Frontend serving with lowest ttfb possible, API with horizontal auto-scaling, archive ClickHouse + tx-scanner + devshard-poller on dedicated server.
- Continuous deploys for explorer fixes without taking the archive down.

Explorer: [https://gonka.gg](https://gonka.gg)  
Inference: [https://gonka.gg/network/inference](https://gonka.gg/network/inference)  
Network: [https://gonka.gg/network](https://gonka.gg/network)

### Why it matters

Faster deploys, less risk of a bugfix taking down indexing, room to run the heavier pre-compute work from the V2 explorer roadmap.

***

## 4. proxy.gonka.gg - B2B inference + public status

[proxy.gonka.gg](https://proxy.gonka.gg) is our OpenAI-compatible inference proxy on top of Gonka DevShards - API keys, balances, usage, docs, chat playground. Public API at [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1). Pulse (and other Gonka Labs apps) call the same stack for LLM work, so when we harden the proxy we harden half the product surface too.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/2SJccZe5re5SE93.png)

### Numbers (as of Jul 18)

Measured window below is **since the Jul 4 dedicated-server migrate** (usage DB moved with the stack - earlier Railway and even earlier Qupra DC history is not in this series). The product itself was already live before Proposal #74.

- **~29.0B tokens** served (~5.2M requests, ~96.8% OK)
- **~23.6B tokens in the last 7 days** (~3.5M requests)
- **~7.3B tokens in the last 24 hours** (~1.1M requests)
- Peak recent days ~**4.8-5.0B tokens / day**; peak hour observed ~**823M tokens** in a single hour (~270k requests)
- Model mix (token share): **MiniMax-M2.7 ~25.6B**, **Kimi-K2.6 ~3.4B**, plus residual Qwen / other
- Accounts: +10-30 new accounts daily.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/hzZ0XERXO0tSDDp.png)

### What shipped since the vote

- **Dedicated production box** for the API (`api.proxy.gonka.gg`) - moved off the flaky VPS / and too unreliable Railway path onto a tuned server with local Postgres, own DevShard gateway, Proxy edge for the API. Frontend stays on other host at `proxy.gonka.gg` with rewrites into the API.
- **Own DevShard gateway ops** - escrow rotation, capacity-aware concurrency limits, admin tooling. Gateway now on **DevShards v3** (`mainnet-v0.2.13-v3-post1`, route `/devshard/v3`) ahead of the network v0.2.14 deadline - blue/green cutover with a temp gateway + drain so in-flight MiniMax traffic survived the switch. Currently **32+32 (64 inflight escrows) active v3 escrows** (MiniMax + Kimi)
- **Public status / analytics page** at [https://proxy.gonka.gg/status](https://proxy.gonka.gg/status) - aggregate capacity %, load, in-flight vs cap, active shards, network participant counts, error-rate history + reason breakdown. Deliberately no escrow ids / host IPs (safe to share with customers)
- **Usage honesty** - requested-vs-served model on usage logs when fallback fires, so dashboards show what the client asked for and what actually ran
- Product surface kept current for B2B: models page, docs, partner paths, top-up flows, password reset, etc. (dashboard UX work continued alongside the infra move)

### Why it matters

Proposal #74 called out proxy.gonka.gg as the B2B / analytics lane. This stretch was less "new landing page" and more "make the pipe carry real load": multi-billion token days, a public status surface customers can trust, and staying on the current DevShard protocol so keys do not die when classic `/v1/devshard` goes away. Same gateway lessons feed OpenBroker - one network path. More "b2b" work ahead.

Links:

- Product: [https://proxy.gonka.gg](https://proxy.gonka.gg)
- API: [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1)
- Status: [https://proxy.gonka.gg/status](https://proxy.gonka.gg/status)

***

We are still heads-down on the rest of the Proposal #74 checklist - hardening infra under real load, polishing what already shipped, and building the next products on the list. More updates as they land. Stay tuned.

***

## Links

- Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)
- Explorer: [https://gonka.gg](https://gonka.gg)
- OpenBroker: [https://openbroker.gonka.gg](https://openbroker.gonka.gg)
- Pulse: [https://pulse.gonka.gg](https://pulse.gonka.gg)
- Proxy: [https://proxy.gonka.gg](https://proxy.gonka.gg)
- RPC: [https://rpc.gonka.gg](https://rpc.gonka.gg)
- GitHub: [https://github.com/gonkalabs](https://github.com/gonkalabs)
- OpenBroker launch: [https://github.com/gonka-ai/gonka/discussions/1363](https://github.com/gonka-ai/gonka/discussions/1363)

Feedback welcome in the thread - what should we prioritize next month from the proposal list?
