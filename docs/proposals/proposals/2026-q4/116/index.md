---
title: "#116 – Approve DevShard v6 and distribute bounty rewards"
description: "Devshard v6

This proposal adds v6 to the approved devshard versions and distributes contributor bounty rewards for the release. The existing v4.1 and v4.2 entries stay unchanged.

The main change in "
template: proposals-proposals-main.html
---

# #116 – Approve DevShard v6 and distribute bounty rewards

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-11T07:58:21.061917426Z"></span></div>

**Proposal ID:** `116`

**Type:** Batch Transfer With Vesting, Community Pool Spend, Execute Contract, Put Devshard Approved Version

**Submit:** 2026-11-09 07:58 UTC

**Voting:** 2026-11-09 07:58 UTC → 2026-11-11 07:58 UTC

**Proposer:** [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/devshard-0.2.x-v6/devshard/docs/release-0.2.16-v6.md](https://github.com/gonka-ai/gonka/blob/devshard-0.2.x-v6/devshard/docs/release-0.2.16-v6.md)

<div class="prop-funding-line prop-funding-line-voting">85,000 GNK · $69,425 · Community Pool · 85,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/116){:target="_blank"}

</div>

Devshard v6

This proposal adds v6 to the approved devshard versions and distributes contributor bounty rewards for the release. The existing v4.1 and v4.2 entries stay unchanged.

The main change in Devshard v6 is authenticated peer gRPC over HTTP/2 on InferenceUrl (Connect; HTTP/1.1 fallback while the host is still on the old wrapping). A peer authenticates once with Attach, then reuses one multiplexed connection for chat, Watch, and the other RPCs. Gzip on that path and per-peer / per-connection rate limits ride the same transport. The release also carries the Docker load-test harness plus security and performance patches. On testnet load tests, sustained RPS improved by roughly 30–50% versus the previous line. Steady-state memory is lower, and catch-up no longer spikes process memory: diffs are paged (at most 64 nonces / 8 MiB per read) and the gateway sends at most 200 diffs per chunk instead of holding the whole journal.

## Proposal

Update the approved devshard versions and pay contributor bounties:

- Add `v6`, whose primary change is authenticated peer gRPC over HTTP/2, with the related transport, security, and performance work described in the release notes.
- Keep the existing `v4.1` and `v4.2` entries unchanged.
- Distribute 69,425 USDT and 85,000 vested GNK as described in the bounty estimation.

This update is approved through governance and does not require a full chain software upgrade.

## Full description and bounty

Full release description:
<https://github.com/gonka-ai/gonka/blob/devshard-0.2.x-v6/devshard/docs/release-0.2.16-v6.md>
(sha256 3341f999cb0fbea22d77d7e2514d6f05b2de5e2f1501690e711b0d3b934ab086)

Bounty distribution explanation:
<https://github.com/gonka-ai/gonka/blob/devshard-0.2.x-v6/devshard/docs/v6-bounty-estimation.md>
(sha256 f9fe513f23899091fd1cc498e9a8bdc7578383a60b9043c094391a2dab01fd88)

Release tag: <https://github.com/gonka-ai/gonka/releases/tag/devshard%2Fv6.0.0>

## Implementation

Register protocol `v6` via MsgPutDevshardApprovedVersion:

- Binary: `<https://github.com/gonka-ai/gonka/releases/download/devshard%2Fv6.0.0/devshardd.zip`>
- SHA-256: `531eb433392a56d009c14c63a74070cac410110f4c761437614af1a4360722e2`

The existing `v4.1` and `v4.2` binary URLs and checksums remain unchanged.

`versiond` downloads and verifies the approved binary and serves it under `/devshard/v6`. Host and gateway releases are built from the same v6 source. Gateways must use v6 escrows to use the new runtime.

## Bounty payouts

USDT total: 69,425 USDT (IBC USDT; aleksandr-cstl 300 omitted pending address).

- 10,000 USDT from the community pool via MsgCommunityPoolSpend (part of a-kuprin / akup).
- 59,425 USDT from the community-sale contract via withdraw_ibc.
- 85,000 GNK from the community pool into gov, then MsgBatchTransferWithVesting over 365 epochs (a-kuprin 30,000; qdanik 55,000).

Recipient amounts, exclusions, and rationale are in the bounty estimation document linked above.


---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:37.6%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (610,318)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 610,318 votes</span>
    <span class="prop-tally-yes-text">✓ Turnout <strong>37.6%</strong> (610,318 / 1,624,785) · Quorum <strong>25%</strong> (406,196)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl" target="_blank" class="prop-voter-addr">gonka1qwfrtz…33xdkl</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1q60h5av2pxe6gz3edmlcvd8p36vtj7r24fm43v" target="_blank" class="prop-voter-addr">gonka1q60h5a…4fm43v</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1pckmegery0q58lghaw4av9zl2fl4nw956zsyrs" target="_blank" class="prop-voter-addr">gonka1pckmeg…6zsyrs</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1rqm2u7lxzn7r68y0drcyhag6xnckpsnfmgd53t" target="_blank" class="prop-voter-addr">gonka1rqm2u7…mgd53t</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka19wskgkz4xwwxa9s80nfx4q97w2ucmcyfezmhjk" target="_blank" class="prop-voter-addr">gonka19wskgk…ezmhjk</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka190ey5n74v0wufy408yv0ggmpghctkvhxqfels3" target="_blank" class="prop-voter-addr">gonka190ey5n…qfels3</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka18x6wprs8c4x7awjgvn5t0e04fscrrash8rvmw4" target="_blank" class="prop-voter-addr">gonka18x6wpr…8rvmw4</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l" target="_blank" class="prop-voter-addr">gonka105ce44…2eza5l</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka10eg5wakkmc0tee3llwj2qwa67knzk48cht38c5" target="_blank" class="prop-voter-addr">gonka10eg5wa…ht38c5</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka133xdfvcyj2ccv38jrl0qjp970u9lz5plptfwuh" target="_blank" class="prop-voter-addr">gonka133xdfv…ptfwuh</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1k45p6gzq6970v9u650mdl5l4r34h9dvtz2gmxt" target="_blank" class="prop-voter-addr">gonka1k45p6g…z2gmxt</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2" target="_blank" class="prop-voter-addr">gonka168rtjf…lnkns2</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ue6k3pcgdg2g962l2n0g8hpg3r4vf827a4hpgh" target="_blank" class="prop-voter-addr">gonka1ue6k3p…a4hpgh</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ajmhqgvkf76hss5xe35kcnntqqhs7r8jz8s939" target="_blank" class="prop-voter-addr">gonka1ajmhqg…z8s939</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgPutDevshardApprovedVersion` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 3 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 4 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 5 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 6 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 7 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 8 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 9 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 10 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 11 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 12 | `/inference.streamvesting.MsgBatchTransferWithVesting` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.inference.MsgPutDevshardApprovedVersion",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "version": {
      "name": "v6",
      "binary": "https://github.com/gonka-ai/gonka/releases/download/devshard%2Fv6.0.0/devshardd.zip",
      "sha256": "531eb433392a56d009c14c63a74070cac410110f4c761437614af1a4360722e2"
    }
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56",
    "amount": [
      {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "10000000000"
      }
    ]
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "10000000000",
        "recipient": "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "14500000000",
        "recipient": "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "9000000000",
        "recipient": "gonka1vnupswg7qz2w5k5ax6zrp02mxmln6arnvjc87h"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "19125000000",
        "recipient": "gonka1frlfyz2wtltdy47dq3w9pwc8ruvjvlthp2lh53"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "5500000000",
        "recipient": "gonka15u0r3mf6t7zsfuslusnyt7hsjrq357yumpe8st"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "500000000",
        "recipient": "gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "300000000",
        "recipient": "gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "500000000",
        "recipient": "gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "85000000000000"
      }
    ]
  },
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30000000000000"
          }
        ]
      },
      {
        "recipient": "gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55000000000000"
          }
        ]
      }
    ],
    "vesting_epochs": "365"
  }
]
```

</details>
