---
title: "#1710 — Gonka Labs: x402 on Gonka - payments for Agents"
source: https://github.com/gonka-ai/gonka/discussions/1710
discussion_number: 1710
category: show-and-tell
synced_at: 2026-09-04T22:18:44Z
---

> 🔄 **Auto-sync:** from [Discussion #1710](https://github.com/gonka-ai/gonka/discussions/1710) every hour. 

# Gonka Labs: x402 on Gonka - payments for Agents

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-09-03 00:10 UTC · **Обновлено:** 2026-09-03 00:12 UTC

---

## 📝 Описание

Hey! Gonka Labs here.

At 26th of August we introduced x402 on Gonka: [https://x402.gonka.gg](https://x402.gonka.gg)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/E2MWThZKmaHh7Og.jpg)

x402 is an open payment standard for AI agents. It was started by the Coinbase team and is now run by the independent x402 Foundation under the Linux Foundation. The idea is simple on purpose. An agent makes a micropayment in stablecoins (almost always USDC) and gets the resource it asked for. No signup, no API keys, no checkout page. The payment sits inside the request itself, the same way data already moves over HTTP.

That is why people call it a native way to move value on the internet. Same shape as a normal GET, just with a bill attached.

### The problem

People pay with a card and a login. A program can't. It has no cabinet and no "Pay" button. It needs to buy one API response, one model call, one file - in the same request - and move on.

Without a standard like this, an agent either cannot buy a Gonka-priced service, or a human pays for it by hand. Sellers have the other mess: watch the chain, wait for inclusion, then serve. Most HTTP APIs do not want to be a wallet.

So you get prepaid credits, API keys, custom invoices. Fine for a dashboard. Useless if the caller is a script that only speaks HTTP.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/OQBIsjN52wAJeqh.png)

### What we run

`x402.gonka.gg` is the public middle piece. The client signs locally. We only broadcast. We do not hold funds.

Flow, short version:

1. Client hits a paid URL like any other HTTP call.
2. Server answers `402 Payment Required` with network, asset, amount, and `payTo`.
3. Client signs a Gonka transfer and retries with `PAYMENT-SIGNATURE`.
4. Seller calls `POST /settle` here. Tx goes on-chain. Then the resource is served, plus a `PAYMENT-RESPONSE` with the hash.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/g0NRChIdMC5Bg0c.png)

(read more about agent / buyer + seller lifecycle at https://x402.gonka.gg/agents and https://x402.gonka.gg/sellers)

Settlement is upfront: money moves first, then you get the thing. Source is on the website (git hosting is temporarily down, use the tarball).

### How to try it

1. Open [https://x402.gonka.gg](https://x402.gonka.gg)
2. On Get started, request `/demo`. You should get HTTP 402 with the payment terms.
3. Download the source from the same site.
4. Pay from your own address:

````
go run ./cmd/x402-gonka pay --key "$GONKA_PRIVATE_KEY" --url https://x402.gonka.gg/demo
````

The key stays with you. For USDC add `--asset usdc`.

Sellers: return 402 with your `accepts`, then `POST /settle` on `x402.gonka.gg` after the client retries. You do not talk to the chain yourself. Same hook works for a shop, another agent, or a broker that wants agents to buy from it.

(read full tutorial at https://x402.gonka.gg/get-started)

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/yUckpolceOlcnZ4.png)

### What you get

- Public facilitator at [https://x402.gonka.gg](https://x402.gonka.gg) - docs, `/supported`, `/verify`, `/settle`, `/demo`.
- GNK (`ngonka`) and Ethereum-bridged Circle USDC (CW-20 on Gonka).
- No accounts, no API keys, no custody.
- Client signs the full tx. We only broadcast.
- Open source. `go run` from the tarball on the site.
- EN / RU / ZH docs.

### It already settled

Here is a demo transaction that is paid under`/demo` in GNK. 1000 ngonka, height 5745133, code 0.

- Payer: `gonka150c4lsmsdr23vly466lskajkfhqh7eghmyjern`
- Tx: [https://gonka.gg/tx/23B76D1281F9EFCC7AFC90659480CF3219A7099959C0513720769F700E9B73B2](https://gonka.gg/tx/23B76D1281F9EFCC7AFC90659480CF3219A7099959C0513720769F700E9B73B2)

The exact commands and the RPC checks are on [https://x402.gonka.gg/get-started#proof](https://x402.gonka.gg/get-started#proof)



**Would love feedback, feature requests, and bug reports. If you put a real paid route behind this (broker, API, your own agent), drop it in the thread or publish to Resource listing so others can see and use it - https://x402.gonka.gg/resources**

### Links

- Docs + demo: [https://x402.gonka.gg](https://x402.gonka.gg)
- Source instructions: https://x402.gonka.gg/source
- Srouce code: https://github.com/gonkalabs/x402-gonka
- Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)
- Chat: [https://t.me/gonka_gg](https://t.me/gonka_gg)
- Announcements: [https://t.me/gonkalabs](https://t.me/gonkalabs)
