---
title: "#1914 — pplying a diff copies the whole escrow state, and the copy grows for the life of the escrow"
source: https://github.com/gonka-ai/gonka/issues/1914
issue_number: 1914
synced_at: 2026-10-05T07:10:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    pplying a diff copies the whole escrow state, and the copy grows for the life of the escrow
    <span class="issues-number">#1914</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-04 13:06 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-04 13:30 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Applying a diff copies the whole escrow state, and the copy grows for the life of the escrow

## Summary

Every diff on a host with storage, and every diff the gateway composes, deep-copies the mutable escrow state twice. Most of that state stays small. Two maps do not: `sealedNonces` keeps one entry per sealed inference and is never trimmed, and `TurnTracker.heartbeatAt` keeps one entry per heartbeat nonce for the whole session. Both are copied on every diff.

The cost of applying a diff therefore grows with the escrow's history, not with the diff. Over the life of an escrow the total copy work grows roughly with the square of the number of sealed inferences. The discarded copies are also the main source of allocation and GC on this path.

This needs measurements before a fix. The fix changes how state is snapshotted and rolled back, and post-state roots have to stay byte-identical, so it should be its own change.

## What the apply path does

A host with a store applies a diff in `Host.applyAndPersist`:

1. `StateMachine.ValidateDiff` copies the mutable state (`pre`), applies the diff to the live maps, copies the result (`post`), then puts `pre` back.
2. The diff is persisted.
3. `StateMachine.CommitValidated` installs `post` by assigning the copied maps. It does not copy them again.

The gateway does the same thing in `StateMachine.PreviewLocalBestEffort` when it composes a diff, and `CommitValidated` installs that copy too.

`snapshotMutable` (`devshard/state/machine.go`) is the copy. It deep-copies:

| Copied | Bound |
| --- | --- |
| Live `Inferences`, including `PromptHash` and `ResponseHash` | In-flight and in-grace records only |
| `committedEntries` | Same window. Sealing deletes the entry (`seal.go`, auto-seal, `SealInference`, and the settlement drain). The field comment that says it keeps every inference ever created is out of date |
| `HostStats`, `WarmKeys` | One entry per slot |
| `sealedNonces` | One `uint64` to `uint64` per sealed inference. Nothing deletes these entries |
| `TurnTracker` (`turns`, `heartbeatAt`) | `turns` keeps the newest 64. `heartbeatAt` keeps one entry per heartbeat nonce for the session (`heightsync/turn.go`) |
| `FloorIndex.entries` | Capped at `DefaultFloorWindow` (4096) |

On a successful diff both copies are allocated. `post` becomes the live state and stays until the next diff replaces it. `pre`, and the previous live maps, become garbage immediately. Hosts without a store take one rollback snapshot inside `ApplyDiff` instead of this pair.

Go's heap profile reports in-use memory by the allocating stack, so the surviving copy shows up under `snapshotMutable`, `copyInferences`, and `cloneCommittedInferenceEntries`. That is the live escrow state. `cmd/devshardd/memwatch.go` notes this next to `topHeapInUse`.

## Why this is the next cost

A diff's CPU and allocation are proportional to `len(sealedNonces)` plus `len(heartbeatAt)`, on top of the live inference set. Those two maps only grow.

If an escrow seals on the order of its diff count, each new diff copies a larger map than the last, so the copies across the escrow add up quadratically. The garbage is the same size, so GC CPU and peak heap rise with it. `FloorIndex.Clone` already calls this out: it runs several times per diff on the apply hot path.

The live inference copy is real too, but it tracks concurrency, not history.

## Measure before changing it

The size of the problem depends on production numbers we do not have:

- `len(sealedNonces)` and `len(heartbeatAt)` on busy escrows, and how fast they grow.
- The live inference count per escrow.
- The diff rate.
- The share of CPU and allocations in `snapshotMutable` during `ValidateDiff` and `CommitValidated`.

A benchmark of `ValidateDiff` plus `CommitValidated` at about 1k, 10k, and 100k sealed inferences, read against a production heap and CPU profile, is enough to decide whether this is worth a release of its own.

`/stats/memory` already reports live and sealed inference counts per process, and the fattest escrow. It does not report `sealedNonces` or `heartbeatAt` sizes. Those two lengths are the missing series.

## Directions, once there is a number

Any of these keeps the trial apply off the live maps and has to leave `post_state_root` unchanged:

- An undo log for maps that only gain entries (`sealedNonces`, `heartbeatAt`), so a rollback deletes the keys added during the trial instead of cloning the whole map.
- Copy-on-write for those maps.
- Leaving `sealedNonces` out of the full snapshot if its only mutation on apply is insertion.

`Inferences` is still mutated in place and still needs a real copy or a copy-on-write map. That part stays proportional to the live set.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-04 13:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Measurements for the <code>sealedNonces</code> / <code>heartbeatAt</code> part, in case they help size the fix. On a host it is three copies per diff, not two: <code>pre</code> (<code>machine.go:318</code>), the rollback copy in <code>applyCore</code> (<code>:709</code>) and <code>post</code> (<code>:330</code>). <code>devshard/v5</code> 99c9ae9f4, Apple M1, <code>go test -bench</code>, those three copies with an empty live set:</p>
<table>
<thead>
<tr>
<th>state</th>
<th>time per diff</th>
<th>allocated per diff</th>
</tr>
</thead>
<tbody>
<tr>
<td>empty</td>
<td>1.3 µs</td>
<td>2 KB</td>
</tr>
<tr>
<td>7,810 sealed</td>
<td>0.56 ms</td>
<td>0.89 MB</td>
</tr>
<tr>
<td>25,307 sealed</td>
<td>1.7 ms</td>
<td>1.8 MB</td>
</tr>
<tr>
<td>96,676 sealed</td>
<td>6.5 ms</td>
<td>7.1 MB</td>
</tr>
<tr>
<td>25,307 heartbeat nonces</td>
<td>1.7 ms</td>
<td>1.8 MB</td>
</tr>
</tbody>
</table>
<p>So about 67 ns and 73 B per entry per diff, the same for either map. The sealed counts are the median, the v5 median and the largest escrow among the last 1000 <code>devshard_escrow_settled</code> events on mainnet (25–26 Sep, nonces = fees / fee_per_nonce; at most one inference per nonce, so these are upper bounds). Summed over an escrow's life, where diff k copies about k entries, that is roughly 21 s of CPU and 23 GB allocated per host for a 25k-nonce escrow, and 310 s and 340 GB for the largest one.</p>
<p>Nothing deletes from <code>sealedNonces</code> (only <code>restoreMutable</code> and <code>RestoreSealedNonces</code> replace it), which supports recording the inserted ids instead of copying. #1905 cuts the gateway path to one copy but still copies <code>sealedNonces</code> in full and does not touch the host's <code>ValidateDiff</code>.</p>
<details><summary>benchmark (devshard/state)</summary>


<pre><code class="language-go">func BenchmarkSnapshotMutableSealed(b *testing.B) {
    hb := []*types.DevshardTx{{Tx: &amp;types.DevshardTx_Heartbeat{Heartbeat: &amp;types.MsgHeartbeat{}}}}
    for _, c := range []struct{ sealed, heartbeats int }{
        {0, 0}, {7_810, 0}, {25_307, 0}, {96_676, 0}, {0, 25_307},
    } {
        b.Run(fmt.Sprintf(&quot;sealed=%d/heartbeats=%d&quot;, c.sealed, c.heartbeats), func(b *testing.B) {
            sm, _ := benchFillSQLite(b, &quot;bench-copy&quot;)
            nonces, _ := benchSealedNonces(c.sealed)
            sm.RestoreSealedNonces(nonces)
            for i := 1; i &lt;= c.heartbeats; i++ {
                sm.turnTracker.Observe(uint64(i), hb, 0)
            }
            b.ReportAllocs()
            b.ResetTimer()
            for i := 0; i &lt; b.N; i++ {
                pre := sm.snapshotMutable()
                _ = sm.snapshotMutable()
                _ = sm.snapshotMutable()
                sm.restoreMutable(pre)
            }
        })
    }
}
</code></pre>

</details>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1914](https://github.com/gonka-ai/gonka/issues/1914) every hour.
