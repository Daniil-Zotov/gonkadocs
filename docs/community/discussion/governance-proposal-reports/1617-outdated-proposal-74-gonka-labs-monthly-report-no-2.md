---
title: "#1617 — (outdated) Proposal #74: Gonka Labs - Monthly Report No. 2"
source: https://github.com/gonka-ai/gonka/discussions/1617
discussion_number: 1617
category: governance-proposal-reports
synced_at: 2026-09-04T16:15:45Z
---

> 🔄 **Auto-sync:** from [Discussion #1617](https://github.com/gonka-ai/gonka/discussions/1617) every hour. 

# (outdated) Proposal #74: Gonka Labs - Monthly Report No. 2

**Автор:** [@nsvdev](https://github.com/nsvdev) · **Категория:** :bookmark_tabs: Governance Proposal Reports · **Создано:** 2026-08-20 15:36 UTC · **Обновлено:** 2026-08-20 15:45 UTC

---

## 📝 Описание


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6267b894-26b8-47a1-a34e-97ff83dca34b" />

Hey! Gonka Labs here. Last update was [Monthly Report No.1](https://github.com/gonka-ai/gonka/discussions/1477) on Jul 18. 

Report #1 was the launch month: OpenBroker and Pulse went live, the explorer got a big QA + inference pass, and proxy.gonka.gg moved onto dedicated infra under real load. This month is what we added on top. New transparency dashboard, a real agent workspace on the proxy, a third model on our own DevShards, and the ops that show up when hosts leave mid-epoch or a disk fills up.

**Short version** of what landed since Jul 18:

- **proxy.gonka.gg**: Workspaces live (Chat / Docs / Slides / Sheets), MCP + file parsing, DeepSeek next to MiniMax + Kimi
- **PTD**: new product, live (proposal transparency: claim, updates, Core reports)
- **gonka.gg**: holders bubble map + charts, inference tab honesty, live map arcs back, full Chinese, phone pass
- **OpenBroker**: DeepSeek on both gateways, escrow auto-top-up, broker UX + billing under real relay load
- **Pulse**: Reddit + TikTok, Telegram community pulse, reach honesty, more press
- **rpc.gonka.gg**: public gRPC, live gateway on a new host, archive move, Feather recovery without dropping wallets
- **G-Meter**: stayed up through cutovers, DeepSeek + OpenBroker in the probe lineup

---

## 1. proxy.gonka.gg. Workspaces + third model + agent compat

proxy.gonka.gg is our OpenAI-compatible inference proxy on top of Gonka DevShards. API keys, balances, usage, docs, chat. Public API at [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1). Report #1 was the dedicated-box migrate, public `/status`, and DevShards v3. This month we put a real product on that pipe, and we made agents plus a third model work at the same scale.

**Short version**

- **Proxy Workspaces** live (Chat / Docs / Slides / Sheets, shareable)
- MCP + file parsing in chat (attachments free inside Workspaces)
- DeepSeek added next to MiniMax + Kimi (32 healthy escrows each)
- Agent / tool-call compat: `$ref`/`$defs`, empty `tool_call.id`, MiniMax content shape, leftover client knobs
- Public `/status` now shows mid-epoch confirmation PoC, so a capacity dip is not mistaken for an outage
- Fallback ladder + BYOK OpenRouter as last resort

**Numbers (since Jul 18)**

- 60B+ tokens
- Registered Accounts: +3,5k since Jul 18

**What shipped**

Workspaces are not just a playground chat. The agent writes docs, slides, sheets, and code in one session on Gonka inference. Pick a surface at [https://proxy.gonka.gg/workspaces](https://proxy.gonka.gg/workspaces) and share the finished space.

<img width="1345" height="993" alt="Screenshot 2026-08-18 at 11 09 10 PM" src="https://github.com/user-attachments/assets/3789be7c-f263-4825-a379-a3fcaacbebc0" />


In `/chat` you can connect any MCP (search, external services, your own connectors). The agent calls them in-dialog. Attach images, PDF, text, HTML, XML, CSV, XLSX, etc. 


<img width="1335" height="1011" alt="Screenshot 2026-08-18 at 11 10 51 PM" src="https://github.com/user-attachments/assets/6f67f7df-c71f-40e3-a34e-2c0e8b1f108e" />

<img width="1338" height="832" alt="Screenshot 2026-08-18 at 11 13 11 PM" src="https://github.com/user-attachments/assets/9b04a7a2-ffca-4459-a08c-e577a84dfcf7" />

The Proxy parses files sent by user (images, pdf, xlsxs, etc) and sends the model the meaning (if user enables "File Ingestion" option in the Account settings). Attachments in Workspaces stay **free**.

On our own DevShards: DeepSeek as the third model, same 32-escrow target as MiniMax and Kimi. Escrow refill-to-target (settlement stays off). Empty-escrow 502s are no longer the failure mode. `/status` shows network confirmation PoC when hosts leave inference mid-epoch. That is a rate limit, not a Proxy outage.

Compat, because Cline / agents suddenly 400'd: Gonka hosts tightened tool-schema validation. We kept the old repairs and added request rewrites so clients still work. Inline `$ref` / `$defs` on tools and `response_format.json_schema`. Fill empty `tool_calls[].id` (and matching tool results). MiniMax content becomes `[{name,type,text}]` on every role. `reasoning_effort: max` becomes `high`. We drop `extraBody` / `json_mode` / `output_config` / `fallback` before upstream.

**Why it matters**

Proposal #74 listed proxy.gonka.gg as the B2B / analytics lane. Report #1 made the pipe carry real load. This month is the product on that pipe: a shareable workspace, agents that do not 400 on strict hosts, and a third model with enough escrow that a mid-epoch host exit looks like a rate limit, not an outage. Same gateway lessons still feed OpenBroker.

Links: [Product](https://proxy.gonka.gg) · [API](https://api.proxy.gonka.gg/v1) · [Status](https://proxy.gonka.gg/status) · [Workspaces](https://proxy.gonka.gg/workspaces)

---

## 2. PTD. Proposal Transparency Dashboard

Report #1 shipped Pulse as the first slice of the proposal's transparency item (then called MTD). PTD itself was built this window and launched in August.

<img width="1339" height="1002" alt="Screenshot 2026-08-18 at 11 15 01 PM" src="https://github.com/user-attachments/assets/ab420652-0acf-47d2-94d9-e09da8f40e0b" />


**Quick recap:** every passed on-chain proposal is listed automatically. A team can claim a page (contact required, moderator review) and then post tasks, rich updates, and discussion. Core-team GitHub category reports are ingested automatically and show for claimed and unclaimed proposals. No login to read.

Live: [https://ptd.gonka.gg](https://ptd.gonka.gg)

**What shipped**

Product built late July (email + GG Wallet auth, proposal cache from rpc.gonka.gg, claim / tasks / append-only updates / discussion). [https://ptd.gonka.gg](https://ptd.gonka.gg) went live with TLS on Jul 31.

Early August we reworked on-chain tasks on the claim form, put the full proposal text on the initiative page (claimant can edit it), and sent claims through a moderation queue. Images work in the rich editor.

Aug 6: ingest from Core's [Governance Proposal Reports](https://github.com/gonka-ai/gonka/discussions/categories/governance-proposal-reports) (`Proposal #<n>: …` threads). Public `/reports/[id]`. No auth, no claim wall. Home shows the latest 5 reports (preview image + excerpt) plus an all-reports grid.

Aug 13: OG title / description / image so Telegram (and others) get a proper card when someone shares ptd.gonka.gg or a report link.

**Why it matters**

Proposal #74 asked for a transparency layer so people can see what funded work is actually doing. Pulse was the media slice. PTD is the governance one: initiative pages and the reports we (and others) post on GitHub, readable without a login.

Links: [PTD](https://ptd.gonka.gg) · [Reports](https://ptd.gonka.gg/reports) · [GitHub source](https://github.com/gonka-ai/gonka/discussions/categories/governance-proposal-reports)

---

## 3. gonka.gg. Explorer + inference + holders

Report #1 already had the inference tab, Model Weight Share, GPU / reward charts, and the holders page, plus the ~240 QA smash. This month is what we added or fixed on top of that.

**Short version**

- New on holders: bubble map, holders chart, new/active account timeseries
- Inference tab: Confirmed/All, 24h per-model tokens; public DevShard aggregates API
- Inference map broke; we put live arcs back and made multi-broker traffic fair
- Numbers that were lying got fixed (participant cap, ghost ML nodes, model-weight formula, dust "new accounts")
- Full Chinese; phone pass on homepage / header / inference / GPUs
- Ongoing QA (proposal votes, reward calculator, wallets, copy, etc.)

**What shipped**

Public DevShard aggregates on the API so partners do not scrape the UI. New broker added in the gateway panel. Live Devshard Flow "participants" was capped at 12. Uncapped it. Readable tx type labels, copy toasts, epoch countdown tooltip in the header. MCAP / FDV on the ticker. Supply + accounts rows put back in the price tooltip. AI assistant reliability / live-data pass (assistant was already there).

<img width="1333" height="905" alt="Screenshot 2026-08-18 at 11 21 14 PM" src="https://github.com/user-attachments/assets/74812023-cc14-4690-af76-216911df7384" />

Chinese localization finished across the explorer. Wallet page: account details + transaction summary.

Holders: account bubble map, new/active activity charts, holders chart. Account totals made cumulative (dust transfers still count in the total). 

<img width="1297" height="442" alt="Screenshot 2026-08-18 at 11 23 24 PM" src="https://github.com/user-attachments/assets/769cf727-1fa8-463e-8b42-5cc48728fe4a" />


Honesty fixes elsewhere: escrow inference duplicates (diff nonce vs id), stale ghost ML nodes no longer inflate GPU counts, reward calculator showing 0% GPU weight coverage, proposal detail voter count (QA: proposal 95, "3 vs 12"). Inference tab: Confirmed/All on 24h gateway traffic; 24h model tokens table. Model Weight Share recounts hosted PoC, not confirmation weight (the chart was already in report #1).

Phone: homepage blocks, header, blocks/rewards widget. GPU page on phone defaults to top-4 + a latest-epoch mix instead of 12 overlapping lines. Inference tab no longer overflows the viewport on a phone. 

**Why it matters**

Explorer side of the proposal was gonka.gg V2.0: faster engine, better UI, mobile, accurate GPU/inference metrics. Report #1 closed the painful day-to-day bugs. This is the next layer of that.

Links: [Explorer](https://gonka.gg) · [Inference](https://gonka.gg/network/inference) · [GPUs](https://gonka.gg/network/gpus) · [Holders](https://gonka.gg/network/token-holders) · [Inference map](https://gonka.gg/network/inference-map)

---

## 4. OpenBroker

We already announced the launch in [discussion #1363](https://github.com/gonka-ai/gonka/discussions/1363) and covered it in Report #1: dedicated box, dual-gateway router, DevShards v3, `obk-*` keys, GNK ledger billing, `GET /v1/usage` / `{id}`, public stats. This month is capacity + ops + broker UX under real relay load.

**Quick recap:** OpenBroker is managed DevShards-as-a-service. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at [https://api.openbroker.gonka.gg/v1](https://api.openbroker.gonka.gg/v1) (UI at [https://openbroker.gonka.gg](https://openbroker.gonka.gg)). GNK billing with no markup. Public stats at [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats).

<img width="1173" height="749" alt="Screenshot 2026-08-18 at 11 26 42 PM" src="https://github.com/user-attachments/assets/883c4e31-bccc-4b61-ad4c-f59ea0b064c5" />


**Numbers (since Jul 18)**

- 50B+ tokens
- Brokers: 70 registered (was 48 on Jul 18) · +23 new Brokers since Jul 18
- Active broker ledgers: ~6.3k GNK on deposit

**What shipped**

Third model: DeepSeek-V4-Flash-0731 minted on both production gateways (live Aug 14). Docs / status / canonicalize updated.

Escrow maintainer now refills MiniMax / Kimi / DeepSeek to per-model targets on v2 + v2b independently. We tightened hard opens/run + opens/day caps and added a min operator-wallet floor.

DeepSeek clients get `reasoning` + `reasoning_content` (alias so contract clients see thinking fields).

Deposit dashboard now says the address is custodial, not personal wallet, with explicit steps. Password-reset feature added.

Ongoing: keep MiniMax / Kimi / DeepSeek escrow pools topped for dual-GW HA. proxy.gonka.gg Secondary / joingonka fallback accounts keep using OpenBroker as their overflow path. Common sense.

**Why it matters**

OpenBroker is still doing what the launch post promised: shake out new DevShard versions and models at production scale. DeepSeek on both gateways, refill-to-target, honest billing when final-cost is missing, plus deposit / reset UX so brokers can actually get back in when something breaks.

Links: [Product](https://openbroker.gonka.gg) · [API](https://api.openbroker.gonka.gg/v1) · [Stats](https://openbroker.gonka.gg/stats) · [Launch post](https://github.com/gonka-ai/gonka/discussions/1363)

---

## 5. Pulse

Report #1 launched Pulse with X / Instagram / YouTube / web, 24h charts, sentiment on Gonka LLMs, and the public read API. This month is more sources, cleaner signal, and a couple of community surfaces.

Live: [https://pulse.gonka.gg](https://pulse.gonka.gg)

<img width="1156" height="756" alt="Screenshot 2026-08-18 at 11 31 05 PM" src="https://github.com/user-attachments/assets/193acd3f-20a6-49dd-866c-1715992266df" />


**Numbers (as of Aug 18)**

-  3k+ posts indexed
- 11.4M+ total reach · 129K+ engagement
- Sentiment: 100% analyzed (latest reading ~65)
- Sources now: X · YouTube · Instagram · website · TikTok · Reddit (+ Telegram insights separately)

**What shipped**

Reddit + TikTok collectors. Noise / Top Creators filters so homonyms do not pollute the feed. Off-topic X "gonka" homonym filter and UTF-16 emoji sanitization in ingest. TikTok Top Creators noise filter so junk accounts do not dominate the board.

Telegram community pulse bot + discourse "talking about" digest (EN + RU), with sentiment chips / topic bars on the community panel.

More web / press: curated sources, Medium RSS, original-article discovery. Mobile + feed QA, creator profile links, GNK price archive fallbacks.

**Why it matters**

Proposal #74 asked for demand activation and making Gonka easier to follow. Pulse is still that layer. Two more public sources, a Telegram surface if you do not live on the dashboard, and reach numbers that do not jump when Instagram resets a counter.

Links: [Pulse](https://pulse.gonka.gg) · API: [https://api-production-960a.up.railway.app/api](https://api-production-960a.up.railway.app/api) (stats / feed / news / creators / telegram / discourse)

---

## 6. [rpc.gonka.gg](https://rpc.gonka.gg)

Public RPC / LCD gateway. Report #1 mentioned it in the footer. The free / no-key pool, Hyperfusion + 6block, JSON-RPC failover, CosmWasm limits, and IP scrubbing shipped in June, before that report. This month is gRPC, a live-host cutover, and not hanging wallets when a Feather falls off tip.

**Short version**

- gRPC now on `rpc.gonka.gg:9090` (TLS)
- Live gateway moved to a new host. API keys + users intact, Keplr / GG wallets kept working
- Archive ClickHouse + tx index pointed at the new indexer box
- Drained / restored Feather nodes when they fell off tip, then decommissioned some RPC nodes from the pool without dropping the public RPC
- Public `/health` no longer hangs if one sub-service is dead
- Full mobile UI shipped

**What shipped**

Mobile: full mobile layout shipped.

Some RPC nodes in the pool lagged in late July. We drained the lagging nodes from the community pool, rerouted traffic, then brought them back in when they caught up.

Cosmos gRPC is forwarded on `rpc.gonka.gg:9090` (TLS at the edge, our Feather nodes behind it). Weight / drain when a Feather is in recovery after an upgrade.

Live gateway cut over to a new box. Moved to better servers. ClickHouse + tx scanner follow the archive host. One Feather decommissioned. Pool still serves as it was, just faster and more stable. Health probes are time-bounded so a dead scanner cannot freeze `/health` or the homepage "Powered by" strip.

**Why it matters**

Wallets and the explorer only look healthy if the public RPC stays on tip. This stretch was: move the box, add gRPC, do not take Keplr down while we do it. So we did.

Links: [Gateway](https://rpc.gonka.gg) · [Docs](https://rpc.gonka.gg/endpoints) · [Health](https://rpc.gonka.gg/health) · gRPC: `rpc.gonka.gg:9090` · [Access](https://rpc.gonka.gg/access) (optional)

---

## 7. G-Meter

This month is ops hardening + QA + DeepSeek / OpenBroker / AI status.

<img width="1282" height="987" alt="Screenshot 2026-08-18 at 11 33 29 PM" src="https://github.com/user-attachments/assets/a7db343b-6ac1-430e-8dc2-a8ae85bc5440" />


Live: [https://meter.gonka.gg](https://meter.gonka.gg)

**What shipped**

`/compare` linked in the top nav. Explained aggregate "failed tests %" vs latest-run broker list (history includes older underpayment failures).

Front QA: Limits / Providers / pricing UI; live `/v1/models` prices, shared price-scale domain, CIS language on compare. Mobile probe-log + providers layout.

DeepSeek-V4-Flash-0731 added to the active probe lineup (catalog / probes / brokers). Trends filter dedupe. Dropped DeepSeek probes on brokers that do not list it (Hyperfusion / Gonkarouter).

OpenBroker (`api.openbroker.gonka.gg`) added as **OpenBroker by Gonka Labs**. DeepSeek via `proxy.gonka.gg` writes cached network + broker AI summaries (refresh after probes). At a glance opens the broker note from a message-icon modal, with plain-language notes like "billing unavailable".

**Why it matters**

G-Meter is how anyone can see whether a broker is actually serving, at what price, without trusting a landing page. Adding DeepSeek and our own OpenBroker to that lineup, and not dying during a host cutover, is the point of the page.

Links: [Dashboard](https://meter.gonka.gg) · [Compare](https://meter.gonka.gg/compare) · [Get started](https://meter.gonka.gg/compare/start)

---

Still working to make Gonka Labs products better while creating new onsed. Hardening infra under real load, polishing what already shipped, building the next products on the list. More updates as they land.

**Links**

- Last report: [Monthly Report No.1](https://github.com/gonka-ai/gonka/discussions/1477)
- Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)
- Explorer: [https://gonka.gg](https://gonka.gg)
- OpenBroker: [https://openbroker.gonka.gg](https://openbroker.gonka.gg)
- Pulse: [https://pulse.gonka.gg](https://pulse.gonka.gg)
- Proxy: [https://proxy.gonka.gg](https://proxy.gonka.gg)
- PTD: [https://ptd.gonka.gg](https://ptd.gonka.gg)
- RPC: [https://rpc.gonka.gg](https://rpc.gonka.gg)
- G-Meter: [https://meter.gonka.gg](https://meter.gonka.gg)
- GitHub: [https://github.com/gonkalabs](https://github.com/gonkalabs)

Feedback welcome in the thread,
Gonka Labs team.

