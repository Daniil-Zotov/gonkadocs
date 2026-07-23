---
title: "#55 – GRC Proposal #2 - Restitution (epochs 248-254)"
description: "Distribute restitution for Cases 2, 3, and 4 across epochs 248-254. Case 2: preserver weight double-scaling bug (epochs 249-253). Case 3: epoch loss restitution: broad epoch losses, consecutive failur"
template: proposals-proposals-main.html
---

# #55 – GRC Proposal #2 - Restitution (epochs 248-254)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `55`

**Type:** Batch Transfer With Vesting, Community Pool Spend

**Submit:** 2026-05-21 16:18 UTC

**Voting:** 2026-05-21 16:18 UTC → 2026-05-23 16:18 UTC

**Proposer:** [`gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k`](https://gonka.gg/address/gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k){:target="_blank"}

**Metadata:** [https://github.com/votkon/grc-proposal-2](https://github.com/votkon/grc-proposal-2)

<div class="prop-funding-line">39,722 GNK · Community Pool · 306,307 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/55){:target="_blank"}

</div>

Distribute restitution for Cases 2, 3, and 4 across epochs 248-254. Case 2: preserver weight double-scaling bug (epochs 249-253). Case 3: epoch loss restitution: broad epoch losses, consecutive failures restriction, and remaining delta (epochs 248, 249, 250). Case 4: API startup blocking issue (epoch 254). Total: 306,307.29 GNK to 90 addresses. Bounties: 39,722.20 GNK to 4 addresses.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:25.4%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:16.2%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 188,670 (61.2%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 119,835 (38.8%)</span>
    <span class="prop-tally-total-text">Total 308,505 votes</span>
    
  </div>
</div>


## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 3 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 4 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 5 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka12av9up884t9lcsf70rs0l7jfmkmc8k9sxfuknt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "87515706412000"
          }
        ]
      },
      {
        "recipient": "gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52989936765000"
          }
        ]
      },
      {
        "recipient": "gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30915639076000"
          }
        ]
      },
      {
        "recipient": "gonka1umvyh0rz5fdmk9qhxurshhchennajced6f4s89",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19853590458000"
          }
        ]
      },
      {
        "recipient": "gonka188c86f9mrlt4nlcg89f82nnfm9jzq9gtjafj50",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11685431400000"
          }
        ]
      },
      {
        "recipient": "gonka1dzdmx5ljrwkelrmgd7suv2q43epn293qacpgqn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10930934355000"
          }
        ]
      },
      {
        "recipient": "gonka1r5hdy9q5v783ef7td98k4c68cxl6a58h5sytfq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4623954018000"
          }
        ]
      },
      {
        "recipient": "gonka163ug8zucqeag9v5ey4au34jqt7vejkmxsg74eu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4086605073000"
          }
        ]
      },
      {
        "recipient": "gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3933361320000"
          }
        ]
      },
      {
        "recipient": "gonka1zsvl7ujlc8z3a35v2q6e3nml7ftyk23v76jqgl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3409330900000"
          }
        ]
      },
      {
        "recipient": "gonka1vcvn2p5gczr5pynqq0ca0933tdrf5w64sjgtdg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2481939374000"
          }
        ]
      },
      {
        "recipient": "gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2358756296000"
          }
        ]
      },
      {
        "recipient": "gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1987904622000"
          }
        ]
      },
      {
        "recipient": "gonka1u9a7r4w76gult5n9ysadnual9fghkc6yda60wj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1945265555000"
          }
        ]
      },
      {
        "recipient": "gonka1pvkv59e72vju2h7s9j3ex62c5xneqey350vpwn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1927972100000"
          }
        ]
      },
      {
        "recipient": "gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1894756997000"
          }
        ]
      },
      {
        "recipient": "gonka1dpt9zx2dqcky6yjjwrd8xz2w7lq6vffy9mhvgs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1841921987000"
          }
        ]
      },
      {
        "recipient": "gonka1lswsj2x7u4606wqpunmm07skgf76r3dyz4v0d8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1827469872000"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1812926330000"
          }
        ]
      },
      {
        "recipient": "gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1780381271000"
          }
        ]
      },
      {
        "recipient": "gonka1ge9amk4ymld27d35akj3ky9uph4gyz6rdpepjj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1771829231000"
          }
        ]
      },
      {
        "recipient": "gonka1jltjehxsnum94nt8c00ts7khmpy4lafv6gryzk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1741951170000"
          }
        ]
      },
      {
        "recipient": "gonka1llgg3kvg9sc6xz09jtkcrucrppxgn78xe4xlv0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1727750282000"
          }
        ]
      },
      {
        "recipient": "gonka145666cll76ptcyy9ceymtalr8gnvv73ne99p32",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1688729573000"
          }
        ]
      },
      {
        "recipient": "gonka1slndy4rsmld579628302rj5gz8z9qf4v6ppmc4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1602460126000"
          }
        ]
      },
      {
        "recipient": "gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1581661457000"
          }
        ]
      },
      {
        "recipient": "gonka187tn9y92ur6tu0zf69u94hwl0q77m47y0k36hv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1573597372000"
          }
        ]
      },
      {
        "recipient": "gonka1pllyukkeymx3hfd9mts3pryr9y6efs9eshty87",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1572442861000"
          }
        ]
      },
      {
        "recipient": "gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1482391068000"
          }
        ]
      },
      {
        "recipient": "gonka1043d00lu0v3fz53cut34twtcanalqg9u8vehp2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1478451308000"
          }
        ]
      },
      {
        "recipient": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1446802128000"
          }
        ]
      },
      {
        "recipient": "gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1416649392000"
          }
        ]
      },
      {
        "recipient": "gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1387426691000"
          }
        ]
      },
      {
        "recipient": "gonka1t8p0tjqls358gmzvd3rnnjulraq2k3m772vnt8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1377181840000"
          }
        ]
      },
      {
        "recipient": "gonka19ghzvgfr065s3fr5awuvs3nhy9fq4n7wrr9kel",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1348734584000"
          }
        ]
      },
      {
        "recipient": "gonka1h3s37p0l23mg6ak9h9nmayh6r9f2vm6umj3qet",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1343669924000"
          }
        ]
      },
      {
        "recipient": "gonka16k03ze5ynkprsd4n6e5uzhthvu9jjk553rauqy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1291153511000"
          }
        ]
      },
      {
        "recipient": "gonka1zpw8tml8xl4fm6zm8zpf2u4pq4tehmd9e2vgq7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1252141319000"
          }
        ]
      },
      {
        "recipient": "gonka1ccdm8j6sjyhq4qask049dwgaczs7f3pxte6zmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1240267552000"
          }
        ]
      },
      {
        "recipient": "gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1155361073000"
          }
        ]
      },
      {
        "recipient": "gonka16q0zaetd6hq6d8zj48ur0v967xrrwh566kcazc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1122206687000"
          }
        ]
      },
      {
        "recipient": "gonka12gc47yq8m7rnsa3aucq8mlzm7men8jaac7qkkz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1048532370000"
          }
        ]
      },
      {
        "recipient": "gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1045748557000"
          }
        ]
      },
      {
        "recipient": "gonka1mdy7nlecw4xaqdxmeh3qlqzakg9ftge9szfqgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1042787803000"
          }
        ]
      },
      {
        "recipient": "gonka1y4kyhqy022gt4kklxxflgqkutnx96ssww66zg6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "942026558000"
          }
        ]
      },
      {
        "recipient": "gonka1m27e6qup7q8jmvnrn29kahd7vlx6r4l84z4thz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "889089066000"
          }
        ]
      },
      {
        "recipient": "gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "858868299000"
          }
        ]
      },
      {
        "recipient": "gonka12fazh3etpdx947ldwen4wudnds7wu4kjp5vd76",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "811918139000"
          }
        ]
      },
      {
        "recipient": "gonka1lr9mj6dgkv0h76c8y8w0l3esztyg9v2q8d6d8d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "806228688000"
          }
        ]
      },
      {
        "recipient": "gonka17ef5hl0588tmjm9ypw7t2kge78wrkcpvyspc0p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "771087961000"
          }
        ]
      },
      {
        "recipient": "gonka1fp8zl07qccdzuekns2q55jgmcag40kjrm8z0z9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "741302011000"
          }
        ]
      },
      {
        "recipient": "gonka12tfc6ccmadjqv6yaa3axxsuhy6zv6tupu78p8u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "726053879000"
          }
        ]
      },
      {
        "recipient": "gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "722793158000"
          }
        ]
      },
      {
        "recipient": "gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "705402646000"
          }
        ]
      },
      {
        "recipient": "gonka1fc9tzt83dgrqswlgay4668cuqjrk7zsqks2vm2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "688423583000"
          }
        ]
      },
      {
        "recipient": "gonka17tlh09e32xpv2uj433ytjnwwd8fh24jclpzm5s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "643577322000"
          }
        ]
      },
      {
        "recipient": "gonka1cckj93kp9kegry64scpn4ew9965g3qrswyshl9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "599735081000"
          }
        ]
      },
      {
        "recipient": "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "579778319000"
          }
        ]
      },
      {
        "recipient": "gonka17fcahf38xh8ghzyyrc55tarz9nd0vw6xd29nsk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "568610436000"
          }
        ]
      },
      {
        "recipient": "gonka1gyydhl9lp0udz3409ps0c0lk0y4ft8qcyv8tfq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "562251638000"
          }
        ]
      },
      {
        "recipient": "gonka1nkzdygk3g2p2usnueuqxyep3462350hgzxs86s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "558904902000"
          }
        ]
      },
      {
        "recipient": "gonka15rvksn9gxgpszyr8270cd4wj2x3d460r394uv4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "552211430000"
          }
        ]
      },
      {
        "recipient": "gonka1usmu5mfu8vsafvsrsvdutl50vy8kumdhv0j2x9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "552211430000"
          }
        ]
      },
      {
        "recipient": "gonka1psgzz288a434dv6863ldd73xma70zw7387muj2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "548864694000"
          }
        ]
      },
      {
        "recipient": "gonka1ql9asemklpkpr2d4mh33xw5gj0g5tm0v98c5q3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "548864694000"
          }
        ]
      },
      {
        "recipient": "gonka1vcawx5jc2hahydd9sqw30hlxyd9ppupm9ez0yz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "542171223000"
          }
        ]
      },
      {
        "recipient": "gonka1p60lruhxmwcsa9taa28cp4k4f6kv2kvyu5h5ep",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "534999150000"
          }
        ]
      },
      {
        "recipient": "gonka10snluhflqhmwl5xrpuy9ugevypxdjjsft370fq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "525437543000"
          }
        ]
      },
      {
        "recipient": "gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "522077665000"
          }
        ]
      },
      {
        "recipient": "gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "515397335000"
          }
        ]
      },
      {
        "recipient": "gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "505691801000"
          }
        ]
      },
      {
        "recipient": "gonka168yvlgt9jg86frg2z90cc8w4pz9hnd7f8lshux",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "498998329000"
          }
        ]
      },
      {
        "recipient": "gonka1h2m79scgaq6ultrwge03wjk0ys4whgcejphmql",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "474959200000"
          }
        ]
      },
      {
        "recipient": "gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "451760266000"
          }
        ]
      },
      {
        "recipient": "gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "396253535000"
          }
        ]
      },
      {
        "recipient": "gonka1d7p03cu2y2yt3vytq9wlfm6tlz0lfhlgv9h82p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "365789060000"
          }
        ]
      },
      {
        "recipient": "gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "365789060000"
          }
        ]
      },
      {
        "recipient": "gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "357960400000"
          }
        ]
      },
      {
        "recipient": "gonka1k6p754pyhxud2399knyccgjpjvdafj2u9xlgyf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "329318817000"
          }
        ]
      },
      {
        "recipient": "gonka1eazh84v0e60s9m7exxp3nsadcfgvnsthgypjvl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "311581116000"
          }
        ]
      },
      {
        "recipient": "gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "271309892000"
          }
        ]
      },
      {
        "recipient": "gonka1x7zh2277spp7jfqjhv0g5mnezg290xdr4kpfnk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "252678564000"
          }
        ]
      },
      {
        "recipient": "gonka1vjz8csqsr0ph0lv0yylc4auypnzrld7y6l2feu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "233997500000"
          }
        ]
      },
      {
        "recipient": "gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "220215225000"
          }
        ]
      },
      {
        "recipient": "gonka1l0qv64xdu3dk2zzm5vk97j0drcmkus95u50gqk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "192771990000"
          }
        ]
      },
      {
        "recipient": "gonka10jjrlvkfkqupgudz0l603sq99y3wkt3urwjm0x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "149599097000"
          }
        ]
      },
      {
        "recipient": "gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "142236278000"
          }
        ]
      },
      {
        "recipient": "gonka10t67f5zxh7canhuznxg7cperec6286jjqh5pey",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "140897583000"
          }
        ]
      },
      {
        "recipient": "gonka1uf5cg7ef0ns6877nl27y0s6rt06cdmn40k5a88",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59571900000"
          }
        ]
      },
      {
        "recipient": "gonka15sptlamre9vq4m5t7pa7je5r2pc34kmlwvj0jz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23911954000"
          }
        ]
      }
    ],
    "vesting_epochs": "150"
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "4500000000000"
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
        "amount": "8875000000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "11062500000000"
      }
    ]
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "15284700000000"
      }
    ]
  }
]
```

</details>
