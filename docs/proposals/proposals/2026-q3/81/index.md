---
title: "#81 – Kimi cPoC Restitution (epochs 306-309)"
description: "Distribute restitution for Kimi operators affected by cPoC validation failure in epochs 306-309. The Kimi validation path failed starting in e306 causing confirmation_weight suppression for Kimi opera"
template: proposals-proposals-main.html
---

# #81 – Kimi cPoC Restitution (epochs 306-309)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-voting">Voting</span>

**Proposal ID:** `81`

**Type:** Batch Transfer With Vesting

**Submit:** 2026-07-08 05:57 UTC

**Voting:** 2026-07-08 05:57 UTC → 2026-07-10 05:57 UTC

**Proposer:** [`gonka123pr0p0salv96xvne9qln70x3usvpyscug5f9a`](https://gonka.gg/address/gonka123pr0p0salv96xvne9qln70x3usvpyscug5f9a){:target="_blank"}

**Metadata:** [https://github.com/votkon/gonka-kimi-e306-issue](https://github.com/votkon/gonka-kimi-e306-issue)

<div class="prop-funding-line prop-funding-line-voting">175,082 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/81){:target="_blank"}

</div>

Distribute restitution for Kimi operators affected by cPoC validation failure in epochs 306-309. The Kimi validation path failed starting in e306 causing confirmation_weight suppression for Kimi operators while non-Kimi operators ran normally. Failure worsened in e307 and carried into the e309 bootstrap attempt. Total: 175082.07 GONKA to 19 addresses, vested over 170 days (160 epochs).

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:82.4%"></div>
    <div class="prop-tally-no" style="width:0.2%"></div>
    <div class="prop-tally-veto" style="width:17.4%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 227,818 (82.4%)</span>
    <span class="prop-tally-no-text">No 624 (0.2%)</span>
    <span class="prop-tally-veto-text">Veto 48,054 (17.4%)</span>
    <span class="prop-tally-abstain-text">Abstain 18 (0.0%)</span>
    <span class="prop-tally-total-text">Total 276,514 votes</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45002842624839"
          }
        ]
      },
      {
        "recipient": "gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27081229515922"
          }
        ]
      },
      {
        "recipient": "gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10752097867403"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9348214480985"
          }
        ]
      },
      {
        "recipient": "gonka1gtdrqh9jpkqxdaskxkpwjpy2q284q8qnvg58uj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9007313194119"
          }
        ]
      },
      {
        "recipient": "gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7827216214294"
          }
        ]
      },
      {
        "recipient": "gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7754878837428"
          }
        ]
      },
      {
        "recipient": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6449817683838"
          }
        ]
      },
      {
        "recipient": "gonka1uhqpup9fev3zahlx6n326lp0krznc6usjtx6lu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5784283093297"
          }
        ]
      },
      {
        "recipient": "gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5654647873240"
          }
        ]
      },
      {
        "recipient": "gonka16j7xfk3hvguy5gz95mzg3p5dkuwla7aux03kdw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5614918581345"
          }
        ]
      },
      {
        "recipient": "gonka1skw86pm4dvfhzslu5a9gsc98ahspalge8rprp4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5546181336564"
          }
        ]
      },
      {
        "recipient": "gonka1aw77zuy536tufqd56zfq6ev3234u5ftty0zkte",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5545625985548"
          }
        ]
      },
      {
        "recipient": "gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5545062683374"
          }
        ]
      },
      {
        "recipient": "gonka1ujg4pt8crhxdymnsatalzdj0hhkgfqjmlp9zel",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5533752395951"
          }
        ]
      },
      {
        "recipient": "gonka1jfv9n2af9y8xgnn6834mnp924vkpucmvchsq8d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5310157560537"
          }
        ]
      },
      {
        "recipient": "gonka1kvmerzu64094dt9t62ea0cp75larh39ulzldum",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3368636073541"
          }
        ]
      },
      {
        "recipient": "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2248987476581"
          }
        ]
      },
      {
        "recipient": "gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1706210826186"
          }
        ]
      }
    ],
    "vesting_epochs": "160"
  }
]
```

</details>

---