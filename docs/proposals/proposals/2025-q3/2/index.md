---
title: "#2 – Proposal introducing new Qwen3 models"
description: "This proposal introduces new Qwen3 models including Qwen3-32B-FP8 and Qwen3-235B-A22B-Instruct-2507-FP8, along with updating parameters for Qwen2.5-7B-Instruct and QwQ-32B."
template: proposals-proposals-main.html
---

# #2 – Proposal introducing new Qwen3 models

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `2`

**Type:** Register Model

**Submit:** 2025-09-09 21:40 UTC

**Voting:** 2025-09-09 21:40 UTC → 2025-09-11 21:40 UTC

**Proposer:** `gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`

**Metadata:** [https://github.com/gonka-ai/gonka/blob/c8668fd0f6144109165e0386f55fe22eb3cb27c7/proposals/governance-artifacts/models-1/README.md](https://github.com/gonka-ai/gonka/blob/c8668fd0f6144109165e0386f55fe22eb3cb27c7/proposals/governance-artifacts/models-1/README.md)

</div>

This proposal introduces new Qwen3 models including Qwen3-32B-FP8 and Qwen3-235B-A22B-Instruct-2507-FP8, along with updating parameters for Qwen2.5-7B-Instruct and QwQ-32B.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:100.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 62,612 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgRegisterModel` |
| 2 | `/inference.inference.MsgRegisterModel` |
| 3 | `/inference.inference.MsgRegisterModel` |
| 4 | `/inference.inference.MsgRegisterModel` |
| 5 | `/inference.inference.MsgRegisterModel` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/inference.inference.MsgRegisterModel",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "proposed_by": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "id": "Qwen/Qwen2.5-7B-Instruct",
    "units_of_compute_per_token": "100",
    "hf_repo": "Qwen/Qwen2.5-7B-Instruct",
    "hf_commit": "a09a35458c702b33eeacc393d103063234e8bc28",
    "model_args": [
      "--quantization",
      "fp8"
    ],
    "v_ram": "24",
    "throughput_per_nonce": "20000",
    "validation_threshold": {
      "value": "97",
      "exponent": -2
    }
  },
  {
    "@type": "/inference.inference.MsgRegisterModel",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "proposed_by": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "id": "Qwen/QwQ-32B",
    "units_of_compute_per_token": "1000",
    "hf_repo": "Qwen/QwQ-32B",
    "hf_commit": "976055f8c83f394f35dbd3ab09a285a984907bd0",
    "model_args": [
      "--quantization",
      "fp8",
      "--kv-cache-dtype",
      "fp8"
    ],
    "v_ram": "80",
    "throughput_per_nonce": "6000",
    "validation_threshold": {
      "value": "97",
      "exponent": -2
    }
  },
  {
    "@type": "/inference.inference.MsgRegisterModel",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "proposed_by": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
    "id": "RedHatAI/Qwen2.5-7B-Instruct-quantized.w8a16",
    "units_of_compute_per_token": "100",
    "hf_repo": "RedHatAI/Qwen2.5-7B-Instruct-quantized.w8a16",
    "hf_commit": "a5609cbf939e46f4c17f189100d5e6825da318b0",
    "model_args": [],
    "v_ram": "24",
    "throughput_per_nonce": "20000",
    "validation_threshold": {
      "value": "991429",
      "exponent": -6
    }
  },
  {
    "@type": "/inference.inference.MsgRegisterModel",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "proposed_by": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
    "id": "Qwen/Qwen3-32B-FP8",
    "units_of_compute_per_token": "1000",
    "hf_repo": "Qwen/Qwen3-32B-FP8",
    "hf_commit": "aa55da1ecc13d006e8b8e4f54579b1ea8c3db2df",
    "model_args": [],
    "v_ram": "80",
    "throughput_per_nonce": "6000",
    "validation_threshold": {
      "value": "95814",
      "exponent": -5
    }
  },
  {
    "@type": "/inference.inference.MsgRegisterModel",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "proposed_by": "gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5",
    "id": "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    "units_of_compute_per_token": "10000",
    "hf_repo": "Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
    "hf_commit": "c0eb82898e3da8fb6dd017e3e6698a5e37b3a3e6",
    "model_args": [
      "--max-model-len",
      "240000"
    ],
    "v_ram": "320",
    "throughput_per_nonce": "1500",
    "validation_threshold": {
      "value": "970917",
      "exponent": -6
    }
  }
]
```

</details>

---

<div class="prop-footer" markdown="1">

[View on gonka.gg](https://gonka.gg/network/proposals/2){:target="_blank"}

</div>
