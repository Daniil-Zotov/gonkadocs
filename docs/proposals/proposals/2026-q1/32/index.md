---
title: "#32 – Epoch 158 compensation payout from gov module (batch vesting)"
description: "Distribute compensation proportional to epoch 158 lost preserved weights. Implemented as one MsgBatchTransferWithVesting."
template: proposals-proposals-main.html
---

# #32 – Epoch 158 compensation payout from gov module (batch vesting)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `32`

**Type:** Batch Transfer With Vesting, Community Pool Spend

**Submit:** 2026-03-23 17:30 UTC

**Voting:** 2026-03-23 17:30 UTC → 2026-03-24 17:30 UTC

**Proposer:** [`gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6`](https://gonka.gg/address/gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6){:target="_blank"}

**Metadata:** [https://github.com/huxuxuya/epoch158/blob/main/SIMPLE_COIN_AMOUNT_LOGIC.md](https://github.com/huxuxuya/epoch158/blob/main/SIMPLE_COIN_AMOUNT_LOGIC.md)

<div class="prop-funding-line">500 GNK · Community Pool · 30,038 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/32){:target="_blank"}

</div>

Distribute compensation proportional to epoch 158 lost preserved weights. Implemented as one MsgBatchTransferWithVesting.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:67.6%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (501,114)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 501,114 votes</span>
    
  </div>
</div>


## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka10000627dkz6nvmf09ctqy073v0fls696uznwgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "236153328927"
          }
        ]
      },
      {
        "recipient": "gonka100009u7hegukxy5ne3w6ycfleaj7uuvh2juxqd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "181761590719"
          }
        ]
      },
      {
        "recipient": "gonka10003spukrualhl3h80k9x5m9vrmvlmp8kf4t4w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "217718885065"
          }
        ]
      },
      {
        "recipient": "gonka10008pmwrke48xh42dhe0ul0mm0mhhvz6ta9srs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "244307025251"
          }
        ]
      },
      {
        "recipient": "gonka1000937gjpju4udj2wlj3yld0lcw024tp0ztqew",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "228860581905"
          }
        ]
      },
      {
        "recipient": "gonka1000hqfkcp3cs0fq4r78vvpkjlv5n4x4sdgcv7v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "282391370813"
          }
        ]
      },
      {
        "recipient": "gonka1000rv0ddp9yk6djr4y29mt0gu3m4p8mg4kmjcv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "146158804908"
          }
        ]
      },
      {
        "recipient": "gonka1000xjetteyu7gy726vnhdxq69y3meq04gvnk4d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "187129862832"
          }
        ]
      },
      {
        "recipient": "gonka1000xmydnfvphwy4n5yww4ex6nwk9mqslf2gnhs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "185104099770"
          }
        ]
      },
      {
        "recipient": "gonka1000zfcrzdjwwucvs9k2wuy4j5ecj69q5f4v57h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "209767765048"
          }
        ]
      },
      {
        "recipient": "gonka100k8hr43z5vp0fnyc94m7lum6mj4st6vksxz8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "234380786248"
          }
        ]
      },
      {
        "recipient": "gonka10etnufq85u67k075yuxq6h3rzwlcln5rffhlyx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka10fvaz7sgva6563fkcp9wxlk5hz7gj8fmu0w699",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "178165861284"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "131775887169"
          }
        ]
      },
      {
        "recipient": "gonka10p49jx70haq9uhjy94y80zkfv3xk5pafk5wc5q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "291760524973"
          }
        ]
      },
      {
        "recipient": "gonka10vljxvwy6n9hh263chkt0hj0kg7t0qmdwfrurs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "298800051613"
          }
        ]
      },
      {
        "recipient": "gonka1270mrwh27pgnrtmmsmyy5rsq2h8ug6l4zvg4cu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "179229386891"
          }
        ]
      },
      {
        "recipient": "gonka12gwxa8vcvahyd4ygcxp4624ywaw98wp953wuva",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "310802697754"
          }
        ]
      },
      {
        "recipient": "gonka12hzd9zlz3tgslky477d4wa0jlwacv4nj9vxlmj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "302091916588"
          }
        ]
      },
      {
        "recipient": "gonka1450wvd5uugfj7gru4heut5ulnneunplvxs995e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "359269079007"
          }
        ]
      },
      {
        "recipient": "gonka14cu38xpsd8pz5zdkkzwf0jwtpc0vv309ake364",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "166619011832"
          }
        ]
      },
      {
        "recipient": "gonka14dkhe6rhy2nq6snmkp2ssnaesumsuwctlmrzcn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33323802366"
          }
        ]
      },
      {
        "recipient": "gonka14jxtac6gra9cc97q7gw6el2l7f2v2d32f8973x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157148569518"
          }
        ]
      },
      {
        "recipient": "gonka14pdvgt025fwkf38cr74hhcj2nfl98c044tswya",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93185100842"
          }
        ]
      },
      {
        "recipient": "gonka14qwpw2l0qmevxy9snllfaw0r9svnh4vdyl3897",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "86449438662"
          }
        ]
      },
      {
        "recipient": "gonka14s76f83l8m3guvr8vu54dmla798jzy3u09vxzx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85993641973"
          }
        ]
      },
      {
        "recipient": "gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "621200242896"
          }
        ]
      },
      {
        "recipient": "gonka155cnj622zfdl64f23ljmk2tzv7tewl6fp4m2hl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "248814348064"
          }
        ]
      },
      {
        "recipient": "gonka15kf06ehfplnqtvgnndyfym9w9f63686cvw3nqj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157047281365"
          }
        ]
      },
      {
        "recipient": "gonka15mh2v944wxk3phxfkegglpgfpq9mjcm6vmpyng",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "179533251351"
          }
        ]
      },
      {
        "recipient": "gonka16324l7r5jllqjm7e5wlf2h44cr3dsmjj8a6py7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "170012164960"
          }
        ]
      },
      {
        "recipient": "gonka168yvlgt9jg86frg2z90cc8w4pz9hnd7f8lshux",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "103769712840"
          }
        ]
      },
      {
        "recipient": "gonka16lksjaqq2gqpeexvqg4xgux6hdtms3wnk4jjle",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka16sfwtnse80aleg7sgmumnu3qxhtf93mf86479a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "147323618668"
          }
        ]
      },
      {
        "recipient": "gonka174srhxhfktxx4hv94zcdz4jqfw9kvc4ge2p0pu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "165656774377"
          }
        ]
      },
      {
        "recipient": "gonka178p3vw9zxs885l4a29g3sep0v9uplfq4pzvmrq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "791212407856"
          }
        ]
      },
      {
        "recipient": "gonka17amsnz2csvjwt3rdezys6gj7wggexxwtwt03a9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "105643543672"
          }
        ]
      },
      {
        "recipient": "gonka17nhy0gakmp3yhlrm5h9xghj5mgwgyxagr8zmm0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "22891122598"
          }
        ]
      },
      {
        "recipient": "gonka17w5kpa57jtqnqy7wdp5d03jkjmk0vjwdpp5xmg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "171683419486"
          }
        ]
      },
      {
        "recipient": "gonka184jz8ja5gqkr3kt98a3a4syyypwj07j0qngukg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29525496625"
          }
        ]
      },
      {
        "recipient": "gonka185kgdje9wjucxtkdu0nqhpqlwxutc5kc7nss8u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "290190558600"
          }
        ]
      },
      {
        "recipient": "gonka18xpmr5v362gwvxlq78twhg7ht07wu4kzdqu4y2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "386819456648"
          }
        ]
      },
      {
        "recipient": "gonka192gv4k5kh88g5s9xll8k7w065lz0rjwh7zj55v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "167479961133"
          }
        ]
      },
      {
        "recipient": "gonka1948n747ayualpznexxchnx95pdnpu25mph804e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka199lgrq8l9xcqqnr0agajzl78c4dpfvwnsc4elm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "327312666708"
          }
        ]
      },
      {
        "recipient": "gonka19g7jp7tcpnh9ul6gkr3kdc3lmcy55w6swvql0f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka19mh7jn9xmzz9m0nrczgd32usqrcqm7mpsrh77j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "178469725743"
          }
        ]
      },
      {
        "recipient": "gonka19nsaq8gdavl04mx0v6lhvzzdkqhu6uf56l38w0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "156236976140"
          }
        ]
      },
      {
        "recipient": "gonka1a32tfg0a3xe7zer9m3ttuxr57wdffpc82qnacq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16256748571"
          }
        ]
      },
      {
        "recipient": "gonka1a3f2cpds29pq0x7yvuh5we233l6aytcgl8gtlx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "383375659443"
          }
        ]
      },
      {
        "recipient": "gonka1a9yz979xxryjh9hdzuyxddscwtg9g92079hjra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "306751171631"
          }
        ]
      },
      {
        "recipient": "gonka1aev99sylsnfzyu2dwlnw6f9lugjkvav7kxqp0k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49023466095"
          }
        ]
      },
      {
        "recipient": "gonka1ajvs7j8wlgjy8d3kjad520am6jm3a4alj7k4jq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "167631893363"
          }
        ]
      },
      {
        "recipient": "gonka1au034ld8fsrvtyxpzxx8nnnqe5kmhe20lmhuwm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17269630102"
          }
        ]
      },
      {
        "recipient": "gonka1c8pemd8czpgeg69cu95y58fstuquw93uwqml7f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "385907863270"
          }
        ]
      },
      {
        "recipient": "gonka1cjvdez8e6mwjxg0e3g7rrds9ezm9c7kemlu3g7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "175076572615"
          }
        ]
      },
      {
        "recipient": "gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "21371800302"
          }
        ]
      },
      {
        "recipient": "gonka1erjgpt52lp7atyq5c5u5tpprtqjr4pt6zd2pny",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157604366207"
          }
        ]
      },
      {
        "recipient": "gonka1ewlwawmd4z42daay08hspv45nmzlvffw0ums94",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "180140980269"
          }
        ]
      },
      {
        "recipient": "gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49327330554"
          }
        ]
      },
      {
        "recipient": "gonka1f5fhrywmd5p0jcd5atk4rm2tjxpdn772lw833k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "277326963158"
          }
        ]
      },
      {
        "recipient": "gonka1f7d43z2qpcv07huwf3qjj4zpssvx6080a357wh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "297280729317"
          }
        ]
      },
      {
        "recipient": "gonka1frfr2z4lclq0wjqsrstnhm48rmvkmd0tfsssvk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "178520369820"
          }
        ]
      },
      {
        "recipient": "gonka1fryp5vn5xppkwykzjul6e2crkgxgwhl2cunrmx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "186724710220"
          }
        ]
      },
      {
        "recipient": "gonka1fs4fapsf05qf3992m92ac3cl38uzh56vev4806",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29474852549"
          }
        ]
      },
      {
        "recipient": "gonka1fvyenm5ms57hmyze8yl659c8ljg4r89nlwap9u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27601021717"
          }
        ]
      },
      {
        "recipient": "gonka1g884r7q58wptvlcpuk09gvw9j5uhwadr4qjexs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "269173266834"
          }
        ]
      },
      {
        "recipient": "gonka1gsarmv9gsc7g9fv9nsqtk6t0d7erxpurf5mvvl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "313334901581"
          }
        ]
      },
      {
        "recipient": "gonka1gz6d9j834xvhvyt7c67ux6egugns7dlc5dzqds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "315715173179"
          }
        ]
      },
      {
        "recipient": "gonka1h3s37p0l23mg6ak9h9nmayh6r9f2vm6umj3qet",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "314246494959"
          }
        ]
      },
      {
        "recipient": "gonka1j3m7rwdjrf44xy8p7ff4w3srqxaml0f73x09ud",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98300152573"
          }
        ]
      },
      {
        "recipient": "gonka1jrkf560tvgqw3f9z4axs9da34lgnrd396e3rs0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "56366857194"
          }
        ]
      },
      {
        "recipient": "gonka1ju7jfznld7vg0f35wgz507m6c0lzgugpmajnvn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "188446608822"
          }
        ]
      },
      {
        "recipient": "gonka1juwk05glldgn7850a3547jsl7l4vrhx9k5g3cr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "195891288074"
          }
        ]
      },
      {
        "recipient": "gonka1k3lva2jsxu5qx30f65yxdlcey8d6f3unmy2gks",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101541373472"
          }
        ]
      },
      {
        "recipient": "gonka1k3xh9h66ye5pdgv2v94xhf7paz445e7qwraz7h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129344971495"
          }
        ]
      },
      {
        "recipient": "gonka1kjrvy4xme4ctepdjspjdw677nmvdwlps4hl5h8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1ks3t0r8g5glvv4um6ml2gy5dzg7l3t2xmp3fg2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94197982373"
          }
        ]
      },
      {
        "recipient": "gonka1ktl3kkn9l68c9amanu8u4868mcjmtsr5tgzmjk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "169505724195"
          }
        ]
      },
      {
        "recipient": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23549495593"
          }
        ]
      },
      {
        "recipient": "gonka1ky9mpdps70l9fe59dg7a7ctnaunkuuc8uet8q2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "176140098222"
          }
        ]
      },
      {
        "recipient": "gonka1l44nacmpmt83kavvevmhlh8elspjtjn6wvwzm0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "667438284781"
          }
        ]
      },
      {
        "recipient": "gonka1l4vfzkwd555pvxqzr3ksphgwgv8xsh89ytmjp0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1252276080718"
          }
        ]
      },
      {
        "recipient": "gonka1lh0danzlvxm5qtaly7myqd3n5sus0fq92n8shx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "116633308282"
          }
        ]
      },
      {
        "recipient": "gonka1llxvtg0657ldmqn4l3t0ag496ff355j5kawagy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "287557066620"
          }
        ]
      },
      {
        "recipient": "gonka1lqv96tny8a0344e6jfgxk500q5ct7zy9ekz49m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "329996802765"
          }
        ]
      },
      {
        "recipient": "gonka1lrls7q8nu8rhjgchctswfsjlnjh84vwycw3jgt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "318146088853"
          }
        ]
      },
      {
        "recipient": "gonka1lzxwqhc5fqwltg57emk2lprd7qzmapp22mv0h7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "183078336709"
          }
        ]
      },
      {
        "recipient": "gonka1mecj5za64q5cnuu3vaey88g7kn996h2lv8aylu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "316829342863"
          }
        ]
      },
      {
        "recipient": "gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "160744298953"
          }
        ]
      },
      {
        "recipient": "gonka1n5r055hu5tr63rgqs7xg4d45ar8q6yy3qdhn04",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10483323845"
          }
        ]
      },
      {
        "recipient": "gonka1nccp3l8d8n36akvaper2ngzpe8a843key0n985",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36261158806"
          }
        ]
      },
      {
        "recipient": "gonka1p2959dx973hd57qsalxvesrcv649296x90ry76",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "418573292641"
          }
        ]
      },
      {
        "recipient": "gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31449971534"
          }
        ]
      },
      {
        "recipient": "gonka1p57jas3hm3gmdvh64z92ycr28z968j0fn6n6jd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "147880703510"
          }
        ]
      },
      {
        "recipient": "gonka1pf4z32nqz5ax7zsxsmf4tan8wsnp957y9t4qtt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "126002462443"
          }
        ]
      },
      {
        "recipient": "gonka1pnfyj6kw3h3v2qu60j42j8h3cuf3jpqqgnaet7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "867026590443"
          }
        ]
      },
      {
        "recipient": "gonka1pvkv59e72vju2h7s9j3ex62c5xneqey350vpwn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "137751888201"
          }
        ]
      },
      {
        "recipient": "gonka1pzdzdgd3auppy7x8a73suxaucgjcutfevrwzjp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "862417979478"
          }
        ]
      },
      {
        "recipient": "gonka1q6v5taltnxxzjrgpheu5t7pfjwmsu6x8gs24sw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "161352027871"
          }
        ]
      },
      {
        "recipient": "gonka1q96dv6st48490vtzx2pwuwkjg439dr4hg6dzjn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1274458186245"
          }
        ]
      },
      {
        "recipient": "gonka1qjdt3qykdrka2am7s5rtrze44f7y8vccegjc70",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "158414671431"
          }
        ]
      },
      {
        "recipient": "gonka1qmlkwzrpv5zkzzpgkthftd29uqg0ka8dddc290",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "179533251351"
          }
        ]
      },
      {
        "recipient": "gonka1qre9aepalndahwj37xrcepndmut2vu9dr3kh4t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1qvpct2fqwpfqhznwjqs498ggp7wyxjkd4mvxhz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "176190742299"
          }
        ]
      },
      {
        "recipient": "gonka1r34p353cxrvxf3x29raz0x8axflen82a04env4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "304117679650"
          }
        ]
      },
      {
        "recipient": "gonka1r4qetzmw4g3aenwtcxpdm6l42aeq5gzwqltn39",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99211745951"
          }
        ]
      },
      {
        "recipient": "gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "253119094570"
          }
        ]
      },
      {
        "recipient": "gonka1rk43zfsxe7tefa88qh3t7wl3dvjwn3hq22njc4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "176950403447"
          }
        ]
      },
      {
        "recipient": "gonka1rpedugp4rhy989wfg8tr5ux7k6d4fhkjlqk234",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "187737591751"
          }
        ]
      },
      {
        "recipient": "gonka1rt963v04mgt43ju2smuakde99pv7wscy5yxnte",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "172595012864"
          }
        ]
      },
      {
        "recipient": "gonka1shc0ywxd993zz3w3h5xdp5uhgu9rv27ws7mmqx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "251042687432"
          }
        ]
      },
      {
        "recipient": "gonka1slnscxc26qm7vvpn5qs9yzq9n0l82r4ywkl054",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17117697872"
          }
        ]
      },
      {
        "recipient": "gonka1tvjdvlf3jmc48ckycguvdvlepgj7jgx9q5m2aw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "86854591274"
          }
        ]
      },
      {
        "recipient": "gonka1u60q4n3ymcglvhglylchpyvc04kvvurl967mgk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16712545260"
          }
        ]
      },
      {
        "recipient": "gonka1uk73fw4tnfv9rfdeekxycvt0v8cncr64syejra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "153704772313"
          }
        ]
      },
      {
        "recipient": "gonka1un2c9f66mg2g6xcpmulq9tqfs3vjd7nn0ftjs5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10000000000"
          }
        ]
      },
      {
        "recipient": "gonka1uv8lw89ththtj05c54wehfnqls9u2pza53q33z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "173101453629"
          }
        ]
      },
      {
        "recipient": "gonka1v425qs8gxupjcw3lqx5fsldtve88vd9gaa7r60",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "345240669804"
          }
        ]
      },
      {
        "recipient": "gonka1v5ggga7lslfg2e57m9anxud40v2s4t9dw8yj68",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "913213988252"
          }
        ]
      },
      {
        "recipient": "gonka1vkafyzr5yz5aht6gzapw6lc52h5wwmnrjwvqlz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "345645822417"
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
      },
      {
        "recipient": "gonka1vn6hk34wme5xvqzjmm26u9snkxg7nqd490gmwq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "347013212484"
          }
        ]
      },
      {
        "recipient": "gonka1vwsp87trl60t4g67fa677k7d7jztuc3g4qjc3w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "383578235749"
          }
        ]
      },
      {
        "recipient": "gonka1vxs4azxcym36wts0t7z5nj65ma8pnkvpmywxa0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82701776997"
          }
        ]
      },
      {
        "recipient": "gonka1w2pxkv4v6r5h6sdvges287l2g5rsd3r4x77080",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17320274178"
          }
        ]
      },
      {
        "recipient": "gonka1w3ewq7swwdxx8fsht8tl250f7qv44edhlltrh8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "210020985430"
          }
        ]
      },
      {
        "recipient": "gonka1w6cjf08fgm3yalqf7ytt0hz6thlhs53d2fn7j2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10331391615"
          }
        ]
      },
      {
        "recipient": "gonka1xteg3zgysvkvfl4lzs5gwxpkgtx0qra6m90jv3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "75712894434"
          }
        ]
      },
      {
        "recipient": "gonka1y29s2ckdl0csktxhpx77a7dvwyhj9u4xyrcynm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "183483489321"
          }
        ]
      },
      {
        "recipient": "gonka1y95qr73kms3zv5ju0kxtu58ksxdyrkyz8m0430",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "186522133914"
          }
        ]
      },
      {
        "recipient": "gonka1yk34z38t92jzjgq2ga7tkfpj07sf4ss3tj6n2m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157705654360"
          }
        ]
      },
      {
        "recipient": "gonka1ypy2ygsa7se9lrcwxlstgwsy0lfged0kg8ft95",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "197056101835"
          }
        ]
      },
      {
        "recipient": "gonka1yq4vwn7fc9x7lykjhc0x3e7r2atee32czy34mt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31956412300"
          }
        ]
      },
      {
        "recipient": "gonka1yquunstmnn35tuc6wsrlv020ul2rnuyldqkt37",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "991104577978"
          }
        ]
      },
      {
        "recipient": "gonka1z3kelh3gx3t6kz303f8trdll3j5ap3zz8csyfm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52416619224"
          }
        ]
      },
      {
        "recipient": "gonka1z4ldfav9tl7x3w9aqfry89zd0kt7sa2lhff6te",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "512771275014"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1t7mcnc8zjkkvhwmfmst54sasulj68e5zsv4yzu",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "500000000000"
      }
    ]
  }
]
```

</details>
