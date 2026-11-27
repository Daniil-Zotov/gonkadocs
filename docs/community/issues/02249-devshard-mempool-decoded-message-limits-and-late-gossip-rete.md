---
title: "#2249 — DevShard mempool: decoded-message limits and late gossip retention"
source: https://github.com/gonka-ai/gonka/issues/2249
issue_number: 2249
synced_at: 2026-11-27T02:17:06Z
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
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-17 05:34 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-17 05:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Follow-up verification (2026-11-17) to help scope any further work: I checked <code>devshard/v7</code> at <code>34ddd777475be05f583945add3c275b490f3cf39</code>, #2226 at <code>237b94ff0392f0bb2210e8fb8d2c8b7abbb42901</code>, and #2042 at <code>ddc0b31a116978f7c520cf9a24d61bd38325ccd7</code>.</p>
<p>The current production <code>devshardd</code> HostManager <a href="https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/session/manager.go#L2287-L2310">leaves gossip unwired</a>. The existing <code>TestRecoverSessions_HappyPath</code> passed and checks that inbound gossip does not populate its mempool. With gossip explicitly wired, my combined signed HTTP RPC → real Server → Host fixture reproduced the already-applied Finish being retained and returned at nonce 20 on the shared branch and #2226, using <strong>v6 session protocol</strong>. With gossip unwired, the same late delivery retained zero entries. This supports the local retention finding; it does not establish that this gossip path is active in a deployed production host.</p>
<p>There is now partial overlap with #2042, which is still an open draft. In a <strong>v7 session</strong>, its <a href="https://github.com/gonka-ai/gonka/blob/ddc0b31a116978f7c520cf9a24d61bd38325ccd7/devshard/host/mempool_auth.go">logical mempool cleanup</a> removed the genuine late Finish when <code>Host.MempoolTxs()</code> ran: raw count after RPC = 1, after cleanup = 0. That cleanup is protocol-gated; the v6 control still retained the duplicate. This is worth coordinating with before implementing another stale-Finish fix.</p>
<p>Cumulative retention remains a separate gap in these explicitly wired fixtures. Three batches of 32,768 distinct, slot-owner-signed Finish transactions left 98,304 entries after replay and <code>PruneBelow</code>; on #2042 in v7 mode they also survived authorization/logical cleanup. These referenced <strong>unknown future inference IDs</strong>, not 98,304 completed inferences. #2226 correctly rejected the single-message 65,537-entry control. A follow-up therefore still needs an explicit cumulative admission/retention policy while preserving legitimate pending recovery work.</p>
<p>Scope: Go 1.25.9, darwin/arm64, local HTTP loopback, actual Attach/signed envelopes and Server membership handling, real Host/state/mempool, stub inference engine and v7 chain-proof oracle. No deployed traffic, OOM, throughput, or retained-memory measurement. These were additional local characterization fixtures, not the companion files listed in the issue.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2249](https://github.com/gonka-ai/gonka/issues/2249) every hour.
