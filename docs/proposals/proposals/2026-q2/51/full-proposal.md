# Support Gonka's Presence at WebX Asia

**Status:** Governance proposal pending on-chain submission to `gonka-mainnet`
**Requested amount:** 75,000 USDT
**Recipient address:** `gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g`
**Voting period:** 48 hours after submission
**Submitted by:** 6Block

---

## Summary

6Block, a long-term Gonka mining and infrastructure participant, proposes allocating 75,000 USDT from the Community Pool to support Gonka's effective participation at WebX Asia / WebX 2026 in Tokyo. 6Block has already committed 50% of the needed 150,000 USDT of its own funds for the official Platinum sponsorship.

This community funding is crucial for covering essential event execution costs, including team travel, accommodation, booth production, materials, media support, and partner coordination. Without the additional funding, participation in the event is not possible. The objective is to maximize WebX's impact as a serious ecosystem growth opportunity for Gonka, a decentralized infrastructure for AI compute.

WebX is Asia's largest Web3 conference and is strategically relevant to Gonka, which operates at the intersection of Web3, AI, and decentralized networks. A professional presence is key to gaining visibility and connecting with potential GPU providers, developers, investors, and media in the Asian market.

This shared funding model ensures joint responsibility (6Block funds sponsorship, community funds execution), maximizing benefits like stronger public positioning and market recognition for the whole network. If approved, 6Block will receive the funds and provide a post-event summary covering execution and outcomes.

## On-chain Proposal Text

### Support Gonka's presence at WebX Asia

6Block proposes that the Gonka community allocate 75,000 USDT from the Community Pool to support Gonka's participation at WebX Asia / WebX 2026 in Tokyo.

6Block, a long-term Gonka mining and infrastructure participant, proposes allocating 75,000 USDT from the Community Pool to support Gonka's effective participation at WebX Asia / WebX 2026 in Tokyo. 6Block has already committed 50% of the needed 150,000 USDT of its own funds for the official Platinum sponsorship.

WebX is one of Asia's largest Web3 conferences and brings together Web3 companies, infrastructure providers, investors, developers, media, and policy-related participants from Japan and the global market. Gonka is already listed as a Platinum sponsor of WebX, creating a strong opportunity to increase visibility in Asia and reach GPU providers, miners, infrastructure partners, developers, exchanges, investors, and media.

If approved, the funds will be transferred to 6Block's designated wallet and used for event execution related to Gonka's WebX presence. 6Block will provide a post-event summary to the community.

**Requested amount:** 75,000 USDT.

## On-chain Execution Details

**Proposal JSON:** [`proposal.json`](./proposal.json)

This proposal uses `wasm/MsgExecuteContract` to invoke the `withdraw_ibc` entrypoint on Gonka's `community-sale` contract, transferring USDT to the recipient address. This mirrors the execution pattern of previously approved proposal [#42](http://node1.gonka.ai:8000/dashboard/gonka/gov/42) ("Support Gonka at Global Compute Sovereignty Summit").

| Field | Value |
|---|---|
| Message type | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| Contract | `gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2` (community-sale) |
| Contract admin | `gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33` (gov module) |
| Denom | `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` (USDT, 6 decimals, IBC from Kava) |
| Amount | `75000000000` base units = **75,000 USDT** |
| Recipient | `gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g` (6Block) |

## Post-Event Reporting

6Block commits to publishing a post-event summary in this repository covering execution outcomes, expense breakdown, and follow-up actions following Gonka's participation at WebX 2026.

## About 6Block

6Block, a long-term Gonka mining and infrastructure participant, proposes allocating 75,000 USDT from the Community Pool to support Gonka's effective participation at WebX Asia / WebX 2026 in Tokyo on July 13-14.
