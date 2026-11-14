---
title: "#2267 — [Proposal] Lightweight TypeScript CLI for Automated Ethereum Bridge Epoch Synchronization"
source: https://github.com/gonka-ai/gonka/discussions/2267
discussion_number: 2267
category: protocol-improvements
synced_at: 2026-11-14T16:58:52Z
---

> 🔄 **Auto-sync:** from [Discussion #2267](https://github.com/gonka-ai/gonka/discussions/2267) every hour. 

# [Proposal] Lightweight TypeScript CLI for Automated Ethereum Bridge Epoch Synchronization

**Автор:** [@kakavaanen](https://github.com/kakavaanen) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-14 13:58 UTC · **Обновлено:** 2026-11-14 13:58 UTC

---

## 📝 Описание

**Motivation**
Currently, submitting epoch updates to the Ethereum BridgeContract requires using the `submit-epoch-public.js` script located in `proposals/ethereum-bridge-contact/`. 

This process has several bottlenecks:
1. It requires a full Hardhat installation and Solidity compilation just to read an ABI.
2. It requires the operator to manually query the Gonka API (`/epoch_data` and `/signing_history`), manually copy-paste the Base64 keys, and pass them as CLI arguments.
3. It is single-shot. If the bridge falls 5 epochs behind, the operator must run the script 5 times, waiting for Ethereum confirmations in between.
4. It crashes if the Gonka chain hasn't reached the target epoch yet, rather than exiting gracefully.

**Proposed Solution**
I propose building a lightweight, standalone TypeScript CLI (`@gonka/bridge-sync`) that automates the entire process without any Hardhat dependencies. 

The tool will:
* Use `ethers` and `@noble/curves` to handle all ABI interactions and EIP-2537 BLS conversions natively.
* Automatically query the Gonka REST API for the `group_public_key` and the `final_signature` from the signing history.
* Run a catch-up loop: reading the contract's latest epoch, fetching the data for `latest + 1`, submitting the transaction, and waiting for confirmation, repeating until the bridge is fully synced.
* Handle edge cases: gracefully exiting if the Gonka chain hasn't reached the target epoch (HTTP 404), and alerting if the bridge enters ADMIN_CONTROL mode (30-day timeout).

**Proof of Concept**
I have already built and tested the core logic locally. It successfully:
* Fetches the current epoch from the smart contract (`0x972a7a92d92796a98801a8818bcf91f1648f2f68`).
* Queries the Gonka API for the next epoch's BLS data.
* Converts the Base64 keys to EIP-2537 hex using `@noble/curves`.
* Generates the exact encoded transaction payload (`0x969731f6...`) required by `submitGroupKey`.
* Handles the 404 edge case when the chain hasn't produced the next epoch yet.

**Deliverable**
A public npm package and CLI script (`npx gonka-bridge-sync --rpc <url> --key <pk>`) that vastly improves the operational experience for bridge maintainers and validators.

I am looking for feedback from the community and Hosts before opening a PR.
