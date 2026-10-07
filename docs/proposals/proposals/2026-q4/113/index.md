---
title: "#113 – Distribute v0.2.16 bounty rewards"
description: "Bounty Payments Associated with v0.2.16

This proposal covers 104,150 USDT from community funds for development, research, infrastructure, security reporting, and code review work on the Gonka protoco"
template: proposals-proposals-main.html
---

# #113 – Distribute v0.2.16 bounty rewards

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-10-08T02:43:54.969935178Z"></span></div>

**Proposal ID:** `113`

**Type:** Execute Contract

**Submit:** 2026-10-06 02:43 UTC

**Voting:** 2026-10-06 02:43 UTC → 2026-10-08 02:43 UTC

**Proposer:** [`gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le`](https://gonka.gg/address/gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le){:target="_blank"}

<div class="prop-funding-line prop-funding-line-voting">$104,150 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/113){:target="_blank"}

</div>

Bounty Payments Associated with v0.2.16

This proposal covers 104,150 USDT from community funds for development, research, infrastructure, security reporting, and code review work on the Gonka protocol. The work includes contributions to upgrade v0.2.16 and larger projects spanning multiple upgrade cycles.

## 1. Decode-PoC: 38,000 USDT.

Decode-PoC moves from prefill-only proof of compute covering token generation, aiming to make measured compute capacity better align with real inference workloads. Axel-t published the [original proposal](<https://github.com/gonka-ai/gonka/issues/1135>) in April 2026.

The work covers CUDA graph support, vLLM porting, and testing across hardware configurations and models.

Axel-t: 18,000 USDT for CUDA graph support. Technical details are available in the [PoC-decode documentation](<https://github.com/axeltec-software/vllm/blob/poc-v0.20-decode-poc-cg/benchmarks/poc/POC_DECODE.md>).

- Previously paid: 30,000 USDT on June 17, 2026, through governance proposal 76, for the scheme's design and experimental feasibility validation.

- Upon completion, a final bounty of 12,000 USDT for Axel-t's contribution to the vLLM port, test suite, and on-chain integration will be proposed together with the upgrade that integrates decode-PoC on-chain. Both the previous payment and the planned final bounty are outside this proposal's total.

Kaitaku.ai: 20,000 USDT for porting, experiments, validation, and integration work. The [initial report](<https://github.com/kaitakuai/experiments/blob/main/reports/2026-06-decode-poc-research-and-integration.md>) covers June 9-September 10, 2026, with [continued integration work](<https://github.com/kaitakuai/experiments/blob/main/reports/2026-09-decode-poc-glm-028-and-0300-migration.md>) documented through September 25, 2026.

## 2. gonka-poc plugin: 5,000 USDT.

This project packages PoC functionality as a vLLM plugin, reducing the work needed to support new vLLM releases.

Kaitaku.ai: 5,000 USDT for plugin development and integration. The [report](<https://github.com/kaitakuai/experiments/blob/main/reports/2026-07-gonka-poc-plugin-and-residual.md>) covers June 16-September 8, 2026.

## 3. Model benchmarking and integration: 13,000 USDT.

This work prepares candidate models for use on Gonka. It includes necessary vLLM updates, PoC benchmarks across common GPU types, and testing validation thresholds to detect model substitution while allowing different GPU types to validate each other. It also includes on-chain proposals with model parameters and coefficients.

Kaitaku.ai:

- DeepSeek-V4-Flash: 5,000 USDT for experiments, a vLLM update, an on-chain model proposal, and additional experiments for the 0731 version.

- GLM-5.3-Flash: 4,000 USDT for experiments, a vLLM update, and an on-chain model proposal.

- GLM-5.2: 2,000 USDT for experiments and deployment images for B300, B200, and H200.

- Hy3: 2,000 USDT for experiments. This initial evaluation did not result in an on-chain proposal.

> The proposed amounts use the following breakdown: 2,000 for a set of experiments; 1,000 for a vLLM update associated with a new model proposal; and 1,000 for preparing the on-chain proposal with model parameters and coefficients. DeepSeek includes an additional 1,000 for repeating experiments for the 0731 version, without any additional updates specific for that version.

## 4. Vulnerability reporting: 5,000 USDT.

This payment recognizes the report of a vulnerability that could halt the chain.

@vitaly-andr: 5,000 USDT for the high-severity vulnerability report [#1205](<https://github.com/gonka-ai/gonka/issues/1205>), with a proposed fix in [cosmos-sdk#16](<https://github.com/gonka-ai/cosmos-sdk/pull/16>).

## 5. Trainshards: 7,000 USDT.

This work contributes to the development of the network's training capabilities, including contributions [#1350](<https://github.com/gonka-ai/gonka/pull/1350>) and [#1618](<https://github.com/gonka-ai/gonka/pull/1618>).

@x0152: 7,000 USDT for eight weeks of part-time Trainshards v0 development.

## 6. ML-node observability: 12,500 USDT.

This project provides an ML-node metrics exporter, a DAPI federation endpoint, and Grafana dashboards for monitoring node performance, together with hosting and maintenance.

Kaitaku.ai: 12,000 USDT, comprising 4,000 for development and 8,000 for hosting and maintenance, with a commitment to continued hosting and support. The [report](<https://github.com/kaitakuai/experiments/blob/main/reports/2026-07-mlnode-observability.md>) covers July 6-September 8, 2026. Grafana hosting began in July, and the public community instance launched on September 4.

@qdanik: 500 USDT for contributions to the same project.

## 7. GPU rental reimbursement: 9,600 USDT.

This covers GPUs rented for model and PoC experiments across different hardware configurations since June 1, 2026.

Kaitaku.ai: 9,600 USDT for GPU rental expenses related to model and PoC experiments. Details of the experiments and GPU configurations are available in [Kaitaku.ai's technical reports](<https://github.com/kaitakuai/experiments/tree/main/reports>) covering June-September 2026.

*These costs are listed separately from Kaitaku.ai's development and research bounties. Other teams' or projects' bounty amounts may already include their GPU costs.*

## 8. Security reviews, upgrade reviews, fixes, and release management: 14,050 USDT.

This work covers assessment of incoming security reports, review of the v0.2.16 upgrade, and fixes addressing identified issues.

@staaason / @zpoken: 8,050 USDT jointly for reviewing 115 HackerOne reports and delivering fixes [#1767](<https://github.com/gonka-ai/gonka/pull/1767>) and [#1552](<https://github.com/gonka-ai/gonka/pull/1552>), the latter incorporated into [#1623](<https://github.com/gonka-ai/gonka/pull/1623>). The review work covered initial assessment of approximately 50% of incoming HackerOne reports over six weeks. The fixes address genesis-transfer status reporting and PoC submission permissions.

@vitaly-andr: 1,000 USDT for upgrade review with valuable actionable comments.

@bonujel: 1,000 USDT for upgrade review with valuable actionable comments.

@cyberdelamain: 3,000 USDT, comprising 1,000 for upgrade review and 2,000 for fixes [#1828](<https://github.com/gonka-ai/gonka/pull/1828>), [#1846](<https://github.com/gonka-ai/gonka/pull/1846>), [#1845](<https://github.com/gonka-ai/gonka/pull/1845>), and [#1859](<https://github.com/gonka-ai/gonka/pull/1859>).

@x0152: 1,000 USDT for upgrade review work under release management.


---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:1.3%"></div>
    <div class="prop-tally-no" style="width:0.7%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:11.2%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>9.9%</strong> (12,402)</span>
    <span class="prop-tally-no-text">No <strong>5.1%</strong> (6,416)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>85.0%</strong> (106,860)</span>
    <span class="prop-tally-total-text">Total 125,678 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>13.1%</strong> (125,678 / 955,875) · Quorum <strong>25%</strong> (238,968)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl" target="_blank" class="prop-voter-addr">gonka1qwfrtz…33xdkl</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1pd5vx98y59w5v48f6j0gkqyvs5s6z9su7mytch" target="_blank" class="prop-voter-addr">gonka1pd5vx9…7mytch</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1rqm2u7lxzn7r68y0drcyhag6xnckpsnfmgd53t" target="_blank" class="prop-voter-addr">gonka1rqm2u7…mgd53t</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p" target="_blank" class="prop-voter-addr">gonka1ym3np7…0e4a2p</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5" target="_blank" class="prop-voter-addr">gonka1gyk0aa…k8svc5</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2" target="_blank" class="prop-voter-addr">gonka168rtjf…lnkns2</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ajmhqgvkf76hss5xe35kcnntqqhs7r8jz8s939" target="_blank" class="prop-voter-addr">gonka1ajmhqg…z8s939</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 2 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 3 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 4 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 5 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 6 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 7 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 8 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 9 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 10 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 11 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 12 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 13 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 14 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 15 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 16 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "12000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "20000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "18000000000",
        "recipient": "gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m"
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
        "amount": "5000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "5000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "4000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "2000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "2000000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "9600000000",
        "recipient": "gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp"
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
        "amount": "8000000000",
        "recipient": "gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe"
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
        "amount": "5000000000",
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
        "amount": "1000000000",
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
        "amount": "1000000000",
        "recipient": "gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57"
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
        "amount": "8050000000",
        "recipient": "gonka1s8zggm642e3kncy48c7vxwmeclt2wxyyd8qtdt"
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
        "amount": "3000000000",
        "recipient": "gonka15u0r3mf6t7zsfuslusnyt7hsjrq357yumpe8st"
      }
    },
    "funds": []
  }
]
```

</details>
