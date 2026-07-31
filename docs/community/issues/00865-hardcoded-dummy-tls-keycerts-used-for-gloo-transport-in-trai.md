---
title: "#865 — Hard‑coded dummy TLS key/certs used for Gloo transport in training manager Body"
source: https://github.com/gonka-ai/gonka/issues/865
issue_number: 865
synced_at: 2026-07-31T07:19:39Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Hard‑coded dummy TLS key/certs used for Gloo transport in training manager Body
    <span class="issues-number">#865</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/VVSMEN">@VVSMEN</a> opened 2026-03-05 13:09 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-12 20:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
### Summary
The ML training manager for the `mlnode` component is currently configured to use hard‑coded dummy TLS credentials for Gloo’s `TCP_TLS` transport. These credentials are stored in the repository and wired into the runtime via environment variables. The code still contains a `TODO` comment indicating that real certificates should replace these placeholders, but this change has not yet been implemented.

**Risk level:** Medium (configuration / crypto hygiene; impact depends on deployment model and network exposure)  
**Affected component:** `mlnode/packages/train/src/zeroband/service/manager.py` (plus bundled test key in `mlnode/packages/train/resources/certs/dummy.key`)

---

### Technical Details

#### Where is the dummy key?
The private key file is present in the repository:
```
mlnode/packages/train/resources/certs/dummy.key
```
(there is also a matching `dummy.crt` in the same directory)  
This is a full PEM‑formatted private key committed to the repo.

#### How is it used by Gloo?
In `mlnode/packages/train/src/zeroband/service/manager.py`, the training manager wires these dummy credentials into Gloo’s TLS transport:

```python
# mlnode/packages/train/src/zeroband/service/manager.py
# ...

def set_gloo_certs(self, private_key_path: str, node_cert_path: str, ca_cert_path: str):
    """
    Configure Gloo to use TCP_TLS with the provided key and certificates.
    """
    os.environ["GLOO_DEVICE_TRANSPORT"] = "TCP_TLS"
    os.environ["GLOO_DEVICE_TRANSPORT_TCP_TLS_PKEY"] = private_key_path
    os.environ["GLOO_DEVICE_TRANSPORT_TCP_TLS_CERT"] = node_cert_path
    os.environ["GLOO_DEVICE_TRANSPORT_TCP_TLS_CA_FILE"] = ca_cert_path

def _start(self, train_dict: dict):
    if self.process is not None:
        raise RuntimeError("Training is already running")

    # TODO: Replace with actual certs when integrated
    self.set_gloo_certs(
        os.path.join(CERTS_DIR, "dummy.key"),
        os.path.join(CERTS_DIR, "dummy.crt"),
        os.path.join(CERTS_DIR, "dummy.crt")   # CA points to the same self‑signed cert
    )
    # ...
```

**Key points:**
- Gloo is explicitly configured to use `TCP_TLS`.
- The private key (`GLOO_DEVICE_TRANSPORT_TCP_TLS_PKEY`) and certificate/CA values are always set to `dummy.key` / `dummy.crt` from the repo.
- The `TODO: Replace with actual certs when integrated` comment indicates this was intended as a temporary/testing setup.
- As of the latest commit I pulled locally, this `TODO` is still present and the dummy files are still referenced.

#### Why this is a problem
- **Shared static key:** The same private key is committed to the public repository and reused across all deployments that don’t override it. Anyone with repo access can know this key.
- **No per‑deployment isolation:** There is no built‑in mechanism to enforce using deployment‑specific certificates/keys.
- **Potential for MITM / impersonation (depending on deployment):** If Gloo traffic can be observed or intercepted (e.g., in a multi‑tenant environment, misconfigured network, or if an attacker has partial access), knowledge of the private key and certificate makes it easier to impersonate legitimate Gloo endpoints or terminate TLS traffic.
- Actual impact depends on how/where this training stack is deployed (e.g., isolated lab vs. shared cluster vs. cloud), but as a default configuration, shipping live code that wires in a known test key is a security anti‑pattern.

---

### Status
- The `dummy.key` private key is present in the repository under `mlnode/packages/train/resources/certs/`.
- The training manager (`service/manager.py`) still uses this dummy key and certificate by default, with the `TODO: Replace with actual certs when integrated` comment unchanged in the current revision.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tamazgadaev">@tamazgadaev</a></span>
    <span class="issues-meta-item">commented 2026-03-12 19:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This was a quick debug fix. Training is not currently supported and basically needs total revision, so I'd say this issue low-priority</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-12 20:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>It’s hardcoded for test pipeline, on purpose</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #865](https://github.com/gonka-ai/gonka/issues/865) every hour.
