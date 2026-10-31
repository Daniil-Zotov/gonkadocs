---
title: "#2190 — Gateway allowlist request: Patrick Baumgartner"
source: https://github.com/gonka-ai/gonka/issues/2190
issue_number: 2190
synced_at: 2026-10-31T18:38:11Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway allowlist request: Patrick Baumgartner
    <span class="issues-number">#2190</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/patbaumgartner">@patbaumgartner</a> opened 2026-10-30 17:53 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-30 18:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hello Gonka team,

I would like to request allowlisting for a personal, self-hosted inference gateway.

This gateway will be used exclusively for my own development and tooling work. It will not be operated as a public broker, and I do not intend to resell API access.

### Creator address

`gonka1ypnfllakjvwztu24zvtaswggsk5wja7dt5vgqv`

### Operator / contact

- Operator: Patrick Baumgartner
- GitHub: @patbaumgartner
- Site: https://patbaumgartner.com

### Intended use

- Personal / solo-use inference gateway
- AI-assisted software development
- OpenAI-compatible API for local coding tools and assistants
- Private, non-commercial usage
- No resale of Gonka inference, no third-party customers
- Endpoint is published over HTTPS at `gonka.baumgartner.sg` behind a reverse proxy, but requests still require a per-key API credential I issue to myself

### Environment

- Self-hosted gateway, gateway-only deployment (no chain node, no ML node)
- Docker (`libermans/gonka-devshard-proxy`), gateway container only
- Host: Synology DS918+ NAS, DSM 7.x, Docker 24.0.2, x86_64
- Chain access via public mainnet REST/RPC (`node3.gonka.ai`)

### Models

I am primarily interested in:

- `MiniMaxAI/MiniMax-M2.7`
- `deepseek-ai/DeepSeek-V4-Flash-0731`
- `moonshotai/Kimi-K2.6`
- `zai-org/GLM-5.3-Flash`

Please add the creator address above to `devshard_escrow_params.allowed_creator_addresses` for personal inference usage.

I have verified the address is currently not on the allowlist and have not funded the wallet yet, since escrow creation cannot succeed until approval.

Thank you.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/patbaumgartner">@patbaumgartner</a></span>
    <span class="issues-meta-item">commented 2026-10-30 18:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the clarifications in #1624 and #1824 — understood that the allowlist is governance-only and that this issue records intent rather than acting as a queue.</p>
<p>Given that, I won't hold the setup open waiting on it: I'll use OpenBroker for actual inference in the meantime. The self-hosted gateway stays deployed and healthy against <code>gonka1ypnfllakjvwztu24zvtaswggsk5wja7dt5vgqv</code>, so if governance ever adds this address it can be activated immediately.</p>
<p>Closing for now — happy to reopen or file a fresh request if the situation changes. Thanks for the details along the way.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2190](https://github.com/gonka-ai/gonka/issues/2190) every hour.
