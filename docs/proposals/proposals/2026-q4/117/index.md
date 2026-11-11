---
title: "#117 – Bitfury buys another tranche of GNK for 1.75M USDT as part of previously approved 12M USDT smart contract: 1.14M to Community Pool, 0.6M reimbursement of expenditures paid by Bitfury directly to vendors for bug bounty program and security audit"
description: "Bitfury intends to purchase GNK for 1.75M USDT from the previously approved 12M USDT Community Sale contract at $0.60 per GNK. 

Of this amount, 607,250 USDT is returned to Bitfury as reimbursement fo"
template: proposals-proposals-main.html
---

# #117 – Bitfury buys another tranche of GNK for 1.75M USDT as part of previously approved 12M USDT smart contract: 1.14M to Community Pool, 0.6M reimbursement of expenditures paid by Bitfury directly to vendors for bug bounty program and security audit

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-13T16:43:30.468794619Z"></span></div>

**Proposal ID:** `117`

**Type:** Exec, Execute Contract

**Submit:** 2026-11-11 16:43 UTC

**Voting:** 2026-11-11 16:43 UTC → 2026-11-13 16:43 UTC

**Proposer:** [`gonka1as7g7ansh8wurv22gqqa9kq7592eclt8tkyycg`](https://gonka.gg/address/gonka1as7g7ansh8wurv22gqqa9kq7592eclt8tkyycg){:target="_blank"}

**Metadata:** [https://github.com/bitfury-com/gonka/blob/6c8444c4153e1c313c1bb383e587b3ce5ef69942/proposals/117/readme.md](https://github.com/bitfury-com/gonka/blob/6c8444c4153e1c313c1bb383e587b3ce5ef69942/proposals/117/readme.md)



[View on gonka.gg](https://gonka.gg/network/proposals/117){:target="_blank"}

</div>

Bitfury intends to purchase GNK for 1.75M USDT from the previously approved 12M USDT Community Sale contract at $0.60 per GNK. 

Of this amount, 607,250 USDT is returned to Bitfury as reimbursement for security audit contracts with HackerOne and Trail of Bits, which Bitfury paid in fiat directly to vendors, because Gonka had no legal entity at the time which both providers needed. 

The remaining part of 1,142,750 USDT stays on the Community Pool. 

If the proposal is not approved, none of these transactions will take place.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:56.5%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (851,665)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 851,665 votes</span>
    <span class="prop-tally-yes-text">✓ Turnout <strong>56.5%</strong> (851,665 / 1,506,224) · Quorum <strong>25%</strong> (376,556)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka133xdfvcyj2ccv38jrl0qjp970u9lz5plptfwuh" target="_blank" class="prop-voter-addr">gonka133xdfv…ptfwuh</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1nurzpppvn0lxg20v2c3gf8zfltpdpz599rggst" target="_blank" class="prop-voter-addr">gonka1nurzpp…9rggst</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka147qfckm9hpdzd9dgfvfj2r5rsv0eeunj4gpvz8" target="_blank" class="prop-voter-addr">gonka147qfck…4gpvz8</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1kvmerzu64094dt9t62ea0cp75larh39ulzldum" target="_blank" class="prop-voter-addr">gonka1kvmerz…lzldum</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2" target="_blank" class="prop-voter-addr">gonka168rtjf…lnkns2</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka16dgkvx7mh609ntkzknckwaskgq9lcdp86j0skk" target="_blank" class="prop-voter-addr">gonka16dgkvx…6j0skk</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.authz.v1beta1.MsgExec` |
| 2 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.authz.v1beta1.MsgExec",
    "grantee": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "msgs": [
      {
        "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
        "sender": "gonka1as7g7ansh8wurv22gqqa9kq7592eclt8tkyycg",
        "contract": "gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk",
        "msg": {
          "send": {
            "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
            "amount": "1750000000000",
            "msg": "e30="
          }
        },
        "funds": []
      }
    ]
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_cw20": {
        "contract_addr": "gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk",
        "amount": "607250000000",
        "recipient": "gonka1as7g7ansh8wurv22gqqa9kq7592eclt8tkyycg"
      }
    },
    "funds": []
  }
]
```

</details>
