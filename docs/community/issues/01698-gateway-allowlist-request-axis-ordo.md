---
title: "#1698 — Gateway allowlist request: Axis Ordo"
source: https://github.com/gonka-ai/gonka/issues/1698
issue_number: 1698
synced_at: 2026-09-22T10:05:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request: Axis Ordo
    <span class="issues-number">#1698</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/leonidkachuliak-eng">@leonidkachuliak-eng</a> opened 2026-09-01 19:41 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-21 18:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Operator:** Axis Ordo — multi-tenant SaaS platform for AI agents,
operated by Soft Dev Oy (Finland). https://platform.axis-ordo.com

**Contact:** @leonidkachuliak-eng · support@softdev.fi

**Creator address:** gonka12qnvu86dh3ts9t94l2cq3hyhtfh6ty6dsft9f6

**Models:** MiniMaxAI/MiniMax-M2.7, Kimi-K2.6,
DeepSeek-V4-Flash-0731, GLM-5.2-FP8

**Use case:**
We run a multi-tenant agent platform. Each tenant's agents call LLMs
through our own provider gateway, which already integrates OpenAI,
Anthropic, OpenRouter and xAI behind one OpenAI-compatible layer.
We want to add Gonka as a first-class provider available to our tenants.

We are requesting a self-hosted devshard because our billing is
per-run and per-tenant: every inference must be attributed to an
individual tenant run and settled inside our own ledger, with cost
of goods tracked per agent. Routing through a shared broker gives us
one aggregate bill and no per-run attribution, which we cannot resell
from.

We do not mine and do not run inference hardware. Escrow will be
funded from a dedicated address used for nothing else.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-01 23:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @leonidkachuliak-eng  </p>
<p>Allowlisting is an on-chain governance decision, so this registers intent but timing/inclusion aren't guaranteed. Before waiting on that: per-run attribution doesn't actually need a self-hosted gateway. You already attribute per-tenant for OpenAI, Anthropic, OpenRouter and xAI — all aggregate-billed too. It's done on your side by counting tokens per request, not by the provider. So Gonka works the same way through OpenBroker (https://github.com/gonka-ai/gonka/discussions/1363): OpenAI-compatible, no markup (1-to-1 with escrow cost), no governance wait — attribute per tenant in your own ledger and resell, live within minutes. Since this is a resale product: brokers that surface the network ("powered by Gonka") are an easier yes for hosts and help the ecosystem — just an observation, not a requirement. If you try it and something genuinely doesn't fit, say so here.  </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/leonidkachuliak-eng">@leonidkachuliak-eng</a></span>
    <span class="issues-meta-item">commented 2026-09-21 07:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi Tania,</p>
<p>Hope you're doing well! Could you please tell me how I might get in touch
with Daniil and David? I'd love to get to know them and explore the
prospects for cooperation.</p>
<p>Thank you so much!
Leonid Kachuliak, CEO, Soft Dev Oy</p>
<p>ср, 2 сент. 2026 г. в 01:00, Tania Charchian <strong><em>@</em></strong>.***&gt;:</p>
<blockquote>
<p><em>tcharchian</em> left a comment (gonka-ai/gonka#1698)
<a href="https://github.com/gonka-ai/gonka/issues/1698#issuecomment-5501585728">https://github.com/gonka-ai/gonka/issues/1698#issuecomment-5501585728</a></p>
<p>Hi @leonidkachuliak-eng <a href="https://github.com/leonidkachuliak-eng">https://github.com/leonidkachuliak-eng</a></p>
<p>Allowlisting is an on-chain governance decision, so this registers intent
but timing/inclusion aren't guaranteed. Before waiting on that: per-run
attribution doesn't actually need a self-hosted gateway. You already
attribute per-tenant for OpenAI, Anthropic, OpenRouter and xAI — all
aggregate-billed too. It's done on your side by counting tokens per
request, not by the provider. So Gonka works the same way through
OpenBroker (#1363 <a href="https://github.com/gonka-ai/gonka/discussions/1363">https://github.com/gonka-ai/gonka/discussions/1363</a>):
OpenAI-compatible, no markup (1-to-1 with escrow cost), no governance wait
— attribute per tenant in your own ledger and resell, live within minutes.
Since this is a resale product: brokers that surface the network ("powered
by Gonka") are an easier yes for hosts and help the ecosystem — just an
observation, not a requirement. If you try it and something genuinely
doesn't fit, say so here.</p>
<p>—
Reply to this email directly, view it on GitHub
<a href="https://github.com/gonka-ai/gonka/issues/1698?email_source=notifications&amp;email_token=BYQ3OK2KQBOLTCLER3F6AMT5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-5501585728">https://github.com/gonka-ai/gonka/issues/1698?email_source=notifications&amp;email_token=BYQ3OK2KQBOLTCLER3F6AMT5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-5501585728</a>,
or unsubscribe
<a href="https://github.com/notifications/unsubscribe-auth/BYQ3OKY6E554FQNX7QDHT5T5M5IKVAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TKMZRGYYDMMRQHA42C5QC">https://github.com/notifications/unsubscribe-auth/BYQ3OKY6E554FQNX7QDHT5T5M5IKVAVCNFSNUABFKJSXA33TNF2G64TZHM4DENZQGYYTAOJSHNEXG43VMU5TKMZRGYYDMMRQHA42C5QC</a>
.
Triage notifications, keep track of coding agent tasks and review pull
requests on the go with GitHub Mobile for iOS
<a href="https://github.com/notifications/mobile/ios/BYQ3OKYWDJYXNDYGEE4ZQHL5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y">https://github.com/notifications/mobile/ios/BYQ3OKYWDJYXNDYGEE4ZQHL5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJKTGN5XXIZLSL5UW64Y</a>
and Android
<a href="https://github.com/notifications/mobile/android/BYQ3OKYWSLZE24QCU3UGCJT5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI">https://github.com/notifications/mobile/android/BYQ3OKYWSLZE24QCU3UGCJT5M5IKVA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTKNJQGE2TQNJXGI4KM4TFMFZW63VHNVSW45DJN5XKKZLWMVXHJLTGN5XXIZLSL5QW4ZDSN5UWI</a>.
Download it today!
You are receiving this because you were mentioned.Message ID:
<strong><em>@</em></strong>.***&gt;
</p>
</blockquote>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-21 18:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @leonidkachuliak-eng!  Could you share a bit more about your question or the kind of collaboration you have in mind? If you have any technical ideas, experiments, or implementations around Gonka, feel free to share them here. We’d be happy to take a look, and other members of the community may also want to jump into the discussion, share feedback, or help answer your questions. You can also always reach David and Daniil via public email, hi @ libermans . co
But posting here can be a great way to get some early feedback, support, and validation from the community as well.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1698](https://github.com/gonka-ai/gonka/issues/1698) every hour.
