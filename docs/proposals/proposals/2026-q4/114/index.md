---
title: "#114 – Approve devshard v4.2 and remove v5"
description: "Devshard v4.2

This proposal removes v5 from the approved devshard versions and adds v4.2. The existing v4.1 entry stays unchanged.

Devshard v4.2 polishes the v4 runtime with fixes for production iss"
template: proposals-proposals-main.html
---

# #114 – Approve devshard v4.2 and remove v5

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-10-14T04:46:24.436120594Z"></span></div>

**Proposal ID:** `114`

**Type:** Delete Devshard Approved Version, Put Devshard Approved Version

**Submit:** 2026-10-12 04:46 UTC

**Voting:** 2026-10-12 04:46 UTC → 2026-10-14 04:46 UTC

**Proposer:** [`gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le`](https://gonka.gg/address/gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/b88062c9529389a61d4ba15b8b5603716a50909e/proposals/governance-artifacts/devshard/v4.2/README.md](https://github.com/gonka-ai/gonka/blob/b88062c9529389a61d4ba15b8b5603716a50909e/proposals/governance-artifacts/devshard/v4.2/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/114){:target="_blank"}

</div>

Devshard v4.2

This proposal removes v5 from the approved devshard versions and adds v4.2. The existing v4.1 entry stays unchanged.

Devshard v4.2 polishes the v4 runtime with fixes for production issues and performance improvements. It uses less CPU and memory, reduces repeated validation work, fixes validation recovery, refusal handling, and gateway routing. The changes are listed below.

## Proposal

Update the approved devshard versions:

- Remove `v5`.
- Add `v4.2` with the fixes and performance improvements below.
- Keep the existing `v4.1` entry unchanged.

This update is approved through devshard governance and does not require a full chain software upgrade.

## Fixes and Improvements

### Fixes

1. Inference validation enforces every token in a streamed chunk instead of only the first.
2. ML requests and validation leases use the same 32-minute timeout.
3. Validation leases are scoped to the escrow's epoch, so expired escrows cannot create new validation work in a later epoch.
4. Recovery submits a validation vote for challenged inferences and skips queued work that is already resolved.
5. A refusal recheck accepts the timeout if the executor stops advancing or reports a mismatched state. An advancing executor gets at most three further challenges to return a valid receipt.
6. A confirmed inference stops the refusal attempt. Executor receipts must pass signature verification before they can cancel a refusal.
7. Executors return challenge receipts before execution finishes, so a running inference does not hold up the refusal check.
8. Pooled chat routes use the resolved model. Omitting the model cannot route a request to a different model with stricter access rules ([#1976](<https://github.com/gonka-ai/gonka/pull/1976>)).
9. DeepSeek V4 Flash 0731 validation handles known prompt-formatting differences between MLNode versions. It accepts exactly 78 or 79 extra claimed input tokens while retaining output and logit checks.

### Performance

1. The live inference set uses a running sum of Ristretto255 points, so adding, updating, or removing a record does not require hashing the whole set.
2. Diff application journals changed records for rollback instead of making full-state copies.
3. Payload signing keeps the decrypted key in memory and reloads it when its file changes.
4. Validation walks a journaled set of outstanding inference IDs instead of scanning all live inferences.
5. Each successful inference earns one per-model validation credit for that process, valid for 60 minutes. Each ML validation dispatch spends one credit, limiting validation load when generation slows.
6. Repeated lease conflicts are deferred to reduce scheduling overhead and log noise.
7. Refusal challenges forward only missing diffs when the executor's state matches. Full-history fallback remains for other cases.
8. Gateway catch-up reads history in pages, saves session state in each diff transaction, and trims cached history.
9. Auto-seal logs contain counts instead of full inference lists.

### Testing and Diagnostics

1. Regression tests cover validation, recovery, refusal handling, state updates, and routing.
2. A v4.2 load-testing harness covers sustained load, escrow rotation, and slow or failing ML nodes ([#1953](<https://github.com/gonka-ai/gonka/pull/1953>)).
3. Memory diagnostics run every 10 minutes without the stop-the-world memory-stat read.

## Implementation

Submit an on-chain governance proposal to update the approved devshard versions. The new entry uses:

- Register protocol `v4.2`.
- Binary: `<https://github.com/gonka-ai/gonka/releases/download/devshard%2Fv4.2.0/devshardd.zip`>
- SHA-256: `068599a524d4f456b36c6a208aad05d962b6751752fc0cab5991b24cf5429625`

The existing `v4.1` binary URL and checksum remain unchanged. v5 is removed.

`versiond` downloads and verifies the approved binary and serves it under `/devshard/v4.2`. Host and gateway releases are built from the same v4.2 source. Gateways must use v4.2 escrows to use the new runtime.

## Contributors (sorted alphabetically)

- @a-kuprin
- @aikuznetsov
- @gmorgachev
- @qdanik
- @vbgd0


---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:39.7%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (270,364)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 270,364 votes</span>
    <span class="prop-tally-yes-text">✓ Turnout <strong>39.7%</strong> (270,364 / 680,386) · Quorum <strong>25%</strong> (170,096)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p" target="_blank" class="prop-voter-addr">gonka1ym3np7…0e4a2p</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1dcagmtcnra345dza6uf7c80tekm0q5usjtqz7c" target="_blank" class="prop-voter-addr">gonka1dcagmt…jtqz7c</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1nurzpppvn0lxg20v2c3gf8zfltpdpz599rggst" target="_blank" class="prop-voter-addr">gonka1nurzpp…9rggst</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka147qfckm9hpdzd9dgfvfj2r5rsv0eeunj4gpvz8" target="_blank" class="prop-voter-addr">gonka147qfck…4gpvz8</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1kvmerzu64094dt9t62ea0cp75larh39ulzldum" target="_blank" class="prop-voter-addr">gonka1kvmerz…lzldum</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka16dgkvx7mh609ntkzknckwaskgq9lcdp86j0skk" target="_blank" class="prop-voter-addr">gonka16dgkvx…6j0skk</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka16k7nzvlheye8zhtyykcanxz0hldnfkmaedye8d" target="_blank" class="prop-voter-addr">gonka16k7nzv…edye8d</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgDeleteDevshardApprovedVersion` |
| 2 | `/inference.inference.MsgPutDevshardApprovedVersion` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.inference.MsgDeleteDevshardApprovedVersion",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "name": "v5"
  },
  {
    "@type": "/inference.inference.MsgPutDevshardApprovedVersion",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "version": {
      "name": "v4.2",
      "binary": "https://github.com/gonka-ai/gonka/releases/download/devshard%2Fv4.2.0/devshardd.zip",
      "sha256": "068599a524d4f456b36c6a208aad05d962b6751752fc0cab5991b24cf5429625"
    }
  }
]
```

</details>
