---
title: "#730 — [P0] vLLM 0.15.1 Compatibility Experiments"
source: https://github.com/gonka-ai/gonka/issues/730
issue_number: 730
synced_at: 2026-07-07T04:29:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] vLLM 0.15.1 Compatibility Experiments
    <span class="issues-number">#730</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-02-11 01:26 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-24 00:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content">
*(empty)*
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tamazgadaev](https://github.com/tamazgadaev)</span>
    <span class="issues-meta-item">commented 2026-03-03 03:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    PoC and inference (tentatively) seem compatible, in the next 2 days we'll try to deploy 2 nodes with 15 version and know for sute about the comaptibility
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@baychak](https://github.com/baychak)</span>
    <span class="issues-meta-item">commented 2026-03-17 19:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    # ML Node Migration to vLLM 0.15.1 — Results and Artifacts

## Summary

The [kaitaku.ai](https://github.com/kaitakuai) team together with Tamaz Gadaev completed the migration of ML Node from vLLM 0.9.1 to 0.15.1 for the Gonka network, including:

- Support for all NVIDIA architectures through a single image for A100, H100, H200, and B200
- Performance validation during the upgrade to the new version
- Extensive benchmarking of three models (Qwen 235B, GPT-OSS 120B, Kimi K2.5) across five GPU architectures

---

## Benchmark Results

### Deployment Parameters

| GPU | Model | TP | PP | Max Seq Len | VRAM | PoC Seq Len | Attn Backend | Tools |
|-----|-------|----|----|-------------|------|-------------|--------------|-------|
| 4×H100 80GB | Qwen 235B | 4 | 1 | 240 000 | 78/80 GiB (96%) | 1024 | FLASHINFER | TRUE |
| 4×H100 80GB | GPT OSS | — | — | 32 768 | 73/80 GiB (90%) | 1024 | FLASHINFER | TRUE |
| 4×H100 80GB | Kimi K2.5 | — | — | — | — | 1024 | FLASHINFER | TRUE |
| 4×H200 140GB | Qwen 235B | 4 | 1 | 262 144 | 129/140 GiB (92%) | 1024 | FLASHINFER | TRUE |
| 4×H200 140GB | GPT OSS | — | — | 131 072 | 128/140 GiB (91%) | 1024 | FLASHINFER | TRUE |
| 4×H200 140GB | Kimi K2.5 | 8 | 1 | 262 144 | 130/140 GiB (92%) | 1024 | FLASHINFER | TRUE |
| 2×B200 180GB | Qwen 235B | 2 | 1 | 262 144 | 164/179 GiB (92%) | 1024 | FLASHINFER | TRUE |
| 2×B200 180GB | GPT OSS | — | — | 131 072 | 164/179 GiB (91%) | 1024 | FLASHINFER | TRUE |
| 4×B200 180GB | Kimi K2.5 | 4 | 1 | 262 144 | 135/179 GiB (74%) | 1024 | FLASHINFER_MLA | TRUE |

### Qwen 235B — Configuration Comparison (Nonces/min per cluster)

| Configuration | A | B | C | D | E | F | Best/GPU |
|---------------|--:|--:|--:|--:|--:|--:|---------:|
| 4×A100 SXM4 | 384 | 448 | 484 | — | — | — | **121** |
| 4×H100 SXM | 640 | 832 | 1 056 | — | — | — | **264** |
| 4×H200 | — | — | 1 136 | 1 058 | 832 | 640 | **284** |
| 2×B200 (TP=2) | — | — | 1 633 | — | — | — | **816** |

> **Legend:** A — TP=4 `--enforce-eager` · B — TP=4 compiled · C — TP=4 batched compiled · D — TP=4 batched `--enforce-eager` · E — TP=2;PP=2 batched `--enforce-eager` · F — PP=4 batched `--enforce-eager`

### All Models — Batched + Compiled (Nonces/min, total across 8 GPUs)

| GPU | Qwen 235B | GPT-OSS 120B | Kimi K2.5 |
|-----|----------:|-------------:|----------:|
| 8×A100 SXM4 (b=2) | 968 | 5 712 | — |
| 8×H100 (b=8) | 2 112 | 24 568 | — |
| 8×H200 (b=8) | 2 272 | 24 568 | 1 189 |
| 8×B200 (b=8) | 6 908 | 53 216 | 1 989 |
| 8×AMD MI300X | 1 078 | 4 126 | — |

### All Models — Batched + Not Compiled (Nonces/min, total across 8 GPUs)

| GPU | Qwen 235B | GPT-OSS 120B | Kimi K2.5 |
|-----|----------:|-------------:|----------:|
| 8×A100 SXM4 (b=16) | 1 024 | 6 144 (b=32) | — |
| 8×H100 | 1 920 | 21 496 | — |
| 8×H200 | 1 919 | 21 496 | 1 145 |
| 8×B200 (b=32) | 6 140 | 54248 | 1 948 |
| 8×AMD MI300X | 1 032 | 3 984 | — |

**Key takeaway:**

- The single image works across all four GPU architectures

## Cross-GPU PoC Validation

### L2 Distance Between GPUs (enforce-eager mode)

All GPU pairs show close distances, meaning PoC validation passes successfully across all architectures within the single image.

<details>
<summary><strong>Cross-version/cross-GPU experiments (6 experiments)</strong></summary>

| # | GPU Honest | Version | Model | GPU Fraud | Fraud Version | Fraud Model | GPU Validator | Validator Version | Validator Model | Artifacts |
|---|------------|---------|-------|-----------|---------------|-------------|---------------|-------------------|-----------------|-----------|
| 1 | A800 | v0.9.1 | Qwen FP8 | RTX 6000 | v0.15.1 | Qwen INT4 | RTX 6000 | v0.15.1 | Qwen FP8 | [artifacts](https://drive.google.com/drive/folders/1ZoNHlDW4zOjMDyMHtbkVychlIBwc_JOA?usp=sharing) |
| 2 | A800 | v0.15.1 | Qwen FP8 | RTX 6000 | v0.15.1 | Qwen INT4 | RTX 6000 | v0.15.1 | Qwen FP8 | [artifacts](https://drive.google.com/drive/folders/1ZoNHlDW4zOjMDyMHtbkVychlIBwc_JOA?usp=sharing) |
| 3 | A800 | v0.15.1 | Kimi INT4 | RTX 6000 | v0.15.1 | Kimi INT4 | RTX 6000 | v0.15.1 | Kimi INT4 | [artifacts](https://drive.google.com/drive/folders/1wGgZieGdKzBQHwOK8gYEpIYBwAR8BZ8z?usp=sharing) |
| 4 | A800 | v0.15.1 | Kimi INT4 | RTX 6000 | v0.15.1 | Kimi INT2 | RTX 6000 | v0.15.1 | Kimi INT4 | [artifacts](https://drive.google.com/drive/folders/1wGgZieGdKzBQHwOK8gYEpIYBwAR8BZ8z?usp=sharing) |
| 5 | A800 | v0.15.1 | GPT-OSS INT4 | RTX 6000 | v0.15.1 | GPT-OSS INT2 | RTX 6000 | v0.15.1 | GPT-OSS INT4 | [artifacts](https://drive.google.com/drive/folders/1GdoMrwkcMu5kMxVb848TIgDuL6-hHEd1?usp=sharing) |
| 6 | A800 | v0.15.1 | GPT-OSS INT4 | RTX 6000 | v0.15.1 | GPT-OSS INT4 | RTX 6000 | v0.15.1 | GPT-OSS INT4 | [artifacts](https://drive.google.com/drive/folders/1GdoMrwkcMu5kMxVb848TIgDuL6-hHEd1?usp=sharing) |

</details>

## Per-GPU Experiments

<details>
<summary><strong>Full experiment table (16 experiments)</strong></summary>

| # | GPU | Version | Model | Nonces/min | 8×GPU | TP | PoC Vectors | Docker run |
|--:|-----|---------|-------|-----------:|------:|---:|-------------|------------|
| 1 | A800 NVLink | v0.9.1 | Qwen FP8 | 480 | 960 | 4 | [vectors](https://drive.google.com/file/d/1lMMZpa02lj0mHXYuoDkvzzeTz0clVEzo/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 2 | A800 NVLink | v0.15.1 | Qwen FP8 | 512 | 1 024 | 4 | [vectors](https://drive.google.com/file/d/1M-US9sxPa_f8DlBvxLxHEWgDOU-CdZQZ/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 3 | A800 NVLink | v0.9.1 | Qwen INT4 | 512 | 1 024 | 4 | [vectors](https://drive.google.com/file/d/1Wbwrwm2J4PsR8HhLafw53MfU125UCyY2/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 4 | A800 NVLink | v0.15.1 | Qwen INT4 | 512 | 1 024 | 4 | [vectors](https://drive.google.com/file/d/1x3RcVJJbYiGk6ayLuOCc4w93A9QGGFOo/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 5 | RTX 6000 | v0.9.1 | Qwen FP8 | 416 | 832 | 4 | [vectors](https://drive.google.com/file/d/17sYIXIFa8Ex9iMp14A9sgqWHmcUpBoyI/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 6 | RTX 6000 | v0.15.1 | Qwen FP8 | 451 | 902 | 4 | [vectors](https://drive.google.com/file/d/1k6VgdvdYuvQONi-YRpA5pJ2QFn6OUkjS/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 7 | RTX 6000 | v0.9.1 | Qwen INT4 | ? | — | 4 | [vectors](https://drive.google.com/file/d/12VXHKTYLzhvxhK0K71puJnLwe4zd64RX/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 8 | RTX 6000 | v0.15.1 | Qwen INT4 | 400 | 800 | 4 | [vectors](https://drive.google.com/file/d/1RLDuWzqvqkwoQaHXwu3nw9uES7mNXjpo/view?usp=sharing) | [command](https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing) |
| 9 | A800 NVLink | v0.15.1 | Kimi K2.5 INT4 | 349 | 349 | 8 | [vectors](https://drive.google.com/file/d/155zGRY2HH6bptw8lc85bKOowN-bvbGZA/view?usp=sharing) | [command](https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing) |
| 10 | A800 NVLink | v0.15.1 | Kimi K2.5 INT2 | 417 | 417 | 8 | [vectors](https://drive.google.com/file/d/1U20bobTBSK3gyEIGS4HNp_6SOJDfARE6/view?usp=sharing) | [command](https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing) |
| 11 | RTX 6000 | v0.15.1 | Kimi K2.5 INT4 | 258 | 258 | 8 | [vectors](https://drive.google.com/file/d/1Dq1_5gVmv0a5kp7qkY9tR2tQrBHOVlct/view?usp=sharing) | [command](https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing) |
| 12 | RTX 6000 | v0.15.1 | Kimi K2.5 INT2 | 288 | 288 | 8 | [vectors](https://drive.google.com/file/d/1HeludcbAP0TCQXDnSGLAdaBH8BHl8TnK/view?usp=sharing) | [command](https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing) |
| 13 | A800 | v0.15.1 | GPT-OSS MXFP4 | 472 | 3 776 | 1 | [vectors](https://drive.google.com/file/d/1SSTz_m58aMcvyr07D75bvOVnwddlgjzd/view?usp=sharing) | [command](https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing) |
| 14 | A800 | v0.15.1 | GPT-OSS INT2 | 472 | 3 776 | 1 | [vectors](https://drive.google.com/file/d/1pq4pLHS2fPyf5IKD_e7uZF5oYMsYFkJq/view?usp=sharing) | [command](https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing) |
| 15 | RTX 6000 | v0.15.1 | GPT-OSS MXFP4 | 833 | 6 664 | 1 | [vectors](https://drive.google.com/file/d/1FQksG3gCqNhOGdjM9Q44zb_rlR8T4IT9/view?usp=sharing) | [command](https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing) |
| 16 | RTX 6000 | v0.15.1 | GPT-OSS INT2 | 833 | 6 664 | 1 | [vectors](https://drive.google.com/file/d/1uXFKZLUwG2Us82vluLCXTsbsytcJEz3i/view?usp=sharing) | [command](https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing) |

</details>

## Artifacts

| Resource | Link |
|----------|------|
| Main vLLM 0.15.1 + PoC test branch | [mb/poc-v015-no-dummy-input-ids](https://github.com/kaitakuai/vllm/tree/mb/poc-v015-no-dummy-input-ids) |
| Test Docker image | `ghcr.io/kaitakuai/mlnode:v0.15.1-no-dummy-input-ids` |
| All test images | [GitHub Packages](https://github.com/orgs/kaitakuai/packages) |
| Benchmark spreadsheet | [Google Sheets](https://docs.google.com/spreadsheets/d/1A_wyBQvYNmz0H8bmQxMah53Gj1hjMIOHC19XFAQY6Mg/edit?usp=sharing) |

## Participants

| Participant | GitHub | Contribution |
|-------------|--------|--------------|
| Pavlo | [@clanster](https://github.com/clanster) | GPU testing, benchmark and artifact collection, visualization |
| Mykola Baichak | [@baychak](https://github.com/baychak) | Image builds, benchmarks, batching fixes, and torch.compile fixes |
| Tamaz Gadaev | [@tamazgadaev](https://github.com/tamazgadaev) | PoC architecture, review, and fixes on the Gonka core team side |


  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #730](https://github.com/gonka-ai/gonka/issues/730) every hour.
