---
title: "#1689 — First full MNode image for Decode PoC (MiniMax): testing"
source: https://github.com/gonka-ai/gonka/issues/1689
issue_number: 1689
synced_at: 2026-09-06T14:13:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    First full MNode image for Decode PoC (MiniMax): testing
    <span class="issues-number">#1689</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:20 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-04 23:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
A full MLNode image for Decode PoC on MiniMax, with the current implementation verified. Collecting coefficients or thresholds is not acceptance.
Self-validation and cross-device validation must pass under every scenario below. They must not break when PoC, Decode PoC, and inference are combined.
Related: integration / design — #1688. DeepSeek thresholds and seeding — #1690.
Confirm live on-chain models from poc_params.models if the MiniMax id has drifted. Target model for this image: MiniMaxAI/MiniMax-M2.7.

**Process**
— Experiments completed and written up (hardware, models, what passed, what did not)
— MLNode starts and reaches a working state (does not crash on boot)
— Current Decode PoC implementation is tested against the matrix below, not only coefficients
— Image rechecked before handover
— If a scenario is skipped: notes before handover, with the reason

**Six steps**

1. Self-validation on one machine
Decode PoC validates against itself on a single host / GPU
2. Cross-device validation
Decode PoC validates across different hardware
3. Chain cycle: PoC starts, then PoC stops
— Cycle runs with no inference in the window — self-validation
— Cycle runs with no inference in the window — cross-device
— Cycle runs with inference in the window — self-validation
— Cycle runs with inference in the window — cross-device
4. Decode cycle: Decode PoC starts, then Decode PoC stops, then inference runs
— Decode ON → Decode OFF → inference — self-validation
— Decode ON → Decode OFF → inference — cross-device
5. Backward compatibility: old (prefill) PoC is turned on
— Old PoC still works after Decode PoC has been used — self-validation
— Old PoC still works after Decode PoC has been used — cross-device
6. Mix matrix: Decode PoC, old PoC, and inference, every combination 

**Static combinations**

- [ ] **1.** Old PoC on, Decode PoC off, Inference no — self
- [ ] **1.** Old PoC on, Decode PoC off, Inference no — cross-device
- [ ] **2.** Old PoC on, Decode PoC off, Inference yes — self
- [ ] **2.** Old PoC on, Decode PoC off, Inference yes — cross-device
- [ ] **3.** Old PoC off, Decode PoC on, Inference no — self
- [ ] **3.** Old PoC off, Decode PoC on, Inference no — cross-device
- [ ] **4.** Old PoC off, Decode PoC on, Inference yes — self
- [ ] **4.** Old PoC off, Decode PoC on, Inference yes — cross-device
- [ ] **5.** Old PoC on, Decode PoC on, Inference no — self
- [ ] **5.** Old PoC on, Decode PoC on, Inference no — cross-device
- [ ] **6.** Old PoC on, Decode PoC on, Inference yes — self
- [ ] **6.** Old PoC on, Decode PoC on, Inference yes — cross-device
- [ ] **7.** Old PoC off, Decode PoC off, Inference yes — self
- [ ] **7.** Old PoC off, Decode PoC off, Inference yes — cross-device
- [ ] **8.** Old PoC off, Decode PoC off, Inference no — self
- [ ] **8.** Old PoC off, Decode PoC off, Inference no — cross-device

Each row is a scenario. Both self-validation and cross-device must pass.
 
Scenario 8 is the idle baseline (both PoCs off, no inference). If it is not a meaningful run, that is stated in notes, and the row is still marked.

**Cycles (order matters)**

- [ ] **9.** Old PoC ON → Old PoC OFF, no inference in the window — self
- [ ] **9.** Old PoC ON → Old PoC OFF, no inference in the window — cross-device
- [ ] **10.** Old PoC ON → Old PoC OFF, inference in the window — self
- [ ] **10.** Old PoC ON → Old PoC OFF, inference in the window — cross-device
- [ ] **11.** Decode PoC ON → Decode PoC OFF → inference after — self
- [ ] **11.** Decode PoC ON → Decode PoC OFF → inference after — cross-device
- [ ] **12.** Decode PoC ON → Decode PoC OFF, no inference after — self
- [ ] **12.** Decode PoC ON → Decode PoC OFF, no inference after — cross-device
- [ ] **13.** Decode PoC used, then old PoC ON (backward compatibility) — self
- [ ] **13.** Decode PoC used, then old PoC ON (backward compatibility) — cross-device
- [ ] **14.** Old PoC ON → Decode PoC ON — self
- [ ] **14.** Old PoC ON → Decode PoC ON — cross-device
- [ ] **15.** Decode PoC ON → old PoC ON — self
- [ ] **15.** Decode PoC ON → old PoC ON — cross-device
- [ ] **16.** Both ON → Decode PoC OFF (old PoC remains) — self
- [ ] **16.** Both ON → Decode PoC OFF (old PoC remains) — cross-device
- [ ] **17.** Both ON → old PoC OFF (Decode PoC remains) — self
- [ ] **17.** Both ON → old PoC OFF (Decode PoC remains) — cross-device
- [ ] **18.** Inference → old PoC ON → old PoC OFF → inference — self
- [ ] **18.** Inference → old PoC ON → old PoC OFF → inference — cross-device
- [ ] **19.** Inference → Decode PoC ON → Decode PoC OFF → inference — self
- [ ] **19.** Inference → Decode PoC ON → Decode PoC OFF → inference — cross-device
 
**This image (MiniMax Decode PoC)**

- [ ] Full MLNode image tag published
- [ ] PoC (old and/or decode, as in the matrix) stays within the allowed memory budget
- [ ] Inference works on MiniMaxAI/MiniMax-M2.7 where the scenario includes inference
- [ ] Experiment notes attached (hardware for self, hardware pair for cross-device, logs / notebooks)
- [ ] Every scenario above is pass, fail, or skipped-with-reason

**Handover**

- [ ] Image tag published
- [ ] Matrix filled
- [ ] Limitations, if any, written in notes before handover
- [ ] The image is treated as delivered when this checklist is complete.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>TY!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/clanster">@clanster</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ty</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 23:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Dependency:</strong> blocked by <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a>. @tcharchian — this changes the ordering.</p>
<p><strong>Why</strong></p>
<ul>
<li>Acceptance here is the acceptance of a frozen algorithm: 19 scenarios, each in self-validation and cross-device validation. Cross-device results depend on every consensus constant (expert seeding, ladder base, artifact payload, admission behaviour) — a change after the run invalidates the whole matrix.</li>
<li>Two items on <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a> would still change those constants: whether the old prefill PoC stays behind a flag, and sign-off on the constants themselves (<a href="https://github.com/axeltec-gonka">@axeltec-gonka</a>, not given).</li>
<li>The image is built from <a href="https://github.com/gonka-ai/vllm/pull/100">gonka-ai/vllm#100</a> and <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/8">gonka-ai/gonka-vllm-plugins#8</a>; neither has landed in the intake branches.</li>
</ul>
<p><strong>Can run before that, as smoke rather than acceptance:</strong> image build, boot/crash checks, old PoC after Decode PoC (scenarios 13-17), ON/OFF cycles without inference.</p>
<p><strong>Next:</strong> smoke set starts after the <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/8">gonka-ai/gonka-vllm-plugins#8</a> refresh, 2026-09-05. The acceptance matrix is scheduled here the day <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a> closes. Status update every Monday, next 2026-09-07.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1689](https://github.com/gonka-ai/gonka/issues/1689) every hour.
