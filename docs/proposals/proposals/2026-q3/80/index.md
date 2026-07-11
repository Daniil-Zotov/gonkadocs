---
title: "#80 – GRC Proposal #3 - Restitution"
description: "Restitution payout for confirmed GRC Proposal #3 cases, with Case 05 payments from proposal_id=67 deducted where the same address and epoch were already compensated, and positive victim outputs below "
template: proposals-proposals-main.html
---

# #80 – GRC Proposal #3 - Restitution

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `80`

**Type:** Batch Transfer With Vesting, Community Pool Spend

**Submit:** 2026-07-05 19:40 UTC

**Voting:** 2026-07-05 19:40 UTC → 2026-07-07 19:40 UTC

**Proposer:** [`gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6`](https://gonka.gg/address/gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6){:target="_blank"}

**Metadata:** [https://github.com/huxuxuya/GRC-3-result](https://github.com/huxuxuya/GRC-3-result)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">47,850 GNK · Community Pool · 70,184 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/80){:target="_blank"}

</div>

Restitution payout for confirmed GRC Proposal #3 cases, with Case 05 payments from proposal_id=67 deducted where the same address and epoch were already compensated, and positive victim outputs below the chain minimum raised to 10 GNK.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:10.4%"></div>
    <div class="prop-tally-no" style="width:60.4%"></div>
    <div class="prop-tally-veto" style="width:25.1%"></div>
    <div class="prop-tally-abstain" style="width:4.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 16,378 (10.4%)</span>
    <span class="prop-tally-no-text">No 94,721 (60.4%)</span>
    <span class="prop-tally-veto-text">Veto 39,454 (25.1%)</span>
    <span class="prop-tally-abstain-text">Abstain 6,344 (4.0%)</span>
    <span class="prop-tally-total-text">Total 156,897 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout 156,897 / 741,825 (21.2%) · Quorum 25% (185,456)</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 3 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 4 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 5 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 6 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5890493167171"
          }
        ]
      },
      {
        "recipient": "gonka1007dchuqgdnute4qam70kmn56j2vfw38mhyrqv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7287485958471"
          }
        ]
      },
      {
        "recipient": "gonka1007g0ut3u4wjkay9hegqfev4pj90qgexwskmcw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7238152949000"
          }
        ]
      },
      {
        "recipient": "gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14096689777"
          }
        ]
      },
      {
        "recipient": "gonka10kmsyy00yxnky2xfqy9wce0l7uaadq4jjp3ykg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16028213179615"
          }
        ]
      },
      {
        "recipient": "gonka12l3fwycgvs9tdpze59za89zq4cexhkxddafxdh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "150749450599"
          }
        ]
      },
      {
        "recipient": "gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "79662604523"
          }
        ]
      },
      {
        "recipient": "gonka1598sglu00mktw3973jmwsu3vdw29mgcfjleju2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "71065864191"
          }
        ]
      },
      {
        "recipient": "gonka15fpzwc7d2z3r4y5475p6k7uqknnkj38gsus3d9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4064625997098"
          }
        ]
      },
      {
        "recipient": "gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "69342202123"
          }
        ]
      },
      {
        "recipient": "gonka170wwtpvhwzgghd638z84z35gjggl7cvyzrkh8p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "156696892692"
          }
        ]
      },
      {
        "recipient": "gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "923163292052"
          }
        ]
      },
      {
        "recipient": "gonka19nd876302m3ll2h7sd55hp9pqzv2hpqalh8pjj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "217372045879"
          }
        ]
      },
      {
        "recipient": "gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1975688510632"
          }
        ]
      },
      {
        "recipient": "gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113179188133"
          }
        ]
      },
      {
        "recipient": "gonka1duuaqdx06sx8v2dzggltwwmqyuw8lvjkjq7xll",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "161268199400"
          }
        ]
      },
      {
        "recipient": "gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "83791459026"
          }
        ]
      },
      {
        "recipient": "gonka1h9asnq9x2kux2m8pcwaeegljzmd4ym4h26p07n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33560566095"
          }
        ]
      },
      {
        "recipient": "gonka1hjjse9r0zfe0q8k4hfe4t5xuzstjqvky7dnj05",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "56561388067"
          }
        ]
      },
      {
        "recipient": "gonka1hmjjq6ghykww8f8ujajnnmu2dpk2drrth8mtva",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11227314154"
          }
        ]
      },
      {
        "recipient": "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10262057515369"
          }
        ]
      },
      {
        "recipient": "gonka1jt5mqrx0yg5k6qdqhnkc4kpya4mzy52ngyh34c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19116778155"
          }
        ]
      },
      {
        "recipient": "gonka1lh0danzlvxm5qtaly7myqd3n5sus0fq92n8shx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "182307306602"
          }
        ]
      },
      {
        "recipient": "gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3540857046786"
          }
        ]
      },
      {
        "recipient": "gonka1mmwngrtpc4fd4jquv5vfsnscqdzmcz0zgrvy0g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15900304370"
          }
        ]
      },
      {
        "recipient": "gonka1pks9m29wqac2kxdj8v8acq58rjshh6u8y2a772",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "243541684885"
          }
        ]
      },
      {
        "recipient": "gonka1q3n37e2uc4npkheyjllx2ztx5yh42rk6vz3kgn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27431059448"
          }
        ]
      },
      {
        "recipient": "gonka1qx3znmtpxqgmz3t4tgpdk68dsfxuccn6cxnp8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25489037540"
          }
        ]
      },
      {
        "recipient": "gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1531342862912"
          }
        ]
      },
      {
        "recipient": "gonka1t88kkvnrayz5l2u043tccd2pks4rt8y346z9dv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1t8jjpaq2m0svru73kh9l0m62e7lr7qxxw6uvea",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "246274027398"
          }
        ]
      },
      {
        "recipient": "gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8784035574445"
          }
        ]
      },
      {
        "recipient": "gonka1xy9py6zlxsum2m0z422qwa0um6au7ls4r65ky8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32043361480"
          }
        ]
      },
      {
        "recipient": "gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "578039630382"
          }
        ]
      }
    ],
    "vesting_epochs": "150"
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "13950000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka123pr0p0salv96xvne9qln70x3usvpyscug5f9a",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "4600000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "10800000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "12300000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1ppn53fu8q3pxvwwf8ycjf3c6nzlugs3hmw6a3q",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "6200000000000"
      }
    ]
  }
]
```

</details>

---