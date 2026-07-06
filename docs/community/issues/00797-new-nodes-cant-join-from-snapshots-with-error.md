---
title: "#797 — New nodes can't join from snapshots with error"
source: https://github.com/gonka-ai/gonka/issues/797
issue_number: 797
synced_at: 2026-07-06T09:52:48Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #797](https://github.com/gonka-ai/gonka/issues/797) каждые 6 часов. 

# 🔴 New nodes can't join from snapshots with error

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-02-24 19:35 UTC · **Обновлено:** 2026-02-25 17:50 UTC

**Метки:** `help wanted` `up-for-grabs` `Priority: High`

---

## 📝 Описание

**This is an urgent, open issue, and many contributors are working on it in parallel.**

There is a quite weird issue today - new nodes can't join from snapshots with error like that:
```
5:49AM ERR error in proxyAppConn.FinalizeBlock err="no validator signing info found" module=consensus
```
[no-validator-signing.log](https://github.com/user-attachments/files/25529057/no-validator-signing.log)

Seems like there is no signing info in snapshot. But that issue happens with different set of peers for state sync (pex=false) and seems reproducable in most cases 

Experiment was done to ignore this issue in cosmos-sdk and them it fails like the state doesn't have slashing params also 

Seems like active nodes had all this data at the state at this height 

How to reproduce it - to start new node, it is likely you get it (it passes with some snapshots, which makes everything even stranger)

main hypothesis that something is with producing snapshots, it's cosmo-sdk level

There is also a hypothesis that it is somehow connected to slashing, as it started to happen when collateral was activated. But we are not sure.

it happens the same block the validator list usually updated.

Also, collateral needs to be checked. 

---

## 💬 Комментарии (5)

### Комментарий 1 — [@hleb-albau](https://github.com/hleb-albau)

*2026-02-24 19:53 UTC*

As a workaround(before fix), it is possible to just compress data folder(except some filers) and distribute it as is archive. Quite popular in cosmos world. See https://snapshots.osmosis.zone/index.html as example

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-02-24 20:11 UTC*

@hleb-albau thanks, that makes sense and it’s a well-known approach in the Cosmos ecosystem. You are right, it’s more of an operational workaround than a real fix (it doesn’t address the underlying issue we’re trying to solve)

### Комментарий 3 — [@blizko](https://github.com/blizko)

*2026-02-24 21:35 UTC*

Additional feedback:
The issue was observed before collateral slashing was activated. During epoch 179 have been observing same error.
Known failed attempt time around Feb 21st 01:47 UTC

### Комментарий 4 — [@x0152](https://github.com/x0152)

*2026-02-24 23:49 UTC*

The issue is in [cosmos/iavl v1.2.4](https://github.com/cosmos/iavl/tree/v1.2.4)

After snapshot restore, IAVL rebuilds a "fast node" index by iterating the tree. If the iterator hits an error mid-way, it silently stops - the error is never stored ([iterator.go:230-235](https://github.com/cosmos/iavl/blob/v1.2.4/iterator.go#L230-L235)). The fast index ends up incomplete, but IAVL marks it as ready

Then when the node starts processing blocks, `Get()` checks the fast index, doesn't find the key, and assumes it doesn't exist - without checking the actual tree ([immutable_tree.go:192-198](https://github.com/cosmos/iavl/blob/v1.2.4/immutable_tree.go#L192-L198)). The data is in the tree, but the code never reaches it

That's why slashing module gets `nil` -> `no validator signing info found` -> crash

The exact error that triggers the iterator failure is still unknown - since IAVL swallows it, there's no way to see it without patching the code

**Workaround (was found by @gmorgachev):** setting `iavl-disable-fastnode = true` on the same snapshot - works immediately. This skips the fast index and reads the tree directly

### Комментарий 5 — [@tcharchian](https://github.com/tcharchian)

*2026-02-25 17:50 UTC*

https://gonka.ai/FAQ/#how-do-i-fix-errno-validator-signing-info-found-when-starting-from-a-state-sync-snapshot
