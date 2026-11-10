---
title: "#2249 — DevShard mempool: decoded-message limits and late gossip retention"
source: https://github.com/gonka-ai/gonka/issues/2249
issue_number: 2249
synced_at: 2026-11-10T23:30:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    DevShard mempool: decoded-message limits and late gossip retention
    <span class="issues-number">#2249</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/ilyar">@ilyar</a> opened 2026-11-08 18:38 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-08 18:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Local tests reproduce the retention behaviour reported in [issue #1899, item 3](https://github.com/gonka-ai/gonka/issues/1899), including a genuine Finish transaction received again after its signed diff was applied

The tests also support the per-message protection in [PR #2226](https://github.com/gonka-ai/gonka/pull/2226): its parent accepts 65,537 valid encoded transaction entries, while the proposed change rejects the same request before the mempool sink

These are separate properties, the PR bounds one decoded message but does not bound the total retained mempool across messages, this report is not a request to block that narrower fix

Status: `REPRODUCED`, local regression evidence only, no production exhaustion or throughput claim

## Checked revisions

Snapshot: 2026-11-08, Linux amd64, Go 1.25.9, local HTTP loopback and in-memory Host fixtures, no deployed host traffic

| Target | Exact revision | Check |
|---|---|---|
| PR candidate | [22f6ee5f](https://github.com/gonka-ai/gonka/commit/22f6ee5f3f7f3a5d2e71f2d5beaf02dfedba3523) | All four selected tests passed three consecutive runs |
| Candidate parent | [4b8deb65](https://github.com/gonka-ai/gonka/commit/4b8deb65045042e473c66411011da19b126609c9) | Same new fixtures, one run, count-limit assertion fails because the RPC returns success, late-arrival checks pass |

## Observations

| Test | Observation | What it establishes |
|---|---|---|
| `TestResearchMempoolRPCBatchVersusLifetime` | Three accepted batches of 32,768 distinct entries leave 98,304 entries, replaying the last batch adds none, `PruneBelow` leaves the count unchanged | Per-message acceptance and cumulative retention are independent, identical hashes are deduplicated |
| Same test, over-count control | A single batch of 65,537 valid repeated entries returns `InvalidArgument` on the candidate and succeeds on the parent | The proposed count gate works, rejection is not caused by malformed transaction bytes |
| `TestResearchLateGossipAfterSignedDiff` | Real Host executes an inference, signed diffs include its ConfirmStart and Finish, mempool becomes empty, a late copy of that Finish remains after signed empty diffs advance to nonce 20 | Normal inclusion removes the entry, late delivery reintroduces it and later diffs do not remove it |
| `TestResearchMempoolLateArrivalPrimitive` | Arrival before removal leaves zero entries, arrival after removal leaves one | Minimal ordering control for the retention mechanism |
| Existing `TestSessionHandler_RefusesOverCountDiffsBeforeDecode` | Passes on the candidate in all three runs | Existing diff-count and summed-transaction rejection checks remain green |

The late-arrival Host returns the retained Finish in its response mempool and continues signing, the fixture does not enable the test-only `WithGrace` checker

The RPC fixture uses the repository's actual local HTTP server, Attach/session-token flow, signed envelopes, decoder, gossip handler, real Gossip and real Mempool, its SessionCore membership decision is a stub returning true, it is not an independent test of membership enforcement or the full production Server adapter

The Host fixture uses real state-machine application and signed diffs with a stub inference engine, delayed delivery enters through `OnTxsReceived`, it is not a combined end-to-end RPC-to-Host lifecycle test

## Reproduction

Use a disposable checkout at the [candidate revision](https://github.com/gonka-ai/gonka/commit/22f6ee5f3f7f3a5d2e71f2d5beaf02dfedba3523), preserve the normal Go and CGO prerequisites for the repository, including its wasmvm library

Companion files to attach alongside this report:

- `26-003/host_retention_research_test.go` → `devshard/host/mempool_retention_research_test.go`
- `26-003/mempool_retention_research_test.go` → `devshard/transport/rpcserver/mempool_retention_research_test.go`

```bash
cd devshard
GOTOOLCHAIN=go1.25.9 go test ./host ./transport/rpcserver \
  -run 'TestResearch|TestSessionHandler_RefusesOverCountDiffsBeforeDecode' \
  -count=3 -v
```

Expected candidate excerpts:

```text
signed inclusion retained=0; late identical finish retained=1 after nonce 20, returned in response
over-count response: invalid_argument: ... decode limit ...
three admitted batches: retained=98304; replay unchanged; prune unchanged; over-count rejected
PASS
```

On the [parent revision](https://github.com/gonka-ai/gonka/commit/4b8deb65045042e473c66411011da19b126609c9), run the same new files with `-run TestResearch -count=1`, the RPC test fails at the over-count rejection assertion and logs `over-count response: <nil>`, that expected failure distinguishes the candidate's protection from its parent

These are characterization tests, a `PASS` on retention assertions means the issue was reproduced, not that retention is correct, a future retention fix should invert those assertions around its documented eviction or stale-entry contract

## Relevance to existing work

[Issue #1899](https://github.com/gonka-ai/gonka/issues/1899): this adds an executed late-arrival regression to item 3, it does not validate every performance claim in that issue

[PR #2226](https://github.com/gonka-ai/gonka/pull/2226): the candidate's per-request gate is verified against its parent, cumulative retention remains a separate follow-up, a message limit alone is not a lifetime storage limit

[PR #1312](https://github.com/gonka-ai/gonka/pull/1312): signature filtering addresses which transactions enter the pool, the late-arrival example is an authentic Finish already accepted by a signed diff, so signature validation alone would not identify it as stale, this is a design observation rather than a test of that old PR branch

A retention fix needs to distinguish local unsequenced work needed for recovery from imported entries that are already applied or otherwise stale, simply clearing the pool risks dropping valid recovery data, an appropriate regression set should preserve pending legitimate transactions while reclaiming the demonstrated late duplicate

## Limits

No OOM, production load, malicious remote access, memory-per-entry estimate or sustained rate was measured, no claim is made that normal signature or settlement processing stops

The earlier exploratory memory estimate counted allocations during insertion and excluded transaction construction, it is not a full retained-memory measurement and is deliberately omitted

The historical signature-filtering PR was read but not built, neither a complete review of it nor approval of the count-limit PR is implied

No new public issue or PR has been created, recheck current PR heads before attaching these results, attach both companion tests so the report remains reproducible

</div>

---

> 🔄 **Auto-synced** from [Issue #2249](https://github.com/gonka-ai/gonka/issues/2249) every hour.
