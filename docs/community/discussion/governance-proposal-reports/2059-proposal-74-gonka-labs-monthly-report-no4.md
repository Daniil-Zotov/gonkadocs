---
title: "#2059 — Proposal #74: Gonka Labs - Monthly Report No.4"
source: https://github.com/gonka-ai/gonka/discussions/2059
discussion_number: 2059
category: governance-proposal-reports
synced_at: 2026-10-22T23:15:38Z
---

> 🔄 **Auto-sync:** from [Discussion #2059](https://github.com/gonka-ai/gonka/discussions/2059) every hour. 

# Proposal #74: Gonka Labs - Monthly Report No.4

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :bookmark_tabs: Governance Proposal Reports · **Создано:** 2026-10-19 11:34 UTC · **Обновлено:** 2026-10-19 11:34 UTC

---

## 📝 Описание

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7796a968-8c9b-4156-9aab-3acbede4dfca" />

Hey! Gonka Labs here.  
Last updates: [Report No.1](https://github.com/gonka-ai/gonka/discussions/1477) (Jul 18), [Report No.2](https://github.com/gonka-ai/gonka/discussions/1612) (Aug 18), and [Report No.3](https://github.com/gonka-ai/gonka/discussions/1815) (Sep 19).  
On June 12 the community passed [Proposal #74](https://gonka.gg/network/proposals/74). That vote funded six months of infra, ops, and product work. This report is **month 4 of 6**.  
Report #3 was published on Sep 19. This one is what landed since that date.  
Short version since Sep 19:

- About **720B (0.7T)** tokens processed in the month by Proxy and OpenBroker.
- **gonka.gg** - v0.2.16 dashboard pass, inference charts, wallet balances that match the chain, public embed API
- **proxy.gonka.gg** - DevShards v4.2, Jev, deep research, interactive answers in Chat and Workspaces, docs wiki in EN/RU
- **OpenBroker** - DevShards v4.2 on both gateways, Kimi off the lineup, `/status` cap is host weight
- **rpc.gonka.gg** - public request charts (~84.1M gateway requests since Sep 24), accounts closed (no key, no rate limits), chain-api failover when Feather cannot serve an old transaction, site restyle
- **G-Meter** - updated URLs, a page per broker with public gateway volume, share cards on links. Checks no longer dump a burst that a broker RPM cap scores as downtime
- **GG Wallet** - extension 0.2.1. Fees after chain v0.2.16, Keplr hex import, Gonka Chat inside the extension

## 1. gonka.gg

Explorer side of the proposal is still "V2.0": faster, honest numbers, usable on a phone. Report #3 was the AI Tokens card, this-epoch participant nodes, proposals render update, and the wallet heatmap. This month is the v0.2.16 dashboard pass, inference charts people asked for in chat, wallet balances that match the chain in real time, and a public read API for partner websites.

[https://gonka.gg](https://gonka.gg)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/JYTnHbEkoLH0Anr.png)

### Inference and the network

Gateway v5 is its own route (`/devshard/v5`). The indexer now reads it next to v4.1, v4, and the older mounts, so that traffic shows up on `/network/inference`. Image tags 4.1.1, 4.1.2, and 4.1.3 are not separate routes. Hosts serve them on `/devshard/v4.1`, and they were already counted.  


![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/PCpvi3VCvAUkGaE.png)

  
Two charts that were on `/network` now sit on the inference tab, between the 24h cards and gateway traffic. One is inference quality (finished and accepted versus missed and invalid). The other is average request size. The quality chart can lay AI-token volume on the same line. Names and tooltips match what the chart actually is.  
Participants: an explainer on the DevShard columns. Total, Missed, Valid, Invalid, and Miss% are for the whole epoch. Missed = 0 means we counted zero timeouts that name that participant. Most timeouts never name an executor, so they do not land on a row. The text does not mention hosts or internal systems.

  
PoC fee readiness (https://gonka.gg/network/participants?view=fees) is a tab on `/network/participants`, with the same wallet avatars as the rest of that page. After v0.2.16, `MsgPoCV2StoreCommit` and `MsgSubmitHardwareDiff` need a fee. The tab shows whether the warm key's feegrant can still pay that. A grant is often 10 GNK. When it is spent, the warm key stops.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/vaURtdIQHoWERrX.png)

  
H100 equivalent is updated at chain level, now it matches what we used all this time. One important update from our side, is that it is no longer flashes 0 when the current epoch has no fresh H100 80GB HBM3 sample (that happens in confirmation PoC). The card keeps the last good weight-per-card and the tooltip says the sample is weight per GPU, not "this epoch's number is last epoch's number." The v0.2.16 sample counts H100 80GB HBM3 nodes on mixed hosts. A host is no longer dropped because another card in the box is not an H100. The same median fix covers other cards reverting dropped RTX 5090.  


![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/IFOVsbPfv4AND2p.png)



Delegations now hold shape each time you refresh the page. One chain read is served until the next refresh.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/qG6QNt1BEt8kYy5.png)

### Homepage, price, transfers

Chart modals (weight, H100, participants, AI tokens) now track the point under the cursor with a rolling number, zoom on scroll, and pan by dragging. Double-click resets the window. The rest of the homepage is unchanged.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/uAJayBjtBqYDF8J.png)

  
A transfer row on the homepage opens the transaction. Amounts are no longer forced to 3 decimals. 0.0098 GNK stays 0.0098 GNK in the list and on the transaction page. Round amounts still show three places (1.000 GNK).  
Market cap is native circulating supply times the HEX price.

### Proposals

Proposal page (https://gonka.gg/network/proposals) updates when a new proposal is on chain, and the list is served from cache so a slow chain read cannot blank the page. Pages after the first show turnout and quorum. Individual Proposals are now translated upon discovery to En, Ru, ZH and displayed with accordance to the global language selection. Translation is prepared ahead of time and does not run while the page loads.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/AuIimwZCWiW1RxA.png)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/v5SWkOssW1ZjAq2.png)

### Wallets

The balance on a wallet page is read from the chain when you open it in milliseconds, not from cache so balance is updated **live**. Overview has a balance chart: it starts at the live balance and walks every transaction backward, so the line cannot go negative. Days, hours, or minutes. Blue line, inside Overview.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/6mo5RO6Vxh48yfQ.png)

  
Neighbors: open the address, see the transactions with that neighbor in a modal, instead of hunting the full history.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/oJLrHsBtFRdIpDr.png)

### Embed API

Other sites can read the public cards without scraping the HTML. One key, four routes. Any website can call them from the browser after applying to get api key.

- `GET /api/embed/v1` lists the datasets
- `GET /api/embed/v1/charts/network` is the four homepage sparklines: weight, H100 equivalent, participants, AI tokens
- `GET /api/embed/v1/network` is what those charts do not have: confirmed tokens for the last closed epoch, confirmed tokens for the last 24 hours, the WGNK/GNK price (HEX mid), and the models hosts currently serve
- `GET /api/embed/v1/usage` is the four "live network usage" cards: inferences and tokens in the last closed epoch, hosts that served them, and live model ids  
  The 274k / 1.2M / 70 / 4 figures in that design are placeholders. The usage route returns the live counts. Confirmed tokens are billed input plus output after a request finishes, same rule as the inference page.

## 2. proxy.gonka.gg

Report #1 was the dedicated-box migrate, public `/status`, DevShards v3. Report #2 was Workspaces, MCP in chat, DeepSeek, and the agent/tool-schema repairs. Report #3 was the v4.1 path, GLM, a status page you can send to a customer, persist-through-rate-limits, OAuth, and file ingest at $0. This month is the next protocol step, research, a decision model, and the chat surface learning to draw instead of only writing paragraphs.  
Quick recap: OpenAI-compatible proxy on Gonka DevShards. Keys, balances, usage, Chat, Workspaces. Public API at [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1). UI at [https://proxy.gonka.gg](https://proxy.gonka.gg). Status at [https://proxy.gonka.gg/status](https://proxy.gonka.gg/status). Docs at [https://proxy.gonka.gg/docs](https://proxy.gonka.gg/docs).  
Numbers (19 Sep through 18 Oct, served completions on proxy accounts):

- **526B** tokens
- **40M** served requests
- Peak day **15 Oct: 34.5B**
- **8k** new accounts

### Deep research

Docs: https://proxy.gonka.gg/docs/deep-research

Chat and the API run the same loop. The proxy plans several searches, reads public pages, asks Jev which pages to keep, then has the model you named write a cited report. You are billed for that model's tokens. Jev inside the loop is not a Jev API call and is not billed.  
In Chat, turn on Deep research in the composer. The page shows the stages (plan, search, judge, deepen, read, write), the searches, and the keep/drop list. Closing the tab does not cancel it. Open the chat again and the run is still there. The finished report is saved in the thread.  
On the API, add `deep_research: true` to a normal `/v1/chat/completions` call. Progress is an SSE comment (`: research …`) so an OpenAI SDK still returns only the report. Clients need a long timeout. That call stays on the HTTP connection: if the client disconnects, the API run stops. Only Chat keeps going after the page is gone.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/F8vgsjla8DHJyrU.jpg)

  
Workspaces use the same loop from the composer. The research board replaces the generic "Thinking" line. Text already written is saved while the report is still streaming, so closing the page no longer wipes it. 

### Jev

Docs: https://proxy.gonka.gg/docs/jev

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/pE9k0gbPGe3QqhH.jpg)

Jev is not a Gonka chat model. Do not send `jev` to `/v1/chat/completions`. It takes a `state` and the judgments you need, and returns structured answers your code can act on.  
`POST https://api.proxy.gonka.gg/v1/systemone` (`/v1/decisions` is the same call). Price is $0. It does not count against the proxy rate limit. An account can call it only after 100,000,000 tokens in the last 30 days. Under that line, the call is refused and nothing is forwarded. The dashboard shows that line.

### Interactive answers

Docs: https://proxy.gonka.gg/docs/chat

https://github.com/user-attachments/assets/6e10c291-529e-490f-ac26-9e21ccb0ee43




When a chart, diagram, or calculator is more useful than a paragraph, Chat and Workspaces render it. The model emits one or two fenced `gonka-ui` JSON blocks. The page draws them. Nothing in the block is executed as HTML or JavaScript.  
What you can get: a line / bar / area / pie chart, a small dashboard, a diagram you can click through, a slider calculator, a short frame-by-frame motion, and choice buttons. A choice fills the composer. It does not send by itself.  
A plain factual answer stays text. "Build me a tracker" is still a Workspace block, not a widget in the thread. `/v1/chat/completions` still returns the text. An SDK does not draw the block.

### Workspaces

The extra title row is gone. Share sits on the chat row. The model picker follows `/v1/models`: DeepSeek, GLM, MiniMax. Kimi is not offered. A failed inference turn retries on its own (three tries, then one error). Stop and an empty balance are not retried.

### Also

Docs are a wiki now, in English and Russian, with a language switch. New pages cover Copilot, Windsurf, and Cursor, plus the features above. [https://proxy.gonka.gg/docs](https://proxy.gonka.gg/docs) and [https://proxy.gonka.gg/ru/docs](https://proxy.gonka.gg/ru/docs).  
Public status: client disconnects and invalid requests are their own series, so they do not paint the capacity chart red. A confirmation PoC is labeled as a network check, not a Proxy outage. The page is served from a cache, so a gateway blip does not zero every number.

## 3. OpenBroker

Launch was discussion #1363 and Report #1. Report #2 put DeepSeek on both gateways. Report #3 moved serving to DevShards v4.1, turned GLM on, and shipped public `/status`. This month is the next protocol step, and a status page that says when the cap fell because hosts left, not because the service did.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/CxuJnNLIJ49tnAr.png)

Quick recap: managed DevShards. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at [https://api.openbroker.gonka.gg/v1](https://api.openbroker.gonka.gg/v1). UI at [https://openbroker.gonka.gg](https://openbroker.gonka.gg). No markup on inference. Stats at [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats). Status at [https://openbroker.gonka.gg/status](https://openbroker.gonka.gg/status).

Numbers (19 Sep through 18 Oct):

- About 720B tokens and 63M requests
- Peak day 15 Oct: about 51.5B tokens / 3.3M requests
- 12-18 Oct: about 287B tokens / 16.6M requests
- 18 Oct: about 27.6B tokens / 1.6M requests
- Mix: MiniMax about 436B, DeepSeek about 180B, GLM about 96B. Kimi is not in this window
- Brokers: 175 registered (was 142 on 19 Sep). 96 active, 79 still waiting on a first deposit

Both live gateways moved onto DevShards v4.2 (`/devshard/v4.2`). Same public URL. Brokers did not rotate keys. v4.1.3 is off. Same job as the v4.1 cutover in report #3: stay on the protocol the network actually runs.

Public lineup is MiniMax-M2.7, DeepSeek-V4-Flash, and GLM-5.3-Flash. Kimi is gone from the pool. Docs, `/v1/models`, and `/status` match that list.

`/status` got another honesty pass. "Capacity available" is the share of epoch host weight the gateway can still send to. The effective cap is that share times the configured max, so a card can show a small cap while escrow counts are full. "Unavailable" is weight we are not using. "Quarantined" stays at 0 while quarantine is in shadow mode, so those are not the same list. Each model row is in-flight against its own live cap. A red capacity number is hosts, not an OpenBroker outage.

A host that fails used to sit out for 30-60 minutes. That window is now shorter and mostly in seconds (empty stream and a stalled winner at few seconds, HTTP and transport failures at a bit more seconds). One bad stretch no longer parks a heavy host for the rest of the hour. The cap on `/status` still moves when several large hosts drop at once. It comes back when they do.

Cabinet: the requests view has 24h / 7d / 30d / all, pages, and duration. Models show the same logos as proxy.gonka.gg. The Labs secondary broker is labeled as the proxy.gonka.gg fallback in the UI. The name in the database did not change.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/YvNmExJdJJxKpUK.png)

Overall design was updated to follow update gonkalabs design.

## 4. GG Wallet

Browser extension for a Gonka address: send, stake, names, governance, and now the mailbox. Same identity as gonka.gg and chat.gonka.gg. No second account.

Repo: [https://github.com/gonkalabs/ggwallet](https://github.com/gonkalabs/ggwallet) · extension version **0.2.1**

Links: Chrome extension repo · https://chromewebstore.google.com/detail/gg-wallet/elicodfmaffbndngiifcpmammicgjidd

### Fees after chain v0.2.16

The chain started charging **1 ngonka per gas** on paid messages. The wallet was still attaching `0ngonka`, so sends died with `insufficient fee`. Governance votes stay free.

What shipped in **0.2.0** (Oct 8):

- Paid transactions (send, stake, IBC, contracts, proposal deposits, the inferenced runner) use that minimum. Votes stay at a zero fee.
- If a site asks the wallet to sign a Gonka transaction with a fee that is too low, the sign document is raised before the user reviews it. Vote-only requests are left alone.
- Gas simulation was short by a hair (a send asked for 96,526 gas and used 96,667). Headroom is a slider from 1.0× to 3.0×. **2.0×** is the recommended setting. Under **1.5×** is marked as too low. The confirm screen shows the multiplier, the gas limit, and the fee in GNK.
- **Max** no longer sends the whole balance. The fee comes out of spendable GNK, and vesting coins cannot pay it. Review stops the send when the amount plus the fee is more than the spendable balance, instead of failing on chain after confirm.

### Import a Keplr key

Keplr’s Gonka export is a hex private key, not a 12- or 24-word phrase, and that key cannot be turned back into a phrase. Import now accepts the hex key and signs with it directly. The address matches the Keplr Gonka account. That wallet has no recovery phrase to reveal later. A phrase import still works the same way.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/cA3VRyvtckDwau7.png)

### Chat inside the extension

Gonka Chat was already a separate site (Report No.3). The extension now speaks to `chat.gonka.gg` itself. Text is encrypted on the device with the same nacl room key the website uses, then only ciphertext is uploaded. Signing in is two wallet signatures and does not spend GNK. The encryption signature is over the fixed string `Gonka Chat encryption key v1`, so the inbox matches the one in the browser.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/6XWlaeVE3DnJQGJ.png)

- Switch wallets and the inbox follows that address. Keys stay stored per address.
- Inbox filters: All, DM, Group, Channel, Inbox. Each row has a type badge and how long ago the last message arrived.
- Open a thread and each message has its own time. Your messages show **Delivered** until the other side opens them, then **Read** (in a group, **Read by** the people who opened it). Channels do not track reads.
- In a group or channel, `@` mentions the other members. Tap the title to see who is in the room and their role.
- A `.gnk` name in New message resolves to the `gonka1…` address as you type. An unknown name cannot be sent.
- Home screen Chat button shows the unread count for the active wallet (`GET /api/<address>/count`). The same count sits on the browser toolbar icon and refreshes about once a minute. Blank when there is nothing unread. **99+** when the mailbox caps the total.

The public counter has been up since September 24. Here is a section in the same voice as Report No.3, plus the short line and the checklist row.

**Short version**

- rpc.gonka.gg - public request charts (~84.1M gateway requests since Sep 24), accounts closed (no key, no rate limits), chain-api failover when Feather cannot serve an old transaction, site restyle

## 5. rpc.gonka.gg

Public RPC / LCD gateway. Still free. Report #3 already had wallet JSON-RPC failover (one 503 no longer blanks GG Wallet / Keplr balances), honest health checks, and a phone pass on the site. gRPC was already on `rpc.gonka.gg:9090`.

This month we updated the design language of the system, and a historical transaction lookup that was stuck on a 503 now fails over.

[https://rpc.gonka.gg](https://rpc.gonka.gg) · [https://rpc.gonka.gg/endpoints](https://rpc.gonka.gg/endpoints) · [https://rpc.gonka.gg/health](https://rpc.gonka.gg/health)

Numbers (counter started Sep 24, as of Oct 18):

- ~84.1M gateway requests in 25 days
- Peak day ~3.84M (Oct 5)
- Last 7 days ~23.7M
- About 40 requests/second through the day. Homepage was showing ~44 req/s at the end of Oct 18

That count is gateway traffic, including anonymous calls. It does not include the public pages themselves. Sep 19-23 is not in the series. The chart says "not recorded" for anything before the counter existed.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/4BqPLNScJEShWIK.png)

Homepage has a live request rate, a last-60-minutes chart, and a requests-per-day chart with a 7 / 30 day switch. Hover a bar for the count.

Accounts are closed. Report #3 still had an optional `/access` key if you wanted usage tracking. Login, sign-up, portal keys, and checkout now return 410. `/portal` sends you to `/access`, and that page says the same thing: no account, no API key, no rate limits. Point at `https://rpc.gonka.gg`. The public charts replaced per-key usage.

The site was restyled to the new brand look.

Chain API failover, for old transactions. A tx-by-hash GET on `/chain-api` was coming back as nginx 503. `/chain-api` only went to the two Feather nodes. One node's chain API was down. The other answered, then rejected the height: that transaction is in block 6,330,721, and Feather's earliest kept block is about 6,474,695. Hyperfusion and 6block still have the transaction. They were only in the pool for `/chain-rpc` and `/v1`. They are now the fallback for `/chain-api`, and only after both Feather nodes fail. A normal chain-api call still comes from Feather. node1.gonka.ai stays off this path. It is pruned at the same height, so it cannot return that transaction either.

A response now carries `X-Rpc-Node` with the public name of the node that actually answered (Feather RPC #1, Hyperfusion, 6block, and so on).

**Also, we released an explainer video about RPC as a part of our new media content initiative:**

EN: https://youtu.be/HA7gG2nEuKw

RU: https://youtu.be/u1RLkgsxLHk



Since Report #3 (Sep 19). Drop this in as the G-Meter section, and this line in the short list at the top:

- **G-Meter** - real URLs, a page per broker with public gateway volume, share cards on links. Checks no longer dump a burst that a broker RPM cap scores as downtime.

## 6. G-Meter

Links: [Meter](https://meter.gonka.gg/) · [Compare](https://meter.gonka.gg/compare)

[meter.gonka.gg](https://meter.gonka.gg) still probes public Gonka brokers on a timer (quick checks, limits about hourly) and shows who is up, how slow, and what it costs. Report #3 added eterial.ai, GLM-5.3 Flash, and compare-at-the-lowest-Gonka-rate. This month the site itself changed.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/8yaus8RKyyMmVMb.png)

It is no longer one page with tabs. Every view has a URL: trends, providers, limits, history, compare, a model, a log. Broker names on those pages stay on meter. The outbound link sits on that broker's own page.

### Broker page

Open [OpenBroker](https://meter.gonka.gg/brokers/openbroker-by-gonka-labs-b11) (or any other name in the tables). You get the latest meter check, then the public 24h gateway volume from gonka.gg:

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/uc9tsqH7zR5KXXo.png)

- A devshard operator (allowlisted wallet, own escrow gateway) gets that gateway's inferences and tokens.
- Proxy and OpenBroker are split. The page uses each product's own total, not the combined Gonka Labs row.
- Someone who only rides OpenBroker gets their own usage inside OpenBroker, labeled as that, not the operator total.
- A node plus a broker key is not in those public stats. The page says so and does not invent a count.

**See all stats** goes to the [inference tab](https://gonka.gg/network/inference?tab=inference). **Visit broker** is the one link that leaves the site.

### Share a link

Paste a meter URL in Telegram and you get a card, same idea as a tx card on gonka.gg: title plus a 1200×630 image (health, uptime, failed, latency, tokens when the public stats have them). Homepage, compare, and each broker page each get their own.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/OdHBMHJDjKkBKN2.png)

### Checks

Trends, Providers and Compare stay on MiniMax, DeepSeek, and GLM. Kimi is off those pills.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/sIDTY5BDKBmdNzo.png)

A quick check is about 30 chat calls, back to back, roughly once an hour per broker. Fired with no gap, that burst is well over a small RPM cap, and HTTP 429 was counted as a failed probe, so Degraded. Chat calls are now spaced (about 30 RPM). A cap at 40 or 60 is enough for a normal run. Limits are lighter, about 15-18 calls, with one long output.

## 7. gonkalabs.com

The Labs homepage. Not a new product. It is the index in front of the ones in this report. Report #3 did not touch it. The website is fully updated.

Live: [https://gonkalabs.com](https://gonkalabs.com)

The homepage uses the same brand design system as proxy.gonka.gg, openbroker.gonka.gg and rpc.gonka.gg. White canvas, stone product cards, the deep-green bands. The hero is the static dotted wave from gonka.ai. It does not animate.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/F58T7uLOle3tYqA.png)

The catalog is 18 products. Gonkablocks is gone from this page. Workspaces is its own card and opens [https://proxy.gonka.gg/workspaces](https://proxy.gonka.gg/workspaces). Chat, x402, Pulse, and PTD are on the grid with everything that was already live. The first row is Proxy, Workspaces, OpenBroker, rpc.gonka.gg.

The header shows the sum of public GitHub stars. Hover lists each public repo and its count. As of Oct 19 that sum is **65** across 19 public repos.

Articles on the page are the gonkalabs posts on gonka-ai/gonka discussions, including these monthly reports, newest first. X is [@gonkalabs](https://x.com/gonkalabs), next to Telegram.

## 7. Share&Earn

At 13th of October, we launched a program to reward users who actively share the benefits of Gonka's inference capabilities.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/Fkk8OoQ2T7bIb3R.jpg)

Over the next few weeks, we will distribute 500B (500 billion) AI tokens in the form of 1000 fixed rewards, each worth 500M tokens.

This reward is for valuable content that demonstrates how you are using Proxy.gonka.gg: case studies, tutorials, screen recordings, and explanations of features.

What we consider valuable:

- Videos or screen recordings showing a real-world process.
- Tutorials or guides on solving a specific problem.
- Reviews with data: "saved X hours," "reduced the process by Y%," or a public project or template built on Gonka.
- Standard AI-generated videos are also accepted, provided they have a meaningful message about the advantages of using Gonka compared to other AI providers.

How to get the bonus:

1. Create content and publish it on your platform (X, LinkedIn, YouTube, Instagram, Reddit, blog, or relevant forum).
2. Send the link through the form on proxy.gonka.gg/earn.
3. We will review it and credit 500M tokens to your account.

Important:

- A simple mention is not enough. It's important to have a meaningful message.
- We reserve the right to choose. Empty spam accounts, artificially inflated views, and non-informative posts without mentioning proxy.gonka.gg will not be accepted. One account is eligible for one bonus. Mult-accounting, if detected, will be blocked.
- Since the rewards are limited, preference will be given to posts that meet the criteria above.

The number of bonuses is limited.  
The promotion will end automatically once all rewards have been distributed.  
We may extend the promotion if it proves effective.

Details and the form - proxy.gonka.gg/earn

***

*Still working to make Gonka Labs products better while creating new ones. Hardening infra under real load, polishing what already shipped, building the next products on the list. More updates as they land.*

## Links

Last report: [Monthly Report No.3](https://github.com/gonka-ai/gonka/discussions/1815)

Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)

Explorer: [https://gonka.gg](https://gonka.gg)

OpenBroker: [https://openbroker.gonka.gg](https://openbroker.gonka.gg)

Pulse: [https://pulse.gonka.gg](https://pulse.gonka.gg)

Proxy: [https://proxy.gonka.gg](https://proxy.gonka.gg)

PTD: [https://ptd.gonka.gg](https://ptd.gonka.gg)

RPC: [https://rpc.gonka.gg](https://rpc.gonka.gg)

G-Meter: [https://meter.gonka.gg](https://meter.gonka.gg)

GitHub: [https://github.com/gonkalabs](https://github.com/gonkalabs)



**Feedback welcome in the thread,**

**Gonka Labs team**
