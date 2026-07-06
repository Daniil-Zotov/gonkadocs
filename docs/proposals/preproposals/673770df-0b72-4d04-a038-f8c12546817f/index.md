---
title: "Universal Continuous GPU Benchmark for Gonka Hosts (vLLM v0.19+, Anti-Sybil)"
template: proposals-main.html
---

# Universal Continuous GPU Benchmark for Gonka Hosts (vLLM v0.19+, Anti-Sybil)

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🟢 Active</div>

**Author:** Evgenii Maksimenkov
**Created:** 2026-04-25 06:31 UTC
**Closes:** 2026-07-24 06:31 UTC
**Language:** EN
**Votes:** 4
**Avg. Bid:** 2.7M GNK

</div>

Develop a vLLM v0.19+ universal GPU benchmark that runs continuously during the epoch without interrupting inference, fairly scores any model size, and is hardened against hot-plug and Sybil attacks.

---

## Full Proposal

Context

Gonka measures Host compute capacity via Proof of Compute (PoC) Sprints. The current Sprint model concentrates measurement into a short synchronized window, which (a) creates a measurable inference-revenue gap during the Sprint and (b) opens a surface for "burst attacks" — Hosts attaching extra GPUs only for the Sprint window and detaching them afterwards.

This tender procures a **universal, continuous GPU benchmark** that runs throughout the epoch on the Host's actual production inference stack (vLLM v0.19+), produces a verifiable per-GPU compute score, and is robust against hot-plug, Sybil, and replay attacks.

The deliverable replaces (or supplements, subject to governance) burst-style Sprint scoring with a continuously-sampled metric that cannot be gamed by transient hardware, while preserving existing PoC validation properties (randomized verification, on-chain artifacts, slashing).

## 2. Scope of Work

The Contractor shall design, implement, test, document, and upstream a benchmark subsystem (hereinafter — *the Benchmark*) consisting of:

1. A **measurement agent** integrated into the ML Node, running alongside vLLM serving.
2. An **on-chain attestation protocol** for submitting and verifying samples.
3. A **scoring function** producing per-Host weight inputs consumable by the existing PoC pipeline.
4. A **reference verifier** runnable by any Host to independently re-check published artifacts.
5. **Operator tooling, dashboards, and full test/CI coverage.**

## 3. Functional Requirements

### 3.1. Continuous, Non-Interrupting Operation

- The Benchmark MUST run as a persistent workload throughout the epoch (17280 blocks, ~24h), not as a discrete Sprint window.
- The Benchmark MUST NOT pause, drain, or evict active inference requests. p99 inter-token latency degradation on the served production model MUST NOT exceed **3%** versus a clean baseline measured under identical concurrency.
- The Benchmark MUST integrate with vLLM v0.19+ scheduler hooks (continuous batching, chunked prefill, prefix caching) and submit its workload as **first-class requests through the same engine** — not via a parallel CUDA context that would distort accounting.
- KV cache pressure introduced by the Benchmark MUST be bounded by an operator-configurable ceiling (default: ≤5% of `gpu_memory_utilization`).
- The Benchmark MUST yield CPU/GPU resources to user-paid inference under load (configurable QoS class; default: lower priority than paid traffic, higher than idle).

### 3.2. Universality Across Models

- The Benchmark MUST produce comparable scores **independent of the model the Host currently serves**, including but not limited to: Qwen3-235B-A22B-Instruct-2507-FP8, dense models in the 7B–70B range, and MoE models with active-parameter counts from 7B to 50B+.
- Scoring MUST normalize across: dense vs. MoE architectures, FP8 / BF16 / FP16 / INT8 precisions, single-GPU and tensor-parallel (TP=2/4/8) and pipeline-parallel deployments, NVLink and PCIe interconnects.
- The Benchmark MUST define a canonical **reference workload**: a fixed set of synthetic transformer micro-tasks (attention, MLP/MoE routing, all-reduce, prefill, decode) executed on a **canonical Sprint-style transformer with randomized layer transformations** seeded by on-chain randomness, identical for every Host in a given measurement window.
- Score units MUST be expressed in **AI Tokens per second per GPU-equivalent**, calibrated so that hardware tiers (e.g., A100 80GB, H100, H200, RTX PRO 6000 Blackwell, MI300X) map to a stable, monotonic ranking across the supported model spectrum.

### 3.3. Sampling and Randomization

- Each epoch MUST contain **N ≥ 64 micro-measurements per GPU**, scheduled at **unpredictable times** derived from a VRF over `(epoch_seed, host_address, gpu_uuid)`.
- The exact start time, duration, seed, model permutation, and input nonces of each micro-measurement MUST NOT be predictable by the Host more than **one block (~5s)** in advance.
- Micro-measurement duration MUST be bounded (target: 200ms–2s) so that no single measurement materially affects served latency, while N samples aggregate to a low-variance epoch score (target: per-Host score CoV ≤ 2% across 3 consecutive honest epochs on identical hardware).

## 4. Security Requirements

### 4.1. Anti-Hot-Plug / Anti-Burst Hardware Attack

- The Benchmark MUST detect and penalize Hosts that add GPUs only for measurement windows. Required mechanisms:
  - **Continuous GPU presence attestation**: each declared GPU MUST report a signed heartbeat at least once per **30s**, including `gpu_uuid`, `pci_bus_id`, `nvml_serial`, `vbios_version`, `driver_version`, current power draw, current SM clock, current memory clock, ECC error counters, and a monotonic uptime counter sourced from the device.
  - GPUs that miss more than **0.5% of heartbeats per epoch** MUST be excluded from the epoch score for that Host.
  - **Hardware fingerprint binding**: a GPU's contribution to the epoch score MUST be discounted by `min(1, observed_uptime_in_epoch / required_uptime)` where `required_uptime` ≥ 95% of the epoch.
  - **Cross-Host fingerprint deduplication**: the same `nvml_serial` / `vbios` / `pci` triple appearing on two Hosts within a rolling 7-epoch window MUST trigger automatic disqualification of both Hosts pending governance review.

### 4.2. Anti-Sybil and Anti-Replay

- All measurement inputs MUST be derived from on-chain VRF output; a Host cannot precompute outputs.
- All measurement outputs MUST be committed via `(commit, reveal)` with a commit deadline ≤1 block after measurement and reveal ≤2 blocks after commit. Late reveals MUST be rejected.
- Replay of a previous epoch's outputs MUST be detectable via VRF binding to `(epoch_id, block_height, gpu_uuid)`.
- **No-mock guarantee**: the Benchmark workload MUST share weights, KV cache, and CUDA streams with the production vLLM engine, so substituting a synthetic high-throughput kernel for the real one is detectable via cache-coherency and timing-side-channel signatures.

### 4.3. Anti-Outsourcing

- Sample latency MUST be measured **end-to-end inside the Chain Node**, not self-reported by the ML Node, with RTT bounds enforced (default: ≤50ms intra-Host, configurable). This makes it economically irrational to forward measurement workloads to a remote GPU farm.
- Optional TEE attestation (SEV-SNP, TDX, or NVIDIA H100/H200 Confidential Computing) SHOULD be supported as a verification booster (higher Confirmation Ratio for TEE-attested Hosts).

### 4.4. Statistical Validation Compatible with Existing PoC

- Verification MUST follow Gonka's existing **statistical (non-bitwise) validation** model: a Validator Host re-runs a random subset (1–10% per Reputation tier) of the Executor's micro-measurements and accepts results within a defined tolerance band (e.g., logits L2 distance ≤ ε, throughput within ±5% of declared).
- Cheating detection MUST trigger the existing slashing path: full epoch reward forfeiture for the offending Host.

## 5. Technical Requirements

| Area | Requirement |
|---|---|
| Language | Python 3.11+ for agent; Go for Chain Node integration; Rust acceptable for hot-path kernels |
| Runtime | vLLM v0.19+, CUDA 12.4+, NCCL 2.21+, PyTorch 2.4+ |
| GPUs | NVIDIA Ampere/Hopper/Blackwell (A100, H100, H200, B200, RTX PRO 6000 Blackwell); AMD MI300X support as stretch goal |
| Interconnects | NVLink 3/4/5, NVSwitch, PCIe Gen4/Gen5, InfiniBand HDR/NDR |
| Orchestration | Docker + docker-compose parity with existing `inference-ignite` deployment; optional Kubernetes Helm chart |
| Observability | Prometheus metrics, structured JSON logs, OpenTelemetry traces; Grafana dashboard with per-GPU score, heartbeat status, sample histogram |
| Config | All thresholds (heartbeat interval, uptime floor, KV ceiling, QoS class, sample count) MUST be governance-tunable parameters, not compile-time constants |
| API | OpenAI-compatible inference path MUST remain unchanged externally; new `/poc/continuous/*` endpoints exposed on the API Node |
| Determinism | Reference workload MUST be reproducible with `seed`, `top_logprobs`, and batch-invariant kernels enabled; tolerance bands documented per kernel |

## 6. Deliverables

1. **Source code** in the `gonka-ai/gonka` GitHub organization, dual-licensed compatible with the Gonka Protocol License, with ≥85% unit test coverage on the agent and ≥70% on Chain Node integration.
2. **Reference Docker images** published to a public registry, signed with cosign.
3. **Whitepaper update** extending the existing `pow-security-analysis.pdf`, formally analyzing the continuous-measurement security model and providing a probabilistic bound on the expected cost-of-attack for hot-plug and Sybil scenarios.
4. **Migration guide** for existing Hosts, including a parallel-run period (≥2 epochs) where both legacy Sprint and Continuous Benchmark scores are produced and reconciled.
5. **Governance proposal text** ready for on-chain submission to activate the new scoring path.
6. **Operator runbook**: deployment, troubleshooting, expected metric ranges per GPU SKU.
7. **Conformance test suite** runnable by any Host as `inferenced benchmark verify`.

## 7. Acceptance Criteria

The Benchmark is accepted when, on a testnet of ≥20 heterogeneous Hosts running for ≥7 consecutive epochs:

- Inference p99 latency degradation ≤3% versus pre-deployment baseline.
- Per-Host score CoV ≤2% across 3 consecutive honest epochs on stable hardware.
- All four reference attack scenarios (hot-plug burst, output replay, remote outsourcing, kernel substitution) are detected with ≥99% true-positive rate and ≤0.1% false-positive rate.
- Score ranking across Hosts is monotonic in raw GPU FLOPS×memory-bandwidth product within ±5% noise, independent of which model the Host serves.
- Verifier re-execution of a random 10% sample yields ≥99.5% agreement with Executor-published artifacts on honest Hosts.

---

## Votes (4)

| Voter | Amount | Date |
| :----- | :----- | :--- |
| `gonka1gm...gzg6ry` | 2.0M GNK | 2026-04-25 06:36 |
| `gonka1wv...zsa8f6` | 7.8M GNK | 2026-04-25 19:55 |
| `gonka178...08g7pn` | 3.1M GNK | 2026-05-04 07:06 |
| `gonka1rw...dftj3l` | 3.0M GNK | 2026-04-25 16:06 |

---

## Comments (12)

### 💬 Evgenii Maksimenkov
*2026-04-25 18:41* · 👍 2 · 👎 0

What are your thoughts?

---

### 💬 Alex A.A.
*2026-04-25 19:05* · 👍 2 · 👎 0

Начало положено! Язык работает.

---

### 💬 Alex A.A.
*2026-04-25 19:09* · 👍 1 · 👎 0

Через телеграм можно зайти. Круто!

---

### 💬 Nikita
*2026-04-25 19:45* · 👍 1 · 👎 0

🔥🔥🔥

---

### 💬 Alisa Chudinov
*2026-04-25 19:47* · 👍 1 · 👎 0

Very intresting!

---

### 💬 Mikhail Chudinov
*2026-04-25 19:50* · 👍 1 · 👎 0

Изучаю пока функционал сервиса.
Проблема с мульти PoC точно есть, и над ней надо думать.
Но такой бенчмарк не единственный подход.
Думаю что надо думать о полностью рыночном механизме, который не может быть заменен бенчмарком.

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 19:57* · 👍 1 · 👎 0

Тест. Интересно, как работает )
Не обращайте внимание )

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 19:58* · 👍 0 · 👎 0

Тестирую функционал тоже ) Не обращай внимание )

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 19:59* · 👍 0 · 👎 0

Hi! How is it going?!

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 20:09* · 👍 0 · 👎 0

https://www.youtube.com/shorts/WTSRfhsLYwQ

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-29 04:45* · 👍 0 · 👎 0

А сколько проверка PoC занимает сейчас ресурсов?
Предлагаемое решение будет забирать до 3%, верно?

2. Когда у сети будет больше Инференса, не решит ли это проблему с читерами? Не будут ли они улетать в МисРейт тогда?

---

### 💬 Alex Sharoiko Александр Шаройко
*2026-04-26 19:57* · 👍 0 · 👎 1

But what will happend if I reply in English?

---


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/673770df-0b72-4d04-a038-f8c12546817f)

</div>
