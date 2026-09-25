---
title: "#1815 — Proposal #74: Gonka Labs - Monthly Report No.3"
source: https://github.com/gonka-ai/gonka/discussions/1815
discussion_number: 1815
category: governance-proposal-reports
synced_at: 2026-09-25T22:13:37Z
---

> 🔄 **Auto-sync:** from [Discussion #1815](https://github.com/gonka-ai/gonka/discussions/1815) every hour. 

# Proposal #74: Gonka Labs - Monthly Report No.3

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :bookmark_tabs: Governance Proposal Reports · **Создано:** 2026-09-19 09:57 UTC · **Обновлено:** 2026-09-19 12:36 UTC

---

## 📝 Описание

# Proposal #74: Gonka Labs - Monthly Report No.3

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/612d6724-aa9f-4868-aaac-b10b6cdfbe88" />

Hey! Gonka Labs here.

Last updates: [Report No.1](https://github.com/gonka-ai/gonka/discussions/1477) (Jul 18) and [Report No.2](https://github.com/gonka-ai/gonka/discussions/1612) (Aug 18).

On June 12 the community passed [Proposal #74](https://gonka.gg/network/proposals/74) ([full text](https://gonkalabs.com/proposal)). That vote funded six months of infra, ops, and product work. This report is **month 3 of 6** - about halfway through the window we raised for.

Report #1 was launches (OpenBroker, Pulse) plus the explorer QA / inference pass and the proxy box move. Report #2 was Workspaces, PTD, holders / inference honesty, DeepSeek, rpc gRPC. This one is what landed since Aug 18.

Short version since Aug 18:

- **300.000.000.000 (300B) tokens** processed by Proxy and OpenBroker in a month.
- **gonka.gg** - homepage AI Tokens widget, participants show this epoch's nodes, proposals list/detail + Featured widget actually renders, wallet heatmap opens the day's txs, IBC holder channels, `/snap`, tx share cards
- **proxy.gonka.gg** - GLM on the pipe, v4.1 path, persist-through-rate-limits, OAuth login, file ingest now $0, 171B+ tokens in a month
- **OpenBroker** - DevShards v4.1, GLM live, public `/status`, cabinet escrow line, 129B+ tokens in a month
- **Pulse** - chart units, sentiment faces (not Fear & Greed), news mix, catch-up without a fake 24h spike. 4.3k posts / 28.4M reach as of Sep 19
- **rpc.gonka.gg** - wallet JSON-RPC failover (one 503 no longer blanks GG Wallet / Keplr balances), honest health checks, second phone pass on the site
- **PTD** - Report #2 hosted on PTD itself, a proposal page lists every report (not only the latest), markdown + screenshots actually render
- **G-Meter** - eterial.ai in the probe set, GLM-5.3 Flash as the new active model, compare uses the cheapest Gonka rate (not the average)
- **Gonka Chat** - new product, live. Wallet-to-wallet mailbox (GG Wallet / Keplr). DMs, groups, channels, invites / replies / mentions. Message button + unread badge on gonka.gg wallet pages
- **x402** - new product, live. Public facilitator at x402.gonka.gg. Agents / apps pay an HTTP route in GNK or bridged USDC. No accounts, no API keys. Source on GitHub.

***

## 1. gonka.gg

Explorer side of the proposal is still "V2.0": faster, honest numbers, usable on a phone. Report #1 closed the big QA pile and stood up inference after DevShards. Report #2 added holders charts / bubble map, Confirmed/All on the inference tab, Chinese, a phone pass.

This month is smaller surfaces that people actually click, plus a few numbers that were still lying.

### Homepage - AI Tokens

The four growth cards on the home page include **AI Tokens**. Click it: chart modal, Confirmed / All, 10 / 30 / 90 days / All, jump to the Inference page.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/yZPbypW22kuayS6.png)

Same rules as `/network/inference` (and the same ClickHouse feed the poller writes):

- **Confirmed** (default) - billed tokens after finish: actual in + actual out
- **All** - Confirmed plus claimed prompt size on Gonka Labs requests that are accepted but not finished yet
- We do not pour other brokers' unfinished claimed / STARTED / heartbeat probes into All. That pile is synthetic and would smear gateway shares (same reason Dahl drops synthetics before counting tokens)

Widget number is the last 24 hours. Chart is UTC days; last point is that same 24h number so hover matches the card. Y-axis is compact (`7.5B`, not `7,500,000,000` clipped off the left).

### Participants

Expand a row on `/network/participants` (All / current epoch). You get **this epoch's** ML nodes, not last epoch's confirmation list. Hosts that added a node after confirmation were missing it in the table. Weight on the list follows the live epoch the same way.

### Proposals

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/iTnPBSIM0YYEOmQ.png)

- Featured Proposals on the homepage was not rendering. It does now.
- `/network/proposals` list + detail restyle (chips, vote strip). Titles wrap on a phone instead of getting cut.
- Prevote tab dropped from this surface.
- Finished proposals stay put (no live-tally flicker after the vote ended).

### Wallets / holders / calculator

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/HXf8J7q6F7TFmXp.png)

- Wallet activity heatmap: click a day, see that day's transactions (not only a hover count).
- Holders: IBC balances by channel on hover; IBC grouping so one wallet is not split into junk rows.
- Reward calculator: minus amounts display correctly; HEX sell price on the USD hint.

### Other

- Gateway Traffic tooltip on the inference tab rewritten for the public page (no internal notes).
- [gonka.gg/snap](https://gonka.gg/snap) - landing for the GG Wallet MetaMask snap.
- Share a tx link and the card now has a short summary (not a blank title). Example: [0634bfaf…](https://gonka.gg/transactions/0634bfaf4017b65ed327084c5e81c15b572ed16da33a63657713277d13809d23)

Links: [Explorer](https://gonka.gg) · [Inference](https://gonka.gg/network/inference) · [Participants](https://gonka.gg/network/participants) · [Proposals](https://gonka.gg/network/proposals) · [Holders](https://gonka.gg/network/holders)

***

## 2. proxy.gonka.gg

Report #1 was the dedicated-box migrate, public `/status`, DevShards v3. Report #2 was Workspaces, MCP in chat, DeepSeek, and the agent/tool-schema repairs. This month is the next protocol step, a fourth model, a status page you can send to a customer without lying, and a couple of settings that stop common client 400s / 429s.

Quick recap: OpenAI-compatible proxy on Gonka DevShards. Keys, balances, usage, Workspaces. Public API at https://api.proxy.gonka.gg/v1. UI at https://proxy.gonka.gg. Status at https://proxy.gonka.gg/status.

Numbers (since Aug 18 / as of Sep 18):

- **171B tokens** in a month
- Peak day **~10.2B tokens**
- +2k users

What shipped

Serving path moved onto **DevShards v4.1**. Same public URL. Keys did not have to rotate. Same job as the v3 cutover in report #1: stay on the protocol the network actually runs.

**GLM-5.3-Flash** came on (`zai-org/GLM-5.3-Flash`). Docs, `/status`, and the models page list it. Public `/v1/models` still only lists a model when the live pool can take it, so a quiet GLM hour can drop the id off that list. That is pool state, not a delist.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/783uFSTWxHqRYc7.png)

Public **[status](https://proxy.gonka.gg/status)** got an honesty pass: incoming vs served, host 429s vs our own errors, in-flight vs cap, confirmation PoC when hosts leave inference mid-epoch. Incoming is a thin line so an over-capacity band does not paint the whole chart red. Kimi is off that page - it still accepts `tools` and then returns no `tool_calls`, which is a capability miss, not a Proxy outage.

We raised concurrency caps on the live gateway. DeepSeek was sitting on our own in-flight ceiling, not on empty network weight. After the bump, the concurrent-429 pile mostly went away. Caps help until you push past what hosts will take.

**Persist through rate limits** is a Settings toggle (off by default). Hosts still return `too many concurrent requests (24/24)` when every slot is full. With the toggle on, the proxy keeps that request open and retries under the hood for up to two minutes. You should almost always get a response; it may just take longer. API and Chat.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/5Qy1e9PT3JxOt1Q.png)

**DeepSeek reasoning compatibility** (off by default): official `reasoning_effort` / `thinking: {type: enabled}` get mapped onto what the hosts actually honor, so `reasoning_content` comes back instead of leaking into `content` and breaking tool harnesses.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/U9mRpRzgBSHkYUY.png)

**MCP on the API**, not only in Chat. Opt-in in Settings. `/v1/chat/completions` can list and run remote HTTPS MCP tools and return the final answer. Local npx/stdio stays in the client.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/FODU8wUCEQhBjHp.png)

**Login with proxy.gonka.gg** shipped: OAuth 2.0 Authorization Code + PKCE, consent screen, scopes `profile` / `usage` / `api_key`. Client registration is manual. We mint a fresh revocable key for that connection; we never hand out an existing user key. Docs: https://proxy.gonka.gg/docs#login. Settings has a Connected Apps row so you can revoke it.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/hQR4pLG3bBDbU2K.png)

Also this window: public [models](https://proxy.gonka.gg/models) page (context, tools, reasoning, live rates), shareable Workspace URLs.

**File ingest** is free now - no separate attachment line. Docs (`md` / `txt` / `csv` / `html` / `pdf` / `docx` / `xlsx` / `odt` / `ods`) are $0. Images are $0 inside the account caps (5 files per request, 20/min, 200/day). Settings → File ingestion has the toggle and the remaining quota. MCP in chat and web search (chat + API) stay $0. Inference is still the network rate.

Links: [Product](https://proxy.gonka.gg) · [API](https://api.proxy.gonka.gg/v1) · [Status](https://proxy.gonka.gg/status) · [Models](https://proxy.gonka.gg/models) · [Workspaces](https://proxy.gonka.gg/workspaces) · [Docs](https://proxy.gonka.gg/docs)

***

## 3. OpenBroker

Launch was [discussion #1363](https://github.com/gonka-ai/gonka/discussions/1363) and Report #1. Report #2 already had DeepSeek on both gateways, refill-to-target, deposit copy, and password reset. This month is the next protocol step, a new model, and a public status page brokers can actually send to customers.

Quick recap: OpenBroker is managed DevShards-as-a-service. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at https://api.openbroker.gonka.gg/v1 (UI at https://openbroker.gonka.gg). GNK billing with no markup. Public stats at https://openbroker.gonka.gg/stats.

https://openbroker.gonka.gg · https://api.openbroker.gonka.gg/v1 · https://openbroker.gonka.gg/stats · https://openbroker.gonka.gg/status

Numbers (as of Sep 18):

- **~129B tokens** and **~32M requests** in a month
- Peak day **~7.1B tokens** (Sep 12)
- Last 7 days: **~30B tokens** / **~8.9M requests**
- Last 24h: **~2.7B tokens** / **~1.0M requests**
- Mix in that window: DeepSeek ~95B, MiniMax ~26B, Kimi ~3.3B, GLM ~1.9B (GLM only came on late)
- Brokers: **142 registered** (was 70 on Aug 18) - **+74 signups** since report #2. **77 active** ledgers, 65 still pending first deposit
- Live pools: **40 MiniMax / 40 DeepSeek / 24 GLM** shards on the current path

What shipped

Serving path moved onto official **DevShards v4.1** (`/devshard/v4.1`). Same public URL. Brokers did not have to rotate keys. That is the same job as the v3 cutover in report #1: stay on the protocol the network actually runs.

**GLM-5.3-Flash** is live (`zai-org/GLM-5.3-Flash`). Docs, `/v1/models`, maintainer targets, and the status page all list it. Public lineup right now is MiniMax, DeepSeek, and GLM.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/uu9qd4emckLCylU.png)

Public **[status](https://openbroker.gonka.gg/status)** shipped: incoming vs served, error rate by model, reason breakdown, in-flight vs cap, shard counts. No host IPs, no escrow ids. Incoming is drawn as a thin gray line so an over-capacity band does not look like the whole chart is on fire. When the network is in confirmation PoC, capacity drops on the same page - that is hosts leaving inference, not OpenBroker going dark.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/577qASONeR7yUfo.png)

We raised concurrency and token caps on the live gateway, and lifted escrow targets (DeepSeek 22 to 40, GLM 12 to 24, MiniMax stays 40). DeepSeek was sitting on our own in-flight ceiling, not on empty network weight. Caps help until you push past what hosts will take - the gateway scales itself down if you get greedy, so we stopped there.

Register: you cannot jump to the OTP step with a password under 8 characters. The API already rejected it; the form was sending the email anyway.

Cabinet got a desktop / phone pass. Billing now shows the network cost of opening new escrows we raise for traffic, plus leftover lock only on shards we cannot settle back on-chain. If an escrow settles, the remainder is not billed - that line is **Epoch escrow**, split by your share of successful tokens that epoch. Inference is still no markup; the cabinet just stopped hiding those network fees. Updates also go to [t.me/openbroker_gg](https://t.me/openbroker_gg). Docs: [https://openbroker.gonka.gg/docs](https://openbroker.gonka.gg/docs).

Still the same promise as the launch post: run new DevShard versions and new models at production scale so relays do not find the bugs first.

Links: [Product](https://openbroker.gonka.gg) · [API](https://api.openbroker.gonka.gg/v1) · [Stats](https://openbroker.gonka.gg/stats) · [Status](https://openbroker.gonka.gg/status) · [Docs](https://openbroker.gonka.gg/docs) · [Register](https://openbroker.gonka.gg/register) · [Launch](https://github.com/gonka-ai/gonka/discussions/1363)

***

## 4. Pulse

Report #1 launched it (X / Instagram / YouTube / web + sentiment on Gonka LLMs). Report #2 added Reddit, TikTok, Telegram, and the "What people are saying" digest. This month is less new sources and more "can you read the board without guessing."

Live: https://pulse.gonka.gg

Numbers (as of Sep 19):

- **4,348 posts** indexed (was 3k+ on Aug 18)
- **28.4M** total reach · **232K** engagement (was 11.4M / 129K)
- Sentiment: still 100% analyzed. Latest reading **75** (was ~65)
- Last 24h (volatile): 22 posts, ~491K reach, 414 engagement
- Sources same as #2: X · YouTube · Instagram · web · TikTok · Reddit, plus Telegram / discourse on the side

What shipped

The big chart numbers used to be bare digits. People had to guess if 13.2K was views or posts. Activity / reach / engagement now say **posts**, **views**, **engagements**. Sentiment chart says **index**.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/3cd5eeE8p7Mq68H.png)

General sentiment gauge got sad / happy faces on the ends so it does not look like the market Fear & Greed widget sitting next to it. Dropped the "N items analyzed" line under the gauge - it was just repeating the hero count.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/rohKk6JKVZMnyl3.png)

**In the news:** one publisher's weekly digest was eating the list. We still keep a couple of those posts. The rest of the slots go to other outlets (Product Science, Coin Edition, BlockchainReporter, etc.).

Founder / investor X timelines (official accounts + BitfuryGeorge) get a deeper pull. Top Creators was overweight a single viral clip.

If collectors miss a stretch, the next run updates stored view counts. It does **not** dump weeks of growth onto today's 24h chart. That is how you get a fake spike.

Same public read API as before (stats / feed / news / creators / telegram / discourse). Sentiment still runs on Gonka inference via proxy.gonka.gg.

Links: [Pulse](https://pulse.gonka.gg)

***

## 5. rpc.gonka.gg

Public RPC / LCD gateway. Still free, no key required. Report #2 already had gRPC on `rpc.gonka.gg:9090`, the live-host cutover, archive + indexer move, Feather drain/restore, `/health` that does not hang on a dead sub-service, and the first mobile pass.

This month the wallets broke. Then we fixed the path they actually use.

https://rpc.gonka.gg · https://rpc.gonka.gg/endpoints · https://rpc.gonka.gg/health

What shipped

GG Wallet, Keplr, and CosmJS POST CometBFT JSON-RPC (`status`, `abci_query`) to `/chain-rpc/`. That is a different pool than the GET Feather path. Mid-September one community backend started answering 503. The gateway forwarded the first 503 and never tried the next node. Balances went blank even though other backends were fine.

Pool now walks every backend on 502/503/504 before it fails. `broadcast_tx` 500 is still not retried - we do not want a double submit. Health checks for that pool look at the real JSON-RPC status path, not a webpage that is always 200.

Phone: second layout pass on the landing / health pages after a screenshot that was still ugly (hero buttons, "how traffic flows" stack, Powered-by cards).

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/X1TZcymsHhloNd0.png)

As of Sep 19 public `/health` shows 5 backends up (2 Feather + community). Same docs, same optional `/access` key if you want usage tracking. gRPC still `rpc.gonka.gg:9090`.

Geo-aware routing from the proposal list is still open. Failover and the public health page are what we spent this window on.

Links: [Gateway](https://rpc.gonka.gg) · [Docs](https://rpc.gonka.gg/endpoints) · [Health](https://rpc.gonka.gg/health) · gRPC: `rpc.gonka.gg:9090` · [Access](https://rpc.gonka.gg/access) (optional)

***

## 6. PTD

Proposal text called this MTD. We shipped it as PTD. Report #1 was Pulse (the media slice). Report #2 launched the dashboard: claim a passed proposal, tasks, append-only updates, Core GitHub reports ingested for claimed and unclaimed pages. This month is the report surface, not a second product.

Live: https://ptd.gonka.gg · https://ptd.gonka.gg/reports · https://ptd.gonka.gg/reports/74

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/HeYH95u4C47VKAp.png)

What shipped

Report #2 went up on PTD on Aug 19 ([/reports/74](https://ptd.gonka.gg/reports/74)). Same public report URL as everyone else. No login. GitHub Discussions still has the thread ([#1612](https://github.com/gonka-ai/gonka/discussions/1612)); PTD is the copy you can share if you only want the dashboard.

A proposal page used to show one ingested thread. It now lists **every** report for that id, newest first. #74 shows No.2 on top and No.1 under it. Cards on the home strip and `/reports` jump to the right report (`#report-…`).

Bodies can start with a screenshot (`<img>`) and still parse as markdown. First time we posted #2 that way, headings / bold / links printed as raw `**` and `##`. Fixed the same day.

Core ingest is still the same path as report #2. As of Sep 19 the public list also has #82, #77, #51, plus both #74 reports. We did not add a separate MTD app this window.

Links: [PTD](https://ptd.gonka.gg) · [Reports](https://ptd.gonka.gg/reports) · [Proposal #74 reports](https://ptd.gonka.gg/reports/74) · [GitHub source](https://github.com/gonka-ai/gonka/discussions/categories/governance-proposal-reports)

***

## 7. G-Meter

Report #2 already had DeepSeek and OpenBroker in the probe lineup, plus the AI status notes. This month is a new broker, a new active model, and a couple of honesty / speed fixes on the public page.

Live: https://meter.gonka.gg

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/KnGKRgDtSAT2CwQ.png)

As of Sep 19: **11 brokers** on the dashboard (eterial.ai is the new one). Active models we probe: MiniMax M2.7, DeepSeek V4 Flash, GLM-5.3 Flash. Kimi is marked deprecated - the network dropped it as a PoC model. GLM-5.2 stays optional.

What shipped

**eterial.ai** added to the monitored set. Same checks as everyone else: uptime, latency, price, limits.

**GLM-5.3 Flash** is in the active lineup (catalog, probes, compare, Limits). Limits used to hide a model until the hourly run finished; now a newly added model shows up as "not measured" instead of missing.

Compare / price ladders use the **lowest Gonka broker rate**, not the average. That was making Gonka look more expensive than the cheapest public quote.

Dashboard loads faster - we stopped pulling the heavy live-price payload on every home-page refresh.

proxy.gonka.gg probes now hit the API host, not the marketing site. Those checks were failing for the wrong reason.

Links: [Dashboard](https://meter.gonka.gg) · [Compare](https://meter.gonka.gg/compare) · [Get started](https://meter.gonka.gg/compare/start)

***

## 8. Gonka Chat

New product this window. Not on the original five-item list - same extra-ship pattern as OpenBroker and Pulse in report #1.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/ut7YAA4HQFbzRfU.png)

Gonka Chat is a mailbox for Gonka wallets. Connect GG Wallet or Keplr, then write any `gonka1` address or `.gnk` name. No gas. Identity is the address; a name is optional. Messages and files encrypt in the browser before they leave. If the other side has not opened Chat yet, they can still read after they sign in.

Live: https://chat.gonka.gg

What shipped (late August through mid-September)

- Direct chats, groups, and channels (share a handle like `@squad`)
- Files, replies, `@mentions` (a person or the whole room)
- Invite flow: add-to-room creates an invite in their inbox. The room does not show up until they hit Join. Open invites sit in Incoming Invites
- Push notifications are less flaky
- UI pass on the open-chat window, new-chat flow, and phone layout
- First-run safety note; a Labs system note in the inbox is read-only so it does not look like a random DM you can argue with
- Public unread count (`GET /api/<address>/count`) so explorer wallet pages can show **Message** plus a badge. Click goes to Chat.

Numbers (as of Sep 18)

- First wallets signed in Aug 28
- **49** signed-in wallets · **76** devices
- Rooms: **29** DMs, **53** groups, **42** channels
- **225** live messages (not counting one-time Labs notes)
- **5** wallets active in the last 7 days

Still early. The point this month was to get a real mailbox on the same identity people already use on gonka.gg, not a second login.

Links: [Chat](https://chat.gonka.gg) · [App](https://chat.gonka.gg/app) · wallet pages on [gonka.gg](https://gonka.gg) already have the Message control

***

## 9. x402

New product this window. Not on the original five-item list - same extra-ship pattern as OpenBroker, Pulse, and Chat.

x402 is an HTTP payment standard for agents. Coinbase started it; the x402 Foundation under the Linux Foundation runs it now. Usual story on other networks: agent hits a URL, gets `402 Payment Required`, pays a USDC micropayment in the same request, gets the resource. No signup, no API key, no checkout page.

Gonka did not have that rail. We shipped a public facilitator so the same flow works here, in native GNK or Ethereum-bridged Circle USDC.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/KLdEUlhd2aysCdx.png)

Live: https://x402.gonka.gg
Source: https://github.com/gonkalabs/x402-gonka

Quick wording, because this sentence gets read wrong: "agents settle on Gonka" does not mean the agent is hosted on the chain. An agent is just a program. What it means is they pay for a product that accepts GNK or USDC on Gonka.

What shipped (late August through early September)

- Public facilitator: `/supported`, `/verify`, `/settle`, `/discovery/resources`, paid `/demo`
- Docs on the same host (EN / RU / ZH): get started, sellers, CLI, protocol, HTTP API
- CLI in the repo: `pay` (sign locally, retry with `PAYMENT-SIGNATURE`), `keygen`, `serve`
- GNK (`ngonka`, 9 decimals, `MsgSend`) and bridged USDC (CW-20, 6 decimals, contract `transfer`)
- x402 v2, network `cosmos:gonka-mainnet`, scheme `exact`, transfer `signed-tx`, flow `upfront`
- Open source on GitHub (Sep 3). `git clone` + `go run`

How it works, short:

1. Client hits a paid URL.
2. Server answers 402 with network, asset, amount, `payTo`.
3. Client signs a Gonka transfer and retries with `PAYMENT-SIGNATURE`.
4. Seller calls `POST /settle` here. Tx goes on-chain. Then the resource is served, plus a `PAYMENT-RESPONSE` with the hash.

Settlement is upfront: money moves first. The client signs the full tx. We only broadcast. We do not hold funds.

Sellers do not talk to the chain themselves. Return 402 with your `accepts`, then `POST /settle` on x402.gonka.gg after the client retries. Same hook for a shop, another agent, or a broker that wants agents to buy from it.

As of Sep 19: `/health` is ok, `/demo` still returns HTTP 402 with GNK + USDC `accepts`. One live GNK pay already landed.

| | |
| --- | --- |
| Paid | `/demo` · 1000 ngonka (0.000001 GNK) |
| Payer | `gonka150c4lsmsdr23vly466lskajkfhqh7eghmyjern` |
| Height | 5745133 · code 0 |
| Tx | [23B76D1281F9EFCC7AFC90659480CF3219A7099959C0513720769F700E9B73B2](https://gonka.gg/tx/23B76D1281F9EFCC7AFC90659480CF3219A7099959C0513720769F700E9B73B2) |

```
git clone https://github.com/gonkalabs/x402-gonka.git
cd x402-gonka
go run ./cmd/x402-gonka pay --key "$GONKA_PRIVATE_KEY" --url https://x402.gonka.gg/demo
```

The key stays on the signer. For USDC add `--asset usdc`. We did not publish a USDC settle in this window - the path is there; the proof tx above is GNK.

Still early. The point this month was to put the rail on Gonka, not to wire every Labs API behind it yet.

Links: [Product / docs](https://x402.gonka.gg) · [Get started](https://x402.gonka.gg/get-started) · [Sellers](https://x402.gonka.gg/sellers) · [Source](https://github.com/gonkalabs/x402-gonka)

***

## Proposal checklist

Keeping the [proposal](https://gonkalabs.com/proposal) list honest. Status is halfway (month 3 / 6).

| Item | Status | Notes |
| --- | --- | --- |
| gonka.gg V2 (engine, mobile, inference accuracy) | in progress | Inference + holders in #1/#2. This month: AI Tokens widget, current-epoch nodes, proposals UX, wallet heatmap, IBC holders, `/snap`, tx share cards. More V2 still open. |
| proxy.gonka.gg B2B / analytics | in progress | GLM, v4.1, status honesty, persist retries, OAuth login, file ingest $0. 171B tokens / +2k users since #2 |
| rpc.gonka.gg geo / SLA / aggregator | in progress | Aggregation + public `/health` already live. This month: wallet POST failover + honest JSON-RPC probes. Geo routing still open. |
| OpenBroker | shipped / ongoing | v4.1 path, GLM, public `/status`, cabinet Epoch escrow line. 77 active / 142 registered; ~129B tokens since report #2 |
| Pulse | shipped / ongoing | Live since #1. This month: units on charts, sentiment vs F&G, news mix, catch-up without a 24h spike. 4.3k posts / 28.4M reach as of Sep 19 |
| PTD (proposal item: MTD) | shipped / ongoing | Pulse = media, PTD = governance. Live in #2. This month: host reports on PTD, stack all reports per proposal, markdown + screenshots render. No second MTD app. |
| Gonka App iOS/Android | [FILL] | [FILL] |
| Gonkavote expansions | [FILL] | [FILL] |
| GNS marketplace / scam labels | [FILL] | [FILL] |
| G-Router | [FILL] | [FILL] |
| Gonka Chat (extra) | shipped / early | New this window. Wallet mailbox at chat.gonka.gg. Invites / replies / mentions / push. 49 wallets / 225 live msgs as of Sep 18. Explorer Message + unread badge. |
| x402 (extra) | shipped / early | New this window. Public facilitator at x402.gonka.gg. GNK + bridged USDC. Open source Sep 3. Live GNK `/demo` settle. |

Still in the second half of the six months: harden what is live, finish the checklist items that are not. Next report around mid-October.

***

## Links

- Proposal: [https://gonkalabs.com/proposal](https://gonkalabs.com/proposal) · on-chain [#74](https://gonka.gg/network/proposals/74)
- Report #1: [https://github.com/gonka-ai/gonka/discussions/1477](https://github.com/gonka-ai/gonka/discussions/1477)
- Report #2: [https://github.com/gonka-ai/gonka/discussions/1612](https://github.com/gonka-ai/gonka/discussions/1612)
- Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)
- Explorer: [https://gonka.gg](https://gonka.gg)
- OpenBroker: [https://openbroker.gonka.gg](https://openbroker.gonka.gg) · updates [t.me/openbroker_gg](https://t.me/openbroker_gg)
- Pulse: [https://pulse.gonka.gg](https://pulse.gonka.gg)
- Proxy: [https://proxy.gonka.gg](https://proxy.gonka.gg)
- RPC: [https://rpc.gonka.gg](https://rpc.gonka.gg)
- PTD: [https://ptd.gonka.gg](https://ptd.gonka.gg)
- G-Meter: [https://meter.gonka.gg](https://meter.gonka.gg)
- Chat: [https://chat.gonka.gg](https://chat.gonka.gg)
- x402: [https://x402.gonka.gg](https://x402.gonka.gg) · [github.com/gonkalabs/x402-gonka](https://github.com/gonkalabs/x402-gonka)
- GitHub: [https://github.com/gonkalabs](https://github.com/gonkalabs)

Feedback in the thread is fine - what should we push in the second half from the proposal list?

