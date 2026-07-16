---
title: "#1319 — Self-serve (no-broker) flow is documented as working but returns 401 "model requires an API key" — I want to spend my own GNK directly"
source: https://github.com/gonka-ai/gonka/issues/1319
issue_number: 1319
synced_at: 2026-07-16T21:28:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Self-serve (no-broker) flow is documented as working but returns 401 "model requires an API key" — I want to spend my own GNK directly
    <span class="issues-number">#1319</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@dufok](https://github.com/dufok) opened 2026-06-07 22:20 UTC</span>
    <span class="issues-meta-item">7 comments</span>
    <span class="issues-meta-item">Updated 2026-07-03 15:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

Several official surfaces document a **self-serve, no-broker** end-to-end inference
flow (own GNK account + private key → signed request → completion) as if it works.
In practice, a funded, on-chain-registered account gets
`401 {"error":{"message":"model \"...\" requires an API key"}}` for **every** model
on the network. So the documented self-serve path is not actually end-to-end without
a broker.

This is the follow-up to #876 (closed with "use a community broker"). The runtime
behavior matches that answer — but the docs and official SDKs still present the
broker-less path as working, which is the actual bug here: **docs vs. reality.**

### Motivation — I want to use my own GNK, as designed

The whole reason to choose Gonka over a centralized API is to **pay with my own GNK
directly**, the way the network was designed: decentralized, no third party custodying
my funds or gating my access. Routing through a community broker — who holds the GNK,
sets the price, and can rate-limit or cut me off — defeats that purpose. I already hold
GNK and have a registered account; I do **not** want to buy access from a broker, I want
to spend my own coins directly. Please make the self-serve path actually work (option (a)
below).

### Where the no-broker path is presented as working

1. **`gonka-ai/gonka` README** — directs developers to *"create a user account and submit
   an inference request using the `inferenced` CLI tool"* via the Quickstart. No mention
   that a broker API key is required to actually get a completion.

2. **`gonka-ai/gonka-openai` (official SDK)** — minimal usage example constructs the client
   from a **private key** and calls `chat.completions.create`, framed as *"Use exactly like
   the original OpenAI client"*. The OpenAI `api_key` is documented as just `"mock-api-key"`
   ("OpenAI requires any key"). No broker, no caveat:
   ```python
   from gonka_openai import GonkaOpenAI
   client = GonkaOpenAI(
       api_key="mock-api-key",
       gonka_private_key="0x1234...",
       source_url="https://...",
   )
   client.chat.completions.create(
       model="Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
       messages=[{"role": "user", "content": "Hello!"}],
   )
   ```

3. **`gonkalabs/opengnk` README** — a complete self-serve quickstart (download CLI →
   create account → export key → fund via faucet → request) with a curl example that
   *"just works"*. No warning about 401 / broker requirement.

### Actual behavior (reproduction)

Funded, on-chain-registered account:
- address: `gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt`
- balance: `295137045500 ngonka` (~295 GNK), confirmed via
  `http://node1.gonka.ai:8000/chain-api/cosmos/bank/v1beta1/balances/<addr>`

Run the official-pattern self-serve proxy (`gonkalabs/opengnk`) with that key:
```
GONKA_ADDRESS=gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
GONKA_SOURCE_URL=http://node1.gonka.ai:8000
```
Proxy starts fine, registers the wallet, discovers endpoints, signs upstream requests:
```
msg="endpoints discovered" count=3 whitelisted=7
msg="upstream request" method=POST url=https://node4.gonka.ai/v1/chat/completions
     endpoint_addr=gonka1kx9... wallet=gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
```
Request:
```bash
curl http://localhost:8091/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-235B-A22B-Instruct-2507-FP8",
       "messages":[{"role":"user","content":"Hello!"}]}'
```
Response (same for **all** models — `Qwen3-235B-A22B`, `moonshotai/Kimi-K2.6`,
`MiniMaxAI/MiniMax-M2.7`):
```json
{"error":{"message":"model \"Qwen/Qwen3-235B-A22B-Instruct-2507-FP8\" requires an API key"}}
```
A signed `GET /v1/models` returns `count=0`; the unauthenticated catalog lists all three.
The gate is enforced **node-side, per model** — correct signing + funded account do not
bypass it.

### Expected

Preferred — **(a)** a funded, registered self-serve account can run inference on the public
models directly with its own GNK (make the documented broker-less flow actually work
end-to-end).

Otherwise — **(b)** the docs and official SDK READMEs clearly state that a **broker API key
is mandatory**, and the self-serve `gonka-openai` / `inferenced` / OpenGNK examples are
removed or explicitly flagged as non-functional without a broker. Right now a developer
following the official SDK README hits a dead end with no hint that a broker is required.

### Environment

- `gonkalabs/opengnk` @ main (Go proxy, secp256k1 signing, `CGO_ENABLED=0`)
- source node `http://node1.gonka.ai:8000`, gateway `https://node4.gonka.ai`
- models in catalog: `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8`,
  `moonshotai/Kimi-K2.6`, `MiniMaxAI/MiniMax-M2.7`

Related: #876

</div>

---

## 💬 Comments (7)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@JamesJi79](https://github.com/JamesJi79)</span>
    <span class="issues-meta-item">commented 2026-06-08 04:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hello! I took a close look at your issue. The 401 "model requires an API key" is a node-side API key gate, not a signing/auth issue. Your proxy correctly signs requests and your wallet is funded (~295 GNK confirmed on-chain), but the inference nodes reject direct requests that lack a valid broker API key.</p>
<p><strong>What is happening technically:</strong>
1. opengnk proxy signs and forwards correctly
2. Wallet is funded and on-chain registered
3. Node gate checks for broker API key instead of wallet balance
4. Unauthenticated /v1/models shows models but authenticated returns count=0</p>
<p><strong>Two paths:</strong>
- Option A (self-serve fix): Gonka team needs to update node-side validation to accept self-serve wallets. Previous issue #876 suggests broker-required is intentional.
- Option B (workaround): I can help set up a personal broker proxy that gets its own API key, acting as your personal broker without third-party GNK custody.</p>
<p>I do paid consulting on blockchain/proxy integration. If interested in Option B, I can quote a fixed price. Reach me at james@greentoken.center</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-08 12:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for taking a look and confirming the diagnosis.</p>
<p>To be clear about what I'm after: I'm specifically looking for an <strong>official fix (Option A)</strong> — node-side validation that accepts a funded, on-chain-registered self-serve wallet, so I can spend my own GNK directly.</p>
<p>A paid or personal-broker setup (Option B) doesn't fit my goal. The entire reason I chose Gonka is to pay with my own GNK directly, decentralized, with no third party custodying funds, gating access, or charging a fee in between. A "personal broker" still introduces a key/middleman and a cost, which defeats that purpose.</p>
<p>So I'll wait for the maintainers' response on whether the self-serve path can be supported (or, failing that, for the docs/SDK READMEs to clearly state a broker is mandatory). Appreciate the help, but I'm not looking for paid consulting here.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-08 13:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I dug into the source to pin down exactly where the gate lives. It turns out to be <strong>two layers</strong>, and only one of them is actually blocking self-serve:</p>
<h3>Layer 1 — gateway model-access policy (the <code>requires an API key</code> message)</h3>
<p><code>devshard/cmd/devshardctl/gateway.go → modelAccessError()</code>. Each model has an <code>AccessMode</code> configured by <strong>whoever runs the gateway</strong>:</p>
<ul>
<li><code>open</code> → anyone allowed</li>
<li><code>apikey</code> → must present a key from <em>that gateway's</em> store (<code>requestHasAPIKey</code>)</li>
<li><code>admin-only</code> → admin key</li>
</ul>
<p>The public <code>node4.gonka.ai</code> is itself a devshard gateway whose operator set the models to <code>apikey</code> — which is exactly why a community broker (a gateway with <code>apikey</code> mode + its own billing) is the documented path. <strong>This layer is operator config, not a protocol gate</strong> — if I run my own gateway I can set the models to <code>open</code>. So Layer 1 is not the real blocker.</p>
<h3>Layer 2 — the actual blocker: on-chain devshard escrow allow-list</h3>
<p>For my own gateway to pay for inference with my own GNK, it has to open an on-chain devshard escrow. The handler gates on the creator address:</p>
<pre><code class="language-go">// inference-chain/x/inference/keeper/msg_server_create_devshard_escrow.go
if err := k.CheckPermission(goCtx, msg, EscrowAllowListPermission); err != nil {
    return nil, err
}
</code></pre>
<pre><code class="language-go">// inference-chain/x/inference/keeper/params.go
func (k Keeper) IsAllowedEscrowCreator(ctx, address) bool {
    ep := k.GetDevshardEscrowParams(ctx)
    if len(ep.AllowedCreatorAddresses) == 0 { return true } // empty = open to all
    for _, a := range ep.AllowedCreatorAddresses {
        if a == address { return true }
    }
    return false
}
</code></pre>
<p><code>AllowedCreatorAddresses</code> is non-empty (populated via chain upgrades — e.g. <code>app/upgrades/v0_2_13</code> batch-added several <code>gonka1…</code> addresses), my address is not on it, so <code>CreateDevshardEscrow</code> returns <code>ErrNotAllowedEscrowCreator</code>. This is a consensus param, so I can't self-add it.</p>
<h3>The ask</h3>
<p>This makes the fix concrete. <strong>Please add my funded, on-chain-registered address to <code>DevshardEscrowParams.AllowedCreatorAddresses</code> in the next upgrade</strong> — exactly as was done in <code>v0_2_13</code>:</p>
<pre><code>gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt   (~295 GNK on-chain)
</code></pre>
<p>Then I can run my own devshard gateway and pay for inference directly with my own GNK — the decentralized, no-broker, no-middleman flow the network is designed for.</p>
<p>Separately, would you consider <strong>relaxing the escrow allow-list</strong> so any sufficiently-funded address can open a devshard escrow? The existing <code>MinAmount</code> / <code>MaxAmount</code> and <code>MaxEscrowsPerEpoch</code> params already provide anti-spam / rate-limiting, so the hard allow-list seems to add little beyond gatekeeping permissionless self-serve. Happy to open a PR for this if it would be welcome.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-23 23:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @dufok! </p>
<p>The "spend my own GNK, no middleman" flow you want is exactly run your own devshard gateway — and the one thing standing between you and it is having your creator address on that allowlist. There's no hidden self-serve-without-a-gateway path that is withheld; direct signed requests to a participant node returning Transfer Agent not allowed and node4 returning requires an API key are both expected, and the honest end-to-end self-serve path is "own allowlisted gateway → your own escrow → your own GNK."</p>
<p>On the docs-vs-reality point — you're right, and it's fair. The signed-wallet, broker-less examples in some SDK/READMEs (gonka-openai, opengnk, older inferenced quickstart) present an end-to-end path that doesn't actually complete against node4 today without either a key or your own allowlisted gateway. The developer quickstart has since been restructured around the two paths that genuinely work — consume via a community broker, or run your own allowlisted gateway — but the SDK READMEs you cited still need to be reconciled with that.</p>
<p>On adding gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt to the allowlist. This is the right request, but it's an on-chain governance decision — the allowlist is a consensus param changed only through a governance vote (as in the v0_2_13 batch), not something any maintainer or operator adds unilaterally (treat inclusion and timeline as governance-dependent, not guaranteed).</p>
<p>Separately, and only for completeness — not as the answer to your request: Gonka Labs recently posted https://github.com/gonka-ai/gonka/discussions/1363, a managed "devshards as a service" gateway under an already-whitelisted wallet. It's the middleman model you've explicitly declined, so I'm not proposing it as a fix — linking it only because it's directly relevant background to the allowlist discussion and shows what the operator path looks like at production scale.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-29 23:48 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks @tcharchian — that's a clear and fair answer, and it actually points me at exactly what I want to do.</p>
<p>To be concrete: <strong>I want to run and operate my own devshard gateway</strong>, on my own hardware (a server I already own, so infra cost is zero for me), and pay for inference with my own GNK. I'm not looking for a broker to consume — I'm happy to <em>be</em> the allowlisted operator for my own usage. The only thing standing in the way is having my creator address on <code>AllowedCreatorAddresses</code>.</p>
<p>I looked at the current on-chain param: the allowlist has ~17 operator addresses, and they were added in batches via upgrades (e.g. <code>v0_2_13</code>). So my question is about <strong>process</strong>, not a one-off favor:</p>
<ol>
<li><strong>How does an operator get added to <code>AllowedCreatorAddresses</code>?</strong> Is there an application / vetting path to be included in a future upgrade batch (the way the existing 17 were added), or is the only route a standalone governance proposal submitted by the applicant?</li>
<li>If there are <strong>operator criteria</strong> (uptime, stake, hardware, identity, min GNK, etc.), what are they? I'd like to meet them.</li>
<li>If a standalone governance proposal is the only way, is that realistic for a small independent operator, or is batch-inclusion-by-the-team the normal path?</li>
</ol>
<p>My address (funded, on-chain registered, ready to operate):</p>
<pre><code>gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
</code></pre>
<p>Happy to follow whatever the established process is — just want to know which door to walk through. Thanks!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-07-03 00:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @dufok!</p>
<p>On how the allowlist changes: every modification of <code>DevshardEscrowParams.AllowedCreatorAddresses</code> is an on-chain governance action. There's no maintainer-side "add operator" switch. It's either a standalone governance proposal that updates the param, voted on-chain, or inclusion in a governance-approved chain upgrade batch — which is how the current operators were seeded in <code>v0_2_13</code>. (the initial set was added during the early rollout as part of upgrade handlers, as a bootstrap step to get the first operators online.)  </p>
<p>There isn't a published operator-vetting checklist I can point you to (as of now).  </p>
<p>As for which door to walk through: the documented way to register intent is what you've already done here — a public request with your operator identity, contact, creator address, and intended models. That puts it in front of maintainers and governance participants. A standalone proposal is a legitimate route for an independent operator (whether it passes is up to voters).</p>
<p>Additional correction on OpenBroker, since it touches your "no fee in between" point. It isn't a USD reseller with a margin: it settles in GNK and deducts its ledger 1-to-1 with actual escrow cost, at cost with no markup, and there's no enrollment or approval wait. So on price and time-to-start it's effectively a pass-through you could use today.  </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-07-03 15:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks a lot @tcharchian — this fully answers it, and I appreciate the patience and the honest docs-vs-reality acknowledgement. The OpenBroker clarification (GNK-settled, 1:1 at cost, no markup, no approval wait) is exactly what I needed — I'll start there. Cheers.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1319](https://github.com/gonka-ai/gonka/issues/1319) every hour.
