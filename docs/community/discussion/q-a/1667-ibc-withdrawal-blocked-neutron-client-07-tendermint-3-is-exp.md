---
title: "#1667 — IBC withdrawal blocked: Neutron client 07-tendermint-3 is expired"
source: https://github.com/gonka-ai/gonka/discussions/1667
discussion_number: 1667
category: q-a
synced_at: 2026-09-03T05:41:15Z
---

> 🔄 **Auto-sync:** from [Discussion #1667](https://github.com/gonka-ai/gonka/discussions/1667) every hour. 

# IBC withdrawal blocked: Neutron client 07-tendermint-3 is expired

**Автор:** [@xX-mabster-Xx](https://github.com/xX-mabster-Xx) · **Категория:** :interrobang: Q&A · **Создано:** 2026-08-28 13:45 UTC · **Обновлено:** 2026-09-01 16:54 UTC

---

## 📝 Описание

Hello,

I am unable to withdraw my funds from Gonka to Neutron.

The transfer fails with:

failed to execute message; message index: 0:
cannot send packet using client (07-tendermint-3)
with status Expired: client is not active

Wallet:
gonka1s8qkncfz06ke5ns6x3cw57mqj83hywj3fltv0n

Asset denomination:
ibc/4F64FF736B88BA8EA521D6D515D9652B7C23C903BF91ECEFB3991888F3C023F4

Route:

- Gonka: transfer/channel-3
- Neutron: transfer/channel-7423
- Chain ID: neutron-1
- Gonka client: 07-tendermint-3
- Neutron client: 07-tendermint-189

Both IBC clients currently show as expired, although both have allow_update_after_expiry=true. The channel itself still appears to be open.

Could you please help restore this IBC route so that users can withdraw their Neutron-origin USDT.axl from Gonka?

Thank you.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@Borjomik](https://github.com/Borjomik)

*2026-09-01 16:54 UTC*

Hi, thanks for laying it out so clearly, and sorry you've ended up in this spot.

That route has been out of service since April. Transfers sent through it don't complete, and there's nothing we can do from our side. I wish I had a better answer, and I'm sorry to be the one giving this one.

The tokens themselves are Neutron-origin and wrapped through Axelar, so it's worth raising it on their side, closer to where the asset came from. They'll have more visibility into it than we do.

For anything going in or out of Gonka from here on, please use the Uniswap channel.
