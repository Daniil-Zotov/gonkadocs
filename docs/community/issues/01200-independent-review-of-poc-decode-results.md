---
title: "#1200 — Independent review of PoC-decode results"
source: https://github.com/gonka-ai/gonka/issues/1200
issue_number: 1200
synced_at: 2026-10-08T22:11:24Z
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
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-30 02:59 UTC</span>
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

## 💬 Comments (3)

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
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-09-30 02:59 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @tcharchian Thanks for writing this out, it's much easier to review against than what we had before. I've been reading it alongside <code>gonka-vllm-plugins@decode-poc-int</code> (2ca7cd7), the two vllm PRs, and the chain branch behind #1743.</p>
<p>Four things I'd like to settle before starting. The first is the one I'm least sure I'm reading correctly.</p>
<p>1.The decode threshold.The description gives τ as 0.025–0.03 for GLM-5.3-Flash and 0.04–0.05 for MiniMax, per model on chain. I tried to trace where those get set, and I couldn't find them, so I suspect I'm looking in the wrong place. What I can see on the branch is this: the validator sends <code>stat_test</code> from <code>StatTestForScheme(scheme, modelConfig)</code> (<code>decentralized-api/poc/validator.go:968</code>), which returns the scheme block's <code>StatTest</code> — and for DECODE there's no fallback block, which the comment at <code>poc_scheme.go:44-64</code> says is deliberate while the scheme isn't deployed. A nil then resolves to <code>0.4</code> in <code>StatTestParamsFromChain</code> (<code>mlnodeclient/poc_v2_requests.go:86-98</code>). I also can't find any model with a populated <code>Schemes[]</code> list, so as far as I can tell the flat prefill values are what's live: 0.4 by default (<code>params.go:282</code>), 0.4 for Kimi in v0_2_12, 0.75 for MiniMax in v0_2_13. Since the plugin takes whatever <code>stat_test</code> it's handed (<code>routes.py:714</code>) and only falls back to its own <code>DEFAULT_MARGIN_TAU = 0.025</code> when the field is absent (<code>routes.py:593-595</code>), I'd expect decode validation to run against 0.4 for every model right now. If the per-model τ values are meant to ship as <code>PocSchemeParams.stat_test</code> blocks in a later upgrade, that answers it — I just want to know that's the plan rather than assume it. Same question for the 0.41 in the prefill section, which I also couldn't find (I only see 0.4 and 0.75).</p>
<p>2.The step seed formula. This one may be a doc typo rather than anything real. The description has <code>step_seed(step, prev_k, salt) = murmur((prev_k·A + step·B + salt) mod 2³², base)</code>, but the code puts the salt inside the step term, masks <code>prev_k</code> before the multiply rather than <code>step</code>, and masks after the sum (<code>poc/decode_random.py:97-103</code>). Someone reimplementing from the prose would land on different seeds and every step would disagree. I assume the code is normative, but if it's the other way round that's worth knowing before anyone builds against it.</p>
<p>3.What the argument is optimizing against.The table makes the case that a host tuned for decode is also tuned for serving — 1,253 to 2,047 nonces/min under cudagraph while prefill PoC goes the other way, and billed throughput up 391%. That's convincing for a host that wants to serve well. The host I'd expect this design to be judged against is one that wants the reward and doesn't care about serving, and the two schemes differ in what such a host can do: decode holds 512 KV tokens per nonce and rides the chat scheduler, prefill runs eager on its own. Is there a measurement on that side, intended or existing, or is that out of scope here?</p>
<p>4.Confirmation PoC. <code>params.proto</code> carries <code>confirmation_poc_scheme</code> and <code>confirmation_scheme_events</code> next to <code>poc_scheme</code>, and <code>SchemeForStage</code> does route CPoC events to slot 17. The description covers the regular PoC only. Should I treat CPoC as out of scope for this review, or is that part of what you want checked?</p>
<p>Two process things, I need to confirm that:</p>
<p>I couldn't find a deliverable format anywhere in the issue, so — what would you like out of this? Comments per finding on the issue, or one writeup somewhere? And on the <code>SPHERE_POINTS</code> × fraud-distance sweep, is running that yours or mine?if it's theirs and I'm assessing the result, that's a different shape of work. If it is mine, which near-miss pairs should it cover — an INT4/FP8 pair on Qwen3-235B, a fine-tune delta, or both?</p>
<p>If the sweep stays with the team, I can start on the four points above straight away.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1200](https://github.com/gonka-ai/gonka/issues/1200) every hour.
