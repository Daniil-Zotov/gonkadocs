---
title: "#1762 — devshard: host bridge drops escrow refusal_timeout/execution_timeout, so host and gateway can bind different SessionConfig"
source: https://github.com/gonka-ai/gonka/issues/1762
issue_number: 1762
synced_at: 2026-09-13T10:22:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: host bridge drops escrow refusal_timeout/execution_timeout, so host and gateway can bind different SessionConfig
    <span class="issues-number">#1762</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-09-13 03:44 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-13 03:45 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
On `devshard-0.2.15-v5` (PR #1584), the gateway and the host build `SessionConfig` with the same function but fetch the escrow through different bridges. The gateway's bridge copies `refusal_timeout` / `execution_timeout` off the escrow row; the host's bridge does not, so the host silently falls back to the compiled defaults (60 / 1920). Both values feed consensus — auto-seal and timeout votes — so a governance value other than the default desynchronises the two sides.

All line references are at PR head `9d1f01472459f17b1516933951d2617027b0ad08`.

## Where the two paths diverge

The gateway uses `bridge.GRPCBridge` ([main.go:527](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/cmd/devshardctl/main.go#L527), [gateway.go:410](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/cmd/devshardctl/gateway.go#L410)), which carries both fields:

```go
// devshard/bridge/grpc.go:99-104
		ValidationRate:            e.ValidationRate,
		VoteThresholdFactor:       e.VoteThresholdFactor,
		RefusalTimeout:            e.RefusalTimeout,
		ExecutionTimeout:          e.ExecutionTimeout,
		EpochID:                   e.EpochIndex,
		Settled:                   e.Settled,
```

The host (`devshardd`) uses `CachingEscrowBridge` over `ChainBridge` ([app.go:276](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/cmd/devshardd/app.go#L276)), and that bridge's `EscrowInfo` literal ends without them:

```go
// devshard/cmd/devshardd/bridge/chain.go:130-137
		InferenceSealGraceNonces:  e.InferenceSealGraceNonces,
		InferenceSealGraceSeconds: e.InferenceSealGraceSeconds,
		AutoSealEveryNNonces:      e.AutoSealEveryNNonces,
		ValidationRate:            e.ValidationRate,
		VoteThresholdFactor:       e.VoteThresholdFactor,
		EpochID:                   e.EpochIndex,
		Settled:                   e.Settled,
	}, nil
```

The warm cache cannot restore them either — [`EscrowCacheInfo`](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/storage/interface.go#L130) has no such fields, so [`EscrowInfoFromCache`](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/cmd/devshardd/bridge/caching.go#L129) maps a cached row back without them as well.

Both sides then go through the same mapper, [`SessionConfigAtBind`](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/bridge/config.go#L19) → `SessionConfigFromEscrow`, where zero means "use the compiled default":

```go
// devshard/types/config.go:50-53
func DefaultSessionConfig(groupSize int) SessionConfig {
	return NormalizeSessionConfig(SessionConfig{
		RefusalTimeout:    60,
		ExecutionTimeout:  32 * 60,
```

## Why both values are consensus-relevant

Auto-seal reads `ExecutionTimeout` from the session config ([seal.go:452](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/state/seal.go#L452)) and folds it into the Finished clock gate:

```go
// devshard/state/seal.go:43-51
func FinishedClockRequiredSeconds(graceSeconds, executionTimeout int64) int64 {
	...
	return graceSeconds + executionTimeout
}
```

`autoSealLocked`'s own comment states the consequence: "Mixed binaries that disagree on this sum diverge on SealedAcc / post_state_root."

Host-side timeout votes use the same config — [timeout.go:109](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/host/timeout.go#L109) rejects a REFUSED vote while `now - StartedAt < RefusalTimeout`, and [timeout.go:183](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/host/timeout.go#L183) rejects an EXECUTION vote while `now - ConfirmedAt < ExecutionTimeout` — while the gateway computes its own deadline from its own config ([session.go:2824](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/user/session.go#L2824)).

## Reproduction

Same mapper, same group size, one field differing: the host's escrow (fields dropped by `ChainBridge`) against the gateway's (fields carried by `GRPCBridge`) for a governance `execution_timeout = 1200`, with `inference_seal_grace_seconds = 3600`:

```go
hostCfg := SessionConfigAtBind(16, &hostEscrow)        // RefusalTimeout/ExecutionTimeout zero
gatewayCfg := SessionConfigAtBind(16, &gatewayEscrow)  // RefusalTimeout 60, ExecutionTimeout 1200
state.FinishedClockRequiredSeconds(int64(cfg.InferenceSealGraceSeconds), cfg.ExecutionTimeout)
```

```
SUBJECT host    (ChainBridge drops the fields): refusal=60 execution=1920 sealThreshold=5520
CONTROL gateway (GRPCBridge carries them):      refusal=60 execution=1200 sealThreshold=4800
```

Two consequences follow from that gap:

- **Sealing.** For an inference whose `stateClock - ConfirmedAt` lands between 4800 and 5520, the gateway folds it into `SealedAcc` and the hosts do not, so `post_state_root` disagrees. Hosts answer `post_state_root does not match computed state root` ([types/errors.go:35](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/types/errors.go#L35)) and the gateway marks them `escrow_state_root_diverged` ([redundancy.go:3787](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/cmd/devshardctl/redundancy.go#L3787)). A raised timeout produces the mirror image.
- **Votes.** The gateway starts voting at its own (smaller) deadline while hosts still reject the vote as premature, so quorum is never reached and the record stays `Started`. At settlement a still-live record pays the executor its full reservation ([machine.go:1668](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/state/machine.go#L1668)):

```go
	case types.StatusStarted, types.StatusPending:
		rec.ActualCost = rec.ReservedCost
		rec.Status = types.StatusFinished
		sm.state.HostStats[rec.ExecutorSlot].Cost += rec.ReservedCost
```

## Why it is quiet today

Mainnet governance currently sets exactly the compiled defaults, so the two paths agree by coincidence. Read from the public REST endpoint (`/chain-api/productscience/inference/inference/params` on `node1.gonka.ai:8000`), 2026-09-13:

```
devshard_escrow_params.refusal_timeout = 60
devshard_escrow_params.execution_timeout = 1920
devshard_escrow_params.default_inference_seal_grace_seconds = 3600
```

Nothing detects the mismatch on its own: `SessionConfig` is not part of the state root ([hash.go:38](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/devshard/state/hash.go#L38) folds balance, host stats, inferences, phase, warm keys, fees and version), so a config divergence only ever surfaces later as a root mismatch or a stuck vote.

Stands do change these values through governance — `RuntimeConfigTests.kt` bumps [refusal_timeout](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/testermint/src/test/kotlin/RuntimeConfigTests.kt#L416) and [execution_timeout](https://github.com/gonka-ai/gonka/blob/9d1f01472459f17b1516933951d2617027b0ad08/testermint/src/test/kotlin/RuntimeConfigTests.kt#L435) — so a non-default value is reachable in test environments before it is ever reachable in production.

## Origin

Commit `88ebd4456` (#1564) added `refusal_timeout = 17` / `execution_timeout = 18` to `inference/inference/devshard_escrow.proto` together with the gRPC-bridge mapping and `SessionConfigAtBind`, and touched neither `devshard/cmd/devshardd/bridge/chain.go` nor `devshard/storage/interface.go`. On the branch's merge base `379bebced638aeb5e6077bfd51c986f898443832` none of the three files mentions either field.

## Suggested fix

1. Copy both fields in `ChainBridge.GetEscrow` (`devshard/cmd/devshardd/bridge/chain.go:120`), mirroring `GRPCBridge`.
2. Add both to `storage.EscrowCacheInfo` and to both cache mappers (`EscrowCacheFromInfo` / `EscrowInfoFromCache`) — without this half, a bind served from the warm cache still loses them.
3. Consider a test that feeds one bridge's real `EscrowInfo` into the other's bind path and asserts field-for-field equality, since each side's tests build their own fixtures today.
4. Two related points worth deciding separately:
   - `devshard/user/httpsession.go:156` lets gateway-side configuration override both timeouts after the bind mapping, so the two sides can still be desynchronised by a flag once the bridge is fixed.
   - `devshard/docs/params-dataflow.md` is now stale on this: the lane A table (line 27) does not list the two fields, line 45 still files them under lane C as devshardctl-only, and line 52 says `SessionConfig` carries the defaults.

## Not checked

- No end-to-end run on a stand: the sealing divergence above is code reading plus arithmetic, not an observed root mismatch.
- Whether any escrow row already on mainnet carries non-zero values in fields 17/18 — the chain release carrying this proto is not what mainnet runs today.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a></span>
    <span class="issues-meta-item">commented 2026-09-13 03:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian yo, mind sanity-checking this one? tl;dr: the gateway's bridge maps <code>refusal_timeout</code>/<code>execution_timeout</code> off the escrow row, <code>devshardd</code>'s <code>ChainBridge</code> doesn't, so the host silently falls back to the compiled 60/1920 while the gateway runs the real governance values.</p>
<p>No-op on mainnet today purely because governance happens to sit exactly on the defaults — but bump <code>execution_timeout</code> to 1200 on a stand and the Finished clock gate goes 4800 (gw) vs 5520 (hosts), which is <code>post_state_root</code> mismatch territory plus timeout votes that never reach quorum. Repro output and line refs are in the body.</p>
<p>Fix looks like a two-liner in <code>chain.go</code>, but the warm cache is the other half (<code>EscrowCacheInfo</code> has no such columns) — would be great if you could eyeball whether that needs a schema bump/migration or just the mappers. Also flagged two adjacent things in there: the gateway-side override in <code>httpsession.go</code> and the now-stale lane tables in <code>params-dataflow.md</code>.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1762](https://github.com/gonka-ai/gonka/issues/1762) every hour.
