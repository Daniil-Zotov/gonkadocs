---
title: "#447 — Node Registration Does Not Update After Migration (API stuck using old on-chain config)"
source: https://github.com/gonka-ai/gonka/issues/447
issue_number: 447
synced_at: 2026-08-09T10:56:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Node Registration Does Not Update After Migration (API stuck using old on-chain config)
    <span class="issues-number">#447</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Asplana92">@Asplana92</a> opened 2025-11-20 03:02 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-11 19:09 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
🐞 [BUG] Node Registration Cannot Update After Migration (stuck on old on-chain state; diff returns no changes)
Summary

After migrating the ML inference server to new infrastructure and switching from an unsupported model (Llama) to a governance-approved one (Qwen2.5-7B-Instruct), the node becomes permanently stuck using outdated on-chain registration data.

Even though node_config.json contains the correct configuration and the API reads it correctly on startup, the API never submits an update transaction, because the diff logic always reports “No differences”, even when the on-chain state is completely different.

This leaves the operator unable to recover or participate in inference, even with fully correct infrastructure.


✅ Expected Behavior

When node_config.json changes (host, port, hardware, models),
→ API should detect differences.
→ API should submit an update transaction.
→ On-chain registration should be updated.


❌ Actual Behavior

API loads correct local config

On-chain data is old and completely mismatched

But diff logic reports:
[sync nodes] Hardware diff: NewOrModified:[] Removed:[]
[sync nodes] No diff to submit
API then continues to use the old host + port, even though they are no longer valid:
ERROR: queryNodeStatus → dial tcp OLD_IP:8081 → connection refused
Node is stuck in FAILED state across epochs.


📌 Timeline & Reproduction Story

This issue appeared during a normal model migration, following official guidance.

(1) Initial setup (worked, but received 0 assignments)

Model: Meta-Llama-3.1-8B-Instruct

Framework: llama.cpp

Host: old_IP:8081

Hardware: RTX 4090

Registered successfully

Received 0 inference tasks for multiple epochs, so decision was made to switch to a governance model.

(2) Official guidance from Discord

Gonka team advised:

Llama is not governance-supported

Required: models from https://gonka.hyperfusion.io/v1/models

Recommended: use vLLM

Also required: additional disk space

So migration to new hardware was performed.

(3) Infrastructure migration
A new server with enough disk space was deployed:
Inference server:
- GPU: RTX 4090
- Disk: ~90GB
- Model: Qwen/Qwen2.5-7B-Instruct
- Framework: vLLM
- vLLM running on port 8081

Validation:
curl http://localhost:8081/v1/models
→ returns Qwen2.5-7B-Instruct   (OK)

(4) node_config.json updated
Correct configuration:
[{
  "id": "node1",
  "host": "NEW_IP",
  "inference_port": 8081,
  "poc_port": 8081,
  "models": { "Qwen/Qwen2.5-7B-Instruct": { "args": [] }},
  "hardware": [{ "type": "NVIDIA RTX 4090", "count": 1 }],
  "max_concurrent": 500
}]


(5) API reads config correctly
Startup logs:
INFO Registered node:
Host: NEW_IP
InferencePort: 8081
Models: Qwen/Qwen2.5-7B-Instruct
Hardware: RTX 4090

(6) BUT the API immediately switches back to old on-chain data
ERROR queryNodeStatus
dial tcp OLD_IP:8081 → connection refused

(7) On-chain query shows old/corrupted data
host: "inference"                (incorrect)
port: "8080"                     (incorrect)
models: Qwen3-235B-*             (incorrect)
hardware: H200 140GB             (incorrect)
No fields match local config.

(8) Diff logic incorrectly concludes “no changes”
[sync nodes] Local nodes: 1
[sync nodes] Chain nodes: 1
[sync nodes] Hardware diff: NewOrModified:[] Removed:[]
[sync nodes] No diff to submit

As a result:

No update transaction is sent

Node cannot join inference

Node stays FAILED each epoch

Operator is permanently stuck


🔍 Root Cause (Hypothesis)

The problem seems to be triggered by a combination of:

1. Old registration containing invalid values

(e.g. models not in governance list, incorrect hardware type, host="inference")

2. API’s diff logic

Fails to detect differences between:

local node_config.json

on-chain corrupted registration

This is likely because the comparison:

ignores certain fields

or normalizes the structures so differently that mismatches become “equal”

or treats missing fields as defaults that match

3. Stale on-chain registration overrides local state

Even after deleting:
rm -rf ~/.dapi
and restarting API, the old chain state overwrites config-dump.json.

Result

The operator has no way to force re-registration, even with valid config + valid model.



🧪 Steps to Reproduce (Generalized)

Register a node with a model that was once accepted but is now invalid (e.g. before governance model validation was strict)

Later switch to a different model + different infra:

new host

new port

new model

new hardware specs

Update local config

Restart API

API loads correct local config

API loads outdated on-chain data

API diff logic sees no differences

API never submits update transaction

Node remains stuck in FAILED



🎯 Impact

Node cannot join inference for many epochs

Operator cannot fix the issue manually

Registry becomes permanently stuck in invalid state

Requires team intervention to force removal or re-registration



📝 What would help resolve the issue

Please advise:

1. Is there a way to force a fresh registration?

(e.g. delete existing hardware-node entry on chain)

2. Should operators create a new node ID instead of updating existing nodes?
3. Is this a known issue with the current diff logic?

The behavior strongly suggests it.

4. Should the compare logic be updated to catch mismatched:

host

ports

hardware type

model list

number of models

missing fields

defaults vs explicit values

These should always trigger a diff.




🙏 Thank you

This report is intended to help improve the reliability of node onboarding and recovery, especially during model migrations.

If additional logs are needed, I can provide:

full API startup logs

vLLM logs

config-dump.json snapshots

raw output of inferenced query inference hardware-nodes-all










</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/ASLanin">@ASLanin</a></span>
    <span class="issues-meta-item">commented 2025-11-24 21:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>As far as I get it the api container's (ghcr.io/product-science/api:0.2.5) main process does not reread or at least do not apply <code>node-config.json</code> after the first time creation of  the <code>.dapi/gonka.db</code>
query from the db <code>sqlite&gt; SELECT * FROM inference_nodes LIMIT 20;</code> shows first time used data in <code>models_json</code> regardless of <code>node-config.json</code> contents at the last run. May be all other params are WORM in db.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-06-11 19:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I dug into this from the current <code>main</code> code while looking for the cause, and found two separate layers that together produce the "stuck registration" behavior. Sharing in case it helps — I'm a contributor, not a maintainer, so treat the design parts as observations.</p>
<p><strong>Layer 1 — <code>node_config.json</code> is merged only once, by design.</strong>
<code>ConfigManager.LoadNodeConfig</code> (<code>decentralized-api/apiconfig/config_manager.go</code>) merges <code>node_config.json</code> into the API's local database a single time, gated by a <code>node_config_merged</code> flag stored in that database. After the first run, edits to <code>node_config.json</code> are intentionally ignored ("Node config already merged. Skipping"). Runtime node management is expected to go through the admin API instead: <code>POST/PUT/DELETE /admin/v1/nodes</code> (<code>internal/server/admin/server.go</code>). Two practical consequences for your case:</p>
<ul>
<li>Updating an existing node: <code>PUT /admin/v1/nodes/{id}</code> with the new host/port/models/hardware updates local state without touching config files.</li>
<li>A fresh database does re-trigger the merge, but only if <code>NODE_CONFIG_PATH</code> is set in the API container's environment — if it isn't, the loader logs "NODE_CONFIG_PATH not set. No additional nodes will be added to config" and loads nothing. That might explain why wiping <code>~/.dapi</code> appeared not to help.</li>
</ul>
<p><strong>Layer 2 — host/port changes were never synced to chain, even with correct local state.</strong>
The 60-second sync loop decides whether to resubmit a node by comparing it to the on-chain record with <code>areHardwareNodesEqual</code> (<code>decentralized-api/broker/broker.go</code>). That comparison covered id, status, hardware, models and version — but not <code>Host</code> or <code>Port</code>, although both are submitted and stored on chain. So a migration that only changes the endpoint (same GPU, same models) was reported as "no diff" forever, including after an admin-API update. I've opened #1337 to fix this.</p>
<p>Note that your specific snapshot (on-chain models/hardware completely different from local config, yet "No diff to submit") points at layer 1: the broker was still operating on the old local state from the database, so local and chain genuinely matched. With local state corrected via the admin API (or a re-merge), the model/hardware differences should already trigger a submission today; #1337 additionally covers the host/port-only case.</p>
<p>One related limitation while reading the code: <code>InferencePort</code> is not part of the on-chain <code>HardwareNode</code> record at all (only the PoC port is stored), so inference-port-only changes can't be detected by this mechanism regardless.</p>
<p>Whether <code>node_config.json</code> should stay merge-once (vs. re-syncing on restart) is a design question for the maintainers — the operator expectation in this issue suggests it at least deserves clearer documentation.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #447](https://github.com/gonka-ai/gonka/issues/447) every hour.
