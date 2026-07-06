---
title: "#424 — Privacy and Reliability: IP-layer denials, TLS termination, on-chain prompt exposure, and faster mitigation of unreliable hosts"
source: https://github.com/gonka-ai/gonka/issues/424
issue_number: 424
synced_at: 2026-07-06T09:53:37Z
---

> 🔄 **Авто-синхронизация:** из [Issue #424](https://github.com/gonka-ai/gonka/issues/424) каждые 6 часов. 

# 🟢 Privacy and Reliability: IP-layer denials, TLS termination, on-chain prompt exposure, and faster mitigation of unreliable hosts

**Автор:** [@vvv-tech](https://github.com/vvv-tech) · **Состояние:** Open · **Создано:** 2025-11-10 12:43 UTC · **Обновлено:** 2025-11-10 12:43 UTC

---

## 📝 Описание

### Summary
- Transfer Agents (TAs) can deny requests at the IP layer (e.g., Nginx) without protocol penalties, hurting availability.
- TLS terminates on hosts; plaintext is visible at the host and intra-node hops. No true end-to-end client→executor encryption by default.
- Original prompt payloads are stored on-chain in Start/Finish messages, exposing sensitive content.
- Unreliable hosts degrade UX immediately; invalidation/exclusion improves things over time but needs faster detection and routing away.

### Why this matters
- Privacy risk: plaintext visibility and immutable on-chain prompt content.
- Reliability risk: a modest fraction of unreliable TAs/executors can produce high failure rates. If fTA is the TA deny fraction and fEXE is executor failure fraction, P(fail) = 1 − (1 − fTA)(1 − fEXE). ≥50% failures if fTA≥50% or fEXE≥50%; if fTA≈fEXE, then f≥1−√0.5≈29.3%.

### Evidence and related work
- Invalid/Inactive participant handling (SPRT-based status, exclusion list, slashing dedupe) — helps prune bad actors over time: [PR #407](https://github.com/gonka-ai/gonka/pull/407).
- Faster resilience to unreliable nodes (assume FAILED on status errors, retries for LockNode, health-check timeouts/debounce, don’t send to inactive nodes, clearer errors) — improves short-term routing/selection behavior: [PR #408](https://github.com/gonka-ai/gonka/pull/408).

### Problems observed
- Privacy
  - TLS termination on hosts → host can see plaintext; intra-node HTTP by default.
  - On-chain storage of `OriginalPrompt` in `MsgStartInference`/`MsgFinishInference`.
  - Potential logging of bodies unless explicitly disabled.
- Reliability
  - TA can IP-block/deny without immediate protocol-level penalty.
  - Users experience failures before invalidation/exclusion takes effect.
  - Selection may briefly include nodes that recently turned unhealthy unless actively filtered.

### Proposed remediations
- Privacy
  - End-to-end transport security: require TLS from clients to TA and mTLS TA→executor; prefer TLS passthrough to executor where feasible. Bind TA’s HTTP listener to loopback/unix socket.
  - On-chain data minimization: remove/stage-gate `OriginalPrompt`; store only `PromptHash`/commitment. If needed, support optional encrypted payload (hybrid encryption with requester pubkey) and off-chain reveal.
  - Logging and retention: default to body redaction; explicit config gates for sampling.

- Reliability and incentives
  - Telemetry and fast-path routing: export TA refusal/timeout metrics; add synthetic probes from multiple vantage points; immediately route away from unhealthy/unresponsive nodes.
  - Selection weighting and penalties: weight random executor selection by recent success/refusal rates; temporarily exclude high-deny nodes within the epoch; incorporate reputation impact.
  - Client-visible failover: circuit-breaker at TA with immediate retry to another executor/TA (bounded backoff).
  - Integrate and extend recent stability work: build on [PR #408](https://github.com/gonka-ai/gonka/pull/408) (lock retries, FAILED on status errors, health-check timeouts, debounce; “don’t send to inactive nodes”) to reduce time-in-pool for flaky nodes.

### Quick wins
- Disable on-chain storage of raw `OriginalPrompt` by default; keep only `PromptHash`. Optionally allow encrypted payload.
- Enforce mTLS TA→executor; keep TA HTTP on loopback/unix socket only.
- Expose TA refusal/timeout metrics and incorporate into selection scoring.
- Add immediate lock-retry and clearer “no nodes available” paths; align with [PR #408](https://github.com/gonka-ai/gonka/pull/408).

### Acceptance criteria
- No plaintext over untrusted links: TLS to TA; mTLS TA→executor; no intra-node plaintext exposure.
- Chain no longer stores raw prompt content by default; only hashes/commitments (or encrypted payloads).
- TA refusal/timeout telemetry drives selection/exclusion automatically; repeated offenders excluded within the epoch per policy.
- Documentation updates for operators (TLS/mTLS setup, Nginx hardening, logging redaction) and governance params.

### Open questions
- Default client-side encryption for prompts (public-key bootstrap) to decouple privacy from infra?
- Acceptable false-positive rate for quick exclusions; guardrails against adversarial probing?
- Migration path for legacy clients relying on on-chain prompt payloads?

Status reference
- Reliability hardening and faster node health reaction: [PR #408](https://github.com/gonka-ai/gonka/pull/408).
- Invalidation/exclusion, SPRT-based status, slashing dedupe: [PR #407](https://github.com/gonka-ai/gonka/pull/407).
