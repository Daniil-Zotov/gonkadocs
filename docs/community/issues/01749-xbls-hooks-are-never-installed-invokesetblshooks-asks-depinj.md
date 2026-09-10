---
title: "#1749 — x/bls hooks are never installed: InvokeSetBlsHooks asks depinject for a pointer the module never provides"
source: https://github.com/gonka-ai/gonka/issues/1749
issue_number: 1749
synced_at: 2026-09-10T21:41:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/bls hooks are never installed: InvokeSetBlsHooks asks depinject for a pointer the module never provides
    <span class="issues-number">#1749</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-09-10 14:30 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-10 19:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
The `x/bls` hooks are never installed in an app built through depinject, so both callbacks that the
bridge relies on have been dead in every build I can see. `AfterThresholdSigningFailed` never runs, so
the automatic refund of a bridge operation whose signing terminally failed never happens.
`AfterThresholdSigningCompleted` never runs either, so the pending-refund entry written for every
accepted bridge operation is never deleted and accumulates.

**The wiring.** The provider exports the keeper by value:

```go
// x/bls/module/module.go:214-218
type ModuleOutputs struct {
    depinject.Out
    BlsKeeper keeper.Keeper
    Module    appmodule.AppModule
}
```

The registered invoker asks for a pointer, and gives up quietly when it does not get one:

```go
// x/bls/module/module.go:243-249
func InvokeSetBlsHooks(
    keeper *keeper.Keeper,
    blsHooks map[string]types.BlsHooksWrapper,
) error {
    if keeper == nil || len(blsHooks) == 0 {
        return nil
    }
```

Nothing provides `*keeper.Keeper` anywhere in the module, and depinject requires an exact type match
while treating invoker dependencies as optional — an unsatisfied one arrives as nil and the invoker is
still called. So the guard returns, `SetHooks` is never reached, and `Hooks()` keeps returning the
empty `MultiBlsHooks{}` from `x/bls/keeper/keeper.go:69-74`. App construction succeeds with no error
and no log line.

**How I found it.** I was measuring how the bridge behaves when threshold signing fails. In a
500-block simulation run an accepted `MsgRequestBridgeMint` requested a signature at height 263, the
request retried twice on schedule (deadlines 273→283→293) and then failed with `deadline expired`,
which the chain logged itself. With an unconditional print as the first line of
`AfterThresholdSigningFailed` I got zero output across three runs of different lengths. Instrumenting
the invoker showed why: `keeper_nil=true num_hooks=1` — the inference hook is collected correctly,
there is simply nothing to install it on. The simulation app and `inferenced` both go through the same
`app.New` depinject path, so this is not sim-specific.

**What follows for a live chain.** A terminal signing failure leaves the escrowed value where it is
with no automatic refund; recovery then depends on someone sending `MsgCancelBridgeOperation`, which
still works for `FAILED`/`EXPIRED` requests. On the success side the pending entry simply stays. On the
public mainnet I count 852 threshold signing requests across epochs 278-389, all of them COMPLETED and
none failed — so no funds are stuck today, but each of those completions should have left an entry
that the dead cleanup hook never removed.

**Please do not bulk-process the accumulated entries when you fix the wiring.** This is the part I
would most like to flag. `ProcessAutoRefundForFailedBridgeOperation`
(`x/inference/keeper/bridge_pending_refund.go:187-218`) does not check the signing status itself — it
is safe only because its intended caller is the failure hook. A migration or cleanup job that walks the
pending maps and calls it would release escrow backing for operations that already completed, while the
wrapped tokens minted against that backing still exist on the destination chain. The escrow account
`bridge_escrow` currently holds about 1.85% of total supply, which bounds what such a sweep could
release. A safe migration can decode each key back to its BLS request id and use `GetSigningStatus`:
delete metadata only for `COMPLETED`, leave `FAILED`/`EXPIRED` for the existing cancellation path, and
quarantine anything unrecognised.

The sturdier version of that advice is to move the guard into the function rather than rely on callers
having it. The cancellation path already refuses a completed request
(`cancelThresholdSigningRequest`, `bridge_pending_refund.go:86-95`), and that single check is what
currently keeps escrow backing safe — including on the governance path, which may cancel someone
else's operation and redirect the refund to an arbitrary address through `OverrideRecipient`
(`msg_server_cancel_bridge_operation.go:72-79`). The auto-refund function has no such check of its
own. Putting a `GetSigningStatus` check for `FAILED`/`EXPIRED` inside
`ProcessAutoRefundForFailedBridgeOperation` would make its safety independent of who calls it, which
matters most for whatever tooling you write to clear the backlog.

**Fix.** The keeper's hook state is already pointer-backed (`hooksState *blsHooksState`, initialised in
`NewKeeper`) and you have a test that relies on copies sharing it, so the smallest change is to take
the keeper by value in the invoker. The alternative, and the more common shape in the SDK, is to export
`*keeper.Keeper` from `ModuleOutputs` the way `x/staking` does, though that one ripples into
`app.App.BlsKeeper` and the `depinject.Inject` call. Either way I would make the "hooks exist but no
keeper" case a construction error rather than a silent return.

**A test that would have caught it** has to run at app-construction level: build the app through
`app.New`, then assert `BlsKeeper.Hooks()` is not the empty implementation — ideally by calling
`AfterThresholdSigningCompleted` against app state and checking the pending entry is gone. The existing
keeper tests call `SetHooks` themselves in setup, which exercises the hook logic and by construction
cannot see that nothing installs it in a real app.

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bendrikoff">@bendrikoff</a></span>
    <span class="issues-meta-item">commented 2026-09-10 16:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi! I'm interested in implementing this.</p>
<p>I’d start with the minimal DI wiring fix and add an app-construction regression test to verify that the BLS hooks are actually installed.</p>
<p>Would you be okay with me picking this up?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-09-10 19:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the offer, but I'm going to take this one myself — the fix is ready on my side.</p>
<p>Both halves of your plan are already written out above: the wiring change (have the invoker take the keeper by value, or export <code>*keeper.Keeper</code> from <code>ModuleOutputs</code> the way <code>x/staking</code> does) and the app-construction test that asserts <code>BlsKeeper.Hooks()</code> is not the empty implementation.</p>
<p>What the plan leaves out matters more than the wiring. Once the hooks go live on a chain that has been accumulating pending entries for four and a half months, the failure hook reaches <code>ProcessAutoRefundForFailedBridgeOperation</code>, which does not check signing status. All 852 signing requests I counted on mainnet completed successfully, so those entries are exactly the ones a naive rollout would touch: their escrow backing would be released a second time while the wrapped tokens minted against it still exist on the destination chain. So this is three changes in a specific order: move the status guard inside the function, then wire the hooks, then decide what happens to everything already queued up. Only the middle one is small.</p>
<p>I'd rather wait for a maintainer to triage this before opening a PR — the question of what to do with the accumulated entries is theirs to answer.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1749](https://github.com/gonka-ai/gonka/issues/1749) every hour.
