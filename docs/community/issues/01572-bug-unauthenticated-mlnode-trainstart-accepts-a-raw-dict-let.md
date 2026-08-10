---
title: "#1572 — [BUG] Unauthenticated mlnode /train/start accepts a raw dict, letting a remote attacker control training and inject arbitrary process environment variables on GPU workers"
source: https://github.com/gonka-ai/gonka/issues/1572
issue_number: 1572
synced_at: 2026-08-10T17:13:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Unauthenticated mlnode /train/start accepts a raw dict, letting a remote attacker control training and inject arbitrary process environment variables on GPU workers
    <span class="issues-number">#1572</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/iceiceic3">@iceiceic3</a> opened 2026-08-10 15:15 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-10 15:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
**Summary**
The mlnode control API exposes POST /api/v1/train/start with no authentication and no schema — the handler takes a raw dict. From that dict, the service sets arbitrary process environment variables (os.environ[key] = value for every attacker-supplied key), writes an attacker-supplied training config to disk, and launches a training subprocess. An unauthenticated remote attacker can therefore start/stop training on any reachable GPU worker (control-plane denial of service and resource abuse) and inject arbitrary environment variables into the mlnode process and its children. The reference deployment publishes this API on 0.0.0.0:8080.

**Motivation**
This is the second half of an entirely unauthenticated control surface on the GPU workers (the first being /inference/up). Even though the direct remote-code-execution vectors through this endpoint are blocked by the project’s pinned dependency versions (documented honestly below), the endpoint still hands an anonymous attacker the training control plane and the process environment of a machine that holds GPUs, model weights, and PoC-signing material. Environment-variable control is a well-known lever for behavior subversion and exfiltration, and the control-plane access alone is a fleet griefing/DoS primitive. It is worth fixing alongside the inference RCE because both stem from the same missing authentication layer.

**Impact**

- Who is affected (hosts, developers, validators): GPU-worker hosts (mlnode operators). The wider network is affected indirectly through worker griefing/DoS and potential PoC-behavior subversion.
- Is effect network-wide or limited: Per reachable host: control-plane takeover + arbitrary process environment. Fleet-wide to the extent multiple workers expose :8080. Not a network-consensus-wide effect on its own.
- Likelihood (common, intermittent, edge case, or intentional attack): Intentional — Griefing, trivially reachable (single unauthenticated POST) where the port is exposed. Rated High likelihood on the reference compose.
- Severity Impact × Likelihood: Impact Medium (single/host-scope control-plane + environment control; no direct chain-wide effect, and direct RCE is mitigated by pins) × Likelihood High → High (per Gonka risk matrix, Medium × High = High). Conservative reading: if scored as a purely single-participant availability/integrity issue, Impact Medium × Likelihood Medium = Medium — stated so triage can calibrate.
- Affected components: mlnode/packages/api (unauthenticated app), mlnode/packages/train (service/routes.py, service/manager.py, scripts/run-diloco-node.sh, train.py), deploy/join/docker-compose.mlnode.yml.

**Detailed description**
**Verified flow (commit f040d0a), unauthenticated end-to-end:**
- **No auth (same app as the inference endpoint)**. mlnode/packages/api/src/api/app.py: the only router Depends() is the state-guard check_service_conflicts (lines 92 / 99 / 106); no credential/token/IP check anywhere (grep for auth primitives across mlnode/packages/api/src/ non-test returns zero hits). Published on 0.0.0.0:8080 via deploy/join/docker-compose.mlnode.yml.
- **Raw dict entry, no validation**. mlnode/packages/train/src/zeroband/service/routes.py:8-14: POST /train/start takes training_dict: dict and calls manager.start_async(training_dict) — no pydantic schema, no auth.
- **Arbitrary environment variables**. service/manager.py:40-42: set_training_env(train_env_dict) runs for key, value in train_env_dict.items(): os.environ[key] = value — every attacker-chosen key/value becomes a process env var, inherited by all child processes.
- **Attacker config written to disk**. service/manager.py:58-59 serializes train_dict["train_config"] to train_config.toml.
- Subprocess spawn. service/manager.py:61-68: subprocess.Popen(["bash", "run-diloco-node.sh", "src/zeroband/train.py", "@train_config.toml"]).

**Verification note — why this is not the shell-injection / malicious-model Critical (honest correction; do not overclaim):** an earlier draft called this a Critical RCE. Full source verification disproved every direct code-exec vector through this endpoint:
- **The unquoted $@ in run-diloco-node.sh:72-79 is NOT attacker-controlled**. The script’s positional arguments are the fixed src/zeroband/train.py @train_config.toml set at manager.py:61-68; the attacker never controls $@. train.py:287 parses @train_config.toml via pydantic_config.parse_argv() into a typed Config, so TOML values become typed fields (ints, floats, enums, bounded sub-configs), not shell-re-expanded strings.
- **No attacker-chosen model**. train.py:36,52 load a hardcoded meta-llama/Llama-3.2-1B-Instruct with no trust_remote_code.
- **Dataset-script execution is mitigated**. data.dataset_name_or_paths is attacker-controllable and reaches datasets.load_dataset() (data/loader.py:110), but pyproject.toml pins datasets >= 4.0.0, which removed dataset loading scripts — no arbitrary-code dataset path.
- **Pickle torch.load is mitigated and unreachable.** monitor/checkpoint.py:301,308,336 use torch.load, but pyproject.toml pins torch >= 2.8.0 (default weights_only=True), and CkptManager.load() / _load_data() are never called from train.py (only save) — so the resume/pickle path is not reachable via /train/start at all.

**What genuinely remains (still serious):** an unauthenticated remote attacker can (a) start/stop training on any reachable GPU worker — a control-plane DoS and resource-abuse primitive — and (b) inject arbitrary environment variables into the mlnode process and its children, which can subvert behavior and enable exfiltration depending on child binaries (e.g. HF_*, HTTP_PROXY/HTTPS_PROXY, and other env-driven configuration). On the same unauthenticated surface as the inference RCE, the worker is effectively attacker-controlled.

**Reproduction (isolated local harness only — no live testing performed):**
- Boot the mlnode stack locally: docker compose -f deploy/join/docker-compose.mlnode.yml up -d api (test fixtures only).
- Send, unauthenticated: curl -s -X POST http://127.0.0.1:8080/api/v1/train/start -H 'Content-Type: application/json' -d '{"train_env":{"HTTP_PROXY":"http://127.0.0.1:9","HF_ENDPOINT":"http://127.0.0.1:9"},"train_config":{...minimal valid config...}}'.
- Observe that (a) the attacker-supplied env vars are set on the mlnode process (they are inherited by the spawned training subprocess), and (b) training is started/stopped at the anonymous caller’s command. All artifacts are local test fixtures. The PoC deliberately stays to the provable primitives (env injection + control-plane) and does not claim shell/model code-exec, which verification ruled out.

**Precondition:** the mlnode API port must be reachable. The reference deploy/join compose binds 0.0.0.0:8080; a firewalled deployment downgrades this to authenticated-network scope.

**Links to evidence:** mlnode/packages/api/src/api/app.py:92,99,106; service_management.py:58-60; service/routes.py:8-14; service/manager.py:40-42,58-59,61-68; scripts/run-diloco-node.sh:72-79; train.py:36,52,287; data/loader.py:110; monitor/checkpoint.py:301,308,336; pyproject.toml:16-24; deploy/join/docker-compose.mlnode.yml.

**Suggested remediation:** require authentication on the mlnode control API; validate /train/start against a strict schema; remove set_training_env or restrict it to an allowlist of safe keys; never bind 8080 to 0.0.0.0 in the reference deployment.

[report-3-train-controlplane.zip](https://github.com/user-attachments/files/30904359/report-3-train-controlplane.zip)
</div>

---

> 🔄 **Auto-synced** from [Issue #1572](https://github.com/gonka-ai/gonka/issues/1572) every hour.
