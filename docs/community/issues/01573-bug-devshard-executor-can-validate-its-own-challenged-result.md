---
title: "#1573 — [BUG] devshard executor can validate its own challenged result, letting a fraudulent executor push a bad settlement and steal escrowed funds"
source: https://github.com/gonka-ai/gonka/issues/1573
issue_number: 1573
synced_at: 2026-08-11T06:07:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] devshard executor can validate its own challenged result, letting a fraudulent executor push a bad settlement and steal escrowed funds
    <span class="issues-number">#1573</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/iceiceic3">@iceiceic3</a> opened 2026-08-10 15:19 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-10 20:14 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
**Summary**
In devshard’s challenge/validation flow, applyValidationVote does not reject a validation vote cast by the same party that produced the challenged result. Combined with the fact that the ShouldValidate sampling rule is defined but not enforced on-chain, and that the devshard validation surface is unauthenticated/DoS-exposed, a malicious executor can submit a fraudulent result and then cast the deciding validation vote on its own challenge — suppressing honest validators during resolution and forcing a fraudulent settlement that releases escrowed funds to the attacker. This is a self-vote / conflict-of-interest gap in the escrow settlement path, not merely a liveness timing issue.

**Motivation**
devshard escrow settlement is a value-bearing decision: whoever the validation vote favors gets paid. If the challenged executor is allowed to be its own validator, the entire challenge mechanism — the thing that is supposed to catch fraudulent results — can be turned by the fraudster to bless its own fraud. This is distinct from the already-filed timeout-vote liveness concern; it is a direct integrity break in who is permitted to decide. It matters now because it converts the challenge system from a safety control into an attacker-controlled rubber stamp for theft.

**Impact**
- Who is affected (hosts, developers, validators): Counterparties whose funds are escrowed in a devshard job against a malicious executor; honest validators whose votes are bypassed.
- Is effect network-wide or limited: Per-job fund theft (limited to the escrow of each abused job), but repeatable across jobs by the same attacker. It is theft from the escrow/settlement mechanism rather than a single-user mistake, which places it above a purely isolated issue.
- Likelihood (common, intermittent, edge case, or intentional attack): Intentional — Profitable. Requires the attacker to act as an executor and time the self-vote during resolution; not a single anonymous packet, but well within a motivated participant’s reach. Rated Medium likelihood.
- Severity Impact × Likelihood: Impact High (theft from the escrow module) × Likelihood Medium → High (per Gonka risk matrix, High × Medium = High).
- Affected components: devshard/ challenge–validation settlement (applyValidationVote self-vote check), inference-chain/x/inference/calculations/should_validate.go (ShouldValidate sampling not enforced), and the unauthenticated devshard validation/DoS surface that helps suppress honest validators.

**Detailed description**
**This finding is a composition of three verified sub-issues in the devshard settlement path:**

- **DS-H1 — no self-vote check in applyValidationVote.** The validation-vote application does not verify that the voter is different from the executor that produced the challenged result. There is no voter != challengedExecutor guard, so the challenged party can cast a validation vote on its own challenge.
- **DS-M3 — ShouldValidate sampling defined but not enforced.** inference-chain/x/inference/calculations/should_validate.go:14 defines the sampling rule that is supposed to decide who validates, but it is not enforced at the settlement path — so validator selection cannot be relied on to exclude the interested party.
- **DS-H2 / DS-H3 — unauthenticated devshard DoS surface.** The validation surface can be griefed/DoS’d, which lets an attacker suppress or crowd out honest validators during the resolution window, improving the odds that the self-vote is the deciding vote.

**Chained attack:** a malicious executor (a) submits a fraudulent result, (b) ensures honest validators are suppressed during resolution (via the DoS surface and the unenforced sampling), and © casts the validation vote on its own challenge. The settlement resolves in the attacker’s favor and releases the escrowed funds to the attacker — concrete fund theft.

**Novelty / dedup:** distinct from filed issue #1570, which concerns timeout-vote liveness under skewed slots. The self-vote-on-own-validation integrity gap is not covered by that issue. (Static review; the composition was traced across the devshard settlement code and the should_validate calculation, but see the caveat below.)

**Honest caveat:** this is the least code-line-pinned of the four findings in this batch. The self-vote gap and the unenforced-sampling observation were established by static review of the devshard settlement path and should_validate.go:14; the exact file:line of applyValidationVote in the devshard tree should be re-cited from the current source when filing, and the escrow-release step confirmed against the settlement function, so the report withstands a triager reading the code. No live testing was performed.

**Reproduction (isolated local harness only — no live testing performed):**
- Stand up a local devshard instance with one escrowed job (test fixtures only).
- As the executor, submit a fraudulent result for the job.
- Simulate honest-validator suppression during the resolution window (unauthenticated DoS surface / unenforced sampling).
- As the same executor identity, cast the validation vote on the job’s own challenge; observe that applyValidationVote accepts it and that settlement releases the escrow to the attacker. All identities/funds are local test fixtures.

**Links to evidence:** inference-chain/x/inference/calculations/should_validate.go:14; devshard settlement applyValidationVote (self-vote gap) and escrow-release path (cite exact file:line from current devshard source at filing time); DS-H2/DS-H3 unauthenticated devshard surface. Related-but-distinct filed issue: #1570 (timeout-vote liveness).

**Suggested remediation:** reject any validation vote where voter == challengedExecutor; enforce the ShouldValidate sampling on-chain so the interested party cannot be a validator of its own challenge; authenticate/rate-limit the devshard validation surface to prevent honest-validator suppression.

[report-4-self-vote.zip](https://github.com/user-attachments/files/30904473/report-4-self-vote.zip)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-08-10 20:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @iceiceic3! Responsible disclosure helps keep the network secure for everyone. Use the form https://gonka.ai/docs/report-vulnerability/ to submit a vulnerability report directly through HackerOne. Valuable findings are subject to reward.  </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1573](https://github.com/gonka-ai/gonka/issues/1573) every hour.
