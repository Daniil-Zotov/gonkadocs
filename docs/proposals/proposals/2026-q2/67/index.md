---
title: "#67 – Kimi Restitution (epochs 265-276)"
description: "Distribute restitution for Kimi operators across epochs 265-276. Epochs 265-266: external attack causing CPoC degradation and nonce exclusion. Epochs 267-276: ComputeGroupCap systematic underpayment d"
template: proposals-proposals-main.html
---

# #67 – Kimi Restitution (epochs 265-276)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `67`

**Type:** Batch Transfer With Vesting

**Submit:** 2026-06-03 21:54 UTC

**Voting:** 2026-06-03 22:09 UTC → 2026-06-05 22:09 UTC

**Proposer:** [`gonka1nvcwl2c7jxj2h47c56y8dmcmf0tynt5dplzngy`](https://gonka.gg/address/gonka1nvcwl2c7jxj2h47c56y8dmcmf0tynt5dplzngy){:target="_blank"}

**Metadata:** [https://github.com/votkon/gonka-kimi-restitution](https://github.com/votkon/gonka-kimi-restitution)

<div class="prop-funding-line">946,509 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/67){:target="_blank"}

</div>

Distribute restitution for Kimi operators across epochs 265-276. Epochs 265-266: external attack causing CPoC degradation and nonce exclusion. Epochs 267-276: ComputeGroupCap systematic underpayment due to attack-induced N-1 weight collapse. Total: 946,509.93 GNK to 53 addresses.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:43.1%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:11.4%"></div>
    <div class="prop-tally-abstain" style="width:0.1%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 319,920 (78.9%)</span>
    <span class="prop-tally-no-text">No 150 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 84,623 (20.9%)</span>
    <span class="prop-tally-abstain-text">Abstain 744 (0.2%)</span>
    <span class="prop-tally-total-text">Total 405,437 votes</span>
    
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
        "recipient": "gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "158541879455919"
          }
        ]
      },
      {
        "recipient": "gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101147807218599"
          }
        ]
      },
      {
        "recipient": "gonka1uhqpup9fev3zahlx6n326lp0krznc6usjtx6lu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96601320933414"
          }
        ]
      },
      {
        "recipient": "gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "79247555226990"
          }
        ]
      },
      {
        "recipient": "gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "73073708453292"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66487744752217"
          }
        ]
      },
      {
        "recipient": "gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52290195675726"
          }
        ]
      },
      {
        "recipient": "gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "39809676543013"
          }
        ]
      },
      {
        "recipient": "gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33750579636210"
          }
        ]
      },
      {
        "recipient": "gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "20610390027954"
          }
        ]
      },
      {
        "recipient": "gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18234887510983"
          }
        ]
      },
      {
        "recipient": "gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17630158097135"
          }
        ]
      },
      {
        "recipient": "gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13958367773340"
          }
        ]
      },
      {
        "recipient": "gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12612234865692"
          }
        ]
      },
      {
        "recipient": "gonka1007g0ut3u4wjkay9hegqfev4pj90qgexwskmcw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11688555563236"
          }
        ]
      },
      {
        "recipient": "gonka1c6fwzedfsmpu4jnjekv4cn7mvr7x7fuqd6uqt9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11366419253907"
          }
        ]
      },
      {
        "recipient": "gonka1007dchuqgdnute4qam70kmn56j2vfw38mhyrqv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11262520197774"
          }
        ]
      },
      {
        "recipient": "gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11021183080111"
          }
        ]
      },
      {
        "recipient": "gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10934181496134"
          }
        ]
      },
      {
        "recipient": "gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10456612261496"
          }
        ]
      },
      {
        "recipient": "gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9768694504061"
          }
        ]
      },
      {
        "recipient": "gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9423072516255"
          }
        ]
      },
      {
        "recipient": "gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8441669467829"
          }
        ]
      },
      {
        "recipient": "gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6820652573831"
          }
        ]
      },
      {
        "recipient": "gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6618057560512"
          }
        ]
      },
      {
        "recipient": "gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5645801436758"
          }
        ]
      },
      {
        "recipient": "gonka1wvv656pt2d8x2khcvytqeessck5uzjnxzsa8f6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5511598438612"
          }
        ]
      },
      {
        "recipient": "gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4673802241961"
          }
        ]
      },
      {
        "recipient": "gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4444392150972"
          }
        ]
      },
      {
        "recipient": "gonka1l8jd2nz92mnem0xwgwkltcw2952cnlphs5arsa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4167200640617"
          }
        ]
      },
      {
        "recipient": "gonka1007n977a7uda3pd9m6hftw8xcql0tc20m96myu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3396492511794"
          }
        ]
      },
      {
        "recipient": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3018840187451"
          }
        ]
      },
      {
        "recipient": "gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2731396085272"
          }
        ]
      },
      {
        "recipient": "gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2602055673919"
          }
        ]
      },
      {
        "recipient": "gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2392222959397"
          }
        ]
      },
      {
        "recipient": "gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2293694674600"
          }
        ]
      },
      {
        "recipient": "gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2034501080557"
          }
        ]
      },
      {
        "recipient": "gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1805142497891"
          }
        ]
      },
      {
        "recipient": "gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1753409171279"
          }
        ]
      },
      {
        "recipient": "gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1575513416778"
          }
        ]
      },
      {
        "recipient": "gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1166439755518"
          }
        ]
      },
      {
        "recipient": "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1025259358283"
          }
        ]
      },
      {
        "recipient": "gonka10070xwkwv00sulsa7gdfwkgh8w069stkjjf39x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1017602508283"
          }
        ]
      },
      {
        "recipient": "gonka10075dz43h94zhqu5hwdj3nyjay6v8mzwvpxr0s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1017602508283"
          }
        ]
      },
      {
        "recipient": "gonka1007lnkyhdh7aq0vjdcdwcerkdh4yy85rymjdg6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1007974841606"
          }
        ]
      },
      {
        "recipient": "gonka13a4v8gxxjav5t4xq5y9cv9d8rfnvkjfw5adqz3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "521637814838"
          }
        ]
      },
      {
        "recipient": "gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "279015575378"
          }
        ]
      },
      {
        "recipient": "gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "276414090986"
          }
        ]
      },
      {
        "recipient": "gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113864833864"
          }
        ]
      },
      {
        "recipient": "gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "108366531966"
          }
        ]
      },
      {
        "recipient": "gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "100568940182"
          }
        ]
      },
      {
        "recipient": "gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30990428883"
          }
        ]
      }
    ],
    "vesting_epochs": "160"
  }
]
```

</details>
