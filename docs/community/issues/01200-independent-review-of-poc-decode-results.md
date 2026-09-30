---
title: "#1200 — Independent review of PoC-decode results"
source: https://github.com/gonka-ai/gonka/issues/1200
issue_number: 1200
synced_at: 2026-09-30T00:33:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Independent review of PoC-decode results
    <span class="issues-number">#1200</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:36 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-29 16:23 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
Independently review and re-check the PoC-decode approach

# Gonka Proof-of-Compute: the prefill scheme and the decode scheme

What a prover computes per nonce, what it sends, and what a validator recomputes and compares. Source of truth: `gonka-ai/gonka-vllm-plugins` branch `decode-poc-int` (2ca7cd7), engine seams `gonka-ai/vllm#100` / `#113`, chain `gonka-ai/gonka#1743`. Both schemes are served by the same plugin; the chain picks one per PoC stage (`PocParams.poc_scheme`).

**Why decode instead of prefill.** A host that optimizes its node for decode PoC also optimizes it for inference: decode nonces are ordinary engine requests that go through the same scheduler, KV cache and compiled graphs as chat. A host that optimizes for prefill PoC optimizes only the prefill phase, which can even hurt inference: e.g. on MiniMax, compile mode speeds up both inference and decode PoC, while prefill PoC runs faster without it.

Example on DeepSeek-V4-Flash with cudagraph on and off (`--enforce-eager`); billed = prompt incl. cache hits + output, tokens/s per instance, 256 agentic sessions with high cache hit (`session_bench` from gonka#1839):

| | eager | cudagraph | cudagraph vs eager | eager vs cudagraph |
|---|---:|---:|---:|---:|
| decode PoC, nonces/min | 1,253 | 2,047 | +63.4% | −38.8% |
| prefill PoC, nonces/min | 1,728 | 1,350 | −21.9% | +28.0% |
| billed, tokens/s | 45,382 | 222,808 | +391.0% | −79.6% |

Notation. `H` is the model hidden size, `L` the number of decoder layers. `seed(s) = int(sha256(s)[:8], 16)`; `normal(seed, n)` is a deterministic standard-normal vector of length `n` (murmur3 counter stream + Box–Muller); `murmur(keys, seed)` is murmur3-32. All of this is integer arithmetic plus elementary float ops, identical on every node.

---

## 1. Prefill scheme (in production, `POC_SCHEME_PREFILL`)

One forward pass per nonce; the artifact is a 12-dimensional vector.

**Prover, per nonce `n` with `(block_hash, public_key)`:**

1. **Input.** `X = normal(seed(f"{block_hash}_{public_key}_nonce{n}"), seq_len·H)` reshaped to `[seq_len, H]` (`seq_len` = 1024 on mainnet), cast to the model dtype. It is fed as `inputs_embeds`, bypassing the token embedding. Token-id-routed models (DeepSeek-V4 hash-MoE) also get pseudo token ids `murmur(position, seed(...+"_input_ids")) mod vocab`. With `poc_stronger_rng` the normal stream is split over 8 sub-seeds of the full sha256.
2. **Forward with per-layer reflections.** A forward hook on every decoder layer `i` applies a Householder reflection to the layer's output hidden state and residual: `x ← x − 2 (x·v_i) v_i`, `v_i = normalize(normal(seed(f"{block_hash}_layer_{i}_householder"), H))`. Same `v_i` for every nonce of the block; MoE routing is the model's own.
3. **Fingerprint.** `h = normalize(hidden[last position])` (`[H]`, fp32). Pick `k_dim = 12` coordinates: `idx = 12 smallest of murmur(0..H−1, seed(f"{block_hash}_{public_key}_nonce_{n}_pick_12"))`; `x = h[idx]`. Apply a Haar-random rotation as 11 Householder reflections in R¹²: for `j = 0..10`, `u_j = normalize(normal(seed(f"..._haar_hh_12_{j}"), 12))`, `x ← x − 2 (x·u_j) u_j`. Normalize again.
4. **Artifact.** `vector_b64` = the 12 values as fp16 little-endian, base64 (24 bytes). A nonce whose hidden state or fp16 vector is non-finite is dropped, not sent.

**Validator, for a sampled set of nonces:** recompute 1–3 on its own model, `d = ‖x_validator − x_prover‖₂`. A nonce mismatches if `d > dist_threshold` (per model on chain, e.g. 0.41 for DeepSeek-V4-Flash), if the received vector is not 12 fp16 values, or if it contains NaN/Inf. Over the sample: binomial test of the mismatch count against `p_mismatch` with `alternative='greater'`; `fraud = p_value < fraud_threshold`. A nonce the validator itself failed to compute (non-finite state, engine failure) leaves the sample.

---

## 2. Decode scheme (`POC_SCHEME_DECODE`)

A prefill of 256 positions followed by 256 decode steps per nonce, run as an ordinary engine request that shares the scheduler and batch with chat. The artifact is a chain of 257 codebook indices.

**Fixed constants.** Codebook `C`: 16 unit vectors in R²⁵⁶ (`SPHERE_POINTS = 16`, `SPHERE_DIM = 256`), built once (Halton init + Thomson repulsion), shipped as `sphere_codebook.pt` and checked against a frozen sha256 at load. MoE logit baseline `LADDER_BASE = 100`. It's using to make a top-k expert sampling smoothier, just adding for the top-k experts value LADDER_BASE + 1, LADDER_BASE + 2 etc.

**Per-nonce seeds.** `base = seed(f"{block_hash}_{public_key}_nonce{n}")`. Per step, `step_seed(step, prev_k, salt) = murmur((prev_k·A + step·B + salt) mod 2³², base)` with fixed odd constants `A, B` and three salts: `0x0D` input embedding, `0x91` coordinate pick, `0x57` pseudo token id. `prev_k` is the codebook index of the previous step, so every stream of step `t+1` depends on the fingerprint of step `t`.

**Model transforms (installed once, inside the compiled/captured graph, applied only to PoC rows via a per-row mask; chat rows are untouched):**

- *Embedding.* PoC rows bypass the token embedding: prefill rows take `X` exactly as in the prefill scheme (step 1 above, `seq_len = 256`); decode row at step `t` takes `e_t = normal(step_seed(t, k_{t−1}, 0x0D), H)`.
- *Per-layer reflection.* Every decoder layer's output hidden and residual are reflected on PoC rows, `x ← x − 2 (x·v_i) v_i`, with `v_i` from `f"{block_hash}_layer_{i}_householder"` (or `f"{block_hash}_nonce{n}_layer_{i}_householder"` when the request sets `per_nonce_reflection`). Same reflection family as the prefill scheme, step-independent.
- *Seeded MoE routing.* On every MoE layer `ℓ` the router logits of PoC rows are replaced: `r = murmur(step, seed(f"{block_hash}_n{n}_route_layer_{ℓ}"))`, `start = r mod n_experts`, experts `start … start+top_k−1 (mod n_experts)` get logits `100+top_k … 101`, all others `−10⁴`; the engine's top-k then selects exactly these experts with softmax-of-ladder weights. Expert choice never reads the hidden state (cross-hardware routing noise is removed). Hash-MoE models (DeepSeek-V4) keep their token-id routing and get a per-step pseudo id `murmur(0, step_seed(t, k_{t−1}, 0x57)) mod vocab` instead.
- *Snap (the "sampler").* After the final norm, for each PoC row: `h = normalize(hidden)`; `idx = 256 smallest of murmur(0..H−1, step_seed(t, k_{t−1}, 0x91))` (prefill step: `t = 0`, no `prev_k` term); `q = normalize(h[idx])` ∈ S²⁵⁵; scores `s_j = q·C_j`, `j = 0..15`; `k_t = argmax_j s_j`. A non-finite `q` yields `k = −1` (compute fault marker). No token is sampled; PoC rows never enter the LM head or sampler.

**Prover, per nonce:** prefill on the 256 seeded embeddings → `k_0`; then for `t = 1..256`: build `e_t` from `k_{t−1}`, one decode step, snap → `k_t`. The KV cache grows as in normal generation (512 tokens per nonce at the end). Artifact: `k_points_steps = [k_0 … k_256]`, 257 values in `0..15`, packed on chain as one byte per step. A nonce with any `k = −1` is dropped, not sent; the chain rejects any byte outside `0..15`.

**Validator, for a sampled set of nonces (teacher-forced):** run the same request with the prover's chain as reference. At every step the validator computes its own snap from its own hidden state, but seeds step `t+1` with the prover's `k_t`, so both sides follow one trajectory and a disagreement at one step does not propagate. For each disagreeing step it keeps the score row `s` of its own `q` and measures the claim against it: `margin_t = max_j s_j − s[k_t^prover]` (0 when the claim is its own snap; the top1−top2 gap when the claim is its runner-up, i.e. boundary jitter; ≈0.7 for a far cell on this codebook; 2.0 for a claim outside `0..15`). The nonce's distance is `max_t margin_t` over disagreeing steps, and the nonce mismatches if it exceeds `τ = dist_threshold` (per model on chain, e.g. 0.025 for DeepSeek-V4-Flash, 0.025–0.03 for GLM-5.3-Flash, 0.04–0.05 for MiniMax-M2.7). Then the same binomial test over nonces as in the prefill scheme. Nonces the validator could not compute (non-finite step) leave the sample; a reference with a value outside the codebook is a mismatch, not an error.

---

## 3. What differs

| | prefill | decode |
|---|---|---|
| work per nonce | 1 forward over 1024 positions | prefill 256 + 256 decode steps (512 KV tokens held) |
| model transforms | reflections on every layer | reflections on every layer + seeded MoE routing + seeded embedding per step + in-graph snap |
| artifact | 12 fp16 values (24 B) | 257 codebook indices (257 B) |
| chaining | none | `k_t` seeds the input embedding, the coordinate pick and the pseudo id of step `t+1` |
| observations per nonce | 1 L2 distance | 257 index comparisons, scored by claimed-cell margin |
| validator replay | independent recompute | teacher-forced on the prover's chain |
| verdict | L2 > `dist_threshold` per nonce → binomial | `max` claimed margin > `τ` per nonce → binomial |
| execution | eager, separate forward outside the scheduler | ordinary engine requests, cudagraph/compiled, batched with chat |

## Notes

This task is about independent verification and critical review. 
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-09-26 03:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @tcharchian , do you need help with this? Maybe I can take on this task.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-29 16:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @Ryanchen911, I've updated the issue description, you are welcome to review</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1200](https://github.com/gonka-ai/gonka/issues/1200) every hour.
