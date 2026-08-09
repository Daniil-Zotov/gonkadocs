---
title: "#1229 — Request for phased DevShards creator allowlist access for local gateway MVP validation"
source: https://github.com/gonka-ai/gonka/issues/1229
issue_number: 1229
synced_at: 2026-08-09T23:51:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request for phased DevShards creator allowlist access for local gateway MVP validation
    <span class="issues-number">#1229</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/sspotanin">@sspotanin</a> opened 2026-05-22 16:08 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 23:22 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

I am building an OpenAI-compatible reliability gateway for Gonka-hosted models, starting with `moonshotai/Kimi-K2.6`.

The goal is to make Gonka-hosted models practically usable for developer and agentic engineering workflows, where reliability requirements are higher than for basic single-turn chat.

This request is for a phased DevShards creator allowlist process:

1. one creator address for local/pre-MVP validation;
2. limited-access beta endpoint after the local MVP is validated;
3. public broker request after the limited beta proves stable.

I am not requesting a public broker listing yet.

## Operator

Operator:
Sergei Potanin

Project status:
pre-MVP / local validation

Final project name and public domain:
TBD before public launch

Contact:
sspotanin@gmail.com

## Motivation

I would be happy to continue local gateway development without asking for public access. However, the current DevShards creator allowlist blocks validation of the gateway/operator path from a normal funded Gonka account.

I have tested the current public gateway/broker options available to me for this workflow. While they can be useful for simple prompts, I have not found one that is reliable enough yet for sustained agentic engineering sessions.

Agentic coding workflows stress the gateway layer much more heavily:

- long reasoning;
- streaming behavior;
- tool-call compatibility;
- continuation after output limits;
- retries and recovery;
- clear failure modes;
- long-running sessions without manual provider switching.

This is the reliability gap I want to work on.

Creating a public landing page, buying a domain, and launching a public endpoint before I can validate the core local MVP would be premature. I am therefore requesting a small, controlled allowlist entry first, so I can validate the DevShards creator/operator path locally.

When the local MVP works, I will move to a limited-access beta endpoint for closed testing. When that beta is stable, I will then submit a follow-up public broker listing request with a final name, endpoint, documented limits, and billing model.

## Requested Access

Please add one creator address to `devshard_escrow_params.allowed_creator_addresses` for local/pre-MVP validation:

```text
gonka17ag8defq5afygld2n6pln6y2xw8z9378jwpca6
```

This account is already funded above `devshard_escrow_params.min_amount` and has its on-chain pubkey published.

Initial scope:

- Kimi K2.6 only;
- low request volume;
- local/private validation only;
- no public broker listing initially;
- no public high-volume traffic;
- logs/results shared with maintainers if useful;
- fast rollback if maintainers observe any issue.

## Endpoint

Public endpoint:
not available yet

I can expose a limited-access endpoint for maintainers or closed beta testers after the local MVP validation succeeds.

## Billing Model

No public billing model is requested for this local validation phase.

For a later public broker request, I expect to provide a usage-backed billing model together with documented limits and abuse controls.

## Current Validation

I have already validated the basic account prerequisites:

- account funded above `devshard_escrow_params.min_amount`;
- on-chain pubkey published;
- public model discovery works.

Current direct requests from a normal funded account do not proceed to inference execution under the current DevShards setup, so I would like to validate the intended creator/operator path.

I can provide minimal reproduction logs privately or in a follow-up comment if useful.

## Review Request

Could someone from the DevShards / broker allowlist maintainers please review this request or point me to the preferred process?

I am happy to coordinate and adjust the validation scope, limits, or rollout process to match network policy.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 23:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @sspotanin!</p>
<p>On the process you asked about: allowlisting a <code>gonka1…</code> creator address is an on-chain governance decision. Addresses on <code>devshard_escrow_params.allowed_creator_addresses</code> are added through a governance vote — no single maintainer or operator adds one unilaterally.  To be clear, your actual ask (validating the creator/operator path locally) does require the allowlist; that's the part where you create and settle escrows yourself, and no managed service substitutes for it. So nothing below replaces this request.</p>
<p>That said, given the specific gap you're targeting (reliability for sustained agentic sessions), one community option worth being aware of in parallel is <strong>OpenBroker</strong> (run by Gonka Labs). https://github.com/gonka-ai/gonka/discussions/1363 It's a managed devshard platform that runs v1/v2 (and future versions) at production scale with full per-request and network observability, and it's explicitly used as a live testbed for exercising devshard versions under load. Two ways it might be useful while the governance request is reviewed:</p>
<ul>
<li><strong>As a stable reference endpoint</strong> to build and benchmark the OpenAI-compatible client side of your gateway against — streaming, tool-call compatibility, long sessions — so that work isn't blocked on allowlisting.</li>
<li><strong>As a production-scale baseline</strong> for the reliability behaviors you're measuring, since it surfaces real telemetry and failure modes rather than single-turn happy-path responses.</li>
</ul>
<p>OpenBroker is an <strong>independent third party</strong>, not part of the core protocol, and exactly the kind of existing option you said you've already evaluated — so treat it as a reference/benchmark, not as the answer to the reliability gap you're building toward. It's just a way to keep the client-side work moving in parallel with the allowlist governance process.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1229](https://github.com/gonka-ai/gonka/issues/1229) every hour.
