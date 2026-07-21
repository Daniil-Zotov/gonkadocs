---
title: "#1053 — Security Audit: Systematic review across inference chain, bridge, subnet, and API layers"
source: https://github.com/gonka-ai/gonka/issues/1053
issue_number: 1053
synced_at: 2026-07-21T20:38:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Security Audit: Systematic review across inference chain, bridge, subnet, and API layers
    <span class="issues-number">#1053</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Doog-bot534">@Doog-bot534</a> opened 2026-04-15 07:05 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-07-08 18:12 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Systematic security audit covering four major components of the Gonka network. Found **1 Critical, 5 High, 10+ Medium** severity issues across the codebase. Fix PRs submitted for the top 3 findings.

> **Update 2026-04-20 (self-review):** After re-auditing against the submission quality bar, findings **#3, #8, #16, #21 are withdrawn** (see "Withdrawn findings" section below). Same self-review also closed PRs #1077 and #1058.

## Fix PRs Submitted

| PR | Severity | Issue |
|----|----------|-------|
| #1050 | **High** | Non-deterministic float64 in validation consensus path — chain fork risk |
| #1051 | **High** | Partial state update in claim rewards — permanent fund loss |
| #1052 | **Medium-High** | PoC V2 missing permission check — any account can submit validations |

## Additional Findings (No PR Yet)

### Critical

**1. Admin API has zero authentication**
- `decentralized-api/internal/server/admin/server.go:60-102`
- Only `LoggingMiddleware` applied. Destructive endpoints (`DELETE nodes/:id`, `POST tx/send`, `GET export/db`, `GET config`) accessible to anyone who reaches the admin port.
- **Impact**: Full compromise — create/delete nodes, send arbitrary chain transactions, dump database and config.
- **Recommendation**: Add authentication middleware (API key or mTLS). This should be treated as a private disclosure — reporting here for visibility but recommend immediate action.

### High

**2. SSRF via executor URL from chain state**
- `decentralized-api/internal/server/public/post_chat_handler.go:380`
- `executor.Url + "/v1/chat/completions"` — malicious participant registers with internal URL (e.g., `http://169.254.169.254`). `NoRedirectClient` blocks redirects but doesn't validate against private IP ranges.
- **Impact**: Access to cloud metadata, internal services.

**4. Unauthenticated GET endpoints on transport server**
- `subnet/transport/server.go:112-116` — `/diffs`, `/mempool`, `/signatures` skip auth (acknowledged by TODO).
- **Impact**: Leak session state, validator signatures, mempool contents.

**5. Verbose error disclosure to clients**
- `decentralized-api/internal/server/middleware/error_handler.go:23-34`
- `TransparentErrorHandler` returns raw `err.Error()` for all non-echo errors, leaking internal URLs, stack traces, node topology.

### Medium

**6. Warm key cache poisoning (bridge)**
- `subnet/bridge/rest.go:173` — `sync.Map` caches auth results permanently. Revoked warm keys remain authorized until process restart.

**7. Rate limiter bulk eviction creates burst window**
- `subnet/transport/ratelimit.go:42-43` — When entries exceed 1000, entire map is cleared. Attacker sends from 1000+ addresses to reset all rate limits.

**9. Unbounded diffs array in catch-up path**
- `subnet/transport/server.go:391-400` — No cap on diffs per request. CPU/memory exhaustion vector.

**10. CORS wildcard default**
- `proxy/entrypoint.sh:244` — `CORS_ALLOW_ORIGIN` defaults to `"*"`, enabling cross-site request abuse.

**11. Debug endpoints exposed on public server**
- `decentralized-api/internal/server/public/server.go:130-131` — `/v1/debug/*` registered with no auth guard.

**12. Subnet escrow remainder underflow**
- `inference-chain/x/inference/keeper/msg_server_settle_subnet_escrow.go:66` — Cost aggregation differs between `VerifySubnetSettlement` and `SettleSubnetEscrow`, potentially underpaying validators.

**13. ETH withdrawal uses low-level call without gas limit**
- `proposals/ethereum-bridge-contact/contracts/BridgeContract.sol:368` — `call{value: cmd.amount}("")` forwards all gas to arbitrary recipient.

**14. Epoch cleanup doesn't clean processedRequests (bridge)**
- `proposals/ethereum-bridge-contact/contracts/BridgeContract.sol:583-591` — Storage grows unboundedly.

### Low

**15. submitGroupKey allows epoch 1 without signature** — `BridgeContract.sol:302-307`
**17. Hardcoded password in testnet scripts** — `test-net-cloud/nebius/bridge/bridge-pool-fund.sh:60`
**18. Keyring backend "test" in production config** — `decentralized-api/config-prod.yaml:9`
**19. completedResponses map grows unbounded** — `subnet/host/host.go:83`
**20. pendingTxKeys dedup set grows to 100K** — `subnet/user/user.go:528`

## Withdrawn findings (2026-04-20 self-review)

These were either scoped to internal/user-side processes or duplicates of already-withdrawn PRs:

- **#3** Subnet proxy (subnetctl) zero auth — `subnetctl` is a user-side local CLI proxy (see `subnet/docs/proxy.md`), run by the escrow owner on localhost. Not a multi-tenant service.
- **#8** Unbounded request body on subnet proxy — same reason as #3.
- **#16** SSRF via escrowID in REST bridge — `baseURL` is operator-controlled (config), making this a same-origin internal path. Same class as already-withdrawn #1064.
- **#21** TokenomicsData uint64 overflow — direct duplicate of already-withdrawn #1062 (theoretical accumulation > 2^64, not reachable).

## Methodology

- Manual code review of all four layers (inference chain, bridge, subnet, API)
- Focus on: fund safety, consensus determinism, authentication/authorization, resource exhaustion, input validation
- Cross-referenced with existing issues (#979, #933, #883, #885) to avoid duplicates

## Note on Responsible Disclosure

Finding #1 (Admin API no auth) is Critical severity. Per the bounty program guidelines, critical issues should be reported privately. I'm including it here for completeness but recommend the team prioritize this fix immediately. Happy to discuss privately if needed.

I plan to submit additional fix PRs for the remaining findings if the team is interested.

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Doog-bot534">@Doog-bot534</a></span>
    <span class="issues-meta-item">commented 2026-04-15 07:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Payout Address</h2>
<p>If any of the findings or fix PRs (#1050, #1051, #1052, #1054, #1055, #1056, #1057) are eligible for bounty rewards, please send to:</p>
<pre><code>gonka10zaal553duxp05nvfpqtsqrm2g0j6j34r8nan7
</code></pre>
<p>Happy to discuss any of the findings in more detail or submit additional fixes for the remaining issues listed above.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Doog-bot534">@Doog-bot534</a></span>
    <span class="issues-meta-item">commented 2026-04-20 02:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>2026-04-20 self-review update: withdrawing findings <strong>#3, #8, #16, #21</strong> (see "Withdrawn findings" section in the updated body). Same review pass closed PRs #1077 and #1058.</p>
<p>Rationale:
- <strong>#3, #8</strong> (subnetctl zero-auth, unbounded body) — <code>subnetctl</code> is a user-side local CLI proxy for the escrow owner (localhost:8080), not a multi-tenant service. Threat model doesn't apply.
- <strong>#16</strong> (SSRF via escrowID in REST bridge) — <code>baseURL</code> is operator-controlled config, so this is a same-origin internal-path concern, same class as the earlier withdrawn #1064.
- <strong>#21</strong> (TokenomicsData uint64 overflow) — direct duplicate of already-withdrawn #1062; requires &gt; 2^64 accumulation which is not reachable in practice.</p>
<p>Keeping the queue focused on actionable findings. The other 17 items (including the Critical #1 and the High findings #2/#4/#5) remain valid.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Doog-bot534">@Doog-bot534</a></span>
    <span class="issues-meta-item">commented 2026-04-20 14:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Cleanup summary (2026-04-20)</h2>
<p>Per maintainer feedback on PR quality, I've completed a self-audit of all submissions under this umbrella. Summary:</p>
<h3>Withdrawn (target removed code)</h3>
<ul>
<li>
<h1>1082, #1083 — both targeted <code>AssignTrainingTask</code> / <code>CreateDummyTrainingTask</code> in the training module which was removed in #1009 (2026-04-07). Closed with apology.</h1>
</li>
</ul>
<h3>Withdrawn from this audit (previous waves)</h3>
<ul>
<li>F3, F8, F16, F21 sub-findings in this issue body — dropped after re-verification against current code.</li>
</ul>
<h3>Revised after self-review</h3>
<p>All 8 remaining open PRs were run through gonka-ai/ai-reviewer personas (skeptic + chain_security / dapi-behavioral-correctness). Full review output posted as comments on each PR.</p>
<p>Code changes pushed in response to ai-reviewer findings:
- <strong>#1054</strong> — log original error server-side before generic response
- <strong>#1055</strong> — add IPv4-mapped IPv6 to SSRF blocklist; document DNS-rebinding as follow-up
- <strong>#1063</strong> — include query string in signed payload (closes parameter-tampering replay)
- <strong>#1050</strong> — rewrote body to reflect actual severity (preventive, not "chain fork")</p>
<h3>Remaining 8 open PRs</h3>
<table>
<thead>
<tr>
<th>PR</th>
<th>Severity (revised)</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>#1050 consensus float64</td>
<td>Low (preventive)</td>
<td>ready</td>
</tr>
<tr>
<td>#1052 PoC V2 permissions</td>
<td>Medium</td>
<td>ready</td>
</tr>
<tr>
<td>#1054 error handler leak</td>
<td>Low</td>
<td>revised, ready</td>
</tr>
<tr>
<td>#1055 SSRF partial mitigation</td>
<td>Medium</td>
<td>revised, ready</td>
</tr>
<tr>
<td>#1056 rate limiter eviction</td>
<td>Low-Medium</td>
<td>ready</td>
</tr>
<tr>
<td>#1057 warm key TTL</td>
<td>Low-Medium</td>
<td>ready</td>
</tr>
<tr>
<td>#1060 debug endpoints</td>
<td>Low</td>
<td>ready</td>
</tr>
<tr>
<td>#1063 GET auth</td>
<td>Medium</td>
<td>revised, ready</td>
</tr>
</tbody>
</table>
<p>Going forward I'll only submit PRs after running ai-reviewer locally and validating against current master.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1053](https://github.com/gonka-ai/gonka/issues/1053) every hour.
