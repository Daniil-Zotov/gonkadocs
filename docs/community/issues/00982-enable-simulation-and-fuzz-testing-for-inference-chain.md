---
title: "#982 — Enable simulation and fuzz testing for inference-chain"
source: https://github.com/gonka-ai/gonka/issues/982
issue_number: 982
synced_at: 2026-08-10T08:54:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Enable simulation and fuzz testing for inference-chain
    <span class="issues-number">#982</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/patimen">@patimen</a> opened 2026-03-30 21:41 UTC</span>
    <span class="issues-meta-item">7 comments</span>
    <span class="issues-meta-item">Updated 2026-06-06 08:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
# Proposal: Enable Cosmos SDK Simulation and Fuzz Testing for `inference-chain`

## Summary

`inference-chain` should make Cosmos SDK simulation and fuzz-style state exploration a near-term engineering priority.

For a Cosmos chain, this kind of testing is not just “more tests.” It is one of the main ways to pressure-test the chain as a state machine. The simulator repeatedly generates and executes randomized operations, feeds the application unexpected or adversarial sequences of state transitions, and helps expose invalid assumptions that are easy to miss in hand-written tests. Its purpose is to hammer chain state, explore weird edges, and discover cases where the application accepts bad transitions, enters inconsistent state, fails determinism, or breaks import/export assumptions.

Today, `inference-chain` has the app-level simulator wiring in place, but it does not yet have meaningful custom-module simulation coverage. As a result, one of the most valuable testing tools in the Cosmos SDK stack is largely unused for the logic that matters most.

This proposal recommends a focused effort to:

1. treat Cosmos SDK simulation as a chain-hardening priority,
2. make simulator runs easy to execute locally and in CI,
3. implement real simulation coverage for `x/inference` first,
4. expand coverage to other custom modules where it creates real value,
5. use repeated seeded runs to find edge cases, invalid states, and hidden assumptions.

## What Cosmos SDK Simulation and Fuzz Testing Is For

Cosmos SDK simulation exists to explore the behavior of a blockchain application under broad, randomized, and often ugly execution conditions.

Rather than proving one expected path, simulation asks a harder question: what happens when the chain is subjected to long sequences of randomized operations, odd ordering, unusual account selections, unexpected timing, and state transitions we would not think to hand-author in tests?

The purpose is to:

- generate large amounts of unusual but structurally valid activity,
- feed the application edge-case inputs and bad sequences of state transitions,
- stress interactions between modules over time,
- explore unusual parameter configurations and boundary values,
- reveal invalid assumptions about ordering, balances, epochs, or participant state,
- detect import/export and determinism issues,
- surface bugs that only appear after many steps of evolving chain state.

For a complex Cosmos application, this is one of the closest things we have to adversarial state-machine testing inside the normal SDK toolchain.

## Problem

`inference-chain` contains complex custom stateful logic, especially in `x/inference`. That logic spans multi-step workflows, participant lifecycle, epoch-based coordination, balances, rewards, validation, and cross-module interactions. These are exactly the kinds of features where bugs often emerge not from one message in isolation, but from the sequence and combination of many valid actions over time.

Unit tests and integration tests remain necessary, but they are not designed to broadly search for strange emergent behavior. They usually validate known scenarios. Simulation and fuzz-style state exploration exist to find the scenarios we did not already think of.

Without meaningful simulator coverage, we are more likely to miss:

- invalid state transitions that only show up after long chains of operations,
- combinations of valid messages that produce broken or inconsistent state,
- subtle cross-module regressions,
- bugs that only appear under unusual parameter values or combinations,
- edge cases around randomized accounts, ordering, and sequencing,
- failures in import/export or non-determinism under broader state exploration,
- assumptions in custom business logic that hold in example-based tests but not under sustained random execution.

The problem is not that the chain has no simulation support at all. The problem is that simulation is not yet doing the job it is supposed to do for the custom logic of the chain.

## Why This Should Be a Priority

This is a high-leverage hardening investment.

- It improves confidence in the correctness of the chain as a state machine, not just the correctness of isolated handlers.
- It helps us find cases where the chain accepts or produces invalid state under complex execution histories.
- It provides a repeatable way to stress workflows that are awkward to cover comprehensively with unit tests.
- It surfaces higher-order bugs earlier, before they become upgrade issues or production incidents.
- It creates a foundation for long-running automated and agent-assisted hardening work, since repeated seeded runs and simulator implementation are highly parallelizable.

In short, simulation matters because the chain’s biggest risks are not only “does this message work,” but also “what happens after many steps of valid and semi-adversarial state evolution.”

## Current State

`inference-chain` already has the base app-level simulator hooks in place:

- the app constructs a `SimulationManager`,
- app-level simulation tests exist for import/export, post-import simulation, and determinism,
- the standard Cosmos SDK simulator entrypoints are present.

However, the custom-module layer is still mostly scaffolding.

- `x/inference` registers many weighted operations, but the individual simulator implementations are currently stubs that return `NoOpMsg`,
- several other custom modules include simulation files but empty `WeightedOperations`,
- randomized genesis support is minimal,
- parameter-space exploration is minimal, especially for unusual runtime parameters and boundary combinations,
- store decoders are not implemented for the custom modules,
- simulator runs are not part of the normal developer or CI workflow.

The practical result is that simulation can be “enabled” without meaningfully hammering the custom business logic of the chain.

## Parameter Surface and Testing Strategy

One especially important area for this initiative is parameter variation.

For `inference-chain`, there are two parameter categories that should be treated differently:

- genesis-only parameters, which are fixed at genesis and cannot be changed later through governance,
- standard runtime parameters, which can be modified after chain start.

The primary fuzzing target in this proposal is the runtime parameter surface.

For `inference-chain`, risk does not only come from message execution under normal settings. It also comes from the space of possible runtime parameter values and combinations the chain may operate under. Some issues only appear when parameters are pushed toward edge values or when multiple parameters interact in surprising ways.

Genesis-only parameters should generally remain at the actual chain values during simulation and fuzz runs. They represent fixed operating assumptions of the network, and varying them freely would often reduce realism and produce lower-signal results. They should only be changed intentionally when there is a specific reason to believe that a genesis-only edge is needed to reach a meaningful correctness or security condition.

This matters because runtime parameter combinations can create correctness, safety, and vulnerability issues:

- parameter combinations may make previously safe logic unsafe,
- boundary values may expose arithmetic, sequencing, or liveness problems,
- modules may behave correctly under common settings but fail under extreme or merely less common ones.

As a result, simulation and fuzz-style testing should not only randomize operations. It should also intentionally explore runtime parameter edges and dangerous combinations where doing so produces meaningful signal.

This does not always mean forcing parameter changes through governance inside the simulation itself. In many cases, we can explore more of the runtime parameter state space by starting a simulation run with alternate initial values for parameters that are normally mutable at runtime. That gives us broader coverage without requiring every test path to first simulate a governance vote.

The intended strategy is:

- use the real genesis-only parameters by default,
- vary standard mutable parameters aggressively,
- allow alternate initial values for mutable parameters as a testing shortcut,
- use governance-driven parameter changes inside simulation only when the governance transition itself is the behavior under test.

## Proposal

We should adopt a phased plan that first makes simulation runnable and useful, then expands coverage in a disciplined way.

### Phase 1: Make Simulation Operational

Goal: make it easy for developers and CI to run a small simulation smoke test and a larger seeded run.

This phase should include:

- a documented command or Make target for a short simulator smoke run,
- a documented command for a longer seeded run,
- clear guidance on required flags and expected runtime,
- optional CI coverage for a short simulation run so the path does not silently rot.

This phase is about reliability and ergonomics, not depth of coverage.

### Phase 2: Implement Meaningful `x/inference` Simulation

Goal: make the simulator actually exercise the most important chain logic.

This should start with a deliberately chosen subset of operations that represent real workflows instead of trying to implement every message at once.

Recommended first-wave operations:

- `SubmitNewParticipant`
- `StartInference`
- `FinishInference`
- `Validation`
- `ClaimRewards`

Possible second-wave operations:

- `InvalidateInference`
- `RevalidateInference`
- training-task flows,
- selected admin or allow-list flows where they are central to system correctness.

This phase should also include helper logic for selecting valid accounts and valid preconditions so the simulator creates realistic messages rather than mostly generating invalid transactions.

### Phase 3: Improve Simulation Quality

Goal: move from “it runs” to “it finds real issues.”

This phase should include:

- tuning operation weights based on realistic workflow frequency and bug-finding value,
- using realistic genesis defaults by default, with targeted alternate initial states only where they improve coverage of mutable runtime parameter behavior,
- exploring parameter boundaries and parameter combinations more aggressively,
- deciding which mutable parameters should be varied by alternate initial values versus by in-simulation governance flows,
- implementing store decoders for clearer simulation diff output,
- adding invariants or strengthening existing ones where simulator findings justify it,
- running repeated seeded simulations and triaging recurring failures.

### Phase 4: Expand to Other Custom Modules Selectively

Goal: cover the rest of the chain where simulation adds meaningful value.

Not every module needs the same level of simulator depth. Some modules may justify only a small number of operations; others may not need much beyond genesis and invariants. The point is to make conscious choices rather than leaving default Starport scaffolding in place indefinitely.

## What Needs To Be Done

The work can be broken into concrete deliverables:

1. Simulator execution

- add local run targets,
- document short and long run modes,
- verify simulator runs complete in current developer environments.

2. `x/inference` operation implementation

- replace `NoOpMsg` stubs with real message generation and execution,
- build helper utilities for account and state selection,
- ensure operations honor message preconditions,
- keep the first set of operations intentionally small and high-value.

3. Debuggability and confidence

- add store decoders for custom modules,
- improve failure output and seed capture,
- define a strategy for runtime parameter variation,
- document that genesis-only parameters remain fixed by default, with targeted exceptions only where justified,
- define a catalog of mutable parameters that should be varied directly at simulation start for faster coverage,
- add targeted automated coverage for parameter edge cases and dangerous combinations,
- add guidance for replaying failing seeds locally.

4. CI and maintenance

- run a short smoke simulation in CI or another regular automation path,
- define ownership so simulator coverage grows with module changes,
- treat new major message flows as candidates for simulator support.

## Benefits

If we do this well, we should get several concrete benefits:

- higher confidence in custom state-machine correctness,
- earlier detection of regressions in long workflows,
- better confidence that unusual runtime parameter settings do not create unsafe or inconsistent chain behavior,
- broader runtime-parameter coverage without requiring every scenario to simulate governance first,
- better validation of import/export and determinism assumptions,
- stronger upgrade safety,
- a reusable framework for agent-assisted hardening and repeated stress runs,
- fewer blind spots in the chain’s most complex business logic.

## Scope and Non-Goals

This proposal does not recommend trying to implement every simulator operation immediately.

Non-goals for the initial effort:

- full coverage for every message in every module,
- perfect random genesis modeling on day one,
- using simulator implementation to change product semantics,
- treating simulator success as a replacement for unit, integration, or property tests.

The right first milestone is meaningful coverage for the most important workflows, not exhaustive completion.

## Risks and Tradeoffs

There are real tradeoffs to manage:

- poorly designed simulation operations can generate noise instead of signal,
- implementing too many operations too early can create maintenance burden,
- naive parameter randomization can create mostly invalid or low-signal runs if it is not constrained thoughtfully,
- varying genesis-only parameters too freely can pull testing away from the real chain assumptions and reduce signal,
- random exploration without good precondition logic may mostly hit invalid tx paths,
- long-running simulation in CI can become expensive if not scoped carefully.

These are manageable risks, and they argue for a phased rollout rather than against the effort itself.

## Success Criteria

We should consider this initiative successful when:

- a developer can easily run a short simulation smoke test locally,
- CI or another regular automation path exercises that smoke path,
- `x/inference` has a first meaningful set of real simulation operations,
- parameter-edge testing covers runtime params in a deliberate way,
- genesis-only parameters remain fixed by default, with exceptions only where they are intentionally justified,
- seeded simulation failures are reproducible and diagnosable,
- simulation results begin surfacing actionable bugs, invariants, or hardening work.

## Suggested Priority

This should be treated as a high-value engineering hardening initiative, with `x/inference` as the first target.

It does not need to block all other work, but it should be prioritized above lower-leverage test scaffolding because it directly improves confidence in the correctness of the chain’s stateful core.

## Proposed Next Step

Approve a first milestone focused on:

- simulator run ergonomics,
- a smoke run path,
- first-wave `x/inference` operation support,
- repeated seeded runs and triage.

That would give the project a practical starting point without overcommitting to a large one-shot implementation.

</div>

---

## 💬 Comments (7)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/hleb-albau">@hleb-albau</a></span>
    <span class="issues-meta-item">commented 2026-03-31 10:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>grabbing</p>
<p>Upd: still have problems with health, release grabbing :(
you can start from PR i done</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-08 09:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @patimen, I'd like to take this on.</p>
<p>Per @hleb-albau's release ("you can start from PR i done"), starting fresh from <code>main</code> rather than building on PR #995. That PR removes 3 upstream tests (<code>TestAppImportExport</code>, <code>TestAppSimulationAfterImport</code>, <code>TestAppStateDeterminism</code>) without restoring their semantics under simsx. Crediting Hleb for the Make-target naming and <code>fixBankGenesisState</code> helper.</p>
<p>Phased delivery to match the issue's "without overcommitting to a large one-shot implementation":</p>
<ul>
<li><strong>PR-A (Phase 1):</strong> simsx migration, smoke/full Make targets, disabled upstream ops (<code>staking</code>, <code>distribution</code>, <code>wasmd</code>), restored test semantics (<code>TestAppImportExport_Postrun</code>, <code>TestAppSimulationAfterImport_Postrun</code>, <code>TestAppStateDeterminism</code>), <code>docs/simulation.md</code>, optional manual-trigger CI workflow.</li>
<li><strong>PR-B (Phase 2):</strong> first-wave <code>x/inference</code> real ops via <code>HasWeightedOperationsX</code> — the 5 ops named in the issue (<code>SubmitNewParticipant</code>, <code>StartInference</code>, <code>FinishInference</code>, <code>Validation</code>, <code>ClaimRewards</code>).</li>
<li><strong>PR-C (Phase 3):</strong> weight tuning, custom invariants, parameter-edge fuzzing, store decoders.</li>
</ul>
<p>PR-A is locally complete; finalizing ai-reviewer pass before pushing. Will link the PR here once opened. Happy to adjust the phased split if you'd prefer a different structure.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-08 18:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Phase 1 PR opened: #1156. Scope is intentionally narrow ("make simulation runnable") so subsequent phases can land incrementally per the proposal; Phase 2 first-wave x/inference real ops to follow as a separate PR.</p>
<p>cc @patimen as the issue author for review and scope feedback.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-18 08:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Update: Phase 1 and Phase 2 are now combined in #1182, which supersedes #1156 (closed).</p>
<p>The comment above said Phase 2 would follow as a separate PR. Combining them instead matches the issue's "Proposed Next Step", which bundles run ergonomics and first-wave operation support into a single milestone — one self-contained, reviewable PR that exercises real <code>x/inference</code> logic rather than plumbing alone.</p>
<h1>1182 covers the 5 first-wave <code>x/inference</code> operations named in the issue (<code>SubmitNewParticipant</code>, <code>StartInference</code>, <code>FinishInference</code>, <code>Validation</code>, <code>ClaimRewards</code>) plus the runnable-simulation infrastructure. Phase 3 (second-wave ops, operation-weight tuning, custom invariants, parameter-edge fuzzing, store decoders) still follows as a separate PR.</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-22 14:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Phase 1 + 2 + 3 combined PR opened: #1228 (supersedes #1182, which is now closed).</p>
<p>Full local-verification milestone:
- <code>make sim-smoke-test</code> PASS — lifecycle <code>total=75 startProcessed=72 finishProcessed=62 validated=50 proposed=4</code>
- <code>make sim-full-test</code> PASS — height=501, opsCount=60763, deterministic app-hash, ≥12 epoch rotations
- Verified cross-compatible with <code>gm/microrelease</code> (v0.2.13 staging) — one adapter line for <code>NewEpochMemberFromActiveParticipant</code> signature change</p>
<p>V2 PoC chain factory family on cosmos-sdk simsx <code>HasFutureOpsRegistry</code>; sim-full surfaced two orthogonal <code>gonka-ai/cosmos-sdk</code> bugs both required for liveness — filed separately as #1205 and gonka-ai/cosmos-sdk PR #14.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-29 14:59 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status update — Phase 1–3 complete and assembled for review.</strong></p>
<p>The simulator now runs end-to-end and exercises real <code>x/inference</code> logic — and, the point of this issue, the seeded runs have <strong>surfaced several actionable bugs</strong>. Everything is assembled as focused, individually reviewable PRs.</p>
<p><strong>Main PR — #1228</strong> (Phase 1 + 2 + 3)
- <strong>Phase 1</strong>: simsx migration; <code>sim-smoke</code> / <code>sim-full</code> Make targets; restored <code>TestAppImportExport</code> / <code>TestAppSimulationAfterImport</code> / <code>TestAppStateDeterminism</code>; <code>docs/simulation.md</code>.
- <strong>Phase 2</strong>: first-wave real ops (<code>SubmitNewParticipant</code>, <code>StartInference</code>, <code>FinishInference</code>, <code>Validation</code>, <code>ClaimRewards</code>) + valid-precondition helpers; a V2 PoC-chain factory family so the validator set survives multi-epoch runs.
- <strong>Phase 3</strong>: custom invariants (incl. a <code>bank-backs</code> solvency invariant), store decoders, parameter-edge fuzzing, secondary-op factories, weight tuning.
- <strong>Verification</strong>: <code>sim-smoke</code> and <code>sim-full</code> (500×200, pinned GenesisTime) pass with a deterministic app-hash across ≥12 epoch rotations.</p>
<p><strong>Bugs the simulation surfaced — <code>x/inference</code></strong> (each filed narrowly, with a fail-without / pass-with reproducer):</p>
<table>
<thead>
<tr>
<th>Issue</th>
<th>What</th>
<th>Fix</th>
</tr>
</thead>
<tbody>
<tr>
<td>#1265</td>
<td>Stuck <code>VOTING</code> inferences orphan client escrow when x/group proposals miss quorum</td>
<td>PR #1275</td>
</tr>
<tr>
<td>#1269</td>
<td>Revalidation vote fails when the voter is absent from the epoch x/group</td>
<td>PR #1276</td>
</tr>
<tr>
<td>#1273</td>
<td>Asymmetric debit in <code>refundInvalidatedInference</code> (left as a design question, not patched)</td>
<td>—</td>
</tr>
</tbody>
</table>
<p><strong>Most severe — a chain halt in the <code>cosmos-sdk</code> fork.</strong> <code>sim-full</code> deterministically halted: <code>markValidatorForDeletion</code>'s jailed branch deletes a validator's record while its votes are still inside CometBFT's validator-update lag, so <code>slashing.BeginBlocker</code> fails with <code>ErrNoValidatorFound</code>. Reported as #1205 and fixed in <strong>gonka-ai/cosmos-sdk#16</strong>, which also resolves a non-jailed <code>DelegatorShares</code> divide-by-zero in the same function. Worked through in the <strong>cosmos-sdk#14 thread with @0xgonka</strong> (GON-191 author): the two fixes are orthogonal — different functions — but both are needed for staking liveness, so #16 is complementary to #14 (cc gmorgachev as the fork maintainer / author of <code>markValidatorForDeletion</code>).</p>
<p><strong>Phase 4</strong> (selective simulation coverage of the other custom modules) can follow as a separate effort if useful — happy to scope it on request.</p>
<p>@patimen — whenever you have bandwidth, I'd really appreciate a review of #1228 and any scope feedback. No rush, and happy to restructure the phase split if you'd prefer.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-06-06 08:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>A second staking-liveness halt — surfaced running the sim on <code>#14 + #16</code>.</strong></p>
<p>Building the suite on a fork with both fork PRs applied (<code>#14</code> GON-191 + <code>#16</code> <code>markValidatorForDeletion</code>), the multi-seed sweep still halted: <strong>27 / 37 seeds</strong> with <code>block finalization failed: validator does not exist</code>.</p>
<p>It is distinct from the <code>markValidatorForDeletion</code> halt (<code>#16</code>): GON-191's stale-validator cleanup is a <em>different</em> deletion path, also with no unbonding period, so evidence/slashing <code>BeginBlock</code> looks up a just-deleted validator and <code>ValidatorByConsAddr</code> returns <code>ErrNoValidatorFound</code> before either consumer's existing graceful <code>nil</code> branch can run. A small, self-contained fix — return <code>(nil, nil)</code> on not-found — takes the sweep <strong>27 / 37 → 0 / 37</strong>.</p>
<p>Full root-cause + diff in the cosmos-sdk#14 thread: https://github.com/gonka-ai/cosmos-sdk/pull/14#issuecomment-4637525807</p>
<p>Net: staking liveness under the PoC delete-immediately model needs both <code>#16</code> (the <code>markValidatorForDeletion</code> paths) and this <code>ValidatorByConsAddr</code> contract fix, which is robust against any deletion path including GON-191.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #982](https://github.com/gonka-ai/gonka/issues/982) every hour.
