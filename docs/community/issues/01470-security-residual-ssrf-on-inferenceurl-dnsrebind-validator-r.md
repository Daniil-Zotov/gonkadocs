---
title: "#1470 — Security: Residual SSRF on InferenceUrl — DNS/rebind + validator redirect (incomplete fix after #505/#534)"
source: https://github.com/gonka-ai/gonka/issues/1470
issue_number: 1470
synced_at: 2026-07-27T11:44:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Security: Residual SSRF on InferenceUrl — DNS/rebind + validator redirect (incomplete fix after #505/#534)
    <span class="issues-number">#1470</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 2026-07-18 03:05 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-20 02:30 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

**Residual SSRF** after prior paid mitigations (v0.2.7 / v0.2.8):

| Prior fix | What it covered | What remains broken |
|-----------|-----------------|---------------------|
| [PR #534](https://github.com/gonka-ai/gonka/pull/534) | TA client **no redirects** (`NewNoRedirectClient`) | Direct dial to DNS→private IP still allowed |
| [PR #505](https://github.com/gonka-ai/gonka/pull/505) | `ValidateURLWithSSRFProtection` rejects **literal** private IPs | **No DNS resolve**; hostnames always pass |

Any participant-controlled `InferenceUrl` hostname (or public URL that **redirects**) can force **validator DAPIs** (and other sinks) to connect to loopback, link-local metadata (`169.254.169.254`), or RFC1918 during **mandatory** payload retrieval / PoC validation / TA executor forwarding.

This is incomplete remediation, not a greenfield finding.

---

## Severity (self-assessment)

**High** — protocol-mandated HTTP from validator hosts to attacker-controlled URL; host infrastructure compromise (IMDS, localhost admin, internal network). Not direct on-chain fund drain.

---

## Architecture / threat model

```
Attacker sets InferenceUrl (hostname / rebind / open redirect)
        │
        ▼
   Chain: Participant.InferenceUrl
        │
   ┌────┴─────────────────┬──────────────────┐
   ▼                      ▼                  ▼
Validator payload     TA → executor       PoC off-chain
retrieval (primary)   POST                proof HTTP
DEFAULT http.Client   NoRedirectClient    multi-worker
FOLLOWS REDIRECTS     still dials DNS IP
```

**Attacker preconditions**

- Can set/update `InferenceUrl` via `MsgSubmitNewParticipant` / unfunded variant while `OpenRegistrationPermission` allows, **or**
- Already has a **hostname** URL on-chain → **DNS rebinding** needs **no new tx**

**Victim:** any honest host running DAPI that validates / TAs / PoC-validates against that participant.

---

## Root cause (registration gate)

`inference-chain/x/inference/utils/signature_and_url_validation.go`:

```go
func ValidateURLWithSSRFProtection(fieldName, raw string) error {
    // scheme http/https + host non-empty
    if isLocalhost(host) { return err }
    ip := net.ParseIP(host)
    if ip != nil {
        if isPrivateIP(ip) { return err }
    }
    return nil // hostname path: NEVER resolves DNS
}
```

Called from:

- `types/message_submit_new_participant.go` `ValidateBasic`
- `types/message_submit_new_unfunded_participant.go` `ValidateBasic`

Unit tests only cover: public URL, `localhost`, `192.168.0.1` — **no hostname/DNS cases**  
(`signature_and_url_validation_test.go`).

### Matrix (registration)

| URL | Gate result | Notes |
|-----|-------------|--------|
| `http://127.0.0.1/` | REJECT | literal |
| `http://169.254.169.254/` | REJECT | literal |
| `http://localtest.me/` | **ACCEPT** | DNS → 127.0.0.1 |
| `http://ssrf.attacker.tld/` | **ACCEPT** | attacker DNS |
| `http://0x7f000001/` / decimal IP strings | **ACCEPT*** | `ParseIP` fails → hostname |
| `http://[::ffff:127.0.0.1]/` | REJECT | mapped IPv6 parsed |

\*Depends on OS resolver if those “hostnames” resolve.

---

## URL write path

`keeper/msg_server_submit_new_participant.go`:

- **Create** participant with `Url`
- **Update** existing: `existing.InferenceUrl = msg.Url` (same permission gate)

DAPI registers `PublicUrl` via `participant_registration.go`.

If registration later closes, create/update txs fail — **rebinding still works** for hostnames already stored.

---

## HTTP sinks (all participant `InferenceUrl`)

### 1) Validator payload retrieval — **primary**

```
validateInferenceAndSendValMessage
  → retrievePayloadsWithRetry  // up to 10 attempts, long backoff
      → RetrievePayloadsFromExecutor
          → Participant.InferenceUrl from chain
          → BuildPayloadRequestURL(..., "v1/inference/payloads", id)
          → FetchPayloadsHTTP(payloadRetrievalClient, ...)
```

```go
// decentralized-api/internal/validation/payload_retrieval.go
var payloadRetrievalClient = &http.Client{
    Timeout: 30 * time.Second,
    // no CheckRedirect → default Go client follows up to 10 redirects
    // no DialContext IP ACL
}
```

Also sends validator identity headers (`X-Validator-Address`, signature, epoch) to whatever is dialed.

### 2) Transfer Agent → executor

```
getExecutorForRequest → GetRandomExecutor → executor.InferenceUrl
POST via NewNoRedirectClient  // redirects blocked (#534)
```

Direct **DNS → private IP** still dials.

### 3) PoC off-chain validator

`decentralized-api/poc/validator.go` — loads `InferenceUrl`, parallel proof HTTP workers.

### 4) Devshard

Reuses `FetchPayloadsHTTP` / `BuildPayloadRequestURL`.

### Not a fix: proxy sidecar

`proxy/sidecar` resolves DNS and skips private IPs only when building nginx **whitelist** — does **not** stop DAPI egress SSRF.

---

## Attack chains

### A — DNS hostname (register/update)

1. Point `ssrf.attacker.tld` → `169.254.169.254` / internal IP / loopback  
2. `MsgSubmitNewParticipant{ Url: "http://ssrf.attacker.tld" }`  
3. Passes `ValidateBasic`  
4. When peers validate / TA / PoC-hit this host → SSRF

### B — DNS rebinding (no chain update)

1. Register hostname with public A record  
2. During validation window, flip A to private (low TTL)  
3. No on-chain re-validation at fetch time  

### C — Redirect residual (validator payload client only)

1. `InferenceUrl = http://attacker.example/open` (public, accepts registration)  
2. Attacker responds `302 Location: http://127.0.0.1:9200/admin/v1/config` (or IMDS)  
3. TA client will **not** follow; **`payloadRetrievalClient` will**  
4. Can turn this into **localhost admin/config impact on validators** without publishing admin ports  

---

## Lab proof (safe, local)

Using public DNS name `localtest.me` → `127.0.0.1`:

1. `http://127.0.0.1:PORT/...` → **REJECT** (literal)  
2. `http://localtest.me:PORT/...` → **ACCEPT** (hostname)  
3. Validator-style HTTP GET retrieves loopback service body (exfiltrates lab secret)

Runnable replica (research package): registration gate replica + e2e fetch against local victim service.

---

## Impact

| Impact | Detail |
|--------|--------|
| Confidentiality | Cloud IMDS, internal HTTP, localhost admin/config on validators |
| Integrity | Pivot into host networks; secondary compromise of DAPI/node |
| Availability | Hang/slow validators on attacker-controlled responses; retry amplification (×10) |
| Scale | Every honest validator that retrieves payloads becomes an SSRF client |

---

## Required remediation

1. **Dial-time deny-list** (mandatory): shared safe `http.Client` that resolves, rejects loopback/link-local/RFC1918/ULA, dials only public IPs  
2. Apply to **all** sinks: `payloadRetrievalClient`, PoC proof client, TA client (defense-in-depth)  
3. Disable redirects on payload client **or** re-check `Location` host/IPs with the same policy  
4. Registration-time resolve is optional extra; **not sufficient alone** (rebinding)  
5. Regression tests: hostname→127.0.0.1, hostname→169.254.169.254, public→302 private, IPv4-mapped IPv6, decimal/hex host strings  

### Sketch

```go
// DialContext: LookupIP → reject isPrivateIP → dial public only
// CheckRedirect: ErrUseLastResponse OR validate Location with same policy
```

---

## Evidence index

| Path | Role |
|------|------|
| `inference-chain/x/inference/utils/signature_and_url_validation.go` | Gate gap |
| `inference-chain/x/inference/utils/signature_and_url_validation_test.go` | Thin tests |
| `inference-chain/x/inference/types/message_submit_new_participant.go` | ValidateBasic |
| `inference-chain/x/inference/keeper/msg_server_submit_new_participant.go` | Create/update URL |
| `decentralized-api/internal/validation/payload_retrieval.go` | Client + sink |
| `decentralized-api/internal/validation/inference_validation.go` | Retry loop |
| `decentralized-api/internal/server/public/post_chat_handler.go` | TA NoRedirect + executor URL |
| `decentralized-api/poc/validator.go` | PoC sink |
| `inference-chain/app/upgrades/v0_2_8/upgrades.go` | Prior bounty / PR #505 #534 context |

---

## Disclosure

- Static analysis + **local lab only**; no production hosts targeted.  
- If public issues are not preferred, please close and accept via **HackerOne** ([gonka.ai report vulnerability](https://gonka.ai/docs/report-vulnerability/)); we can re-file privately with PoC artifacts.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a></span>
    <span class="issues-meta-item">commented 2026-07-18 03:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Deep dive (follow-up analysis)</h2>
<h3>Historical context (residual after prior SSRF fixes)</h3>
<p>From <code>inference-chain/app/upgrades/v0_2_8/upgrades.go</code> bounty notes:</p>
<ul>
<li><strong>PR #534</strong> — blocked <strong>redirect</strong>-based SSRF on the Transfer Agent HTTP client (<code>NewNoRedirectClient</code>).</li>
<li><strong>PR #505</strong> — added <code>ValidateURLWithSSRFProtection</code> for <code>InferenceUrl</code> (literal private IPs + timeouts).</li>
</ul>
<p>This report is a <strong>residual / incomplete-fix</strong> issue, not a greenfield class:</p>
<table>
<thead>
<tr>
<th>Layer</th>
<th>Status after #505/#534</th>
</tr>
</thead>
<tbody>
<tr>
<td>Registration string check</td>
<td>Literal private IPs only — <strong>no DNS resolve</strong></td>
</tr>
<tr>
<td>TA client redirects</td>
<td>Fixed (<code>CheckRedirect</code> → <code>ErrUseLastResponse</code>)</td>
</tr>
<tr>
<td>Validator <code>payloadRetrievalClient</code></td>
<td><strong>Still default <code>http.Client</code> → follows redirects</strong></td>
</tr>
<tr>
<td>Dial-time IP ACL on any sink</td>
<td><strong>Missing</strong></td>
</tr>
<tr>
<td>Re-validate URL at fetch time</td>
<td><strong>Missing</strong> (DNS rebinding works without new txs)</td>
</tr>
</tbody>
</table>
<h3>Full sink map (participant <code>InferenceUrl</code> → HTTP)</h3>
<ol>
<li>
<p><strong>Validator payload retrieval (primary)</strong><br />
<code>validateInferenceAndSendValMessage</code> → <code>retrievePayloadsWithRetry</code> (up to 10 attempts) → <code>RetrievePayloadsFromExecutor</code> →<br />
<code>BuildPayloadRequestURL(InferenceUrl, "v1/inference/payloads", id)</code> → <code>FetchPayloadsHTTP</code><br />
   Client: <code>payloadRetrievalClient = &amp;http.Client{Timeout: 30s}</code> — <strong>no <code>CheckRedirect</code>, no dial ACL</strong>.</p>
</li>
<li>
<p><strong>Transfer Agent → executor</strong><br />
<code>getExecutorForRequest</code> → <code>executor.InferenceUrl</code> → <code>POST</code> via <code>NewNoRedirectClient</code><br />
   Redirects blocked; <strong>direct DNS→private IP still dials</strong>.</p>
</li>
<li>
<p><strong>PoC off-chain validator</strong><br />
<code>poc/validator.go</code> loads <code>Participant.InferenceUrl</code> and hits it via proof HTTP client (parallel workers).</p>
</li>
<li>
<p><strong>Devshard paths</strong> reuse <code>FetchPayloadsHTTP</code> / <code>BuildPayloadRequestURL</code>.</p>
</li>
</ol>
<p>Proxy sidecar <em>does</em> resolve DNS and skips private IPs — but only for nginx <strong>whitelist generation</strong>, not for DAPI egress.</p>
<h3>Attack chains</h3>
<p><strong>A. DNS hostname (registration-time)</strong><br />
<code>MsgSubmitNewParticipant{Url: "http://ssrf.attacker.tld"}</code> with A/<code>AAAA</code> → <code>169.254.169.254</code> / RFC1918 / loopback.<br />
<code>ValidateBasic</code> accepts because <code>net.ParseIP(hostname) == nil</code>.</p>
<p><strong>B. DNS rebinding (no chain update)</strong><br />
Register hostname with public A record; later flip A to private during validation windows. No re-check at fetch.</p>
<p><strong>C. Redirect residual (validator only)</strong><br />
Public <code>InferenceUrl</code> returns <code>302 Location: http://127.0.0.1:9200/admin/v1/config</code> (or IMDS).<br />
TA client will not follow; <strong><code>payloadRetrievalClient</code> will follow</strong> → can turn #1470 into localhost admin/config impact on validators.</p>
<h3>Control-flow gap (source)</h3>
<pre><code class="language-go">// signature_and_url_validation.go
ip := net.ParseIP(host)
if ip != nil {
    if isPrivateIP(ip) { return err }
}
return nil // hostname path never resolves
</code></pre>
<p>Unit tests only cover public URL, localhost, and <code>192.168.0.1</code> — no hostname/DNS cases.</p>
<h3>URL write path</h3>
<p>Existing participants can update <code>InferenceUrl</code> via the same <code>MsgSubmitNewParticipant</code> (when <code>OpenRegistrationPermission</code> allows).<br />
Even if registration is later closed, <strong>rebinding</strong> still works for already-stored hostnames.</p>
<h3>Lab proof (safe)</h3>
<p><code>localtest.me</code> → <code>127.0.0.1</code>:</p>
<ol>
<li>Literal <code>http://127.0.0.1:...</code> → REJECT  </li>
<li><code>http://localtest.me:...</code> → ACCEPT  </li>
<li>Validator-style GET retrieves loopback service content  </li>
</ol>
<h3>Required fix (defense-in-depth)</h3>
<ol>
<li><strong>Dial-time</strong> deny-list (resolve → reject loopback/link-local/RFC1918/ULA) in a shared safe <code>http.Client</code>.  </li>
<li>Apply to <strong>all</strong> sinks: payload retrieval, PoC client, (defense-in-depth) TA client.  </li>
<li>Disable redirects on payload client <strong>or</strong> re-check <code>Location</code> host/IPs.  </li>
<li>Regression tests: hostname→127.0.0.1, hostname→169.254.169.254, public→302 private, IPv4-mapped IPv6.</li>
</ol>
<p>Happy to provide a draft patch or HackerOne-formatted write-up if public issues are not the preferred channel.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-07-20 02:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to pick this up. The residual-SSRF analysis matches what I see in the code — the real fix has to be at dial-time (registration-time DNS resolution alone can't stop rebinding), via a shared SSRF-safe HTTP client applied to all participant-<code>InferenceUrl</code> sinks, plus disabling redirects on the payload retrieval client.</p>
<p>@tcharchian could you assign this to me?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1470](https://github.com/gonka-ai/gonka/issues/1470) every hour.
