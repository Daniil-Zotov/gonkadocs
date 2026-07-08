---
title: "#46 – Epochs 132-247 compensation payout from gov module (batch vesting)"
description: "Two prior upgrades changed the lifecycle of unpaid miner rewards. v0.2.9 (proposal #26, 2026-02-01): when a participant is penalized during cPoC validation, the unaccounted portion of their epoch rewa"
template: proposals-proposals-main.html
---

# #46 – Epochs 132-247 compensation payout from gov module (batch vesting)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `46`

**Type:** Batch Transfer With Vesting, Multi Send

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">3,053,800 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/46){:target="_blank"}

</div>

Two prior upgrades changed the lifecycle of unpaid miner rewards. v0.2.9 (proposal #26, 2026-02-01): when a participant is penalized during cPoC validation, the unaccounted portion of their epoch rewa

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 3 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 4 | `/cosmos.bank.v1beta1.MsgMultiSend` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka17gpuntq09zsaqtmpe544gc32tk4424dwv5t34f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "257001064815774"
          }
        ]
      },
      {
        "recipient": "gonka12av9up884t9lcsf70rs0l7jfmkmc8k9sxfuknt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "255743613433661"
          }
        ]
      },
      {
        "recipient": "gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "146181292922666"
          }
        ]
      },
      {
        "recipient": "gonka1vjshzxh3sfam2xh0f7vzz4klrv5pkq4zutk8qt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "133077773396493"
          }
        ]
      },
      {
        "recipient": "gonka1famtxh54kad6ylwtm60j6d7h6unpc08d4vdqnk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "109602184403519"
          }
        ]
      },
      {
        "recipient": "gonka1r34p353cxrvxf3x29raz0x8axflen82a04env4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91015967243441"
          }
        ]
      },
      {
        "recipient": "gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "74190426382549"
          }
        ]
      },
      {
        "recipient": "gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "67057435920376"
          }
        ]
      },
      {
        "recipient": "gonka155cnj622zfdl64f23ljmk2tzv7tewl6fp4m2hl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59254989887340"
          }
        ]
      },
      {
        "recipient": "gonka1myu058axjs62mc3e7na9krwvqpfl9z3gtcw9es",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "56304331223331"
          }
        ]
      },
      {
        "recipient": "gonka1pvkv59e72vju2h7s9j3ex62c5xneqey350vpwn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "48774245916588"
          }
        ]
      },
      {
        "recipient": "gonka1v425qs8gxupjcw3lqx5fsldtve88vd9gaa7r60",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45239835425126"
          }
        ]
      },
      {
        "recipient": "gonka1umvyh0rz5fdmk9qhxurshhchennajced6f4s89",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45211223884337"
          }
        ]
      },
      {
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43574867284019"
          }
        ]
      },
      {
        "recipient": "gonka187tn9y92ur6tu0zf69u94hwl0q77m47y0k36hv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35326094895179"
          }
        ]
      },
      {
        "recipient": "gonka1llxvtg0657ldmqn4l3t0ag496ff355j5kawagy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34703179493138"
          }
        ]
      },
      {
        "recipient": "gonka1w6wwv3wq25p8qge4lqsnfzs8lsd3s8ty6au65p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34463669064904"
          }
        ]
      },
      {
        "recipient": "gonka1jltjehxsnum94nt8c00ts7khmpy4lafv6gryzk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31922079726022"
          }
        ]
      },
      {
        "recipient": "gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29700347178857"
          }
        ]
      },
      {
        "recipient": "gonka1yq4vwn7fc9x7lykjhc0x3e7r2atee32czy34mt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29575164563616"
          }
        ]
      },
      {
        "recipient": "gonka1pllyukkeymx3hfd9mts3pryr9y6efs9eshty87",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "24858173755208"
          }
        ]
      },
      {
        "recipient": "gonka1zrnrd7zcqnhjytqa8zsg63slxt2g45ctlqy3fm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23491990914627"
          }
        ]
      },
      {
        "recipient": "gonka1022747hjz6sdfeup0dalcys6hshlqlnnpkdmqk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23169453291659"
          }
        ]
      },
      {
        "recipient": "gonka1zap7nsccl6x83ucwvq0q6qrefmf9n7ejmj49j3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23114014245507"
          }
        ]
      },
      {
        "recipient": "gonka1ln28jur0gvuwf8frx63lwwagysdf03e8ldayf3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "20534659528938"
          }
        ]
      },
      {
        "recipient": "gonka1f7d43z2qpcv07huwf3qjj4zpssvx6080a357wh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "20232541892180"
          }
        ]
      },
      {
        "recipient": "gonka19ghzvgfr065s3fr5awuvs3nhy9fq4n7wrr9kel",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19798354315593"
          }
        ]
      },
      {
        "recipient": "gonka1f5fhrywmd5p0jcd5atk4rm2tjxpdn772lw833k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19460684093418"
          }
        ]
      },
      {
        "recipient": "gonka1w6kt2aj02du25kuc9wsza94h9l7exa0uf64fjq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18811567809251"
          }
        ]
      },
      {
        "recipient": "gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18694274050888"
          }
        ]
      },
      {
        "recipient": "gonka1kzmqu27lhan874pzxr0fy0v7xqyenydh9mp8sj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18036443683332"
          }
        ]
      },
      {
        "recipient": "gonka1hqwfnnh30scu6lyzhl5alwjqmaeq3vhkcfxkgu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17681834939234"
          }
        ]
      },
      {
        "recipient": "gonka17rfqamx8vr4zpd6z0jnulre4acht2lj7tq205e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16531786626167"
          }
        ]
      },
      {
        "recipient": "gonka1uzk2scggfzghr9a5j92l00gzw4jx4adc66977y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16134062752611"
          }
        ]
      },
      {
        "recipient": "gonka1m9sf2rpg635efaw59djqlxkqew9sxvmqd6g343",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15283991233760"
          }
        ]
      },
      {
        "recipient": "gonka1rdarkrtrfnfcvrnf58jyndccqj0r4k630n38rh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14730803064393"
          }
        ]
      },
      {
        "recipient": "gonka1ffjt0acf87chys5w93wsrdj2s94rrmcq8mt48l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14595703339352"
          }
        ]
      },
      {
        "recipient": "gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14474260304851"
          }
        ]
      },
      {
        "recipient": "gonka1cw859nqcd9mg3y3alraluswu55xz9j36evsxd3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14322176494890"
          }
        ]
      },
      {
        "recipient": "gonka1ag5r7em9qp7dn8nf6jecudhu38amu3nwtqv3cg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13573694792548"
          }
        ]
      },
      {
        "recipient": "gonka14ued4vcdeluj9v9vmsmteap7vtg7t50640hvmf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13242399993440"
          }
        ]
      },
      {
        "recipient": "gonka1jv4fcx2gtuj4ejwnng4phugfclgjmhvg9d9cvz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13080046839379"
          }
        ]
      },
      {
        "recipient": "gonka1fkrsesmn2hdj30fhwyam6h4f2e77un36xalhvl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12497662398412"
          }
        ]
      },
      {
        "recipient": "gonka1lrls7q8nu8rhjgchctswfsjlnjh84vwycw3jgt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12126284267879"
          }
        ]
      },
      {
        "recipient": "gonka188c86f9mrlt4nlcg89f82nnfm9jzq9gtjafj50",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11969739290348"
          }
        ]
      },
      {
        "recipient": "gonka1apnzzz6wlpevze3vzsmk7n0vp6az5609magdf6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11932993515432"
          }
        ]
      },
      {
        "recipient": "gonka13pacjyw9quwfvzllp2h7u27h6f5khqlftw3jmk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11908860089941"
          }
        ]
      },
      {
        "recipient": "gonka109g8dnt43nj45xhg83jyjt5f2ywz336w36qzyl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11857109690479"
          }
        ]
      },
      {
        "recipient": "gonka1ea4hhgnahtu4g0zzpmz2p8elcyx7x99hamk0x4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11834634316463"
          }
        ]
      },
      {
        "recipient": "gonka1dms4wtzer5zjx32c3grc5twksd8kdp0ut952g7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11804999068025"
          }
        ]
      },
      {
        "recipient": "gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11775889822160"
          }
        ]
      },
      {
        "recipient": "gonka1caju8tg6yg3wkvryhks57jwd8des6ssypfrhhj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11755346548282"
          }
        ]
      },
      {
        "recipient": "gonka1vkafyzr5yz5aht6gzapw6lc52h5wwmnrjwvqlz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11717956702716"
          }
        ]
      },
      {
        "recipient": "gonka1yn54kaefrf7sjk66c74gqap0mquzjqvthsyhwe",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11673458189519"
          }
        ]
      },
      {
        "recipient": "gonka1h3s37p0l23mg6ak9h9nmayh6r9f2vm6umj3qet",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11513343140557"
          }
        ]
      },
      {
        "recipient": "gonka167mtkjz3c7k4mnv77zgneul4eakz35qqysgj2l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11305089109736"
          }
        ]
      },
      {
        "recipient": "gonka1wr20kvjrm6y6cvqk7jt2e5gpyl45qq3mvt7sr4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11078446910205"
          }
        ]
      },
      {
        "recipient": "gonka1m08n5646hjpavvmjfarad9kr9pxufe7sfy3v7e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11016071211074"
          }
        ]
      },
      {
        "recipient": "gonka16sthutkxgr88vlkgvqak2h7pdt76fcznfz6w43",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10921214768840"
          }
        ]
      },
      {
        "recipient": "gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10711052597420"
          }
        ]
      },
      {
        "recipient": "gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10356524697948"
          }
        ]
      },
      {
        "recipient": "gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9988586022231"
          }
        ]
      },
      {
        "recipient": "gonka10etnufq85u67k075yuxq6h3rzwlcln5rffhlyx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9921527771819"
          }
        ]
      },
      {
        "recipient": "gonka1zauv3up2rp4al5lhsqnqfh2kqfx2zvy3l0qwss",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "9155922064919"
          }
        ]
      },
      {
        "recipient": "gonka1apw5tzk6a3l9hdpdx5q9v2leehvz5rvvw44x8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8903896410063"
          }
        ]
      },
      {
        "recipient": "gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8669865143449"
          }
        ]
      },
      {
        "recipient": "gonka12mqkaycdsc7qr37ey5rqw6vhjvkk7waxdc7rjh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8536705102147"
          }
        ]
      },
      {
        "recipient": "gonka1z3kelh3gx3t6kz303f8trdll3j5ap3zz8csyfm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "8325426582463"
          }
        ]
      },
      {
        "recipient": "gonka1756ph2flj5y6kw5xqktfgwj3s2ct54ddz0jj0e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7783596922366"
          }
        ]
      },
      {
        "recipient": "gonka1aazyzjuywye4530acgjgw0stu4ydpt9hv4afut",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7472635175272"
          }
        ]
      },
      {
        "recipient": "gonka1vdw6tst3lelc84garssnnjzx7fjpkja2wzpxe8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7257439323925"
          }
        ]
      },
      {
        "recipient": "gonka10vljxvwy6n9hh263chkt0hj0kg7t0qmdwfrurs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7126663727384"
          }
        ]
      },
      {
        "recipient": "gonka1y95qr73kms3zv5ju0kxtu58ksxdyrkyz8m0430",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "7004483068232"
          }
        ]
      },
      {
        "recipient": "gonka1shc0ywxd993zz3w3h5xdp5uhgu9rv27ws7mmqx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6835043483003"
          }
        ]
      },
      {
        "recipient": "gonka1hszud9tlfe7qs2elkjmmkavk5yhrdned587frx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6775865712894"
          }
        ]
      },
      {
        "recipient": "gonka1p2959dx973hd57qsalxvesrcv649296x90ry76",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6713217861349"
          }
        ]
      },
      {
        "recipient": "gonka1rxprdtkfpkszyx3zvyerzk0z52uqpn85wpfvdj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6510598709806"
          }
        ]
      },
      {
        "recipient": "gonka16p322ch887xjv67erm5dw0lgt4kqj9gz498pv7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6442327838961"
          }
        ]
      },
      {
        "recipient": "gonka1ad7al35f74hdlwl5vzmqla4gg3zlajthqsyeva",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6326560493160"
          }
        ]
      },
      {
        "recipient": "gonka1kyl5le4t0k9dftmu5lj0xqp0dx52dyvn0rtr8y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "6235376338191"
          }
        ]
      },
      {
        "recipient": "gonka100k8hr43z5vp0fnyc94m7lum6mj4st6vksxz8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5805465594251"
          }
        ]
      },
      {
        "recipient": "gonka12gwxa8vcvahyd4ygcxp4624ywaw98wp953wuva",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5785980666618"
          }
        ]
      },
      {
        "recipient": "gonka1fyghf5n3uk7dtl529mxk6389vryd4xvnh93825",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5740322096699"
          }
        ]
      },
      {
        "recipient": "gonka1lr9mj6dgkv0h76c8y8w0l3esztyg9v2q8d6d8d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5649008951922"
          }
        ]
      },
      {
        "recipient": "gonka1v6gqe8zaqqmlevnmpxa6chjy9mt422mac2lhwc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5626416345685"
          }
        ]
      },
      {
        "recipient": "gonka19xadn767xykcg4j5jl6nxk55dsdr2muu9r3fhy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5420417253933"
          }
        ]
      },
      {
        "recipient": "gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5233882003557"
          }
        ]
      },
      {
        "recipient": "gonka1z7h4mzz5kkcydj4l6lzr9j73x49dlcq84mmkrv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5225544478337"
          }
        ]
      },
      {
        "recipient": "gonka1z8dh5kqdn2nnsg527qawy58ca5fme38xffq7ah",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5150029035155"
          }
        ]
      },
      {
        "recipient": "gonka1lh0danzlvxm5qtaly7myqd3n5sus0fq92n8shx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "5146315546795"
          }
        ]
      },
      {
        "recipient": "gonka1vcvn2p5gczr5pynqq0ca0933tdrf5w64sjgtdg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4919938488061"
          }
        ]
      },
      {
        "recipient": "gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4894031265459"
          }
        ]
      },
      {
        "recipient": "gonka1fc9tzt83dgrqswlgay4668cuqjrk7zsqks2vm2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4879946653867"
          }
        ]
      },
      {
        "recipient": "gonka168yvlgt9jg86frg2z90cc8w4pz9hnd7f8lshux",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4828093037828"
          }
        ]
      },
      {
        "recipient": "gonka15kf06ehfplnqtvgnndyfym9w9f63686cvw3nqj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4809487452462"
          }
        ]
      },
      {
        "recipient": "gonka18v2az8fn2z28ykxu7zyc09crqdmjuldmnag0g2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4766372692428"
          }
        ]
      },
      {
        "recipient": "gonka12s5q7gzej93ty6ydqrr4ugwrt26zcwtggamz0k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4615281886684"
          }
        ]
      },
      {
        "recipient": "gonka14cu38xpsd8pz5zdkkzwf0jwtpc0vv309ake364",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4508685844396"
          }
        ]
      },
      {
        "recipient": "gonka1jrkf560tvgqw3f9z4axs9da34lgnrd396e3rs0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4504841695639"
          }
        ]
      },
      {
        "recipient": "gonka10vh6xfdrksy7npapnhs6pnwmd3ldpxgl8n2gdd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4499200011386"
          }
        ]
      },
      {
        "recipient": "gonka19pve9p3eth8j7ssv7k4f57lljrtjtl6mjgnuxq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4394936385598"
          }
        ]
      },
      {
        "recipient": "gonka17t9elrdnnzqd5q2w240ue47tn253gjuhpkflwx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4374758888276"
          }
        ]
      },
      {
        "recipient": "gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4258606767870"
          }
        ]
      },
      {
        "recipient": "gonka1u4gtnwh0hvzlyvran3l7my7hr883ej367ed80r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4251488209351"
          }
        ]
      },
      {
        "recipient": "gonka1ux86q8cgnpvkal497xag8p04ds2u2v23qxawv6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4240884907658"
          }
        ]
      },
      {
        "recipient": "gonka1r288zwzcvw87qeyk7tdwe29nux2s4wxzustuk8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4232778601728"
          }
        ]
      },
      {
        "recipient": "gonka13rcy8ytzdfyfz8jx5l3ru0l093k7mp5e9waanq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4199542856791"
          }
        ]
      },
      {
        "recipient": "gonka19dh0tamdjnhtccfdpmsnty3gxfpp0wkdusl0xr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4118725388207"
          }
        ]
      },
      {
        "recipient": "gonka1t8x0m85qvyfzvyevwrj2m28ytf6w3kmlf5r7ez",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4080444259026"
          }
        ]
      },
      {
        "recipient": "gonka1wvv656pt2d8x2khcvytqeessck5uzjnxzsa8f6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "4004509906206"
          }
        ]
      },
      {
        "recipient": "gonka18hns0dspklh6r89nyeg8qaph4vhfkd63tl7a37",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3987721650077"
          }
        ]
      },
      {
        "recipient": "gonka17ef5hl0588tmjm9ypw7t2kge78wrkcpvyspc0p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3672928729539"
          }
        ]
      },
      {
        "recipient": "gonka19s3wpdecq3znh7gflv5xax06p96s2uv3qdrtup",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3669248888230"
          }
        ]
      },
      {
        "recipient": "gonka1aun6f73uq2r5fujk38xe0tww980r6a0lz6a45g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3621234292444"
          }
        ]
      },
      {
        "recipient": "gonka1ltv80h8740pc8u4jj7fqwvt8d4rnw3nkc4shaa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3457371816527"
          }
        ]
      },
      {
        "recipient": "gonka1zpw8tml8xl4fm6zm8zpf2u4pq4tehmd9e2vgq7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3362231861628"
          }
        ]
      },
      {
        "recipient": "gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3285555682598"
          }
        ]
      },
      {
        "recipient": "gonka1yd8s6z8enw080kj2wgynuwdxzx40gttchqe4za",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3258863349046"
          }
        ]
      },
      {
        "recipient": "gonka1vwsp87trl60t4g67fa677k7d7jztuc3g4qjc3w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3221665521411"
          }
        ]
      },
      {
        "recipient": "gonka1r5hdy9q5v783ef7td98k4c68cxl6a58h5sytfq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3220639632240"
          }
        ]
      },
      {
        "recipient": "gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3211234640565"
          }
        ]
      },
      {
        "recipient": "gonka15suq3puxz0ec7fnyurwf47qn8jqs8trhyw0uau",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3149836763605"
          }
        ]
      },
      {
        "recipient": "gonka19dqylqjzp4x04mkktz067l4exrcrg8g7777777",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3133323012338"
          }
        ]
      },
      {
        "recipient": "gonka1k7qdnu46x2uyta6fuja3jsmr2cw7ta38krfhfv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3065588470988"
          }
        ]
      },
      {
        "recipient": "gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3017095901974"
          }
        ]
      },
      {
        "recipient": "gonka1svynlfqqsxzuxfm67lgy986438h6l2u8tz4clj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "3012757568456"
          }
        ]
      },
      {
        "recipient": "gonka1zpm8qujddac84y7wfh7h3p85ys336n9zjqckzl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2999175542710"
          }
        ]
      },
      {
        "recipient": "gonka172esz53695ykvv038y8mvdfc6mkk2q0dgfmjks",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2941665532530"
          }
        ]
      },
      {
        "recipient": "gonka1zsvl7ujlc8z3a35v2q6e3nml7ftyk23v76jqgl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2926379308218"
          }
        ]
      },
      {
        "recipient": "gonka1czmu5smv804kq6pqtyvmjxcjjj720mgl4xc3hd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2797625789804"
          }
        ]
      },
      {
        "recipient": "gonka1f37ltf3h2fcytmxf5svyc4w88k5wzsammgyk69",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2785737330882"
          }
        ]
      },
      {
        "recipient": "gonka14c0vannxsak0qq4lpmr5qkn40gcfmcvnyu4z2r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2765024397341"
          }
        ]
      },
      {
        "recipient": "gonka157lvhw8ay84qf6xs6rhvud7hjpnsp5zdcqg0s5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2739159995711"
          }
        ]
      },
      {
        "recipient": "gonka1yewc6rmr5zhcpy6dnpt4wup990j299qt03x40s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2614646090348"
          }
        ]
      },
      {
        "recipient": "gonka1nzjz6svr80uqt49r6u409rsq3skd7fqdmz0lks",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2597919588432"
          }
        ]
      },
      {
        "recipient": "gonka1zqqrnrlnam5knwvpmxvlpj4za04t62pxzh65y4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2594962821488"
          }
        ]
      },
      {
        "recipient": "gonka1zvpy47fagx96g8zzhwwxu9yztke82cqvwearsg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2593764205535"
          }
        ]
      },
      {
        "recipient": "gonka1g3xpka5ynkdgspd2r2atma4vzlklrz0kssez0d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2586979530168"
          }
        ]
      },
      {
        "recipient": "gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2579411768290"
          }
        ]
      },
      {
        "recipient": "gonka18nzvzzync0v9q73ka2jsh05ptmhda73t8g6gzl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2554062642627"
          }
        ]
      },
      {
        "recipient": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2526605346157"
          }
        ]
      },
      {
        "recipient": "gonka16q0zaetd6hq6d8zj48ur0v967xrrwh566kcazc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2525839052072"
          }
        ]
      },
      {
        "recipient": "gonka1mwwzgd5qztcjddg2pwej0xw8xywqr5l4san6ee",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2516239230812"
          }
        ]
      },
      {
        "recipient": "gonka1p2hqmt2lxgw5ctdlt6valanxxqsmtf73g27mpg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2487864393256"
          }
        ]
      },
      {
        "recipient": "gonka1m27e6qup7q8jmvnrn29kahd7vlx6r4l84z4thz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2475577450540"
          }
        ]
      },
      {
        "recipient": "gonka1wj0jmwtwjk0g05tuugh9t028nxl92qrn7e8ajy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2448108786799"
          }
        ]
      },
      {
        "recipient": "gonka1a3urcggdzkamu76nd847034z7w6kx2en46jzan",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2438132794092"
          }
        ]
      },
      {
        "recipient": "gonka1snq79gf7l5kjm00gkdcu9dmpwzk207eq07nuue",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2431479512542"
          }
        ]
      },
      {
        "recipient": "gonka17wmjdfda8tfkfujp24usqzsxv32vrycnhvj3cl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2410047815267"
          }
        ]
      },
      {
        "recipient": "gonka1uawu7tlxcuss8xk9m63fpjm86y58chsg5xwsjt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2307961462204"
          }
        ]
      },
      {
        "recipient": "gonka10yvlwvt2t3eqrze399ky2wtqfr507zld06wn9m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2291889908713"
          }
        ]
      },
      {
        "recipient": "gonka1vn8dkrcwmqet2954u7zxt6e3q4q5p87zf4ug8m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2274332708925"
          }
        ]
      },
      {
        "recipient": "gonka1wtg6f6xstldpe4ty2khcf4h7ggkwhyez3f5xn9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2211681613298"
          }
        ]
      },
      {
        "recipient": "gonka1zr82xvxge0n8hf2u9ysrvfgr8u5lcvrqwc6ufx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2184531466278"
          }
        ]
      },
      {
        "recipient": "gonka1zyh5wtm75k9hnwyavx9uhserp9hf7mnw7m8tzk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2180450032879"
          }
        ]
      },
      {
        "recipient": "gonka12nwehnhahquy97ulu8824pnw9p0fszxzpnexk7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2164973775818"
          }
        ]
      },
      {
        "recipient": "gonka134gw5wnwukm032r3xn4fe73ptrfqewjwnj42q9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2122972978099"
          }
        ]
      },
      {
        "recipient": "gonka1nwkzwsy9msnvw6dvx7dwyvqgpzrll5th3qjnqx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2114472670926"
          }
        ]
      },
      {
        "recipient": "gonka1vvnnc0aw2v8j8zarm7p0egfgajpmus23sm8gd5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2113698536568"
          }
        ]
      },
      {
        "recipient": "gonka18gjl3tetpx0qdknl0vdhhducfycggpjrrjy6me",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2112266881636"
          }
        ]
      },
      {
        "recipient": "gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2097917153622"
          }
        ]
      },
      {
        "recipient": "gonka15x0egllrr3wlucagztrpf7u8365zdjjy3qh8aa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2095430372995"
          }
        ]
      },
      {
        "recipient": "gonka1vy396smh98ak3ts4zlthjnsv2ypr845mrfz7x5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2094173145999"
          }
        ]
      },
      {
        "recipient": "gonka1dg6s2c2mrwg972xs7309nh57t7q98hqv99jew8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2087135335497"
          }
        ]
      },
      {
        "recipient": "gonka1zx097psrq9p99yz8src4henyrtsdpjv3n7hp5u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2071309702684"
          }
        ]
      },
      {
        "recipient": "gonka1lv34hh600uye40wjjq9fspqwernyjqjuz92w8f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2063313281497"
          }
        ]
      },
      {
        "recipient": "gonka1tx980hp394dfn80rut6gr3j5yujz7wdl08dups",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2050662840697"
          }
        ]
      },
      {
        "recipient": "gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2047604055909"
          }
        ]
      },
      {
        "recipient": "gonka1ymupls5cj6dfkvppeetcfpkszqxmyyrjtsn5pz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2046231858543"
          }
        ]
      },
      {
        "recipient": "gonka1hytku6t3cfd7wppyrjvu357jjqpsgsw6wcprcy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2034728655450"
          }
        ]
      },
      {
        "recipient": "gonka1k3xh9h66ye5pdgv2v94xhf7paz445e7qwraz7h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2025139415576"
          }
        ]
      },
      {
        "recipient": "gonka1nkedq5vefl0xlxf66cgpx5l6eldtjtr3e2q5sp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "2014461604344"
          }
        ]
      },
      {
        "recipient": "gonka1a3f2cpds29pq0x7yvuh5we233l6aytcgl8gtlx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1999560523360"
          }
        ]
      },
      {
        "recipient": "gonka17v3mupkkl6gapd2nfe8n442npj0vm8tezv53rx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1988287022886"
          }
        ]
      },
      {
        "recipient": "gonka1eazh84v0e60s9m7exxp3nsadcfgvnsthgypjvl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1981994552976"
          }
        ]
      },
      {
        "recipient": "gonka14pdvgt025fwkf38cr74hhcj2nfl98c044tswya",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1978853219827"
          }
        ]
      },
      {
        "recipient": "gonka1l4vfzkwd555pvxqzr3ksphgwgv8xsh89ytmjp0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1974075810606"
          }
        ]
      },
      {
        "recipient": "gonka1x5fvtepacy4gk0nsjenj0fgs46jmhs22an4zyg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1950427976353"
          }
        ]
      },
      {
        "recipient": "gonka1d7p03cu2y2yt3vytq9wlfm6tlz0lfhlgv9h82p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1950216716356"
          }
        ]
      },
      {
        "recipient": "gonka1kwflqwdrvk6ax62er4tkdwmjayh3eq80ketq2u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1936371393787"
          }
        ]
      },
      {
        "recipient": "gonka1kk9m3h8y5qg2qt50m4htdczlmu9nuvgssa7wvx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1930810890692"
          }
        ]
      },
      {
        "recipient": "gonka18zc66p9kmjxe43zfm0ckmzds2aey7nd7lz7tju",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1911831420473"
          }
        ]
      },
      {
        "recipient": "gonka1llgg3kvg9sc6xz09jtkcrucrppxgn78xe4xlv0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1909204747983"
          }
        ]
      },
      {
        "recipient": "gonka1sszyf9vva7xvyk84fnc7zwk0gde3avrhstp8yq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1898302802394"
          }
        ]
      },
      {
        "recipient": "gonka1ntsw9ufhpvzan82lhe496zhdqvfy9rptm6rr5s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1882174535198"
          }
        ]
      },
      {
        "recipient": "gonka1hr7tssnwuw7jk8s4gjf8uq6k9aw2evnygsfd5y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1881610689490"
          }
        ]
      },
      {
        "recipient": "gonka1py4j23jhz2nah9d8lqpxn2lq6e07lx6e6jmaym",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1869327972267"
          }
        ]
      },
      {
        "recipient": "gonka1y29s2ckdl0csktxhpx77a7dvwyhj9u4xyrcynm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1868663974330"
          }
        ]
      },
      {
        "recipient": "gonka13yg0vc937qfnhc0lr7c57cr63edl5jxh6g6sds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1856520150195"
          }
        ]
      },
      {
        "recipient": "gonka1nrutssh27xyjxa2a3x7xqs5j72uwfcfhkux0lq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1852033816609"
          }
        ]
      },
      {
        "recipient": "gonka1mrjfnu5n4cpz0kc6ctkj7m6wyydgjstje8yyg2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1832711080363"
          }
        ]
      },
      {
        "recipient": "gonka16gmle2g7g0n654xpq5sq6p4kakwhyglzwzj84x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1823343472413"
          }
        ]
      },
      {
        "recipient": "gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1809157685416"
          }
        ]
      },
      {
        "recipient": "gonka1z4ldfav9tl7x3w9aqfry89zd0kt7sa2lhff6te",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1793236353527"
          }
        ]
      },
      {
        "recipient": "gonka100yl7qvcpdrt834zay8wusptg8g6yrv4p7fh4w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1772948015912"
          }
        ]
      },
      {
        "recipient": "gonka15uz4vcp4r0yrn3wy6lw7kslcv75l04cmy5vfac",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1766341236334"
          }
        ]
      },
      {
        "recipient": "gonka16k03ze5ynkprsd4n6e5uzhthvu9jjk553rauqy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1763176140135"
          }
        ]
      },
      {
        "recipient": "gonka14a0856a3q78pmesxpc946xm9nsj3f275l9f5pa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1762281983678"
          }
        ]
      },
      {
        "recipient": "gonka1t8p0tjqls358gmzvd3rnnjulraq2k3m772vnt8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1760449387496"
          }
        ]
      },
      {
        "recipient": "gonka10dmnjuj9pyxk8zcyhykccr2pte2e8sj93e2ljp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1743800721431"
          }
        ]
      },
      {
        "recipient": "gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1730972390651"
          }
        ]
      },
      {
        "recipient": "gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1729511203691"
          }
        ]
      },
      {
        "recipient": "gonka1uqdg47fc37pxn0px59mgs6jaxzyu5axjsunqcn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1722700206424"
          }
        ]
      },
      {
        "recipient": "gonka145666cll76ptcyy9ceymtalr8gnvv73ne99p32",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1721387071686"
          }
        ]
      },
      {
        "recipient": "gonka1slndy4rsmld579628302rj5gz8z9qf4v6ppmc4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1720964413511"
          }
        ]
      },
      {
        "recipient": "gonka1k3lva2jsxu5qx30f65yxdlcey8d6f3unmy2gks",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1714912277605"
          }
        ]
      },
      {
        "recipient": "gonka1lq2qtfapw52lkqnwkadr9a7yyhzllz32hhg75l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1712950116810"
          }
        ]
      },
      {
        "recipient": "gonka1qraf3edrgj8j0jmm9p709p8jver4kfa5qm2dlw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1712937593153"
          }
        ]
      },
      {
        "recipient": "gonka1dpt9zx2dqcky6yjjwrd8xz2w7lq6vffy9mhvgs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1710228510544"
          }
        ]
      },
      {
        "recipient": "gonka1l44nacmpmt83kavvevmhlh8elspjtjn6wvwzm0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1705987345103"
          }
        ]
      },
      {
        "recipient": "gonka1st0kn8x2slqc4ruphzwcsqux8fz4y9fxkgny2p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1703111172537"
          }
        ]
      },
      {
        "recipient": "gonka1sa32xmpxvv7nepfc22004rgdl4ddjvne42guce",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1701186828287"
          }
        ]
      },
      {
        "recipient": "gonka1y2gqpy8533d23dyuwsx67snesddu2w6pf4la73",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1679548662497"
          }
        ]
      },
      {
        "recipient": "gonka1d0cekvf368psxff6ur7pl42vvs225rzu9a76nj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1676087196251"
          }
        ]
      },
      {
        "recipient": "gonka1ju7jfznld7vg0f35wgz507m6c0lzgugpmajnvn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1657983373908"
          }
        ]
      },
      {
        "recipient": "gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1649092472277"
          }
        ]
      },
      {
        "recipient": "gonka1x0tmf77y7pgwjz3pmjtdphr6gr264fsya0ck97",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1644308356211"
          }
        ]
      },
      {
        "recipient": "gonka1ge9amk4ymld27d35akj3ky9uph4gyz6rdpepjj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1640782235179"
          }
        ]
      },
      {
        "recipient": "gonka18vjpx0ju0su0t89y3gjvktsx9cak579a8tvzlv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1640531529430"
          }
        ]
      },
      {
        "recipient": "gonka197mvutfxtz0kfuttd8pedys2qscffqatzf7cks",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1635594374059"
          }
        ]
      },
      {
        "recipient": "gonka1p2hcr8q3zst98rnw5t2ek7ah04xc7avjyqsykx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1635540874840"
          }
        ]
      },
      {
        "recipient": "gonka1jnvpyydsxvqx484qua8nj6sm8gw7zq0jrv5qch",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1624531548601"
          }
        ]
      },
      {
        "recipient": "gonka17pnpw8uphnvsehcdpsxuar5nctlksvftlpvfcm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1612758520040"
          }
        ]
      },
      {
        "recipient": "gonka1pxnftcgh4cf20326zvqxu7d8zmwrpfn07qmpn8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1610736048493"
          }
        ]
      },
      {
        "recipient": "gonka1s5vtmnn8tqvqfh7gd9hv48kkt2t4mkh7s85zh6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1600385389897"
          }
        ]
      },
      {
        "recipient": "gonka1nkmwp905ka4dzvuwvdaudgjj7yjk8h5aslfw73",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1587901780412"
          }
        ]
      },
      {
        "recipient": "gonka1450wvd5uugfj7gru4heut5ulnneunplvxs995e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1585492932064"
          }
        ]
      },
      {
        "recipient": "gonka178p3vw9zxs885l4a29g3sep0v9uplfq4pzvmrq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1568245761958"
          }
        ]
      },
      {
        "recipient": "gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1550424742012"
          }
        ]
      },
      {
        "recipient": "gonka18gx37lvw563n8h27zg4r86hpxyhfkrnc9v8gsx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1545986812272"
          }
        ]
      },
      {
        "recipient": "gonka1rcxn206a5smzzhd3g0edgg6tyv97jk052nc9fx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1543746149423"
          }
        ]
      },
      {
        "recipient": "gonka15ye48c3rp57hwt9t6tzc6h0t5sh88zvj0yznwn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1542148067169"
          }
        ]
      },
      {
        "recipient": "gonka1czjrfgs9xfuax25j8nsjrdklzn6repcn25zjxd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1533880283950"
          }
        ]
      },
      {
        "recipient": "gonka14s76f83l8m3guvr8vu54dmla798jzy3u09vxzx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1532015935333"
          }
        ]
      },
      {
        "recipient": "gonka1sgpe9jdpa407ykm537demqj26xn7x88ayjdzly",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1529218270093"
          }
        ]
      },
      {
        "recipient": "gonka1gstreuc0fz4gksar9sx2uzg4au2k7k83cremld",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1503708999515"
          }
        ]
      },
      {
        "recipient": "gonka1xkk2g9t0t7euahr5wtjerv7tng3pnrcl0h3gcz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1496033993846"
          }
        ]
      },
      {
        "recipient": "gonka1m3vrwz0e6wmclfl3kmwvqq4j7pl65nmvhuz0le",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1493192656255"
          }
        ]
      },
      {
        "recipient": "gonka1nrf23a58fa0t0haq584272lsw2tfkm553l04a0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1467443775463"
          }
        ]
      },
      {
        "recipient": "gonka1x3wd5ypslj50nk9cvs72e3re9mfcdpcqwhnulj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1467176555799"
          }
        ]
      },
      {
        "recipient": "gonka14vyhz7henu2lxssa02lf3qwmufv8kvxzn85frf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1434213603092"
          }
        ]
      },
      {
        "recipient": "gonka188qynuf5zs5966vzlrf2q2tj7h7laa995vrxr3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1432954903593"
          }
        ]
      },
      {
        "recipient": "gonka1dx3kzqghjsfr4scjvmy0lvk4lk7qhvh9n358k2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1429796170034"
          }
        ]
      },
      {
        "recipient": "gonka1juwk05glldgn7850a3547jsl7l4vrhx9k5g3cr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1423107302701"
          }
        ]
      },
      {
        "recipient": "gonka1ccdm8j6sjyhq4qask049dwgaczs7f3pxte6zmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1421622489933"
          }
        ]
      },
      {
        "recipient": "gonka1q4mexpvre73dwjaz93xuwwxgh5526pe2ps2eec",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1417150602535"
          }
        ]
      },
      {
        "recipient": "gonka1qmpm8tsynnfkqe9902dd6ny4lc5hvp8q7wkrpc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1402806799218"
          }
        ]
      },
      {
        "recipient": "gonka186ghmxetau6dykfzqdqxe7vhra5w77e98gcdn7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1382392335195"
          }
        ]
      },
      {
        "recipient": "gonka1ctz9hz6c2pc9hpj5qsw83fmmf9uekqesg4k9sh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1380013105932"
          }
        ]
      },
      {
        "recipient": "gonka1mhepzjgj5asrx2rjh69ckdae9cuhaynqtuv4sp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1376447164167"
          }
        ]
      },
      {
        "recipient": "gonka1dzdmx5ljrwkelrmgd7suv2q43epn293qacpgqn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1352946136845"
          }
        ]
      },
      {
        "recipient": "gonka19zxzp5xlgj0gq7xlnfhaqcedjrqv0jhpq3zdwc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1344056281126"
          }
        ]
      },
      {
        "recipient": "gonka19sf4axsacdphm598alpxt7t2qpacxttdmj5e06",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1323698843693"
          }
        ]
      },
      {
        "recipient": "gonka1ekx3z5gm4azxvsectsflhpul24d06x7rz978d5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1315872206099"
          }
        ]
      },
      {
        "recipient": "gonka1jvmumx6rwyq302m6y6z5hdkc4cgu845mcgjwud",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1293131959851"
          }
        ]
      },
      {
        "recipient": "gonka19f9hkpmjaldncsfly4j63sy932y8hughn4l3d8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1288877578717"
          }
        ]
      },
      {
        "recipient": "gonka1qx3znmtpxqgmz3t4tgpdk68dsfxuccn6cxnp8s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1288707962259"
          }
        ]
      },
      {
        "recipient": "gonka14yprk25twtverkpcsdgnrg5raeuycmkl5dwa34",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1276582463923"
          }
        ]
      },
      {
        "recipient": "gonka1lecmns7dj5wm8f53pe6c8nueukqafknel2wt2m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1269049737730"
          }
        ]
      },
      {
        "recipient": "gonka1lswsj2x7u4606wqpunmm07skgf76r3dyz4v0d8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1241250357209"
          }
        ]
      },
      {
        "recipient": "gonka1d5c40gkxqycyxpmup22lw0sp3e3pxat9aee7sx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1236651340303"
          }
        ]
      },
      {
        "recipient": "gonka14qwpw2l0qmevxy9snllfaw0r9svnh4vdyl3897",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1229611229584"
          }
        ]
      },
      {
        "recipient": "gonka1hx9a6297776yndfgajr7tc3e9kj96t77m4xxf7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1228846322760"
          }
        ]
      },
      {
        "recipient": "gonka1d5nn7u0hq0pumgmfxk95nj5h3zkuskkdh96dzd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1211538663678"
          }
        ]
      },
      {
        "recipient": "gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1210731495895"
          }
        ]
      },
      {
        "recipient": "gonka1u3fmal7ep88gcgauwe09zk8e77985cqmeuu2fc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1206598666620"
          }
        ]
      },
      {
        "recipient": "gonka1n6uaty84yezgfcymndq75nmza8y8krt9j0czjm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1199452287667"
          }
        ]
      },
      {
        "recipient": "gonka16r4kxszdpa6k7wakgt6wk6vus6txhqwqd5drkh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1193662593554"
          }
        ]
      },
      {
        "recipient": "gonka1h5cc5829dh3260vmnugr5vp0nac7mmktrrhe6l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1188612232016"
          }
        ]
      },
      {
        "recipient": "gonka12dvpyn0a2tvuc28vanrj7nr7d8ez022mms4vf2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1186466441984"
          }
        ]
      },
      {
        "recipient": "gonka1j8l7fcxqxakp2py7jcgh27ccgxaze7krscxfe5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1169732083672"
          }
        ]
      },
      {
        "recipient": "gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1167393439685"
          }
        ]
      },
      {
        "recipient": "gonka1mtahyzwk726p50mqkj2n6jt3u32vcyrgwzqmw8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1161040511004"
          }
        ]
      },
      {
        "recipient": "gonka174srhxhfktxx4hv94zcdz4jqfw9kvc4ge2p0pu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1160447819571"
          }
        ]
      },
      {
        "recipient": "gonka1a46zzvkdg5kf7raesh7rp2e3alx7gzgq3ww4ac",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1152015798500"
          }
        ]
      },
      {
        "recipient": "gonka1qmlkwzrpv5zkzzpgkthftd29uqg0ka8dddc290",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1151698611178"
          }
        ]
      },
      {
        "recipient": "gonka12tfc6ccmadjqv6yaa3axxsuhy6zv6tupu78p8u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1134910852048"
          }
        ]
      },
      {
        "recipient": "gonka1e4elawx3wgp407u3vqr8kj7ctef0qzme6wvntr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1129567802700"
          }
        ]
      },
      {
        "recipient": "gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1124226587642"
          }
        ]
      },
      {
        "recipient": "gonka1erjgpt52lp7atyq5c5u5tpprtqjr4pt6zd2pny",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1122166176790"
          }
        ]
      },
      {
        "recipient": "gonka12qz87r7g5sde33c6jnjp7n5kxj4t650v9ezxu7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1095484122804"
          }
        ]
      },
      {
        "recipient": "gonka1k4ufjpu9h79zy4hdtly8dcgyfkjmeunqtk3k9e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1094749475242"
          }
        ]
      },
      {
        "recipient": "gonka1u60q4n3ymcglvhglylchpyvc04kvvurl967mgk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1092175889843"
          }
        ]
      },
      {
        "recipient": "gonka1zhjhpgcmzyc92mlhawja4esnwuwu5u8sjlm4c2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1090676645680"
          }
        ]
      },
      {
        "recipient": "gonka1338kw8rwv6qlujzrgfacce3ej6emekzjwudrge",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1085517708212"
          }
        ]
      },
      {
        "recipient": "gonka1ypy2ygsa7se9lrcwxlstgwsy0lfged0kg8ft95",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1085335893801"
          }
        ]
      },
      {
        "recipient": "gonka18py93vhrf7mn3yjkqjdpkwlqfpavu3f06ssllv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1084494242094"
          }
        ]
      },
      {
        "recipient": "gonka12pwvrkm7vqkme62y0u6pgms79w8eqyt57s2vcx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1081514356117"
          }
        ]
      },
      {
        "recipient": "gonka18qd8fhk9uj0zk5xlgnsfkpj78ed65sptf0jkwr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1077905106645"
          }
        ]
      },
      {
        "recipient": "gonka1x5zn0e5n9c8qjjjt38g0wd05px89q5pxaxqpq7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1075980413077"
          }
        ]
      },
      {
        "recipient": "gonka1rw9fhpnf6pnlwzpfq836w89qmu6v7kfxs9xmvn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1075006911309"
          }
        ]
      },
      {
        "recipient": "gonka1ajvs7j8wlgjy8d3kjad520am6jm3a4alj7k4jq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1070942320028"
          }
        ]
      },
      {
        "recipient": "gonka1l45efpupwqw9uky3gjwy35mwae9jwgffuqpm7s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1067617076850"
          }
        ]
      },
      {
        "recipient": "gonka1j6dthe47wll5rhf2nn6r7xw9zy2luah2ant9pf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1050721942469"
          }
        ]
      },
      {
        "recipient": "gonka129ks6ra4ddy8ppsfk0gr8yu24sqk3nanmm34cs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1036348256503"
          }
        ]
      },
      {
        "recipient": "gonka1xg25gmn8uzeyzqqrchx6mfz379mvg43zsvj0y3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1035165938494"
          }
        ]
      },
      {
        "recipient": "gonka10kjjhgzngn2yj9fgrcfu4wf5lj6xv05u7xhz53",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1032271654590"
          }
        ]
      },
      {
        "recipient": "gonka1qpvpnr3anscj0tsnm64fus27xhnx20lf4rvjeq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1011681975315"
          }
        ]
      },
      {
        "recipient": "gonka1trz6e3rczlp4ma749v8zk6xng9jmcnrvnwv4rh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1011128733862"
          }
        ]
      },
      {
        "recipient": "gonka16p9vx68hfr5vpy6s59rvrz85le5dq22uymukgv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1010920650828"
          }
        ]
      },
      {
        "recipient": "gonka1tfds6hy4tge3p3pkzcj38qjnsgpadjhjk5f3ga",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1006193213519"
          }
        ]
      },
      {
        "recipient": "gonka1eg6tyw49ujmk7mgwqzyhzzyzcupzhw7fhku0qz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1003350070071"
          }
        ]
      },
      {
        "recipient": "gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1003067493292"
          }
        ]
      },
      {
        "recipient": "gonka1qjdt3qykdrka2am7s5rtrze44f7y8vccegjc70",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "1002860190000"
          }
        ]
      },
      {
        "recipient": "gonka1ex0ck58q3elelsysl3r9qwjljs7yn2yd65kr6h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "984546173428"
          }
        ]
      },
      {
        "recipient": "gonka105qfr38n0rz0d2r8hererw9ws5qx7njcujezvu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "968810021710"
          }
        ]
      },
      {
        "recipient": "gonka1k3aj9lxjllcslaus7a2ha5d3pla4rre67ksnsc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "963915416268"
          }
        ]
      },
      {
        "recipient": "gonka1y07fqanen3dwgr5dku36gy8lfk3uxtj000t38p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "960156417708"
          }
        ]
      },
      {
        "recipient": "gonka19f8zl7a979j0z90r5k0pajhua2y6ajtykxe8dk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "936394415904"
          }
        ]
      },
      {
        "recipient": "gonka1y3r32jhy6s4ge2sl5ly5s90gc0r9d2n4wmzvu9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "920045323759"
          }
        ]
      },
      {
        "recipient": "gonka1rn5nud8367cnspgas0dmtq2plxkacjsttqtdy8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "916211818671"
          }
        ]
      },
      {
        "recipient": "gonka13jelpte0qx5f0up3pzmmgnnqj5877rwfs08n7q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "915755003150"
          }
        ]
      },
      {
        "recipient": "gonka1gz6d9j834xvhvyt7c67ux6egugns7dlc5dzqds",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "912883054093"
          }
        ]
      },
      {
        "recipient": "gonka1c6y9p4w87equy52va4us3qzycz9w28ua9693gl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "893219350563"
          }
        ]
      },
      {
        "recipient": "gonka10g4ak0ku3lezt0q3kk346updcyyz83369pqtgx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "883688223962"
          }
        ]
      },
      {
        "recipient": "gonka1nq396dmfz2rntud8urt7ddyc7ysyg6rlax5vyc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "880740116277"
          }
        ]
      },
      {
        "recipient": "gonka1c8pemd8czpgeg69cu95y58fstuquw93uwqml7f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "879178934834"
          }
        ]
      },
      {
        "recipient": "gonka100xav7dpl82gxrtg72yjhpz2zn6f24gv035ted",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "866376648961"
          }
        ]
      },
      {
        "recipient": "gonka14zg378dzun4p2zhyuaq59y2q0e340wzahgz97q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "861590303143"
          }
        ]
      },
      {
        "recipient": "gonka1wkgawwdzj623ss8eywayzdj6qcgr2llygactje",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "860922847224"
          }
        ]
      },
      {
        "recipient": "gonka1afe8squhg6aqwuts34wsyuu3rmn349hqqp6tqf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "838808955066"
          }
        ]
      },
      {
        "recipient": "gonka1jqwrpyqn34jx0ermlus46f87epayqxtakhyu5u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "838114379054"
          }
        ]
      },
      {
        "recipient": "gonka12gc47yq8m7rnsa3aucq8mlzm7men8jaac7qkkz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "834890948011"
          }
        ]
      },
      {
        "recipient": "gonka167m8t885t8j4wr8qmh652x9d2jvhtdk4f367fd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "827209263037"
          }
        ]
      },
      {
        "recipient": "gonka14nurupejmd8vgu806jx4qpf6jfs55mrlc6umem",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "824722902081"
          }
        ]
      },
      {
        "recipient": "gonka1y0y9fcfhlhuz76falhdekx8w56pk88jaxssydu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "823559566189"
          }
        ]
      },
      {
        "recipient": "gonka1k6p754pyhxud2399knyccgjpjvdafj2u9xlgyf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "811589446121"
          }
        ]
      },
      {
        "recipient": "gonka106prclvpt5lgl9p20ql8kr6ap8vt0un535slvu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "808642141902"
          }
        ]
      },
      {
        "recipient": "gonka1ehqrd2828q8zrkn4qafym30eky56krezucxxhz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "807768895044"
          }
        ]
      },
      {
        "recipient": "gonka1p209mlvngz8hu0p5ff7dsjzqhjpx4jzn6k652r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "805071964127"
          }
        ]
      },
      {
        "recipient": "gonka1662dun8ufuvjfa652th9farq6devh57p0v4r3y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "803355958966"
          }
        ]
      },
      {
        "recipient": "gonka16msrxqwfedlll09hdwv0zmma6wttxx0wqqlt0y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "781828824066"
          }
        ]
      },
      {
        "recipient": "gonka12fazh3etpdx947ldwen4wudnds7wu4kjp5vd76",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "775232433739"
          }
        ]
      },
      {
        "recipient": "gonka17cnuuvplky4ck8hwj8smh6he6tgq6su45r5v5y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "774143127202"
          }
        ]
      },
      {
        "recipient": "gonka12hzd9zlz3tgslky477d4wa0jlwacv4nj9vxlmj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "771984739406"
          }
        ]
      },
      {
        "recipient": "gonka1hxtg78hm0lneuygmgzanxmasn4x5rykwmmle7z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "768342112553"
          }
        ]
      },
      {
        "recipient": "gonka14sk8te3wu4zh9dal9yd9tm3pd2qerdru4aqm05",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "764375908138"
          }
        ]
      },
      {
        "recipient": "gonka13tfjp70mhjxhdl3kjweuln07zu6y9ed3gr9k6y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "763220498896"
          }
        ]
      },
      {
        "recipient": "gonka1p6wekfevflq2h4rx9jekc86qaqa4ussw8legsd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "756975902050"
          }
        ]
      },
      {
        "recipient": "gonka1x2lalvrn6cucvzwfcd5cwwhggfuxqckw8k0zrq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "755267022910"
          }
        ]
      },
      {
        "recipient": "gonka1369ax8kr4ma8zu708jr3x2r902lfs8tcguyxl8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "755258914621"
          }
        ]
      },
      {
        "recipient": "gonka1x7zh2277spp7jfqjhv0g5mnezg290xdr4kpfnk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "752017682985"
          }
        ]
      },
      {
        "recipient": "gonka1lhycnwdtc6txcpvdvz2wym3zpdhlrj6w2z4evj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "749894259281"
          }
        ]
      },
      {
        "recipient": "gonka1eaf9r3qqnweqx23z0ahh77legtv2gnk3wwdwl2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "739075526779"
          }
        ]
      },
      {
        "recipient": "gonka1v5ggga7lslfg2e57m9anxud40v2s4t9dw8yj68",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "726622286387"
          }
        ]
      },
      {
        "recipient": "gonka10e7qay76svkulq7wx3mez60jvdxj5pmjynmyrz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "716814751592"
          }
        ]
      },
      {
        "recipient": "gonka1hhw376qvn4wuu424r9ueflvkv7fzzat9wuuvjg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "714039075269"
          }
        ]
      },
      {
        "recipient": "gonka1j4gwddnpf9h6n6899znss7tprqzxpwpedk7ayf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "712231234908"
          }
        ]
      },
      {
        "recipient": "gonka10ux22dq9a5dn5t4v370vzkww874yc6pmudxjen",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "710726835542"
          }
        ]
      },
      {
        "recipient": "gonka1vmwqf4mkl4ucqnrgjmnsl694hktepaecuvvyz0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "698413545705"
          }
        ]
      },
      {
        "recipient": "gonka1mdy7nlecw4xaqdxmeh3qlqzakg9ftge9szfqgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "696337292930"
          }
        ]
      },
      {
        "recipient": "gonka1ktl3kkn9l68c9amanu8u4868mcjmtsr5tgzmjk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "694260787860"
          }
        ]
      },
      {
        "recipient": "gonka1lmh6fy92ac2wldnpugg3t3xhp8lnqzgq0j0efg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "693656303863"
          }
        ]
      },
      {
        "recipient": "gonka1ccgvme9cpkwqes65jqgcmy09dtze9cp933cm0p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "693235305004"
          }
        ]
      },
      {
        "recipient": "gonka1g9n5yek0sk84qpx0lwc7hq6p3v2fqr5ggml3gg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "684113588212"
          }
        ]
      },
      {
        "recipient": "gonka1y4kyhqy022gt4kklxxflgqkutnx96ssww66zg6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "668334873066"
          }
        ]
      },
      {
        "recipient": "gonka1vz2jg42w39l63dmvmjqdsnxx0ywnzt9nzypdy7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "667372982192"
          }
        ]
      },
      {
        "recipient": "gonka19yqs6l5s2wl908fswm58zptxvkvg82dtynwuku",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "660800031574"
          }
        ]
      },
      {
        "recipient": "gonka1g884r7q58wptvlcpuk09gvw9j5uhwadr4qjexs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "657348636670"
          }
        ]
      },
      {
        "recipient": "gonka1w3ewq7swwdxx8fsht8tl250f7qv44edhlltrh8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "642705050439"
          }
        ]
      },
      {
        "recipient": "gonka1h2c3mkxq4xej7dmsp5hcva8msn78v07xuqhl90",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "641937320557"
          }
        ]
      },
      {
        "recipient": "gonka14cqs3cnsahrr52end3twr7sq3rhtwnj8j8pyzv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "641595530709"
          }
        ]
      },
      {
        "recipient": "gonka1l289k89zulv5ml63ursf975cvmr0j85k8ls46t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "636049841835"
          }
        ]
      },
      {
        "recipient": "gonka10cyq8zuplcwr5ntesxn52wp5ky3a7c3nrqdce8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "634870695105"
          }
        ]
      },
      {
        "recipient": "gonka1j62evzhlg556krdfhynpduchyl0px8qga8wfut",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "633074416696"
          }
        ]
      },
      {
        "recipient": "gonka14fn68sulr6v6l78kvur9u6yw5lwurtqcrqkh93",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "618164993040"
          }
        ]
      },
      {
        "recipient": "gonka1h796gh5vnp0l3k0klvzk9rw9240223njss8g5y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "617132119663"
          }
        ]
      },
      {
        "recipient": "gonka1zsnpv9htjtq35ux04hal5l8dnlgah22zl6rk3h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "616305081132"
          }
        ]
      },
      {
        "recipient": "gonka1lqv96tny8a0344e6jfgxk500q5ct7zy9ekz49m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "613560930734"
          }
        ]
      },
      {
        "recipient": "gonka1aev99sylsnfzyu2dwlnw6f9lugjkvav7kxqp0k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "605263625720"
          }
        ]
      },
      {
        "recipient": "gonka140f97y9dsnjc2cdusp0hzx73tk693ycg6mkqy5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "598119300722"
          }
        ]
      },
      {
        "recipient": "gonka1hhx6pvs6n4ehgv4wzz7h9f68t8hm96t9fq0ydd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "594067847856"
          }
        ]
      },
      {
        "recipient": "gonka1fp8zl07qccdzuekns2q55jgmcag40kjrm8z0z9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "588451915703"
          }
        ]
      },
      {
        "recipient": "gonka1frfr2z4lclq0wjqsrstnhm48rmvkmd0tfsssvk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "586439098001"
          }
        ]
      },
      {
        "recipient": "gonka1chktrhryd3zpxcwtw595wg9mxgj0wwwmzsule5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "583192531647"
          }
        ]
      },
      {
        "recipient": "gonka163ug8zucqeag9v5ey4au34jqt7vejkmxsg74eu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "578583751996"
          }
        ]
      },
      {
        "recipient": "gonka147rfj8kg892wfqvqrsl39d3h26k002cv54qxv7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "576363693008"
          }
        ]
      },
      {
        "recipient": "gonka1ndlfjnp5d7eruyrhjvn6uape3jp630qld7l9yl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "570320457368"
          }
        ]
      },
      {
        "recipient": "gonka1fxdt48vp78uxa7apuuamv4clwafxagnjg9eulc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "566039434935"
          }
        ]
      },
      {
        "recipient": "gonka1elw9xd79mpsrt7jqwkweg6yv02nvda49xhcej2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "564618912568"
          }
        ]
      },
      {
        "recipient": "gonka12hw8xf5rgy7fn0wt3qaxyk9gav6eu2rns25t2v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "563676112102"
          }
        ]
      },
      {
        "recipient": "gonka1clevcl55wh3g8fx82y9nuhcnxc8kalwf53a4gj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "560601174860"
          }
        ]
      },
      {
        "recipient": "gonka15sptlamre9vq4m5t7pa7je5r2pc34kmlwvj0jz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "558487767957"
          }
        ]
      },
      {
        "recipient": "gonka159kqhlp3psj4r7r9646lhjpfz5apwmyen6y7m2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "552690033928"
          }
        ]
      },
      {
        "recipient": "gonka14law208gj4hgpr04y2udwlkkxh3k9mv07evgh4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "548618679904"
          }
        ]
      },
      {
        "recipient": "gonka1p22v6ncqsys9fh85gdmkakpe24x2zqfyp60z5q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "547116218730"
          }
        ]
      },
      {
        "recipient": "gonka1ujfwdfe0tq667vt5sz2pus524zpjveedp4tkj2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "545997408120"
          }
        ]
      },
      {
        "recipient": "gonka1p60lruhxmwcsa9taa28cp4k4f6kv2kvyu5h5ep",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "545755552498"
          }
        ]
      },
      {
        "recipient": "gonka10t67f5zxh7canhuznxg7cperec6286jjqh5pey",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "544379556981"
          }
        ]
      },
      {
        "recipient": "gonka10t34t7tvvgrzd8npm30u8dx4uw2v9axcercgak",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "543506694568"
          }
        ]
      },
      {
        "recipient": "gonka1sskwvat6wk6sdjjg87ne2nhexdyznxntu07vzh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "542959627601"
          }
        ]
      },
      {
        "recipient": "gonka1d2mfxjhvx0zm3jd05arl0d36qn2k03mc5y7zt4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "538035929178"
          }
        ]
      },
      {
        "recipient": "gonka1vn6hk34wme5xvqzjmm26u9snkxg7nqd490gmwq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "535027430493"
          }
        ]
      },
      {
        "recipient": "gonka15vunu0new53m83ccvfcmkf84v7q4s8ldsjfu4y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "530331698652"
          }
        ]
      },
      {
        "recipient": "gonka1c40y2drwhu7px0gue02696y8ypwq2y30fxnfp5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "523388377860"
          }
        ]
      },
      {
        "recipient": "gonka1yquunstmnn35tuc6wsrlv020ul2rnuyldqkt37",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "523050197093"
          }
        ]
      },
      {
        "recipient": "gonka1gsarmv9gsc7g9fv9nsqtk6t0d7erxpurf5mvvl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "521369292752"
          }
        ]
      },
      {
        "recipient": "gonka1fryp5vn5xppkwykzjul6e2crkgxgwhl2cunrmx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "514067267997"
          }
        ]
      },
      {
        "recipient": "gonka1mkdgh784u7la8fpexnge9wqhdw65al67f9e2k3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "496529632342"
          }
        ]
      },
      {
        "recipient": "gonka1043d00lu0v3fz53cut34twtcanalqg9u8vehp2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "490582260899"
          }
        ]
      },
      {
        "recipient": "gonka1w568mv4h5c7sln767rxc8hzf6s9nhxvs7raz08",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "489475546267"
          }
        ]
      },
      {
        "recipient": "gonka1awufch9x3slh9h9t3exa36r23rwjknswldce09",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "489140116165"
          }
        ]
      },
      {
        "recipient": "gonka1wt8sr9jxzpec65j7zkxsgh6edk3m6r8nlf5za4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "488209774154"
          }
        ]
      },
      {
        "recipient": "gonka18ejynmrg67epw5psqhv9stm9yrskerhvqvm5qs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "486890528819"
          }
        ]
      },
      {
        "recipient": "gonka1desd6924c4aturcdmwk59jpye5em3q2ze8gvjn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "486556076647"
          }
        ]
      },
      {
        "recipient": "gonka1crldgzq22fly44ek58rq900ef48usac8f3hpxd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "483028542609"
          }
        ]
      },
      {
        "recipient": "gonka1yk34z38t92jzjgq2ga7tkfpj07sf4ss3tj6n2m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "480269006881"
          }
        ]
      },
      {
        "recipient": "gonka1vxs4azxcym36wts0t7z5nj65ma8pnkvpmywxa0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "479871438049"
          }
        ]
      },
      {
        "recipient": "gonka1g99cz2zdgalleuzhwa6h3yxf5k7khjwxg423ms",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "476757658504"
          }
        ]
      },
      {
        "recipient": "gonka17tlh09e32xpv2uj433ytjnwwd8fh24jclpzm5s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "476168080739"
          }
        ]
      },
      {
        "recipient": "gonka13r2vlppxhkmk0868yfu79hkaewrzv50luhnyev",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "475133166252"
          }
        ]
      },
      {
        "recipient": "gonka14ayvun7uw0d9u6nk7k6w3zdeewq0p9qzqycsmv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "472492213078"
          }
        ]
      },
      {
        "recipient": "gonka17amsnz2csvjwt3rdezys6gj7wggexxwtwt03a9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "471319390306"
          }
        ]
      },
      {
        "recipient": "gonka18x3y80uu9s53lewvt0eu6tgc9rrvaht7yqzmw4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "470090030109"
          }
        ]
      },
      {
        "recipient": "gonka1290wk5as5vg4f6l5r5sl2hjr2ty24lam3l6vlj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "469485703062"
          }
        ]
      },
      {
        "recipient": "gonka1sun7e0re84mjf79c6euqp9v4jeujgz2x25w4e9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "448558908153"
          }
        ]
      },
      {
        "recipient": "gonka1eqjpx0k806kcu8tjr64zlswk9vkznsstyeq0j8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "443820315340"
          }
        ]
      },
      {
        "recipient": "gonka1cy5x2c2zq4s9zq5r2xz609j63mprpc9tdz8drr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "443036488390"
          }
        ]
      },
      {
        "recipient": "gonka1l279mvj0rgkr5gkrtkdfeetmf602lkfvkf038j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "442746566649"
          }
        ]
      },
      {
        "recipient": "gonka1534swfr4vp6s9zc8prhw6uzzvp9teg5pnrrs06",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "440021550150"
          }
        ]
      },
      {
        "recipient": "gonka1975m3w08ywrc89aqcr9m8z6z70a38jf64vwte8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "438907596251"
          }
        ]
      },
      {
        "recipient": "gonka1lacrx7sdpwvy2fjxsldmz0w8ptk5qlegrh0qyc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "438552332390"
          }
        ]
      },
      {
        "recipient": "gonka1cv73drcy44vfspr9ryhdh4yxq3r4w4n7lt0a06",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "438282542671"
          }
        ]
      },
      {
        "recipient": "gonka1g69nf83247psxptvw9clwehma6f2g4q2c08073",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "434588074767"
          }
        ]
      },
      {
        "recipient": "gonka19f20kkuwra4z2ml74ephrallpguclua83l9zrt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "433808055245"
          }
        ]
      },
      {
        "recipient": "gonka1kdhuzlaahg0du24n5kyr29h3344gewmmmrs89z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "432325812729"
          }
        ]
      },
      {
        "recipient": "gonka18hsyhvgheg5agh86jkut9d7ggkx4swq2ms3f7s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "431488493451"
          }
        ]
      },
      {
        "recipient": "gonka1kx5y69fvgcag8n2lvwtjq2yqu4rkqauwc0nuy8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "431006304323"
          }
        ]
      },
      {
        "recipient": "gonka1he4syma87py2f65rfy3zsrtw5e4nhs69t3sgjt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "425831596283"
          }
        ]
      },
      {
        "recipient": "gonka17lw5msaae6hupgylapqcqmggcyyzhvdgy406s4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "425243818848"
          }
        ]
      },
      {
        "recipient": "gonka1a9yz979xxryjh9hdzuyxddscwtg9g92079hjra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "425076183432"
          }
        ]
      },
      {
        "recipient": "gonka19nsaq8gdavl04mx0v6lhvzzdkqhu6uf56l38w0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "424272905394"
          }
        ]
      },
      {
        "recipient": "gonka1063hmy29tgwh5zpup7m9qat7nvgrnyyyuudjaa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "423526894395"
          }
        ]
      },
      {
        "recipient": "gonka1cs744mzemn5h8p2e7c0zkc67sgdd5p8es3qe9v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "419663870856"
          }
        ]
      },
      {
        "recipient": "gonka1cu4et2vt7squt6jslmn7jc6sr3kr9dwx8807er",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "416726958772"
          }
        ]
      },
      {
        "recipient": "gonka1k8emnxc8ex8qa47h9l5y0dxprxen0hhqlnexwy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "415098212687"
          }
        ]
      },
      {
        "recipient": "gonka1hz02vsjwrjnfu65knc8xnwh4xawt02nzaltctt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "414514027990"
          }
        ]
      },
      {
        "recipient": "gonka1w2dtrs7thx2jfeu389ztwc38h0nd4pv2hl7xtp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "413803912716"
          }
        ]
      },
      {
        "recipient": "gonka1d7fl3tfcjj52uavnfsalmydtdn3uvqvs2wph58",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "413793735098"
          }
        ]
      },
      {
        "recipient": "gonka15vwfhvvya0xhf8cfxxgsqwkjmv8ay2hhzdd0yl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "411140962032"
          }
        ]
      },
      {
        "recipient": "gonka1nxp4edhgytlmczmmwvzgu6humsuwpf8t8yvd40",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "404230785405"
          }
        ]
      },
      {
        "recipient": "gonka1gku2agvxyl9yvq6j0ulu8thm8n2mmg32dxvm8k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "400668604165"
          }
        ]
      },
      {
        "recipient": "gonka18xpmr5v362gwvxlq78twhg7ht07wu4kzdqu4y2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "399555085227"
          }
        ]
      },
      {
        "recipient": "gonka1k9wr42jrdudvxsrdrgnxqaxcchrwy2ss84ha7t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "397336261711"
          }
        ]
      },
      {
        "recipient": "gonka1wnhd4uqvf3k38av7m9s3ssdzu0kvqskmes69gu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "389942484029"
          }
        ]
      },
      {
        "recipient": "gonka19z0dg9zpfkdfye0ddrnkcynrwvqslw4a2alzf0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "388059563885"
          }
        ]
      },
      {
        "recipient": "gonka1fhcxxfnk0ap7u5hjyvgvd0500lpq8qre59hwza",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "387606471004"
          }
        ]
      },
      {
        "recipient": "gonka1uwknfekug2ykhygjpfy5n7uc8l6naxz267dgsw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "381373301630"
          }
        ]
      },
      {
        "recipient": "gonka107et3r7gxsrkce7wq42jjf5k98r5xvsfy6xsn5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "380030638392"
          }
        ]
      },
      {
        "recipient": "gonka16dqp2jfmnaahwxq5x7snn2h2ap026v5lwhr5m7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "378999867692"
          }
        ]
      },
      {
        "recipient": "gonka1c7wr8u3j78dfd2jmymzq3c3a2gzx75g2s682dl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "378149101711"
          }
        ]
      },
      {
        "recipient": "gonka15e0y6kxleal3l4vr9vucwv72vu8cfndjtljl6y",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "375476917342"
          }
        ]
      },
      {
        "recipient": "gonka1lmcyrg9fh0lj7spq2ra4kduttf86ede5xlrmay",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "372770462475"
          }
        ]
      },
      {
        "recipient": "gonka1w29nvdy6caqtrw30whz9h6ghl0xszwh3egndah",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "372546833803"
          }
        ]
      },
      {
        "recipient": "gonka1n8sczgy8379gqx0z4xuwrv7g50tcml6r9whkxa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "370848240747"
          }
        ]
      },
      {
        "recipient": "gonka165eh4p7rkucdv3p0pd92l67rm8fw8apq0p2c9e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "365333781875"
          }
        ]
      },
      {
        "recipient": "gonka1f7uwyhetekfar5h5q7vtatne28futuffypde4j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "364832113795"
          }
        ]
      },
      {
        "recipient": "gonka16a89kpc76p0m26zv4rck5sm9kc7yl5d59ztjpr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "361064732604"
          }
        ]
      },
      {
        "recipient": "gonka10p49jx70haq9uhjy94y80zkfv3xk5pafk5wc5q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "353283309527"
          }
        ]
      },
      {
        "recipient": "gonka1lmgutdlel0fny79zvlsh9aw3c0dw75gtscka3g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "353061160395"
          }
        ]
      },
      {
        "recipient": "gonka1gsnlch7sav73dxearvt7ylh3qcq3fdurad72za",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "351121509816"
          }
        ]
      },
      {
        "recipient": "gonka17njwpngllwv7hlgsdx2h7n0yxjjsqgth2lsy72",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "351084936780"
          }
        ]
      },
      {
        "recipient": "gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "348627504128"
          }
        ]
      },
      {
        "recipient": "gonka1hzqehs8eq609tmmwhhj239acd4t04ev97277q3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "345108557136"
          }
        ]
      },
      {
        "recipient": "gonka1yt2s5u5k06rm2au8dsqm4kzwmw7klqsrd6xd95",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "344628037407"
          }
        ]
      },
      {
        "recipient": "gonka1qlt90c4hxccgnuc478jaa3xl5klga84xzrvpda",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "344336495222"
          }
        ]
      },
      {
        "recipient": "gonka1nhsw6z4z4vevzzyrdkq2fxfgn8dypuudjvangc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "340275511499"
          }
        ]
      },
      {
        "recipient": "gonka13w7j5pmzg0an9gutm40eflfkl74zsja9jqqvcs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "335905698946"
          }
        ]
      },
      {
        "recipient": "gonka125xgn4z89quhrjhv6qfgn83wqwlaykxs8upjrt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "331972513490"
          }
        ]
      },
      {
        "recipient": "gonka1q96dv6st48490vtzx2pwuwkjg439dr4hg6dzjn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "330848630051"
          }
        ]
      },
      {
        "recipient": "gonka1qkwzxe3hwrghhmgek5kvnyhyaw9akkc8mfwsaa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "327938028015"
          }
        ]
      },
      {
        "recipient": "gonka1pa6xam0gh4hccrsunf9nmervcqt3pe5z9l3xrl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "322218386967"
          }
        ]
      },
      {
        "recipient": "gonka18c9r7maxex83kfdm8zpvquleqam8aqm2klkag5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "321451865905"
          }
        ]
      },
      {
        "recipient": "gonka19yvj22q22w5nr8uxtlj6e5wu30cqn3sexmcdcs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "320461635235"
          }
        ]
      },
      {
        "recipient": "gonka1kyft3snetrh9fnetvwrzt4fr5dwm5szl9sx9hq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "319963060625"
          }
        ]
      },
      {
        "recipient": "gonka1xfg6ed596n8ka7tjp7j604prf5n4mgv3h9d02t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "319780202816"
          }
        ]
      },
      {
        "recipient": "gonka17ypfh585hv7g2vyrmdqqpy2czssa7h0pmndyul",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "316536534268"
          }
        ]
      },
      {
        "recipient": "gonka1au9qsemsqtng83kf3nfac38gqe0c0f9qslw750",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "305617072534"
          }
        ]
      },
      {
        "recipient": "gonka107yrh33u84sund37fkkpslen5untjl7vw3pd9e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "304553256378"
          }
        ]
      },
      {
        "recipient": "gonka19teuc4q23h48m2ser9aqll9nactthfkcs9meke",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "303905885385"
          }
        ]
      },
      {
        "recipient": "gonka1fy86zl25jft206rx0j63km5ru2cn3e7t80zzu8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "300459975051"
          }
        ]
      },
      {
        "recipient": "gonka1gdrrsudtxaldp2jrtn2v6qzpd8zr2u544pz3u5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "295893581436"
          }
        ]
      },
      {
        "recipient": "gonka1ceuk4gvskjw9deuvequ0hd6ty2u7h4jsg5a8uj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "295213275244"
          }
        ]
      },
      {
        "recipient": "gonka1g58w4wu7yyla55vfmhm96v9jheyetnxr02jzz7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "295111850857"
          }
        ]
      },
      {
        "recipient": "gonka10ay2yczzqfpels9ez3m6q7mwuje2tqkwjym8wc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "293127877431"
          }
        ]
      },
      {
        "recipient": "gonka1dg7tym5xfd6rt0mnujqcgsdjtdarhtz6pnrvse",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "291849556888"
          }
        ]
      },
      {
        "recipient": "gonka10qf25fwar63g6zkvn2nm6pj65va2yz2esl3yd4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "285924438943"
          }
        ]
      },
      {
        "recipient": "gonka1uv8lw89ththtj05c54wehfnqls9u2pza53q33z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "285901741010"
          }
        ]
      },
      {
        "recipient": "gonka1jpxayv4ef6c5z4wn9mxqsla0zkcwu5tq2536sw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "285899745563"
          }
        ]
      },
      {
        "recipient": "gonka1pj07u20jn9cx48r0jwen6evz7mrfj75t3argv4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "285330045368"
          }
        ]
      },
      {
        "recipient": "gonka12fz88uq255gr4l34fedtd240qu9ajhppettvx2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "282968038250"
          }
        ]
      },
      {
        "recipient": "gonka19xy6zmvpu9x4cyhnuryd3c8c4q8t9v5guj3hzl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "279949746921"
          }
        ]
      },
      {
        "recipient": "gonka13r0fwd8flq4psphqkda8u5f5pxu79wcx3s3zmu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "278793671891"
          }
        ]
      },
      {
        "recipient": "gonka1tan3ssg0sz6kzseze5ezvnynhtyf2rfn6pczjv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "278205980463"
          }
        ]
      },
      {
        "recipient": "gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "277853300380"
          }
        ]
      },
      {
        "recipient": "gonka15zc68q2924r90hdwmcdgw0pfwvlsnltn6nht9a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "277420674432"
          }
        ]
      },
      {
        "recipient": "gonka1crlh7547ndxs8kl0urejhlttns7fy4ft344zy5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "276941913821"
          }
        ]
      },
      {
        "recipient": "gonka19kd8xatmw86wyz6v5qmc9kqwfnk62cydql7da5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "270590570224"
          }
        ]
      },
      {
        "recipient": "gonka1lajfpxh74xse4xxease0trz5gwecze99875tjf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "268236872042"
          }
        ]
      },
      {
        "recipient": "gonka1xx297g3m4um7g6eayn03cwdmu8feal93sqv4wh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "268107287831"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1m2wtkjw80ukazgyngp8eykjukr9jx5rumdsmyr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "267346122911"
          }
        ]
      },
      {
        "recipient": "gonka1wcdrfhud0ey55mq7r83r9jm9n99qauzpm2egp6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "266334120077"
          }
        ]
      },
      {
        "recipient": "gonka1gfltwk9nphmfgn9d77c97p3xzqt4yr0a20md6m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "266302403647"
          }
        ]
      },
      {
        "recipient": "gonka1qvpct2fqwpfqhznwjqs498ggp7wyxjkd4mvxhz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "266127303219"
          }
        ]
      },
      {
        "recipient": "gonka1l46sylzza3jymv5mhf7aa7v2ncgq5zadd4ye4k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "264732746305"
          }
        ]
      },
      {
        "recipient": "gonka1eheatjgzlu9pulsh7ggsx9gan4sy20ay5ytmvn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "264208241317"
          }
        ]
      },
      {
        "recipient": "gonka1vlk3ck2mkdeehrvr523aq5fz4dmqazyeppy08r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "264161735479"
          }
        ]
      },
      {
        "recipient": "gonka1ewlwawmd4z42daay08hspv45nmzlvffw0ums94",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "263088357407"
          }
        ]
      },
      {
        "recipient": "gonka1uvfshcyxnasdt5grn9we9qzl90ryujfkpcarjf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "262854578382"
          }
        ]
      },
      {
        "recipient": "gonka18ee58ff309k3fv2dn9f8zfa9q94huk4ue9y7t4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "261363469059"
          }
        ]
      },
      {
        "recipient": "gonka1lnvyznywq8u2kda780e6h82t6r9nmsuj4j4dp5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "261153730494"
          }
        ]
      },
      {
        "recipient": "gonka13a4v8gxxjav5t4xq5y9cv9d8rfnvkjfw5adqz3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "259477811528"
          }
        ]
      },
      {
        "recipient": "gonka1pf4z32nqz5ax7zsxsmf4tan8wsnp957y9t4qtt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "258408978669"
          }
        ]
      },
      {
        "recipient": "gonka1myfzqktyp8lrdwpymqw5cfyjsr0msa6a3y9c2n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "256716919639"
          }
        ]
      },
      {
        "recipient": "gonka12p7vdr8am7w6yakudrk7l2nqcnka8xqrruejty",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "256536328020"
          }
        ]
      },
      {
        "recipient": "gonka1uk73fw4tnfv9rfdeekxycvt0v8cncr64syejra",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "256395083588"
          }
        ]
      },
      {
        "recipient": "gonka14m522cfm77emja0fnd0y0p9ls74q8kfpxvemsq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "254971732952"
          }
        ]
      },
      {
        "recipient": "gonka10y0j44g5zae0kep8xmgv8upl7p6dcurnl72m5n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "250313363132"
          }
        ]
      },
      {
        "recipient": "gonka1p57jas3hm3gmdvh64z92ycr28z968j0fn6n6jd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "249620064759"
          }
        ]
      },
      {
        "recipient": "gonka1l2pah3qf2jgdw50lzm6hpt352fsccthmrz57ms",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "249348523620"
          }
        ]
      },
      {
        "recipient": "gonka1pts20pjtryksdxp9lvydk9vvs8mmd9ruzqgu4z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "248032627366"
          }
        ]
      },
      {
        "recipient": "gonka1a333gjgcsen6wkg0m5j7vnyw3paz8e598pfsev",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "247131413356"
          }
        ]
      },
      {
        "recipient": "gonka1fpkw6p595r2npvtx6l02tmtggwlkz0s7ns7xev",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "246941799835"
          }
        ]
      },
      {
        "recipient": "gonka1p2fj0vx4kpx3tdm7u853v9q67n9frrcmttxrqy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "246560012735"
          }
        ]
      },
      {
        "recipient": "gonka14xc7cn3n2zvnw3a5zh3p0827hw9hruqfze62e8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "246508658850"
          }
        ]
      },
      {
        "recipient": "gonka1ldzl4gaalctyfwupak25avzvu0s29zjvayne49",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "243351881717"
          }
        ]
      },
      {
        "recipient": "gonka1m2s8r88lj40thm3zkd0fc92sqk6wswhx8a2xyh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "240542872784"
          }
        ]
      },
      {
        "recipient": "gonka1p92n7yphf8eqcygcwkpvgggt7d9ql69mchllcr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "240217006117"
          }
        ]
      },
      {
        "recipient": "gonka1jpg0ct9h272lefy99w4sgd2ul9ukvzwhfanvn0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "240216332176"
          }
        ]
      },
      {
        "recipient": "gonka1adz6e58nz8k79fsg3hxq2sg6thym2l073hyyh9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "239700513689"
          }
        ]
      },
      {
        "recipient": "gonka16tru27h865g77cfhsyfpepcjlqlgavl4dc0a0t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "239693182441"
          }
        ]
      },
      {
        "recipient": "gonka1lnynt0wfxhn049m7mjg7kpxcklspwz6ngw0rsv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "239434096502"
          }
        ]
      },
      {
        "recipient": "gonka1kyrhxw6frcjk4hh8rdeswxftwxuxwgphxnk8kk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "238833085068"
          }
        ]
      },
      {
        "recipient": "gonka1mhhq8ky8czhny7wk3sk9uquwn43twd4emksh3e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "237989906345"
          }
        ]
      },
      {
        "recipient": "gonka13nftxrmqx9hum0ajmweyqqpclkgge6wgp33ms3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "236763437310"
          }
        ]
      },
      {
        "recipient": "gonka1q6v5taltnxxzjrgpheu5t7pfjwmsu6x8gs24sw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "235788952207"
          }
        ]
      },
      {
        "recipient": "gonka13z9nw50phzh9sesempfam6prrgzz9c43n7hl0f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "234860999377"
          }
        ]
      },
      {
        "recipient": "gonka1rvuym8r7kmage5jw8jnzxyephcvelkaerzqumx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "234562856172"
          }
        ]
      },
      {
        "recipient": "gonka10k27r58herdqs3m4c6vyjlc2jsxnpjy2x73zgc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "234423646081"
          }
        ]
      },
      {
        "recipient": "gonka1sptzpk2tlxv958s22nu0juamt09hkcrhrrhx5l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "233442651437"
          }
        ]
      },
      {
        "recipient": "gonka13l0e92dedmwm0a2zcxnctvqlcl2tw7hhkdmsnx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "232321910249"
          }
        ]
      },
      {
        "recipient": "gonka138xt5y8kyzg6lcjva8vqyz9av9shhyz6e6nv39",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "231917217521"
          }
        ]
      },
      {
        "recipient": "gonka1663gc0f8f6fdylzk9m9akxjjfvj8f9n94nhvnu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "231917217521"
          }
        ]
      },
      {
        "recipient": "gonka1ad56r73l5z92x9f3qe7e52q0jckmg9ytmghp87",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "227878307385"
          }
        ]
      },
      {
        "recipient": "gonka1tl5m3vuqsx333v7095ymwjdc4vdk2wd9r5hqws",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "224016160981"
          }
        ]
      },
      {
        "recipient": "gonka1as0kls7e88q6ull9t2gyhe5zk9utzaezwml9kt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "223384429920"
          }
        ]
      },
      {
        "recipient": "gonka1pu7h5ntzt94ptwr5y5nctfjvpfd0hclqspcryl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "223117695596"
          }
        ]
      },
      {
        "recipient": "gonka1p7ze99aywsyudnn38wrxjsgzhmcu64swe9zmua",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "220252368742"
          }
        ]
      },
      {
        "recipient": "gonka1j3m7rwdjrf44xy8p7ff4w3srqxaml0f73x09ud",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "218704613298"
          }
        ]
      },
      {
        "recipient": "gonka1mqf4hr9a68zf78gcjkxmkz6nkzp76d0nqea9sv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "218463578010"
          }
        ]
      },
      {
        "recipient": "gonka192gv4k5kh88g5s9xll8k7w065lz0rjwh7zj55v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "217527398702"
          }
        ]
      },
      {
        "recipient": "gonka1gd79gdm2s35rc4mhssgwrqh2lnmaff0wq4mwq6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "214679298921"
          }
        ]
      },
      {
        "recipient": "gonka1tl6wzyuvf8t32ny8deqdz4kufle6fq0k72cy8j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "212901999312"
          }
        ]
      },
      {
        "recipient": "gonka166wgzjsx5hm4cxc58uc42watkgcppgv80yts48",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "212573545475"
          }
        ]
      },
      {
        "recipient": "gonka14jxtac6gra9cc97q7gw6el2l7f2v2d32f8973x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "212467763300"
          }
        ]
      },
      {
        "recipient": "gonka17fcahf38xh8ghzyyrc55tarz9nd0vw6xd29nsk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "212248188434"
          }
        ]
      },
      {
        "recipient": "gonka14p0njxtlnx2c8zn570nvvaf730gnnkwvetlwj8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "211609774624"
          }
        ]
      },
      {
        "recipient": "gonka1zv89w02sdfzwy74s9vcthk38dnfsw36s4h7s93",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "210396399071"
          }
        ]
      },
      {
        "recipient": "gonka1a6jjdd2ufn7x5qpp56627pk40sneqwyl989444",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "209535834916"
          }
        ]
      },
      {
        "recipient": "gonka14flzeq3mc2qh4h8senj5glhrtsknln6ugkhm3x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "209188155802"
          }
        ]
      },
      {
        "recipient": "gonka1lrn7dux37jx6f9nqnh8mfrx2d0p4npw8xnjpxn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "208871586849"
          }
        ]
      },
      {
        "recipient": "gonka1399mlkshf3drn67zqm7vsc6na9a96t55jrhjeu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "208341539624"
          }
        ]
      },
      {
        "recipient": "gonka1rqfj7selleh544mstj7quwmqned0wm2trpe9wu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "206171996533"
          }
        ]
      },
      {
        "recipient": "gonka1su7xfxq7a6dalv38gujj5tz5urkmw0044vush0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "204906813326"
          }
        ]
      },
      {
        "recipient": "gonka1mecj5za64q5cnuu3vaey88g7kn996h2lv8aylu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "204341940016"
          }
        ]
      },
      {
        "recipient": "gonka1umjryvc7nyl6w44u8mrrqwffv3mnk0xftx74er",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "204112867833"
          }
        ]
      },
      {
        "recipient": "gonka1qyw37eedekdrhu9937k2ewvh5ql99qlmsv3nj4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "203997831326"
          }
        ]
      },
      {
        "recipient": "gonka1lzp3eyygk2zttc52r6jnfugdr76eq3mnqyl8hp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "202116870034"
          }
        ]
      },
      {
        "recipient": "gonka1pnfyj6kw3h3v2qu60j42j8h3cuf3jpqqgnaet7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "201720882778"
          }
        ]
      },
      {
        "recipient": "gonka1ukxf7quyy8qsz3gy2crtlzh5qfptd2awzs3a4k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "198376817068"
          }
        ]
      },
      {
        "recipient": "gonka13dyaa9jucv4r06a5nf2nsz27mwdr0ttfpzxx3f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "194440591844"
          }
        ]
      },
      {
        "recipient": "gonka1my88wstqm2e795srgpxzat60z5hy0p7a85ytpk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "192759389776"
          }
        ]
      },
      {
        "recipient": "gonka15e2swr409v3c4ydpq9ahsn3zuqxyj47axn3lf0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "192684097628"
          }
        ]
      },
      {
        "recipient": "gonka1pucvx8mx0nux5gcd2wgfyg9mwkaaqaqplw674l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "188014787856"
          }
        ]
      },
      {
        "recipient": "gonka1gt0406jz45mjt0jujqtfd3m9lcyah93t0wj084",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "184115258724"
          }
        ]
      },
      {
        "recipient": "gonka1k53k8vfzg4vg88vp9anh84ykzwdw4nzqppll97",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "181381921472"
          }
        ]
      },
      {
        "recipient": "gonka14vp3katk6685avqjxhwrn6cckrpgjrf5vjz8jm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "176880182563"
          }
        ]
      },
      {
        "recipient": "gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "175555534697"
          }
        ]
      },
      {
        "recipient": "gonka1cpm8uguw5f3vyl3gz7537e3mln47uyzyld57g3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "175238478624"
          }
        ]
      },
      {
        "recipient": "gonka15mh2v944wxk3phxfkegglpgfpq9mjcm6vmpyng",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "172060368100"
          }
        ]
      },
      {
        "recipient": "gonka10thh6z0wvq9c05j4z3f9qtpxxedruqn5ae350k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "171896958330"
          }
        ]
      },
      {
        "recipient": "gonka1ch7hgwuc2ld0fvp305fkqn2ff38qek8cyls4ww",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "171757160407"
          }
        ]
      },
      {
        "recipient": "gonka139l5ttdauzdt8hfd43yfrwv97df547spjslnpe",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "171401905152"
          }
        ]
      },
      {
        "recipient": "gonka13nuzs6xh6rygx7w3vhtfgadt4vvn0lgfmyd4pt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "171010486577"
          }
        ]
      },
      {
        "recipient": "gonka1xjdmt0s2dy5juxh0uhct3lye94xdmf4ku528sh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "170817573835"
          }
        ]
      },
      {
        "recipient": "gonka145qtr0h90fvz88klshvl4r4htw4thdgcvpey3g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "170468417948"
          }
        ]
      },
      {
        "recipient": "gonka12s6rzcvuq4mc3rl6dm9n3j609vm3pp39vwhuk6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "168900273074"
          }
        ]
      },
      {
        "recipient": "gonka15ekp90x056vsuw37za6vt9p54r6kr7pr76hyyd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "168502394988"
          }
        ]
      },
      {
        "recipient": "gonka1nykx6u9qklnq7nkqm0px2nwthu4hzfkhejcrze",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "166874432859"
          }
        ]
      },
      {
        "recipient": "gonka1zaup3ecnckjvmyqfnfdjj6jn3hsazqt3zjsexv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "166331047284"
          }
        ]
      },
      {
        "recipient": "gonka1cckj93kp9kegry64scpn4ew9965g3qrswyshl9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "165813241052"
          }
        ]
      },
      {
        "recipient": "gonka1dtnru3j85vee0vm20vkvd256nfd9t7jzuvnd27",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "165570544195"
          }
        ]
      },
      {
        "recipient": "gonka18n9rq8q9gq0guvrm2mzk7hd2hvtf6cf6k6ul44",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "164645713730"
          }
        ]
      },
      {
        "recipient": "gonka1uwf8ce2knja6az8x6l2fawxh0yx0pz68n7pk7c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "161957022779"
          }
        ]
      },
      {
        "recipient": "gonka1aumu6ctfvp6hdccmcvrhrz8ete926zleyhacr5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "161849926896"
          }
        ]
      },
      {
        "recipient": "gonka1hhtht6rssq5hy22r7kyrrtkglvslxtkqt5yau8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "160968782293"
          }
        ]
      },
      {
        "recipient": "gonka1fh58x94xd6rdqz599svj9ftdt9rckg6ggxvn3p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "159981237348"
          }
        ]
      },
      {
        "recipient": "gonka18jmc50as0esg8sf4ylkxhxftvwe2xm4fvw87s7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "158802073834"
          }
        ]
      },
      {
        "recipient": "gonka1kysyccuws3hl7ul2e9kfftanevvsskf5jtjfr2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "158644782785"
          }
        ]
      },
      {
        "recipient": "gonka1n57qkc9umnqu4whuy7rse9gx09f9m470wq9f2u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "158346504252"
          }
        ]
      },
      {
        "recipient": "gonka19kue8dlczfr0vl94tta3l9k5s08hwuu0zd5ewv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157578607135"
          }
        ]
      },
      {
        "recipient": "gonka1730jjs2rhajxp434m6syr4uwemqfw3d9dkdvje",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "157245995276"
          }
        ]
      },
      {
        "recipient": "gonka172eahn496yyps4fap74fv4y843n4ghl43atmkk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "156516180131"
          }
        ]
      },
      {
        "recipient": "gonka1cm5hykwz4vygmmvv6uf3jhxtg2dnt56799p3d7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "156182631825"
          }
        ]
      },
      {
        "recipient": "gonka1dutrpxzkvnjqt75yqwlszkeegujsuprdu9vr8g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "155651458202"
          }
        ]
      },
      {
        "recipient": "gonka1kpj3zlnu9cj94nyraaxk4jcmqddvhnxzacjmg9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "154202832584"
          }
        ]
      },
      {
        "recipient": "gonka18fgyw8c7deqkk4zq8n9efgrwjjypdrd7cskv48",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "154076603835"
          }
        ]
      },
      {
        "recipient": "gonka1w0fj4kscwkru05vgq4pk3xwdf6dq63emw7etw6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "153903941571"
          }
        ]
      },
      {
        "recipient": "gonka1yysfdney9ayqhgd8e03zdkhqte3pr09zzevdrq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "153058195413"
          }
        ]
      },
      {
        "recipient": "gonka183y38fjefqfgxafe05fw24rjtj4elzy84wxwdl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "152807764227"
          }
        ]
      },
      {
        "recipient": "gonka1e2wq9deve5zk6znff34c0x9xdklt0qs6u43x4x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "152046448413"
          }
        ]
      },
      {
        "recipient": "gonka1h60zhqxm8c40aupf2fwjd8uxlzsle9n55jmzn2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "151958899171"
          }
        ]
      },
      {
        "recipient": "gonka1az2ancd696ewym33xvskz0pznqxdv6ya2ljy84",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "151932993107"
          }
        ]
      },
      {
        "recipient": "gonka1f9w9z55f4spuhwus5ksc86ynd9t4fxyphlkkvf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "151779181849"
          }
        ]
      },
      {
        "recipient": "gonka10rvvl89yply8d5rks5k0674fadat45e3gvtau5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "150902484619"
          }
        ]
      },
      {
        "recipient": "gonka10jrlgh9yege62d3wnytkgamdgjyqs9xpjxm32n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "149737865560"
          }
        ]
      },
      {
        "recipient": "gonka1ev28hzcw4tduvnuk0avlckq33cusgf3n3gr76k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "147757474732"
          }
        ]
      },
      {
        "recipient": "gonka1h4e7j4h5jy8dac8sjqke2pckvv6eva5ec2v0jv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "146849951021"
          }
        ]
      },
      {
        "recipient": "gonka19ne8zk9j5xk50zvwcpwyeyl2wn72xmwkfycnse",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "145209327994"
          }
        ]
      },
      {
        "recipient": "gonka13e5a0f67nzmvcdt27c083np9wlmqz2sjexnh4g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "144573220781"
          }
        ]
      },
      {
        "recipient": "gonka17339jstnve8h7mzms493x9twwznadymtvj7vjt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "143413498930"
          }
        ]
      },
      {
        "recipient": "gonka1ut2pkphww74zzeyadhs7u7s6k9rrcmfrnzd6y6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "142805232382"
          }
        ]
      },
      {
        "recipient": "gonka1vtz94uthrqn93rcf2yn4hpuj2q6pqkhh632j6s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "142284804161"
          }
        ]
      },
      {
        "recipient": "gonka15natyl5kwtzta9lr0xeqmew3j5thza2lslvw4x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "140802844450"
          }
        ]
      },
      {
        "recipient": "gonka1hk6css6jcxwcjnft04fwmnww67u8kuw0865gv3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "139111306692"
          }
        ]
      },
      {
        "recipient": "gonka12c8m72s7g8mudeaa440tpkafs973vjhllv3fuc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "138036035184"
          }
        ]
      },
      {
        "recipient": "gonka1dc2utw2lm4ucr8q7r6wthglfsrck49z7rqdv2f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "137272425110"
          }
        ]
      },
      {
        "recipient": "gonka1r9zaxcvn5rysp09hrlla6k8ltssuhtpl07wtqu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "137067051773"
          }
        ]
      },
      {
        "recipient": "gonka1lzxwqhc5fqwltg57emk2lprd7qzmapp22mv0h7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "136134900662"
          }
        ]
      },
      {
        "recipient": "gonka1y9vw8ejeknw5h5n0tunzxffjh33rdn5tddhaud",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "136074117621"
          }
        ]
      },
      {
        "recipient": "gonka1w0tk2ghwtgd9l4xakrgvrugcc9rptwpg2z33a2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "135421921802"
          }
        ]
      },
      {
        "recipient": "gonka17h7crvknkw8er5cuc43dgdp8eh974s5hahauuq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "134798235437"
          }
        ]
      },
      {
        "recipient": "gonka19zywrpdzxws82hpqsw2addmlkwkfwwcm805djx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "134784519739"
          }
        ]
      },
      {
        "recipient": "gonka12wcc34cfzmqu57w96squwnmp9yw32j04s9hss3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "134398933707"
          }
        ]
      },
      {
        "recipient": "gonka1k7u2vdwaljgcvhkn8nftxq3ffj6zzq09cw0shq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "134388658518"
          }
        ]
      },
      {
        "recipient": "gonka1um9kz95phrhe439rent9q9ld3huvdcy5jf6t0x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "133426507127"
          }
        ]
      },
      {
        "recipient": "gonka13r5m25jc0q69d9mjzhjfdzdu3t24n5te793l4x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "133343103856"
          }
        ]
      },
      {
        "recipient": "gonka15z2fxrrxx7cwk4j7vp98rat7ajfpjxrqevyp0s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "132724968024"
          }
        ]
      },
      {
        "recipient": "gonka14wp5g2auyarncnwk6ufl8stmyrlgzx0l0d3f80",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "132673212651"
          }
        ]
      },
      {
        "recipient": "gonka1maujm456qnv250gfydngd8dhf7yh356ca3h5pv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "132364393420"
          }
        ]
      },
      {
        "recipient": "gonka15s3uh8xyla66mx86hknjs6rrq740e5dtc6guga",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "132038508775"
          }
        ]
      },
      {
        "recipient": "gonka1pzdzdgd3auppy7x8a73suxaucgjcutfevrwzjp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "131528255395"
          }
        ]
      },
      {
        "recipient": "gonka1laltt78qucmexcplsm9t99un7h2329vmdhrc62",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "131494563463"
          }
        ]
      },
      {
        "recipient": "gonka1ctgxkaut4gdsj5rv3eru275df0t606jav0exfd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "131210890946"
          }
        ]
      },
      {
        "recipient": "gonka1rpedugp4rhy989wfg8tr5ux7k6d4fhkjlqk234",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "131165213697"
          }
        ]
      },
      {
        "recipient": "gonka1z9wz95l4eu2ltwvavy4m7w5qjvyac3ktt5zhs2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "130951300105"
          }
        ]
      },
      {
        "recipient": "gonka18cy6n7f3ceu97uxe5xqtr0ndww55wmmahg330r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "130759784369"
          }
        ]
      },
      {
        "recipient": "gonka1d5v93rmxuramndpmcsxvum6e5snznkw90nedha",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "130371958274"
          }
        ]
      },
      {
        "recipient": "gonka1qpz3622ewmu42cu0l9gelga7wyet57m4pllwc9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "130192901188"
          }
        ]
      },
      {
        "recipient": "gonka1rk43zfsxe7tefa88qh3t7wl3dvjwn3hq22njc4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129962381233"
          }
        ]
      },
      {
        "recipient": "gonka1nlp2g4ze3799z6xqvsjqqkqn746mtjs7t6v7kc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129920348863"
          }
        ]
      },
      {
        "recipient": "gonka1270mrwh27pgnrtmmsmyy5rsq2h8ug6l4zvg4cu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129781359391"
          }
        ]
      },
      {
        "recipient": "gonka1cjvdez8e6mwjxg0e3g7rrds9ezm9c7kemlu3g7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129659729868"
          }
        ]
      },
      {
        "recipient": "gonka16de96xdt4dqfjslenvu6pwd9y96n5scqqq9sy9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129484936698"
          }
        ]
      },
      {
        "recipient": "gonka10fvaz7sgva6563fkcp9wxlk5hz7gj8fmu0w699",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "129266291194"
          }
        ]
      },
      {
        "recipient": "gonka1pmxhj3vqv0uq5l4nvdeky4lpjyryw3fg24ste8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "127476065003"
          }
        ]
      },
      {
        "recipient": "gonka16324l7r5jllqjm7e5wlf2h44cr3dsmjj8a6py7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "127316042720"
          }
        ]
      },
      {
        "recipient": "gonka17w5kpa57jtqnqy7wdp5d03jkjmk0vjwdpp5xmg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "127306159205"
          }
        ]
      },
      {
        "recipient": "gonka1fwjwxw6cvspwautdrhr2jf4mfayy074t5npwnx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "126899324556"
          }
        ]
      },
      {
        "recipient": "gonka1f4mcr5pzn9rtdyzdv9dfg4x47vrqxk0f2ujqs7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "126046910212"
          }
        ]
      },
      {
        "recipient": "gonka1ky9mpdps70l9fe59dg7a7ctnaunkuuc8uet8q2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "126035998095"
          }
        ]
      },
      {
        "recipient": "gonka1z6va0ch94wqltysk7hc6zd6qjp0wddayrw2hua",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "124756655528"
          }
        ]
      },
      {
        "recipient": "gonka1qu9mna5xlvlnw9455ygtjq92wuzkzm237w8l08",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "124587196777"
          }
        ]
      },
      {
        "recipient": "gonka1ays6epuyqejjj0fxgj9lx9mxv42q3ac64y28sp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "124090764074"
          }
        ]
      },
      {
        "recipient": "gonka16sfwtnse80aleg7sgmumnu3qxhtf93mf86479a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "124064035159"
          }
        ]
      },
      {
        "recipient": "gonka1wdcy2gdq7kfj9e0y3g0gtjl2cjdtqep3s8r5dk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "123629210589"
          }
        ]
      },
      {
        "recipient": "gonka1w5vse5uanra5uvkgzwf6mx2ltrev0tvpnx72g3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "123282336551"
          }
        ]
      },
      {
        "recipient": "gonka1qlwcwa7nppc0ng5qccwm3g0t0knkf5nmr036vc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "123151176825"
          }
        ]
      },
      {
        "recipient": "gonka1rt963v04mgt43ju2smuakde99pv7wscy5yxnte",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "123101315702"
          }
        ]
      },
      {
        "recipient": "gonka1jcxsgcnctv69xd9v35qy45m45pg3wwhn0f8pl2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "122771515329"
          }
        ]
      },
      {
        "recipient": "gonka10arv470cmu80mlz3wtrkk0xt93lxy62mqzyfdf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "122241510732"
          }
        ]
      },
      {
        "recipient": "gonka15y9q9je0hs0uhq39v37g9yprhxhj8rqu5cqc58",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "121891963143"
          }
        ]
      },
      {
        "recipient": "gonka15phrun9xzcm2f9vz7lfef9yj26xjhte9jl2jvc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "121106135330"
          }
        ]
      },
      {
        "recipient": "gonka1pjpkm3plwgr3h7jemjxtvfeqypnzemussthdvz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "120561777639"
          }
        ]
      },
      {
        "recipient": "gonka1guvvfsnjfxa573k5f8tc0wam0h4hhcfldlyky5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "119869867063"
          }
        ]
      },
      {
        "recipient": "gonka13u2c48f45umqvmdpfrfxdt9xcu8erd044wpwdg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "119768896713"
          }
        ]
      },
      {
        "recipient": "gonka123fment8nj6mrekwv9rh5zmevxjd7t05c8azrd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "119320259600"
          }
        ]
      },
      {
        "recipient": "gonka1snurcwfvugkldrtr8pmdnpaugf9khcp073sfzz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "118967130447"
          }
        ]
      },
      {
        "recipient": "gonka1fs4fapsf05qf3992m92ac3cl38uzh56vev4806",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "118301931963"
          }
        ]
      },
      {
        "recipient": "gonka1rre47ll99hmea7eselqcmmnh5xncqyx0jlvylh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "116853501225"
          }
        ]
      },
      {
        "recipient": "gonka103tuctlftrr5zzc2vgmu86vw4u6pus9wxnm8a4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "115732147820"
          }
        ]
      },
      {
        "recipient": "gonka1lm0jdqg6v2m5hekyh7ul039sqnlhjc8qw50yq4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "115440034138"
          }
        ]
      },
      {
        "recipient": "gonka1895n7u9np4s675vhksellqkpkqxk5xkv4upaxr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "115354023876"
          }
        ]
      },
      {
        "recipient": "gonka1vrrsqx454f04dmadju83dps8742lh0klrjq05n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "114565133254"
          }
        ]
      },
      {
        "recipient": "gonka185kgdje9wjucxtkdu0nqhpqlwxutc5kc7nss8u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "114359358092"
          }
        ]
      },
      {
        "recipient": "gonka1hdm8wlf8e07e692ezay5g8qyemks4242g7kr9d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113839791894"
          }
        ]
      },
      {
        "recipient": "gonka13kd0e5393704ummmwf7pqvphlm5qsqdpe3kal2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113627417363"
          }
        ]
      },
      {
        "recipient": "gonka1gd74wnjdp0sjxf5slgtwqx4t7pphvwl9qak360",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "113514953117"
          }
        ]
      },
      {
        "recipient": "gonka14mn57n7sq2mcf5mm2399fmqrgujwgxlec970ar",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "111531052020"
          }
        ]
      },
      {
        "recipient": "gonka1jfr0hq4k5lfzu7h2qsvh8dppard9t7lndsrngp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "108753172219"
          }
        ]
      },
      {
        "recipient": "gonka1jcut7ms9l432y90exzpfz5835p04lrzpndtdfl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "108690771987"
          }
        ]
      },
      {
        "recipient": "gonka13mehzn6a86z7mkf0fcked5y2644r7hnq2txxpa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "106795222668"
          }
        ]
      },
      {
        "recipient": "gonka1q35556zp34twsnaa4uk6300zjcn3f6ucpawtf2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "106715637183"
          }
        ]
      },
      {
        "recipient": "gonka1hzcmnax508hhtudrxpk52djg9nkl5cpxflz2uk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "106522545672"
          }
        ]
      },
      {
        "recipient": "gonka19rd75sm0zeh2cmnepmg79ffn00jtpsdw2zj495",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104746067502"
          }
        ]
      },
      {
        "recipient": "gonka1rrmf3s6m7rh3plqn0xam5c38xsl9wwvrtjzr48",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104693626058"
          }
        ]
      },
      {
        "recipient": "gonka1r4vqtz3mhhxzk83693xy8lt3rey5u9l7w809jd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104509634423"
          }
        ]
      },
      {
        "recipient": "gonka1mjtqjukfgjlzg82tz3s4pwna06kan7zmhysfqd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104122884934"
          }
        ]
      },
      {
        "recipient": "gonka17d3y8a0meyn4ql7a9rk5c24dlx0kke0lvt9ndz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "104058765553"
          }
        ]
      },
      {
        "recipient": "gonka1ppvjh3l2q0rrz7hz86uaywzzn44edqqcwstplg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "103288987878"
          }
        ]
      },
      {
        "recipient": "gonka1pd4qf3clxgtc4nu5q0nltwugc49ukl2laep5xx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "103143431572"
          }
        ]
      },
      {
        "recipient": "gonka12p5ausvgfg5m9d8t47pvm4j7wd0vzfflv7s88n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "103118913038"
          }
        ]
      },
      {
        "recipient": "gonka1td0msg9jesqsk8k3wnu32zpg9femfgtaazmt23",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "103108880731"
          }
        ]
      },
      {
        "recipient": "gonka1dzk7rawvnkfwfptkzhdf7dh5s4xsqfml72tmcy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101825659644"
          }
        ]
      },
      {
        "recipient": "gonka12634qjw29fmhf3yw7rlcgf8mldl56r2ufqk8rc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101800864877"
          }
        ]
      },
      {
        "recipient": "gonka1jpr8eqt329k8en46lldxr8hlkmqeaugnhl5yf6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101610655231"
          }
        ]
      },
      {
        "recipient": "gonka1wpz5sgkjwhkh9py26rp3zlefgc9sc673gkncmk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101335290873"
          }
        ]
      },
      {
        "recipient": "gonka1dyhqew6q9xfxx5taqu3purr9nd3e43h5lznqd3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "101007211526"
          }
        ]
      },
      {
        "recipient": "gonka1v0td7x4ndxhveg50vzp6nkz4s25qy2wpvrxm32",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "100348368672"
          }
        ]
      },
      {
        "recipient": "gonka12sjs2wwerzfp25y2w9cqpwk9r8z4uddmlt5spw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "100065871270"
          }
        ]
      },
      {
        "recipient": "gonka1jawqmq4lmu8fadddrt0mejfxu5lkrdc02fwuzm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99394771511"
          }
        ]
      },
      {
        "recipient": "gonka1fyu654mhgdq2fwns2mupuzdtzxjy3k7jwew4rl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99363059061"
          }
        ]
      },
      {
        "recipient": "gonka1mennxsd8zj44rsmlajyv5ygflke4hqhlpvx36x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99112729540"
          }
        ]
      },
      {
        "recipient": "gonka1ya8us8ezzpppg5ncy7z0n6e43hn4z268vgqvh5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99087685606"
          }
        ]
      },
      {
        "recipient": "gonka10ujznhjy9m2chl05dvjhvf525202yz8hwkzsqu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "99080710750"
          }
        ]
      },
      {
        "recipient": "gonka10r5p7vd7sw6tthp0nuld8yajvpgufamrd63epk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98853788734"
          }
        ]
      },
      {
        "recipient": "gonka1r4qetzmw4g3aenwtcxpdm6l42aeq5gzwqltn39",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98841091076"
          }
        ]
      },
      {
        "recipient": "gonka1ap3tj4grfc000wqyxw8hna7aa96xkd65gfq4fs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98600587026"
          }
        ]
      },
      {
        "recipient": "gonka1mjjaep4d3vt9myh96zrslx6cet5qr0xvd9zqg3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98365224243"
          }
        ]
      },
      {
        "recipient": "gonka1zn4ey6xqym4vzr6s8trtu65n9wez648fysxz67",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98152946833"
          }
        ]
      },
      {
        "recipient": "gonka1fujc399fxp9pjrjvd0ymjjk3rzsgl4raq20pg6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98146886859"
          }
        ]
      },
      {
        "recipient": "gonka14g5nf5z695era59sz6zat5mv7n4w73vp26cgx5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "98046972854"
          }
        ]
      },
      {
        "recipient": "gonka1707yvgk9wgpzrp35wd84mcps4pujelx36n5du9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "97633080910"
          }
        ]
      },
      {
        "recipient": "gonka1ach2c5kms3ds2728a7dlqwsgddftxljsefxd3u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "97318831010"
          }
        ]
      },
      {
        "recipient": "gonka1pdk0x9w50zsym389jlkhp6skdzx480m2p8ymvc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "97288189733"
          }
        ]
      },
      {
        "recipient": "gonka1a8u5zzrmhhdz7hp4gk3lmpltrwq90ley2cn5ef",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96908898986"
          }
        ]
      },
      {
        "recipient": "gonka1mjk8kvkr34vm974s0hmjuanrzv8y4fj3r8fjjm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96665741850"
          }
        ]
      },
      {
        "recipient": "gonka1djqnccng4mece9p7kpyh588thq6hzt3vk2fmln",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96631310149"
          }
        ]
      },
      {
        "recipient": "gonka1v765pascdp3v6qqtpdrcqm8qwdwq4hxa85gu5z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96463736476"
          }
        ]
      },
      {
        "recipient": "gonka1y58p9p64g0hu6uct73qhnpwlgum9t2fjjqmu4j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96403504140"
          }
        ]
      },
      {
        "recipient": "gonka1gxk3xjg43ryaht8ze0395m7ph4879gmsfd5emu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96378122086"
          }
        ]
      },
      {
        "recipient": "gonka160q92s7d63d3gtcx5lmdxu92uf8fjqut0v622k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "96131889143"
          }
        ]
      },
      {
        "recipient": "gonka1dmjrdj39n950jzcxqw6zqa7vhtg945gqu5tfhm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "95900252568"
          }
        ]
      },
      {
        "recipient": "gonka16cstfwxnuv08zpyalmv38e48crhe8a9pft7etg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "95852808244"
          }
        ]
      },
      {
        "recipient": "gonka16uc05mvmja22zxgljh6fs82533w805h5ya3nzg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "95099239123"
          }
        ]
      },
      {
        "recipient": "gonka1zepcpcnw6qa45k38muhgavzflelun6rh5hu35k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94985993363"
          }
        ]
      },
      {
        "recipient": "gonka1zzkxnpq2txntwh5eu49jk67x42yh8wystnkamy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94948040978"
          }
        ]
      },
      {
        "recipient": "gonka1udx48lyqzrc2ygpkzjq6wthh3ejm6x5cytvxjh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94914864372"
          }
        ]
      },
      {
        "recipient": "gonka1zhqp9w6nq9sexnew3pg9auqhz85dm86ght6sz0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94865153257"
          }
        ]
      },
      {
        "recipient": "gonka1xycg2mc0ktaz4372q4ln3f0thefk86shhguk0w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94740499656"
          }
        ]
      },
      {
        "recipient": "gonka135jr9e2gyzq5lfqvc9tq8n0k3c398dgmmwy835",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94453083418"
          }
        ]
      },
      {
        "recipient": "gonka1rpszx3te4396yyplpl7lmcqngcwtk5vw0t57ym",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94213445288"
          }
        ]
      },
      {
        "recipient": "gonka13qk3jur62xvma480z767lc0ks8c8esc28nxmvt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94200923689"
          }
        ]
      },
      {
        "recipient": "gonka1h4ajcmsuzuwxx8h9h3vwcn4gr74ld99cxkfux7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94145274686"
          }
        ]
      },
      {
        "recipient": "gonka1zaklf2yedw6my8lw6vt797vzpn67qeusj5a6zl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "94027646763"
          }
        ]
      },
      {
        "recipient": "gonka1n3xkj998f4q6lf62v7hw7r07jcwaer8xlmjrww",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93814425565"
          }
        ]
      },
      {
        "recipient": "gonka1r9u4nyprt7ym64pdea4a7wpjf446c0zsmphqx9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93814268546"
          }
        ]
      },
      {
        "recipient": "gonka1jjredx8nvy86dcae5fhpvge0kmamdxx2h7dr9h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93360669761"
          }
        ]
      },
      {
        "recipient": "gonka1nuhz5kqnmxs3dfd884hdv39kdy2854lff8ma8c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93139084616"
          }
        ]
      },
      {
        "recipient": "gonka1sn2fuds6qh5dhrdp7afdyepmr6lcpwvsuwzlye",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93076148574"
          }
        ]
      },
      {
        "recipient": "gonka1tvgem50n2xna9apg29wm0ts5rjmjxj0zv23t69",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "93040772174"
          }
        ]
      },
      {
        "recipient": "gonka12fnudtsmw6heu6t982rnk8c5lgpgz4wmvwd75s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92917832759"
          }
        ]
      },
      {
        "recipient": "gonka1fp444xd5027mzhx0tnlxkx6euczhp9glt5f09a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92870034734"
          }
        ]
      },
      {
        "recipient": "gonka1w0vl46tr786vdtgtk5fyadnsqtl8pyc8cf7txy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92334898742"
          }
        ]
      },
      {
        "recipient": "gonka1mt6fz28j7rls3psgspaq0xhj862wlklgcat6am",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92230277903"
          }
        ]
      },
      {
        "recipient": "gonka1ylhpz2dd9f6x6apkzr773yw0kaagkhpaph86qn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92052863940"
          }
        ]
      },
      {
        "recipient": "gonka1r4zuhduduwqzyw4a5y5y5aw57sj9jl56qpp7pk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "92046884335"
          }
        ]
      },
      {
        "recipient": "gonka14ntugumwzhdlkc66qlzczdmfa02fcm4pcldtwz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91978374358"
          }
        ]
      },
      {
        "recipient": "gonka182wjthlm5zdkwpcc3x5cfy83sel392ljwufsz7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91796190843"
          }
        ]
      },
      {
        "recipient": "gonka180h3x4dv834pyn2ua3k596hrsk7d2l5utljtg6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91623762432"
          }
        ]
      },
      {
        "recipient": "gonka14r6ypa2jngcd8pwt22f2nwdhlt2s3cxr4k9xne",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91578702172"
          }
        ]
      },
      {
        "recipient": "gonka12gmwdxjwyqs8y2cxjzrnza8jtf2pyp34udp893",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "91160224704"
          }
        ]
      },
      {
        "recipient": "gonka1qfq964gewr83f4vh26qz25hl8na7kmvy93j3el",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90860100796"
          }
        ]
      },
      {
        "recipient": "gonka1p8g3rh58seh553lqywe6rz7ratkm0j4p6kxs3q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90805078088"
          }
        ]
      },
      {
        "recipient": "gonka1jr3644x2p5j90yl3jpyuvfrp28l37vpvkjq2yx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90782290218"
          }
        ]
      },
      {
        "recipient": "gonka1ezpg20aga2mv3avkda2zqh5nh8jys9pg0q2cnq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90775814301"
          }
        ]
      },
      {
        "recipient": "gonka17ftklmd8esnj47nr7dg7c5c6wujvqxqjv03774",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90714808880"
          }
        ]
      },
      {
        "recipient": "gonka1e9vdm8ny7saz4n7yx7hng8hvdj0nu85v4edgnr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90592471780"
          }
        ]
      },
      {
        "recipient": "gonka124hmlh3500ysl26n25nlfsgnj0hxuvy9cwcrql",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90461276907"
          }
        ]
      },
      {
        "recipient": "gonka18vdcv0y6ms6xgvvvt7mrfnd3drqte5qhwcx9z4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "90171717711"
          }
        ]
      },
      {
        "recipient": "gonka1j6ddjngvwy3x0yze36nks8dvlqdep9fxaj67tv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89957741125"
          }
        ]
      },
      {
        "recipient": "gonka1wcqxjxzjsfwvaxl3l24qzemjlf0e8nextxhv8j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89880996129"
          }
        ]
      },
      {
        "recipient": "gonka1a90lj3ks0fg7mxrvqy7dx4g09g72hrlndpmwsj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89781778806"
          }
        ]
      },
      {
        "recipient": "gonka1hqwgkck88d5wnpea0y9dn0gxmyg4rwjgcnvacf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89749374453"
          }
        ]
      },
      {
        "recipient": "gonka17mw34tnvce5jg8s2lrn07556guh7yj25dgm4pf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89631346745"
          }
        ]
      },
      {
        "recipient": "gonka1u7l9jg4krgl8kpu9lc2ml8hscjhmyrgtv6nd2q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89550533869"
          }
        ]
      },
      {
        "recipient": "gonka1y9vdzmy84uy9c9dgqx8adnusg3ssv7wjmscga8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89464227627"
          }
        ]
      },
      {
        "recipient": "gonka19gua58wyw5q5r2zqfnzj8srrftk4wy5kewszue",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89249641302"
          }
        ]
      },
      {
        "recipient": "gonka1r2366aa7ql8t9welxtxpjvzwknzpgzkqqssuld",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89171932070"
          }
        ]
      },
      {
        "recipient": "gonka1xspavhncfmlpsllpfajs3r5623a4s8tcumrmwa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "89095259493"
          }
        ]
      },
      {
        "recipient": "gonka18camnxdy5vc2x6752dqter77a0gjjwxg3k5ece",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "88361666090"
          }
        ]
      },
      {
        "recipient": "gonka1ts6k67zt064z87rx9hztm93cd3yh5mkqje6z4c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "88233756172"
          }
        ]
      },
      {
        "recipient": "gonka1qcamnqy86hqzcatvlgr78mvgmpcc25ms40pdj2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "88140042305"
          }
        ]
      },
      {
        "recipient": "gonka1ktd5rha9hghm4hzt2eyc8v2p6g66a0zmry07qh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "88100124152"
          }
        ]
      },
      {
        "recipient": "gonka1l5y7amaux93wgd60wn0446h97ezl3vjd6sy025",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "87851457797"
          }
        ]
      },
      {
        "recipient": "gonka1eujeuwxcv5skh3pv6njzjcjs53pfafcun307eg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "87631863329"
          }
        ]
      },
      {
        "recipient": "gonka1sycnmyd9rfw0gptt3s604mg9zgpvhg05lgag4m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "87040314540"
          }
        ]
      },
      {
        "recipient": "gonka13fpvt243g8sh87ere5avz74qx5qj7vzesr0p4j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "87031978353"
          }
        ]
      },
      {
        "recipient": "gonka1j6muv0n8023gm7aapthnrf0g3a86w6hg98wgcu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "86957076905"
          }
        ]
      },
      {
        "recipient": "gonka10snluhflqhmwl5xrpuy9ugevypxdjjsft370fq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "86248504694"
          }
        ]
      },
      {
        "recipient": "gonka19h06zf4dmh2qgcdj90cthnw85vpz59cusa72yj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "86082840435"
          }
        ]
      },
      {
        "recipient": "gonka1gxue6uufgvh6dgjexqvsv7ph99k8wkatafymqw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85650539447"
          }
        ]
      },
      {
        "recipient": "gonka1x27t7qzmphupfz88ysycct97m49z2e27khhsw3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85580796539"
          }
        ]
      },
      {
        "recipient": "gonka1g6x8ffcysdfju6anvt7we6u2e80fl7pgzjmk99",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85576402054"
          }
        ]
      },
      {
        "recipient": "gonka1m0ftrwltdf7dntqhx9juwgadzyl2h4m3sm77zj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85261614159"
          }
        ]
      },
      {
        "recipient": "gonka10000627dkz6nvmf09ctqy073v0fls696uznwgg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "85195742182"
          }
        ]
      },
      {
        "recipient": "gonka1xl56zt2c2ahfuk0u68x084avulmth95lptx9cs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "84075875465"
          }
        ]
      },
      {
        "recipient": "gonka1qncqtrf48qrttfwd2s3j42dfnanyvcg6cvwyzs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "83289011476"
          }
        ]
      },
      {
        "recipient": "gonka185kz5j9ur5jczu9wf2vful353vg3eahm77n39x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82904464621"
          }
        ]
      },
      {
        "recipient": "gonka1rpdnweugm7ykl7hy4p0qe858m9fvkgdm9k5m3g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82676318325"
          }
        ]
      },
      {
        "recipient": "gonka1x9qndq86jt6x8r5pqx4hlx92rl0x3qu2hn2d3r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82461286603"
          }
        ]
      },
      {
        "recipient": "gonka1a3qq9jmmhr9xyn8p56v5hzfeuxp9r68suv6uhy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82204026961"
          }
        ]
      },
      {
        "recipient": "gonka1qc0ygywfl626jmy2ccq9a0swt9zr3p39vf4xwq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "82040544704"
          }
        ]
      },
      {
        "recipient": "gonka1j4pnudv2z7wtfn0l83glqv8x7shtkcustzca40",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81950403605"
          }
        ]
      },
      {
        "recipient": "gonka199lgrq8l9xcqqnr0agajzl78c4dpfvwnsc4elm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81906401738"
          }
        ]
      },
      {
        "recipient": "gonka1u33ffwp7rswdy9upkxrgq726gk42z8qyqkv3rz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81393348557"
          }
        ]
      },
      {
        "recipient": "gonka1xccz7s9k0mhys2uuyaqjsnn2wm90uv3lrh7s4r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81323872273"
          }
        ]
      },
      {
        "recipient": "gonka1lyafw67ys2ft7t4npn7y940696r38kfn9k6xlh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81313899110"
          }
        ]
      },
      {
        "recipient": "gonka1fnwznrjccpukhe3u5dnqqnr02nhr5hq89jhghs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81148339233"
          }
        ]
      },
      {
        "recipient": "gonka1l2pu0eqvsah7ap5hy6rdn6dxse37wy6cy4k2ef",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "81013936463"
          }
        ]
      },
      {
        "recipient": "gonka1mu29dgr7yx6l3x46c535p2aymzp0hns2fpz5e3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "80695586398"
          }
        ]
      },
      {
        "recipient": "gonka1pq5f5c4k8qn7k73qkzza460y435r3dusaxytys",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "80636595060"
          }
        ]
      },
      {
        "recipient": "gonka1auert95hm33pzvzau2pe2ft62krx7d39ypknxm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "80467028178"
          }
        ]
      },
      {
        "recipient": "gonka18wn7au6ezwnswn9jaqhjkf7wa9plrppd0ufz3p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "79811207133"
          }
        ]
      },
      {
        "recipient": "gonka1c3wplss6ju6fc5mhp0dg4lc7lhvkyrvjg28ejl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "79442825338"
          }
        ]
      },
      {
        "recipient": "gonka138qmc42pq75mxf3r3fh9k35ukvj9frmvuc7f0p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "79104869230"
          }
        ]
      },
      {
        "recipient": "gonka17kua4qvnfmedl4atk2e03gjlgm42qxckef6uhw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "78966317577"
          }
        ]
      },
      {
        "recipient": "gonka165pppmxfxxzu4dn33twqwq2rz5cnem2srprlnn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "78501576885"
          }
        ]
      },
      {
        "recipient": "gonka1mhmedjwqt6gsx8urpwehyhud5klxxra2r6cgy5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "78191452363"
          }
        ]
      },
      {
        "recipient": "gonka1ucxu8fuqv5vt8rrwrmt45lkjx5u3e99ajtgv4h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "78024194907"
          }
        ]
      },
      {
        "recipient": "gonka1rz9h38uuyxvfhgh9jrdc8s2gjjcsex36xsvl2l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "77833473263"
          }
        ]
      },
      {
        "recipient": "gonka1g2sspwpvsetwxmwjyp5e4pe2e67clkfpc3sfld",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "77383886748"
          }
        ]
      },
      {
        "recipient": "gonka1kadhltjszhue262r7z7khldv90ru8cvy42zv29",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "77216401578"
          }
        ]
      },
      {
        "recipient": "gonka1r4cnahcpv6kktwcg795lnqwx5q74fmawsasg75",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "76804234728"
          }
        ]
      },
      {
        "recipient": "gonka1qx4f2vzhccv0ndhssfgafvf55xf4smuzjmkvky",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "76484009057"
          }
        ]
      },
      {
        "recipient": "gonka149q5us80a94u45uuedufucdmn8ud5xq4de9g9e",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "75888387094"
          }
        ]
      },
      {
        "recipient": "gonka1d5nh80xxh7fkf0hmqlxqfq6vls8cq3j0fgg8f3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "75670029934"
          }
        ]
      },
      {
        "recipient": "gonka1tdgnyws5p4ddg2wsg08tmdwggfxpp6e4ev29yc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "75487213864"
          }
        ]
      },
      {
        "recipient": "gonka1gyydhl9lp0udz3409ps0c0lk0y4ft8qcyv8tfq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "74670879328"
          }
        ]
      },
      {
        "recipient": "gonka105fgwnqwd72m685xcalvvsdyzmf59khq607rlx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "74655472026"
          }
        ]
      },
      {
        "recipient": "gonka15nkz4dxslphkty92y0c8m9umule32g9n5e5wvm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "74224656430"
          }
        ]
      },
      {
        "recipient": "gonka16gu0el3h5p572lswsmldyg358apqphcxsdfuq2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "73664304515"
          }
        ]
      },
      {
        "recipient": "gonka1c3jmrfkysvrlgv9av98wlyq4yed3x7uue0wvy2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "73495720908"
          }
        ]
      },
      {
        "recipient": "gonka15rvksn9gxgpszyr8270cd4wj2x3d460r394uv4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "73364273374"
          }
        ]
      },
      {
        "recipient": "gonka1cgf6pmcnkf54rctpgzpx6j32zeut8udm0rr8rf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "73039999876"
          }
        ]
      },
      {
        "recipient": "gonka1psgzz288a434dv6863ldd73xma70zw7387muj2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "72928738056"
          }
        ]
      },
      {
        "recipient": "gonka1ql9asemklpkpr2d4mh33xw5gj0g5tm0v98c5q3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "72928738056"
          }
        ]
      },
      {
        "recipient": "gonka179g6jf5uulrufkhwlymsmwwu93r0j2qvpkdh53",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "72432731038"
          }
        ]
      },
      {
        "recipient": "gonka1v9r9a4rnmqqvz3h8fzc72aj80j0pma340f45xk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "71749717564"
          }
        ]
      },
      {
        "recipient": "gonka12chgl62wfzvkvjwj7mz568ct7xyzdaa0ld4d8c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "71580103440"
          }
        ]
      },
      {
        "recipient": "gonka1adacqpq6z6sg9qqsy4f0p02p0sfn2f6n6dldae",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "71080597479"
          }
        ]
      },
      {
        "recipient": "gonka13x8n3ttss76js4f86maeck6uey5nklvy6lvdnw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "70873731290"
          }
        ]
      },
      {
        "recipient": "gonka1cnnxxev6yaauzarywk6n6vcs0ej0jygwvff9xz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "70139978358"
          }
        ]
      },
      {
        "recipient": "gonka1thdyumjevc50uf822fzk6ypmychmvsdqu6wnnz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "70006055624"
          }
        ]
      },
      {
        "recipient": "gonka1myknj5jphyt8tlrgzf3zs4a66m4x2httq627sd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "69808784200"
          }
        ]
      },
      {
        "recipient": "gonka10ekkjpyfad6265m2502d4tp3n8yp9n0d7rlzk4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "68295169799"
          }
        ]
      },
      {
        "recipient": "gonka10prje5tj49lek50dpch085f66crl62sut2n0vw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "67445879840"
          }
        ]
      },
      {
        "recipient": "gonka1qhzauckmv78r9wpsr6lvjku5g70hmktgv2ku7d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66900282591"
          }
        ]
      },
      {
        "recipient": "gonka1cmlns93pn4ddkn9rz4lqcedjacwg6t6vxcdzjk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66738741782"
          }
        ]
      },
      {
        "recipient": "gonka1rvjfqzm8spt5nfq84jvfdr8we8pgkv8ent08s5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66694599285"
          }
        ]
      },
      {
        "recipient": "gonka18zgw37evwkpes7redzgh79pjy77rkv5hx4xpz7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66681318749"
          }
        ]
      },
      {
        "recipient": "gonka1k7qxl4aqv4yu2we32v08wxac6hpuzp9z535sxt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66666998214"
          }
        ]
      },
      {
        "recipient": "gonka1ggr0m6pm98pdgm9tacqekclaavm6jgqvxespaq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66088918807"
          }
        ]
      },
      {
        "recipient": "gonka144yh00dcckkpfwr5mv9yz2cpa68c8sw0h3c6cy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "66021237930"
          }
        ]
      },
      {
        "recipient": "gonka1000y038g5sqz6ewnq6f6ktl3xx07fmezc3zrng",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "65864614614"
          }
        ]
      },
      {
        "recipient": "gonka18lrgkmk9jawp93ppzd3q2gvldskn6yxn0gpfcx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "65724151752"
          }
        ]
      },
      {
        "recipient": "gonka1nge0x24twxwvran6rh4qe56ckxk3ecmkrjhjf2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "65668418996"
          }
        ]
      },
      {
        "recipient": "gonka13ykzwj2f5zzngs7jl7ywczgestspevqh2vagsj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "65421547215"
          }
        ]
      },
      {
        "recipient": "gonka1nl4vtgr88sy088djkxsknau5fwnx8akh3ppl6d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "64768866083"
          }
        ]
      },
      {
        "recipient": "gonka1h2qxkeglzstqhdmuewyuwdkae0rk3l8wqxwrl5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "64509160547"
          }
        ]
      },
      {
        "recipient": "gonka1strn82prjujtuh0dkpt024a4j49qgf37dq83dn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "64402004004"
          }
        ]
      },
      {
        "recipient": "gonka1rzchltn9xn5ysur4c6x89xvtuuddzccvt8zqrw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "63860517133"
          }
        ]
      },
      {
        "recipient": "gonka1skdtv4vlkwgcnqel2e48vvquhp40mq83m2yjl7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "63742010063"
          }
        ]
      },
      {
        "recipient": "gonka1zmy7dpumv9akvlsqv0n74fyxhhzsmzgjz9rvxf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "63398728288"
          }
        ]
      },
      {
        "recipient": "gonka1uup559m63mjcq6wyewff2su0e2wv5lsyyrcrll",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "63352709447"
          }
        ]
      },
      {
        "recipient": "gonka1wma6mrcffqsp9xaunscm2phckdaxj3m25efscu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "63157541543"
          }
        ]
      },
      {
        "recipient": "gonka1edyd5lny4esrc35f6egjukmnfseyyyj4vn54mc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62630134385"
          }
        ]
      },
      {
        "recipient": "gonka1a2k2pz759kj543yzxse4hvvsyjkaw0f42mkpl2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62491818490"
          }
        ]
      },
      {
        "recipient": "gonka1n0225yr8w7eqdsw3g4kz45vpnyajy69vv4z678",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62479095739"
          }
        ]
      },
      {
        "recipient": "gonka14zzmvt5esggym639wk0v8s3gdgdmnjzrh6p7rv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62432366788"
          }
        ]
      },
      {
        "recipient": "gonka1zkmn95dkr6kpt7vaqc4vdues0q4f72rttcfxq6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62312811300"
          }
        ]
      },
      {
        "recipient": "gonka162nxvxvppgfx9ahjlptezrd29t96rm9htun3fr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "62243288794"
          }
        ]
      },
      {
        "recipient": "gonka17akw9frq5grupdh9fwtc4mym3fgcujf9esdmta",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61900860097"
          }
        ]
      },
      {
        "recipient": "gonka16w7yu8apgeepr4xc44r6xq65nj2vxnykfcc0yy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61543016753"
          }
        ]
      },
      {
        "recipient": "gonka150qqxu2zf0lzc3nngal79h0n5ls6lhszzraytv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61448135933"
          }
        ]
      },
      {
        "recipient": "gonka1j9rxapzwm06quxcul5686e7f39g6swhfhwxtwa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61417075275"
          }
        ]
      },
      {
        "recipient": "gonka1zmx4cwayvhf8hevcu6am0sk8ul5trckc2uftmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61279907916"
          }
        ]
      },
      {
        "recipient": "gonka1hy4zasaf3knphe923exxm3vl6vyr8m5k8y8ucs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61262015909"
          }
        ]
      },
      {
        "recipient": "gonka1qvzmfwlcx663f6klq9050h0hs7neacy6ltyt0s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "61219102383"
          }
        ]
      },
      {
        "recipient": "gonka1djrtqmjn5gsgdetglnc9j4x6lq3yuvs2rq8ws2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "60826144815"
          }
        ]
      },
      {
        "recipient": "gonka1m7emdk4ez3dm6xmps9v28y8prreq7le58cppmk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "60258273144"
          }
        ]
      },
      {
        "recipient": "gonka1y46v988rv03mdn2c320fxtle6lramzk4nf8s6r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "60074233066"
          }
        ]
      },
      {
        "recipient": "gonka10xrtfzs46mmjs8dy48auh2xfxq07dxs0mhdcmp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "60063333760"
          }
        ]
      },
      {
        "recipient": "gonka129wh6ap5m5v0skcxvdcgn5nrfa8d0v5jwfz83p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59908319488"
          }
        ]
      },
      {
        "recipient": "gonka1fyz5uz37ah85tjls6j9kw5grjtrzugt3nwvdpd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59777122878"
          }
        ]
      },
      {
        "recipient": "gonka1jve3qdmmea6kgcl4y5r3hhll3lm0zuz7kutqft",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59673726353"
          }
        ]
      },
      {
        "recipient": "gonka1ujskhylfq7xqzvanuy90fm640zf459x0qtgtxy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59447873425"
          }
        ]
      },
      {
        "recipient": "gonka1c8utgl2469d7mjlhhd4afhj3ycm6rq60y7v8dl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59398642986"
          }
        ]
      },
      {
        "recipient": "gonka19fpma3577v3fnk8nxjkvg442ss8hvglxwqgzz6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "59024162022"
          }
        ]
      },
      {
        "recipient": "gonka1rtylvt6ylcdphuez6eqerj7d7pv7dc3kh6yvzc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "58194552206"
          }
        ]
      },
      {
        "recipient": "gonka1u9zzj3yj3mwrx0j836u9va0v7swnn4w2u3crl5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "57831348106"
          }
        ]
      },
      {
        "recipient": "gonka1n5gsftqp7ez0tcvaxm5mpxjaw258hcp5zvr6tr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "57811346776"
          }
        ]
      },
      {
        "recipient": "gonka1s5cqcwmggkp47nwczq3nluh0rjsut4auz69lyg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "57773345295"
          }
        ]
      },
      {
        "recipient": "gonka1zej4dv2sf03axwnenq9qfxvpx5wcdd65sd3rn5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "57567254646"
          }
        ]
      },
      {
        "recipient": "gonka19qkysq3adu5lrasgvgy7ecd78erz7jndye92jv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "57280775552"
          }
        ]
      },
      {
        "recipient": "gonka16ehmqk5dkl3v4stgh8k77ttc0kw7se2kn62k8p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "56036171965"
          }
        ]
      },
      {
        "recipient": "gonka104z9al2taf6gspj2qlsqtjwpxt7ypmpn5z0nxa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55771358960"
          }
        ]
      },
      {
        "recipient": "gonka10pgvk2tumqy5n4v2h9dqtkxqes9p208qdy37ta",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55629036578"
          }
        ]
      },
      {
        "recipient": "gonka1cnna5kqqynkkuwl464x4p5zx5jz00lwxdh9adn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55550103611"
          }
        ]
      },
      {
        "recipient": "gonka1000937gjpju4udj2wlj3yld0lcw024tp0ztqew",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55163652942"
          }
        ]
      },
      {
        "recipient": "gonka1ksvye76z43mrtjpdkh3krm579clamh9yh2ytn8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "55154440930"
          }
        ]
      },
      {
        "recipient": "gonka108gphssdzk24czkrm9apwf50uvs8073u4kwn5t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "54736342264"
          }
        ]
      },
      {
        "recipient": "gonka1u35yjypsyfaw4wpf7gn8m8q9ppumz0yys24tw0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "54433755946"
          }
        ]
      },
      {
        "recipient": "gonka1ctja5ccavyeqnfz7d4nw20a6ytmte9m5hrqayj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53932484693"
          }
        ]
      },
      {
        "recipient": "gonka1pgn9v9studsuhud80h8hphdq8nzxf4380vm7jy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53909712952"
          }
        ]
      },
      {
        "recipient": "gonka1rmww9xqyh0p6tyqk0pmzdexnth9q5gj6yw9u85",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53846770983"
          }
        ]
      },
      {
        "recipient": "gonka102yeygzzq74pudsa9nwvjh3q9x4q7wscr23hlw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53748095481"
          }
        ]
      },
      {
        "recipient": "gonka16d7eeauutuukquwqlj4kgunm67wm6nph9n4zxx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53547737659"
          }
        ]
      },
      {
        "recipient": "gonka1rp7kqzjeajyq0qag4hl5gcd7x5v64akghdzuqm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53452611683"
          }
        ]
      },
      {
        "recipient": "gonka15pgw0fe32rv78hdj2clch9acy0mv08j7xkrmxz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53438396225"
          }
        ]
      },
      {
        "recipient": "gonka1ddhzyd0xlhqnzp05apu26s3ay6mn4mlzll5mjz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53359805996"
          }
        ]
      },
      {
        "recipient": "gonka14n7ghzxz6252fzu7zdlfm9a6rrqd2dn3xq3ukm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53319980876"
          }
        ]
      },
      {
        "recipient": "gonka1g5t786e2hnry8c4d6fd4rh5t3vsfdnevejtsvy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "53227984900"
          }
        ]
      },
      {
        "recipient": "gonka1gjuagf8hw0skzwhekxxhccy6zy4g3qxal5ynku",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52838302546"
          }
        ]
      },
      {
        "recipient": "gonka19m47kxgeecyvl4xll882zxwcc7hva5slfxnvq5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52800202780"
          }
        ]
      },
      {
        "recipient": "gonka1d7qwgjstqhlp62hkhdujcfm2dp3snm97jr0vjh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52548445182"
          }
        ]
      },
      {
        "recipient": "gonka17fc94j99063t6ullr6cgu02ps7kwut28f9ggpj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "52038846995"
          }
        ]
      },
      {
        "recipient": "gonka1rvnehahwukcckaeu209jqszkvsztjwmfh2zakj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "51587510358"
          }
        ]
      },
      {
        "recipient": "gonka1vttxzd68fur26l9lew5netz6wxnx7hmmzdkqrn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "51489220843"
          }
        ]
      },
      {
        "recipient": "gonka10006x5p5z8zukfye552fd58qqj2qth69kv5kmn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "51393381221"
          }
        ]
      },
      {
        "recipient": "gonka16s9lzz6z882l4lzhm6lh6p4xgsy7r4qlzlgq2u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "51026162306"
          }
        ]
      },
      {
        "recipient": "gonka1qw4wmm6gp57yanpe5jmhmwpcwqzag30zgk7tat",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "50976766164"
          }
        ]
      },
      {
        "recipient": "gonka1zrmra5s53f6pgzxx89znkn5k0duwsksr2xuzke",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "50696660699"
          }
        ]
      },
      {
        "recipient": "gonka19sftyj72xf8g4kulg7jngvfacw07a8yu0yrjrm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "50296636363"
          }
        ]
      },
      {
        "recipient": "gonka1n3hh2ysxeg37hus7txur32qvxnkmx20fpqfqyr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49854734345"
          }
        ]
      },
      {
        "recipient": "gonka12kqft8tme0z5zm6skx8zwja7aq8knqc0udfcwp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49596016899"
          }
        ]
      },
      {
        "recipient": "gonka10009skl232h4c94st5ar3j3c2e34cfk2cpgrj0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49529511304"
          }
        ]
      },
      {
        "recipient": "gonka1275py7sglqhuyqzmzmdgmpfz9mxsthp8cayjkt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49381058895"
          }
        ]
      },
      {
        "recipient": "gonka1000hqfkcp3cs0fq4r78vvpkjlv5n4x4sdgcv7v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49375333358"
          }
        ]
      },
      {
        "recipient": "gonka1000xmydnfvphwy4n5yww4ex6nwk9mqslf2gnhs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "49347000732"
          }
        ]
      },
      {
        "recipient": "gonka1x2qapwtlprmlcxrdtvrskswuznn8v29r4se5tc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "48764873138"
          }
        ]
      },
      {
        "recipient": "gonka1kzhcxdkfdkdyzvl3sdp34yrwkfngdhjwrmua03",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "48442213992"
          }
        ]
      },
      {
        "recipient": "gonka1hkz4qdpl2z4zvlyt6mxfsx04yxfp7sjhnyu2xn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "47842380548"
          }
        ]
      },
      {
        "recipient": "gonka10008pmwrke48xh42dhe0ul0mm0mhhvz6ta9srs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "46976792533"
          }
        ]
      },
      {
        "recipient": "gonka1zw680tan4k6uwklyq6eedmga8ew85ys4arqkdg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "46885742385"
          }
        ]
      },
      {
        "recipient": "gonka1nm6gfclrfgtf7j56pxpk07ywpazl92puma7a2g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "46821448184"
          }
        ]
      },
      {
        "recipient": "gonka100009u7hegukxy5ne3w6ycfleaj7uuvh2juxqd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45998425495"
          }
        ]
      },
      {
        "recipient": "gonka1m8f37e29m7lpvycx5u9dzxp89lzqu2ghfhumw4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45932814256"
          }
        ]
      },
      {
        "recipient": "gonka1slnscxc26qm7vvpn5qs9yzq9n0l82r4ywkl054",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45861564016"
          }
        ]
      },
      {
        "recipient": "gonka1ym8g5f34h5zu4p4d4ldjnycfkty9qxpmyx5a3m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45641991851"
          }
        ]
      },
      {
        "recipient": "gonka1qzmhx83xnamk0uqup3lxpf2te9karrwjm9cjh7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "45410751244"
          }
        ]
      },
      {
        "recipient": "gonka1nplx25jwgvg072v4a408vs4xcevceumd04khx5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "44230778694"
          }
        ]
      },
      {
        "recipient": "gonka1l42zhzv3hy6d3y88aq37mdgux4u9crd968v9s4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "44220485796"
          }
        ]
      },
      {
        "recipient": "gonka14a7gpyhushhjhdmwn6dw45tfypaxyeks2kpqtd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43804495764"
          }
        ]
      },
      {
        "recipient": "gonka16jcz67lj4683hn9ky6w07z7qx2ls5vzgqtc3ey",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43733608497"
          }
        ]
      },
      {
        "recipient": "gonka1u94lnzwgv84xmlu5yhm27pt9qelh0xxay434rn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43657912074"
          }
        ]
      },
      {
        "recipient": "gonka1t90v237jp5zmw5qu3cmja30nvc9n7t0wstq4vz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43355126381"
          }
        ]
      },
      {
        "recipient": "gonka13t5wu88fecl8uts96p2gl9xxrta0kavrm2tpfw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43317278170"
          }
        ]
      },
      {
        "recipient": "gonka1q7sm2pxvn6fauhtvaqemww8pjpauc3rxqkdl6h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43184809429"
          }
        ]
      },
      {
        "recipient": "gonka1g273eq5mzhlmd6au5wsm3xymhqhphcer93dtpa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43146961218"
          }
        ]
      },
      {
        "recipient": "gonka1zu2y7jyppptuzgute0ftldhpjl6uzdrduh8xcu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43090188900"
          }
        ]
      },
      {
        "recipient": "gonka1llw9eff2va8jdt2z0wsy470xag4f7nlhazm4cy",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43052340689"
          }
        ]
      },
      {
        "recipient": "gonka14u7kt72elx59t45gexkkz83a78cfr3vt5976sq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43014492477"
          }
        ]
      },
      {
        "recipient": "gonka1mh2mjta097tak0ak29d0awd3esy7lkwsnxqc87",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "43014492477"
          }
        ]
      },
      {
        "recipient": "gonka16l5sg48x82jqn9am9us6gug43vj3eg40cxf5uw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42976644265"
          }
        ]
      },
      {
        "recipient": "gonka10k9lnnfq0m73dcunyskt6yhccvw9xyzajeujcs",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42957720160"
          }
        ]
      },
      {
        "recipient": "gonka1dfzzlu0v33hhw0uqyxa665hjdddjvhc4ktzkm3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42900947842"
          }
        ]
      },
      {
        "recipient": "gonka1f9zjwwe5dgstuk4y9fkcu5kdmdx68r5l4wvvek",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42768479102"
          }
        ]
      },
      {
        "recipient": "gonka1hm9s72e0ampva68rvtz57n7d3gp3dxgs37mdge",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42768479102"
          }
        ]
      },
      {
        "recipient": "gonka1qw9ezz48getxr5y3xcwuawyc3l3syk2j7520ap",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42579238044"
          }
        ]
      },
      {
        "recipient": "gonka1f5gtxpge7xn85nh230dwcg6qvz7cv8h74h3mha",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42560313938"
          }
        ]
      },
      {
        "recipient": "gonka1jm9euh70xtv3xg7jpnqwvclqtwwdxm83jucuj2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42560313938"
          }
        ]
      },
      {
        "recipient": "gonka1j9drlddzf50vmnk85cep0n4c5shca8n84t90tz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42427845197"
          }
        ]
      },
      {
        "recipient": "gonka1hfum2nzy80k3uq86nla97a4w423u0zh26axfxt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42424052467"
          }
        ]
      },
      {
        "recipient": "gonka1xt7gy4ya2095jxnf9aerspw95r8h4t5mk39z57",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "42026901717"
          }
        ]
      },
      {
        "recipient": "gonka1vhprg9epy683xghp8ddtdlw2y9cycecmm64tje",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "41636379591"
          }
        ]
      },
      {
        "recipient": "gonka1x2rltnk5rggqh73xluduge4gznf2ynakkg0ma4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "41595184542"
          }
        ]
      },
      {
        "recipient": "gonka1kth9pyyalm0u0wfc7dwdwnsntaer9gmfntlgq9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "41352784953"
          }
        ]
      },
      {
        "recipient": "gonka1ks3t0r8g5glvv4um6ml2gy5dzg7l3t2xmp3fg2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "40888897439"
          }
        ]
      },
      {
        "recipient": "gonka1h360mfpkc9py7hya69mylceahm9a7hmd09et8p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "40648916574"
          }
        ]
      },
      {
        "recipient": "gonka19lvs39k8pewhh2ecjp2t8ey5xpeac46jvtlprk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "40038583196"
          }
        ]
      },
      {
        "recipient": "gonka1hatmw3tnlskh6jzkc8ds2yxvlpmrvhrz8pgx0c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "39954392489"
          }
        ]
      },
      {
        "recipient": "gonka1fuezrv0q9hslr4jjgl4cwquytxqe3drksxq6fa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "39354187373"
          }
        ]
      },
      {
        "recipient": "gonka1zmxs507rnegc0takkkarfsu4cktemhzz4anmet",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "39296624546"
          }
        ]
      },
      {
        "recipient": "gonka1uzruntzafa6pvv80gxqfcq0kl7f4vxlyw9n0g8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "38302782759"
          }
        ]
      },
      {
        "recipient": "gonka1sg2uj8u59hjkzh6qwfsgg0n0w63ux35my80h4a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "37153182023"
          }
        ]
      },
      {
        "recipient": "gonka100070ewvrcraax995yd78cm0nraryzp4hal3hk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36874808119"
          }
        ]
      },
      {
        "recipient": "gonka1cpjcdc97u67m3x35hjj8znuvq37pldfsatmcd6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36854153699"
          }
        ]
      },
      {
        "recipient": "gonka14vypx85sx0qd4aajmzklhy6s0ygftf57zafd8a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36709046746"
          }
        ]
      },
      {
        "recipient": "gonka1cq9f8uc3hz39qtuf3q77r5kv2y2hy52ehmmvy6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36635985230"
          }
        ]
      },
      {
        "recipient": "gonka1ax52nxfepvshvatstyd3t3v56feaph24xzzf79",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36609116979"
          }
        ]
      },
      {
        "recipient": "gonka1tj9573sdggg2s9ysq8ec7me8xactn0a4kusqaa",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36287326427"
          }
        ]
      },
      {
        "recipient": "gonka1clm58yldg7zp7dmuwrqyh4quqt339qr3q8fajm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36201014737"
          }
        ]
      },
      {
        "recipient": "gonka1equqcel7hzlu07ekt7tep62yh23wp0cc2ryqyr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "36063803320"
          }
        ]
      },
      {
        "recipient": "gonka1wn9aqvsgnl7zdf4qqndczawav7a22gtq23qax0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35946029498"
          }
        ]
      },
      {
        "recipient": "gonka1362yedf9k0xpce8y30xg4g4e2mmgvstaf856qd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35860557521"
          }
        ]
      },
      {
        "recipient": "gonka1000zfcrzdjwwucvs9k2wuy4j5ecj69q5f4v57h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35723100105"
          }
        ]
      },
      {
        "recipient": "gonka1aevup75mz4q3vd89ljkqjlrkxvfpwk3dtvtvq2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35621686765"
          }
        ]
      },
      {
        "recipient": "gonka1zvuzj7ya9zafw309prasd0r4jhykf47mhcpp3x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35304088198"
          }
        ]
      },
      {
        "recipient": "gonka1a2hgufj4f8d307cfa8n4kc8xts56rtnvsxydkz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35301237878"
          }
        ]
      },
      {
        "recipient": "gonka1fnmyrkw6qta9uqn4q666c4d8k2vj3ves68rt38",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35296092668"
          }
        ]
      },
      {
        "recipient": "gonka1gwakaz7dzpay0e4at7jmj0mrnqwjex6kza4dlf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35279872145"
          }
        ]
      },
      {
        "recipient": "gonka1kch7y24sjux5s7qd9l9j02qzusk33xeqwyz0kc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35208000415"
          }
        ]
      },
      {
        "recipient": "gonka1h9axtmze6nqeeh9azggrk0k2qcx8lz2shd67jg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "35161574671"
          }
        ]
      },
      {
        "recipient": "gonka1m3nnusrecvld0jwueulywqwq0wa0tp7uav2n39",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34979570001"
          }
        ]
      },
      {
        "recipient": "gonka1cn7jka3lx0ex0dxwdcfeaxkqfjl2as080mx90k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34811978339"
          }
        ]
      },
      {
        "recipient": "gonka1qswp63txcftfdcgcle4lshkly0nmmlfr9ecj8r",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34785029208"
          }
        ]
      },
      {
        "recipient": "gonka14q3s4vmmlukl936q7e4asuwjnakv7u59hsvuwm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34699810342"
          }
        ]
      },
      {
        "recipient": "gonka1jyqp04yrjn8vdwqwkuwfd8nqal4d4vr3lpdyuk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34678286219"
          }
        ]
      },
      {
        "recipient": "gonka1jvp4r2dx3t0d736fmxy5ncgwp0w3kdy063m5ps",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34608772474"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1xuk3ganuhygvpge340sfepuwlr89s50fytlx2p",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34550836403"
          }
        ]
      },
      {
        "recipient": "gonka1t0gevkpnxe8000ke344zuhf5ljwefmdxnfzp0g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34441986746"
          }
        ]
      },
      {
        "recipient": "gonka1sl8fmjg6glvq4gl9q9u4dyek74e2lzj2ucua5g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34373143271"
          }
        ]
      },
      {
        "recipient": "gonka19w5vy2z5gz9f4jr76f8uz09023wz2snycaty05",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34354165145"
          }
        ]
      },
      {
        "recipient": "gonka16jw23vytrm9cw93s2aea6s4g6f2zkrg6dch6wm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34270642651"
          }
        ]
      },
      {
        "recipient": "gonka1fjrq7m6xy9wpmm88vr63d08ps8dt9em38lhq08",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34243443664"
          }
        ]
      },
      {
        "recipient": "gonka1e6q0zgndr833egu2050lqqdg7tg8av62duv6em",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "34053173676"
          }
        ]
      },
      {
        "recipient": "gonka106wrpdwkuudnxdm0lwzw2zharr8tfx7ug07p9f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33837315554"
          }
        ]
      },
      {
        "recipient": "gonka1dqgcdz94x42ukcfmy6crj55a0j2qucsaecx0j5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33771096244"
          }
        ]
      },
      {
        "recipient": "gonka10gj5lnsxalcwzeve04k2pdzhx2nrlqp4hkrevd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33752736179"
          }
        ]
      },
      {
        "recipient": "gonka1a357vdludl6kpmx0c7cstf3vc0muu7t7ltw8sd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33655742883"
          }
        ]
      },
      {
        "recipient": "gonka148eld5kxu6k867pz6yxmwps0kpy7rdxg2x2xau",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33642299445"
          }
        ]
      },
      {
        "recipient": "gonka1e9muhlte58rwqrr3493qxcwcj8mqrg5azxa6v4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33452672982"
          }
        ]
      },
      {
        "recipient": "gonka1cze6ecxhaqxmls39l0kwxad50x2skqmk3hswlf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33330881406"
          }
        ]
      },
      {
        "recipient": "gonka15g9vxflt3q92w07kcw099zjtc3lft9vwtr254x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33274192458"
          }
        ]
      },
      {
        "recipient": "gonka1j2g3g844qspgnjjrtmcrt55ssg4h6akdt4f66a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33264959641"
          }
        ]
      },
      {
        "recipient": "gonka1yw3ggwwftvp2u3vt9l5hcyqftkd05nu4j3h7sr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33206286702"
          }
        ]
      },
      {
        "recipient": "gonka1t4jkhfkwexdz6rm95rdd9qg2905uwd59jc7yyt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33195596171"
          }
        ]
      },
      {
        "recipient": "gonka10qpuqx5xcp4l4yjfh49gdcedgjsh3eazjm470v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33112451957"
          }
        ]
      },
      {
        "recipient": "gonka1w2pxkv4v6r5h6sdvges287l2g5rsd3r4x77080",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "33054621263"
          }
        ]
      },
      {
        "recipient": "gonka1vnmmnq4x9f7d3kume6xq2fh8x3mdye25gclzln",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32894864872"
          }
        ]
      },
      {
        "recipient": "gonka1jrwj2hqjwy5ulgkpdsdv6gwch7x4alnj88wmm5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32889996241"
          }
        ]
      },
      {
        "recipient": "gonka1j3xajqgg0mu9lvfu320mknu736nl0ltmeeqje7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32859737836"
          }
        ]
      },
      {
        "recipient": "gonka1r4cynx8smndx0vc3j8h0x8ld8h9wyzzs73cxye",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32787729371"
          }
        ]
      },
      {
        "recipient": "gonka1dn2gwpylkpjmxhgpyp6vfwqp5awydtguck5wc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32775299091"
          }
        ]
      },
      {
        "recipient": "gonka1evnq82x3j2mpf9a7mgrtuav2r2v635q7ekt96g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32774603729"
          }
        ]
      },
      {
        "recipient": "gonka14hruf6ljltha9yklfgpd0s8jleyc3wdraatfre",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32768119221"
          }
        ]
      },
      {
        "recipient": "gonka1nfammd4gwrde0jhn7w0tfu0228a5jfmst76t34",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32744316972"
          }
        ]
      },
      {
        "recipient": "gonka122yzg0agje5a4nq8spx2fwe2cye79x7hz3shgl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32701398221"
          }
        ]
      },
      {
        "recipient": "gonka1mklzy8yt48wkk7qrgz485dn995zkvfmjy29nfz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32625393668"
          }
        ]
      },
      {
        "recipient": "gonka1xcvj6xlqy7p7fzyne5jqrnz96fa4xfh35vymwt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32621269459"
          }
        ]
      },
      {
        "recipient": "gonka15lxz9w7m77dr04dxv7smxmc4xl2vr4klu2gclf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32567168832"
          }
        ]
      },
      {
        "recipient": "gonka1gum47e5sn43ughhktw5a46f7rc6cs2s08tpl69",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32519583467"
          }
        ]
      },
      {
        "recipient": "gonka1neug285zahkpplsfmgrhnkmjjwzalk3z88uekt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32457360602"
          }
        ]
      },
      {
        "recipient": "gonka1p3jfqqnjuu20zyk5t5d9xhemys2z7zxrln5vv0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32452798094"
          }
        ]
      },
      {
        "recipient": "gonka1gg2jwjfjf22gda82gm947mjs8z0gpg9tk2eh3m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32400210330"
          }
        ]
      },
      {
        "recipient": "gonka1mxa996t7rjsuj8l7g82qfwcgy5yed5ckf9lr5k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32365494850"
          }
        ]
      },
      {
        "recipient": "gonka13uuqfsenjazwu6am5fctzscar364s240zek5st",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32363472008"
          }
        ]
      },
      {
        "recipient": "gonka1pwumgsfldkzspvpun6rgty0evpz47l9mwa79v9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32361902785"
          }
        ]
      },
      {
        "recipient": "gonka13vpvregum5amwn0s0qyfac0cdngxc2cq3cp67n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32292448899"
          }
        ]
      },
      {
        "recipient": "gonka1hvat7x6qspwh5vw2pynwcdh57kc6xjl8g67ljx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32279098218"
          }
        ]
      },
      {
        "recipient": "gonka1lp3q5zammhv5a7fmn5u58clz5k7wr0205h6llk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32235369089"
          }
        ]
      },
      {
        "recipient": "gonka1sytjktet2reklks2qk32f2pm4rrah2l0lm8c0c",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32218931896"
          }
        ]
      },
      {
        "recipient": "gonka1x8pupvvcgcn00kguy9umycj98qgqehwlxt6l93",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32184179555"
          }
        ]
      },
      {
        "recipient": "gonka1xcjc32p5g72gc4tjxsm890star2l7w2g8n67w6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32110065428"
          }
        ]
      },
      {
        "recipient": "gonka1urf86dzpmgx44afh32ug7yy3x6hw86gpm9te00",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32098302598"
          }
        ]
      },
      {
        "recipient": "gonka1jmynyvawnx9jlwd6he7q8hdltpy2dv2tz74daz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32080961460"
          }
        ]
      },
      {
        "recipient": "gonka1ta39vdtx4qmlwpvmpjyajn5yulflf0ye2nu4m4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32078160185"
          }
        ]
      },
      {
        "recipient": "gonka1lnus3x4dy0ze8naktrldft5edx4e36qc53yxjf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32045279321"
          }
        ]
      },
      {
        "recipient": "gonka1zqxg52qngwtgzgnrvljdwcwt9q0jz9r2djkpyj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "32037212078"
          }
        ]
      },
      {
        "recipient": "gonka1m2rsvln78rv2rt4m0ypvzmg6z9pm803nef55k9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31953104138"
          }
        ]
      },
      {
        "recipient": "gonka1m3hfvjy92ewcvykqkk69j7kgkhffwxw0n8q0an",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31937771492"
          }
        ]
      },
      {
        "recipient": "gonka1y6g6xx6lyp3gdnyq7k9tm9fa7ykzjdx68hyzpx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31933368965"
          }
        ]
      },
      {
        "recipient": "gonka1mqmvutyh7h87fgw6k246c4q5n0xjjfn3vmqupj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31856310730"
          }
        ]
      },
      {
        "recipient": "gonka1ntlp35e8cyylh5fjmlzt0qvkhyjszsuwngd6ka",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31832976398"
          }
        ]
      },
      {
        "recipient": "gonka1y2e6vzpws7dguken363g9zfs3835l7k3m2p8x0",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31632833215"
          }
        ]
      },
      {
        "recipient": "gonka1scl6c3zk73p920m83r2lndljprz68rjepez6u3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31613895044"
          }
        ]
      },
      {
        "recipient": "gonka1m3twars04gxy3dtxwjrvz4s7x82ljx4y35hmpt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31587952243"
          }
        ]
      },
      {
        "recipient": "gonka18ulrvu3qfvvtq3s079dl2dwql2rev66zmgjk97",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31545402924"
          }
        ]
      },
      {
        "recipient": "gonka1py2eckpy6nqu6uxnxzq8zdfwl533xewpca86sx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31533425283"
          }
        ]
      },
      {
        "recipient": "gonka1cx5jhxlg8mwjgl8v50h8ypcyxrz4qyh4ef20g4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31502791956"
          }
        ]
      },
      {
        "recipient": "gonka1pd4dw77pux8rz63v7wqeyx2nlun874e2l4ycve",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31501836223"
          }
        ]
      },
      {
        "recipient": "gonka1u894qk409f4rt7fta590n7fu6szsu6s8nqq0dj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31471079219"
          }
        ]
      },
      {
        "recipient": "gonka1fvw4sad9uqe75tg3q9gaj8rhav7dc454wr2gxe",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31466429934"
          }
        ]
      },
      {
        "recipient": "gonka1vmhd38lxl68lm76755u4xdxp5wqm646a2hasze",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31391271778"
          }
        ]
      },
      {
        "recipient": "gonka1qlqjyqpmmq4r3fa8tfner44z78728z8ndkgvcc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31334651104"
          }
        ]
      },
      {
        "recipient": "gonka1rs07h66nfduhnf5qg7u968zqumragmmacuand8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31134689297"
          }
        ]
      },
      {
        "recipient": "gonka1000rv0ddp9yk6djr4y29mt0gu3m4p8mg4kmjcv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "31018248930"
          }
        ]
      },
      {
        "recipient": "gonka1evsnmudxqr9lxchjj5gsxq39qk4p3tr0y9uxu7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30946574535"
          }
        ]
      },
      {
        "recipient": "gonka1g8v99pzkqhc752fvh7fkn3vxznrgrx7pdraa7m",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30652966655"
          }
        ]
      },
      {
        "recipient": "gonka1ekdjk6vfnsnn4dr8fsdeyjtg5g3c0wyp4z3ett",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30627286133"
          }
        ]
      },
      {
        "recipient": "gonka1pyvqmxs6rkv8sqpax42gkf9ffvlnqjcx0ht0va",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30537231760"
          }
        ]
      },
      {
        "recipient": "gonka1kjrvy4xme4ctepdjspjdw677nmvdwlps4hl5h8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30329750676"
          }
        ]
      },
      {
        "recipient": "gonka1apdtylf7dfskdy545zv2pxvrfja286vrl7cqh8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30297241505"
          }
        ]
      },
      {
        "recipient": "gonka1000xjetteyu7gy726vnhdxq69y3meq04gvnk4d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30257047419"
          }
        ]
      },
      {
        "recipient": "gonka1qx3stahnpknaf8lq0kzdtedtxmq965hj9tp0jv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30103611780"
          }
        ]
      },
      {
        "recipient": "gonka1000sng4u5jm7jdjnwxvq6uwmw067mvcurd9205",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30052491473"
          }
        ]
      },
      {
        "recipient": "gonka1l059p34y0lcsuudgs8ln83nt6htjnmjcccqn7v",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "30045474025"
          }
        ]
      },
      {
        "recipient": "gonka1xk4mz0avlmvzser49tfrcgsjglq4a8u05j55p6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29865175360"
          }
        ]
      },
      {
        "recipient": "gonka1mev8s38pz9u55jkg46ql6lw8xlsnvf4ggcefd2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29862700465"
          }
        ]
      },
      {
        "recipient": "gonka1qxy42sc078ut52ws06nsa5fyzcfjyx7a56lw84",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29797245460"
          }
        ]
      },
      {
        "recipient": "gonka1xec9u9kczf7jckvtxgalghsfcnk938h2ng9flq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29780634312"
          }
        ]
      },
      {
        "recipient": "gonka1p2t9xrr5qs8xxx7rayy37tjh7pvl0x4sdgnd8h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29746316564"
          }
        ]
      },
      {
        "recipient": "gonka185qz338ahgj324udxakau55tk9frygxrs8zduz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29568742112"
          }
        ]
      },
      {
        "recipient": "gonka1af4yltv435t3f2mx0qkw2mafdrkmqng05g7l8a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29348401884"
          }
        ]
      },
      {
        "recipient": "gonka122dtadquy0ayf6nzx7thg6643w7cv0fcnqssq6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29338115964"
          }
        ]
      },
      {
        "recipient": "gonka1x4wafrl70272pzg3897zzefexwtmeuyar7tsll",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29286218804"
          }
        ]
      },
      {
        "recipient": "gonka14m8tpzysrtjyew3s42mxq9u6gxz3pfacafq28k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29196937196"
          }
        ]
      },
      {
        "recipient": "gonka1uw0kpk6hcmm0sh05l27sq6m5max7pg0n2ptsuk",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29162923009"
          }
        ]
      },
      {
        "recipient": "gonka1tj5jr5439yx3juzdcx77zgyhkq53u7dtsn6vc5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29160747790"
          }
        ]
      },
      {
        "recipient": "gonka1u88dwqlx6ew6mhg0pp3wtjaf9d590w2z8706cu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29156743686"
          }
        ]
      },
      {
        "recipient": "gonka1kfsa9q7upj8wnqrkaud755y7w2vwug3pjp832h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29156126361"
          }
        ]
      },
      {
        "recipient": "gonka1nv5twlr9sl69g650apxxe0h4vy7mw6y8cx9sha",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29156019868"
          }
        ]
      },
      {
        "recipient": "gonka1e4qcqggpllj4ulsd97ha9agm2e05sd48d4lmyh",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29145312078"
          }
        ]
      },
      {
        "recipient": "gonka1cy2l9yrumllfmm2gjs9vu9wmz2qq5qnjfy6sd3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "29087280139"
          }
        ]
      },
      {
        "recipient": "gonka1wpar5p0kmn5cwwn5awzjeycgt6rkr58723fttn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28777782573"
          }
        ]
      },
      {
        "recipient": "gonka1quxrzzy8dwhzpmsdql05nqdzj3u3n0syk4r6pr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28709079143"
          }
        ]
      },
      {
        "recipient": "gonka1d3vxnhh9tm8lahmnehhwcuqy7lc72rudn5hfpg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28656347359"
          }
        ]
      },
      {
        "recipient": "gonka1ndga0ugvxa975ftycq908hrscpcnt6enzvrzt8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28651721737"
          }
        ]
      },
      {
        "recipient": "gonka1nluanlq02cg8qrwyqn2qm2zf0mmlyqdevtf66a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28621080859"
          }
        ]
      },
      {
        "recipient": "gonka1dr9jslmgk9pp3kt0twe98g3hm5cnn2z3ehpaz2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28556369016"
          }
        ]
      },
      {
        "recipient": "gonka16jp0xfvv20eg55wn2lxy298jms3g9wvtjfnkvf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28524035939"
          }
        ]
      },
      {
        "recipient": "gonka1tqr0yuykhd4j4wgzdzng46rd22c9jlfuxkz238",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28381133704"
          }
        ]
      },
      {
        "recipient": "gonka1l5v6g8xahf88pqnv3htq72c6kf792yvw3aqx39",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28359785290"
          }
        ]
      },
      {
        "recipient": "gonka1xrcdrdjy0s0e5nhy6nw3tcm9vrzn347qtct4p2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28330276533"
          }
        ]
      },
      {
        "recipient": "gonka1v8z57yg47n8h4zveyj4cdpn0ll8k9zpcm7egkv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28226744290"
          }
        ]
      },
      {
        "recipient": "gonka1usa7alwmkwrvsu22fg4p8k2ftan35glprkkx4z",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28140172307"
          }
        ]
      },
      {
        "recipient": "gonka1rss07hzdm9d3y45fg3s3rnxjgzs26yt0h7khs6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28114972205"
          }
        ]
      },
      {
        "recipient": "gonka1wjxkarkm69harhu6h77n56slpqmjg6ygarf4tl",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28060817332"
          }
        ]
      },
      {
        "recipient": "gonka1cx4dkft2kzdzfjcuale2lw5cqaptdzgahwrj90",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "28035258544"
          }
        ]
      },
      {
        "recipient": "gonka10ejjacwvwma37rn8wrf3je7gt8u7lulu7vh8ly",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27926968729"
          }
        ]
      },
      {
        "recipient": "gonka1h6829d8eykrqgev9jr630htpze3j220er9f2ag",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27921982770"
          }
        ]
      },
      {
        "recipient": "gonka1w50e3hn86mt8gmaknecnr4mez0j94vlw04lcjq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27903755847"
          }
        ]
      },
      {
        "recipient": "gonka1xlvxvzec4n4xn8mjyj88jrg7zlkmfqy9uglucu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27739201757"
          }
        ]
      },
      {
        "recipient": "gonka1wrcr9gxu2r94chjsuk3wpcqefsv7ts0rnc94ve",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27727239454"
          }
        ]
      },
      {
        "recipient": "gonka1s5ysllxfjd9gglayqe3zpqfzsr4juq9ztzr78a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27630256085"
          }
        ]
      },
      {
        "recipient": "gonka1c8m85uzdz43j9k9539z7zsn4hp8k4qu9qc6cux",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27627053790"
          }
        ]
      },
      {
        "recipient": "gonka1u9832k7znn5k4an7a9ad8nmej0jswc7ep20q3n",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27543558063"
          }
        ]
      },
      {
        "recipient": "gonka1sw7d7r42hqwgxz4ln2x4p4pjqxgejwqnxxzj3f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27537076467"
          }
        ]
      },
      {
        "recipient": "gonka1tpvcpcmmqcku5g53tv2q4wehgqw3nmeq3jk4vn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27513731840"
          }
        ]
      },
      {
        "recipient": "gonka1ut2k5s0jgnwx09nrkzvuprcd58m3afumcv87jm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27303988288"
          }
        ]
      },
      {
        "recipient": "gonka10003spukrualhl3h80k9x5m9vrmvlmp8kf4t4w",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27272106213"
          }
        ]
      },
      {
        "recipient": "gonka1nad4h437q7zl6nmwvuxzh9g73vkm5cdymxvuqp",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "27260782735"
          }
        ]
      },
      {
        "recipient": "gonka1z25rl5qzdeyn5hc6ktnzhpm09q2devk2568pql",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26803751077"
          }
        ]
      },
      {
        "recipient": "gonka1q0r6nmh849xatx62cd09axnx4et4egu4z7n7jj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26667340407"
          }
        ]
      },
      {
        "recipient": "gonka100092zwvcksslturgx39lzwy6ztjxuttt3spej",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26561829616"
          }
        ]
      },
      {
        "recipient": "gonka1679j5jww67exhkzdvsdw0n7ak7ukyszhy0mny6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26427638108"
          }
        ]
      },
      {
        "recipient": "gonka1clpf7wtd8p333p20z3caasxxyru6gdqwhzuun9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26422116370"
          }
        ]
      },
      {
        "recipient": "gonka1yaqxj5hxmme0q7m2wutngne0fdyaajv83p558f",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "26232511177"
          }
        ]
      },
      {
        "recipient": "gonka1fc50lzgcdmrr569grw2sflk7m8ew9ptrqzfru6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25852031521"
          }
        ]
      },
      {
        "recipient": "gonka19k8devnfgkw5ftgsynjrewp4hcwnfph3ynqzfz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25832387144"
          }
        ]
      },
      {
        "recipient": "gonka1n5r055hu5tr63rgqs7xg4d45ar8q6yy3qdhn04",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25418754091"
          }
        ]
      },
      {
        "recipient": "gonka1pks9m29wqac2kxdj8v8acq58rjshh6u8y2a772",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25368378661"
          }
        ]
      },
      {
        "recipient": "gonka10r7l6unulyg0wtk8kl980k7fpvjskxuxdtnt7t",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25228485721"
          }
        ]
      },
      {
        "recipient": "gonka1yqpl6vwwyzkde0ngsclghy7dzyau0mjja3gva8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "24967799828"
          }
        ]
      },
      {
        "recipient": "gonka17ry2rgtktp9f6etejw4ls2dnagrctxqvlu7e9k",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "24660387802"
          }
        ]
      },
      {
        "recipient": "gonka1lzngx5unw6qu7f97zkq6wkvmk5aze4quwn7rnt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "24047476336"
          }
        ]
      },
      {
        "recipient": "gonka1k9ser0a6lr23rqt843z6w0e03us4lp6af546fg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23595720321"
          }
        ]
      },
      {
        "recipient": "gonka13jw6k5lleqepjyjsm8r4lhrfnn955h8wrexdz2",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23566377466"
          }
        ]
      },
      {
        "recipient": "gonka1g47tma3ruze3dtk36ru97pcn6yp0ffcyws5dr6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23474900146"
          }
        ]
      },
      {
        "recipient": "gonka1u5t8ue2699e9z92kytnxys2l0eehywsxeqvnnx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23449857585"
          }
        ]
      },
      {
        "recipient": "gonka149c9zggn4su56mrasyrkakk8apcpuz23sx35eq",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23285172476"
          }
        ]
      },
      {
        "recipient": "gonka1h583klq89w5m39tt832clppkfx807av7m07656",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "23001560992"
          }
        ]
      },
      {
        "recipient": "gonka14dkhe6rhy2nq6snmkp2ssnaesumsuwctlmrzcn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "22218014068"
          }
        ]
      },
      {
        "recipient": "gonka13crxlqch46e2jdm6uq03g8wsxndqkpdgay6j3u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "22005384622"
          }
        ]
      },
      {
        "recipient": "gonka1nc8nlx0dd5uhz82t3fyxlsy4d5n07fw87mrv8g",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "21592621870"
          }
        ]
      },
      {
        "recipient": "gonka1j4zdyxve2f9fkj8d2nx2cvg09wv67cy7xucm0h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "21529927723"
          }
        ]
      },
      {
        "recipient": "gonka1njzjqpx6t4jwe9t0fu8vtzn5cj5xjlaussvctx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "20936569149"
          }
        ]
      },
      {
        "recipient": "gonka1ksz9raj0yvg7wxdfhuj5474lmjpkzkphu0jw27",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "20908935725"
          }
        ]
      },
      {
        "recipient": "gonka1au034ld8fsrvtyxpzxx8nnnqe5kmhe20lmhuwm",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19688669380"
          }
        ]
      },
      {
        "recipient": "gonka10000uv63da0ee5drk26erkwrvcmpmj7kg6kw48",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19682731338"
          }
        ]
      },
      {
        "recipient": "gonka1sq6myvv8r263v4ll5l3ny790nsg5s4507crtqr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19238314261"
          }
        ]
      },
      {
        "recipient": "gonka1cxml8gqycch45s3l54nhmy5usfg2ughrzq4kvx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19235354950"
          }
        ]
      },
      {
        "recipient": "gonka1llyscnv8vdflufpm8j7n52macpd3s6kt73uusn",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19145554351"
          }
        ]
      },
      {
        "recipient": "gonka1aqjsdkgajzdzxlyru3q2rc9eqduyyw2qdc2g3q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19094744887"
          }
        ]
      },
      {
        "recipient": "gonka1tvjdvlf3jmc48ckycguvdvlepgj7jgx9q5m2aw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "19056503512"
          }
        ]
      },
      {
        "recipient": "gonka15hc8eqp4axp7lztjuk0y5z0af6drw5k0eltrue",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18671721349"
          }
        ]
      },
      {
        "recipient": "gonka1e2rnawlpqumhjgmkqwjkyeyhfnsgaxqdelmwqc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18515753485"
          }
        ]
      },
      {
        "recipient": "gonka1zjajt7pt4tx0djf9r7gksur320gug5e9ymqkaf",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18468775368"
          }
        ]
      },
      {
        "recipient": "gonka1velxhp2knfmqa2406rvwygex8j9fr5d8vd8q3u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18462078890"
          }
        ]
      },
      {
        "recipient": "gonka1t8r67ncy50g23sz5xlal9hahnq72ej25jd0nrt",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "18173527129"
          }
        ]
      },
      {
        "recipient": "gonka1d8v8s56a27wrjc0gfj4c0vafq67j2ddhr7n5k7",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17733795714"
          }
        ]
      },
      {
        "recipient": "gonka1v5k8fqqfc0v798gm8svcv6tczppvegsetw4mfc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17582019223"
          }
        ]
      },
      {
        "recipient": "gonka16g6lr5tzelh4m66gxf5hlvcjf0drcwnyse7yau",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17495597361"
          }
        ]
      },
      {
        "recipient": "gonka1e8d0gt4d3u565208jjn035a6h3nvxzwtc4w8j9",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17282570667"
          }
        ]
      },
      {
        "recipient": "gonka16th7hk6p6z9vy02yvt56mtx3aqj78zaxqgka4a",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17247968332"
          }
        ]
      },
      {
        "recipient": "gonka1crsq8zatznue5t6mw4ezrgvw4rtre2paw6lfs3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "17057302371"
          }
        ]
      },
      {
        "recipient": "gonka1cz5pcp5wfnkkahasj9vge9snpvl8ayz5nvu8z5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16858670071"
          }
        ]
      },
      {
        "recipient": "gonka1eqjy6gy8vapf3xtukyrcva0cn952m07sntnlzv",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16690841039"
          }
        ]
      },
      {
        "recipient": "gonka12u5pjkvehkhzky5s0yn3j0teseqa2wk3m26aq5",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16519802104"
          }
        ]
      },
      {
        "recipient": "gonka1nu5tnluwfc6e0m9deyaht2mj0t0tluap9t424s",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "16109548769"
          }
        ]
      },
      {
        "recipient": "gonka1qdulrz55xwma52j8xtmw09pgg6h5pena004s3q",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15992987647"
          }
        ]
      },
      {
        "recipient": "gonka1hp35n496dgnhfl98qlhhzvq5zema6zlcv8slvd",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15872119095"
          }
        ]
      },
      {
        "recipient": "gonka18jd4my9aae5jc3gp8sjkxtt988ctazxwcu00zz",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15809776995"
          }
        ]
      },
      {
        "recipient": "gonka1f2vks2fy4f3gvdmhgemlzygsmwgj4uwhr3eq87",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15665265795"
          }
        ]
      },
      {
        "recipient": "gonka1mvjsdf8cnxwx94umn4ylfnd6n9mjr062z5z2mj",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15665265795"
          }
        ]
      },
      {
        "recipient": "gonka1kmwyjt6nx29k72jtvgdeyduk7mvgra859utwr6",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15521495000"
          }
        ]
      },
      {
        "recipient": "gonka1vlcd8tr2nh5x6h4wl9vacpzucpp9a2p9rv8c57",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15505364916"
          }
        ]
      },
      {
        "recipient": "gonka1xxt27tswyf3aevmrh4g9w6pxhgvm5rhpcah0f3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15453041804"
          }
        ]
      },
      {
        "recipient": "gonka1fvyenm5ms57hmyze8yl659c8ljg4r89nlwap9u",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15416153987"
          }
        ]
      },
      {
        "recipient": "gonka1swxxjxn2gyyjxur62ppty5c8uaa9m8s8tvajfx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15396149423"
          }
        ]
      },
      {
        "recipient": "gonka1du3ra0wra9l7d8uqctdrdzneufpw54k3rngjme",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15380717791"
          }
        ]
      },
      {
        "recipient": "gonka1rd09mzfck3m3nfz3mhmlt6ker6ru2dg2ryhwkx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15359318274"
          }
        ]
      },
      {
        "recipient": "gonka17eha2wcrge8zp36tn85ywgx7dqmwu6hux3wqpu",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15245298006"
          }
        ]
      },
      {
        "recipient": "gonka103w3g3q88yfvcaewfef0l4gmlsjhykdz76wxav",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15233953411"
          }
        ]
      },
      {
        "recipient": "gonka1xteg3zgysvkvfl4lzs5gwxpkgtx0qra6m90jv3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "15057878015"
          }
        ]
      },
      {
        "recipient": "gonka12ha2hfpkjqcs5qgkfl5symtuws9k5rcx0qeuea",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14869979963"
          }
        ]
      },
      {
        "recipient": "gonka1q8a0m7llx9vwpxlt9a4khn9t3d5wgfwcr34dyr",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14714689688"
          }
        ]
      },
      {
        "recipient": "gonka1mmd53mj5u5uepcznq3u4apyc8l7rg9g0d0ec6d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14662835696"
          }
        ]
      },
      {
        "recipient": "gonka1se5fl8amfchfdy5sf4qzxrd7tuu7vua9aphy5x",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "14011977229"
          }
        ]
      },
      {
        "recipient": "gonka19c58vpkdx4gyh6jqzwuhdt7mky534c939fhqg3",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13868650238"
          }
        ]
      },
      {
        "recipient": "gonka1qtd6sqrfhqlfzl5guvq4rh2jduayekf8sx7vze",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13807478913"
          }
        ]
      },
      {
        "recipient": "gonka1e0x4rzdmgcxh4a6e0vz7rncgudvvc06kf3tfpg",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13644783323"
          }
        ]
      },
      {
        "recipient": "gonka1ch7c2pseksehq76xpm9ghfd98ccjxqf7e698h4",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "13588546573"
          }
        ]
      },
      {
        "recipient": "gonka17u6cwzx6f9jkngqllyw4z7fylwyymgvgv6gkj8",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12545963620"
          }
        ]
      },
      {
        "recipient": "gonka13xpjvala86d3y6jdjpnfk56ptjawq29t4gprtx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12189951247"
          }
        ]
      },
      {
        "recipient": "gonka14htw7ph065xeugpwhcsqnvmemfpluhldrvzx6j",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12056464578"
          }
        ]
      },
      {
        "recipient": "gonka12u0uyuexgd37yexwxgwljzstgunaurswguehkx",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "12027960359"
          }
        ]
      },
      {
        "recipient": "gonka16n8lkh7qtyme055xjshfmlrvts8s5ujx396s0d",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11946641426"
          }
        ]
      },
      {
        "recipient": "gonka1ye7unfm0nf6qa7awmcgxql7u2zq9fqv0g5qw3h",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11690401599"
          }
        ]
      },
      {
        "recipient": "gonka127ut4ut239agy405vmznj2jz3z57egrfuza7dw",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11617342739"
          }
        ]
      },
      {
        "recipient": "gonka1yuhp76axp2uvnflmlhjch2cmqcp0xf7595zklc",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "11247620300"
          }
        ]
      },
      {
        "recipient": "gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10338358934"
          }
        ]
      },
      {
        "recipient": "gonka1uf5cg7ef0ns6877nl27y0s6rt06cdmn40k5a88",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "10257214287"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/cosmos.bank.v1beta1.MsgMultiSend",
    "inputs": [
      {
        "address": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "832642933775"
          }
        ]
      }
    ],
    "outputs": [
      {
        "address": "gonka1azuz6leyh94mjyal7deprr2wpwqesr5530872r",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "9501541710"
          }
        ]
      },
      {
        "address": "gonka137kvnsjwkz6aqdlsfz5nkuh04wamt7gydgm570",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "9452166946"
          }
        ]
      },
      {
        "address": "gonka1f3qe6rwl8a8lga0atrdq7uqfu9dewl0vtg9rnv",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "9414778596"
          }
        ]
      },
      {
        "address": "gonka1fezpsxrwms4njwkskesu0s5t8wl46ueegk5s3p",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8844332803"
          }
        ]
      },
      {
        "address": "gonka1tl9ws8h8wje933ggmp6qav870s2kt2vsl8nxtg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8792952388"
          }
        ]
      },
      {
        "address": "gonka1enwgqdpwrthzwzl79xgcf936rt8n4zulnnn89p",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8721856694"
          }
        ]
      },
      {
        "address": "gonka15k9c2xzuman9mtggecwed2kpts0y7wgnnrgzvu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8704908709"
          }
        ]
      },
      {
        "address": "gonka18gm3udhlraw29z4and3yde959fmu3rs9sqm3t6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8528426620"
          }
        ]
      },
      {
        "address": "gonka1a32tfg0a3xe7zer9m3ttuxr57wdffpc82qnacq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8445259634"
          }
        ]
      },
      {
        "address": "gonka1xtzmqjwf0au4ad5m3nmdu07262vjn605uxyjtu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8292640093"
          }
        ]
      },
      {
        "address": "gonka135yst4re34z3rlfquhknqxvnaj35pjwu0mw622",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8165434002"
          }
        ]
      },
      {
        "address": "gonka1p8av4fdlefkwluhx864sw4h7nayytt6c7x9u43",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "8155197424"
          }
        ]
      },
      {
        "address": "gonka19pe5zksljpfjydt64xz5yv7jxsr3cn2tqt8k9r",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7685191084"
          }
        ]
      },
      {
        "address": "gonka1gdg70vwrtr8gmal53zzq7d6xk2exh75uh2mtcm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7672285704"
          }
        ]
      },
      {
        "address": "gonka143x3v0etsful8p4hznnltpeq8arz2g8lkrjumf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7493644311"
          }
        ]
      },
      {
        "address": "gonka1h8fmjrpth99xt8ee0wrdljfg7fpvquc9d4et0d",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7409052775"
          }
        ]
      },
      {
        "address": "gonka1w6cjf08fgm3yalqf7ytt0hz6thlhs53d2fn7j2",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7373299925"
          }
        ]
      },
      {
        "address": "gonka12x78v2mjvvtnhnfmlrezdxejecwzzgxr5wjlty",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7103237040"
          }
        ]
      },
      {
        "address": "gonka1wwx6nhqe7xlyvqjs0r3wj767xaurcucvz0npmn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "7078693293"
          }
        ]
      },
      {
        "address": "gonka1zppcd072lkwv7wxpxv5rd06kz9yf0trexwqtps",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6941440630"
          }
        ]
      },
      {
        "address": "gonka15syzg3weelezg42agd3esadaa3t4tr5hcup57r",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6602202484"
          }
        ]
      },
      {
        "address": "gonka15pfa2nj0m0yrqcynqe2zegzpnttx4tfqp46fgm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6559062334"
          }
        ]
      },
      {
        "address": "gonka1rad9yt3eyaflkhm4xpslk85ps4de2kae2fguyz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6537844596"
          }
        ]
      },
      {
        "address": "gonka19ayh77ndf2k8ps2992vf6n70emsq09ngxuvqh9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6489763866"
          }
        ]
      },
      {
        "address": "gonka1547gss5hs48tg024zg7cm3f4r747a8ed0mrgru",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6244004304"
          }
        ]
      },
      {
        "address": "gonka18dy9cn8e65kh6jy2j6v5du26tq9tkpf8e2n5uk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6174834101"
          }
        ]
      },
      {
        "address": "gonka14rv62lyedvmmghs78qc4yymdtas6rdz3wjupty",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6156917861"
          }
        ]
      },
      {
        "address": "gonka1m7df6745x0vr02pf2lr369vapfzddh3jxhawvq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6144655815"
          }
        ]
      },
      {
        "address": "gonka1qlulzskcx4n7ctlj3tjusjzl9vk5me8zrr7ysl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "6081456323"
          }
        ]
      },
      {
        "address": "gonka1vhg44vzedv5dzp8njajh8rtylxsctqr2xv5v6s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5972208238"
          }
        ]
      },
      {
        "address": "gonka16a28hafy6j6p4z0gdt7tv68e393glanr3td979",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5901353964"
          }
        ]
      },
      {
        "address": "gonka1vkh8e2uqk9mdw0ql83g0p4ge0wmqstcasulngn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5811099649"
          }
        ]
      },
      {
        "address": "gonka1s5997zeltdrwfc35pzzzznhk3908valhlnc76g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5765093045"
          }
        ]
      },
      {
        "address": "gonka18yuxmht359nlwj40cdz6dlr8nyaulgk0gv9yma",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5742736254"
          }
        ]
      },
      {
        "address": "gonka1rlf0ggajudsvxuvgkukpmg2xwd06htv4vu2ktx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5712867994"
          }
        ]
      },
      {
        "address": "gonka1xyj2jlq36rhauw7lx6zwmj26dregc7qqd660vz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5709268559"
          }
        ]
      },
      {
        "address": "gonka1j2m047a6sujxeznp7rkvq5t64k3hu203cruufs",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5390538673"
          }
        ]
      },
      {
        "address": "gonka1nv7pw7xpydpkhxs35zgu450ymhzmtck0aryhls",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5338417094"
          }
        ]
      },
      {
        "address": "gonka15xr92pc7v0jvq5aqwqt43hpvvpvs3q5229lrmh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5307464452"
          }
        ]
      },
      {
        "address": "gonka1a3pkge3g33v3zdkq7qmycpjwpulms6ejt8z00f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5264460448"
          }
        ]
      },
      {
        "address": "gonka1nccp3l8d8n36akvaper2ngzpe8a843key0n985",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5114884594"
          }
        ]
      },
      {
        "address": "gonka1y2vf9hwhemy8rkn69nmqwuf90ndk5cr3985pf9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5080696083"
          }
        ]
      },
      {
        "address": "gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5061339468"
          }
        ]
      },
      {
        "address": "gonka1z669rrm4sygpede8sqddavhsef6wc9vwjsp9wh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "5044445895"
          }
        ]
      },
      {
        "address": "gonka1ddswmmmn38esxegjf6qw36mt4aqyw6etvysy5x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4818475251"
          }
        ]
      },
      {
        "address": "gonka1gvrssnvlsj6he2lyv40y5fpdawn2xuvtldqv99",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4804965891"
          }
        ]
      },
      {
        "address": "gonka1n80jruuunhn8q9scqkuqcvsq8dz3hv03zl6sjn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4800051495"
          }
        ]
      },
      {
        "address": "gonka1pvlt0c9dqyxvxyzwf0t3q7ff2m2andsl4hakn9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4712678395"
          }
        ]
      },
      {
        "address": "gonka12znqneqlv4va4he2vz2safylpx7kj6gw2r48d5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4529478439"
          }
        ]
      },
      {
        "address": "gonka19hfr9trsvue37wfn7tpaqjlp6sdjhyzvyecyw7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4377146350"
          }
        ]
      },
      {
        "address": "gonka1zkegnzhzcyeu9m74f8907tg5ga2dyhxnfuxm0w",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4182985948"
          }
        ]
      },
      {
        "address": "gonka1ke4t935aqvya0kcee2nxcjp82vk8sa3sjs60fh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "4028980470"
          }
        ]
      },
      {
        "address": "gonka1c7fjlg6p7l0ynydyzkzzkxdwue7y864tytj02g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3966294792"
          }
        ]
      },
      {
        "address": "gonka1wuhwtgcrlq7j9yzlev73raej734a9ym4clslnr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3727207309"
          }
        ]
      },
      {
        "address": "gonka1smjq2hmma0c42rvf4epkp6tgfpy5z9cqzp3kqd",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3716196059"
          }
        ]
      },
      {
        "address": "gonka1000aqvxfkugmfy9ygfq3waq9r6q97e2yzjkspk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3695515387"
          }
        ]
      },
      {
        "address": "gonka10ham8mkawe850sk3aq9vfjvsw2nzvl63ulcuyl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3486710564"
          }
        ]
      },
      {
        "address": "gonka1k2dvwkg22kqmgh0s6xt8xuk4s4ak0k4py05cyr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3449792975"
          }
        ]
      },
      {
        "address": "gonka15fpzwc7d2z3r4y5475p6k7uqknnkj38gsus3d9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3404136954"
          }
        ]
      },
      {
        "address": "gonka1ttnyggsrxqyaqkty5uy6umak6cy2epcycmgn7k",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3403934586"
          }
        ]
      },
      {
        "address": "gonka12uttst9yzdrfjqhjanvnlydq0dms2ktaljqaq8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3359427978"
          }
        ]
      },
      {
        "address": "gonka16as27w5m0jtskdgxx6hyhhm6r3khechwcc6quw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3258925442"
          }
        ]
      },
      {
        "address": "gonka1s0hm7zhcw2ms89g2s8lsfr9s02d88yfph9p75v",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3163798107"
          }
        ]
      },
      {
        "address": "gonka12favtgswt6sw2wx8ywf6fz5jz6dl09ga3s2tpu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3140706768"
          }
        ]
      },
      {
        "address": "gonka188zesyhzwt6crz9dlcll2cs3wezput0kfren9t",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3086954434"
          }
        ]
      },
      {
        "address": "gonka1ed4dzdu86mz2jhmn8ddajdh79dmx2lqdhcdulv",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "3007115951"
          }
        ]
      },
      {
        "address": "gonka1un2c9f66mg2g6xcpmulq9tqfs3vjd7nn0ftjs5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2968246664"
          }
        ]
      },
      {
        "address": "gonka1q8pf6vaqxtnnwl896uytd0waejnypkv3wz6a94",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2921590102"
          }
        ]
      },
      {
        "address": "gonka1r9zhmnd99rq9knfzng6smasywxakw2r8ltjvp4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2921590102"
          }
        ]
      },
      {
        "address": "gonka1rtq5mhv2mw9ammge8ezlyy6z0f4yz8c0gjlkcu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2921590102"
          }
        ]
      },
      {
        "address": "gonka1xqrc7jrcx6rgv5zpngnm4yunsf5qvcmklygxn5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2921590102"
          }
        ]
      },
      {
        "address": "gonka184jz8ja5gqkr3kt98a3a4syyypwj07j0qngukg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2918969582"
          }
        ]
      },
      {
        "address": "gonka1948n747ayualpznexxchnx95pdnpu25mph804e",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2761436531"
          }
        ]
      },
      {
        "address": "gonka1vd44gk5gr8x7s6557sx6vnf4q7pn6q848qq7sl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2717813483"
          }
        ]
      },
      {
        "address": "gonka1yn43f97x8hqq66nkezwykqcddngtz4ynwlk6y9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2717813483"
          }
        ]
      },
      {
        "address": "gonka17nhm4sh9wugmrpmpdchpfv5l69n2na4q72y2ch",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2717813482"
          }
        ]
      },
      {
        "address": "gonka1u7pmx5k2s0fj37pge77vxyt2qn4ja8jjsgkl3d",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2695474896"
          }
        ]
      },
      {
        "address": "gonka1xmjrx334m6vsv32uvt0em0jzsd8zn9qfmntmy6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2564657593"
          }
        ]
      },
      {
        "address": "gonka1gkdl40hfau92xwh39updqzzrpllaqv7fjanhlm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2527572548"
          }
        ]
      },
      {
        "address": "gonka1xlskhflqewyv2uaalp4va6efmws2fudf3qxqrn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2446073554"
          }
        ]
      },
      {
        "address": "gonka18vws9s85353vl20qyx5eemfuhdq0auf749hryn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2422922586"
          }
        ]
      },
      {
        "address": "gonka1zq6edydsgjv6k34zh36td2h238wafd6p3r605z",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2411889280"
          }
        ]
      },
      {
        "address": "gonka1w4u0ylrw5sl7nczl52vfjzz8ccvgaltrnejklc",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2405998742"
          }
        ]
      },
      {
        "address": "gonka1rvpg7grgz7gdj2jgpawyc3g996hktavc4e8rf5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2401414751"
          }
        ]
      },
      {
        "address": "gonka1tsjsvfv4n3gvwrjjla0suvwz3ypm42g0unpqpk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2401414751"
          }
        ]
      },
      {
        "address": "gonka1wsrytagxfhv0kn89hnzvsp8pg4xqrxq4x87s48",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2401414751"
          }
        ]
      },
      {
        "address": "gonka1yql3sw3ptvysqgwvh6n0c2fjnyqjdd0wv4xnfn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2401414751"
          }
        ]
      },
      {
        "address": "gonka16lksjaqq2gqpeexvqg4xgux6hdtms3wnk4jjle",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2302664161"
          }
        ]
      },
      {
        "address": "gonka1yhljtdxhznktmyvzns2gpeeqr8ytzcel42amg5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2273140919"
          }
        ]
      },
      {
        "address": "gonka1xzt80teg2sx6245gt3p96qax6dcdr56f6keqwr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2271913154"
          }
        ]
      },
      {
        "address": "gonka1p45pgtzjtjaq0nqxm0a6dstyeqa3lx5dpx253k",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2263994957"
          }
        ]
      },
      {
        "address": "gonka1c5mazlks00w89uumst0ghmk0jyug24ajjrmu4e",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2256402589"
          }
        ]
      },
      {
        "address": "gonka1leq6gdxs2d7fxqg7528hkq8tk50v2pdj2pzq9k",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2241549835"
          }
        ]
      },
      {
        "address": "gonka12mwqjk8y4svymxjndzw4cxcpp09pj9c072l26g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2229759398"
          }
        ]
      },
      {
        "address": "gonka1elhpys4c6cg5k5n6093a6wm865gpyul3pr756q",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2191785067"
          }
        ]
      },
      {
        "address": "gonka1lutcrd6ylg63293aukds7pxardj6sl4pz2y2ls",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2191785067"
          }
        ]
      },
      {
        "address": "gonka1rccd6tq06vl2tq2rz9p6uxuuc8tn9878le92gp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2049597188"
          }
        ]
      },
      {
        "address": "gonka1ft0x56racya2r7asndxdrwyy9ltl993f5h7zyz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "2022244001"
          }
        ]
      },
      {
        "address": "gonka105az9lyvju6l32qvl4xkzqru4cs4xuft8lh0e5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka17f3cgvf0xd5rpafaqeugyqece62ahef2nexa9g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka1kwqlf3mrlv4zg79ffuuq3uxesa22fkdfmfr9gq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka1q5n2dyavs267z64kdljw4u8wy9y6a45sk020pu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka1qlc7kpa3lm8fz0muw54unkwxd8rwt509y5jydd",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka1qp9pyg45lagg2gnpt83ryp05emlekp95jgzdja",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1993090946"
          }
        ]
      },
      {
        "address": "gonka1lf8zrnapty4nny6l9dr66nd7xc4j4ktr6rujha",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1944133310"
          }
        ]
      },
      {
        "address": "gonka1920xc45wphxgq22kfelxscp39jcc2vnmyxpday",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1885982410"
          }
        ]
      },
      {
        "address": "gonka1m935423dlgd36w2ezsn9npyfkvufk4nxmynmyf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1885982410"
          }
        ]
      },
      {
        "address": "gonka1n3l720a7khmcx3th4xzsuttjv0xpq974ej3j6m",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1885982410"
          }
        ]
      },
      {
        "address": "gonka1slzst7ur93jz3rmakat5ygd0pyrl2nxexnwgrp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1885982410"
          }
        ]
      },
      {
        "address": "gonka1x8emnupg2gajvsmy5zdtev26n60uh59zlqznz9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1885982410"
          }
        ]
      },
      {
        "address": "gonka1l9eclck7nn4ame8zm26ahh4wd0j0v7atp9vuh7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1848732764"
          }
        ]
      },
      {
        "address": "gonka19qz97dxgwgfzedtf8yzwzy43quwlggmq33hnuw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1844957304"
          }
        ]
      },
      {
        "address": "gonka1tadzlvqgcj53nnqdlppnpxcvd98ygwp370a6tn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1844957304"
          }
        ]
      },
      {
        "address": "gonka1w4y9r7g7fzh2zq8wxydlh4x9j26casunxfdzmk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1844957304"
          }
        ]
      },
      {
        "address": "gonka12am8m49ejfg4n5sjxrjkgxjqeyv0knw2jxgzzg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka14jrd4theu4uxr6qftuddnqehg2mrcqxzsgv4n0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka18vanjpcvmnarm4t9fcdjjza3vdvnacv63n5675",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1fqd0dz7mnq47p3puhpmgzvrl7x8l2awg0tlwx6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1rkzw2my8pmadftpkpfq7qnsca9fjr573xcv2m7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1ty2k0gdcnr9qflthxcd9mvmakva7arsv8m42qz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1u6gv92fshuc2z927224jecsc5hrwps4en3hlxc",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1wua3u0ts50u0vs2hms9l6u04wnq3m94mn7whcq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1z43km02x94rryj03utuna9y3falahzy3fxl4kw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1833988532"
          }
        ]
      },
      {
        "address": "gonka1tddep45jx77myyua8se2pltqe0glmp0mcgql5r",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1813086360"
          }
        ]
      },
      {
        "address": "gonka1tdm3u8fgwdqr07l9xutal8724986c4n2v8e0m7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1813086360"
          }
        ]
      },
      {
        "address": "gonka1xp332v7jcrvyxnn20zumdfxajydak0mwxusngr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1813086360"
          }
        ]
      },
      {
        "address": "gonka1zt4tedf2rqqdu7m53f5rhpt90pakvqcnnrg6fx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1813086360"
          }
        ]
      },
      {
        "address": "gonka15llevgky75a7jknr5m0kzme669xuwrqdxex5f3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1809031774"
          }
        ]
      },
      {
        "address": "gonka1m50khzaxc3pnhqpjgn8ptlv5ws5uhexnck5qht",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1685013318"
          }
        ]
      },
      {
        "address": "gonka1rd27hnfvz44x6tjc0j355yyxhgdwdkpwj6ppwq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1679070580"
          }
        ]
      },
      {
        "address": "gonka15q3hcqdkvthz82rht3vxayfmx3u5hcq00evfxg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1r4ntslxj8f4xfmrmk939vrkknv2dfdr6rstkf9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1t45g664kkw3dhtcwgux3nvrtn9q5262ez5crlm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1tj0d67xcqhx7xv8fj96c4q0f46cdz6rx02pq8c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1wv38ew6cvmsv9t7y4h6jjdvp70k5s2mh4hhs2y",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1x3uccqp4a6kse5d2r743m9zas5khz900w67hja",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka1z8pr9dy362yvvw9c0wx3fc8w9yrgv2ervakd3x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1663454722"
          }
        ]
      },
      {
        "address": "gonka10rk42wkre2wp24m3n8u2maa4p2nm3ev5r0fwcy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1gz76l4rtf7rkg6fuhnyuq2w3letq9687pqznwy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1lmppztny6yhjcshlh5jd7484lms0hxvjpe8ytu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1m09t38h8fy20qx6896ht450j8rfmtdel6tq93x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1qfvwhm2cpz8y6ekvnqacmlgqhhjvws8ptkcygn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1u4vw85xxgvwmu4zgsy9fxd48w0x98d2hee98h6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1v6gq7sphhr6g7v9xnjl40uzlw39eay8t7vmc0y",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka1xn5rd6anmtkvdvd9hwh4d3pspxp8v458554fmk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1627117056"
          }
        ]
      },
      {
        "address": "gonka143hahlzmxj26dlcdl5552yl9futt7jahjgeu69",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1614219386"
          }
        ]
      },
      {
        "address": "gonka1g9vvr2ynjjuf2etlzg6h22dxuxkl3zphrury58",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1614219386"
          }
        ]
      },
      {
        "address": "gonka1v3v0ydfpycqygs6jlvdzv7cjp04gsk24sepr9m",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1614219386"
          }
        ]
      },
      {
        "address": "gonka1wsx8enzwl8mnwkqfghl7gwe2x930s33qnhw4qp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1614219386"
          }
        ]
      },
      {
        "address": "gonka1y69wttdm3vkadw004kmejj4c0dyae3cz25dxhj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1614219386"
          }
        ]
      },
      {
        "address": "gonka1xk0hzuxrfja57xvm0r5n43v67h3cvhz4vq656l",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1605362777"
          }
        ]
      },
      {
        "address": "gonka1zqddqel0zwzae6zfeh4dpt45d5f656yghdenpp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1593305536"
          }
        ]
      },
      {
        "address": "gonka18emzcnep4wf2kar3zy54cwl7j2j9g857q9q9qw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1589523430"
          }
        ]
      },
      {
        "address": "gonka144sh6452klgn9mp2h9yjesdfv9qy27m3dp6pzm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1574995627"
          }
        ]
      },
      {
        "address": "gonka1s2f53k0y5jydp25gfkz0rzxy3sxl35gyz5z3d7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1574995627"
          }
        ]
      },
      {
        "address": "gonka1vg0ys6nafj3ete8g5td5lyag6fc06uxx40ylcu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1574995627"
          }
        ]
      },
      {
        "address": "gonka1wmsag8tufeqxwefr8swh8v6ujy8h9z67scrxp0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1574995627"
          }
        ]
      },
      {
        "address": "gonka1jn3ldkrdvdpcruz87p65cg8yy8dmpjrmq9g2cd",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1531654714"
          }
        ]
      },
      {
        "address": "gonka1uw65v6surnyfvykqvky6wq3s90zrknr6ceh38h",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1531654714"
          }
        ]
      },
      {
        "address": "gonka1wvs7grm0vc2a3d834sksk46hdc28ypu6dm7cmt",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1531654714"
          }
        ]
      },
      {
        "address": "gonka1ym9lr260763xk06ktu2mstmtcxztn34jvce35f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1531654714"
          }
        ]
      },
      {
        "address": "gonka1fzh9xgz35ugt50z23wwcjvemrcq8mj34v60gme",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1502935837"
          }
        ]
      },
      {
        "address": "gonka1ke9m4zyygwa4cydfrmk6w9axthr84lwagejgve",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1502935837"
          }
        ]
      },
      {
        "address": "gonka1vll2z4rhell9kzwnagqzfwj3lqkkn4lvpyzduw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1502935837"
          }
        ]
      },
      {
        "address": "gonka15ayg9m2kcek8l6ent5vmmczkkujumq0alrtgwz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1502935836"
          }
        ]
      },
      {
        "address": "gonka12vq65qqgep5x2zvjxqzqtnsw2hpyz92czen8z5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1e94a7r2tn3n8ewa3mha3vjnq2dkvgt5stfqgqg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1ecercvenlsnghx4yakvdpdq2mantyh5ythhn29",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1l7p83akwkcxtksnwve23x5wp47zammznm4qus8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1lwl6qhrdqw43sqc2y4eclfrngf799rnm7mmx87",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1wfn87ruutktth7l8ne3rvhmlsscqxah09kua02",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1wzujgkw64xvz3vqttg7ktl5tlsdga7l53g6d55",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1500945892"
          }
        ]
      },
      {
        "address": "gonka1j9xwc4d02qyujg9wvnegyk3sxtl52lc6lpa30r",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1487110895"
          }
        ]
      },
      {
        "address": "gonka1pumyaaza5qtjp0k5ur6nsyzq4n93aukph6vfex",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1479023010"
          }
        ]
      },
      {
        "address": "gonka1x55dmkfh9a0meenzwwmpdavnle0lz993xj5ayu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1479023010"
          }
        ]
      },
      {
        "address": "gonka1j9eurz4unzt8g7ptk7sc0shmaty9gcsh64u6ap",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1475638662"
          }
        ]
      },
      {
        "address": "gonka17yy2ywjsdq652z275pte4rr7u3m7ujk7hzcy2p",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1c3wneuskddk3ddx45454jhwjt679gtc3anl8c4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1n7wy6cx4mf3lw3r8ltasn2uxzxylamkrl4t0kh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1qfqj3853nxm4tesryz98fz32effv9t97s9qvcp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1slww044z57zd56q629zq4le82vw38gjkzfht8s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1yh2k3mtf4wy4ddgae29fxzdrfl3e2zcat927dq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1464169878"
          }
        ]
      },
      {
        "address": "gonka1usnmdjdt2xfzyl9xll67mna8teupacwt0gx2yt",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1462431155"
          }
        ]
      },
      {
        "address": "gonka1ypsleu690v2pj7j7xeejcfwkdpk9ps7yfhdtdq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1462166420"
          }
        ]
      },
      {
        "address": "gonka1zg8sly8kpvgmtg6mapx67du83n6u93z2l4vudj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1462166420"
          }
        ]
      },
      {
        "address": "gonka1n6dhkcn2ek5yy948y487nj52hyp4mcvpxjjqed",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka1raes6xggfna8sxceh5z7slxvdzaa4x63hsdrr6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka1y9y7027gllfnx0u04s0x4nx8u5mfaurgaw57hs",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka1yxjq6h8qq5kvf86004rhmxf2edwjdgynq22l4k",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka1zq5ar3u7l6hzrxgwn9qszy54pc89k7ueqsjwkn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka1zxyjn6yuqm4e2v2wz2y7a9lhcxazc674dyvx5g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1452515195"
          }
        ]
      },
      {
        "address": "gonka18jv6tlf26fekum8zxa5zmgnz7anqunkxddjaf9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1412735200"
          }
        ]
      },
      {
        "address": "gonka1juyynkna0cwjg4xjlzuw62lk0u0jwnhuqegdkh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1412735200"
          }
        ]
      },
      {
        "address": "gonka1wzm3dmnkymnuj8g5mxne9w453ef05mteun4cpz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1412735200"
          }
        ]
      },
      {
        "address": "gonka1ylz70ycevzkv3t2s004xpetd2eqwj6ylr3fpv0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1412735200"
          }
        ]
      },
      {
        "address": "gonka1zphxd376tvtev5drq09dtnj7nfxtghw6gtewpf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1412735200"
          }
        ]
      },
      {
        "address": "gonka1442mg9djng8kvtmj5mjzenkakq4j7n3fs8tjkx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka14sdm8urd88v49ns7n6hz99chpunxjkr0w3m8y7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka16kc6rg5emg6n24pyu78a4m9p2q43tteppx4ee5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka1cw76rlm0ewnj7d90fvgyp37rav9dv5hm3mvy3x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka1eq8ptvu4mecxkdc7gj0eqzxp4ysjnz6f8ez43c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka1ha7fpwwu9st0wgyyz9ahd3xchk05nx7mtj4ng8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka1t9scyr8q6dh3xsajedllt6dn4szd06fvnqjt2y",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka1ttrglrkzc96auuaq6nrv0wdygwm7ph5887j9wr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1403533787"
          }
        ]
      },
      {
        "address": "gonka19g7jp7tcpnh9ul6gkr3kdc3lmcy55w6swvql0f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1380879260"
          }
        ]
      },
      {
        "address": "gonka1dgkjlfqrm56tr6evkydg2qkkldzancnm097hj4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1377704962"
          }
        ]
      },
      {
        "address": "gonka1e38cgywjkf4hejnf9utmpguq3qug0s5rd45kqm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1jcelp2ad2x0jf2vnyhkhd6wquug0zpd09sxxw4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1kdmstpljv33v8lz457lmj8f9g995l7ygwm460s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1l0enytn32rklk95dxrdt3v39hktxdw79trvgj5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1l0qv64xdu3dk2zzm5vk97j0drcmkus95u50gqk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1l6pp6p5hgaa69rj0eazn73f7gkawue94fq5v9g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1nkzdygk3g2p2usnueuqxyep3462350hgzxs86s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1u9a7r4w76gult5n9ysadnual9fghkc6yda60wj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1usmu5mfu8vsafvsrsvdutl50vy8kumdhv0j2x9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1vcawx5jc2hahydd9sqw30hlxyd9ppupm9ez0yz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1350159486"
          }
        ]
      },
      {
        "address": "gonka1y62nqpx6ywvshndet4806nf0wasm4959hv9fgu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1328322785"
          }
        ]
      },
      {
        "address": "gonka18anrx4l59z34te42whq5nx3xy7ftlw0ka98lkx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1328014484"
          }
        ]
      },
      {
        "address": "gonka1jxtdrqyjc52j7wm2h4ec8g7enjz9r3qjy2hn8g",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1328014484"
          }
        ]
      },
      {
        "address": "gonka1s9ecxss47vq0w0hwr72f6sdpthtasem9nx33tf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1328014484"
          }
        ]
      },
      {
        "address": "gonka1xxmpgunsrg9ayx8zejnjw8zu76czmc8fre3ece",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1328014484"
          }
        ]
      },
      {
        "address": "gonka1ws5s5jrnkle6xwe4glk59yehq4qexgamjkct8c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1312191174"
          }
        ]
      },
      {
        "address": "gonka132jlm2gj75cqyuvnnufv5uhnlmfm06jvm25zuv",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1305380116"
          }
        ]
      },
      {
        "address": "gonka167ez4nvjumd0rrk78awcvxawwmf505cwrvk5nq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1305380116"
          }
        ]
      },
      {
        "address": "gonka1hmj9lrcxt9zds40uq94gga2ps7t7x75eky6cvq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1305380116"
          }
        ]
      },
      {
        "address": "gonka1txq9e2jzdfhlnugd63u5630vqnzucwavrqnu4d",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1305380116"
          }
        ]
      },
      {
        "address": "gonka1w2d6hlurl8hn47emf59eenam99gng7j7hmafj5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1305380116"
          }
        ]
      },
      {
        "address": "gonka16lsgkqgz25fj53rtp9kgdafec37kth6nnf4an4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1291375509"
          }
        ]
      },
      {
        "address": "gonka1st5dm5ec3fl084y87wfklum6sv49n782k0tsnk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1291375509"
          }
        ]
      },
      {
        "address": "gonka16m7l3g7hr3y0r3a5wdh0wmwh9rshye44ssyssw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1288230717"
          }
        ]
      },
      {
        "address": "gonka1deyrcv9dfe5a5q9tn9k0ngv8c4p7sm3gq7v2vh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1288230717"
          }
        ]
      },
      {
        "address": "gonka1f3p6j8euk9pv9ap9trvj2eusklny4ue7ys9gun",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1283740510"
          }
        ]
      },
      {
        "address": "gonka1v559jhxth9uqj30f3k78tpd202lyf6x2h8g6c2",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1283740510"
          }
        ]
      },
      {
        "address": "gonka1vye2pcqanatat8n7haxq4ddf3wtlrdefxuxsru",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1283740510"
          }
        ]
      },
      {
        "address": "gonka1qa2dzvnva77uc2778rtvz69n27uau8jtetr4g7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1279683947"
          }
        ]
      },
      {
        "address": "gonka1ue0adff609mng4n78l4vs8vc4fgaz93xcylt9m",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1235205415"
          }
        ]
      },
      {
        "address": "gonka16dhzkyjqvqt2f6h9s9f0fx0dpqaukq5hu47uul",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1233899971"
          }
        ]
      },
      {
        "address": "gonka1287a8wk9nnd7w96ejr5qkj3a04hcf4nmtckc8p",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1226742101"
          }
        ]
      },
      {
        "address": "gonka14z0upz96hw5sd6jgw4qpmy4lfjg294y560f7te",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1226742101"
          }
        ]
      },
      {
        "address": "gonka18g789gnqf4990eel5dzgpx383t0fzdef6nmw2q",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1226742101"
          }
        ]
      },
      {
        "address": "gonka1h82jwcefsu9ur3yfj97593tlyve2jes89kyqg4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1226742101"
          }
        ]
      },
      {
        "address": "gonka1uuywlyxfddqrjgpz8u4lqevz838qr30rp020yp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1226742101"
          }
        ]
      },
      {
        "address": "gonka123vh2t9er866647lsn6kclt8lfq2l9kwy4le76",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1210440236"
          }
        ]
      },
      {
        "address": "gonka17et3ctw6t4d5ylnuc2kwc8xrlwk69y0cggzjqm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1178466861"
          }
        ]
      },
      {
        "address": "gonka169ms5ewh68ervhaxslul5cmfaavnt57nkmrvgt",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1175204200"
          }
        ]
      },
      {
        "address": "gonka1sg7amslhnqrw6qyvkdt5f6ru8kakyw5uss0mj7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1175204200"
          }
        ]
      },
      {
        "address": "gonka1wpy06qhy7j7a0zcsax0q94za5p0g9g3g2sc32y",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1175204200"
          }
        ]
      },
      {
        "address": "gonka1cp45adu29a93qp8fwqn9sqt2hyqkl8qc5hty58",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1171383222"
          }
        ]
      },
      {
        "address": "gonka1ea8zl02zfvpxlpgdpywky9za5yy0ufy7htrwqz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1171383222"
          }
        ]
      },
      {
        "address": "gonka1we6ghh9kgtm5na6wf3cyfjvj5fauuln08nx3r4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1171383222"
          }
        ]
      },
      {
        "address": "gonka1000j4nzln9sg895wqvxn8eg5yrtpvgj2hxsqyw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1169798309"
          }
        ]
      },
      {
        "address": "gonka1rmr4x8lyw76gzuyzta68gj965zfa00gzh2aszz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1151289716"
          }
        ]
      },
      {
        "address": "gonka12fdlw5g8wex6v74nd42vfhnympsz5kn8p3adh5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1cenhl8aucrr06z5wtprdpaxa0dutzt90rgkt99",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1dhn7hjn6udpyv6gkhfulnalufv4947a4e9kyne",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1p3hklp6flhdffdkwr70azcsum77fha3ecqwgg0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1s43peau7vafujfxyape603yklhdzjh2stq702z",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1xmgcpaw6n57ewn6s2fhggxaakemaaxuv4pdpmq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1130375146"
          }
        ]
      },
      {
        "address": "gonka1dzg3tnd6ygsw0tf06fcu9tc7sw3jzrwx6ftv7c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1114827285"
          }
        ]
      },
      {
        "address": "gonka1pka4am8g4atxzlgm3m6sy09uel7ecegtsp04zf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1090219613"
          }
        ]
      },
      {
        "address": "gonka10jjrlvkfkqupgudz0l603sq99y3wkt3urwjm0x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1088838295"
          }
        ]
      },
      {
        "address": "gonka174jxwp94lwgqr4nwlj5kke3z6fnat6p5dlg55x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1ek6mqw0g0jzee3gexx70nepqw86dxmknur6f42",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1mgu675kpx9fxftcs80x7sn4tdxcsqfnhes5j88",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1u9pwgk75elh6qk9ehjm38xx4h9xzt99us3meud",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1y4fvesetallc8w5srs3fdeaashzez0v2maksey",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1yvygc3csnr2c6ee6lag82wk7p2s9vss0npu7an",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1079384495"
          }
        ]
      },
      {
        "address": "gonka1amqg6l5eshydfnhlyhncshducrfnrde58rsmrh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1052725900"
          }
        ]
      },
      {
        "address": "gonka1cldfsqjcch9w892eumdhc5ru80psjt6jck0tg4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1r9e4ew3na86n2mqzwz057930rxq5yycxpj9shj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1smep2w2jmng5987qujy37ux0jf3xrj6kdy59qn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1syr9s5dha0qcanrd2jpx6f85965yde0nytyux4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1vewz77c875qr8lvr0m62wmf0lw8lv3qr94g6e4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1xj5cdd7qfpjsste7lyz8ktfj7xl5q3kjydf3un",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1051968845"
          }
        ]
      },
      {
        "address": "gonka1vev00u8gl87e22eq8zpsr8lrnmhpvk4hl0yx3d",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1022338944"
          }
        ]
      },
      {
        "address": "gonka17py7gzq2pa75eu2z0wzp9kjum20zgxxk2jrxss",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka1cur9xf76n8gvgvw608r3kaxfeamyafpw5wkc99",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka1dc645alkwumpj3fuhxg4xu6hc255w3q5s9p3rs",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka1fwyt5sz43zs3hc8k0r5cgquvss9d6aa2975pfw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka1jfs2xqkykvlpgfahslqpljr5sxcekw7s8kutvl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka1lvmvyuv982ev45srx4yzj8xa4kk63n4ecswq07",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1012832854"
          }
        ]
      },
      {
        "address": "gonka18tm9tu9rak460pjdpj6xvfeffk474h6xhgme3c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1lyc347ysjruw7hvvejekqwu0y62cq0898dzarl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1pcu4wfdv2jtpfsnhgjk4zp7d46z47928xj73st",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1qv2dwvqxt542k5ewhggm2wtcpadvzg6mzupzg8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1upq4e3ahzea8mu5mhrdptff94xru98lx47h43z",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1x20c5d9wzatlr0t69xjm05x9uemq9mnk00udfa",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1yrfq267gf5jz76m3j5sln7f5h00t9g6fmat4gp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1yukev873tps58s6rlkh6czs5rrqp2sdqw7pm58",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "1000955959"
          }
        ]
      },
      {
        "address": "gonka1t4xjvjtrr6fkw50d0mqz93004jh52x62apdlqj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "992484682"
          }
        ]
      },
      {
        "address": "gonka18qpw36ctvuea4g4ygvhlquhefc9ckglffelm98",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "989308146"
          }
        ]
      },
      {
        "address": "gonka1svytprwy050gprlvhp44nkyzfss53y07d8fnj6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "989308146"
          }
        ]
      },
      {
        "address": "gonka1x0wr4u4jnzyqsvme97zy8p2uqdl9llxf938uh4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "989308146"
          }
        ]
      },
      {
        "address": "gonka1wk44rwpyrfe3urqmepx8g7n5wh44j57ywhmzny",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "978610621"
          }
        ]
      },
      {
        "address": "gonka1rhswewu6mczgme9p87uwtyufu3px3t8vksn22c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "971125899"
          }
        ]
      },
      {
        "address": "gonka1lc6gsl33geyvknx9fl54p2rlzjxjvygwfyul74",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "951668342"
          }
        ]
      },
      {
        "address": "gonka1u6ckk5ql3c0xjvha5ll3mhv9cr047njvazx648",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "935153654"
          }
        ]
      },
      {
        "address": "gonka18a9dnx4u7z0jqf66l4uk6zgnhszhd4qs5u7447",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka19tq260hnd4y83q9m7nk6q5yc9xenesukvznak4",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka1m4hsj08wgcjnwdjlnssed0tr4umralj6p5lfsf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka1tr9v4n6v7tycc2rplnazxfa672h82sgg7w5z8k",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka1u4zpegkxj5aj3pkpvgyukh8n2cswc3njk7xf40",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka1wxgfseq4t6ph7jfrvrnjkf88424n7d93e5pskz",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "929101099"
          }
        ]
      },
      {
        "address": "gonka18d032cycta26ussz94was3us7tlwcgh4gx75xp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1grj4l6fr9uqj43tqqe6m4st7a6zwam8rznzryy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1nfz6dszuzcewxaukt7t6natedpdjptf9r7uxwg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1quj84w0dqrkk4jklyg5p0dkvvukey3lnchu9f3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1rs5hvyh4rs2f0y9ywkmwfek8r0d59tf4pvknwg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1tmngrjsrnwu3d3c7r3043wf2ml692w0pnpu044",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1u8s6vtmp79an7f7xw8hmrmvlntadf3j8na3ajc",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "922450792"
          }
        ]
      },
      {
        "address": "gonka1djk2tqcjsqqd56rfz4p5lmpwwug297zs8ygmx3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka1hkccmh2jc7c8wfs5ydtelx8x6m5957ae200dre",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka1l3f79kphpczsw4cz357cxue98gjpcuyxrczh8e",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka1u5ex4n6r7cjqkkqm4wh5khtzxaee7v52yce29n",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka1x805263eml3mwyeny8cvdpe9q27f4ku3h2yatl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka1xsntypk5ehu70rvy4nxh49d7zvk6nwf8tj2xd8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "920305803"
          }
        ]
      },
      {
        "address": "gonka16qm4h6qlv5q65cz6q4m4z4h252tzk55hfu0u6f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka1puuuug080fa7p3kpdvwq624ufnxe4vqg8yd62f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka1r6xg9wcw2ekrlyyp0ct04zqv23dz695tcdx6vh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka1rkr3np6d965ztapgle7hlynvdtx5pqqwef9ks8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka1vxusszuq3z92ck4q5vkd877zu5grk7qu2j7dqf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka1xnf7rsktgug63zfl68f22rnecljruzyk6f0ja6",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "912027590"
          }
        ]
      },
      {
        "address": "gonka17sktsm7djnwla0txhlq3lpeekw3jz38y2shqj3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465613"
          }
        ]
      },
      {
        "address": "gonka19u7w9jek8y5nj7qzssm3x6a8p2ukmrxrust6qs",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465613"
          }
        ]
      },
      {
        "address": "gonka1fwum8860xfxfqghem7npn643ppftsfevwply74",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465613"
          }
        ]
      },
      {
        "address": "gonka1x3szaeuwkx6c6wal4h3pr6z5a5d6p7dus4jy3h",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465613"
          }
        ]
      },
      {
        "address": "gonka146a8kuv4hf6lg5ex0h7k89vwld2c7lwp5923cy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465612"
          }
        ]
      },
      {
        "address": "gonka15dyl07mzr3h6harfrmkkav9vhgv64gsa3qp0s8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "903465612"
          }
        ]
      },
      {
        "address": "gonka1l3m5ake2y2aeka55x62dxem4dd52fyaku2vz3j",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "897394442"
          }
        ]
      },
      {
        "address": "gonka10cgunscfhdwjmndzcjv7znyj8nmdrf2jacxn0x",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka13v2qrzt2r8c0ctwct8j9hzqwew27chx6uwvlkm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka15an2wjcwrqlmqfn52hcycqdqegepdwraux8eqw",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka194pzpr7mqwkdldzgpfaadd8wwu663t3yaupcus",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka1a7ckfc5a9r8w87w3kfw5cxa7fhww67vk7krh03",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka1k6tjjlcj5y0rt3zu4gjq3pqjfync84v84atdel",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka1ym3p4nn8r6xydcj9a5jg88fwfquc23ndufh4td",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "889432972"
          }
        ]
      },
      {
        "address": "gonka1lc3a4lshfj5a7axh5w78edv8lc33hyyjef5692",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "870471367"
          }
        ]
      },
      {
        "address": "gonka14cee9dv3ew5chhttaka7p5q6ua0dfep5eqs0js",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "864229823"
          }
        ]
      },
      {
        "address": "gonka16rq8wlak0r4v9cdqs8sk3k4j28rxveyzn4eu4h",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "864229823"
          }
        ]
      },
      {
        "address": "gonka19akvnwa3dvw8zkthcm36vegvwmymkr3hxq0qve",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "864229823"
          }
        ]
      },
      {
        "address": "gonka1mjcyendh6mej6w6s2xymklpenn6ggw46l78esp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "864229823"
          }
        ]
      },
      {
        "address": "gonka1ve37whw9475rj3l0dy57xch9rnjcha9afv4f3s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "864229823"
          }
        ]
      },
      {
        "address": "gonka19mh7jn9xmzz9m0nrczgd32usqrcqm7mpsrh77j",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "845482324"
          }
        ]
      },
      {
        "address": "gonka1l3f9ze5n0fdwyaz4r9faeujhhx7szc53p9gclf",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "820297858"
          }
        ]
      },
      {
        "address": "gonka1a8dz4xw9xwwe0s3myandm6t0v4kvwea7pwrsmq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "816800688"
          }
        ]
      },
      {
        "address": "gonka1xnnu7yj6lsdmh3cjne9hk929y6yx8u5rwredz0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "816800688"
          }
        ]
      },
      {
        "address": "gonka14dd23kqxte3yhuae93g953ehh73f3djnuq0ern",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka15ra622ntmvwys9mxqncn2uv9vwknlytfu959ff",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka17f97mtfja2d38q8vjw5vsx8w833398aymznrxm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka19w0rclzvhpt0h9skdptfpaz5jw2t80ml2geuw9",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka1k5cycfsyhqk8txq95gtfffhpg20h6vlk84tdhv",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka1qzfec6p82ssja27nzs09ch09p87lqu3xx5e50f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka1whtj4z520meenq52f2zudu8zwmu06vg389x7pu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka1y9ayc8l9jxypsgmpqup0ean597g0ftlywf7urd",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "806821251"
          }
        ]
      },
      {
        "address": "gonka18zmmjk9799qeu7s2cku5yh3ty6xayxds7n42gh",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "803064557"
          }
        ]
      },
      {
        "address": "gonka1mkwqr346yy5ag0x450hht9ndl2wqhuzrfz0fd7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "803064557"
          }
        ]
      },
      {
        "address": "gonka1v3y4tse5aj58d7kxe4jqsw6e2hedewd82d737c",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "803064557"
          }
        ]
      },
      {
        "address": "gonka1w5xvh0ag9a2vd43lrurx5emlckth8fzv2tvepu",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "803064557"
          }
        ]
      },
      {
        "address": "gonka1zqj957tgjylep4vctsz8rw827slsddqww8drj5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "803064557"
          }
        ]
      },
      {
        "address": "gonka1rh9eca49arpw96m2zmvr2usk9qdy6q5gns8gj7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "771105184"
          }
        ]
      },
      {
        "address": "gonka1sv2jztqucv0z6whq6k3wlnd3u2qezpplrwyhdx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "736873285"
          }
        ]
      },
      {
        "address": "gonka1w6clgj4gjpd3r28gjp7vrza3rwzujl4gty6ln7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "735506121"
          }
        ]
      },
      {
        "address": "gonka1dll7aqkqleqt8s363fx2s3versn3r3c0zt3vj0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "729725585"
          }
        ]
      },
      {
        "address": "gonka1q6h4shel59yz6hqshz3ncdtegulj9840nzzyxs",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "728601300"
          }
        ]
      },
      {
        "address": "gonka1w0tchrxx49gfc0n8jua94pav7tw0l5hrhuzywl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "719208754"
          }
        ]
      },
      {
        "address": "gonka1qre9aepalndahwj37xrcepndmut2vu9dr3kh4t",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "703040454"
          }
        ]
      },
      {
        "address": "gonka1rxgvr9yg6xk3l2dak8glg0ld587q2wzzslvrl3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "699277690"
          }
        ]
      },
      {
        "address": "gonka1t9yhhn62sx36kg89h7js2ts507s46mqd40pe4s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "699277690"
          }
        ]
      },
      {
        "address": "gonka1z0lnxp7el2gxcqm37ckg8dfuac4rkuzf54wpa3",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "699277690"
          }
        ]
      },
      {
        "address": "gonka1dpee7kv4dwlmu9nr3skv488lxuhwsy3x70h0uq",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "692810573"
          }
        ]
      },
      {
        "address": "gonka1rq3skz3zfawkh7qsnjyzy9r3wf0xq8at096wy7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "648016885"
          }
        ]
      },
      {
        "address": "gonka1at7qj6ynelhp9kc3mgkw94m8j6jhrfh8wxse4n",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "644755098"
          }
        ]
      },
      {
        "address": "gonka1q8a7k5dl82znt5xwe7f63523gxd8h027epdg54",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586647280"
          }
        ]
      },
      {
        "address": "gonka12yxxjv4n3al94jgythp4jqyas8een5pu6xr2nr",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1cfmrgwmxv9dh5knq2p4fehqpnudr4xm72gnpkm",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1mf3w6hjc3y56tk85zqqgj25rxmp6wuv0vr74d7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1psznjawqr5m4dashm90wp46aq047twrxeel6qe",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1v5e25pcuvnv7q8vd2uwhvkkhskfs5laaxx3g8s",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1wttl0ghw929832auepgvq3gqrpfatcnfrzvqw2",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1y4rhy7fd7hlkrntctmxyehjkq8rrzp27nenk9v",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1yrqlpjnpqv9d626vl8s29vk383x74s0k5tdtd0",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "586612174"
          }
        ]
      },
      {
        "address": "gonka1yr7r80d483ukqeq3xkx6ymgqm6r22n5wdv8atj",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "585881308"
          }
        ]
      },
      {
        "address": "gonka1c2vpftj3n7679qp3k57yrtlhwp4qaay7ege9u8",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "560510475"
          }
        ]
      },
      {
        "address": "gonka1dmrm7jd0lrrgj346sz4kajdq9c3ves860c7hhy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "560510475"
          }
        ]
      },
      {
        "address": "gonka1l0e82j7tr3urs3ekrdqluchv47e0n4y0e5ulgg",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "560510475"
          }
        ]
      },
      {
        "address": "gonka16jrtxjqd8dznacsrtjpkf5mx0knja2xvwrgndp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "559789055"
          }
        ]
      },
      {
        "address": "gonka149ln5ehu48p00qalzafv7y3rkp6p7rmv8h3g8n",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "552021686"
          }
        ]
      },
      {
        "address": "gonka1z3z2lyte45juefxfmsvhnqny7wfg9npmp8gm03",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "552021686"
          }
        ]
      },
      {
        "address": "gonka1z7jrc6dvktlr6fccaj37jm4ncgj29jqrp5jvu7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "552021686"
          }
        ]
      },
      {
        "address": "gonka1t9pfwfag57kxmf3kyt088la4d8f892v24jvsf5",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "541507759"
          }
        ]
      },
      {
        "address": "gonka17y2whumwxn6gmpwppg6q25947h82ev78w0kgup",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "535616589"
          }
        ]
      },
      {
        "address": "gonka1xq4ngnc3zdsdl3rvtu7ytnkndpakzqu4dx0v7v",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "524592936"
          }
        ]
      },
      {
        "address": "gonka1dk535rvfyvd8f46h56rtz46z22a6hmvjmyryha",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "523497524"
          }
        ]
      },
      {
        "address": "gonka1ey9dfu98ngcjpg3lkmwc69xdsp2d9eaknyyl28",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "517494112"
          }
        ]
      },
      {
        "address": "gonka16spupg33ck73rk4d82h8fusxkh823r62dshg0p",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "485580854"
          }
        ]
      },
      {
        "address": "gonka1zj97wuqysdd0snt07z9204hlnf7phc4v9dnl5f",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "473074333"
          }
        ]
      },
      {
        "address": "gonka1y3dmsztt4wewmg2fl7w6t42tcwwa2g0wsy5csl",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "441617349"
          }
        ]
      },
      {
        "address": "gonka1n52k98esfltn4q783kuwg0amjn6cmuf94mwqep",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "440790436"
          }
        ]
      },
      {
        "address": "gonka1q6gwd6gf6pke29257lwfsxds3nlq06882tc6zn",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "440790436"
          }
        ]
      },
      {
        "address": "gonka1qq6cpau55hgse9yvwrup7fz38tvzc604jszfjy",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "440790436"
          }
        ]
      },
      {
        "address": "gonka1uq2fykmv82rdx3qk4lua6hpak9u327swgdgepk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "440790436"
          }
        ]
      },
      {
        "address": "gonka1x9nx86r5sx4awdmpadd2nmhlrnmezlxxe8ncps",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "440790436"
          }
        ]
      },
      {
        "address": "gonka14wmt933kjf2hlred8330gw28qjpt24j9p8muzp",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "385759538"
          }
        ]
      },
      {
        "address": "gonka1htfcs20dtdrywddza7mhv9hjr7naj3juyv8474",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "381624153"
          }
        ]
      },
      {
        "address": "gonka13ejhmp3g53r7csgautav95km9rjycxzy99a058",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "366760323"
          }
        ]
      },
      {
        "address": "gonka1y38q7euwkznfc28agxlugtmn9f5xgufkt8ts7m",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "366760323"
          }
        ]
      },
      {
        "address": "gonka14lhckrwqkxxw5w454yvcn7qv63vyn79rkcakg7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "359592198"
          }
        ]
      },
      {
        "address": "gonka1qty48qty43a3jm6jlq5t4aktz3yzs380uxxg2m",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "287541589"
          }
        ]
      },
      {
        "address": "gonka18frq9ltz0m7u7aw7fkmwhqh89ut3w2e434nxjx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "266551491"
          }
        ]
      },
      {
        "address": "gonka1fthllm8hzk69qkz3dhhyarj029z52yclrlj5va",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "255137616"
          }
        ]
      },
      {
        "address": "gonka1p4epndztqtsdu0cemsvm3kae70ec6nr7snfcms",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "251078150"
          }
        ]
      },
      {
        "address": "gonka1zdmwgnl9ycmctdehe5cqv5wpepty62lcms8alx",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "249741938"
          }
        ]
      },
      {
        "address": "gonka15nafqu6uglskzqkfgvh0mue7gats9dded3nctk",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "199164662"
          }
        ]
      },
      {
        "address": "gonka1hn9wmlfe7nha0x26p7nsqvk9g8pnwml74hrm8n",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "189322890"
          }
        ]
      },
      {
        "address": "gonka1wus9fvrxvx6sls623tme6rfgznu0l2myxm0k7z",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "186513559"
          }
        ]
      },
      {
        "address": "gonka18xk4m8t0zj9vpse5c2dem8uxhqw0egtjuafy77",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "180102359"
          }
        ]
      },
      {
        "address": "gonka1vs26xk4zvv6dv56j8r9ns7wzk6s00p8etk7wu7",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "131853118"
          }
        ]
      },
      {
        "address": "gonka1vz2ygndntgjw2nyrqgehd4sayw64pz26tvw7qt",
        "coins": [
          {
            "denom": "ngonka",
            "amount": "102378278"
          }
        ]
      }
    ]
  }
]
```

</details>

---