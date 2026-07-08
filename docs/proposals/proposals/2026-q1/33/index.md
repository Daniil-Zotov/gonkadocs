---
title: "#33 – Epochs 132-133 compensation payout from gov module"
description: "Distribute compensation for CPoC bug affected participants in epochs 132-133."
template: proposals-proposals-main.html
---

# #33 – Epochs 132-133 compensation payout from gov module

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `33`

**Type:** Batch Transfer With Vesting, Community Pool Spend

**Submit:** 2026-03-26 15:10 UTC

**Voting:** 2026-03-26 15:10 UTC → 2026-03-27 15:10 UTC

**Proposer:** [`gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k`](https://gonka.gg/address/gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k){:target="_blank"}

**Metadata:** [https://github.com/votkon/epoch-132-analysis](https://github.com/votkon/epoch-132-analysis)

<div class="prop-funding-line">3,100 GNK · Community Pool · 24,806 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/33){:target="_blank"}

</div>

Distribute compensation for CPoC bug affected participants in epochs 132-133.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:41.8%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:58.2%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 184,243 (41.8%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 256,296 (58.2%)</span>
    <span class="prop-tally-total-text">Total 440,539 votes</span>
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
| 7 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 8 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1r3h2aumyr3cjma50w9rkhmfp7ewqnzxyysxqxf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4843494827072"
          }
        ]
      },
      {
        "recipient": "gonka1apw5tzk6a3l9hdpdx5q9v2leehvz5rvvw44x8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4255766000801"
          }
        ]
      },
      {
        "recipient": "gonka14ued4vcdeluj9v9vmsmteap7vtg7t50640hvmf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3616886374064"
          }
        ]
      },
      {
        "recipient": "gonka1hec2h63xkf9qf7gn07uwucveuhjfrqks8f4dmh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1825917300632"
          }
        ]
      },
      {
        "recipient": "gonka1p22v6ncqsys9fh85gdmkakpe24x2zqfyp60z5q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1090021596230"
          }
        ]
      },
      {
        "recipient": "gonka178p3vw9zxs885l4a29g3sep0v9uplfq4pzvmrq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1060818652888"
          }
        ]
      },
      {
        "recipient": "gonka19fpma3577v3fnk8nxjkvg442ss8hvglxwqgzz6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "804947679963"
          }
        ]
      },
      {
        "recipient": "gonka1s5vtmnn8tqvqfh7gd9hv48kkt2t4mkh7s85zh6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "758407087247"
          }
        ]
      },
      {
        "recipient": "gonka1pvkv59e72vju2h7s9j3ex62c5xneqey350vpwn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "711355059445"
          }
        ]
      },
      {
        "recipient": "gonka1l45efpupwqw9uky3gjwy35mwae9jwgffuqpm7s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "684300143460"
          }
        ]
      },
      {
        "recipient": "gonka1jrkf560tvgqw3f9z4axs9da34lgnrd396e3rs0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "632440625861"
          }
        ]
      },
      {
        "recipient": "gonka1lmh6fy92ac2wldnpugg3t3xhp8lnqzgq0j0efg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "627223500217"
          }
        ]
      },
      {
        "recipient": "gonka1v0td7x4ndxhveg50vzp6nkz4s25qy2wpvrxm32",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "494711157525"
          }
        ]
      },
      {
        "recipient": "gonka1czmu5smv804kq6pqtyvmjxcjjj720mgl4xc3hd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "271520886519"
          }
        ]
      },
      {
        "recipient": "gonka1ya6mzkqvk7ss3l4jnu5fspt5vvzzmnn2ftqvda",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "220428521548"
          }
        ]
      },
      {
        "recipient": "gonka1dydrqvyaa0s8puwmk9e5d5x5hchrm883eckngj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "175020698924"
          }
        ]
      },
      {
        "recipient": "gonka1ra2jy33a2uuyu4jq2f9gf8va555f4tkhr3e4j9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "165992481875"
          }
        ]
      },
      {
        "recipient": "gonka1ktl3kkn9l68c9amanu8u4868mcjmtsr5tgzmjk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "165398106423"
          }
        ]
      },
      {
        "recipient": "gonka1v8z57yg47n8h4zveyj4cdpn0ll8k9zpcm7egkv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "143659523913"
          }
        ]
      },
      {
        "recipient": "gonka1tpvcpcmmqcku5g53tv2q4wehgqw3nmeq3jk4vn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "138115881866"
          }
        ]
      },
      {
        "recipient": "gonka1hqwgkck88d5wnpea0y9dn0gxmyg4rwjgcnvacf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "137985185878"
          }
        ]
      },
      {
        "recipient": "gonka19w5vy2z5gz9f4jr76f8uz09023wz2snycaty05",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "134507427301"
          }
        ]
      },
      {
        "recipient": "gonka17et3ctw6t4d5ylnuc2kwc8xrlwk69y0cggzjqm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "133680968228"
          }
        ]
      },
      {
        "recipient": "gonka1jvp4r2dx3t0d736fmxy5ncgwp0w3kdy063m5ps",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "130978525216"
          }
        ]
      },
      {
        "recipient": "gonka1clm58yldg7zp7dmuwrqyh4quqt339qr3q8fajm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129955655047"
          }
        ]
      },
      {
        "recipient": "gonka10ekkjpyfad6265m2502d4tp3n8yp9n0d7rlzk4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "128319062775"
          }
        ]
      },
      {
        "recipient": "gonka1njzjqpx6t4jwe9t0fu8vtzn5cj5xjlaussvctx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "122224107996"
          }
        ]
      },
      {
        "recipient": "gonka1zmx4cwayvhf8hevcu6am0sk8ul5trckc2uftmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "122224107996"
          }
        ]
      },
      {
        "recipient": "gonka1g5t786e2hnry8c4d6fd4rh5t3vsfdnevejtsvy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "119689871632"
          }
        ]
      },
      {
        "recipient": "gonka1a357vdludl6kpmx0c7cstf3vc0muu7t7ltw8sd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "118141504588"
          }
        ]
      },
      {
        "recipient": "gonka150qqxu2zf0lzc3nngal79h0n5ls6lhszzraytv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113487445316"
          }
        ]
      },
      {
        "recipient": "gonka1kch7y24sjux5s7qd9l9j02qzusk33xeqwyz0kc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113027153740"
          }
        ]
      },
      {
        "recipient": "gonka1c8utgl2469d7mjlhhd4afhj3ycm6rq60y7v8dl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104997622909"
          }
        ]
      },
      {
        "recipient": "gonka1a2k2pz759kj543yzxse4hvvsyjkaw0f42mkpl2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104895335892"
          }
        ]
      },
      {
        "recipient": "gonka1j9rxapzwm06quxcul5686e7f39g6swhfhwxtwa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104383900807"
          }
        ]
      },
      {
        "recipient": "gonka10xrtfzs46mmjs8dy48auh2xfxq07dxs0mhdcmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94155199111"
          }
        ]
      },
      {
        "recipient": "gonka14zzmvt5esggym639wk0v8s3gdgdmnjzrh6p7rv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91598023687"
          }
        ]
      },
      {
        "recipient": "gonka1ksz9raj0yvg7wxdfhuj5474lmjpkzkphu0jw27",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33420242057"
          }
        ]
      },
      {
        "recipient": "gonka1j6ddjngvwy3x0yze36nks8dvlqdep9fxaj67tv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23781731443"
          }
        ]
      },
      {
        "recipient": "gonka1vlcd8tr2nh5x6h4wl9vacpzucpp9a2p9rv8c57",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19997111815"
          }
        ]
      },
      {
        "recipient": "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18667380595"
          }
        ]
      },
      {
        "recipient": "gonka1rlf0ggajudsvxuvgkukpmg2xwd06htv4vu2ktx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1vkh8e2uqk9mdw0ql83g0p4ge0wmqstcasulngn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "2500000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka170gvlkfx4vg267y7mx0d5nexlf3lxs8nktjw75",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1uvk3w9sswd8nnzt29yjyw94vwmuq6g6h8a2fr7",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1ss36q35zmqhpj83vctedd25s34qz7d5vspahay",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1ajxyae8vgzlh3t6frq64e7vj3fnga7vuxt0zhf",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1d5nn7u0hq0pumgmfxk95nj5h3zkuskkdh96dzd",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "100000000000"
      }
    ]
  }
]
```

</details>

---