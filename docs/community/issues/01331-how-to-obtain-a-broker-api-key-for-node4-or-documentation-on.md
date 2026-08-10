---
title: "#1331 — How to obtain a broker API key for node4 (or documentation on the broker onboarding process)?"
source: https://github.com/gonka-ai/gonka/issues/1331
issue_number: 1331
synced_at: 2026-08-10T13:49:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    How to obtain a broker API key for node4 (or documentation on the broker onboarding process)?
    <span class="issues-number">#1331</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Puyre">@Puyre</a> opened 2026-06-10 15:34 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 23:29 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka core team & community,

## Context 

We previously opened an issue requesting inclusion of our address in
`devshard_escrow_params.allowed_creator_addresses` to run our own
devshard gateway. After discussing with the community, we concluded we
don't actually need to operate our own devshard — for our use case it's
enough to obtain a **broker API key** and send requests through the
public gateway (node4), the documented path for consuming inference
without running an allowlisted escrow creator.

That earlier issue has been closed in favor of this one.

## What we're trying to do

We're building an OpenAI-compatible inference gateway that uses Gonka as
its primary backend — a drop-in replacement for closed AI APIs
(developers change one `base_url` and keep their existing OpenAI SDK
code). Under the hood it routes to Gonka by default and falls back to a
stable provider (OpenRouter) when the network is unavailable, so end
users get Gonka-level cost savings without being exposed to current
uptime variance.

To do this we need programmatic inference access through a broker key.

## The actual question

We've confirmed the following behavior ourselves:

- A correctly signed request sent **directly to a participant node** returns
  `Transfer Agent not allowed` — which is expected behavior, since our
  wallet is not on the allowlist.
- The **same signed request sent to `https://node4.gonka.ai`** returns
  `{"error":{"message":"model \"...\" requires an API key"}}`.

Based on my own testing and on input from community members, I believe
there is some way to obtain an API key (a broker key) that would let us
send requests through this node.

Our questions:

1. How does one obtain a broker API key for node4 specifically (not a
   third-party USD-billed reseller)? Is there an application/onboarding
   process, and who administers it?
2. If there's no public process yet, could this be documented? The SDK
   READMEs and quickstart currently present a signed-wallet path that
   does not work against node4 without a broker key.

## On-chain identity (for reference)

- Account: `gonka15y6xg0ps5w0u4w3ttx557mf46v82ms8svcavy2`
- Funded above `devshard_escrow_params.min_amount`, on-chain pubkey
  published (secp256k1).

## Team and contact

- Contact: `andres@rogilabs.com`
- TG: `@puyre`

Thanks for reviewing.
Rogi AI
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 23:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @Puyre!</p>
<p>On the direct question (a broker API key for node4 specifically): there isn't a public self-serve onboarding process to point you to. node4 is the public gateway that was stood up during the early rollout — whitelisted and rate-limited, intended for demos and bootstrap testing rather than as a production backend. The handful of broker keys behind it were early access arrangements, not an open application flow, and that bootstrap directory isn't being actively expanded. So the <code>requires an API key</code> response you're seeing on node4 isn't something there's a documented "apply here" path to resolve — which is also why the signed-wallet SDK path doesn't work against it without one. The two paths that <em>are</em> governed and documented are: consume through an existing community broker, or operate your own allowlisted devshard gateway (on-chain governance allowlist).</p>
<p>For what you're actually building, the closest fit is a managed devshard endpoint. One community option is <strong>OpenBroker</strong> (run by Gonka Labs https://github.com/gonka-ai/gonka/discussions/1363): it gives you programmatic devshard access (v1, v2, and future versions) under a wallet that's already whitelisted to operate escrows, so you get the "just hit an endpoint and go" behavior of node4 but built for production rather than demos — no rate limits, no escrow lifecycle on your side, GNK billing with no markup (not a USD reseller), and public per-request/network observability.</p>
<p>It maps directly onto your fallback architecture (Gonka primary → OpenRouter fallback): just make OpenBroker the primary base_url. </p>
<p>OpenBroker is an <strong>independent third party</strong>, not part of the core protocol — pricing, models, limits, and data handling are set by the operator, so evaluate it on its own merits. If you later decide you do want to operate your own escrows after all, the on-chain allowlist route stays open.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1331](https://github.com/gonka-ai/gonka/issues/1331) every hour.
