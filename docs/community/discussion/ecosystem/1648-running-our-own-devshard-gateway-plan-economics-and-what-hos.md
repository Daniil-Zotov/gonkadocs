---
title: "#1648 — Running our own devshard gateway — plan, economics, and what hosts want to see for allowlisting"
source: https://github.com/gonka-ai/gonka/discussions/1648
discussion_number: 1648
category: ecosystem
synced_at: 2026-09-05T00:51:22Z
---

> 🔄 **Auto-sync:** from [Discussion #1648](https://github.com/gonka-ai/gonka/discussions/1648) every hour. 

# Running our own devshard gateway — plan, economics, and what hosts want to see for allowlisting

**Автор:** [@theaungmyatmoe](https://github.com/theaungmyatmoe) · **Категория:** :jigsaw: Ecosystem · **Создано:** 2026-08-25 12:18 UTC · **Обновлено:** 2026-08-29 03:39 UTC

---

## 📝 Описание

# Running our own devshard gateway — plan, economics, and the one thing we need from hosts

**Who:** Fusion AI Gateway (`api.fusioncode.app`) — a production broker already serving DeepSeek V4 Flash, MiniMax M2.7, and Kimi K2.6 through the network (currently via OpenBroker).

## Why we want our own gateway

1. **Direct GNK settlement & self-custody** — we have a committed multi-billion-token/day pipeline and need escrow pooling/rotation/settlement under our own control.
2. **The price gap** — the network's on-chain rate is **1 ngonka/token (0.001 GNK/M)**; a broker layer currently marks this up ~15x. Running our own `devshardctl` gateway removes that layer entirely.
3. **Capacity & cache affinity** — broker-side concurrency limits and global load-balancing have surfaced under sustained load; escrow-bound sessions give us better control (and eventually host affinity for prefix reuse).

## What we've done so far

- **Allowlist request filed:** #1637 — dedicated escrow creator address, generated + kept unfunded until membership is confirmed (per the gateway guide).
- **Staged deployment plan:** gateway-only container on an existing VPS, public node endpoints, single escrow → functional checks → concurrency ramp (1→3→10→25→50→100→200) → multi-escrow pooling + rotation → production cutover.
- **Contribution plan:** we'll publish anonymized capacity/TTFT/settlement results back to the community.

## The one thing we need from hosts

Per the process for #1479, allowlist inclusion is an **on-chain governance decision**, and the strongest signal is **support from active hosts**. So we're asking directly:

**What evidence, operational commitments, or safeguards would you want to see from a broker before supporting its creator address in the next allowlist batch?**

- Load-test results against the current network?
- Settlement/refund transparency commitments?
- A cap on concurrent escrows or requests?
- Anything else that de-risks it for hosts?

## Related

- Allowlist request: https://github.com/gonka-ai/gonka/issues/1637
- Cache-served token pricing proposal: https://github.com/gonka-ai/gonka/discussions/1636
- Cache telemetry PR (prerequisite for cache pricing): https://github.com/gonka-ai/gonka/pull/1633

Happy to answer any questions here or in `#dev-chat`.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-08-29 02:10 UTC*

Hi @theaungmyatmoe! Allowlisting is an on-chain governance decision, so the real question is what earns host support.

The thing most likely to move hosts right now: attribution. fusioncode.app doesn't mention Gonka anywhere, and that's come up in the community. A broker running on near-cost Gonka inference is only a net positive if it grows awareness of the network. Add clear "powered by Gonka" attribution (site, docs, where users see it) with a link back. This is just my own observation, not a requirement or any guarantee — hosts decide independently and attribution alone doesn't secure inclusion. Meanwhile OpenBroker stays the practical path (GNK-native, no governance wait, covers your volume).

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-29 03:18 UTC*

> I think I have talking too much about bringing the real users from my side
>
> I am closing some deal that can able to spend 500B to 4T monthly usage 
>
> So that at Gonka side they will get more users and more social presence if we could collaborate closely 
>
> I am currently using openbroker but for long term I like to run myself so that I can introduce more concrete features 
>
> Most of the web3 problems is not having real users and I am solving with a bunch of marketing done by me
>
> Without having to reduce the cost in my side I cannot make advertising properly in paid and viral way.
>
> That is why I am asking that 
>
> And the Gonka cannot even handle at least 100B per day and its destroying my design.
>
>
> I do even planning to make marketing right now by integrating Gonka and my dedicated hardwares 
>
> If I could get as a devshard I can put the Gonka as my provider so that Gonka will also get social presence in both side 
>
> And i bring non Russia users across Asia, US West, SEA but Gonka founders and core team is quiet 
>
> So what will be our deal to get my devshard properly 
>

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-29 03:39 UTC*

> Thanks @tcharchian — that feedback is helpful and very fair.
>
> We are completely aligned on attribution and growing network awareness
> - We have the "Decentralized inference accelerated by Gonka Network" docs page, provider overview, and footer backlinks prepared.
> - This will go live officially across our platform alongside our devshard gateway launch once our creator address is allowlisted.
> - We will also publish public throughput, TTFT, and prefix-cache benchmarks to showcase Gonka's capabilities under real-world multi-billion-token load.
>
> Our committed pipeline (500B to 4T tokens/month from coding assistants and autonomous agents across US West, SEA, and Asia) will bring massive real utility to the network. Running our own devshard gateway is critical for us to manage direct host session affinity and eliminate intermediary concurrency choke points.
>
> We're excited to partner with the Gonka ecosystem and look forward to participating in the upcoming allowlist governance batch!
