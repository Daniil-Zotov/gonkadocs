---
title: "#546 — Node crash: Decimal precision panic in reputation calculation (v0.2.7-post1)"
source: https://github.com/gonka-ai/gonka/issues/546
issue_number: 546
synced_at: 2026-07-10T18:52:30Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Node crash: Decimal precision panic in reputation calculation (v0.2.7-post1)
    <span class="issues-number">#546</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@Olena](https://github.com/Olena) opened 2026-01-12 10:29 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-01-21 21:11 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Node crash: Decimal precision panic in reputation calculation (v0.2.7-post1)
Summary
Node running v0.2.7-post1 crashes with decimal precision panic during reputation calculation in the x/inference module, despite the BLS decimal precision fix included in this release. This indicates the v0.2.7-post1 fix is incomplete and does not cover all decimal precision issues.

Environment
Node Version: inferenced:0.2.7-post1
Image SHA: sha256:9af277c0e464 (created 2026-01-08T20:35:33Z)
Account: gonka1547gss5hs48tg024zg7cm3f4r747a8ed0mrgru
Hardware: H100 GPU node
OS: Ubuntu (Docker)

Error Details
Panic Message
panic: value '0.032335451875111843916048462901' exceeds max precision by -12 decimal places: max precision 18

Value Analysis:

Calculated value has 30 decimal places
Cosmos SDK LegacyMustNewDecFromStr max: 18 decimal places
Overflow: 12 decimal places

Crash Context
[90m9:22AM[0m [32mINF[0m ReputationCalculated module=x/inference participantIndex=gonka1zzkxnpq2txntwh5eu49jk67x42yh8wystnkamy reputation=100 subsystem=EpochGroup

[90m9:22AM[0m [32mINF[0m Adding member address=gonka1zzkxnpq2txntwh5eu49jk67x42yh8wystnkamy models=["Qwen/Qwen3-235B-A22B-Instruct-2507-FP8"] module=x/inference weight=6357

[90m9:22AM[0m [32mINF[0m Closing application.db module=baseapp

[90m9:22AM[0m [32mINF[0m Closing snapshots/metadata.db module=baseapp

panic: value '0.032335451875111843916048462901' exceeds max precision by -12 decimal places: max precision 18

goroutine 1 [running]:

cosmossdk.io/math.LegacyMustNewDecFromStr(...)

	/go/pkg/mod/cosmossdk.io/math@v1.5.3/legacy_dec.go:212

github.com/productscience/inference/x/inference/module.ApplyBLSGuardianSlotReservation(...)

Location:

Module: x/inference
Subsystem: EpochGroup
Operation: ReputationCalculated + Adding member
Affected participant: gonka1zzkxnpq2txntwh5eu49jk67x42yh8wystnkamy

Crash Occurrences
First crash: ~2026-01-01 at block 2,059,054
Second crash: 2026-01-12 at block 2,104,716

Both crashes occurred during epoch transitions when reputation calculations are performed.

Root Cause Analysis
Known v0.2.7-post1 Fix (Incomplete)
The [v0.2.7-post1 release notes](https://github.com/gonka-ai/gonka/releases) state:

"Fix for BLS to prevent consensus panic from decimal precision overflow. shopspring/decimal divisions can produce >18 decimal places, causing LegacyMustNewDecFromStr to panic in ApplyBLSGuardianSlotReservation."

Issue: This fix only addresses ApplyBLSGuardianSlotReservation, but the panic occurs in reputation calculation during epoch group operations.

Affected Code Paths (Not Fixed)
The following operations in x/inference still produce >18 decimal precision:

❌ Reputation calculation (ReputationCalculated)
❌ Weight assignment in epoch groups
❌ Member addition to sub-groups
✅ ApplyBLSGuardianSlotReservation (fixed in v0.2.7-post1)

Impact
Severity: Critical - Complete node crash
Frequency: During epoch transitions
Downtime: ~1 hour (state sync recovery required)
Data Loss: None (blockchain state recoverable)
Scope: Affects nodes at specific block heights where calculations overflow

Reproduction Steps
Run node with inferenced:0.2.7-post1
Sync to block height where reputation calculation for specific participants triggers
Epoch transition executes reputation calculation
Calculation produces value with >18 decimal precision
LegacyMustNewDecFromStr panics
Node crashes and enters restart loop

Current Workaround
State Sync Recovery:

# 1. Stop crashed node

docker compose stop node

# 2. Clean corrupted data

rm -rf .inference/data .inference/wasm

mkdir -p .inference/data

# 3. Update state sync trust parameters

# (Use recent height - 2000 and corresponding hash)

# 4. Restart node - syncs past problematic blocks

docker compose start node

Recovery Time: 30-45 minutes via state sync

Proposed Solution
Immediate Fix Needed
Apply the same decimalToLegacyDec() pattern from the BLS fix to ALL decimal operations in x/inference:

// Helper function (from v0.2.7-post1 BLS fix)

func decimalToLegacyDec(d decimal.Decimal) sdk.Dec {

    // Truncate to 18 decimal places before conversion

    str := d.StringFixed(18)

    dec, err := sdk.NewDecFromStr(str)

    if err != nil {

        // Handle error gracefully

    }

    return dec

}

Apply to:

Reputation calculations in EpochGroup
Weight assignments
Reward distributions
Any other LegacyMustNewDecFromStr conversions

Comprehensive Audit Needed
Full x/inference module audit for all decimal operations
Add validation before legacy dec conversion
Regression tests for all precision-sensitive operations
Graceful error handling instead of panics

Testing
Unit tests with >18 decimal precision values
Integration tests during epoch transitions
Test with actual participant data that triggered crashes

Recommendations
For v0.2.8 Release
Complete decimal precision audit of x/inference module
Apply StringFixed(18) truncation universally
Add pre-conversion validation
Comprehensive testing of reputation calculations
Network-wide upgrade with fix

For Node Operators
Until v0.2.8 is released:

Implement automated health monitoring
Use state sync recovery on crashes
Report additional crash occurrences to help identify edge cases

Additional Context
Related Issues:

v0.2.7-post1 BLS fix (partial solution)

Related Documentation:

[Cosmos SDK Decimal Precision](https://docs.cosmos.network/main)
[Gonka Tokenomics](https://github.com/gonka-ai/gonka/blob/main/docs/tokenomics.md)

Stack Trace Location:

cosmossdk.io/math.LegacyMustNewDecFromStr

github.com/productscience/inference/x/inference/module

Request
Please release v0.2.8 with a complete fix covering all decimal precision issues in the x/inference module, not just ApplyBLSGuardianSlotReservation.

Happy to provide additional logs, debugging assistance, or test the fix before release.



Reporter: Node operator with detailed logs and crash dumps available Status: ⚠️ Production node affected, automated recovery in place
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@patimen](https://github.com/patimen)</span>
    <span class="issues-meta-item">commented 2026-01-12 18:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Can you provide a full stack trace for the panic? I do not see any remaining uses of LegacyMustNewDecFromStr.
For most of the chain, we <em>only</em> use <code>shopspring</code> decimals, not Legacy. In fact, I cannot find places where we use it outside of BLS and chainvalidation.go (and there for only one value quickly)</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-01-21 19:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Olena please take a look at the question above.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@gmorgachev](https://github.com/gmorgachev)</span>
    <span class="issues-meta-item">commented 2026-01-21 21:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The log above contains exact issue from <code>ApplyBLSGuardianSlotReservation</code> (0.032335451875111843916048462901 is exact number and error which was in initial issues)
=&gt; with high probability it's not another issue
If it'd be one more issue in inference module, the whole chain would halt. I assume 0.2.7 binary was used (e.g. <code>.inference/cosmovisor</code> directory was recreated or symlinks inside modified)</p>
<p>Closing if there is no new info</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #546](https://github.com/gonka-ai/gonka/issues/546) every hour.
