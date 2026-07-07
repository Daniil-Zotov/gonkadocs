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
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-11 01:26 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-24 00:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tamazgadaev">@tamazgadaev</a></span>
    <span class="issues-meta-item">commented 2026-03-03 03:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
<p>PoC and inference (tentatively) seem compatible, in the next 2 days we'll try to deploy 2 nodes with 15 version and know for sute about the comaptibility</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-03-17 19:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
<h1>ML Node Migration to vLLM 0.15.1 — Results and Artifacts</h1>
<h2>Summary</h2>
<p>The <a href="https://github.com/kaitakuai">kaitaku.ai</a> team together with Tamaz Gadaev completed the migration of ML Node from vLLM 0.9.1 to 0.15.1 for the Gonka network, including:</p>
<ul>
<li>Support for all NVIDIA architectures through a single image for A100, H100, H200, and B200</li>
<li>Performance validation during the upgrade to the new version</li>
<li>Extensive benchmarking of three models (Qwen 235B, GPT-OSS 120B, Kimi K2.5) across five GPU architectures</li>
</ul>
<hr />
<h2>Benchmark Results</h2>
<h3>Deployment Parameters</h3>
<table>
<thead>
<tr>
<th>GPU</th>
<th>Model</th>
<th>TP</th>
<th>PP</th>
<th>Max Seq Len</th>
<th>VRAM</th>
<th>PoC Seq Len</th>
<th>Attn Backend</th>
<th>Tools</th>
</tr>
</thead>
<tbody>
<tr>
<td>4×H100 80GB</td>
<td>Qwen 235B</td>
<td>4</td>
<td>1</td>
<td>240 000</td>
<td>78/80 GiB (96%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×H100 80GB</td>
<td>GPT OSS</td>
<td>—</td>
<td>—</td>
<td>32 768</td>
<td>73/80 GiB (90%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×H100 80GB</td>
<td>Kimi K2.5</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×H200 140GB</td>
<td>Qwen 235B</td>
<td>4</td>
<td>1</td>
<td>262 144</td>
<td>129/140 GiB (92%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×H200 140GB</td>
<td>GPT OSS</td>
<td>—</td>
<td>—</td>
<td>131 072</td>
<td>128/140 GiB (91%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×H200 140GB</td>
<td>Kimi K2.5</td>
<td>8</td>
<td>1</td>
<td>262 144</td>
<td>130/140 GiB (92%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>2×B200 180GB</td>
<td>Qwen 235B</td>
<td>2</td>
<td>1</td>
<td>262 144</td>
<td>164/179 GiB (92%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>2×B200 180GB</td>
<td>GPT OSS</td>
<td>—</td>
<td>—</td>
<td>131 072</td>
<td>164/179 GiB (91%)</td>
<td>1024</td>
<td>FLASHINFER</td>
<td>TRUE</td>
</tr>
<tr>
<td>4×B200 180GB</td>
<td>Kimi K2.5</td>
<td>4</td>
<td>1</td>
<td>262 144</td>
<td>135/179 GiB (74%)</td>
<td>1024</td>
<td>FLASHINFER_MLA</td>
<td>TRUE</td>
</tr>
</tbody>
</table>
<h3>Qwen 235B — Configuration Comparison (Nonces/min per cluster)</h3>
<table>
<thead>
<tr>
<th>Configuration</th>
<th style="text-align: right;">A</th>
<th style="text-align: right;">B</th>
<th style="text-align: right;">C</th>
<th style="text-align: right;">D</th>
<th style="text-align: right;">E</th>
<th style="text-align: right;">F</th>
<th style="text-align: right;">Best/GPU</th>
</tr>
</thead>
<tbody>
<tr>
<td>4×A100 SXM4</td>
<td style="text-align: right;">384</td>
<td style="text-align: right;">448</td>
<td style="text-align: right;">484</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;"><strong>121</strong></td>
</tr>
<tr>
<td>4×H100 SXM</td>
<td style="text-align: right;">640</td>
<td style="text-align: right;">832</td>
<td style="text-align: right;">1 056</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;"><strong>264</strong></td>
</tr>
<tr>
<td>4×H200</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">1 136</td>
<td style="text-align: right;">1 058</td>
<td style="text-align: right;">832</td>
<td style="text-align: right;">640</td>
<td style="text-align: right;"><strong>284</strong></td>
</tr>
<tr>
<td>2×B200 (TP=2)</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">1 633</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;"><strong>816</strong></td>
</tr>
</tbody>
</table>
<blockquote>
<p><strong>Legend:</strong> A — TP=4 <code>--enforce-eager</code> · B — TP=4 compiled · C — TP=4 batched compiled · D — TP=4 batched <code>--enforce-eager</code> · E — TP=2;PP=2 batched <code>--enforce-eager</code> · F — PP=4 batched <code>--enforce-eager</code></p>
</blockquote>
<h3>All Models — Batched + Compiled (Nonces/min, total across 8 GPUs)</h3>
<table>
<thead>
<tr>
<th>GPU</th>
<th style="text-align: right;">Qwen 235B</th>
<th style="text-align: right;">GPT-OSS 120B</th>
<th style="text-align: right;">Kimi K2.5</th>
</tr>
</thead>
<tbody>
<tr>
<td>8×A100 SXM4 (b=2)</td>
<td style="text-align: right;">968</td>
<td style="text-align: right;">5 712</td>
<td style="text-align: right;">—</td>
</tr>
<tr>
<td>8×H100 (b=8)</td>
<td style="text-align: right;">2 112</td>
<td style="text-align: right;">24 568</td>
<td style="text-align: right;">—</td>
</tr>
<tr>
<td>8×H200 (b=8)</td>
<td style="text-align: right;">2 272</td>
<td style="text-align: right;">24 568</td>
<td style="text-align: right;">1 189</td>
</tr>
<tr>
<td>8×B200 (b=8)</td>
<td style="text-align: right;">6 908</td>
<td style="text-align: right;">53 216</td>
<td style="text-align: right;">1 989</td>
</tr>
<tr>
<td>8×AMD MI300X</td>
<td style="text-align: right;">1 078</td>
<td style="text-align: right;">4 126</td>
<td style="text-align: right;">—</td>
</tr>
</tbody>
</table>
<h3>All Models — Batched + Not Compiled (Nonces/min, total across 8 GPUs)</h3>
<table>
<thead>
<tr>
<th>GPU</th>
<th style="text-align: right;">Qwen 235B</th>
<th style="text-align: right;">GPT-OSS 120B</th>
<th style="text-align: right;">Kimi K2.5</th>
</tr>
</thead>
<tbody>
<tr>
<td>8×A100 SXM4 (b=16)</td>
<td style="text-align: right;">1 024</td>
<td style="text-align: right;">6 144 (b=32)</td>
<td style="text-align: right;">—</td>
</tr>
<tr>
<td>8×H100</td>
<td style="text-align: right;">1 920</td>
<td style="text-align: right;">21 496</td>
<td style="text-align: right;">—</td>
</tr>
<tr>
<td>8×H200</td>
<td style="text-align: right;">1 919</td>
<td style="text-align: right;">21 496</td>
<td style="text-align: right;">1 145</td>
</tr>
<tr>
<td>8×B200 (b=32)</td>
<td style="text-align: right;">6 140</td>
<td style="text-align: right;">54248</td>
<td style="text-align: right;">1 948</td>
</tr>
<tr>
<td>8×AMD MI300X</td>
<td style="text-align: right;">1 032</td>
<td style="text-align: right;">3 984</td>
<td style="text-align: right;">—</td>
</tr>
</tbody>
</table>
<p><strong>Key takeaway:</strong></p>
<ul>
<li>The single image works across all four GPU architectures</li>
</ul>
<h2>Cross-GPU PoC Validation</h2>
<h3>L2 Distance Between GPUs (enforce-eager mode)</h3>
<p>All GPU pairs show close distances, meaning PoC validation passes successfully across all architectures within the single image.</p>
<details>
<summary><strong>Cross-version/cross-GPU experiments (6 experiments)</strong></summary>
<table>
<thead>
<tr>
<th>#</th>
<th>GPU Honest</th>
<th>Version</th>
<th>Model</th>
<th>GPU Fraud</th>
<th>Fraud Version</th>
<th>Fraud Model</th>
<th>GPU Validator</th>
<th>Validator Version</th>
<th>Validator Model</th>
<th>Artifacts</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>A800</td>
<td>v0.9.1</td>
<td>Qwen FP8</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen FP8</td>
<td><a href="https://drive.google.com/drive/folders/1ZoNHlDW4zOjMDyMHtbkVychlIBwc_JOA?usp=sharing">artifacts</a></td>
</tr>
<tr>
<td>2</td>
<td>A800</td>
<td>v0.15.1</td>
<td>Qwen FP8</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen FP8</td>
<td><a href="https://drive.google.com/drive/folders/1ZoNHlDW4zOjMDyMHtbkVychlIBwc_JOA?usp=sharing">artifacts</a></td>
</tr>
<tr>
<td>3</td>
<td>A800</td>
<td>v0.15.1</td>
<td>Kimi INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi INT4</td>
<td><a href="https://drive.google.com/drive/folders/1wGgZieGdKzBQHwOK8gYEpIYBwAR8BZ8z?usp=sharing">artifacts</a></td>
</tr>
<tr>
<td>4</td>
<td>A800</td>
<td>v0.15.1</td>
<td>Kimi INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi INT2</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi INT4</td>
<td><a href="https://drive.google.com/drive/folders/1wGgZieGdKzBQHwOK8gYEpIYBwAR8BZ8z?usp=sharing">artifacts</a></td>
</tr>
<tr>
<td>5</td>
<td>A800</td>
<td>v0.15.1</td>
<td>GPT-OSS INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS INT2</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS INT4</td>
<td><a href="https://drive.google.com/drive/folders/1GdoMrwkcMu5kMxVb848TIgDuL6-hHEd1?usp=sharing">artifacts</a></td>
</tr>
<tr>
<td>6</td>
<td>A800</td>
<td>v0.15.1</td>
<td>GPT-OSS INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS INT4</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS INT4</td>
<td><a href="https://drive.google.com/drive/folders/1GdoMrwkcMu5kMxVb848TIgDuL6-hHEd1?usp=sharing">artifacts</a></td>
</tr>
</tbody>
</table>
</details>
<h2>Per-GPU Experiments</h2>
<details>
<summary><strong>Full experiment table (16 experiments)</strong></summary>
<table>
<thead>
<tr>
<th style="text-align: right;">#</th>
<th>GPU</th>
<th>Version</th>
<th>Model</th>
<th style="text-align: right;">Nonces/min</th>
<th style="text-align: right;">8×GPU</th>
<th style="text-align: right;">TP</th>
<th>PoC Vectors</th>
<th>Docker run</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: right;">1</td>
<td>A800 NVLink</td>
<td>v0.9.1</td>
<td>Qwen FP8</td>
<td style="text-align: right;">480</td>
<td style="text-align: right;">960</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1lMMZpa02lj0mHXYuoDkvzzeTz0clVEzo/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">2</td>
<td>A800 NVLink</td>
<td>v0.15.1</td>
<td>Qwen FP8</td>
<td style="text-align: right;">512</td>
<td style="text-align: right;">1 024</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1M-US9sxPa_f8DlBvxLxHEWgDOU-CdZQZ/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">3</td>
<td>A800 NVLink</td>
<td>v0.9.1</td>
<td>Qwen INT4</td>
<td style="text-align: right;">512</td>
<td style="text-align: right;">1 024</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1Wbwrwm2J4PsR8HhLafw53MfU125UCyY2/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">4</td>
<td>A800 NVLink</td>
<td>v0.15.1</td>
<td>Qwen INT4</td>
<td style="text-align: right;">512</td>
<td style="text-align: right;">1 024</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1x3RcVJJbYiGk6ayLuOCc4w93A9QGGFOo/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">5</td>
<td>RTX 6000</td>
<td>v0.9.1</td>
<td>Qwen FP8</td>
<td style="text-align: right;">416</td>
<td style="text-align: right;">832</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/17sYIXIFa8Ex9iMp14A9sgqWHmcUpBoyI/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">6</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen FP8</td>
<td style="text-align: right;">451</td>
<td style="text-align: right;">902</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1k6VgdvdYuvQONi-YRpA5pJ2QFn6OUkjS/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">7</td>
<td>RTX 6000</td>
<td>v0.9.1</td>
<td>Qwen INT4</td>
<td style="text-align: right;">?</td>
<td style="text-align: right;">—</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/12VXHKTYLzhvxhK0K71puJnLwe4zd64RX/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">8</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Qwen INT4</td>
<td style="text-align: right;">400</td>
<td style="text-align: right;">800</td>
<td style="text-align: right;">4</td>
<td><a href="https://drive.google.com/file/d/1RLDuWzqvqkwoQaHXwu3nw9uES7mNXjpo/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1XZG6yL3IW-mlFxKDhWhfB6A4RrWe5Hag/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">9</td>
<td>A800 NVLink</td>
<td>v0.15.1</td>
<td>Kimi K2.5 INT4</td>
<td style="text-align: right;">349</td>
<td style="text-align: right;">349</td>
<td style="text-align: right;">8</td>
<td><a href="https://drive.google.com/file/d/155zGRY2HH6bptw8lc85bKOowN-bvbGZA/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">10</td>
<td>A800 NVLink</td>
<td>v0.15.1</td>
<td>Kimi K2.5 INT2</td>
<td style="text-align: right;">417</td>
<td style="text-align: right;">417</td>
<td style="text-align: right;">8</td>
<td><a href="https://drive.google.com/file/d/1U20bobTBSK3gyEIGS4HNp_6SOJDfARE6/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">11</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi K2.5 INT4</td>
<td style="text-align: right;">258</td>
<td style="text-align: right;">258</td>
<td style="text-align: right;">8</td>
<td><a href="https://drive.google.com/file/d/1Dq1_5gVmv0a5kp7qkY9tR2tQrBHOVlct/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">12</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>Kimi K2.5 INT2</td>
<td style="text-align: right;">288</td>
<td style="text-align: right;">288</td>
<td style="text-align: right;">8</td>
<td><a href="https://drive.google.com/file/d/1HeludcbAP0TCQXDnSGLAdaBH8BHl8TnK/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1Iyk1ae_z5d9hYgXxrGBzQdyVqOsDWTbz/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">13</td>
<td>A800</td>
<td>v0.15.1</td>
<td>GPT-OSS MXFP4</td>
<td style="text-align: right;">472</td>
<td style="text-align: right;">3 776</td>
<td style="text-align: right;">1</td>
<td><a href="https://drive.google.com/file/d/1SSTz_m58aMcvyr07D75bvOVnwddlgjzd/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">14</td>
<td>A800</td>
<td>v0.15.1</td>
<td>GPT-OSS INT2</td>
<td style="text-align: right;">472</td>
<td style="text-align: right;">3 776</td>
<td style="text-align: right;">1</td>
<td><a href="https://drive.google.com/file/d/1pq4pLHS2fPyf5IKD_e7uZF5oYMsYFkJq/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">15</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS MXFP4</td>
<td style="text-align: right;">833</td>
<td style="text-align: right;">6 664</td>
<td style="text-align: right;">1</td>
<td><a href="https://drive.google.com/file/d/1FQksG3gCqNhOGdjM9Q44zb_rlR8T4IT9/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing">command</a></td>
</tr>
<tr>
<td style="text-align: right;">16</td>
<td>RTX 6000</td>
<td>v0.15.1</td>
<td>GPT-OSS INT2</td>
<td style="text-align: right;">833</td>
<td style="text-align: right;">6 664</td>
<td style="text-align: right;">1</td>
<td><a href="https://drive.google.com/file/d/1uXFKZLUwG2Us82vluLCXTsbsytcJEz3i/view?usp=sharing">vectors</a></td>
<td><a href="https://drive.google.com/file/d/1pw-7JKQ_DZUcaenoo0E04XXzfkAytM59/view?usp=sharing">command</a></td>
</tr>
</tbody>
</table>
</details>
<h2>Artifacts</h2>
<table>
<thead>
<tr>
<th>Resource</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Main vLLM 0.15.1 + PoC test branch</td>
<td><a href="https://github.com/kaitakuai/vllm/tree/mb/poc-v015-no-dummy-input-ids">mb/poc-v015-no-dummy-input-ids</a></td>
</tr>
<tr>
<td>Test Docker image</td>
<td><code>ghcr.io/kaitakuai/mlnode:v0.15.1-no-dummy-input-ids</code></td>
</tr>
<tr>
<td>All test images</td>
<td><a href="https://github.com/orgs/kaitakuai/packages">GitHub Packages</a></td>
</tr>
<tr>
<td>Benchmark spreadsheet</td>
<td><a href="https://docs.google.com/spreadsheets/d/1A_wyBQvYNmz0H8bmQxMah53Gj1hjMIOHC19XFAQY6Mg/edit?usp=sharing">Google Sheets</a></td>
</tr>
</tbody>
</table>
<h2>Participants</h2>
<table>
<thead>
<tr>
<th>Participant</th>
<th>GitHub</th>
<th>Contribution</th>
</tr>
</thead>
<tbody>
<tr>
<td>Pavlo</td>
<td><a href="https://github.com/clanster">@clanster</a></td>
<td>GPU testing, benchmark and artifact collection, visualization</td>
</tr>
<tr>
<td>Mykola Baichak</td>
<td><a href="https://github.com/baychak">@baychak</a></td>
<td>Image builds, benchmarks, batching fixes, and torch.compile fixes</td>
</tr>
<tr>
<td>Tamaz Gadaev</td>
<td><a href="https://github.com/tamazgadaev">@tamazgadaev</a></td>
<td>PoC architecture, review, and fixes on the Gonka core team side</td>
</tr>
</tbody>
</table>


  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #730](https://github.com/gonka-ai/gonka/issues/730) every hour.
