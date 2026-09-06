---
title: "#1711 — Gonka Labs: Gonka Chat - Wallet-to-Wallet messaging on Gonka"
source: https://github.com/gonka-ai/gonka/discussions/1711
discussion_number: 1711
category: show-and-tell
synced_at: 2026-09-06T23:46:51Z
---

> 🔄 **Auto-sync:** from [Discussion #1711](https://github.com/gonka-ai/gonka/discussions/1711) every hour. 

# Gonka Labs: Gonka Chat - Wallet-to-Wallet messaging on Gonka

**Автор:** [@gonkalabs](https://github.com/gonkalabs) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-09-03 00:42 UTC · **Обновлено:** 2026-09-03 00:43 UTC

---

## 📝 Описание

Hey! Gonka Labs here.

On September 1st, we shipped [Gonka Chat](https://chat.gonka.gg) - an open-source wallet-to-wallet messenger for Gonka. 
You write a `gonka1...` address or a `.gnk` (GNS, https://gonka.gg/names) name the same way you'd write a handle. No new account. **The wallet is the identity.**


https://github.com/user-attachments/assets/9cba802d-2891-48a0-a4ef-b4b5881a4f55



### The problem

Most web3 ecosystems already have some form of wallet chat. Solana, Ethereum, Coinbase - same pattern, for the same reason.

On a chain, people are addresses. That is fine until you need to talk to one.

- You sent GNK to the wrong person and need it back.
- You want the operator of a specific node, not a Discord nickname that may or may not be them.
- You are looking at an address on the explorer and there is no "message this wallet" button.
- A group of validators / builders needs a room that is tied to wallets, not emails.

Today the workaround is: paste the address into Telegram, ask in Discord, hope someone recognizes it. That is slow, and it is not how the rest of the stack works. Transfers, names, explorers - those already speak `gonka1...`. Chat should too.

That is the product. Text as a native part of using Gonka, not a side channel.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/3cZprpGoNZvtBox.png)

### Why we built our own

We did not take a ready-made messenger and glue a wallet login on top. Those stacks assume usernames, phone numbers, or a vendor account. Gonka already has an identity layer: the address, plus an optional `.gnk` name.

So we wrote the mailbox, the auth, and the crypto against that.

- Sign-in is an ADR-036 signature. Nothing is spent. Gas is not involved in sending either.
- A second signature (`Gonka Chat encryption key v1`) seeds a per-wallet NaCl box key. Same wallet on another browser = same inbox, same keys. You are not copying a chat backup around.
- Messages and files encrypt in the browser (TweetNaCl, XSalsa20-Poly1305) before they leave the device.
- Each conversation has a room key that never goes out in the clear. The mailbox only stores a wrap: the room key boxed to each member's encryption pubkey. You open a chat once, unwrap, and you are in.
- Ciphertext (message bodies and attachments) lives in Storj. Index on our side is also fully encrypted - who is in the room, pointers, delivery - not a folder of readable chats.

Until both wallets have been on the service and the room key is in place, the payload is still ciphertext. We do not keep a plaintext copy "just in case.", everything is encrypted.

### How sign-in works

1. The app asks `window.gonkaWallet` or `window.keplr` for the address.
2. You sign an ADR-036 login message. That proves the `gonka1...` is yours. No tx, no fee.
3. You sign the encryption-key message. We SHA-256 that signature and derive the box keypair from it. Deterministic, per wallet.
4. The session cookie is just "this browser is that address." Devices show up in the profile so you can kick one if a laptop walks away.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/oJGdO3F5lqPTv6Y.png)

If you have used GG Wallet against gonka.gg or the playground, this is the same provider story. Keplr works the same way on `gonka-mainnet`.

### How a message is sent

**Simplified**:

1. Browser loads (or creates) the room key for that conversation.
2. Plaintext + optional file metadata is packed, then `secretbox`'d with the room key. Attachments are boxed the same way and uploaded as opaque bytes.
3. The mailbox gets ciphertext + nonce. If Storj is on, the body object goes there and the DB keeps a pointer.
4. The other side polls the mailbox, pulls the object, unwraps the room key if they do not have it yet, and opens the box on their device.

![](https://resource.inkdown.me/assets/11g/tk4ZX4b2sHaSu/mLru5zEiN5v7Od6.png)

*(In case you want to verify, you can click "Packets" button at the top bar of the website. It will show all the incoming and outgoing traffic and you can verify that encryption is done ON DEVICE before packet is sent out).*

You can send first. They do not have to be online. They connect that wallet later, you open the chat once so their wrap exists, and they can read.

Groups and channels use the same room-key model. Adding someone to a group or channel creates an invite - the room does not appear in their inbox until they join. DMs are just the two addresses.

<img width="1244" height="919" alt="Screenshot 2026-09-03 at 3 39 54 AM" src="https://github.com/user-attachments/assets/8044f429-a748-46e1-9ac5-60f7d27b9831" />



### What you get

| Piece        | What it actually does                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------- |
| Direct chat  | Message any `gonka1...` or `.gnk`. Address is enough.                                              |
| Groups       | Multi-wallet rooms. Invites, not a silent force-add.                                               |
| Channels     | Broadcast rooms. Admins post, everyone else reads.                                                 |
| Handles      | Share `@squad`. Mentions are clickable.                                                            |
| Files        | Images, video, attachments. Fully Encrypted on this device, same as text.                          |
| Replies      | Quote the original, jump back to it.                                                               |
| Multi-device | Same wallet, another browser. Encryption key comes from the signature, not from a file you export. |
| Block        | Cut an address off if you do not want the thread.                                                  |
| Deep link    | `https://chat.gonka.gg/app?with=gonka1...` - connect if needed, then open or create the DM.        |

`.gnk` (GNS Names, https://gonka.gg/names) is optional. You do not need a name to be reachable. If you have one, it shows up as the label. Same name layer as GG Wallet and gonka.gg.

### Why this is useful on Gonka specifically

Explorer, wallet, names, and now chat all point at the same object: the address.

That is not "yet another DM app." If you can pay an address, you should be able to write it. If you can look an address up on gonka.gg, you should be one click from a thread. If a name resolves to a wallet, that name should work in the composer too.

For node ops and anyone running public infrastructure this is practical. The address on the dashboard is the contact method. No "find me on Telegram" footnote.

Outreach is free and off-chain for everyone. You are not paying gas to say hello, and you are not publishing the message on-chain. Everyting is End-To-End encrypted and stored in the distributed / decentralised storage.

### Open source

MIT, same as the rest of what we ship. 

Source Code: [https://github.com/gonkalabs/gonka-chat](https://github.com/gonkalabs/gonka-chat)

Read the sign-in path and the room-key wrap code if you care how keys move. If something looks wrong, please - open an issue and lets make it better together!

### What's next

Gonka Chat will land in the other Gonka Labs surfaces so you do not have to remember a separate URL every time:

- gonka.gg explorer - write the address you are already looking at
- GG Wallet - chat from the wallet you already use
- Gonka Names - `.gnk` as a chat handle, not only a send target

And many other application layers!

The deep link is already there if you want to wire it from your own tool: `https://chat.gonka.gg/app?with=<address>`(or your domain if you selfhost).

### Try it

1. Open [https://chat.gonka.gg](https://chat.gonka.gg)
2. Connect GG Wallet or Keplr
3. Paste a `gonka1...` or a `.gnk` name
4. Write to someone!

Would love feedback, feature requests, and bug reports. If you use it for node ops, a validator room, support, or just to reach someone you only know as an address - feel free to share your experience in this thread! We would love to hear about application cases!



### Links

- Live: [https://chat.gonka.gg](https://chat.gonka.gg/)
- Srouce code: [https://github.com/gonkalabs/gonka-chat](https://github.com/gonkalabs/gonka-chat)
- Gonka Labs: [https://gonkalabs.com](https://gonkalabs.com)
- Chat: [https://t.me/gonka_gg](https://t.me/gonka_gg)
- Announcements: [https://t.me/gonkalabs](https://t.me/gonkalabs)
