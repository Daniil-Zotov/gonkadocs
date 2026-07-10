---
title: "#1341 — [BUG] devshard: data race on inflight receiptTime between send goroutine and escalation scheduler (go test -race fails on main)"
source: https://github.com/gonka-ai/gonka/issues/1341
issue_number: 1341
synced_at: 2026-07-10T04:28:10Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] devshard: data race on inflight receiptTime between send goroutine and escalation scheduler (go test -race fails on main)
    <span class="issues-number">#1341</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@redstartechno](https://github.com/redstartechno) opened 2026-06-12 20:05 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-06-26 23:54 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary
`go test ./cmd/devshardctl/ -race -run TestRunInference` fails on current `main` (8bd883ba3) with 15 data race reports across 13 tests. The dominant race (11 of the 15 reports) has production code on both sides: the send goroutine writes `inf.receiptTime` inside `receiptOnce.Do` (`redundancy.go:1491`) while the orchestrator's escalation scheduler reads `inf.receiptTime.IsZero()` without synchronization (`redundancy.go:2251`, in `escalationForInflight` ← `nextEscalationTrigger` ← `awaitRace` ← `RunInference`).

## Motivation
`time.Time` is a multi-word struct, so the Go memory model gives this read no guarantees — the scheduler can observe a torn or stale value and mis-schedule (or skip) the receipt-timeout escalation. The comment block at `redundancy.go:1501-1512` documents a previous scheduler race of exactly this shape on `sendTime`, fixed by stamping it synchronously before the goroutine spawns; `receiptTime` has the same consumer but cannot be stamped synchronously (it is set when the receipt arrives), so it needs actual synchronization. The races also block ever enabling `-race` in CI for devshard. Found while race-testing an unrelated branch; reproduces identically on unmodified `main`.

## Impact
- Who is affected: hosts running the devshard gateway (request orchestration / escalation path); developers (the package cannot pass `go test -race`).
- Network-wide or limited: limited — single participant, non-chain.
- Likelihood: intermittent at runtime (timing-dependent); deterministic under the race detector — every `TestRunInference_*` run reports it.
- Severity: Impact limited × likelihood intermittent → low-to-medium. Practical worst case is a missed or mistimed receipt-timeout escalation (tail latency / stall on a silent primary — the exact regression class the `sendTime` fix in the comment describes).
- Affected components: `devshard/cmd/devshardctl` (`Redundancy.RunInference`, escalation scheduling).

## Detailed description

Reproduce (Linux, Go 1.24.2, commit 8bd883ba3):

```
cd devshard
go test ./cmd/devshardctl/ -race -count=1 -run TestRunInference
```

13 tests fail, including `TestRunInference_HappyPath`, `TestRunInference_FastReceiptDoesNotSpuriouslyEscalate`, `TestRunInference_SpeculativeOnKill`, `TestRunInference_PerfTracking`, and the stalled-winner scenarios.

**Race 1 (primary, 11/15 reports):** `receiptHandler` runs on the send goroutine and stamps `inf.receiptTime = time.Now()` inside `inf.receiptOnce.Do(...)` (`redundancy.go:1491`). Concurrently, `escalationForInflight` on the orchestrator goroutine reads `inf.receiptTime.IsZero()` (`redundancy.go:2251`) to decide whether to schedule the receipt-timeout escalation. The `receiptOnce` callback also does `close(inf.receiptCh)`, which would provide the needed happens-before edge — but the reader checks the field directly instead of deriving "receipt received" from the channel.

**Race 2 (secondary, stalled-winner scenarios):** a still-running attempt's `raceWriter.Write` appends stream bytes to the shared group buffer while the orchestrator reads it via `Buffer.String()` (`redundancy.go:1275` path).

Representative full report from the race detector (write side, read side, goroutine origin):

<details>
<summary>go test -race output (TestRunInference_HappyPath)</summary>

```
WARNING: DATA RACE
Write at 0x00c0000c8070 by goroutine 31:
  devshard/cmd/devshardctl.(*Redundancy).startInflight.func1.1()
      devshard/cmd/devshardctl/redundancy.go:1491 +0x7b
  sync.(*Once).doSlow()
      /usr/local/go/src/sync/once.go:78 +0xe1
  sync.(*Once).Do()
      /usr/local/go/src/sync/once.go:69 +0x44
  devshard/cmd/devshardctl.(*Redundancy).startInflight.func1()
      devshard/cmd/devshardctl/redundancy.go:1490 +0xa4
  devshard/user.(*InProcessClient).Send()
      devshard/user/session.go:175 +0x115
  devshard/cmd/devshardctl.(*killableClient).Send()
      devshard/cmd/devshardctl/proxy_test.go:292 +0x26c
  devshard/user.(*Session).SendOnly()
      devshard/user/session.go:773 +0x42f
  devshard/cmd/devshardctl.(*Redundancy).startInflight.func2()
      devshard/cmd/devshardctl/redundancy.go:1520 +0x324

Previous read at 0x00c0000c8070 by goroutine 26:
  devshard/cmd/devshardctl.(*Redundancy).escalationForInflight()
      devshard/cmd/devshardctl/redundancy.go:2251 +0x484
  devshard/cmd/devshardctl.(*Redundancy).nextEscalationTrigger()
      devshard/cmd/devshardctl/redundancy.go:2210 +0x124
  devshard/cmd/devshardctl.(*Redundancy).awaitRace()
      devshard/cmd/devshardctl/redundancy.go:1921 +0x5e4
  devshard/cmd/devshardctl.(*Redundancy).RunInference()
      devshard/cmd/devshardctl/redundancy.go:1412 +0x1184
  devshard/cmd/devshardctl.TestRunInference_HappyPath()
      devshard/cmd/devshardctl/proxy_test.go:638 +0x174
  testing.tRunner()
      /usr/local/go/src/testing/testing.go:1792 +0x225

Goroutine 31 (running) created at:
  devshard/cmd/devshardctl.(*Redundancy).startInflight()
      devshard/cmd/devshardctl/redundancy.go:1516 +0xa84
  devshard/cmd/devshardctl.(*Redundancy).startAdditionalInflight()
      devshard/cmd/devshardctl/redundancy.go:1636 +0xba4
  devshard/cmd/devshardctl.(*Redundancy).RunInference()
      devshard/cmd/devshardctl/redundancy.go:1396 +0x156b
  devshard/cmd/devshardctl.TestRunInference_HappyPath()
      devshard/cmd/devshardctl/proxy_test.go:638 +0x174
  testing.tRunner()
      /usr/local/go/src/testing/testing.go:1792 +0x225
```

</details>

(The `killableClient` / test frames are the in-process stand-ins for remote hosts; in production the same write path runs through the real session client, so the racing accesses are production code in both reports.)

**Possible fix direction (race 1):** derive "receipt received" from `receiptCh` (non-blocking `select` on the closed channel) before touching `inf.receiptTime`, since `close(receiptCh)` already happens-after the timestamp write inside the `Once` — or guard the field with a mutex/atomic. Happy to send a small PR for this if maintainers agree on the direction; race 2 likely wants the group buffer access audited separately.

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-25 00:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @akup @x0152, what are your thoughts here? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@a-kuprin](https://github.com/a-kuprin)</span>
    <span class="issues-meta-item">commented 2026-06-25 17:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@redstartechno fixed here:
https://github.com/gonka-ai/gonka/commit/7b2c7b4dd946d37c32108103dad1a3cdfbdd6d25</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-26 23:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @redstartechno, this does not look like a bug or a vulnerability. It mostly seems to be a test-related issue, but I don’t see how it affects production code. Anyway, thanks for flagging</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1341](https://github.com/gonka-ai/gonka/issues/1341) every hour.
