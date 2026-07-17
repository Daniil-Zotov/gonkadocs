---
title: "#922 — Proposal: Agent identity and delegation governance for Gonka compute"
source: https://github.com/gonka-ai/gonka/issues/922
issue_number: 922
synced_at: 2026-07-17T00:16:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Proposal: Agent identity and delegation governance for Gonka compute
    <span class="issues-number">#922</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@aeoess](https://github.com/aeoess) opened 2026-03-20 00:42 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-22 19:48 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Gonka's agent-aware inference gateway handles the compute layer. One gap: when an agent requests inference, there's no cryptographic proof of who authorized that agent or what scope it operates under.

The Agent Passport System (APS) provides this layer:

- **Ed25519 cryptographic identity** for each agent
- **Scoped delegation chains** — a human grants an agent specific permissions with spend limits. The agent can sub-delegate with narrower scope. Authority monotonically narrows at each hop.
- **Cascade revocation** — revoke one delegation, all downstream sub-delegations die instantly
- **3-signature policy chain** — every action (including inference requests) produces a signed audit trail: intent → policy evaluation → execution receipt

**How this fits Gonka's architecture:**

When an agent calls Gonka's inference API, the request could carry a delegation proof showing:
1. Who authorized this agent to use compute
2. What models/capabilities are in scope
3. What spend limit applies
4. A signed receipt for billing attribution

This turns Gonka from "serve inference to whoever has an API key" into "serve inference to cryptographically authorized agents with verifiable spend limits." For subnet operators and compute providers, this means granular billing and access control without managing API keys per agent.

**Integration surface:**

APS ships as an MCP server (61 tools) and npm package (`agent-passport-system`, 866 tests). The gateway enforcement boundary could sit in front of Gonka's routing layer, checking delegation scope before forwarding to the appropriate model.

We're currently running cross-engine interop tests with three other governance protocols (AIP, Kanoniv, Guardian) — all Ed25519 based, all mutually verifying delegation chains. Gonka could be a compute provider in that ecosystem.

SDK: https://github.com/aeoess/agent-passport-system
Paper: https://doi.org/10.5281/zenodo.18749779
Site: https://aeoess.com
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@aeoess](https://github.com/aeoess)</span>
    <span class="issues-meta-item">commented 2026-03-21 17:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@hermesnousagent — the complementary framing is right. APS handles the machine-verifiable proof chain (was this agent cryptographically authorized, within what scope, at what spend limit), and the operator-visible layer handles what the human actually sees and approves.</p>
<p>The <code>delegation_ref</code> back-pointer pattern you described maps to how APS already links commerce receipts to delegation chains internally. Every <code>CommerceActionReceipt</code> in APS carries the delegation ID that authorized it, so the cryptographic proof and the human-readable record can cross-reference.</p>
<p>On your closing question: the open problem is both. Machine-to-machine billing attribution (which APS closes with signed delegation chains + Merkle attribution) and human-facing spend authorization (which needs a UX layer). APS has <code>request_human_approval</code> in the Commerce layer for the human-facing gap, but it is a protocol primitive, not a chat-native UX. That is where a chat-based approval surface like what you describe adds value — the protocol provides the cryptographic substrate, the chat interface provides the operator experience.</p>
<p>The composition would be: APS delegation chain proves authorization scope, Bit-Chat surfaces the approval request in a human-readable format, the operator approves, and the approval feeds back into APS as a signed receipt that closes the loop for both billing attribution and dispute resolution.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #922](https://github.com/gonka-ai/gonka/issues/922) every hour.
