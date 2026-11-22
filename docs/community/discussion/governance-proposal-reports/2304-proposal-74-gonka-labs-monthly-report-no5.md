---
title: "#2304 — Proposal #74: Gonka Labs - Monthly Report No.5"
source: https://github.com/gonka-ai/gonka/discussions/2304
discussion_number: 2304
category: governance-proposal-reports
synced_at: 2026-11-22T11:10:26Z
---

> 🔄 **Auto-sync:** from [Discussion #2304](https://github.com/gonka-ai/gonka/discussions/2304) every hour. 

# Proposal #74: Gonka Labs - Monthly Report No.5

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :bookmark_tabs: Governance Proposal Reports · **Создано:** 2026-11-21 00:08 UTC · **Обновлено:** 2026-11-21 00:08 UTC

---

## 📝 Описание

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/P7BhXdoyNXBAYj2.png)

Hey! Gonka Labs here.

  
Last updates: [Report No.1](https://github.com/gonka-ai/gonka/discussions/1477) (Jul 18), [Report No.2](https://github.com/gonka-ai/gonka/discussions/1612) (Aug 18), [Report No.3](https://github.com/gonka-ai/gonka/discussions/1815) (Sep 19), and [Report No.4](https://github.com/gonka-ai/gonka/discussions/2059) (Oct 19).

  
On June 12 the community passed [Proposal #74](https://gonka.gg/network/proposals/74). That vote funded six months of infra, ops, and product work. This report is wrapping up **month 5 of 6**.  
Report #4 was published on Oct 19. This one is what landed in public since that date, through Nov 19.

A number of major products are in the finishing stages of multi-month development. They are not in the shipped list below. This report is the infrastructure, the explorer, the gateways, and the public sites those products sit on.

Short version since Oct 19 2026:

- **Inference** on the public devshard index: Proxy: 1.26T prompt + completion tokens, peak day Nov 9: 66.5B. OpenBroker: 0.390T tokens, 47.8M requests, peak day Oct 28: 21.6B.
- **gonka.gg** - the explorer restyle is on production. Wallet pages show bridged balances. Address history can be filtered. The index counts v6. Numerous api-gated apis used by external products.
- **proxy.gonka.gg** - a second gateway, DevShards v6, signup refactor, Jev availability. A full gateway waits for a slot instead of failing the call.
- **OpenBroker** - cabinet links each request to the inference on gonka.gg. Oversized prompts are refused before they hit a host. DevShards v6.
- **rpc.gonka.gg** - **112.1M** gateway requests from Oct 22 through Nov 19. Peak day **Nov 13: 4.82M (3.3M req a day on average)**.
- **G-Meter** - compare numbers are a public API. New brokers added.
- **Pulse** - new public pages added to auto-indexer and gonka.ai website is also scraoed - in the web feed already. Post images keep their full frame.
- **In finishing** — several large products. Groundwork for them shipped on gonka.gg, the proxy, and chat.gonka.gg. The products themselves are not released in this report.

## 1. gonka.gg

Explorer became faster, with more honest numbers, with better usability on a phone. Report #4 was the v0.2.16 dashboard pass, inference charts, wallet balances that match the chain in real time, and a public embed API for partner sites. This month the site was redrawn on one system, the index learned the gateway route the network is actually serving, and the read APIs grew the feeds the products in finishing need.

[https://gonka.gg](https://gonka.gg)

### One visual system, on production

The new system went to production since Oct 22 all the way to Nov 2 nd. It covers the surfaces people actually use.

Inference and the devshard tab. The homepage, including the chart modals and the top bar. Proposals, and a single proposal. Participants. Transactions and blocks. A transaction, including the grouped detail blocks so a section reads as one card instead of a stack of loose rows. Delegations. GPUs. Token holders. The community fund. Slashing. The tools menu: reward calculator, faucet, names, node tracking. The assistant. An address. An escrow. A single inference inside an escrow.

Charts on the homepage and on the GPU page zoom on scroll and pan by dragging. A drag that changes the scale animates. Double-click resets the window, the same gesture as the homepage modals in report #4. GPU charts no longer lead with a row of pills. Selection is a control ("N GPUs"), with a settings icon and a tooltip on "current epoch" and "top 4". The first visit to `/network/gpus` explains that once. It does not come back.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/EPi8jpeIDwIcJRl.png)

The escrow page draws the lifecycle as a sequence, with a tooltip on each step for what it is and when it happens. A raw status string is a poor explanation of store, commit, inference, validation, and settle.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/iPlzprttv4oancU.png)

Amounts on transfer rows read the way other explorers do. 150 GNK is 150. A fractional amount keeps the places it needs. 0.0098 stays 0.0098. Report #4 stopped forcing three decimal places. This pass stops painting `.00` onto a round amount.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/xpCCu9GToNV9prG.png)

The faucet page fits the screen width. The search field no longer renders black type on a black fill. Names and the faucet keep the content width they were given on purpose. Both stay centered.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/MgWvZjbGwJxRE9i.png)

### Inference index

Gateway v5 was already its own route in report #4 (`/devshard/v5`), read next to v4.1, v4, and the older mounts. This month the network moved on again.

On Nov 13 the inference had an upgrade that prevented undercounting under evolving devshard url routes. The pooler reads older mounts as well as newer ones, so a host serving `/devshard/v6` or any new version keeps landing on a row in the indexers table automatically. Proxy and OpenBroker moved onto v6 the week of Nov 17, after the index could see it, and that traffic is in the series, counted correctly.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/rO42vO9WNxHMeYM.png)

GLM is on the devshard tab. A model the chain was serving and the tab was not listing is listed. Double-counted model names on the inference tab are fixed. 

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/xJmMjSVBcYjvicn.png)

Chain reads for the explorer go to rpc.gonka.gg. A direct poll of host LCD endpoints every few seconds was load those hosts should not carry, and it was not buying fresher pages. Health checks against hosts are once a minute. The indexer addresses are allowlisted on the RPC, so that traffic is served and is not scored as abuse.

### Wallets

The balance on a wallet page is still the live chain read from report #4. What changed is everything around it.

An address page can filter the transaction list, sort it, and split incoming from outgoing. The controls sit behind the settings icon, so the default view stays the list. The query is the one the page already used. It is fast on an address with a long history. The page size on that read is 500,000, which is what a full export and a client that wants the whole book both need. 

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/J4qCzJydNS3xnnQ.png)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/K50ddPj9pe6fAtG.png)

Bridged balances are on the address. WGNK and the other bank denoms sit in a wallet-style block: a row per denom, the amount, and the history that belongs to that denom. A wrapped transfer from Ethereum that never showed up next to native GNK is in that history. Opening the address and seeing only GNK was hiding the bridge. Neighbors, from report #4, are unchanged: open the address, see the transactions with that neighbor in a modal.

The homepage weight card can show H100 equivalent or the physical GPU count. The H100 figure keeps the rule from report #4. It holds the last good weight-per-card when the current epoch has no fresh H100 80GB HBM3 sample, and the tooltip says the sample is weight per GPU.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/x3Zwq4QvetiF3Yz.png)

### Proposals and the embed API

Proposal pages still update when a new proposal is on chain, and the list is still served from cache so a slow chain read cannot blank the page. Report #4 translated proposals into English, Russian, and Chinese ahead of time. This month that text is readable under an embed api key. An external service / website / caller passes the proposal id and the locale (`en`, `ru`, `zh`) and gets the text. The translation is still prepared ahead of time. It does not run while the page loads.

The embed API from report #4 is still one key and the public cards. Added this month:

- 24h model usage, the block on `/network/inference`
- The proposal list and a single proposal, including turnout and the translated body
- The network sparkline can be read as H100 equivalent or as the physical GPU count, matching the homepage switch

## 2. proxy.gonka.gg

Report #1 was the dedicated-box migrate, public `/status`, and DevShards v3. Report #2 was Workspaces, MCP in chat, DeepSeek, and the agent and tool-schema repairs. Report #3 was the v4.1 path, GLM, a status page you can send to a customer, persist-through-rate-limits, OAuth, and file ingest at $0. Report #4 was DevShards v4.2, Jev, deep research, interactive answers in Chat and Workspaces, and the docs wiki in English and Russian.

This month is capacity, a second gateway, the v6 line, and the API surface the products in finishing are wiring up. The account ledger from report #4 (proxy's own shards versus the OpenBroker fallback, new accounts, the per-model mix) is not restated. Those books are not split on the public index. Section 1 is the chain-side total for both products together.

Quick recap: OpenAI-compatible proxy on Gonka DevShards. Keys, balances, usage, Chat, Workspaces. Public API at [https://api.proxy.gonka.gg/v1](https://api.proxy.gonka.gg/v1). UI at [https://proxy.gonka.gg](https://proxy.gonka.gg). Status at [https://proxy.gonka.gg/status](https://proxy.gonka.gg/status). Docs at [https://proxy.gonka.gg/docs](https://proxy.gonka.gg/docs).

Lineup is still MiniMax-M2.7, DeepSeek-V4-Flash, and GLM-5.3-Flash. On the morning of Nov 20, `GET /v1/models` listed those three plus Jev. Context on that response: MiniMax 180,000, DeepSeek V4 Flash 400,000, GLM 5.3 Flash 400,000. Kimi is off the lineup, as in report #4. `/v1/models` still only lists a model when the live pool can take it.

### Two gateways

One gateway was the whole proxy. There are two gateways now, on two machines, traffic split across them. `/status` shows the pool: served, errors, and tokens are the sum. Machine addresses are not on the page.

### DevShards v6

Report #4 moved serving onto `/devshard/v4.2`. Same job this month, one protocol step later. In the week of Nov 17 the gateways left v4.2 for the v6 line. Same public URL. Keys did not change. A caller does not pick the gateway version. The proxy does.

### A full model waits, then says which model has room

A full gateway used to fail the call. The caller retried, the retry landed in the same full pool, and the error was a bare 429. A request now waits for a slot. If the wait runs out, the error is specific. A `queue_timeout` names the model that was full and names a model that still has room, with the free-slot count, so the client can switch instead of hammering the same name.

Chat and deep research keep running when the client disconnects. Report #4 already kept a Chat deep-research run alive after the tab closed, and cancelled the API run when the HTTP connection dropped. This month a normal chat reply is in that first category. The text already written is kept. Opening the thread again shows the finished reply. An SDK call that stays on one HTTP connection still ends when that connection ends.

### What callers hit this month

New accounts get file ingest. A picture attached as an OpenAI `image_url` part (a `data:image/jpeg;base64,...` URL) reaches the model. Before this, a brand-new account could send the bytes correctly and the model would answer as if no image had been attached. File ingest at $0, from report #3, now applies from the first request.

Web search and deep research start on for a new user. The loops are the ones from report #4. Docs: [https://proxy.gonka.gg/docs/deep-research](https://proxy.gonka.gg/docs/deep-research). The stages are still plan, search, judge, deepen, read, write. Jev inside the loop is not billed separately. You are billed for the model you named in the request params.

A completion can carry its cost. The figure is the one the dashboard will show for that call, so a client that displays the stream and a client that displays the bill are reading one number.

## 3. OpenBroker

Launch was discussion #1363 and Report #1. Report #2 put DeepSeek on both gateways. Report #3 moved serving to DevShards v4.1, turned GLM on, and shipped public `/status`. Report #4 moved both gateways to v4.2, took Kimi off the lineup, and made `/status` report host weight: "capacity available" is the share of epoch host weight the gateway can still send to, and a red capacity number is hosts, not an OpenBroker outage.

This month is the cabinet, a check before the request is sent, a cap that was silently under the model caps, and the same v6 move as the proxy.

[https://openbroker.gonka.gg](https://openbroker.gonka.gg) · [https://api.openbroker.gonka.gg/v1](https://api.openbroker.gonka.gg/v1) · [https://openbroker.gonka.gg/status](https://openbroker.gonka.gg/status) · stats at [https://openbroker.gonka.gg/stats](https://openbroker.gonka.gg/stats)

Quick recap, unchanged: managed DevShards. Register, deposit GNK, get an `obk-*` key, point any OpenAI client at the API. No markup on inference. Public lineup is MiniMax-M2.7, DeepSeek-V4-Flash, and GLM-5.3-Flash.

The public index does not give OpenBroker its own token total. It is inside the Labs row in section 1. Adding a separate OpenBroker headline on top of the 1.79T would count the same inferences twice.

### Cabinet

The cabinet follows the same system as gonka.gg. The requests view, the overview, and the ledger were on the older layout, and a broker comparing a row to the explorer was doing the translation by hand.

A request opens the exact inference on chain: `https://gonka.gg/network/devshards/escrow/<escrow>/<inference>`. An escrow id opens the escrow. A GNK ledger row opens the transaction. Gateway rows link to the explorer as well. "On chain" is a link, not a label.

Duration is in seconds, with milliseconds under that number in a smaller, dimmer face. The tokens column is the total on the first line and input / output under it. Counts are full numbers. 11,080 is 11,080, not 11.08k. The time window on a widget stays on the range you picked. It was snapping back to a shorter range after a refresh.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/z3akiFzFiN3tbzG.png)

The requests view was stalling on large accounts. Recent requests hung. `/api/auth/me` took more than ten seconds and then returned a timeout, which made the whole dashboard look down. The weight was stored prompt and completion bodies. Those bodies are no longer kept. The page loads. What a broker sees on the dashboard (counts, cost, duration, model, the on-chain link) is still there. A deposit that had landed on chain and had not been credited was credited. The watcher is the same path.

The active tab is marked. Top-up sits where a broker who has paid before can find it without hunting. That sounds small until you watch someone who has deposited repeatedly spend a few minutes on it.

### Before the request reaches a host

A prompt that cannot fit the model, leaving room for the completion, is refused before it is sent. The estimate is local and fast. It uses the tokenizer for that model family, not one shared guess for every name. The target is the model's context minus a completion reserve (on the order of 16k tokens), so a prompt that would finish a few tokens over the limit is caught with the output still possible.

The check is per key. A key that keeps sending those prompts is backed off, and the error says why and how long the backoff runs. A later normal-sized prompt clears it. The key is not paused for good, and a single oversized call does not reject every other call on that account. A broker who only rides OpenBroker, and a broker running their own book, get the same rule. The failure used to show up as a host error, an escrow hold, and a red row on `/status`. It now stops at the door before request hits the chain reducing unnecessary load for Hosts.

This is the same problem Hosts had been seeing from callers sending well past the context window, on the order of a million tokens, which pins an escrow until someone clears it by hand. Refusing the prompt is the fix that does not require that.

### Caps, old escrows, v6

GLM was returning `429` with `openbroker_cap` ("too many concurrent requests") while the model card still showed room. There were two caps. Each model had its own, and a single shared cap sat underneath them. MiniMax alone, across the two gateways, was already near that shared number, so GLM had almost nothing left and the card, which reads the model cap, looked fine. The shared cap is raised above the sum of the model caps.

A host that fails still sits out for seconds, the rule from report #4, not for the rest of the hour. The cap on `/status` still moves when several large hosts drop at once. It comes back when they do.

## 4. rpc.gonka.gg

Public RPC / LCD gateway. Still free. Report #3 had wallet JSON-RPC failover (one 503 no longer blanks GG Wallet or Keplr balances), honest health checks, and a phone pass on the site. Report #4 restyled the site, closed accounts (no key, no rate limits), added the public request charts, and failed a historical transaction lookup over to trusted community members when both Feather nodes were pruned past certain height. gRPC in entroduced fully at `rpc.gonka.gg:9090`. 

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/CSmL1FINRVnfLrY.png)

[https://rpc.gonka.gg](https://rpc.gonka.gg) · [https://rpc.gonka.gg/endpoints](https://rpc.gonka.gg/endpoints) · [https://rpc.gonka.gg/health](https://rpc.gonka.gg/health)

Point at `https://rpc.gonka.gg`. Chain JSON-RPC, Cosmos REST, transaction lookup, block feed, address history, slashing, the hardware registry, and epoch performance sit behind that one host. A response still carries `X-Rpc-Node` with the public name of the node that answered.

The public chart keeps 30 days. Oct 19–21 has rolled off it, so those three days are not in the total. From Oct 22 through Nov 19, 29 days:

- **112.1M** gateway requests
- About **3.87M** a day
- Peak day **Nov 13: 4.82M**
- Nov 13–19: **31.4M**
- About **64** requests/second on the morning of Nov 20

Report #4 was 84.1M across the 25 days from Sep 24, peak 3.84M on Oct 5, about 40 requests/second, with the homepage near 44 req/s at the close of Oct 18. The daily rate is now higher, and the peak day is higher. 

The homepage is the same three pictures: a live request rate, the last 60 minutes, and requests per day with a 7 / 30 day switch. Hover a bar for the count. The count is gateway traffic, including anonymous calls. It does not include the public pages themselves.

### Compound Routing Map (CRM).

Some time during the reports scope period, one Feather node stopped answering. Keplr and anything else pinned to a single dead backend saw timeouts. From that time on, the system has **smart "compound" routing map (CRM)**: it automatically checks all the available upstream nodes, under each node it checks every api path needed by clients and build a comprehensive in-memory map of which exact api route / method is available at which upstream from the pool. If one upstream is up but *some api routes* are not responding this at this exact upstream (node / participant) - it will not be excluded from the pool completely, only the affected routes / methods will be marked degraded and other nodes will compensate just that leaving the total traffic split honest and stable accross the whole pool. The rule from report #4 still holds for old transactions: `/chain-api` prefers Feather, and community nodes are the fallback only after Feather cannot serve the height. 

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/4yNBBBu0RCLN51V.png)

That evening `/v1/epochs/current/participants` returned 404, "active participants not found", including for older epochs, while a single upstream still had the current epoch and the other RPC routes were returning 200. The gateway was answering from a node that had not caught the epoch the rest of the pool had. That route started answering again thanks to CRM and later fully caught up. A current-epoch participant read on Nov 20 returns the set correctly.

gonka.gg's indexer sends its chain reads 100% to rpc.gonka.gg now. 

The tx index behind address and hash lookup holds **120.6M** transactions as of the morning of Nov 20. Hardware snapshots in that store are past 1 billion rows. Epoch performance and slashing sit beside them. Complex reads (an address page, a hardware history) come from that index. The raw node is the fallback, not the first stop.

## 5. G-Meter

[https://meter.gonka.gg](https://meter.gonka.gg) · [https://meter.gonka.gg/compare](https://meter.gonka.gg/compare)

meter.gonka.gg probes public Gonka brokers on a timer (quick checks, limits about hourly) and shows who is up, how slow, and what it costs. Report #3 added eterial.ai, GLM-5.3 Flash, and compare-at-the-lowest-Gonka-rate. Report #4 gave every view a URL, a page per broker with the public gateway volume from gonka.gg, share cards on links, and spaced the quick check so a small RPM cap is not scored as downtime. A quick check is about 30 chat calls, spaced, roughly once an hour. A cap at 40 or 60 is enough. Kimi is off the pills. Trends, Providers, and Compare stay on MiniMax, DeepSeek, and GLM.

### Compare, as an API

The compare page was joining two feeds in the browser. It is one public response now.

[https://meter.gonka.gg/api/compare](https://meter.gonka.gg/api/compare)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/c6RRtk6e7t9wuWX.png)

The same payload is at `/api/metrics/compare`. Prices are USD per 1M tokens. Gonka's rate is the lowest broker price from the latest check, which is what the page divides by. The market side is the OpenRouter average used for the multiplier, plus the median drawn on the track. Each model includes the Gonka low, high, and average, the market average and median, and the provider rows behind those averages. A partner page can render the comparison without scraping the HTML.

### What a broker page claims

A broker page lists the models that were actually probed. One broker wrote in because their page read as if MiniMax-M2.7 were the only model on the bench, while they serve the lineup. The page now says which models the check covered. All model-list inconsistencies accross brokers were solved and lists are now unified.

Also, new Brokers are on the board. 

If the broker is an OpenBroker user, the broker page includes that broker's own OpenBroker usage. The same split as report #4:

- A devshard operator (allowlisted wallet, own escrow gateway) gets that gateway's inferences and tokens.
- Proxy and OpenBroker are split. The page uses each product's own total, not the combined Gonka Labs row on the inference tab.
- Someone who only rides OpenBroker gets their own usage inside OpenBroker.

## 6. Pulse

[https://pulse.gonka.gg](https://pulse.gonka.gg)

Pulse is the public feed of Gonka mentions and official posts. Report #1 launched it. Later reports added units on the charts, sentiment against the fear-and-greed style read, the news mix, and catch-up that does not spike a quiet day into a fake peak. This month added new web sources and stopped cropping pictures.

### Two more web sources

Added this month, as web posts:

- **A new news source from the community portal -** the weekly editions, dated by the edition week. The collector picked up 18 editions. The latest in the feed at the time of the change was the October 24 roundup.
- **gonka.ai** - dated posts from the network updates page. 133 dated posts were collected, including the October 17 note on wider PoC coefficient ranges. 

Everything is shown on the web source. In the news list they sit with the other official digests, a couple at a time, so independent articles still lead the page.

### Pictures

Post pictures scale to the card width and keep their own height. The full frame stays visible. YouTube thumbnails were being sliced to a tall crop, which cut off the title burned into the preview. The whole image shows. The same rule applies to the other sources. A wide preview stays wide. A square one stays square.

## 7. In finishing

The shipped list above is what a User can open today. It is not the whole month.

A new major product is in the finishing stages. Large one. What did land, in public, is the ground under it.

The finishing work continues. The public release of each product will be its own note, with a link, when the last pass is done. This report stays with what is already open.

***

*Still working to make Gonka Labs products better while creating new ones. Hardening infra under real load, polishing what already shipped, and bringing the products in finishing across the line. More updates as they land.*

## Links

Last report: [Monthly Report No.4](https://github.com/gonka-ai/gonka/discussions/2059)

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
