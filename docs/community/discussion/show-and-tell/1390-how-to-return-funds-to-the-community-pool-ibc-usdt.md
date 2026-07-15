---
title: "#1390 — How to return funds to the Community Pool (IBC USDT)"
source: https://github.com/gonka-ai/gonka/discussions/1390
discussion_number: 1390
category: show-and-tell
synced_at: 2026-07-15T19:32:41Z
---

> 🔄 **Auto-sync:** from [Discussion #1390](https://github.com/gonka-ai/gonka/discussions/1390) every hour. 

# How to return funds to the Community Pool (IBC USDT)

**Автор:** [@paranjko](https://github.com/paranjko) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-07-03 04:52 UTC · **Обновлено:** 2026-07-03 04:52 UTC

---

## 📝 Описание

A while back I was helping the DeAI Nation folks with their proposal. Their event ended up being cancelled, and to their credit they decided to do the right thing and return the granted funds to the Community Pool.

Turns out there was no guide for that. The tricky part: their grant was paid out through a governance proposal, and USDT on Gonka comes out of the USDT treasury contract — there is no way to simply send it back into that contract. So where do the funds go? The answer is the Community Pool via `fund-community-pool` (note that a plain bank send to the distribution module address will **not** credit the pool either). We figured it out about a month ago, and I finally found the time to write it down properly.

Sharing the instruction below in case anyone else ever needs it. Hopefully returning funds in cases like this stays the norm in our network.

_By the way, check out their [DeAI Dashboard](https://dashboard.deaination.com): they track decentralized AI networks side by side, Gonka included!_

---

## Returning IBC USDT to the Gonka Community Pool

These instructions are for returning IBC USDT funds (originally received via governance proposal) back to the Gonka community pool.

> **Public Endpoints:**
> - **RPC**: `https://node3.gonka.ai/chain-rpc/`
> - **API**: `https://node3.gonka.ai/chain-api/`

### Step 1: Verify Your Balance

First, confirm that your wallet holds the IBC USDT funds:

```bash
curl https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/<YOUR_GONKA_ADDRESS>
```

Look for a balance with the denom:

```
ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4
```

The amount shown is in **micro-USDT** (6 decimal places). For example, `1000000` = 1 USDT.

### Step 2: Fund the Community Pool

> **Important:** Before returning the full amount, test the flow with a small amount first.
>
> Chain behavior, CLI syntax, endpoints, gas settings, and wallet support may change over time. Send a small test transaction, verify that it appears in the Community Pool, and only then return the remaining funds.

Use the `inferenced` CLI to send the funds to the community pool:

```bash
inferenced tx distribution fund-community-pool \
  <AMOUNT>ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4 \
  --from <YOUR_KEY_NAME_OR_ADDRESS> \
  --chain-id gonka-mainnet \
  --node https://node3.gonka.ai/chain-rpc/ \
  --gas auto \
  --gas-adjustment 1.4 \
  --gas-prices 0.025ngonka \
  -y
```

**Replace:**

- `<AMOUNT>` — the exact amount in micro-USDT (e.g. `5000000` for 5 USDT)
- `<YOUR_KEY_NAME_OR_ADDRESS>` — your local key name or full `gonka1...` address

> Note: you need a small amount of `ngonka` in your wallet to pay for gas fees.

### Step 3: Verify the Deposit

After the transaction is confirmed, verify that the USDT balance in the community pool increased:

```bash
curl https://node3.gonka.ai/chain-api/cosmos/distribution/v1beta1/community_pool
```

Expected response — the IBC USDT amount should have increased by the amount you sent:

```json
{
  "pool": [
    {
      "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
      "amount": "<UPDATED_POOL_AMOUNT>.000000000000000000"
    },
    {
      "denom": "ngonka",
      "amount": "<CURRENT_NGONKA_POOL_AMOUNT>"
    }
  ]
}
```

Tip: run the same query **before** sending to note the starting pool balance, so you can confirm the increase.

### Notes

- This guide reflects the process that worked at the time of writing. Always test with a small amount first and verify the transaction before sending the full amount.
- The `fund-community-pool` transaction is **irreversible** — once sent, the funds are in the community pool and can only be spent via a governance proposal.
- Do **not** send funds directly to the distribution module address (`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`) with a regular bank transfer — that will not credit the community pool. Always use `fund-community-pool`.
- If you do not have the `inferenced` binary, you can use any Cosmos-compatible wallet (e.g. Keplr with a custom chain configured for `gonka-mainnet`) to construct and sign the `MsgFundCommunityPool` transaction.

