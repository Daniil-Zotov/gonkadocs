---
title: "#1667 — IBC withdrawal blocked: Neutron client 07-tendermint-3 is expired"
source: https://github.com/gonka-ai/gonka/discussions/1667
discussion_number: 1667
category: q-a
synced_at: 2026-08-29T15:00:39Z
---

> 🔄 **Auto-sync:** from [Discussion #1667](https://github.com/gonka-ai/gonka/discussions/1667) every hour. 

# IBC withdrawal blocked: Neutron client 07-tendermint-3 is expired

**Автор:** [@xX-mabster-Xx](https://github.com/xX-mabster-Xx) · **Категория:** :interrobang: Q&A · **Создано:** 2026-08-28 13:45 UTC · **Обновлено:** 2026-08-28 13:45 UTC

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

