---
title: "#1319 — Self-serve (no-broker) flow is documented as working but returns 401 "model requires an API key" — I want to spend my own GNK directly"
source: https://github.com/gonka-ai/gonka/issues/1319
issue_number: 1319
synced_at: 2026-07-07T04:27:57Z
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

<div class="issues-content">
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
    Hello! I took a close look at your issue. The 401 "model requires an API key" is a node-side API key gate, not a signing/auth issue. Your proxy correctly signs requests and your wallet is funded (~295 GNK confirmed on-chain), but the inference nodes reject direct requests that lack a valid broker API key.

**What is happening technically:**
1. opengnk proxy signs and forwards correctly
2. Wallet is funded and on-chain registered
3. Node gate checks for broker API key instead of wallet balance
4. Unauthenticated /v1/models shows models but authenticated returns count=0

**Two paths:**
- Option A (self-serve fix): Gonka team needs to update node-side validation to accept self-serve wallets. Previous issue #876 suggests broker-required is intentional.
- Option B (workaround): I can help set up a personal broker proxy that gets its own API key, acting as your personal broker without third-party GNK custody.

I do paid consulting on blockchain/proxy integration. If interested in Option B, I can quote a fixed price. Reach me at james@greentoken.center
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-08 12:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks for taking a look and confirming the diagnosis.

To be clear about what I'm after: I'm specifically looking for an **official fix (Option A)** — node-side validation that accepts a funded, on-chain-registered self-serve wallet, so I can spend my own GNK directly.

A paid or personal-broker setup (Option B) doesn't fit my goal. The entire reason I chose Gonka is to pay with my own GNK directly, decentralized, with no third party custodying funds, gating access, or charging a fee in between. A "personal broker" still introduces a key/middleman and a cost, which defeats that purpose.

So I'll wait for the maintainers' response on whether the self-serve path can be supported (or, failing that, for the docs/SDK READMEs to clearly state a broker is mandatory). Appreciate the help, but I'm not looking for paid consulting here.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-08 13:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    I dug into the source to pin down exactly where the gate lives. It turns out to be **two layers**, and only one of them is actually blocking self-serve:

### Layer 1 — gateway model-access policy (the `requires an API key` message)

`devshard/cmd/devshardctl/gateway.go → modelAccessError()`. Each model has an `AccessMode` configured by **whoever runs the gateway**:

- `open` → anyone allowed
- `apikey` → must present a key from *that gateway's* store (`requestHasAPIKey`)
- `admin-only` → admin key

The public `node4.gonka.ai` is itself a devshard gateway whose operator set the models to `apikey` — which is exactly why a community broker (a gateway with `apikey` mode + its own billing) is the documented path. **This layer is operator config, not a protocol gate** — if I run my own gateway I can set the models to `open`. So Layer 1 is not the real blocker.

### Layer 2 — the actual blocker: on-chain devshard escrow allow-list

For my own gateway to pay for inference with my own GNK, it has to open an on-chain devshard escrow. The handler gates on the creator address:

```go
// inference-chain/x/inference/keeper/msg_server_create_devshard_escrow.go
if err := k.CheckPermission(goCtx, msg, EscrowAllowListPermission); err != nil {
    return nil, err
}
```

```go
// inference-chain/x/inference/keeper/params.go
func (k Keeper) IsAllowedEscrowCreator(ctx, address) bool {
    ep := k.GetDevshardEscrowParams(ctx)
    if len(ep.AllowedCreatorAddresses) == 0 { return true } // empty = open to all
    for _, a := range ep.AllowedCreatorAddresses {
        if a == address { return true }
    }
    return false
}
```

`AllowedCreatorAddresses` is non-empty (populated via chain upgrades — e.g. `app/upgrades/v0_2_13` batch-added several `gonka1…` addresses), my address is not on it, so `CreateDevshardEscrow` returns `ErrNotAllowedEscrowCreator`. This is a consensus param, so I can't self-add it.

### The ask

This makes the fix concrete. **Please add my funded, on-chain-registered address to `DevshardEscrowParams.AllowedCreatorAddresses` in the next upgrade** — exactly as was done in `v0_2_13`:

```
gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt   (~295 GNK on-chain)
```

Then I can run my own devshard gateway and pay for inference directly with my own GNK — the decentralized, no-broker, no-middleman flow the network is designed for.

Separately, would you consider **relaxing the escrow allow-list** so any sufficiently-funded address can open a devshard escrow? The existing `MinAmount` / `MaxAmount` and `MaxEscrowsPerEpoch` params already provide anti-spam / rate-limiting, so the hard allow-list seems to add little beyond gatekeeping permissionless self-serve. Happy to open a PR for this if it would be welcome.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-23 23:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Hi @dufok! 

The "spend my own GNK, no middleman" flow you want is exactly run your own devshard gateway — and the one thing standing between you and it is having your creator address on that allowlist. There's no hidden self-serve-without-a-gateway path that is withheld; direct signed requests to a participant node returning Transfer Agent not allowed and node4 returning requires an API key are both expected, and the honest end-to-end self-serve path is "own allowlisted gateway → your own escrow → your own GNK."

On the docs-vs-reality point — you're right, and it's fair. The signed-wallet, broker-less examples in some SDK/READMEs (gonka-openai, opengnk, older inferenced quickstart) present an end-to-end path that doesn't actually complete against node4 today without either a key or your own allowlisted gateway. The developer quickstart has since been restructured around the two paths that genuinely work — consume via a community broker, or run your own allowlisted gateway — but the SDK READMEs you cited still need to be reconciled with that.

On adding gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt to the allowlist. This is the right request, but it's an on-chain governance decision — the allowlist is a consensus param changed only through a governance vote (as in the v0_2_13 batch), not something any maintainer or operator adds unilaterally (treat inclusion and timeline as governance-dependent, not guaranteed).

Separately, and only for completeness — not as the answer to your request: Gonka Labs recently posted https://github.com/gonka-ai/gonka/discussions/1363, a managed "devshards as a service" gateway under an already-whitelisted wallet. It's the middleman model you've explicitly declined, so I'm not proposing it as a fix — linking it only because it's directly relevant background to the allowlist discussion and shows what the operator path looks like at production scale.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-06-29 23:48 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks @tcharchian — that's a clear and fair answer, and it actually points me at exactly what I want to do.

To be concrete: **I want to run and operate my own devshard gateway**, on my own hardware (a server I already own, so infra cost is zero for me), and pay for inference with my own GNK. I'm not looking for a broker to consume — I'm happy to *be* the allowlisted operator for my own usage. The only thing standing in the way is having my creator address on `AllowedCreatorAddresses`.

I looked at the current on-chain param: the allowlist has ~17 operator addresses, and they were added in batches via upgrades (e.g. `v0_2_13`). So my question is about **process**, not a one-off favor:

1. **How does an operator get added to `AllowedCreatorAddresses`?** Is there an application / vetting path to be included in a future upgrade batch (the way the existing 17 were added), or is the only route a standalone governance proposal submitted by the applicant?
2. If there are **operator criteria** (uptime, stake, hardware, identity, min GNK, etc.), what are they? I'd like to meet them.
3. If a standalone governance proposal is the only way, is that realistic for a small independent operator, or is batch-inclusion-by-the-team the normal path?

My address (funded, on-chain registered, ready to operate):

```
gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt
```

Happy to follow whatever the established process is — just want to know which door to walk through. Thanks!

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-07-03 00:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Hi @dufok!

On how the allowlist changes: every modification of `DevshardEscrowParams.AllowedCreatorAddresses` is an on-chain governance action. There's no maintainer-side "add operator" switch. It's either a standalone governance proposal that updates the param, voted on-chain, or inclusion in a governance-approved chain upgrade batch — which is how the current operators were seeded in `v0_2_13`. (the initial set was added during the early rollout as part of upgrade handlers, as a bootstrap step to get the first operators online.)  

There isn't a published operator-vetting checklist I can point you to (as of now).  

As for which door to walk through: the documented way to register intent is what you've already done here — a public request with your operator identity, contact, creator address, and intended models. That puts it in front of maintainers and governance participants. A standalone proposal is a legitimate route for an independent operator (whether it passes is up to voters).

Additional correction on OpenBroker, since it touches your "no fee in between" point. It isn't a USD reseller with a margin: it settles in GNK and deducts its ledger 1-to-1 with actual escrow cost, at cost with no markup, and there's no enrollment or approval wait. So on price and time-to-start it's effectively a pass-through you could use today.  
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@dufok](https://github.com/dufok)</span>
    <span class="issues-meta-item">commented 2026-07-03 15:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks a lot @tcharchian — this fully answers it, and I appreciate the patience and the honest docs-vs-reality acknowledgement. The OpenBroker clarification (GNK-settled, 1:1 at cost, no markup, no approval wait) is exactly what I needed — I'll start there. Cheers.

  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1319](https://github.com/gonka-ai/gonka/issues/1319) every hour.
